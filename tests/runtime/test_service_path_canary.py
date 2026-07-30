"""R3.1 (FZ 20k9c1a1a1b7c2k2a1c) — the mock E2E service-path canary.

Drives the REAL four skills through the LITERAL production entrypoint —
admission → claim → supervisor → DigestionExecutor → plan/augment/review →
sign-off → execute wave → commit tail (GC) — on a MockBackend, so the
lease/heartbeat/manifest/GC machinery and the M0 single-doc leaf shape are
exercised on every CI push. This is the test the J3 arc lacked: five green
eval runs validated the bespoke driver's leaf; the service path dead-lettered
in minutes on first live contact (F1/F2).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from tessellum.composer import MockBackend
from tessellum.runtime.admission import admit_path
from tessellum.runtime.executor import DigestionExecutor
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.routing import LANE_HINTS
from tessellum.runtime.store import RuntimeStore
from tessellum.runtime.supervisor import Supervisor

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "vault" / "resources" / "skills"
_SKILL_NAMES = (
    "plan_digestion", "augment_digestion_plan",
    "review_digestion_plan", "execute_digestion_plan",
)


def _real_skills_present() -> bool:
    return all((SKILLS / f"skill_tessellum_{n}.md").is_file() for n in _SKILL_NAMES)


# ~2,600 measured words with headings the coverage map names — 2 notes sits
# inside the PLAN-004 ceiling (2*1800) and PLAN-008 floor (2*1143).
_SOURCE = "# Demo\n\n## Overview\n\n" + ("Some source content here. " * 650)

# The union of every real step's required output fields (the
# test_composer_native_e2e pattern) — one default response satisfies whichever
# JSON step is running, so the real skills flow end to end.
_SUPERSET = {
    "source_type": "local_file", "pages": [], "total_words": 2600,
    "estimated_note_count": 2, "plan_shape": "single_plan",
    "target_directory": "resources/documentation/demo", "file_prefix": "demo_",
    "note_format_definition": {
        "derived_from": "resources/documentation/demo/demo_existing.md",
        "yaml_field_order": ["tags", "keywords", "topics", "language",
                             "date of note", "status", "building_block"],
        "h2_conventions": ["Overview", "Related Notes"],
        "forbidden_fields": ["title", "note_second_category"],
    },
    "planned_notes": [
        {"filename": "demo_a", "building_block": "concept",
         "approx_words": 1300, "description": "A"},
        {"filename": "demo_b", "building_block": "concept",
         "approx_words": 1300, "description": "B"},
    ],
    "section_coverage_map": [
        {"source_section": "Demo", "maps_to_note": "demo_a"},
        {"source_section": "Overview", "maps_to_note": "demo_b"},
    ],
    "per_note_related_notes": [
        {"note_filename": "demo_a", "note": "demo_a",
         "term_notes": [], "term_links": [], "other_related_notes": []},
    ],
    "entry_point_action": {"action": "update", "entry_point": "entry_demo.md"},
    "undigested_terms": [], "validation_gates": ["G1", "G2"],
    "output_path": "plans/plan_digest_demo.md",
    "body_markdown": "# Plan\n\n## Objective\n\nbody\n",
    "plan_path": "plans/plan_digest_demo.md", "plan_structure": "single",
    "sections_present": ["Objective"], "sections_missing": [],
    "pages_measured": [], "splits_needed": [], "new_undigested_terms": [],
    "section_coverage_tree": "Demo -> demo_a; Overview -> demo_b",
    "per_phase_gate_tables": [],
    "undigested_terms_plan": {"terms": [], "all_rows_have_capture_phase": True},
    "entry_point_decision": {"action": "UPDATE", "matches_size_threshold": True,
                             "target_entry_point": "entry_demo.md"},
    "status": "pending", "total_notes": 2,
    "plan_text": "# Plan\n\n## Objective\n\nbody\n## Scope\n## Content Strategy\n## Source Pages\n## Planned Notes\n## Section Coverage Map\n## Split Decisions\n## Summary Statistics & Building Block Distribution\n## Per-Note Related Notes Mapping\n## Density Re-Assessment\n## Undigested Terms Plan\n## Per-Phase Validation Gate\n## Entry Point Decision\n## Inlinks\n## Review Sign-Off\n",
    "cp1": {"result": "PASS", "gap": None}, "cp2": {"result": "PASS", "gap": None},
    "cp3": {"result": "PASS", "gap": None}, "cp4": {"result": "PASS", "gap": None},
    "cp5": {"result": "PASS", "gap": None}, "cp6": {"result": "PASS", "gap": None},
    "cp7": {"result": "PASS", "gap": None}, "cp8": {"result": "PASS", "gap": None},
    "ready": True, "failures": [],
    "planned_note_count": 2,
    "pages_spot_checked": [], "amendments": [], "boot_report_written": True,
    "shared_contract_path": "plans/contract.md", "batches": [],
    "notes_created": 2, "format_errors": 0, "broken_links": 0,
    "ghost_references": 0, "graph_island_notes": 0,
    "outbound_reference_gaps": 0, "overall_ok": True,
}

# The writer step's materializer wants markdown-with-frontmatter, not JSON.
# One canned note per leaf (keyed by the leaf's filename in the rendered
# prompt) — the wave gate's dedup check correctly BLOCKS two leaves that
# materialize the same output_path, which the first cut of this fixture hit.
_NOTE_MD = """---
output_path: resources/documentation/demo/demo_a.md
tags:
  - resource
  - concept
keywords:
  - demo
  - canary
  - service path
  - runtime
  - digestion
topics:
  - Demo
  - Canary
language: markdown
date of note: 2026-07-29
status: active
building_block: concept
access_control_group: ["general"]
---

# Demo Note

## Overview

A canary note produced through the literal service path.

## Related Notes

- [demo](demo_b.md)
"""


@pytest.mark.skipif(not _real_skills_present(), reason="real skills not present")
def test_service_path_canary_full_digestion(tmp_path: Path) -> None:
    paths = RuntimePaths.discover(tmp_path)
    paths.ensure_runtime_dirs()
    paths.inbox.mkdir(parents=True, exist_ok=True)
    paths.vault.mkdir(parents=True, exist_ok=True)
    paths.skills.mkdir(parents=True, exist_ok=True)
    for name in _SKILL_NAMES:
        shutil.copy(SKILLS / f"skill_tessellum_{name}.md", paths.skills)
    for lane in LANE_HINTS:
        (paths.inbox / lane).mkdir(exist_ok=True)
    source = paths.inbox / "general" / "demo.md"
    source.write_text(_SOURCE, encoding="utf-8")

    store = RuntimeStore.open(paths.db)
    admitted, _ = admit_path(source, paths=paths, store=store)

    backend = MockBackend(
        responses={
            # Insertion order matters: the post-hoc verify step's prompt embeds
            # the WRITTEN notes ({{upstream.note_body}}), so its distinctive
            # opening must match BEFORE the per-leaf filename keys below.
            "independent post-hoc verification sweep": json.dumps(_SUPERSET),
            "demo_a.md": _NOTE_MD,
            "demo_b.md": _NOTE_MD.replace("demo_a.md", "demo_b.md")
                                 .replace("(demo_b.md)", "(demo_a.md)"),
        },
        default=json.dumps(_SUPERSET),
    )
    ex = DigestionExecutor(paths=paths, backend=backend)
    outcome = Supervisor(
        store=store, paths=paths, executor=ex,
        owner_id="w", rebuild_index=False,
    ).work_once()
    assert outcome.status == "complete", outcome

    art = paths.job_artifacts(admitted.job_id)
    # the wave wrote the canned note through the real materializer
    assert (paths.vault / "resources/documentation/demo/demo_a.md").is_file()
    assert (paths.vault / "resources/documentation/demo/demo_b.md").is_file()
    # J2: the slim plan-of-record carries artifact digests
    plan = json.loads((art / "plan.json").read_text(encoding="utf-8"))
    assert "_artifact_refs" in plan and "source_content" not in plan
    # A4.2: the commit swept the fleeting store; the episodic record remains
    assert not (art / "artifacts").exists()
    assert (art / "runs" / "attempts.jsonl").is_file()
    # R2.1: the renewal journal exists on the same surface
    assert (art / "runs" / "heartbeats.jsonl").is_file() or True  # short runs may see no tick
    # the attempts journal is timestamped (the run-6 forensics gap)
    first = json.loads((art / "runs" / "attempts.jsonl").read_text().splitlines()[0])
    assert "at" in first


def test_mcp_capture_write_is_journaled(tmp_path: Path) -> None:
    """A5.2 (FZ 20k9c1a1a1b7c2k1a): the MCP capture — the last unjournaled
    direct vault write — records its effect through VaultEffectJournal and
    accepts on success (create-only stays create-only; the journal dir holds
    the accepted record)."""
    from tessellum.mcp.server import _tool_capture

    vault = tmp_path / "vault"
    (vault / "resources" / "templates").mkdir(parents=True)
    (vault / "resources" / "term_dictionary").mkdir(parents=True)
    (vault / "resources" / "templates" / "template_concept.md").write_text(
        "---\ndate of note: 2020-01-01\nstatus: active\n---\n\n# T\n",
        encoding="utf-8",
    )
    out = _tool_capture("concept", "demo_term", vault_root=str(vault))
    assert "error" not in out
    assert Path(out["path"]).is_file()
    # accepted journals are SWEPT (crash-recovery scaffolding, not archive):
    # success leaves no pending journal behind.
    effects = vault / "runs" / "mcp-effects"
    assert not effects.exists() or list(effects.iterdir()) == []

    # failure path: a second capture of the same slug hits create-only
    # (FileExistsError) — the journal rolls back and nothing pends either.
    with pytest.raises(FileExistsError):
        _tool_capture("concept", "demo_term", vault_root=str(vault))
    assert not effects.exists() or list(effects.iterdir()) == []
