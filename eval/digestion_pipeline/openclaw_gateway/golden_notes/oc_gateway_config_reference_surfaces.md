---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - configuration
keywords:
  - openclaw config reference surfaces
  - hooks ingress config
  - hooks gmail integration config
  - canvas plugin host config
  - discovery mdns bonjour dns-sd
  - env inline vars substitution
  - hooks mappings transforms
topics:
  - OpenClaw
  - Gateway Configuration Reference
language: markdown
date of note: 2026-06-23
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/configuration-reference
access_control_group: ["general"]
---

# OpenClaw — Gateway Config Reference: Hooks, Canvas, Discovery & Environment

## Overview

This note is the field-level reference for the **ingress / host-surface cluster** of the OpenClaw Gateway config (`~/.openclaw/openclaw.json`, JSON5; all fields optional with safe defaults), drawn from the `gateway/configuration-reference` source page. It documents the `hooks` HTTP-ingress block (including the Gmail integration), the `canvas` plugin host, the `discovery` block (mDNS/Bonjour + wide-area DNS-SD), and the `env` environment surface (inline env vars and `${VAR_NAME}` substitution). The `browser`/`ui`/`gateway`-server surfaces of the same page are split into the sibling [oc_gateway_config_reference_platform](oc_gateway_config_reference_platform.md); the runtime and ops/security clusters live in the other sibling reference notes.

## Hooks

The `hooks` block configures HTTP ingress that wakes or messages agents. Auth is `Authorization: Bearer <token>` or `x-openclaw-token: <token>` (query-string hook tokens are rejected).

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    maxBodyBytes: 262144,
    allowRequestSessionKey: true,
    allowedSessionKeyPrefixes: ["hook:", "hook:gmail:"],
    allowedAgentIds: ["hooks", "main"],
    presets: ["gmail"],
    transformsDir: "~/.openclaw/hooks/transforms",
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        agentId: "hooks",
        sessionKey: "hook:gmail:{{messages[0].id}}",
        messageTemplate: "From: {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}",
        deliver: true,
        channel: "last",
        model: "openai/gpt-5.4-mini",
      },
    ],
  },
}
```

- Validation/safety: `hooks.enabled=true` requires a non-empty `hooks.token`; the hook token should be distinct from Gateway shared-secret auth (startup logs a non-fatal warning on reuse, and `openclaw security audit` flags reuse as critical — `openclaw doctor --fix` rotates a persisted reused token). `hooks.path` cannot be `/` (use a dedicated subpath). If `hooks.allowRequestSessionKey=true`, constrain `hooks.allowedSessionKeyPrefixes` (e.g. `["hook:"]`); a templated `sessionKey` in any mapping/preset makes the prefix allowlist required.
- Endpoints: `POST /hooks/wake` → `{ text, mode?: "now"|"next-heartbeat" }`; `POST /hooks/agent` → `{ message, name?, agentId?, sessionKey?, wakeMode?, deliver?, channel?, to?, model?, thinking?, timeoutSeconds? }` (payload `sessionKey` accepted only when `hooks.allowRequestSessionKey=true`, default `false`); `POST /hooks/<name>` → resolved via `hooks.mappings` (template-rendered mapping `sessionKey` values are treated as externally supplied and also require `allowRequestSessionKey=true`).
- Mapping details: `match.path` matches the sub-path after `/hooks`; `match.source` matches a payload field for generic paths; templates like `{{messages[0].subject}}` read from the payload. `transform.module` must be a relative path that stays within `hooks.transformsDir` (absolute/traversal rejected; keep it under `~/.openclaw/hooks/transforms`). `agentId` routes to a specific agent (unknown IDs fall back to the default agent); `allowedAgentIds` restricts effective routing including the default-agent path (`*` or omitted = allow all, `[]` = deny all). `defaultSessionKey` is an optional fixed key; `deliver: true` sends the final reply to a channel (`channel` defaults to `last`); `model` overrides the LLM for that hook run.

### Gmail integration

The built-in Gmail preset uses `sessionKey: "hook:gmail:{{messages[0].id}}"`. If you keep that per-message routing, set `hooks.allowRequestSessionKey: true` and constrain `hooks.allowedSessionKeyPrefixes` to the Gmail namespace, e.g. `["hook:", "hook:gmail:"]`; if you need `allowRequestSessionKey: false`, override the preset with a static `sessionKey`. The `hooks.gmail` block configures `account`, Pub/Sub `topic`/`subscription`, `pushToken`, `hookUrl`, `includeBody`, `maxBytes`, `renewEveryMinutes`, a `serve` block (`bind`/`port`/`path`), a `tailscale` block (`mode`/`path`), and `model`/`thinking` overrides. The Gateway auto-starts `gog gmail watch serve` on boot when configured (set `OPENCLAW_SKIP_GMAIL_WATCHER=1` to disable); do not run a separate `gog gmail watch serve` alongside the Gateway.

## Canvas plugin host

The `canvas` plugin host serves agent-editable HTML/CSS/JS and A2UI under the Gateway port, configured at `plugins.entries.canvas.config.host` (`root`, `liveReload`, and an `enabled` toggle — or `OPENCLAW_SKIP_CANVAS_HOST=1`).

- Serves over HTTP at `http://<gateway-host>:<gateway.port>/__openclaw__/canvas/` and `http://<gateway-host>:<gateway.port>/__openclaw__/a2ui/`.
- Local-only: keep `gateway.bind: "loopback"` (default). Non-loopback binds require Gateway auth (token/password/trusted-proxy) on canvas routes, same as other Gateway HTTP surfaces.
- Node WebViews typically do not send auth headers; after a node is paired and connected, the Gateway advertises node-scoped capability URLs for canvas/A2UI access. Capability URLs are bound to the active node WS session and expire quickly; IP-based fallback is not used.
- Injects a live-reload client into served HTML and auto-creates a starter `index.html` when empty. Changes require a gateway restart; disable live reload for large directories or `EMFILE` errors.

## Discovery

The `discovery` block controls how the Gateway advertises itself for node discovery.

### mDNS (Bonjour)

`discovery.mdns.mode` is `minimal` (default when the bundled `bonjour` plugin is enabled — omit `cliPath` + `sshPort` from TXT records), `full` (include `cliPath` + `sshPort`; LAN multicast advertising still requires the bundled `bonjour` plugin enabled), or `off` (suppress LAN multicast advertising without changing plugin enablement). The bundled `bonjour` plugin auto-starts on macOS hosts and is opt-in on Linux, Windows, and containerized Gateway deployments. The advertised hostname defaults to the system hostname when it is a valid DNS label, falling back to `openclaw`; override with `OPENCLAW_MDNS_HOSTNAME`.

### Wide-area (DNS-SD)

`discovery.wideArea.enabled: true` writes a unicast DNS-SD zone under `~/.openclaw/dns/`. For cross-network discovery, pair with a DNS server (CoreDNS recommended) plus Tailscale split DNS. Setup: `openclaw dns setup --apply`.

## Environment

### `env` (inline env vars)

The `env` block injects environment variables: `env.<KEY>` and `env.vars.<KEY>` set inline values, and `env.shellEnv` (`enabled`, `timeoutMs`) imports missing expected keys from your login shell profile. Inline env vars are only applied if the process env is missing the key. `.env` files are read from the CWD `.env` and `~/.openclaw/.env` (neither overrides existing vars). See `/help/environment` for full precedence.

### Env var substitution

Reference env vars in any config string with `${VAR_NAME}` (for example `gateway.auth.token: "${OPENCLAW_GATEWAY_TOKEN}"`). Only uppercase names matching `[A-Z_][A-Z0-9_]*` are matched; missing/empty vars throw an error at config load; escape with `$${VAR}` for a literal `${VAR}`; and substitution works with `$include`.

## Related Notes

**Terms**

- **[Webhook](../../term_dictionary/term_webhook.md)** — HTTP callback; relevance: the `hooks` HTTP-ingress block + Gmail integration.
- **[Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md)** — mDNS service discovery; relevance: the `discovery` mDNS/Bonjour config block.
- **[DNS](../../term_dictionary/term_dns.md)** — domain name system; relevance: the wide-area DNS-SD discovery config.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — the gateway product; relevance: the ingress/host surfaces being configured.
- **[OAuth Token](../../term_dictionary/term_oauth_token.md)** — bearer token; relevance: hook `Authorization: Bearer <token>` auth.
- **[WebSocket](../../term_dictionary/term_websocket.md)** — full-duplex transport; relevance: node-scoped canvas/A2UI capability URLs bound to the node WS session.
- **[Cron](../../term_dictionary/term_cron.md)** — scheduled jobs; relevance: hook-driven wakes complement cron scheduling.
- **[Prompt Engineering](../../term_dictionary/term_prompt_engineering.md)** — templating; relevance: hook `messageTemplate` / `{{...}}` payload templates.

**Docs**

- **[oc_gateway_config_reference_platform](oc_gateway_config_reference_platform.md)** — browser/UI/gateway-server (this series, split sibling); relevance: the host/server half of the same source page.
- **[oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md)** — runtime cluster (this series); relevance: sibling field-reference cluster.
- **[oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md)** — ops/security cluster (this series); relevance: sibling field-reference cluster.
- **[oc_gateway_discovery](oc_gateway_discovery.md)** — discovery design (this series); relevance: the design these mDNS/DNS-SD fields configure.
- **[oc_gateway_external_apps](oc_gateway_external_apps.md)** — external app registration (this series); relevance: hook ingress complements external-app integration.
- **[Hermes — MsGraph Webhook Listener](../hermes_agent/hermes_msgraph_webhook_listener.md)** — webhook ingress; relevance: the Gmail/webhook hook config analog.
- **[Hermes — Webhooks: Routing & Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md)** — webhook routing; relevance: hook `mappings`/routing analog.
- **[Claude Code — Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md)** — gateway/network fields; relevance: discovery/env config-surface precedent.
- **[oc_concepts_channel_docking](oc_concepts_channel_docking.md)** — channel delivery (this series); relevance: hook `deliver`/`channel` final-reply routing.

**Repos**

- **[repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md)** — gateway runtime; relevance: hooks/discovery/env config validation + dispatch.
- **[repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md)** — apps/Control UI; relevance: the Canvas plugin host config block.
- **[repo_openclaw](../../../areas/code_repos/repo_openclaw.md)** — monorepo; relevance: the env/discovery config root.

**Snippets**

- **[snippet_openclaw_gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md)** — hooks config payload; relevance: the Hooks block + Gmail preset config.
- **[snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md)** — hooks request handler; relevance: how hook config is dispatched (`/hooks/*` endpoints).
- **[snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md)** — mDNS discovery client; relevance: consumes the `discovery` mDNS/Bonjour config fields.
- **[snippet_openclaw_macos_canvas_filewatcher](../../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md)** — canvas plugin host; relevance: the Canvas plugin host config block + live reload.
- **[snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md)** — canvas lifecycle; relevance: the canvas host lifecycle the config controls.
- **[snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md)** — node pairing; relevance: node-scoped capability URLs for canvas/A2UI access.
- **[snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md)** — server auth/startup; relevance: env-var substitution at config load + hook-token validation.
- **[snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md)** — plugin runtime load; relevance: the canvas plugin host loads via `plugins.entries.canvas`.
- **[snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md)** — webhook signature verify; relevance: hook-token auth analog for inbound HTTP.

## References

- [OpenClaw Docs — Configuration reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw Docs — Configuration](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Docs — Environment](https://docs.openclaw.ai/help/environment)
- [OpenClaw Docs — Plugins](https://docs.openclaw.ai/tools/plugin)

**Source**: OpenClaw documentation — `gateway/configuration-reference` (hooks/canvas/discovery/env cluster; mirror `inbox/openclaw_docs/gateway/configuration-reference.md`)
**Last Updated**: 2026-06-23
**Status**: Active
