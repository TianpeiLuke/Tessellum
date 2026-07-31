---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - reference
keywords:
  - openclaw config reference runtime
  - models.providers custom provider config
  - mcp.servers config
  - skills plugins config block
  - codex harness plugin config
  - openai-compatible endpoints
  - multi-instance isolation
  - commitments config
topics:
  - OpenClaw
  - Gateway Configuration Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/configuration-reference
access_control_group: ["general"]
---

# OpenClaw — Gateway Configuration Reference: Agent Runtime Surfaces

## Overview

This note is the field-level reference for the **agent-runtime cluster** of the OpenClaw Gateway config (`~/.openclaw/openclaw.json`, JSON5 format), drawn from the `gateway/configuration-reference` source page: `channels`, `agents`/`multiAgent`/`session`/`messages` (pointer-only here), `tools`/custom providers (pointer-only), `models` (catalog behavior, custom providers, OpenAI-compatible endpoints, multi-instance isolation), `mcp`, `skills`, `plugins` (including Codex harness config), and `commitments`. Platform surfaces (`browser`/`ui`/`gateway`/`hooks`/`discovery`/`env`) and ops/security surfaces (`secrets`/`auth`/`logging`/`diagnostics`/`cron`) are covered by the sibling reference notes. Config truth: `openclaw config schema` prints the live JSON Schema used for validation, and `config.schema.lookup` returns one path-scoped schema node. All fields are optional — OpenClaw uses safe defaults when omitted.

## Channels

Per-channel config keys live on a dedicated page. The `channels.*` block — Slack, Discord, Telegram, WhatsApp, Matrix, iMessage, and other bundled channels (auth, access control, multi-account, mention gating) — is documented at `/gateway/config-channels` and linked out rather than reproduced.

## Agent Defaults, Multi-Agent, Sessions, and Messages

These blocks moved to a dedicated page (`/gateway/config-agents`) and are referenced by pointer. The reference page enumerates the owning keys: `agents.defaults.*` (workspace, model, thinking, heartbeat, memory, media, skills, sandbox); `multiAgent.*` (multi-agent routing and bindings); `session.*` (session lifecycle, compaction, pruning); `messages.*` (message delivery, TTS, markdown rendering); and `talk.*` (Talk mode). The `talk.*` sub-keys called out are: `talk.consultThinkingLevel` (thinking-level override for the OpenClaw agent run behind Control UI Talk realtime consults), `talk.consultFastMode` (one-shot fast-mode override), `talk.speechLocale` (optional BCP 47 locale id for Talk speech recognition on iOS/macOS), `talk.silenceTimeoutMs` (when unset, Talk keeps the platform default pause window before sending — `700 ms on macOS and Android, 900 ms on iOS`), and `talk.realtime.consultRouting` (Gateway relay fallback for finalized realtime Talk transcripts that skip `openclaw_agent_consult`).

## Tools and Custom Providers

Tool policy, experimental toggles, provider-backed tool config, and custom-provider / base-URL setup moved to a dedicated page (`/gateway/config-tools`), referenced by pointer. The deep `tools.*` policy surface and `models.providers.*` custom-provider field details are digested by the sibling tools/custom-provider notes.

## Models

Provider definitions, model allowlists, and custom-provider setup live in `/gateway/config-tools#custom-providers-and-base-urls`. The `models` root owns global model-catalog behavior:

```json5
{
  models: {
    // Optional. Default: true. Requires a Gateway restart when changed.
    pricing: { enabled: false },
  },
}
```

- `models.mode`: provider catalog behavior (`merge` or `replace`).
- `models.providers`: custom provider map keyed by provider id.
- `models.providers.*.localService`: optional on-demand process manager for local model servers — OpenClaw probes the health endpoint, starts the absolute `command` when needed, waits for readiness, then sends the request (see `/gateway/local-model-services`).
- `models.pricing.enabled`: controls the background pricing bootstrap that starts after sidecars and channels reach the Gateway ready path. When `false`, the Gateway skips OpenRouter and LiteLLM pricing-catalog fetches; configured `models.providers.*.models[].cost` values still work for local estimates.

### Codex Harness Plugin Config

The bundled `codex` plugin owns native Codex app-server harness settings under `plugins.entries.codex.config` (full surface at `/plugins/codex-harness-reference`; runtime model at `/plugins/codex-harness`). `codexPlugins` applies only to sessions that select the native Codex harness — it does not enable Codex plugins for OpenClaw provider runs, ACP conversation bindings, or any non-Codex harness.

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          codexPlugins: {
            enabled: true,
            allow_destructive_actions: true,
            plugins: {
              "google-calendar": {
                enabled: true,
                marketplaceName: "openai-curated",
                pluginName: "google-calendar",
                allow_destructive_actions: false,
              },
            },
          },
        },
      },
    },
  },
}
```

- `plugins.entries.codex.config.codexPlugins.enabled`: enables native Codex plugin/app support for the Codex harness. Default: `false`.
- `plugins.entries.codex.config.codexPlugins.allow_destructive_actions`: default destructive-action policy for migrated plugin app elicitations. Default: `true`.
- `plugins.entries.codex.config.codexPlugins.plugins.<key>.enabled`: enables a migrated plugin entry when global `codexPlugins.enabled` is also true. Default: `true` for explicit entries.
- `plugins.entries.codex.config.codexPlugins.plugins.<key>.marketplaceName`: stable marketplace identity. V1 only supports `"openai-curated"`.
- `plugins.entries.codex.config.codexPlugins.plugins.<key>.pluginName`: stable Codex plugin identity from migration, for example `"google-calendar"`.
- `plugins.entries.codex.config.codexPlugins.plugins.<key>.allow_destructive_actions`: per-plugin destructive-action override; when omitted, the global value is used.

`codexPlugins.enabled` is the global enablement directive; explicit migration-written entries are the durable install/repair eligibility set. `plugins["*"]` is not supported, there is no `install` switch, and local `marketplacePath` values are intentionally not config fields (host-specific). `app/list` readiness checks are cached for one hour and refreshed asynchronously when stale. Codex thread app config is computed at harness session establishment, not per-turn; use `/new`, `/reset`, or a gateway restart after changing native plugin config.

### OpenAI-Compatible Endpoints

The gateway can expose OpenAI-compatible HTTP endpoints, all disabled or off by default:

- Admin HTTP RPC: off by default as the `admin-http-rpc` plugin; enable the plugin to register `POST /api/v1/admin/rpc` (see `/plugins/admin-http-rpc`).
- Chat Completions: disabled by default; enable with `gateway.http.endpoints.chatCompletions.enabled: true`.
- Responses API: `gateway.http.endpoints.responses.enabled`.
- Responses URL-input hardening: `gateway.http.endpoints.responses.maxUrlParts`, `gateway.http.endpoints.responses.files.urlAllowlist`, and `gateway.http.endpoints.responses.images.urlAllowlist`. Empty allowlists are treated as unset; use `gateway.http.endpoints.responses.files.allowUrl=false` and/or `gateway.http.endpoints.responses.images.allowUrl=false` to disable URL fetching.
- Optional response hardening header: `gateway.http.securityHeaders.strictTransportSecurity` (set only for HTTPS origins you control).

### Multi-Instance Isolation

Run multiple gateways on one host with unique ports and state dirs:

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json \
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw gateway --port 19001
```

Convenience flags: `--dev` (uses `~/.openclaw-dev` + port `19001`) and `--profile <name>` (uses `~/.openclaw-<name>`). See `/gateway/multiple-gateways`.

## MCP

OpenClaw-managed MCP server definitions live under `mcp.servers` and are consumed by embedded OpenClaw and other runtime adapters. The `openclaw mcp list`, `show`, `set`, and `unset` commands manage this block without connecting to the target server during config edits.

```json5
{
  mcp: {
    // Optional. Default: 600000 ms (10 minutes). Set 0 to disable idle eviction.
    sessionIdleTtlMs: 600000,
    servers: {
      docs: { command: "npx", args: ["-y", "@modelcontextprotocol/server-fetch"] },
      remote: {
        url: "https://example.com/mcp",
        transport: "streamable-http", // streamable-http | sse
        timeout: 20,
        connectTimeout: 5,
        supportsParallelToolCalls: true,
        headers: { Authorization: "Bearer ${MCP_REMOTE_TOKEN}" },
        auth: "oauth",
        oauth: { scope: "docs.read" },
        sslVerify: true,
        clientCert: "/path/to/client.crt",
        clientKey: "/path/to/client.key",
        toolFilter: { include: ["search_*"], exclude: ["admin_*"] },
        codex: { agents: ["main"], defaultToolsApprovalMode: "approve" }, // auto | prompt | approve
      },
    },
  },
}
```

- `mcp.servers`: named stdio or remote MCP server definitions. Remote entries use `transport: "streamable-http"` or `transport: "sse"`; `type: "http"` is a CLI-native alias that `openclaw mcp set` and `openclaw doctor --fix` normalize into the canonical `transport` field.
- `mcp.servers.<name>.enabled`: set `false` to keep a saved server definition while excluding it from embedded OpenClaw MCP discovery and tool projection.
- `mcp.servers.<name>.timeout` / `requestTimeoutMs`: per-server MCP request timeout in seconds or milliseconds.
- `mcp.servers.<name>.connectTimeout` / `connectionTimeoutMs`: per-server connection timeout in seconds or milliseconds.
- `mcp.servers.<name>.supportsParallelToolCalls`: optional concurrency hint for adapters that can choose whether to issue parallel MCP tool calls.
- `mcp.servers.<name>.auth`: set `"oauth"` for HTTP MCP servers that require OAuth. Run `openclaw mcp login <name>` to store tokens under OpenClaw state.
- `mcp.servers.<name>.oauth`: optional OAuth scope, redirect URL, and client metadata URL overrides.
- `mcp.servers.<name>.sslVerify`, `clientCert`, `clientKey`: HTTP TLS controls for private endpoints and mutual TLS.
- `mcp.servers.<name>.toolFilter`: optional per-server tool selection. `include` limits discovered tools to matching names; `exclude` hides matching names. Entries are exact MCP tool names or simple `*` globs. Servers with resources or prompts also generate utility tool names (`resources_list`, `resources_read`, `prompts_list`, `prompts_get`), which use the same filter.
- `mcp.servers.<name>.codex`: optional Codex app-server projection controls — OpenClaw metadata for Codex app-server threads only; does not affect ACP sessions, generic Codex harness config, or other adapters. Non-empty `codex.agents` limits the server to the listed agent ids (empty/blank/invalid scoped lists are rejected by validation and omitted instead of becoming global). `codex.defaultToolsApprovalMode` emits Codex's native `default_tools_approval_mode`. OpenClaw strips the `codex` block before passing native `mcp_servers` to Codex; omit it to keep the server projected for every Codex app-server agent with Codex's default MCP approval behavior.
- `mcp.sessionIdleTtlMs`: idle TTL for session-scoped bundled MCP runtimes. One-shot embedded runs request run-end cleanup; this TTL is the backstop for long-lived sessions.
- Changes under `mcp.*` hot-apply by disposing cached session MCP runtimes; the next tool discovery/use recreates them, so removed `mcp.servers` entries are reaped immediately instead of waiting for idle TTL. Discovery honors MCP tool-list change notifications by dropping the cached catalog, and repeated tool-call failures pause the server briefly. See `/cli/mcp#openclaw-as-an-mcp-client-registry` and `/gateway/cli-backends#bundle-mcp-overlays`.

## Skills

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills"],
      allowSymlinkTargets: ["~/Projects/manager/skills"],
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn | bun
      allowUploadedArchives: false,
    },
    workshop: { allowSymlinkTargetWrites: false },
    entries: {
      "image-lab": {
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" }, // or plaintext string
        env: { GEMINI_API_KEY: "GEMINI_KEY_HERE" },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

- `allowBundled`: optional allowlist for bundled skills only (managed/workspace skills unaffected).
- `load.extraDirs`: extra shared skill roots (lowest precedence).
- `load.allowSymlinkTargets`: trusted real target roots that skill symlinks may resolve into when the link lives outside its source root.
- `workshop.allowSymlinkTargetWrites`: allows Skill Workshop apply to write through already-trusted symlink targets (default: `false`).
- `install.preferBrew`: when true, prefer Homebrew installers when `brew` is available before falling back to other kinds.
- `install.nodeManager`: node installer preference for `metadata.openclaw.install` specs (`npm` | `pnpm` | `yarn` | `bun`).
- `install.allowUploadedArchives`: allow trusted `operator.admin` Gateway clients to install private zip archives staged through `skills.upload.*` (default: `false`); only enables the uploaded-archive path (normal ClawHub installs do not require it).
- `entries.<skillKey>.enabled: false` disables a skill even if bundled/installed.
- `entries.<skillKey>.apiKey`: convenience for skills declaring a primary env var (plaintext string or SecretRef object).

## Plugins

```json5
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: [],
    load: { paths: ["~/Projects/oss/voice-call-plugin"] },
    entries: {
      "voice-call": {
        enabled: true,
        hooks: { allowPromptInjection: false },
        config: { provider: "twilio" },
      },
    },
  },
}
```

- Loaded from package/bundle directories under `~/.openclaw/extensions` and `<workspace>/.openclaw/extensions`, plus files or directories listed in `plugins.load.paths`. Put standalone plugin files in `plugins.load.paths`; auto-discovered extension roots ignore top-level `.js`, `.mjs`, and `.ts` files so helper scripts do not block startup.
- Discovery accepts native OpenClaw plugins plus compatible Codex bundles and Claude bundles (including manifestless Claude default-layout bundles). **Config changes require a gateway restart.**
- `allow`: optional allowlist (only listed plugins load). `deny` wins.
- `plugins.entries.<id>.apiKey`: plugin-level API key convenience field (when supported by the plugin).
- `plugins.entries.<id>.env`: plugin-scoped env var map.
- `plugins.entries.<id>.hooks.allowPromptInjection`: when `false`, core blocks `before_prompt_build` and ignores prompt-mutating fields from legacy `before_agent_start`, while preserving legacy `modelOverride` and `providerOverride`. Applies to native plugin hooks and supported bundle-provided hook directories.
- `plugins.entries.<id>.hooks.allowConversationAccess`: when `true`, trusted non-bundled plugins may read raw conversation content from typed hooks (`llm_input`, `llm_output`, `before_model_resolve`, `before_agent_reply`, `before_agent_run`, `before_agent_finalize`, `agent_end`).
- `plugins.entries.<id>.subagent.allowModelOverride`: explicitly trust this plugin to request per-run `provider` and `model` overrides for background subagent runs.
- `plugins.entries.<id>.subagent.allowedModels`: optional allowlist of canonical `provider/model` targets for trusted subagent overrides (`"*"` allows any model).
- `plugins.entries.<id>.llm.allowModelOverride`: explicitly trust this plugin to request model overrides for `api.runtime.llm.complete`.
- `plugins.entries.<id>.llm.allowedModels`: optional allowlist of canonical `provider/model` targets for trusted plugin LLM completion overrides (`"*"` allows any model).
- `plugins.entries.<id>.llm.allowAgentIdOverride`: explicitly trust this plugin to run `api.runtime.llm.complete` against a non-default agent id.
- `plugins.entries.<id>.config`: plugin-defined config object (validated by native OpenClaw plugin schema when available).
- Channel plugin account/runtime settings live under `channels.<id>`, described by the owning plugin's manifest `channelConfigs` metadata, not a central OpenClaw option registry.

Selected plugin-specific entries on the reference page: `plugins.entries.firecrawl.config.webFetch` (`apiKey` accepting SecretRef, falling back to `plugins.entries.firecrawl.config.webSearch.apiKey`, legacy `tools.web.fetch.firecrawl.apiKey`, or `FIRECRAWL_API_KEY`; `baseUrl` default `https://api.firecrawl.dev`; `onlyMainContent` default `true`; `maxAgeMs` default `172800000` / 2 days; `timeoutSeconds` default `60`); `plugins.entries.xai.config.xSearch` (`enabled`; `model` such as `"grok-4-1-fast"`); and `plugins.entries.memory-core.config.dreaming` (`enabled` default `false`; `frequency` cron cadence default `"0 3 * * *"`; `model` optional Dream Diary subagent model override requiring `plugins.entries.memory-core.subagent.allowModelOverride: true`). Full memory config (`agents.defaults.memorySearch.*`, `memory.backend`, `memory.citations`, `memory.qmd.*`, `plugins.entries.memory-core.config.dreaming`) lives in `/reference/memory-config`. Enabled Claude bundle plugins can contribute embedded OpenClaw defaults from `settings.json`, applied as sanitized agent settings, not raw config patches. `plugins.slots.memory` picks the active memory plugin id (or `"none"` to disable); `plugins.slots.contextEngine` picks the active context engine plugin id (defaults to `"legacy"`).

## Commitments

`commitments` controls inferred follow-up memory: OpenClaw can detect check-ins from conversation turns and deliver them through heartbeat runs.

- `commitments.enabled`: enable hidden LLM extraction, storage, and heartbeat delivery for inferred follow-up commitments. Default: `false`.
- `commitments.maxPerDay`: maximum inferred follow-up commitments delivered per agent session in a rolling day. Default: `3`.

See `/concepts/commitments`.

**Source**: OpenClaw documentation — `gateway/configuration-reference` (mirror `inbox/openclaw_docs/gateway/configuration-reference.md`), agent-runtime cluster
**Last Updated**: 2026-06-22
**Status**: Active
