"""tessellum.composer.certificate_verifier — feed the grounding_verifier seam.

The runtime's ``grounding_verifier`` seam — ``(step, leaf, result) ->
GroundingVerdict`` on ``run_pipeline_dynamic`` / the close-gate — is UNFED today
(grep of ``runtime``/``cli`` finds no producer). The calibrated certificate
(``semantic_certificate.certify``) produces exactly that ``GroundingVerdict``,
so this module is the C3 adapter that closes the boundary the plans named
(P7 / DKS A4.2 "the wiring"): extract a written note's claims, score them
through the injected (real-model-or-reference) ``ClaimScorer``, run the shipped
conformal ``certify``, and hand back the verdict for the program gate to decide.

Boundary intact: a model (or the reference lexical proxy) produces per-claim
evidence; the calibrated program (``certify``) decides accept/abstain; the gate
consumes the verdict. This module wires, it never judges.

**Opt-in.** Nothing here runs unless a caller explicitly builds a verifier and
passes it as ``grounding_verifier`` — the default runtime path (verifier
``None``) is untouched and byte-identical. And even wired, the certificate only
*accepts* inside a domain the caller listed in
:attr:`ConformalThresholds.domains` (``certify`` fail-closes to ``abstain``
outside it, and on an EMPTY domain set); everywhere else → ``ungrounded`` → the
close gate falls back to the human artifact. So wiring this does NOT by itself
enable unattended promotion; it makes the certificate runnable + its verdict
available.

**A7.5 is the CALLER's contract, NOT enforced here.** The runtime accept path
trusts ``thresholds`` — it does not re-run :func:`run_calibration_gate` per note.
Listing a domain in ``thresholds.domains`` ASSERTS that domain passed the A7.5
held-out false-accept gate; nothing in this module verifies that assertion at
run time. The operator must run the gate and only pass thresholds whose domains
are GO. Until a real model + real corpus return GO, pass thresholds with an
empty / non-production domain set so every note abstains (stays human-supervised).

Pure given pure injected accessors + scorer; no clock/randomness/I/O here.
"""

from __future__ import annotations

from typing import Any, Callable

from tessellum.composer.claim_extraction import extract_claims
from tessellum.composer.knowledge_plan import ClaimProvenance
from tessellum.composer.gates import GroundingVerdict
from tessellum.composer.semantic_certificate import (
    Claim,
    ClaimScorer,
    ConformalThresholds,
    certify,
)


def _default_body_of(step: Any, leaf: dict, result: Any) -> str:
    """Read the written note's markdown body from a step result.

    The note-writing step's materialized ``structured`` dict carries
    ``body_markdown`` (the materializer's ``markdown_with_frontmatter`` /
    ``body_markdown_to_file`` shape). Falls back to an empty string when absent
    — an empty body yields no claims → ``certify`` abstains (fail-closed)."""
    structured = getattr(getattr(result, "materialized", None), "structured", None)
    if isinstance(structured, dict):
        body = structured.get("body_markdown") or structured.get("body") or ""
        if isinstance(body, str):
            return body
    return ""


def _default_provenance_of(
    step: Any, leaf: dict, result: Any
) -> tuple[ClaimProvenance, ...]:
    """Read the note's claim provenance from the leaf/result.

    Looks for a ``provenance`` list (``[{span_id, source_ref}, ...]``) on the
    step's structured output first, then the leaf (the writer leaf projected
    from a ``NoteIntent`` carries provenance). Rows that don't parse as a
    ``{span_id, source_ref}`` pair are skipped. No provenance → no claims →
    fail-closed abstain."""
    candidates: list[Any] = []
    structured = getattr(getattr(result, "materialized", None), "structured", None)
    if isinstance(structured, dict) and isinstance(structured.get("provenance"), list):
        candidates = structured["provenance"]
    elif isinstance(leaf, dict):
        note = leaf.get("note")
        if isinstance(note, dict) and isinstance(note.get("provenance"), list):
            candidates = note["provenance"]
        elif isinstance(leaf.get("provenance"), list):
            candidates = leaf["provenance"]
    rows: list[ClaimProvenance] = []
    for row in candidates:
        if isinstance(row, ClaimProvenance):
            rows.append(row)
        elif (
            isinstance(row, dict)
            and isinstance(row.get("span_id"), str) and row["span_id"]
            and isinstance(row.get("source_ref"), str) and row["source_ref"]
        ):
            # isinstance-str BEFORE construction so a truthy-but-non-string field
            # (e.g. span_id=1) is skipped, not passed to ClaimProvenance's
            # min_length=1 str validator (which would raise ValidationError and
            # crash the whole step). "rows that don't parse are skipped."
            rows.append(
                ClaimProvenance(span_id=row["span_id"], source_ref=row["source_ref"])
            )
    return tuple(rows)


def make_certificate_verifier(
    *,
    scorer: ClaimScorer,
    thresholds: ConformalThresholds,
    body_of: Callable[[Any, dict, Any], str] = _default_body_of,
    provenance_of: Callable[
        [Any, dict, Any], tuple[ClaimProvenance, ...]
    ] = _default_provenance_of,
    note_domain_of: Callable[[Any, dict, Any], str | None] | None = None,
) -> Callable[[Any, dict, Any], GroundingVerdict]:
    """Build a ``grounding_verifier`` from the calibrated certificate (C3).

    The returned callable matches the runtime seam signature ``(step, leaf,
    result) -> GroundingVerdict``:

    1. extract claims from the written note (``body_of`` + ``provenance_of``,
       via :func:`~tessellum.composer.claim_extraction.extract_claims`);
    2. score + certify with the injected ``scorer`` + calibrated ``thresholds``
       (:func:`~tessellum.composer.semantic_certificate.certify`);
    3. return ``result.verdict`` (``grounded`` on accept, ``ungrounded`` on
       abstain) — the exact object the close gate's grounding predicate consumes.

    ``scorer`` is the injected seam — the real NLI/SummaC model in production, or
    :func:`~tessellum.composer.lexical_scorer.make_lexical_scorer` as the
    runnable reference baseline. ``note_domain_of`` (optional) supplies the note's
    domain so the certificate abstains outside its calibrated domain(s).
    """

    def _verify(step: Any, leaf: dict, result: Any) -> GroundingVerdict:
        body = body_of(step, leaf, result)
        provenance = provenance_of(step, leaf, result)
        note_id = ""
        if isinstance(leaf, dict):
            note_id = str(leaf.get("_id") or leaf.get("target_path") or "note")
        claims: list[Claim] = extract_claims(
            body, provenance, note_id=note_id or "note"
        )
        domain = note_domain_of(step, leaf, result) if note_domain_of else None
        return certify(
            claims, scorer=scorer, thresholds=thresholds, note_domain=domain
        ).verdict

    return _verify


__all__ = [
    "make_certificate_verifier",
]
