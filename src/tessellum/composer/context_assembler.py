"""Context assembler — the input-side seam, config-selected + fail-soft.

Composer v4, Phase 6 (context half). A single-active :class:`ContextAssembler`
ABC that assembles the source context a capture step sees, selected by
config so a deployment can swap *full-source* vs *windowed* (vs a future
graph-retrieval assembler) **without touching the executor** — the swap is
guarded by a shared contract test (every assembler obeys the same
`assemble` contract + bounds).

Three hardening properties every assembler inherits:

1. **Percentage-scaled fail-soft bounds.** An oversized or malformed
   source degrades (truncates + warns) rather than crashing a worker —
   one bad source never takes down a wave. The cap is a character budget;
   the assembler truncates to it and records a warning.
2. **Preflight estimate.** :meth:`ContextAssembler.estimate_chars` gives a
   cheap size estimate before the (expensive) assemble, so the caller can
   route/skip on size.
3. **Read-path hardening.** :func:`is_safe_read_path` enforces a
   sensitive-path denylist + workspace confinement + binary detection, so
   the assembler refuses to read a credential file, escape the workspace,
   or slurp a binary blob.

No LLM, no network — pure assembly + I/O guards (IDENT-3).
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from pathlib import Path

# Character budget an assembled context must not exceed. The assembler
# truncates to this and warns rather than raising.
DEFAULT_MAX_CONTEXT_CHARS: int = 200_000

# Fraction of the cap at which a still-under-budget-but-large source earns
# a soft warning (early smoke signal before an actual truncation).
SOFT_WARN_FRACTION: float = 0.9

# Path segments that must never be read as source (a denylist, matched
# case-insensitively against any path part or the filename).
SENSITIVE_PATH_MARKERS: tuple[str, ...] = (
    ".env",
    ".aws",
    ".ssh",
    "credentials",
    "id_rsa",
    "secrets",
    ".pem",
    ".key",
    ".netrc",
    ".git",
)


@dataclass
class AssembledContext:
    """The output of :meth:`ContextAssembler.assemble`.

    Attributes:
        text: The assembled context string (already within the cap).
        truncated: ``True`` iff the source exceeded the cap and was cut.
        original_chars: The pre-truncation source length.
        warnings: Fail-soft warnings (oversized/near-cap/malformed) — the
            worker logs these but is never crashed by them.
    """

    text: str
    truncated: bool = False
    original_chars: int = 0
    warnings: tuple[str, ...] = field(default_factory=tuple)


class ContextAssembler(abc.ABC):
    """Single-active context-assembly strategy (the swappable seam).

    Subclasses implement :meth:`_assemble_raw` (the strategy) and inherit
    the fail-soft bounding + preflight estimate. ``max_chars`` is the
    character budget; the assembled text is always ``<= max_chars``.
    """

    def __init__(self, *, max_chars: int = DEFAULT_MAX_CONTEXT_CHARS) -> None:
        if max_chars <= 0:
            raise ValueError("max_chars must be positive")
        self.max_chars = max_chars

    @property
    @abc.abstractmethod
    def strategy(self) -> str:
        """A short strategy id (e.g. ``"full_source"`` / ``"windowed"``)."""

    @abc.abstractmethod
    def _assemble_raw(self, source: str) -> str:
        """Strategy-specific assembly of the (already-read) source string.

        Must not enforce the cap — the base :meth:`assemble` bounds the
        result uniformly so every strategy shares one fail-soft policy.
        """

    def estimate_chars(self, source: str) -> int:
        """Cheap preflight size estimate (default: raw length)."""
        return len(source)

    def assemble(self, source: str) -> AssembledContext:
        """Assemble + fail-soft bound ``source``. Never raises on size.

        A ``None``/non-string source degrades to an empty context with a
        warning (fail-soft). Over the cap → truncate + warn; near the cap
        (≥ :data:`SOFT_WARN_FRACTION`) → a soft warning without truncation.
        """
        warnings: list[str] = []
        if not isinstance(source, str):
            return AssembledContext(
                text="",
                truncated=False,
                original_chars=0,
                warnings=("source was not a string; degraded to empty context",),
            )

        try:
            assembled = self._assemble_raw(source)
        except Exception as e:  # noqa: BLE001 — a strategy crash degrades, not kills
            return AssembledContext(
                text="",
                truncated=False,
                original_chars=len(source),
                warnings=(f"assembler strategy failed ({type(e).__name__}); "
                          f"degraded to empty context",),
            )

        original = len(assembled)
        truncated = False
        if original > self.max_chars:
            assembled = assembled[: self.max_chars]
            truncated = True
            warnings.append(
                f"source exceeded {self.max_chars} chars ({original}); truncated"
            )
        elif original >= int(self.max_chars * SOFT_WARN_FRACTION):
            warnings.append(
                f"source is near the {self.max_chars}-char cap ({original})"
            )

        return AssembledContext(
            text=assembled,
            truncated=truncated,
            original_chars=original,
            warnings=tuple(warnings),
        )


class FullSourceAssembler(ContextAssembler):
    """Pass the whole source through (bounded by the base cap)."""

    @property
    def strategy(self) -> str:
        return "full_source"

    def _assemble_raw(self, source: str) -> str:
        return source


class WindowedAssembler(ContextAssembler):
    """Keep the head + tail windows, dropping the (often less salient) middle.

    Useful when a source is far larger than the budget and the ends
    (frontmatter / intro + conclusion / references) carry the most signal.
    Emits a clear ``[... middle elided ...]`` marker so the model knows a
    gap exists.
    """

    def __init__(
        self,
        *,
        max_chars: int = DEFAULT_MAX_CONTEXT_CHARS,
        head_fraction: float = 0.6,
    ) -> None:
        super().__init__(max_chars=max_chars)
        if not 0.0 < head_fraction < 1.0:
            raise ValueError("head_fraction must be in (0, 1)")
        self.head_fraction = head_fraction

    @property
    def strategy(self) -> str:
        return "windowed"

    def _assemble_raw(self, source: str) -> str:
        if len(source) <= self.max_chars:
            return source
        marker = "\n\n[... middle elided ...]\n\n"
        budget = self.max_chars - len(marker)
        if budget <= 0:
            return source[: self.max_chars]
        head_n = int(budget * self.head_fraction)
        tail_n = budget - head_n
        return source[:head_n] + marker + source[len(source) - tail_n :]


# Registry so the driver selects an assembler by config string.
ASSEMBLER_REGISTRY: dict[str, type[ContextAssembler]] = {
    "full_source": FullSourceAssembler,
    "windowed": WindowedAssembler,
}


def get_assembler(
    strategy: str = "full_source", *, max_chars: int = DEFAULT_MAX_CONTEXT_CHARS
) -> ContextAssembler:
    """Construct the single-active assembler by config string.

    Raises:
        KeyError: If ``strategy`` is not registered.
    """
    cls = ASSEMBLER_REGISTRY[strategy]
    return cls(max_chars=max_chars)


# ── Read-path hardening ─────────────────────────────────────────────────────


def is_safe_read_path(path: Path | str, *, workspace_root: Path | str) -> bool:
    """Whether ``path`` is safe to read as source (deny secrets/escapes/binaries).

    Fail-closed: returns ``False`` on any of —

    - **Sensitive marker.** Any path part or the filename matches a
      :data:`SENSITIVE_PATH_MARKERS` entry (``.env``, ``.aws``,
      credentials, keys, ``.git``, …).
    - **Workspace escape.** The resolved path is not under the resolved
      ``workspace_root`` (blocks ``../`` traversal + absolute escapes).
    - **Binary.** The file exists and its first chunk contains a NUL byte
      (a cheap binary sniff) — we don't feed binary blobs to a model.

    A path that is under the workspace, non-sensitive, and either
    absent-or-text returns ``True``.
    """
    p = Path(path)
    root = Path(workspace_root).resolve()

    # Sensitive markers — check every part + the name, case-insensitively.
    lowered_parts = [part.lower() for part in p.parts]
    name_lower = p.name.lower()
    for marker in SENSITIVE_PATH_MARKERS:
        if any(marker in part for part in lowered_parts) or marker in name_lower:
            return False

    # Workspace confinement.
    try:
        resolved = p.resolve()
    except (OSError, RuntimeError):
        return False
    if not _is_relative_to(resolved, root):
        return False

    # Binary sniff (only when the file exists).
    if resolved.is_file():
        try:
            with open(resolved, "rb") as f:
                chunk = f.read(8192)
            if b"\x00" in chunk:
                return False
        except OSError:
            return False

    return True


def _is_relative_to(path: Path, root: Path) -> bool:
    """``Path.is_relative_to`` backport-safe check."""
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


__all__ = [
    "DEFAULT_MAX_CONTEXT_CHARS",
    "SOFT_WARN_FRACTION",
    "SENSITIVE_PATH_MARKERS",
    "AssembledContext",
    "ContextAssembler",
    "FullSourceAssembler",
    "WindowedAssembler",
    "ASSEMBLER_REGISTRY",
    "get_assembler",
    "is_safe_read_path",
]
