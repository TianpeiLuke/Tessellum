---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - security
keywords:
  - openclaw credential storage map
  - secrets on disk hardening
  - workspace .env blocking
  - logs transcripts redaction retention
  - dm session isolation dmscope
  - dm allowlists pairing
  - file permissions 700 600
  - incident response contain rotate audit
topics:
  - OpenClaw
  - Gateway Security
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/security
access_control_group: ["general"]
---

# OpenClaw — Gateway On-Disk Data Protection and Incident Response

## Overview

This note is the operator procedure for protecting OpenClaw's on-disk data and responding to a security incident, mirroring the data-protection and incident-response sections of the `gateway/security` source page. It covers the credential storage map (where each credential lives), securing secrets under `~/.openclaw`, blocking provider credentials from untrusted workspace `.env` files, log/transcript redaction and retention, the DM access model (pairing/allowlist/open/disabled) plus DM session isolation and allowlists, file permissions, the shared-inbox quick rule, the Contain/Rotate/Audit/Collect incident-response runbook, secret scanning, and how to report a vulnerability. Network, tool/sandbox, prompt-injection, and audit hardening live in sibling `oc_gateway_security_*` notes; this note is the host/disk trust-boundary layer.

## Credential storage map

Use this map when auditing access or deciding what to back up. OpenClaw stores credentials and private state across these paths:

- **WhatsApp**: `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
- **Telegram bot token**: config/env or `channels.telegram.tokenFile` (regular file only; symlinks rejected)
- **Discord bot token**: config/env or SecretRef (env/file/exec providers)
- **Slack tokens**: config/env (`channels.slack.*`)
- **Pairing allowlists**: `~/.openclaw/credentials/<channel>-allowFrom.json` (default account) and `~/.openclaw/credentials/<channel>-<accountId>-allowFrom.json` (non-default accounts)
- **Model auth profiles**: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- **Codex runtime state**: `~/.openclaw/agents/<agentId>/agent/codex-home/`
- **File-backed secrets payload (optional)**: `~/.openclaw/secrets.json`
- **Legacy OAuth import**: `~/.openclaw/credentials/oauth.json`

## Secrets on disk

Assume anything under `~/.openclaw/` (or `$OPENCLAW_STATE_DIR/`) may contain secrets or private data. The source enumerates the sensitive contents: `openclaw.json` (config may include gateway and remote-gateway tokens, provider settings, and allowlists); `credentials/**` (channel credentials such as WhatsApp creds, pairing allowlists, legacy OAuth imports); `agents/<agentId>/agent/auth-profiles.json` (API keys, token profiles, OAuth tokens, and optional `keyRef`/`tokenRef`); `agents/<agentId>/agent/codex-home/**` (per-agent Codex app-server account, config, skills, plugins, native thread state, and diagnostics); `secrets.json` (optional file-backed secret payload used by `file` SecretRef providers via `secrets.providers`); `agents/<agentId>/agent/auth.json` (legacy compatibility file — static `api_key` entries are scrubbed when discovered); `agents/<agentId>/sessions/**` (session transcripts `*.jsonl` plus routing metadata `sessions.json` that can contain private messages and tool output); bundled plugin packages (installed plugins plus their `node_modules/`); and `sandboxes/**` (tool sandbox workspaces that can accumulate copies of files read/written inside the sandbox).

Hardening tips from the source: keep permissions tight (`700` on dirs, `600` on files); use full-disk encryption on the gateway host; and prefer a dedicated OS user account for the Gateway if the host is shared.

## Local session logs live on disk

OpenClaw stores session transcripts on disk under `~/.openclaw/agents/<agentId>/sessions/*.jsonl`. This is required for session continuity and (optionally) session memory indexing, but it also means **any process/user with filesystem access can read those logs**. Treat disk access as the trust boundary and lock down permissions on `~/.openclaw`. If you need stronger isolation between agents, run them under separate OS users or separate hosts.

## File permissions

Keep config and state private on the gateway host:

- `~/.openclaw/openclaw.json`: `600` (user read/write only)
- `~/.openclaw`: `700` (user only)

`openclaw doctor` can warn and offer to tighten these permissions.

## Workspace `.env` files

OpenClaw loads workspace-local `.env` files for agents and tools, but never lets those files silently override gateway runtime controls. The protections are:

- **Provider credential environment variables are blocked** from untrusted workspace `.env` files. Examples include `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `XAI_API_KEY`, `MISTRAL_API_KEY`, `GROQ_API_KEY`, `DEEPSEEK_API_KEY`, `PERPLEXITY_API_KEY`, `BRAVE_API_KEY`, `TAVILY_API_KEY`, `EXA_API_KEY`, `FIRECRAWL_API_KEY`, and provider auth keys declared by installed trusted plugins. Put provider credentials in the Gateway process environment, `~/.openclaw/.env` (`$OPENCLAW_STATE_DIR/.env`), the config `env` block, or optional login-shell import.
- **Any key that starts with `OPENCLAW_*` is blocked** from untrusted workspace `.env` files.
- **Channel endpoint settings** for Matrix, Mattermost, IRC, and Synology Chat are also blocked from workspace `.env` overrides, so cloned workspaces cannot redirect bundled connector traffic through local endpoint config. Endpoint env keys (such as `MATRIX_HOMESERVER`, `MATTERMOST_URL`, `IRC_HOST`, `SYNOLOGY_CHAT_INCOMING_URL`) must come from the gateway process environment or `env.shellEnv`, not from a workspace-loaded `.env`.
- The block is **fail-closed**: a new runtime-control variable added in a future release cannot be inherited from a checked-in or attacker-supplied `.env`; the key is ignored and the gateway keeps its own value.
- Trusted process/OS environment variables, global runtime dotenv, config `env`, and enabled login-shell import still apply — this only constrains workspace `.env` file loading.

Why: workspace `.env` files frequently live next to agent code, get committed by accident, or get written by tools. Blocking provider credentials prevents a cloned workspace from substituting attacker-controlled provider accounts; blocking the whole `OPENCLAW_*` prefix means adding a new `OPENCLAW_*` flag later can never regress into silent inheritance from workspace state.

## Logs and transcripts (redaction and retention)

Logs and transcripts can leak sensitive info even when access controls are correct: Gateway logs may include tool summaries, errors, and URLs; session transcripts can include pasted secrets, file contents, command output, and links. Recommendations from the source:

- Keep log and transcript redaction on (`logging.redactSensitive: "tools"`; default).
- Add custom patterns for your environment via `logging.redactPatterns` (tokens, hostnames, internal URLs).
- When sharing diagnostics, prefer `openclaw status --all` (pasteable, secrets redacted) over raw logs.
- Prune old session transcripts and log files if you don't need long retention.

## DM access model: pairing, allowlist, open, disabled

All current DM-capable channels support a DM policy (`dmPolicy` or `*.dm.policy`) that gates inbound DMs **before** the message is processed:

- `pairing` (default): unknown senders receive a short pairing code and the bot ignores their message until approved. Codes expire after 1 hour; repeated DMs won't resend a code until a new request is created. Pending requests are capped at **3 per channel** by default.
- `allowlist`: unknown senders are blocked (no pairing handshake).
- `open`: allow anyone to DM (public). **Requires** the channel allowlist to include `"*"` (explicit opt-in).
- `disabled`: ignore inbound DMs entirely.

Approve pending pairing requests via CLI:

```bash
openclaw pairing list <channel>
openclaw pairing approve <channel> <code>
```

## DM session isolation and Secure DM mode

By default, OpenClaw routes **all DMs into the main session** so the assistant has continuity across devices and channels. If **multiple people** can DM the bot (open DMs or a multi-person allowlist), isolate DM sessions with `dmScope`. The "secure DM mode" baseline:

```json5
{
  session: { dmScope: "per-channel-peer" },
}
```

This prevents cross-user context leakage while keeping group chats isolated. It is a messaging-context boundary, not a host-admin boundary: if users are mutually adversarial and share the same Gateway host/config, run separate gateways per trust boundary instead. The `dmScope` options the source documents:

- Default: `session.dmScope: "main"` (all DMs share one session for continuity).
- Local CLI onboarding default: writes `session.dmScope: "per-channel-peer"` when unset (keeps existing explicit values).
- Secure DM mode: `session.dmScope: "per-channel-peer"` (each channel+sender pair gets an isolated DM context).
- Cross-channel peer isolation: `session.dmScope: "per-peer"` (each sender gets one session across all channels of the same type).

If you run multiple accounts on the same channel, use `per-account-channel-peer` instead. If the same person contacts you on multiple channels, use `session.identityLinks` to collapse those DM sessions into one canonical identity.

## Shared inbox quick rule

If more than one person can DM your bot:

- Set `session.dmScope: "per-channel-peer"` (or `"per-account-channel-peer"` for multi-account channels).
- Keep `dmPolicy: "pairing"` or strict allowlists.
- Never combine shared DMs with broad tool access.
- This hardens cooperative/shared inboxes, but is not designed as hostile co-tenant isolation when users share host/config write access.

## Allowlists for DMs and groups

OpenClaw has two separate "who can trigger me?" layers:

- **DM allowlist** (`allowFrom` / `channels.discord.allowFrom` / `channels.slack.allowFrom`; legacy: `channels.discord.dm.allowFrom`, `channels.slack.dm.allowFrom`): who is allowed to talk to the bot in direct messages. When `dmPolicy="pairing"`, approvals are written to the account-scoped pairing allowlist store under `~/.openclaw/credentials/` (`<channel>-allowFrom.json` for the default account, `<channel>-<accountId>-allowFrom.json` for non-default accounts), merged with config allowlists.
- **Group allowlist** (channel-specific): which groups/channels/guilds the bot will accept messages from at all. Common patterns: `channels.whatsapp.groups`, `channels.telegram.groups`, `channels.imessage.groups` (per-group defaults like `requireMention`; when set, it also acts as a group allowlist — include `"*"` to keep allow-all behavior); `groupPolicy="allowlist"` + `groupAllowFrom` (restrict who can trigger the bot inside a group session on WhatsApp/Telegram/Signal/iMessage/Microsoft Teams); `channels.discord.guilds` / `channels.slack.channels` (per-surface allowlists + mention defaults).

Group checks run in this order: `groupPolicy`/group allowlists first, mention/reply activation second. Replying to a bot message (implicit mention) does **not** bypass sender allowlists like `groupAllowFrom`. Security note: treat `dmPolicy="open"` and `groupPolicy="open"` as last-resort settings — they should be barely used; prefer pairing + allowlists unless you fully trust every member of the room.

## Separate numbers (WhatsApp, Signal, Telegram)

For phone-number-based channels, consider running your AI on a separate phone number from your personal one:

- Personal number: your conversations stay private.
- Bot number: AI handles these, with appropriate boundaries.

## Incident response

If your AI does something bad, follow the Contain → Rotate → Audit → Collect runbook.

### Contain

1. **Stop it:** stop the macOS app (if it supervises the Gateway) or terminate your `openclaw gateway` process.
2. **Close exposure:** set `gateway.bind: "loopback"` (or disable Tailscale Funnel/Serve) until you understand what happened.
3. **Freeze access:** switch risky DMs/groups to `dmPolicy: "disabled"` / require mentions, and remove `"*"` allow-all entries if you had them.

### Rotate (assume compromise if secrets leaked)

1. Rotate Gateway auth (`gateway.auth.token` / `OPENCLAW_GATEWAY_PASSWORD`) and restart.
2. Rotate remote client secrets (`gateway.remote.token` / `.password`) on any machine that can call the Gateway.
3. Rotate provider/API credentials (WhatsApp creds, Slack/Discord tokens, model/API keys in `auth-profiles.json`, and encrypted secrets payload values when used).

### Audit

1. Check Gateway logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log` (or `logging.file`).
2. Review the relevant transcript(s): `~/.openclaw/agents/<agentId>/sessions/*.jsonl`.
3. Review recent config changes (anything that could have widened access: `gateway.bind`, `gateway.auth`, dm/group policies, `tools.elevated`, plugin changes).
4. Re-run `openclaw security audit --deep` and confirm critical findings are resolved.

### Collect for a report

- Timestamp, gateway host OS + OpenClaw version.
- The session transcript(s) + a short log tail (after redacting).
- What the attacker sent + what the agent did.
- Whether the Gateway was exposed beyond loopback (LAN/Tailscale Funnel/Serve).

## Secret scanning

CI runs the pre-commit `detect-private-key` hook over the repository. If it fails, remove or rotate the committed key material, then reproduce locally:

```bash
pre-commit run --all-files detect-private-key
```

## Reporting security issues

Found a vulnerability in OpenClaw? Report responsibly:

1. Email: [security@openclaw.ai](mailto:security@openclaw.ai)
2. Don't post publicly until fixed.
3. OpenClaw will credit you (unless you prefer anonymity).

**Source**: OpenClaw documentation — `gateway/security` (mirror `inbox/openclaw_docs/gateway/security.md`)
**Last Updated**: 2026-06-22
**Status**: Active
