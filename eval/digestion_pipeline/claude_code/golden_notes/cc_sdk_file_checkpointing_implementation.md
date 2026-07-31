---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - file_checkpointing
keywords:
  - file checkpointing implementation
  - enable_file_checkpointing
  - replay-user-messages
  - rewind_files
  - checkpoint uuid
  - resume session rewind
  - checkpoint before risky operations
  - multiple restore points
  - rewind-files cli
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/file-checkpointing
access_control_group: ["general"]
---

# Claude Code SDK — Implement File Checkpointing

## Overview

This note is the procedure for wiring file checkpointing into a Claude Agent SDK application: how to enable it, capture checkpoint UUIDs from the response stream, and rewind files to a previous state with `rewind_files()` (Python) / `rewindFiles()` (TypeScript). It also covers two reusable capture patterns (checkpoint-before-risky-operations and multiple restore points) and the four documented troubleshooting cases. For *what* checkpointing tracks and its limitations (the concept layer), see the sibling note [Checkpointing Concepts](cc_sdk_file_checkpointing_concepts.md).

The implementation hinges on three SDK pieces: the `enable_file_checkpointing` option, the `extra_args={"replay-user-messages": None}` flag that surfaces checkpoint UUIDs in the stream, and (for rewinding after a stream completes) resuming the session by its `session_id`. Code blocks below show the representative Python form; the TypeScript equivalent of each is available in the TypeScript SDK reference.

## Implement checkpointing

To use file checkpointing, enable it in your options, capture checkpoint UUIDs from the response stream, then call `rewindFiles()` (TypeScript) or `rewind_files()` (Python) when you need to restore. The complete flow is enable checkpointing, capture the checkpoint UUID and session ID from the response stream, then resume the session later to rewind files.

```python
import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    UserMessage,
    ResultMessage,
)


async def main():
    # Step 1: Enable checkpointing
    options = ClaudeAgentOptions(
        enable_file_checkpointing=True,
        permission_mode="acceptEdits",  # Auto-accept file edits without prompting
        extra_args={
            "replay-user-messages": None
        },  # Required to receive checkpoint UUIDs in the response stream
    )

    checkpoint_id = None
    session_id = None

    # Run the query and capture checkpoint UUID and session ID
    async with ClaudeSDKClient(options) as client:
        await client.query("Refactor the authentication module")

        # Step 2: Capture checkpoint UUID from the first user message
        async for message in client.receive_response():
            if isinstance(message, UserMessage) and message.uuid and not checkpoint_id:
                checkpoint_id = message.uuid
            if isinstance(message, ResultMessage) and not session_id:
                session_id = message.session_id

    # Step 3: Later, rewind by resuming the session with an empty prompt
    if checkpoint_id and session_id:
        async with ClaudeSDKClient(
            ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
        ) as client:
            await client.query("")  # Empty prompt to open the connection
            async for message in client.receive_response():
                await client.rewind_files(checkpoint_id)
                break
        print(f"Rewound to checkpoint: {checkpoint_id}")


asyncio.run(main())
```

### Step 1 — Enable checkpointing

Configure your SDK options to enable checkpointing and receive checkpoint UUIDs. Two options matter:

| Option | Python | TypeScript | Description |
|---|---|---|---|
| Enable checkpointing | `enable_file_checkpointing=True` | `enableFileCheckpointing: true` | Tracks file changes for rewinding |
| Receive checkpoint UUIDs | `extra_args={"replay-user-messages": None}` | `extraArgs: { 'replay-user-messages': null }` | Required to get user message UUIDs in the stream |

The examples also set `permission_mode="acceptEdits"` to auto-accept file edits without prompting.

### Step 2 — Capture checkpoint UUID and session ID

With the `replay-user-messages` option set, each user message in the response stream has a UUID that serves as a checkpoint. For most use cases, capture the first user message UUID (`message.uuid`); rewinding to it restores all files to their original state. To store multiple checkpoints and rewind to intermediate states, see [Multiple restore points](#multiple-restore-points).

Capturing the session ID (`message.session_id`) is optional — you only need it if you want to rewind *later*, after the stream completes. If you call `rewind_files()` immediately while still processing messages (as the [Checkpoint before risky operations](#checkpoint-before-risky-operations) pattern does), you can skip capturing the session ID.

### Step 3 — Rewind files

To rewind after the stream completes, resume the session with an empty prompt and call `rewind_files()` (Python) / `rewindFiles()` (TypeScript) with your checkpoint UUID. You can also rewind during the stream (see the risky-operations pattern). If you capture the session ID and checkpoint ID, you can also rewind from the CLI:

```bash
claude -p --resume <session-id> --rewind-files <checkpoint-uuid>
```

## Common patterns

These patterns show different ways to capture and use checkpoint UUIDs depending on the use case.

### Checkpoint before risky operations

This pattern keeps only the *most recent* checkpoint UUID, updating it before each agent turn. If something goes wrong during processing, you can immediately rewind to the last safe state and break out of the loop — note that rewind happens inline within the response loop, so no `session_id` capture or resume is needed.

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, UserMessage


async def main():
    options = ClaudeAgentOptions(
        enable_file_checkpointing=True,
        permission_mode="acceptEdits",
        extra_args={"replay-user-messages": None},
    )

    safe_checkpoint = None

    async with ClaudeSDKClient(options) as client:
        await client.query("Refactor the authentication module")

        async for message in client.receive_response():
            # Update checkpoint before each agent turn starts
            # This overwrites the previous checkpoint. Only keep the latest
            if isinstance(message, UserMessage) and message.uuid:
                safe_checkpoint = message.uuid

            # Decide when to revert based on your own logic
            # For example: error detection, validation failure, or user input
            if your_revert_condition and safe_checkpoint:
                await client.rewind_files(safe_checkpoint)
                # Exit the loop after rewinding, files are restored
                break


asyncio.run(main())
```

### Multiple restore points

If Claude makes changes across multiple turns, you might want to rewind to a *specific* point rather than all the way back — for example, if Claude refactors a file in turn one and adds tests in turn two, you might keep the refactor but undo the tests. This pattern stores all checkpoint UUIDs in an array with metadata; after the session completes, you can rewind to any previous checkpoint by resuming the session.

```python
import asyncio
from dataclasses import dataclass
from datetime import datetime
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    UserMessage,
    ResultMessage,
)


# Store checkpoint metadata for better tracking
@dataclass
class Checkpoint:
    id: str
    description: str
    timestamp: datetime


async def main():
    options = ClaudeAgentOptions(
        enable_file_checkpointing=True,
        permission_mode="acceptEdits",
        extra_args={"replay-user-messages": None},
    )

    checkpoints = []
    session_id = None

    async with ClaudeSDKClient(options) as client:
        await client.query("Refactor the authentication module")

        async for message in client.receive_response():
            if isinstance(message, UserMessage) and message.uuid:
                checkpoints.append(
                    Checkpoint(
                        id=message.uuid,
                        description=f"After turn {len(checkpoints) + 1}",
                        timestamp=datetime.now(),
                    )
                )
            if isinstance(message, ResultMessage) and not session_id:
                session_id = message.session_id

    # Later: rewind to any checkpoint by resuming the session
    if checkpoints and session_id:
        target = checkpoints[0]  # Pick any checkpoint
        async with ClaudeSDKClient(
            ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
        ) as client:
            await client.query("")  # Empty prompt to open the connection
            async for message in client.receive_response():
                await client.rewind_files(target.id)
                break
        print(f"Rewound to: {target.description}")


asyncio.run(main())
```

## Try it out

The docs ship a complete interactive example that creates a small utility file (`utils.py` / `utils.ts`), has the agent add documentation comments, shows you the changes, then asks if you want to rewind. The end-to-end workflow it demonstrates is:

1. **Enable checkpointing** — configure the SDK with `enable_file_checkpointing=True` and `permission_mode="acceptEdits"` to auto-approve file edits.
2. **Capture checkpoint data** — as the agent runs, store the first user message UUID (your restore point) and the session ID.
3. **Prompt for rewind** — after the agent finishes, check the utility file to see the doc comments, then decide if you want to undo the changes.
4. **Resume and rewind** — if yes, resume the session with an empty prompt and call `rewind_files()` to restore the original file.

Run it from the same directory as the utility file with `python try_checkpointing.py` (Python) or `npx tsx try_checkpointing.ts` (TypeScript). Open the utility file in your editor first to watch it update in real time and then revert on rewind. (Requires the Claude Agent SDK installed — see the SDK quickstart.) The full script source for both languages is in the source page.

## Limitations

File checkpointing has the following limitations:

| Limitation | Description |
|---|---|
| Write/Edit/NotebookEdit tools only | Changes made through Bash commands are not tracked |
| Same session | Checkpoints are tied to the session that created them |
| File content only | Creating, moving, or deleting directories is not undone by rewinding |
| Local files | Remote or network files are not tracked |

## Troubleshooting

### Checkpointing options not recognized

If `enableFileCheckpointing` or `rewindFiles()` isn't available, you may be on an older SDK version. **Solution**: update to the latest SDK — Python `pip install --upgrade claude-agent-sdk`; TypeScript `npm install @anthropic-ai/claude-agent-sdk@latest`.

### User messages don't have UUIDs

If `message.uuid` is `undefined` or missing, you're not receiving checkpoint UUIDs. **Cause**: the `replay-user-messages` option isn't set. **Solution**: add `extra_args={"replay-user-messages": None}` (Python) or `extraArgs: { 'replay-user-messages': null }` (TypeScript) to your options.

### "No file checkpoint found for message" error

This occurs when the checkpoint data doesn't exist for the specified user message UUID. **Common causes**: file checkpointing was not enabled on the original session (`enable_file_checkpointing` / `enableFileCheckpointing` not set to `true`); or the session wasn't properly completed before attempting to resume and rewind. **Solution**: ensure checkpointing was set on the original session, then use the pattern from the examples — capture the first user message UUID, complete the session fully, then resume with an empty prompt and call `rewindFiles()` once.

### "ProcessTransport is not ready for writing" error

This occurs when you call `rewindFiles()` / `rewind_files()` after you've finished iterating through the response — the connection to the CLI process closes when the loop completes. **Solution**: resume the session with an empty prompt, then call rewind on the new query (the Step 3 resume-then-rewind pattern shown above).

**Source**: https://code.claude.com/docs/en/agent-sdk/file-checkpointing
**Last Updated**: 2026-06-13
**Status**: Active
