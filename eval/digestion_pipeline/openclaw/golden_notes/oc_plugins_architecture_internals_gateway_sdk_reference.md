---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw plugin gateway http routes
  - registerHttpRoute auth gateway plugin
  - openclaw plugin-sdk import subpaths
  - describeMessageTool message presentation
  - channel target resolution messaging adapter
  - registerContextEngine context engine plugin
  - registerModelCatalogProvider provider catalog order
  - package packs openclaw.extensions setupEntry
topics:
  - OpenClaw
  - Plugin Architecture Internals
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/architecture-internals
access_control_group: ["general"]
---

# OpenClaw — Plugin Internals: Gateway Routes, SDK Import Paths & Catalog Reference

## Overview

This note models the **reference surfaces** a native OpenClaw plugin uses against the live registry — the back half of the `plugins/architecture-internals` source page, after the load pipeline / registry model and the runtime-hook surface. It tables gateway HTTP routes (`api.registerHttpRoute`), plugin SDK import subpaths (`openclaw/plugin-sdk/*`), message-tool schema contributions (`describeMessageTool`), channel target resolution, config-backed directory helpers, provider catalogs (`catalog.order`, `registerModelCatalogProvider`) and channel catalog metadata (`openclaw.channel` / `openclaw.install`), read-only channel inspection (`inspectAccount`), package packs (`openclaw.extensions` / `setupEntry`), and context-engine plugins (`registerContextEngine`) — the consumption-side contracts the registry exposes to gateway/channel/feature plugins.

## Gateway HTTP Routes

Plugins expose HTTP endpoints with `api.registerHttpRoute(...)`. Route fields: `path` (route path under the gateway HTTP server); `auth` (**required** — `"gateway"` for normal gateway auth, or `"plugin"` for plugin-managed auth/webhook verification); `match` (optional — `"exact"` (default) or `"prefix"`); `replaceExisting` (optional — lets the same plugin replace its own route); `handler` (return `true` when the route handled the request).

```ts
api.registerHttpRoute({
  path: "/acme/webhook",
  auth: "plugin",
  match: "exact",
  handler: async (_req, res) => {
    res.statusCode = 200;
    res.end("ok");
    return true;
  },
});
```

Constraints: `api.registerHttpHandler(...)` was removed and will cause a plugin-load error — use `api.registerHttpRoute(...)`. Plugin routes must declare `auth` explicitly. Exact `path + match` conflicts are rejected unless `replaceExisting: true`, and one plugin cannot replace another's route. Overlapping routes with different `auth` levels are rejected; keep `exact`/`prefix` fallthrough chains on the same auth level only.

The `auth` levels carry distinct runtime-scope semantics. `auth: "plugin"` routes do **not** receive operator runtime scopes automatically — they are for plugin-managed webhooks/signature verification, not privileged Gateway helper calls. `auth: "gateway"` routes run inside an intentionally conservative scope: shared-secret bearer auth (`gateway.auth.mode = "token"` / `"password"`) keeps scopes pinned to `operator.write` even if the caller sends `x-openclaw-scopes`; trusted identity-bearing HTTP modes (e.g. `trusted-proxy` or `gateway.auth.mode = "none"` on a private ingress) honor `x-openclaw-scopes` only when explicitly present, falling back to `operator.write` when absent. Practical rule: do not assume a gateway-auth plugin route is an implicit admin surface — for admin-only behavior, require an identity-bearing auth mode and document the explicit `x-openclaw-scopes` header contract.

## Plugin SDK Import Paths

New plugins should use narrow SDK subpaths, not the monolithic `openclaw/plugin-sdk` root barrel. Core subpaths:

| Subpath | Purpose |
| --- | --- |
| `openclaw/plugin-sdk/plugin-entry` | Plugin registration primitives |
| `openclaw/plugin-sdk/channel-core` | Channel entry/build helpers |
| `openclaw/plugin-sdk/core` | Generic shared helpers and umbrella contract |
| `openclaw/plugin-sdk/config-schema` | Root `openclaw.json` Zod schema (`OpenClawSchema`) |

Channel plugins pick from narrow seams: `channel-setup`, `setup-runtime`, `setup-tools`, `channel-pairing`, `channel-contract`, `channel-feedback`, `channel-inbound`, `channel-outbound`, `command-auth`, `secret-input`, `webhook-ingress`, `channel-targets`, `channel-actions`; approval behavior should consolidate on one `approvalCapability` contract. Runtime/config helpers live under focused `*-runtime` subpaths (`approval-runtime`, `agent-runtime`, `lazy-runtime`, `directory-runtime`, `text-runtime`, `runtime-store`, `system-event-runtime`, `heartbeat-runtime`, `channel-activity-runtime`, etc.); prefer `config-contracts`, `plugin-config-runtime`, `runtime-config-snapshot`, and `config-mutation` over the broad `config-runtime` compatibility barrel.

Deprecated compatibility shims (new code should import narrower generic primitives): `openclaw/plugin-sdk/channel-runtime`, `openclaw/plugin-sdk/channel-lifecycle`, small channel helper facades, `openclaw/plugin-sdk/outbound-runtime`, `openclaw/plugin-sdk/outbound-send-deps`, `openclaw/plugin-sdk/config-runtime`, and `openclaw/plugin-sdk/infra-runtime`. Repo-internal entry points (per bundled plugin package root): `index.js` (bundled plugin entry), `api.js` (helper/types barrel), `runtime-api.js` (runtime-only barrel), `setup-entry.js` (setup plugin entry). External plugins should only import `openclaw/plugin-sdk/*` subpaths; never another plugin package's `src/*`. Facade-loaded entry points prefer the active runtime config snapshot when one exists, then fall back to the on-disk config file. Capability-specific subpaths such as `image-generation`, `media-understanding`, and `speech` exist because bundled plugins use them today, but are not long-term frozen external contracts — check the relevant SDK reference page when relying on them.

## Message Tool Schemas

Plugins should own channel-specific `describeMessageTool(...)` schema contributions for non-message primitives such as reactions, reads, and polls. Shared send presentation should use the generic `MessagePresentation` contract, not provider-native button, component, block, or card fields. Send-capable plugins declare what they can render through message capabilities: `presentation` for semantic presentation blocks (`text`, `context`, `divider`, `buttons`, `select`), and `delivery-pin` for pinned-delivery requests. Core decides whether to render presentation natively or degrade to text; do not expose provider-native UI escape hatches from the generic message tool. Deprecated SDK helpers for legacy native schemas remain exported for existing third-party plugins; new plugins should not use them.

## Channel Target Resolution

Channel plugins should own channel-specific target semantics while the shared outbound host stays generic, using the messaging adapter for provider rules. The adapter methods: `messaging.inferTargetChatType({ to })` decides whether a normalized target is `direct`, `group`, or `channel` before directory lookup; `messaging.targetResolver.looksLikeId(raw, normalized)` tells core whether an input should skip to id-like resolution instead of directory search; `messaging.targetResolver.resolveTarget(...)` is the plugin fallback when core needs a final provider-owned resolution after normalization or a directory miss; `messaging.resolveOutboundSessionRoute(...)` owns provider-specific session route construction once a target is resolved.

Recommended split: use `inferTargetChatType` for category decisions before searching peers/groups; `looksLikeId` for "treat this as an explicit/native target id" checks; `resolveTarget` for provider-specific normalization fallback (not broad directory search); keep provider-native ids (chat ids, thread ids, JIDs, handles, room ids) inside `target` values or provider-specific params, not generic SDK fields.

## Config-Backed Directories

Plugins deriving directory entries from config should keep that logic in the plugin and reuse the shared helpers from `openclaw/plugin-sdk/directory-runtime` — for config-backed peers/groups such as allowlist-driven DM peers, configured channel/group maps, or account-scoped static directory fallbacks. The `directory-runtime` helpers only handle generic operations: query filtering, limit application, deduping/normalization, and building `ChannelDirectoryEntry[]`. Channel-specific account inspection and id normalization stay in the plugin.

## Provider Catalogs

Provider plugins define model catalogs with `registerProvider({ catalog: { run(...) { ... } } })`. `catalog.run(...)` returns the shape OpenClaw writes into `models.providers`: `{ provider }` for one entry or `{ providers }` for multiple. Use `catalog` when the plugin owns provider-specific model ids, base URL defaults, or auth-gated metadata. `catalog.order` controls when a catalog merges relative to built-in implicit providers: `simple` (plain API-key/env-driven), `profile` (appear when auth profiles exist), `paired` (synthesize related entries), `late` (last pass). Later providers win on key collision, so a plugin can override a built-in provider with the same id.

Plugins can also publish read-only model rows through `api.registerModelCatalogProvider({ provider, kinds, staticCatalog, liveCatalog })` — the forward path for list/help/picker surfaces, supporting `text`, `image_generation`, `video_generation`, and `music_generation` rows. Provider plugins still own live endpoint calls, token exchange, and vendor response mapping; core owns the common row shape, source labels, and media-tool help formatting; media-generation registrations synthesize static rows from `defaultModel`, `models`, and `capabilities`. Compatibility: `discovery` is a legacy alias (deprecation warning); if both `catalog` and `discovery` register, OpenClaw uses `catalog`; `augmentModelCatalog` is deprecated — publish supplemental rows through `registerModelCatalogProvider`.

### Channel Catalog Metadata

Channel plugins advertise setup/discovery metadata via `openclaw.channel` and install hints via `openclaw.install` in `package.json`, keeping the core catalog data-free.

```json
{
  "name": "@openclaw/nextcloud-talk",
  "openclaw": {
    "extensions": ["./index.ts"],
    "channel": {
      "id": "nextcloud-talk",
      "label": "Nextcloud Talk",
      "docsPath": "/channels/nextcloud-talk",
      "order": 65,
      "aliases": ["nc-talk", "nc"]
    },
    "install": {
      "npmSpec": "@openclaw/nextcloud-talk",
      "localPath": "<bundled-plugin-local-path>",
      "defaultChoice": "npm"
    }
  }
}
```

Other `openclaw.channel` fields: `selectionLabel` / `detailLabel` / `docsLabel` (catalog/status/docs labels); `blurb`; `preferOver` (ids this entry outranks); `selectionDocsPrefix` / `selectionDocsOmitLabel` / `selectionExtras` (selection-surface copy); `markdownCapable`; `exposure.configured` / `exposure.setup` / `exposure.docs` (hide from configured listings / setup pickers / mark internal for docs); `showConfigured` / `showInSetup` (legacy aliases, prefer `exposure`); `quickstartAllowFrom`; `forceAccountBinding` (require explicit binding even with one account); `preferSessionLookupForAnnounceTarget`.

OpenClaw can also merge **external channel catalogs** (e.g. an MPM registry export): drop a JSON file at `~/.openclaw/mpm/plugins.json`, `~/.openclaw/mpm/catalog.json`, or `~/.openclaw/plugins/catalog.json`, or point `OPENCLAW_PLUGIN_CATALOG_PATHS` (or `OPENCLAW_MPM_CATALOG_PATHS`) at one or more JSON files (comma/semicolon/`PATH`-delimited). Each file should contain `{ "entries": [ { "name": "@scope/pkg", "openclaw": { "channel": {...}, "install": {...} } } ] }` (the parser also accepts `"packages"` / `"plugins"` as legacy aliases for `"entries"`). Generated catalog/provider-install entries expose normalized install-source facts (`installSource` is additive optional), warning when the npm name drifts from a known identity, when `defaultChoice` is invalid or unavailable, and when integrity metadata lacks a valid npm source; official external npm entries should prefer an exact `npmSpec` plus `expectedIntegrity`. The persisted `installed_plugin_index` SQLite row is the install source of truth, refreshable without loading plugin runtime — its `installRecords` map is durable even when a manifest is missing or invalid, and its `plugins` payload is a rebuildable manifest view.

## Read-Only Channel Inspection

If a plugin registers a channel, it should prefer implementing `plugin.config.inspectAccount(cfg, accountId)` alongside `resolveAccount(...)`. Rationale: `resolveAccount(...)` is the runtime path — it may assume credentials are fully materialized and fail fast on missing secrets; read-only command paths (`openclaw status`, `openclaw status --all`, `openclaw channels status`, `openclaw channels resolve`, doctor/config repair) should not need to materialize runtime credentials just to describe configuration.

Recommended `inspectAccount(...)` behavior: return descriptive account state only; preserve `enabled` and `configured`; include credential source/status fields when relevant (`tokenSource` / `tokenStatus`, `botTokenSource` / `botTokenStatus`, `appTokenSource` / `appTokenStatus`, `signingSecretSource` / `signingSecretStatus`). Raw token values are not needed — `tokenStatus: "available"` (plus the matching source field) suffices for status commands. Use `configured_unavailable` when a credential is configured via SecretRef but unavailable in the current command path, so read-only commands report "configured but unavailable in this command path" instead of crashing or misreporting the account.

## Package Packs

A plugin directory may include a `package.json` with `openclaw.extensions`. Each entry becomes a plugin; with multiple extensions, the plugin id becomes `name/<fileBase>`.

```json
{
  "name": "my-pack",
  "openclaw": {
    "extensions": ["./src/safety.ts", "./src/tools.ts"],
    "setupEntry": "./src/setup-entry.ts"
  }
}
```

Install npm deps in that directory so `node_modules` is available. Security guardrail: every `openclaw.extensions` entry must stay inside the plugin directory after symlink resolution — escaping entries are rejected. `openclaw plugins install` installs deps with a project-local `npm install --omit=dev --ignore-scripts` (no lifecycle scripts, no dev deps at runtime), ignoring global npm settings; keep dependency trees "pure JS/TS" and avoid packages needing `postinstall` builds.

Optional `openclaw.setupEntry` points at a lightweight setup-only module: for a disabled channel plugin, or an enabled-but-unconfigured one, OpenClaw loads `setupEntry` instead of the full entry — keeping startup lighter when the main entry also wires runtime-only code. Optional `openclaw.startup.deferConfiguredChannelFullLoadUntilAfterListen` opts a channel plugin into the same `setupEntry` path during the gateway's pre-listen phase even when configured — use only when `setupEntry` fully covers the pre-listen startup surface (channel registration, HTTP routes, gateway methods/tools/services needed in that window); if the full entry still owns any required startup capability, do not enable the flag.

Bundled channels can also publish setup-only contract-surface helpers core consults before the full channel runtime loads; the promotion surface is `singleAccountKeysToMove`, `namedAccountPromotionKeys`, and `resolveSingleAccountPromotionTarget(...)`, used to promote a legacy single-account channel config into `channels.<id>.accounts.*` without loading the full entry (Matrix is the bundled example). When startup surfaces include gateway RPC methods, keep them on a plugin-specific prefix: core admin namespaces (`config.*`, `exec.approvals.*`, `wizard.*`, `update.*`) stay reserved and always resolve to `operator.admin`.

## Context Engine Plugins

Context engine plugins own session context orchestration for ingest, assembly, and compaction. Register them with `api.registerContextEngine(id, factory)`, then select the active engine with `plugins.slots.contextEngine` — for replacing or extending the default context pipeline, not just adding memory search or hooks. The factory `ctx` exposes optional `config`, `agentDir`, `workspaceDir`.

```ts
import { buildMemorySystemPromptAddition } from "openclaw/plugin-sdk/core";

export default function (api) {
  api.registerContextEngine("lossless-claw", (ctx) => ({
    info: { id: "lossless-claw", name: "Lossless Claw", ownsCompaction: true },
    async ingest() {
      return { ingested: true };
    },
    async assemble({ messages, availableTools, citationsMode }) {
      return {
        messages,
        estimatedTokens: 0,
        systemPromptAddition: buildMemorySystemPromptAddition({
          availableTools: availableTools ?? new Set(),
          citationsMode,
        }),
      };
    },
    async compact() {
      return { ok: true, compacted: false };
    },
  }));
}
```

`assemble()` may return `contextProjection` when the active harness has a persistent backend thread (omit for legacy per-turn projection); return `{ mode: "thread_bootstrap", epoch }` to inject context once into a backend thread and reuse until the epoch changes (bump the epoch after the engine's semantic context changes, e.g. an engine-owned compaction pass). If an engine does **not** own the compaction algorithm, keep `compact()` implemented and delegate via `delegateCompactionToRuntime(params)` (from `openclaw/plugin-sdk/core`), declaring `info.ownsCompaction: false`.

**Source**: OpenClaw documentation — `plugins/architecture-internals` (mirror `inbox/openclaw_docs/plugins/architecture-internals.md`), reference sections: Gateway HTTP routes, Plugin SDK import paths, Message tool schemas, Channel target resolution, Config-backed directories, Provider catalogs, Read-only channel inspection, Package packs, Context engine plugins
**Last Updated**: 2026-06-22
**Status**: Active
