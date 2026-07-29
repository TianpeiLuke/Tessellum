"""A5.3 (FZ 20k9c1a1a1b7c2k1a): the ``AgentMemory`` facade — a NAMING pass.

The vault-as-memory design's four tiers all exist as shipped seams; what was
missing was the one name that lets each be designed against the others
instead of reinvented (the retrospective's principle 4 forbade building this
before the tiers stabilized — A0–A4 have). This module adds NO behavior:
every method is a thin delegation to the seam that already owns the tier.

- WORKING    → the durable artifact store (``page_plan_artifacts`` /
               ``{{artifact.X}}`` deref) — run-scoped, GC'd at commit (A4.2).
- EPISODIC   → the run-dir journals (attempts, heartbeats, checkpoints,
               events) — append-only, at the grain the control flow acts on.
- SEMANTIC   → the vault index (hybrid retrieval over the notes DB).
- PROCEDURAL → the compiled skills (``compile_skill``).
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tessellum.composer.compiler import CompiledPipeline, compile_skill
from tessellum.composer.digestion import page_plan_artifacts


@dataclass(frozen=True)
class AgentMemory:
    """The four-tier memory facade. Construct once per run scope.

    Attributes:
        artifacts_dir: The durable working store root (``<job>/artifacts``).
        runs_dir: The episodic root (``<job>/runs``).
        index_db: The vault index for semantic search (``None`` → semantic
            queries return empty, the bootstrap posture).
        skills_dir: The procedural canonicals' directory.
    """

    artifacts_dir: Path
    runs_dir: Path
    index_db: Path | None
    skills_dir: Path

    # ── WORKING ──────────────────────────────────────────────────────────
    def working_put(self, plan_doc: dict[str, Any]) -> dict[str, Any]:
        """Page the doc's heavy fields to the durable store; returns the store
        (refs for paged keys) — delegates to :func:`page_plan_artifacts`."""
        return page_plan_artifacts(plan_doc, self.artifacts_dir)

    def working_get(self, key: str) -> str | None:
        """Read one of-record artifact's text, or ``None`` if absent."""
        target = self.artifacts_dir / key
        return target.read_text(encoding="utf-8") if target.is_file() else None

    # ── EPISODIC ─────────────────────────────────────────────────────────
    def episodic_append(self, stream: str, record: dict[str, Any]) -> None:
        """Append one timestamped record to a named episodic stream
        (``<runs_dir>/<stream>.jsonl``) — fail-soft, like every journal."""
        try:
            self.runs_dir.mkdir(parents=True, exist_ok=True)
            with (self.runs_dir / f"{stream}.jsonl").open(
                "a", encoding="utf-8"
            ) as fh:
                fh.write(json.dumps({"at": time.time(), **record}) + "\n")
        except Exception:
            pass

    def episodic_read(self, stream: str) -> list[dict[str, Any]]:
        path = self.runs_dir / f"{stream}.jsonl"
        if not path.is_file():
            return []
        out = []
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
        return out

    # ── SEMANTIC ─────────────────────────────────────────────────────────
    def semantic_search(self, query: str, *, limit: int = 8) -> list[dict[str, Any]]:
        """Hybrid retrieval over the vault index; empty in the bootstrap
        posture (no index yet) — the CP5 lesson, applied as a default."""
        if self.index_db is None or not Path(self.index_db).is_file():
            return []
        from tessellum.retrieval.hybrid import hybrid_search

        try:
            hits = hybrid_search(self.index_db, query, k=limit)
            return [
                h if isinstance(h, dict) else dict(getattr(h, "__dict__", {}) or h._asdict())
                for h in hits
            ]
        except Exception:
            return []

    # ── PROCEDURAL ───────────────────────────────────────────────────────
    def procedural_load(self, skill_name: str) -> CompiledPipeline:
        """Compile a skill canonical — the procedural tier's read path."""
        return compile_skill(self.skills_dir / f"{skill_name}.md")
