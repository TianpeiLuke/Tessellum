---
title: Sub-Plan pf04 — OpenClaw Docs: Platforms (mac voicewake / webchat / xpc, macOS app, Windows)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["platforms/mac/voicewake", "platforms/mac/webchat", "platforms/mac/xpc", "platforms/macos", "platforms/windows"]
---

# Sub-Plan pf04: Platforms

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), YAML/body format, dedup-before-create (term_dictionary +
> documentation/ + `repo_openclaw*`), the 9-GATE table, cross-reference floors, and the `entry_openclaw_docs.md`
> entry-point/W1–W5 wiring are ALL inherited from the master — not re-derived here.

## Scope

The five Platforms pages covering the **macOS** and **Windows** host integrations: the macOS Voice Wake /
push-to-talk pathway (`mac/voicewake`), the macOS embedded WebChat view (`mac/webchat`), the macOS IPC
architecture / PeekabooBridge (`mac/xpc`), the macOS menu-bar companion app (`macos`), and Windows support —
Windows Hub, native CLI/Gateway, WSL2 Gateway, node mode, local MCP mode, and troubleshooting (`windows`).
These document how OpenClaw exposes desktop-OS capabilities (canvas/screen/camera/mic/speech/`system.run`) to
the agent as a **node**, manage the local **Gateway** lifecycle (launchd / Scheduled Tasks / WSL), and harden
the local IPC surface. **Priority P2 (Phase B)** — features/integration layer that references the Phase-A
gateway/node/concepts vocabulary; the code-side counterparts (`repo_openclaw_apps`, `repo_openclaw_gateway`,
`repo_openclaw_security`, voice/IPC snippets) are LINKED, never recreated.

**Source**: OpenClaw docs, 5 pages, 3,930 measured words. **Planned: 6 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Voice Wake & Push-to-Talk (mac) | /platforms/mac/voicewake | 624 | 0 | 11 | 0 | concept |
| WebChat (mac) | /platforms/mac/webchat | 264 | 1 | 5 | 0 | concept |
| macOS IPC (mac/xpc) | /platforms/mac/xpc | 404 | 1 | 6 | 3 | model (IPC architecture) |
| macOS app | /platforms/macos | 1,208 | 7 | 12 | 2 | procedure |
| Windows | /platforms/windows | 1,430 | 17 | 9 | 7 | procedure (split: install vs node/MCP/troubleshoot) |

Totals: 3,930 words · 26 code blocks · 43 H2 · 12 H3.

## Content Strategy

- **Prioritize**: the macOS app page (the menu-bar companion that owns TCC permissions, Gateway launchd
  lifecycle, node capabilities, Exec-approvals for `system.run`, deep links, and remote SSH-tunnel plumbing)
  and Windows install (the three install paths — Hub / native CLI / WSL2 — plus auto-start). These are the
  operational entry points users hit first.
- **Split**: only `windows.md` (1,430w, **17 code fences** > the 6-block cap, mixed BB) → an install/setup
  procedure note + a node-mode/MCP/troubleshooting note, so each stays ≤6 code blocks and one BB.
- **Keep as 1 note** (most reference pages = 1 note): voicewake, webchat, xpc, macos — each ≤2,500w and
  single-BB-coherent. `macos.md` (1,208w, 7 fences) trims to ≤6 representative fences (launchctl, exec-approvals
  JSON, deep-link `open`, state-dir env, debug-CLI, SSH shape) without losing coverage.
- **Link-out, do not redefine**: TCC/permissions detail → `mac/permissions` (pf03); Canvas → `mac/canvas`
  (pf01); PeekabooBridge → `mac/peekaboo` (pf03); remote access → `mac/remote` (pf03); bundled Gateway →
  `mac/bundled-gateway` (pf01); voice-overlay → `mac/voice-overlay` (pf03); node `voicewake` →
  `nodes/voicewake` (nd02); Gateway protocol/troubleshooting/config → gw0x; exec-approvals tool semantics →
  `tools/exec-approvals-advanced` (to03); install overview/Node setup → in0x. These are sibling-series links,
  not duplicated content.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_platforms_mac_voicewake.md` | concept | mac/voicewake.md: Requirements, Modes, Runtime behavior (wake-word), Lifecycle invariants, Sticky overlay failure mode, Push-to-talk specifics, User-facing settings, Forwarding behavior, Forwarding payload, Quick verification | 520 | macOS Voice Wake and push-to-talk: macOS-26 requirement, wake-word vs Right-Option PTT modes, the `VoiceWakeRuntime` recognizer behavior (trigger pause, silence windows, hard-stop, debounce), overlay lifecycle invariants, settings, and how transcripts forward to the active gateway/agent and replies route to the last-used main provider. |
| 2 | `oc_platforms_mac_webchat.md` | concept | mac/webchat.md: (intro), Launch and debugging, How it is wired, Security surface, Known limitations | 320 | The macOS app's embedded native-SwiftUI WebChat view: local vs remote (SSH-tunneled) connection modes, the Gateway WS data plane (`chat.*` methods + `chat`/`agent`/`presence`/`tick`/`health` events), display-normalized `chat.history` (directive/tool-call XML/control-token stripping), session defaulting/switching, and launch/debug entry points. |
| 3 | `oc_platforms_mac_xpc.md` | model | mac/xpc.md: (intro), Goals, How it works (Gateway+node transport, Node service + app IPC, PeekabooBridge), Operational flows, Hardening notes | 480 | macOS IPC architecture: the single TCC-owning GUI app, agent actions via `node.invoke` over the Gateway WS, `system.run` forwarded from the headless node host service to the app over a local Unix domain socket (token + HMAC challenge/response + peer-UID + 0600 + TTL), and PeekabooBridge (`bridge.sock`, TeamID-gated) for UI automation. |
| 4 | `oc_platforms_macos.md` | procedure | macos.md: (intro), What it does, Local vs remote mode, Launchd control, Node capabilities (mac), Exec approvals (system.run), Deep links (`openclaw://agent`), Onboarding flow, State dir placement, Build and dev workflow, Debug gateway connectivity, Remote connection plumbing (SSH tunnels) | 760 | The macOS menu-bar companion app: TCC ownership, local-vs-remote Gateway management via the `ai.openclaw.gateway` LaunchAgent, node capabilities (canvas/camera/screen/system), Exec-approvals policy for `system.run` (`exec-approvals.json`, allowlist globs, shell-control + env-var filtering), the `openclaw://agent` deep-link scheme, state-dir placement, native build/dev workflow, `openclaw-mac` debug CLI, and the Remote-mode SSH control tunnel. |
| 5 | `oc_platforms_windows_install.md` | procedure | windows.md: (intro), Recommended: Windows Hub (What Windows Hub includes, First launch), Native Windows CLI and Gateway, WSL2 Gateway, Gateway auto-start before Windows login, Expose WSL services over LAN | 700 | Installing OpenClaw on Windows: choosing among Windows Hub (signed WinUI app, app-owned WSL Gateway, first-run setup), native PowerShell CLI/Gateway install (`install.ps1`, `gateway install/run`, Scheduled-Tasks startup), and a manual WSL2 Gateway (systemd, headless auto-start with `dbus-launch`, linger), plus exposing WSL services over the LAN via `netsh portproxy`. |
| 6 | `oc_platforms_windows_node_modes.md` | procedure | windows.md: Windows node mode, Local MCP mode (mode matrix), Troubleshooting (tray icon, local setup, pairing, web chat reach, screen/camera/audio, Git/GitHub), Related | 560 | Windows Hub as a node and local MCP server: declaring Windows-native capabilities (canvas/screen/camera/system/location/device/stt/tts) over the Gateway with pairing + `gateway.nodes.allowCommands` opt-in for privacy-sensitive commands, the off/on node × MCP mode matrix, the loopback MCP-server endpoint, and the Windows troubleshooting runbook. |

## Section Coverage Map

```
platforms/mac/voicewake.md
├── (frontmatter summary/read_when) ──────────────── (metadata, not a note)
├── Requirements ─────────────────────────────────── → note 1 (oc_platforms_mac_voicewake)
├── Modes (wake-word / push-to-talk) ─────────────── → note 1
├── Runtime behavior (wake-word) ─────────────────── → note 1
├── Lifecycle invariants ─────────────────────────── → note 1
├── Sticky overlay failure mode (previous) ───────── → note 1
├── Push-to-talk specifics ───────────────────────── → note 1
├── User-facing settings ─────────────────────────── → note 1
├── Forwarding behavior ──────────────────────────── → note 1
├── Forwarding payload ───────────────────────────── → note 1
├── Quick verification ───────────────────────────── → note 1
└── Related (links) ──────────────────────────────── → note 1 References/Related (link-out: nodes/voicewake, mac/voice-overlay, macos)
platforms/mac/webchat.md
├── (intro: embeds WebChat as SwiftUI, local/remote) → note 2 (oc_platforms_mac_webchat) Overview
├── Launch and debugging ─────────────────────────── → note 2
├── How it is wired (chat.* methods + events) ────── → note 2
├── Security surface ─────────────────────────────── → note 2
├── Known limitations ────────────────────────────── → note 2
└── Related (links) ──────────────────────────────── → note 2 (link-out: web/webchat, macos)
platforms/mac/xpc.md
├── (intro: current model) ───────────────────────── → note 3 (oc_platforms_mac_xpc) Overview
├── Goals ────────────────────────────────────────── → note 3
├── How it works
│   ├── Gateway + node transport ─────────────────── → note 3
│   ├── Node service + app IPC (+ SCI diagram) ───── → note 3
│   └── PeekabooBridge (UI automation) ───────────── → note 3 (link-out: mac/peekaboo)
├── Operational flows ────────────────────────────── → note 3
├── Hardening notes ──────────────────────────────── → note 3
└── Related (links) ──────────────────────────────── → note 3 (link-out: macos, tools/exec-approvals-advanced)
platforms/macos.md
├── (intro: menu-bar companion) ──────────────────── → note 4 (oc_platforms_macos) Overview
├── What it does ─────────────────────────────────── → note 4
├── Local vs remote mode ─────────────────────────── → note 4
├── Launchd control (launchctl) ──────────────────── → note 4
├── Node capabilities (mac) (+ SCI diagram) ──────── → note 4
├── Exec approvals (system.run) (exec-approvals.json) → note 4
├── Deep links → openclaw://agent ────────────────── → note 4
├── Onboarding flow (typical) ────────────────────── → note 4
├── State dir placement (macOS) ──────────────────── → note 4
├── Build and dev workflow (native) ──────────────── → note 4
├── Debug gateway connectivity (macOS CLI) ───────── → note 4
├── Remote connection plumbing → Control tunnel ──── → note 4
└── Related docs (links) ─────────────────────────── → note 4 (link-out: gateway, mac/bundled-gateway, mac/permissions, mac/canvas, mac/remote, gateway/protocol)
platforms/windows.md
├── (intro: Hub / native CLI / WSL2 paths) ───────── → note 5 (oc_platforms_windows_install) Overview
├── Recommended: Windows Hub
│   ├── What Windows Hub includes ────────────────── → note 5
│   └── First launch ─────────────────────────────── → note 5
├── Native Windows CLI and Gateway ───────────────── → note 5
├── WSL2 Gateway ─────────────────────────────────── → note 5
├── Gateway auto-start before Windows login ──────── → note 5
├── Expose WSL services over LAN ─────────────────── → note 5
├── Windows node mode ────────────────────────────── → note 6 (oc_platforms_windows_node_modes)
├── Local MCP mode (mode matrix) ─────────────────── → note 6
├── Troubleshooting
│   ├── The tray icon does not appear ────────────── → note 6
│   ├── Local setup fails ────────────────────────── → note 6
│   ├── The app says pairing is required ─────────── → note 6
│   ├── Web chat cannot reach a remote Gateway ───── → note 6
│   ├── screen.snapshot/camera/audio commands fail ─ → note 6
│   └── Git or GitHub connectivity fails ─────────── → note 6
└── Related (links) ──────────────────────────────── → note 6 (link-out: install, install/node, nodes, web/control-ui, gateway/configuration)
```
No orphaned sections. Every H2/H3 maps to exactly one planned note; `## Related`/`## Related docs` link lists
become each note's `## References`/cross-references (link-out to sibling series, not duplicated bodies).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| windows.md (1,430w, 9 H2 / 7 H3, **17 code fences**, mixed BB) | notes 5 + 6 | The page mixes an install/setup procedure (Hub install, native CLI, WSL2 Gateway, auto-start, LAN port-proxy) with a node/MCP capability + troubleshooting cluster. Single note would carry 17 code fences (>6 cap). Split keeps each ≤6 code blocks, ≤~700w, and one coherent BB (both procedure; install vs operate/troubleshoot). |

All four other pages remain 1 note each (each ≤2,500w, single-BB-coherent; voicewake 0 fences, webchat 1,
xpc 1, macos 7→trimmed to ≤6 representative fences).

## Summary Statistics & Building Block Distribution

- Source pages: **5** (3,930 measured words, 26 code fences). New `oc_*` notes: **6**. New `term_dictionary`
  notes: **0** (see Undigested Terms Plan).
- BB distribution: **concept ×2** (notes 1, 2) · **model ×1** (note 3, IPC architecture) · **procedure ×3**
  (notes 4, 5, 6).
- Est. digest words ~3,340 (avg ~557/note). The 26 source fences distribute across the procedure/model notes;
  each note kept **≤6 code blocks** (windows split so neither node carries >6; macos trims 7→≤6 representative
  fences; voicewake has none, webchat/xpc 1 each).
- Cross-refs (LOCKED at xref-augment 2026-06-21 at RAISED FLOORS): each note maps **≥8 relevance-selected
  planned sibling `oc_*` this series)** PLUS relevant `repo_openclaw*`/entry points, each with a per-link
  See **## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)**.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

note_id) at this augment; sibling `oc_*` docs are this series (created by their own waves) and marked
claude_code/hermes_agent/pi/band coding-agent corpora toward the 10-doc floor. Relative paths are FROM a
note at `resources/documentation/openclaw/oc_X.md` (term → `../../term_dictionary/`; sibling oc_ → bare
`oc_Y.md`; other docs → `../<folder>/`; repo → `../../../areas/code_repos/`; snippet →
`../../code_snippets/`; entry → `../../../0_entry_points/`).

### oc_platforms_mac_voicewake (12t · 11s · 11d)

**Terms**
- [Voice Wake](../../term_dictionary/term_voice_wake.md) — always-on wake-word listening that triggers capture; relevance: this note IS the macOS Voice-Wake feature (`VoiceWakeRuntime`, `swabbleTriggerWords`).
- [Push-to-Talk](../../term_dictionary/term_pushtotalk.md) — hold-key voice capture without a trigger word; relevance: the Right-Option PTT mode is half of this page's two-mode design.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — interactive voice interaction mode for an agent; relevance: voicewake is the macOS entry to OpenClaw's voice mode.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — converts captured audio into text; relevance: the Speech recognizer transcribes the spoken command before forwarding.
- [Real-Time Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming partial transcripts as speech flows; relevance: the overlay shows committed/volatile partials live during capture.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesizes spoken output / chimes; relevance: the Sounds setting (Glass chime on detect/send) and reply-delivery side.
- [Multimodal](../../term_dictionary/term_multimodal.md) — combining audio/text/visual modalities; relevance: voice capture feeds the same text agent loop as typed chat.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway-to-agent product; relevance: the host product whose macOS app owns this feature.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional transport; relevance: transcripts forward to the active gateway/agent over the Gateway WS.
- [LLM](../../term_dictionary/term_llm.md) — the agent model behind the conversation; relevance: the forwarded transcript is the prompt the agent answers.
- [Voice Call](../../term_dictionary/term_voice_call.md) — phone/voice channel pathway; relevance: replies route to the last-used main provider (WhatsApp/Telegram/Discord/WebChat), the voice/messaging delivery side.
- [Voice Bot](../../term_dictionary/term_voice_bot.md) — agent reachable over a voice interface; relevance: the macOS Voice-Wake makes the Mac a hands-free voice front-end to the agent.

**Docs**
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, this series) the menu-bar app that hosts the recognizer; relevance: voicewake inherits its local-vs-remote forwarding mode.
- [oc_platforms_mac_webchat](oc_platforms_mac_webchat.md) — (planned, this series) embedded chat view; relevance: a failed reply is still visible via WebChat/session logs.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — Claude Code voice dictation feature; relevance: the closest peer feature (speech captured into an agent prompt).
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — how to use Hermes voice mode end-to-end; relevance: sibling coding-agent voice-mode UX for comparison.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — CLI flags driving Hermes voice mode; relevance: the CLI counterpart of the macOS Voice settings toggles.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — Hermes speech-to-text transcription pipeline; relevance: the same STT step OpenClaw's `VoiceWakeRuntime` performs.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — Hermes text-to-speech provider options; relevance: the reply/chime synthesis side of a voice loop.
- [hermes_voice_gateway_discord_vc](../hermes_agent/hermes_voice_gateway_discord_vc.md) — voice over a Discord voice channel via the gateway; relevance: forwarding voice transcripts through a gateway to the agent.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media/audio message settings; relevance: the device/mic and media-routing settings analog.
- [oc_platforms_mac_xpc](oc_platforms_mac_xpc.md) — (planned, this series) IPC architecture; relevance: voice capture runs in the TCC-owning GUI app this note describes.
- [oc_nodes_voicewake](oc_nodes_voicewake.md) — (planned, this series, nd02) the node-level voicewake capability; relevance: the page's `## Related` links the node voicewake doc.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS/desktop companion apps; relevance: hosts `VoiceWakeRuntime`, the overlay controller, and the PTT monitor.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech / STT-TTS extension layer; relevance: the recognizer + chime synthesis implementation.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channel pathway; relevance: the reply-delivery counterpart for voice.

**Snippets**
- [snippet_openclaw_macos_voice_wake_audio](../../code_snippets/snippet_openclaw_macos_voice_wake_audio.md) — the audio-tap / capture path; relevance: the mic capture stage of wake-word mode.
- [snippet_openclaw_macos_voice_wake_state](../../code_snippets/snippet_openclaw_macos_voice_wake_state.md) — recognizer state machine; relevance: the lifecycle invariants (restart-on-resume) this page hardens.
- [snippet_openclaw_macos_voice_wake_trigger](../../code_snippets/snippet_openclaw_macos_voice_wake_trigger.md) — trigger-token + pause detection; relevance: the ~0.55s meaningful-pause gate before firing.
- [snippet_openclaw_macos_pushtotalk_nsevent](../../code_snippets/snippet_openclaw_macos_pushtotalk_nsevent.md) — global `.flagsChanged` right-Option monitor; relevance: the PTT hotkey (`keyCode 61` + `.option`).
- [snippet_openclaw_macos_pushtotalk_overlay](../../code_snippets/snippet_openclaw_macos_pushtotalk_overlay.md) — PTT overlay streaming partials; relevance: the held-key overlay this page describes.
- [snippet_openclaw_gateway_agent_voice_wake_tracking](../../code_snippets/snippet_openclaw_gateway_agent_voice_wake_tracking.md) — gateway-side voice-wake session tracking; relevance: how the forwarded transcript is tracked agent-side.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — the `swabbleTriggerWords` speech pipeline; relevance: the exact trigger-word pipeline named in this page.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — dedup of voice-driven node exec events; relevance: a single utterance must not double-fire forwarding.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — relays transcription to the agent; relevance: the forward-to-active-gateway step.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — a concrete STT provider integration; relevance: an implementation of the speech-recognition step.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local TTS synthesis; relevance: the chime/reply synthesis side.

**Entry**

### oc_platforms_mac_webchat (10t · 11s · 11d)

**Terms**
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional transport; relevance: the WebChat data plane is the Gateway WS (`chat.*` methods + events).
- [Server-Sent Events](../../term_dictionary/term_sse.md) — server-pushed event stream; relevance: the `chat`/`agent`/`presence`/`tick`/`health` events streamed to the view.
- [Streaming](../../term_dictionary/term_realtime_transcription.md) — incremental message delivery; relevance: WebChat renders the assistant reply as it streams in.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host product; relevance: WebChat is the macOS app's native chat surface for OpenClaw.
- [LLM](../../term_dictionary/term_llm.md) — the agent model; relevance: the conversation in WebChat is with the agent.
- [Authentication](../../term_dictionary/term_authentication.md) — connection trust/credentials; relevance: remote mode forwards the control port over an authenticated SSH tunnel.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — tunnel that fronts a backend; relevance: the SSH tunnel acts as the data-plane proxy in remote mode.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell / tunneling; relevance: remote mode forwards only the Gateway WS control port over SSH.
- [Remote SSH](../../term_dictionary/term_remote_ssh.md) — remote-host SSH access pattern; relevance: WebChat's remote mode is exactly this pattern for the data plane.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/function-call protocol; relevance: `chat.history` strips inline tool-call XML (`<tool_call>`, `<function_call>`) from visible text.

**Docs**
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, this series) the menu-bar host app; relevance: WebChat is launched from the Lobster menu and shares local-vs-remote modes.
- [oc_web_webchat](oc_web_webchat.md) — (planned, this series, wb01) the browser WebChat doc; relevance: the page's `## Related` links the web WebChat; same data plane.
- [hermes_web_dashboard_overview](../hermes_agent/hermes_web_dashboard_overview.md) — Hermes web chat/dashboard UI; relevance: sibling coding-agent web-chat surface for comparison.
- [hermes_desktop_app](../hermes_agent/hermes_desktop_app.md) — Hermes desktop companion app; relevance: the closest analog (a native desktop app embedding chat).
- [hermes_tui_interface](../hermes_agent/hermes_tui_interface.md) — Hermes terminal chat UI; relevance: another front-end over the same session/transcript model.
- [cc_vs_code_prompt_box_and_sessions](../claude_code/cc_vs_code_prompt_box_and_sessions.md) — Claude Code embedded prompt + sessions; relevance: an embedded chat view with a session switcher, like WebChat.
- [cc_web_session_management](../claude_code/cc_web_session_management.md) — Claude Code web session handling; relevance: defaulting to main session + switching sessions, mirrored here.
- [cc_desktop_overview_and_sessions](../claude_code/cc_desktop_overview_and_sessions.md) — Claude Code desktop sessions overview; relevance: session-centric desktop chat UX analog.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard auth; relevance: the remote-mode auth/trust surface of a web chat.
- [band_websocket_overview](../band/band_websocket_overview.md) — WebSocket transport for human chat channels; relevance: the WS data-plane model WebChat consumes.
- [oc_platforms_mac_voicewake](oc_platforms_mac_voicewake.md) — (planned, this series) voice capture; relevance: failed voice replies are surfaced via WebChat.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — desktop companion apps; relevance: hosts the native SwiftUI WebChat view.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: implements the `chat.history`/`chat.send`/`chat.abort`/`chat.inject` methods + events.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session management; relevance: main/global session defaulting + the session switcher.

**Snippets**
- [snippet_openclaw_gateway_chat_history_inject_handler](../../code_snippets/snippet_openclaw_gateway_chat_history_inject_handler.md) — `chat.history`/`chat.inject` handler; relevance: the display-normalized transcript this page describes.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — `chat.send` handler; relevance: the send method the WebChat view calls.
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — `chat.abort` handler; relevance: the abort method exposed to WebChat.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — sanitizes attachments / control tokens; relevance: the tool-call XML + control-token stripping in `chat.history`.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — transcript media pipeline; relevance: how media rows are normalized for display.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — chat-session lifecycle persistence; relevance: defaulting to the primary session + onboarding's dedicated session.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered deltas + `tick`/`health`; relevance: the `tick`/`health` events the view consumes.
- [snippet_openclaw_macos_menu_sessions_control](../../code_snippets/snippet_openclaw_macos_menu_sessions_control.md) — menu-bar session control; relevance: the session switcher driving the WebChat session.
- [snippet_openclaw_macos_menu_sessions_submenu](../../code_snippets/snippet_openclaw_macos_menu_sessions_submenu.md) — sessions submenu; relevance: the per-session UI surface for switching.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — Gateway WS connection setup; relevance: the local-mode direct WS connection WebChat opens.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect over a proxy/tunnel; relevance: remote mode's tunneled control-port connection.

**Entry**

### oc_platforms_mac_xpc (10t · 12s · 11d)

**Terms**
- [IPC](../../term_dictionary/term_ipc.md) — inter-process communication; relevance: this note IS the macOS IPC architecture.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: agent actions flow through the Gateway WS via `node.invoke`.
- [RPC](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: `node.invoke` is an RPC over the transport.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON RPC framing; relevance: PeekabooBridge uses a JSON protocol over its socket; node commands are RPC-shaped.
- [Authentication](../../term_dictionary/term_authentication.md) — peer/token trust; relevance: the UDS uses token + peer-UID + HMAC challenge/response.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host product; relevance: the macOS IPC surface of OpenClaw's app.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation of a privileged surface; relevance: all comms stay local-only (no network sockets), TeamID-gated.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/function invocation; relevance: `node.invoke` of `system.run`/`canvas.*`/`system.notify` are function calls.
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — the exec/`system.run` capability; relevance: `system.run` is forwarded over the UDS to the app's UI context.
- [Kill Tree](../../term_dictionary/term_kill_tree.md) — terminating a process subtree; relevance: the single-instance + restart/rebuild flow kills existing instances.

**Docs**
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, this series) the menu-bar app; relevance: shares the same SCI diagram + exec-approvals flow.
- [oc_platforms_mac_peekaboo](oc_platforms_mac_peekaboo.md) — (planned, this series, pf03) PeekabooBridge details; relevance: the `bridge.sock` UI-automation surface this page summarizes.
- [oc_tools_exec_approvals_advanced](oc_tools_exec_approvals_advanced.md) — (planned, this series, to03) the macOS IPC exec-approvals flow; relevance: the page's `## Related` links the exec-approvals IPC flow anchor.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — Claude Code security/process model; relevance: the architectural peer for a coding-agent's privileged-surface model.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permission split; relevance: the local-only / privileged-surface isolation argument.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — filesystem/network isolation; relevance: "no network sockets exposed; all comms local-only" mirrors this.
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — the Pi agent RPC protocol; relevance: the RPC/transport peer for agent-to-host invocation.
- [pi_security_model](../pi/pi_security_model.md) — Pi agent security model; relevance: token/peer-trust hardening peer.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation; relevance: the same "keep the privileged surface single + signed" principle.
- [band_websocket_overview](../band/band_websocket_overview.md) — WebSocket transport overview; relevance: the WS/`node.invoke` transport this IPC sits behind.
- [band_a2a_overview](../band/band_a2a_overview.md) — agent-to-agent transport; relevance: a peer transport-architecture doc for cross-process agent commands.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/hardening code; relevance: the 0600 socket, token, HMAC, TTL, TeamID gate.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — desktop apps; relevance: the single signed GUI app instance that owns TCC.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: the WS + `node.invoke` transport and node host service.

**Snippets**
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — `system.run` approval manager; relevance: the exec-approval path the UDS forwards to.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: privileged-surface hardening behind the IPC.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: forward only declared/allowed `node.invoke` commands.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — in-app exec orchestration; relevance: the app performs the exec in UI/TCC context.
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — shell backend behind exec; relevance: how `system.run` reaches a shell after approval.
- [snippet_openclaw_security_openshell_fs_bridge](../../code_snippets/snippet_openclaw_security_openshell_fs_bridge.md) — fs bridge for the shell; relevance: bridging exec output back over the socket.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny-list for dangerous tools; relevance: the hardening posture for the privileged surface.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — process kill-tree; relevance: the restart/single-instance flow that kills existing instances.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervision; relevance: managing the node host service + app lifecycle.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — Gateway WS connection; relevance: the node host service connecting to the Gateway WS.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — node exec event dedup; relevance: the node-command event path over the transport.
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP server/transport; relevance: a peer agent-transport surface to the WS+UDS model.

**Entry**

### oc_platforms_macos (12t · 12s · 12d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host product; relevance: this is OpenClaw's macOS menu-bar companion app.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: the Gateway WS handshake/discovery the app and debug CLI exercise.
- [Authentication](../../term_dictionary/term_authentication.md) — trust/credentials; relevance: exec-approvals deny/ask, the deep-link `key`, and remote auth.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/function invocation; relevance: node `canvas.*`/`system.run`/`screen.*`/`camera.*` commands.
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — the exec/`system.run` capability; relevance: `system.run` governed by Exec approvals is the central operational surface.
- [Sandbox](../../term_dictionary/term_sandbox.md) — execution-policy isolation; relevance: exec-approvals allowlist + env-var filtering is a sandboxing policy.
- [Safelist](../../term_dictionary/term_safelist.md) — allowlist of permitted items; relevance: `exec-approvals.json` allowlist glob patterns for resolved binaries.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — tunnel fronting a backend; relevance: the Remote-mode SSH control tunnel.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell / tunnel; relevance: `ssh -N -L` control tunnel to a remote Gateway.
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — local service discovery; relevance: gateway discovery (local + Tailscale + `dns-sd`) the app/debug CLI runs.
- [IPC](../../term_dictionary/term_ipc.md) — inter-process communication; relevance: the node host service ↔ app UDS for `system.run`.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: remote-mode connection auth tokens.

**Docs**
- [oc_platforms_mac_xpc](oc_platforms_mac_xpc.md) — (planned, this series) IPC architecture; relevance: the same SCI diagram this app implements.
- [oc_platforms_mac_webchat](oc_platforms_mac_webchat.md) — (planned, this series) embedded chat; relevance: launched from this app over the same Gateway.
- [oc_platforms_mac_voicewake](oc_platforms_mac_voicewake.md) — (planned, this series) voice capture; relevance: shares the app's local-vs-remote forwarding mode.
- [oc_gateway_troubleshooting](oc_gateway_troubleshooting.md) — (planned, this series, gw07) Gateway troubleshooting; relevance: the launchd respawn-protection / Maintenance-Sleep note this page links.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — hosting a background agent process; relevance: the launchd-managed background Gateway lifecycle analog.
- [cc_desktop_overview_and_sessions](../claude_code/cc_desktop_overview_and_sessions.md) — desktop app overview + sessions; relevance: the closest peer (a desktop companion managing an agent).
- [cc_remote_vs_web_and_deep_links](../claude_code/cc_remote_vs_web_and_deep_links.md) — remote/web modes + deep links; relevance: directly mirrors local-vs-remote mode and the `openclaw://agent` deep-link scheme.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permissions; relevance: the exec-approvals security/ask/allowlist model.
- [cc_tool_specific_permission_rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool permission rules; relevance: per-command allowlist + shell-control-syntax handling.
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — command-approval flow; relevance: the peer of `system.run` Exec approvals (deny/ask/allow-always).
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway operations/lifecycle; relevance: install/attach/restart of a managed gateway service.
- [hermes_desktop_remote_backend](../hermes_agent/hermes_desktop_remote_backend.md) — desktop app over a remote backend; relevance: Remote-mode SSH-tunneled connection to a remote Gateway.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — desktop apps; relevance: the menu-bar companion app itself.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: the launchd-managed Gateway the app installs/attaches to.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security code; relevance: exec-approvals + `system.run` env-var/shell filtering.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/onboarding; relevance: `openclaw gateway install` and `openclaw doctor` referenced here.

**Snippets**
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — renders the LaunchAgent plist; relevance: the `ai.openclaw.gateway` LaunchAgent definition.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart handoff; relevance: `launchctl kickstart -k` / `bootout` lifecycle.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval manager; relevance: Exec approvals / `exec-approvals.json` enforcement.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: env-var dropping + shell-wrapper allowlist this page lists.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — respawn protection; relevance: the launchd respawn-protection gate referenced in troubleshooting.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: which node `canvas.*`/`system.*` commands are forwarded.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — node exec event dedup; relevance: the node command path the app exposes.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — in-app exec orchestration; relevance: `system.run` executes in the app's UI/TCC context.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — Gateway WS connection; relevance: the WS handshake the app/debug CLI performs.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — connect over a proxy/tunnel; relevance: Remote-mode tunneled connection plumbing.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — discovery normalization; relevance: the gateway discovery pipeline (`local.` + wide-area + Tailscale).
- [snippet_openclaw_macos_menu_sessions_control](../../code_snippets/snippet_openclaw_macos_menu_sessions_control.md) — menu-bar session control; relevance: the menu-bar status/session surface this app owns.

**Entry**

### oc_platforms_windows_install (11t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host product; relevance: installing OpenClaw (Hub / native / WSL2) on Windows.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: the Gateway WS listener the install exposes (and over LAN).
- [Authentication](../../term_dictionary/term_authentication.md) — connection trust; relevance: setup-code / token / SSH-tunnel connection auth in first-run setup.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — port forwarding to a backend; relevance: `netsh portproxy` forwarding a Windows port to the WSL Gateway.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell / tunnel; relevance: connecting to a Gateway through an SSH tunnel; LAN SSH example.
- [Cron](../../term_dictionary/term_cron.md) — scheduled/recurring execution; relevance: Windows Scheduled Tasks / `systemd` linger auto-start are the scheduling analog.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: Windows Hub also installs the local MCP-server path.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — gateway fronting services; relevance: the WSL/native Gateway as the service endpoint being installed.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: WSL2 as the Linux-compatible runtime alternative to native install.
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — local discovery; relevance: connecting to a local Gateway on the PC vs a remote URL.
- [VPN](../../term_dictionary/term_vpn.md) — private network reachability; relevance: remote nodes must reach a reachable Gateway URL (LAN/VPN), not `127.0.0.1`.

**Docs**
- [oc_platforms_windows_node_modes](oc_platforms_windows_node_modes.md) — (planned, this series) the node/MCP/troubleshooting half; relevance: same source page, the operate-after-install companion.
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, this series) macOS app; relevance: the analogous launchd-vs-Scheduled-Tasks managed-Gateway lifecycle.
- [oc_install_node](oc_install_node.md) — (planned, this series, in04) Node.js setup; relevance: the page's `## Related` links Node setup (recommended Gateway runtime).
- [hermes_install_windows_native](../hermes_agent/hermes_install_windows_native.md) — native Windows install; relevance: the direct peer of the PowerShell `install.ps1` / native CLI path.
- [hermes_install_windows_wsl2](../hermes_agent/hermes_install_windows_wsl2.md) — Windows WSL2 install; relevance: the direct peer of the WSL2 Gateway setup (systemd, distro).
- [cc_install](../claude_code/cc_install.md) — Claude Code install paths; relevance: the multi-path installer pattern (Hub vs CLI) for a coding agent.
- [cc_desktop_scheduled_tasks](../claude_code/cc_desktop_scheduled_tasks.md) — Windows Scheduled Tasks for an agent; relevance: the `schtasks` auto-start-before-login mechanism.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway operations; relevance: `gateway install/run/status` lifecycle the install configures.
- [hermes_profile_gateways_services](../hermes_agent/hermes_profile_gateways_services.md) — gateway service profiles; relevance: managed-startup service installation analog.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote/tunnel auth; relevance: connecting to a remote Gateway by URL+token or SSH tunnel.
- [cc_mcp_installation_scopes](../claude_code/cc_mcp_installation_scopes.md) — MCP install scopes; relevance: the local MCP-server install path Hub also provides.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — desktop apps; relevance: the Windows Hub WinUI companion app.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: the Gateway installed inside WSL / natively.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/onboarding wizard; relevance: `openclaw onboard`/`gateway install`/`doctor`/`gateway run`.

**Snippets**
- [snippet_openclaw_daemon_schtasks_argv_render](../../code_snippets/snippet_openclaw_daemon_schtasks_argv_render.md) — renders the `schtasks` argv; relevance: the Windows Scheduled-Task startup command this page builds.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — renders/parses the systemd unit; relevance: the WSL `systemd` `openclaw-gateway.service` install.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger/env; relevance: `loginctl enable-linger` for headless WSL auto-start.
- [snippet_openclaw_daemon_schtasks_pid_kill_tree](../../code_snippets/snippet_openclaw_daemon_schtasks_pid_kill_tree.md) — schtasks PID kill-tree; relevance: managing the Scheduled-Task-launched process tree.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — the Gateway WS/HTTP listener; relevance: the listener exposed over LAN via portproxy.
- [snippet_openclaw_process_windows_cmd_shim](../../code_snippets/snippet_openclaw_process_windows_cmd_shim.md) — Windows command shim; relevance: invoking `wsl.exe`/PowerShell commands from the app/CLI.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist render; relevance: the cross-OS managed-startup analog (macOS counterpart).
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — gateway auth at startup; relevance: setup-code/token auth when the Gateway starts.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — install/auth rate-limit policy; relevance: hardening the freshly installed Gateway's auth surface.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — connect over a tunnel/proxy; relevance: connecting to a Gateway through an SSH tunnel.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervision; relevance: keeping the installed Gateway process alive.

**Entry**

### oc_platforms_windows_node_modes (12t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host product; relevance: Windows Hub as an OpenClaw node + local MCP server.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the local MCP-server mode + off/on mode matrix.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/function invocation; relevance: node capability commands (`canvas.*`/`screen.*`/`camera.*`/`system.run`/`stt.transcribe`/`tts.speak`).
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — the exec/`system.run` capability; relevance: controlled `system.run`/`system.run.prepare`/`system.which` node commands.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: the Gateway-connected node command transport.
- [Authentication](../../term_dictionary/term_authentication.md) — pairing/trust; relevance: node mode requires Gateway pairing (`devices approve`) + bearer token for MCP.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — device/operator pairing approval; relevance: `openclaw devices list/approve <request-id>` to authorize the node.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: the `tts.speak` declared node capability.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — speech recognition; relevance: the `stt.transcribe` declared node capability.
- [Safelist](../../term_dictionary/term_safelist.md) — allowlist of permitted commands; relevance: `gateway.nodes.allowCommands` opt-in for privacy-sensitive commands.
- [Access Control](../../term_dictionary/term_access_control.md) — permission gating; relevance: the Gateway forwards only declared + server-policy-allowed commands.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic UI control; relevance: `canvas.*`/`screen.snapshot` node commands automate the desktop surface.

**Docs**
- [oc_platforms_windows_install](oc_platforms_windows_install.md) — (planned, this series) the install half; relevance: same source page, prerequisite to node/MCP mode.
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, this series) macOS app node; relevance: node-capability parity (`canvas.*`/`screen.*`/`camera.*`/`system.*`).
- [oc_nodes](oc_nodes.md) — (planned, this series, rt02) the Nodes overview; relevance: the page's `## Related` links the Nodes doc.
- [oc_web_control_ui](oc_web_control_ui.md) — (planned, this series, wb01) the Control UI; relevance: linked from `## Related`; pairing/node status surface.
- [band_mcp_overview](../band/band_mcp_overview.md) — MCP server overview; relevance: exposing a capability registry as an MCP server, like local MCP mode.
- [band_mcp_ai_assistant_setup](../band/band_mcp_ai_assistant_setup.md) — local MCP for assistants (Claude Desktop/Cursor); relevance: the exact MCP clients this page names.
- [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — Claude Code MCP overview; relevance: the MCP-client/server model the loopback server serves.
- [cc_mcp_transports](../claude_code/cc_mcp_transports.md) — MCP transports (stdio/HTTP/loopback); relevance: the loopback MCP endpoint + bearer token.
- [hermes_mcp_concept_config](../hermes_agent/hermes_mcp_concept_config.md) — MCP concept + config; relevance: enabling/configuring a local MCP server peer.
- [hermes_use_mcp_guide](../hermes_agent/hermes_use_mcp_guide.md) — how to use MCP servers/clients; relevance: driving Windows capabilities from an MCP client.
- [cc_desktop_permission_modes](../claude_code/cc_desktop_permission_modes.md) — desktop permission modes; relevance: explicit opt-in for privacy-sensitive (`screen.record`/`camera.*`) commands.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — desktop apps; relevance: Windows Hub acting as a node + MCP server.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: pairing + command forwarding + `allowCommands` policy.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security code; relevance: the privacy-sensitive-command opt-in enforcement.

**Snippets**
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — the pairing flow; relevance: `devices list/approve` + node pairing this page documents.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: forward only declared + `allowCommands`-allowed commands.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback MCP HTTP server; relevance: the local MCP-server endpoint + bearer token.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — node exec event dedup; relevance: the node command/event execution path.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — pairing allowlist; relevance: approving + allowlisting a paired device.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: invoking a declared node capability from the Gateway.
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — node presence/status events; relevance: `openclaw nodes status` health/presence the page checks.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: the privacy-sensitive command gating.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listener; relevance: the loopback listener hosting the MCP server.
- [snippet_openclaw_process_windows_cmd_shim](../../code_snippets/snippet_openclaw_process_windows_cmd_shim.md) — Windows command shim; relevance: running the Windows-side `openclaw devices`/`nodes` commands.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP plugin/route mux; relevance: routing the MCP-server endpoint alongside gateway routes.

**Entry**

> **Verified-existing reusable targets pool (DB-checked at xref-augment 2026-06-21).** Terms (all present):
> term_voice_wake, term_pushtotalk, term_voice_mode, term_speech_to_text, term_realtime_transcription,
> term_text_to_speech, term_multimodal, term_voice_call, term_voice_bot, term_openclaw, term_websocket,
> term_sse, term_llm, term_authentication, term_reverse_proxy, term_ssh, term_remote_ssh, term_function_calling,
> term_ipc, term_rpc, term_json_rpc, term_sandbox, term_code_execution_tool, term_kill_tree, term_safelist,
> term_bonjour_discovery, term_oauth_token, term_mcp, term_dm_pairing, term_access_control, term_browser_automation,
> _security/_sessions/_cli_wizard/_extensions_voice_speech/_channels_voice_phone/_extensions/_skills),
> claude_code/cc_voice_dictation, cc_vs_code_prompt_box_and_sessions, cc_web_session_management,
> cc_desktop_overview_and_sessions, cc_remote_vs_web_and_deep_links, cc_background_session_hosting,
> cc_sandbox_vs_permissions, cc_sandbox_filesystem_network_isolation, cc_tool_specific_permission_rules,
> cc_security_architecture, cc_install, cc_mcp_overview, cc_mcp_transports, cc_mcp_installation_scopes,
> cc_desktop_scheduled_tasks, cc_desktop_permission_modes; hermes_agent/hermes_use_voice_mode_guide,
> hermes_voice_mode_cli, hermes_stt_transcription, hermes_tts_providers, hermes_voice_gateway_discord_vc,
> hermes_messaging_media_settings, hermes_web_dashboard_overview, hermes_desktop_app, hermes_tui_interface,
> hermes_dashboard_auth_remote, hermes_security_isolation_credentials, hermes_security_command_approval,
> hermes_gateway_operations, hermes_desktop_remote_backend, hermes_install_windows_native,
> hermes_install_windows_wsl2, hermes_profile_gateways_services, hermes_mcp_concept_config, hermes_use_mcp_guide;
> pi/pi_rpc_protocol, pi_security_model; band/band_websocket_overview, band_a2a_overview, band_mcp_overview,
> series (created by their own waves: pf03 peekaboo/permissions, gw07 troubleshooting, in04 node, nd02 voicewake,
> rt02 nodes, wb01 control-ui/webchat, to03 exec-approvals-advanced) — marked "(planned, this series)".

## Undigested Terms Plan (Step 4e)

pf04 creates **0 new `term_dictionary` notes** (per master design: OpenClaw vocabulary is digested as `oc_*`
doc notes by its home sub-plan; the only term-dictionary interaction is LINKING existing terms; no term
definition is ever inlined in an `oc_*` note).

| Term | Disposition |
|---|---|
| Voice Wake / push-to-talk / wake-word / `swabbleTriggerWords` | Documented in note 1 (`oc_platforms_mac_voicewake`); link existing `term_voice_wake`, `term_speech_to_text`, `term_text_to_speech`. Not a new term. |
| `VoiceWakeRuntime` / `VoiceSessionCoordinator` / `VoiceWakeForwarder` / `VoicePushToTalk` (code symbols) | Implementation symbols documented in note 1 body + linked to voice snippets; not vault terms. |
| WebChat (embedded SwiftUI view) / `chat.history`/`chat.send`/`chat.abort`/`chat.inject` (WS methods) | Documented in note 2; link `term_websocket`, `term_sse`. WS method names are config/API surface, not promoted to terms. |
| IPC / Unix domain socket / HMAC challenge-response / TTL / peer-UID / PeekabooBridge / TeamID | Documented in note 3; link existing `term_ipc`, `term_authentication`, `term_sandbox`. UDS/HMAC/TeamID are described in-body (no existing `term_unix_domain_socket`/`term_hmac` note — see new-term candidates). |
| launchd / LaunchAgent (`ai.openclaw.gateway`) / `launchctl kickstart`/`bootout` | Documented in note 4; macOS-specific service mechanism described in-body (no `term_launchd` note; not cross-cutting enough to capture — see candidates). |
| Exec approvals / `exec-approvals.json` / allowlist globs / env-var filtering | Documented in note 4; link existing `term_sandbox`, `term_authentication`. Policy surface, not a term. |
| Deep links / `openclaw://` URL scheme / `openclaw://agent` | Documented in note 4; described in-body (no `term_url_scheme`/`term_deep_link` note; macOS app surface). |
| Windows Hub / Windows node mode / Command Center | Documented in notes 5–6; product/UI surface, link `term_openclaw`. Not terms. |
| WSL2 / `systemd` / `dbus-launch` / linger / Scheduled Tasks / `netsh portproxy` | Documented in notes 5–6; OS-mechanism config described in-body (no `term_wsl`/`term_systemd` note; OS-specific, not cross-cutting). |
| Local MCP mode / loopback MCP server / bearer token / mode matrix | Documented in note 6; link existing `term_mcp`. MCP-server-as-config, not a new term. |
| Tailscale / MagicDNS / Bonjour discovery / SSH control tunnel | Mentioned in notes 2/4 as link-out; link `term_reverse_proxy`; remote-access detail deferred to `mac/remote` (pf03) + gateway series. |

**New-term candidates (genuinely cross-cutting, no existing note):** none proposed for capture in pf04.
Two recurring cross-cutting concepts (`Unix domain socket` and `HMAC challenge/response`) lack a vault term
note and appear across the IPC/security corpus; they are NOT promoted here because (a) they are described
in-body in note 3 and (b) the security/gateway sub-plans (se01/gw0x) are the better owners if a vault-wide
`term_unix_domain_socket` / `term_hmac` is ever warranted. pf04 flags them for the master's corpus-wide
new-term inventory but captures **0**.

## Term-Note Authoring Requirements

**N/A (0 new terms).** pf04 authors zero `term_dictionary` notes; it only LINKS existing terms (inherited from
master). If augment's re-run of Step 2d surfaces a genuinely reusable, no-home, no-existing-note term, it is
captured via `/tessellum-capture-term-note` + added to its best-fit acronym glossary (candidate glossary for the
two flagged infra terms above: `acronym_glossary_software_engineering.md` / a systems-glossary) — expected 0.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (6 notes, P2). All gates must pass before commit.

| Gate | Check | Tooling |
|------|-------|---------|
| G1 | Format: YAML field order + forbidden fields; H1 `# OpenClaw — …`, `## Overview`, `## Related Notes`, `## References`, bold footer; ≤400 lines / ≤2,500 words / ≤6 code blocks; one building_block | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim/code fence traces to `inbox/openclaw_docs/platforms/<page>.md` (diff vs source) | manual diff vs mirror |
| G3 | Density + coverage: within caps AND every mapped H2/H3 represented (Section Coverage Map) | `wc -w` + fence count |
| G4 | Cross-reference: ≥6 relevance-selected terms + repo_openclaw* + sibling oc_* + snippets per note, each indexed link with a relevance statement | review vs Candidate Cross-References |
| G5 | Ghost-reference detect + redirect (no link to a non-existent note) | `/tessellum-fix-ghost-references` / `scripts` |
| G6 | Broken-link fix (correct relative paths) | `/tessellum-fix-broken-links` |
| G7 | Discoverability: every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | inlink check (entry_openclaw_docs + repos/terms) |
| G8 | In-degree ≥1 (anti-island) after reindex | `note_links` query |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_platforms_mac_voicewake oc_platforms_mac_webchat oc_platforms_mac_xpc oc_platforms_macos oc_platforms_windows_install oc_platforms_windows_node_modes"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT-OK"
  # required H2 sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density caps (body words excl. frontmatter; code blocks)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
  # sibling-prefix cross-link presence (G4 quick signal)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "$n NO SIBLING oc_ LINK"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G6 after reindex:
bash scripts/update_notes_database.sh --force   # then broken-link + in-degree sweep
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code (≤6) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_platforms_mac_voicewake | concept | 520 | 0 | ✅ |
| 2 | oc_platforms_mac_webchat | concept | 320 | 1 | ✅ |
| 3 | oc_platforms_mac_xpc | model | 480 | 1 (SCI diagram fence) | ✅ |
| 4 | oc_platforms_macos | procedure | 760 | ≤6 (trim 7→6: launchctl, exec-approvals JSON, deep-link `open`, state-dir env, debug-CLI, SSH shape) | ✅ |
| 5 | oc_platforms_windows_install | procedure | 700 | ≤6 (install.ps1, gateway install/run, onboard, wsl install, systemd wsl.conf, netsh portproxy — select 6 of ~13) | ✅ |
| 6 | oc_platforms_windows_node_modes | procedure | 560 | ≤4 (pairing PowerShell, mode-matrix table, troubleshooting setup-log, gh-auth) | ✅ |

No note approaches the 2,500-word / 400-line cap. The split of `windows.md` (17 fences) is the only one
required to respect the 6-code-block cap; `macos.md` (7 fences) trims to 6 representative fences (the dropped
fence is the duplicate SCI diagram already shown in note 3 / the build-workflow snippet, reproduced selectively).

## Entry Point Decision (inherited from master)

Contributes **6 rows** to `entry_openclaw_docs.md` (created as a master pre-step, W1) under a **"Platforms →
macOS / Windows"** cluster (pf04). Each note receives its entry-point back-link at finalization — this is the
primary G7/G8 inbound-link source (anti-island). No new entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution; all sources verified EXISTING):

- `entry_openclaw_docs.md` (planned, master pre-step) → all 6 notes (primary inbound source).
- `repo_openclaw_apps.md` → notes 1, 2, 3, 4, 5, 6 (the desktop companion apps documented across all pages).
- `repo_openclaw_gateway.md` → notes 2, 4, 5, 6 (Gateway WS / launchd / install / pairing).
- `repo_openclaw_security.md` → notes 3, 4, 6 (IPC hardening / exec-approvals / command opt-in).
- `repo_openclaw_extensions_voice_speech.md` → note 1 (speech/STT-TTS pathway).
- `term_voice_wake.md` → note 1; `term_ipc.md` → note 3; `term_mcp.md` → notes 5, 6;
  `term_websocket.md` → notes 2, 3, 4; `term_openclaw.md` → all 6.

## Pacing Rules (inherited from master)

One execution phase, 6 notes (≤ fan-out cap). Re-read each source page during execution; reproduce config/CLI
snippets verbatim from the mirror; one BB per note. 8 gates pass before commit. `git pull --rebase --autostash`
first; no Claude co-author trailer; reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1
before commit; commit + push in the same cycle.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment at raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

---

### DB Verification Log (this plan)

term_agent_harness, term_autonomous_coding_agents, term_function_calling, term_sandbox, term_llm, term_claude,
term_oauth_token, term_websocket, term_json_rpc, term_cron, term_speech_to_text, term_text_to_speech,
term_voice_wake, term_ipc, term_reverse_proxy, term_sse, term_message_queue, term_authentication, term_oauth,
term_threat_model, term_tls; repo_openclaw(+_apps/_agents/_channels/_channels_messaging/_channels_voice_phone/
_cli_wizard/_extensions/_extensions_llm_providers/_extensions_voice_speech/_gateway/_memory/_security/_sessions/
entry_code_repos, entry_gen_ai_dev, entry_claude_code_docs, entry_pi_docs, entry_code_snippets_openclaw; and the
~27 `snippet_openclaw_*` ids cited in Candidate Cross-References (exact note_id match). NOT FOUND (so NOT cited
as existing — described in-body or flagged as new-term candidates): term_wake_word, term_ssh_tunnel,
term_unix_domain_socket, term_hmac, term_launchd, term_tailscale, term_wsl, term_systemd, term_url_scheme,
term_deep_link, term_tcc, term_node, term_gateway, term_session, term_speech_recognition, term_microphone,
term_accessibility, term_screen_recording, term_canvas, term_loopback, term_bearer_token, repo_hermes_agent_core,
entry_openclaw_docs (planned, master pre-step).

---

## Augmentation Report (2026-06-21)

**Scope of this augment:** xref-augment of pf04 to RAISED FLOORS (≥8 terms · ≥10 snippets · ≥10 docs per
note), relevance-selected from a fresh re-read of all 5 source pages under `inbox/openclaw_docs/platforms/`,
`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`; the Summary-Statistics cross-ref line
was updated to the raised-floor standard.

**Re-read measurements (CP7, body words excl. frontmatter):** voicewake 596w/0 fences · webchat 236w/1
(indented) fence · xpc 377w/1 fence · macos 1178w/7 fences · windows 1384w/17 fences. All within 0.7–1.3× the
plan's Source-table estimates (624/264/404/1208/1430) — no under-estimation; the windows split (17 fences →
notes 5+6) remains the only required split. No new splits; no over-compression or omitted section found.


| Note | Terms | Snippets | Docs (≥5 existing) | Repos | Floors met (≥8t·≥10s·≥10d) |
|---|---:|---:|---:|---:|---|
| oc_platforms_mac_voicewake | 12 | 11 | 11 (9 existing + 2 planned) | 3 | YES |
| oc_platforms_mac_webchat | 10 | 11 | 11 (9 existing + 2 planned) | 3 | YES |
| oc_platforms_mac_xpc | 10 | 12 | 11 (8 existing + 3 planned) | 3 | YES |
| oc_platforms_macos | 12 | 12 | 12 (8 existing + 4 planned) | 4 | YES |
| oc_platforms_windows_install | 11 | 11 | 11 (8 existing + 3 planned) | 3 | YES |
| oc_platforms_windows_node_modes | 12 | 11 | 11 (7 existing + 4 planned) | 3 | YES |

All six notes meet every floor. Every cited term (37 distinct), snippet (~40 distinct), repo (10 distinct),
xpc/macos/windows-install 8 each; windows-node-modes 7) — the remainder are sibling `oc_*` docs created by
their own waves, marked "(planned, this series)".

**New-term candidates + best-fit glossary:** none captured by pf04 (per master design: OpenClaw vocabulary is
digested as `oc_*` doc notes by its home sub-plan; the only `term_dictionary` interaction is LINKING existing
terms). Two recurring cross-cutting infra concepts remain without a vault term note and were flagged (NOT
captured) for the master's corpus-wide new-term inventory:
- **Unix domain socket** → candidate `term_unix_domain_socket`; best-fit glossary
  `acronym_glossary_software_engineering.md`. Owner: security/gateway sub-plans (se01 / gw0x), not pf04
  (described in-body in note 3).
- **HMAC challenge/response** → candidate `term_hmac`; best-fit glossary
  `acronym_glossary_software_engineering.md`. Owner: se01 / gw0x (described in-body in note 3).

These do not change pf04's term floors (every note already meets ≥8 with existing terms). The augment's Step-2d
re-read surfaced no additional capture-worthy term beyond the two already flagged.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link-fix, G7 outside-folder inbound, G8 in-degree≥1; single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` contributes 6 rows to `entry_openclaw_docs.md` (master W1 pre-step) under "Platforms → macOS / Windows"; every note's mapping cites `entry_openclaw_docs` as the primary inbound link. |
| CP4 | Plan size manageable (≤30 or split) | **PASS** | 6 planned notes ≤ 30 and ≤ fan-out cap; single phase. |
| CP5 | Note format derived from existing target-dir notes | **PASS** | Format inherited from master (derived from `claude_code/cc_*` + `pi/pi_*` corpora): `# OpenClaw — …` / `## Overview` / `## Related Notes` / `## References` / bold footer; YAML field order + forbidden-field list match; `source_url` required. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: all 6 notes ≤760w / ≤6 fences, far below the 2,500w / 400-line / 6-fence caps; windows.md split (17 fences) already applied; macos.md trims 7→6 fences. No borderline note unaddressed. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured all 5 pages this augment: 596/236/377/1178/1384w vs plan 624/264/404/1208/1430 — all within ±30%; no page >1.5× estimate, no re-split required. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (0 new terms by design; per-row disposition table); `## Term-Note Authoring Requirements` present (N/A — 0 new terms; capture-via-skill path stated if a term ever surfaces). |
| CP8f | Term-slug specificity / all-notes dedup-collision audit | **PASS** | 0 new term slugs ⇒ no specificity rename needed; all-notes dedup audit confirms 0 existing `documentation/openclaw/` notes (whole series new) and no planned `oc_*` doc duplicates an existing `term_*` (the mapping LINKS existing terms, never recreates them). |
| CP9 | Discoverability / inlinks executed (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound source (entry_openclaw_docs + repo_openclaw_* + term notes); G8-Discoverability is in the gate table; inlink-addition is a gated execution step, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
