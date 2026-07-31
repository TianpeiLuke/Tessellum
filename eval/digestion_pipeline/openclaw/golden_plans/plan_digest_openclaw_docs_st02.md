---
title: Sub-Plan st02 — OpenClaw Docs: Start / Getting Started (openclaw, quickstart, setup, showcase, wizard×3)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["start/openclaw", "start/quickstart", "start/setup", "start/showcase", "start/wizard", "start/wizard-cli-automation", "start/wizard-cli-reference"]
---

# Sub-Plan st02: Start

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format/YAML, dedup-before-create, 9-GATE, cross-ref
> floors, undigested-term policy, and entry-point wiring are ALL inherited from the master and not re-derived here.

## Scope

The 7 **Start / Getting Started** pages that cover the user's first contact with OpenClaw: the personal-assistant
walkthrough (`start/openclaw`), the old quick-start redirect (`start/quickstart`), the advanced/dev setup workflows
(`start/setup`), the community showcase gallery (`start/showcase`), and the three CLI-onboarding pages — the
onboarding hub (`start/wizard`), the non-interactive/CI automation guide (`start/wizard-cli-automation`), and the
complete onboarding reference (`start/wizard-cli-reference`). **Priority P1 (Phase A)** — these are the entry-point
"how do I run this" pages the rest of the corpus references; they define the onboarding/setup/heartbeat/workspace
vocabulary CLI, gateway, and concepts sub-plans build on. The code-side counterpart `repo_openclaw_cli_wizard` is
LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **7,219 measured words** (`wc -w`, mirror `inbox/openclaw_docs/start/`). **Planned: 6 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| openclaw | start/openclaw | 1,269 | 11 | 11 | 0 | procedure |
| quickstart | start/quickstart | 78 | 0 | 1 | 0 | procedure (redirect stub) |
| setup | start/setup | 842 | 9 | 9 | 5 | procedure |
| showcase | start/showcase | 1,560 | 0 | 8 | 0 | argument (community-evidence gallery) |
| wizard | start/wizard | 878 | 3 | 5 | 0 | procedure |
| wizard-cli-automation | start/wizard-cli-automation | 709 | 15 | 3 | 0 | procedure |
| wizard-cli-reference | start/wizard-cli-reference | 1,883 | 0 | 5 | 0 | procedure |

(H2/H3 counts exclude the trailing `## Related` / `## Related docs` link blocks; the wizard pages carry their
real sub-structure in MDX `<Steps>/<Step>` and `<Accordion>` blocks, which are mapped as logical sub-sections in
the Section Coverage Map below even though they are not `##`/`###` headers.)

## Content Strategy

- **Prioritize**: the onboarding **reference** (`wizard-cli-reference`, 1,883w — the auth/model option matrix,
  per-step local flow, outputs/internals, RPC) and the **assistant walkthrough** (`openclaw`, 1,269w — the
  end-to-end "two-phone" personal-assistant setup, heartbeats, sessions, media, ops). These are the densest and
  most-referenced setup pages.
- **One note per page** (no word-cap splits): every page is ≤1,883 words (well under the 2,500w cap) and centers
  on a single building block, so each maps cleanly to one `oc_*` note.
- **Fold the redirect stub**: `quickstart.md` (78w) is a pure "Quick start has moved to Getting Started" redirect
  with two cards (Getting Started, Onboarding-CLI). It carries no standalone digestible content, so it is FOLDED
  into the assistant note as a `## References` pointer rather than spawning a near-empty orphan note (see Split
  Decisions). `start/getting-started` itself belongs to sibling sub-plan **st01**, not here.
- **Link-out, do not duplicate**: provider/auth specifics (Anthropic/OpenAI/Gemini/Ollama/Cloudflare/Vercel/etc.)
  → Providers sub-plans `pr01–pr09`; per-channel setup (WhatsApp/Telegram/Discord/Signal/iMessage) → Channels
  `ch01–ch06`; gateway flags/auth/Tailscale → Gateway `gw01–gw07`; `openclaw onboard`/`configure`/`agents`/
  `dashboard` CLI command pages → CLI `cl01–cl09`; agent-workspace/memory/heartbeat/session/soul concepts →
  Concepts `co01–co07`; daemon/systemd/LaunchAgent install → Install/Platforms. These are referenced, never redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_start_openclaw.md` | procedure | start/openclaw (all 11 H2) + start/quickstart (folded as pointer) | 650 | Personal-assistant setup walkthrough: the two-phone WhatsApp pattern, 5-minute quick start, AGENTS workspace/bootstrap files, the "assistant" config, sessions/memory, heartbeats (proactive mode), inbound/outbound media, and the ops checklist. |
| 2 | `oc_start_setup.md` | procedure | start/setup (all 9 H2 + 5 H3) | 600 | Advanced + developer setup workflows: stable (macOS app runs the bundled Gateway) vs bleeding-edge (`pnpm gateway:watch`), tailoring strategy (config/workspace outside the repo), credential storage map, updating without breaking your setup, and the Linux systemd-user-service lingering note. |
| 3 | `oc_start_wizard.md` | procedure | start/wizard (5 H2: Locale, QuickStart vs Advanced, What onboarding configures, Add another agent, Full reference) | 550 | The CLI onboarding hub (`openclaw onboard`): the recommended terminal setup path — locale resolution, QuickStart-vs-Advanced defaults, the 7 things local-mode onboarding configures (Model/Auth → Workspace → Gateway → Channels → Daemon → Health → Skills), remote mode, and adding another agent. |
| 4 | `oc_start_wizard_cli_reference.md` | procedure | start/wizard-cli-reference (5 H2: What the wizard does, Local flow details, Remote mode, Auth and model options, Outputs and internals) | 700 | Complete `openclaw onboard` reference: the per-step local flow (config detection/reset scopes, model/auth, workspace, gateway token vs SecretRef, channels/pairing, daemon per-OS, health, skills), remote mode, the full auth/model option matrix, credential-storage modes, and the config outputs + `wizard.*` RPC internals. |
| 5 | `oc_start_wizard_cli_automation.md` | procedure | start/wizard-cli-automation (3 H2: Baseline non-interactive example, Provider-specific examples, Add another agent) | 500 | Scripted/CI onboarding with `--non-interactive`: the baseline example, `--secret-input-mode plaintext` vs `ref`, the per-provider non-interactive flag sets (Anthropic, Gemini, Z.AI, Vercel/Cloudflare AI Gateway, Moonshot, Mistral, Synthetic, OpenCode, Ollama, custom provider), and scripted `openclaw agents add`. |
| 6 | `oc_start_showcase.md` | argument | start/showcase (8 H2 cluster sections: Fresh from Discord, Automation, Knowledge/Memory, Voice/Phone, Infrastructure, Home/Hardware, Community projects, Submit) | 500 | Community-evidence gallery: real-world OpenClaw projects organized by theme (devtools/PR-review, browser-automation, memory/knowledge, voice/phone, deployment, home/hardware) — the "what people actually build" case for OpenClaw's chat-native, no-API, physical-world reach. |

## Section Coverage Map

```
start/openclaw.md  (11 H2)
├── ⚠️ Safety first ──────────────────────────────── → note 1 (oc_start_openclaw)
├── Prerequisites ───────────────────────────────── → note 1
├── The two-phone setup (recommended) [mermaid] ─── → note 1
├── 5-minute quick start ────────────────────────── → note 1
├── Give the agent a workspace (AGENTS) ─────────── → note 1 (→ links co: agent-workspace, memory)
├── The config that turns it into "an assistant" ── → note 1
├── Sessions and memory ─────────────────────────── → note 1
├── Heartbeats (proactive mode) ─────────────────── → note 1
├── Media in and out ────────────────────────────── → note 1
├── Operations checklist ────────────────────────── → note 1
└── Next steps + Related (links) ────────────────── → note 1 References (link-out to web/gateway/cron/platforms)
start/quickstart.md  (redirect stub, 78w)
└── Info card → Getting Started / Onboarding-CLI ── → note 1 References pointer (folded; see Split Decisions)
start/setup.md  (9 H2 + 5 H3)
├── TL;DR ───────────────────────────────────────── → note 2 (oc_start_setup)
├── Prereqs (from source) ───────────────────────── → note 2
├── Tailoring strategy (so updates do not hurt) ─── → note 2
├── Run the Gateway from this repo ──────────────── → note 2
├── Stable workflow (macOS app first) ───────────── → note 2
├── Bleeding edge workflow (Gateway in a terminal) → note 2
│     ├── 0) Run the macOS app from source too ──── → note 2
│     ├── 1) Start the dev Gateway ──────────────── → note 2
│     ├── 2) Point the macOS app at your Gateway ── → note 2
│     ├── 3) Verify ─────────────────────────────── → note 2
│     └── Common footguns ───────────────────────── → note 2
├── Credential storage map ──────────────────────── → note 2
├── Updating (without wrecking your setup) ──────── → note 2
├── Linux (systemd user service) ────────────────── → note 2
└── Related docs (links) ────────────────────────── → note 2 References (link-out gw/channels/platforms)
start/wizard.md  (5 H2)
├── Locale ──────────────────────────────────────── → note 3 (oc_start_wizard)
├── QuickStart vs Advanced ──────────────────────── → note 3
├── What onboarding configures (7 steps) ────────── → note 3 (detail → note 4)
├── Add another agent ───────────────────────────── → note 3
├── Full reference (pointers) ───────────────────── → note 3 (→ note 4, → reference/wizard rt/rf)
└── Related docs (links) ────────────────────────── → note 3 References (link-out cli/onboarding)
start/wizard-cli-reference.md  (5 H2)
├── What the wizard does ────────────────────────── → note 4 (oc_start_wizard_cli_reference)
├── Local flow details <Steps> (config-detect, model/auth,
│     workspace, gateway, channels, daemon, health, skills,
│     finish) ───────────────────────────────────── → note 4
├── Remote mode details ─────────────────────────── → note 4
├── Auth and model options <AccordionGroup> (Anthropic,
│     OpenAI OAuth/device/key, xAI×3, OpenCode, generic,
│     Vercel/Cloudflare gateway, MiniMax, StepFun,
│     Synthetic, Ollama, Moonshot/Kimi, Custom, Skip) → note 4
├── Outputs and internals (openclaw.json fields,
│     wizard.* RPC, Signal setup) ─────────────────── → note 4
└── Related docs (links) ────────────────────────── → note 4 References (link-out wizard/automation/cli)
start/wizard-cli-automation.md  (3 H2)
├── Baseline non-interactive example ────────────── → note 5 (oc_start_wizard_cli_automation)
├── Provider-specific examples <AccordionGroup>
│     (Anthropic, Gemini, Z.AI, Vercel/Cloudflare,
│     Moonshot, Mistral, Synthetic, OpenCode, Ollama,
│     Custom) ──────────────────────────────────── → note 5
├── Add another agent (scripted) ────────────────── → note 5
└── Related docs (links) ────────────────────────── → note 5 References (link-out wizard/reference/cli)
start/showcase.md  (8 H2 cluster sections)
├── Fresh from Discord ──────────────────────────── → note 6 (oc_start_showcase)
├── Automation and workflows ────────────────────── → note 6
├── Knowledge and memory ────────────────────────── → note 6
├── Voice and phone ─────────────────────────────── → note 6
├── Infrastructure and deployment ───────────────── → note 6
├── Home and hardware ───────────────────────────── → note 6
├── Community projects ──────────────────────────── → note 6
├── Submit your project ─────────────────────────── → note 6
└── Related (links) ─────────────────────────────── → note 6 References (link-out getting-started/openclaw)
```
No orphaned sections. Provider/auth detail, per-channel setup, gateway flags, CLI command pages, daemon/install,
and concept (workspace/memory/heartbeat/session/soul) sections are LINKED to their owning sub-plans, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none — no page split) | — | Every page is ≤1,883w (< 2,500w cap) and single-BB; each maps to exactly one `oc_*` note. |
| start/quickstart.md (78w redirect stub) | FOLDED into note 1 (`oc_start_openclaw`) as a `## References` pointer | The page is a pure "Quick start has moved to Getting Started" redirect (two cards → Getting Started + Onboarding-CLI) with no standalone digestible content; a dedicated note would be a near-empty orphan. `start/getting-started` is owned by sibling sub-plan st01; this sub-plan only records the redirect as a pointer. Net: 7 pages → 6 notes. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (7,219 measured words). New `oc_` notes: **6**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×5** (notes 1–5: assistant setup, dev setup, onboarding hub, onboarding reference,
  CLI automation) · **argument ×1** (note 6: showcase community-evidence gallery — claims OpenClaw's real-world
  reach, supported by curated examples).
- Est. digest words: **~3,500** (avg ~580/note; all ≤700w, far under the 2,500w cap).
- Source code fences: openclaw 11 · setup 9 · wizard 3 · wizard-cli-automation 15 · (quickstart/showcase/
  wizard-cli-reference 0). Code-heavy `wizard-cli-automation` (15 fences) keeps ≤6 by reproducing one
  representative non-interactive command plus a compact per-provider flag table (flags listed as prose/table, not
  10 near-identical fenced blocks). All other notes are naturally ≤6.
- **Cross-refs (LOCKED at raised xref-augment floors, 2026-06-21):** every note maps **≥8 relevance-selected
  `oc_*`) PLUS relevant `repo_openclaw*`, each with a per-link relevance statement, ALL existing targets
  10t/11s/11d · oc_start_setup 10t/12s/11d · oc_start_wizard 10t/11s/11d · oc_start_wizard_cli_reference
  12t/13s/12d · oc_start_wizard_cli_automation 10t/11s/11d · oc_start_showcase 10t/11s/11d.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> Sibling `oc_*` notes (this series) do not exist yet → marked **(planned, this series)** and count toward the
> rendered for the executor as `- [Name](relpath.md) — what it is; relevance: why THIS note`. Relative paths are
> FROM a note at `resources/documentation/openclaw/oc_X.md` (term → `../../term_dictionary/`; snippet →
> `../../code_snippets/`; sibling oc_ → `oc_Y.md`; other doc → `../<folder>/`; repo →
> `../../../areas/code_repos/`; entry → `../../../0_entry_points/`; thought/analysis → `../../analysis_thoughts/`).

### oc_start_openclaw (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway this note onboards; relevance: the product the whole walkthrough sets up as a personal assistant.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents that run commands and send messages; relevance: the "Safety first" section warns you are putting such an agent in a position to act on your machine.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — proactive periodic agent run; relevance: the Heartbeats section documents the 30m default, `HEARTBEAT_OK` suppression, and `ackMaxChars`.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the assistant config sets `agents.defaults.model.primary`.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: the worked assistant config uses `anthropic/claude-opus-4-6`.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — adversarial instruction smuggling; relevance: the safety-first tool-policy caution about agents reading inbound content.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: gateway token vs password auth + the shared-secret Control UI prompt at onboarding finish.
- [SOUL.md](../../term_dictionary/term_soul_md.md) — agent persona/instructions file; relevance: "the config that turns it into an assistant" tunes persona in `SOUL.md`.
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — agent operating-instructions workspace file; relevance: the "Give the agent a workspace (AGENTS)" section seeds `AGENTS.md` + bootstrap files.

**Docs**
- [oc_start_setup](oc_start_setup.md) — advanced/dev setup (planned, this series); relevance: the follow-on once the basic assistant runs.
- [oc_start_wizard](oc_start_wizard.md) — CLI onboarding hub (planned, this series); relevance: the guided flow that produces this assistant config.
- [cc_quickstart](../claude_code/cc_quickstart.md) — Claude Code "run your first chat" walkthrough; relevance: closest sibling-tool first-contact procedure.
- [cc_overview](../claude_code/cc_overview.md) — Claude Code product overview; relevance: analogous coding-agent product entry point.
- [hermes_quickstart_first_chat](../hermes_agent/hermes_quickstart_first_chat.md) — Hermes first-chat quickstart; relevance: the same "5-minute first message" pattern in the sibling ecosystem.
- [hermes_personality_soul](../hermes_agent/hermes_personality_soul.md) — Hermes persona/SOUL config; relevance: analogous "turn it into an assistant" persona tuning.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — Hermes workspace memory; relevance: analog of the AGENTS workspace + memory-loading model.
- [hermes_guide_team_telegram_assistant](../hermes_agent/hermes_guide_team_telegram_assistant.md) — chat-native assistant guide; relevance: the same always-on chat-assistant deployment shape.
- [cc_context_window_anatomy](../claude_code/cc_context_window_anatomy.md) — context window structure; relevance: grounds the sessions/`/compact` context-budget discussion.
- [hermes_messaging_whatsapp_baileys](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp channel setup; relevance: the two-phone WhatsApp pairing this note recommends.
- [pi_quickstart](../pi/pi_quickstart.md) — Pi agent quickstart; relevance: parallel coding-agent "install → first run" path.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway codebase; relevance: the gateway this walkthrough runs.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime + workspace; relevance: heartbeat runtime + AGENTS workspace seeding.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — workspace memory loader; relevance: `MEMORY.md` optional load behavior.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: per-sender session jsonl + `/new`/`/reset` triggers.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: the WhatsApp channel this walkthrough pairs.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat delivery buffering; relevance: implements the proactive heartbeat run + `HEARTBEAT_OK` suppression.
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity/workspace; relevance: the AGENTS/IDENTITY workspace files this note seeds.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap file budget; relevance: the auto-created `AGENTS.md`/`SOUL.md`/`HEARTBEAT.md` bootstrap set.
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — workspace memory root files; relevance: `MEMORY.md` optional loading into normal sessions.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — `/compact` + reset; relevance: the Sessions-and-memory `/compact` and `/new`/`/reset` behavior.
- [snippet_openclaw_gateway_session_reset_mutation_perform](../../code_snippets/snippet_openclaw_gateway_session_reset_mutation_perform.md) — session reset mutation; relevance: per-sender daily/idle session reset config.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — outbound send policy; relevance: heartbeat `directPolicy` / DM-target delivery suppression.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — inbound attachment sanitize; relevance: the inbound `{{MediaPath}}`/`{{MediaUrl}}`/`{{Transcript}}` media handling.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media pipeline; relevance: the "media in and out" inbound/outbound flow.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM allowlist; relevance: the `channels.whatsapp.allowFrom` allowlist safety control.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy gate; relevance: the safety-first tool-policy / `tools.fs.workspaceOnly` boundary.

**Other vault**

### oc_start_setup (10t · 12s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: the product this advanced/dev setup runs (`pnpm gateway:watch` / packaged CLI).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent class; relevance: the dev setup is for working ON the agent gateway TypeScript itself.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored auth token; relevance: the credential-storage map's `auth-profiles.json` + legacy `oauth.json` import.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: the credential storage map (per-channel token files, SecretRef providers).
- [WebSocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: the "wrong port" footgun — Gateway WS defaults to `ws://127.0.0.1:18789`.
- [Sandbox](../../term_dictionary/term_sandbox.md) — execution isolation; relevance: the fs trust model / where agent state lives.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — per-agent auth-profile store; relevance: `~/.openclaw/agents/<id>/agent/auth-profiles.json` in the credential map.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret storage abstraction; relevance: the SecretRef (env/file/exec) credential providers in the storage map.
- [Cron](../../term_dictionary/term_cron.md) — scheduled execution; relevance: the systemd-user-service "lingering" keep-alive that underlies background scheduling.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — pooled credential management; relevance: the "what to back up" credential-storage map for multi-account state.

**Docs**
- [oc_start_openclaw](oc_start_openclaw.md) — assistant setup (planned, this series); relevance: the basic setup this dev workflow extends.
- [oc_start_wizard_cli_reference](oc_start_wizard_cli_reference.md) — onboarding reference (planned, this series); relevance: the credential/profile paths cross-referenced here.
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — env/config setup; relevance: analogous "keep config outside the repo" tailoring.
- [cc_settings_reference](../claude_code/cc_settings_reference.md) — settings file reference; relevance: parallel to `~/.openclaw/openclaw.json` config-outside-repo model.
- [cc_dot_claude_directory](../claude_code/cc_dot_claude_directory.md) — `.claude` state directory; relevance: analog of the `~/.openclaw/` state/credentials/workspace layout.
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — volume + supervision setup; relevance: the gateway supervision / keep-running concern (systemd/linger analog).
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway run/ops; relevance: analogous "run the gateway yourself" operational workflow.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — headless OAuth copy; relevance: the headless/server credential-copy pattern in the storage map.
- [band_setup](../band/band_setup.md) — coding-agent setup; relevance: parallel stable-vs-dev install decision.
- [band_connect_remote_agent](../band/band_connect_remote_agent.md) — remote agent connection; relevance: pointing a UI/app at a self-run gateway (Local connection mode analog).
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — run-mode selection; relevance: stable (bundled) vs bleeding-edge (terminal) workflow choice.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway codebase; relevance: the repo run via `pnpm gateway:watch` / `node openclaw.mjs gateway`.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway internals; relevance: watch/supervision/port behavior + `gateway:watch` tmux session.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding/setup CLI; relevance: the `openclaw setup` bootstrap step.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — secret/credential handling; relevance: the credential-storage map / SecretRef providers.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: `pnpm gateway:watch` env (`OPENCLAW_GATEWAY_WATCH_*`) behavior.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — watch hot-reload respawn; relevance: the dev gateway watcher reload-on-change loop.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — WS listen/bind; relevance: the `ws://127.0.0.1:18789` port + bind footgun.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: editing `~/.openclaw/openclaw.json` without restarting.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload plan; relevance: the config-outside-repo tailoring being picked up live.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: the credential-storage map + SecretRef providers.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile resolution order; relevance: `auth-profiles.json` model-auth profile in the storage map.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: the headless copy of `auth-profiles.json` + legacy `oauth.json` import.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger env; relevance: the Linux `loginctl enable-linger` user-service keep-alive.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervision; relevance: keeping the gateway alive (stable vs dev supervision).
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — `openclaw setup` config write; relevance: the bootstrap `openclaw setup` step.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — channel allowlist creds; relevance: per-channel `*-allowFrom.json` pairing allowlists in the storage map.

**Other vault**

### oc_start_wizard (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `openclaw onboard` configures this gateway.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization flow; relevance: the Model/Auth step offers provider OAuth flows.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored token; relevance: auth-profile token storage seeded by onboarding.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: the Gateway step's token/password auth mode choice.
- [WebSocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: the Gateway step sets port/bind (default 18789).
- [LLM](../../term_dictionary/term_llm.md) — language model; relevance: the Model/Auth step picks a default model.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: Anthropic Claude CLI / API-key preferred onboarding paths.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — first-DM pairing approval; relevance: Telegram/WhatsApp DMs default to allowlist + pairing prompt.
- [Skills](../../term_dictionary/term_skills.md) — agent skill packages; relevance: the Skills step installs recommended skills + deps.
- [Agents.md](../../term_dictionary/term_agents_md.md) — workspace seed file; relevance: the Workspace step seeds bootstrap files (AGENTS etc.).

**Docs**
- [oc_start_wizard_cli_reference](oc_start_wizard_cli_reference.md) — full onboarding reference (planned, this series); relevance: the detailed step breakdown this hub points to.
- [oc_start_wizard_cli_automation](oc_start_wizard_cli_automation.md) — non-interactive onboarding (planned, this series); relevance: the scripted variant of this flow.
- [pi_provider_auth](../pi/pi_provider_auth.md) — coding-agent provider auth; relevance: analogous Model/Auth provider-choice step.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code auth; relevance: analog of the Anthropic Claude-CLI/API-key auth choice.
- [hermes_provider_xai_grok_oauth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — provider OAuth flow; relevance: the provider OAuth path offered in the Model/Auth step.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — dashboard/control-UI auth; relevance: the "fastest first chat: open the Control UI" onboarding hint.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel setup; relevance: the Channels step (Telegram/WhatsApp/Discord/Slack/Signal).
- [hermes_skills_system](../hermes_agent/hermes_skills_system.md) — skills install/system; relevance: the Skills step (install recommended skills + node manager).
- [band_adapter_setup](../band/band_adapter_setup.md) — guided adapter setup; relevance: parallel guided onboarding (QuickStart vs Advanced defaults).
- [hermes_quickstart_next_layer](../hermes_agent/hermes_quickstart_next_layer.md) — post-quickstart config; relevance: the "add another agent / reconfigure later" continuation.
- [cc_skills_overview](../claude_code/cc_skills_overview.md) — skills concept; relevance: grounds the onboarding Skills install step.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding wizard; relevance: the `openclaw onboard` flow itself.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway; relevance: the gateway the wizard configures.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent/workspace runtime; relevance: `agents add` workspace + auth profiles.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: the provider/auth choices the wizard offers.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — interactive prompter; relevance: the guided terminal prompt UX of `openclaw onboard`.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard config write; relevance: what the 7 onboarding steps write into `openclaw.json`.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard step composition; relevance: the Model/Workspace/Gateway/Channels/Daemon/Health/Skills step assembly.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `openclaw onboard`/`configure`/`agents add` command surface.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI routing; relevance: how `onboard`/`configure` dispatch into the wizard.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config; relevance: the `agents add` workspace/agentDir config the wizard writes.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: Telegram/WhatsApp allowlist-default prompt.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth mode; relevance: the Gateway step's token-auth-on-loopback default.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skills planner; relevance: the Skills step's recommended-skill selection.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — skill availability/requirements; relevance: the Skills step's requirement check + optional deps.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — daemon LaunchAgent render; relevance: the Daemon step's macOS LaunchAgent install.

**Other vault**

### oc_start_wizard_cli_reference (12t · 13s · 12d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: this is the full reference for `openclaw onboard`.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated authorization; relevance: OpenAI Code subscription OAuth + xAI OAuth/device-code flows.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored token; relevance: `auth-profiles.json` + legacy `oauth.json` import paths.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: gateway token vs SecretRef, password mode, non-loopback-requires-auth.
- [WebSocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: remote-mode `ws://` gateway URL + bind.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC protocol; relevance: the `wizard.start`/`next`/`cancel`/`status` gateway RPC surface.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model providers; relevance: the full auth/model option matrix (MiniMax/StepFun/Synthetic/Ollama/Moonshot/…).
- [LLM](../../term_dictionary/term_llm.md) — language model; relevance: the model picker + preferred-provider filter behavior.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider; relevance: the Custom Provider (OpenAI/Anthropic-compatible) choice.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — auth-profile store; relevance: where API keys + OAuth are persisted (`auth-profiles.json`).
- [PKCE](../../term_dictionary/term_pkce.md) — OAuth code-exchange security; relevance: the browser/device-code OAuth flows (xAI device code, OpenAI device pairing).
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — discoverable model list; relevance: the model picker detecting + filtering provider models.

**Docs**
- [oc_start_wizard](oc_start_wizard.md) — onboarding hub (planned, this series); relevance: the short guide this reference expands.
- [oc_start_wizard_cli_automation](oc_start_wizard_cli_automation.md) — non-interactive flags (planned, this series); relevance: the scripted equivalents of each interactive option.
- [cc_authentication](../claude_code/cc_authentication.md) — auth-option reference; relevance: analogous per-provider auth-method matrix.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth reference; relevance: analogous per-provider auth-choice catalog.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud gateways; relevance: the Vercel/Cloudflare AI Gateway accordions.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — custom provider registration; relevance: the Custom Provider OpenAI/Anthropic-compatible flags.
- [hermes_provider_minimax_oauth](../hermes_agent/hermes_provider_minimax_oauth.md) — MiniMax OAuth; relevance: the MiniMax accordion (`minimax/...` vs `minimax-portal/...`).
- [hermes_provider_xai_grok_oauth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — xAI Grok OAuth; relevance: the xAI OAuth / device-code / API-key accordions.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: the broad provider/auth option matrix.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — credential pooling; relevance: credential-storage modes (plaintext vs ref).
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — RPC protocol; relevance: analog of the `wizard.*` gateway RPC surface clients render.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — headless OAuth copy; relevance: the headless/server "complete OAuth on a browser machine then copy auth-profiles.json" tip.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding flow + RPC; relevance: the wizard this reference documents.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway internals; relevance: gateway auth/bind/daemon behavior + `wizard.*` RPC.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: the auth/model option matrix.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — secret handling; relevance: SecretRef / credential-storage modes.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — config outputs; relevance: the `openclaw.json` fields onboarding writes.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — step composition; relevance: the per-step local-flow assembly this page details.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth (Claude CLI); relevance: the "Anthropic Claude CLI as preferred local path" option.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: the headless copy of `auth-profiles.json`.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution order; relevance: plaintext vs env-ref credential-storage modes.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth modes; relevance: token vs password, SecretRef, loopback-still-needs-auth.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret resolution; relevance: `--gateway-token-ref-env` SecretRef resolution.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: the `wizard.*` RPC method group.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: how `wizard.start/next/cancel/status` calls are framed.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery; relevance: "pick default model from detected options" picker.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: the Anthropic API-key / Claude-CLI auth accordion.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — Ollama local provider; relevance: the Ollama Cloud/Local/Cloud+Local accordion.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render; relevance: the Daemon-install step (systemd user unit, linger).

**Other vault**

### oc_start_wizard_cli_automation (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: the `--non-interactive` onboarding automated here.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: the page's purpose — automating onboarding in scripts/CI.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: `--auth-choice` + `--secret-input-mode plaintext|ref`.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored token/ref; relevance: env-backed key refs stored in auth profiles in `ref` mode.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external providers; relevance: the per-provider non-interactive examples (Anthropic/Gemini/Z.AI/Mistral/Moonshot/Synthetic/OpenCode/Ollama/custom).
- [LLM](../../term_dictionary/term_llm.md) — language model; relevance: `--model` / `--custom-model-id` selection.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider; relevance: `--auth-choice custom-api-key` + `--custom-compatibility` custom-provider flags.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — auth-profile store; relevance: `ref` mode writes `keyRef` into auth profiles instead of plaintext.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret storage; relevance: env-backed `--secret-input-mode ref` secret handling in CI.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — channel pairing; relevance: scripted `agents add --bind` channel routing.

**Docs**
- [oc_start_wizard](oc_start_wizard.md) — interactive hub (planned, this series); relevance: the interactive flow these flags automate.
- [oc_start_wizard_cli_reference](oc_start_wizard_cli_reference.md) — full flag semantics (planned, this series); relevance: each `--flag` here is defined there.
- [cc_headless_mode](../claude_code/cc_headless_mode.md) — headless/non-interactive mode; relevance: the same scripted no-prompt invocation pattern.
- [cc_headless_examples](../claude_code/cc_headless_examples.md) — headless command examples; relevance: analogous copy-paste non-interactive command set.
- [hermes_guide_pipe_script_output](../hermes_agent/hermes_guide_pipe_script_output.md) — scripted/piped runs; relevance: `--json` machine-readable summary for scripts.
- [hermes_guide_cron_script_only](../hermes_agent/hermes_guide_cron_script_only.md) — cron/script-only runs; relevance: the unattended CI/cron onboarding shape.
- [cc_gitlab_ci_cd](../claude_code/cc_gitlab_ci_cd.md) — CI/CD pipeline integration; relevance: running onboarding inside a CI pipeline.
- [cc_github_actions](../claude_code/cc_github_actions.md) — GitHub Actions integration; relevance: secret-via-env (`$ANTHROPIC_API_KEY`) non-interactive auth in CI.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider env vars; relevance: the per-provider `$..._API_KEY` env vars the examples reference.
- [pi_cli_reference](../pi/pi_cli_reference.md) — CLI flag reference; relevance: analogous non-interactive CLI-flag catalog.
- [hermes_automation_blueprints_scheduled](../hermes_agent/hermes_automation_blueprints_scheduled.md) — scheduled automation; relevance: scripted/unattended agent provisioning analog.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding CLI; relevance: the `--non-interactive` onboarding path.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway; relevance: `--gateway-port`/`--gateway-bind` flags.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: scripted `agents add` + `--bind` routing.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: the provider-specific flag sets.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: the `openclaw onboard` / `agents add` commands automated.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI routing; relevance: how `--non-interactive` flags dispatch.
- [snippet_openclaw_cli_run_main_primary](../../code_snippets/snippet_openclaw_cli_run_main_primary.md) — CLI main entry; relevance: argv parsing for the non-interactive flag set.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — config write; relevance: what `--non-interactive` writes into `openclaw.json`.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution order; relevance: `--secret-input-mode plaintext` vs `ref` storage.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret resolution; relevance: env-backed ref-mode secret resolution + fail-fast on missing env var.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: the `--anthropic-api-key` baseline example.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: the `--auth-choice openai-api-key` example.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — Ollama local; relevance: the `--auth-choice ollama --custom-model-id` example.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator/custom endpoint; relevance: the `--custom-base-url`/`--custom-compatibility` custom-provider example.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config; relevance: scripted `agents add --workspace --model --bind` writes.

**Other vault**

### oc_start_showcase (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: the product these community projects are built on.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed coding agents; relevance: PR-review loops, build-a-skill-on-the-fly, autonomous bug fixes.
- [Chatbot](../../term_dictionary/term_chatbot.md) — chat interface agent; relevance: chat-native builds on Telegram/WhatsApp/Discord.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the Beeper local MCP API integration example.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: browser-control / skill tool use across the automation examples.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — multi-agent protocol; relevance: the 14+ agent orchestration (Opus orchestrator → Codex workers) example.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: Tesco/TradingView/ParentPay "no API, just browser control" projects.
- [Skills](../../term_dictionary/term_skills.md) — agent skill packages; relevance: "build a skill in minutes" (wine cellar, Jira, Todoist) examples.
- [Agentic Workflow](../../term_dictionary/term_agentic_workflow.md) — multi-step autonomous workflow; relevance: scheduled briefings, support loops, "just do the task" automations.

**Docs**
- [oc_start_openclaw](oc_start_openclaw.md) — assistant setup (planned, this series); relevance: the setup behind the showcased projects.
- [hermes_integrations_overview](../hermes_agent/hermes_integrations_overview.md) — integrations catalog; relevance: the analogous "what you can connect" ecosystem breadth.
- [hermes_messaging_homeassistant](../hermes_agent/hermes_messaging_homeassistant.md) — Home Assistant integration; relevance: the Home Assistant add-on / skill showcase entries.
- [hermes_spotify_integration](../hermes_agent/hermes_spotify_integration.md) — third-party service integration; relevance: the "control a real service via chat" project pattern.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice mode; relevance: the Voice/phone cluster (Clawdia bridge, transcription).
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — browser automation; relevance: the browser-control shopping/booking/trading projects.
- [hermes_features_overview](../hermes_agent/hermes_features_overview.md) — feature catalog; relevance: the breadth of capabilities the gallery demonstrates.
- [hermes_guide_team_telegram_assistant](../hermes_agent/hermes_guide_team_telegram_assistant.md) — chat-native assistant; relevance: the Telegram-driven build/deploy projects (iOS app via Telegram).
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media in/out; relevance: voice-note TTS + screenshot/camera projects.
- [cc_overview](../claude_code/cc_overview.md) — coding-agent overview; relevance: the devtools/PR-review category of projects.
- [band_mcp_platform_automation](../band/band_mcp_platform_automation.md) — MCP-driven automation; relevance: the MCP-integration + automation projects.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway; relevance: the gateway powering every showcased project.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills system; relevance: the "build a skill in minutes" + ClawHub-published skills.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — chat channels; relevance: the Telegram/WhatsApp/Discord chat surfaces.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — mobile/desktop apps; relevance: the iOS app + Agents UI desktop projects.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skills planner; relevance: the on-the-fly skill generation in the showcase.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest format; relevance: how the showcased custom skills are packaged.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — skill availability; relevance: skills built/tested then offered (wine cellar 962-bottle example).
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram transport; relevance: the Telegram-delivered projects (PR review, briefings, iOS app).
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket mode; relevance: the Slack auto-support project.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord intents; relevance: the "fresh from Discord" chat-native builds.
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP server; relevance: the 14+ agent orchestration under one gateway.
- [snippet_openclaw_agents_subagent_registry_lifecycle](../../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md) — subagent lifecycle; relevance: the orchestrator → Codex worker delegation example.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — subagent spawn policy; relevance: multi-agent sandboxing (Clawdspace) in the 14+ agent project.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media pipeline; relevance: voice-note / screenshot / camera media projects.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice call manager; relevance: the Clawdia Vapi phone-bridge project.

**Other vault**

> **Augment-stage cleanup applied (2026-06-21):** the plan-stage MISSING/reconsidered candidates were resolved
> `term_function_calling`; added `term_browser_automation`, `term_skills`, `term_agentic_workflow`). Every locked
> Terms Plan).

## Undigested Terms Plan

Per master: OpenClaw vocabulary that is the *subject* of a doc page is digested as `oc_*` documentation notes, not
new `term_dictionary` entries; the only `term_dictionary` interaction is LINKING existing terms. **Expected: 0 new
`term_dictionary` captures.**

| Term (encountered in source) | Disposition |
|---|---|
| heartbeat / proactive mode | Link existing `term_heartbeat`; the OpenClaw-specific behavior (30m default, `HEARTBEAT_OK`, `ackMaxChars`) lives in note 1. |
| onboarding wizard / `openclaw onboard` | Documented in notes 3–5 (oc_* doc notes); no term note (it is a CLI command — CLI page owned by cl05). |
| agent workspace / AGENTS / bootstrap files | Link concept doc `oc_concepts_agent_workspace` (planned, co01 sibling) + existing `repo_openclaw_agents`; no new term. |
| heartbeat / session / compaction / `/compact` | Link existing `term_heartbeat` / `term_compaction`; `term_session` is DB-MISSING → link `term_compaction` + note-internal definition reference only (no new term — session is a doc-page subject owned by Concepts co06). |
| SecretRef / secret-input-mode ref | Link existing `term_oauth_token` / `term_authentication`; SecretRef is an OpenClaw config mechanism → documented inline in note 4, not promoted (gateway/secrets owned by gw05/gw06). |
| Tailscale / loopback / bind | Link Gateway sub-plan docs (gw); `term_tailscale` is DB-MISSING and is a third-party tool subject of `gateway/tailscale` (gw06) — not promoted here. |
| daemon / LaunchAgent / systemd user unit / Scheduled Task | Documented inline in notes 2 & 4; install/platform detail owned by Install/Platforms sub-plans; no new term. |
| custom provider (OpenAI/Anthropic-compatible) | Link existing `term_provider_plugin` / `term_third_party_genai_services`; provider detail owned by Providers (pr). |
| showcase / ClawHub / skills | Link existing `repo_openclaw_skills`; ClawHub is owned by ClawHub sub-plans (cw01–cw03); no new term. |

**New-term candidates: NONE.** No genuinely cross-cutting, vault-reusable term with no doc-page home AND no
existing note was found in these 7 pages — all encountered vocabulary either has an existing term note to link or
is a doc-page subject owned by another sub-plan. (Augment Step 2d re-scans to confirm.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** st02 authors zero `term_dictionary` notes. Inherited from master: were a new term ever
`acronym_glossary_*.md` (best-fit glossary for agentic/LLM vocab) — not inlined in any `oc_*` digest note.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (6 notes, P1). All gates must pass before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format + YAML | `/tessellum-check-note-format` + `scripts/check_note_format.py` + `scripts/check_yaml_frontmatter.py` (fixed field order; no forbidden fields; quoted year tags; itemized keywords/topics). |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/start/<page>.md`; every claim/command traceable to source; no fabricated flags/paths. |
| G3 | Density + Coverage | ≤400 lines · ≤2,500 words · ≤6 code blocks · one `building_block` per note; every mapped H2/H3 (+ MDX Steps/Accordion) section present. |
| G4 | Cross-Reference | `## Related Notes` ≥6 relevance-selected `term_dictionary` terms + sibling `oc_*` + `repo_openclaw*` + other vault, each indexed `[text](path.md)` with a relevance statement. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` (correct relative paths) post-write; reindex; 0 broken links. |
| G7 | Discoverability (inbound) | Each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (anti-island) — satisfied via `entry_openclaw_docs.md` + repo/term inlinks. |
| G8 | In-degree ≥1 | `note_links` confirms in-degree ≥1 for every new note after reindex. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_start_openclaw oc_start_setup oc_start_wizard oc_start_wizard_cli_reference oc_start_wizard_cli_automation oc_start_showcase"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # at least one sibling oc_* related link
  grep -qE "\($SIBLING_PREFIX[a-z0-9_]+\.md\)" "$f" || echo "$n NO sibling $SIBLING_PREFIX link"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (${words}w/${cb}cb/${lines}L)"
done

# YAML frontmatter sweep over the whole folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences | Within caps (≤400L · ≤2500w · ≤6cb · 1 BB)? |
|---|---|---|---:|---:|---|
| 1 | oc_start_openclaw | procedure | 650 | 11 → ≤6 kept (login/gateway, minimal config, assistant config, heartbeat, media; rest as prose) | ✅ |
| 2 | oc_start_setup | procedure | 600 | 9 → ≤6 kept (setup, gateway:watch, health, footguns; credential map as prose list) | ✅ |
| 3 | oc_start_wizard | procedure | 550 | 3 → 3 (onboard, locale, configure) | ✅ |
| 4 | oc_start_wizard_cli_reference | procedure | 700 | 0 (reference prose; option matrix as table/list) | ✅ |
| 5 | oc_start_wizard_cli_automation | procedure | 500 | 15 → ≤6 (1 baseline + 1 ref + 1 agents-add example; per-provider flags as a compact table, not 10 fences) | ✅ |
| 6 | oc_start_showcase | argument | 500 | 0 (project gallery as themed prose/list, not card MDX) | ✅ |

No note approaches the caps. The two code-dense pages (`wizard-cli-automation` 15 fences, `openclaw` 11 fences)
deliberately reproduce a representative subset (≤6) and render the remaining near-identical command variants as
a flag table / prose to stay within the density cap without losing the option coverage.

## Entry Point Decision (inherited from master)

Contributes **6 rows** to `entry_openclaw_docs.md` (the navigation hub CREATED as a master pre-step W1, >30
corpus notes ⇒ required) under a **"Start / Getting Started"** cluster (shared with sibling sub-plan st01). Each
of the 6 notes receives its entry-point back-link at finalization, satisfying G7/G8 (≥1 outside-folder inbound).
No new entry point is created by this sub-plan; W2/W3 parent-hub wiring is owned by the master pre-step.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution):

- `entry_openclaw_docs.md` (planned, master pre-step) → **all 6** notes (primary anti-island guarantee).
- `repo_openclaw_cli_wizard.md` (existing) → notes 3, 4, 5 (the onboarding wizard ↔ its docs).
- `repo_openclaw.md` (existing) → notes 1, 2 (gateway run/setup ↔ its docs).
- `repo_openclaw_agents.md` (existing) → notes 1, 3 (workspace/heartbeat + `agents add`).
- `repo_openclaw_skills.md` (existing) → note 6 (showcase "build a skill" projects).
- `term_openclaw.md` (existing) → notes 1, 6 (product overview ↔ assistant setup + showcase).
- `term_heartbeat.md` (existing) → note 1 (proactive-mode heartbeat).
- `term_ci_cd.md` (existing) → note 5 (CI/scripted onboarding).

Each inbound link is reciprocal where the new note also links back (added in the note's `## Related Notes`).

## Pacing Rules (inherited from master)

One execution phase, 6 notes (≤ fan-out cap of ~30 agents/run). Re-read each source page before authoring;
reproduce commands/config verbatim from the mirror; one BB per note; ≤6 code blocks per note. `git pull --rebase
--autostash` before committing; commit+push the phase as one cycle (no Claude co-author trailer). Reindex
incrementally; verify `note_links` (in-degree ≥1) + 0 broken links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — READY (9/9 checkpoints pass) |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

## Augmentation Report (2026-06-21)

**Scope of this augment pass:** per-note Related Notes mapping raised to xref-augment floors (≥8 terms · ≥10
**Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)** section. Summary Statistics cross-ref line
updated to the locked per-note counts.


| Note | Terms | Snippets | Docs (existing / planned-sibling) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_start_openclaw | 10 | 11 | 11 (9 / 2) | 5 | ✅ |
| oc_start_setup | 10 | 12 | 11 (9 / 2) | 4 | ✅ |
| oc_start_wizard | 10 | 11 | 11 (9 / 2) | 4 | ✅ |
| oc_start_wizard_cli_reference | 12 | 13 | 12 (10 / 2) | 4 | ✅ |
| oc_start_wizard_cli_automation | 10 | 11 | 11 (9 / 2) | 4 | ✅ |
| oc_start_showcase | 10 | 11 | 11 (10 / 1) | 4 | ✅ |

  (the `/compact` context-budget term) + `term_soul_md` + `term_agents_md`; the reconsidered `term_perplexity`
  wizard/cli/agents/auth-profiles/gateway/daemon/provider/model-catalog/channels/sessions/memory/skills/acp).
  `claude_code/cc_*`, `pi/pi_*`, `hermes_agent/hermes_*`, `band/band_*` coding-agent corpora, plus 1–2 planned
  sibling `oc_*` (this series) toward the 10-doc floor.
- **Deterministic ghost sweep (2026-06-21):** 221 total `.md` links in the locked section → 215 EXISTING

**New-term candidates:** NONE. The augment-stage re-read (Step 2d) confirmed the plan-digestion Step 4e finding —
every term encountered in the 7 pages either has an existing term note to link or is a doc-page subject owned by
another sub-plan (session→co06, tailscale→gw06, agent-workspace→co01, ClawHub→cw). No genuinely cross-cutting,
vault-reusable term with no doc-page home AND no existing note was found. **Expected `term_dictionary` captures: 0.**
Best-fit glossary, were a term ever required: `acronym_glossary_*` for agentic/LLM vocabulary (inherited from master).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table per batch (G1–G6, G8, G9) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table present for the single execution phase: G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost detect+redirect, G6 broken-link fix, G7/G8 discoverability/in-degree. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | Entry Point Decision contributes 6 rows to `entry_openclaw_docs.md` (CREATED master pre-step W1, >30 corpus notes ⇒ required); no new entry point created here; W2/W3 owned by master. |
| CP4 | Plan size (≤30 or split) | **PASS** | 6 notes — well under 30; single execution phase ≤ fan-out cap. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited verbatim from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` opener, `## Related Notes`, `building_block`, `source_url`, `access_control_group`); validation script greps `## Overview|## Related Notes`. |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment: every note ≤700w / ≤6 code blocks / 1 BB; code-dense pages (`wizard-cli-automation` 15 fences, `openclaw` 11 fences) reproduce ≤6 + render the rest as a flag table/prose. No borderline note. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured 2026-06-21 (body words): openclaw 1,239 · setup 812 · wizard 846 · wizard-cli-reference 1,843 · wizard-cli-automation 673 · showcase 1,528 · quickstart 46 — all within ±10% of plan estimates; wizard-cli-automation "15 fences" confirmed (3 top-level + 12 MDX-`<Accordion>`-indented). No under-estimation. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements | **PASS** | Both sections present; disposition table maps every encountered term to an existing-note link or owning sub-plan; New-term candidates: NONE; Term-Note Authoring Requirements = N/A (0 new terms) with the inherited `/tessellum-capture-term-note` mandate recorded. |
| CP8f | Term-slug specificity + all-notes collision audit | **PASS** | 0 new term slugs to rename (no captures). Collision audit generalized to the 6 planned `oc_*` doc notes: none duplicate an existing term/doc note — they are page-subject docs (assistant setup / dev setup / onboarding hub / onboarding reference / CLI automation / showcase) with no existing `oc_*` equivalents; `term_openclaw` etc. are LINKED not recreated. |
| CP9 | Discoverability / inlinks executed (G8) | **PASS** | Inlinks section maps every new note to ≥1 outside-folder inbound link (`entry_openclaw_docs` → all 6; repo/term inlinks per note); G8 in-degree ≥1 is in the phase gate table as a gated execution step, not a recommendation. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
