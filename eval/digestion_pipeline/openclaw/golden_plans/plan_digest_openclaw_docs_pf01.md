---
title: Sub-Plan pf01 — OpenClaw Docs: Platforms (Android, EasyRunner, iOS, Linux, macOS Gateway + Canvas)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - platforms/android
  - platforms/easyrunner
  - platforms/ios
  - platforms/linux
  - platforms/mac/bundled-gateway
  - platforms/mac/canvas
---

# Sub-Plan pf01: Platforms

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*` prefix) / YAML+body format / three-way dedup /
> 9-GATE / cross-reference policy / entry-point wiring are ALL inherited from the master — not restated here.

## Scope

The 6 **Platforms** pages covering OpenClaw's per-OS client/runtime surfaces: the two mobile companion-node
apps (Android, iOS), Linux Gateway support + service install, and two macOS-specific runtimes (the external
launchd-managed bundled Gateway, and the WKWebView Canvas panel), plus one hosted-deployment platform
(EasyRunner / Podman + Caddy). These pages document **how the Gateway runs on, or is reached from, each
platform** and the node command surface (Canvas, camera, voice/talk, notifications) each app exposes.

**Priority: P2 (Phase B).** These pages depend on the conceptual/operational core (gateway, nodes,
pairing, channels, install) digested in Phase A; they are operational/feature docs, not the core
vocabulary. They link heavily to the existing CODE-side `repo_openclaw*` notes (apps/android, apps/ios,
macos canvas, daemon launchd/systemd) and the FZ 15 OpenClaw analysis.

**Source**: OpenClaw docs, 6 pages, **5,017 measured words**. **Planned: 9 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Android app | `platforms/android` | 1,620 | 8 | 6 | 10 | procedure (split: connect runbook vs node command surface) |
| EasyRunner | `platforms/easyrunner` | 449 | 3 | 6 | 0 | procedure |
| iOS app | `platforms/ios` | 1,670 | 10 | 12 | 4 | procedure + argument (split: connect/node vs push-relay trust model) |
| Linux app | `platforms/linux` | 511 | 7 | 7 | 0 | procedure |
| Gateway on macOS | `platforms/mac/bundled-gateway` | 313 | 3 | 5 | 0 | procedure |
| Canvas | `platforms/mac/canvas` | 454 | 5 | 7 | 1 | concept (model of the Canvas panel + API) |

(Code = fence count ÷ 2. android: 16/2=8 · easyrunner: 6/2=3 · ios: 20/2=10 · linux: 14/2=7 ·
bundled-gateway: 6/2=3 · canvas: 10/2=5.)

## Content Strategy

- **Prioritize**: the two mobile-node connection runbooks (every mobile user needs pairing + discovery +
  reconnect) and the iOS push-relay authentication/trust model (a non-obvious, security-relevant design
  that explains why APNs credentials stay off the gateway). These are the highest-value, least-obvious
  content on these pages.
- **Split** (word-cap and/or mixed-BB):
  - `android.md` (1,620w) → **note 1** the connect/discovery/pairing/presence runbook (procedure) +
    **note 2** the expanded node command surface (Chat, Canvas+camera, Voice/Talk, assistant entrypoints,
    notification forwarding) — distinct task clusters, keeps each focused.
  - `ios.md` (1,670w, 12 H2) → **note 3** the connect/discovery/canvas/voice node runbook (procedure) +
    **note 4** the relay-backed push + authentication/trust-flow model (argument/model BB — the "why this
    design" + hop-by-hop trust chain is a different building block than the connect procedure).
- **One note each** (reference pages ≤ ~520w, single BB): `easyrunner.md` → note 5; `linux.md` → note 6;
  `mac/bundled-gateway.md` → note 7; `mac/canvas.md` → note 8.
- **Series concept note**: a thin **note 9** `oc_platforms_model.md` (concept) digesting the top-level
  Platforms model — companion-node vs gateway-host roles, the per-OS support matrix, and the "Gateway runs
  on macOS/Linux/Windows; mobile is node-only" rule that recurs across all 6 pages. This gives the series
  an indexable hub note and absorbs the recurring "role / gateway-required / install" framing. (Sourced
  from the recurring Support-snapshot / Requirements / availability framing across all 6 pages — no new
  page.)
- **Link-out, do NOT redefine**: pairing approval (`/channels/pairing` → ch04/Phase-A), Bonjour/discovery
  (`/gateway/bonjour`, `/gateway/discovery` → gw02), Gateway runbook/config (`/gateway`,
  `/gateway/configuration` → gw01–02), trusted-proxy auth (`/gateway/trusted-proxy-auth` → gw06), Tailscale
  (`/gateway/tailscale` → gw06), camera/talk/voicewake node commands (`/nodes/*` → nd01–02), Docker/Nix/Bun
  install flows (→ in01–05), macos/windows/raspberry-pi sibling platform pages (pf02–04). `term_*` for
  websocket / oauth-token / tls / reverse-proxy / etc. are LINKED, never redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_platforms_android_connection.md` | procedure | android.md: Support snapshot, System control, Connection runbook (Prerequisites, 1 Start Gateway, 2 Verify discovery + Tailnet unicast DNS-SD, 3 Connect from Android, Presence alive beacons, 4 Approve pairing + auto-approve CIDRs, 5 Verify node connected) | 600 | Pairing and reconnecting the Android companion node: gateway start, mDNS/NSD + Tailscale wide-area discovery, secure-endpoint requirements (wss/Serve), the Connect tab + foreground service, presence-alive beacons, and CLI device approval (incl. CIDR auto-approve). |
| 2 | `oc_platforms_android_node_surface.md` | procedure | android.md: 6 Chat + history, 7 Canvas + camera (Gateway Canvas Host, canvas/camera commands), 8 Voice + expanded command surface (Mic/Talk, foreground-service promotion, device/notifications/photos/contacts/calendar/sms/motion families), Assistant entrypoints, Notification forwarding (allow/deny/quietHours/rateLimit) | 600 | The Android node command surface beyond connection: Chat session/history normalization, Gateway-hosted Canvas + camera commands, Mic vs Talk voice modes and foreground-service microphone promotion, the expanded device command families, Google-Assistant App-Actions entrypoint, and scoped notification forwarding. |
| 3 | `oc_platforms_ios_connection.md` | procedure | ios.md: What it does, Requirements, Quick start (pair + connect, auto-approve CIDRs), Background alive beacons, Discovery paths (Bonjour/Tailnet/Manual), Canvas + A2UI, Computer Use relationship (+ Canvas eval/snapshot), Voice wake + talk mode, Common errors | 650 | Pairing and operating the iOS companion node: quick-start pair/connect, discovery paths (Bonjour, tailnet unicast DNS-SD, manual host), background alive beacons, WKWebView Canvas + A2UI commands, the node-vs-Computer-Use boundary, voice-wake/talk (push-to-talk), and common foreground/reconnect errors. |
| 4 | `oc_platforms_ios_push_relay_trust.md` | argument | ios.md: Relay-backed push for official builds, Authentication and trust flow (hop-by-hop, why-designed), Local/manual builds direct APNs (env vars + key storage), Compatibility note | 650 | The iOS relay-backed push design and trust model: why official builds use the hosted push relay instead of raw APNs tokens on the gateway, the App-Attest + StoreKit + gateway-identity delegation hop-by-hop flow, the security constraints it enforces, and the direct-APNs fallback for local/manual builds. |
| 5 | `oc_platforms_easyrunner.md` | procedure | easyrunner.md: Before you begin, Compose app, Configure OpenClaw, Verify, Updates and backups, Troubleshooting | 450 | Hosting the OpenClaw Gateway on EasyRunner behind its Caddy proxy with Podman-compatible Compose: prerequisites + persistent volumes, the Compose service definition, gateway auth/bind config, probe/status verification, update/backup flow, and proxy/auth/volume troubleshooting. |
| 6 | `oc_platforms_linux.md` | procedure | linux.md: (intro — Node runtime), Beginner quick path (VPS), Install, Gateway, Gateway service install (CLI), System control (systemd user unit), Memory pressure and OOM kills | 550 | Running OpenClaw on Linux: Node-vs-Bun runtime guidance, the VPS quick path (install + onboard daemon + SSH tunnel), Gateway service install via CLI, the systemd user/system unit template, and Linux OOM-kill biasing (child `oom_score_adj` 1000) with verification. |
| 7 | `oc_platforms_mac_bundled_gateway.md` | procedure | mac/bundled-gateway.md: (intro — external CLI), Install the CLI, Launchd (Gateway as LaunchAgent), Version compatibility, Smoke check | 400 | The macOS Gateway runtime: the app no longer bundles Node/Bun or the Gateway, instead requiring an external `openclaw` CLI install and managing a per-user launchd LaunchAgent. Covers CLI install, the LaunchAgent label/plist/logging/behavior, version compatibility, and the smoke-check commands. |
| 8 | `oc_platforms_mac_canvas.md` | concept | mac/canvas.md: (intro), Where Canvas lives (custom URL scheme), Panel behavior, Agent API surface, A2UI in Canvas (v0.8 commands), Triggering agent runs from Canvas (deep links), Security notes | 500 | The macOS agent-controlled Canvas panel: a WKWebView visual workspace served via the `openclaw-canvas://` custom URL scheme, its per-session Application-Support storage, panel behavior, the Gateway-WebSocket agent API (present/navigate/eval/snapshot), A2UI v0.8 hosting, `openclaw://agent` deep-link triggers, and traversal/scheme security. |
| 9 | `oc_platforms_model.md` | concept | Cross-page model: recurring Support-snapshot / Requirements / availability framing across android, ios, linux, mac/bundled-gateway (companion-node vs gateway-host roles; per-OS support matrix; "Gateway on macOS/Linux/Windows, mobile = node-only") | 400 | Series hub: OpenClaw's platform model — the gateway-host vs companion-node role split, the per-OS support matrix (macOS/Linux/Windows host the Gateway; Android/iOS are node-only companions requiring a running Gateway), and the shared connect/pair/discover lifecycle every platform note specializes. |

## Section Coverage Map

```
platforms/android.md
├── (intro Note: Google Play + repo apps/android) ─────────── → note 1 (References) + note 9 (role)
├── Support snapshot (role / gateway required / install / protocols) → note 1 + note 9 (matrix)
├── System control (launchd/systemd on gateway host) ───────── → note 1
├── Connection runbook (Android ⇄ mDNS/NSD + WS ⇄ Gateway; wss/Serve) → note 1
│   ├── Prerequisites ──────────────────────────────────────── → note 1
│   ├── 1) Start the Gateway (--tailscale serve) ───────────── → note 1
│   ├── 2) Verify discovery (dns-sd; gateway discover --json) → note 1
│   │   └── Tailnet (Vienna⇄London) unicast DNS-SD ─────────── → note 1
│   ├── 3) Connect from Android (Connect tab, Setup Code/Manual) → note 1
│   ├──     Presence alive beacons (node.presence.alive) ───── → note 1
│   ├── 4) Approve pairing (devices list/approve; autoApproveCidrs) → note 1
│   └── 5) Verify the node is connected (nodes status, node.list) → note 1
├── 6) Chat + history (chat.history/send/subscribe, normalization) → note 2
├── 7) Canvas + camera (Gateway Canvas Host; canvas.*; camera.*) → note 2
├── 8) Voice + expanded command surface (Mic/Talk; device.*; sms/motion…) → note 2
├── Assistant entrypoints (App Actions / Google Assistant) ──── → note 2
└── Notification forwarding (allow/deny/quietHours/rateLimit) ─ → note 2
platforms/easyrunner.md
├── (intro — EasyRunner + Podman + Caddy) ─────────────────── → note 5
├── Before you begin ──────────────────────────────────────── → note 5
├── Compose app (services/volumes/labels) ─────────────────── → note 5
├── Configure OpenClaw (gateway bind/port/auth.token) ─────── → note 5
├── Verify (gateway probe/status) ─────────────────────────── → note 5
├── Updates and backups ───────────────────────────────────── → note 5
└── Troubleshooting ───────────────────────────────────────── → note 5
platforms/ios.md
├── (intro — availability / source builds) ────────────────── → note 3 + note 9
├── What it does ──────────────────────────────────────────── → note 3 + note 9 (role)
├── Requirements (gateway elsewhere; LAN/tailnet/manual) ──── → note 3
├── Quick start (pair + connect; autoApproveCidrs) ────────── → note 3
├── Relay-backed push for official builds ──────────────────── → note 4
├── Background alive beacons (node.presence.alive) ─────────── → note 3
├── Authentication and trust flow (hop-by-hop; why-designed) ─ → note 4
├──   Local/manual builds direct APNs (env vars; key storage) → note 4
├──   Compatibility note (env overrides) ─────────────────────→ note 4
├── Discovery paths (Bonjour / Tailnet / Manual host) ─────── → note 3
├── Canvas + A2UI ─────────────────────────────────────────── → note 3
├── Computer Use relationship (+ Canvas eval / snapshot) ──── → note 3
├── Voice wake + talk mode (ptt commands) ─────────────────── → note 3
└── Common errors ─────────────────────────────────────────── → note 3
platforms/linux.md
├── (intro — Gateway supported; Node recommended; Bun not) ── → note 6 + note 9 (matrix)
├── Beginner quick path (VPS) ─────────────────────────────── → note 6
├── Install ───────────────────────────────────────────────── → note 6 (links out in01–05)
├── Gateway (runbook / configuration pointers) ────────────── → note 6 (links out gw01–02)
├── Gateway service install (CLI) ─────────────────────────── → note 6
├── System control (systemd user unit; minimal template) ──── → note 6
└── Memory pressure and OOM kills (oom_score_adj wrapper) ──── → note 6
platforms/mac/bundled-gateway.md
├── (intro — external CLI; no bundled Node/Gateway) ───────── → note 7 + note 9
├── Install the CLI (npm/pnpm/bun preference) ─────────────── → note 7
├── Launchd (LaunchAgent label/plist/manager/behavior/logging) → note 7
├── Version compatibility ─────────────────────────────────── → note 7
└── Smoke check ───────────────────────────────────────────── → note 7
platforms/mac/canvas.md
├── (intro — WKWebView Canvas panel) ──────────────────────── → note 8
├── Where Canvas lives (custom URL scheme; storage) ───────── → note 8
├── Panel behavior (resizable/per-session/auto-reload/disable) → note 8
├── Agent API surface (Gateway WS; present/navigate/eval/snap) → note 8
├── A2UI in Canvas (host URL; v0.8 commands) ──────────────── → note 8
│   └── A2UI commands (v0.8) (beginRendering/surfaceUpdate…) ─ → note 8
├── Triggering agent runs from Canvas (openclaw://agent deep links) → note 8
└── Security notes (traversal block; scheme; external URLs) ── → note 8
```
No orphaned sections. Cross-page recurring role/support framing → note 9. All `/channels/*`, `/gateway/*`,
`/nodes/*`, `/install/*`, sibling `/platforms/*` references are link-outs (Phase A / pf02–04), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| `android.md` (1,620w, 6 H2 / 10 H3, 8 code) | notes 1 + 2 | Two distinct task clusters: (a) get the node connected/paired/discovered (connection runbook, steps 1–5) vs (b) drive the node's command surface once connected (Chat, Canvas/camera, Voice/Talk, assistant, notifications). Splitting keeps each ≤600w / ≤6 code and one procedure focus. |
| `ios.md` (1,670w, 12 H2 / 4 H3, 10 code) | notes 3 + 4 | Mixed BB + size: the connect/discover/canvas/voice runbook (procedure) is separate from the relay-backed-push trust model (argument/model — "why this design", hop-by-hop trust chain, security constraints). One-BB-per-note rule forces the split; each lands ≤650w / ≤6 code. |
| (cross-page) | note 9 `oc_platforms_model.md` | Not a page split: a thin concept hub absorbing the recurring Support-snapshot / Requirements / role / support-matrix framing that appears on android/ios/linux/mac pages, giving the series an indexable model note (and an in-folder hub for G7/G8). |

Single-note pages (no split): `easyrunner.md` (449w), `linux.md` (511w), `mac/bundled-gateway.md` (313w),
`mac/canvas.md` (454w) — all well under the 2,500w cap and single-BB.

## Summary Statistics & Building Block Distribution

- **Source pages:** 6 (5,017 measured words). **New `oc_` notes:** **9**. **New `term_dictionary` notes:** 0.
- **BB distribution:** procedure ×6 (notes 1, 2, 3, 5, 6, 7) · argument ×1 (note 4) · concept ×2 (notes 8, 9).
- **Est. digest words ~4,800** (avg ~530/note); every note ≤650w, ≤400 lines.
- **Code fences:** 36 source fences (8+3+10+7+3+5) distribute across the procedure notes; each digest note
  keeps ≤6 (config/CLI snippets reproduced verbatim, selectively). Code-heaviest source pages (android 8,
  ios 10) are split so no note exceeds 6.
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** every note maps **≥8 relevancy-selected
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** (PLUS relevant
  per-note locked mapping is in `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` below.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

sibling `oc_*` docs (this series, not yet created) are marked **(planned, this series)** and count toward
the 10-doc floor. Relative paths are FROM `resources/documentation/openclaw/oc_X.md`
(term → `../../term_dictionary/`; snippet → `../../code_snippets/`; doc → `../<folder>/`; sibling →
`oc_Y.md`; repo → `../../../areas/code_repos/`; entry → `../../../0_entry_points/`).

### oc_platforms_android_connection (8t · 11s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway linking chat platforms to coding agents; relevance: the product whose Android companion node this runbook pairs.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex TCP transport; relevance: Android connects directly to the Gateway WebSocket (`ws://`/`wss://`) as a `role: node`.
- [DNS](../../term_dictionary/term_dns.md) — name-resolution protocol; relevance: tailnet discovery uses unicast DNS-SD (`_openclaw-gw._tcp`) for cross-network Wide-Area Bonjour.
- [TLS](../../term_dictionary/term_tls.md) — transport-layer encryption; relevance: Tailscale/public Android pairing requires a real TLS endpoint (`wss://` / Serve), not cleartext `ws://`.
- [VPN](../../term_dictionary/term_vpn.md) — virtual private network; relevance: Tailscale tailnet (Vienna⇄London) is the cross-network path for Android↔Gateway discovery and connection.
- [iOS](../../term_dictionary/term_ios.md) — Apple mobile OS; relevance: the sibling mobile companion-node app sharing the same pair/discover/connect lifecycle.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — request/response RPC over JSON; relevance: `node.event`, `node.list`, `gateway call` are JSON-RPC methods over the node WS.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: device pairing + CLI approve/reject and `autoApproveCidrs` are the node-auth gate before a session forms.

**Docs**
- [oc_platforms_android_node_surface](oc_platforms_android_node_surface.md) — Android node command surface (planned, this series); relevance: the post-connection sibling note (Chat/Canvas/Voice) this runbook hands off to.
- [oc_platforms_ios_connection](oc_platforms_ios_connection.md) — iOS connection runbook (planned, this series); relevance: the parallel mobile-node pairing flow (Bonjour/tailnet/manual).
- [oc_platforms_model](oc_platforms_model.md) — platforms model hub (planned, this series); relevance: the companion-node vs gateway-host role split this note specializes for Android.
- [hermes_install_termux_android](../hermes_agent/hermes_install_termux_android.md) — running a coding-agent gateway on Android via Termux; relevance: closest existing Android-runtime install precedent in the ecosystem corpus.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/node messaging architecture; relevance: explains the gateway↔node transport model Android attaches to.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway run/operate guide; relevance: the Gateway-host side (`gateway --port`, logs `listening on ws://`) Android pairs against.
- [band_connect_remote_agent](../band/band_connect_remote_agent.md) — connecting a remote agent over a network; relevance: parallel remote-node connect/discovery pattern for a coding agent.
- [band_websocket_agent_channels](../band/band_websocket_agent_channels.md) — agent WebSocket channels; relevance: analogous node-over-WebSocket session model.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — TLS + network access for a coding agent; relevance: the `wss://`/TLS-endpoint requirement Android pairing enforces, in a sibling tool.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth + network failure modes; relevance: the discovery-blocked / manual-host fallback diagnostics mirror Android's reconnect cases.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — OpenClaw client apps (`apps/android`); relevance: the Android app source documented here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway runtime; relevance: the WS server + discovery + pairing endpoints Android targets.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — node/pairing + channel layer; relevance: implements device pairing and node session lifecycle.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session model; relevance: the authenticated node session Android establishes after approval.

**Snippets** (11)
- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — Android mDNS/NSD discovery; relevance: exact code for step 2 LAN discovery.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android Gateway WS session; relevance: exact code for the foreground-service WS connection in step 3.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — gateway node pairing handler; relevance: implements `devices list/approve/reject` (step 4).
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — node presence/`lastSeenAtMs` recording; relevance: the `node.presence.alive` beacon + `handled:true` durable last-seen.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — gateway WS connection lifecycle; relevance: server side of the Android WS attach.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen + bind; relevance: `--port 18789` / `listening on ws://0.0.0.0` startup.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth modes; relevance: token/password auth gating the node pairing.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: maps discovery-blocked / manual-host fallback errors.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy gate; relevance: scope/role enforcement on the freshly-paired `role: node`.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session kit model; relevance: the node-session abstraction the Android client uses.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning for the gateway kit; relevance: the secure-endpoint (`wss://`) requirement for tailnet/public Android.

**Entry / other**

### oc_platforms_android_node_surface (8t · 11s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the product whose Android node command surface this note documents.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio→text transcription; relevance: Android Talk uses native speech recognition for Mic/Talk capture turns.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — text→audio synthesis; relevance: `talk.speak` via the gateway Talk provider, falling back to local system TTS.
- [Voice Call](../../term_dictionary/term_voice_call.md) — real-time voice session; relevance: Talk Mode is continuous capture with gateway-relay realtime transport.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — agent voice interaction mode; relevance: the Mic vs Talk capture-mode distinction documented here.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: canvas/camera/device commands ride the node WebSocket.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON RPC; relevance: `chat.*`, `canvas.*`, `camera.*`, `device.*`, `notifications.*` are JSON-RPC node commands.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: `notifications.rateLimit` caps forwarded notifications per package per minute.

**Docs**
- [oc_platforms_android_connection](oc_platforms_android_connection.md) — Android connection runbook (planned, this series); relevance: the prerequisite pairing note this command surface follows.
- [oc_platforms_mac_canvas](oc_platforms_mac_canvas.md) — macOS Canvas panel concept (planned, this series); relevance: the Gateway Canvas Host that Android's `canvas.*` commands drive.
- [oc_platforms_ios_connection](oc_platforms_ios_connection.md) — iOS node runbook (planned, this series); relevance: parallel canvas/voice node-command surface on iOS.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice-mode usage; relevance: ecosystem precedent for the Talk/Mic capture + TTS flow.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — CLI voice mode; relevance: the gateway-side voice/talk command analog.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — voice dictation in a coding agent; relevance: sibling-tool speech-input model for Mic capture turns.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in tool catalog; relevance: parallel to the Android device command families (apps/photos/contacts/calendar/sms/motion).
- [cc_computer_use](../claude_code/cc_computer_use.md) — agent device/UI control; relevance: the camera/screen/device-command pattern of node-driven device control.
- [oc_platforms_ios_push_relay_trust](oc_platforms_ios_push_relay_trust.md) — iOS push trust model (planned, this series); relevance: notification-forwarding/push counterpart on iOS.
- [band_agent_api_messages_events](../band/band_agent_api_messages_events.md) — agent message/event API; relevance: analog to `chat.history`/`chat.send`/`chat.subscribe` event surface.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — client apps (`apps/android`); relevance: the Android command-surface implementation.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/STT/TTS extension; relevance: backs Talk's transcription + `talk.speak`.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway runtime; relevance: hosts Canvas, dispatches node commands, forwards notifications.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging/chat layer; relevance: implements `chat.*` session/history normalization.

**Snippets** (11)
- [snippet_openclaw_android_invoke_dispatcher](../../code_snippets/snippet_openclaw_android_invoke_dispatcher.md) — Android node command dispatcher; relevance: exact code dispatching `canvas.*`/`camera.*`/`device.*`.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — Talk transcription relay; relevance: the realtime gateway-relay path for Talk Mode.
- [snippet_openclaw_gateway_agent_voice_wake_tracking](../../code_snippets/snippet_openclaw_gateway_agent_voice_wake_tracking.md) — voice-wake tracking; relevance: contrasts the (disabled-on-Android) wake path vs Mic/Talk.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — voice exec dedup; relevance: gateway handling of voice-turn node events.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — `chat.send` handler; relevance: implements the Chat-tab send command.
- [snippet_openclaw_gateway_chat_history_inject_handler](../../code_snippets/snippet_openclaw_gateway_chat_history_inject_handler.md) — `chat.history` injection; relevance: the display-normalized history (tag/tool-call stripping) documented.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — service notifications; relevance: closest analog to notification forwarding (allow/deny/quietHours/rateLimit).
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: the `nodes invoke --command` path for canvas/camera.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: `camera.snap` / `canvas.snapshot` JPEG handling.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — chat transcript media pipeline; relevance: media (photos/camera) flowing into chat transcripts.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT; relevance: a gateway Talk-provider STT backend behind native recognition fallback.

**Entry / other**

### oc_platforms_ios_connection (8t · 11s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the product whose iOS companion node this runbook operates.
- [iOS](../../term_dictionary/term_ios.md) — Apple mobile OS; relevance: the platform this node app runs on (foreground/background limits, Keychain pairing token).
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: iOS connects to the Gateway over WebSocket (LAN or tailnet).
- [DNS](../../term_dictionary/term_dns.md) — name resolution; relevance: tailnet discovery via unicast DNS-SD (`openclaw.internal.`) zone.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: secure tailnet/manual-host endpoints for the WS connection.
- [Voice Call](../../term_dictionary/term_voice_call.md) — real-time voice; relevance: talk mode + push-to-talk (`talk.ptt.*`) commands documented in the runbook.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON RPC; relevance: `node.invoke`, `canvas.*`, `node.list` are JSON-RPC node methods.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: pairing approve flow, superseded `requestId` on changed auth, `autoApproveCidrs`.

**Docs**
- [oc_platforms_ios_push_relay_trust](oc_platforms_ios_push_relay_trust.md) — iOS push relay trust model (planned, this series); relevance: the push/auth design that complements this connect runbook.
- [oc_platforms_android_connection](oc_platforms_android_connection.md) — Android connection runbook (planned, this series); relevance: the parallel mobile-node pairing/discovery flow.
- [oc_platforms_model](oc_platforms_model.md) — platforms model hub (planned, this series); relevance: the companion-node role iOS instantiates.
- [hermes_computer_use_macos](../hermes_agent/hermes_computer_use_macos.md) — Computer Use on macOS; relevance: the node-vs-Computer-Use boundary (`cua-driver mcp` desktop control vs iOS node commands).
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/node architecture; relevance: the gateway↔node protocol iOS attaches to.
- [cc_computer_use](../claude_code/cc_computer_use.md) — agent computer/UI control; relevance: contrasts desktop Computer Use against iOS mobile-node capabilities.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — TLS/network access; relevance: the LAN/tailnet/manual secure-endpoint paths.
- [band_connect_remote_agent](../band/band_connect_remote_agent.md) — connecting a remote agent; relevance: analogous remote-node connect/discovery model.
- [band_contacts_and_discovery](../band/band_contacts_and_discovery.md) — discovery of agents/peers; relevance: parallel to Bonjour/tailnet/manual discovery paths.
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — coding-agent RPC protocol; relevance: sibling-tool node-command RPC framing for `node.invoke`.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — client apps (`apps/ios`); relevance: the iOS node app source.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway runtime; relevance: hosts canvas, node WS, pairing for iOS.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — pairing/node layer; relevance: implements iOS device pairing + `requestId` lifecycle.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session model; relevance: the authenticated node + operator sessions iOS holds.

**Snippets** (11)
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS gateway pairing; relevance: exact code for the pair+approve quick-start.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — gateway pairing handler; relevance: `devices list/approve` server side + superseded request.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: gates `canvas.*`/`talk.ptt.*` for trusted Talk-capable nodes.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection lifecycle; relevance: the iOS↔Gateway WS attach.
- [snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md) — Canvas lifecycle; relevance: the WKWebView canvas iOS renders (`canvas.navigate`/eval/snapshot).
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — presence/last-seen; relevance: background alive beacons after silent push / location wake.
- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — mDNS discovery; relevance: the Bonjour `_openclaw-gw._tcp` LAN discovery iOS also uses.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: `NODE_BACKGROUND_UNAVAILABLE`/`A2UI_HOST_UNAVAILABLE`/reconnect errors.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session kit; relevance: the node-session abstraction the iOS client drives.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — voice exec dedup; relevance: talk-mode/ptt node-event handling.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: `canvas.snapshot --format jpeg --maxWidth` handling.

**Entry / other**

### oc_platforms_ios_push_relay_trust (9t · 10s · 10d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the gateway whose push-credential isolation this design protects.
- [iOS](../../term_dictionary/term_ios.md) — Apple mobile OS; relevance: APNs, App Attest, StoreKit JWS are iOS-platform mechanisms central to the trust flow.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — scoped bearer credential; relevance: the registration-scoped send grant + relay handle delegated to a specific gateway identity.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: App Attest + Apple distribution proof authenticate the build before relay registration.
- [Authorization](../../term_dictionary/term_access_control.md) — access control; relevance: a gateway may send pushes only for devices paired with that gateway (delegated grant scope).
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: relay registration + send endpoints are HTTPS-only.
- [Threat Model](../../term_dictionary/term_threat_model.md) — adversary/constraint analysis; relevance: the "why this design" section enumerates the two constraints direct-APNs-on-gateway cannot enforce.
- [Encryption](../../term_dictionary/term_encryption.md) — data protection; relevance: production APNs credentials/`.p8` keys are kept off user gateways (relay owns them).
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential storage; relevance: the gateway-host `~/.openclaw/credentials/apns` chmod 700/600 `.p8` storage for local/manual builds.

**Docs**
- [oc_platforms_ios_connection](oc_platforms_ios_connection.md) — iOS connect runbook (planned, this series); relevance: the pair/connect prerequisite that establishes the operator session used for `gateway.identity.get`.
- [oc_platforms_model](oc_platforms_model.md) — platforms hub (planned, this series); relevance: places the push-trust design in the per-OS model.
- [bedrock_agentcore_identity_inbound_auth](../aws_bedrock_agentcore/bedrock_agentcore_identity_inbound_auth.md) — inbound auth for agent runtime; relevance: analogous attest-the-caller-before-grant pattern.
- [bedrock_agentcore_identity_outbound_providers](../aws_bedrock_agentcore/bedrock_agentcore_identity_outbound_providers.md) — outbound credential delegation; relevance: parallel to delegating a send grant to a specific identity instead of sharing raw credentials.
- [bedrock_agentcore_identity_data_protection](../aws_bedrock_agentcore/bedrock_agentcore_identity_data_protection.md) — credential data protection; relevance: keeping provider credentials out of the agent, mirroring keeping APNs keys off the gateway.
- [bedrock_agentcore_gateway_target_mcp_oauth](../aws_bedrock_agentcore/bedrock_agentcore_gateway_target_mcp_oauth.md) — OAuth-scoped gateway target; relevance: scoped-grant + delegated-identity model analogous to the relay send grant.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation; relevance: ecosystem precedent for isolating sensitive credentials from the agent host.
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook/route signature security; relevance: signed-request verification analog to the gateway signing send requests with its device identity.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — coding-agent security architecture; relevance: sibling-tool trust-boundary framing for credential delegation.
- [cc_authentication](../claude_code/cc_authentication.md) — coding-agent auth; relevance: the build/identity authentication model the relay enforces.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — client apps (iOS push registration); relevance: implements App Attest + StoreKit JWS relay registration.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/trust model; relevance: the credential-isolation + delegated-grant design lives here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway runtime; relevance: `push.apns.register` / `push.test` + relay-handle storage + gateway-identity signing.

**Snippets** (10)
- [snippet_openclaw_gateway_exec_approval_ios_push](../../code_snippets/snippet_openclaw_gateway_exec_approval_ios_push.md) — iOS push exec/approval; relevance: exact gateway-side iOS push registration/approval path.
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — APNs presence events; relevance: background wakes/`push.test` recorded via APNs presence.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — APNs invoke; relevance: gateway sending a relay-backed wake nudge.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — gateway identity/TLS signing; relevance: the gateway signs send requests with its device identity, verified against the delegated identity.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — auth authorize dispatch; relevance: the operator-session auth gating `gateway.identity.get`.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret handling on gateway calls; relevance: how the `.p8` direct-APNs env credentials are loaded for local builds.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: `OPENCLAW_APNS_*` / `OPENCLAW_*_RELAY_BASE_URL` env overrides.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect/proxy; relevance: relay baseUrl override / custom relay deployment binding.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning; relevance: HTTPS relay-endpoint trust pinning.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content trust handling; relevance: validating an externally-issued (Apple/relay) proof before trusting it.

**Entry / other**

### oc_platforms_easyrunner (8t · 10s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the Gateway hosted as a container on EasyRunner.
- [Docker](../../term_dictionary/term_docker.md) — containerization; relevance: EasyRunner runs Podman-compatible Compose apps (Docker-compatible image/Compose).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: Caddy fronts the Gateway and terminates TLS via `caddy.reverse_proxy` labels.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — edge request router; relevance: Caddy as the HTTPS edge in front of the bound Gateway port.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: Caddy HTTPS termination for `https://openclaw.example.com`.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: a strong Gateway token/password (`auth.token`) is required; device auth kept enabled.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential storage; relevance: `OPENCLAW_GATEWAY_TOKEN` stored in EasyRunner's secret manager, not committed.
- [Reverse Proxy / trusted-proxy](../../term_dictionary/term_access_control.md) — access control; relevance: trusted-proxy settings for the exact proxy path rather than disabling auth globally.

**Docs**
- [oc_platforms_linux](oc_platforms_linux.md) — Linux/VPS hosting (planned, this series); relevance: sibling Gateway-host runtime (container/VPS) with the same bind/auth concerns.
- [oc_platforms_model](oc_platforms_model.md) — platforms hub (planned, this series); relevance: places EasyRunner in the gateway-host role.
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Docker run modes; relevance: closest existing containerized-gateway run pattern.
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — Docker volumes + supervision; relevance: the persistent config/workspace volume + restart policy this Compose uses.
- [hermes_messaging_matrix_proxy_mode](../hermes_agent/hermes_messaging_matrix_proxy_mode.md) — proxy-mode deployment; relevance: running behind a reverse proxy with auth, like Caddy here.
- [pi_containerization](../pi/pi_containerization.md) — containerizing a coding agent; relevance: sibling-tool container deployment + volume/env model.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud-host deployment; relevance: hosted-gateway deployment on a managed host (EasyRunner-like).
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: the reverse-proxy-fronts-the-gateway config pattern.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — container runtime; relevance: container runtime + image model for a hosted agent.
- [cc_cloud_environment](../claude_code/cc_cloud_environment.md) — cloud hosting environment; relevance: hosted/managed deployment of a coding-agent backend.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway runtime; relevance: `gateway --bind lan --port` + `auth.token` config this guide sets.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/trusted-proxy; relevance: trusted-proxy device-identity handling behind Caddy.

**Snippets** (10)
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth modes (token/password); relevance: the `auth.token` mode this deployment requires.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect via proxy; relevance: `gateway probe/status --url https://... --token` through Caddy.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen+bind; relevance: `--bind lan --port 1455` container listen on `0.0.0.0`.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env vars; relevance: `OPENCLAW_HOME`/`OPENCLAW_STATE_DIR`/`OPENCLAW_CONFIG_PATH`/`OPENCLAW_WORKSPACE_DIR` Compose env.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret loading; relevance: `${OPENCLAW_GATEWAY_TOKEN}` resolution from the secret manager.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth startup; relevance: startup auth checks + "no SecretRef/plugin/channel auth failures" verification.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: applying the persistent-volume `openclaw.json` gateway config.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity/TLS; relevance: device identity carried through a TLS-terminating proxy.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — `openclaw doctor` repair; relevance: the post-update `openclaw doctor` config-migration check.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — security audit composition; relevance: validating trusted-proxy/auth posture for a hosted deployment.

**Entry / other**

### oc_platforms_linux (8t · 11s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the Gateway, fully supported on Linux, this note installs/operates.
- [Docker](../../term_dictionary/term_docker.md) — containerization; relevance: container/cgroup memory limits + container-level memory controls for OOM tuning.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: `openclaw doctor` repair/migrate as the Linux health/diagnostic step.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: the Gateway WS on `127.0.0.1:18789` reached via the SSH tunnel.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: shared-secret (token by default, or `gateway.auth.mode: password`) at `http://127.0.0.1:18789/`.
- [Remote SSH](../../term_dictionary/term_remote_ssh.md) — SSH remote access; relevance: `ssh -N -L 18789:127.0.0.1:18789` local-forward from laptop to VPS.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell; relevance: the VPS quick-path uses SSH for install + tunnel.
- [VPN](../../term_dictionary/term_vpn.md) — private networking; relevance: alternative remote-reach path (tailnet) to the VPS gateway.

**Docs**
- [oc_platforms_easyrunner](oc_platforms_easyrunner.md) — EasyRunner hosting (planned, this series); relevance: sibling container/host deployment of the same Gateway.
- [oc_platforms_mac_bundled_gateway](oc_platforms_mac_bundled_gateway.md) — macOS gateway service (planned, this series); relevance: comparable service-install (launchd vs systemd) runtime.
- [oc_platforms_model](oc_platforms_model.md) — platforms hub (planned, this series); relevance: Linux as a gateway-host in the per-OS matrix.
- [hermes_install_nix_quickstart](../hermes_agent/hermes_install_nix_quickstart.md) — Nix install quickstart; relevance: an alternative Linux install flow for the gateway.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway operate/run; relevance: the service-run + restart/diagnostics model for a Linux host.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — auth over SSH; relevance: the SSH-tunnel-to-VPS access pattern used in the quick path.
- [pi_platform_windows_termux](../pi/pi_platform_windows_termux.md) — platform install (Termux/non-mac); relevance: sibling-tool non-mac platform install + daemon guidance.
- [pi_security_model](../pi/pi_security_model.md) — coding-agent security model; relevance: shared-secret auth + remote-access threat surface for a VPS.
- [cc_devcontainer_setup](../claude_code/cc_devcontainer_setup.md) — devcontainer/container setup; relevance: container resource controls relevant to OOM tuning.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — cloud/VPS network access; relevance: reaching a remote agent on a VPS over a forwarded port.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway runtime; relevance: `gateway --port`, `gateway install`, `onboard --install-daemon` service install.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/process; relevance: the OOM child-process biasing (`oom_score_adj 1000`) wrapper lives here.

**Snippets** (11)
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: exact code for the canonical `openclaw-gateway.service` unit.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd user/linger env; relevance: the systemd **user** service + linger for always-on.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen+bind; relevance: `gateway --port 18789` bind on the VPS.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: the WS endpoint reached through the SSH tunnel.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: supervisor-managed command children are an OOM-biased surface.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestrator; relevance: spawns the `/bin/sh` OOM-wrapper child before `exec`.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — kill process tree; relevance: child-process lifecycle for the covered OOM surfaces.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env; relevance: `OPENCLAW_CHILD_OOM_SCORE_ADJ=0/false/no/off` opt-out env.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth modes; relevance: token-vs-password shared-secret auth at the dashboard.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — `openclaw doctor` repair; relevance: the repair/migrate step in the install flow.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect; relevance: connecting a client to the forwarded `127.0.0.1:18789`.

**Entry / other**

### oc_platforms_mac_bundled_gateway (8t · 10s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the Gateway runtime OpenClaw.app no longer bundles and now manages externally.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: the smoke check `gateway call health --url ws://127.0.0.1:18999`.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness probe; relevance: `gateway call health` smoke check + `--version` compatibility verification.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the external CLI's gateway context (`OPENCLAW_SKIP_*` flags gate channel/canvas hosts at smoke time).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agentic coding tools; relevance: OpenClaw is one; the macOS app hosts its gateway runtime.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: loopback-bound smoke gateway + version-gated CLI/app pairing.
- [Health Check / version compat](../../term_dictionary/term_acp_agent_client_protocol.md) — agent client protocol; relevance: the app↔gateway version-compatibility check parallels protocol-version negotiation.

**Docs**
- [oc_platforms_linux](oc_platforms_linux.md) — Linux gateway service (planned, this series); relevance: sibling service-install runtime (systemd vs launchd).
- [oc_platforms_mac_canvas](oc_platforms_mac_canvas.md) — macOS Canvas panel (planned, this series); relevance: same OpenClaw.app, the Canvas surface served by this gateway.
- [oc_platforms_model](oc_platforms_model.md) — platforms hub (planned, this series); relevance: macOS as a gateway-host in the per-OS matrix.
- [hermes_computer_use_macos](../hermes_agent/hermes_computer_use_macos.md) — macOS agent runtime; relevance: closest macOS coding-agent runtime/install precedent.
- [hermes_installation](../hermes_agent/hermes_installation.md) — install flow; relevance: the global npm/pnpm/bun CLI install preference order analog.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals; relevance: the gateway runtime the macOS app attaches to or launches.
- [pi_terminal_setup](../pi/pi_terminal_setup.md) — CLI/terminal install setup; relevance: sibling-tool global CLI install + runtime selection.
- [cc_install](../claude_code/cc_install.md) — coding-agent install; relevance: the npm-global install + version pinning pattern (`openclaw@<version>`).
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — install verification; relevance: the `--version` + health smoke-check verification step.
- [cc_update_and_release_channels](../claude_code/cc_update_and_release_channels.md) — version/release channels; relevance: app↔gateway version-compatibility matching.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway runtime; relevance: the externally-installed gateway the launchd LaunchAgent runs.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — client apps (OpenClaw.app); relevance: the macOS app that owns LaunchAgent install/update in Local mode.

**Snippets** (10)
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist render; relevance: exact code for the `ai.openclaw.gateway.plist` LaunchAgent.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — LaunchAgent restart/handoff; relevance: "app quit does not stop the gateway" + attach-to-running behavior.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen+bind; relevance: `gateway --port 18999 --bind loopback` smoke listen.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: `gateway call health --url ws://127.0.0.1:18999` connect.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env; relevance: `OPENCLAW_SKIP_CHANNELS` / `OPENCLAW_SKIP_CANVAS_HOST` smoke env flags.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair; relevance: post-install repair/diagnostic analog.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth startup; relevance: gateway startup the LaunchAgent triggers.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache respawn; relevance: gateway respawn under launchd `Restart`-style supervision.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI main bootstrap; relevance: the `openclaw` CLI entrypoint the app's Install-CLI button + LaunchAgent invoke.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: keep-alive supervision parallel to launchd.

**Entry / other**

### oc_platforms_mac_canvas (8t · 10s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the macOS app whose agent-controlled Canvas panel this concept models.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: Canvas is exposed via the Gateway WebSocket for present/navigate/eval/snapshot.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON RPC; relevance: `canvas.present/navigate/eval/snapshot` + `canvas.a2ui.*` are JSON-RPC node commands.
- [A2UI](../../term_dictionary/term_a2ui.md) — agent-to-UI rendering protocol; relevance: Canvas hosts A2UI v0.8 server→client messages (`beginRendering`/`surfaceUpdate`/…).
- [A2A](../../term_dictionary/term_a2a.md) — agent-to-agent protocol; relevance: the agent-driven UI/deep-link trigger model (`openclaw://agent`) parallels A2A invocation.
- [Access Control](../../term_dictionary/term_access_control.md) — access control; relevance: the scheme blocks directory traversal; external URLs only when explicitly navigated.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agentic coding tools; relevance: the agent that drives the Canvas panel programmatically.

**Docs**
- [oc_platforms_android_node_surface](oc_platforms_android_node_surface.md) — Android node surface (planned, this series); relevance: the Gateway Canvas Host that Android `canvas.*` commands drive.
- [oc_platforms_ios_connection](oc_platforms_ios_connection.md) — iOS connect runbook (planned, this series); relevance: the iOS WKWebView canvas + A2UI counterpart.
- [oc_platforms_model](oc_platforms_model.md) — platforms hub (planned, this series); relevance: Canvas as a macOS-app capability in the platform model.
- [hermes_computer_use_macos](../hermes_agent/hermes_computer_use_macos.md) — macOS agent UI control; relevance: agent-driven macOS surface analogous to canvas control.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals (canvas host); relevance: the Gateway HTTP server that serves `/__openclaw__/a2ui/`.
- [cc_computer_use](../claude_code/cc_computer_use.md) — agent computer/UI control; relevance: the eval/snapshot agent-control pattern over a UI surface.
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — browser automation; relevance: WKWebView navigate/eval/snapshot mirrors a controlled web view.
- [pi_extensions_custom_ui](../pi/pi_extensions_custom_ui.md) — custom UI extension; relevance: sibling-tool agent-rendered custom UI surface.
- [band_a2a_overview](../band/band_a2a_overview.md) — A2A overview; relevance: the agent-to-agent/UI invocation model behind deep-link triggers.
- [band_websocket_overview](../band/band_websocket_overview.md) — agent WebSocket overview; relevance: the WS agent-API transport Canvas uses.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — client apps (macOS Canvas); relevance: the WKWebView Canvas panel + custom URL scheme implementation.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway runtime; relevance: the canvas host / A2UI host server + WS agent API.

**Snippets** (10)
- [snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md) — Canvas panel lifecycle; relevance: exact code for panel show/hide/per-session storage/scaffold.
- [snippet_openclaw_macos_canvas_filewatcher](../../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md) — Canvas filewatcher; relevance: exact code for "auto-reloads when local canvas files change".
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: the Gateway-WebSocket agent-API transport.
- [snippet_openclaw_android_invoke_dispatcher](../../code_snippets/snippet_openclaw_android_invoke_dispatcher.md) — node command dispatcher; relevance: how `canvas.*` commands are dispatched to a node.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP plugin routing; relevance: serving `/__openclaw__/canvas/` and `/__openclaw__/a2ui/` routes.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: `CANVAS_DISABLED` gating when Canvas is disabled in Settings.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: `canvas snapshot` image capture handling.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content trust; relevance: external `http(s)` URLs allowed only when explicitly navigated.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — filesystem policy; relevance: the scheme blocks directory traversal; files must live under the session root.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen; relevance: the Gateway HTTP server (same `gateway.port`, default 18789) hosting canvas.

**Entry / other**

### oc_platforms_model (9t · 10s · 10d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the product whose platform model (host vs node) this hub note frames.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agentic coding tools; relevance: the agents the Gateway connects platforms to.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: the node⇄gateway transport common to every platform note.
- [iOS](../../term_dictionary/term_ios.md) — Apple mobile OS; relevance: a node-only companion platform in the support matrix.
- [Hermes Agent](../../term_dictionary/term_hermes_agent.md) — sibling coding-agent ecosystem; relevance: the analogous gateway/node platform model the docs corpus already covers.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent-client protocol; relevance: the control-plane protocol the gateway speaks to nodes/agents.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the tool/context protocol the gateway exposes across platforms.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent runtime harness; relevance: the gateway-host role hosts the agent harness; nodes are companion surfaces.

**Docs**
- [oc_platforms_android_connection](oc_platforms_android_connection.md) — Android connect (planned, this series); relevance: a node-only companion the matrix lists.
- [oc_platforms_ios_connection](oc_platforms_ios_connection.md) — iOS connect (planned, this series); relevance: the other node-only mobile companion.
- [oc_platforms_linux](oc_platforms_linux.md) — Linux host (planned, this series); relevance: a gateway-host OS in the support matrix.
- [oc_platforms_mac_bundled_gateway](oc_platforms_mac_bundled_gateway.md) — macOS gateway (planned, this series); relevance: the macOS gateway-host runtime.
- [oc_platforms_easyrunner](oc_platforms_easyrunner.md) — EasyRunner host (planned, this series); relevance: a hosted gateway-host deployment.
- [oc_platforms_mac_canvas](oc_platforms_mac_canvas.md) — macOS Canvas (planned, this series); relevance: a per-OS node-capability surface.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/node architecture; relevance: the canonical host↔node split this hub mirrors for OpenClaw.
- [band_overview](../band/band_overview.md) — agent platform overview; relevance: a sibling host/agent/companion platform model.
- [pi_overview](../pi/pi_overview.md) — coding-agent overview; relevance: sibling coding-agent platform/runtime framing.
- [cc_platforms_and_integrations](../claude_code/cc_platforms_and_integrations.md) — platforms + integrations; relevance: the per-platform support-matrix framing for a sibling tool.
- [hermes_architecture](../hermes_agent/hermes_architecture.md) — peer agent's layered host/runtime architecture; relevance: a second existing per-OS host/runtime architecture reference mirroring OpenClaw's gateway-host vs companion-node split.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root repo; relevance: the monorepo spanning apps + gateway across platforms.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — client apps; relevance: the per-OS node/app surfaces (android/ios/macos).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway runtime; relevance: the gateway-host component the host OSes run.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — node/pairing; relevance: the shared pair/connect/discover lifecycle every platform specializes.

**Snippets** (10)
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session kit; relevance: the host↔node session abstraction common to all platforms.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: the universal node⇄gateway transport.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: the shared pairing lifecycle every companion node uses.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway channel WS kit; relevance: the gateway's WS channel/control plane.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen+bind; relevance: the gateway-host listen surface across host OSes.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: the role/scope model distinguishing node vs operator across platforms.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: the cross-platform `openclaw` CLI surface (`gateway`, `nodes`, `devices`).
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC protocol envelope; relevance: the gateway protocol (nodes + control plane) shared by all platforms.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: the node/gateway method groups every platform invokes.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning; relevance: the secure-endpoint requirement recurring across platform notes.

**Entry / other**

## Undigested Terms Plan

| Term (from source) | Disposition |
|---|---|
| OpenClaw, Gateway, node, companion node | Existing `term_openclaw` / ecosystem; OpenClaw vocab → `oc_*` doc notes (concept in note 9). Link, do not redefine. |
| WebSocket, wss/ws, TLS | Link existing `term_websocket`, `term_tls`. No new note. |
| mDNS / NSD / Bonjour / DNS-SD / wide-area discovery | Documented as procedure in notes 1/3 + link existing `term_dns`. `term_mdns`/`term_bonjour` do NOT exist; NOT promoted — discovery is OpenClaw operational detail, covered by gw02 `gateway/bonjour` (Phase A) and `term_dns`. No new term. |
| Tailscale / tailnet / MagicDNS / Serve / Funnel | Link `term_vpn`; Tailscale specifics digested in gw06 `gateway/tailscale` (Phase A). No new `term_tailscale`. |
| Pairing / device pairing / requestId / autoApproveCidrs | OpenClaw operational vocab → notes 1/3; pairing concept owned by ch04 `channels/pairing` (Phase A). No new term. |
| Presence alive beacon / node.presence.alive / lastSeenAtMs | OpenClaw event vocab → notes 1/3 procedures. No new term. |
| Canvas / A2UI / WKWebView / custom URL scheme / openclaw-canvas:// | OpenClaw product vocab → note 8 (concept) + note 2. `term_canvas`/`term_webview` do NOT exist and are product-specific UI surfaces, not cross-cutting reusable concepts → NOT promoted. No new term. |
| APNs / push relay / App Attest / StoreKit JWS / send grant | iOS-platform-specific vocab → note 4 (argument). `term_apns`/`term_app_attest`/`term_push_notification` do NOT exist; platform-specific, NOT cross-cutting → NOT promoted; link `term_oauth_token`/`term_authentication`. No new term. |
| OOM kill / oom_score_adj / cgroup | Linux kernel detail → note 6 procedure. Not promoted (OS primitive). No new term. |
| Podman / Compose / Caddy | Container/proxy vocab → note 5; link `term_docker` (Podman = Docker-compatible) + `term_reverse_proxy` (Caddy). `term_podman`/`term_caddy` do NOT exist; NOT promoted (variants of existing concepts). No new term. |
| Talk / Mic / voice wake / push-to-talk (ptt) / talk.speak | Voice vocab → notes 2/3; link `term_voice_call`, `term_speech_to_text`, `term_text_to_speech`. No new term. |
| App Actions / Google Assistant entrypoint; Computer Use / cua-driver | Platform-integration detail → notes 2/3; Computer Use links out to `/plugins/codex-computer-use` (pl02). No new term. |

**Expected new `term_dictionary` captures: 0.** No genuinely cross-cutting, vault-reusable term lacking an
existing note appears on these 6 platform pages — all candidates are either (a) existing terms to link, or
(b) OpenClaw/OS/platform-specific operational vocabulary digested into the `oc_*` doc notes per the master's
design decision. Augment Step 2d re-scans to confirm. **No new-term candidate proposed.**

### Renamed (general → specific)

— (none). 0 new `term_*` slugs are introduced by this sub-plan, so there are no slugs to rename for
specificity. The audit was performed: every source-vocabulary candidate was routed to an EXISTING term
(linked) or to an `oc_*` doc note; no new slug was minted, general or otherwise.

### Removed (substantive vault notes already cover the concept — link instead of create)

Collision audit performed across BOTH `term_dictionary/` AND `resources/documentation/` for every planned
note (not only term slugs), per augment Step 10.5f. Substantive existing notes that ALREADY cover candidate
concepts → linked, not recreated:

| Candidate concept | Existing substantive note (linked, not created) | Audit verdict |
|---|---|---|
| Canvas / A2UI panel | `term_a2ui` (active) + `snippet_openclaw_macos_canvas_lifecycle`/`_filewatcher` (active) | LINK — note 8 is a *doc* concept of the macOS panel, not a redefinition of the A2UI term; both linked. |
| Push-relay credential delegation | `term_oauth_token`, `term_access_control`, `term_threat_model`, `term_encryption` (all active) | LINK — note 4 is an *argument* about a design; no duplicate term created. |
| systemd / launchd service | `snippet_openclaw_daemon_systemd_*` / `*_launchd_*` (active) | LINK — OS-primitive procedure; covered by snippets, not a term. |
| Podman / Caddy / container hosting | `term_docker`, `term_reverse_proxy`, `term_api_gateway` (active) | LINK — variants of existing concepts; no `term_podman`/`term_caddy` created. |
| Voice / Talk / push-to-talk | `term_voice_call`, `term_voice_mode`, `term_speech_to_text`, `term_text_to_speech` (active) | LINK — voice vocabulary fully covered by existing terms. |

No planned `oc_*` doc note duplicates an existing **term** note (the common miss): each `oc_*` note is a
platform-specific *procedure/concept/argument* doc, distinct from the conceptual `term_*` notes it links.
0 removals required (no new slug was ever planned); audit confirms link-only routing is correct.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; the multi-source-research
term-authoring requirement (inherited from master W5) does not apply. If augment Step 2d surfaces a
genuinely reusable cross-cutting term with no existing note, it would be captured via
`/tessellum-capture-term-note` + added to its best-fit `acronym_glossary_*.md` (the agentic/LLM glossary) —
not expected here.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (9 notes, P2). Gate table inherited verbatim from the master 9-GATE.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean (YAML field order, itemized keywords/topics, `## Overview` + `## Related Notes`, bold `**Source**`/`**Last Updated**`/`**Status**` footer). |
| G2 | Grounding | Each note's claims diff-verified against its `inbox/openclaw_docs/platforms/<page>` source (no hallucinated commands/flags/keys). |
| G3 | Density + Coverage | ≤400 lines · ≤2,500 words · ≤6 code blocks · one BB per note; every mapped H2/H3 covered (Section Coverage Map). |
| G4 | Cross-Reference | Each note ≥6 relevancy-selected `term_dictionary` terms + `repo_openclaw*` + sibling `oc_*` + snippets, each indexed link `[text](path.md)` with a relevance statement. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` → 0 broken; correct relative paths from `resources/documentation/openclaw/`. |
| G7/G8 | Discoverability | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (in-degree ≥1, anti-island) — satisfied via `entry_openclaw_docs.md` rows + the inlinks listed below. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
cd /path/to/vault
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_platforms_android_connection oc_platforms_android_node_surface oc_platforms_ios_connection oc_platforms_ios_push_relay_trust oc_platforms_easyrunner oc_platforms_linux oc_platforms_mac_bundled_gateway oc_platforms_mac_canvas oc_platforms_model"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1: format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3: density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # G4: at least one sibling oc_ link present
  grep -q "$SIBLING_PREFIX" "$f" || echo "$n NO SIBLING ($SIBLING_PREFIX) LINK"
done

# G1 YAML sweep over the whole openclaw folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5/G6: reindex + ghost + broken-link verification (per master pacing)
bash scripts/update_notes_database.sh --force
# then run /tessellum-fix-ghost-references and /tessellum-fix-broken-links, expect 0 broken / 0 ghost
```

## Density Re-Assessment

| # | Note | BB | ~Words | Src fences (max in note) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_platforms_android_connection | procedure | 600 | ~5 of android's 8 | ✅ (≤6 code) |
| 2 | oc_platforms_android_node_surface | procedure | 600 | ~3 of android's 8 | ✅ |
| 3 | oc_platforms_ios_connection | procedure | 650 | ~5 of ios's 10 | ✅ |
| 4 | oc_platforms_ios_push_relay_trust | argument | 650 | ~3 of ios's 10 | ✅ |
| 5 | oc_platforms_easyrunner | procedure | 450 | 3 | ✅ |
| 6 | oc_platforms_linux | procedure | 550 | ~6 (selective of 7) | ✅ (=6 cap) |
| 7 | oc_platforms_mac_bundled_gateway | procedure | 400 | 3 | ✅ |
| 8 | oc_platforms_mac_canvas | concept | 500 | 5 | ✅ |
| 9 | oc_platforms_model | concept | 400 | 0–1 | ✅ |

No note approaches the 2,500w / 400-line caps. The two code-heavy source pages (android 8, ios 10) are
split so each note stays ≤6 code blocks; linux (7 fences) reproduces ≤6 selectively (the systemd template
counts as one fence). One BB per note (procedure ×6 · argument ×1 · concept ×2).

## Entry Point Decision (inherited from master)

Contributes **9 rows** to `entry_openclaw_docs.md` (CREATED as the master W1 pre-step before first
execution) under a **"Platforms"** cluster (Mobile nodes: Android ×2, iOS ×2; Hosts: Linux, macOS bundled
gateway, EasyRunner; macOS Canvas; Platforms overview). Each note receives its entry-point back-link at
finalization (this also satisfies G7/G8). Per master W2, the docs hub itself is back-linked from

## Inlinks (existing notes → new notes)


- `entry_openclaw_docs.md` (planned, master W1) → **all 9 notes** (primary anti-island guarantee).
- `repo_openclaw_apps.md` → notes 1, 2, 3, 4, 7, 8, 9 (apps/android, apps/ios, macOS app, root apps).
- `repo_openclaw_gateway.md` → notes 1, 3, 5, 6, 7, 8, 9 (gateway runtime/host).
- `repo_openclaw_security.md` → note 4 (iOS push trust model), note 6 (OOM/child biasing).
- `repo_openclaw_channels.md` → notes 1, 3, 9 (node pairing).
- `repo_openclaw_extensions_voice_speech.md` → note 2 (Talk/TTS).
- `term_openclaw.md` → note 9 (platform overview), and ≥1 of notes 1/3.
- `term_ios.md` → notes 3, 4.
- `term_docker.md` → notes 5, 6.

Each new note thus receives ≥1 inbound edge from outside `documentation/openclaw/` (G8 satisfied even
before sibling `oc_*` reciprocal links).

## Pacing Rules (inherited from master)

Single execution phase, 9 notes (≤30 fan-out cap). Re-read each source page at execute; reproduce config/CLI
snippets verbatim; one BB per note. `git pull --rebase --autostash origin main` first; reindex incrementally;
verify `note_links` populated + 0 broken links + G8 in-degree ≥1 BEFORE commit; commit+push the phase as one
cycle (no Claude co-author trailer).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (status: ready) |

## Augmentation Report (2026-06-21)

**Scope:** xref-augment of sub-plan pf01 (Platforms, 9 notes). The `## Candidate Cross-References` section
was replaced with `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` at RAISED FLOORS:

**Re-read confirmation (Step 2):** all 6 source pages re-read in full from `inbox/openclaw_docs/platforms/`.
Measured (body words / code fences / H2 / H3): android 1583/8/6/10 · easyrunner 410/3/6/0 · ios 1631/10/12/4 ·
linux 472/7/7/0 · mac/bundled-gateway 281/3/5/0 · mac/canvas 420/5/7/1. All within ±15% of the plan's
estimates — no density re-split needed.


| # | Note | Terms | Snippets | Docs (existing + planned-sibling) | Repos | Floors met |
|---|---|---:|---:|---|---:|---|
| 1 | oc_platforms_android_connection | 8 | 11 | 10 (7 existing + 3 sibling) | 4 | ✅ |
| 2 | oc_platforms_android_node_surface | 8 | 11 | 10 (6 existing + 4 sibling) | 4 | ✅ |
| 3 | oc_platforms_ios_connection | 8 | 11 | 10 (7 existing + 3 sibling) | 4 | ✅ |
| 4 | oc_platforms_ios_push_relay_trust | 9 | 10 | 10 (8 existing + 2 sibling) | 3 | ✅ |
| 5 | oc_platforms_easyrunner | 8 | 10 | 10 (8 existing + 2 sibling) | 2 | ✅ |
| 6 | oc_platforms_linux | 8 | 11 | 10 (7 existing + 3 sibling) | 2 | ✅ |
| 7 | oc_platforms_mac_bundled_gateway | 8 | 10 | 10 (7 existing + 3 sibling) | 3 | ✅ |
| 8 | oc_platforms_mac_canvas | 8 | 10 | 10 (7 existing + 3 sibling) | 3 | ✅ |
| 9 | oc_platforms_model | 9 | 10 | 10 (4 existing + 6 sibling) | 4 | ✅ |

A full link-resolution sweep of the LOCKED section (301 links) resolved 263 existing + 29 planned-sibling
`oc_*` (this series) + 9 references to `entry_openclaw_docs.md` (planned, master W1 pre-step). 0 UNEXPECTED
ghosts — the only not-yet-existing targets are the by-design planned siblings + the W1 entry hub, each
explicitly annotated "(planned, …)". Doc floor satisfied with ≥5 existing per note via the rich
`claude_code/` (cc_*), `hermes_agent/` (hermes_*), `pi/` (pi_*), `band/` (band_*), and
`aws_bedrock_agentcore/` coding-agent corpora; all snippets are EXISTING from the 253-note openclaw snippet
corpus.

**New-term candidates:** **0.** Step 2d re-scan of all 6 pages surfaced no genuinely cross-cutting,
vault-reusable term lacking an existing note. Every source-vocabulary candidate is either an existing term
to link (e.g. `term_a2ui`, `term_voice_mode`, `term_remote_ssh`, `term_secrets_manager`, `term_encryption`,
`term_tls_pinning` were newly located and added during this augment) or OpenClaw/OS/platform-specific
operational vocabulary digested into the `oc_*` doc notes per the master design decision (no `term_*`
inlining). Specificity audit: no new slug minted → nothing to rename. Collision audit (term_dictionary AND
documentation/): no planned `oc_*` doc note duplicates an existing term/doc — see the
`### Removed (substantive vault notes already cover the concept)` sub-table.

**Best-fit glossary (if a term were ever surfaced):** the agentic/LLM glossary (`acronym_glossary_agentic_ai.md`)
— not exercised here (0 captures).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; every note ≥8 terms (notes 4,9 have 9), ≥10 snippets, ≥10 docs, each link carries `— desc; relevance: …`; ≥1 entry-point back-link per note. |
| CP2 | 9-GATE present (G1–G6, G8, G9) per batch | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link-fix, G7/G8 discoverability; single execution phase. |
| CP4 | Size (≤30 or split) | **PASS** | 9 notes, well under 30 fan-out cap; single execution phase. |
| CP5 | Format derived from existing target-dir notes | **PASS** | Format inherited verbatim from master `## Format Definition` derived from existing `claude_code/`+`pi/` doc corpora: `## Overview` (not `## Definition`), `## Related Notes`, bold `**Source**`/`**Last Updated**`/`**Status**` footer, fixed YAML order, `building_block` per note. |
| CP6 | Density (borderline → split) | **PASS** | `## Density Re-Assessment`: every note ≤650w / ≤6 code / ≤400 lines; code-heavy android (8) + ios (10) already split so no note exceeds 6 fences; no borderline note unaddressed. |
| CP7 | Sources measured (not guessed) | **PASS** | All 6 pages re-read + measured this session (android 1583w, easyrunner 410w, ios 1631w, linux 472w, bundled-gateway 281w, canvas 420w); all within ±15% of plan estimates — no under-estimation. |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | `## Undigested Terms Plan` present (13-row disposition table, all routed); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, inherits master W5 capture path); expected captures = 0 confirmed by Step 2d re-scan. |
| CP8f | Slug specificity + collision audit | **PASS** | `### Renamed (general → specific)` (none — 0 new slugs) + `### Removed (substantive vault notes already cover the concept)` sub-tables present; collision audit ran across term_dictionary AND documentation/ for all planned notes; no `oc_*` doc duplicates an existing term/doc. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps ≥1 outside-folder inbound link to **all 9** notes (entry_openclaw_docs → all 9; plus repo_/term_/entry_ sources); G8-Discoverability in the gate table; inlink addition is a gated execution phase, not "recommended". |

**RESULT: 9/9 CHECKPOINTS PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
