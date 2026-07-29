"""R3.2 (FZ 20k9c1a1a1b7c2k2a1c): prompt-diff parity across leaf constructors.

Two leaf constructors exist for "the same" pipeline — the eval driver's
inline-excerpt leaf and the runtime's URI-only M0 leaf — and the J3 arc
proved a green eval certifies skill∧driver, not the skill: F1/F2 lived
exactly in the constructor difference. This module makes that difference a
DETERMINISTIC finding with no model call: normalize each leaf the way the
pipeline does (code ledger + joined source excerpt), then compare which
informational bindings resolve non-empty per step. Any binding present in
one shape and absent in the other is a parity finding — the next A3.2-style
migration gap surfaces the day it is written, not on first live contact.
"""
from __future__ import annotations

import re
from pathlib import Path

from tessellum.composer.compiler import CompiledPipeline, compile_skill
from tessellum.composer.digestion import (
    _build_artifact_store,
    _ensure_source_excerpt,
    compute_source_ledger,
)

_HOLE_RE = re.compile(r"\{\{\s*(leaf|artifact)\.([a-z0-9_]+)\s*\}\}")

PHASE_SKILL_NAMES: tuple[str, ...] = (
    "skill_tessellum_plan_digestion",
    "skill_tessellum_augment_digestion_plan",
    "skill_tessellum_review_digestion_plan",
    "skill_tessellum_execute_digestion_plan",
)


def _normalize(leaf: dict) -> dict:
    """Apply the pipeline's pre-phase enrichment so parity compares what the
    steps would actually see: the code ledger (``pages``) and the joined
    source excerpt — the same normalization ``run_digestion_pipeline`` does
    before its first phase."""
    doc = dict(leaf)
    # Mirror digestion's ledger call-site: members when present, else the F4
    # pseudo-member synthesized from top-level source_content — so the M0
    # single-doc shape is code-measured here exactly as on the live path.
    members = doc.get("members")
    if not (isinstance(members, list) and members):
        sc = doc.get("source_content")
        members = (
            [{"source_id": doc.get("source_name") or doc.get("id") or "source",
              "excerpt": sc}]
            if isinstance(sc, str) and sc.strip() else []
        )
    ledger = compute_source_ledger(members)
    if ledger:
        doc["pages"] = ledger
        doc["_pages_code_measured"] = True
    _ensure_source_excerpt(doc)
    return doc


def binding_resolution(
    pipeline: CompiledPipeline, leaf: dict
) -> dict[str, dict[str, bool]]:
    """Per step: which ``leaf.X`` / ``artifact.X`` bindings resolve to a
    non-empty value for this leaf shape. ``upstream.*`` / ``retry.*`` are
    runtime-produced and identical across constructors, so they are outside
    parity's scope."""
    artifacts = _build_artifact_store(leaf)
    out: dict[str, dict[str, bool]] = {}
    for step in pipeline.steps:
        prompt = step.prompt_section_text or ""
        resolution: dict[str, bool] = {}
        for ns, key in _HOLE_RE.findall(prompt):
            name = f"{ns}.{key}"
            if ns == "leaf":
                val = leaf.get(key)
            else:
                val = artifacts.get(key)
            resolution[name] = val not in (None, "", [], (), {})
        out[step.section_id] = resolution
    return out


# Bindings whose presence LEGITIMATELY differs across constructors, by the
# skills' own documented contract: `member_count: 1` with an EMPTY `members`
# list IS the single-source shape (the identify_source prose handles both
# renderings). An exemption here must cite the prose that handles the
# variance — everything else that differs is a finding.
DECLARED_SHAPE_VARIANT: frozenset[str] = frozenset({"leaf.members"})


def diff_leaf_shapes(
    skills_dir: Path | str,
    leaf_a: dict,
    leaf_b: dict,
    *,
    skill_names: tuple[str, ...] = PHASE_SKILL_NAMES,
    label_a: str = "shape_a",
    label_b: str = "shape_b",
    allowed_variance: frozenset[str] = DECLARED_SHAPE_VARIANT,
) -> list[str]:
    """The parity diff: normalize both leaf shapes, resolve every step's
    informational bindings under each, and report every binding that is
    present in one shape but absent in the other. An empty return means the
    two constructors feed the compiled skills identically."""
    skills_dir = Path(skills_dir)
    a = _normalize(leaf_a)
    b = _normalize(leaf_b)
    findings: list[str] = []
    for name in skill_names:
        path = skills_dir / f"{name}.md"
        if not path.is_file():
            findings.append(f"{name}: skill file missing at {path}")
            continue
        pipeline = compile_skill(path)
        res_a = binding_resolution(pipeline, a)
        res_b = binding_resolution(pipeline, b)
        for section_id in res_a:
            for binding, present_a in res_a[section_id].items():
                if binding in allowed_variance:
                    continue
                present_b = res_b[section_id].get(binding, False)
                if present_a != present_b:
                    have, lack = (
                        (label_a, label_b) if present_a else (label_b, label_a)
                    )
                    findings.append(
                        f"{name}/{section_id}: {binding} resolves under "
                        f"{have} but NOT under {lack}"
                    )
    return findings
