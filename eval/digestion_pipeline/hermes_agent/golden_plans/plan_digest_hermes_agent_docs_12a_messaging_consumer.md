---
title: Hermes Agent Docs Digestion — Sub-Plan 12a — Messaging: Consumer Messengers A
date: 2026-06-15
revised: 2026-06-19
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
mirror_commit: c253b07
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/
pages:
  - user-guide/messaging/whatsapp.md
  - user-guide/messaging/whatsapp-cloud.md
  - user-guide/messaging/signal.md
  - user-guide/messaging/sms.md
  - user-guide/messaging/email.md
  - user-guide/messaging/line.md
  - user-guide/messaging/ntfy.md
---

# Sub-Plan 12a: Messaging — Consumer Messengers A

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP12a's note
> filenames/BBs/coverage are defined. SP12a is **part a of the SP12 split** (the master's "Messaging:
> Consumer & Webhooks" row, split a/b during augmentation). SP12b owns webhooks/open-webui/simplex/
> bluebubbles/photon/homeassistant/msgraph-webhook.

## Scope

SP12a covers the **consumer-messenger platform-setup procedures** for Hermes' messaging gateway:
WhatsApp (the unofficial Baileys bridge AND Meta's official Business Cloud API), Signal (signal-cli
daemon), SMS via Twilio, Email via IMAP/SMTP, LINE (LINE Messaging API), and ntfy (HTTP pub-sub push).
Source = 7 mirrored pages in `inbox/hermes_agent_docs/user-guide/messaging/` (all substantive).
**P2 / messaging.** Every page is a "connect Hermes to platform X" runbook: prerequisites → credentials
→ allowlist/access control → start the gateway → platform-specific delivery behavior → troubleshooting →
security. These notes are the **user-facing setup layer**; they cross-link DOWN to the existing
`snippet_hermes_agent_gw_platform_*` adapter code and the shared gateway runner/pairing/streaming code.

## Content Strategy

- **One BB per note.** Six pages are single-BB procedures → one note each. `whatsapp-cloud.md` (3439w,
  9 code) exceeds the 2500w cap AND mixes a procedural setup arc with a substantial reference/model arc
  (configuration-variable table + inbound/outbound feature matrix + known-limitations + Baileys-vs-Cloud
  comparison table) → **SPLIT into 2 notes** (procedure + model). Total **8 notes**.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the gateway
  concept + DM-pairing + silence-token (SP11a), per-platform session isolation + unauthorized-DM-behavior
  config blocks (SP02 `hermes_messaging_media_settings`), STT/voice/TTS subsystems (SP08), cron delivery /
  `home_channel` (SP06), the credential/secret model (SP03), webhooks/msgraph-webhook adapters (SP12b).
- **Owned NEW term captures: 0.** The gateway concepts these pages exercise (`term_messaging_gateway`,
  `term_dm_pairing`, `term_silence_token`) are **SP11a-owned** and not yet captured → LINK as `+fin`
  forward-refs (EXCLUDED from the ≥8 term floor). A collision audit (below) confirms no platform here
  introduces a genuinely-new, reusable, survives-collision concept that SP12a should own. Product names
  (Baileys, signal-cli, Twilio, cloudflared, ntfy) are **link-only references inside notes**, not term
  captures (master low-value-product-name rule).
  `term_authentication`, `term_autonomous_coding_agents`, `term_subagent`, `term_prompt_injection`.

## Source Pages (Measured 2026-06-15, from local mirror — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/messaging/whatsapp-cloud.md | 3439 | 9 | MIXED procedure+model | 2 (split) |
| user-guide/messaging/whatsapp.md | 1700 | 8 | procedure | 1 |
| user-guide/messaging/signal.md | 1504 | 7 | procedure | 1 |
| user-guide/messaging/line.md | 1258 | 8 | procedure | 1 |
| user-guide/messaging/email.md | 1173 | 4 | procedure | 1 |
| user-guide/messaging/ntfy.md | 1046 | 9 | procedure | 1 |
| user-guide/messaging/sms.md | 896 | 10 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **8 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_messaging_whatsapp_baileys.md` | procedure | whatsapp §Two Modes, §Prerequisites, §Step 1 Setup Wizard (QR scan), §Step 2 Second Phone Number, §Step 3 Configure Hermes (.env + config.yaml), §Session Persistence, §Re-pairing, §Voice Messages, §Message Formatting & Delivery (chunking, markdown map, tool progress, debounce), §Troubleshooting, §Security | ~1500 | WhatsApp via the unofficial Baileys WhatsApp-Web bridge: pick bot-number vs self-chat mode, `hermes whatsapp` QR pairing, get a second number, `.env` allowlist + `unauthorized_dm_behavior`, persisted session dir, voice transcription, 4096-char chunking + markdown conversion + 5s text debounce, ban-risk security. |
| 2 | `hermes_messaging_whatsapp_cloud_setup.md` | procedure | whatsapp-cloud §Quick start, §Prerequisites, §Creating the Meta app (+credential table), §Permanent token (System User), §Exposing Hermes to the internet (cloudflared/ngrok/reverse-proxy), §Configuring the webhook on Meta's side (verify-token handshake + curl probe), §Recipient whitelist (Meta-side), §Allowlist (Hermes-side), §Polishing the profile, §Troubleshooting (graph errors), §Security notes | ~1600 | WhatsApp Business Cloud API setup: `hermes whatsapp-cloud` wizard, Meta app + WABA + Phone-Number-ID/Access-Token/App-Secret/Verify-Token, System-User permanent token, public HTTPS tunnel, Meta webhook verify handshake + curl loop probe, dual Meta-side + Hermes-side allowlists, graph-error troubleshooting, App-Secret/token security. |
| 3 | `hermes_messaging_whatsapp_cloud_model.md` | model | whatsapp-cloud §Configuration reference (full env-var table), §Features (Inbound/Outbound/Interactive UX/Read-receipts/Voice messages), §Known limitations (24h window, group DMs-only, outbound rate limit), §Comparison to the Baileys bridge | ~1400 | The Cloud-API adapter's capability + config model: the `WHATSAPP_CLOUD_*` variable reference, the inbound/outbound/interactive-message feature matrix (vision images, voice notes, tap-to-answer buttons, blue-tick receipts), Meta's 24-hour conversation-window rule + graph-error `131047`, DMs-only/80-msg-sec limits, and the Baileys-vs-Cloud trade-off table. |
| 4 | `hermes_messaging_signal.md` | procedure | signal §Prerequisites (+Installing signal-cli), §Step 1 Link Account (linked device), §Step 2 Start the daemon (`--http`), §Step 3 Configure Hermes (.env), §Access Control (DM + Group), §Features (attachments, native formatting/reply-quotes/reactions, typing, tool-progress suppression, phone redaction, Note-to-Self, health monitoring), §Troubleshooting, §Security, §Env Vars Reference | ~1500 | Signal via the signal-cli HTTP daemon: install signal-cli (Java 17+), link as a secondary device, run `--http` daemon, `.env` account+allowlist+group config, SSE-streamed inbound + JSON-RPC outbound, attachment batching + native bodyRanges formatting + reactions, Note-to-Self single-number mode, SSE reconnect/health, E2EE + phone-redaction security. |
| 5 | `hermes_messaging_sms_twilio.md` | procedure | sms §Prerequisites, §Step 1 Twilio Credentials, §Step 2 Configure Hermes (.env), §Step 3 Configure Twilio Webhook (+exposing), §Step 4 Start the Gateway, §Environment Variables, §SMS-Specific Behavior, §Security (webhook signature validation + allowlists), §Troubleshooting | ~900 | SMS via Twilio: Account-SID/Auth-Token/phone-number, `.env` + `SMS_WEBHOOK_URL` (required for `X-Twilio-Signature` HMAC-SHA1 validation), point the Twilio webhook at `/webhooks/twilio`, plain-text-only 1600-char chunking + echo prevention, allowlist-deny-by-default security, no-encryption caveat. |
| 6 | `hermes_messaging_email.md` | procedure | email §(gateway-vs-Himalaya table), §Prerequisites (Gmail/Outlook/other app passwords), §Step 1 Configure Hermes (.env), §Step 2 Start the Gateway, §How It Works (receiving/sending/attachments/skip-attachments), §Access Control, §Troubleshooting, §Security, §Env Vars Reference | ~1100 | Email via IMAP/SMTP (stdlib `imaplib`/`smtplib`, no external deps): dedicated account + app password, `.env` host/port/poll-interval/allowlist, UNSEEN-polling inbound with subject context + attachment caching + noreply filtering, In-Reply-To/References threaded SMTP replies, `skip_attachments`, app-password + dedicated-account security. |
| 7 | `hermes_messaging_line.md` | procedure | line §How the bot responds (1:1/group/room), §Step 1 Create channel, §Step 2 Expose webhook port, §Step 3 Configure Hermes (.env + config.yaml plugin enable), §Step 4 Set webhook URL, §Step 5 Run gateway, §Slow LLM responses (postback button state machine), §Cron/notification delivery, §Env Var Reference, §Troubleshooting, §Limitations | ~1300 | LINE Messaging API (bundled platform plugin, no core edit): channel access token + secret, public HTTPS webhook at `/line/webhook` (HMAC-SHA256), U/C/R-ID allowlists, `LINE_PUBLIC_URL` for media, free-reply-token-first delivery + the slow-response postback-button state machine (`PENDING→READY→DELIVERED`), 5000-char bubble caps, no-edit/no-markdown limits. |
| 8 | `hermes_messaging_ntfy.md` | procedure | ntfy §Prerequisites, §Configure Hermes (wizard + env vars table), §Identity model (topic-as-identity), §Quick start, §Using ntfy with cron jobs, §Self-hosting ntfy, §Markdown formatting, §Outgoing-only setup, §Limits, §Troubleshooting | ~1000 | ntfy HTTP pub-sub push (httpx, no daemon/SDK): subscribe a topic from the mobile app, `.env` topic+server+token, the topic-IS-the-identity authorization model (allowlist = the topic name), cron-deliverable home channel with out-of-process `standalone_sender_fn`, self-hosting for real access control, 4096-char limit, outgoing-only one-way mode, 401/404 fatal-status + backoff reconnect. |

**SP12a totals:** 8 notes · procedure 7 · model 1 · concept 0 (gateway concepts owned by SP11a term notes).
7 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 8 · procedure 7 · model 1 · concept 0 (messaging-gateway/dm-pairing/silence-token concepts are SP11a-owned terms, linked as +fin).
- Source: 7 digested pages (~11.0K words) → ~9.8K words of notes (modest compression via link-outs to SP02/03/06/08/11a feature pages).
- BB mix: procedure 88%, model 12%.

## Section Coverage Map

```
whatsapp.md (1700w)
├── intro (Baileys/WhatsApp-Web, no Meta acct) / Two-WhatsApp tip / Ban-Risk + Protocol-Update warnings → Note 1
├── Two Modes (separate-bot vs self-chat) / Prerequisites (Node 18+) ──────────── → Note 1
├── Step 1 Setup Wizard (hermes whatsapp, QR scan) ──────────────────────────────── → Note 1
├── Step 2 Second Phone Number (Google Voice / prepaid / VoIP) ───────────────────── → Note 1
├── Step 3 Configure Hermes (.env allowlist, config.yaml unauthorized_dm_behavior) → Note 1 (DM-pairing concept→SP11a)
├── Session Persistence / Re-pairing / Voice Messages ──────────────────────────── → Note 1 (STT/voice→SP08)
├── Message Formatting & Delivery (chunking / markdown map / tool progress / debounce) → Note 1
└── Troubleshooting / Security ──────────────────────────────────────────────────── → Note 1
whatsapp-cloud.md (3439w)
├── intro (official Meta path) / Quick start (hermes whatsapp-cloud) / Prerequisites → Note 2
├── Creating the Meta app (+credential table) / Permanent token (System User) ────── → Note 2
├── Exposing Hermes to the internet (cloudflared / ngrok / reverse-proxy) ────────── → Note 2
├── Configuring the webhook on Meta's side (verify handshake + curl probe) ───────── → Note 2
├── Recipient whitelist (Meta-side) / Allowlist (Hermes-side) / Polishing profile ── → Note 2
├── Troubleshooting (graph errors 100/190/131047/401) / Security notes ──────────── → Note 2
├── Configuration reference (full WHATSAPP_CLOUD_* env-var table) ────────────────── → Note 3
├── Features (Inbound / Outbound / Interactive UX / Read receipts / Voice messages) → Note 3 (vision→SP08; STT→SP08)
├── Known limitations (24h window / group DMs-only / outbound rate limit) ────────── → Note 3
└── Comparison to the Baileys bridge (trade-off table) / See also ────────────────── → Note 3 (Baileys=Note 1)
signal.md (1504w) ── ALL sections ───────────────────────────────────────────────── → Note 4 (STT/voice→SP08; DM-pairing→SP11a)
sms.md (896w) ── ALL sections ────────────────────────────────────────────────────── → Note 5 (cron home-channel→SP06)
email.md (1173w) ── ALL sections ─────────────────────────────────────────────────── → Note 6 (Himalaya skill→SP21 catalog; vision→SP08)
line.md (1258w) ── ALL sections ──────────────────────────────────────────────────── → Note 7 (display/tool-progress config→SP02; cron→SP06)
ntfy.md (1046w) ── ALL sections ──────────────────────────────────────────────────── → Note 8 (cron home-channel→SP06)
```

No source H2/H3 orphaned. All 7 pages fully covered; STT/voice/vision, DM-pairing concept, cron-delivery,
display config, and the Himalaya email skill are intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| whatsapp-cloud.md (3439w, 9 code) | Note 2 (Meta-app/token/tunnel/webhook/allowlist setup, procedure) + Note 3 (config-variable + feature-matrix + limitations + Baileys-comparison, model) | >2500w (MUST split 2500-4000w per Step 3c); ALSO a BB split — the first arc is a step-by-step setup procedure, the second is a reference/capability model (env-var table + inbound/outbound/interactive feature matrix + comparison table). Keeps each note one BB, ≤6 code. |

The other six pages are each ≤1700w, single-BB procedures → one note each, no split.

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_messaging_line` | `term_linear_*`, `term_live_pipeline_templates` | **NOT a dup** — substring "line" collisions with unrelated linear-algebra/pipeline terms | CREATE; ignore. |
| `hermes_messaging_whatsapp_baileys`, `hermes_messaging_whatsapp_cloud_setup`, `hermes_messaging_whatsapp_cloud_model`, `hermes_messaging_signal`, `hermes_messaging_ntfy` | no term/doc note covers these platform-setup procedures; no `hermes_agent/` doc notes exist yet | NEW | CREATE. |
| owned-term audit (any platform introduce a new reusable concept?) | `term_messaging_gateway`/`term_dm_pairing`/`term_silence_token` (absent — SP11a-owned); product names Baileys/signal-cli/Twilio/ntfy | **No new owned term** — every reusable concept is SP11a-owned (forward-ref +fin) or a low-value product name (link-only) | SP12a owns 0 captures. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
confirmed by reading the note topics). New `hermes_agent/` folder → no doc-doc collisions (intra-series
links resolve at finalization). Adversarial skeptic pass: each "NOT a dup" verdict re-checked against the
note's actual subject (abuse signals vs Hermes platform runbook) — verdicts hold.

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **FOUR-FLOOR standard set 2026-06-19 (user directive — supersedes the 2026-06-14 master floor AND the
> interim 2026-06-19 three-floor wording).** Each note's `## Related Notes` now carries **FOUR counted,
> repos whose modules implement what the doc note documents), ≥10 snippet notes
> documents), and ≥10 documentation notes (`../../documentation/`, sibling `hermes_*` in this series + analogous
> `claude_code/cc_*` agent-tool docs + other relevant existing doc notes)** — each rendered as
> `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`. **The snippet group is NO LONGER a bonus
> group — it is a COUNTED floor, raised from the prior ≥8 to ≥10.** (Floor history: ≥6 → ≥8 term + ≥8 snippet
> + ≥5 doc → interim ≥8 term + ≥5 code-repo + ≥10 doc with snippets demoted to bonus → **now the four-floor
> (terms/snippets/repos and existing `cc_*` docs re-verified 2026-06-19). Intra-series doc links (sibling
> `hermes_*`) resolve at finalization (G5/G8) and are allowed un-verified. SP11a-owned gateway terms
> (`term_messaging_gateway`, `term_dm_pairing`, `term_silence_token`) and SP08-owned media terms
> (`term_text_to_speech`, `term_speech_to_text`, `term_voice_mode`) are ADDITIONAL forward-refs marked `[own]`
> in (+fin …), **EXCLUDED from the ≥8 term floor** (they do not exist yet). Code-repo IDs are the
> `repo_hermes_agent_*` prefix under `areas/code_repos/`; snippet IDs are the `snippet_hermes_agent_` prefix
> under `code_snippets/`.

**Note 1 `hermes_messaging_whatsapp_baileys`**
- Terms (8): term_node_js, term_session_persistence, term_authentication, term_access_control, term_pii, term_multimodal, term_autonomous_coding_agents, term_prompt_injection — relevance: the Baileys bridge runs as a Node.js v18+ subprocess (term_node_js), saves device creds under `~/.hermes/platforms/whatsapp/session` so sessions survive restarts (term_session_persistence), authenticates the WhatsApp-Web session via the QR-scan link (term_authentication), gates inbound on `WHATSAPP_ALLOWED_USERS` deny-by-default (term_access_control), partially redacts phone numbers in logs (term_pii), transcribes incoming `.ogg` voice and reads images (term_multimodal), and because the bot has terminal access by default (term_autonomous_coding_agents) the allowlist is a prompt-injection guard against arbitrary senders driving the agent (term_prompt_injection). (+fin: term_messaging_gateway [own], term_dm_pairing [own], term_speech_to_text [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging, repo_hermes_agent_cli, repo_hermes_agent, repo_hermes_agent_tools, repo_hermes_agent_agent_core — relevance: the Baileys adapter + Node-bridge runner live in the messaging-gateway repo (repo_hermes_agent_gateway_messaging); the `hermes whatsapp` QR-pairing wizard + `hermes gateway` start are CLI subcommands (repo_hermes_agent_cli); the umbrella repo packages the bundled bridge dependency and pull-latest re-pair flow (repo_hermes_agent); the bot's default terminal access — the reason the allowlist exists — is the bash/file toolset (repo_hermes_agent_tools); transcribed voice/text is fed to the AIAgent orchestrator (repo_hermes_agent_agent_core).
- Snippets (11): gw_platform_whatsapp, gw_platform_whatsapp_connect, gw_platform_whatsapp_dispatch, gw_whatsapp_identity, gw_pairing, gw_runner_acl, gw_stream_batching, gw_platform_base_normalize, gw_delivery, gw_platform_base_outbound, gw_session_lifecycle — relevance: the Baileys adapter + its QR/connect + outbound dispatch (gw_platform_whatsapp/_connect/_dispatch), WhatsApp identity-resolution (gw_whatsapp_identity), the DM-pairing handshake (gw_pairing), allowlist ACL (gw_runner_acl), the 5s/10s text-debounce buffer (gw_stream_batching), inbound normalization (gw_platform_base_normalize), 4096-char chunked delivery + WhatsApp-markdown conversion (gw_delivery), the base outbound send path (gw_platform_base_outbound), and the persisted-session-dir lifecycle that survives restarts (gw_session_lifecycle) — all code paths this page drives.
- Docs (11): hermes_messaging_whatsapp_cloud_setup, hermes_messaging_whatsapp_cloud_model, hermes_messaging_signal, hermes_messaging_sms_twilio, hermes_messaging_media_settings, hermes_messaging_gateway_architecture, hermes_security_skill_memory_settings, hermes_stt_transcription, cc_channels_setup, cc_claude_code_in_slack, cc_what_claude_can_access — relevance: the Cloud-API sibling pair is the official-vs-unofficial alternative (cloud_setup/cloud_model); signal/sms are the same linked-device + allowlist setup arc; media_settings owns the shared unauthorized-DM/voice config blocks this page links DOWN to; gateway_architecture is the parent runner/pairing model; security_skill_memory_settings frames the terminal-access guard; stt_transcription owns the voice→text path used here; the `cc_*` analogues are the closest external-agent-docs pattern — per-channel setup (cc_channels_setup), a chat-platform bot integration (cc_claude_code_in_slack), and the terminal-access surface the allowlist protects (cc_what_claude_can_access).

**Note 2 `hermes_messaging_whatsapp_cloud_setup`**
- Terms (9): term_oauth_token, term_authentication, term_access_control, term_reverse_proxy, term_tls, term_replay_attack, term_signature_on_delivery, term_webhook, term_autonomous_coding_agents — relevance: setup hinges on a Meta System-User access token (term_oauth_token) that is the bot's authenticated identity (term_authentication); inbound is an HTTPS webhook POST from Meta (term_webhook) whose payload signature is verified with `WHATSAPP_CLOUD_APP_SECRET` (term_signature_on_delivery) so forged/re-sent requests are rejected (term_replay_attack); a TLS reverse-proxy/tunnel (cloudflared/ngrok/nginx) exposes the local port over HTTPS (term_tls, term_reverse_proxy); dual Meta-side + Hermes-side allowlists gate which numbers reach the bot (term_access_control); and the bot's terminal access motivates the deny-by-default allowlist (term_autonomous_coding_agents). (+fin: term_messaging_gateway [own], term_dm_pairing [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging, repo_hermes_agent_cli, repo_hermes_agent, repo_hermes_agent_tools, repo_hermes_agent_agent_core — relevance: the `whatsapp_cloud` aiohttp webhook server + verify-token handshake + App-Secret signature check live in the messaging-gateway repo (repo_hermes_agent_gateway_messaging); the `hermes whatsapp-cloud` credential-validating wizard + `hermes gateway` start are CLI subcommands (repo_hermes_agent_cli); the umbrella repo ships the pure-Python httpx/aiohttp Cloud adapter (repo_hermes_agent); the terminal toolset the dual allowlist protects is repo_hermes_agent_tools; inbound text/media is routed to the AIAgent orchestrator (repo_hermes_agent_agent_core).
- Snippets (11): gw_platform_webhook, gw_platform_whatsapp, gw_platform_whatsapp_connect, gw_platform_whatsapp_dispatch, gw_whatsapp_identity, gw_runner_acl, gw_slash_access, gw_status_health, gw_platform_base_outbound, gw_delivery, gw_config_load — relevance: the aiohttp webhook server hosting the verify-token GET handshake + App-Secret HMAC signature check (gw_platform_webhook), the Cloud WhatsApp adapter + its connect path + outbound dispatch (gw_platform_whatsapp/_connect/_dispatch), wa_id identity-resolution (gw_whatsapp_identity), the Hermes-side allowlist ACL (gw_runner_acl), slash-command approval gating (gw_slash_access), the `/health` config-presence endpoint the curl probe hits (gw_status_health), the graph.facebook.com outbound send (gw_platform_base_outbound), 4096-char chunked delivery (gw_delivery), and `.env`/`WHATSAPP_CLOUD_*` config loading (gw_config_load) — the code paths the page configures.
- Docs (11): hermes_messaging_whatsapp_cloud_model, hermes_messaging_whatsapp_baileys, hermes_messaging_sms_twilio, hermes_messaging_line, hermes_security_skill_memory_settings, hermes_messaging_gateway_architecture, hermes_webhooks_routes_security, hermes_msgraph_webhook_listener, cc_channels_setup, cc_network_tls_and_access, cc_mcp_authentication — relevance: the Cloud model note is the capability/config half of this same page (cloud_model); the Baileys note is the unofficial alternative; sms_twilio + line are the other webhook-signature platform setups; gateway_architecture is the parent webhook-server/runner model; webhooks_routes_security (SP12b) owns the shared `/whatsapp/webhook` route security this links into; msgraph_webhook_listener (SP12b) is the analogous signed-webhook listener; security_skill_memory_settings frames the terminal guard; the `cc_*` analogues cover per-channel setup (cc_channels_setup), the TLS/public-network exposure the tunnel performs (cc_network_tls_and_access), and the shared-secret auth pattern the App-Secret/verify-token use (cc_mcp_authentication).

**Note 3 `hermes_messaging_whatsapp_cloud_model`** (model)
- Terms (9): term_multimodal, term_computer_vision, term_rate_limiting, term_throttling, term_idempotency, term_authentication, term_human_in_the_loop, term_context_window, term_cron — relevance: the model enumerates inbound multimodal handling — vision images for Claude/GPT-4o/Gemini (term_computer_vision, term_multimodal) and voice-note transcription; Meta's 80-msg/sec outbound rate limit (term_rate_limiting) that Hermes does not yet enforce client-side (term_throttling); idempotent webhook receipt + reply-context dedup (term_idempotency); the token-authenticated graph send (term_authentication); tap-to-answer `clarify`/approval/slash-confirm interactive buttons (term_human_in_the_loop); the conversation context the adapter feeds the agent and the 24h "customer service window" that bounds it (term_context_window); and the constraint that cron jobs delivering after the 24h window fail with graph error `131047` (term_cron). (+fin: term_speech_to_text [own], term_text_to_speech [own], term_messaging_gateway [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging, repo_hermes_agent_cron, repo_hermes_agent_agent_core, repo_hermes_agent, repo_hermes_agent_tools — relevance: the `whatsapp_cloud` adapter's inbound/outbound/interactive-message capability code + 24h-window system-prompt warning live in the messaging-gateway repo (repo_hermes_agent_gateway_messaging); the cron scheduler is the subsystem the 24h-window limitation and `WHATSAPP_CLOUD_HOME_CHANNEL` directly constrain (repo_hermes_agent_cron); vision/voice payloads and reply-context are assembled for the AIAgent orchestrator (repo_hermes_agent_agent_core); the umbrella repo defines the platform→default-toolset mapping (`hermes-whatsapp`) referenced in troubleshooting (repo_hermes_agent); the tool registry is what the interactive approval buttons gate (repo_hermes_agent_tools).
- Snippets (10): gw_platform_whatsapp, gw_platform_whatsapp_dispatch, gw_platform_base_outbound, gw_delivery, gw_runner_outbound, gw_platform_helpers, gw_stream_consumer, gw_runner_cron, gw_channel_directory, gw_status_health — relevance: the Cloud adapter's inbound/outbound/interactive capability code (gw_platform_whatsapp), the dispatch/outbound/delivery code paths that emit text/image/voice/buttons (gw_platform_whatsapp_dispatch, gw_platform_base_outbound, gw_delivery, gw_runner_outbound), the media/markdown helpers (gw_platform_helpers), the SSE stream consumer feeding the agent (gw_stream_consumer), the cron + home-channel delivery the 24h-window limitation (graph `131047`) constrains (gw_runner_cron, gw_channel_directory), and the `/health` ffmpeg_present/config report (gw_status_health).
- Docs (10): hermes_messaging_whatsapp_cloud_setup, hermes_messaging_whatsapp_baileys, hermes_messaging_signal, hermes_messaging_media_settings, hermes_messaging_line, hermes_messaging_gateway_architecture, hermes_stt_transcription, hermes_vision_image_paste, cc_computer_use, cc_channel_reply_tool — relevance: the setup note is the procedural half of this same page (cloud_setup); the Baileys note's feature column is the explicit comparison target; signal/line are the parallel feature/limitation models; media_settings owns the shared voice/display config; gateway_architecture is the parent capability-tier (TIER_MEDIUM) model; stt_transcription + vision_image_paste (SP08) own the voice/vision multimodal paths this matrix enumerates; the `cc_*` analogues cover the vision/computer-use capability surface (cc_computer_use) and the interactive channel-reply UX (cc_channel_reply_tool).

**Note 4 `hermes_messaging_signal`**
- Terms (8): term_json_rpc, term_encryption, term_pii, term_access_control, term_exponential_backoff, term_multimodal, term_session_persistence, term_autonomous_coding_agents — relevance: signal-cli streams over SSE and replies via JSON-RPC (term_json_rpc), E2EE protects content (term_encryption), phone numbers are redacted in logs (term_pii), DM + group allowlist access control (term_access_control), exponential-backoff SSE reconnect (2s→60s) on drop (term_exponential_backoff), multimodal image/audio/document attachment handling (term_multimodal), the `~/.local/share/signal-cli/` linked-device credential session persists across restarts (term_session_persistence), and the agent's default terminal access motivates the allowlist guard (term_autonomous_coding_agents). (+fin: term_dm_pairing [own], term_speech_to_text [own], term_messaging_gateway [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging, repo_hermes_agent_cli, repo_hermes_agent, repo_hermes_agent_tools, repo_hermes_agent_agent_core — relevance: the Signal adapter (SSE consumer + JSON-RPC sender + bodyRanges/reaction/Note-to-Self handling) lives in the messaging-gateway repo (repo_hermes_agent_gateway_messaging); the `hermes gateway setup` Signal wizard (signal-cli probe + allowlist config) + `hermes pairing approve signal` + `hermes gateway` start are CLI subcommands (repo_hermes_agent_cli); the umbrella repo ships the pure-`httpx` adapter with no extra Python deps (repo_hermes_agent); the terminal toolset the allowlist protects is repo_hermes_agent_tools; transcribed/inbound text is routed to the AIAgent orchestrator (repo_hermes_agent_agent_core).
- Snippets (11): gw_platform_signal, gw_platform_signal_sse, gw_platform_signal_media, gw_platform_signal_rate_limit, gw_pairing, gw_runner_acl, gw_runner_session_key, gw_platform_base_normalize, gw_status_health, gw_platform_base_outbound, gw_delivery — relevance: the Signal adapter (gw_platform_signal), the SSE inbound stream + 120s-idle ping health (gw_platform_signal_sse), media/attachment handling (gw_platform_signal_media), the 32-image-batch upload rate-limit scheduler (gw_platform_signal_rate_limit), the DM-pairing handshake (gw_pairing), the DM+group ACL (gw_runner_acl), per-account session-keying (gw_runner_session_key), inbound normalization (gw_platform_base_normalize), the SSE reconnect/health monitor (gw_status_health), the JSON-RPC outbound send (gw_platform_base_outbound), and native-formatting/reply-quote delivery (gw_delivery) the page documents.
- Docs (10): hermes_messaging_whatsapp_baileys, hermes_messaging_sms_twilio, hermes_messaging_email, hermes_messaging_ntfy, hermes_messaging_media_settings, hermes_messaging_gateway_architecture, hermes_security_skill_memory_settings, hermes_stt_transcription, cc_channels_setup, cc_what_claude_can_access — relevance: baileys/sms/email/ntfy are the parallel linked-device-or-allowlist platform setups; media_settings owns the shared attachment/voice config Signal links DOWN to; gateway_architecture is the parent SSE-runner/reconnect model; security_skill_memory_settings frames the terminal-access guard the allowlist defends; stt_transcription owns the voice-note→text path Signal uses; the `cc_*` analogues cover per-channel setup (cc_channels_setup) and the terminal-access surface the allowlist protects (cc_what_claude_can_access).

**Note 5 `hermes_messaging_sms_twilio`**
- Terms (8): term_authentication, term_access_control, term_replay_attack, term_reverse_proxy, term_pii, term_rate_limiting, term_cron, term_autonomous_coding_agents — relevance: the Twilio Account-SID/Auth-Token authenticate the bot (term_authentication) and the Auth-Token doubles as the `X-Twilio-Signature` HMAC-SHA1 webhook-signature key that rejects forged/re-sent POSTs (term_replay_attack); allowlist-deny-by-default access control (term_access_control) behind a cloudflared/ngrok TLS tunnel/reverse-proxy (term_reverse_proxy); phone numbers are redacted in logs (term_pii); 1600-char SMS chunking + Twilio throughput constraints (term_rate_limiting); and `SMS_HOME_CHANNEL` cron delivery (term_cron) for a terminal-capable agent (term_autonomous_coding_agents). (+fin: term_messaging_gateway [own], term_dm_pairing [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging, repo_hermes_agent_cli, repo_hermes_agent, repo_hermes_agent_tools, repo_hermes_agent_cron — relevance: the `sms` adapter's `/webhooks/twilio` aiohttp endpoint + `X-Twilio-Signature` validation + echo-prevention + plain-text chunking live in the messaging-gateway repo (repo_hermes_agent_gateway_messaging); the `hermes gateway setup` SMS wizard + `hermes gateway` start are CLI subcommands (repo_hermes_agent_cli); the umbrella repo declares the `hermes-agent[sms]` aiohttp extra (repo_hermes_agent); the terminal toolset the allowlist protects is repo_hermes_agent_tools; the `SMS_HOME_CHANNEL` cron/notification delivery is the cron scheduler (repo_hermes_agent_cron).
- Snippets (11): gw_platform_sms, gw_platform_webhook, gw_runner_acl, gw_slash_access, gw_runner_cron, gw_delivery, gw_platform_base_outbound, gw_status_health, gw_config_load, gw_channel_directory, gw_platform_base_normalize — relevance: the SMS/Twilio adapter (gw_platform_sms), the aiohttp webhook server hosting `/webhooks/twilio` + `X-Twilio-Signature` validation (gw_platform_webhook), the deny-by-default ACL (gw_runner_acl), slash-command approval gating (gw_slash_access), `SMS_HOME_CHANNEL` cron delivery (gw_runner_cron), 1600-char multi-segment delivery (gw_delivery), the Twilio outbound send (gw_platform_base_outbound), the listener `[sms]` startup/health line + `SMS_WEBHOOK_URL`-required refusal (gw_status_health), `.env` config + `SMS_WEBHOOK_URL` requirement loading (gw_config_load), the home-channel directory (gw_channel_directory), and inbound normalization + echo-prevention (gw_platform_base_normalize) this page configures.
- Docs (10): hermes_messaging_email, hermes_messaging_signal, hermes_messaging_whatsapp_cloud_setup, hermes_messaging_line, hermes_messaging_media_settings, hermes_messaging_gateway_architecture, hermes_webhooks_routes_security, hermes_security_skill_memory_settings, cc_channels_setup, cc_network_tls_and_access — relevance: email/signal are parallel allowlist platform setups; whatsapp_cloud_setup + line are the other webhook-signature platforms; media_settings owns the shared display/home-channel config; gateway_architecture is the parent webhook-server/runner model; webhooks_routes_security (SP12b) owns the shared aiohttp route security; security_skill_memory_settings frames the terminal-access guard; the `cc_*` analogues cover per-channel setup (cc_channels_setup) and the public-tunnel TLS exposure (cc_network_tls_and_access).

**Note 6 `hermes_messaging_email`**
- Terms (8): term_authentication, term_mfa, term_tls, term_access_control, term_pii, term_idempotency, term_multimodal, term_autonomous_coding_agents — relevance: IMAP/SMTP auth with app passwords (term_authentication) generated behind 2FA/MFA (term_mfa) over SSL port 993 / STARTTLS port 587 (term_tls); allowlist access control (term_access_control); a dedicated account isolates PII/inbox exposure (term_pii); the idempotent UNSEEN-poll receive loop with self-message + noreply/bounce/Auto-Submitted filtering avoids reply duplicates (term_idempotency); attachments are cached for the vision/file tools (term_multimodal); and the agent's default terminal access motivates the allowlist guard (term_autonomous_coding_agents). (+fin: term_messaging_gateway [own], term_dm_pairing [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging, repo_hermes_agent_cli, repo_hermes_agent, repo_hermes_agent_tools, repo_hermes_agent_cron — relevance: the Email adapter (stdlib `imaplib`/`smtplib`/`email` UNSEEN-poll receive loop + In-Reply-To/References threaded send + `skip_attachments`) lives in the messaging-gateway repo (repo_hermes_agent_gateway_messaging); the `hermes gateway setup` Email wizard + `hermes gateway`/`hermes gateway status` are CLI subcommands (repo_hermes_agent_cli); the umbrella repo ships the no-external-dependency stdlib adapter (repo_hermes_agent); the terminal toolset the allowlist protects + the vision/file tools attachments feed is repo_hermes_agent_tools; `EMAIL_HOME_ADDRESS` cron delivery is the cron scheduler (repo_hermes_agent_cron).
- Snippets (11): gw_platform_email, gw_runner_acl, gw_pairing, gw_slash_access, gw_runner_cron, gw_delivery, gw_platform_base_normalize, gw_platform_base_outbound, gw_config_load, gw_channel_directory, gw_status_health — relevance: the Email IMAP/SMTP adapter (gw_platform_email), the deny-by-default ACL (gw_runner_acl), the unknown-sender pairing code (gw_pairing), slash-command approval gating (gw_slash_access), `EMAIL_HOME_ADDRESS` cron delivery (gw_runner_cron), plain-text SMTP reply delivery (gw_delivery), inbound normalization + HTML-strip + self/noreply filtering (gw_platform_base_normalize), the threaded outbound send with In-Reply-To/References (gw_platform_base_outbound), `.env` host/port/poll-interval config loading (gw_config_load), the home-address directory (gw_channel_directory), and the startup IMAP/SMTP connection test + mark-seen health (gw_status_health) the page documents.
- Docs (10): hermes_messaging_sms_twilio, hermes_messaging_signal, hermes_messaging_ntfy, hermes_messaging_whatsapp_baileys, hermes_security_skill_memory_settings, hermes_messaging_gateway_architecture, hermes_messaging_media_settings, hermes_stt_transcription, cc_channels_setup, cc_what_claude_can_access — relevance: sms/signal/ntfy/baileys are parallel allowlist platform setups; security_skill_memory_settings frames the dedicated-account + terminal-access guard; gateway_architecture is the parent poll-loop/runner model; media_settings owns the shared attachment/`skip_attachments` config; stt_transcription owns the multimodal-attachment-to-tool path; the `cc_*` analogues cover per-channel setup (cc_channels_setup) and the inbox/terminal-access surface the allowlist protects (cc_what_claude_can_access).

**Note 7 `hermes_messaging_line`**
- Terms (8): term_authentication, term_access_control, term_replay_attack, term_reverse_proxy, term_session_persistence, term_multimodal, term_human_in_the_loop, term_autonomous_coding_agents — relevance: the channel access token authenticates Push/Reply sends (term_authentication) and the channel secret drives HMAC-SHA256 webhook-signature verification that rejects forged/re-sent events (term_replay_attack); U/C/R-prefixed allowlist access control (term_access_control) behind a cloudflared/ngrok/devtunnel TLS reverse-proxy (term_reverse_proxy); the `PENDING→READY→DELIVERED` reply-token state machine persists the pending run across the postback round-trip (term_session_persistence); image/audio/video/sticker handling + `LINE_PUBLIC_URL` media sends (term_multimodal); the postback "Get answer" button is the slow-LLM human-in-the-loop affordance (term_human_in_the_loop); and the agent's terminal access motivates the allowlist guard (term_autonomous_coding_agents). (+fin: term_messaging_gateway [own], term_silence_token [own], term_dm_pairing [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging, repo_hermes_agent_plugins, repo_hermes_agent_cli, repo_hermes_agent_cron, repo_hermes_agent_tools — relevance: the LINE adapter's `/line/webhook` aiohttp listener + HMAC-SHA256 verify + reply-token state machine + Push fallback live in the messaging-gateway repo (repo_hermes_agent_gateway_messaging); the adapter ships as a bundled platform plugin under `plugins/platforms/line/` auto-discovered by the plugin scan — no core edit (repo_hermes_agent_plugins); the `hermes gateway setup` LINE wizard + `hermes gateway` start are CLI subcommands (repo_hermes_agent_cli); `LINE_HOME_CHANNEL` cron Push-only delivery is the cron scheduler with its standalone sender (repo_hermes_agent_cron); the terminal toolset the allowlist protects is repo_hermes_agent_tools.
- Snippets (11): gw_platform_registry, gw_platform_base_abstract, gw_platform_webhook, gw_runner_acl, gw_delivery, gw_runner_outbound, gw_runner_cron, gw_config_per_channel, gw_config_load, gw_platform_base_outbound, gw_status_health — relevance: the bundled-plugin registry that auto-discovers `plugins/platforms/line/` (gw_platform_registry), the abstract base the LINE adapter subclasses (gw_platform_base_abstract), the `/line/webhook` aiohttp server (gw_platform_webhook), the U/C/R ACL (gw_runner_acl), 5000/4500-char bubble chunking delivery (gw_delivery), the reply-token-first / Push-fallback outbound path (gw_runner_outbound), `LINE_HOME_CHANNEL` Push-only cron delivery (gw_runner_cron), per-channel config + `display.platforms.line.tool_progress` suppression (gw_config_per_channel), `.env`/`config.yaml` plugin-enable loading (gw_config_load), the Push/Reply API send (gw_platform_base_outbound), and the `/line/webhook/health` + LINE-verify status (gw_status_health) the page wires.
- Docs (10): hermes_messaging_whatsapp_cloud_setup, hermes_messaging_signal, hermes_messaging_sms_twilio, hermes_messaging_media_settings, hermes_messaging_ntfy, hermes_messaging_gateway_architecture, hermes_webhooks_routes_security, hermes_security_skill_memory_settings, cc_channels_setup, cc_network_tls_and_access — relevance: whatsapp_cloud_setup + sms are the other webhook-signature platforms; signal/ntfy are parallel allowlist setups; media_settings owns the shared display/tool-progress-suppression config this page edits; gateway_architecture is the parent webhook-server/runner model; webhooks_routes_security (SP12b) owns the shared aiohttp route security; security_skill_memory_settings frames the terminal-access guard; the `cc_*` analogues cover per-channel setup (cc_channels_setup) and the public-tunnel TLS exposure (cc_network_tls_and_access).

**Note 8 `hermes_messaging_ntfy`**
- Terms (8): term_pub_sub, term_message_queue, term_access_control, term_authentication, term_replay_attack, term_exponential_backoff, term_cron, term_autonomous_coding_agents — relevance: ntfy is an HTTP pub-sub topic channel (term_pub_sub) with message-queue-like topic delivery (term_message_queue); the topic-IS-the-identity model gates access via a single-entry `NTFY_ALLOWED_USERS` topic allowlist (term_access_control); `NTFY_TOKEN` bearer/basic auth on private/reserved topics (term_authentication); the publisher-controlled `title` field is a forged-sender/spoofing vector the adapter refuses to trust for authorization (term_replay_attack); exponential-backoff stream reconnect 2→5→10→30→60s (term_exponential_backoff); `NTFY_HOME_CHANNEL` cron delivery (term_cron) for a terminal-capable agent (term_autonomous_coding_agents). (+fin: term_messaging_gateway [own], term_dm_pairing [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging, repo_hermes_agent_plugins, repo_hermes_agent_cli, repo_hermes_agent_cron, repo_hermes_agent — relevance: the ntfy adapter's `httpx` SSE subscribe-stream + topic-as-identity authorization + 401/404-fatal reconnect-halt live in the messaging-gateway repo (repo_hermes_agent_gateway_messaging); the adapter ships as a bundled plugin that registers a `standalone_sender_fn` (repo_hermes_agent_plugins); the `hermes gateway setup` ntfy wizard + `hermes gateway restart` are CLI subcommands (repo_hermes_agent_cli); `NTFY_HOME_CHANNEL` cron delivery via the out-of-process standalone sender is the cron scheduler (repo_hermes_agent_cron); the umbrella repo ships the no-daemon/no-SDK `httpx`-only adapter (repo_hermes_agent).
- Snippets (11): gw_platform_registry, gw_platform_base_abstract, gw_platform_base_outbound, gw_runner_acl, gw_runner_cron, gw_delivery, gw_stream_consumer, gw_status_health, gw_config_load, gw_channel_directory, gw_run_helpers — relevance: the bundled-plugin registry (gw_platform_registry), the abstract base the ntfy adapter subclasses (gw_platform_base_abstract), the topic-publish outbound sender (gw_platform_base_outbound), the topic-allowlist ACL (gw_runner_acl), `NTFY_HOME_CHANNEL` cron delivery (gw_runner_cron), 4096-char-capped + `X-Markdown` delivery (gw_delivery), the SSE subscribe-stream consumer (gw_stream_consumer), `fatal: ntfy_unauthorized`/`ntfy_topic_not_found` runtime-status reporting (gw_status_health), `.env` topic/server/token config loading (gw_config_load), the home-channel/topic directory (gw_channel_directory), and the out-of-process `standalone_sender_fn` opening its own HTTP connection (gw_run_helpers) the page documents.
- Docs (10): hermes_messaging_email, hermes_messaging_sms_twilio, hermes_messaging_signal, hermes_messaging_line, hermes_messaging_media_settings, hermes_messaging_gateway_architecture, hermes_security_skill_memory_settings, hermes_messaging_whatsapp_cloud_model, cc_channels_setup, cc_what_claude_can_access — relevance: email/sms/signal/line are parallel allowlist platform setups; media_settings owns the shared markdown/display config; gateway_architecture is the parent stream-consumer/runner + standalone-sender model; security_skill_memory_settings frames the topic-as-shared-secret + terminal-access guard; whatsapp_cloud_model is the parallel cron/home-channel-delivery model; the `cc_*` analogues cover per-channel setup (cc_channels_setup) and the terminal-access surface the topic allowlist protects (cc_what_claude_can_access).

All 8 notes meet the FOUR-FLOOR standard: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc (the `[own]`-marked
SP08/SP11a forward-refs are ADDITIONAL, excluded from the ≥8 term floor). Per-note counts: terms 8–9, code-repos
5, snippets 10–11, docs 10–11. Code-repo IDs are under `areas/code_repos/` with the `repo_hermes_agent_*` prefix;
snippet IDs are under `resources/code_snippets/` with the `snippet_hermes_agent_` prefix (the `gw` gateway bucket
`hermes_*` sibling doc links resolve in `resources/documentation/hermes_agent/` (intra-series links land at
finalization, verified by G5/G8). All term + code-repo + snippet + existing-doc IDs above are final clean

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 7 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages table
(no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 whatsapp-baileys | procedure | 1500 | ≤6 (curate from 8 source blocks: env, config.yaml, gateway start, debounce, prefix) | ✓ |
| 2 whatsapp-cloud-setup | procedure | 1600 | ≤6 (curate: wizard cmd, tunnel install/run, verify-token gen, curl probe, allowlist) | ✓ |
| 3 whatsapp-cloud-model | model | 1400 | ≤6 (config-var table in prose; keep `curl /health`, ffmpeg-install, comparison rendered as table) | ✓ |
| 4 signal | procedure | 1500 | ≤6 (curate from 7 source blocks: install, link, daemon, check, .env, gateway) | ✓ |
| 5 sms-twilio | procedure | 900 | ≤6 (curate from 10 short blocks: .env, webhook, tunnel, start, port override) | ✓ |
| 6 email | procedure | 1100 | 4 | ✓ |
| 7 line | procedure | 1300 | ≤6 (curate from 8 blocks: tunnel, .env, config.yaml enable, webhook log, suppression yaml) | ✓ |
| 8 ntfy | procedure | 1000 | ≤6 (curate from 9 blocks: env vars, cron python, self-host, markdown) | ✓ |

No further splits needed beyond the planned whatsapp-cloud→2. All 8 notes ≤1600w. Code-heavy pages
(sms 10, ntfy 9, signal 7, line 8) are curated to ≤6 load-bearing blocks (verbatim for kept blocks), with
the rest (long env-var reference tables, repeated `.env` fragments) summarized in prose/table. Borderline
check: no note exceeds ~1600w or 6 curated code blocks; each is a topically-cohesive single BB → KEEP (review
CP6 default-to-keep justification). If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and siblings): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP12a)

**SP12a owns 0 new term captures.** Per the master's corpus-wide ownership sweep, every Hermes-specific
concept SP12a touches is owned by another sub-plan (link at finalization) or is an existing verified term.
Augment re-read of all 7 pages surfaced **0 new** undigested terms that SP12a should own — every reusable
concept is the messaging-gateway/DM-pairing/silence-token cluster owned by SP11a, or a media subsystem
owned by SP08; the rest are low-value product names treated as in-note link-only references.

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_messaging_gateway`, `term_dm_pairing`, `term_silence_token` | LINK only (forward-ref, +fin, marked [own]) | SP11a | Platform↔agent bridge concept + user-authorization handshake + `[SILENT]` non-reply; SP12a *uses* them in every note, SP11a *owns* them. Confirmed absent in DB 2026-06-15. |
| `term_text_to_speech`, `term_speech_to_text`, `term_voice_mode` | LINK only (+fin, marked [own]) | SP08 | Incoming voice transcription / outbound TTS appear in whatsapp/signal notes; concept homes are SP08 media. Confirmed absent in DB 2026-06-15. |
| product names: Baileys, signal-cli, Twilio, cloudflared/ngrok, ntfy, himalaya CLI | NOT captured (link-only references in-note) | — | Low-value product names per master rule; no recurring conceptual use justifying a standalone term. |

### Renamed (general → specific)

— (audit performed; SP12a owns 0 new term captures, so no slugs to rename. The specificity heuristic was
applied to the master's forward-ref slugs SP12a links; all are already scope-qualified by their owners
— `term_messaging_gateway` (≠ `term_api_gateway`), `term_dm_pairing`, `term_silence_token`.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_whatsapp` / `term_signal` / `term_twilio_sms` / platform-setup concept | none substantive (no Hermes platform-setup term/doc note exists; `term_sms` is an abuse SMS-pumping concept, unrelated) | No removal — SP12a was never going to capture these; doc notes `hermes_messaging_*` created instead. |
| `term_messaging_gateway` (would duplicate SP11a) | SP11a-owned (absent in DB; captured by SP11a) | Not captured here — linked as +fin forward-ref from every SP12a note. |

## Term-Note Authoring Requirements

N/A (inherited) — SP12a owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans (SP08/SP11a). The full Term-Note Authoring
fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12, backlink expansion,
>200-line decomposition) apply to those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (WhatsApp family, P2 pilot):** Notes 1, 2, 3. Pilot Note 1 (`hermes_messaging_whatsapp_baileys`)
  first → reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (Signal + SMS + Email):** Notes 4, 5, 6. GATE G1–G8.
- **Phase 3 (LINE + ntfy):** Notes 7, 8. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/user-guide/messaging/<page>`
(code verbatim for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4,
DB-verify every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** ·
G7 single-BB · **G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_messaging_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder
for n in hermes_messaging_whatsapp_baileys hermes_messaging_whatsapp_cloud_setup hermes_messaging_whatsapp_cloud_model hermes_messaging_signal hermes_messaging_sms_twilio hermes_messaging_email hermes_messaging_line hermes_messaging_ntfy; do
```

## Entry Point Decision (inherited)

Contributes 8 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Messaging: Consumer Messengers" section (shared with SP12b). Parent hub back-link
in `entry_research_and_ai_hub.md` is handled at master level. SP12a does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_gateway_messaging.md` | → all 8 notes | messaging-gateway repo ↔ per-platform setup docs |
| `entry_code_snippets_hermes_agent.md` | → `hermes_messaging_whatsapp_baileys`, `hermes_messaging_signal` | code layer ↔ docs layer |
| `snippet_hermes_agent_gw_platform_whatsapp.md` | → `hermes_messaging_whatsapp_baileys`, `hermes_messaging_whatsapp_cloud_setup` | WhatsApp adapter code ↔ WhatsApp setup docs |
| `snippet_hermes_agent_gw_platform_signal.md` | → `hermes_messaging_signal` | Signal adapter code ↔ Signal setup doc |
| `snippet_hermes_agent_gw_platform_sms.md` | → `hermes_messaging_sms_twilio` | SMS adapter code ↔ SMS setup doc |
| `snippet_hermes_agent_gw_platform_email.md` | → `hermes_messaging_email` | Email adapter code ↔ Email setup doc |
| `snippet_hermes_agent_gw_platform_webhook.md` | → `hermes_messaging_whatsapp_cloud_setup`, `hermes_messaging_sms_twilio`, `hermes_messaging_line` | shared webhook server ↔ webhook-based platform docs |
| `snippet_hermes_agent_gw_pairing.md` | → `hermes_messaging_whatsapp_baileys`, `hermes_messaging_signal` | DM-pairing code ↔ platforms using pairing |
| `repo_hermes_agent.md` | → `hermes_messaging_ntfy`, `hermes_messaging_line` | implementation ↔ bundled-plugin platform docs |
| `entry_hermes_agent_docs.md` (new, master) | → all 8 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_messaging_whatsapp_baileys`) → reindex → verify format/ghost/in-degree BEFORE
authoring the rest. Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before
writing each note — do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes
to ≤6 load-bearing blocks, summarize the rest (long env-var reference tables) in prose/table. If a note
exceeds 350 lines during writing, STOP and split. If multi-agent: agents return note content, master writes
serially where there is write-contention; ≤30 agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP12a lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 8 rows to
  the master-created entry point; backfill the `repo_hermes_agent_gateway_messaging` / `snippet_*` inlinks
  (G8); run `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After SP11a lands: backfill the `term_messaging_gateway` / `term_dm_pairing` / `term_silence_token`
  forward-refs (+fin) into all 8 notes; after SP08 lands, backfill `term_text_to_speech` /
  `term_speech_to_text` / `term_voice_mode`.
- Coordinate with SP12b (webhooks/open-webui/simplex/bluebubbles/photon/homeassistant/msgraph-webhook) so the
  shared "Messaging: Consumer" entry-point section is built once; cross-link the two whatsapp notes to SP12b's
  `webhooks`/`msgraph-webhook` notes (shared webhook server).

## Augmentation Report

- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  the snippet group was promoted from "bonus" back to a COUNTED floor and raised from ≥8 to ≥10. All 7 owned
  source pages re-read 2026-06-19 to ground the new snippet/repo relevance clauses; all term + code-repo +
  snippet IDs and existing `cc_*` doc IDs re-verified active against the DB.
  false-positives confirmed by reading the note topics), finalized Per-Note Mapping (FOUR-FLOOR ≥8 term + ≥5
  Density Re-Assessment (re-read confirmed), G5 ghost + G8 scripts, Inlinks.
- Density re-read: counts match measured; **one split** (whatsapp-cloud→2, procedure + model) — the only
  >2500w page; all other 6 pages ≤1700w single-BB. All 8 notes ≤1600w; code-heavy pages curated to ≤6 blocks.
- Collision audit: **0 removals** — `term_sms`/`term_sms_pumping`/`term_email_domain_risk`/`term_linear_*`
  an existing term/doc note. SP12a owns 0 captures.
  before lock-in; the `[own]` SP08/SP11a forward-refs are explicitly excluded from the ≥8 floor.
- Undigested terms surfaced at augment: **0 new** (SP12a owns 0 captures; all concepts owned by SP08/SP11a).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs
Phase GATEs incl G5/G6/G8 ✓ Note Format Def (derived) ✓
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (N/A — 0 owned) ✓ best-fit glossary (N/A) ✓ Term-Note Auth Reqs (N/A-inherited) ✓ invokes
capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (N/A — 0 owned;
ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks EXECUTED ✓
Doc-Note Authoring Spec derived ✓). Term-capture items are N/A-pass (SP12a owns 0 captures); dedup/collision
items are substantively PASS (audit performed on all 8 doc notes).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass). Re-reviewed 2026-06-19 against the
FOUR-FLOOR standard — STILL READY (9/9). Independent four-floor audit: all 8 notes meet ≥8 term + ≥5
code-repo + ≥10 snippet + ≥10 doc (declared==actual, every link relevance-claused, no intra-group dups);
anti-fabrication DB spot-check verified 72 cited IDs active (7 repos + 27 distinct terms + 31 distinct
snippets + 7 cc_* docs, 0 missing); the 6 `[own]` forward-ref terms confirmed ABSENT (correctly floor-
excluded); CP7 source counts re-measured exact (whatsapp-cloud 3439/9, whatsapp 1700/8, signal 1504/7,
line 1258/8, email 1173/4, ntfy 1046/9, sms 896/10 — code 9 for whatsapp-cloud/ntfy confirmed via
indented-fence pairs). No factual fixes required.**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (8 rows under a Consumer-Messengers section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 8 notes ≤30; master holds the corpus-level split (SP12 split a/b). |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`); not invented. |
| CP6 | Borderline density → split | PASS | whatsapp-cloud→2 (procedure+model, >2500w + BB split); all notes ≤1600w; code-heavy pages curated ≤6; single-BB cohesive clusters, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15: whatsapp-cloud 3439 (only >2500w page), whatsapp 1700, signal 1504, line 1258, email 1173, ntfy 1046, sms 896 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP12a owns 0 term captures (gateway concepts SP11a-owned, media SP08-owned); Undigested Terms Plan + Authoring Reqs sections present; multi-source mandate inherited by owners. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 8 notes from repo_*/snippet_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.**

## Re-Sync Note (2026-06-19)

The local doc mirror `inbox/hermes_agent_docs/` was re-synced from upstream `NousResearch/hermes-agent`
`website/docs/` — pin moved from `95715dc` to `c253b07` (now byte-identical to upstream main HEAD). All 7
of SP12a's owned pages were independently re-measured with the ledger convention (body words = words after
stripping the YAML frontmatter; code-block count = fence-line count ÷ 2) and the word/code counts are **UNCHANGED**:

- `user-guide/messaging/whatsapp-cloud.md` — 3439w / 9code (unchanged)
- `user-guide/messaging/whatsapp.md` — 1700w / 8code (unchanged)
- `user-guide/messaging/signal.md` — 1504w / 7code (unchanged)
- `user-guide/messaging/line.md` — 1258w / 8code (unchanged)
- `user-guide/messaging/email.md` — 1173w / 4code (unchanged)
- `user-guide/messaging/ntfy.md` — 1046w / 9code (unchanged)
- `user-guide/messaging/sms.md` — 896w / 10code (unchanged)

No planned-note, split (whatsapp-cloud→2), density, or cross-ref (FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10
snippet + ≥10 doc) decision is affected by the re-sync — every count is exact against the fresh mirror. Plan
remains **READY**.

## Pipeline Status (Per-Sub-Plan)


**Source**: `inbox/hermes_agent_docs/user-guide/messaging/{whatsapp,whatsapp-cloud,signal,sms,email,line,ntfy}.md`
**Last Updated**: 2026-06-15 (re-verified 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
