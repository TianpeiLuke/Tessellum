---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - install
keywords:
  - openclaw plugin install overrides
  - OPENCLAW_PLUGIN_INSTALL_OVERRIDES
  - OPENCLAW_ALLOW_PLUGIN_INSTALL_OVERRIDES
  - npm-pack tarball override
  - setup-time plugin installer
  - package e2e isolated state dir
  - override manifest id enforcement
  - untrusted operator install input
topics:
  - OpenClaw
  - Plugin Install Overrides
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/install-overrides
access_control_group: ["general"]
---

# OpenClaw — Plugin Install Overrides (E2E / Package Testing)

## Overview

This note is the procedure for **plugin install overrides** — a maintainer-only mechanism that redirects OpenClaw's setup-time plugin installs to a specific npm package or a local `npm pack` tarball, for E2E and package validation only. It mirrors the `plugins/install-overrides` source page: the two environment variables that gate the feature (`OPENCLAW_ALLOW_PLUGIN_INSTALL_OVERRIDES` + `OPENCLAW_PLUGIN_INSTALL_OVERRIDES`), the `npm:` / `npm-pack:` override-map value forms, the runtime behavior (source substitution, id enforcement, trust caveat, `.env` exclusion), and the isolated-state-dir package E2E flow. Normal users do NOT use overrides — they install plugins with `openclaw plugins install` instead.

Per the source, overrides **execute plugin code from the source you provide**, so they must be used only in an isolated state directory or a disposable test machine.

## Environment

Overrides are disabled unless **both** variables are set:

```bash
export OPENCLAW_ALLOW_PLUGIN_INSTALL_OVERRIDES=1
export OPENCLAW_PLUGIN_INSTALL_OVERRIDES='{
  "codex": "npm-pack:/tmp/openclaw-codex-2026.5.8.tgz",
  "openclaw-web-search": "npm:@openclaw/web-search@2026.5.8"
}'
```

`OPENCLAW_PLUGIN_INSTALL_OVERRIDES` is a **JSON object keyed by plugin id**. Each value selects an install source for that id:

- `npm:<registry-spec>` — for registry packages, supporting exact versions or tags (e.g. `npm:@openclaw/web-search@2026.5.8`).
- `npm-pack:<path.tgz>` — for local tarballs produced by `npm pack` (e.g. `npm-pack:/tmp/openclaw-codex-2026.5.8.tgz`).

Relative `npm-pack:` paths resolve **from the current working directory**.

## Behavior

When a setup-time flow asks to install a plugin whose id appears in the override map, OpenClaw uses the **override source instead of the catalog, bundled, or default npm source**. This applies to onboarding and other flows that use the shared setup-time plugin installer.

Overrides still **enforce the expected plugin id**: a tarball mapped to `codex` must install a plugin whose manifest id is `codex`.

Overrides **do not inherit official trusted-source status**. Even when the catalog entry normally represents an OpenClaw-owned package, an override is treated as **operator-supplied test input**.

Workspace `.env` files **cannot enable install overrides**. Set these variables in the trusted shell, CI job, or remote test command that launches OpenClaw.

## Package E2E

Use an **isolated state directory** so package installs and install records do not touch your normal OpenClaw state. Pack the local extension, then launch onboarding with the override active against a throwaway `OPENCLAW_STATE_DIR`:

```bash
npm pack extensions/codex --pack-destination /tmp

OPENCLAW_STATE_DIR="$(mktemp -d)" \
OPENCLAW_ALLOW_PLUGIN_INSTALL_OVERRIDES=1 \
OPENCLAW_PLUGIN_INSTALL_OVERRIDES='{"codex":"npm-pack:/tmp/openclaw-codex-2026.5.8.tgz"}' \
pnpm openclaw onboard --mode local
```

Verify the installed package under the state directory:

```bash
find "$OPENCLAW_STATE_DIR/npm/projects" -path '*/node_modules/@openclaw/codex/package.json' -print
grep -R '"@openclaw/codex"' "$OPENCLAW_STATE_DIR/npm/projects"/*/package-lock.json
```

For live provider E2E, **source the real API key from a trusted shell or CI secret** before launching the test command. Do not print keys; report only the source and whether the key was present.

**Source**: OpenClaw documentation — `plugins/install-overrides` (mirror `inbox/openclaw_docs/plugins/install-overrides.md`)
**Last Updated**: 2026-06-22
**Status**: Active
