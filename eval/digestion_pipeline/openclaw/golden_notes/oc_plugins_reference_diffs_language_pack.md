---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - diffs
keywords:
  - openclaw diffs-language-pack plugin
  - diffs language pack
  - shiki syntax highlighting
  - "@openclaw/diffs-language-pack"
  - clawhub diffs language pack
  - diff viewer language support
  - plain-text fallback
  - added languages shiki
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/diffs-language-pack
access_control_group: ["general"]
---

# OpenClaw — Diffs Language Pack Plugin (`@openclaw/diffs-language-pack`)

## Overview

This note describes the OpenClaw **Diffs Language Pack** plugin, the `plugins/reference/diffs-language-pack` reference card. The plugin adds syntax highlighting for languages outside the default `diffs` viewer set, broadening the Shiki-supported languages the diff viewer can render. It is an optional companion to the base `@openclaw/diffs` plugin: when this pack is not installed, files in the extra languages still render as readable plain text. This note mirrors the source page's summary, `## Distribution`, `## Surface`, and `## Added languages` sections, copying the package name, install route, and the Shiki language examples verbatim.

## Distribution

The plugin is distributed as the npm package `@openclaw/diffs-language-pack`. Per the source page, its install routes are: npm, and ClawHub via the identifier `clawhub:@openclaw/diffs-language-pack`.

## Surface

The source page declares this plugin's surface as `plugin` — that is, the package registers as an OpenClaw plugin (an extension to the base diffs viewer's rendering capability) rather than declaring a distinct `tools`, `channels`, or contract surface of its own. The base `@openclaw/diffs` plugin is what provides the read-only diff-viewer `tools` contract and `skills`; this language pack extends the file types that viewer can syntax-highlight.

## Added Languages

The base `diffs` plugin already highlights the common languages documented in the Diffs tool doc (`/tools/diffs`). Install this language pack when you want syntax highlighting for a broader set of Shiki-supported languages. If the pack is not installed, those files still render as readable plain text — the absence of the pack is a graceful degradation, not a failure.

The source page lists these examples of the added languages: Astro, Vue, Svelte, MDX, GraphQL, Terraform/HCL, Nix, Clojure, Elixir, Haskell, OCaml, Scala, Zig, Solidity, Verilog/VHDL, Fortran, MATLAB, LaTeX, Mermaid, Sass/Less/SCSS, Nginx, Apache, CSV, dotenv, INI, and diff files. This is an illustrative ("Examples include …") list, not the exhaustive set; the upstream Shiki language and alias catalog is the authoritative source for the full supported list (linked under References).

**Source**: OpenClaw documentation — `plugins/reference/diffs-language-pack` (mirror `inbox/openclaw_docs/plugins/reference/diffs-language-pack.md`)
**Last Updated**: 2026-06-22
**Status**: Active
