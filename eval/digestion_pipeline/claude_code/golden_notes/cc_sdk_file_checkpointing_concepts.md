---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - file_checkpointing
keywords:
  - file checkpointing
  - rewind file changes
  - checkpoint uuid
  - restore point
  - write edit notebookedit
  - original content backup
  - checkpoint limitations
  - rewind files
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/file-checkpointing
access_control_group: ["general"]
---

# Claude Agent SDK — File Checkpointing Concepts

## Overview

**File checkpointing** is an Agent SDK feature that tracks file modifications made through the **Write**, **Edit**, and **NotebookEdit** tools during an agent session, allowing you to rewind files to any previous state. It exists so an SDK app can undo unwanted changes (restore files to a known-good state), explore alternatives (restore and try a different approach), and recover from errors when the agent makes incorrect modifications.

When checkpointing is enabled, the SDK creates backups of files before modifying them through those three tools, and the user messages in the response stream carry a **checkpoint UUID** that serves as a restore point. This note covers what the checkpoint system tracks and the boundaries of what it can recover; the enable→capture→rewind mechanics live in [SDK File Checkpointing Implementation](cc_sdk_file_checkpointing_implementation.md).

## How checkpointing works

When you enable file checkpointing, the SDK **creates backups of files before modifying them** through the Write, Edit, or NotebookEdit tools. User messages in the response stream include a checkpoint UUID that you can use as a restore point.

Checkpointing works with these built-in tools that the agent uses to modify files:

| Tool         | Description                                                        |
| ------------ | ------------------------------------------------------------------ |
| Write        | Creates a new file or overwrites an existing file with new content |
| Edit         | Makes targeted edits to specific parts of an existing file         |
| NotebookEdit | Modifies cells in Jupyter notebooks (`.ipynb` files)               |

### What the checkpoint tracks

The checkpoint system tracks:

- Files **created** during the session
- Files **modified** during the session
- The **original content** of modified files

When you rewind to a checkpoint, **created files are deleted** and **modified files are restored** to their content at that point.

### Files on disk, not the conversation

File rewinding restores files on disk to a previous state. It does **not** rewind the conversation itself — the conversation history and context remain intact after calling `rewindFiles()` (TypeScript) or `rewind_files()` (Python). Checkpointing is therefore purely a file-system recovery mechanism, separate from session/conversation state.

### Checkpoint UUID = user-message UUID

Each user message in the response stream has a UUID (surfaced when the `replay-user-messages` option is set) that serves as a checkpoint. For most use cases you capture the first user message UUID; rewinding to it restores all files to their original state. Capturing multiple UUIDs gives multiple restore points to rewind to intermediate states (the implementation note covers both patterns).

## Limitations

File checkpointing has the following limitations:

| Limitation                         | Description                                                          |
| ---------------------------------- | -------------------------------------------------------------------- |
| Write/Edit/NotebookEdit tools only | Changes made through Bash commands are not tracked                   |
| Same session                       | Checkpoints are tied to the session that created them                |
| File content only                  | Creating, moving, or deleting directories is not undone by rewinding |
| Local files                        | Remote or network files are not tracked                              |

The most consequential boundary is the first: only changes made through Write, Edit, and NotebookEdit are tracked, so file mutations via Bash commands (like `echo > file.txt` or `sed -i`) are **not** captured by the checkpoint system and cannot be rewound. Because checkpoints are tied to the originating session, a rewind after the stream completes requires resuming that same session (see implementation). Directory operations and remote/network files fall outside the tracked set entirely.

**Source**: https://code.claude.com/docs/en/agent-sdk/file-checkpointing
**Last Updated**: 2026-06-13
**Status**: Active
