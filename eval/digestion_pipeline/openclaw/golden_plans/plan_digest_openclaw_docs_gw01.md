---
title: Sub-Plan gw01 — OpenClaw Docs: Gateway (Auth, Background Process, Bonjour, Bridge Protocol, CLI Backends, Config Agents, Config Channels)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["gateway/authentication", "gateway/background-process", "gateway/bonjour", "gateway/bridge-protocol", "gateway/cli-backends", "gateway/config-agents", "gateway/config-channels"]
---

# Sub-Plan gw01: Gateway

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*` prefix), format, dedup (3-way vs term_dictionary + documentation + repo_openclaw*), undigested-terms ownership, 9-GATE validation, cross-references, and entry-point wiring are ALL inherited from the master and are NOT re-derived here.

## Scope

The 7 Gateway-section pages covering the model-authentication reference, the gateway's process/subprocess machinery (exec/process tools, child-process bridging), the Bonjour/DNS-SD service-discovery layer over Tailscale, the legacy bridge wire protocol, the CLI-backend fallback subsystem, and the two large configuration references — agent defaults/multi-agent routing/session/messages/talk (`config-agents`) and per-channel configuration (`config-channels`). **Priority P1 (Phase A)** — the gateway is the FZ 15 integration target and defines the auth/process/config vocabulary the CLI, channels, providers, and tools sub-plans reference. The code-side counterparts `repo_openclaw_gateway`, `repo_openclaw_agents`, `repo_openclaw_channels`, `repo_openclaw_security` are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **20,858 measured words** (mirror `inbox/openclaw_docs/gateway/`). **Planned: 13 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| authentication | gateway/authentication | 1,575 | 14 | 9 | 6 | procedure |
| background-process | gateway/background-process | 862 | 8 | 5 | 0 | concept (exec/process model) |
| bonjour | gateway/bonjour | 1,713 | 6 | 16 | 4 | procedure (discovery setup + troubleshooting) |
| bridge-protocol | gateway/bridge-protocol | 537 | 0 | 8 | 0 | model (wire protocol) |
| cli-backends | gateway/cli-backends | 2,680 | 10 | 16 | 1 | procedure (split: setup/usage vs internals) |
| config-agents | gateway/config-agents | 8,129 | 41 | 6 | 33 | procedure (split ×6: agent defaults config) |
| config-channels | gateway/config-channels | 5,362 | 20 | 2 | 18 | procedure (split ×2: per-channel config + routing/commands) |

## Content Strategy

- **Prioritize**: model authentication (every gateway run depends on credential resolution + rotation behavior); the agent-defaults configuration surface (the largest, most-referenced reference page); per-channel configuration (the channels sub-plans reference these config keys); Bonjour discovery (the multi-node networking entry point).
- **Split**: `config-agents.md` (8,129w / 41 fences) → **6 notes** by config-key cluster (bootstrap/context, model/image/timezone, runtime-policy/backends/overlays, heartbeat/compaction/retries/pruning/streaming/sandbox, multi-agent routing, session+messages+talk). `config-channels.md` (5,362w / 20 fences) → **2 notes** (per-channel transport config vs routing/groups/mention-gating/commands). `cli-backends.md` (2,680w / 10 fences) → **2 notes** (setup+usage procedure vs internals/sessions/defaults/compaction). Each split note kept ≤2,500w / ≤6 code fences / one BB.
- **Link-out (do not redefine)**: model-provider catalog & provider-specific keys → `pr01–pr09`; `concepts/oauth` flow → `co05` (oc note, planned); SecretRef `env`/`file`/`exec` providers → `gateway/secrets` (gw05); trusted-proxy / gateway-connection auth → `gateway/trusted-proxy-auth` (gw07) + `gateway/configuration` (gw02); `auth-credential-semantics` → `rt01`; the channel transport plugins themselves → `ch01–ch06`. Existing vault terms (`term_openclaw`, `term_oauth`, `term_oauth_token`, `term_mcp`, `term_dns`, `term_function_calling`, etc.) are LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_gateway_authentication.md` | procedure | authentication.md: Recommended setup; Anthropic Claude CLI / token compatibility; Anthropic note; Checking model auth status; API key rotation behavior; Removing provider auth while running; Controlling which credential is used (login / per-session / per-agent); OpenAI legacy ids; Troubleshooting | 700 | Authenticating OpenClaw to model providers: API-key recommended setup, Claude CLI / setup-token reuse, checking auth status, in-flight API-key rotation, removing provider auth, and per-login/session/agent credential control. |
| 2 | `oc_gateway_background_process.md` | concept | background-process.md: exec tool; Child process bridging; process tool; Examples | 550 | The gateway's background-process model: the `exec` tool for shell commands, child-process bridging into the gateway, and the `process` tool for managing long-running background processes. |
| 3 | `oc_gateway_bonjour.md` | procedure | bonjour.md: Wide-area Bonjour (Unicast DNS-SD) over Tailscale (Gateway config, DNS server setup, Tailscale DNS, listener security); What advertises; Service types; TXT keys; When to enable/disable; Enabling/disabling/configuration | 750 | Configuring wide-area Bonjour (Unicast DNS-SD) service discovery over Tailscale: gateway/DNS/Tailscale setup, what is advertised, service types and TXT hint keys, listener security, and when to enable or disable discovery. |
| 4 | `oc_gateway_bonjour_troubleshooting.md` | procedure | bonjour.md: Debugging on macOS; Debugging in Gateway logs; Debugging on iOS node; Docker gotchas; Troubleshooting disabled Bonjour; Common failure modes; Escaped instance names (`\032`) | 600 | Troubleshooting Bonjour/DNS-SD discovery: debugging on macOS, in gateway logs, and on iOS nodes; Docker networking gotchas; resolving disabled Bonjour; common failure modes; and escaped (`\032`) instance names. |
| 5 | `oc_gateway_bridge_protocol.md` | model | bridge-protocol.md: Why it existed; Transport; Handshake + pairing; Frames; Exec lifecycle events; Historical tailnet usage; Versioning | 450 | The legacy gateway bridge wire protocol: its purpose, transport, handshake/pairing, frame format, exec-lifecycle events, historical tailnet usage, and versioning. |
| 6 | `oc_gateway_cli_backends.md` | procedure | cli-backends.md: Beginner-friendly quick start; Using it as a fallback; Configuration overview (incl. Example configuration); Images (pass-through); Inputs / outputs; Limitations; Troubleshooting | 700 | Setting up CLI backends as a text-only model fallback: quick start, fallback configuration, the config schema with worked example, image pass-through, I/O behavior, limitations, and troubleshooting. |
| 7 | `oc_gateway_cli_backends_internals.md` | concept | cli-backends.md: How it works; Sessions; Fallback prelude from claude-cli sessions; Defaults (plugin-owned); Plugin-owned defaults; Native compaction ownership; Bundle MCP overlays; Reseed history cap | 650 | How CLI backends work internally: the JSONL streaming loop and MCP loopback bridge, session reuse, claude-cli fallback prelude, plugin-owned defaults, native-compaction ownership, bundle MCP overlays, and the reseed history cap. |
| 8 | `oc_gateway_config_agents_bootstrap_context.md` | procedure | config-agents.md: Agent defaults — workspace, repoRoot, skills, skipBootstrap, skipOptionalBootstrapFiles, contextInjection, bootstrapMaxChars, bootstrapTotalMaxChars, per-agent bootstrap profile overrides, bootstrapPromptTruncationWarning, Context budget ownership map | 700 | Agent-defaults config for workspace/bootstrap/context: `workspace`, `repoRoot`, `skills`, bootstrap skip flags, `contextInjection`, bootstrap char budgets, per-agent bootstrap profile overrides, and the context-budget ownership map. |
| 9 | `oc_gateway_config_agents_model_media.md` | procedure | config-agents.md: Agent defaults — imageMaxDimensionPx, imageQuality, userTimezone, timeFormat, model, Runtime policy | 600 | Agent-defaults config for model, media, and time: `imageMaxDimensionPx`, `imageQuality`, `userTimezone`, `timeFormat`, the `model` selection block, and the runtime policy section. |
| 10 | `oc_gateway_config_agents_backends_overlays.md` | procedure | config-agents.md: Agent defaults — cliBackends, promptOverlays | 500 | Agent-defaults config for backends and prompts: the `cliBackends` fallback config block and `promptOverlays` for injecting/overriding prompt fragments. |
| 11 | `oc_gateway_config_agents_runtime_resilience.md` | procedure | config-agents.md: Agent defaults — heartbeat, compaction, runRetries, contextPruning, Block streaming, Typing indicators, sandbox | 750 | Agent-defaults config for runtime resilience and presentation: `heartbeat`, `compaction`, `runRetries`, `contextPruning`, block streaming, typing indicators, and the `sandbox` execution policy. |
| 12 | `oc_gateway_config_agents_routing.md` | procedure | config-agents.md: agents.list (per-agent overrides); Multi-agent routing (Binding match fields, Per-agent access profiles) | 600 | Per-agent overrides and multi-agent routing config: the `agents.list` array, binding match fields that route inbound messages to a specific agent, and per-agent access profiles. |
| 13 | `oc_gateway_config_agents_session_messages.md` | procedure | config-agents.md: Session; Messages (Response prefix, Ack reaction, Inbound debounce, TTS); Talk | 600 | Agent-defaults config for session, messaging, and talk: the `Session` block, the `Messages` block (response prefix, ack reaction, inbound debounce, TTS), and the `Talk` (voice) block. |
| 14 | `oc_gateway_config_channels.md` | procedure | config-channels.md: Channels — DM and group access; Channel model overrides; Channel defaults and heartbeat; WhatsApp; Telegram; Discord; Google Chat; Slack; Mattermost; Signal; iMessage; Matrix; Microsoft Teams; IRC; Multi-account; Other plugin channels | 750 | Per-channel transport configuration: DM/group access, channel model overrides, channel defaults/heartbeat, and the per-platform config blocks (WhatsApp, Telegram, Discord, Google Chat, Slack, Mattermost, Signal, iMessage, Matrix, Teams, IRC) plus multi-account setup. |
| 15 | `oc_gateway_config_channels_routing_commands.md` | procedure | config-channels.md: Channels — Group chat mention gating; Commands (chat command handling) | 600 | Channel routing and command handling config: group-chat mention gating (when the bot responds in groups) and the chat-command handling configuration. |

> **Note:** 15 notes against the master's 11-note estimate — the two oversized config reference pages (`config-agents` 8,129w, `config-channels` 5,362w) drive the split. Final count locks at augment.

## Section Coverage Map

```
authentication.md
├── Recommended setup (API key) ─────────────────── → note 1 (oc_gateway_authentication)
├── Anthropic: Claude CLI and token compatibility ─ → note 1
│   └── OpenAI and legacy openai-codex ids (H3) ─── → note 1
├── Anthropic note ──────────────────────────────── → note 1
├── Checking model auth status ──────────────────── → note 1
├── API key rotation behavior (gateway) ─────────── → note 1
├── Removing provider auth while running ─────────── → note 1
├── Controlling which credential is used ─────────── → note 1
│   ├── During login (CLI) (H3) ─────────────────── → note 1
│   ├── Per-session (chat command) (H3) ─────────── → note 1
│   └── Per-agent (CLI override) (H3) ───────────── → note 1
├── Troubleshooting (No credentials / expiring H3s) → note 1
└── Related ─────────────────────────────────────── → (link-out, not a section)
background-process.md
├── exec tool ───────────────────────────────────── → note 2 (oc_gateway_background_process)
├── Child process bridging ──────────────────────── → note 2
├── process tool ────────────────────────────────── → note 2
├── Examples ────────────────────────────────────── → note 2
└── Related ─────────────────────────────────────── → (link-out)
bonjour.md
├── Wide-area Bonjour (Unicast DNS-SD) over Tailscale → note 3 (oc_gateway_bonjour)
│   ├── Gateway config (recommended) (H3) ───────── → note 3
│   ├── One-time DNS server setup (H3) ──────────── → note 3
│   ├── Tailscale DNS settings (H3) ─────────────── → note 3
│   └── Gateway listener security (H3) ──────────── → note 3
├── What advertises / Service types / TXT keys ──── → note 3
├── When to enable / disable Bonjour ────────────── → note 3
├── Enabling / disabling / configuration ────────── → note 3
├── Debugging on macOS ──────────────────────────── → note 4 (oc_gateway_bonjour_troubleshooting)
├── Debugging in Gateway logs ───────────────────── → note 4
├── Debugging on iOS node ───────────────────────── → note 4
├── Docker gotchas ──────────────────────────────── → note 4
├── Troubleshooting disabled Bonjour ────────────── → note 4
├── Common failure modes ────────────────────────── → note 4
├── Escaped instance names (\032) ───────────────── → note 4
└── Related docs ────────────────────────────────── → (link-out)
bridge-protocol.md
├── Why it existed / Transport / Handshake + pairing → note 5 (oc_gateway_bridge_protocol)
├── Frames / Exec lifecycle events ──────────────── → note 5
├── Historical tailnet usage / Versioning ───────── → note 5
└── Related ─────────────────────────────────────── → (link-out)
cli-backends.md
├── Beginner-friendly quick start ───────────────── → note 6 (oc_gateway_cli_backends)
├── Using it as a fallback ──────────────────────── → note 6
├── Configuration overview (+ Example config H3) ── → note 6
├── Images (pass-through) / Inputs / outputs ────── → note 6
├── Limitations / Troubleshooting ───────────────── → note 6
├── How it works ────────────────────────────────── → note 7 (oc_gateway_cli_backends_internals)
├── Sessions / Fallback prelude from claude-cli ─── → note 7
├── Defaults / Plugin-owned defaults ────────────── → note 7
├── Native compaction ownership ─────────────────── → note 7
├── Bundle MCP overlays / Reseed history cap ────── → note 7
└── Related ─────────────────────────────────────── → (link-out)
config-agents.md
├── Agent defaults (H2, 6,197w — 6-way H3 split):
│   ├── workspace, repoRoot, skills, skip* flags ── → note 8 (…bootstrap_context)
│   ├── contextInjection, bootstrap*Chars,
│   │   per-agent bootstrap profile, truncation,
│   │   Context budget ownership map ────────────── → note 8
│   ├── imageMaxDimensionPx, imageQuality,
│   │   userTimezone, timeFormat ────────────────── → note 9 (…model_media)
│   ├── model, Runtime policy ───────────────────── → note 9
│   ├── cliBackends, promptOverlays ────────────── → note 10 (…backends_overlays)
│   ├── heartbeat, compaction, runRetries,
│   │   contextPruning, Block streaming,
│   │   Typing indicators, sandbox ──────────────── → note 11 (…runtime_resilience)
│   └── agents.list (per-agent overrides) ───────── → note 12 (…routing)
├── Multi-agent routing (Binding match fields,
│   Per-agent access profiles) ──────────────────── → note 12
├── Session ─────────────────────────────────────── → note 13 (…session_messages)
├── Messages (Response prefix, Ack reaction,
│   Inbound debounce, TTS) ──────────────────────── → note 13
├── Talk ────────────────────────────────────────── → note 13
└── Related ─────────────────────────────────────── → (link-out)
config-channels.md
├── Channels (H2):
│   ├── DM and group access ─────────────────────── → note 14 (oc_gateway_config_channels)
│   ├── Channel model overrides ─────────────────── → note 14
│   ├── Channel defaults and heartbeat ──────────── → note 14
│   ├── WhatsApp / Telegram / Discord / Google Chat → note 14
│   ├── Slack / Mattermost / Signal / iMessage ──── → note 14
│   ├── Matrix / Microsoft Teams / IRC ──────────── → note 14
│   ├── Multi-account / Other plugin channels ───── → note 14
│   ├── Group chat mention gating ───────────────── → note 15 (…routing_commands)
│   └── Commands (chat command handling) ────────── → note 15
└── Related ─────────────────────────────────────── → (link-out)
```
No orphaned sections. `## Related` blocks and intra-doc pointers (concepts/oauth, gateway/secrets, gateway/trusted-proxy-auth, auth-credential-semantics, provider pages, channel plugin pages) are link-outs to their home sub-plans, not duplicated content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| `config-agents.md` (8,129w, 41 fences, 6 H2 / 33 H3) | notes 8–13 (6 notes) | 3.25× the 2,500w cap; the dominant `Agent defaults` H2 alone is 6,197w/33 H3 keys. Split by config-key cluster (bootstrap/context · model/media/time · backends/overlays · runtime-resilience/sandbox · per-agent + multi-agent routing · session/messages/talk) so each note ≤750w, ≤6 fences, one procedural focus. |
| `config-channels.md` (5,362w, 20 fences, 2 H2 / 18 H3) | notes 14 + 15 | 2.14× the cap; separates per-channel transport configuration (the platform config blocks) from cross-channel routing behavior (group mention gating + chat-command handling), which is a distinct concern referenced by the channels sub-plans. |
| `cli-backends.md` (2,680w, 10 fences, 16 H2 / 1 H3) | notes 6 + 7 | Just over the 2,500w cap and mixes a user-facing setup/usage procedure with the internal mechanics (JSONL streaming loop, MCP loopback bridge, plugin-owned defaults, native-compaction ownership). Split per word-cap + BB-clarity (procedure vs concept). |

## Summary Statistics & Building Block Distribution

- Source pages: 7 (20,858 words). New `oc_` notes: **15**. New `term_dictionary` notes: **0** (expected).
- BB distribution: **procedure ×12** (notes 1, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15) · **concept ×2** (notes 2, 7) · **model ×1** (note 5).
- Est. digest words ~9,300 (avg ~620/note); every note ≤750w (well under the 2,500w cap). 99 source code fences distribute across the procedure/concept notes; each note kept ≤6 (config snippets reproduced selectively, verbatim from the mirror — `config-agents` 41 fences spread across 6 notes ≈ 6–7 source fences each, trimmed to the ≤6 most load-bearing per note).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_gateway_authentication (12t · 12s · 12d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway being authenticated to model providers; relevance: the whole page is OpenClaw's `models auth` flow.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization flow; relevance: subscription/OAuth provider logins are one of the two supported credential paths.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — access/refresh token pair; relevance: token expiry, refresh, and `tokenRef` SecretRefs are core to the auth store.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the page IS the model-provider authentication reference.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — per-agent stored credential record; relevance: OpenClaw reads `auth-profiles` from each agent's SQLite store (`openclaw-agent.sqlite`).
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — multi-key rotation set; relevance: `<PROVIDER>_API_KEYS` list + rate-limit key rotation is exactly a credential pool.
- [PKCE](../../term_dictionary/term_pkce.md) — proof-key OAuth extension; relevance: the OAuth login flow OpenClaw uses for ChatGPT/Codex/subscription providers.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: the Anthropic API-key / setup-token / Claude-CLI-reuse paths are documented in depth.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's coding CLI; relevance: `claude auth login` + `--method cli` reuse is the preferred Anthropic host path.
- [LLM](../../term_dictionary/term_llm.md) — the model class being authenticated; relevance: auth resolves the credential a model run uses.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external provider catalog; relevance: the provider set (OpenAI/Anthropic/Bedrock/OpenRouter…) the keys unlock.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: alternate-key retry triggers ONLY on rate-limit errors (429/quota/throttling).

**Docs**
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code auth overview; relevance: sibling coding-agent's credential-setup analog.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login/token-refresh debugging; relevance: mirrors OpenClaw's "No credentials" / expiring-token troubleshooting.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth + network error reference; relevance: same failure surface (expired token, missing key).
- [cc_amazon_bedrock_setup](../claude_code/cc_amazon_bedrock_setup.md) — Bedrock `aws-sdk` auth; relevance: OpenClaw's `auth: "aws-sdk"` Bedrock route is the same non-credential external-auth model.
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi subscription-vs-API-key + resolution order; relevance: closest Pi analog of credential precedence.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering provider creds; relevance: the `models.providers.<id>` endpoint metadata vs auth-store split.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — Hermes multi-key pool; relevance: direct analog of `<PROVIDER>_API_KEYS` rotation.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: `~/.openclaw/.env` + `<PROVIDER>_API_KEY` env inheritance analog.
- [hermes_subscription_proxy](../hermes_agent/hermes_subscription_proxy.md) — subscription-login proxy; relevance: the Claude-CLI / setup-token subscription path.
- [hermes_provider_minimax_oauth](../hermes_agent/hermes_provider_minimax_oauth.md) — provider OAuth login; relevance: per-provider named-profile OAuth login pattern.
- [oc_gateway_secrets](oc_gateway_secrets.md) — SecretRef env/file/exec providers (planned, this series, gw05); relevance: `keyRef`/`tokenRef` SecretRef-backed credentials.
- [oc_gateway_config_agents_model_media](oc_gateway_config_agents_model_media.md) — per-agent `model`/auth selection (planned, this series); relevance: the `model` block resolves against these credentials.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway credential resolution layer; relevance: implements `models auth`/`models status`.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/secrets subsystem; relevance: the auth-profile store + SecretRef resolution.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extensions; relevance: the provider whose keys this authenticates.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — analogous CLI auth; relevance: `/login`/`/logout` + provider-auth flows in the sibling ecosystem.

**Snippets**
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OpenClaw auth-profile OAuth portability; relevance: the auth-profile store this page documents.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profile; relevance: the `claude-cli` reuse credential path.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-order/credential selection; relevance: `auth.order.<provider>` precedence + `excluded_by_auth_order`.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — gateway credential/secret call path; relevance: how a run resolves the stored credential.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode helpers; relevance: auth mode selection at the gateway.
- [snippet_hermes_agent_core_auxiliary_auth_resolution](../../code_snippets/snippet_hermes_agent_core_auxiliary_auth_resolution.md) — auth resolution order; relevance: analog of the priority-order credential resolution.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source enumeration; relevance: env/profile/`models.json` source precedence.
- [snippet_hermes_agent_core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — multi-key pool seeding; relevance: `<PROVIDER>_API_KEYS` dedup + seed.
- [snippet_hermes_agent_core_credential_pool_selection](../../code_snippets/snippet_hermes_agent_core_credential_pool_selection.md) — rate-limit key rotation; relevance: retry-next-key on rate-limit errors.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — CLI login/logout; relevance: `models auth login`/`--force` analog.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: per-provider profile resolution.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — credential redaction; relevance: the auth store keeps credentials only / secret hygiene.

### oc_gateway_background_process (8t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway runtime; relevance: `exec`/`process` are OpenClaw gateway tools.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: `exec` runs inside the sandbox unless `elevated`.
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — the sandbox implementation; relevance: the backend the exec process runs under.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: `exec`/`process` are exposed to the agent as callable tools.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — tool catalog; relevance: registers/owns the `exec` and `process` tools.
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — sandboxed code-run tool; relevance: `exec` IS OpenClaw's code-execution tool.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: child-process bridging and MCP loopback feed gateway tools.
- [Kill Tree](../../term_dictionary/term_kill_tree.md) — process-tree termination; relevance: child-process bridge forwards termination signals to avoid orphaned processes.

**Docs**
- [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — Claude Code exec-tool behavior; relevance: direct analog of `exec` foreground/background semantics.
- [cc_dispatch_background_agents](../claude_code/cc_dispatch_background_agents.md) — background task dispatch; relevance: backgrounding + polling long-running work.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs elevated; relevance: the `elevated` flag and sandbox boundary.
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — shell/env execution context; relevance: `OPENCLAW_SHELL=exec`, `workdir`, `env` overrides.
- [hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md) — runtime exec tooling; relevance: analogous exec/process runtime tools.
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — terminal/PTY backends; relevance: `pty: true` TTY-backed sessions + send-keys/submit/paste.
- [hermes_tools_reference_core](../hermes_agent/hermes_tools_reference_core.md) — core tool reference; relevance: exec/process parameter reference analog.
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — custom-tool extension; relevance: how exec-like tools are exposed.
- [oc_gateway_cli_backends_internals](oc_gateway_cli_backends_internals.md) — child-process + MCP loopback bridge (planned, this series); relevance: the bridge helper that detaches listeners on exit.
- [oc_gateway_config_agents_runtime_resilience](oc_gateway_config_agents_runtime_resilience.md) — `sandbox` execution policy (planned, this series); relevance: the sandbox policy `exec` honors.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime spawning child processes; relevance: owns `exec`/`process`.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: `process` is scoped per agent.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session layer; relevance: tracks backgrounded sessions in memory.

**Snippets**
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — OpenClaw exec orchestration; relevance: the `exec` tool's foreground/background orchestration.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervision; relevance: backgrounded-session lifecycle in memory.
- [snippet_openclaw_process_windows_cmd_shim](../../code_snippets/snippet_openclaw_process_windows_cmd_shim.md) — cross-platform shell shim; relevance: shell/profile rules per platform.
- [snippet_openclaw_security_openshell_cli](../../code_snippets/snippet_openclaw_security_openshell_cli.md) — openshell exec entry; relevance: shell command execution surface.
- [snippet_openclaw_gateway_shutdown_forensics](../../code_snippets/snippet_hermes_agent_gw_shutdown_forensics.md) — shutdown/orphan forensics; relevance: child-process bridge avoiding orphaned processes on shutdown.
- [snippet_hermes_agent_tools_process_register](../../code_snippets/snippet_hermes_agent_tools_process_register.md) — process-tool registration; relevance: `process` actions (list/poll/log/write/kill) analog.
- [snippet_hermes_agent_tools_process_cleanup](../../code_snippets/snippet_hermes_agent_tools_process_cleanup.md) — process cleanup/TTL; relevance: `cleanupMs`/finished-session reaping.
- [snippet_hermes_agent_tools_terminal_exec](../../code_snippets/snippet_hermes_agent_tools_terminal_exec.md) — terminal exec; relevance: foreground exec returning output.
- [snippet_hermes_agent_tools_terminal_bg](../../code_snippets/snippet_hermes_agent_tools_terminal_bg.md) — backgrounded terminal; relevance: `background: true` / `yieldMs` auto-background.
- [snippet_hermes_agent_core_shell_hooks_callback](../../code_snippets/snippet_hermes_agent_core_shell_hooks_callback.md) — shell hook callbacks; relevance: `notifyOnExit` system-event enqueue on exit.
- [snippet_hermes_agent_tools_code_exec_result](../../code_snippets/snippet_hermes_agent_tools_code_exec_result.md) — exec result handling; relevance: exit code/output/`status: running` result shape.

### oc_gateway_bonjour (10t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being discovered; relevance: only the Gateway advertises `_openclaw-gw._tcp`.
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — mDNS/DNS-SD discovery; relevance: the page IS OpenClaw's Bonjour discovery reference.
- [DNS](../../term_dictionary/term_dns.md) — name resolution; relevance: Unicast DNS-SD over a CoreDNS server + split DNS.
- [DNS Delegation](../../term_dictionary/term_dns_delegation.md) — zone delegation; relevance: serving `_openclaw-gw._tcp` under a dedicated zone (`openclaw.internal.`).
- [WebSocket](../../term_dictionary/term_websocket.md) — the discovered endpoint; relevance: Bonjour discovers the Gateway WS endpoint (port 18789).
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — fingerprint pinning; relevance: `gatewayTlsSha256` TXT hint MUST NOT override a stored pin.
- [Access Control](../../term_dictionary/term_access_control.md) — listener security; relevance: bind mode + auth on advertised services.
- [SSH](../../term_dictionary/term_ssh.md) — secure tunnel; relevance: `sshPort` TXT hint + SSH as the non-discovery connectivity fallback.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — feature/mode hints; relevance: `discovery.mdns.mode` minimal/full TXT-hint negotiation.

**Docs**
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote/dashboard reachability; relevance: bind/remote-access analog of gateway listener exposure.
- [hermes_desktop_remote_backend](../hermes_agent/hermes_desktop_remote_backend.md) — remote backend connect; relevance: cross-network gateway connectivity analog.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — listener isolation; relevance: keeping the listener auth-protected.
- [band_a2a_gateway](../band/band_a2a_gateway.md) — agent-to-agent gateway; relevance: gateway-as-discovered-service analog.
- [band_connect_remote_agent](../band/band_connect_remote_agent.md) — remote agent connection; relevance: connecting to a discovered remote gateway.
- [pi_containerization](../pi/pi_containerization.md) — container networking; relevance: Docker bridge / container discovery constraints (mirrored in note 4).
- [oc_gateway_bonjour_troubleshooting](oc_gateway_bonjour_troubleshooting.md) — debugging this setup (planned, this series); relevance: the troubleshooting half.
- [oc_gateway_bridge_protocol](oc_gateway_bridge_protocol.md) — historical tailnet transport (planned, this series); relevance: Bonjour-on-LAN vs tailnet bridge history.
- [oc_gateway_tailscale](oc_gateway_tailscale.md) — Tailscale split-DNS setup (planned, this series, gw06); relevance: the tailnet layer wide-area DNS-SD rides on.
- [oc_gateway_discovery](oc_gateway_discovery.md) — discovery policy/transport selection (planned, this series, gw02); relevance: the `## Related docs` discovery-policy pointer.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway that advertises; relevance: owns wide-area DNS-SD publishing + the ciao advertiser.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — listener security; relevance: bind mode + TLS pinning policy.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — node/app discovery consumers; relevance: iOS/Android nodes browse `_openclaw-gw._tcp`.

**Snippets**
- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — Android mDNS browse; relevance: node-side `_openclaw-gw._tcp` discovery.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — gateway beacon broadcast; relevance: what the Gateway advertises (role/displayName/TXT keys).
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway server methods; relevance: discovery/listener server-side wiring.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect/resolve; relevance: routing to the resolved service endpoint (SRV+A/AAAA) not TXT.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client TLS identity; relevance: TLS-only direct connects + fingerprint confirmation.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection setup; relevance: the WS endpoint Bonjour resolves to.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android WS session; relevance: node connecting to the discovered gateway.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — kit WS channel; relevance: node-kit transport over the discovered endpoint.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS pairing; relevance: iOS `NWBrowser` discovery → pairing.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — listener auth at startup; relevance: keeping auth enabled on the bound listener.
- [snippet_hermes_agent_gw_platform_homeassistant](../../code_snippets/snippet_hermes_agent_gw_platform_homeassistant.md) — LAN service integration; relevance: LAN-service discovery/integration analog.

### oc_gateway_bonjour_troubleshooting (9t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being debugged; relevance: the troubleshooting target.
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — mDNS/DNS-SD; relevance: the discovery mechanism whose failures this debugs.
- [DNS](../../term_dictionary/term_dns.md) — name resolution; relevance: `dns-sd -B`/`dig` debugging + resolver issues.
- [Sandbox](../../term_dictionary/term_sandbox.md) — container isolation; relevance: Docker bridge / container network isolation is a documented failure cause.
- [WebSocket](../../term_dictionary/term_websocket.md) — the reachable endpoint; relevance: `curl /healthz` direct-port check when Bonjour is down.
- [Access Control](../../term_dictionary/term_access_control.md) — bind/network policy; relevance: LAN policy / multicast-blocked Wi-Fi failure modes.
- [SSH](../../term_dictionary/term_ssh.md) — fallback tunnel; relevance: SSH tunnel as the direct route when Bonjour is disabled.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — discovery mode; relevance: forced-on/forced-off/auto Bonjour modes.

**Docs**
- [hermes_install_windows_wsl2](../hermes_agent/hermes_install_windows_wsl2.md) — WSL networking; relevance: WSL is a documented mDNS-multicast-drop environment.
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — Docker runtime; relevance: Docker bridge networking gotchas.
- [pi_containerization](../pi/pi_containerization.md) — container networking; relevance: container mDNS multicast forwarding constraints.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — direct/remote reachability; relevance: the published-URL direct route when discovery fails.
- [hermes_faq_messaging_perf_profiles_workflows](../hermes_agent/hermes_faq_messaging_perf_profiles_workflows.md) — operational FAQ/troubleshooting; relevance: failure-mode triage analog.
- [band_connect_remote_agent](../band/band_connect_remote_agent.md) — remote connect fallback; relevance: connecting without LAN discovery.
- [oc_gateway_bonjour](oc_gateway_bonjour.md) — the setup it debugs (planned, this series); relevance: the configuration page this troubleshoots.
- [oc_gateway_diagnostics](oc_gateway_diagnostics.md) — gateway diagnostics (planned, this series, gw02); relevance: diagnostic tooling for discovery faults.
- [oc_gateway_doctor](oc_gateway_doctor.md) — `openclaw doctor` (planned, this series, gw02); relevance: doctor health checks for discovery.
- [oc_gateway_logging](oc_gateway_logging.md) — gateway logging (planned, this series, gw03); relevance: reading `bonjour:` lines in the rolling log.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — discovery diagnostics + watchdog; relevance: ciao advertiser retry/disable logic.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — listener/bind security; relevance: bind mode interactions with discovery.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — iOS/Android node apps; relevance: node-side discovery debug logs.

**Snippets**
- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — Android mDNS browse; relevance: node-side discovery that fails when multicast is blocked.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — advertiser shutdown/cancel; relevance: "suppressing ciao cancellation" log line.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — beacon broadcast; relevance: advertise-failed / name-conflict states.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — server methods; relevance: discovery server wiring under fault.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect fallback; relevance: direct/proxy route when Bonjour disabled.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android WS session; relevance: falling back to direct WS host:port.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: the reachable endpoint behind discovery.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS discovery/pairing; relevance: iOS discovery-debug-logs flow.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — TLS identity on direct connect; relevance: first-time fingerprint confirmation when bypassing discovery.
- [snippet_hermes_agent_gw_shutdown_forensics](../../code_snippets/snippet_hermes_agent_gw_shutdown_forensics.md) — shutdown forensics; relevance: diagnosing stuck advertiser / restart loops.
- [snippet_hermes_agent_gw_platform_homeassistant](../../code_snippets/snippet_hermes_agent_gw_platform_homeassistant.md) — LAN integration debugging; relevance: LAN-service reachability triage analog.

### oc_gateway_bridge_protocol (10t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: the bridge was OpenClaw's legacy node transport.
- [WebSocket](../../term_dictionary/term_websocket.md) — the successor transport; relevance: current clients use the WS Gateway Protocol that replaced the bridge.
- [WebSocket Framing](../../term_dictionary/term_websocket_framing.md) — frame structure; relevance: the bridge's JSONL frame format (`req`/`res`/`event`/`invoke`).
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC framing; relevance: scoped gateway RPC over the bridge.
- [RPC](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: the `req`/`res` scoped RPC surface.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — modern agent protocol; relevance: the protocol family that superseded the bridge.
- [TLS](../../term_dictionary/term_tls.md) — transport security; relevance: optional `bridge.tls.enabled` + `bridgeTls`/`bridgeTlsSha256` TXT hints.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — version handshake; relevance: the bridge was implicit-v1 with no min/max negotiation.
- [Function Calling](../../term_dictionary/term_function_calling.md) — exec/tool invocation; relevance: `exec.finished`/`exec.denied` exec-lifecycle events the bridge carried.

**Docs**
- [hermes_acp_internals](../hermes_agent/hermes_acp_internals.md) — ACP internals; relevance: the successor protocol's frame/session model.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway protocol internals; relevance: handshake/pairing/RPC analog.
- [band_websocket_overview](../band/band_websocket_overview.md) — WS protocol overview; relevance: the WS control plane that replaced the bridge.
- [band_a2a_overview](../band/band_a2a_overview.md) — agent-to-agent protocol; relevance: scoped-RPC + event framing analog.
- [band_a2a_adapter](../band/band_a2a_adapter.md) — A2A adapter; relevance: invoke/invoke-res node command analog.
- [pi_rpc_events](../pi/pi_rpc_events.md) — RPC event stream; relevance: `event` frames (transcript, agent request, exec lifecycle).
- [oc_gateway_protocol](oc_gateway_protocol.md) — current WS Gateway Protocol (planned, this series, gw05); relevance: the replacement this page redirects to.
- [oc_gateway_background_process](oc_gateway_background_process.md) — exec lifecycle events (planned, this series); relevance: `exec.finished`/`system.run` events the bridge surfaced.
- [oc_gateway_bonjour](oc_gateway_bonjour.md) — historical tailnet/Bonjour usage (planned, this series); relevance: bridge `bind: tailnet` + Bonjour-on-LAN history.
- [oc_gateway_pairing](oc_gateway_pairing.md) — node pairing/approvals (planned, this series, gw04); relevance: the `pair-request`/`pair-ok` handshake.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway protocol layer; relevance: hosted the removed `server-bridge.ts` allowlist.

**Snippets**
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: the `req`/`res` scoped-RPC frame shape.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method allowlist gating; relevance: the bridge's small-allowlist security boundary.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: `hello`/`pair-request`/`pair-ok` handshake.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS pairing; relevance: per-node token pairing client-side.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — TLS identity; relevance: optional bridge TLS + non-secret fingerprint hint.
- [snippet_openclaw_android_invoke_dispatcher](../../code_snippets/snippet_openclaw_android_invoke_dispatcher.md) — node invoke dispatch; relevance: `invoke`/`invoke-res` node commands (`canvas.*`, `camera.*`).
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session; relevance: node→gateway session over the transport.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: the WS transport replacing TCP JSONL.
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP server; relevance: the modern protocol server.

### oc_gateway_cli_backends (11t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: CLI backends are an OpenClaw fallback subsystem.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the claude-cli backend; relevance: the bundled default CLI backend.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model; relevance: `claude-cli/claude-sonnet-4-6` model refs.
- [LLM](../../term_dictionary/term_llm.md) — the model class; relevance: CLI backends are a text-only model path.
- [Model Failover](../../term_dictionary/term_model_failover.md) — fallback routing; relevance: CLI backends run only when primary models fail.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — fallback model entry; relevance: added to `agents.defaults.model.fallbacks`.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: `bundleMcp: true` loopback MCP tool bridge.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider-owning plugin; relevance: bundled plugin registers the default backend.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — provider-prefix routing; relevance: `<provider>/<model>` model ref selects the backend.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — provider set; relevance: the providers CLI backends back up.
- [Structured Output](../../term_dictionary/term_structured_output.md) — JSON output parsing; relevance: `output: json`/`jsonl`/`text` parsing modes.

**Docs**
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — fallback-model routing; relevance: direct analog of the CLI-backend-as-fallback config.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — gateway-fronted model access; relevance: CLI backend as a gateway-managed model path.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — fallback provider list; relevance: `model.fallbacks` ladder analog.
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — local CLI/terminal backends; relevance: running local AI CLIs as backends.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — provider runtime; relevance: how a backend is invoked at runtime.
- [hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md) — Codex CLI runtime; relevance: Codex harness path (vs the removed bundled `codex-cli`).
- [pi_provider_auth](../pi/pi_provider_auth.md) — CLI/provider auth prerequisite; relevance: `claude auth login` before backend use.
- [oc_gateway_cli_backends_internals](oc_gateway_cli_backends_internals.md) — the internals half (planned, this series); relevance: JSONL loop + MCP bridge mechanics.
- [oc_gateway_config_agents_backends_overlays](oc_gateway_config_agents_backends_overlays.md) — the `cliBackends` config block (planned, this series); relevance: where backends are configured.
- [oc_gateway_authentication](oc_gateway_authentication.md) — Claude-CLI auth setup (planned, this series); relevance: the host login the backend requires.
- [oc_concepts_model_failover](oc_concepts_model_failover.md) — failover concept (planned, this series, co04); relevance: the failover model this backs.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway invoking CLI backends; relevance: spawns the CLI per model ref.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: builds the system prompt + workspace context for the CLI.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extensions; relevance: bundled plugins owning `claude-cli`/`google-gemini-cli` defaults.

**Snippets**
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: `primary`+`fallbacks` ordering CLI backends sit in.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error classification; relevance: try-CLI-backend-next on primary auth/rate/timeout failure.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — provider/backend registration; relevance: provider-prefix → backend resolution.
- [snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — fallback activation; relevance: switching to the fallback candidate.
- [snippet_hermes_agent_core_error_classifier_provider_maps](../../code_snippets/snippet_hermes_agent_core_error_classifier_provider_maps.md) — error classification; relevance: which errors trigger fallback.
- [snippet_hermes_agent_tools_terminal_exec](../../code_snippets/snippet_hermes_agent_tools_terminal_exec.md) — terminal-backed exec; relevance: executing the local CLI process.
- [snippet_hermes_agent_core_codex_runtime](../../code_snippets/snippet_hermes_agent_core_codex_runtime.md) — Codex runtime; relevance: Codex harness path vs CLI backend.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — CLI install/setup; relevance: ensuring the `claude`/`gemini` binary on PATH.
- [snippet_hermes_agent_cli_models_normalize](../../code_snippets/snippet_hermes_agent_cli_models_normalize.md) — model-ref normalization; relevance: `modelAliases` mapping `provider/model` → CLI model.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: registered backend id → provider prefix.
- [snippet_hermes_agent_tools_code_exec_languages](../../code_snippets/snippet_hermes_agent_tools_code_exec_languages.md) — exec output handling; relevance: parsing CLI stdout (json/text).
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — image/path passthrough I/O; relevance: passing image paths/args to the CLI.

### oc_gateway_cli_backends_internals (11t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: the internal JSONL loop + MCP bridge are OpenClaw machinery.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the loopback HTTP MCP server exposing gateway tools.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript summarization; relevance: `ownsNativeCompaction` opt-out so OpenClaw doesn't fight the backend.
- [Context Compression](../../term_dictionary/term_context_compression.md) — context shrinking; relevance: reseed from compaction summary + post-boundary tail.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool injection; relevance: gateway tools reach the CLI only via bundle MCP, not direct calls.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness runtime; relevance: native-harness sessions (Codex) route to their harness compaction endpoint.
- [LLM](../../term_dictionary/term_llm.md) — the model; relevance: the CLI-backed model whose session is reused.
- [Claude Code](../../term_dictionary/term_claude_code.md) — claude-cli; relevance: warm stdio session, `--resume`, native skill resolver.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — owning plugin; relevance: plugin-owned defaults via `registerCliBackend`.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — prompt reuse; relevance: prompt-build + reseed-cap context economy.
- [Append-Only State](../../term_dictionary/term_append_only_state.md) — JSONL transcript; relevance: parsing Claude Code's local JSONL transcript at `~/.claude/projects/`.

**Docs**
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — gateway-fronted access internals; relevance: gateway-managed model session analog.
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — fallback prelude; relevance: seeding the next attempt on failover.
- [hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md) — native harness runtime; relevance: harness-owned compaction routing.
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — terminal backend internals; relevance: stdio process kept alive per session.
- [hermes_use_mcp_guide](../hermes_agent/hermes_use_mcp_guide.md) — MCP usage; relevance: the loopback MCP config overlay.
- [pi_compaction](../pi/pi_compaction.md) — compaction mechanics; relevance: native vs safeguard compaction.
- [pi_compaction_extensions](../pi/pi_compaction_extensions.md) — compaction extension hooks; relevance: per-backend compaction ownership.
- [oc_gateway_cli_backends](oc_gateway_cli_backends.md) — the setup half (planned, this series); relevance: the user-facing config this implements.
- [oc_gateway_background_process](oc_gateway_background_process.md) — child-process + MCP bridge (planned, this series); relevance: the bridge helper + loopback server lifecycle.
- [oc_concepts_compaction](oc_concepts_compaction.md) — compaction concept (planned, this series, co02); relevance: the compaction model `ownsNativeCompaction` opts out of.
- [oc_gateway_config_agents_runtime_resilience](oc_gateway_config_agents_runtime_resilience.md) — `compaction` config (planned, this series); relevance: the compaction settings this interacts with.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway internals; relevance: loopback MCP server + session FS scan.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: prompt build + compaction path.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session layer; relevance: stored CLI session-id reuse + reset semantics.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extensions; relevance: plugin-owned backend defaults + dialects.

**Snippets**
- [snippet_openclaw_gateway_session_fs_transcript_candidate_scan](../../code_snippets/snippet_openclaw_gateway_session_fs_transcript_candidate_scan.md) — transcript candidate scan; relevance: verifying a stored session against a readable transcript before resume.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction identifier handoff; relevance: native-compaction ownership routing.
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction chunk safety; relevance: bounded reseed / safeguard summarizer behavior.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — session compact/reset; relevance: `/reset` cuts CLI sessions, daily reset doesn't.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — provider/backend internals; relevance: backend selection by provider prefix.
- [snippet_hermes_agent_core_conversation_compression_entry](../../code_snippets/snippet_hermes_agent_core_conversation_compression_entry.md) — compression entry; relevance: when the safeguard summarizer fires.
- [snippet_hermes_agent_core_conversation_compression_strategy](../../code_snippets/snippet_hermes_agent_core_conversation_compression_strategy.md) — compression strategy; relevance: summary + post-boundary tail reseed.
- [snippet_hermes_agent_core_codex_runtime](../../code_snippets/snippet_hermes_agent_core_codex_runtime.md) — Codex native runtime; relevance: native-harness compaction endpoint.
- [snippet_hermes_agent_core_chat_helpers_max_iter](../../code_snippets/snippet_hermes_agent_core_chat_helpers_max_iter.md) — output-limit guards; relevance: bounded JSONL output (`maxTurnRawChars`/`maxTurnLines`).

### oc_gateway_config_agents_bootstrap_context (10t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `agents.defaults` is OpenClaw config.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: bootstrap char caps protect the context window.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — context curation; relevance: `contextInjection` + bootstrap budget ownership map.
- [Context Engine](../../term_dictionary/term_context_engine.md) — context assembly subsystem; relevance: assembles workspace/skills/memory into the prompt.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness runtime; relevance: the agent bootstrapped from workspace/repoRoot/skills.
- [Skills](../../term_dictionary/term_skills.md) — agent capabilities; relevance: `agents.defaults.skills` loaded at bootstrap.
- [Skills Hub](../../term_dictionary/term_skills_hub.md) — skill catalog/source; relevance: where bootstrap skills are sourced.
- [Progressive Disclosure](../../term_dictionary/term_progressive_disclosure.md) — staged context loading; relevance: bootstrap char budgets + truncation warning.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript shrink; relevance: the budget the context-injection map coordinates with.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — prompt reuse; relevance: bootstrap content economy across runs.

**Docs**
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — workspace/env config; relevance: `workspace`/`repoRoot` analog.
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — token economy; relevance: `bootstrapMaxChars`/`bootstrapTotalMaxChars` budgets.
- [cc_skill_dynamic_context_and_subagent](../claude_code/cc_skill_dynamic_context_and_subagent.md) — skills + dynamic context; relevance: `skills` + `contextInjection` analog.
- [hermes_context_references](../hermes_agent/hermes_context_references.md) — context reference injection; relevance: `contextInjection` mechanics analog.
- [hermes_context_files](../hermes_agent/hermes_context_files.md) — context files; relevance: bootstrap files (`skipOptionalBootstrapFiles`).
- [hermes_prompt_assembly](../hermes_agent/hermes_prompt_assembly.md) — prompt assembly; relevance: how bootstrap content + budget assemble the prompt.
- [hermes_runtime_context_settings](../hermes_agent/hermes_runtime_context_settings.md) — runtime context settings; relevance: the context-budget ownership map analog.
- [oc_gateway_config_agents_model_media](oc_gateway_config_agents_model_media.md) — sibling config cluster (planned, this series); relevance: prev/next in the config-agents split.
- [oc_concepts_context](oc_concepts_context.md) — context concept (planned, this series, co02); relevance: the context model the budget protects.
- [oc_concepts_agent_workspace](oc_concepts_agent_workspace.md) — agent workspace concept (planned, this series, co01); relevance: `workspace`/`repoRoot` semantics.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent-defaults consumer; relevance: applies workspace/bootstrap/context config.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: hosts the agent-defaults config.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: skills loaded at bootstrap.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: memory/context injected into bootstrap.

**Snippets**
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap char budgeting; relevance: `bootstrapMaxChars`/`bootstrapTotalMaxChars` enforcement.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — context injection; relevance: the `contextInjection` mechanism.
- [snippet_openclaw_agents_context_lookup](../../code_snippets/snippet_openclaw_agents_context_lookup.md) — context lookup; relevance: resolving injected context sources.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — system-prompt modes; relevance: bootstrap-skip flags shaping the prompt.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — cached prompt sections; relevance: bootstrap content cached across runs.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — context loaders; relevance: per-source context loading + budget.
- [snippet_hermes_agent_core_prompt_builder_subscription_truncate](../../code_snippets/snippet_hermes_agent_core_prompt_builder_subscription_truncate.md) — prompt truncation; relevance: `bootstrapPromptTruncationWarning`.
- [snippet_hermes_agent_core_prompt_builder_skills_snapshot](../../code_snippets/snippet_hermes_agent_core_prompt_builder_skills_snapshot.md) — skills snapshot; relevance: snapshotting selected skills into the prompt.

### oc_gateway_config_agents_model_media (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: the `model`/media config is OpenClaw `agents.defaults`.
- [LLM](../../term_dictionary/term_llm.md) — the model; relevance: the `model` selection block.
- [Claude](../../term_dictionary/term_claude.md) — model family; relevance: example `primary`/alias entries.
- [Model Router](../../term_dictionary/term_model_router.md) — selection/routing; relevance: `model.primary`/`fallbacks`/aliases routing.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — available-model set; relevance: `agents.defaults.models` allowlist.
- [Model Failover](../../term_dictionary/term_model_failover.md) — fallback routing; relevance: the `model.fallbacks` ladder.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — provider resolution; relevance: `<provider>/<model>` ref resolution.
- [Inference Profile](../../term_dictionary/term_inference_profile.md) — model runtime profile; relevance: per-agent model/runtime selection.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — provider set; relevance: the selectable provider catalog.
- [Computer Vision](../../term_dictionary/term_computer_vision.md) — image handling; relevance: `imageMaxDimensionPx`/`imageQuality` media config.

**Docs**
- [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: the `model` block analog.
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — fallback models; relevance: `model.fallbacks` analog.
- [cc_restrict_model_selection](../claude_code/cc_restrict_model_selection.md) — model allowlist; relevance: `agents.defaults.models` allowlist analog.
- [pi_custom_models](../pi/pi_custom_models.md) — custom-model/alias config; relevance: `modelAliases` + alias config.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — per-model overrides; relevance: per-model entry overrides under `models`.
- [hermes_configuring_models_dashboard](../hermes_agent/hermes_configuring_models_dashboard.md) — model configuration; relevance: configuring primary/fallback/alias.
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog; relevance: the model-id catalog selectable.
- [oc_gateway_config_agents_bootstrap_context](oc_gateway_config_agents_bootstrap_context.md) — prev config cluster (planned, this series); relevance: prev/next in the config-agents split.
- [oc_gateway_authentication](oc_gateway_authentication.md) — the `model` block's credentials (planned, this series); relevance: auth resolves the model's credential.
- [oc_concepts_models](oc_concepts_models.md) — models concept (planned, this series, co04); relevance: the model abstraction this configures.
- [oc_concepts_model_failover](oc_concepts_model_failover.md) — failover concept (planned, this series, co04); relevance: the `fallbacks` behavior.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — model-selection consumer; relevance: applies the `model` block.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider registry; relevance: resolves `<provider>/<model>` refs.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: hosts the agent-defaults model config.

**Snippets**
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — fallback ladder; relevance: `primary`+`fallbacks` ordering.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — model cooldown; relevance: model-scoped rate-limit cooldown in selection.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — provider resolution; relevance: provider-prefix → model resolution.
- [snippet_hermes_agent_cli_model_switch_swap](../../code_snippets/snippet_hermes_agent_cli_model_switch_swap.md) — model switch; relevance: `/model` selection / per-session pin analog.
- [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — model-switch entry; relevance: alias-or-id selection.
- [snippet_hermes_agent_cli_models_normalize](../../code_snippets/snippet_hermes_agent_cli_models_normalize.md) — model-ref normalization; relevance: alias → canonical model id.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: provider set the model resolves against.
- [snippet_hermes_agent_core_auxiliary_normalization](../../code_snippets/snippet_hermes_agent_core_auxiliary_normalization.md) — model/config normalization; relevance: normalizing the `model` block.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — image/vision dispatch; relevance: `imageMaxDimensionPx`/`imageQuality` handling.
- [snippet_hermes_agent_tools_vision_input](../../code_snippets/snippet_hermes_agent_tools_vision_input.md) — image input; relevance: image dimension/quality on input media.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image generation dispatch; relevance: image media config path.

### oc_gateway_config_agents_backends_overlays (9t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `cliBackends`/`promptOverlays` are OpenClaw `agents.defaults`.
- [Model Failover](../../term_dictionary/term_model_failover.md) — fallback config; relevance: `cliBackends` define the fallback CLI providers.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — fallback entry; relevance: CLI backends added as fallbacks.
- [Claude Code](../../term_dictionary/term_claude_code.md) — claude-cli; relevance: the default `cliBackends` entry.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — owning plugin; relevance: plugin-owned backend defaults overridden here.
- [LLM](../../term_dictionary/term_llm.md) — the model; relevance: backends provide a text-only model path.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — prompt reuse; relevance: `promptOverlays` modify cached prompt fragments.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — prompt design; relevance: `promptOverlays` inject/override prompt fragments.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness runtime; relevance: the runtime the overlays/backends configure.

**Docs**
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — fallback config; relevance: `cliBackends` fallback analog.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — gateway-managed backends; relevance: backend config surface analog.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — fallback providers; relevance: the fallback list `cliBackends` populate.
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — terminal/CLI backends; relevance: the `cliBackends` config target.
- [hermes_prompt_assembly](../hermes_agent/hermes_prompt_assembly.md) — prompt assembly; relevance: where `promptOverlays` are applied.
- [hermes_plugin_extensions_hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — plugin/extension hooks; relevance: plugin-owned backend defaults.
- [oc_gateway_cli_backends](oc_gateway_cli_backends.md) — the `cliBackends` target (planned, this series); relevance: the backend subsystem this configures.
- [oc_gateway_config_agents_bootstrap_context](oc_gateway_config_agents_bootstrap_context.md) — prompt/context overlap (planned, this series); relevance: overlays interact with context injection.
- [oc_reference_templates_bootstrap](oc_reference_templates_bootstrap.md) — prompt templates (planned, this series, rf03/rf04); relevance: the BOOT/CLAUDE/SOUL templates overlays modify.
- [oc_concepts_model_failover](oc_concepts_model_failover.md) — failover concept (planned, this series, co04); relevance: the failover `cliBackends` serve.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — config consumer; relevance: applies `cliBackends`/`promptOverlays`.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: hosts the config + prompt subsystem.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — CLI-backend plugins; relevance: registers plugin-owned backend defaults.

**Snippets**
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — fallback ladder; relevance: where `cliBackends` slot into fallbacks.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — prompt modes; relevance: `promptOverlays` shaping the prompt.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — prompt context injection; relevance: overlay fragments injected into the prompt.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — cached prompt sections; relevance: overlays modifying cached sections.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — provider/backend registration; relevance: `cliBackends.<id>` provider id.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error path; relevance: when configured `cliBackends` activate.
- [snippet_hermes_agent_core_prompt_builder_context_helpers](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_helpers.md) — prompt builder helpers; relevance: applying overlay text transforms.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — context loaders; relevance: overlay fragments as loaded context.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: backend id → provider prefix.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — backend setup; relevance: configuring the `command` path for a CLI backend.
- [snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — fallback activation; relevance: activating a configured CLI backend.

### oc_gateway_config_agents_runtime_resilience (11t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: runtime-resilience knobs are OpenClaw `agents.defaults`.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — liveness signal; relevance: the `heartbeat` config block.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript shrink; relevance: the `compaction` config block.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: `contextPruning` keeps runs within the window.
- [Context Compression](../../term_dictionary/term_context_compression.md) — context shrink; relevance: pruning/compaction interplay.
- [Sandbox](../../term_dictionary/term_sandbox.md) — execution boundary; relevance: the `sandbox` execution-policy block.
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — sandbox impl; relevance: the backend `sandbox` policy selects.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool execution; relevance: sandbox governs tool/exec runs.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: `runRetries` + rate-limit recovery.
- [Failover](../../term_dictionary/term_failover.md) — retry/recovery; relevance: run retries on transient failures.
- [Structured Output](../../term_dictionary/term_structured_output.md) — streamed output; relevance: block streaming + typing indicators presentation.

**Docs**
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — runtime/execution policy; relevance: `sandbox` execution-policy analog.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandbox runtime; relevance: the `sandbox` policy + container execution.
- [cc_agent_sdk_context_window](../claude_code/cc_agent_sdk_context_window.md) — context-window mgmt; relevance: `contextPruning`/compaction budgeting.
- [pi_compaction](../pi/pi_compaction.md) — compaction; relevance: the `compaction` block analog.
- [pi_sessions](../pi/pi_sessions.md) — session runtime; relevance: heartbeat/streaming over a session.
- [hermes_runtime_context_settings](../hermes_agent/hermes_runtime_context_settings.md) — runtime settings; relevance: heartbeat/retry/pruning settings analog.
- [hermes_event_hooks](../hermes_agent/hermes_event_hooks.md) — runtime event hooks; relevance: heartbeat/typing lifecycle events.
- [oc_gateway_cli_backends_internals](oc_gateway_cli_backends_internals.md) — native compaction (planned, this series); relevance: `ownsNativeCompaction` interplay with `compaction`.
- [oc_concepts_retry](oc_concepts_retry.md) — retry concept (planned, this series, co06); relevance: `runRetries` semantics.
- [oc_concepts_streaming](oc_concepts_streaming.md) — streaming concept (planned, this series, co07); relevance: block streaming behavior.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — runtime-resilience consumer; relevance: applies heartbeat/compaction/retry/pruning.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: streaming/heartbeat delivery layer.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session layer; relevance: streaming + pruning over a session.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — sandbox security; relevance: the `sandbox` policy enforcement.

**Snippets**
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — chat heartbeat/buffered delta; relevance: the `heartbeat` + block-streaming delivery.
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction chunk safety; relevance: the `compaction` block behavior.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction handoff; relevance: compaction-ownership routing.
- [snippet_openclaw_gateway_session_utils_title_runtime](../../code_snippets/snippet_openclaw_gateway_session_utils_title_runtime.md) — session runtime utils; relevance: streaming/typing-indicator session state.
- [snippet_hermes_agent_core_conversation_loop_retry_handler](../../code_snippets/snippet_hermes_agent_core_conversation_loop_retry_handler.md) — retry handler; relevance: `runRetries` retry loop.
- [snippet_hermes_agent_core_conversation_loop_retry_sleep](../../code_snippets/snippet_hermes_agent_core_conversation_loop_retry_sleep.md) — retry backoff sleep; relevance: retry pacing.
- [snippet_hermes_agent_core_conversation_loop_rate_limit_recovery](../../code_snippets/snippet_hermes_agent_core_conversation_loop_rate_limit_recovery.md) — rate-limit recovery; relevance: retries on rate-limit.
- [snippet_hermes_agent_core_retry_utils](../../code_snippets/snippet_hermes_agent_core_retry_utils.md) — retry utilities; relevance: bounded-retry helpers.
- [snippet_hermes_agent_core_chat_helpers_streaming_loop](../../code_snippets/snippet_hermes_agent_core_chat_helpers_streaming_loop.md) — streaming loop; relevance: block-streaming output.
- [snippet_hermes_agent_core_chat_helpers_interruptible_call](../../code_snippets/snippet_hermes_agent_core_chat_helpers_interruptible_call.md) — interruptible call; relevance: streaming + heartbeat interruption.
- [snippet_hermes_agent_core_conversation_loop_length_recovery](../../code_snippets/snippet_hermes_agent_core_conversation_loop_length_recovery.md) — length recovery; relevance: `contextPruning` on overflow.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — sandboxed exec; relevance: the `sandbox` execution policy in action.

### oc_gateway_config_agents_routing (10t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `agents.list` + multi-agent routing are OpenClaw config.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multi-agent system; relevance: routing inbound messages across multiple agents.
- [Multi-Agent Collaboration](../../term_dictionary/term_multi_agent_collaboration.md) — agent cooperation; relevance: per-agent routing/access profiles.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — orchestration; relevance: binding match fields selecting the agent.
- [Agent Card](../../term_dictionary/term_agent_card.md) — agent descriptor; relevance: per-agent identity/overrides in `agents.list`.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned child agent; relevance: per-agent overrides + spawn policy.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — thread→agent binding; relevance: binding match fields route a thread to an agent.
- [Access Control](../../term_dictionary/term_access_control.md) — access profiles; relevance: per-agent access profiles.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: the per-agent runtime being overridden.
- [Bot](../../term_dictionary/term_bot.md) — chat bot; relevance: inbound chat messages routed to an agent.

**Docs**
- [hermes_messaging_slack_config](../hermes_agent/hermes_messaging_slack_config.md) — channel→agent config; relevance: binding inbound channel messages to an agent.
- [hermes_profile_gateways_services](../hermes_agent/hermes_profile_gateways_services.md) — per-profile agent/gateway; relevance: per-agent overrides analog.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — routing internals; relevance: inbound-message → agent selection.
- [band_chat_rooms_and_routing](../band/band_chat_rooms_and_routing.md) — chat-room routing; relevance: routing messages to the right agent/room.
- [band_human_api_model](../band/band_human_api_model.md) — agent/peer model; relevance: per-agent identity + access.
- [cc_skill_dynamic_context_and_subagent](../claude_code/cc_skill_dynamic_context_and_subagent.md) — subagent model; relevance: per-agent overrides + subagent analog.
- [oc_gateway_config_channels](oc_gateway_config_channels.md) — channel→agent binding (planned, this series); relevance: the channel side of routing.
- [oc_gateway_config_channels_routing_commands](oc_gateway_config_channels_routing_commands.md) — mention gating (planned, this series); relevance: when a routed agent responds.
- [oc_concepts_multi_agent](oc_concepts_multi_agent.md) — multi-agent concept (planned, this series, co05); relevance: the multi-agent model this configures.
- [oc_channels_access_groups](oc_channels_access_groups.md) — access groups (planned, this series, ch01); relevance: per-agent access profiles.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — routing consumer; relevance: applies `agents.list` + binding fields.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel layer; relevance: inbound messages routed from channels.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: hosts the routing config.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — access profiles; relevance: per-agent access-profile security.

**Snippets**
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding routing; relevance: binding match fields → agent selection.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread binding policy; relevance: routing a thread to a specific agent.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — spawn thread binding; relevance: per-agent thread binding on spawn.
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — persistent bindings; relevance: stable thread→agent bindings.
- [snippet_openclaw_acp_spawn_policy](../../code_snippets/snippet_openclaw_acp_spawn_policy.md) — spawn policy; relevance: per-agent access/spawn policy.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — subagent spawn policy; relevance: per-agent override + spawn caps.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — subagent spawn (ACP); relevance: spawning a routed agent.
- [snippet_openclaw_agents_subagent_registry_announce](../../code_snippets/snippet_openclaw_agents_subagent_registry_announce.md) — subagent registry announce; relevance: per-agent registry/identity.
- [snippet_openclaw_agents_subagent_registry_lifecycle](../../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md) — subagent lifecycle; relevance: per-agent lifecycle in routing.
- [snippet_openclaw_agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — spawn caps; relevance: per-agent spawn limits.
- [snippet_openclaw_acp_spawn_session_handoff](../../code_snippets/snippet_openclaw_acp_spawn_session_handoff.md) — session handoff; relevance: handing an inbound session to the routed agent.

### oc_gateway_config_agents_session_messages (10t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: Session/Messages/Talk are OpenClaw `agents.defaults`.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — TTS; relevance: the Messages TTS + Talk voice blocks.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — voice interaction; relevance: the Talk (voice) block.
- [Voice Call](../../term_dictionary/term_voice_call.md) — voice session; relevance: Talk/voice-call session config.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — live STT; relevance: voice/talk inbound transcription.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — STT; relevance: voice message transcription.
- [Bot](../../term_dictionary/term_bot.md) — chat bot; relevance: response prefix / ack reaction / debounce shape bot replies.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — dedup key; relevance: inbound debounce dedups bursts.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: the session the messages run in.
- [Self-Management](../../term_dictionary/term_self_management.md) — session lifecycle; relevance: the Session block (reset/continuity).

**Docs**
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — message/media settings; relevance: response/ack/media message behavior.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — voice mode; relevance: the Talk/voice block analog.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — TTS providers; relevance: the Messages TTS config.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — STT transcription; relevance: voice inbound transcription.
- [hermes_sessions_lifecycle_resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — session lifecycle/resume; relevance: the Session block.
- [pi_sessions](../pi/pi_sessions.md) — session model; relevance: session continuity/reset analog.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — voice dictation; relevance: voice input → message analog.
- [oc_gateway_config_channels](oc_gateway_config_channels.md) — per-channel message behavior (planned, this series); relevance: channel-level message overrides.
- [oc_concepts_session](oc_concepts_session.md) — session concept (planned, this series, co06); relevance: the session model this configures.
- [oc_concepts_typing_indicators](oc_concepts_typing_indicators.md) — typing indicators (planned, this series, co07); relevance: message presentation behavior.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — session/message config consumer; relevance: applies Session/Messages/Talk.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session layer; relevance: the Session block consumer.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel delivery; relevance: response prefix/ack reaction delivery.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/talk subsystem; relevance: the Talk (voice) block.

**Snippets**
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/ack reactions; relevance: the Messages ack-reaction config.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — session reset hooks; relevance: the Session block reset/continuity.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session key utils; relevance: session identity in the Session block.
- [snippet_openclaw_voice_call_media_stream_admission](../../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md) — voice-call admission; relevance: the Talk/voice session setup.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice audio stream; relevance: Talk audio I/O.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — voice transcription; relevance: inbound voice → text.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS; relevance: the Messages/Talk TTS path.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS; relevance: local TTS backend for Talk.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: the Talk voice mode analog.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: STT for voice messages.
- [snippet_hermes_agent_tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — message send/format; relevance: response prefix formatting.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — message dispatch + debounce; relevance: inbound-debounce + reply dispatch.

### oc_gateway_config_channels (10t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `channels.*` config is OpenClaw.
- [Slack](../../term_dictionary/term_slack.md) — Slack platform; relevance: the Slack per-channel config block.
- [Bot](../../term_dictionary/term_bot.md) — chat bot; relevance: the per-platform bot the channels host.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound hook; relevance: webhook-based channel transports.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — multi-platform gateway; relevance: OpenClaw IS the messaging gateway these channels plug into.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — channel abstraction; relevance: the shared channel config surface across platforms.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — DM/group access; relevance: the "DM and group access" config block.
- [Socket Mode](../../term_dictionary/term_socket_mode.md) — Slack socket transport; relevance: Slack channel transport config.
- [Block Kit](../../term_dictionary/term_block_kit.md) — Slack UI blocks; relevance: Slack channel message presentation.
- [Omnichannel](../../term_dictionary/term_omnichannel.md) — many-platform reach; relevance: the 11+ platform config blocks.

**Docs**
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel setup; relevance: per-platform channel config analog.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — channels overview; relevance: the channel-config concept.
- [hermes_messaging_slack_config](../hermes_agent/hermes_messaging_slack_config.md) — Slack config; relevance: the Slack block analog.
- [hermes_discord_setup](../hermes_agent/hermes_discord_setup.md) — Discord setup; relevance: the Discord block analog.
- [hermes_telegram_setup](../hermes_agent/hermes_telegram_setup.md) — Telegram setup; relevance: the Telegram block analog.
- [hermes_messaging_whatsapp_baileys](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp transport; relevance: the WhatsApp block analog.
- [hermes_messaging_mattermost](../hermes_agent/hermes_messaging_mattermost.md) — Mattermost; relevance: the Mattermost block analog.
- [oc_gateway_config_channels_routing_commands](oc_gateway_config_channels_routing_commands.md) — routing/commands half (planned, this series); relevance: the cross-channel routing split.
- [oc_gateway_config_agents_routing](oc_gateway_config_agents_routing.md) — channel→agent binding (planned, this series); relevance: how channels bind to agents.
- [oc_channels_slack](oc_channels_slack.md) — Slack deep-dive (planned, this series, ch05); relevance: the platform deep-dive for the Slack config.
- [oc_channels_discord](oc_channels_discord.md) — Discord deep-dive (planned, this series, ch01); relevance: the platform deep-dive for the Discord config.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel transport plugins; relevance: the platforms this configures.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: Slack/Discord/Telegram transport impl.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: hosts the `channels.*` config.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — channel→agent binding; relevance: channel model overrides bind to agents.

**Snippets**
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel config; relevance: the per-platform config-block shape.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory; relevance: registry of configured channels.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — platform base class; relevance: the shared channel-config contract.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Slack platform; relevance: the Slack config block impl.
- [snippet_hermes_agent_gw_platform_discord_connect](../../code_snippets/snippet_hermes_agent_gw_platform_discord_connect.md) — Discord connect; relevance: the Discord config block impl.
- [snippet_hermes_agent_gw_platform_telegram_connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram connect; relevance: the Telegram config block impl.
- [snippet_hermes_agent_gw_platform_whatsapp](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp.md) — WhatsApp platform; relevance: the WhatsApp config block impl.
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Matrix platform; relevance: the Matrix config block impl.
- [snippet_hermes_agent_gw_platform_qqbot_adapter](../../code_snippets/snippet_hermes_agent_gw_platform_qqbot_adapter.md) — other-platform adapter; relevance: "other plugin channels" config.
- [snippet_hermes_agent_gw_platform_dingtalk](../../code_snippets/snippet_hermes_agent_gw_platform_dingtalk.md) — DingTalk platform; relevance: additional platform config block.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord intents; relevance: Discord channel-specific config.
- [snippet_hermes_agent_gw_runner_supervisor](../../code_snippets/snippet_hermes_agent_gw_runner_supervisor.md) — multi-channel supervisor; relevance: multi-account/multi-channel runtime.

### oc_gateway_config_channels_routing_commands (10t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: mention gating + commands are OpenClaw channel config.
- [Bot](../../term_dictionary/term_bot.md) — chat bot; relevance: when the bot responds in a group.
- [Slack](../../term_dictionary/term_slack.md) — Slack platform; relevance: mention gating + slash-commands on Slack.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — DM/group response policy; relevance: group-chat mention gating.
- [Silence Token](../../term_dictionary/term_silence_token.md) — suppress-response marker; relevance: gating whether the bot replies in a group.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — thread→agent binding; relevance: which agent a mention routes to.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multi-agent routing; relevance: routing a gated mention to the bound agent.
- [Access Control](../../term_dictionary/term_access_control.md) — command access; relevance: who can run chat commands.
- [Function Calling](../../term_dictionary/term_function_calling.md) — command handling; relevance: chat commands invoke handlers/tools.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — lifecycle signals; relevance: command-triggered lifecycle (reset/new).

**Docs**
- [hermes_slash_commands_messaging](../hermes_agent/hermes_slash_commands_messaging.md) — chat slash commands; relevance: the chat-command handling config analog.
- [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Slack messaging; relevance: mention gating + command handling on Slack.
- [hermes_discord_advanced](../hermes_agent/hermes_discord_advanced.md) — Discord advanced routing; relevance: group mention gating analog.
- [hermes_faq_messaging_perf_profiles_workflows](../hermes_agent/hermes_faq_messaging_perf_profiles_workflows.md) — messaging behavior FAQ; relevance: when/whether the bot responds.
- [band_chat_rooms_and_routing](../band/band_chat_rooms_and_routing.md) — chat-room routing; relevance: group routing + response gating.
- [cc_claude_code_in_slack](../claude_code/cc_claude_code_in_slack.md) — bot-in-Slack; relevance: mention/command behavior in a group bot.
- [oc_gateway_config_channels](oc_gateway_config_channels.md) — transport half (planned, this series); relevance: the per-channel transport config split.
- [oc_gateway_config_agents_routing](oc_gateway_config_agents_routing.md) — agent binding (planned, this series); relevance: which agent a gated mention routes to.
- [oc_channels_bot_loop_protection](oc_channels_bot_loop_protection.md) — bot loop protection (planned, this series, ch01); relevance: gating bot-to-bot reply loops.
- [oc_channels_group_messages](oc_channels_group_messages.md) — group messages (planned, this series, ch02); relevance: group-chat mention behavior.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — mention-gating/command consumers; relevance: implements gating + command dispatch.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: per-platform command/mention handling.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent routing target; relevance: the agent a gated mention routes to.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: hosts the routing/command config.

**Snippets**
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding routing; relevance: routing a gated mention to an agent.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread binding policy; relevance: which thread/agent a command targets.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status reactions; relevance: command/mention acknowledgement.
- [snippet_hermes_agent_gw_platform_discord_slash](../../code_snippets/snippet_hermes_agent_gw_platform_discord_slash.md) — Discord slash commands; relevance: chat-command handling.
- [snippet_hermes_agent_gw_platform_discord_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_discord_normalize.md) — Discord message normalize; relevance: detecting mentions in group messages.
- [snippet_hermes_agent_gw_platform_discord_thread](../../code_snippets/snippet_hermes_agent_gw_platform_discord_thread.md) — Discord thread handling; relevance: group/thread mention gating.
- [snippet_hermes_agent_tui_server_slash](../../code_snippets/snippet_hermes_agent_tui_server_slash.md) — slash-command server; relevance: chat-command parsing/dispatch.
- [snippet_slipbot_slack_handlers](../../code_snippets/snippet_slipbot_slack_handlers.md) — Slack event handlers; relevance: mention-triggered handling in a Slack bot.
- [snippet_hermes_agent_gw_platform_matrix_acl](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_acl.md) — Matrix ACL; relevance: access control on group commands.
- [snippet_hermes_agent_gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — gateway session state; relevance: command-triggered session reset/new.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — reply dispatch; relevance: dispatching the gated response.

## Undigested Terms Plan

> Per master ownership rule: OpenClaw vocabulary that is the subject of a doc page is digested as an `oc_*` doc note by its home sub-plan, NOT as a new `term_dictionary` entry. The only `term_dictionary` interaction is **linking existing** terms. **Expected: 0 new `term_dictionary` captures.** No term definition is ever inlined in an `oc_*` note.

| Term | Disposition |
|---|---|
| OpenClaw, gateway, agent defaults, multi-agent routing, CLI backends, Bonjour/DNS-SD, bridge protocol, exec/process tool, child-process bridging, mention gating, chat commands, prompt overlays, context budget, heartbeat config, compaction config, sandbox policy, ack reaction, inbound debounce | OpenClaw vocab → digested in-place as `oc_gateway_*` notes (notes 1–15). Not promoted to `term_dictionary`. |
| Tailscale | No existing `term_tailscale` (verified MISSING). Cross-cutting (used by gateway/remote/bonjour/multiple-gateways). **New-term candidate** — but gw06 owns `gateway/tailscale.md`; defer capture decision to gw06 (the doc-page home). gw01 links the planned `oc_gateway_tailscale` sibling instead. |
| service discovery / DNS-SD / mDNS / Bonjour | No existing `term_service_discovery`/`term_mdns` (verified MISSING). The concept's doc-page home is `gateway/bonjour` (gw01 note 3). Per master ownership rule → digested in-place as note 3, NOT promoted to a term. **Not a new-term capture.** |
| Codex, GitHub Copilot (subscription providers in auth.md) | No existing term notes (verified MISSING). Documented as auth/config in note 1, not promoted (link `term_third_party_genai_services` / `term_oauth`). |
| Discord, Telegram, WhatsApp, Signal, Matrix, Mattermost, iMessage, Teams, IRC (channel platforms) | No existing per-platform term notes except `term_slack` (verified). Documented as channel config in note 14; per-platform deep-dives are ch01–ch06 doc notes. Not promoted to terms (link `term_slack`/`term_bot` where relevant). |

**Net: 0 new `term_dictionary` captures planned by gw01.** Tailscale's capture decision is deferred to its doc-page owner gw06; if gw06 also defers, the cross-cutting reuse flags `term_tailscale` as a candidate for `acronym_glossary_gen_ai_dev.md` (best-fit glossary for dev-tooling networking) — but that is gw06's call, not gw01's.

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (15 notes, P1). Gate table identical to the master's 9-GATE definition.

| Gate | Check | Tool / Method | Pass criterion |
|------|-------|---------------|----------------|
| G1 | Format (YAML + body structure) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` | 0 ERROR; YAML field order + forbidden-field absence; `## Overview` + `## Related Notes` present; `**Source**`/`**Last Updated**`/`**Status**` footer |
| G2 | Grounding (no hallucination) | diff each note vs `inbox/openclaw_docs/gateway/<page>.md` | every claim traces to source; config snippets verbatim |
| G3 | Density + Coverage | per-note `wc -w` (body) + fence count; section coverage map | ≤2,500w, ≤6 fences, ≤400 lines, one BB; every mapped section covered |
| G4 | Cross-Reference | `## Related Notes` ≥6 relevance-selected terms + repo/sibling/doc links | floor met; each link has a relevance statement |
| G5 | Ghost-reference detect + redirect | `/tessellum-fix-ghost-references` (DB-verify every cited id) | 0 ghost references |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` after reindex | 0 broken links |
| G7 | Discoverability (outbound) | each note links ≥6 terms + siblings | satisfied by G4 |
| G8 | Discoverability (inbound / in-degree ≥1) | each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | satisfied via `entry_openclaw_docs.md` (W1) + repo/term inlinks |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_gateway_authentication oc_gateway_background_process oc_gateway_bonjour oc_gateway_bonjour_troubleshooting oc_gateway_bridge_protocol oc_gateway_cli_backends oc_gateway_cli_backends_internals oc_gateway_config_agents_bootstrap_context oc_gateway_config_agents_model_media oc_gateway_config_agents_backends_overlays oc_gateway_config_agents_runtime_resilience oc_gateway_config_agents_routing oc_gateway_config_agents_session_messages oc_gateway_config_channels oc_gateway_config_channels_routing_commands"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # G1 required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # G1 source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density (body words / fences)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb fences)"
  # G7 sibling link presence (≥1 oc_ sibling or repo/term link)
  grep -q "($SIBLING_PREFIX" "$f" || grep -qE '\((\.\./)+term_dictionary/term_' "$f" || echo "$n NO SIBLING/TERM LINK"
done

# G1 YAML frontmatter sweep (whole folder)
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source fences (page total) | Within caps? |
|---|---|---|---:|---|---|
| 1 | oc_gateway_authentication | procedure | 700 | ≤6 of 14 | ✅ |
| 2 | oc_gateway_background_process | concept | 550 | ≤6 of 8 | ✅ |
| 3 | oc_gateway_bonjour | procedure | 750 | ≤4 of 6 | ✅ |
| 4 | oc_gateway_bonjour_troubleshooting | procedure | 600 | ≤4 of 6 | ✅ |
| 5 | oc_gateway_bridge_protocol | model | 450 | 0 | ✅ |
| 6 | oc_gateway_cli_backends | procedure | 700 | ≤6 of 10 | ✅ |
| 7 | oc_gateway_cli_backends_internals | concept | 650 | ≤5 of 10 | ✅ |
| 8 | oc_gateway_config_agents_bootstrap_context | procedure | 700 | ≤6 of 41 | ✅ |
| 9 | oc_gateway_config_agents_model_media | procedure | 600 | ≤6 of 41 | ✅ |
| 10 | oc_gateway_config_agents_backends_overlays | procedure | 500 | ≤5 of 41 | ✅ |
| 11 | oc_gateway_config_agents_runtime_resilience | procedure | 750 | ≤6 of 41 | ✅ |
| 12 | oc_gateway_config_agents_routing | procedure | 600 | ≤6 of 41 | ✅ |
| 13 | oc_gateway_config_agents_session_messages | procedure | 600 | ≤6 of 41 | ✅ |
| 14 | oc_gateway_config_channels | procedure | 750 | ≤6 of 20 | ✅ |
| 15 | oc_gateway_config_channels_routing_commands | procedure | 600 | ≤5 of 20 | ✅ |

No note approaches the 2,500w / 6-fence / 400-line caps. The 3 oversized source pages were split (Split Decisions) precisely so each note stays well under caps; the 41 fences of `config-agents` are distributed across 6 notes, each trimmed to the ≤6 most load-bearing config snippets (reproduced verbatim).

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)


- `entry_openclaw_docs.md` (W1, created pre-execution) → **all 15** notes (primary G8 source).
- `repo_openclaw_gateway` → notes 1, 2, 3, 4, 5, 6, 7, 11.
- `repo_openclaw_agents` → notes 2, 6, 8, 9, 10, 11, 12, 13.
- `repo_openclaw_channels` / `repo_openclaw_channels_messaging` → notes 12, 13, 14, 15.
- `repo_openclaw_security` → notes 1, 3, 4, 11, 12.
- `repo_openclaw_extensions_llm_providers` → notes 1, 6, 7, 9, 10.
- `repo_openclaw_sessions` → notes 2, 7, 11, 13.
- `term_openclaw` → notes 1–15 (subset, relevance-selected at execution).
- `term_oauth` / `term_oauth_token` / `term_authentication` → note 1.
- `term_dns` → notes 3, 4.
- `term_slack` → notes 14, 15.
- `term_heartbeat` / `term_compaction` → note 11.

## Pacing Rules (inherited from master)

One execution phase; all 8 gates pass before commit. Re-read each source page during execution; config snippets reproduced verbatim from the mirror. One BB per note. Cap dynamic-workflow fan-out at ~30 agents/run (15 notes is one wave). `git pull --rebase --autostash` first; no Claude co-author trailer; reindex incrementally and verify `note_links` + 0 broken links before commit; commit + push after the phase.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — READY (9/9 CP pass) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (ready to dispatch) |

## Augmentation Report (2026-06-21)


**What was locked (per-note counts — terms / snippets / docs[existing+planned] / repos)**:

| # | Note | Terms | Snippets | Docs (exist+plan=tot) | Repos | Floors met |
|---|---|---:|---:|---|---:|---|
| 1 | oc_gateway_authentication | 12 | 12 | 10+2=12 | 4 | ✅ |
| 2 | oc_gateway_background_process | 8 | 12 | 8+2=10 | 4 | ✅ |
| 3 | oc_gateway_bonjour | 10 | 11 | 6+4=10 | 3 | ✅ |
| 4 | oc_gateway_bonjour_troubleshooting | 9 | 11 | 6+4=10 | 3 | ✅ |
| 5 | oc_gateway_bridge_protocol | 10 | 11 | 6+4=10 | 3 | ✅ |
| 6 | oc_gateway_cli_backends | 11 | 12 | 7+4=11 | 4 | ✅ |
| 7 | oc_gateway_cli_backends_internals | 11 | 12 | 7+4=11 | 4 | ✅ |
| 8 | oc_gateway_config_agents_bootstrap_context | 10 | 11 | 7+3=10 | 4 | ✅ |
| 9 | oc_gateway_config_agents_model_media | 10 | 11 | 7+4=11 | 4 | ✅ |
| 10 | oc_gateway_config_agents_backends_overlays | 9 | 11 | 6+4=10 | 3 | ✅ |
| 11 | oc_gateway_config_agents_runtime_resilience | 11 | 12 | 7+3=10 | 4 | ✅ |
| 12 | oc_gateway_config_agents_routing | 10 | 11 | 6+4=10 | 4 | ✅ |
| 13 | oc_gateway_config_agents_session_messages | 10 | 12 | 7+3=10 | 4 | ✅ |
| 14 | oc_gateway_config_channels | 10 | 12 | 7+4=11 | 4 | ✅ |
| 15 | oc_gateway_config_channels_routing_commands | 10 | 11 | 6+4=10 | 4 | ✅ |


**New-term candidates**: **0 new `term_dictionary` captures** for gw01 (consistent with the master ownership rule + the plan's Undigested Terms Plan). The xref re-read confirmed the prior plan's MISSING-term notes (`term_tailscale`, `term_service_discovery`/`term_mdns`, per-platform channel terms `term_discord`/`term_telegram`/etc.) are correctly handled: Tailscale's capture is deferred to its doc-page owner gw06 (best-fit glossary if captured: `acronym_glossary_gen_ai_dev.md`); DNS-SD/mDNS is digested in-place as note 3 (doc-page home `gateway/bonjour`); per-platform channels stay config in note 14 (link `term_slack`/`term_bot`). The augment surfaced a substantive existing `term_bonjour_discovery` note (not previously linked) and now links it from notes 3 + 4 — no new capture, link-only. Net new-term candidates flagged to glossary: **none owned by gw01**.


## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors (terms+snippets+docs, relevance-stated) | **PASS** | Per-Note Related Notes Mapping present; all 15 notes ≥8 terms / ≥10 snippets / ≥10 docs; every link carries a `— what it is; relevance: why THIS note` statement (no bare links). Min observed: 8 terms (note 2), 11 snippets, 10 docs. |
| CP2 | 9-GATE table present (G1-G6, G7/G8) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` present with all gates incl. G5 ghost-detect (`/tessellum-fix-ghost-references`), G6 broken-link (`/tessellum-fix-broken-links`), G7/G8 discoverability; single execution phase, one gate table covering it. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision (inherited from master)` contributes 15 rows to `entry_openclaw_docs.md` (CREATED as master W1 pre-step; DB-confirmed not-yet-created → correctly a pre-execution step). Parent-hub wiring is master W2/W3. Size: 105-sub-plan / >30-note series → CREATE required (matches threshold). |
| CP4 | Size manageable | **PASS** | 15 notes (one wave, ≤30); sub-plan of a properly split 105-sub-plan master. |
| CP5 | Format derived from existing notes | **PASS** | Format Definition inherited from master, DERIVED from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) notes (verified: `tags: resource→documentation→<area>` order; `## Overview` opener; `## Related Notes` reference section; `language: markdown`; `access_control_group: ["general"]`; same forbidden-field list). Not invented. |
| CP6 | Density borderline → split promoted | **PASS** | Density Re-Assessment table: no note approaches caps (max ~750w vs 2,500w; max ≤6 fences; ≤400 lines). The 3 oversized source pages (config-agents 7,179w, config-channels 5,299w, cli-backends 2,626w) split per Split Decisions; no borderline note left un-split. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 pages re-read + `wc -w` measured 2026-06-21: 1,545 / 834 / 1,678 / 495 / 2,626 / 7,179 / 5,299 (body words). Every page within ±10% of the plan's Source-table estimate (ratio 0.88–1.01); none >1.5× → no under-estimation, no re-split required. |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | `## Undigested Terms Plan` present (disposition per term); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, link-existing-only inherited from master; multi-source mandate applies only on capture, which gw01 does not do). Net: 0 new `term_dictionary` captures. |
| CP8f | Term-slug specificity + all-notes collision audit | **PASS** | Specificity: 0 too-general slugs (gw01 creates 0 term slugs). Collision (generalized to ALL planned notes, term_dictionary AND documentation/): each of the 15 `oc_gateway_*` doc-note slugs checked vs existing vault — no doc-note duplicates an existing term or doc (OpenClaw gateway-config docs are net-new; the existing `term_*`/`repo_openclaw_*`/cc_*/pi_*/hermes_* notes are LINKED, not recreated). Surfaced + linked existing `term_bonjour_discovery` (link-only, no recreate). |

**RESULT: 9/9 CP PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
