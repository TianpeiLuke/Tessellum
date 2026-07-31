---
title: Sub-Plan pl03 — OpenClaw Docs: Plugins (copilot, dependency-resolution, google-meet, hooks, install-overrides, llama-cpp, manage-plugins)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
status_history:
  - "pending (planned 2026-06-20)"
  - "ready (xref-augmented + reviewed 2026-06-21)"
pages:
  - plugins/copilot
  - plugins/dependency-resolution
  - plugins/google-meet
  - plugins/hooks
  - plugins/install-overrides
  - plugins/llama-cpp
  - plugins/manage-plugins
---

# Sub-Plan pl03: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format/YAML, dedup (3-way across term_dictionary
> + documentation + repo_openclaw\*), the 9-GATE table, cross-refs, undigested-terms ownership, and entry-point
> (`entry_openclaw_docs.md`) decisions are ALL inherited from the master. This file locks the per-page section
> map, planned notes, split decisions, and candidate cross-references from a fresh re-read + `wc -w` of the 7
> assigned mirror pages. Augment/review/execute follow per the master pipeline.

## Scope

The 7 mixed-topic Plugins pages NOT in the `plugins/reference/*` provider/channel grid (those are pl05–pl23):
an alternate **agent runtime** (Copilot SDK harness), the **plugin loading/dependency model** (install roots,
local plugins, startup/reload, bundled vs legacy), a heavyweight **integration plugin** (Google Meet
participant support via Chrome/Twilio with realtime voice), the **hook system** (lifecycle/tool/message/model
hooks), **install overrides** (E2E/package testing), the **llama.cpp local-embeddings provider plugin**, and
**plugin management** CLI quick-reference. Priority **P3** (Phase C — plugin sprawl), but several of these
(dependency-resolution, hooks, manage-plugins) are conceptually load-bearing for the rest of the plugin corpus,
so they are prioritized within the sub-plan. The code-side counterparts (`repo_openclaw_extensions`,
`repo_openclaw_extensions_voice_speech`, `repo_openclaw_memory`, `repo_openclaw_gateway`) are LINKED, not
recreated.

**Source**: OpenClaw docs, 7 pages, **16,729 measured words**. **Planned: 11 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| copilot | plugins/copilot | 2,201 | 2 | 13 | 1 | procedure |
| dependency-resolution | plugins/dependency-resolution | 1,101 | 4 | 6 | 0 | concept |
| google-meet | plugins/google-meet | 8,511 | 84 | 11 | 13 | procedure (SPLIT ×4) |
| hooks | plugins/hooks | 3,280 | 5 | 10 | 3 | procedure (SPLIT ×2) |
| install-overrides | plugins/install-overrides | 374 | 3 | 3 | 0 | procedure |
| llama-cpp | plugins/llama-cpp | 207 | 3 | 2 | 0 | procedure |
| manage-plugins | plugins/manage-plugins | 1,055 | 10 | 7 | 0 | procedure |

Code = `(grep -c '```') / 2` (fence pairs). Words = raw `wc -w` of the full file (frontmatter included; ~10–30w
of frontmatter per page is negligible at these sizes).

## Content Strategy

- **Prioritize**: the **plugin loading/dependency model** (dependency-resolution — every other plugin page
  assumes install roots / startup-reload / bundled-vs-local semantics) and the **hook catalog** (hooks — the
  extensibility contract many tools/channels reference). These two are the conceptual backbone of the section.
- **Split**: `google-meet.md` (8,511w / 84 fences — **3.4× the 2,500w cap and 14× the 6-code cap**) splits into
  4 task-cluster notes (overview+quickstart+transports, OAuth/preflight/config, tool+agent/bidi modes,
  troubleshooting+notes). `hooks.md` (3,280w — over the 2,500w cap) splits into 2 notes (catalog of hook types
  vs install/gateway-lifecycle/deprecations). Each resulting note stays ≤6 code blocks (config/CLI snippets
  reproduced selectively, verbatim) and one building_block.
- **Link-out (do NOT redefine here)**: `openclaw plugins install/list/enable` full command contract → CLI
  sub-plans (cl06 `cli/plugins`); plugin manifest schema → pl04 (`plugins/manifest`); plugin SDK / building
  plugins → pl01/pl23–25; provider config (Copilot model, realtime voice providers) → pr0x (providers);
  memory-search internals → co03/co04 (concepts/memory\*); voice-call plugin → pl21/pl25 (`plugins/voice-call`).
  Existing terms (`term_oauth`, `term_oauth_token`, `term_mcp`, `term_function_calling`, `term_compaction`,
  `term_vector_database`, `term_embedding`) are LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_copilot.md` | procedure | copilot.md: all 13 H2 (Requirements, Plugin install, Quickstart, Supported providers, Auth + Session-level GitHub token, Configuration surface, Compaction, Transcript mirroring, Side questions /btw, Doctor and probes, Limitations, Permissions and ask_user) | 650 | The external `@openclaw/copilot` SDK-harness runtime: installing the plugin, opting an agent into `agentRuntime.id: "copilot"`, supported subscription providers, GitHub-token/auth, the OpenClaw-vs-Copilot ownership split (channels/sessions vs agent loop/compaction), transcript mirroring, `/btw`, doctor probes, and limitations. |
| 2 | `oc_plugins_dependency_resolution.md` | concept | dependency-resolution.md: all 6 H2 (Responsibility split, Install roots, Local plugins, Startup and reload, Bundled plugins, Legacy cleanup) | 600 | OpenClaw's plugin dependency/loading model: which layer owns install vs runtime resolution, the install-root layout, how local (path) plugins resolve, startup/reload re-resolution, bundled-plugin shipping, and legacy-install cleanup. |
| 3 | `oc_plugins_google_meet_overview.md` | procedure | google-meet.md: lead + Quick start, Install notes, Transports (Chrome, Twilio) | 700 | Google Meet participant plugin overview: explicit-URL/create-space design, BlackHole/SoX audio prerequisites, enabling the plugin, `googlemeet setup/join/create`, the four modes (agent/bidi/transcribe), and the Chrome vs Twilio transports. |
| 4 | `oc_plugins_google_meet_oauth_config.md` | procedure | google-meet.md: OAuth and preflight (Create Google credentials, Mint the refresh token, Verify OAuth with doctor) + Config | 650 | Authenticating Google Meet: creating Google OAuth credentials, the `meetings.space.settings` scope, minting/storing the refresh token, `googlemeet auth login`, doctor preflight verification, and the plugin `config` block (transports, chrome/chromeNode, realtime). |
| 5 | `oc_plugins_google_meet_agent_modes.md` | procedure | google-meet.md: Tool, Agent and bidi modes, Live test checklist | 650 | The agent-facing `google_meet` tool and join behavior: `agent` (transcription + OpenClaw agent + TTS talk-back), `bidi` (direct realtime voice), and `transcribe` (observe-only) modes, the realtime audio bridge / caption observer, manual-action reporting, and the live-test checklist. |
| 6 | `oc_plugins_google_meet_troubleshooting.md` | procedure | google-meet.md: Local gateway + Parallels Chrome (under Quick start), Troubleshooting (all 8 H3 symptoms), Notes | 600 | Operating Google Meet across a node host: the Parallels-Chrome node split, `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS`, node pairing/allowCommands, and the symptom→fix troubleshooting matrix (tool not visible, no capable node, browser can't join, creation fails, no talk-back, Twilio checks/dial-in failures). |
| 7 | `oc_plugins_hooks_catalog.md` | procedure | hooks.md: Quick start, Hook catalog, Debug runtime hooks (+ Exec environment hook, Tool result persistence, Session extensions H3), Tool call policy, Prompt and model hooks, Message hooks | 700 | The OpenClaw hook catalog: registering hooks, the per-phase hook types (exec-environment, tool-call policy, tool-result persistence, prompt/model, message, session-extension/next-turn-injection), their payloads, and how each phase mutates or gates a turn. |
| 8 | `oc_plugins_hooks_lifecycle_install.md` | procedure | hooks.md: Install hooks, Gateway lifecycle, Upcoming deprecations | 500 | Installing hooks and the gateway-lifecycle hook points: where install/lifecycle hooks fire during plugin setup and gateway start/stop/reload, plus the upcoming hook deprecations to migrate away from. |
| 9 | `oc_plugins_install_overrides.md` | procedure | install-overrides.md: all 3 H2 (Environment, Behavior, Package E2E) | 400 | Plugin install overrides for E2E/package testing: the `OPENCLAW_ALLOW_PLUGIN_INSTALL_OVERRIDES` + `OPENCLAW_PLUGIN_INSTALL_OVERRIDES` env vars, the `npm:`/`npm-pack:` override-map values, id-enforcement and trust caveats, and the isolated-state-dir package E2E flow. |
| 10 | `oc_plugins_llama_cpp.md` | procedure | llama-cpp.md: lead + Configuration, Native Runtime | 350 | The official `@openclaw/llama-cpp-provider` plugin for local GGUF memory embeddings: installing it (owns the `node-llama-cpp` runtime), pointing `memorySearch.provider: "local"` at a GGUF model, and the native-runtime build steps (Node 24, pnpm approve/rebuild). |
| 11 | `oc_plugins_manage_plugins.md` | procedure | manage-plugins.md: all 7 H2 (List and search, Install, Restart and inspect, Update, Uninstall, Choose a source, Publish) | 550 | Plugin management quick-reference: `openclaw plugins list/search/install/update/uninstall`, restart-and-inspect after install, choosing an install source (ClawHub/npm/git/local), and the pointer to publishing — the everyday command surface (full contract linked to `cli/plugins`). |

## Section Coverage Map

```
copilot.md
├── (lead: @openclaw/copilot harness, OpenClaw-vs-Copilot split) → note 1 (oc_plugins_copilot)
├── Requirements ─────────────────────────────────────────────── → note 1
├── Plugin install ───────────────────────────────────────────── → note 1
├── Quickstart ───────────────────────────────────────────────── → note 1
├── Supported providers ──────────────────────────────────────── → note 1
├── Auth (+ ### Session-level GitHub token) ──────────────────── → note 1
├── Configuration surface ────────────────────────────────────── → note 1
├── Compaction ───────────────────────────────────────────────── → note 1
├── Transcript mirroring ─────────────────────────────────────── → note 1
├── Side questions (/btw) ────────────────────────────────────── → note 1
├── Doctor and probes ────────────────────────────────────────── → note 1
├── Limitations ──────────────────────────────────────────────── → note 1
└── Permissions and ask_user ─────────────────────────────────── → note 1
dependency-resolution.md
├── Responsibility split ─────────────────────────────────────── → note 2 (oc_plugins_dependency_resolution)
├── Install roots ────────────────────────────────────────────── → note 2
├── Local plugins ────────────────────────────────────────────── → note 2
├── Startup and reload ───────────────────────────────────────── → note 2
├── Bundled plugins ──────────────────────────────────────────── → note 2
└── Legacy cleanup ───────────────────────────────────────────── → note 2
google-meet.md
├── (lead: explicit design / modes / transports) ─────────────── → note 3 (oc_plugins_google_meet_overview)
├── Quick start ──────────────────────────────────────────────── → note 3
│   └── ### Local gateway + Parallels Chrome ─────────────────── → note 6 (operate-across-node; troubleshooting)
├── Install notes ────────────────────────────────────────────── → note 3
├── Transports (### Chrome, ### Twilio) ──────────────────────── → note 3
├── OAuth and preflight ──────────────────────────────────────── → note 4 (oc_plugins_google_meet_oauth_config)
│   ├── ### Create Google credentials ────────────────────────── → note 4
│   ├── ### Mint the refresh token ───────────────────────────── → note 4
│   └── ### Verify OAuth with doctor ─────────────────────────── → note 4
├── Config ───────────────────────────────────────────────────── → note 4
├── Tool ─────────────────────────────────────────────────────── → note 5 (oc_plugins_google_meet_agent_modes)
├── Agent and bidi modes ─────────────────────────────────────── → note 5
├── Live test checklist ──────────────────────────────────────── → note 5
├── Troubleshooting (8 × H3 symptoms) ────────────────────────── → note 6 (oc_plugins_google_meet_troubleshooting)
│   ├── ### Agent cannot see the Google Meet tool ────────────── → note 6
│   ├── ### No connected Google Meet-capable node ────────────── → note 6
│   ├── ### Browser opens but agent cannot join ──────────────── → note 6
│   ├── ### Meeting creation fails ───────────────────────────── → note 6
│   ├── ### Agent joins but does not talk ────────────────────── → note 6
│   ├── ### Twilio setup checks fail ─────────────────────────── → note 6
│   └── ### Twilio call starts but never enters the meeting ──── → note 6
├── Notes ────────────────────────────────────────────────────── → note 6
└── Related (pointers only) ──────────────────────────────────── → notes 3–6 Related Notes / References
hooks.md
├── Quick start ──────────────────────────────────────────────── → note 7 (oc_plugins_hooks_catalog)
├── Hook catalog ─────────────────────────────────────────────── → note 7
├── Debug runtime hooks ──────────────────────────────────────── → note 7
│   ├── ### Exec environment hook ────────────────────────────── → note 7
│   ├── ### Tool result persistence ──────────────────────────── → note 7
│   └── ### Session extensions and next-turn injections ──────── → note 7
├── Tool call policy ─────────────────────────────────────────── → note 7
├── Prompt and model hooks ───────────────────────────────────── → note 7
├── Message hooks ────────────────────────────────────────────── → note 7
├── Install hooks ────────────────────────────────────────────── → note 8 (oc_plugins_hooks_lifecycle_install)
├── Gateway lifecycle ────────────────────────────────────────── → note 8
├── Upcoming deprecations ────────────────────────────────────── → note 8
└── Related (pointers only) ──────────────────────────────────── → notes 7–8 Related Notes / References
install-overrides.md
├── (lead: maintainer E2E test installs) ─────────────────────── → note 9 (oc_plugins_install_overrides)
├── Environment ──────────────────────────────────────────────── → note 9
├── Behavior ─────────────────────────────────────────────────── → note 9
└── Package E2E ──────────────────────────────────────────────── → note 9
llama-cpp.md
├── (lead: official local-GGUF-embeddings provider plugin) ───── → note 10 (oc_plugins_llama_cpp)
├── Configuration ────────────────────────────────────────────── → note 10
└── Native Runtime ───────────────────────────────────────────── → note 10
manage-plugins.md
├── List and search plugins ──────────────────────────────────── → note 11 (oc_plugins_manage_plugins)
├── Install plugins ──────────────────────────────────────────── → note 11
├── Restart and inspect ──────────────────────────────────────── → note 11
├── Update plugins ───────────────────────────────────────────── → note 11
├── Uninstall plugins ────────────────────────────────────────── → note 11
├── Choose a source ──────────────────────────────────────────── → note 11
├── Publish plugins ──────────────────────────────────────────── → note 11
└── Related (pointers only) ──────────────────────────────────── → note 11 Related Notes / References
```
No orphaned sections. The `## Related` sections on copilot/google-meet/hooks/manage-plugins pages are docs-site
cross-links (e.g. `cli/plugins`, `concepts/agent-runtimes`, `plugins/voice-call`); they become Related Notes /
References pointers, not standalone notes. Command/manifest/SDK details link out per Content Strategy.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| google-meet.md (8,511w · 84 fences · 11 H2 / 13 H3) | notes 3 + 4 + 5 + 6 | **3.4× the 2,500w word cap and 14× the 6-code cap** — far too large for one note. Splits along four distinct task clusters: (3) overview + install + transports, (4) Google OAuth credential setup + plugin config, (5) the agent-facing tool + agent/bidi/transcribe modes + live test, (6) node-host operation (Parallels Chrome) + troubleshooting matrix + notes. Each child ≤700w, ≤6 code blocks, single procedure BB; verbatim config/CLI snippets distributed across children. |
| hooks.md (3,280w · 5 fences · 10 H2 / 3 H3) | notes 7 + 8 | Over the 2,500w cap. Split: (7) the hook **catalog** — the per-phase hook types and payloads (exec/tool-policy/tool-result/prompt-model/message/session) an extension author registers; (8) **install + gateway-lifecycle hooks + upcoming deprecations** — a smaller operational cluster. Keeps each focused and ≤700w. |
| copilot.md (2,201w · 13 H2) | note 1 (no split) | Within the 2,500w cap, only 2 code fences, single procedure BB (configure an agent runtime). 13 short H2 sections cohere as one "use the Copilot harness" procedure. |
| dependency-resolution.md (1,101w) | note 2 (no split) | Within caps; one concept (the loading/resolution model). |
| install-overrides.md (374w) / llama-cpp.md (207w) / manage-plugins.md (1,055w) | notes 9 / 10 / 11 (no split) | All well within caps; each a single-procedure reference page. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (16,729 measured words). New `oc_` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×10** (notes 1, 3–11) · **concept ×1** (note 2, dependency-resolution model).
- Est. digest words ≈ **6,350** (avg ~577/note; min 350 llama-cpp, max 700 copilot/google-meet-overview/hooks-catalog).
  All 11 notes ≤700w, ≤6 code blocks (the 84 google-meet + 10 manage-plugins source fences distribute across the
  split notes; only the most load-bearing config/CLI snippets are reproduced verbatim).
- Cross-refs (LOCKED at xref-augment 2026-06-21; raised floors = **≥8 relevance-selected term_dictionary terms ·
  `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`. Every EXISTING cited target was

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

series marked "(planned, this series)"), PLUS relevant `repo_openclaw*` and sibling `oc_*`. Every EXISTING
positives discarded, no padding. Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`:
terms `../../term_dictionary/term_Y.md`; sibling oc `oc_Y.md`; cc/pi/hermes/band doc `../<folder>/<file>.md`;
repo `../../../areas/code_repos/repo_Y.md`; snippet `../../code_snippets/snippet_Y.md`; entry
`../../../0_entry_points/entry_Y.md`.

### oc_plugins_copilot (8t · 10s · 10d)

**Terms**
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — pluggable agent-execution-loop abstraction; relevance: this page IS the "Copilot SDK harness" vs the built-in PI harness split.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding-agent runtimes; relevance: the Copilot CLI is an alternate coding-agent runtime OpenClaw drives.
- [term_claude_code](../../term_dictionary/term_claude_code.md) — Anthropic's coding-agent CLI; relevance: directly analogous external-agent runtime wired through a harness/SDK.
- [term_pi_agent](../../term_dictionary/term_pi_agent.md) — OpenClaw's built-in PI harness; relevance: the harness Copilot replaces per attempt; `/btw` falls back to PI.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — bearer/refresh credential; relevance: `gitHubToken` / `COPILOT_GITHUB_TOKEN` env + auth-profile `resolvedApiKey` drive headless auth.
- [term_oauth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: subscription Copilot login + `github-copilot:<profile>` auth profile resolution.
- [term_compaction](../../term_dictionary/term_compaction.md) — session-history shrinking; relevance: the Copilot SDK owns native `infiniteSessions` compaction inside the loop.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model-invoked tools; relevance: bridged OpenClaw tools (`overridesBuiltInTool`/`skipPermission`) flow through the wrapped `execute()`.

**Docs**
- [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — Claude Code SDK plugin model; relevance: external-agent SDK plugin packaging analog for `@openclaw/copilot`.
- [cc_agent_sdk_overview](../claude_code/cc_agent_sdk_overview.md) — embedding an agent via an SDK; relevance: the same "drive an external agent loop through an SDK" pattern.
- [cc_headless_mode](../claude_code/cc_headless_mode.md) — non-interactive/headless agent runs; relevance: Copilot harness targets headless/cron runs via `gitHubToken`.
- [pi_sdk_overview](../pi/pi_sdk_overview.md) — PI agent SDK surface; relevance: the in-tree PI harness Copilot competes with / falls back to.
- [pi_provider_auth](../pi/pi_provider_auth.md) — PI provider auth resolution; relevance: the `github-copilot` provider auth precedence the harness mirrors.
- [pi_compaction_extensions](../pi/pi_compaction_extensions.md) — PI compaction hook extensions; relevance: contrast OpenClaw `before/after_compaction` vs the SDK-owned compaction.
- [band_adapter_codex](../band/band_adapter_codex.md) — an external-CLI agent adapter (Codex); relevance: the codex harness is the documented sibling pattern Copilot mirrors (approval bridge, dynamic tools).
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — deploying coding-agent runtimes; relevance: operational deployment of an alternate agent runtime.
- [oc_plugins_dependency_resolution](oc_plugins_dependency_resolution.md) (planned, this series) — how the external plugin installs/loads; relevance: `@openclaw/copilot` resolves SDK via per-plugin npm root.
- [oc_plugins_manage_plugins](oc_plugins_manage_plugins.md) (planned, this series) — installing/inspecting plugins; relevance: `openclaw plugins install @openclaw/copilot`.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: hosts `extensions/copilot/*` (harness, doctor, tool-bridge).
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime selection; relevance: `agentRuntime.id: "copilot"` opt-in + `selection.ts` auto_pi fallback.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/transcript ownership; relevance: OpenClaw owns the audit transcript mirror while Copilot owns thread state.

**Snippets**
- [snippet_hermes_agent_cli_copilot_auth](../../code_snippets/snippet_hermes_agent_cli_copilot_auth.md) — GitHub Copilot subscription auth flow; relevance: the exact `gitHubToken`/login resolution this page documents.
- [snippet_hermes_agent_plugins_provider_copilot](../../code_snippets/snippet_hermes_agent_plugins_provider_copilot.md) — Copilot provider plugin impl; relevance: the `github-copilot` provider the harness claims.
- [snippet_hermes_agent_core_codex_runtime](../../code_snippets/snippet_hermes_agent_core_codex_runtime.md) — external-CLI agent runtime; relevance: codex-style runtime analog Copilot follows.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime selection config; relevance: how a model/provider is pinned to a runtime.
- [snippet_hermes_agent_core_runtime_helpers_switch_client](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_switch_client.md) — switching the active runtime client; relevance: per-attempt runtime routing.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — resolving API/runtime mode at init; relevance: the auto_pi-vs-copilot decision.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: `resolveProviderAuths` precedence the harness consumes.
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — `/btw` harness/transcript path; relevance: `/btw` PI fallback + transcript mirror behavior.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction identifier handoff; relevance: SDK compaction returning outcomes to OpenClaw.
- [snippet_openclaw_agents_model_fallback_observation](../../code_snippets/snippet_openclaw_agents_model_fallback_observation.md) — model-fallback observation; relevance: the supported-provider fall-through back to PI.

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned hub).

### oc_plugins_dependency_resolution (8t · 10s · 10d)

**Terms**
- [term_npm](../../term_dictionary/term_npm.md) — Node package manager/registry; relevance: install roots run `npm install` in per-plugin project roots; `npm-pack:` tarballs, shrinkwrap, bundledDependencies.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node runtime + module resolution; relevance: package-local + parent `node_modules` resolution underlies plugin loading.
- [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — plugin manifest/metadata; relevance: `openclaw.extensions` entrypoint + `publishToNpm`/`bundleRuntimeDependencies` flags.
- [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin SDK; relevance: plugins importing `openclaw/plugin-sdk/*` declare `openclaw` as a peer dependency.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider-type plugins; relevance: native-heavy provider/runtime packages (Codex, ACP) opt out of bundling.
- [term_npm_scoping](../../term_dictionary/term_npm_scoping.md) — scoped npm packages; relevance: `@openclaw/<pkg>` scope + per-plugin `~/.openclaw/npm/projects/<encoded-package>` roots.
- [term_dependency_confusion](../../term_dictionary/term_dependency_confusion.md) — registry-confusion supply-chain risk; relevance: why OpenClaw blocks a separate registry copy of the host peer and reasserts plugin-local `node_modules/openclaw`.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the host product; relevance: the loading/resolution model documented is OpenClaw's.

**Docs**
- [cc_plugin_dependencies](../claude_code/cc_plugin_dependencies.md) — Claude Code plugin dependency handling; relevance: the closest cross-tool analog (install-time dependency ownership).
- [cc_sdk_plugin_structure](../claude_code/cc_sdk_plugin_structure.md) — plugin package layout; relevance: install-root / entrypoint resolution analog.
- [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — npm/git/local plugin sources; relevance: the per-source root model (npm vs git vs local/path).
- [cc_plugin_directory_structure](../claude_code/cc_plugin_directory_structure.md) — on-disk plugin layout; relevance: managed install dirs + cleanup boundary.
- [pi_packages](../pi/pi_packages.md) — PI package/dependency model; relevance: peer/bundled-dependency semantics analog.
- [pi_extensions_overview](../pi/pi_extensions_overview.md) — PI extension loading; relevance: discover→install→record→load lifecycle analog.
- [hermes_agent/hermes_plugin_extensions_hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — Hermes plugin/extension model; relevance: bundled-vs-downloadable plugin shipping analog.
- [hermes_agent/hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — building a plugin package; relevance: package `dependencies`/peer declaration in practice.
- [oc_plugins_manage_plugins](oc_plugins_manage_plugins.md) (planned, this series) — the CLI that triggers install/update; relevance: `openclaw plugins install/update` is the explicit-request entry to resolution.
- [oc_plugins_llama_cpp](oc_plugins_llama_cpp.md) (planned, this series) — a native-dep plugin kept out of core; relevance: the canonical "why a native dep lives in a plugin to survive npm updates" example.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension loading subsystem; relevance: discover/install/record/load lifecycle owner.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: startup/reload read install records + load entrypoints (no package-manager runs).
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — packaged apps / bundled shipping; relevance: bundled-plugin packaging in `npm install -g openclaw`.

**Snippets**
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: read records → compute entrypoint → load.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — config→plugins resolution; relevance: config references resolved to plugin sources.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — reload-plan computation; relevance: config reload re-resolution without installing.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — reload apply; relevance: startup/reload load of updated plugin set.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — install-root package contract; relevance: per-plugin project root + manifest expectations.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load lifecycle; relevance: install→record→load→fail-actionable phases.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: peer/SDK-import boundary analog.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: `definePluginEntry`/entrypoint resolution.
- [snippet_hermes_agent_tools_lazy_deps](../../code_snippets/snippet_hermes_agent_tools_lazy_deps.md) — lazy/optional dependency loading; relevance: `optionalDependencies` + actionable missing-dep errors.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard setup-time imports; relevance: wizard installs the plugin at first-use (the explicit-request path).

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned), [entry_code_repos](../../../0_entry_points/entry_code_repos.md) (code-side cross-link).

### oc_plugins_google_meet_overview (8t · 10s · 10d)

**Terms**
- [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — TTS synthesis; relevance: regular OpenClaw TTS speaks the agent answer into Meet.
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — STT/ASR; relevance: realtime transcription listens to meeting audio.
- [term_realtime_transcription](../../term_dictionary/term_realtime_transcription.md) — streaming live transcription; relevance: OpenAI default transcription provider drives `agent` mode.
- [term_voice_call](../../term_dictionary/term_voice_call.md) — voice-call subsystem; relevance: Twilio transport reuses the voice-call plugin / shared consult machinery.
- [term_homebrew](../../term_dictionary/term_homebrew.md) — macOS package manager; relevance: `brew install blackhole-2ch sox` host audio prerequisites.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — host product; relevance: the participant plugin runs in OpenClaw.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: the `googlemeet` CLI vs the agent-facing `google_meet` tool.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: the configured OpenClaw agent answers in `agent` mode.

**Docs**
- [hermes_agent/hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — agent voice-mode guide; relevance: the join/listen/talk-back model analog.
- [hermes_agent/hermes_voice_gateway_discord_vc](../hermes_agent/hermes_voice_gateway_discord_vc.md) — agent in a voice channel; relevance: directly analogous "agent joins a live call" integration.
- [hermes_agent/hermes_messaging_teams_meetings_pipeline](../hermes_agent/hermes_messaging_teams_meetings_pipeline.md) — Teams meetings pipeline; relevance: another meeting-participant integration analog.
- [hermes_agent/hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — TTS providers; relevance: the OpenClaw TTS runtime the talk-back uses.
- [hermes_agent/hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — STT/transcription providers; relevance: realtime transcription provider config.
- [hermes_agent/hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — browser automation setup; relevance: Chrome transport joins through a signed-in Chrome profile.
- [oc_plugins_google_meet_oauth_config](oc_plugins_google_meet_oauth_config.md) (planned, this series) — OAuth + plugin config; relevance: the create-space API path needs OAuth.
- [oc_plugins_google_meet_agent_modes](oc_plugins_google_meet_agent_modes.md) (planned, this series) — the agent/bidi/transcribe modes; relevance: this overview defines the modes detailed there.
- [oc_plugins_google_meet_troubleshooting](oc_plugins_google_meet_troubleshooting.md) (planned, this series) — node/transport troubleshooting; relevance: operating across a node host.
- [oc_plugins_manage_plugins](oc_plugins_manage_plugins.md) (planned, this series) — enabling/installing the plugin; relevance: `plugins.entries.google-meet` enablement.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension subsystem; relevance: realtime audio bridge + TTS/STT.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — Twilio/phone transport; relevance: the Twilio dial-in transport.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework; relevance: hosts the google-meet plugin.

**Snippets**
- [snippet_hermes_agent_plugins_google_meet](../../code_snippets/snippet_hermes_agent_plugins_google_meet.md) — Google Meet plugin impl; relevance: the directly-analogous Meet plugin implementation.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-call manager; relevance: voice-call/Twilio delegation the plugin reuses.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: shared realtime call runtime.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — TTS provider bridge; relevance: the speak-into-Meet end of the bridge.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — STT provider bridge; relevance: the listen end of the bridge.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech audio pipeline; relevance: the BlackHole/SoX audio pipeline.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: agent talk-back-in-a-call analog.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: realtime transcription wiring.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local TTS engine; relevance: a TTS backend option for the talk-back path.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: OpenAI is the default transcription provider (`OPENAI_API_KEY`).

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned).

### oc_plugins_google_meet_oauth_config (8t · 10s · 10d)

**Terms**
- [term_oauth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: the Google OAuth consent-screen + scopes flow.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — refresh/access token; relevance: the minted refresh token + `expiresAt` access-token lifecycle.
- [term_pkce](../../term_dictionary/term_pkce.md) — Proof Key for Code Exchange; relevance: `googlemeet auth login` uses PKCE + localhost callback.
- [term_authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the auth step gating create-space / Media API preflight.
- [term_auth_profile](../../term_dictionary/term_auth_profile.md) — stored credential profile; relevance: config-vs-env resolution of the `oauth` block.
- [term_credential_pool](../../term_dictionary/term_credential_pool.md) — credential resolution pool; relevance: config-first then env fallback for client id/secret/refresh.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — host product; relevance: the Google Meet plugin config lives in OpenClaw.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — machine-readable tool output; relevance: `googlemeet auth login --json` / `doctor --oauth --json` agent-readable output.

**Docs**
- [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — OAuth login/refresh for a connector; relevance: direct analog of minting + storing a refresh token for an external API.
- [cc_authentication](../claude_code/cc_authentication.md) — auth setup; relevance: client-id/secret + token-store conventions analog.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login/auth troubleshooting; relevance: doctor-style preflight verification analog.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth resolution; relevance: config-vs-env credential precedence analog.
- [hermes_agent/hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — OAuth with manual/remote callback; relevance: `--manual` copy/paste flow when the browser can't reach localhost.
- [hermes_agent/hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: `OPENCLAW_GOOGLE_MEET_*` env-var alternative to config.
- [hermes_agent/hermes_provider_minimax_oauth](../hermes_agent/hermes_provider_minimax_oauth.md) — a provider OAuth login flow; relevance: mint-refresh-token-then-store pattern analog.
- [oc_plugins_google_meet_overview](oc_plugins_google_meet_overview.md) (planned, this series) — overview that points here; relevance: when OAuth is needed vs Chrome-only.
- [oc_plugins_google_meet_agent_modes](oc_plugins_google_meet_agent_modes.md) (planned, this series) — modes config; relevance: the `config` block feeds realtime/transports/modes.
- [oc_plugins_google_meet_troubleshooting](oc_plugins_google_meet_troubleshooting.md) (planned, this series) — auth/scope failure fixes; relevance: re-mint token when `meetings.space.created` scope is missing.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension; relevance: owns the realtime/voice config block.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: doctor/preflight + secret storage.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework; relevance: the plugin `config` surface.

**Snippets**
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — OAuth callback/refresh-token mint; relevance: the `localhost:8085/oauth2callback` mint flow.
- [snippet_hermes_agent_cli_auth_spotify_pkce](../../code_snippets/snippet_hermes_agent_cli_auth_spotify_pkce.md) — PKCE login flow; relevance: the PKCE + localhost-callback pattern `googlemeet auth login` uses.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — persist/restore `{refresh, access, expires}`; relevance: storing the minted `oauth` object.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profiles; relevance: CLI-minted credentials stored to a profile.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution order; relevance: config-first then env fallback.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: which auth mode applies for an attempt.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — auth login/logout CLI; relevance: the `auth login` command analog.
- [snippet_hermes_agent_tools_mcp_oauth_manager](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth_manager.md) — OAuth manager for a connector; relevance: refresh-token lifecycle management.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — storing call credentials/secrets; relevance: keeping the refresh token out of config via secrets.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — provider with API-key auth; relevance: the `OPENAI_API_KEY` transcription credential alongside Google OAuth.

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned).

### oc_plugins_google_meet_agent_modes (8t · 10s · 10d)

**Terms**
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: the `google_meet` tool's `action`/`mode` + `openclaw_agent_consult` calls.
- [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — TTS; relevance: `agent` mode speaks the answer via the OpenClaw TTS runtime.
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — STT; relevance: the transcription/caption observer hears the meeting.
- [term_realtime_transcription](../../term_dictionary/term_realtime_transcription.md) — streaming transcription; relevance: final transcripts routed to the consult, fragments coalesced.
- [term_voice_mode](../../term_dictionary/term_voice_mode.md) — realtime voice conversation mode; relevance: `bidi` is the direct realtime-voice-model loop.
- [term_silence_token](../../term_dictionary/term_silence_token.md) — suppress-output control; relevance: input suppressed while assistant audio plays / echo ignored before consult.
- [term_llm](../../term_dictionary/term_llm.md) — language model; relevance: the configured OpenClaw agent that answers.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — host product; relevance: the tool/modes run in OpenClaw.

**Docs**
- [hermes_agent/hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice-mode guide; relevance: agent-vs-direct-voice mode distinction analog.
- [hermes_agent/hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — voice-mode CLI; relevance: `googlemeet speak/test-speech` CLI analog.
- [hermes_agent/hermes_voice_gateway_discord_vc](../hermes_agent/hermes_voice_gateway_discord_vc.md) — agent in a live voice channel; relevance: the talk-back-in-a-call behavior.
- [hermes_agent/hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — transcription; relevance: the caption observer / final-transcript routing.
- [hermes_agent/hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — TTS providers; relevance: the speech-output path for `agent` mode.
- [cc_sdk_subagents_lifecycle](../claude_code/cc_sdk_subagents_lifecycle.md) — subagent lifecycle; relevance: the per-meeting `subagent:google-meet:<session>` consult session key.
- [cc_sdk_permission_modes](../claude_code/cc_sdk_permission_modes.md) — permission/tool-policy modes; relevance: `realtime.toolPolicy` (`safe-read-only`/`owner`/`none`).
- [oc_plugins_google_meet_overview](oc_plugins_google_meet_overview.md) (planned, this series) — defines the modes; relevance: this note details them.
- [oc_plugins_google_meet_oauth_config](oc_plugins_google_meet_oauth_config.md) (planned, this series) — the config behind the modes; relevance: `realtime.agentId`/`voiceProvider` config.
- [oc_plugins_google_meet_troubleshooting](oc_plugins_google_meet_troubleshooting.md) (planned, this series) — manual-action failures; relevance: `manualActionRequired`/`speechReady` symptoms.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension; relevance: the realtime audio bridge + consult.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the configured agent that talks back / consults.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework; relevance: the `google_meet` tool registration.

**Snippets**
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — duplex realtime audio stream; relevance: the audio bridge in `agent`/`bidi`.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — realtime transcription stream; relevance: the listen/caption side.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — talk/transcription relay; relevance: routing final transcripts to the consult and TTS out.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — voice-exec event dedup; relevance: echo/loopback suppression before consult.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: `agent` vs `bidi` answer path analog.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: realtime transcription provider wiring.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: shared consult machinery with Voice Call.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-call manager; relevance: session lifecycle (`speak`/`status`/`leave`).
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: routing the consult answer to the TTS runtime in `agent` mode.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — subagent spawn policy; relevance: the per-meeting consult subagent session + tool policy.

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned).

### oc_plugins_google_meet_troubleshooting (8t · 10s · 10d)

**Terms**
- [term_websocket](../../term_dictionary/term_websocket.md) — WebSocket transport; relevance: `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS` plaintext-WS node opt-in + token-mismatch.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — machine-readable probe output; relevance: `googlemeet doctor/status/test-speech --json` probe surface.
- [term_browser_automation](../../term_dictionary/term_browser_automation.md) — controlling a browser programmatically; relevance: Chrome join, "Use microphone" click, manual-action repair.
- [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — TTS; relevance: "agent joins but does not talk" / `speechReady:false` symptoms.
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — STT; relevance: caption/transcription failure symptoms.
- [term_homebrew](../../term_dictionary/term_homebrew.md) — macOS package manager; relevance: BlackHole/SoX reinstall fixes; Linux lacks the audio device.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — refresh token; relevance: re-mint/re-auth fix for "meeting creation fails" (missing scope).
- [term_openclaw](../../term_dictionary/term_openclaw.md) — host product; relevance: gateway/node-config fixes are OpenClaw operations.

**Docs**
- [hermes_agent/hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — browser supervisor/recovery; relevance: browser-control repair when Chrome can't join.
- [hermes_agent/hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — browser automation setup; relevance: signed-in Chrome profile + permissions prerequisites.
- [hermes_agent/hermes_desktop_remote_backend](../hermes_agent/hermes_desktop_remote_backend.md) — remote/paired desktop backend; relevance: the Parallels-Chrome node-host split.
- [cc_remote_control](../claude_code/cc_remote_control.md) — remote control of an agent host; relevance: node pairing/approval + remote command gating analog.
- [hermes_agent/hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals; relevance: `nodes.allowCommands` + token-mismatch reload behavior.
- [band/band_websocket_overview](../band/band_websocket_overview.md) — WebSocket connection model; relevance: the insecure-private-WS node connection.
- [oc_plugins_google_meet_overview](oc_plugins_google_meet_overview.md) (planned, this series) — the flows that fail; relevance: transports/quick-start that the symptoms reference.
- [oc_plugins_google_meet_agent_modes](oc_plugins_google_meet_agent_modes.md) (planned, this series) — talk-back failures; relevance: `manualActionRequired`/`speechReady` come from the modes.
- [oc_plugins_google_meet_oauth_config](oc_plugins_google_meet_oauth_config.md) (planned, this series) — create-space auth; relevance: "meeting creation fails" without OAuth/scope.
- [oc_plugins_dependency_resolution](oc_plugins_dependency_resolution.md) (planned, this series) — plugin-enable/node-load failures; relevance: "agent cannot see the tool" = plugin not loaded by current gateway.

**Repos**
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — Twilio/phone transport; relevance: "Twilio setup checks fail" / "call never enters the meeting" symptoms.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension; relevance: audio-bridge / talk-back failures.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: node pairing/approval + `nodes.allowCommands`.

**Snippets**
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — node command gating; relevance: `allowCommands` must include `browser.proxy`/`googlemeet.chrome`.
- [snippet_openclaw_voice_call_media_stream_admission](../../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md) — call admission; relevance: Twilio call admission / dial-in failures.
- [snippet_openclaw_gateway_agent_voice_wake_tracking](../../code_snippets/snippet_openclaw_gateway_agent_voice_wake_tracking.md) — audio/voice node state; relevance: audio-bridge readiness tracking.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: `devices approve` + node-connect flow.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — node client connect/proxy; relevance: node-to-gateway connection + `browser.proxy`.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — invoking a node command; relevance: `nodes invoke --command googlemeet.chrome`.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: which node commands a gateway permits.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: `gateway token mismatch` diagnosis.
- [snippet_hermes_agent_tools_browser_supervisor_recovery](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_recovery.md) — browser recovery; relevance: "browser opens but agent cannot join" repair.
- [snippet_hermes_agent_gw_pairing](../../code_snippets/snippet_hermes_agent_gw_pairing.md) — gateway pairing; relevance: node install/pairing with the current token.

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned).

### oc_plugins_hooks_catalog (8t · 10s · 10d)

**Terms**
- [term_gateway_hooks](../../term_dictionary/term_gateway_hooks.md) — the gateway hook system; relevance: this page IS the OpenClaw hook catalog (closest term match).
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — event/lifecycle extensibility; relevance: hooks fire on per-phase turn events.
- [term_observer_pattern](../../term_dictionary/term_observer_pattern.md) — observe/notify pattern; relevance: observation-only hooks (`llm_input`, `agent_end`, `message_received`).
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: `before_tool_call`/`tool_result_persist` rewrite/gate tool calls.
- [term_guardrails](../../term_dictionary/term_guardrails.md) — policy enforcement; relevance: tool-call-policy hooks (`requireApproval`, block, deny-on-timeout).
- [term_template_method_pattern](../../term_dictionary/term_template_method_pattern.md) — fixed pipeline with overridable steps; relevance: the priority-ordered, sequential hook pipeline.
- [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin SDK; relevance: hooks are registered via `api.on(...)` from `definePluginEntry`.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — host product; relevance: the hook runner is OpenClaw's.

**Docs**
- [cc_hooks_overview](../claude_code/cc_hooks_overview.md) — Claude Code hooks overview; relevance: the per-phase lifecycle-hook catalog analog.
- [cc_hook_handler_types](../claude_code/cc_hook_handler_types.md) — hook handler/event types; relevance: catalog of hook events analog.
- [cc_hooks_io_and_decision_control](../claude_code/cc_hooks_io_and_decision_control.md) — hook decision/control output; relevance: block/cancel/override/require-approval decision results.
- [cc_permissions_hooks_and_working_directories](../claude_code/cc_permissions_hooks_and_working_directories.md) — permission hooks; relevance: tool-call-policy/approval gating analog.
- [hermes_agent/hermes_event_hooks](../hermes_agent/hermes_event_hooks.md) — Hermes event hooks; relevance: the directly-analogous typed event-hook system.
- [hermes_agent/hermes_plugin_hook_reference](../hermes_agent/hermes_plugin_hook_reference.md) — plugin hook reference; relevance: per-hook payload/decision reference analog.
- [pi_extensions_overview](../pi/pi_extensions_overview.md) — PI extension hooks; relevance: the in-tree extension hook surface OpenClaw mirrors.
- [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — SDK plugin/hook registration; relevance: registering hooks through the SDK analog.
- [oc_plugins_hooks_lifecycle_install](oc_plugins_hooks_lifecycle_install.md) (planned, this series) — install + gateway-lifecycle hooks; relevance: the other half of the hook surface.
- [oc_plugins_dependency_resolution](oc_plugins_dependency_resolution.md) (planned, this series) — hook-providing plugins load here; relevance: a registered hook implies a loaded plugin.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: where `api.on(...)` hooks are registered.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: runs the priority-ordered hook pipeline.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: session-extension / next-turn-injection + `session_start/end` hooks.

**Snippets**
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — hook request handler; relevance: the runner that dispatches hooks per phase.
- [snippet_openclaw_gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — hook config payload; relevance: `hooks.timeoutMs`/`hooks.timeouts.<name>` config.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — session-reset hooks; relevance: `before_reset`/`session_end` handling.
- [snippet_hermes_agent_gw_hooks](../../code_snippets/snippet_hermes_agent_gw_hooks.md) — gateway hooks; relevance: the analogous gateway hook registry/runner.
- [snippet_hermes_agent_conv_loop_post_api_hook](../../code_snippets/snippet_hermes_agent_conv_loop_post_api_hook.md) — post-API model hook; relevance: `llm_output`/`model_call_ended` observation analog.
- [snippet_hermes_agent_tools_approval_ui](../../code_snippets/snippet_hermes_agent_tools_approval_ui.md) — approval UI; relevance: `requireApproval` result surfaced to the operator.
- [snippet_hermes_agent_core_shell_hooks_callback](../../code_snippets/snippet_hermes_agent_core_shell_hooks_callback.md) — exec/shell hook callback; relevance: `resolve_exec_env` / exec-environment hook analog.
- [snippet_hermes_agent_core_shell_hooks_allowlist](../../code_snippets/snippet_hermes_agent_core_shell_hooks_allowlist.md) — exec hook allowlist; relevance: tool-call-policy gating analog.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — runner/router; relevance: routing a turn through the hook phases.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — subagent spawn policy; relevance: `subagent_spawned`/`subagent_ended` hooks.

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned).

### oc_plugins_hooks_lifecycle_install (8t · 10s · 10d)

**Terms**
- [term_gateway_hooks](../../term_dictionary/term_gateway_hooks.md) — gateway hook system; relevance: `gateway_start`/`gateway_stop` lifecycle hook points.
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — lifecycle events; relevance: install/lifecycle hooks fire on gateway start/stop/reload + plugin install.
- [term_observer_pattern](../../term_dictionary/term_observer_pattern.md) — lifecycle observers; relevance: `cron_changed`/`gateway_start` observe lifecycle changes.
- [term_agent_lifecycle_event](../../term_dictionary/term_agent_lifecycle_event.md) — agent/session lifecycle event; relevance: the lifecycle-event taxonomy install/lifecycle hooks subscribe to.
- [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin SDK; relevance: install/lifecycle hooks are SDK-registered (`before_install`).
- [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — plugin manifest; relevance: install hooks ship with the plugin package.
- [term_npm](../../term_dictionary/term_npm.md) — npm install; relevance: `before_install` inspects staged install material at plugin install.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — host product; relevance: gateway lifecycle + deprecations are OpenClaw's.

**Docs**
- [pi_extensions_events_lifecycle](../pi/pi_extensions_events_lifecycle.md) — PI extension lifecycle events; relevance: the directly-analogous start/stop/install lifecycle hooks.
- [band/band_agent_lifecycle](../band/band_agent_lifecycle.md) — agent lifecycle; relevance: start/stop/reload lifecycle phases analog.
- [hermes_agent/hermes_event_hooks](../hermes_agent/hermes_event_hooks.md) — event hooks (incl. lifecycle); relevance: gateway start/stop hook analog.
- [cc_hook_configuration_settings](../claude_code/cc_hook_configuration_settings.md) — hook configuration; relevance: install/lifecycle hook configuration analog.
- [cc_plugin_quickstart](../claude_code/cc_plugin_quickstart.md) — plugin setup; relevance: where install hooks fire during plugin setup.
- [hermes_agent/hermes_plugin_extensions_hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — plugin extension hooks; relevance: deprecation-migration of hook names analog.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — plugin install security; relevance: `before_install` inspecting staged install material.
- [oc_plugins_hooks_catalog](oc_plugins_hooks_catalog.md) (planned, this series) — the runtime-hooks half; relevance: this note is the install/lifecycle complement.
- [oc_plugins_dependency_resolution](oc_plugins_dependency_resolution.md) (planned, this series) — startup/reload loading; relevance: lifecycle hooks fire when startup/reload loads plugins.
- [oc_plugins_manage_plugins](oc_plugins_manage_plugins.md) (planned, this series) — install triggers install hooks; relevance: `plugins install/update` runs `before_install`.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: gateway start/stop/reload lifecycle finalizer.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions; relevance: plugin install hooks (`before_install`).
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — packaged apps; relevance: bundled-plugin install at package level.

**Snippets**
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle phases; relevance: install→load→start lifecycle the hooks attach to.
- [snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md) — gateway startup hook point; relevance: `gateway_start` fires here.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — reload apply; relevance: reload lifecycle re-loads plugins.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — restart/startup of services; relevance: services started/stopped with the gateway.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — gateway shutdown; relevance: `gateway_stop` + bounded shutdown finalizer.
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — gateway lifecycle CLI; relevance: gateway start/stop/restart analog.
- [snippet_hermes_agent_gw_shutdown_forensics](../../code_snippets/snippet_hermes_agent_gw_shutdown_forensics.md) — shutdown forensics; relevance: finalizing ghost rows on `shutdown`/`restart`.
- [snippet_hermes_agent_cli_plugins_install](../../code_snippets/snippet_hermes_agent_cli_plugins_install.md) — plugin install command; relevance: the install path that runs `before_install`.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: install hooks declared with the plugin.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — reload plan; relevance: reload computes what to (re)load before lifecycle hooks fire.

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned).

### oc_plugins_install_overrides (8t · 10s · 10d)

**Terms**
- [term_npm](../../term_dictionary/term_npm.md) — npm; relevance: `npm:<spec>` / `npm-pack:<path.tgz>` override sources + `npm pack` tarballs.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node; relevance: the package install the override redirects.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — isolated execution; relevance: isolated `OPENCLAW_STATE_DIR` / disposable test machine requirement.
- [term_dependency_confusion](../../term_dictionary/term_dependency_confusion.md) — registry-confusion supply-chain risk; relevance: overrides execute plugin code from operator-supplied untrusted sources.
- [term_supply_chain](../../term_dictionary/term_supply_chain.md) — software supply-chain trust; relevance: overrides do NOT inherit trusted-source status; id-enforcement caveat.
- [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — plugin manifest id; relevance: override enforces the expected manifest id (a `codex` override must install manifest id `codex`).
- [term_access_control](../../term_dictionary/term_access_control.md) — trust/permission gating; relevance: `.env` cannot enable overrides — set them in the trusted shell/CI.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — host product; relevance: the setup-time installer the override hooks into.

**Docs**
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — advanced install + verification; relevance: verify-installed-package step analog.
- [cc_marketplace_restrictions](../claude_code/cc_marketplace_restrictions.md) — restricting install sources; relevance: operator-controlled source override analog.
- [cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md) — managed plugin policy; relevance: enterprise-controlled install source/trust analog.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — plugin install security; relevance: untrusted-plugin-code execution caveat.
- [cc_plugin_caching_and_troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin install troubleshooting; relevance: verifying an installed test artifact.
- [pi_packages](../pi/pi_packages.md) — PI package install; relevance: local/tarball package install analog.
- [pi_development](../pi/pi_development.md) — local plugin development/testing; relevance: testing a local package before publishing.
- [oc_plugins_dependency_resolution](oc_plugins_dependency_resolution.md) (planned, this series) — overrides replace the catalog/bundled/default source; relevance: the resolution path overrides intercept.
- [oc_plugins_manage_plugins](oc_plugins_manage_plugins.md) (planned, this series) — the normal-user install path; relevance: overrides are the E2E/test alternative to `plugins install`.
- [oc_plugins_copilot](oc_plugins_copilot.md) (planned, this series) — a native-heavy package (codex sibling) tested via override; relevance: codex/copilot are the override examples.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions; relevance: the install path overrides intercept.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: the setup-time installer + onboarding flow.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: trusted-source / operator-input trust treatment.

**Snippets**
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugin install command; relevance: the install path the override replaces the source for.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolver; relevance: why an override is treated as untrusted operator input.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: trusted-source status the override does NOT inherit.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — process-env gating; relevance: `OPENCLAW_ALLOW_PLUGIN_INSTALL_OVERRIDES` env-gated behavior.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — runtime exec audit; relevance: executing plugin code from a provided source.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config; relevance: the setup-time/onboarding flow that consults the override map.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard setup imports; relevance: the shared setup-time plugin installer.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package/manifest-id contract; relevance: override enforces the expected manifest id.
- [snippet_hermes_agent_lsp_servers_install](../../code_snippets/snippet_hermes_agent_lsp_servers_install.md) — installing a packaged artifact from a source; relevance: source-selection-at-install analog.
- [snippet_hermes_agent_cli_plugins_install](../../code_snippets/snippet_hermes_agent_cli_plugins_install.md) — plugins install flow; relevance: the install flow the override map redirects.

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned).

### oc_plugins_llama_cpp (8t · 10s · 10d)

**Terms**
- [term_embedding](../../term_dictionary/term_embedding.md) — vector embeddings; relevance: local GGUF memory embeddings the plugin produces.
- [term_vector_database](../../term_dictionary/term_vector_database.md) — vector store; relevance: the memory-search embedding store the provider feeds.
- [term_rag](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: embedding-backed memory search is retrieval augmentation.
- [term_quantization](../../term_dictionary/term_quantization.md) — model weight quantization; relevance: GGUF Q8_0 (`embeddinggemma-300m-qat-Q8_0`) quantized model.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node runtime; relevance: Node 24 + the `node-llama-cpp` native runtime + pnpm rebuild.
- [term_npm](../../term_dictionary/term_npm.md) — npm; relevance: `openclaw plugins install @openclaw/llama-cpp-provider`; native dep kept out of core to survive npm updates.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider-type plugin; relevance: this is the official external embeddings *provider* plugin.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — host product; relevance: `memorySearch.provider: "local"` is OpenClaw config.

**Docs**
- [hermes_agent/hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — memory provider plugin; relevance: the directly-analogous memory-embeddings provider plugin.
- [hermes_agent/hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory provider catalog; relevance: local-vs-cloud embeddings provider choices.
- [hermes_agent/hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — local Ollama provider; relevance: the recommended lower-friction local alternative.
- [hermes_agent/hermes_provider_local_llm_mac](../hermes_agent/hermes_provider_local_llm_mac.md) — local LLM on mac; relevance: local native-runtime setup analog.
- [hermes_agent/hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — self-hosted local LLM; relevance: running models locally for memory/inference.
- [aws_bedrock/bedrock_kb_how_it_works](../aws_bedrock/bedrock_kb_how_it_works.md) — knowledge-base embeddings + retrieval; relevance: embedding-store + retrieval concept analog.
- [aws_opensearch/opensearch_semantic_search](../aws_opensearch/opensearch_semantic_search.md) — semantic/vector search; relevance: the embedding-backed search the provider enables.
- [pi_custom_models](../pi/pi_custom_models.md) — custom/local model registration; relevance: pointing at a local `.gguf` model path.
- [oc_plugins_dependency_resolution](oc_plugins_dependency_resolution.md) (planned, this series) — native dep kept in a plugin; relevance: the canonical reason `node-llama-cpp` lives here, not core.
- [oc_plugins_manage_plugins](oc_plugins_manage_plugins.md) (planned, this series) — installing the plugin; relevance: `plugins install @openclaw/llama-cpp-provider`.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: the memory-search the provider feeds.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — external-provider plugin framework; relevance: the provider-plugin host.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions; relevance: plugin packaging.

**Snippets**
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — memory embedding host; relevance: where the local embeddings provider plugs in.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs; relevance: what gets embedded for memory search.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: the recommended local-service alternative.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search; relevance: the consumer of the embeddings.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine; relevance: the engine `memorySearch.provider` configures.
- [snippet_hermes_agent_core_agent_init_memory_ollama](../../code_snippets/snippet_hermes_agent_core_agent_init_memory_ollama.md) — init memory with local provider; relevance: wiring a local embeddings provider at init.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: the external-provider plugin shape.
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — memory store schema; relevance: the embedding-backed memory store.
- [snippet_tattletale_mode_opensearch_knn](../../code_snippets/snippet_tattletale_mode_opensearch_knn.md) — kNN vector search; relevance: nearest-neighbor retrieval over embeddings.

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned).

### oc_plugins_manage_plugins (8t · 10s · 10d)

**Terms**
- [term_npm](../../term_dictionary/term_npm.md) — npm; relevance: `npm:`/bare/`npm-pack:` install sources + dist-tags.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node runtime; relevance: the package runtime plugins run on.
- [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — plugin manifest; relevance: `dependencyStatus`/registrations + native-plugin `openclaw.extensions` manifest.
- [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin SDK; relevance: the managed plugins are SDK-built.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider-type plugin; relevance: providers are one managed plugin kind.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — machine-readable output; relevance: `plugins list --json | jq` agent/script output.
- [term_npm_scoping](../../term_dictionary/term_npm_scoping.md) — scoped npm packages; relevance: `npm:@scope/openclaw-plugin` install specs.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — host product; relevance: the `openclaw plugins` command surface.

**Docs**
- [cc_plugin_cli_commands](../claude_code/cc_plugin_cli_commands.md) — plugin CLI commands; relevance: the directly-analogous list/install/update/uninstall command surface.
- [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — marketplace + install; relevance: choosing an install source (marketplace/registry).
- [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — plugin sources; relevance: the ClawHub/npm/git/local "choose a source" table analog.
- [cc_host_and_manage_marketplaces](../claude_code/cc_host_and_manage_marketplaces.md) — host/manage marketplaces; relevance: publishing/discovery (ClawHub) analog.
- [cc_plugin_marketplace_walkthrough](../claude_code/cc_plugin_marketplace_walkthrough.md) — marketplace walkthrough; relevance: search→install→verify workflow analog.
- [pi_cli_reference](../pi/pi_cli_reference.md) — PI CLI reference; relevance: plugin/package management CLI analog.
- [hermes_agent/hermes_plugins_management](../hermes_agent/hermes_plugins_management.md) — Hermes plugin management; relevance: the directly-analogous manage-plugins surface.
- [oc_plugins_dependency_resolution](oc_plugins_dependency_resolution.md) (planned, this series) — what install/reload does under the hood; relevance: the resolution behind these commands.
- [oc_plugins_install_overrides](oc_plugins_install_overrides.md) (planned, this series) — the test-install alternative; relevance: override map vs normal install.
- [oc_plugins_llama_cpp](oc_plugins_llama_cpp.md) (planned, this series) — a concrete plugin to install; relevance: `plugins install @openclaw/llama-cpp-provider` example.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions; relevance: the plugin subsystem managed.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: managed-gateway auto-restart after install/uninstall.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/wizard; relevance: the `openclaw plugins` CLI surface.

**Snippets**
- [snippet_hermes_agent_cli_plugins_cmd_list_info](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_list_info.md) — plugins list/search/inspect; relevance: `plugins list/search` + `--json`.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugins install; relevance: `plugins install` from each source.
- [snippet_hermes_agent_cli_plugins_cmd_remove](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_remove.md) — plugins uninstall; relevance: `plugins uninstall` (+ `--keep-files`/`--dry-run`).
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — source discovery; relevance: `plugins search` ClawHub discovery.
- [snippet_hermes_agent_cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — plugins inspect/doctor; relevance: `inspect --runtime` proof of registrations.
- [snippet_hermes_agent_cli_plugins_install](../../code_snippets/snippet_hermes_agent_cli_plugins_install.md) — plugins install flow; relevance: source-prefix selection (`clawhub:`/`npm:`/`git:`).
- [snippet_hermes_agent_cli_uninstall](../../code_snippets/snippet_hermes_agent_cli_uninstall.md) — uninstall flow; relevance: removing config/index/load-path entries.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — restart/startup; relevance: managed-gateway auto-restart after a plugin change.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package/manifest contract; relevance: native-plugin `openclaw.extensions` metadata for publish.
- [snippet_hermes_agent_cli_doctor_entry_early_checks](../../code_snippets/snippet_hermes_agent_cli_doctor_entry_early_checks.md) — doctor early checks; relevance: verifying runtime registrations after install.

**Entry**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned), [entry_code_snippets_openclaw](../../../0_entry_points/entry_code_snippets_openclaw.md) (snippet hub cross-link).

> are "(planned, this series)" and resolve at execution. Each note meets ≥8 terms · ≥10 snippets · ≥10 docs

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc notes by their home sub-plan, NOT as new
`term_dictionary` entries; the only term-dictionary interaction is LINKING existing terms. **pl03 creates 0 new
`term_dictionary` notes.**

| Term (as it appears in source) | Disposition |
|---|---|
| Copilot SDK harness / agent runtime (`agentRuntime.id`) | Documented in `oc_plugins_copilot` (note 1). Link existing `term_agent_harness`, `term_autonomous_coding_agents`. No new term. |
| Plugin dependency resolution / install roots / bundled vs local plugins | Documented in `oc_plugins_dependency_resolution` (note 2). Link `term_plugin_manifest`, `term_plugin_sdk`, `term_npm`. No new term. |
| Google Meet plugin / transport (Chrome / Twilio) / talk-back modes (agent/bidi/transcribe) | Documented in notes 3–6. Link `term_text_to_speech`, `term_speech_to_text`, `term_oauth`. No new term. |
| BlackHole 2ch / SoX (host audio dependencies) | Config detail inside note 3 (named, not defined). Link `term_homebrew`. No new term (tool-specific, not vault-reusable). |
| Hooks (exec-environment / tool-call-policy / tool-result / prompt-model / message / session-extension / install / gateway-lifecycle) | Documented in notes 7–8. Link `term_event_driven_architecture`, `term_observer_pattern`, `term_guardrails`. No new term. |
| Install overrides (`OPENCLAW_PLUGIN_INSTALL_OVERRIDES`, `npm:`/`npm-pack:`) | Documented in note 9. Link `term_npm`, `term_sandbox`. No new term. |
| llama.cpp provider / GGUF / `node-llama-cpp` / local memory embeddings | Documented in note 10. Link `term_embedding`, `term_vector_database`, `term_quantization`, `term_rag`. No new term (GGUF/node-llama-cpp are product/runtime specifics, not cross-cutting). |
| Plugin management commands (list/search/install/update/uninstall/source/publish) | Documented in note 11. Link `term_npm`. Full CLI contract links out to `cli/plugins` (cl06). No new term. |
| ClawHub (mentioned as an install source) | Named in note 11; full coverage owned by ClawHub sub-plans (cw01–03). Link out at augment. No new term here. |

**New-term candidates (cross-cutting, no doc-page home, no existing note):** none identified. The closest
borderline was a generic "agent runtime" concept; it is covered as documentation (`concepts/agent-runtimes`,
co01) and by `term_agent_harness`, so no `term_dictionary` capture is proposed. (DB confirmed `term_agent_runtime`
MISSING but the concept is doc-owned, not a vault-reusable definitional gap.)

## Term-Note Authoring Requirements

above). Inherited from master: were a genuinely cross-cutting, vault-reusable term with no doc-page home and no
existing note to surface at augment, it would be captured via `/tessellum-capture-term-note` (multi-source
research) and added to its best-fit `acronym_glossary_*.md` — not inlined in any `oc_*` note.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P3). All 8 gates must PASS before commit.

| Gate | Check | Tool / method |
|------|-------|---------------|
| G1 | Format: YAML field order + forbidden fields, H1/`## Overview`/`## Related Notes`/`## References`/footer, density caps | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim traces to `inbox/openclaw_docs/plugins/<page>.md` (no invented config/flags) | diff vs mirror source |
| G3 | Density + Coverage: ≤400 lines / ≤2,500 words / ≤6 code blocks per note; every mapped H2/H3 present | word/line/fence count + Section Coverage Map |
| G4 | Cross-Reference: raised floors per note — ≥8 relevance-selected terms · ≥10 code_snippets · ≥10 docs (≥5 existing) + repo_openclaw\*/sibling oc_\*, each with a relevance statement | Related Notes review vs `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` |
| G5 | Ghost-reference detect + redirect: every internal link resolves to an existing note (or planned sibling) | `/tessellum-fix-ghost-references` + DB existence check |
| G6 | Broken-link fix: correct relative paths; reindex shows 0 broken links | `/tessellum-fix-broken-links` + reindex |
| G7 | Discoverability: each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | inlink audit (via `entry_openclaw_docs.md` + repo/term backlinks) |
| G8 | In-degree ≥1 (anti-island) for every new note after reindex | `note_links` query / in_degree column |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_copilot oc_plugins_dependency_resolution oc_plugins_google_meet_overview \
oc_plugins_google_meet_oauth_config oc_plugins_google_meet_agent_modes oc_plugins_google_meet_troubleshooting \
oc_plugins_hooks_catalog oc_plugins_hooks_lifecycle_install oc_plugins_install_overrides \
oc_plugins_llama_cpp oc_plugins_manage_plugins"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec': $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # density caps (body only, frontmatter stripped)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code / ${lines}L)"
  # sibling-prefix self-reference sanity (informational)
  grep -oq "($SIBLING_PREFIX" "$f" || echo "NOTE: $n has no $SIBLING_PREFIX sibling link"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
bash scripts/update_notes_database.sh --force   # reindex, then verify note_links + 0 broken links (G6/G8)
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w / ≤6 code / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_copilot | procedure | 650 | 2 | ✅ |
| 2 | oc_plugins_dependency_resolution | concept | 600 | 3 | ✅ |
| 3 | oc_plugins_google_meet_overview | procedure | 700 | 6 | ✅ (at code cap; trim least-load-bearing snippet if needed) |
| 4 | oc_plugins_google_meet_oauth_config | procedure | 650 | 5 | ✅ |
| 5 | oc_plugins_google_meet_agent_modes | procedure | 650 | 5 | ✅ |
| 6 | oc_plugins_google_meet_troubleshooting | procedure | 600 | 5 | ✅ |
| 7 | oc_plugins_hooks_catalog | procedure | 700 | 4 | ✅ |
| 8 | oc_plugins_hooks_lifecycle_install | procedure | 500 | 2 | ✅ |
| 9 | oc_plugins_install_overrides | procedure | 400 | 3 | ✅ |
| 10 | oc_plugins_llama_cpp | procedure | 350 | 3 | ✅ |
| 11 | oc_plugins_manage_plugins | procedure | 550 | 6 | ✅ (at code cap; manage-plugins has 10 source fences — reproduce only the 6 most load-bearing) |

No note exceeds caps. The two outliers (google-meet 8,511w/84 fences, hooks 3,280w) are resolved by the 4-way
and 2-way splits; the code-dense manage-plugins (10 fences) and google-meet-overview reproduce a curated ≤6.

## Entry Point Decision (inherited from master)

Per master W1, `0_entry_points/entry_openclaw_docs.md` is CREATED as a pre-step before the first sub-plan
executes (DB-confirmed MISSING today). pl03 contributes **11 rows** to that hub under a **Plugins** section
(sub-row `pl03`): one row per planned note (filename, BB, source slug, 1-line description). Each note receives
its `entry_openclaw_docs.md` back-link at finalization (satisfies G7/G8). No per-sub-plan entry point is created
(the master hub is the single index for all 105 sub-plans).

## Inlinks (existing notes → new notes)

Candidate outside-`documentation/openclaw/` inbound links (DB-verify + add at execution) so every new note has
in-degree ≥1 (G7/G8):

- `entry_openclaw_docs.md` (planned hub) → **all 11** notes (primary anti-island guarantee).
- `repo_openclaw_extensions.md` → notes 1, 2, 3, 5, 7, 8, 9, 11 (the plugin/extension framework).
- `repo_openclaw_extensions_voice_speech.md` → notes 3, 4, 5, 6 (Google Meet voice/speech).
- `repo_openclaw_memory.md` → note 10 (local embeddings memory search).
- `repo_openclaw_extensions_llm_providers.md` → notes 1, 10 (Copilot runtime / llama-cpp provider).
- `repo_openclaw_gateway.md` → notes 2, 7, 8 (loading/reload + hook pipeline + lifecycle).
- `term_agent_harness.md` → note 1; `term_plugin_manifest.md` → notes 2, 11; `term_event_driven_architecture.md`
  → notes 7, 8; `term_embedding.md` → note 10; `term_oauth.md` → note 4; `term_npm.md` → notes 2, 9, 11.
  (runtime comparison).

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Cap dynamic-workflow fan-out at ~30 agents/run (11 notes is well
under). Re-read each source page; reproduce config/CLI snippets verbatim; one building_block per note. Reindex
incrementally and verify `note_links` + 0 broken links before commit. `git pull --rebase --autostash` first; no
Claude co-author trailer; commit + push the sub-plan's notes as one wave.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending (plan is `status: ready`) |

## Augmentation Report (2026-06-21)

**Scope of this augment pass:** per-note Related Notes mapping LOCKED at the RAISED floors (**≥8 terms · ≥10
"Candidate Cross-References" section. Sources re-read from `inbox/openclaw_docs/plugins/` (measured word counts
re-confirmed: copilot 2,201 · dependency-resolution 1,101 · google-meet 8,511 · hooks 3,280 · install-overrides
374 · llama-cpp 207 · manage-plugins 1,055 — all match the plan's Source table). All EXISTING `note_id`s were

**What was locked (per-note counts; all floors met):**

| # | Note | Terms | Snippets (all existing) | Docs (existing + planned-sibling) | Repos | Floors met (≥8t·≥10s·≥10d, ≥5 existing docs) |
|---|---|---:|---:|---|---:|---|
| 1 | oc_plugins_copilot | 8 | 10 | 10 (8 existing + 2 sibling) | 3 | ✅ |
| 2 | oc_plugins_dependency_resolution | 8 | 10 | 10 (8 existing + 2 sibling) | 3 | ✅ |
| 3 | oc_plugins_google_meet_overview | 8 | 10 | 10 (6 existing + 4 sibling) | 3 | ✅ |
| 4 | oc_plugins_google_meet_oauth_config | 8 | 10 | 10 (7 existing + 3 sibling) | 3 | ✅ |
| 5 | oc_plugins_google_meet_agent_modes | 8 | 10 | 10 (7 existing + 3 sibling) | 3 | ✅ |
| 6 | oc_plugins_google_meet_troubleshooting | 8 | 10 | 10 (6 existing + 4 sibling) | 3 | ✅ |
| 7 | oc_plugins_hooks_catalog | 8 | 10 | 10 (8 existing + 2 sibling) | 3 | ✅ |
| 8 | oc_plugins_hooks_lifecycle_install | 8 | 10 | 10 (7 existing + 3 sibling) | 3 | ✅ |
| 9 | oc_plugins_install_overrides | 8 | 10 | 10 (7 existing + 3 sibling) | 3 | ✅ |
| 10 | oc_plugins_llama_cpp | 8 | 10 | 10 (8 existing + 2 sibling) | 3 | ✅ |
| 11 | oc_plugins_manage_plugins | 8 | 10 | 10 (7 existing + 3 sibling) | 3 | ✅ |

google-meet split children that lean on 4 planned-this-series siblings). Total distinct existing targets

terms added beyond the plan-stage list: `term_realtime_transcription`, `term_voice_call`, `term_voice_mode`,
`term_silence_token`, `term_pkce`, `term_auth_profile`, `term_credential_pool`, `term_browser_automation`,
`term_gateway_hooks`, `term_template_method_pattern`, `term_agent_lifecycle_event`, `term_npm_scoping`,
`term_dependency_confusion`, `term_supply_chain`. Snippet/doc pools expanded via BM25 over `code_snippet` and
`dev_tool_docs`/`tutorial`/`aws_*` subcategories; the claude_code (`cc_*`), pi (`pi_*`), hermes_agent
(`hermes_*`), and band (`band_*`) coding-agent doc corpora supplied the existing-doc floor (e.g. dedicated
analogs `cc_plugin_dependencies`, `cc_hooks_overview`/`cc_hook_handler_types`/`hermes_event_hooks`,
`hermes_memory_provider_plugin`, `hermes_use_voice_mode_guide`, `cc_plugin_cli_commands`).

**New-term candidates + best-fit glossary:** **none.** Per the master's corpus-wide ownership decision, OpenClaw
vocabulary is digested as `oc_*` doc notes by their home sub-plan, not as new `term_dictionary` entries. The
augment re-read surfaced no cross-cutting, vault-reusable term lacking both a doc-page home AND an existing note.
The only borderline ("agent runtime") is doc-owned (`concepts/agent-runtimes`, co01) and already covered by the
existing `term_agent_harness` / `term_autonomous_coding_agents`; DB confirms `term_agent_runtime`,
`term_voice_agent`, `term_environment_variable`, `term_dependency_injection` are MISSING but none is a genuine
definitional gap (each is doc-owned or product-specific). **pl03 still creates 0 `term_dictionary` notes**, so
the `## Term-Note Authoring Requirements` N/A verdict and `## Undigested Terms Plan` remain unchanged.

**Slug specificity + collision audit (generalized to ALL planned notes):** the 11 planned slugs are all
`oc_plugins_*` documentation notes (procedure ×10 / concept ×1), each scoped to one source page or task cluster;
none collides with an existing `term_*` or other `resources/documentation/` note (verified: no `oc_plugins_*`
note exists in the DB today; the closest existing notes are the LINKED `repo_openclaw_*`, `term_*`, and
sibling-corpus `cc_*`/`hermes_*` docs — all distinct concepts). No rename or removal required.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review run after the xref-augment pass. Source pages spot-re-read from
`inbox/openclaw_docs/plugins/` (CP7 measured, not guessed).

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step exists at ≥8 terms + floors | **PASS** | `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` present; each of the 11 notes has grouped Terms (≥8) / Docs (≥10, ≥5 existing) / Repos / Snippets (≥10) lists, every link carrying a relevance statement. |
| CP2 | 9-GATE table per batch (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref (updated to raised floors), G5 ghost-detect, G6 broken-link-fix, G7 discoverability, G8 in-degree≥1. Single execution phase; all 8 gates present. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision (inherited from master)` — `entry_openclaw_docs.md` CREATED as a W1 pre-step (DB-confirmed MISSING today); pl03 contributes 11 rows under a Plugins/pl03 section; each note gets its hub back-link at finalization (G7/G8). Size rule satisfied (>30 master-total ⇒ CREATE required). |
| CP4 | Plan size manageable | **PASS** | 11 notes (well ≤30); single execution phase; fan-out cap ~30 (11 is well under). |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited from master's Format Definition, derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora: `# OpenClaw — Title` → `## Overview` → source-mirrored H2/H3 → `## Related Notes` → `## References` → bold footer; YAML field order + forbidden-field list match existing target-dir notes. |
| CP6 | Density / BB atomicity (borderline → split) | **PASS** | `## Density Re-Assessment` — all 11 notes ≤700w / ≤6 code / ≤400L; the two outliers (google-meet 8,511w/84 fences, hooks 3,280w) resolved by the 4-way + 2-way splits; code-dense manage-plugins (10 src fences) reproduces a curated ≤6. No unaddressed borderline. |
| CP7 | Source word counts measured | **PASS** | Re-measured `wc -w` 2026-06-21: copilot 2,201 · dependency-resolution 1,101 · google-meet 8,511 · hooks 3,280 · install-overrides 374 · llama-cpp 207 · manage-plugins 1,055 — all within ±0% of the plan's Source table (no under-estimation). |
| CP8 | Undigested Terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (9 rows, all dispositioned to an owner note + link existing terms, 0 new terms); `## Term-Note Authoring Requirements` present (N/A — 0 new terms — with the inherited multi-source/format mandate if a future term surfaces). Must-language preserved. |
| CP8f | Slug/collision audit | **PASS** | All 11 `oc_plugins_*` slugs page/cluster-specific; generalized dedup across `term_dictionary/` AND `resources/documentation/` found no substantive duplicate (no `oc_plugins_*` note exists in the DB); no rename/removal needed. Audit recorded in the Augmentation Report. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps every one of the 11 notes to ≥1 inbound link from OUTSIDE `documentation/openclaw/` (`entry_openclaw_docs` → all 11; plus `repo_openclaw_*` and `term_*` backlinks); G8 in-degree≥1 is a gate in the phase table and an executed-+-verified step. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan `status` advanced `pending → ready`.
