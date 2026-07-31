---
tags:
  - resource
  - documentation
  - hermes_agent
  - environment_variables
  - runtime_configuration
keywords:
  - hermes environment variables
  - terminal backend
  - messaging gateway
  - agent behavior
  - context compression
  - provider routing
  - session settings
topics:
  - Hermes Agent
  - Environment Variables
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/reference/environment-variables
access_control_group: ["general"]
---

# Hermes Agent — Environment Variables: Runtime, Messaging & Behavior

## Overview

This is the second half of the Hermes Agent environment-variable reference: the variables that control **how the runtime behaves** rather than which provider it authenticates against. It covers the execution-backend selectors (terminal, SSH, container, persistent shell), the messaging-gateway and per-platform variables (Telegram/Discord/Slack/WhatsApp/Signal/Matrix/Feishu/…, plus the web dashboard, Microsoft Graph, LINE, ntfy, and advanced batcher tuning), and the agent-behavior / interface / session / context-compression / auxiliary-task / fallback-provider / provider-routing knobs. (The provider/auth/tool-API keys are the companion note [hermes_env_vars_providers_auth_tools](hermes_env_vars_providers_auth_tools.md).) Like all Hermes vars, these live in `~/.hermes/.env` or are set with `hermes config set VAR value` — which routes secrets to `.env` and everything else into `config.yaml`. A few sections (Context Compression, Fallback Providers, Provider Routing) have **no env vars at all** and are configured exclusively in `config.yaml`; they are documented here because they sit in this section of the source reference.

## Terminal, SSH & Container Backends

`TERMINAL_ENV` selects the execution backend: `local`, `docker`, `ssh`, `singularity`, `modal`, or `daytona`. Backend-specific image/resource vars:

- **Container binary & image**: `HERMES_DOCKER_BINARY` (override `docker`/`podman` discovery), `TERMINAL_DOCKER_IMAGE` (default `nikolaik/python-nodejs:python3.11-nodejs20`), `TERMINAL_SINGULARITY_IMAGE`, `TERMINAL_MODAL_IMAGE`, `TERMINAL_DAYTONA_IMAGE`.
- **Docker session shape**: `TERMINAL_DOCKER_FORWARD_ENV` (JSON array of env names to forward — skill-declared `required_environment_variables` forward automatically), `TERMINAL_DOCKER_VOLUMES` (comma-separated `host:container`), `TERMINAL_DOCKER_MOUNT_CWD_TO_WORKSPACE`.
- **Limits & lifetime**: `TERMINAL_TIMEOUT`, `TERMINAL_LIFETIME_SECONDS` (idle cleanup; later resumes may recreate cloud sandboxes rather than keep live processes), `TERMINAL_CWD` (deprecated — prefer `terminal.cwd`), `SUDO_PASSWORD` (sudo without an interactive prompt).
- **SSH backend**: `TERMINAL_SSH_HOST`, `TERMINAL_SSH_USER`, `TERMINAL_SSH_PORT` (default 22), `TERMINAL_SSH_KEY`, `TERMINAL_SSH_PERSISTENT`.
- **Container resources** (Docker/Singularity/Modal/Daytona): `TERMINAL_CONTAINER_CPU` (1), `TERMINAL_CONTAINER_MEMORY` (5120 MB), `TERMINAL_CONTAINER_DISK` (51200 MB), `TERMINAL_CONTAINER_PERSISTENT` (`true`), `TERMINAL_SANDBOX_DIR` (default `~/.hermes/sandboxes/`).
- **Persistent shell**: `TERMINAL_PERSISTENT_SHELL` (non-local backends, default `true`; also `terminal.persistent_shell`), `TERMINAL_LOCAL_PERSISTENT` (local backend, default `false`), `TERMINAL_SSH_PERSISTENT` (SSH override).

## Messaging Gateway & Per-Platform Variables

The Messaging section is the largest table in the source — one block of variables per chat platform. The recurring naming pattern is `<PLATFORM>_BOT_TOKEN`/credentials, `<PLATFORM>_ALLOWED_USERS` (allowlist / access control), `<PLATFORM>_HOME_CHANNEL` (default cron-delivery target), and per-platform `REQUIRE_MENTION`/`REACTIONS`/`REPLY_TO_MODE`/`ALLOW_ALL_USERS` toggles. Platforms covered, each with its credential gate:

- **Telegram** — `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS`, `TELEGRAM_GROUP_ALLOWED_USERS`/`_CHATS`, `TELEGRAM_HOME_CHANNEL`(`_NAME`), `TELEGRAM_CRON_THREAD_ID`, webhook mode (`TELEGRAM_WEBHOOK_URL`/`_PORT`/`_SECRET` — secret is **required** whenever the URL is set), `TELEGRAM_REACTIONS`, `TELEGRAM_REQUIRE_MENTION`, `TELEGRAM_MENTION_PATTERNS`, `TELEGRAM_EXCLUSIVE_BOT_MENTIONS`, `TELEGRAM_REPLY_TO_MODE`, `TELEGRAM_IGNORED_THREADS`, `TELEGRAM_PROXY`.
- **Discord** — `DISCORD_BOT_TOKEN`, `DISCORD_ALLOWED_USERS`/`_ROLES`/`_CHANNELS`, `DISCORD_PROXY`, `DISCORD_HOME_CHANNEL`(`_NAME`), `DISCORD_COMMAND_SYNC_POLICY` (`safe`/`bulk`/`off`), `DISCORD_REQUIRE_MENTION`, `DISCORD_FREE_RESPONSE_CHANNELS`, `DISCORD_AUTO_THREAD`, attachment knobs (`DISCORD_ALLOW_ANY_ATTACHMENT`, `DISCORD_MAX_ATTACHMENT_BYTES`), `DISCORD_REACTIONS`, `DISCORD_IGNORED_CHANNELS`, `DISCORD_NO_THREAD_CHANNELS`, `DISCORD_REPLY_TO_MODE`, and four `DISCORD_ALLOW_MENTION_*` ping controls.
- **Slack** — `SLACK_BOT_TOKEN` (`xoxb-`), `SLACK_APP_TOKEN` (`xapp-`, Socket Mode), `SLACK_ALLOWED_USERS`, `SLACK_HOME_CHANNEL`(`_NAME`).
- **Google Chat** — `GOOGLE_CHAT_PROJECT_ID`, `GOOGLE_CHAT_SUBSCRIPTION_NAME`, `GOOGLE_CHAT_SERVICE_ACCOUNT_JSON`, `GOOGLE_CHAT_ALLOWED_USERS`/`ALLOW_ALL_USERS`, `GOOGLE_CHAT_HOME_CHANNEL`(`_NAME`), Pub/Sub FlowControl (`_MAX_MESSAGES`/`_MAX_BYTES`), `GOOGLE_CHAT_BOOTSTRAP_SPACES`, `GOOGLE_CHAT_DEBUG_RAW`.
- **WhatsApp** (Baileys bridge `WHATSAPP_*` + Cloud API `WHATSAPP_CLOUD_*`) — bridge mode (`WHATSAPP_ENABLED`/`MODE`/`ALLOWED_USERS`/`ALLOW_ALL_USERS`/`DEBUG`) and the full Cloud API set (`WHATSAPP_CLOUD_PHONE_NUMBER_ID`, `_ACCESS_TOKEN`, `_APP_SECRET`, `_VERIFY_TOKEN`, webhook host/port/path, DM/group policies, etc.).
- **Signal** (`SIGNAL_*`), **SMS/Twilio** (`TWILIO_*` + `SMS_*` webhook listener), **Email** (`EMAIL_*` IMAP/SMTP adapter), **DingTalk** (`DINGTALK_*`), **Feishu/Lark** (`FEISHU_APP_ID`/`_SECRET`, `FEISHU_DOMAIN`, `FEISHU_CONNECTION_MODE`, `FEISHU_ALLOW_BOTS`, `FEISHU_REQUIRE_MENTION`, …), **WeCom** (`WECOM_*` + self-built-app `WECOM_CALLBACK_*`), **Weixin** (`WEIXIN_*` iLink Bot API), **BlueBubbles** (iMessage, `BLUEBUBBLES_*`), **QQ** (`QQ_*`/`QQBOT_*` + STT fallback), **Mattermost** (`MATTERMOST_*`), and **Matrix** (`MATRIX_*` — homeserver/token/user/password, allowed users/rooms, the full E2EE set `MATRIX_ENCRYPTION`/`_E2EE_MODE`/`_DEVICE_ID`/`_RECOVERY_KEY`, and granular `MATRIX_TOOLS_ALLOW_*` tool gates).
- **Home Assistant** — `HASS_TOKEN`, `HASS_URL` (enables HA platform + tools).
- **Generic webhook & API server** — `WEBHOOK_ENABLED`/`_PORT`/`_SECRET`; the OpenAI-compatible `API_SERVER_ENABLED`/`_KEY`/`_CORS_ORIGINS`/`_PORT`/`_HOST`/`_MODEL_NAME`.
- **Gateway-wide** — `GATEWAY_PROXY_URL`/`GATEWAY_PROXY_KEY` (proxy mode: forward all agent work to a remote Hermes API server), `MESSAGING_CWD` (deprecated — prefer `terminal.cwd`), `GATEWAY_ALLOWED_USERS`, `GATEWAY_ALLOW_ALL_USERS`.

### Web Dashboard, MS-Graph, LINE & ntfy

Sub-sections layer in delivery/auth surfaces:

- **Web Dashboard & Hermes Desktop** — three bundled auth providers: username/password (`HERMES_DASHBOARD_BASIC_AUTH_USERNAME`/`_PASSWORD`/`_PASSWORD_HASH`/`_SECRET`/`_TTL_SECONDS`), OAuth via Nous Portal (`HERMES_DASHBOARD_OAUTH_CLIENT_ID`, `HERMES_DASHBOARD_PUBLIC_URL`), and self-hosted OIDC (`HERMES_DASHBOARD_OIDC_ISSUER`/`_CLIENT_ID`/`_SCOPES`); plus `HERMES_DESKTOP_REMOTE_URL` on the Desktop side. A non-loopback bind engages the auth gate.
- **Microsoft Graph (Teams)** — app-only creds `MSGRAPH_TENANT_ID`/`_CLIENT_ID`/`_CLIENT_SECRET`/`_SCOPE`/`_AUTHORITY_URL`; the **Webhook Listener** (`MSGRAPH_WEBHOOK_ENABLED`/`_PORT`/`_CLIENT_STATE`/`_ACCEPTED_RESOURCES`/`_ALLOWED_SOURCE_CIDRS`); and **Teams Meeting Summary Delivery** (`TEAMS_DELIVERY_MODE`, `TEAMS_INCOMING_WEBHOOK_URL`, `TEAMS_GRAPH_ACCESS_TOKEN`, `TEAMS_TEAM_ID`/`_CHANNEL_ID`/`_CHAT_ID`).
- **LINE** — `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_CHANNEL_SECRET` (HMAC-SHA256 webhook verification), `LINE_HOST`/`_PORT`/`_PUBLIC_URL`, allowlists (`LINE_ALLOWED_USERS`/`_GROUPS`/`_ROOMS`), `LINE_HOME_CHANNEL`, and the slow-LLM postback button knobs (`LINE_SLOW_RESPONSE_THRESHOLD`, `LINE_PENDING_TEXT`, `LINE_BUTTON_LABEL`, `LINE_DELIVERED_TEXT`, `LINE_INTERRUPTED_TEXT`).
- **ntfy** — `NTFY_TOPIC` (required), `NTFY_SERVER_URL`, `NTFY_TOKEN`, `NTFY_PUBLISH_TOPIC`, `NTFY_MARKDOWN`, `NTFY_ALLOWED_USERS`/`ALLOW_ALL_USERS`, `NTFY_HOME_CHANNEL`(`_NAME`).

### Advanced Messaging Tuning

The `HERMES_<PLATFORM>_TEXT_BATCH_DELAY_SECONDS` / `_SPLIT_DELAY_SECONDS` family throttles the outbound batcher per platform (Telegram, Discord, Matrix, Feishu, WeCom), with Telegram HTTP-timeout/pool overrides and Feishu `_MAX_CHARS`/`_MAX_MESSAGES`/dedup-cache knobs. Defaults respect each platform's rate limits, so most users never set these. This section also carries cross-cutting gateway-runtime vars: `HERMES_VISION_DOWNLOAD_TIMEOUT`, `HERMES_RESTART_DRAIN_TIMEOUT`, `HERMES_GATEWAY_PLATFORM_CONNECT_TIMEOUT`, `HERMES_GATEWAY_BUSY_INPUT_MODE`/`_BUSY_ACK_ENABLED`, the s6-supervision controls `HERMES_GATEWAY_NO_SUPERVISE`/`_BOOTSTRAP_STATE`, `HERMES_FILE_MUTATION_VERIFIER`, and the cron-runner limits `HERMES_CRON_TIMEOUT`/`_SCRIPT_TIMEOUT`/`_MAX_PARALLEL`.

## Agent Behavior, Interface & Session

`Agent Behavior` is the largest behavior cluster. Iteration/model: `HERMES_MAX_ITERATIONS` (default 90), `HERMES_INFERENCE_MODEL` (per-session model override, also `-m`/`--model`). Safety/approval flags: `HERMES_YOLO_MODE` (bypass dangerous-command approval), `HERMES_ACCEPT_HOOKS`, `HERMES_IGNORE_USER_CONFIG`, `HERMES_IGNORE_RULES`, `HERMES_SAFE_MODE` (disable all customizations), `HERMES_EXEC_ASK`, `HERMES_ALLOW_PRIVATE_URLS`, `HERMES_REDACT_SECRETS` (default `true`), `HERMES_WRITE_SAFE_ROOT`, `HERMES_DISABLE_FILE_STATE_GUARD`. Timeouts: `HERMES_API_TIMEOUT` (1800s), `HERMES_API_CALL_STALE_TIMEOUT`, `HERMES_STREAM_READ_TIMEOUT`/`_STALE_TIMEOUT`/`HERMES_STREAM_RETRIES`, `HERMES_AGENT_TIMEOUT`(`_WARNING`)/`HERMES_AGENT_NOTIFY_INTERVAL`, `HERMES_CHECKPOINT_TIMEOUT`. Tool/skill overrides: `HERMES_CORE_TOOLS`, `HERMES_BUNDLED_SKILLS`, `HERMES_OPTIONAL_SKILLS`, `DELEGATION_MAX_CONCURRENT_CHILDREN` (default 3). Rules-file injection (`HERMES_MD_NAMES`), prompt injection (`HERMES_EPHEMERAL_SYSTEM_PROMPT`, `HERMES_PREFILL_MESSAGES_FILE`, `HERMES_AGENT_HELP_GUIDANCE`), human-delay pacing (`HERMES_HUMAN_DELAY_MODE`/`_MIN_MS`/`_MAX_MS`), and tracing/debug (`HERMES_DUMP_REQUESTS`, `HERMES_OAUTH_TRACE`, `HERMES_PLUGINS_DEBUG`) round it out.

`Interface`: `HERMES_TUI` (launch TUI, `=1`), `HERMES_TUI_DIR`, `HERMES_TUI_RESUME`, `HERMES_TUI_THEME`. `Session Settings`: `SESSION_IDLE_MINUTES` (default 1440), `SESSION_RESET_HOUR` (default 4 = 4am), and `HERMES_SESSION_ID` — auto-exported into every tool subprocess (you should **not** set it manually).

## Config-Only Sections: Compression, Fallback, Routing

Three blocks have **no environment variables** and are set only in `config.yaml`. **Context Compression** lives in the `compression:` block (threshold, target_ratio, protect_last_n; the summarization model under `auxiliary.compression.*`):

```yaml
compression:
  enabled: true
  threshold: 0.50
  target_ratio: 0.20         # fraction of threshold to preserve as recent tail
  protect_last_n: 20         # minimum recent messages to keep uncompressed
```

**Fallback Providers** is a top-level list enabling automatic failover when the main model errors (auxiliary `auto` tasks also consult it):

```yaml
fallback_providers:
  - provider: openrouter
    model: anthropic/claude-sonnet-4
```

**Provider Routing** goes under `provider_routing` with keys `sort` (`price`/`throughput`/`latency`), `only`/`ignore`/`order` (provider-slug lists), `require_parameters`, and `data_collection` (`allow`/`deny`). The one **Auxiliary Task Override** block that *is* env-driven covers vision and web-extract sub-tasks: `AUXILIARY_VISION_PROVIDER`/`_MODEL`/`_BASE_URL`/`_API_KEY` and `AUXILIARY_WEB_EXTRACT_PROVIDER`/`_MODEL`/`_BASE_URL`/`_API_KEY` (Hermes falls back to the task key or `OPENAI_API_KEY`, never `OPENROUTER_API_KEY`, for these custom endpoints).

**Source**: `inbox/hermes_agent_docs/reference/environment-variables.md` · https://hermes-agent.nousresearch.com/docs/reference/environment-variables
**Last Updated**: 2026-06-19
**Status**: Active
