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
import re
from dataclasses import dataclass, field
from pathlib import Path

# Alphanumeric (incl. underscore) token runs — everything else (FTS5-special
# punctuation: - : " ( ) # * ^ etc., and markdown/YAML markers) is dropped so a
# source-derived query can never be an FTS5 syntax error.
_FTS5_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")
# Cap the number of query terms — a 512-char head can hold ~80 tokens; a long
# OR-bag both dilutes relevance and slows MATCH. First N content tokens.
_MAX_QUERY_TERMS = 32


def _fts5_safe_query(text: str) -> str:
    """Reduce arbitrary text to a valid FTS5 query: the first
    :data:`_MAX_QUERY_TERMS` alphanumeric tokens, lowercased, joined by the
    ``OR`` operator.

    Two properties matter:

    - **Safe.** Tokens are ``[A-Za-z0-9_]`` runs only — every FTS5-special char
      (``- : " ( ) # * ^`` and YAML/markdown markers) is dropped, so the result
      can never be a MATCH syntax error.
    - **Recall.** ``OR`` (not the space-implicit ``AND``) joins the terms: a
      source-head query carries frontmatter noise (``title``/``tags``/…) that
      appears in NO note body, so an implicit-AND bag would require every token
      present in one doc and match nothing. ``OR`` lets any term contribute a
      hit; BM25 then ranks the seeds by relevance. Terms are lowercased so a
      token equal to ``and``/``or``/``not`` is a bareword literal, never an
      operator (FTS5 operators must be uppercase).

    Returns ``""`` when no usable token remains."""
    if not isinstance(text, str):
        return ""
    tokens = _FTS5_TOKEN_RE.findall(text.lower())
    return " OR ".join(tokens[:_MAX_QUERY_TERMS])

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


# Fraction of the context budget reserved for retrieved related-note context
# (the rest stays for the source). Kept modest so retrieval AUGMENTS, never
# crowds out, the primary source the writer is digesting.
DEFAULT_RETRIEVAL_BUDGET_FRACTION: float = 0.25

# Retrieval-neighborhood defaults for the augmenting assembler.
DEFAULT_RETRIEVAL_SEEDS: int = 5      # hybrid top-K used as BFS seeds
DEFAULT_RETRIEVAL_NEIGHBORS: int = 8  # BFS neighbors per seed (best-first)


class RetrievalAugmentedAssembler(ContextAssembler):
    """The graph-retrieval assembler the module header anticipated (WIRING).

    Turns the composer's input seam into a hybrid-retrieval consumer: before
    the writer sees the source, this PREPENDS a bounded "Related vault notes"
    block gathered from the indexed vault via the FULL hybrid stack —

    - **hybrid_search** (BM25 + dense, RRF-fused) picks the top ``seeds`` most
      relevant existing notes to the query; then
    - **best_first_bfs** expands each seed's neighborhood over the note-link
      graph (priority queue, depth-major + in_degree-minor, hub-skipped), so
      the writer also sees structurally-adjacent context, not just lexical/
      semantic top hits — the multi-hop surface the vault's search skill calls
      Best-First BFS.

    The block is capped to ``retrieval_fraction`` of ``max_chars`` (the source
    keeps the rest), deduped by note_id, and clearly delimited so the writer
    treats it as REFERENCE context, not the source of record.

    **Fail-soft + opt-in.** Constructed only when a caller selects the
    ``"retrieval"`` strategy AND supplies a ``db_path``; the default assembler
    is unchanged. ANY retrieval failure (missing index, missing dense embeddings
    — dense simply drops per hybrid's own fallback, unreadable DB) degrades to
    the bare source with a warning — retrieval never crashes a write. The query
    defaults to the source's head (the note being written is about its own
    opening); a caller can inject an explicit ``query``.
    """

    def __init__(
        self,
        *,
        max_chars: int = DEFAULT_MAX_CONTEXT_CHARS,
        db_path: "Path | str | None" = None,
        query: str | None = None,
        seeds: int = DEFAULT_RETRIEVAL_SEEDS,
        neighbors: int = DEFAULT_RETRIEVAL_NEIGHBORS,
        retrieval_fraction: float = DEFAULT_RETRIEVAL_BUDGET_FRACTION,
    ) -> None:
        super().__init__(max_chars=max_chars)
        if not (0.0 < retrieval_fraction < 1.0):
            raise ValueError("retrieval_fraction must be in (0, 1)")
        self.db_path = Path(db_path) if db_path is not None else None
        self.query = query
        self.seeds = max(1, seeds)
        self.neighbors = max(0, neighbors)
        self.retrieval_fraction = retrieval_fraction
        # A fail-soft warning to surface on the NEXT assemble() (retrieval was
        # requested but degraded to bare source). Reset at the top of each
        # assemble() call; merged into the AssembledContext.warnings there.
        # Assemblers are single-active (one write at a time) per the seam's
        # contract, so a single-slot pending warning is safe.
        self._pending_warning: str | None = None

    _BLOCK_HEADER = (
        "## Related vault notes (retrieved context — reference only, "
        "NOT the source of record)\n"
    )

    @property
    def strategy(self) -> str:
        return "retrieval"

    def assemble(self, source: str) -> AssembledContext:
        """Assemble with retrieval augmentation, then surface any fail-soft
        retrieval warning alongside the base size warnings.

        The base :meth:`ContextAssembler.assemble` only knows about
        size/type warnings; a retrieval degradation (missing/broken index,
        empty query, dense-drop) is recorded by :meth:`_related_block` /
        :meth:`_assemble_raw` in ``self._pending_warning`` and merged in here so
        the worker can log that augmentation silently fell back to bare source.
        """
        self._pending_warning = None
        result = super().assemble(source)
        if self._pending_warning is None:
            return result
        return AssembledContext(
            text=result.text,
            truncated=result.truncated,
            original_chars=result.original_chars,
            warnings=result.warnings + (self._pending_warning,),
        )

    def _query_for(self, source: str) -> str:
        """The retrieval query: the injected query, else the source head —
        SANITIZED into a valid FTS5 bag-of-words.

        A raw note source begins with YAML frontmatter (``---``), markdown
        headers (``#``), and punctuation (``:``, ``(``, quotes) — all FTS5
        syntax errors that would make ``bm25_search``'s ``MATCH`` raise and
        silently no-op the whole retrieval. So the query is reduced to
        alphanumeric content tokens joined by spaces (an implicit FTS5 AND/OR
        over bare terms — no operators), which can never be a syntax error.
        Returns ``""`` when nothing usable remains (caller skips retrieval)."""
        raw = self.query if self.query else source[:512]
        return _fts5_safe_query(raw)

    def _related_note_ids(self, source: str) -> list[str]:
        """Retrieve the ordered related note-ids via hybrid + BFS.

        Returns ``[]`` on any degradation (no db configured, empty query,
        missing/broken index, no hits), recording a fail-soft warning in
        ``self._pending_warning`` when retrieval was ATTEMPTED but yielded
        nothing usable — so the caller degrades to bare source AND the worker
        can see that augmentation silently fell back."""
        if self.db_path is None:
            return []
        # Lazy import: retrieval pulls sqlite_vec / networkx; keep the composer
        # import DAG light for callers that never use the retrieval strategy.
        from tessellum.retrieval.graph import best_first_bfs
        from tessellum.retrieval.hybrid import hybrid_search

        query = self._query_for(source)
        if not query:
            self._pending_warning = (
                "retrieval degraded: query reduced to empty after FTS5 "
                "sanitization; using bare source"
            )
            return []
        try:
            hits = hybrid_search(self.db_path, query, k=self.seeds)
        except Exception as e:  # noqa: BLE001 — index failure degrades, not kills
            self._pending_warning = (
                f"retrieval degraded: hybrid_search failed "
                f"({type(e).__name__}); using bare source"
            )
            return []
        if not hits:
            self._pending_warning = (
                "retrieval degraded: no related notes found; using bare source"
            )
            return []
        # first-seen dedup: hybrid seeds first (most relevant), then each seed's
        # best-first neighborhood, so the block reads relevance-ordered.
        ordered: list[str] = []
        seen: set[str] = set()
        for h in hits:
            if h.note_id not in seen:
                seen.add(h.note_id)
                ordered.append(h.note_id)
        if self.neighbors:
            for h in hits:
                try:
                    neigh = best_first_bfs(self.db_path, h.note_id, k=self.neighbors)
                except Exception:  # noqa: BLE001 — a bad seed never sinks the block
                    continue
                for g in neigh:
                    if g.note_id not in seen:
                        seen.add(g.note_id)
                        ordered.append(g.note_id)
        return ordered

    def _render_block(self, note_ids: list[str], block_budget: int) -> str:
        """Render the related-notes block to fit ``block_budget`` chars by
        dropping WHOLE note lines from the tail — never char-slicing (which
        would cut the anti-fabrication header mid-string). Returns "" if not
        even the header + one line fits, so the disclaimer is all-or-nothing."""
        header = self._BLOCK_HEADER
        kept: list[str] = []
        # +1 for the trailing "\n\n" the joined block ends with.
        size = len(header) + 1
        for nid in note_ids:
            line = f"- {nid}\n"
            if size + len(line) > block_budget:
                break
            kept.append(line)
            size += len(line)
        if not kept:
            return ""  # header alone (or +1 line) won't fit → drop whole block
        if len(kept) < len(note_ids):
            self._pending_warning = (
                f"retrieval block trimmed to {len(kept)}/{len(note_ids)} "
                f"notes to fit the source-first budget"
            )
        return header + "".join(kept) + "\n"

    def _assemble_raw(self, source: str) -> str:
        # Retrieval is best-effort: never let it crash assembly (the base class
        # also guards, but we degrade to bare source explicitly here too so a
        # retrieval failure yields the FULL source, not an empty context).
        try:
            note_ids = self._related_note_ids(source)
        except Exception as e:  # noqa: BLE001
            self._pending_warning = (
                f"retrieval degraded ({type(e).__name__}); using bare source"
            )
            note_ids = []
        if not note_ids:
            return source
        # SOURCE-FIRST budgeting. The source is the record the writer must
        # digest; augmentation must NEVER evict it. The base assemble() bounds
        # the whole output to max_chars by truncating from the END — so a
        # prepended block that pushes block+source over max_chars would drop the
        # SOURCE tail. Guard against that here: the block gets at most its
        # fraction AND at most the room the source leaves; if the source alone
        # already fills (or overflows) max_chars, the block is dropped entirely
        # so the base truncation only ever trims the source, never loses it to
        # retrieved context. (The base then still windows an oversized source.)
        room_for_block = self.max_chars - len(source)
        block_budget = min(int(self.max_chars * self.retrieval_fraction), room_for_block)
        if block_budget <= 0:
            self._pending_warning = (
                "retrieval block dropped: source fills the char budget; "
                "source preserved (never evicted for retrieved context)"
            )
            return source  # no room without evicting source → source-only
        block = self._render_block(note_ids, block_budget)
        if not block:
            self._pending_warning = (
                "retrieval block dropped: does not fit the source-first "
                "budget without char-slicing the disclaimer header"
            )
            return source
        return block + source


# Registry so the driver selects an assembler by config string.
ASSEMBLER_REGISTRY: dict[str, type[ContextAssembler]] = {
    "full_source": FullSourceAssembler,
    "windowed": WindowedAssembler,
    "retrieval": RetrievalAugmentedAssembler,
}


def get_assembler(
    strategy: str = "full_source",
    *,
    max_chars: int = DEFAULT_MAX_CONTEXT_CHARS,
    db_path: "Path | str | None" = None,
    query: str | None = None,
) -> ContextAssembler:
    """Construct the single-active assembler by config string.

    ``db_path`` / ``query`` are consumed only by the ``"retrieval"`` strategy
    (the :class:`RetrievalAugmentedAssembler`); the source-only strategies
    (``full_source`` / ``windowed``) ignore them, so existing callers are
    unaffected. Selecting ``"retrieval"`` without a ``db_path`` yields an
    assembler that simply passes the source through (fail-soft).

    Raises:
        KeyError: If ``strategy`` is not registered.
    """
    cls = ASSEMBLER_REGISTRY[strategy]
    if cls is RetrievalAugmentedAssembler:
        return cls(max_chars=max_chars, db_path=db_path, query=query)
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
