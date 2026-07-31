---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - memory
keywords:
  - openclaw memory-wiki plugin
  - compiled knowledge vault
  - structured claims and evidence
  - vault modes isolated bridge unsafe-local
  - wiki_search wiki_get wiki_apply
  - bridge mode memory artifacts
  - okf open knowledge format import
  - qmd hybrid memory pattern
topics:
  - OpenClaw
  - Memory Wiki Plugin
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/memory-wiki
access_control_group: ["general"]
---

# OpenClaw — The memory-wiki Compiled Knowledge Vault Plugin

## Overview

This note models the OpenClaw `memory-wiki` plugin, a bundled plugin that turns durable memory into a compiled knowledge vault: a navigable wiki of deterministic pages with structured claims, page-level provenance, dashboards, and machine-readable digests. It does **not** replace the active memory plugin — the active memory plugin (`memory-core`, QMD, Honcho, etc.) still owns recall, promotion, indexing, and dreaming, while `memory-wiki` sits beside it and compiles durable knowledge into a maintained knowledge layer that behaves "less like a pile of Markdown files." This note covers what the plugin adds, how it fits beside active memory, the recommended QMD-hybrid pattern, the three vault modes, vault layout, Open Knowledge Format (OKF) imports, structured claims/evidence, agent-facing entity metadata, the compile pipeline, dashboards, search/retrieval, the agent tools, prompt/context behavior, configuration, the `openclaw wiki` CLI, Obsidian support, and the recommended workflow — mirroring the `plugins/memory-wiki` source page.

## What It Adds and How It Fits With Memory

`memory-wiki` adds, on top of plain `MEMORY.md` notes: a dedicated wiki vault with deterministic page layout; structured claim and evidence metadata (not just prose); page-level provenance, confidence, contradictions, and open questions; compiled digests for agent/runtime consumers; wiki-native search/get/apply/lint tools; Open Knowledge Format imports into compiled wiki concepts; an optional bridge mode that imports public artifacts from the active memory plugin; and an optional Obsidian-friendly render mode with CLI integration.

The layering split is explicit. The **active memory plugin** (`memory-core`, QMD, Honcho, etc.) owns recall, semantic search, promotion, dreaming, and the memory runtime. `memory-wiki` owns compiled wiki pages, provenance-rich syntheses, dashboards, and wiki-specific search/get/apply. If the active memory plugin exposes shared recall artifacts, OpenClaw can search both layers in one pass with `memory_search corpus=all`; when you need wiki-specific ranking, provenance, or direct page access, you use the wiki-native tools instead.

## Recommended Hybrid Pattern

A strong default for local-first setups pairs **QMD as the active memory backend** (recall and broad semantic search) with **`memory-wiki` in `bridge` mode** for durable synthesized knowledge pages. Each layer stays focused: QMD keeps raw notes, session exports, and extra collections searchable, while `memory-wiki` compiles stable entities, claims, dashboards, and source pages. The practical rule is: use `memory_search` for one broad recall pass across memory; use `wiki_search` and `wiki_get` for provenance-aware wiki results; and use `memory_search corpus=all` when you want shared search to span both layers.

If bridge mode reports zero exported artifacts, the active memory plugin is not yet exposing public bridge inputs — run `openclaw wiki doctor` first, then confirm the active memory plugin supports public artifacts. When bridge mode is active and `bridge.readMemoryArtifacts` is enabled, `openclaw wiki status`, `openclaw wiki doctor`, and `openclaw wiki bridge import` read through the running Gateway, which keeps CLI bridge checks aligned with the runtime memory plugin context; if bridge is disabled or artifact reads are turned off, those commands keep their local/offline behavior.

## Vault Modes

`memory-wiki` supports three vault modes:

- **`isolated`** — own vault, own sources, no dependency on `memory-core`. Use it when you want the wiki to be its own curated knowledge store.
- **`bridge`** — reads public memory artifacts and memory events from the active memory plugin through public plugin SDK seams. Use it to compile and organize the memory plugin's exported artifacts without reaching into private plugin internals. Bridge mode can index: exported memory artifacts, dream reports, daily notes, memory root files, and memory event logs.
- **`unsafe-local`** — an explicit same-machine escape hatch for local private paths. It is intentionally experimental and non-portable; use it only when you understand the trust boundary and specifically need local filesystem access that bridge mode cannot provide.

## Vault Layout

The plugin initializes a vault with this structure (managed content stays inside generated blocks; human note blocks are preserved):

```text
<vault>/
  AGENTS.md
  WIKI.md
  index.md
  inbox.md
  entities/
  concepts/
  syntheses/
  sources/
  reports/
  _attachments/
  _views/
  .openclaw-wiki/
```

The main page groups are: `sources/` for imported raw material and bridge-backed pages; `entities/` for durable things, people, systems, projects, and objects; `concepts/` for ideas, abstractions, patterns, and policies; `syntheses/` for compiled summaries and maintained rollups; and `reports/` for generated dashboards.

## Open Knowledge Format Imports

`memory-wiki` can import unpacked Open Knowledge Format bundles with `openclaw wiki okf import ./bundles/ga4`. This is the cleanest fit when a data catalog, documentation crawler, or enrichment agent already produces OKF: keep OKF as the portable exchange artifact, then let `memory-wiki` turn it into OpenClaw-native concept pages and compiled digests. The importer follows the OKF v0.1 shape: non-reserved `.md` files are concept documents; each imported concept needs a non-empty `type` frontmatter field; unknown OKF `type` values are accepted; reserved `index.md` and `log.md` files are not imported as concepts; and broken or external markdown links are preserved.

Imported concept pages are flattened under `concepts/` so the existing compile, search, get, dashboard, and prompt-digest paths see them without adding a second wiki tree. Each page keeps the original OKF concept ID, source path, `type`, `resource`, `tags`, timestamp, and full producer frontmatter. Internal OKF links are rewritten to the generated wiki concept pages and also emitted as structured `relationships` entries with `kind: okf-link`.

## Structured Claims and Evidence

Pages can carry structured `claims` frontmatter, not just freeform text. Each claim can include `id`, `text`, `status`, `confidence`, `evidence[]`, and `updatedAt`. Each evidence entry can include `kind`, `sourceId`, `path`, `lines`, `weight`, `confidence`, `privacyTier`, `note`, and `updatedAt`. This is what makes the wiki act more like a belief layer than a passive note dump: claims can be tracked, scored, contested, and resolved back to sources.

## Agent-Facing Entity Metadata

Entity pages can also carry routing metadata for agent use. This is generic frontmatter, so it works for people, teams, systems, projects, or any other entity type. Common fields include `entityType` (for example `person`, `team`, `system`, or `project`); `canonicalId` (stable identity key used across aliases and imports); `aliases` (names, handles, or labels that resolve to the same page); `privacyTier` (`public`, `local-private`, `sensitive`, or `confirm-before-use`); `bestUsedFor` / `notEnoughFor` (compact routing hints); `lastRefreshedAt` (source-refresh timestamp separate from page edit time); `personCard` (an optional person-specific routing card with handles, socials, emails, timezone, lane, ask-for, avoid-asking-for, confidence, and privacy); and `relationships` (typed edges to related pages with target, kind, weight, confidence, evidence kind, privacy tier, and note). For a people wiki, the agent should usually start with `reports/person-agent-directory.md`, then open the person page with `wiki_get` before using contact details or inferred facts. An example entity page combines these blocks:

```yaml
pageType: entity
entityType: person
id: entity.brad-groux
canonicalId: maintainer.brad-groux
aliases:
  - Brad
  - bgroux
privacyTier: local-private
bestUsedFor:
  - Microsoft Teams and Azure routing
notEnoughFor:
  - legal approval
lastRefreshedAt: "2026-04-29T00:00:00.000Z"
personCard:
  handles:
    - "@bgroux"
  lane: Microsoft ecosystem
  confidence: 0.8
  privacyTier: confirm-before-use
relationships:
  - targetId: entity.alice
    kind: collaborates-with
    confidence: 0.7
    evidenceKind: discrawl-stat
claims:
  - id: claim.brad.teams
    text: Brad is useful for Microsoft Teams routing.
    status: supported
    confidence: 0.9
    evidence:
      - kind: maintainer-whois
        sourceId: source.maintainers
        privacyTier: local-private
```

## Compile Pipeline

The compile step reads wiki pages, normalizes summaries, and emits stable machine-facing artifacts under `.openclaw-wiki/cache/agent-digest.json` and `.openclaw-wiki/cache/claims.jsonl`. These digests exist so agents and runtime code do not have to scrape Markdown pages. Compiled output also powers first-pass wiki indexing for search/get flows, claim-id lookup back to owning pages, compact prompt supplements, and report/dashboard generation.

## Dashboards and Health Reports

When `render.createDashboards` is enabled, compile maintains dashboards under `reports/`. Built-in reports include `reports/open-questions.md`, `reports/contradictions.md`, `reports/low-confidence.md`, `reports/claim-health.md`, `reports/stale-pages.md`, `reports/person-agent-directory.md`, `reports/relationship-graph.md`, `reports/provenance-coverage.md`, and `reports/privacy-review.md`. These reports track things like contradiction note clusters, competing claim clusters, claims missing structured evidence, low-confidence pages and claims, stale or unknown freshness, pages with unresolved questions, person/entity routing cards, structured relationship edges, evidence class coverage, and non-public privacy tiers that need review before use.

## Search and Retrieval

`memory-wiki` supports two search backends — `shared` (use the shared memory search flow when available) and `local` (search the wiki locally) — and three corpora: `wiki`, `memory`, and `all`. Important behavior: `wiki_search` and `wiki_get` use compiled digests as a first pass when possible; claim ids can resolve back to the owning page; contested/stale/fresh claims influence ranking; provenance labels can survive into results; and search mode can bias ranking for person lookup, question routing, source evidence, or raw claims. The practical rule is to use `memory_search corpus=all` for one broad recall pass and `wiki_search` + `wiki_get` when you care about wiki-specific ranking, provenance, or page-level belief structure.

The search modes are: `auto` (balanced default); `find-person` (boost person-like entities, aliases, handles, socials, and canonical IDs); `route-question` (boost agent cards, ask-for hints, best-used-for hints, and relationship context); `source-evidence` (boost source pages and structured evidence metadata); and `raw-claim` (boost matching structured claims and return claim/evidence metadata in results). When a result matches a structured claim, `wiki_search` can return `matchedClaimId`, `matchedClaimStatus`, `matchedClaimConfidence`, `evidenceKinds`, and `evidenceSourceIds` in its details payload, and text output also includes compact `Claim:` and `Evidence:` lines when available.

## Agent Tools

The plugin registers five agent tools: `wiki_status` (current vault mode, health, Obsidian CLI availability); `wiki_search` (search wiki pages and, when configured, shared memory corpora — accepts a `mode` for person lookup, question routing, source evidence, or raw claim drilldown); `wiki_get` (read a wiki page by id/path or fall back to the shared memory corpus); `wiki_apply` (narrow synthesis/metadata mutations without freeform page surgery); and `wiki_lint` (structural checks, provenance gaps, contradictions, open questions). The plugin also registers a non-exclusive memory corpus supplement, so shared `memory_search` and `memory_get` can reach the wiki when the active memory plugin supports corpus selection.

## Prompt and Context Behavior

When `context.includeCompiledDigestPrompt` is enabled, memory prompt sections append a compact compiled snapshot from `agent-digest.json`. That snapshot is intentionally small and high-signal: top pages only, top claims only, contradiction count, question count, and confidence/freshness qualifiers. This is opt-in because it changes prompt shape and is mainly useful for context engines or legacy prompt assembly that explicitly consume memory supplements.

## Configuration

Config lives under `plugins.entries.memory-wiki.config`:

```json5
{
  plugins: {
    entries: {
      "memory-wiki": {
        enabled: true,
        config: {
          vaultMode: "isolated",
          vault: { path: "~/.openclaw/wiki/main", renderMode: "obsidian" },
          obsidian: { enabled: true, useOfficialCli: true, vaultName: "OpenClaw Wiki", openAfterWrites: false },
          bridge: { enabled: false, readMemoryArtifacts: true, indexDreamReports: true, indexDailyNotes: true, indexMemoryRoot: true, followMemoryEvents: true },
          ingest: { autoCompile: true, maxConcurrentJobs: 1, allowUrlIngest: true },
          search: { backend: "shared", corpus: "wiki" },
          context: { includeCompiledDigestPrompt: false },
          render: { preserveHumanBlocks: true, createBacklinks: true, createDashboards: true },
        },
      },
    },
  },
}
```

Key toggles: `vaultMode` (`isolated` / `bridge` / `unsafe-local`); `vault.renderMode` (`native` or `obsidian`); `bridge.readMemoryArtifacts` (import active memory plugin public artifacts); `bridge.followMemoryEvents` (include event logs in bridge mode); `search.backend` (`shared` or `local`); `search.corpus` (`wiki`, `memory`, or `all`); `context.includeCompiledDigestPrompt` (append compact digest snapshot to memory prompt sections); `render.createBacklinks` (generate deterministic related blocks); and `render.createDashboards` (generate dashboard pages). For the recommended **QMD + bridge** example, set `memory.backend: "qmd"`, then `vaultMode: "bridge"` with `bridge.enabled: true` and `search: { backend: "shared", corpus: "all" }` — keeping QMD in charge of active memory recall, `memory-wiki` focused on compiled pages and dashboards, and prompt shape unchanged until you intentionally enable compiled digest prompts.

## CLI

`memory-wiki` exposes a top-level `openclaw wiki` CLI surface (see the full command reference in the CLI: wiki docs):

```bash
openclaw wiki status
openclaw wiki doctor
openclaw wiki init
openclaw wiki ingest ./notes/alpha.md
openclaw wiki compile
openclaw wiki lint
openclaw wiki search "alpha"
openclaw wiki get entity.alpha
openclaw wiki apply synthesis "Alpha Summary" --body "..." --source-id source.alpha
openclaw wiki bridge import
openclaw wiki obsidian status
```

## Obsidian Support and Recommended Workflow

When `vault.renderMode` is `obsidian`, the plugin writes Obsidian-friendly Markdown and can optionally use the official `obsidian` CLI. Supported workflows include status probing, vault search, opening a page, invoking an Obsidian command, and jumping to the daily note. This is optional — the wiki still works in native mode without Obsidian. The recommended end-to-end workflow is: (1) keep your active memory plugin for recall/promotion/dreaming; (2) enable `memory-wiki`; (3) start with `isolated` mode unless you explicitly want bridge mode; (4) use `wiki_search` / `wiki_get` when provenance matters; (5) use `wiki_apply` for narrow syntheses or metadata updates; (6) run `wiki_lint` after meaningful changes; and (7) turn on dashboards if you want stale/contradiction visibility.

**Source**: OpenClaw documentation — `plugins/memory-wiki` (mirror `inbox/openclaw_docs/plugins/memory-wiki.md`)
**Last Updated**: 2026-06-22
**Status**: Active
