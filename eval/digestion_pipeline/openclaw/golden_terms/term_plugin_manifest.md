---
tags:
  - resource
  - terminology
  - openclaw
  - plugin-manifest
  - plugin-system
  - package-json
  - semver
  - compat-api
  - host-loader-gate
  - agent-framework
keywords:
  - Plugin Manifest
  - openclaw.compat.pluginApi
  - openclaw.build.openclawVersion
  - openclaw.build.pluginSdkVersion
  - openclaw.install.minHostVersion
  - EXTERNAL_CODE_PLUGIN_REQUIRED_FIELD_PATHS
  - readOpenClawBlock
  - normalizeExternalPluginCompatibility
  - listMissingExternalCodePluginFieldPaths
  - validateExternalCodePluginPackageJson
  - ExternalPluginCompatibility
  - ExternalCodePluginValidationResult
  - plugin-package-contract
  - package.json openclaw block
  - host compatibility gate
topics:
  - OpenClaw plugin authoring
  - Plugin package contract
  - Host loader compatibility gate
  - package.json manifest extensions
  - Semver host-version gating
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://github.com/openclaw/openclaw/tree/main/packages/plugin-package-contract
access_control_group: ["general"]
---

# Plugin Manifest

## Definition

A **Plugin Manifest** is the on-disk declaration — carried inside an OpenClaw extension's `package.json` under a vendor-namespaced `openclaw` block — that tells the OpenClaw host **what host API version the plugin was built against** (`openclaw.compat.pluginApi`, a [semver](https://semver.org/) range expression), **what OpenClaw release it was built with** (`openclaw.build.openclawVersion`), and **what minimum host environment it needs** (`openclaw.install.minHostVersion`). The host loader reads this block BEFORE activating the plugin, runs a `semver.satisfies(hostVersion, pluginApiRange)` predicate, and refuses to load the plugin if the gate fails — so an incompatible extension surfaces as a clean publish-time rejection or load-time skip rather than a runtime crash after the plugin has begun mutating state.

This is the same pattern as [VS Code's `engines.vscode`](https://code.visualstudio.com/api/references/extension-manifest) field (where extensions declare `"engines": { "vscode": "^1.85.0" }` and the marketplace refuses to install on older VS Code builds), [Obsidian's `minAppVersion`](https://docs.obsidian.md/Reference/Manifest) in its `manifest.json` (which Obsidian compares against the running app version at plugin enable time), and [npm `peerDependencies`](https://nodejs.org/en/blog/npm/peer-dependencies) (which let a plugin module declare "I only work when plugged into version x.y.z of a particular host package"). OpenClaw's twist is that the manifest lives in a vendor-namespaced sub-object (`openclaw.*`) rather than at the package root — so the same `package.json` can carry VS Code's `engines`, npm's `peerDependencies`, AND `openclaw.compat.pluginApi` without collision, and OpenClaw's contract is to ignore everything outside its namespace.

## Context

The Plugin Manifest is OpenClaw's **publish-time and load-time compatibility gate** — the file every external code plugin published to ClawHub (the OpenClaw plugin registry) MUST populate before the registry will accept it, and the file the host loader MUST consult before activating a plugin in a running session. It is the *code-side* loading contract; its companion the [Skill Manifest](term_skill_manifest.md) is the *prompt-side* authoring contract for bundled skills. The two are independent — a plugin can ship code-only (Plugin Manifest required, no `SKILL.md`), prompt-only (`SKILL.md` required, no `openclaw` block), or both.

The validation surface lives in `packages/plugin-package-contract/src/index.ts` — a 100-LOC TypeScript file exporting `validateExternalCodePluginPackageJson(parsed: unknown) -> { compatibility?, issues[] }`, plus the `EXTERNAL_CODE_PLUGIN_REQUIRED_FIELD_PATHS` frozen tuple that downstream tooling (ClawHub publisher, host loader, IDE plugins) all import to stay in lock-step on what counts as a required field. The whole file uses defensive type-guards (`isRecord` with explicit array exclusion) and a single `normalizeOptionalString` (trim-then-empty-is-undefined) so type-mismatch, missing-key, AND whitespace-only values all collapse to the SAME "absent" signal — making the missing-list accumulator and the normalized-compatibility record produce coherent results end-to-end. Authors publishing plugins to ClawHub use the validation function indirectly through the publisher CLI; host operators use it directly through the loader. The runtime activation manifest (per-plugin `openclaw.plugin.json` carrying tool/skill/contributesPoint declarations) is a SEPARATE file — Plugin Manifest is the publish-time gate, `openclaw.plugin.json` is the runtime activation surface.

## Key Characteristics

- **`openclaw.compat.pluginApi` semver range — REQUIRED** — a semver expression (e.g. `"^1.0.0"`, `">=2.3.0 <3.0.0"`) declaring the range of OpenClaw plugin-API versions the plugin will work against. The host's runtime API version is matched against this range via standard `semver.satisfies(host, range)`. This is one of TWO entries in `EXTERNAL_CODE_PLUGIN_REQUIRED_FIELD_PATHS`; absence (or whitespace-only) emits a typed `ExternalPluginValidationIssue { fieldPath: "openclaw.compat.pluginApi", message: "openclaw.compat.pluginApi is required for external code plugins published to ClawHub." }`. Directly analogous to VS Code's `engines.vscode` and Obsidian's `minAppVersion`.
- **`openclaw.build.openclawVersion` build provenance — REQUIRED** — the OpenClaw release the plugin was BUILT against (vs `compat.pluginApi` which is the range it CLAIMS COMPATIBILITY with). Used for telemetry, bug-reproduction (which OpenClaw version's headers did this plugin compile against), and conservative inference when authors over-claim their compatibility range. The second entry in the required-paths tuple; falls back to the package's own `version` field in the normalized compatibility record (so telemetry is always populated even when the publisher rejects the manifest).
- **`openclaw.build.pluginSdkVersion` SDK provenance — OPTIONAL** — the version of `@openclaw/plugin-sdk` (the authoring library) the plugin was built with. Carried in the normalized record for telemetry and SDK-version-cohort analysis, not gated on. Authors using a `^` range against the SDK get the same lenient-host pattern [npm peer-dependency conventions](https://nodejs.org/en/blog/npm/peer-dependencies) recommend.
- **`openclaw.install.minHostVersion` host floor — OPTIONAL with fallback to `compat.minGatewayVersion`** — the minimum OpenClaw HOST process version (not API version) the plugin's install recipe needs. Cross-block fallback rule baked into `normalizeExternalPluginCompatibility`: `compat.minGatewayVersion ?? install.minHostVersion`. The `??` (NOT `||`) is load-bearing because `normalizeOptionalString` returns `undefined` (not `""`) for whitespace-only, so the fallback triggers on absence only — not on empty-string surprises.
- **Vendor namespace under `package.json#openclaw`** — the entire manifest lives under one root key, leaving `package.json` siblings (`name`, `version`, `dependencies`, `peerDependencies`, `scripts`) untouched. This is why a plugin's `package.json` can simultaneously declare an npm dependency tree, VS Code `engines`, AND `openclaw.compat.pluginApi` without collision — each tool only reads its own namespace. Same convention `package.json` already uses for `eslintConfig`, `babel`, `husky`, etc.
- **`readOpenClawBlock` cascade returns flat destructurable** — single helper narrows the parsed `package.json` from `unknown` to `Record<string, unknown>` via `isRecord` four times (root → `openclaw` → `compat` / `build` / `install`) and returns `{ root, openclaw, compat, build, install }` as a flat object. Every reader becomes a one-line `const { compat, build } = readOpenClawBlock(pkg)` followed by direct `compat?.field` access. The flat shape (NOT nested) is what lets `normalizeExternalPluginCompatibility` and `listMissingExternalCodePluginFieldPaths` share the same destructuring pattern.
- **Type-guard chain — `isRecord` with explicit array exclusion** — the single guard the whole file uses to narrow `unknown` to `Record<string, unknown>` before any property access; the `!Array.isArray(value)` clause is mandatory because `typeof [] === "object"` and arrays are non-null — without explicit exclusion, a buggy publish that accidentally serialized an array at a record position would silently bypass every validation gate. The `value is Record<string, unknown>` predicate annotation is what gives downstream optional-chaining (`root?.openclaw`) its narrowed type.
- **Required-field accumulator — `listMissingExternalCodePluginFieldPaths`** — reads the same `openclaw` block via `readOpenClawBlock`, runs each required path through the SAME `normalizeOptionalString` used by `normalizeExternalPluginCompatibility`, pushes the dotted-path string (`"openclaw.compat.pluginApi"`) into a `string[]` when the normalized value is absent. Using the same normalizer for absence-checking and value-extraction is what guarantees "missing" and "normalized-as-absent" stay coherent — otherwise a whitespace-only `"   "` value could pass the missing-check but disappear from the compatibility record, producing `issues = []` + `compatibility.pluginApiRange = undefined` simultaneously.
- **Frozen required-paths tuple — `EXTERNAL_CODE_PLUGIN_REQUIRED_FIELD_PATHS`** — `readonly` const-asserted array (`as const`) so its element types are literal-typed (`"openclaw.compat.pluginApi" | "openclaw.build.openclawVersion"`) and downstream `switch (fieldPath)` consumers get exhaustiveness checking at compile time. Exported so ClawHub lint rules, IDE plugins, and error-message tables can import the same constant rather than re-declare it.
- **Two-field independent result envelope — `{ compatibility?, issues[] }`** — `validateExternalCodePluginPackageJson` returns a normalized compatibility record AND an issues list; the two are INDEPENDENT. A plugin with `openclaw.build.pluginSdkVersion` set but `openclaw.compat.pluginApi` missing produces `compatibility = { pluginSdkVersion: "..." }` AND `issues = [{ fieldPath: "openclaw.compat.pluginApi", ... }]`. Callers branch on `issues.length > 0` for the publish gate AND can read `compatibility` for telemetry — orthogonal signals, never collapsed.
- **Empty-record-as-undefined collapse** — when EVERY field in the normalized compatibility record would be absent (no `openclaw` block at all), `normalizeExternalPluginCompatibility` returns `undefined` rather than `{}`. The `Object.keys(rec).length > 0 ? rec : undefined` collapse at the end is what makes callsite branching (`if (result.compatibility)`) clean. Without it, every plugin without an `openclaw` block would still produce `compatibility: {}`, forcing callers to do `Object.keys(...).length > 0` everywhere.

## Related Terms

- **[OpenClaw — Packaging a Plugin (package.json, Manifest, ClawHub Publish, Setup Entry)](../documentation/openclaw/oc_plugins_sdk_setup_packaging.md)** — This note is the packaging procedure for an OpenClaw plugin, covering the four packaging concerns of the `plugins/sdk-setup` source page that precede…
- **[OpenClaw — ClawHub CLI: Package (Plugin) Workflows](../documentation/openclaw/oc_clawhub_cli_packages.md)** — This note is the package/plugin half of the `clawhub` CLI reference — the procedures for browsing, inspecting, downloading, verifying, validating, publishing…

## Related Code Snippets

- [OpenClaw Extensions — plugin-package-contract/index.ts — `openclaw.compat.pluginApi` Semver + Validation Surface](../code_snippets/snippet_openclaw_plugin_package_contract.md): full 100-LOC source covering all six patterns — `isRecord` defensive guard, `normalizeOptionalString` trim-empty-to-undefined coercion, `readOpenClawBlock` cascade, `normalizeExternalPluginCompatibility` cross-block-fallback assembler, `listMissingExternalCodePluginFieldPaths` accumulator, and `validateExternalCodePluginPackageJson` orchestration

## References

- [OpenClaw `packages/plugin-package-contract/`](https://github.com/openclaw/openclaw/tree/main/packages/plugin-package-contract) — the package directory carrying the validation surface (Class 2: project source)
- [OpenClaw `plugin-package-contract/src/index.ts`](https://github.com/openclaw/openclaw/blob/main/packages/plugin-package-contract/src/index.ts) — full source file for the 100-LOC validation surface (Class 2: project source)
- [Semantic Versioning 2.0.0 specification](https://semver.org/) — the authoritative semver spec defining MAJOR.MINOR.PATCH and the range expressions `openclaw.compat.pluginApi` uses (Class 1: authoritative spec)
- [VS Code — Extension Manifest reference](https://code.visualstudio.com/api/references/extension-manifest) — Microsoft's `engines.vscode` contract that OpenClaw's `openclaw.compat.pluginApi` directly parallels (Class 2: framework docs)
- [Obsidian — Manifest reference (`manifest.json` with `minAppVersion`)](https://docs.obsidian.md/Reference/Manifest) — Obsidian's plugin-manifest with `minAppVersion` compared against the running app at enable time (Class 2: framework docs)
- [npm — `package.json` reference](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/) — authoritative npm spec for `package.json` fields including `peerDependencies` and `engines`, the baseline OpenClaw extends via its vendor-namespaced sub-object (Class 2: framework docs)
- [Node.js — Peer Dependencies (npm blog)](https://nodejs.org/en/blog/npm/peer-dependencies) — the foundational article on plugin-host version compatibility via peer-dependencies; OpenClaw's `openclaw.compat.pluginApi` is the same plugin-host gate at a different layer (Class 2: framework docs)
