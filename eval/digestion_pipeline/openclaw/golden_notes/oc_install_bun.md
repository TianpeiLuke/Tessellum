---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - bun
keywords:
  - openclaw bun runtime
  - bun install no-save
  - bun run build vitest
  - bun pm trust baileys protobufjs
  - bun lifecycle scripts blocked
  - bun not recommended gateway runtime
  - pnpm hardcoded scripts
  - bun ignores pnpm-lock
topics:
  - OpenClaw
  - Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/bun
access_control_group: ["general"]
---

# OpenClaw — Bun Experimental Local Runtime

## Overview

This note is a procedure for using **Bun as an optional, experimental local runtime** for the OpenClaw monorepo — the `bun install` / `bun run` dev loop, the blocked dependency lifecycle scripts and how to trust them, and the pnpm-hardcoded-script caveats. It mirrors the `install/bun` source page. The page opens with a load-bearing warning: Bun is **not recommended for gateway runtime** (known issues with WhatsApp and Telegram), so Node should be used for production, and the **default package manager remains `pnpm`** (fully supported and used by docs tooling). Bun is an optional local runtime for running TypeScript directly (`bun run ...`, `bun --watch ...`); because Bun cannot use `pnpm-lock.yaml` and will ignore it, this path is a developer-convenience dev loop, not a supported install method.

## Install

Install dependencies with `bun install`. The page notes that `bun.lock` / `bun.lockb` are gitignored, so there is no repo churn from running this. To skip lockfile writes entirely, pass `--no-save`:

```sh
bun install
bun install --no-save
```

Build and test the repo through Bun's script runner:

```sh
bun run build
bun run vitest run
```

## Lifecycle scripts

Bun **blocks dependency lifecycle scripts unless explicitly trusted**. For this repo, the commonly blocked scripts are *not required*, so the block is normally harmless:

- `baileys` `preinstall` — checks Node major >= 20 (OpenClaw defaults to Node 24 and still supports Node 22 LTS, currently `22.19+`).
- `protobufjs` `postinstall` — emits warnings about incompatible version schemes (no build artifacts).

If you hit a runtime issue that requires these scripts, trust them explicitly with `bun pm trust`:

```sh
bun pm trust baileys protobufjs
```

## Caveats

Some scripts still **hardcode pnpm** (for example `check:docs`, `ui:*`, `protocol:check`). The source instructs running those via pnpm for now — Bun's script runner does not transparently substitute for pnpm in these cases, so a Bun-only setup is incomplete and the developer must keep pnpm available for the hardcoded scripts.

**Source**: OpenClaw documentation — `install/bun` (mirror `inbox/openclaw_docs/install/bun.md`)
**Last Updated**: 2026-06-22
**Status**: Active
