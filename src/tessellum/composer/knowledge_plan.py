"""Typed knowledge-plan intent graph + a pure writer-leaf projection.

Phase **P2** (core) of "Dynamic Digestion as a Snapshot-Pinned Knowledge
Transaction". This module is the typed, deterministic replacement for the
untyped whole-plan fallback at :func:`digestion.run_digestion_pipeline`
(``execute_leaves = [dict(plan_doc)]``, currently at digestion.py:284-288):
instead of one leaf carrying the entire opaque plan dict, a *set* of typed,
provenance-carrying :class:`NoteIntent` objects is projected — one writer
leaf per intent — via :func:`project_note_intent_graph`.

Action items realized here (all pure — no clock, no randomness, no I/O
anywhere in this module):

* **A2.3** — frozen pydantic-v2 :class:`NoteIntent` / :class:`NoteIntentGraph`
  typed models. Style mirrors :class:`tessellum.composer.loader.PipelineStep`
  and :mod:`tessellum.composer.proposals` (``ConfigDict(frozen=True,
  extra="forbid")`` + ``tuple[...]`` immutable collections + ``Literal``
  discriminators). Unlike the loader's ``extra="allow"`` these are *closed*
  models (``extra="forbid"``), like :class:`proposals._Effect`. Each
  :class:`NoteIntent` carries a thesis, exactly one building block, REQUIRED
  claim provenance (an intent with zero source spans is invalid), a
  disposition (only ``"create"`` is accepted in P2 — ``update``/``merge``/
  ``skip`` are defined in the enum but REJECTED here, deferred to P9), a
  vault-relative target path, coverage responsibility, dependency edges,
  outbound relevance links, navigation membership, and required reverse
  inlinks. The parent ``SourceBundle`` is represented for now by a plain
  ``objective_id`` string on :class:`NoteIntentGraph`; the full SourceBundle
  admission is DEFERRED to **P2b** (A2.1 — see module note below).

* **A2.4** — :func:`project_note_intent_graph`, a pure, deterministic,
  order-preserving projection of a :class:`NoteIntentGraph` into a list of
  typed "writer leaves" (one leaf per :class:`NoteIntent`). This is the
  TYPED replacement for the whole-plan fallback in
  :func:`digestion.run_digestion_pipeline`. NOTE: this phase does NOT touch
  ``digestion.py`` — no import, no wiring; the docstring is a forward pointer
  only. Wiring :func:`project_note_intent_graph` into
  ``run_digestion_pipeline`` is **P2b** (it needs the deferred SourceBundle /
  hash-addressed source delivery — A2.1/A2.2), so digestion's behavior stays
  byte-identical for now.

Deferred to **P2b** (NOT implemented here):

* **A2.1** — SourceBundle bundle admission in ``InboxScanner.scan_once``
  (runtime/inbox.py). The parent objective is represented here only as a
  plain ``objective_id: str`` on :class:`NoteIntentGraph`.
* **A2.2** — hash-addressed parsed-artifact delivery of ``source_content`` to
  the planner prompt (runtime/executor.py + composer/executor.py prompt cap).
  No whole-content injection is added; source delivery is what
  :func:`project_note_intent_graph` will consume in P2b.

Content-id reuse (no reinvented hashing): :func:`note_intent_content_id`
reuses P0's :func:`tessellum.composer.proposals.canonical_json_bytes`
(float-ban + NFC-normalized + sorted keys), so the id is order- and
process-stable. This module imports ONLY from
:mod:`tessellum.composer.proposals` (plus stdlib + pydantic) — no runtime, no
materializer — keeping the composer import DAG acyclic (composer never
imports runtime).
"""

from __future__ import annotations

import hashlib
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tessellum.composer.proposals import canonical_json_bytes

# ── A2.3 — claim provenance + disposition enum ─────────────────────────────


class ClaimProvenance(BaseModel):
    """One ``{span_id, source_ref}`` provenance row backing a note's claims.

    A blank ref is not provenance — both fields are non-empty. ``frozen`` +
    ``extra="forbid"`` (closed model, like :class:`proposals._Effect`).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    span_id: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)


NoteDisposition = Literal["create", "update", "merge", "drop", "skip"]
"""Every note-intent disposition. As of **P9** all effect classes are enabled
(A9.2). Preimage rules (enforced by :class:`NoteIntent`'s validator):

- ``create``: target must NOT exist → ``expected_preimage`` MUST be absent.
- ``update`` / ``merge`` / ``drop``: target MUST exist → ``expected_preimage``
  (the pinned pre-image hash) is REQUIRED (the promotion CAS checks it).
- ``skip``: an explicit no-op (nothing is written).

(Edge-level ``reroute`` is a P0 ``Effect``, not a note disposition.)"""


# ── A2.3 — the typed note intent ───────────────────────────────────────────


class NoteIntent(BaseModel):
    """One typed, provenance-carrying intent to author a single note.

    Mirrors the :class:`proposals._Effect` idiom: ``frozen=True`` blocks
    attribute reassignment, ``extra="forbid"`` rejects unknown fields
    (closed model), and every collection is an immutable ``tuple[...]``.

    Attributes:
        note_id: Stable graph-local id; dependency/inlink edges reference it.
        thesis: The single claim/point the note makes.
        building_block: Exactly ONE building block per intent. The model stays
            permissive (``min_length=1``); single-BB-atomicity is enforced by
            the GATES — ``STRUCT-BB-ATOMIC`` (structural gate) and ``PLAN-005``
            (plan gate, FZ 20k9d4) reject a multi-BB value so it surfaces as a
            re-plannable failure, not a construction error.
        approx_words: Planner's estimated word count for this note's body
            (0 = unknown / not estimated). The plan-atomicity gate (FZ 20k9d4)
            fails a plan whose note declares ``approx_words >= 1800`` — the
            OBJECTIVE density trigger that forces a re-plan (split OR rearrange).
        disposition: Only ``"create"`` is accepted in P2 (see class note).
        target_path: Vault-relative path. The MODEL only stores it; the
            relative-only + confinement enforcement lives in the overlay
            writer (:class:`tessellum.composer.overlay.OverlayWriter`),
            mirroring materializer semantics.
        expected_preimage: For a ``"create"`` this MUST be ``None``/absent —
            the target must not exist. (Non-None reserved for P9 update flow.)
        provenance: REQUIRED, non-empty tuple of :class:`ClaimProvenance` —
            an intent with zero source spans is invalid (``min_length=1``).
        coverage: Coverage-responsibility tokens (section/topic ids owned).
        depends_on: Dependency edges (``note_id`` refs).
        relevance_links: Outbound relevance links (``note_id``/slug refs).
        navigation: ``entry_point`` ids this note registers under.
        required_inlinks: ``note_id`` refs that must add a reverse inlink
            back to this note.

    Validators (``model_validator(mode="after")``):
        - preimage rule (P9, A9.2): ``create`` forbids ``expected_preimage``
          (target must not exist); ``update``/``merge``/``drop`` REQUIRE it
          (target must exist; the promotion CAS checks the pinned pre-image).
        - self-dep guard: ``note_id`` may not appear in ``depends_on``.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    note_id: str = Field(min_length=1)
    thesis: str = Field(min_length=1)
    building_block: str = Field(min_length=1)
    approx_words: int = Field(default=0, ge=0)
    disposition: NoteDisposition = "create"
    target_path: str = Field(min_length=1)
    expected_preimage: str | None = None
    provenance: tuple[ClaimProvenance, ...] = Field(..., min_length=1)
    coverage: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    relevance_links: tuple[str, ...] = ()
    navigation: tuple[str, ...] = ()
    required_inlinks: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _check_disposition_rules(self) -> "NoteIntent":
        # P9 (A9.2): all effect classes enabled, gated by the preimage rule.
        if self.disposition == "create":
            if self.expected_preimage is not None:
                raise ValueError(
                    "create disposition forbids expected_preimage; the target "
                    "must not exist"
                )
        elif self.disposition in ("update", "merge", "drop"):
            if self.expected_preimage is None:
                raise ValueError(
                    f"{self.disposition} disposition requires expected_preimage "
                    "(the target must exist; the promotion CAS checks it)"
                )
        # "skip" is an explicit no-op; expected_preimage is optional there.
        if self.note_id in self.depends_on:
            raise ValueError("NoteIntent cannot depend on itself")
        # NOTE: single-BB-atomicity is deliberately NOT enforced on the model —
        # the model stays permissive (min_length=1) and the GATES enforce it
        # (STRUCT-BB-ATOMIC in structural_gates + PLAN-005 in the plan gate,
        # FZ 20k9d4), so a malformed BB surfaces as a re-plannable gate failure
        # rather than an unrecoverable construction error.
        return self


class NoteIntentGraph(BaseModel):
    """An ordered set of :class:`NoteIntent` under one parent objective.

    Attributes:
        objective_id: The parent ``SourceBundle``-ish id — a plain string for
            now. The FULL SourceBundle admission (A2.1) is DEFERRED to P2b;
            here the objective is just an id token so this core stays
            self-contained and off the live admission path.
        intents: ORDERED tuple of :class:`NoteIntent`. Projection is
            order-preserving; an empty tuple is allowed (projects to ``[]``).

    Validator (``model_validator(mode="after")``): ``note_id`` values are
    unique across ``intents`` — projection and dependency edges key on
    ``note_id``, so duplicates are unsound. Referential closure of
    ``depends_on`` / ``relevance_links`` / ``required_inlinks`` is
    deliberately NOT enforced — those may legitimately point at pre-existing
    vault notes, not graph members.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    objective_id: str = Field(min_length=1)
    intents: tuple[NoteIntent, ...] = ()

    @model_validator(mode="after")
    def _unique_note_ids(self) -> "NoteIntentGraph":
        seen: set[str] = set()
        for intent in self.intents:
            if intent.note_id in seen:
                raise ValueError(
                    f"duplicate note_id in NoteIntentGraph: {intent.note_id!r}"
                )
            seen.add(intent.note_id)
        return self


# ── Content id (reuses P0 canonical hashing — no reinvention) ──────────────


def note_intent_content_id(intent: NoteIntent) -> str:
    """Stable content id for a :class:`NoteIntent` — pure, no clock/random/IO.

    ``sha256`` over :func:`proposals.canonical_json_bytes` of the intent's
    JSON-mode dump (float-ban + NFC-normalized + sorted keys), so the id is
    order- and process-stable. Reuses the P0 canonicalizer rather than
    reinventing hashing; stamped into the projected leaf's ``"note"`` payload
    for P2b traceability.
    """
    return hashlib.sha256(
        canonical_json_bytes(intent.model_dump(mode="json"))
    ).hexdigest()


# ── A2.4 — pure writer-leaf projection ─────────────────────────────────────


def project_note_intent_graph(graph: NoteIntentGraph) -> list[dict]:
    """Project a :class:`NoteIntentGraph` into typed writer leaves — pure.

    Deterministic, order-preserving, no clock/random/IO: iterates
    ``graph.intents`` in declared order (no sorting, no dedup), emitting
    exactly one leaf dict per :class:`NoteIntent`. Reads only the frozen
    input; never mutates it (builds fresh dicts).

    This is the TYPED replacement for the whole-plan fallback
    ``execute_leaves = [dict(plan_doc)]`` in
    :func:`digestion.run_digestion_pipeline` (currently at digestion.py:284-288).
    This phase does NOT wire it in — no import of / edit to ``digestion.py``;
    the pointer is forward-looking only. Wiring is **P2b** (it needs the
    deferred SourceBundle / source delivery — A2.1/A2.2).

    Leaf shape (exactly three top-level keys, nothing else):

        {
          "note": {**intent.model_dump(mode="json"),
                   "content_id": note_intent_content_id(intent)},
          "target_path": intent.target_path,
          "source_ref": [distinct source_refs from provenance, first-seen order],
        }

    - ``"note"``: the full JSON-mode dump of the typed intent (lossless for
      P2b) plus the reused content id. ``model_dump(mode="json")`` is
      deterministic (tuples → lists, Literals → str).
    - ``"target_path"``: ``intent.target_path`` verbatim (the same relative
      path the overlay writer will confine).
    - ``"source_ref"``: distinct source refs from provenance in first-seen
      order (``dict.fromkeys``). Provenance is non-empty by model rule, so
      this list is always non-empty. The full span_id→source_ref mapping
      stays inside ``"note"`` for lossless downstream use.

    Leaves carry no ``"_id"`` key — compatible with
    :func:`scheduler.run_pipeline_dynamic`, which auto-injects
    ``_id = f"leaf_{i}"`` when absent (scheduler.py:621-623), so P2b can feed
    these straight in.
    """
    leaves: list[dict] = []
    for intent in graph.intents:
        note_payload = dict(intent.model_dump(mode="json"))
        note_payload["content_id"] = note_intent_content_id(intent)
        source_refs = list(
            dict.fromkeys(p.source_ref for p in intent.provenance)
        )
        leaves.append(
            {
                "note": note_payload,
                "target_path": intent.target_path,
                "source_ref": source_refs,
            }
        )
    return leaves


# ── P2b (A2.1): SourceBundle — a document set admitted as ONE objective ─────


class BundleMember(BaseModel):
    """One member of a :class:`SourceBundle`.

    ``ordinal`` fixes the member's position in the objective (members are
    stored in ascending-ordinal canonical order so the bundle content hash is
    order-independent of admission order). ``ref`` is the member's source
    reference (path/URL); ``extracted_text_hash`` pins the parsed content.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    source_id: str = Field(min_length=1)
    ordinal: int = Field(ge=0)
    ref: str = Field(min_length=1)
    parser_id: str = Field(min_length=1)
    extracted_text_hash: str = Field(min_length=1)
    provenance: str = ""


class SourceBundle(BaseModel):
    """A set of sources admitted as ONE coordinated objective (P2b, A2.1).

    This is the parent that :attr:`NoteIntentGraph.objective_id` points at. A
    bundle is admitted as a single objective — never inferred from a directory
    scan. Members are normalized into ascending-ordinal order at construction
    so :func:`bundle_content_hash` is independent of admission order.

    Validators (``model_validator(mode="after")``): ordinals are unique;
    members are re-sorted into canonical ascending-ordinal order.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    bundle_id: str = Field(min_length=1)
    objective: str = Field(min_length=1)
    members: tuple[BundleMember, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _normalize_members(self) -> "SourceBundle":
        ordinals = [m.ordinal for m in self.members]
        if len(set(ordinals)) != len(ordinals):
            raise ValueError("SourceBundle members must have unique ordinals")
        ordered = tuple(sorted(self.members, key=lambda m: m.ordinal))
        if ordered != self.members:
            # frozen model → rebuild via object.__setattr__ on the validated copy
            object.__setattr__(self, "members", ordered)
        return self


def bundle_content_hash(bundle: SourceBundle) -> str:
    """Deterministic content id for a bundle (P2b, A2.1).

    ``sha256`` over :func:`proposals.canonical_json_bytes` of the bundle's
    JSON dump (float-banned, NFC-normalized, order-independent). Pure — no
    clock/random/IO — so re-admitting the same members yields the same id.
    """
    return hashlib.sha256(
        canonical_json_bytes(bundle.model_dump(mode="json"))
    ).hexdigest()


__all__ = [
    "ClaimProvenance",
    "NoteDisposition",
    "NoteIntent",
    "NoteIntentGraph",
    "note_intent_content_id",
    "project_note_intent_graph",
    # P2b (A2.1) — SourceBundle
    "BundleMember",
    "SourceBundle",
    "bundle_content_hash",
]
