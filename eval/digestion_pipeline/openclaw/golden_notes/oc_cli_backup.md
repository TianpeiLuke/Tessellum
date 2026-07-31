---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - backup
keywords:
  - openclaw backup
  - openclaw backup create
  - openclaw backup verify
  - backup archive manifest.json
  - what gets backed up
  - no-include-workspace only-config
  - skippedVolatileCount
  - invalid config recovery backup
topics:
  - OpenClaw
  - CLI Backup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/backup
access_control_group: ["general"]
---

# OpenClaw — `openclaw backup` (Local State Backup Archives)

## Overview

This note is the procedure reference for `openclaw backup`, the OpenClaw CLI command that creates a local backup archive of OpenClaw state, config, auth profiles, channel/provider credentials, sessions, and optionally workspaces. It mirrors the `cli/backup` source page: the `create`/`verify` invocations, the archive `manifest.json` and default `.tar.gz` naming, exactly what gets backed up (state directory, active config, external `credentials/`, workspaces) versus what is skipped (volatile live-mutation files, `node_modules/`), the `--no-include-workspace`/`--only-config`/`--verify`/`--dry-run` flags, the invalid-config recovery path, and size/performance considerations. Operators run this before a `reset` or `uninstall`, or to preview included paths via `--dry-run --json`.

## What the Command Does

`openclaw backup create` produces a first-class backup archive for local OpenClaw state. The archive includes a `manifest.json` file with the resolved source paths and archive layout. The default output is a timestamped `.tar.gz` archive in the current working directory; timestamped backup filenames use your machine's local timezone and include the UTC offset (e.g. `2026-03-09T08-00-00.000+08-00-openclaw-backup.tar.gz`). If the current working directory is inside a backed-up source tree, OpenClaw falls back to your home directory for the default archive location. Existing archive files are never overwritten, and output paths inside the source state/workspace trees are rejected to avoid self-inclusion.

## Examples

```bash
openclaw backup create
openclaw backup create --output ~/Backups
openclaw backup create --dry-run --json
openclaw backup create --verify
openclaw backup create --no-include-workspace
openclaw backup create --only-config
openclaw backup verify ./2026-03-09T08-00-00.000+08-00-openclaw-backup.tar.gz
```

`openclaw backup create --verify` runs the verification validation immediately after writing the archive. `openclaw backup create --only-config` backs up just the active JSON config file.

## What Gets Backed Up

`openclaw backup create` plans backup sources from your local OpenClaw install:

- The state directory returned by OpenClaw's local state resolver, usually `~/.openclaw`.
- The active config file path.
- The resolved `credentials/` directory when it exists outside the state directory.
- Workspace directories discovered from the current config, unless you pass `--no-include-workspace`.

Model auth profiles are already part of the state directory under `agents/<agentId>/agent/auth-profiles.json`, so they are normally covered by the state backup entry. If you use `--only-config`, OpenClaw skips state, credentials-directory, and workspace discovery and archives only the active config file path.

OpenClaw canonicalizes paths before building the archive. If config, the credentials directory, or a workspace already live inside the state directory, they are not duplicated as separate top-level backup sources. Missing paths are skipped. The archive payload stores file contents from those source trees, and the embedded `manifest.json` records the resolved absolute source paths plus the archive layout used for each asset.

### Skipped Volatile Files and `node_modules/`

During archive creation, OpenClaw skips known live-mutation files that do not have restoration value, including active agent session transcripts, cron run logs, rolling logs, delivery queues, socket/pid/temp files under the state directory, and related durable-queue temp files. The JSON result includes `skippedVolatileCount` so automation can see how many files were intentionally omitted. Installed plugin source and manifest files under the state directory's `extensions/` tree are included, but their nested `node_modules/` dependency trees are skipped — those dependencies are rebuildable install artifacts. After restoring an archive, use `openclaw plugins update <id>` or reinstall the plugin with `openclaw plugins install <spec> --force` when a restored plugin reports missing dependencies.

## Verify Semantics

`openclaw backup verify <archive>` validates that the archive contains exactly one root manifest, rejects traversal-style archive paths, and checks that every manifest-declared payload exists in the tarball. Passing `--verify` to `openclaw backup create` runs that same validation immediately after the archive is written, so a single create-and-verify pass confirms the new archive is structurally complete before you rely on it.

## Invalid Config Behavior

`openclaw backup` intentionally bypasses the normal config preflight so it can still help during recovery. Because workspace discovery depends on a valid config, `openclaw backup create` now fails fast when the config file exists but is invalid and workspace backup is still enabled. If you still want a partial backup in that situation, rerun with workspace discovery disabled:

```bash
openclaw backup create --no-include-workspace
```

That keeps state, config, and the external credentials directory in scope while skipping workspace discovery entirely. If you only need a copy of the config file itself, `--only-config` also works when the config is malformed because it does not rely on parsing the config for workspace discovery.

## Size and Performance

OpenClaw does not enforce a built-in maximum backup size or per-file size limit. Practical limits come from the local machine and destination filesystem:

- Available space for the temporary archive write plus the final archive.
- Time to walk large workspace trees and compress them into a `.tar.gz`.
- Time to rescan the archive if you use `openclaw backup create --verify` or run `openclaw backup verify`.
- Filesystem behavior at the destination path. OpenClaw prefers a no-overwrite hard-link publish step and falls back to exclusive copy when hard links are unsupported.

Large workspaces are usually the main driver of archive size. If you want a smaller or faster backup, use `--no-include-workspace`. For the smallest archive, use `--only-config`.

**Source**: OpenClaw documentation — `cli/backup` (mirror `inbox/openclaw_docs/cli/backup.md`)
**Last Updated**: 2026-06-22
**Status**: Active
