"""Create-only staging OVERLAY writer for typed note intents.

Phase **P2** (A2.5) of "Dynamic Digestion as a Snapshot-Pinned Knowledge
Transaction". An :class:`OverlayWriter` materializes a
:class:`tessellum.composer.knowledge_plan.NoteIntent` (``"create"``
disposition) into a PRIVATE overlay directory — NEVER the live vault. This is
the fail-closed, unit-testable staging surface that P2b will promote from;
this module has NO promotion, NO update, and NO delete path.

Key guarantees:

* **CREATE-ONLY.** Any non-``"create"`` disposition, or a create whose target
  already exists (in the overlay OR, when a base vault is given for the
  collision check, in the base vault), fails closed with :class:`OverlayError`.
  Create means the note must NOT already exist.
* **OVERLAY-ONLY.** The sole write is :func:`materializer._atomic_write_bytes`
  to an ``overlay_path`` that is ``relative_to(overlay_root)``-verified.
  ``base_vault_root`` is stat-read ONLY (the collision check) — there is no
  code path from it (or any vault root) to a write. The live vault cannot be
  written by this module.
* **PATH CONFINEMENT.** ``_resolve_overlay_path`` mirrors
  :func:`materializer._resolve_vault_path`: absolute paths and ``..`` escapes
  raise :class:`OverlayError` before any I/O.
* **ROLLBACK PARITY (optional).** An optional, DUCK-TYPED effect recorder
  (the exact ``VaultEffectJournal``-style contract
  :func:`materializer._record_effect` already expects: a callable
  ``record(path)`` plus an optional ``.record_postimage(path, bytes)``) is
  invoked for rollback parity. It is NOT required, and this module never
  imports the concrete :class:`tessellum.runtime.executor.VaultEffectJournal`
  — keeping the composer import DAG acyclic (composer never imports runtime).

Reuses the SHIPPED atomic write primitive
(:func:`materializer._atomic_write_bytes`: tmp-file + fsync + ``os.replace`` +
dir fsync), retargeted at ``overlay_root`` via the confined path.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from tessellum.composer.knowledge_plan import NoteIntent
from tessellum.composer.materializer import _atomic_write_bytes, _record_effect
from tessellum.composer.proposals import canonical_json_bytes


class OverlayError(Exception):
    """Raised when the overlay writer refuses or cannot perform a write.

    Dedicated typed error (mirrors :class:`materializer.MaterializerError`) so
    overlay failures are distinguishable from materializer failures. Cases:
    non-create disposition, a create-collision (overlay or base vault), a
    non-relative or escaping ``target_path``, or a ``create`` carrying an
    ``expected_preimage``.
    """


@dataclass(frozen=True)
class OverlayWriteResult:
    """The result of materializing one :class:`NoteIntent` into the overlay.

    Attributes:
        overlay_path: The absolute path written under ``overlay_root``.
        target_path: The vault-relative path from the intent (verbatim).
        content_hash: ``sha256`` hex of the written bytes (raw-bytes digest,
            consistent with ``VaultEffectJournal.record_postimage``).
        created: Always ``True`` on success — this writer is create-only.
    """

    overlay_path: Path
    target_path: str
    content_hash: str
    created: bool


class OverlayWriter:
    """Materializes create-disposition note intents into a private overlay.

    The overlay is a staging directory disjoint from the live vault. This
    writer NEVER writes outside ``overlay_root``; ``base_vault_root`` (when
    supplied) is used ONLY for a read-only create-collision check.
    """

    def __init__(
        self,
        overlay_root: Path,
        *,
        base_vault_root: Path | None = None,
        effect_recorder: Callable[[Path], None] | None = None,
    ) -> None:
        """Args:
        overlay_root: Private staging directory. The ONLY write target.
        base_vault_root: Optional live-vault root, READ-ONLY, for the
            create-collision check (``.exists()`` stat). NEVER written.
        effect_recorder: Optional duck-typed ``VaultEffectJournal``-style
            recorder (callable ``record(path)`` + optional
            ``.record_postimage(path, bytes)``) for rollback parity. Optional;
            not required. Not the concrete runtime journal — duck-typed so
            this module never imports runtime.
        """
        self._overlay_root = Path(overlay_root).resolve()
        self._base_vault_root = (
            Path(base_vault_root).resolve() if base_vault_root is not None else None
        )
        self._recorder = effect_recorder

    @staticmethod
    def _resolve_confined(root: Path, value: str, *, root_label: str) -> Path:
        """Resolve a relative ``value`` under ``root`` and confine it there.

        Mirrors :func:`materializer._resolve_vault_path` (:168-179) but raises
        :class:`OverlayError`. Absolute paths and ``..`` escapes are rejected
        BEFORE any I/O.
        """
        supplied = Path(str(value))
        if supplied.is_absolute():
            raise OverlayError(
                f"target_path must be relative (not absolute): {value!r}"
            )
        target = (root / supplied).resolve()
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise OverlayError(
                f"target_path escapes {root_label}: {value!r}"
            ) from exc
        return target

    def _build_stub_bytes(self, intent: NoteIntent) -> bytes:
        """Compose deterministic materialized bytes when no body is given.

        No clock/random: a ``---\\n<canonical yaml-ish>\\n---\\n<thesis>``
        frontmatter+body built from the already-typed, float-free
        :class:`NoteIntent` fields. The frontmatter surface is the canonical
        (sorted-key, float-free, NFC-normalized) serialization of the intent's
        identity/coverage fields via :func:`proposals.canonical_json_bytes`,
        so it inherits the P0 canonicalization guarantees. (No rendered agent
        content exists in this pure core; P2b supplies the real body.)
        """
        frontmatter_surface = {
            "note_id": intent.note_id,
            "building_block": intent.building_block,
            "disposition": intent.disposition,
            "target_path": intent.target_path,
            "coverage": list(intent.coverage),
            "depends_on": list(intent.depends_on),
            "relevance_links": list(intent.relevance_links),
            "navigation": list(intent.navigation),
            "required_inlinks": list(intent.required_inlinks),
            "provenance": [
                {"span_id": p.span_id, "source_ref": p.source_ref}
                for p in intent.provenance
            ],
        }
        frontmatter = canonical_json_bytes(frontmatter_surface).decode("utf-8")
        body = intent.thesis
        return f"---\n{frontmatter}\n---\n{body}".encode("utf-8")

    def materialize(
        self, intent: NoteIntent, *, body: str | None = None
    ) -> OverlayWriteResult:
        """Write ``intent`` (create disposition) into the overlay — fail-closed.

        Args:
            intent: The typed :class:`NoteIntent` to stage. Must be a
                ``"create"`` (the model already enforces this; this method
                re-checks defensively).
            body: Optional exact note body. When ``None``, a deterministic
                stub is composed from the intent (see :meth:`_build_stub_bytes`).

        Returns:
            :class:`OverlayWriteResult` on success (``created=True``).

        Raises:
            OverlayError: non-create disposition, a create carrying an
                ``expected_preimage``, a create-collision (overlay or base
                vault), or a non-relative / escaping ``target_path``.
        """
        # 1. CREATE-ONLY defense-in-depth. The model enforces this, but the
        #    writer re-checks so a future enum change can't silently write a
        #    non-create through this path.
        if intent.disposition != "create":
            raise OverlayError(
                f"OverlayWriter is create-only; got disposition "
                f"{intent.disposition!r}"
            )
        # 2. A create must carry no preimage (the target must not exist).
        if intent.expected_preimage is not None:
            raise OverlayError(
                "create requires no expected_preimage; the target must not exist"
            )

        # 3. Path confinement + escape rejection (before any I/O).
        overlay_path = self._resolve_confined(
            self._overlay_root, intent.target_path, root_label="overlay_root"
        )

        # 4. FAIL-CLOSED create-collision (create ⇒ the note must NOT exist).
        if overlay_path.exists():
            raise OverlayError(
                f"create target already exists in overlay: {intent.target_path}"
            )
        if self._base_vault_root is not None:
            base_path = self._resolve_confined(
                self._base_vault_root,
                intent.target_path,
                root_label="base_vault_root",
            )
            # READ-only stat; the base vault is NEVER written.
            if base_path.exists():
                raise OverlayError(
                    f"create target already exists in base vault: "
                    f"{intent.target_path}"
                )

        # 5. Compose bytes deterministically (no clock/random).
        if body is not None:
            content = body.encode("utf-8")
        else:
            content = self._build_stub_bytes(intent)

        # 6. Raw-bytes digest (consistent with VaultEffectJournal.record_postimage,
        #    executor.py:165) — NOT the canonical-json hashing reserved for the
        #    intent content id.
        content_hash = hashlib.sha256(content).hexdigest()

        # 7. Rollback parity (optional): the exact materializer recorder
        #    contract — no-op when no recorder was supplied.
        if self._recorder is not None:
            _record_effect(self._recorder, overlay_path, content)

        # 8. The SOLE write — the shipped atomic primitive, retargeted at the
        #    confined overlay path (tmp + fsync + os.replace + dir fsync).
        _atomic_write_bytes(overlay_path, content)

        return OverlayWriteResult(
            overlay_path=overlay_path,
            target_path=intent.target_path,
            content_hash=content_hash,
            created=True,
        )


__all__ = ["OverlayWriter", "OverlayError", "OverlayWriteResult"]
