---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - memory_wiki
keywords:
  - openclaw wiki cli
  - memory-wiki vault
  - wiki compile lint search
  - wiki okf import
  - wiki bridge import
  - wiki apply synthesis
  - wiki obsidian helpers
  - vaultmode search backend corpus
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/wiki
access_control_group: ["general"]
---

# OpenClaw — `openclaw wiki` CLI (memory-wiki vault)

## Overview

This note documents the `openclaw wiki` command family — the operator-facing CLI for inspecting and maintaining the `memory-wiki` vault, provided by the bundled `memory-wiki` plugin. It mirrors the `cli/wiki` source page: what the CLI is for, the common-command quick reference, each subcommand (`status`, `doctor`, `init`, `ingest`, `okf import`, `compile`, `lint`, `search`, `get`, `apply`, `bridge import`, `unsafe-local import`, and the `obsidian` helpers), the practical usage guidance, and the `memory-wiki` config keys that shape behavior. The vault itself — a compiled knowledge store with wiki-native search, provenance-rich syntheses, contradiction and freshness reports, and optional Obsidian helpers — is the procedure's subject; the full plugin config model lives in the Memory Wiki plugin page (link-out).

## What it is for

Use `openclaw wiki` when you want a compiled knowledge vault with: wiki-native search and page reads; provenance-rich syntheses; contradiction and freshness reports; bridge imports from the active memory plugin; and optional Obsidian CLI helpers.

## Common commands

The quick reference covers the full lifecycle — inspect, init, import, compile, lint, search/read, apply mutations, bridge import, and Obsidian helpers:

```bash
openclaw wiki status
openclaw wiki doctor
openclaw wiki init
openclaw wiki ingest ./notes/alpha.md
openclaw wiki okf import ./knowledge-catalog/okf/bundles/ga4
openclaw wiki compile
openclaw wiki lint
openclaw wiki search "alpha"
openclaw wiki search "who should I ask about Teams?" --mode route-question
openclaw wiki get entity.alpha --from 1 --lines 80

openclaw wiki apply synthesis "Alpha Summary" \
  --body "Short synthesis body" \
  --source-id source.alpha

openclaw wiki apply metadata entity.alpha \
  --source-id source.alpha \
  --status review \
  --question "Still active?"

openclaw wiki bridge import
openclaw wiki unsafe-local import

openclaw wiki obsidian status
openclaw wiki obsidian search "alpha"
openclaw wiki obsidian open syntheses/alpha-summary.md
openclaw wiki obsidian command workspace:quick-switcher
openclaw wiki obsidian daily
```

## Commands

### `wiki status`

Inspect current vault mode, health, and Obsidian CLI availability. Use this first when you are unsure whether the vault is initialized, bridge mode is healthy, or Obsidian integration is available. When bridge mode is active and configured to read memory artifacts, this command queries the running Gateway so it sees the same active memory plugin context as agent/runtime memory.

### `wiki doctor`

Run wiki health checks and surface configuration or vault problems. When bridge mode is active and configured to read memory artifacts, this command queries the running Gateway before building the report; disabled bridge imports and bridge configs that do not read memory artifacts remain local/offline. Typical issues include: bridge mode enabled without public memory artifacts; invalid or missing vault layout; and missing external Obsidian CLI when Obsidian mode is expected.

### `wiki init`

Create the wiki vault layout and starter pages. This initializes the root structure, including top-level indexes and cache directories.

### `wiki ingest <path-or-url>`

Import content into the wiki source layer. Notes: URL ingest is controlled by `ingest.allowUrlIngest`; imported source pages keep provenance in frontmatter; and auto-compile can run after ingest when enabled.

### `wiki okf import <path>`

Import an unpacked Open Knowledge Format (OKF) bundle into wiki concept pages. The importer reads every non-reserved `.md` concept document in the OKF directory tree, requires a non-empty `type` field, and treats unknown OKF `type` values as generic concepts. Reserved OKF `index.md` and `log.md` files are not imported as concepts. Imported pages are flattened under `concepts/` so existing wiki compile, search, get, digest, and dashboard flows see them immediately. The original OKF concept ID, `type`, `resource`, `tags`, timestamp, source path, and full frontmatter are preserved in the page frontmatter. Internal OKF markdown links are rewritten to the generated wiki pages; broken or external links are left unchanged.

```bash
openclaw wiki okf import ./bundles/ga4
openclaw wiki okf import ./bundles/ga4 --json
openclaw wiki search "BigQuery Table" --mode source-evidence --json
openclaw wiki get <path-from-json-result>
```

### `wiki compile`

Rebuild indexes, related blocks, dashboards, and compiled digests. This writes stable machine-facing artifacts under `.openclaw-wiki/cache/agent-digest.json` and `.openclaw-wiki/cache/claims.jsonl`. If `render.createDashboards` is enabled, compile also refreshes report pages.

### `wiki lint`

Lint the vault and report: structural issues; provenance gaps; contradictions; open questions; low-confidence pages/claims; and stale pages/claims. Run this after meaningful wiki updates.

### `wiki search <query>`

Search wiki content. Behavior depends on config: `search.backend` is `shared` or `local`; `search.corpus` is `wiki`, `memory`, or `all`; and `--mode` is `auto`, `find-person`, `route-question`, `source-evidence`, or `raw-claim`. Use `wiki search` when you want wiki-specific ranking or provenance details; for one broad shared recall pass, prefer `openclaw memory search` when the active memory plugin exposes shared search. Search modes help the agent choose the right surface: `find-person` (aliases, handles, socials, canonical IDs, and person pages); `route-question` (ask-for/best-used-for hints and relationship context); `source-evidence` (source pages and structured evidence fields); and `raw-claim` (structured claim text with claim/evidence metadata).

```bash
openclaw wiki search "bgroux" --mode find-person
openclaw wiki search "who knows Teams rollout?" --mode route-question
openclaw wiki search "maintainer-whois" --mode source-evidence
openclaw wiki search "strong route Teams" --mode raw-claim --json
```

Text output includes `Claim:` and `Evidence:` lines when a result matches a structured claim. JSON output additionally exposes `matchedClaimId`, `matchedClaimStatus`, `matchedClaimConfidence`, `evidenceKinds`, and `evidenceSourceIds` for agent-side drilldown.

### `wiki get <lookup>`

Read a wiki page by id or relative path.

```bash
openclaw wiki get entity.alpha
openclaw wiki get syntheses/alpha-summary.md --from 1 --lines 80
```

### `wiki apply`

Apply narrow mutations without freeform page surgery. Supported flows include: create/update a synthesis page; update page metadata; attach source ids; add questions; add contradictions; update confidence/status; and write structured claims. This command exists so the wiki can evolve safely without manually editing managed blocks.

### `wiki bridge import`

Import public memory artifacts from the active memory plugin into bridge-backed source pages. Use this in `bridge` mode when you want the latest exported memory artifacts pulled into the wiki vault. For active bridge artifact reads, the CLI routes the import through Gateway RPC so the import uses the runtime memory plugin context. If bridge imports are disabled or artifact reads are turned off, the command keeps the local/offline zero-import behavior.

### `wiki unsafe-local import`

Import from explicitly configured local paths in `unsafe-local` mode. This is intentionally experimental and same-machine only.

### `wiki obsidian ...`

Obsidian helper commands for vaults running in Obsidian-friendly mode. Subcommands are `status`, `search`, `open`, `command`, and `daily`. These require the official `obsidian` CLI on `PATH` when `obsidian.useOfficialCli` is enabled.

## Practical usage guidance

Source-recommended workflows for choosing the right subcommand: use `wiki search` + `wiki get` when provenance and page identity matter; use `wiki apply` instead of hand-editing managed generated sections; use `wiki lint` before trusting contradictory or low-confidence content; use `wiki compile` after bulk imports or source changes when you want fresh dashboards and compiled digests immediately; use `wiki okf import` when a data catalog, documentation export, or agent enrichment pipeline already emits OKF markdown bundles; and use `wiki bridge import` when bridge mode depends on newly exported memory artifacts.

## Configuration tie-ins

`openclaw wiki` behavior is shaped by these `memory-wiki` plugin config keys: `plugins.entries.memory-wiki.config.vaultMode`; `plugins.entries.memory-wiki.config.search.backend`; `plugins.entries.memory-wiki.config.search.corpus`; `plugins.entries.memory-wiki.config.bridge.*`; `plugins.entries.memory-wiki.config.obsidian.*`; `plugins.entries.memory-wiki.config.render.*`; and `plugins.entries.memory-wiki.config.context.includeCompiledDigestPrompt`. See the Memory Wiki plugin page for the full config model.

**Source**: OpenClaw documentation — `cli/wiki` (mirror `inbox/openclaw_docs/cli/wiki.md`)
**Last Updated**: 2026-06-22
**Status**: Active
