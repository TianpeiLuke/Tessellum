"""Phase 2 (FZ 20k9c1a1a1b7c2k2a3a): note-level fabrication defense.

Two layers behind the close gate's ``grounding_verifier`` seam, cheapest
first:

1. **Identifier grounding** — deterministic, free: every code-like token a
   note asserts (CLI flags, KEY_LIKE constants, dotted config keys, backtick
   commands) must appear in the source. The Bedrock leg's invented flag
   names — and the dual-context rescore's cross-slice accuracy ~3.0–3.8 —
   are exactly this class, and token presence is a string check.
2. **The calibrated claim certificate** — the B3 pilot's thresholds through
   the existing C3 adapter (``make_certificate_verifier``), with the span
   built the SAME way the calibration built it (full source, 40K cap) —
   switching to owned-section spans without re-calibrating would invalidate
   the threshold (recorded follow-on).

Fail-closed at every uncertainty, per the grounding predicate's contract.
"""
from __future__ import annotations

import re
from typing import Any, Callable

from tessellum.composer.certificate_verifier import make_certificate_verifier
from tessellum.composer.llm import LLMBackend
from tessellum.composer.llm_claim_scorer import make_llm_claim_scorer
from tessellum.composer.semantic_certificate import ConformalThresholds

# Backtick inline-code spans — the only place identifiers are extracted from,
# so ordinary prose words never count as "identifiers".
_CODE_SPAN_RE = re.compile(r"`([^`\n]{2,80})`")
# Code-like shapes WITHIN a span: a CLI flag, a KEY_LIKE constant, a dotted
# or underscored config key. Conservative on purpose: high precision beats
# recall for a blocking check.
_IDENTIFIER_RES = (
    re.compile(r"--[a-z][a-z0-9-]{1,40}"),            # --flag-name
    re.compile(r"\b[A-Z][A-Z0-9_]{3,40}\b"),           # ENV_VAR / CONSTANT
    re.compile(r"\b[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){2,}\b"),  # a.b.c keys
)
# Precision allowlist (tuned on the first offline audit, 2026-07-29): writer-
# invented PLACEHOLDERS (`YOUR_TOKEN`, `MY_VAR`) are legitimate documentation
# practice, and a few tokens are universal beyond any one source. Everything
# else absent from the source stays flagged — the invented-API-surface class
# (`--memory`, `agents.defaults.memory.lancedb`) is the target.
_PLACEHOLDER_RE = re.compile(r"^(?:YOUR|MY|EXAMPLE|SAMPLE|TEST)_[A-Z0-9_]+$")
_UNIVERSAL_TOKENS = frozenset({"--help", "--version", "PATH", "HOME", "TODO", "NOTE"})

_CALIBRATION_SPAN_CAP = 40_000
"""Must match the B3 pilot's span construction — thresholds are span-method
specific."""


def extract_note_identifiers(note_text: str) -> set[str]:
    """Code-like tokens the note ASSERTS, from its inline-code spans only."""
    out: set[str] = set()
    for span in _CODE_SPAN_RE.findall(note_text):
        for pattern in _IDENTIFIER_RES:
            out.update(pattern.findall(span))
    return out


def identifier_violations(note_text: str, source_text: str) -> list[str]:
    """Identifiers the note asserts that appear NOWHERE in the source —
    the deterministic fabrication check. Empty list = clean."""
    if not source_text:
        return []
    return sorted(
        ident for ident in extract_note_identifiers(note_text)
        if ident not in source_text
        and ident not in _UNIVERSAL_TOKENS
        and not _PLACEHOLDER_RE.match(ident)
    )


def make_grounded_verifier(
    backend: LLMBackend,
    thresholds: ConformalThresholds,
    source_text: str,
    *,
    scorer_backend: LLMBackend | None = None,
    note_domain: str = "documentation",
) -> Callable[[Any, dict, Any], Any]:
    """The two-layer grounding verifier for the close gate.

    Layer 1 (deterministic): identifier grounding against ``source_text`` —
    a violation returns an ``ungrounded`` verdict naming the invented tokens
    WITHOUT spending a single scorer call. Layer 2: the calibrated
    certificate through the shipped C3 adapter, its claim spans resolved the
    same way the calibration resolved them (full source, 40K cap).
    """
    from tessellum.composer.gates import GroundingVerdict

    span = source_text[:_CALIBRATION_SPAN_CAP]

    def span_text_of(_ref: str) -> str | None:
        return span or None

    scorer = make_llm_claim_scorer(scorer_backend or backend, span_text_of)

    def provenance_of(step: Any, leaf: dict, result: Any):
        # The A3 metadata-only writer leaves carry `source_ref` (a list of
        # refs), not a `provenance` row list — synthesize the single-span
        # provenance the certificate needs; span_text_of resolves any ref to
        # the calibration-consistent span anyway.
        from tessellum.composer.knowledge_plan import ClaimProvenance

        refs = leaf.get("source_ref") if isinstance(leaf, dict) else None
        ref = (str(refs[0]) if isinstance(refs, list) and refs else "source")
        return (ClaimProvenance(span_id="source", source_ref=ref),)

    def body_of(step: Any, leaf: dict, result: Any) -> str:
        # The frontmatter materializer's structured output carries only
        # output_path — read the WRITTEN note file (the artifact of record)
        # and strip its frontmatter, so claims come from the body on disk.
        paths = list(getattr(result.materialized, "files_written", ())) + list(
            getattr(result.materialized, "files_applied", ())
        )
        if not paths:
            return ""
        try:
            text = paths[0].read_text(encoding="utf-8")
        except OSError:
            return ""
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                return text[end + 4:]
        return text

    certificate = make_certificate_verifier(
        scorer=scorer, thresholds=thresholds,
        body_of=body_of,
        provenance_of=provenance_of,
        note_domain_of=lambda *_a: note_domain,
    )

    def _verify(step: Any, leaf: dict, result: Any) -> Any:
        paths = list(getattr(result.materialized, "files_written", ())) + list(
            getattr(result.materialized, "files_applied", ())
        )
        if paths:
            try:
                note_text = paths[0].read_text(encoding="utf-8")
            except OSError:
                note_text = ""
            violations = identifier_violations(note_text, source_text)
            if violations:
                return GroundingVerdict(
                    "ungrounded",
                    detail=(
                        "identifier grounding: asserted tokens absent from "
                        f"the source: {violations[:8]}"
                    ),
                )
        return certificate(step, leaf, result)

    return _verify
