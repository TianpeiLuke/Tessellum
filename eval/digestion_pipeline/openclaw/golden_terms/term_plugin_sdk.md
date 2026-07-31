---
tags:
  - resource
  - terminology
  - openclaw
  - plugin-sdk
  - plugin-system
  - typescript-sdk
keywords:
  - Plugin SDK
  - definePluginEntry
  - defineSingleProviderPluginEntry
  - OpenClawPluginApi
  - openclaw.compat.pluginApi
  - plugin-package-contract
topics:
  - Plugin systems
  - SDK design
  - OpenClaw extensibility
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://github.com/openclaw/openclaw/tree/main/packages/plugin-sdk
access_control_group: ["general"]
---

# Plugin SDK

## Definition

A **Plugin SDK** is the authoring surface an extensible host application publishes to third-party developers: a typed, versioned package of factories, lifecycle hooks, and registration APIs that lets an out-of-tree module register new capabilities (providers, tools, commands, UI surfaces, services) without modifying or recompiling the host. The pattern is a specialization of the classic plugin / factory-method architecture catalogued by Martin Fowler — the host queries the plugin for known entry-point functions, and the plugin returns a normalized declarative record that the host loader consumes at activation time. VS Code's `vscode` extension API, Obsidian's `Plugin` base class, WordPress's `register_activation_hook`, Babel's preset factories, and Webpack's `apply(compiler)` hook are all instances of the same surface — a stable, typed boundary between the host runtime and the out-of-tree code that extends it.

In **OpenClaw**, the Plugin SDK is published as two cooperating packages: `packages/plugin-sdk/` (the authoring factories — `definePluginEntry` and the `defineSingleProviderPluginEntry` convenience wrapper, plus type re-exports for `OpenClawPluginApi`, `ProviderRuntimeModel`, and ~80 `Provider*Context` request/response types) and `packages/plugin-package-contract/` (the publish-time validation gate — `openclaw.compat.pluginApi` semver field, `openclaw.build.openclawVersion` declaration, and the `validateExternalCodePluginPackageJson` parser that turns an opaque `package.json` into a typed `{ compatibility, issues[] }` result). The split is deliberate: the authoring surface is the *what you write*, the package contract is the *what you ship* — host loaders can reject incompatible packages before activation without ever importing the plugin.

## Context

Plugin SDKs are the dominant extensibility pattern across modern developer tools and content apps: VS Code's `vscode` API (one of the largest documented extension APIs, with capability slots for commands, configurations, keybindings, views, and language servers); Obsidian's `Plugin` subclass with `onload`/`onunload` and registration helpers (`addCommand`, `addRibbonIcon`, `registerView`); WordPress's hook + filter API; Babel and Webpack's loader/plugin contracts. The agent-framework generation extends the same idea — Anthropic's "Skills + Plugins + MCP" layering, Microsoft's Semantic Kernel plugin API, and AWS Bedrock AgentCore's runtime all expose a typed authoring boundary above the raw protocol. Critically, **Plugin SDKs and MCP servers are not interchangeable**: an MCP server is a single-purpose tool-contract endpoint speaking JSON-RPC over a transport, whereas a Plugin SDK ships bundles that can include hooks, subagents, commands, configurations, *and* MCP connections. MCP servers stay clean and reusable across hosts; Plugin SDKs trade portability for deep host-UX integration.

OpenClaw's ~120 first-party extensions (channels for Slack/Discord/iMessage, providers for Anthropic/OpenAI/Mistral, sandbox backends, voice-call adapters, memory hosts) are all composed against this same SDK — every extension's `pluginEntry.ts` calls one of the two factories and `export default`s the result, and the runtime loads the module knowing nothing about which kind of extension it is. The two-package split (authoring SDK + package contract) means a plugin can be statically validated at publish time (ClawHub uses `validateExternalCodePluginPackageJson` as a gate) and then dynamically loaded with confidence at activation time.

## Key Characteristics

- **`definePluginEntry` factory** — the single canonical authoring entry point. Takes a declarative options bag (`id`, `name`, `description`, optional `kind`, optional `configSchema` as value-or-thunk, optional `reload` / `nodeHostCommands` / `securityAuditCollectors`, required `register(api: OpenClawPluginApi) => void` callback) and returns a normalized `DefinedPluginEntry` the runtime consumes. Conditional-spread guards (`...(x ? { x } : {})`) keep optional fields off the returned record so the runtime never sees `undefined` keys.
- **`defineSingleProviderPluginEntry` convenience wrapper** — collapses the 80% case (one API-key provider with a small text-model catalog) into a declarative `provider` field. Delegates to `definePluginEntry` under the hood, synthesizing the `register` callback that builds auth methods, wizard setup, and the catalog runner. Optional `register?(api)` escape hatch runs after auto-registration so plugins can add tools/commands alongside their provider.
- **`OpenClawPluginApi` type seam** — the registration callback receives an `OpenClawPluginApi` instance exposing `registerProvider`, `registerTool`, `registerCommand`, `registerService`, `registerModelCatalogProvider`. Every extension hook is method-on-API, never bare export — the runtime owns the registry, the plugin only declares intent. This mirrors VS Code's `vscode.commands.registerCommand(...)` and Obsidian's `this.addCommand(...)` patterns.
- **`openclaw.compat.pluginApi` semver gate** — the publish-time compatibility field in the plugin's `package.json`; the host loader runs `semver.satisfies(hostApiVersion, plugin.compat.pluginApiRange)` before activation. Companion fields `openclaw.build.openclawVersion` (required) and `openclaw.build.pluginSdkVersion` / `openclaw.install.minHostVersion` (optional) carry build provenance and minimum-host hints. Cross-block fallbacks normalize `build.openclawVersion ?? package.version` and `compat.minGatewayVersion ?? install.minHostVersion` so plugins with partial metadata still produce a usable compatibility record.
- **Per-plugin namespaced `PluginStateKeyedStore<T>`** — every plugin gets a typed SQLite-backed keyed store scoped to `(pluginId, namespace)` with 7 methods (`register`, `registerIfAbsent`, `lookup`, `consume`, `delete`, `entries`, `clear`). A process-wide `assertConsistentOptions` Map keyed by `${pluginId}\0${namespace}` prevents two openers from silently disagreeing on `maxEntries` or `defaultTtlMs`. The `core:` prefix is a runtime-enforced ownership boundary — third-party plugins cannot mint stores in the reserved core namespace.
- **Manifest-driven activation sequence** — `openclaw.plugin.json` carries the 8-slot `PluginManifestActivation` trigger surface (`onStartup`, `onProviders`, `onAgentHarnesses`, `onCommands`, `onChannels`, `onRoutes`, `onConfigPaths`, `onCapabilities`). The Gateway intersects each slot against the current session's actual surface and produces a deterministic load plan — plugins that never match any trigger never get imported, keeping cold-start fast. `loadPluginManifest` returns a discriminated `{ ok: true, manifest, manifestPath } | { ok: false, error, manifestPath }` with hardened root-relative file open, 256 KB cap, and JSON5 fallback parsing.
- **`ApiKeyAuthMethodOptions` re-export and type-derived options** — public option types are derived from underlying factory signatures via `Parameters<typeof X>[0]` + `Omit`, so when `createProviderApiKeyAuthMethod` adds a field the SDK's `SingleProviderPluginApiKeyAuthOptions` updates without manual sync. Catalog options are a discriminated union with `?: never` brands so `buildProvider` and `run` cannot be co-supplied at the type level.
- **Type-only re-export hub as public boundary** — `plugin-entry.ts` re-exports every type a plugin author might need from a single `export type { ... } from "../plugins/types.js"` block, so plugin packages import from `openclaw/plugin-sdk` and never reach into internal paths. This is the same pattern Obsidian uses with the `obsidian` module and VS Code with the `vscode` module — the public package becomes the API audit point.

## Related Terms

- **[OpenClaw — Packaging a Plugin (package.json, Manifest, ClawHub Publish, Setup Entry)](../documentation/openclaw/oc_plugins_sdk_setup_packaging.md)** — This note is the packaging procedure for an OpenClaw plugin, covering the four packaging concerns of the `plugins/sdk-setup` source page that precede…

## Related Code Snippets

- [Plugin SDK — Entries (definePluginEntry / defineSingleProviderPluginEntry)](../code_snippets/snippet_openclaw_plugin_sdk_entries.md): full pattern catalog (7 patterns) for the two authoring factories and the type re-export hub
- [Plugin Package Contract — openclaw.compat.pluginApi](../code_snippets/snippet_openclaw_plugin_package_contract.md): the publish-time validation surface — `isRecord`, `normalizeOptionalString`, `readOpenClawBlock`, `normalizeExternalPluginCompatibility`, `listMissingExternalCodePluginFieldPaths`, `validateExternalCodePluginPackageJson`
- [Plugin Lifecycle — PluginStateKeyedStore + manifest activation](../code_snippets/snippet_openclaw_plugin_lifecycle.md): per-plugin SQLite-backed namespaced state store, `PluginManifestActivation` 8-slot trigger surface, and `loadPluginManifest` hardened parse-and-validate entry

## Related Analysis (FZ 15)


## References

- [OpenClaw `packages/plugin-sdk/` source](https://github.com/openclaw/openclaw/tree/main/packages/plugin-sdk) — upstream authoring package (Class 2: project docs)
- [VS Code Extension API](https://code.visualstudio.com/api) — canonical large-host plugin SDK; commands/configurations/keybindings/views capability slots (Class 2: framework docs)
- [VS Code Extension Manifest reference](https://code.visualstudio.com/api/references/extension-manifest) — manifest-driven activation analog to OpenClaw's `openclaw.plugin.json` (Class 2: framework docs)
- [Obsidian Plugin API — Plugin class reference](https://docs.obsidian.md/Reference/TypeScript+API/Plugin) — `onload`/`onunload` lifecycle + registration helpers pattern (Class 2: framework docs)
- [Plug-in (computing) — Wikipedia](https://en.wikipedia.org/wiki/Plug-in_(computing)) — foundational definition of plugin pattern and host-discovery model (Class 1: Wikipedia foundational)
- [Plugin pattern — Martin Fowler, P of EAA](https://martinfowler.com/eaaCatalog/plugin.html) — canonical patterns-of-enterprise-architecture entry for the host-queries-plugin factory model (Class 1: authoritative pattern catalog)
