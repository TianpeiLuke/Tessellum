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
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


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
    return handler(response_text, vault_root, dry_run)


# ── Concrete materializers ─────────────────────────────────────────────────


def _no_op(text: str, vault_root: Path, dry_run: bool) -> MaterializedOutput:
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


def _body_markdown_frontmatter_to_file(
    text: str, vault_root: Path, dry_run: bool
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
    m = _FRONTMATTER_RE.match(text)
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
    output_path = fm.get("output_path")
    if not output_path:
        raise MaterializerError("frontmatter missing required `output_path` field")

    target = (vault_root / str(output_path)).resolve()

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
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(full_content, encoding="utf-8")

    return MaterializedOutput(
        structured={"output_path": str(output_path), "body_markdown": body},
        files_written=(target,) if not dry_run else (),
        notes=f"wrote {output_path} ({len(full_content)} chars)",
    )


def _body_markdown_to_file(
    text: str, vault_root: Path, dry_run: bool
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

    target = (vault_root / str(output_path)).resolve()
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(body), encoding="utf-8")

    return MaterializedOutput(
        structured=data,
        files_written=(target,) if not dry_run else (),
        notes=f"wrote {output_path} ({len(str(body))} chars)",
    )


def _edits_apply_to_files(
    text: str, vault_root: Path, dry_run: bool
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

    applied: list[Path] = []
    for i, edit in enumerate(edits):
        if not isinstance(edit, dict):
            raise MaterializerError(f"edits[{i}] must be a JSON object")
        file_path = edit.get("file")
        content = edit.get("content")
        if not file_path:
            raise MaterializerError(f"edits[{i}] missing `file`")
        if content is None:
            raise MaterializerError(f"edits[{i}] missing `content`")
        target = (vault_root / str(file_path)).resolve()
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(str(content), encoding="utf-8")
        applied.append(target)

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
    text: str, vault_root: Path, dry_run: bool
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

    applied: list[Path] = []
    edits_records: list[dict] = []
    for file_path, content in matches:
        file_clean = file_path.strip()
        if not file_clean:
            raise MaterializerError("edit has empty <file> tag")
        target = (vault_root / file_clean).resolve()
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        applied.append(target)
        edits_records.append({"file": file_clean, "content": content})

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
