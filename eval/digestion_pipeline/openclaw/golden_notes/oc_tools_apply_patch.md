---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - apply_patch
keywords:
  - openclaw apply_patch tool
  - apply patch envelope format
  - begin patch end patch
  - multi-file structured edit
  - tools.exec.applyPatch.workspaceOnly
  - tools.exec.applyPatch.allowModels
  - add file update file delete file move to
  - openai codex apply_patch default
topics:
  - OpenClaw
  - Tools
  - File Editing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/apply-patch
access_control_group: ["general"]
---

# OpenClaw — The `apply_patch` File-Edit Tool

## Overview

This note documents OpenClaw's **`apply_patch`** agent tool, which applies file changes through a structured, multi-file patch format — mirroring the `tools/apply-patch` source page (intro, Parameters, Notes, Example). `apply_patch` is positioned as the right tool for **multi-file or multi-hunk edits where a single `edit` call would be brittle**: the agent emits one patch envelope describing add/update/delete/move operations, and the tool applies them in one call. The procedure below covers the patch envelope syntax, the single `input` parameter, the behavior notes (relative/absolute paths, the `workspaceOnly` default, in-hunk `*** Move to:`, EOF inserts, model-default availability, enable/`allowModels` gating, and the `tools.exec`-only config location), and a worked example.

## What `apply_patch` Is For

`apply_patch` applies file changes using a structured patch format. The source page frames it as **ideal for multi-file or multi-hunk edits where a single `edit` call would be brittle** — instead of issuing many fragile single-region edits, the agent sends one patch describing all operations at once.

## Patch Envelope Format

The tool accepts a single `input` string that wraps one or more file operations. The envelope begins with `*** Begin Patch` and ends with `*** End Patch`, with each operation introduced by an `*** Add File:`, `*** Update File:`, or `*** Delete File:` marker. Update hunks use a `@@` separator with `-` lines (removed) and `+` lines (added); Add operations list `+`-prefixed new lines:

```
*** Begin Patch
*** Add File: path/to/file.txt
+line 1
+line 2
*** Update File: src/app.ts
@@
-old line
+new line
*** Delete File: obsolete.txt
*** End Patch
```

## Parameters

The tool exposes a single parameter:

- **`input`** (required): Full patch contents including `*** Begin Patch` and `*** End Patch`.

## Behavior Notes

The source page lists the following behavior and configuration notes for `apply_patch`:

- Patch paths support **relative paths** (from the workspace directory) **and absolute paths**.
- **`tools.exec.applyPatch.workspaceOnly`** defaults to `true` (workspace-contained). Set it to `false` only if you intentionally want `apply_patch` to write/delete outside the workspace directory.
- Use **`*** Move to:`** within an `*** Update File:` hunk to **rename files**.
- **`*** End of File`** marks an EOF-only insert when needed.
- Available by default for **OpenAI and OpenAI Codex models**. Set **`tools.exec.applyPatch.enabled: false`** to disable it.
- Optionally gate by model via **`tools.exec.applyPatch.allowModels`**.
- Config is only under **`tools.exec`**.

## Example

A single-hunk update of `src/index.ts`, sent as the tool call's structured payload (the `input` string carries the full `*** Begin Patch ... *** End Patch` envelope with embedded `\n` line breaks):

```json
{
  "tool": "apply_patch",
  "input": "*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch"
}
```

**Source**: OpenClaw documentation — `tools/apply-patch` (mirror `inbox/openclaw_docs/tools/apply-patch.md`)
**Last Updated**: 2026-06-22
**Status**: Active
