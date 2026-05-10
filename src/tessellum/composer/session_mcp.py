"""Session-MCP: read-only access to the active Claude Code transcript.

Pure-Python handlers that surface four tools for skills (e.g.,
``skill_tessellum_write_coe``) that need to inspect the conversation
that *triggered* their invocation:

    - ``get_session_metadata`` — static snapshot (cwd / git branch / model /
      turn counts / transcript size)
    - ``read_recent_messages`` — last N user/assistant messages with role +
      flattened text
    - ``search_transcript`` — keyword/regex search across messages with
      200-char snippets around each match
    - ``get_tool_uses`` — tool_use blocks from assistant messages, optionally
      filtered by tool name pattern

The functions are pure Python with stdlib-only dependencies. The thin
MCP-protocol wrapper that exposes them over stdio JSON-RPC lives in
``scripts/tessellum_session_mcp_server.py`` and requires the ``mcp``
SDK (``pip install tessellum[mcp]``).

Composer wiring: a skill sidecar's step can declare
``mcp_dependencies: [{name: session-mcp, calls: [...]}]`` and the
compiler validates the call list against this module's
:data:`SESSION_MCP_TOOLS` keys via the registered
:class:`tessellum.composer.contracts.MCPContract`.

Transcript path resolution precedence:

    1. Explicit path passed by the caller
    2. ``SESSION_TRANSCRIPT_PATH`` environment variable
    3. Auto-detect: most recent ``~/.claude/projects/<encoded-cwd>/*.jsonl``
       for the current working directory

Transcripts are line-delimited JSON (each line one event with a ``type``
field); we stream-read since transcripts can be hundreds of MB.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Iterator

__all__ = [
    "SESSION_MCP_TOOLS",
    "resolve_transcript_path",
    "get_session_metadata",
    "read_recent_messages",
    "search_transcript",
    "get_tool_uses",
]


# ── Transcript path resolution ────────────────────────────────────────────


def _encode_cwd_for_claude_projects(cwd: Path) -> str:
    """Mirror Claude Code's project-directory encoding.

    Claude stores per-project transcripts at
    ``~/.claude/projects/<encoded-cwd>/<session-id>.jsonl``. The encoding
    replaces both ``/`` AND ``_`` with ``-`` (e.g., ``/Users/x/my_repo``
    → ``-Users-x-my-repo``). Verified empirically against
    ``~/.claude/projects/``; if Claude Code changes the encoding, this
    resolver will silently miss the active session and fall through to
    returning ``None`` — caller's degraded path handles it.
    """
    return str(cwd.resolve()).replace("/", "-").replace("_", "-")


def resolve_transcript_path(
    explicit_path: Path | str | None = None,
    cwd: Path | None = None,
) -> Path | None:
    """Resolve the transcript path with documented precedence.

    Returns ``None`` if no transcript can be located — caller's
    responsibility to handle (e.g., return a degraded result).
    """
    if explicit_path is not None:
        p = Path(explicit_path)
        return p if p.exists() else None

    env_path = os.environ.get("SESSION_TRANSCRIPT_PATH")
    if env_path:
        p = Path(env_path)
        return p if p.exists() else None

    cwd = cwd or Path.cwd()
    project_dir = (
        Path.home() / ".claude" / "projects" / _encode_cwd_for_claude_projects(cwd)
    )
    if not project_dir.exists():
        return None

    jsonls = sorted(
        project_dir.glob("*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return jsonls[0] if jsonls else None


# ── Transcript streaming + content flattening ─────────────────────────────


def _iter_transcript(transcript_path: Path) -> Iterator[dict[str, Any]]:
    """Yield each JSONL line as a parsed dict. Skips malformed lines."""
    with transcript_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


# Per-block cap on serialized tool_use.input / tool_result.content text.
# 10K chars handles typical Write / Edit / Bash payloads while bounding
# memory growth across a multi-MB transcript scan.
_TOOL_IO_TEXT_CAP = 10_000


def _truncate(s: str) -> str:
    if len(s) <= _TOOL_IO_TEXT_CAP:
        return s
    return s[:_TOOL_IO_TEXT_CAP] + f"... [+{len(s) - _TOOL_IO_TEXT_CAP} chars truncated]"


def _serialize_tool_input(payload: Any) -> str:
    """Render a tool_use.input dict (or other shape) as a searchable string.

    Stringifies dict values; truncates with a marker if over the cap.
    Robust to ``None`` / non-dict payloads (returns empty / repr).
    """
    if payload is None:
        return ""
    if isinstance(payload, str):
        return _truncate(payload)
    if isinstance(payload, dict):
        items = []
        for k, v in payload.items():
            if isinstance(v, str):
                items.append(f"{k}={v}")
            else:
                items.append(f"{k}={v!r}")
        return _truncate(" | ".join(items))
    return _truncate(repr(payload))


def _serialize_tool_result(content: Any) -> str:
    """Render a tool_result.content (string, list-of-blocks, dict) as text.

    Handles the canonical Anthropic shapes: bare string, list of
    ``{type:'text', text:'...'}`` blocks, or arbitrary dicts (rendered
    as ``repr``). Truncated.
    """
    if content is None:
        return ""
    if isinstance(content, str):
        return _truncate(content)
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                else:
                    parts.append(repr(block))
            elif isinstance(block, str):
                parts.append(block)
        return _truncate("\n".join(parts))
    return _truncate(repr(content))


def _extract_text_from_content(
    content: Any, *, include_tool_io: bool = True
) -> str:
    """Flatten ``message.content`` (str or list-of-blocks) into one string.

    By default, ``tool_use`` ``input`` payloads and ``tool_result``
    ``content`` are surfaced in the flattened text so ``search_transcript``
    matches strings the agent wrote via Write / Edit / Bash. Without this,
    content that lives only in tool_use payloads (e.g., file bodies created
    via ``Write``) is invisible to search.

    Set ``include_tool_io=False`` for the minimal view (only
    ``[tool_use: <name>]`` / ``[tool_result]`` markers).
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict):
                btype = block.get("type")
                if btype == "text":
                    parts.append(block.get("text", ""))
                elif btype == "thinking":
                    parts.append(block.get("thinking", ""))
                elif btype == "tool_use":
                    name = block.get("name", "?")
                    if include_tool_io:
                        payload = _serialize_tool_input(block.get("input"))
                        parts.append(f"[tool_use: {name}] {payload}")
                    else:
                        parts.append(f"[tool_use: {name}]")
                elif btype == "tool_result":
                    if include_tool_io:
                        payload = _serialize_tool_result(block.get("content"))
                        parts.append(f"[tool_result] {payload}")
                    else:
                        parts.append("[tool_result]")
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return ""


# ── Public tool handlers ──────────────────────────────────────────────────


def get_session_metadata(transcript_path: Path) -> dict[str, Any]:
    """Static snapshot of the active session.

    Returns ``session_id``, ``transcript_path``, ``transcript_size_bytes``,
    ``transcript_mtime``, ``user_turn_count``, ``assistant_turn_count``, and
    (when present in the transcript) ``cwd``, ``git_branch``, ``entrypoint``,
    ``model``.
    """
    if not transcript_path.exists():
        return {
            "error": "transcript_not_found",
            "transcript_path": str(transcript_path),
        }

    metadata: dict[str, Any] = {
        "session_id": transcript_path.stem,
        "transcript_path": str(transcript_path),
        "transcript_size_bytes": transcript_path.stat().st_size,
        "transcript_mtime": transcript_path.stat().st_mtime,
        "user_turn_count": 0,
        "assistant_turn_count": 0,
    }

    for event in _iter_transcript(transcript_path):
        etype = event.get("type")
        if etype == "user":
            metadata["user_turn_count"] += 1
            if "cwd" not in metadata and "cwd" in event:
                metadata["cwd"] = event["cwd"]
            if "git_branch" not in metadata and "gitBranch" in event:
                metadata["git_branch"] = event["gitBranch"]
            if "entrypoint" not in metadata and "entrypoint" in event:
                metadata["entrypoint"] = event["entrypoint"]
        elif etype == "assistant":
            metadata["assistant_turn_count"] += 1
            msg = event.get("message", {})
            if (
                "model" not in metadata
                and isinstance(msg, dict)
                and "model" in msg
            ):
                metadata["model"] = msg["model"]

    return metadata


def read_recent_messages(
    transcript_path: Path,
    n: int = 20,
    include_thinking: bool = False,
) -> dict[str, Any]:
    """Last N user/assistant messages with role + flattened text content.

    ``include_thinking=False`` strips assistant ``thinking`` blocks (typically
    the most verbose part); pass ``True`` if the caller needs them.
    """
    if not transcript_path.exists():
        return {"error": "transcript_not_found", "messages": []}

    messages: list[dict[str, Any]] = []
    for event in _iter_transcript(transcript_path):
        etype = event.get("type")
        if etype not in {"user", "assistant"}:
            continue
        msg = event.get("message", {})
        if not isinstance(msg, dict):
            continue
        role = msg.get("role", etype)
        content = msg.get("content")
        if not include_thinking and isinstance(content, list):
            content = [
                b
                for b in content
                if not (isinstance(b, dict) and b.get("type") == "thinking")
            ]
        text = _extract_text_from_content(content)
        if not text:
            continue
        messages.append({"role": role, "text": text})

    return {"messages": messages[-n:], "total_messages": len(messages)}


def search_transcript(
    transcript_path: Path,
    query: str,
    regex: bool = False,
    max_matches: int = 50,
) -> dict[str, Any]:
    """Search messages for ``query``. Returns matches with role + snippet.

    Searches across user prompts, assistant text+thinking, and tool_use
    inputs. Each match includes the message role + a snippet (200 chars
    around the match).
    """
    if not transcript_path.exists():
        return {"error": "transcript_not_found", "matches": []}

    if regex:
        try:
            pattern = re.compile(query, re.IGNORECASE)
        except re.error as e:
            return {"error": f"invalid_regex: {e}", "matches": []}
    else:
        pattern = re.compile(re.escape(query), re.IGNORECASE)

    matches: list[dict[str, Any]] = []
    for idx, event in enumerate(_iter_transcript(transcript_path)):
        etype = event.get("type")
        if etype not in {"user", "assistant"}:
            continue
        msg = event.get("message", {})
        if not isinstance(msg, dict):
            continue
        text = _extract_text_from_content(msg.get("content"))
        m = pattern.search(text)
        if not m:
            continue
        start = max(0, m.start() - 100)
        end = min(len(text), m.end() + 100)
        matches.append(
            {
                "event_index": idx,
                "role": msg.get("role", etype),
                "snippet": text[start:end],
                "match": m.group(0),
            }
        )
        if len(matches) >= max_matches:
            break

    return {
        "matches": matches,
        "match_count": len(matches),
        "truncated": len(matches) >= max_matches,
    }


def get_tool_uses(
    transcript_path: Path,
    tool_name_pattern: str | None = None,
    max_results: int = 100,
) -> dict[str, Any]:
    """All tool_use blocks; optionally filter by tool name pattern (regex)."""
    if not transcript_path.exists():
        return {"error": "transcript_not_found", "tool_uses": []}

    name_re: re.Pattern[str] | None = None
    if tool_name_pattern:
        try:
            name_re = re.compile(tool_name_pattern)
        except re.error as e:
            return {"error": f"invalid_regex: {e}", "tool_uses": []}

    tool_uses: list[dict[str, Any]] = []
    for event in _iter_transcript(transcript_path):
        if event.get("type") != "assistant":
            continue
        msg = event.get("message", {})
        content = msg.get("content") if isinstance(msg, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            name = block.get("name", "")
            if name_re and not name_re.search(name):
                continue
            tool_uses.append({"name": name, "input": block.get("input", {})})
            if len(tool_uses) >= max_results:
                break
        if len(tool_uses) >= max_results:
            break

    return {
        "tool_uses": tool_uses,
        "count": len(tool_uses),
        "truncated": len(tool_uses) >= max_results,
    }


# ── Dispatcher ────────────────────────────────────────────────────────────

SESSION_MCP_TOOLS = {
    "get_session_metadata": get_session_metadata,
    "get_tool_uses": get_tool_uses,
    "read_recent_messages": read_recent_messages,
    "search_transcript": search_transcript,
}
"""The 4 tools session-mcp exposes. Names match the registered
:class:`tessellum.composer.contracts.MCPContract`'s ``available_tools``;
the composer's compiler validates ``mcp_dependencies[].calls`` entries
against the contract's tool list."""
