#!/usr/bin/env python3
"""Fold a skill's ``.pipeline.yaml`` sidecar into its canonical ``.md``.

Single-file skill format: each step is an H2 section with a
``<!-- :: section_id = X :: -->`` anchor, a leading ``` ```yaml ``` contract
block (the typed step declaration, minus ``section_id`` and minus the
``prompt_template``), and the step's prompt prose (taken from the sidecar's
``prompt_template``, falling back to the canonical section body if the sidecar
had no ``prompt_template`` for that step).

Usage:
    python scripts/migrate_skill_to_single_md.py <skill_canonical.md> [--write]

Without ``--write`` it prints a unified preview and does not touch disk.
With ``--write`` it rewrites the canonical in place and deletes the sidecar.

This is a one-shot migration tool; it is not part of the runtime.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

# The step declaration keys that belong in the contract block, in a stable
# author-friendly order. ``section_id`` is intentionally excluded (it lives in
# the anchor) and ``prompt_template`` is excluded (it becomes the prose).
_CONTRACT_KEY_ORDER = [
    "role",
    "aggregation",
    "batchable",
    "depends_on",
    "materializer",
    "wire_format",
    "operation_verb",
    "applies_to_files",
    "applies_to_files_query",
    "output_key",
    "expected_output_schema",
    "mcp_dependencies",
    "timeout_seconds",
    "max_prompt_chars",
]

_ANCHOR_RE = re.compile(
    r"^(##\s+.*?<!--\s*::\s*section_id\s*=\s*([a-z0-9_]+)\s*::\s*-->\s*)$",
    re.MULTILINE,
)

# The stale self-reference the two-file format used: "Apply the procedure in
# section \"X\" of skill_Y." Now that both live in one file, we inline the
# canonical SOP prose where this reference stood, rather than pointing at a
# section the (tool-free) model can't fetch.
_APPLY_REF_RE = re.compile(
    r"Apply the procedure in (?:the section|section)\s+"
    r"\"?[a-z0-9_]+\"?\s+of\s+skill_[a-z0-9_]+\s*\.",
    re.IGNORECASE,
)


def _compose_prompt(sidecar_prompt: str, canonical_prose: str) -> str:
    """Compose the step prompt from the sidecar prompt + canonical SOP prose.

    The sidecar prompt carries the data wiring ({{leaf}}/{{upstream}}) and the
    output contract; the canonical prose carries the rich SOP (format spec,
    required sections). If the sidecar referenced the canonical section
    ("Apply the procedure in section X of skill_Y."), inline the SOP prose
    there. If it did not (self-contained sidecar), keep the sidecar prompt and
    append the canonical prose only when it adds substance.
    """
    sidecar_prompt = (sidecar_prompt or "").strip()
    canonical_prose = (canonical_prose or "").strip()

    if not sidecar_prompt:
        return canonical_prose
    if not canonical_prose:
        return sidecar_prompt

    if _APPLY_REF_RE.search(sidecar_prompt):
        # Inline the SOP where the reference stood.
        inlined = f"Follow this procedure:\n\n{canonical_prose}"
        return _APPLY_REF_RE.sub(inlined, sidecar_prompt, count=1).strip()

    # Self-contained sidecar prompt. Append canonical prose only if it is more
    # than a trivial one-liner (Setup/Resources sections are dropped by the
    # step filter anyway; this guards a terse step section).
    if len(canonical_prose) > 120:
        return f"{sidecar_prompt}\n\n---\n\n{canonical_prose}"
    return sidecar_prompt


# Schema-required Step keys — always emitted even when empty/default, so the
# per-step schema validation (which requires them) passes.
_ALWAYS_EMIT = {"role", "aggregation", "batchable", "depends_on"}


def _ordered_contract(step: dict) -> dict:
    """Return the step dict minus section_id/prompt_template, key-ordered.

    Schema-required keys (role/aggregation/batchable/depends_on) are always
    emitted; other keys are dropped when empty to keep the block terse.
    """
    out: dict = {}
    for k in _CONTRACT_KEY_ORDER:
        if k not in step:
            continue
        if k in _ALWAYS_EMIT or step[k] not in (None, [], (), {}):
            out[k] = step[k]
    # Guarantee depends_on is present (schema-required; older sidecars always
    # had it, but be defensive).
    out.setdefault("depends_on", list(step.get("depends_on") or []))
    # Preserve any extra keys we didn't enumerate (forward-compat).
    for k, v in step.items():
        if k in ("section_id", "prompt_template"):
            continue
        if k not in out and v not in (None, [], (), {}):
            out[k] = v
    return out


def _yaml_block(contract: dict) -> str:
    body = yaml.safe_dump(
        contract, sort_keys=False, default_flow_style=False, width=88
    ).rstrip()
    return f"```yaml\n{body}\n```"


def migrate(canonical_path: Path) -> tuple[str, Path]:
    """Return (new_canonical_text, sidecar_path)."""
    sidecar_path = canonical_path.with_suffix(".pipeline.yaml")
    if not sidecar_path.is_file():
        raise SystemExit(f"no sidecar found at {sidecar_path}")

    sidecar = yaml.safe_load(sidecar_path.read_text(encoding="utf-8"))
    steps_by_id = {s["section_id"]: s for s in sidecar.get("pipeline", [])}

    text = canonical_path.read_text(encoding="utf-8")

    # Strip the frontmatter ``pipeline_metadata:`` line (sidecar is going away).
    text = re.sub(
        r"^pipeline_metadata:.*$\n", "", text, count=1, flags=re.MULTILINE
    )

    # Walk sections; for each anchored H2 that is a pipeline step, inject the
    # contract block + prompt right after the heading, replacing the existing
    # section body.
    anchors = list(_ANCHOR_RE.finditer(text))
    # Build the new text by processing sections back-to-front (so offsets hold).
    pieces: list[tuple[int, int, str]] = []  # (start, end, replacement)
    for i, m in enumerate(anchors):
        section_id = m.group(2)
        if section_id not in steps_by_id:
            continue  # prose section (Setup/Resources/description) — leave as is
        step = steps_by_id[section_id]
        heading = m.group(1)
        body_start = m.end()
        body_end = anchors[i + 1].start() if i + 1 < len(anchors) else len(text)

        contract = _ordered_contract(step)
        canonical_prose = text[body_start:body_end].strip()
        sidecar_prompt = (step.get("prompt_template") or "").strip()
        # Compose: the sidecar prompt (data wiring + output contract) with the
        # canonical SOP prose inlined where it was referenced. This is the
        # whole point of the single-file fold — both reach the tool-free model.
        prompt = _compose_prompt(sidecar_prompt, canonical_prose)

        new_section = f"{heading}\n\n{_yaml_block(contract)}\n\n{prompt}\n\n"
        pieces.append((m.start(), body_end, new_section))

    for start, end, replacement in reversed(pieces):
        text = text[:start] + replacement + text[end:]

    # Collapse any 3+ blank lines introduced by the splice.
    text = re.sub(r"\n{3,}", "\n\n", text)
    if not text.endswith("\n"):
        text += "\n"
    return text, sidecar_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical", type=Path)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    new_text, sidecar_path = migrate(args.canonical)

    if not args.write:
        sys.stdout.write(new_text)
        print(f"\n--- preview only; pass --write to apply + delete {sidecar_path.name} ---",
              file=sys.stderr)
        return 0

    args.canonical.write_text(new_text, encoding="utf-8")
    sidecar_path.unlink()
    print(f"migrated {args.canonical.name}; deleted {sidecar_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
