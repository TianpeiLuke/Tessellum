---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - oc_path
keywords:
  - openclaw oc-path plugin
  - oc:// workspace addressing
  - openclaw path cli
  - workspace file leaf addressing
  - plugin surface plugin
  - included in openclaw
  - redaction sentinel guard
  - byte-preserving file edit
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/oc-path
access_control_group: ["general"]
---

# OpenClaw — `oc-path` Plugin (`oc://` Workspace File Addressing)

## Overview

This note documents the OpenClaw **`oc-path`** built-in plugin, mirroring the `plugins/reference/oc-path` reference stub and the deeper `plugins/oc-path` page. `oc-path` adds the `openclaw path` CLI for the **`oc://` workspace-file addressing scheme** — a deterministic way to name a single leaf (or wildcard set of leaves) inside a workspace file and read or write it with byte-fidelity. Unlike the model-provider reference plugins, its declared `## Surface` is `plugin` (a CLI/addressing capability, not a model `providers:` registration). It ships in OpenClaw (npm `@openclaw/oc-path`), and the per-provider/deeper CLI semantics live in the `plugins/oc-path` and `cli/path` docs this stub points to.

## Distribution

Per the reference stub's `## Distribution` section, the plugin is published and bundled as follows:

- **Package**: `@openclaw/oc-path`
- **Install route**: included in OpenClaw

The deeper `plugins/oc-path` page adds that, although bundled, the plugin is **opt-in**: it "ships in the OpenClaw repo under `extensions/oc-path/`" but "install/build leaves it dormant until you enable it." Enable and disable it via the CLI:

```bash
openclaw plugins enable oc-path
openclaw plugins disable oc-path
```

After enabling, restart the Gateway (if one is running) so the manifest snapshot picks up the new state; bare `openclaw path` invocations work immediately on the same host because the CLI loads the plugin on demand.

## Surface

The reference stub's `## Surface` section lists a single value: **`plugin`**. This is the surface type — `oc-path` contributes a CLI/addressing capability rather than a model `providers:` entry or a `skills` pack. The plugin metadata in `extensions/oc-path/openclaw.plugin.json` declares this lazy CLI surface verbatim:

```json
{
  "id": "oc-path",
  "name": "OC Path",
  "activation": {
    "onStartup": false,
    "onCommands": ["path"]
  },
  "commandAliases": [{ "name": "path", "kind": "cli" }]
}
```

`onStartup: false` keeps the plugin out of the Gateway hot path; `onCommands: ["path"]` tells the CLI to load it lazily the first time you run `openclaw path …`, so installs that never use the verb pay no cost. The plugin runs **in-process inside the `openclaw` CLI** on the host where you invoke the command — it does not need a running Gateway and does not open any network sockets; every verb is a pure transform over a file you point it at. The CLI is the only public surface today; the substrate verbs are private to the plugin (consumers use the CLI or build their own plugin against the SDK).

### What `oc://` addresses

An `oc://` address points at a single leaf, or a wildcard set of leaves, inside a workspace file. The plugin understands four file kinds today: **markdown** (`.md`, `.mdx`: frontmatter, sections, items, fields), **jsonc** (`.jsonc`, `.json5`, `.json`: comments and formatting preserved), **jsonl** (`.jsonl`, `.ndjson`: line-oriented records), and **yaml** (`.yaml`, `.yml`, `.lobster`: map/sequence/scalar nodes through the YAML document API). A single address can name a markdown frontmatter key, a section item, a JSONC config leaf, a JSONL event field, or a YAML workflow step, so scripts, hooks, and agent tooling can target precise workspace state without inventing a parser per file shape. Self-hosters and editor extensions use the CLI to read or write one leaf without scripting against the SDK directly, while agents and hooks treat it as a deterministic substrate so byte-fidelity round-trips and the redaction-sentinel guard apply uniformly across kinds.

The `openclaw path` CLI exposes the verbs `resolve`, `find`, `set`, `validate`, and `emit`. Concrete examples from the source page:

```bash
openclaw path resolve 'oc://config.jsonc/plugins/github/enabled' --json
openclaw path find 'oc://session.jsonl/[event=tool_call]/name' --json
openclaw path set 'oc://config.jsonc/plugins/github/enabled' 'true' --dry-run
```

`emit` round-trips a file through the parser and emitter so you can check whether a file kind is byte-stable before relying on automated edits. The `set` verb writes raw bytes through the substrate's emit path, which applies the **redaction-sentinel guard** automatically: a leaf carrying `__OPENCLAW_REDACTED__` (verbatim or as a substring) is refused at write time with `OC_EMIT_SENTINEL`, and the CLI scrubs the literal sentinel from any human or JSON output, replacing it with `[REDACTED]` so terminal captures and pipelines never leak the marker. All parser dependencies are plugin-local (`commander`, `jsonc-parser`, `markdown-it`, `yaml`; JSONL parsing is hand-rolled), so enabling `oc-path` does not pull new packages into the core runtime. The plugin is intentionally not the owner of higher-level semantics: memory plugins still own memory writes, config commands still own full config management, and LKG logic still owns restore/promotion — `oc-path` is the narrow addressing and byte-preserving file-operation layer those higher-level tools build around.

**Source**: OpenClaw documentation — `plugins/reference/oc-path` (mirror `inbox/openclaw_docs/plugins/reference/oc-path.md`; deeper page `inbox/openclaw_docs/plugins/oc-path.md`)
**Last Updated**: 2026-06-22
**Status**: Active
