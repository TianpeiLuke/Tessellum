"""Tessellum MCP server — 13 tools exposing the runtime + skill canonicals.

The server registers its tools via the MCP Python SDK's decorator API
(``@server.list_tools()``, ``@server.call_tool()``) and runs over the
standard stdio transport. Build the ``Server`` instance with
:func:`build_server`; run it via :func:`run_stdio` (called by
``tessellum mcp serve``).

Tool inventory:

1. ``tessellum_search`` — hybrid BM25 + dense retrieval fused by RRF
2. ``tessellum_format_check`` — TESS-001..005 validators against a note
3. ``tessellum_bb_audit`` — corpus BBGraph telemetry (node + edge counts,
   untyped edges, unrealised schema edges)
4. ``tessellum_fz_traverse`` — walk a Folgezettel trail
   (ancestors / descendants / siblings)
5. ``tessellum_capture`` — create a new typed note from a template
6. ``tessellum_get_skill`` — return a skill canonical's body so the
   calling agent can apply the procedure itself
7. ``tessellum_list_skills`` — enumerate available skill canonicals
8. ``tessellum_submit_job`` — durably admit one inbox source
9. ``tessellum_get_job`` — inspect one job and its event history
10. ``tessellum_list_jobs`` — list durable runtime jobs
11. ``tessellum_cancel_job`` — request cooperative cancellation
12. ``tessellum_retry_job`` — retry a cancelled or dead-letter job
13. ``tessellum_dks_query`` — invoke the registered ``dks_query``
    capability and return its three-way decision

The runtime tools are deterministic Python-API wrappers; no LLM call
on the server side. The skill-canonical tools let the calling agent
execute the procedure in its own context — the canonical is the
prompt; the agent supplies the LLM.

``tessellum_dks_query`` is a **thin caller** of the registered capability,
not a parallel implementation of it: it looks the factory up on the
runtime capability registry and drives it through ``DKSExecutor``, which
returns a candidate transaction and never writes. If nothing has
registered ``dks_query`` the tool says so and stops — there is no
fallback path, because a second way to answer a query is a second set of
epistemic rules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_server():
    """Construct the Tessellum MCP server instance with all tools registered.

    Imports the ``mcp`` SDK lazily so the optional dependency is only
    required when the server is actually constructed (not when the
    package is imported). Raises ``ImportError`` if ``[mcp]`` extras
    aren't installed.
    """
    try:
        from mcp.server import Server
        from mcp import types
    except ImportError as e:
        raise ImportError(
            "tessellum.mcp requires the [mcp] extras: "
            "`pip install tessellum[mcp]`"
        ) from e

    server = Server("tessellum")

    # ── Tool descriptors ──────────────────────────────────────────────────
    tool_specs: list[dict[str, Any]] = [
        {
            "name": "tessellum_search",
            "description": (
                "Hybrid BM25 + dense RRF retrieval over the vault. "
                "Returns note ids/names, fused scores, and per-signal ranks."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {"type": "string", "description": "Natural-language query"},
                    "k": {"type": "integer", "default": 10, "description": "Top-K hits"},
                    "db_path": {
                        "type": "string",
                        "default": "data/tessellum.db",
                        "description": "Index DB path (relative to cwd)",
                    },
                },
            },
        },
        {
            "name": "tessellum_format_check",
            "description": (
                "Validate one note (or a directory) against TESS-001..005 + "
                "YAML frontmatter + link rules. Returns the list of issues."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["path"],
                "properties": {
                    "path": {"type": "string", "description": "Note file or directory"},
                },
            },
        },
        {
            "name": "tessellum_bb_audit",
            "description": (
                "Corpus BBGraph telemetry: node counts by BB type, edge "
                "counts by epistemic-edge label, untyped corpus edges, "
                "unrealised schema edges. Pure read of the index DB."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "db_path": {
                        "type": "string",
                        "default": "data/tessellum.db",
                        "description": "Index DB path",
                    },
                },
            },
        },
        {
            "name": "tessellum_fz_traverse",
            "description": (
                "Walk a Folgezettel trail from a starting note. Returns "
                "ancestors / descendants / siblings as ordered FZ IDs."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["fz", "direction"],
                "properties": {
                    "fz": {"type": "string", "description": "Starting FZ ID (e.g., '2a1')"},
                    "direction": {
                        "type": "string",
                        "enum": ["ancestors", "descendants", "siblings"],
                        "description": "Traversal direction",
                    },
                    "db_path": {
                        "type": "string",
                        "default": "data/tessellum.db",
                        "description": "Index DB path",
                    },
                },
            },
        },
        {
            "name": "tessellum_capture",
            "description": (
                "Create a new typed note from a template. Returns the "
                "created file path. Optional destination + filename_prefix "
                "overrides let the caller override the flavor's defaults."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["flavor", "slug"],
                "properties": {
                    "flavor": {
                        "type": "string",
                        "description": "Template flavor (concept / argument / model / procedure / ...)",
                    },
                    "slug": {
                        "type": "string",
                        "description": "Note identifier (lowercase letters/digits/underscores)",
                    },
                    "vault_root": {
                        "type": "string",
                        "default": "vault",
                        "description": "Vault root directory",
                    },
                    "destination": {
                        "type": ["string", "null"],
                        "description": "Override REGISTRY default destination (e.g., 'areas/tools')",
                    },
                    "filename_prefix": {
                        "type": ["string", "null"],
                        "description": "Override REGISTRY default filename prefix (e.g., 'tool_')",
                    },
                },
            },
        },
        {
            "name": "tessellum_list_skills",
            "description": (
                "Enumerate available skill canonicals from the seed vault. "
                "Returns each skill's name + H1 title."
            ),
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "tessellum_get_skill",
            "description": (
                "Return a skill canonical's body as text. The calling "
                "agent applies the procedure in its own LLM context — "
                "the server does not invoke an LLM."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["skill_name"],
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "description": "Skill stem (e.g., 'tessellum_dks_cycle')",
                    },
                },
            },
        },
        {
            "name": "tessellum_submit_job",
            "description": "Durably admit one file already inside a Tessellum inbox lane.",
            "inputSchema": {
                "type": "object",
                "required": ["path"],
                "properties": {
                    "path": {"type": "string"},
                    "root": {"type": "string", "default": "."},
                },
            },
        },
        {
            "name": "tessellum_get_job",
            "description": "Return durable runtime state and event history for one job.",
            "inputSchema": {
                "type": "object",
                "required": ["job_id"],
                "properties": {
                    "job_id": {"type": "string"},
                    "root": {"type": "string", "default": "."},
                },
            },
        },
        {
            "name": "tessellum_list_jobs",
            "description": "List durable automatic-runtime jobs.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "root": {"type": "string", "default": "."},
                    "state": {"type": ["string", "null"]},
                    "limit": {"type": "integer", "default": 100},
                },
            },
        },
        {
            "name": "tessellum_cancel_job",
            "description": "Request cooperative cancellation of a durable job.",
            "inputSchema": {
                "type": "object",
                "required": ["job_id"],
                "properties": {
                    "job_id": {"type": "string"},
                    "root": {"type": "string", "default": "."},
                },
            },
        },
        {
            "name": "tessellum_retry_job",
            "description": (
                "Create a linked retry generation for a cancelled or "
                "dead-letter job."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["job_id"],
                "properties": {
                    "job_id": {"type": "string"},
                    "root": {"type": "string", "default": "."},
                },
            },
        },
        {
            "name": "tessellum_dks_query",
            "description": (
                "Invoke the registered dks_query capability on one question. "
                "Returns a three-way decision: an ANSWER with its support "
                "chain and locator, a surfaced CONFLICT with both chains, or "
                "an explicit ABSTENTION with its reason. Proposes effects; "
                "writes nothing. Requires a registered dks_query capability."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {"type": "string", "description": "The question"},
                    "mention": {
                        "type": "string",
                        "default": "",
                        "description": "Entity surface form to resolve (step 1)",
                    },
                    "subject_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Resolved subjects for the Tier-A read",
                    },
                    "note_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Extra note ids for the memory read",
                    },
                    "entity_type": {"type": ["string", "null"]},
                    "k": {"type": "integer", "default": 20},
                },
            },
        },
    ]

    @server.list_tools()
    async def list_tools():
        return [
            types.Tool(
                name=spec["name"],
                description=spec["description"],
                inputSchema=spec["inputSchema"],
            )
            for spec in tool_specs
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]):
        try:
            result = _dispatch(name, arguments)
        except Exception as e:  # noqa: BLE001 — surface error as MCP content
            result = {"error": f"{type(e).__name__}: {e}"}
        return [
            types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str),
            )
        ]

    return server


def _dispatch(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Route a tool call to its Python implementation."""
    if name == "tessellum_search":
        return _tool_search(**arguments)
    if name == "tessellum_format_check":
        return _tool_format_check(**arguments)
    if name == "tessellum_bb_audit":
        return _tool_bb_audit(**arguments)
    if name == "tessellum_fz_traverse":
        return _tool_fz_traverse(**arguments)
    if name == "tessellum_capture":
        return _tool_capture(**arguments)
    if name == "tessellum_list_skills":
        return _tool_list_skills(**arguments)
    if name == "tessellum_get_skill":
        return _tool_get_skill(**arguments)
    if name == "tessellum_submit_job":
        return _tool_submit_job(**arguments)
    if name == "tessellum_get_job":
        return _tool_get_job(**arguments)
    if name == "tessellum_list_jobs":
        return _tool_list_jobs(**arguments)
    if name == "tessellum_cancel_job":
        return _tool_cancel_job(**arguments)
    if name == "tessellum_retry_job":
        return _tool_retry_job(**arguments)
    if name == "tessellum_dks_query":
        return _tool_dks_query(**arguments)
    raise ValueError(f"unknown tool: {name}")


# ── Tool implementations ────────────────────────────────────────────────────


def _tool_search(query: str, k: int = 10, db_path: str = "data/tessellum.db") -> dict:
    from tessellum.retrieval import hybrid_search

    db = Path(db_path).expanduser().resolve()
    if not db.is_file():
        return {"error": f"Index DB not found at {db}. Run `tessellum index build` first."}
    hits = hybrid_search(db, query, k=k)
    return {
        "query": query,
        "k": k,
        "hits": [
            {
                "note_id": h.note_id,
                "note_name": h.note_name,
                "score": h.score,
                "bm25_rank": h.bm25_rank,
                "dense_rank": h.dense_rank,
            }
            for h in hits
        ],
    }


def _tool_format_check(path: str) -> dict:
    from tessellum.format import validate

    p = Path(path).expanduser().resolve()
    if p.is_dir():
        files = sorted(p.rglob("*.md"))
    elif p.is_file():
        files = [p]
    else:
        return {"error": f"path not found: {path}"}
    out = []
    for f in files:
        issues = validate(f)
        if issues:
            out.append(
                {
                    "path": str(f),
                    "issues": [
                        {
                            "severity": i.severity.value,
                            "rule_id": i.rule_id,
                            "field": i.field,
                            "message": i.message,
                        }
                        for i in issues
                    ],
                }
            )
    return {
        "files_checked": len(files),
        "files_with_issues": len(out),
        "issues": out,
    }


def _tool_bb_audit(db_path: str = "data/tessellum.db") -> dict:
    from tessellum.bb import BBGraph

    db = Path(db_path).expanduser().resolve()
    if not db.is_file():
        return {"error": f"Index DB not found at {db}."}
    graph = BBGraph.from_db(db)
    return {
        "db_path": str(db),
        "node_count": len(graph),
        "edges_by_label": graph.edges_by_type(),
        "untyped_edge_count": len(graph.untyped_edges()),
        "unrealised_schema_edges": [
            {
                "source": e.source.value,
                "target": e.target.value,
                "label": e.label,
            }
            for e in graph.unrealised_schema_edges()
        ],
    }


def _tool_fz_traverse(
    fz: str,
    direction: str,
    db_path: str = "data/tessellum.db",
) -> dict:
    from tessellum.bb import BBGraph

    db = Path(db_path).expanduser().resolve()
    if not db.is_file():
        return {"error": f"Index DB not found at {db}."}
    graph = BBGraph.from_db(db)
    # Find the node at this FZ
    start = next(
        (n for n in graph if getattr(n, "folgezettel", "") == fz),
        None,
    )
    if start is None:
        return {"error": f"No note found at FZ {fz!r}."}
    # Naive traversal: walk parent / children via folgezettel prefix
    results: list[dict] = []
    for n in graph:
        n_fz = getattr(n, "folgezettel", "") or ""
        if not n_fz or n_fz == fz:
            continue
        if direction == "ancestors":
            if fz.startswith(n_fz) and fz != n_fz:
                results.append({"fz": n_fz, "note_id": n.note_id})
        elif direction == "descendants":
            if n_fz.startswith(fz) and n_fz != fz:
                results.append({"fz": n_fz, "note_id": n.note_id})
        elif direction == "siblings":
            parent_fz = getattr(start, "folgezettel_parent", "") or ""
            sibling_parent = getattr(n, "folgezettel_parent", "") or ""
            if parent_fz and sibling_parent == parent_fz:
                results.append({"fz": n_fz, "note_id": n.note_id})
    results.sort(key=lambda r: r["fz"])
    return {
        "starting_fz": fz,
        "direction": direction,
        "results": results,
    }


def _tool_capture(
    flavor: str,
    slug: str,
    vault_root: str = "vault",
    destination: str | None = None,
    filename_prefix: str | None = None,
) -> dict:
    import uuid as _uuid

    from tessellum.capture import capture
    from tessellum.runtime.executor import VaultEffectJournal

    root = Path(vault_root).expanduser().resolve()
    if not root.is_dir():
        return {"error": f"Vault root not found at {root}."}
    # A5.2 (FZ 20k9c1a1a1b7c2k1a): the MCP capture was the last UNJOURNALED
    # direct write into the vault-of-record. capture() is create-only
    # (FileExistsError on collision; force is never passed here), so the
    # journal's role is the uniform effect record + crash recovery: pre-image
    # recorded before the write, journal ACCEPTED right after success — a
    # crash in between leaves an open journal recover_pending can roll back,
    # the same semantics every runtime vault write already has.
    journal = VaultEffectJournal(
        root,
        effect_guard=None,
        journal_dir=root / "runs" / "mcp-effects" / _uuid.uuid4().hex[:12],
    )
    try:
        result = capture(
            flavor=flavor,
            slug=slug,
            vault_root=root,
            destination=destination,
            filename_prefix=filename_prefix,
            effect_recorder=journal.record,
        )
    except Exception:
        journal.rollback()
        raise
    journal.accept()
    return {
        "path": str(result.path),
        "flavor": result.flavor,
        "slug": result.slug,
        "sidecar_path": str(result.sidecar_path) if result.sidecar_path else None,
    }


def _runtime(root: str):
    from tessellum.runtime import RuntimePaths, RuntimeStore

    paths = RuntimePaths.discover(root)
    paths.ensure_runtime_dirs()
    return paths, RuntimeStore.open(paths.db)


def _job_dict(job) -> dict[str, Any]:
    return {
        "job_id": job.job_id,
        "state": job.state.value,
        "lane": job.request.lane,
        "source_event_id": job.request.source_event_id,
        "capability": job.capability,
        "attempts": job.attempts,
        "commit_attempts": job.commit_attempts,
        "cancel_requested": job.cancel_requested,
        "last_error": job.last_error,
        "result_path": job.result_path,
        "supersedes_job_id": job.supersedes_job_id,
    }


def _tool_submit_job(path: str, root: str = ".") -> dict:
    from tessellum.runtime import admit_path

    paths, store = _runtime(root)
    job, created = admit_path(path, paths=paths, store=store)
    return {**_job_dict(job), "created": created}


def _tool_get_job(job_id: str, root: str = ".") -> dict:
    _paths, store = _runtime(root)
    job = store.get(job_id)
    if job is None:
        return {"error": f"job not found: {job_id}"}
    return {
        **_job_dict(job),
        "events": [
            {
                "sequence": event.sequence,
                "event_type": event.event_type,
                "at": event.at,
                "detail": event.detail,
            }
            for event in store.events(job_id)
        ],
    }


def _tool_list_jobs(
    root: str = ".",
    state: str | None = None,
    limit: int = 100,
) -> dict:
    from tessellum.runtime.models import JobState

    _paths, store = _runtime(root)
    states = None if state is None else [JobState(state)]
    return {"jobs": [_job_dict(job) for job in store.list(states=states, limit=limit)]}


def _tool_cancel_job(job_id: str, root: str = ".") -> dict:
    _paths, store = _runtime(root)
    return _job_dict(store.request_cancel(job_id))


def _tool_retry_job(job_id: str, root: str = ".") -> dict:
    _paths, store = _runtime(root)
    return _job_dict(store.retry_terminal(job_id))


def _chain_dict(chain) -> dict[str, Any]:
    """One chain — the head claim plus the located steps that license it."""
    return {
        "role": chain.role,
        "claim_id": chain.claim_id,
        "text": chain.text,
        "note_id": chain.note_id,
        "locator": chain.locator,
        "status": chain.status,
        "steps": [
            {
                "op": step.op,
                "claim_id": step.claim_id,
                "text": step.text,
                "note_id": step.note_id,
                "locator": step.locator,
                "status": step.status,
                "evidence_locator": step.evidence_locator,
            }
            for step in chain.steps
        ],
    }


def _tool_dks_query(
    query: str,
    mention: str = "",
    subject_ids: list[str] | None = None,
    note_ids: list[str] | None = None,
    entity_type: str | None = None,
    k: int = 20,
) -> dict:
    """Drive the registered ``dks_query`` capability. A thin caller; never writes.

    The capability is looked up on the runtime registry and invoked through
    ``DKSExecutor``, which returns a CANDIDATE transaction — the effects are
    proposals for the commit tail, and this tool renders them rather than
    applying them. An unregistered capability is reported, not worked around.
    """
    from tessellum.dks.capability import DKSExecutor
    from tessellum.dks.query_protocol import QueryRequest, QueryResult
    from tessellum.runtime.routing import (
        DKS_QUERY,
        CapabilityNotRegistered,
        get_capability_factory,
    )

    try:
        factory = get_capability_factory(DKS_QUERY)
    except CapabilityNotRegistered as e:
        return {
            "error": str(e),
            "hint": (
                "register one with tessellum.runtime.routing.register_dks_query"
                "(factory); nothing registers it by default and there is no "
                "fallback answer path"
            ),
        }
    request = QueryRequest(
        query=query,
        mention=mention,
        subject_ids=tuple(subject_ids or ()),
        note_ids=tuple(note_ids or ()),
        entity_type=entity_type,
        k=k,
    )
    # The episode pins its own snapshot lazily, so the digest is known only after
    # the invocation; it travels on the result, and a caller holding the memory
    # boundary uses EpisodeMemory.pinned_candidate to fill the candidate's field.
    candidate = DKSExecutor(factory()).execute(request)
    envelope = candidate.result
    out: dict[str, Any] = {
        "query": query,
        "capability": DKS_QUERY,
        "status": envelope.status,
        "qualifier": envelope.qualifier,
        "promotion_eligibility": envelope.promotion_eligibility,
        "replay_token": envelope.replay_token,
        "diagnostics": list(envelope.diagnostics),
        "proposed_effects": [
            {"kind": effect.kind, "bb_role": effect.bb_role}
            for effect in envelope.effects
        ],
        "wrote_anything": False,
    }
    result = envelope.payload
    if not isinstance(result, QueryResult):
        return out
    out.update(
        {
            "outcome": result.outcome,
            "relation": result.relation,
            "grounded": result.grounded,
            "answer": _chain_dict(result.answer) if result.answer else None,
            "conflict": [_chain_dict(chain) for chain in result.conflict],
            "abstention_reason": result.abstention_reason,
            "statuses": dict(result.statuses),
            "memory": {
                "cache_hit": result.memory.cache_hit,
                "claims": result.memory.claims,
                "relations": result.memory.relations,
                "short_circuited": result.memory.short_circuited,
            },
            "refutations": [
                {
                    "claim_id": record.claim_id,
                    "candidate_claim_id": record.candidate_claim_id,
                    "judged": record.judged,
                    "incompatible": record.incompatible,
                    "direction": record.direction,
                    "produced_edge": record.produced_edge,
                }
                for record in result.refutations
            ],
            "model_budget": {
                "relation_namings": result.budget.relation_namings,
                "claim_reads": result.budget.claim_reads,
                "refutation_judgements": result.budget.refutation_judgements,
                "refutation_truncated": result.budget.refutation_truncated,
                "total": result.budget.total,
            },
            "base_snapshot_id": result.base_snapshot_id,
            "grounding_notice": result.grounding.notice if result.grounding else "",
        }
    )
    return out


def _skills_dir() -> Path | None:
    """Locate the skills directory in the wheel-shipped vault.

    Mirrors :func:`tessellum.data.templates_dir` but for skills.
    Returns ``None`` if no skills directory is found.
    """
    # Wheel-installed: under tessellum/data/seed_vault/resources/skills/
    from tessellum import data as data_pkg

    pkg_root = Path(data_pkg.__file__).parent
    candidate = pkg_root / "seed_vault" / "resources" / "skills"
    if candidate.is_dir():
        return candidate
    # Editable install / repo dev: vault/resources/skills/ relative to repo root
    repo_root = Path(__file__).resolve().parents[3]
    candidate = repo_root / "vault" / "resources" / "skills"
    if candidate.is_dir():
        return candidate
    return None


def _tool_list_skills() -> dict:
    skills_dir = _skills_dir()
    if skills_dir is None:
        return {"error": "skills directory not found"}
    skills = []
    for p in sorted(skills_dir.glob("skill_tessellum_*.md")):
        # Read frontmatter for description
        text = p.read_text(encoding="utf-8")
        # Extract H1 line as the short description
        title = ""
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        # Single-file skills: a skill "has a pipeline" iff its step sections
        # carry contract blocks (compile to ≥1 step).
        step_count = 0
        try:
            from tessellum.composer import compile_skill

            step_count = len(compile_skill(p).steps)
        except Exception:
            step_count = 0
        skills.append(
            {
                "name": p.stem,
                "title": title,
                "pipeline_step_count": step_count,
            }
        )
    return {"skills_dir": str(skills_dir), "skills": skills, "count": len(skills)}


def _tool_get_skill(skill_name: str) -> dict:
    skills_dir = _skills_dir()
    if skills_dir is None:
        return {"error": "skills directory not found"}
    # Accept both 'tessellum_dks_cycle' and 'skill_tessellum_dks_cycle' forms
    stem = skill_name if skill_name.startswith("skill_") else f"skill_{skill_name}"
    path = skills_dir / f"{stem}.md"
    if not path.is_file():
        return {"error": f"skill not found: {skill_name} (looked for {path.name})"}
    # Single-file skills: the typed contract lives in per-section ```yaml```
    # blocks inside the canonical, not a separate sidecar. Surface the compiled
    # step count so callers can see whether the skill has Composer dispatch.
    step_count: int | None = None
    try:
        from tessellum.composer import compile_skill

        step_count = len(compile_skill(path).steps)
    except Exception:
        step_count = None
    return {
        "skill_name": skill_name,
        "canonical_path": str(path),
        "canonical_body": path.read_text(encoding="utf-8"),
        "pipeline_step_count": step_count,
    }


# ── Stdio runner ────────────────────────────────────────────────────────────


def run_stdio() -> int:
    """Run the Tessellum MCP server over stdio transport.

    Called by ``tessellum mcp serve``. Blocks until the client closes
    the connection (typical lifecycle for Claude Desktop and similar
    MCP hosts).
    """
    import asyncio

    try:
        from mcp.server.stdio import stdio_server
    except ImportError as e:
        print(
            "tessellum mcp: missing the [mcp] extras. "
            "Install with: pip install tessellum[mcp]"
        )
        print(f"  ({e})")
        return 2

    server = build_server()

    async def _main() -> None:
        async with stdio_server() as (read, write):
            await server.run(
                read,
                write,
                server.create_initialization_options(),
            )

    asyncio.run(_main())
    return 0
