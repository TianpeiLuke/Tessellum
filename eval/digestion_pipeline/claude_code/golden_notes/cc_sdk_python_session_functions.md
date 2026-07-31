---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - python_reference
keywords:
  - list_sessions
  - get_session_messages
  - get_session_info
  - rename_session
  - tag_session
  - sdksessioninfo
  - sessionmessage
  - claude-agent-sdk
  - session management
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/python
access_control_group: ["general"]
---

# Python Agent SDK — Session-Management Functions

## Overview

The Python Agent SDK (`claude-agent-sdk`) exposes five **synchronous** module-level functions for working with past Claude Code sessions: `list_sessions()`, `get_session_messages()`, `get_session_info()`, `rename_session()`, and `tag_session()`. All return (or act) immediately without an async context, so they can be called directly outside an event loop. Together they let a host program enumerate persisted sessions, page through a session's transcript, read a single session's metadata cheaply, and annotate sessions with custom titles and tags for later retrieval.

Two return shapes back these functions: `SDKSessionInfo` (session metadata) and `SessionMessage` (one transcript message). The *behavioral* model of how sessions are stored and resumed lives in the Sessions / Session-storage guides ([code.claude.com/docs/en/agent-sdk/sessions](https://code.claude.com/docs/en/agent-sdk/sessions)); this note documents only the function signatures, parameters, and return types.

## `list_sessions()`

Lists past sessions with metadata. Filter by project directory or list sessions across all projects. Synchronous; returns immediately.

```python
def list_sessions(
    directory: str | None = None,
    limit: int | None = None,
    include_worktrees: bool = True
) -> list[SDKSessionInfo]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `directory` | `str \| None` | `None` | Directory to list sessions for. When omitted, returns sessions across all projects |
| `limit` | `int \| None` | `None` | Maximum number of sessions to return |
| `include_worktrees` | `bool` | `True` | When `directory` is inside a git repository, include sessions from all worktree paths |

Results are sorted by `last_modified` descending, so the first item is the newest. Omit `directory` to search across all projects.

```python
from claude_agent_sdk import list_sessions

for session in list_sessions(directory="/path/to/project", limit=10):
    print(f"{session.summary} ({session.session_id})")
```

### Return type: `SDKSessionInfo`

`SDKSessionInfo` is also the return type of `get_session_info()`.

| Property | Type | Description |
| :--- | :--- | :--- |
| `session_id` | `str` | Unique session identifier |
| `summary` | `str` | Display title: custom title, auto-generated summary, or first prompt |
| `last_modified` | `int` | Last modified time in milliseconds since epoch |
| `file_size` | `int \| None` | Session file size in bytes (`None` for remote storage backends) |
| `custom_title` | `str \| None` | User-set session title |
| `first_prompt` | `str \| None` | First meaningful user prompt in the session |
| `git_branch` | `str \| None` | Git branch at the end of the session |
| `cwd` | `str \| None` | Working directory for the session |
| `tag` | `str \| None` | User-set session tag (see `tag_session()`) |
| `created_at` | `int \| None` | Session creation time in milliseconds since epoch |

## `get_session_messages()`

Retrieves messages from a past session. Synchronous; returns immediately. Supports `limit`/`offset` paging through a transcript.

```python
def get_session_messages(
    session_id: str,
    directory: str | None = None,
    limit: int | None = None,
    offset: int = 0
) -> list[SessionMessage]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `session_id` | `str` | required | The session ID to retrieve messages for |
| `directory` | `str \| None` | `None` | Project directory to look in. When omitted, searches all projects |
| `limit` | `int \| None` | `None` | Maximum number of messages to return |
| `offset` | `int` | `0` | Number of messages to skip from the start |

### Return type: `SessionMessage`

| Property | Type | Description |
| :--- | :--- | :--- |
| `type` | `Literal["user", "assistant"]` | Message role |
| `uuid` | `str` | Unique message identifier |
| `session_id` | `str` | Session identifier |
| `message` | `Any` | Raw message content |
| `parent_tool_use_id` | `None` | Reserved for future use |

A typical paging read takes the newest session ID from `list_sessions(limit=1)`, passes it to `get_session_messages(...)`, and iterates the returned `SessionMessage` list (each item exposes `.type` and `.uuid`).

## `get_session_info()`

Reads metadata for a single session by ID without scanning the full project directory. Synchronous; returns immediately. Returns `SDKSessionInfo`, or `None` if the session is not found. Useful when you already have a session ID from a previous run.

```python
def get_session_info(
    session_id: str,
    directory: str | None = None,
) -> SDKSessionInfo | None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `session_id` | `str` | required | UUID of the session to look up |
| `directory` | `str \| None` | `None` | Project directory path. When omitted, searches all project directories |

## `rename_session()`

Renames a session by appending a custom-title entry. Repeated calls are safe; the most recent title wins. Synchronous. The new title appears in `SDKSessionInfo.custom_title` on subsequent reads.

```python
def rename_session(
    session_id: str,
    title: str,
    directory: str | None = None,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `session_id` | `str` | required | UUID of the session to rename |
| `title` | `str` | required | New title. Must be non-empty after stripping whitespace |
| `directory` | `str \| None` | `None` | Project directory path. When omitted, searches all project directories |

Raises `ValueError` if `session_id` is not a valid UUID or `title` is empty; `FileNotFoundError` if the session cannot be found.

## `tag_session()`

Tags a session. Pass `None` to clear the tag. Repeated calls are safe; the most recent tag wins. Synchronous. The tag surfaces in `SDKSessionInfo.tag`, so a later `list_sessions()` read can filter by it.

```python
def tag_session(
    session_id: str,
    tag: str | None,
    directory: str | None = None,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `session_id` | `str` | required | UUID of the session to tag |
| `tag` | `str \| None` | required | Tag string, or `None` to clear. Unicode-sanitized before storing |
| `directory` | `str \| None` | `None` | Project directory path. When omitted, searches all project directories |

Raises `ValueError` if `session_id` is not a valid UUID or `tag` is empty after sanitization; `FileNotFoundError` if the session cannot be found. A common pattern is to `tag_session(session_id, "needs-review")` and then on a later `list_sessions(directory=...)` read, filter on `session.tag == "needs-review"` to find the tagged sessions; passing `None` as the tag clears an existing tag.

**Source**: https://code.claude.com/docs/en/agent-sdk/python
**Last Updated**: 2026-06-13
**Status**: Active
