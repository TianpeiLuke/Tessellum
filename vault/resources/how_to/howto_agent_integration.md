---
tags:
  - resource
  - how_to
  - agent_integration
  - mcp
  - composer
keywords:
  - invoke Tessellum skills
  - MCP server
  - Claude Code
  - Composer pipeline
  - agent harness
topics:
  - Agent Integration
  - MCP
  - Composer Runtime
language: markdown
date of note: 2026-05-11
status: active
building_block: procedure
bb_schema_version: 1
---

# How To: Invoke Tessellum Skills from an Agent

Tessellum's 13 skill canonicals are designed to be invoked by AI agents — directly via the Python API, via the Composer pipeline runtime, or via an MCP server. This guide covers all three paths.

## Three invocation paths

| Path | When to use | Setup |
|---|---|---|
| **MCP server** | Claude Desktop / IDE / any MCP-compatible host | `pip install tessellum[mcp]`; `tessellum mcp serve` |
| **Composer pipeline** | One-shot programmatic dispatch with a sidecar's structured prompts | `pip install tessellum[agent]`; `tessellum composer run <skill>` |
| **Python API** | Embedding Tessellum's runtime into your own code | `pip install tessellum`; `from tessellum.<module> import ...` |

Choose by *who's invoking*:

- **A user in Claude Desktop** → MCP server
- **A script that composes Tessellum into a larger workflow** → Composer pipeline OR Python API
- **A custom agent harness** → MCP server (cleanest tool interface) or Python API (no SDK overhead)

## Path 1: MCP server

The MCP server exposes Tessellum's runtime APIs as MCP tools so any MCP-compatible host (Claude Desktop, etc.) can invoke them.

### Install + start

```bash
pip install tessellum[mcp]
tessellum mcp serve
# → stdio MCP server. Add to Claude Desktop config:
#   {"mcpServers": {"tessellum": {"command": "tessellum", "args": ["mcp", "serve"]}}}
```

### Tools exposed (v0.0.59)

| Tool | What it does |
|---|---|
| `tessellum_search` | Hybrid retrieval (BM25 + dense + graph) over the vault |
| `tessellum_format_check` | Validate notes against TESS-001..005 |
| `tessellum_bb_audit` | BBGraph telemetry — node + edge counts, untyped + unrealised edges |
| `tessellum_fz_traverse` | Walk a Folgezettel trail (ancestors / descendants / siblings) |
| `tessellum_capture` | Create a new typed note from a template |
| `tessellum_list_skills` | Enumerate available skill canonicals |
| `tessellum_get_skill` | Return a skill's canonical body so the calling agent can apply the procedure itself |

The server is **deterministic** — no LLM call on the server side. The runtime tools wrap Python APIs; the `get_skill` tool returns canonical text the calling agent applies in its own context.

### Two-tier interaction model

Most agents will use MCP in two ways during one session:

1. **Get the procedure** via `tessellum_get_skill` (returns the canonical body).
2. **Apply the procedure** in the agent's own LLM context, calling out to deterministic tools (`tessellum_search`, etc.) at the relevant steps.

Example for the DKS cycle:

```
agent → mcp.tessellum_get_skill(skill_name="tessellum_dks_cycle")
      ← canonical_body (the markdown procedure)
agent → applies the 7-component procedure step-by-step in its own context
agent → mcp.tessellum_search(query="warrant in toulmin") at step 2
      ← top hits (substrate-grounding for argument A)
agent → ... continues through steps 3-7 ...
```

The MCP server doesn't run the DKS cycle itself — that needs an LLM, which the calling agent supplies.

## Path 2: Composer pipeline

The Composer pipeline runtime is Tessellum's structured-prompt execution engine. Each skill canonical has a paired `*.pipeline.yaml` sidecar that declares the prompt for each step.

### Install + invoke

```bash
pip install tessellum[agent]   # adds anthropic SDK for the LLM backend
tessellum composer compile vault/resources/skills/skill_tessellum_dks_cycle.md
# → validates the canonical + sidecar pair

tessellum composer run vault/resources/skills/skill_tessellum_dks_cycle.md \
    --leaves leaves.jsonl \
    --backend anthropic
# → runs the pipeline; each step's prompt → LLM → validated output
```

The leaves JSONL contains the per-cycle input (observation summary, warrants, etc.). Output is per-step JSON + materialised notes.

### When to prefer Composer over MCP

- **Deterministic dispatch.** Composer is invoked by a script; MCP is invoked by a user chatting with an agent. If you want reproducible runs (e.g., a CI job that exercises the DKS cycle on every PR), Composer is the cleaner path.
- **Trace persistence.** Composer writes per-step trace JSON under `--runs-dir`; the MCP server doesn't.
- **No-LLM steps benefit.** Composer's `materializer: deterministic_no_llm` lets a sidecar skip LLM calls on steps that don't need them — useful for the aggregate / land steps of meta-DKS.

## Path 3: Python API

For embedding Tessellum into a larger Python program:

```python
from tessellum.dks import DKSRunner, DKSObservation, DKSWarrant
from tessellum.composer import AnthropicBackend

runner = DKSRunner(
    observations=(DKSObservation(folgezettel="1", summary="..."),),
    backend=AnthropicBackend(),
)
result = runner.run()
for cycle in result.cycles:
    print(cycle.surviving_argument_fzs, cycle.rule_revisions)
```

Top-level modules:

| Module | What it does |
|---|---|
| `tessellum.bb` | BB ontology — `BBType`, `BB_SCHEMA`, `BBGraph` |
| `tessellum.dks` | DKS runtime — `DKSCycle`, `DKSRunner`, `MetaCycle` |
| `tessellum.dks.dung` | Dung grounded labelling (Phase 10) |
| `tessellum.composer` | Pipeline executor + LLM backends |
| `tessellum.retrieval` | `hybrid_search`, `bm25_search`, `dense_search`, etc. |
| `tessellum.indexer` | `build`, `Database` |
| `tessellum.format` | `validate`, `parse_note` |
| `tessellum.capture` | `capture`, `REGISTRY` |

Read [`repo_tessellum`](../../areas/code_repos/repo_tessellum.md) for the full module decomposition.

## Authoring your own skill

Once you've used the existing skills, you'll probably want to author one. Run:

```bash
tessellum capture skill my_new_skill
# → scaffolds skill_my_new_skill.md (canonical) + skill_my_new_skill.pipeline.yaml (sidecar)
```

Fill the canonical's H2 sections (per [`howto_note_format`](howto_note_format.md)), populate the sidecar's `pipeline:` array, validate via:

```bash
tessellum composer compile vault/resources/skills/skill_my_new_skill.md
```

Then list it in [`entry_skill_catalog`](../../0_entry_points/entry_skill_catalog.md) + add to the seed manifest at `src/tessellum/data/_seed_manifest.py`.

## Choosing between MCP, Composer, and Python API

A simple decision rule:

```
Is the invoker a user chatting with an agent?
├── Yes → MCP server (`tessellum mcp serve` + host config)
└── No → Is the invocation programmatic?
        ├── Yes, with structured prompts via sidecars → Composer pipeline
        └── Yes, calling individual functions → Python API
```

All three paths work simultaneously — pick per use case; they share the same underlying skill canonicals + runtime.

## Related Notes

- [`howto_first_vault`](howto_first_vault.md) — install + initial vault setup (prerequisite)
- [`howto_note_format`](howto_note_format.md) — the YAML frontmatter spec your skill canonicals must satisfy
- [`entry_skill_catalog`](../../0_entry_points/entry_skill_catalog.md) — the 13 skills you can invoke

## See Also

- `tessellum.mcp.server` — MCP server source
- `tessellum.composer` — pipeline executor source
- [`term_dialectic_knowledge_system`](../term_dictionary/term_dialectic_knowledge_system.md) — the most complex multi-step skill
