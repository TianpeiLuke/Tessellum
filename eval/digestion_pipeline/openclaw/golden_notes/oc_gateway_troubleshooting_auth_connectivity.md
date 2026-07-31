---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - troubleshooting
keywords:
  - openclaw gateway auth troubleshooting
  - anthropic 429 long context
  - upstream 403 blocked waf
  - openai-compatible backend agent runs fail
  - dashboard control ui connectivity
  - error.details.code auth detail codes
  - device auth v2 nonce signature
  - post-upgrade auth url drift
topics:
  - OpenClaw
  - Gateway Troubleshooting
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/troubleshooting
access_control_group: ["general"]
---

# OpenClaw — Gateway Auth, Model-Call, and Control UI Connectivity Troubleshooting

## Overview

This note is the auth/connectivity cluster of the OpenClaw Gateway troubleshooting runbook (`gateway/troubleshooting`): the symptom-based recovery steps for model-call and connectivity failures that are NOT a dead gateway process. It covers Anthropic long-context `429`, upstream `403` blocked responses from a WAF/CDN, a local OpenAI-compatible backend that passes direct probes but fails on real agent runs, Dashboard/Control UI connect failures with the `error.details.code` auth detail-code map and device-auth v2 handshake, and the post-upgrade drift checklist for auth/URL/bind changes. Each section gives exact commands, the log signatures to look for, and the fix. Sibling clusters cover the process/config and message-flow/runtime sides; deeper auth-mode definitions live in the gateway authentication/configuration pages — linked, not restated.

## Anthropic 429 extra usage required for long context

Use this when logs/errors include: `HTTP 429: rate_limit_error: Extra usage is required for long context requests`.

```bash
openclaw logs --follow
openclaw models status
openclaw config get agents.defaults.models
```

Look for:

- Selected Anthropic model is a GA-capable 1M Claude 4.x model, or the model has legacy `params.context1m: true`.
- Current Anthropic credential is not eligible for long-context usage.
- Requests fail only on long sessions/model runs that need the 1M context path.

Fix options:

1. **Use a standard context window** — switch to a standard-window model, or remove legacy `context1m` from older model config that is not GA-capable for 1M context.
2. **Use an eligible credential** — use an Anthropic credential that is eligible for long-context requests, or switch to an Anthropic API key.
3. **Configure fallback models** — configure fallback models so runs continue when Anthropic long-context requests are rejected.

## Upstream 403 blocked responses

Use this when an upstream LLM provider returns a generic `403` such as `Your request was blocked`. Do not assume this is always an OpenClaw configuration issue. The response can come from an upstream security layer such as a CDN, WAF, bot-management rule, or reverse proxy in front of an OpenAI-compatible endpoint.

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
```

Look for:

- multiple models under the same provider failing in the same way
- HTML or generic security text instead of a normal provider API error
- provider-side security events for the same request time
- a tiny direct `curl` probe succeeding while normal SDK-shaped requests fail

Fix the provider-side filtering first when the evidence points to a WAF/CDN block. Prefer a narrowly scoped allow or skip rule for the API path OpenClaw uses, and avoid disabling protection for the whole site. A successful minimal `curl` does NOT guarantee that real SDK-style requests will pass through the same upstream security layer.

## Local OpenAI-compatible backend passes direct probes but agent runs fail

Use this when `curl ... /v1/models` works, tiny direct `/v1/chat/completions` calls work, but OpenClaw model runs fail only on normal agent turns.

```bash
curl http://127.0.0.1:1234/v1/models
curl http://127.0.0.1:1234/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"<id>","messages":[{"role":"user","content":"hi"}],"stream":false}'
openclaw infer model run --model <provider/model> --prompt "hi" --json
openclaw logs --follow
```

Look for:

- direct tiny calls succeed, but OpenClaw runs fail only on larger prompts
- `model_not_found` or 404 errors even though direct `/v1/chat/completions` works with the same bare model id
- backend errors about `messages[].content` expecting a string
- intermittent `incomplete turn detected ... stopReason=stop payloads=0` warnings with an OpenAI-compatible local backend
- backend crashes that appear only with larger prompt-token counts or full agent runtime prompts

### Common signatures

- `model_not_found` with a local MLX/vLLM-style server → verify `baseUrl` includes `/v1`, `api` is `"openai-completions"` for `/v1/chat/completions` backends, and `models.providers.<provider>.models[].id` is the bare provider-local id. Select it with the provider prefix once, for example `mlx/mlx-community/Qwen3-30B-A3B-6bit`; keep the catalog entry as `mlx-community/Qwen3-30B-A3B-6bit`.
- `messages[...].content: invalid type: sequence, expected a string` → backend rejects structured Chat Completions content parts. Fix: set `models.providers.<provider>.models[].compat.requiresStringContent: true`.
- `validation.keys` or allowed message keys like `["role","content"]` → backend rejects OpenAI-style replay metadata on Chat Completions messages. Fix: set `models.providers.<provider>.models[].compat.strictMessageKeys: true`.
- `incomplete turn detected ... stopReason=stop payloads=0` → the backend completed the Chat Completions request but returned no user-visible assistant text for that turn. OpenClaw retries replay-safe empty OpenAI-compatible turns once; persistent failures usually mean the backend is emitting empty/non-text content or suppressing final-answer text.
- direct tiny requests succeed, but OpenClaw agent runs fail with backend/model crashes (for example Gemma on some `inferrs` builds) → OpenClaw transport is likely already correct; the backend is failing on the larger agent-runtime prompt shape.
- failures shrink after disabling tools but do not disappear → tool schemas were part of the pressure, but the remaining issue is still upstream model/server capacity or a backend bug.

### Fix options

1. Set `compat.requiresStringContent: true` for string-only Chat Completions backends.
2. Set `compat.strictMessageKeys: true` for strict Chat Completions backends that only accept `role` and `content` on each message.
3. Set `compat.supportsTools: false` for models/backends that cannot handle OpenClaw's tool schema surface reliably.
4. Lower prompt pressure where possible: smaller workspace bootstrap, shorter session history, lighter local model, or a backend with stronger long-context support.
5. If tiny direct requests keep passing while OpenClaw agent turns still crash inside the backend, treat it as an upstream server/model limitation and file a repro there with the accepted payload shape.

## Dashboard control UI connectivity

When dashboard/control UI will not connect, validate URL, auth mode, and secure context assumptions.

```bash
openclaw gateway status
openclaw status
openclaw logs --follow
openclaw doctor
openclaw gateway status --json
```

Look for: correct probe URL and dashboard URL; auth mode/token mismatch between client and gateway; HTTP usage where device identity is required.

If a local browser cannot connect to `127.0.0.1:18789` after an update, first recover the local Gateway service and confirm it is serving the dashboard:

```bash
openclaw gateway restart
lsof -i :18789
curl http://127.0.0.1:18789
```

If `curl` returns OpenClaw HTML, the Gateway is working and the remaining issue is likely browser cache, an old deep link, or stale tab state. Open `http://127.0.0.1:18789` directly and navigate from the dashboard. If restart does not leave the service running, run `openclaw gateway start` and recheck `openclaw gateway status`.

**Connect / auth signatures:**

- `device identity required` → non-secure context or missing device auth.
- `origin not allowed` → browser `Origin` is not in `gateway.controlUi.allowedOrigins` (or you are connecting from a non-loopback browser origin without an explicit allowlist).
- `device nonce required` / `device nonce mismatch` → client is not completing the challenge-based device auth flow (`connect.challenge` + `device.nonce`).
- `device signature invalid` / `device signature expired` → client signed the wrong payload (or stale timestamp) for the current handshake.
- `AUTH_TOKEN_MISMATCH` with `canRetryWithDeviceToken=true` → client can do one trusted retry with cached device token. That cached-token retry reuses the cached scope set stored with the paired device token. Explicit `deviceToken` / explicit `scopes` callers keep their requested scope set instead.
- `AUTH_SCOPE_MISMATCH` → the device token was recognized, but its approved scopes do not cover this connect request; re-pair or approve the requested scope contract instead of rotating a shared gateway token.
- Outside that retry path, connect auth precedence is explicit shared token/password first, then explicit `deviceToken`, then stored device token, then bootstrap token.
- On the async Tailscale Serve Control UI path, failed attempts for the same `{scope, ip}` are serialized before the limiter records the failure. Two bad concurrent retries from the same client can therefore surface `retry later` on the second attempt instead of two plain mismatches.
- `too many failed authentication attempts (retry later)` from a browser-origin loopback client → repeated failures from that same normalized `Origin` are locked out temporarily; another localhost origin uses a separate bucket.
- repeated `unauthorized` after that retry → shared token/device token drift; refresh token config and re-approve/rotate device token if needed.
- `gateway connect failed:` → wrong host/port/url target.

### Auth detail codes quick map

Use `error.details.code` from the failed `connect` response to pick the next action:

| Detail code | Meaning | Recommended action |
| --- | --- | --- |
| `AUTH_TOKEN_MISSING` | Client did not send a required shared token. | Paste/set token in the client and retry. For dashboard paths: `openclaw config get gateway.auth.token` then paste into Control UI settings. |
| `AUTH_TOKEN_MISMATCH` | Shared token did not match gateway auth token. | If `canRetryWithDeviceToken=true`, allow one trusted retry. Cached-token retries reuse stored approved scopes; explicit `deviceToken` / `scopes` callers keep requested scopes. If still failing, run the token drift recovery checklist. |
| `AUTH_DEVICE_TOKEN_MISMATCH` | Cached per-device token is stale or revoked. | Rotate/re-approve device token using the devices CLI, then reconnect. |
| `AUTH_SCOPE_MISMATCH` | Device token is valid, but its approved role/scopes do not cover this connect request. | Re-pair the device or approve the requested scope contract; do not treat this as shared-token drift. |
| `PAIRING_REQUIRED` | Device identity needs approval. Check `error.details.reason` for `not-paired`, `scope-upgrade`, `role-upgrade`, or `metadata-upgrade`, and use `requestId` / `remediationHint` when present. | Approve pending request: `openclaw devices list` then `openclaw devices approve <requestId>`. Scope/role upgrades use the same flow after you review the requested access. |

Direct loopback backend RPCs authenticated with the shared gateway token/password should not depend on the CLI's paired-device scope baseline. If subagents or other internal calls still fail with `scope-upgrade`, verify the caller is using `client.id: "gateway-client"` and `client.mode: "backend"` and is not forcing an explicit `deviceIdentity` or device token.

**Device auth v2 migration check** — run `openclaw --version`, `openclaw doctor`, and `openclaw gateway status`. If logs show nonce/signature errors, update the connecting client and verify the three-step handshake: (1) the client waits for the gateway-issued `connect.challenge`; (2) the client signs the challenge-bound payload; (3) the client sends `connect.params.device.nonce` with the same challenge nonce. If `openclaw devices rotate` / `revoke` / `remove` is denied unexpectedly: paired-device token sessions can manage only **their own** device unless the caller also has `operator.admin`, and `openclaw devices rotate --scope ...` can only request operator scopes that the caller session already holds.

## If you upgraded and something suddenly broke

Most post-upgrade breakage is config drift or stricter defaults now being enforced. The page lists three sub-checks.

**1. Auth and URL override behavior changed** — run `openclaw gateway status`, `openclaw config get gateway.mode`, `openclaw config get gateway.remote.url`, and `openclaw config get gateway.auth.mode`. Check: if `gateway.mode=remote`, CLI calls may be targeting remote while your local service is fine; explicit `--url` calls do not fall back to stored credentials. Signatures: `gateway connect failed:` → wrong URL target; `unauthorized` → endpoint reachable but wrong auth.

**2. Bind and auth guardrails are stricter** — run `openclaw config get gateway.bind`, `openclaw config get gateway.auth.mode`, `openclaw config get gateway.auth.token`, `openclaw gateway status`, and `openclaw logs --follow`. Check: non-loopback binds (`lan`, `tailnet`, `custom`) need a valid gateway auth path — shared token/password auth, or a correctly configured non-loopback `trusted-proxy` deployment; old keys like `gateway.token` do not replace `gateway.auth.token`. Signatures: `refusing to bind gateway ... without auth` → non-loopback bind without a valid gateway auth path; `Connectivity probe: failed` while runtime is running → gateway alive but inaccessible with current auth/url.

**3. Pairing and device identity state changed** — run `openclaw devices list`, `openclaw pairing list --channel <channel> [--account <id>]`, `openclaw logs --follow`, and `openclaw doctor`. Check: pending device approvals for dashboard/nodes; pending DM pairing approvals after policy or identity changes. Signatures: `device identity required` → device auth not satisfied; `pairing required` → sender/device must be approved.

If the service config and runtime still disagree after checks, reinstall service metadata from the same profile/state directory:

```bash
openclaw gateway install --force
openclaw gateway restart
```

**Source**: OpenClaw documentation — `gateway/troubleshooting` (auth/connectivity cluster; mirror `inbox/openclaw_docs/gateway/troubleshooting.md`)
**Last Updated**: 2026-06-22
**Status**: Active
