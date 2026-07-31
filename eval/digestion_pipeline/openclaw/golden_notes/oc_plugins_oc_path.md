---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - oc_path
keywords:
  - oc-path plugin
  - oc:// workspace addressing
  - openclaw path cli
  - resolve find set validate emit
  - byte-fidelity file edits
  - redaction sentinel guard
  - opt-in bundled plugin
  - markdown jsonc jsonl yaml addressing
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/oc-path
access_control_group: ["general"]
---

# OpenClaw — The `oc-path` Plugin and the `oc://` Workspace-File Addressing Scheme

## Overview

This note is the procedure for the bundled, opt-in `oc-path` plugin, which ships the `openclaw path` CLI for the `oc://` workspace-file addressing scheme — mirroring the `plugins/oc-path` source page. `oc://` addresses point at a single leaf (or a wildcard set of leaves) inside a workspace file, and the plugin understands four file kinds: markdown, jsonc, jsonl, and yaml. The note covers why you would enable it, where it runs (in-process inside the `openclaw` CLI), how to enable/disable it, its plugin-local dependencies, the surfaces it provides, its relationship to other plugins, and the redaction-sentinel safety guard. The plugin ships in the OpenClaw repo under `extensions/oc-path/` but is opt-in — install/build leaves it dormant until you enable it.

## Addressing Model — Four File Kinds

`oc://` addresses point at a single leaf or a wildcard set of leaves inside a workspace file. The plugin understands four kinds of files today:

- **markdown** (`.md`, `.mdx`): frontmatter, sections, items, fields.
- **jsonc** (`.jsonc`, `.json5`, `.json`): comments and formatting preserved.
- **jsonl** (`.jsonl`, `.ndjson`): line-oriented records.
- **yaml** (`.yaml`, `.yml`, `.lobster`): map/sequence/scalar nodes through the YAML document API.

Self-hosters and editor extensions use the CLI to read or write a single leaf without scripting against the SDK directly; agents and hooks treat it as a deterministic substrate so byte-fidelity round-trips and the redaction-sentinel guard apply uniformly across kinds.

## Why Enable It

Enable `oc-path` when you want scripts, hooks, or local agent tooling to point at a precise piece of workspace state without inventing a parser for each file shape. A single `oc://` address can name a markdown frontmatter key, a section item, a JSONC config leaf, a JSONL event field, or a YAML workflow step. That matters for maintainer workflows where the change should be small, auditable, and repeatable: inspect one value, find matching records, dry-run a write, then apply only that leaf while leaving comments, line endings, and nearby formatting alone. Keeping this as an opt-in plugin gives power users the addressing substrate without putting parser dependencies or CLI surface into core for installs that never need it.

Common reasons to enable it, per source:

- **Local automation**: shell scripts can resolve or update one workspace value with `openclaw path … --json` instead of carrying separate markdown, JSONC, JSONL, and YAML parsing code.
- **Agent-visible edits**: an agent can show a dry-run diff for one addressed leaf before writing, which is easier to review than a free-form file rewrite.
- **Editor integrations**: an editor can map `oc://AGENTS.md/tools/gh` to the exact markdown node and line number without guessing from heading text.
- **Diagnostics**: `emit` round-trips a file through the parser and emitter, so you can check whether a file kind is byte-stable before relying on automated edits.

Concrete examples (verbatim from source):

```bash
# Is the GitHub plugin enabled in this config?
openclaw path resolve 'oc://config.jsonc/plugins/github/enabled' --json

# Which tool-call names appear in this session log?
openclaw path find 'oc://session.jsonl/[event=tool_call]/name' --json

# What bytes would this tiny config edit write?
openclaw path set 'oc://config.jsonc/plugins/github/enabled' 'true' --dry-run
```

The plugin is intentionally not the owner of higher-level semantics. Memory plugins still own memory writes, config commands still own full config management, and LKG logic still owns restore/promotion. `oc-path` is the narrow addressing and byte-preserving file operation layer those higher-level tools can build around.

## Where It Runs

The plugin runs **in-process inside the `openclaw` CLI** on the host where you invoke the command. It does not need a running Gateway and does not open any network sockets — every verb is a pure transform over a file you point it at. The plugin metadata lives in `extensions/oc-path/openclaw.plugin.json`:

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

`onStartup: false` keeps the plugin out of the Gateway hot path. `onCommands: ["path"]` tells the CLI to load the plugin lazily the first time you run `openclaw path …`, so installs that never use the verb pay no cost.

## Enable

Enable the plugin with:

```bash
openclaw plugins enable oc-path
```

Restart the Gateway (if you run one) so the manifest snapshot picks up the new state. Bare `openclaw path` invocations work immediately on the same host — the CLI loads the plugin on demand. Disable with:

```bash
openclaw plugins disable oc-path
```

## Dependencies

All parser dependencies are plugin-local — enabling `oc-path` does not pull new packages into the core runtime:

| Dependency     | Purpose                                                                |
| -------------- | ---------------------------------------------------------------------- |
| `commander`    | Subcommand wiring for `resolve`, `find`, `set`, `validate`, `emit`.    |
| `jsonc-parser` | JSONC parse + leaf edits with comments and trailing commas kept.       |
| `markdown-it`  | Markdown tokenization for the section / item / field model.            |
| `yaml`         | YAML `Document` parse / emit / edit with comments and flow style kept. |

JSONL stays hand-rolled — line-oriented parsing is simpler than any dependency, and the per-line JSONC parse already goes through `jsonc-parser`.

## What It Provides

| Surface                        | Provided by                                             |
| ------------------------------ | ------------------------------------------------------- |
| `openclaw path` CLI            | `extensions/oc-path/cli-registration.ts`                |
| `oc://` parser / formatter     | `extensions/oc-path/src/oc-path/oc-path.ts`             |
| Per-kind parse / emit / edit   | `extensions/oc-path/src/oc-path/{md,jsonc,jsonl,yaml}`  |
| Universal resolve / find / set | `extensions/oc-path/src/oc-path/{resolve,find,edit}.ts` |
| Redaction-sentinel guard       | `extensions/oc-path/src/oc-path/sentinel.ts`            |

The CLI is the only public surface today. The substrate verbs are private to the plugin; consumers use the CLI (or build their own plugin against the SDK).

## Relationship to Other Plugins

- **`memory-*`**: memory writes go through the memory plugins, not `oc-path`. `oc-path` is a generic file substrate; memory plugins layer their own semantics on top.
- **LKG**: `path` does not know about Last-Known-Good config restore. If a file is LKG-tracked, the next `observe` call decides whether to promote or recover; `set --batch` for atomic multi-set through the LKG promote/recover lifecycle is planned alongside the LKG-recovery substrate.

## Safety

`set` writes raw bytes through the substrate's emit path, which applies the redaction-sentinel guard automatically. A leaf carrying `__OPENCLAW_REDACTED__` (verbatim or as a substring) is refused at write time with `OC_EMIT_SENTINEL`. The CLI also scrubs the literal sentinel from any human or JSON output it prints, replacing it with `[REDACTED]` so terminal captures and pipelines never leak the marker.

**Source**: OpenClaw documentation — `plugins/oc-path` (mirror `inbox/openclaw_docs/plugins/oc-path.md`)
**Last Updated**: 2026-06-22
**Status**: Active
