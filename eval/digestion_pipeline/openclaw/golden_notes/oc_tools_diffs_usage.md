---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - diffs
keywords:
  - openclaw diffs tool
  - diff viewer plugin
  - openclaw plugins install diffs
  - diffs tool input reference
  - before after patch mode
  - diffs syntax highlighting language pack
  - diffs plugin defaults
  - viewerBaseUrl persistent viewer url
topics:
  - OpenClaw
  - Diffs Tool
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/diffs
access_control_group: ["general"]
---

# OpenClaw — Using the `diffs` Diff-Viewer Plugin Tool

## Overview

This note is the usage/config procedure for OpenClaw's `diffs` tool — an optional plugin tool with short built-in system guidance and a companion skill that turns change content into a read-only diff artifact for agents. It mirrors the install/enable/mode steps, the disable-guidance toggle, the typical agent workflow, the input examples, the full tool-input reference, syntax-highlighting languages, plugin-wide defaults, and persistent viewer-URL config from the `tools/diffs` source page. The viewer-artifact output `details` contract, artifact lifecycle/storage, viewer URL + network behavior, the security model, browser requirements, and troubleshooting are the model/security half and are documented in the split sibling **[oc_tools_diffs_viewer_security](oc_tools_diffs_viewer_security.md)**.

The `diffs` tool accepts either `before` and `after` text, or a unified `patch`. It can return a gateway viewer URL for canvas presentation, a rendered file path (PNG or PDF) for message delivery, or both outputs in one call. When enabled, the plugin prepends concise usage guidance into system-prompt space and also exposes a detailed skill for cases where the agent needs fuller instructions.

## Quick Start

Install, enable, then pick an output mode.

1. **Install the plugin.**

```bash
openclaw plugins install diffs
```

2. **Enable the plugin** in OpenClaw config:

```json5
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
      },
    },
  },
}
```

3. **Pick a mode** — the agent passes a `mode` on the `diffs` call:
- `view` — canvas-first flows: agents call `diffs` with `mode: "view"` and open `details.viewerUrl` with `canvas present`.
- `file` — chat file delivery: agents call `diffs` with `mode: "file"` and send `details.filePath` with `message` using `path` or `filePath`.
- `both` — combined: agents call `diffs` with `mode: "both"` to get both artifacts in one call.

## Disable Built-in System Guidance

If you want to keep the `diffs` tool enabled but disable its built-in system-prompt guidance, set `plugins.entries.diffs.hooks.allowPromptInjection` to `false`:

```json5
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
        hooks: {
          allowPromptInjection: false,
        },
      },
    },
  },
}
```

This blocks the diffs plugin's `before_prompt_build` hook while keeping the plugin, tool, and companion skill available. If you want to disable both the guidance and the tool, disable the plugin instead.

## Typical Agent Workflow

The agent runs three steps: (1) **Call `diffs`** — the agent calls the `diffs` tool with input; (2) **Read details** — the agent reads `details` fields from the response; (3) **Present** — the agent either opens `details.viewerUrl` with `canvas present`, sends `details.filePath` with `message` using `path` or `filePath`, or does both.

## Input Examples

The tool takes either before/after text plus a display path (first example), or a unified patch (second example):

```json
// before-and-after input
{
  "before": "# Hello\n\nOne",
  "after": "# Hello\n\nTwo",
  "path": "docs/example.md",
  "mode": "view"
}
// patch input
{
  "patch": "diff --git a/src/example.ts b/src/example.ts\n--- a/src/example.ts\n+++ b/src/example.ts\n@@ -1 +1 @@\n-const x = 1;\n+const x = 2;\n",
  "mode": "both"
}
```

## Tool Input Reference

All fields are optional unless noted.

| Field | Type | Notes |
|---|---|---|
| `before` | string | Original text. Required with `after` when `patch` is omitted. |
| `after` | string | Updated text. Required with `before` when `patch` is omitted. |
| `patch` | string | Unified diff text. Mutually exclusive with `before` and `after`. |
| `path` | string | Display filename for before and after mode. |
| `lang` | string | Language override hint for before and after mode. Unknown values and languages outside the default viewer set fall back to plain text unless the Diff Viewer Language Pack plugin is installed. |
| `title` | string | Viewer title override. |
| `mode` | `"view" \| "file" \| "both"` | Output mode. Defaults to plugin default `defaults.mode`. Deprecated alias: `"image"` behaves like `"file"` and is still accepted for backward compatibility. |
| `theme` | `"light" \| "dark"` | Viewer theme. Defaults to plugin default `defaults.theme`. |
| `layout` | `"unified" \| "split"` | Diff layout. Defaults to plugin default `defaults.layout`. |
| `expandUnchanged` | boolean | Expand unchanged sections when full context is available. Per-call option only (not a plugin default key). |
| `fileFormat` | `"png" \| "pdf"` | Rendered file format. Defaults to plugin default `defaults.fileFormat`. |
| `fileQuality` | `"standard" \| "hq" \| "print"` | Quality preset for PNG or PDF rendering. |
| `fileScale` | number | Device scale override (`1`-`4`). |
| `fileMaxWidth` | number | Max render width in CSS pixels (`640`-`2400`). |
| `ttlSeconds` | number (default `1800`) | Artifact TTL in seconds for viewer and standalone file outputs. Max 21600. |
| `baseUrl` | string | Viewer URL origin override. Overrides plugin `viewerBaseUrl`. Must be `http` or `https`, no query/hash. |

**Legacy input aliases** (still accepted for backward compatibility): `format` -> `fileFormat`; `imageFormat` -> `fileFormat`; `imageQuality` -> `fileQuality`; `imageScale` -> `fileScale`; `imageMaxWidth` -> `fileMaxWidth`.

**Validation and limits**: `before` and `after` each max 512 KiB; `patch` max 2 MiB; `path` max 2048 bytes; `lang` max 128 bytes; `title` max 1024 bytes. Patch complexity cap: max 128 files and 120000 total lines. `patch` and `before` or `after` together are rejected. Rendered file safety limits (apply to PNG and PDF): `fileQuality: "standard"` max 8 MP (8,000,000 rendered pixels); `fileQuality: "hq"` max 14 MP (14,000,000 rendered pixels); `fileQuality: "print"` max 24 MP (24,000,000 rendered pixels); PDF also has a max of 50 pages.

## Syntax Highlighting

OpenClaw includes syntax highlighting for common source, config, and documentation languages: `javascript`, `typescript`, `tsx`, `jsx`, `json`, `markdown`, `yaml`, `css`, `html`, `sh`, `python`, `go`, `rust`, `java`, `c`, `cpp`, `csharp`, `php`, `sql`, `docker`, `ruby`, `swift`, `kotlin`, `r`, `dart`, `lua`, `powershell`, `xml`, and `toml`. Common aliases such as `js`, `ts`, `bash`, `md`, `yml`, `c++`, `dockerfile`, `rb`, `kt`, and `ps1` are normalized to those default languages.

Install the Diff Viewer Language Pack plugin to highlight other languages with `openclaw plugins install clawhub:@openclaw/diffs-language-pack`. With the language pack available, OpenClaw can highlight many more languages. If the pack is not installed, files outside the default list still render as readable plain text. Examples include Astro, Vue, Svelte, MDX, GraphQL, Terraform/HCL, Nix, Clojure, Elixir, Haskell, OCaml, Scala, Zig, Solidity, Verilog/VHDL, Fortran, MATLAB, LaTeX, Mermaid, Sass/Less/SCSS, Nginx, Apache, CSV, dotenv, INI, and diff files.

## Plugin Defaults

Set plugin-wide defaults in `~/.openclaw/openclaw.json` under `plugins.entries.diffs.config.defaults`. Supported default keys: `fontFamily`, `fontSize`, `lineSpacing`, `layout`, `showLineNumbers`, `diffIndicators`, `wordWrap`, `background`, `theme`, `fileFormat`, `fileQuality`, `fileScale`, `fileMaxWidth`, `mode`, and `ttlSeconds`. Explicit tool parameters override these defaults.

```json5
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
        config: {
          defaults: {
            fontFamily: "Fira Code",
            fontSize: 15,
            lineSpacing: 1.6,
            layout: "unified",
            showLineNumbers: true,
            diffIndicators: "bars",
            wordWrap: true,
            background: true,
            theme: "dark",
            fileFormat: "png",
            fileQuality: "standard",
            fileScale: 2,
            fileMaxWidth: 960,
            mode: "both",
            ttlSeconds: 21600,
          },
        },
      },
    },
  },
}
```

### Persistent Viewer URL Config

`viewerBaseUrl` (string) is the plugin-owned fallback for returned viewer links when a tool call does not pass `baseUrl`. It must be `http` or `https`, with no query/hash. Set it under `plugins.entries.diffs.config.viewerBaseUrl`:

```json5
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
        config: {
          viewerBaseUrl: "https://gateway.example.com/openclaw",
        },
      },
    },
  },
}
```

The full URL-construction precedence (per-call `baseUrl` → plugin `viewerBaseUrl` → loopback `127.0.0.1` → custom bind host) and the viewer route/network behavior are documented in **[oc_tools_diffs_viewer_security](oc_tools_diffs_viewer_security.md)**.

**Source**: OpenClaw documentation — `tools/diffs` (mirror `inbox/openclaw_docs/tools/diffs.md`)
**Last Updated**: 2026-06-22
**Status**: Active
