---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - compatibility
keywords:
  - openclaw plugin compatibility
  - compatibility registry
  - named compatibility adapter
  - plugin inspector package
  - deprecation policy
  - removal-pending removed status
  - maintainer acceptance lane
  - crabbox blacksmith testbox
topics:
  - OpenClaw
  - Plugin Compatibility
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/compatibility
access_control_group: ["general"]
---

# OpenClaw — Plugin Compatibility Registry, Inspector, and Deprecation Policy

## Overview

This note models the OpenClaw **plugin compatibility lifecycle**: how OpenClaw keeps older plugin contracts wired through *named compatibility adapters* before removing them, so existing bundled and external plugins keep working while the SDK, manifest, setup, config, and agent runtime contracts evolve. It mirrors the policy/lifecycle half of the `plugins/compatibility` source page — the **compatibility registry** record schema (and the separate doctor migration registry), the external **plugin inspector** package and its **maintainer acceptance lane**, the seven-step **deprecation policy** with its ≤3-month removal window, and the **release-notes** warning requirement. The concrete per-area schema shims (legacy SDK aliases, WhatsApp inbound callback flat aliases, WhatsApp inbound admission fields) are the subject of the sibling note **[oc_plugins_compatibility_areas](oc_plugins_compatibility_areas.md)** and are not re-detailed here.

## Compatibility registry

Plugin compatibility contracts are tracked in the core registry at `src/plugins/compat/registry.ts`. This registry is the source of truth for maintainer planning and for future plugin-inspector checks. Each record carries a fixed set of fields:

- a stable **compatibility code**
- **status**: `active`, `deprecated`, `removal-pending`, or `removed`
- **owner**: SDK, config, setup, channel, provider, plugin execution, agent runtime, or core
- **introduction and deprecation dates** when applicable
- **replacement guidance**
- **docs, diagnostics, and tests** that cover the old and new behavior

The governing rule is that if a plugin-facing behavior changes, the compatibility record must be added or updated *in the same change that adds the adapter* — the adapter and its registry record ship together.

A **separate registry** tracks doctor repair and migration compatibility at `src/commands/doctor/shared/deprecation-compat.ts`. Those records cover old config shapes, install-ledger layouts, and repair shims that may need to stay available even after the runtime compatibility path is removed. Because of this split, **release sweeps must check both registries**: a doctor migration must not be deleted just because the matching runtime or config compatibility record expired — first verify there is no supported upgrade path that still needs the repair. Release planning must also revalidate each replacement annotation, because plugin ownership and config footprint can change as providers and channels move out of core.

## Plugin inspector package

The plugin inspector is designed to live **outside the core OpenClaw repo** as a separate package/repository, backed by the versioned compatibility and manifest contracts. The day-one CLI invocation is:

```sh
openclaw-plugin-inspector ./my-plugin
```

The inspector emits five categories of output:

- manifest/schema validation
- the contract compatibility version being checked
- install/source metadata checks
- cold-path import checks
- deprecation and compatibility warnings

Pass `--json` for stable machine-readable output suitable for CI annotations. The division of responsibility is explicit: OpenClaw core *should expose contracts and fixtures* the inspector can consume, but *should not publish the inspector binary* from the main `openclaw` package.

### Maintainer acceptance lane

For validating the external inspector against real OpenClaw plugin packages, maintainers use the **Crabbox-backed Blacksmith Testbox** installable-package acceptance lane, run from a clean OpenClaw checkout *after* the package is built:

```sh
pnpm crabbox:run -- --provider blacksmith-testbox --timing-json --shell -- "pnpm install && pnpm build && npm exec --yes @openclaw/plugin-inspector@0.1.0 -- ./extensions/telegram --json"
pnpm crabbox:run -- --provider blacksmith-testbox --timing-json --shell -- "npm exec --yes @openclaw/plugin-inspector@0.1.0 -- ./extensions/discord --json"
pnpm crabbox:run -- --provider blacksmith-testbox --timing-json --shell -- "npm exec --yes @openclaw/plugin-inspector@0.1.0 -- <clawhub-plugin-dir> --json"
```

This lane is kept **opt-in for maintainers** because it installs an external npm package and may inspect plugin packages cloned outside the repo. The division of coverage is precise: the **local repo guards** cover the SDK export map, compatibility-registry metadata, deprecated SDK-import burn-down, and bundled-extension import boundaries; the **Testbox inspector proof** covers the package exactly as external plugin authors consume it.

## Deprecation policy

The core deprecation rule is that OpenClaw **should not remove a documented plugin contract in the same release that introduces its replacement**. Removal is staged through a fixed seven-step migration sequence:

1. Add the new contract.
2. Keep the old behavior wired through a named compatibility adapter.
3. Emit diagnostics or warnings when plugin authors can act.
4. Document the replacement and timeline.
5. Test both old and new paths.
6. Wait through the announced migration window.
7. Remove only with explicit breaking-release approval.

Every deprecated record must include a **warning start date, a replacement, a docs link, and a final removal date no more than three months after the warning starts**. A deprecated compatibility path must not be added with an open-ended removal window — unless maintainers explicitly decide it is permanent compatibility, in which case it is marked `active` instead of `deprecated`. New plugin code should prefer the replacement listed in the registry and the specific migration guide, while existing plugins may keep using a compatibility path until the docs, diagnostics, and release notes announce a removal window. The concrete records this policy governs — the current compatibility areas, including the WhatsApp inbound callback flat aliases and admission fields with their `2026-08-30` removal window — are detailed in **[oc_plugins_compatibility_areas](oc_plugins_compatibility_areas.md)**.

## Release notes

Release notes should include **upcoming plugin deprecations with target dates and links to migration docs**. That warning must happen *before* a compatibility path moves to the `removal-pending` or `removed` status — i.e., the release-notes announcement is a precondition for advancing a record's status toward removal, closing the loop between the registry's status field and the deprecation policy's announced migration window.

**Source**: OpenClaw documentation — `plugins/compatibility` (mirror `inbox/openclaw_docs/plugins/compatibility.md`)
**Last Updated**: 2026-06-22
**Status**: Active
