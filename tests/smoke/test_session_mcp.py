"""Smoke tests for session-mcp's pure handlers.

The handler functions are stdlib-only and read JSONL transcript files.
Tests construct synthetic transcripts in ``tmp_path`` and verify the
four public tools return the expected shape.

The MCP-protocol wrapper (``scripts/tessellum_session_mcp_server.py``)
is not tested here — it's a thin stdio adapter around these same
functions and integration-tests through Claude Code.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tessellum.composer import (
    SESSION_MCP_TOOLS,
    get_session_metadata,
    get_tool_uses,
    read_recent_messages,
    resolve_transcript_path,
    search_transcript,
)


# ── Fixture: synthesise a small transcript ────────────────────────────────


def _write_transcript(path: Path, events: list[dict]) -> Path:
    with path.open("w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")
    return path


@pytest.fixture
def transcript(tmp_path: Path) -> Path:
    """Synthetic 6-event transcript covering the shapes the handlers parse."""
    events = [
        {
            "type": "user",
            "cwd": "/Users/test/my_repo",
            "gitBranch": "main",
            "entrypoint": "cli",
            "message": {
                "role": "user",
                "content": "Please add tests for the search feature.",
            },
        },
        {
            "type": "assistant",
            "message": {
                "model": "claude-opus-4-7",
                "role": "assistant",
                "content": [
                    {
                        "type": "thinking",
                        "thinking": "I should start by reading the existing tests.",
                    },
                    {"type": "text", "text": "I'll add a test file."},
                    {
                        "type": "tool_use",
                        "name": "Read",
                        "input": {"file_path": "tests/test_search.py"},
                    },
                ],
            },
        },
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": [
                    {"type": "tool_result", "content": "(file not found)"},
                ],
            },
        },
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "Creating new test file."},
                    {
                        "type": "tool_use",
                        "name": "Write",
                        "input": {
                            "file_path": "tests/test_search.py",
                            "content": "def test_search(): assert True",
                        },
                    },
                    {
                        "type": "tool_use",
                        "name": "Bash",
                        "input": {"command": "pytest tests/test_search.py"},
                    },
                ],
            },
        },
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Test passes. Now wire it into the CI workflow.",
            },
        },
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": "I'll add the CI step.",
            },
        },
    ]
    return _write_transcript(tmp_path / "session.jsonl", events)


# ── get_session_metadata ──────────────────────────────────────────────────


def test_get_session_metadata_basic(transcript: Path) -> None:
    md = get_session_metadata(transcript)
    assert md["session_id"] == "session"
    assert md["transcript_path"] == str(transcript)
    assert md["transcript_size_bytes"] > 0
    assert md["user_turn_count"] == 3
    assert md["assistant_turn_count"] == 3
    assert md["cwd"] == "/Users/test/my_repo"
    assert md["git_branch"] == "main"
    assert md["entrypoint"] == "cli"
    assert md["model"] == "claude-opus-4-7"


def test_get_session_metadata_missing_file(tmp_path: Path) -> None:
    md = get_session_metadata(tmp_path / "does_not_exist.jsonl")
    assert md["error"] == "transcript_not_found"


# ── read_recent_messages ──────────────────────────────────────────────────


def test_read_recent_messages_returns_last_n(transcript: Path) -> None:
    r = read_recent_messages(transcript, n=2)
    assert r["total_messages"] >= 2
    assert len(r["messages"]) == 2
    # Last message should be the assistant's "I'll add the CI step."
    assert r["messages"][-1]["role"] == "assistant"
    assert "CI step" in r["messages"][-1]["text"]


def test_read_recent_messages_strips_thinking_by_default(transcript: Path) -> None:
    r = read_recent_messages(transcript, n=20)
    all_text = "\n".join(m["text"] for m in r["messages"])
    assert "I should start by reading" not in all_text


def test_read_recent_messages_includes_thinking_when_asked(transcript: Path) -> None:
    r = read_recent_messages(transcript, n=20, include_thinking=True)
    all_text = "\n".join(m["text"] for m in r["messages"])
    assert "I should start by reading" in all_text


def test_read_recent_messages_includes_tool_io_in_flatten(transcript: Path) -> None:
    """tool_use input + tool_result content surface in flattened text by default."""
    r = read_recent_messages(transcript, n=20)
    all_text = "\n".join(m["text"] for m in r["messages"])
    # tool_use input was serialised → file_path=tests/test_search.py visible
    assert "tests/test_search.py" in all_text
    # tool_result content visible too
    assert "file not found" in all_text


# ── search_transcript ─────────────────────────────────────────────────────


def test_search_transcript_keyword(transcript: Path) -> None:
    r = search_transcript(transcript, query="pytest")
    assert r["match_count"] == 1
    assert r["matches"][0]["role"] == "assistant"
    assert "pytest" in r["matches"][0]["snippet"]


def test_search_transcript_no_match(transcript: Path) -> None:
    r = search_transcript(transcript, query="kubernetes")
    assert r["match_count"] == 0
    assert r["matches"] == []


def test_search_transcript_regex(transcript: Path) -> None:
    r = search_transcript(transcript, query=r"CI\s+step", regex=True)
    assert r["match_count"] >= 1


def test_search_transcript_invalid_regex(transcript: Path) -> None:
    r = search_transcript(transcript, query="[unclosed", regex=True)
    assert "invalid_regex" in r["error"]


def test_search_transcript_max_matches(transcript: Path) -> None:
    r = search_transcript(transcript, query="t", max_matches=2)
    assert len(r["matches"]) <= 2


# ── get_tool_uses ─────────────────────────────────────────────────────────


def test_get_tool_uses_all(transcript: Path) -> None:
    r = get_tool_uses(transcript)
    assert r["count"] == 3
    names = [tu["name"] for tu in r["tool_uses"]]
    assert names == ["Read", "Write", "Bash"]


def test_get_tool_uses_filter_by_pattern(transcript: Path) -> None:
    r = get_tool_uses(transcript, tool_name_pattern="Write|Bash")
    assert r["count"] == 2
    assert {tu["name"] for tu in r["tool_uses"]} == {"Write", "Bash"}


def test_get_tool_uses_inputs_preserved(transcript: Path) -> None:
    r = get_tool_uses(transcript, tool_name_pattern="^Write$")
    assert r["count"] == 1
    assert r["tool_uses"][0]["input"]["file_path"] == "tests/test_search.py"
    assert "def test_search" in r["tool_uses"][0]["input"]["content"]


def test_get_tool_uses_invalid_regex(transcript: Path) -> None:
    r = get_tool_uses(transcript, tool_name_pattern="[unclosed")
    assert "invalid_regex" in r["error"]


# ── resolve_transcript_path ───────────────────────────────────────────────


def test_resolve_transcript_path_explicit(transcript: Path) -> None:
    p = resolve_transcript_path(transcript)
    assert p == transcript


def test_resolve_transcript_path_explicit_missing(tmp_path: Path) -> None:
    p = resolve_transcript_path(tmp_path / "nope.jsonl")
    assert p is None


def test_resolve_transcript_path_env(monkeypatch, transcript: Path) -> None:
    monkeypatch.setenv("SESSION_TRANSCRIPT_PATH", str(transcript))
    assert resolve_transcript_path() == transcript


# ── Registry shape ────────────────────────────────────────────────────────


def test_session_mcp_tools_dict_is_complete() -> None:
    assert set(SESSION_MCP_TOOLS) == {
        "get_session_metadata",
        "get_tool_uses",
        "read_recent_messages",
        "search_transcript",
    }
    assert all(callable(fn) for fn in SESSION_MCP_TOOLS.values())


# ── Contract registration ────────────────────────────────────────────────


def test_session_mcp_contract_registered() -> None:
    from tessellum.composer.contracts import MCP_CONTRACTS

    assert "session-mcp" in MCP_CONTRACTS
    c = MCP_CONTRACTS["session-mcp"]
    assert c.name == "session-mcp"
    # Every handler in the dispatcher must be in the contract's available_tools.
    assert set(c.available_tools) == set(SESSION_MCP_TOOLS)
