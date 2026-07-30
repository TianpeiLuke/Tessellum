"""Materializer dispatch — applies the agent's response to the filesystem.

Five concrete materializers, one per ``MaterializerContract`` registered
in :data:`tessellum.composer.contracts.MATERIALIZER_CONTRACTS`:

  no_op                              DESCRIBE — parse JSON, no side effect
  body_markdown_to_file              PRODUCE — JSON envelope, write body_markdown
  body_markdown_frontmatter_to_file  PRODUCE — markdown-with-frontmatter direct write
  edits_apply_to_files               APPLY — JSON {edits: [...]}, overwrite each
  edits_apply_xml_tags               APPLY — <edits><edit><file>…</file><content>…</content></edit></edits>

Each materializer:

  - Parses the agent's raw response text into a structured payload.
  - Writes / applies files under ``vault_root`` (skipped when ``dry_run=True``).
  - Returns a ``MaterializedOutput`` carrying the structured payload (for
    downstream ``{{upstream.X}}`` resolution) plus diagnostic info
    (which files were written, human-readable notes).

Materializer errors raise :class:`MaterializerError`. Callers catch
this, surface it on the step's ``StepResult.error``, and continue —
one bad step doesn't kill the whole pipeline.
"""

from __future__ import annotations

import json
import os
import re
import stat
import uuid
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, ContextManager

import yaml


def _fsync_dir(path: Path) -> None:
    try:
        descriptor = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _ensure_directory_durable(path: Path) -> None:
    missing: list[Path] = []
    current = path
    while not current.exists():
        missing.append(current)
        current = current.parent
    for directory in reversed(missing):
        directory.mkdir()
        _fsync_dir(directory.parent)


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    _ensure_directory_durable(path.parent)
    mode = stat.S_IMODE(path.stat().st_mode) if path.is_file() else None
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(temporary, mode)
        os.replace(temporary, path)
        _fsync_dir(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def _record_effect(
    recorder: Callable[[Path], None],
    path: Path,
    content: bytes,
) -> None:
    recorder(path)
    record_postimage = getattr(recorder, "record_postimage", None)
    if record_postimage is not None:
        record_postimage(path, content)


class MaterializerError(Exception):
    """Raised when a materializer cannot apply the agent's response.

    Cases: malformed wire format (bad JSON, missing XML tags), missing
    required fields (no ``output_path``, no ``edits``), unknown
    materializer key. Recoverable in the sense that the executor
    catches it and reports per-step; non-recoverable for that one step.
    """


@dataclass(frozen=True)
class MaterializedOutput:
    """The result of applying one step's response.

    Attributes:
        structured: Parsed dict form of the agent's response. Used as
            the value of ``upstream.<output_key>`` for downstream steps.
        files_written: Paths that were created/overwritten with new
            content (PRODUCE mode). Empty if ``dry_run=True``.
        files_applied: Paths that had existing content overwritten by
            edits (APPLY mode). Empty if ``dry_run=True``.
        notes: Short human-readable summary for trace logs.
    """

    structured: dict[str, Any]
    files_written: tuple[Path, ...] = ()
    files_applied: tuple[Path, ...] = ()
    notes: str = ""


# ── Public dispatch ────────────────────────────────────────────────────────


def materialize(
    materializer_key: str,
    response_text: str,
    *,
    vault_root: Path,
    dry_run: bool = False,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    effect_recorder: Callable[[Path], None] | None = None,
    leaf: dict | None = None,
) -> MaterializedOutput:
    """Dispatch ``response_text`` to the materializer for ``materializer_key``.

    Args:
        materializer_key: Must be a key in
            :data:`tessellum.composer.contracts.MATERIALIZER_CONTRACTS`.
        response_text: Raw agent response.
        vault_root: Root directory for resolving relative paths in the
            response.
        dry_run: If True, skip all filesystem writes. The structured
            payload is still returned so downstream placeholders resolve
            correctly during a dry run.

    Returns:
        MaterializedOutput with structured + files written/applied.

    Raises:
        MaterializerError: malformed response, unknown key.
    """
    handler = _DISPATCH.get(materializer_key)
    if handler is None:
        raise MaterializerError(
            f"unknown materializer key {materializer_key!r}. "
            f"Known: {sorted(_DISPATCH)}"
        )
    # k2a4a: sibling-link healing at write time (the F9/F10 absorption
    # pattern applied to links) — only for note-body materializers, only
    # when the leaf carries the planned-sibling list.
    if (
        isinstance(leaf, dict)
        and leaf.get("planned_siblings_md")
        and materializer_key in ("body_markdown_to_file",
                                 "body_markdown_frontmatter_to_file")
    ):
        response_text = _heal_sibling_links(
            response_text, str(leaf["planned_siblings_md"])
        )
    return handler(
        response_text,
        vault_root,
        dry_run,
        effect_guard or nullcontext,
        effect_recorder or (lambda _path: None),
    )


# ── Concrete materializers ─────────────────────────────────────────────────


def _resolve_vault_path(vault_root: Path, value: object, *, field: str) -> Path:
    """Resolve an agent-supplied relative path and confine it to the vault."""
    root = Path(vault_root).resolve()
    supplied = Path(str(value))
    if supplied.is_absolute():
        raise MaterializerError(f"{field} must be relative to vault_root")
    target = (root / supplied).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise MaterializerError(f"{field} escapes vault_root: {value}") from exc
    return target


def _no_op(
    text: str,
    vault_root: Path,
    dry_run: bool,
    effect_guard: Callable[[], ContextManager[None]],
    effect_recorder: Callable[[Path], None],
) -> MaterializedOutput:
    """DESCRIBE materializer — parse JSON, no side effect."""
    if not text.strip():
        return MaterializedOutput(structured={}, notes="no_op (empty response)")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Tolerant: wrap non-JSON text so downstream placeholders still resolve.
        data = {"text": text}
    if not isinstance(data, dict):
        data = {"value": data}
    return MaterializedOutput(structured=data, notes="no_op (no side effect)")


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)

# F9 (FZ 20k9c1a1a1b7c2k2a — the openclaw sweep): writers naturally render
# the frontmatter as a ```yaml fence (every wave leaf emitted it; run 8's
# retries happened to converge to bare ---, openclaw's did not — structural
# absorption beats mandates, the F1-vs-F2 lesson again). The fenced form is
# MEANING-IDENTICAL rendering variance, so per the canonical-form contract
# (R4.3) the code side absorbs it: a leading ```yaml fence becomes the
# frontmatter, the remainder after the closing fence the body. An optional
# whole-document ```markdown wrapper is unwrapped first.
_FENCED_DOC_RE = re.compile(r"^```(?:markdown|md)\s*\n(.*)\n```\s*$", re.DOTALL)
_FENCED_YAML_RE = re.compile(r"^```(?:yaml|yml)\s*\n(.*?)\n```\s*\n?(.*)$", re.DOTALL)


def _heal_sibling_links(text: str, siblings_md: str) -> str:
    """k2a4a: deterministic sibling-link healing — the F9/F10 absorption
    pattern applied to links. A relative .md link whose basename does not
    match any planned sibling but whose NORMALIZED stem (kebab and snake
    collapse to one alphabet) matches exactly ONE sibling is rewritten to
    that sibling's verbatim filename. Conservative: ambiguous or unmatched
    targets are left for the wave's link_resolution sweep to report."""
    if not siblings_md:
        return text
    siblings = [ln[2:].strip() for ln in siblings_md.splitlines()
                if ln.startswith("- ") and ln.strip().endswith(".md")]
    if not siblings:
        return text
    sib_set = set(siblings)

    def norm(name: str) -> str:
        return name.lower().replace("-", "_")

    by_norm: dict[str, list[str]] = {}
    for sib in siblings:
        by_norm.setdefault(norm(sib), []).append(sib)

    import re as _re

    def _fix(m: "_re.Match[str]") -> str:
        target = m.group(2)
        base = target.rsplit("/", 1)[-1]
        if base in sib_set:
            return m.group(0)
        candidates = by_norm.get(norm(base), [])
        if len(candidates) == 1:
            healed = target[: len(target) - len(base)] + candidates[0]
            return f"[{m.group(1)}]({healed})"
        return m.group(0)

    return _re.sub(r"\[([^\]]+)\]\(([^)\s]+\.md)\)", _fix, text)


def _absorb_frontmatter_rendering(text: str) -> str:
    """Normalize known meaning-identical frontmatter renderings to the
    canonical ``---``-delimited form. Pure; unknown shapes pass through
    untouched (the strict check still fails them loudly)."""
    stripped = text.strip()
    doc = _FENCED_DOC_RE.match(stripped)
    if doc:
        stripped = doc.group(1).strip()
    if stripped.startswith("---"):
        return stripped
    fenced = _FENCED_YAML_RE.match(stripped)
    if fenced:
        return f"---\n{fenced.group(1)}\n---\n{fenced.group(2)}"
    return stripped


def _body_markdown_frontmatter_to_file(
    text: str,
    vault_root: Path,
    dry_run: bool,
    effect_guard: Callable[[], ContextManager[None]],
    effect_recorder: Callable[[Path], None],
) -> MaterializedOutput:
    """PRODUCE — agent emits markdown-with-frontmatter directly.

    Expected wire format::

        ---
        output_path: relative/path.md
        ... (other YAML fields, optional)
        ---
        <body markdown>

    The materializer extracts ``output_path``, strips it from the
    frontmatter, and writes the remaining frontmatter + body to disk.
    """
    m = _FRONTMATTER_RE.match(_absorb_frontmatter_rendering(text))
    if not m:
        raise MaterializerError(
            "body_markdown_frontmatter_to_file: response missing YAML frontmatter "
            "(expected leading `---\\n…\\n---`)"
        )
    raw_yaml = m.group(1)
    body = m.group(2)
    try:
        fm = yaml.safe_load(raw_yaml) or {}
    except yaml.YAMLError as e:
        raise MaterializerError(f"frontmatter YAML parse error: {e}") from e
    if not isinstance(fm, dict):
        raise MaterializerError(
            f"frontmatter must be a YAML mapping, got {type(fm).__name__}"
        )
    # F10 (FZ 20k9c1a1a1b7c2k2a — the openclaw sweep): the vault's tag
    # alphabet is lowercase/digits/underscores (YAML-015); writers digesting
    # kebab-case-heavy sources naturally emit kebab tags ('active-memory'),
    # which blocked 7 of 9 leaves at the close gate. A hyphenated tag is the
    # SAME tag in a different rendering — per the canonical-form contract the
    # code side absorbs it deterministically; genuinely alien values still
    # fail the validator downstream.
    if isinstance(fm.get("tags"), list):
        fm["tags"] = [
            re.sub(r"[^a-z0-9_]+", "_", str(t).strip().lower()).strip("_") or str(t)
            for t in fm["tags"]
        ]
    output_path = fm.get("output_path")
    if not output_path:
        raise MaterializerError("frontmatter missing required `output_path` field")

    target = _resolve_vault_path(
        vault_root, output_path, field="frontmatter output_path"
    )

    # Strip output_path from the frontmatter that gets written — it's a
    # coordination field, not vault content.
    fm_for_file = {k: v for k, v in fm.items() if k != "output_path"}
    if fm_for_file:
        new_yaml = yaml.safe_dump(fm_for_file, default_flow_style=False, sort_keys=False)
        full_content = f"---\n{new_yaml}---\n{body}"
    else:
        # No remaining frontmatter — emit body only (rare, mostly tests).
        full_content = body

    if not dry_run:
        with effect_guard():
            content = full_content.encode("utf-8")
            _record_effect(effect_recorder, target, content)
            _atomic_write_bytes(target, content)

    return MaterializedOutput(
        structured={"output_path": str(output_path), "body_markdown": body},
        files_written=(target,) if not dry_run else (),
        notes=f"wrote {output_path} ({len(full_content)} chars)",
    )


def _body_markdown_to_file(
    text: str,
    vault_root: Path,
    dry_run: bool,
    effect_guard: Callable[[], ContextManager[None]],
    effect_recorder: Callable[[Path], None],
) -> MaterializedOutput:
    """Legacy v0.4 PRODUCE materializer — JSON envelope.

    Expected wire format::

        {"output_path": "relative/path.md", "body_markdown": "<full body text>"}
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise MaterializerError(
            f"body_markdown_to_file: response is not valid JSON: {e}"
        ) from e
    if not isinstance(data, dict):
        raise MaterializerError(
            f"body_markdown_to_file: response must be a JSON object, "
            f"got {type(data).__name__}"
        )
    output_path = data.get("output_path")
    body = data.get("body_markdown")
    if not output_path:
        raise MaterializerError("missing required field `output_path`")
    if body is None:
        raise MaterializerError("missing required field `body_markdown`")

    target = _resolve_vault_path(vault_root, output_path, field="output_path")
    if not dry_run:
        with effect_guard():
            content = str(body).encode("utf-8")
            _record_effect(effect_recorder, target, content)
            _atomic_write_bytes(target, content)

    return MaterializedOutput(
        structured=data,
        files_written=(target,) if not dry_run else (),
        notes=f"wrote {output_path} ({len(str(body))} chars)",
    )


def _edits_apply_to_files(
    text: str,
    vault_root: Path,
    dry_run: bool,
    effect_guard: Callable[[], ContextManager[None]],
    effect_recorder: Callable[[Path], None],
) -> MaterializedOutput:
    """APPLY (legacy) — JSON edits envelope.

    Expected wire format::

        {"edits": [{"file": "relative/path.md", "content": "<full new content>"}, ...]}

    Each edit overwrites the target file.
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise MaterializerError(
            f"edits_apply_to_files: response is not valid JSON: {e}"
        ) from e
    if not isinstance(data, dict):
        raise MaterializerError("response must be a JSON object")
    edits = data.get("edits")
    if not isinstance(edits, list):
        raise MaterializerError("missing or non-list `edits` field")

    pending: list[tuple[Path, str]] = []
    for i, edit in enumerate(edits):
        if not isinstance(edit, dict):
            raise MaterializerError(f"edits[{i}] must be a JSON object")
        file_path = edit.get("file")
        content = edit.get("content")
        if not file_path:
            raise MaterializerError(f"edits[{i}] missing `file`")
        if content is None:
            raise MaterializerError(f"edits[{i}] missing `content`")
        target = _resolve_vault_path(
            vault_root, file_path, field=f"edits[{i}].file"
        )
        pending.append((target, str(content)))

    applied = [target for target, _content in pending]
    if not dry_run:
        for target, content in pending:
            with effect_guard():
                encoded = content.encode("utf-8")
                _record_effect(effect_recorder, target, encoded)
                _atomic_write_bytes(target, encoded)

    return MaterializedOutput(
        structured=data,
        files_applied=tuple(applied) if not dry_run else (),
        notes=f"applied {len(applied)} edit(s)",
    )


_XML_EDIT_RE = re.compile(
    r"<edit>\s*<file>(.*?)</file>\s*<content>(.*?)</content>\s*</edit>",
    re.DOTALL,
)


def _edits_apply_xml_tags(
    text: str,
    vault_root: Path,
    dry_run: bool,
    effect_guard: Callable[[], ContextManager[None]],
    effect_recorder: Callable[[Path], None],
) -> MaterializedOutput:
    """APPLY — XML wire format (preferred over the legacy JSON envelope).

    Expected wire format::

        <edits>
          <edit>
            <file>relative/path.md</file>
            <content>(full new content)</content>
          </edit>
          <edit>...</edit>
        </edits>

    More forgiving of natural-language content than JSON (no escape
    headaches for quotes, newlines, or backslashes).
    """
    matches = _XML_EDIT_RE.findall(text)
    if not matches:
        raise MaterializerError(
            "edits_apply_xml_tags: no <edit><file>…</file><content>…</content></edit> "
            "blocks found in response"
        )

    pending: list[tuple[Path, str]] = []
    edits_records: list[dict] = []
    for i, (file_path, content) in enumerate(matches):
        file_clean = file_path.strip()
        if not file_clean:
            raise MaterializerError("edit has empty <file> tag")
        target = _resolve_vault_path(
            vault_root, file_clean, field=f"edits[{i}].file"
        )
        pending.append((target, content))
        edits_records.append({"file": file_clean, "content": content})

    applied = [target for target, _content in pending]
    if not dry_run:
        for target, content in pending:
            with effect_guard():
                encoded = content.encode("utf-8")
                _record_effect(effect_recorder, target, encoded)
                _atomic_write_bytes(target, encoded)

    return MaterializedOutput(
        structured={"edits": edits_records},
        files_applied=tuple(applied) if not dry_run else (),
        notes=f"applied {len(applied)} XML edit(s)",
    )


_DISPATCH = {
    "no_op": _no_op,
    "body_markdown_to_file": _body_markdown_to_file,
    "body_markdown_frontmatter_to_file": _body_markdown_frontmatter_to_file,
    "edits_apply_to_files": _edits_apply_to_files,
    "edits_apply_xml_tags": _edits_apply_xml_tags,
}


__all__ = ["MaterializerError", "MaterializedOutput", "materialize"]
