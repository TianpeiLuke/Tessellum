---
title: Sub-Plan rf03 — OpenClaw Docs: Reference (SecretRef Surface, Session/Compaction, Workspace Templates)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - reference/secretref-credential-surface
  - reference/session-management-compaction
  - reference/templates/AGENTS.dev
  - reference/templates/BOOT
  - reference/templates/BOOTSTRAP
  - reference/templates/CLAUDE
  - reference/templates/HEARTBEAT
---

# Sub-Plan rf03: Reference

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML + `## Overview`/`## Related Notes` body),
> dedup (3-way: term_dictionary + documentation + repo_openclaw*), 9-GATE, cross-refs, and entry-point wiring are ALL inherited from the master.

## Scope

The 7 Reference-section pages covering credential-surface canon and session/agent runtime mechanics plus the
default agent-workspace file templates:

- **`secretref-credential-surface`** — the canonical list of which config paths are eligible for SecretRef
  resolution (`secrets configure`/`apply`/`audit`) and which are out of scope (minted/rotating/OAuth-durable).
- **`session-management-compaction`** — the deep-dive on the session store (`sessions.json`), transcript JSONL,
  session-key/session-id lifecycle, context limits, and (auto)compaction internals + memory-flush hooks.
- **`templates/AGENTS.dev`, `templates/CLAUDE`, `templates/BOOT`, `templates/BOOTSTRAP`, `templates/HEARTBEAT`** —
  the scaffold files that ship into a fresh agent workspace and define identity/memory/heartbeat conventions.

**Priority: P2** (Reference, Phase B). The session/compaction and SecretRef pages are referenced by the
gateway, secrets, CLI, and concepts sections; the templates are the user-facing materialization of the
agent-workspace/memory concepts. The code-side counterparts (`repo_openclaw_sessions`, `repo_openclaw_memory`,
`repo_openclaw_security`, `repo_openclaw_agents`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 5,842 measured words. **Planned: 6 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| SecretRef credential surface | reference/secretref-credential-surface | 580 | 0 | 3 | 2 | model (credential-surface reference) |
| Session management deep dive | reference/session-management-compaction | 3,055 | 2 | 20 | 0 | model + procedure (split: store/lifecycle model vs compaction procedure) |
| AGENTS.dev template | reference/templates/AGENTS.dev | 475 | 1 | 8 | 2 | model (dev workspace template) |
| BOOT.md template | reference/templates/BOOT | 57 | 0 | 1 | 0 | procedure (consolidated → note 5) |
| BOOTSTRAP.md template | reference/templates/BOOTSTRAP | 280 | 0 | 5 | 0 | procedure (consolidated → note 5) |
| CLAUDE.md template | reference/templates/CLAUDE | 1,284 | 1 | 10 | 6 | model (default workspace instruction template) |
| HEARTBEAT.md template | reference/templates/HEARTBEAT | 111 | 1 | 1 | 0 | procedure (consolidated → note 5) |

Totals: 5,842 words · 5 code blocks (raw fences/2) · 48 H2 · 10 H3.

## Content Strategy

- **Prioritize**: (a) the SecretRef supported/unsupported surface (it is the authority for secrets tooling
  eligibility) and (b) the session-store + (auto)compaction internals (every long-running conversation depends
  on the store schema, reset/idle/daily lifecycle, overflow recovery, and the memory-flush hook).
- **Split**: `session-management-compaction.md` (3,055w > 2,500w cap; mixed BB) → one **model** note for the
  store/transcript/lifecycle data model and one **procedure** note for compaction config + operation +
  troubleshooting. Each stays well under caps.
- **Consolidate**: the three tiny workspace ritual templates — `BOOT` (57w), `BOOTSTRAP` (280w),
  `HEARTBEAT` (111w) — into ONE procedure note on the workspace lifecycle scaffolds (448w combined). Each is too
  small to be a meaningful atomic note alone, and all three are first-run / recurring-wake workspace rituals
  that belong to the same task cluster (create → boot → heartbeat).
- **Keep separate**: `CLAUDE.md` (1,284w — the comprehensive default workspace instruction template, distinct
  audience/content from the dev template) and `AGENTS.dev.md` (475w — the dev-gateway agent identity template
  with the C-3PO origin memory) each get a dedicated note.
- **Link-out (do NOT redefine)**: the higher-level concept pages this Reference section points to
  (`/concepts/session`, `/concepts/compaction`, `/concepts/memory`, `/concepts/agent-workspace`,
  `/gateway/secrets`, `/auth-credential-semantics`, `/reference/transcript-hygiene`, `/reference/token-use`) are
  owned by co05/co06/co02/co01, gw05, rt01, rf05, rf05 respectively — cross-link as siblings, never inline.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_reference_secretref_credential_surface.md` | model | secretref-credential-surface.md: Scope intent, Supported credentials (`openclaw.json` targets, `auth-profiles.json` targets, Notes), Unsupported credentials + Rationale | 550 | The canonical SecretRef credential surface: which `openclaw.json` and `auth-profiles.json` config paths are eligible for `secrets configure`/`apply`/`audit`, the structured-object SecretRef requirement, the OAuth-mode policy guard, web-search precedence rules, and the out-of-scope (minted/rotating/OAuth-durable) credentials. |
| 2 | `oc_reference_session_management_store.md` | model | session-management-compaction.md: Areas overview, Source of truth (Gateway), Two persistence layers, On-disk locations, Store maintenance + disk controls, Cron sessions + run logs, Session keys, Session ids, Session store schema, Transcript structure, Context windows vs tracked tokens | 650 | The session persistence data model: Gateway as source of truth, the two layers (`sessions.json` store + `<sessionId>.jsonl` transcript), on-disk paths, store-maintenance/disk-budget controls + write locks, session-key routing patterns, session-id reset/idle/daily lifecycle, the `SessionEntry` schema, JSONL transcript entry types, and context-window vs tracked-token counters. |
| 3 | `oc_reference_session_management_compaction.md` | procedure | session-management-compaction.md: Compaction (what it is), Compaction chunk boundaries + tool pairing, When auto-compaction happens, Compaction settings, Pluggable compaction providers, User-visible surfaces, Silent housekeeping (`NO_REPLY`), Pre-compaction memory flush, Troubleshooting checklist | 700 | OpenClaw compaction operation: what compaction persists, chunk-boundary tool-pairing rules, the two auto-compaction triggers (overflow recovery + threshold maintenance) plus preflight/mid-turn guards, the `reserveTokens`/`keepRecentTokens`/floor settings, pluggable compaction providers, observability surfaces, `NO_REPLY` silent turns, the pre-compaction memory flush, and the troubleshooting checklist. |
| 4 | `oc_reference_templates_claude_md.md` | model | templates/CLAUDE.md: First Run, Session Startup, Memory (+ MEMORY.md, Write It Down), Red Lines, External vs Internal, Group Chats (Know When to Speak, React Like a Human), Tools, Heartbeats (+ Heartbeat vs Cron, Memory Maintenance), Make It Yours | 650 | The default agent-workspace instruction template (`CLAUDE.md`/`AGENTS.md`): first-run bootstrap, session-startup context reuse, the daily/long-term memory model (MEMORY.md main-session-only), red lines/safety defaults, external-vs-internal action gating, group-chat speaking + reaction etiquette, tools/skills conventions, and proactive heartbeat behavior. |
| 5 | `oc_reference_templates_workspace_lifecycle.md` | procedure | templates/BOOT.md (all), templates/BOOTSTRAP.md (The Conversation, After You Know Who You Are, Connect, When you are done), templates/HEARTBEAT.md (all) | 500 | The workspace lifecycle ritual scaffolds: `BOOTSTRAP.md` (one-time identity-creation conversation that writes IDENTITY/USER/SOUL then self-deletes), `BOOT.md` (startup checklist with the `hooks.internal.enabled` + `NO_REPLY` silent-message convention), and `HEARTBEAT.md` (recurring-wake checklist kept empty to skip heartbeat model calls). |
| 6 | `oc_reference_templates_agents_dev.md` | model | templates/AGENTS.dev.md: First run, Backup tip, Safety defaults, Daily memory, Heartbeats, Customize, C-3PO Origin Memory (Birth Day, Core Truths) | 450 | The dev-gateway agent workspace template (`AGENTS.dev.md`, "C-3PO"): the dev-agent identity defaults (workspace-as-memory git backup, safety defaults, daily `memory/YYYY-MM-DD.md` log discipline, optional heartbeat checklist) plus the bundled C-3PO origin-memory persona seed. |

## Section Coverage Map

```
secretref-credential-surface.md
├── (intro) Scope intent (in/out of scope) ───────────────────────── → note 1 (oc_reference_secretref_credential_surface)
├── ## Supported credentials
│   ├── ### openclaw.json targets (configure/apply/audit) ────────── → note 1
│   ├── ### auth-profiles.json targets (configure/apply/audit) ───── → note 1
│   └── Notes (structured-object SecretRef, OAuth policy guard,
│       marker persistence, web-search precedence) ───────────────── → note 1
└── ## Unsupported credentials + Rationale ───────────────────────── → note 1

session-management-compaction.md
├── (intro) areas overview + higher-level pointers ──────────────── → note 2 (oc_reference_session_management_store)
├── ## Source of truth: the Gateway ─────────────────────────────── → note 2
├── ## Two persistence layers ───────────────────────────────────── → note 2
├── ## On-disk locations ────────────────────────────────────────── → note 2
├── ## Store maintenance and disk controls ──────────────────────── → note 2
├── ## Cron sessions and run logs ───────────────────────────────── → note 2
├── ## Session keys (sessionKey) ────────────────────────────────── → note 2
├── ## Session ids (sessionId) ──────────────────────────────────── → note 2
├── ## Session store schema (sessions.json) ─────────────────────── → note 2
├── ## Transcript structure (*.jsonl) ───────────────────────────── → note 2
├── ## Context windows vs tracked tokens ────────────────────────── → note 2
├── ## Compaction: what it is ───────────────────────────────────── → note 3 (oc_reference_session_management_compaction)
├── ## Compaction chunk boundaries and tool pairing ─────────────── → note 3
├── ## When auto-compaction happens (OpenClaw runtime) ──────────── → note 3
├── ## Compaction settings (reserveTokens, keepRecentTokens) ─────── → note 3
├── ## Pluggable compaction providers ───────────────────────────── → note 3
├── ## User-visible surfaces ────────────────────────────────────── → note 3
├── ## Silent housekeeping (NO_REPLY) ───────────────────────────── → note 3
├── ## Pre-compaction "memory flush" (implemented) ──────────────── → note 3
└── ## Troubleshooting checklist ────────────────────────────────── → note 3

templates/CLAUDE.md
├── ## First Run ────────────────────────────────────────────────── → note 4 (oc_reference_templates_claude_md)
├── ## Session Startup ──────────────────────────────────────────── → note 4
├── ## Memory (### MEMORY.md, ### Write It Down) ─────────────────── → note 4
├── ## Red Lines ────────────────────────────────────────────────── → note 4
├── ## External vs Internal ─────────────────────────────────────── → note 4
├── ## Group Chats (### Know When to Speak, ### React Like a Human) → note 4
├── ## Tools ────────────────────────────────────────────────────── → note 4
├── ## Heartbeats (### Heartbeat vs Cron, ### Memory Maintenance) ── → note 4
└── ## Make It Yours ────────────────────────────────────────────── → note 4

templates/BOOT.md
└── # BOOT.md (startup checklist, hooks.internal.enabled, NO_REPLY) → note 5 (oc_reference_templates_workspace_lifecycle)
templates/BOOTSTRAP.md
├── (intro fresh-workspace note) ────────────────────────────────── → note 5
├── ## The Conversation ─────────────────────────────────────────── → note 5
├── ## After You Know Who You Are ───────────────────────────────── → note 5
├── ## Connect (Optional) ───────────────────────────────────────── → note 5
└── ## When you are done (self-delete) ──────────────────────────── → note 5
templates/HEARTBEAT.md
└── # HEARTBEAT.md (empty-to-skip rule, default runtime template) ── → note 5

templates/AGENTS.dev.md
├── ## First run (one-time) ─────────────────────────────────────── → note 6 (oc_reference_templates_agents_dev)
├── ## Backup tip (recommended) ─────────────────────────────────── → note 6
├── ## Safety defaults ──────────────────────────────────────────── → note 6
├── ## Daily memory (recommended) ───────────────────────────────── → note 6
├── ## Heartbeats (optional) ────────────────────────────────────── → note 6
├── ## Customize ────────────────────────────────────────────────── → note 6
└── ## C-3PO Origin Memory (### Birth Day, ### Core Truths) ──────── → note 6
```

No orphaned sections. The `## Related` link blocks at the foot of each source page become `## Related Notes` /
`## References` entries (concept/gateway/reference pointers cross-linked to their owning sub-plans, never inlined).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| session-management-compaction.md (3,055w, 20 H2, mixed BB) | notes 2 + 3 | Exceeds the 2,500-word cap AND mixes two building blocks: the session-store/transcript/lifecycle **data model** (note 2) vs the compaction **operation/config/troubleshooting procedure** (note 3). Split per word-cap + one-BB-per-note rules; each child stays ≤700w. |
| BOOT.md (57w) + BOOTSTRAP.md (280w) + HEARTBEAT.md (111w) | note 5 (consolidated) | Reverse split — three sub-atomic template pages (each far below a viable note size) merged into one procedure note. All three are same-BB (procedure) workspace-lifecycle ritual scaffolds (create→boot→recurring-wake) and read together as the workspace setup story; combined 448w stays well under caps. |

## Summary Statistics & Building Block Distribution

- Source pages: 7 (5,842 words). New `oc_*` notes: **6**. New `term_dictionary` notes: **0**.
- BB distribution: **model ×4** (notes 1 credential surface, 2 session-store data model, 4 CLAUDE template,
  6 AGENTS.dev template) · **procedure ×2** (notes 3 compaction operation, 5 workspace lifecycle rituals).
- Est. digest words ~3,500 (avg ~583/note); all ≤700w, all ≤2,500w cap. 5 source code fences (1 bash in
  AGENTS.dev, 1 markdown in HEARTBEAT, 1 json in CLAUDE, 2 in session/compaction) distribute across notes 3/4/5/6,
  each ≤6 fences.
- Cross-refs (xref-augment LOCKED 2026-06-21, RAISED FLOORS): every note maps **≥8 relevancy-selected
  `oc_*` count toward the 10-doc floor as "planned, this series") + relevant `repo_openclaw*`, each with a
  per-link relevance statement. Locked per-note counts: note 1 = 10t·11s·10d, note 2 = 10t·12s·10d,
  note 3 = 10t·12s·10d, note 4 = 10t·11s·10d, note 5 = 9t·11s·10d, note 6 = 9t·11s·10d. All EXISTING cited

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (source re-read; no padding,
> Sibling `oc_*` docs in this rf03 series do not exist yet → cited "(planned, this series)" toward the 10-doc
> `hermes_*` / band `band_*` coding-agent corpora). `entry_openclaw_docs` is "(planned — master pre-step W1)".
> Relative paths are FROM `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/term_Y.md`;
> sibling oc_ → `oc_Y.md`; other doc → `../<folder>/<file>.md`; repo → `../../../areas/code_repos/repo_Y.md`;
> snippet → `../../code_snippets/snippet_Y.md`; entry → `../../../0_entry_points/entry_Y.md`.

### oc_reference_secretref_credential_surface (10t · 11s · 10d)

**Terms**
- [TLS](../../term_dictionary/term_tls.md) — transport-layer security; relevance: the supported surface includes the proxy/request `tls.{ca,cert,key,passphrase}` SecretRef paths verbatim.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer/refresh token credential; relevance: `gateway.auth.token`, `*.authToken`, and `tokenRef` are supported, while OAuth-durable refresh material is explicitly out of scope.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated authorization protocol; relevance: the page's OAuth policy guard (`auth.profiles.<id>.mode = "oauth"` cannot combine with SecretRef) is a load-bearing rule.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the entire surface governs how OpenClaw resolves auth credentials for gateway/channels/providers.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — `auth-profiles.json` credential profile; relevance: `profiles.*.keyRef`/`tokenRef` are the second supported config file with `agentId`-scoped plan targets.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model/provider plugin config; relevance: `plugins.entries.*.config.webSearch.apiKey` is the canonical SecretRef surface (legacy `tools.web.search.*` deprecating).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model/web-search vendors; relevance: most supported keys (`models.providers.*.apiKey`, search-provider keys) are third-party vendor credentials.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — request-forwarding proxy; relevance: `models.providers.*.request.proxy.tls.*` SecretRef paths secure an upstream proxy TLS hop.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw.json`/`secrets configure|apply|audit` and `openclaw doctor --fix` marker migration are OpenClaw tooling.
- [PII](../../term_dictionary/term_pii.md) — sensitive personal data; relevance: marker-persistence (writing non-secret markers, never resolved values) is the page's data-protection guarantee for `agents/*/agent/models.json`.

**Docs**
- [Claude Code Authentication](../claude_code/cc_authentication.md) — coding-agent credential login; relevance: parallel "which credentials and how they're stored" reference for a sibling agent.
- [Claude Code MCP Authentication](../claude_code/cc_mcp_authentication.md) — OAuth for MCP servers; relevance: the same OAuth-vs-API-key distinction OpenClaw's policy guard enforces.
- [Claude Code SDK Credential & Filesystem Controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — programmatic credential gating; relevance: closest analog to OpenClaw's read-only external SecretRef resolution model.
- [Claude Code Amazon Bedrock Setup](../claude_code/cc_amazon_bedrock_setup.md) — provider credential setup; relevance: example of a provider `apiKey`-class credential mirroring `models.providers.*.apiKey`.
- [Claude Code Environment Variables](../claude_code/cc_environment_variables.md) — env-based config; relevance: SecretRefs use a structured `{"source":"env",...}` object, the canonical replacement for legacy `secretref-env:<ENV>` markers.
- [Pi Provider Auth](../pi/pi_provider_auth.md) — provider auth config; relevance: another coding agent's provider-key/auth-profile model for contrast.
- [Hermes Credential Pools](../hermes_agent/hermes_credential_pools.md) — multi-key credential rotation; relevance: contrasts OpenClaw's "user-supplied, not minted/rotated" scope boundary against a rotating-pool design.
- [Hermes Env Vars (Providers/Auth/Tools)](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env catalog; relevance: parallel catalog of which provider/tool credentials exist and how they're sourced.
- [Hermes Security Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation/storage model; relevance: cross-stack analog of how secret material is isolated and resolved without persisting plaintext, mirroring OpenClaw's read-only SecretRef + marker-persistence boundary.
- [oc_reference_session_management_store](oc_reference_session_management_store.md) (planned, this series) — session store data model; relevance: the unsupported `hooks.mappings[].sessionKey` is session-scoped and belongs to that note's domain.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/audit/redaction package; relevance: owns SecretRef resolution, audit coverage, and marker handling.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: `secrets apply` and runtime resolution flow through the gateway call layer.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM provider plugins; relevance: provider `apiKey`/header/TLS SecretRef paths are defined by these plugins.

**Snippets**
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — gateway secret-resolution call; relevance: implements `secrets apply`/runtime SecretRef resolution this page specifies.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential ordering; relevance: implements `profiles.*.keyRef`/`tokenRef` resolution + OAuth-mode guard.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profile; relevance: the OAuth/externally-managed profile classes excluded from the SecretRef surface.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth-mode profile portability; relevance: the OAuth-durable material the page declares out of scope.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — untrusted-content handling; relevance: same security package enforcing read-only credential resolution boundaries.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool denial policy; relevance: companion guardrail in the security package that owns SecretRef.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client TLS identity; relevance: implements the `*.tls.{ca,cert,key,passphrase}` credential surface.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode helpers; relevance: resolves `gateway.auth.{password,token}`/`gateway.remote.*` supported credentials.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider adapter; relevance: consumes `models.providers.*.apiKey`/header SecretRef values.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: cross-stack analog of credential-source precedence (env/config/profile).

### oc_reference_session_management_store (10t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the Gateway process is the declared single source of truth for session state.
- [Context Window](../../term_dictionary/term_context_window.md) — model token budget; relevance: the "context window vs tracked tokens" section distinguishes the model cap from `contextTokens` store counters.
- [Tokenization](../../term_dictionary/term_tokenization.md) — token counting; relevance: `inputTokens`/`outputTokens`/`totalTokens`/`contextTokens` counters in `SessionEntry`.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript summarization; relevance: `compactionCount` and the `compaction` transcript entry type are stored here; sibling note 3 operates over this model.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: isolated cron runs create `cron:<jobId>` session entries with dedicated retention controls.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — periodic wake poll; relevance: heartbeat system events mutate the session row but do not extend idle/daily reset freshness.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound HTTP callback; relevance: `hook:<uuid>` is a documented `sessionKey` routing pattern.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent runtime protocol; relevance: cron session sanitization drops "ACP runtime binding" so a fresh run cannot inherit stale runtime authority.
- [Markdown](../../term_dictionary/term_markdown.md) — text format; relevance: the JSONL transcript stores markdown message bodies and compaction summaries as conversation content.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeat-safe writes; relevance: the per-store serialized writer + write-lock model (`session.writeLock.*`) makes concurrent store mutations safe.

**Docs**
- [Claude Code Sessions](../claude_code/cc_sessions.md) — session model; relevance: parallel session-list/continue model for a sibling agent.
- [Claude Code Manage Your Session](../claude_code/cc_manage_your_session.md) — session lifecycle ops; relevance: analog of reset/`/new`/idle lifecycle described here.
- [Claude Code SDK Session Store](../claude_code/cc_sdk_session_store.md) — pluggable session store; relevance: closest analog to the `sessions.json` key/value `sessionKey -> SessionEntry` store.
- [Claude Code SDK Session Management API](../claude_code/cc_sdk_session_management_api.md) — session read/write API; relevance: parallel of the bounded-tail vs full-scan transcript read model.
- [Claude Code Context Window Anatomy](../claude_code/cc_context_window_anatomy.md) — context budget structure; relevance: parallels "model context window vs store counters."
- [Pi Sessions](../pi/pi_sessions.md) — session concept; relevance: another coding agent's session abstraction for contrast.
- [Pi Session File Format](../pi/pi_session_file_format.md) — on-disk session JSONL; relevance: direct analog of OpenClaw's `<sessionId>.jsonl` tree-structured transcript (id+parentId entries).
- [Hermes Gateway Session Lifecycle / Internals](../hermes_agent/hermes_gateway_internals.md) — gateway-owned session state; relevance: parallel "gateway is source of truth" architecture.
- [Hermes Session Storage](../hermes_agent/hermes_session_storage.md) — on-disk session persistence layer; relevance: direct cross-stack analog of OpenClaw's `sessions.json` key/value store plus `<sessionId>.jsonl` transcript persistence.
- [oc_reference_session_management_compaction](oc_reference_session_management_compaction.md) (planned, this series) — compaction operation; relevance: the procedure that reads/writes this data model.

**Repos**
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store/transcript package; relevance: owns `src/config/sessions.ts`, `SessionEntry`, and `initSessionState()`.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory package; relevance: `memoryFlushAt`/`memoryFlushCompactionCount` store fields tie to memory-flush.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: the gateway-side session writer queue + read methods own the store.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: agent toggles/overrides (`thinkingLevel`, `modelOverride`, …) live in the store row.

**Snippets**
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — sessionId resolution; relevance: implements reset/idle/daily `sessionId` selection per `sessionKey`.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — sessionKey utilities; relevance: implements the `agent:<id>:...`/`cron:`/`hook:` key patterns.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: reset/idle/daily rollover behavior documented here.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript entry types; relevance: implements `message`/`custom_message`/`compaction`/`branch_summary` JSONL entries.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — chatType resolution; relevance: implements the `direct|group|room` `chatType` store field.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — per-session model overrides; relevance: implements `providerOverride`/`modelOverride`/`authProfileOverride` fields.
- [snippet_openclaw_sessions_level_overrides](../../code_snippets/snippet_openclaw_sessions_level_overrides.md) — per-session level toggles; relevance: implements `thinkingLevel`/`verboseLevel`/`reasoningLevel`/`elevatedLevel`.
- [snippet_openclaw_gateway_session_utils_store_target](../../code_snippets/snippet_openclaw_gateway_session_utils_store_target.md) — store-path resolution; relevance: implements the on-disk `sessions.json`/`--store` path logic.
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — store-row patch helpers; relevance: implements `updateSessionStore`/`updateSessionStoreEntry` serialized writes.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — async transcript index read; relevance: implements the cached-by-path+mtime full-scan transcript index.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — chat→session persistence; relevance: writes `lastInteractionAt`/token counters per turn.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input provenance tracking; relevance: distinguishes real user interaction from system events for idle freshness.

### oc_reference_session_management_compaction (10t · 12s · 10d)

**Terms**
- [Compaction](../../term_dictionary/term_compaction.md) — transcript summarization; relevance: the entire note is OpenClaw's compaction operation, settings, and troubleshooting.
- [Context Window](../../term_dictionary/term_context_window.md) — model token budget; relevance: threshold-maintenance fires when `contextTokens > contextWindow - reserveTokens`.
- [Tokenization](../../term_dictionary/term_tokenization.md) — token counting; relevance: `reserveTokens`/`keepRecentTokens`/`softThresholdTokens` are all token budgets.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — KV/prompt cache reuse; relevance: compaction rewrites the prefix, which is the cache-headroom tradeoff this note's settings tune.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: default summarization is an LLM call; `model` override routes the flush turn to a cheaper local model.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: these are OpenClaw runtime semantics (`/compact`, `openclaw status`, embedded-runner triggers).
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — periodic agentic turn; relevance: the pre-compaction memory flush is a silent agentic turn analogous to heartbeat housekeeping.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — transformer key/value cache; relevance: `reserveTokens` headroom and recent-tail preservation directly affect cache reuse cost.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — managing what enters context; relevance: chunk-boundary tool-pairing + recent-tail preservation are context-engineering rules.
- [Markdown](../../term_dictionary/term_markdown.md) — text format; relevance: the flush writes durable `memory/YYYY-MM-DD.md` markdown and the summary is markdown content.

**Docs**
- [Claude Code What Survives Compaction](../claude_code/cc_what_survives_compaction.md) — compaction retention rules; relevance: direct analog of "future turns see summary + messages after firstKeptEntryId."
- [Claude Code Reduce Token Usage](../claude_code/cc_reduce_token_usage.md) — token-budget tuning; relevance: parallel guidance for the compaction-spam troubleshooting (reserveTokens too high, pruning).
- [Claude Code Context Window Anatomy](../claude_code/cc_context_window_anatomy.md) — context budget structure; relevance: the `contextWindow - reserveTokens` threshold math.
- [Claude Code Extended Context (1M)](../claude_code/cc_extended_context_1m.md) — large context windows; relevance: larger windows change when threshold-maintenance compaction triggers.
- [Pi Compaction](../pi/pi_compaction.md) — compaction concept; relevance: another embedded-agent's compaction model for contrast.
- [Pi Compaction Extensions](../pi/pi_compaction_extensions.md) — pluggable compaction; relevance: direct analog of `registerCompactionProvider()` pluggable providers.
- [Hermes Context Compression & Caching](../hermes_agent/hermes_context_compression_caching.md) — conversation compression; relevance: parallel overflow-recovery + threshold-compression design.
- [Hermes Event Hooks](../hermes_agent/hermes_event_hooks.md) — lifecycle hooks; relevance: analog of the `session_before_compact` extension hook noted on this page.
- [oc_reference_session_management_store](oc_reference_session_management_store.md) (planned, this series) — session data model; relevance: the store/transcript model compaction reads and writes.
- [oc_reference_templates_workspace_lifecycle](oc_reference_templates_workspace_lifecycle.md) (planned, this series) — workspace rituals; relevance: shares the exact `NO_REPLY` silent-turn convention with BOOT.md/memory-flush.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime/compaction; relevance: owns `agent-settings.ts` compaction settings, chunk safety, mid-turn precheck.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/transcript package; relevance: the `compaction` transcript entry + `truncateAfterCompaction` successor rotation.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory package; relevance: the pre-compaction memory flush writes workspace memory.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin runtime; relevance: registers pluggable compaction providers and the safeguard extension.

**Snippets**
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — chunk tool-pairing safety; relevance: implements "keep tool call paired with its toolResult" boundary shifting.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — identifier preservation; relevance: the identifier-preservation policy passed to both built-in and plugin providers.
- [snippet_openclaw_agents_context_window_guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — context-pressure guard; relevance: implements the preflight/mid-turn precheck budget logic.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — `/compact` + reset handling; relevance: implements manual `/compact` and overflow-recovery session preservation.
- [snippet_openclaw_gateway_session_reset_mutation_perform](../../code_snippets/snippet_openclaw_gateway_session_reset_mutation_perform.md) — reset mutation; relevance: the `/new` path the troubleshooting checklist routes to when overflow recovery fails.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory write events; relevance: the durable memory writes the pre-compaction flush performs.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine; relevance: backs the `memory/YYYY-MM-DD.md` flush write path.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — cached prompt sections; relevance: AGENTS.md section reinjection after compaction (`postCompactionSections`).
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered streaming delta; relevance: implements draft/typing suppression when a chunk begins with `NO_REPLY`.
- [snippet_hermes_agent_core_conversation_compression_strategy](../../code_snippets/snippet_hermes_agent_core_conversation_compression_strategy.md) — compression strategy; relevance: cross-stack analog of staged summarization / re-distillation.
- [snippet_hermes_agent_core_conversation_loop_context_overflow](../../code_snippets/snippet_hermes_agent_core_conversation_loop_context_overflow.md) — overflow recovery; relevance: cross-stack analog of overflow-error → compact → retry.

### oc_reference_templates_claude_md (10t · 11s · 10d)

**Terms**
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — agent instruction file; relevance: this template IS the default `CLAUDE.md`/`AGENTS.md` workspace instruction file.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — periodic wake poll; relevance: the "Heartbeats — Be Proactive" section + heartbeat-vs-cron decision table.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: the heartbeat-vs-cron guidance ("exact timing → cron").
- [Persona](../../term_dictionary/term_persona.md) — agent personality/identity; relevance: "Make It Yours" + the memory/voice conventions define agent persona.
- [Markdown](../../term_dictionary/term_markdown.md) — text format; relevance: platform-formatting rules (no tables on Discord/WhatsApp, headers) are markdown conventions.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the template ships into an OpenClaw agent workspace.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — instruction design; relevance: the whole template is a system-prompt-scaffold (when to speak, react, escalate).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed agents; relevance: the "proactive work you can do without asking" + red-lines define autonomy bounds.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the "Tools — Skills provide your tools" section governs the tool/skill surface (MCP-backed).
- [Skills](../../term_dictionary/term_skills.md) — agent skill packages; relevance: "check its SKILL.md" + TOOLS.md notes reference the skills system.

**Docs**
- [Claude Code CLAUDE.md Files](../claude_code/cc_claude_md_files.md) — project instruction file; relevance: direct analog — the named `CLAUDE.md` instruction-file concept.
- [Claude Code Memory Overview](../claude_code/cc_memory_overview.md) — agent memory model; relevance: parallels the daily-notes + MEMORY.md long-term memory model.
- [Claude Code Auto Memory](../claude_code/cc_auto_memory.md) — automatic memory capture; relevance: analog of "Write It Down — no mental notes" capture discipline.
- [Claude Code Manage CLAUDE.md for Teams](../claude_code/cc_manage_claude_md_for_teams.md) — shared instruction files; relevance: the external-vs-internal + group-chat gating mirrors team-shared conventions.
- [Pi Skills](../pi/pi_skills.md) — skill system; relevance: parallels the Tools/Skills section's SKILL.md convention.
- [Hermes Context Files](../hermes_agent/hermes_context_files.md) — workspace context files; relevance: analog of AGENTS.md/SOUL.md/USER.md startup-context files.
- [Hermes Agent Loop](../hermes_agent/hermes_agent_loop.md) — agent run loop; relevance: the "session startup — use runtime-provided context first" rule is a loop-startup convention.
- [Hermes Personality / SOUL.md](../hermes_agent/hermes_personality_soul.md) — agent persona/voice file; relevance: direct analog of the template's "Make It Yours" + SOUL.md persona/voice conventions that shape how the agent speaks and behaves.
- [oc_reference_templates_agents_dev](oc_reference_templates_agents_dev.md) (planned, this series) — dev workspace template; relevance: sibling template with the same section skeleton plus a persona seed.
- [oc_reference_templates_workspace_lifecycle](oc_reference_templates_workspace_lifecycle.md) (planned, this series) — bootstrap/boot/heartbeat rituals; relevance: this template directly references BOOTSTRAP.md/BOOT.md/HEARTBEAT.md.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory package; relevance: implements the MEMORY.md/daily-notes read/write the template prescribes.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: loads AGENTS.md/SOUL.md/USER.md into startup context.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills package; relevance: backs the "Skills provide your tools / SKILL.md" convention.

**Snippets**
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — workspace root memory files; relevance: implements AGENTS.md/MEMORY.md/SOUL.md/USER.md file handling.
- [snippet_openclaw_memory_host_session_files_text](../../code_snippets/snippet_openclaw_memory_host_session_files_text.md) — session memory file text; relevance: implements daily `memory/YYYY-MM-DD.md` read/append.
- [snippet_openclaw_memory_host_session_files_classify](../../code_snippets/snippet_openclaw_memory_host_session_files_classify.md) — memory-file classification; relevance: distinguishes main-session-only MEMORY.md from shared-context files (security rule).
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity load; relevance: loads the workspace identity files this template defines.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — startup-context injection; relevance: implements "use runtime-provided startup context first."
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — system-prompt modes; relevance: main-session vs shared-context gating for MEMORY.md.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat delta streaming; relevance: implements the heartbeat poll the "Be Proactive" section responds to.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — channel emoji reactions; relevance: implements "React Like a Human" emoji-reaction behavior.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — per-session send policy; relevance: backs group-chat "know when to speak"/silence gating.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search; relevance: surfaces past daily notes for the memory-maintenance routine.

### oc_reference_templates_workspace_lifecycle (9t · 11s · 10d)

**Terms**
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — agent instruction file; relevance: BOOTSTRAP writes IDENTITY/USER/SOUL and BOOT/HEARTBEAT live beside AGENTS.md in the workspace.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — recurring wake checklist; relevance: HEARTBEAT.md is kept empty to skip heartbeat model calls (the note's third scaffold).
- [Persona](../../term_dictionary/term_persona.md) — agent identity/personality; relevance: BOOTSTRAP's "figure out who you are" ritual writes the persona (name/nature/vibe/emoji).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: BOOT.md enables `hooks.internal.enabled` and uses OpenClaw's `NO_REPLY` convention.
- [Markdown](../../term_dictionary/term_markdown.md) — text format; relevance: all three scaffolds are markdown checklist files read at startup/wake.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed agents; relevance: the create→boot→recurring-wake lifecycle is the agent's autonomous self-setup.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: HEARTBEAT.md tasks are the heartbeat alternative to cron for periodic checks.
- [Webhook](../../term_dictionary/term_webhook.md) — internal hooks; relevance: BOOT.md's `hooks.internal.enabled` gates the startup hook that runs the boot checklist.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — managing context cost; relevance: "keep HEARTBEAT.md small" is a token-budget rule for recurring-wake context.

**Docs**
- [Claude Code Routines Overview](../claude_code/cc_routines_overview.md) — scheduled agent routines; relevance: analog of the recurring-wake (heartbeat) ritual.
- [Claude Code Create Routine](../claude_code/cc_create_routine.md) — define a routine; relevance: parallels HEARTBEAT.md task authoring for periodic checks.
- [Claude Code CLAUDE.md Files](../claude_code/cc_claude_md_files.md) — instruction file; relevance: BOOTSTRAP/BOOT/HEARTBEAT are the lifecycle scaffolds the CLAUDE.md template references.
- [Claude Code Memory Overview](../claude_code/cc_memory_overview.md) — agent memory; relevance: BOOTSTRAP writes the initial identity/memory files (IDENTITY/USER/SOUL).
- [Pi Skills](../pi/pi_skills.md) — startup/skill conventions; relevance: contrast for first-run skill/tool setup.
- [Hermes Cron Scheduling](../hermes_agent/hermes_cron_scheduling.md) — scheduled jobs; relevance: the cron alternative to HEARTBEAT.md for precise schedules.
- [Hermes Context Files](../hermes_agent/hermes_context_files.md) — workspace files; relevance: analog of BOOTSTRAP-written identity files + startup file layout.
- [oc_reference_templates_claude_md](oc_reference_templates_claude_md.md) (planned, this series) — workspace instruction template; relevance: references BOOTSTRAP/BOOT/HEARTBEAT directly.
- [oc_reference_templates_agents_dev](oc_reference_templates_agents_dev.md) (planned, this series) — dev workspace template; relevance: its "First run" section follows the same BOOTSTRAP-then-delete ritual.
- [oc_reference_session_management_compaction](oc_reference_session_management_compaction.md) (planned, this series) — compaction/`NO_REPLY`; relevance: BOOT.md's silent-token convention is defined in that note.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: runs the first-run bootstrap budget + boot checklist.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory package; relevance: BOOTSTRAP/BOOT write the workspace identity/memory files.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding wizard; relevance: the wizard materializes these scaffold files into a fresh workspace.

**Snippets**
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — first-run bootstrap budget; relevance: implements the BOOTSTRAP first-run identity-creation turn.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap entry; relevance: the CLI path that triggers first-run bootstrap.
- [snippet_openclaw_gateway_agent_identity_reset](../../code_snippets/snippet_openclaw_gateway_agent_identity_reset.md) — identity reset; relevance: re-running the first-run ritual / clearing identity files.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat delta; relevance: implements the HEARTBEAT.md recurring-wake poll.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron/service wake notifications; relevance: the system-event wakes BOOT/HEARTBEAT respond to.
- [snippet_openclaw_gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — hooks config payload; relevance: implements `hooks.internal.enabled` that BOOT.md requires.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — internal hook handler; relevance: runs the BOOT.md startup checklist via the internal hook.
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — workspace root files; relevance: implements IDENTITY/USER/SOUL/AGENTS.md the BOOTSTRAP ritual writes.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config; relevance: scaffolds the workspace template files during onboarding.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard import step; relevance: materializes/imports the lifecycle scaffolds on first setup.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — startup context injection; relevance: injects the BOOT/HEARTBEAT checklist context at wake.

### oc_reference_templates_agents_dev (9t · 11s · 10d)

**Terms**
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — agent instruction file; relevance: AGENTS.dev.md IS the dev-gateway variant of the workspace AGENTS.md.
- [Persona](../../term_dictionary/term_persona.md) — agent identity/personality; relevance: the bundled "C-3PO Origin Memory" is a packaged persona seed.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — recurring wake checklist; relevance: the optional "Heartbeats" section ships a tiny HEARTBEAT.md checklist.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: this is the OpenClaw dev-gateway default agent identity template.
- [Markdown](../../term_dictionary/term_markdown.md) — text format; relevance: identity/daily-memory/SOUL files are markdown the template prescribes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed agents; relevance: the dev agent's safety defaults + "be concise, write to files" define autonomy bounds.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model; relevance: the dev gateway is a coding-agent shell typically backed by Claude (the C-3PO dev persona).
- [Zettelkasten](../../term_dictionary/term_zettelkasten.md) — atomic note/memory discipline; relevance: the "Daily memory" `memory/YYYY-MM-DD.md` durable-fact log is a zettel-style write-it-down memory practice.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — managing context cost; relevance: "read today + yesterday on start; keep HEARTBEAT small" are context-budget rules.

**Docs**
- [Claude Code CLAUDE.md Files](../claude_code/cc_claude_md_files.md) — instruction file; relevance: AGENTS.dev.md is a CLAUDE.md-class instruction file (dev variant).
- [Claude Code Memory Overview](../claude_code/cc_memory_overview.md) — agent memory; relevance: parallels the daily-memory log discipline.
- [Claude Code Create a Subagent](../claude_code/cc_create_a_subagent.md) — sub-agent identity; relevance: analog of defining a named agent identity/persona.
- [Pi Skills](../pi/pi_skills.md) — skill/customize conventions; relevance: contrast for the dev template's "Customize" section.
- [Hermes Context Files](../hermes_agent/hermes_context_files.md) — workspace context files; relevance: analog of IDENTITY.md/USER.md/SOUL.md identity files.
- [Hermes Creating Skill Format](../hermes_agent/hermes_creating_skill_format.md) — skill authoring; relevance: contrast for the dev agent's tool/skill conventions.
- [Band Agent Lifecycle](../band/band_agent_lifecycle.md) — agent identity/lifecycle; relevance: cross-stack analog of an agent's birth/identity setup.
- [Hermes Personality / SOUL.md](../hermes_agent/hermes_personality_soul.md) — agent persona/voice file; relevance: direct analog of the dev template's bundled "C-3PO Origin Memory" persona seed and SOUL.md identity file.
- [oc_reference_templates_claude_md](oc_reference_templates_claude_md.md) (planned, this series) — production workspace template; relevance: the prod counterpart to this dev template (same section skeleton).
- [oc_reference_templates_workspace_lifecycle](oc_reference_templates_workspace_lifecycle.md) (planned, this series) — first-run rituals; relevance: AGENTS.dev's "First run" references the BOOTSTRAP-then-delete ritual.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: loads the dev-agent identity files this template defines.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory package; relevance: implements the daily `memory/YYYY-MM-DD.md` log discipline.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app/dev-gateway shell; relevance: the dev gateway this template ships with.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding wizard; relevance: materializes the dev template into a fresh dev workspace.

**Snippets**
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity load; relevance: loads IDENTITY.md/USER.md the dev template defines.
- [snippet_openclaw_gateway_agent_identity_reset](../../code_snippets/snippet_openclaw_gateway_agent_identity_reset.md) — identity reset; relevance: re-seeding the dev-agent identity/persona.
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — workspace root files; relevance: implements AGENTS.md/IDENTITY/USER/SOUL handling for the dev workspace.
- [snippet_openclaw_memory_host_session_files_text](../../code_snippets/snippet_openclaw_memory_host_session_files_text.md) — daily memory file text; relevance: implements the `memory/YYYY-MM-DD.md` daily-log read/append.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — first-run bootstrap; relevance: the "First run — follow BOOTSTRAP then delete" ritual.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — startup context injection; relevance: injects the dev identity/daily-memory at session start.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool denial; relevance: enforces the "don't run destructive commands" safety default.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — untrusted-content handling; relevance: enforces "don't exfiltrate secrets/private data" safety default.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat delta; relevance: implements the optional heartbeat checklist run.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config; relevance: scaffolds the dev workspace template during onboarding.

> **DB-verify result (LOCKED set, 2026-06-21):** every EXISTING `note_id` cited above resolves in
> term_authentication, term_auth_profile, term_provider_plugin, term_third_party_genai_services, term_openclaw,
> term_reverse_proxy, term_pii, term_context_window, term_tokenization, term_compaction, term_cron,
> term_heartbeat, term_webhook, term_acp_agent_client_protocol, term_markdown, term_idempotency,
> term_prompt_caching, term_llm, term_kv_cache, term_context_engineering, term_persona, term_agents_md,
> term_prompt_engineering, term_autonomous_coding_agents, term_mcp, term_skills, term_claude,
> term_zettelkasten. Repos: repo_openclaw[_security|_gateway|_extensions|_extensions_llm_providers|_sessions|
> _memory|_agents|_skills|_apps|_cli_wizard]. Docs: cc_authentication, cc_mcp_authentication,
> cc_sdk_credential_and_filesystem_controls, cc_amazon_bedrock_setup, cc_environment_variables, cc_sessions,
> cc_manage_your_session, cc_sdk_session_store, cc_sdk_session_management_api, cc_context_window_anatomy,
> cc_what_survives_compaction, cc_reduce_token_usage, cc_extended_context_1m, cc_claude_md_files,
> cc_memory_overview, cc_auto_memory, cc_manage_claude_md_for_teams, cc_routines_overview, cc_create_routine,
> cc_create_a_subagent, pi_provider_auth, pi_sessions, pi_session_file_format, pi_compaction,
> pi_compaction_extensions, pi_skills, hermes_credential_pools, hermes_env_vars_providers_auth_tools,
> hermes_gateway_internals, hermes_context_compression_caching, hermes_event_hooks, hermes_context_files,
> hermes_agent_loop, hermes_cron_scheduling, hermes_creating_skill_format, hermes_security_isolation_credentials,
> hermes_session_storage, hermes_personality_soul, band_agent_lifecycle;
> term_secret_management, term_session, term_session_management, term_gateway, term_claude_md, term_token,
> term_agent_workspace, term_memory, term_agent_memory, term_system_prompt, term_git (verified MISSING →
> note 6 uses term_zettelkasten + term_claude in its place; term_git is MISSING and is NOT cited anywhere).

## Undigested Terms Plan

Per master design decision: OpenClaw vocabulary terms are the subjects of dedicated doc pages, so they are
digested as `oc_*` documentation concept notes by their home sub-plan, NOT as new `term_dictionary` entries. The
only `term_dictionary` interaction is linking existing terms. **Expect 0 new `term_dictionary` captures.**

| Term (appears in source) | Disposition |
|---|---|
| SecretRef / secret reference | OpenClaw vocab → digested in `oc_reference_secretref_credential_surface` (the page IS its definition); link existing `term_oauth_token`/`term_authentication`/`term_tls`. NOT a new term note. |
| `secrets configure` / `apply` / `audit` (secrets tooling) | OpenClaw CLI vocab → owned by the CLI sub-plan (`cli/secrets`, cl07) + gateway secrets (gw05 `gateway/secrets`); link, do not capture here. |
| auth profile (`auth-profiles.json`, oauth mode) | Link existing `term_auth_profile` + `term_oauth`; covered by `auth-credential-semantics` (rt01). NOT new. |
| sessionKey / sessionId / session store / transcript (JSONL) | OpenClaw vocab → digested in `oc_reference_session_management_store`; `term_session`/`term_session_management` do NOT exist but the concept is doc-page-owned (`/concepts/session`, co06) — NOT promoted to a new term note. |
| compaction / auto-compaction / overflow recovery | Link existing `term_compaction` + `term_context_window`; deeper concept owned by `/concepts/compaction` (co02). NOT new. |
| memory flush / `NO_REPLY` silent turn | OpenClaw runtime convention → digested in `oc_reference_session_management_compaction`; concept owned by `/concepts/memory` (co03). NOT new. |
| agent workspace / MEMORY.md / daily memory / SOUL / IDENTITY | OpenClaw workspace-file vocab → digested across notes 4/5/6; concept owned by `/concepts/agent-workspace` (co01); link existing `term_agents_md`. NOT new. |
| heartbeat (HEARTBEAT.md, heartbeat-vs-cron) | Link existing `term_heartbeat` + `term_cron`; config owned by `gateway/config-agents` (gw01). NOT new. |

**New-term candidates: NONE.** No genuinely cross-cutting, vault-reusable term lacking both a doc-page home AND
an existing note appears in these 7 pages. (The closest gap — a generic "secrets management" term — is owned by
the CLI/gateway secrets pages, not this Reference sub-plan, so it is not proposed here.) Augment Step 2d
re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** rf03 authors zero `term_dictionary` notes; it only links existing terms. Inherited from
to its `acronym_glossary_*.md`.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (6 notes, P2). The gate table is identical to the master's 9-GATE definition.

| Gate | Check | How |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` (YAML field order/forbidden fields, H1/`## Overview`/`## Related Notes`/`## References`/footer). |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/reference/<page>.md`; every claim traceable, no invented config keys/defaults. |
| G3 | Density + Coverage | ≤400 lines · ≤2,500 words · ≤6 code blocks · one BB per note; every mapped section present (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevancy-selected term links + repo_openclaw*/sibling oc_* + relevance statements per note. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` after incremental reindex. |
| G7/G8 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (in-degree ≥1, anti-island), satisfied via `entry_openclaw_docs.md` + repo/term inlinks (see Inlinks). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

All gates must PASS before commit.

## Validation Scripts

```bash
cd /path/to/vault
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_reference_secretref_credential_surface oc_reference_session_management_store oc_reference_session_management_compaction oc_reference_templates_claude_md oc_reference_templates_workspace_lifecycle oc_reference_templates_agents_dev"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required in frontmatter
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"; }
  # G3 density caps
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # G4 sibling/cross-ref presence
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING/CROSSREF ($SIBLING_PREFIX) in $n"
done

# YAML frontmatter sweep for the whole folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost / DB-verify a cited target resolves (note_name lookup, since note_id == relative path)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for id in term_openclaw term_compaction term_context_window term_oauth_token term_agents_md \
          repo_openclaw_sessions repo_openclaw_security snippet_openclaw_agents_compaction_chunk_safety; do
  r=$(sqlite3 "$DB" "SELECT note_name FROM notes WHERE note_name='$id'"); echo "$id => ${r:-GHOST}"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w / ≤6 code / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_reference_secretref_credential_surface | model | 550 | 0 | ✅ (source has 0 code; long bullet lists summarized, not reproduced verbatim) |
| 2 | oc_reference_session_management_store | model | 650 | 1 | ✅ |
| 3 | oc_reference_session_management_compaction | procedure | 700 | 2 | ✅ |
| 4 | oc_reference_templates_claude_md | model | 650 | 1 | ✅ |
| 5 | oc_reference_templates_workspace_lifecycle | procedure | 500 | 1 | ✅ |
| 6 | oc_reference_templates_agents_dev | model | 450 | 1 | ✅ |

No note approaches caps. The 3,055-word session page split (notes 2+3) and the consolidation of the three tiny
templates (note 5) keep every note ≤700w / ≤6 code blocks. The SecretRef page's long supported/unsupported
config-path lists are summarized by category (model-provider TLS/keys, channels, plugins, gateway, auth-profiles)
with representative examples — not reproduced as a 100-line bullet dump — to honor the density + atomicity caps.

## Entry Point Decision (inherited from master)

Contributes **6 rows** to `entry_openclaw_docs.md` (CREATED as master pre-step W1) under a **"Reference"**
section (sub-plan rf03 cluster: SecretRef surface, session store, session compaction, workspace templates). Each
new note receives its entry-point back-link at finalization (satisfies G7/G8 in-degree ≥1). Per master W2/W3,
(`term_openclaw`, `repo_openclaw`) are handled at the master/series level, not per-note here.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; each satisfies G7/G8 in-degree ≥1):

- `entry_openclaw_docs.md` (planned — master pre-step) → **all 6 notes** (primary anti-island guarantee).
- `repo_openclaw_security` → note 1 (SecretRef surface).
- `repo_openclaw_sessions` → notes 2, 3 (session store + compaction).
- `repo_openclaw_memory` → notes 3, 4, 5, 6 (memory flush + workspace memory templates).
- `repo_openclaw_agents` → notes 2, 3, 5, 6.
- `term_compaction` → notes 2, 3; `term_context_window` → notes 2, 3.
- `term_agents_md` → notes 4, 5, 6; `term_heartbeat` → notes 3, 4, 5, 6.
- `term_oauth_token` / `term_auth_profile` → note 1.

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Re-read each source page during execution; reproduce config keys /
defaults verbatim where quoted (don't paraphrase a default value). One BB per note. Cap dynamic-workflow fan-out
at ~30 agents/run. `git pull --rebase --autostash` first; commit+push after the phase (no Claude co-author
trailer). Reindex incrementally; verify `note_links` + 0 broken links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (status: ready) |

## Augmentation Report (2026-06-21)

**Scope:** xref-augment pass — replaced `## Candidate Cross-References` with `## Per-Note Related Notes
Mapping (LOCKED — xref-augment 2026-06-21)` at the RAISED FLOORS (≥8 terms · ≥10 code_snippets · ≥10 docs per
false-positives excluded; no padding (every link carries a why-THIS-note relevance statement).

**What was locked (per note, terms · snippets · docs):**

| Note | BB | terms | snippets | docs (existing / planned-sibling) | repos | floorsMet |
|---|---|---:|---:|---|---:|---|
| oc_reference_secretref_credential_surface | model | 10 | 11 | 10 (9 / 1) | 3 | ✅ |
| oc_reference_session_management_store | model | 10 | 12 | 10 (9 / 1) | 4 | ✅ |
| oc_reference_session_management_compaction | procedure | 10 | 12 | 10 (8 / 2) | 4 | ✅ |
| oc_reference_templates_claude_md | model | 10 | 11 | 10 (8 / 2) | 3 | ✅ |
| oc_reference_templates_workspace_lifecycle | procedure | 9 | 11 | 10 (7 / 3) | 3 | ✅ |
| oc_reference_templates_agents_dev | model | 9 | 11 | 10 (8 / 2) | 4 | ✅ |

- All 6 notes meet ALL floors (≥8t · ≥10s · ≥10d) and the ≥5-existing-docs rule (7–9 existing docs each).
- Docs floor uses the EXISTING claude_code (`cc_*`), pi (`pi_*`), hermes_agent (`hermes_*`), band (`band_*`)
  remainder toward 10, explicitly marked "(planned, this series)".
- **DB-verify:** every EXISTING cited `note_id` was confirmed by `note_name` lookup against

**Slug-collision / dedup re-confirm (Step 10.5f generalized):** all 6 planned `oc_*` slugs remain NEW (no
substantive `term_dictionary/` or `resources/documentation/` note covers the same concept under another name).
The OpenClaw vocab terms (SecretRef, sessionKey/sessionId, compaction, agent workspace, MEMORY.md, heartbeat,
NO_REPLY) are doc-page-owned and linked to EXISTING terms — not promoted to new `term_dictionary` entries (per
master design decision). Confirmed: `term_secrets`, `term_session`, `term_gateway`, `term_claude_md`,
`term_agent_workspace`, `term_memory`, `term_system_prompt` are MISSING and were NOT cited (excluded set).

**New-term candidates:** NONE. The xref re-scan surfaced no genuinely cross-cutting, vault-reusable term
lacking BOTH a doc-page home AND an existing note. Closest near-gap is a generic "secrets management" term —
owned by the CLI/gateway secrets pages (cl07/gw05), not this Reference sub-plan — so not proposed. (Best-fit
glossary, were it ever captured: `acronym_glossary_ai_agents.md` / `acronym_glossary_software_engineering.md`.)
Expected `term_dictionary` captures: **0** (consistent with the master Undigested-Terms design).

**Issues found + fixed during augment:** (1) initially cited `term_git` in note 6 toward its term floor —
note 6 lands at 9 valid terms. No other ghosts.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review of the augmented plan. CP7 source word counts re-measured against the local
mirror (`inbox/openclaw_docs/reference/*`) during this pass.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step ≥8 terms + floors | **PASS** | `## Per-Note Related Notes Mapping (LOCKED …)` present; all 6 notes ≥8 terms · ≥10 snippets · ≥10 docs; every link rendered `- [Name](relpath.md) — desc; relevance: …` with a per-link relevance statement (no bare links). |
| CP2 | 9-GATE present per batch | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present for the single P2 phase: G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect, G6 broken-link, G7/G8 discoverability. |
| CP4 | Size | **PASS** | 6 notes ≤30; single execution phase. |
| CP5 | Format derived | **PASS** | YAML field order + `# Title → ## Overview → body H2 → ## Related Notes → ## References → footer` inherited verbatim from master Format Definition, derived from existing `cc_*`/`pi_*` doc corpora (not invented). |
| CP6 | Density | **PASS** | `## Density Re-Assessment` — all notes ≤700w / ≤6 code / ≤400L; the 3,055w session page split (notes 2+3) and the BOOT+BOOTSTRAP+HEARTBEAT consolidation (note 5, 448w) keep every note well under caps. |
| CP7 | Sources measured | **PASS** | Re-measured mirror files 2026-06-21: secretref-credential-surface ≈580w (matches), session-management-compaction ≈3,055w (matches; split is correct), CLAUDE.md ≈1,284w, AGENTS.dev ≈475w, BOOT/BOOTSTRAP/HEARTBEAT 57/280/111w. All within ±30% of plan estimates; no under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present; 0 new `term_dictionary` captures (OpenClaw vocab is doc-page-owned per master); `## Term-Note Authoring Requirements` = N/A (0 new terms) with inherited multi-source mandate for any future term. |
| CP8f | Slug specificity / collision | **PASS** | All 6 `oc_*` slugs specific + NEW; collision audit (term_dictionary AND documentation/) found no substantive same-concept note under another name; excluded-MISSING term set recorded and not cited. |
| CP9 | Discoverability / inlinks | **PASS** | `## Inlinks (existing → new)` covers all 6 notes with ≥1 outside-folder inbound link (primary: `entry_openclaw_docs.md` → all 6; plus repo/term inlinks); G7/G8 in the phase gate table; in-degree ≥1 guaranteed. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
