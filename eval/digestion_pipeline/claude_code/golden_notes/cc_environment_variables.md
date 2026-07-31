---
tags:
  - resource
  - documentation
  - claude_code
  - configuration
  - environment_variables
keywords:
  - environment variables
  - env key settings json
  - anthropic_model
  - claude_code_oauth_token
  - api_timeout_ms
  - mcp_timeout
  - claude_code_enable_telemetry
  - env-var precedence
  - provider selection variables
  - behavior toggles
topics:
  - Claude Code
  - Settings & Environment Variables
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/env-vars
access_control_group: ["general"]
---

# Claude Code — Environment Variables

## Overview

Environment variables control Claude Code behavior such as model selection, authentication, request routing, and feature toggles. Many of the same behaviors can also be configured through a `settings.json` field, a CLI flag, or an in-session command like `/model`. This note covers **how and where to set environment variables** (shell vs. the settings `env` key), **how precedence resolves** when a behavior can be set more than one way, and a **purpose-grouped tour of the ~250-variable reference** (model/auth/provider, API/timeout/streaming, behavior toggles, telemetry/OTel, and MCP/subagent/plugin). Deep per-domain semantics are linked to their owning pages: model variables to [Model configuration](https://code.claude.com/docs/en/model-config), telemetry to [Monitoring](https://code.claude.com/docs/en/monitoring-usage), and provider variables to the per-provider pages (Bedrock, Vertex AI, Foundry, Claude Platform on AWS).

## Set environment variables

A variable you set in your shell lasts for that terminal session, while a variable in a settings file applies every time `claude` runs.

### In your shell

Set the variable before launching `claude`:

```bash
export API_TIMEOUT_MS="1200000"
claude
```

To set it for every session, add the `export` line to `~/.bashrc`, `~/.zshrc`, or your shell's profile file. On Windows PowerShell use `$env:API_TIMEOUT_MS = "1200000"` (persist with `[Environment]::SetEnvironmentVariable(...)`); on Windows CMD use `set API_TIMEOUT_MS=1200000` (persist with `setx`).

### In settings files

Add variables under the `env` key in a `settings.json` file. Claude Code reads them directly from the file at startup, so they take effect no matter how `claude` was launched:

```json
{
  "env": {
    "API_TIMEOUT_MS": "1200000",
    "BASH_DEFAULT_TIMEOUT_MS": "300000"
  }
}
```

The file you choose controls who the variables apply to: `~/.claude/settings.json` applies to you in every project; `.claude/settings.json` applies to everyone working in the project (checked into source control); `.claude/settings.local.json` applies to you in this project only (add to gitignore if hand-created); and **managed settings** apply to everyone in your organization (deployed by an admin). See [cc_settings_files](cc_settings_files.md) for where each file lives and [cc_settings_scopes_and_precedence](cc_settings_scopes_and_precedence.md) for how they combine when more than one sets the same variable. The `env` key itself is documented as a `settings.json` field in [cc_settings_reference](cc_settings_reference.md).

## Precedence

Where the same behavior has both an environment variable and a settings field, **the environment variable takes precedence**. For example, `ANTHROPIC_MODEL` overrides the `model` setting, and `CLAUDE_CODE_AUTO_CONNECT_IDE` overrides `autoConnectIde`. The settings field applies when the environment variable is not set.

How an environment variable interacts with CLI flags and in-session commands **varies per feature**: `--model` and `/model` override `ANTHROPIC_MODEL`, while `CLAUDE_CODE_EFFORT_LEVEL` overrides `/effort`. When a variable interacts with another configuration source, its row in the Variables reference states the precedence or links to the page that documents it. Claude Code reads environment variables at startup, so changes take effect the next time you launch `claude`.

## Variables (purpose-grouped reference)

The full reference is one alphabetical table of ~250 variables; below it is regrouped by purpose. Each entry states the variable's purpose verbatim per source; repeated model-alias variants are folded into prose. For the canonical alphabetical list see the [environment variables reference](https://code.claude.com/docs/en/env-vars).

### Model selection, aliases, and effort

- `ANTHROPIC_MODEL` — name of the model setting to use (overrides the `model` setting; `--model`/`/model` override it). See [Model configuration](https://code.claude.com/docs/en/model-config).
- `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU,FABLE}_MODEL` — pin the model used for each class; each has `_NAME`, `_DESCRIPTION`, and `_SUPPORTED_CAPABILITIES` variants that customize the picker display.
- `ANTHROPIC_CUSTOM_MODEL_OPTION` (+ `_NAME`, `_DESCRIPTION`, `_SUPPORTED_CAPABILITIES`) — add a non-standard or gateway-specific model as a selectable `/model` entry without replacing built-in aliases.
- `ANTHROPIC_SMALL_FAST_MODEL` — `[DEPRECATED]` name of the Haiku-class model for background tasks; `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` overrides its AWS region on Bedrock/Mantle.
- `CLAUDE_CODE_EFFORT_LEVEL` / `CLAUDE_EFFORT` — effort level (`low`, `medium`, `high`, `xhigh`, `max`, or `auto`); takes precedence over `/effort` and the `effortLevel` setting.
- `MAX_THINKING_TOKENS` — override the extended-thinking token budget (ceiling is the model's max output tokens minus one); `0` disables thinking on the Anthropic API (except Fable 5). `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` falls back to this fixed budget; `CLAUDE_CODE_DISABLE_THINKING`/`DISABLE_INTERLEAVED_THINKING` are gateway-compat toggles.
- `CLAUDE_CODE_MAX_OUTPUT_TOKENS` — max output tokens for most requests (increasing it reduces the effective context window before auto-compaction).
- `FALLBACK_FOR_ALL_PRIMARY_MODELS` — make all models (not only Opus) stop retrying on repeated-overload errors when no fallback is configured; superseded by a configured fallback chain as of v2.1.160.

### Authentication and OAuth

- `ANTHROPIC_API_KEY` — API key sent as `X-Api-Key`; when set it is used instead of your subscription. In non-interactive mode (`-p`) it is always used when present; interactively you approve it once. `unset ANTHROPIC_API_KEY` to revert to your subscription.
- `ANTHROPIC_AUTH_TOKEN` — custom `Authorization` header value (prefixed with `Bearer `).
- `CLAUDE_CODE_OAUTH_TOKEN` — OAuth access token for Claude.ai auth (alternative to `/login`); takes precedence over keychain-stored credentials. Generate with `claude setup-token`.
- `CLAUDE_CODE_OAUTH_REFRESH_TOKEN` — OAuth refresh token; when set, `claude auth login` exchanges it directly instead of opening a browser. Requires `CLAUDE_CODE_OAUTH_SCOPES` (space-separated scopes the refresh token was issued with). Useful for provisioning auth in automated environments.
- `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` — interval at which credentials from `apiKeyHelper` are refreshed.
- mTLS: `CLAUDE_CODE_CLIENT_CERT`, `CLAUDE_CODE_CLIENT_KEY`, `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`; CA sources via `CLAUDE_CODE_CERT_STORE` (default `bundled,system`).

### Provider selection, endpoints, and routing

- Provider toggles: `CLAUDE_CODE_USE_BEDROCK` (Bedrock), `CLAUDE_CODE_USE_VERTEX` (Vertex), `CLAUDE_CODE_USE_FOUNDRY` (Microsoft Foundry), `CLAUDE_CODE_USE_ANTHROPIC_AWS` (Claude Platform on AWS), `CLAUDE_CODE_USE_MANTLE` (Bedrock Mantle).
- Endpoint overrides: `ANTHROPIC_BASE_URL` (route through a proxy/gateway; on a non-first-party host MCP tool search is disabled unless `ENABLE_TOOL_SEARCH=true`), plus per-provider `ANTHROPIC_BEDROCK_BASE_URL`, `ANTHROPIC_VERTEX_BASE_URL`, `ANTHROPIC_FOUNDRY_BASE_URL`, `ANTHROPIC_AWS_BASE_URL`, `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`.
- Provider auth/IDs: `AWS_BEARER_TOKEN_BEDROCK`, `ANTHROPIC_AWS_API_KEY` / `ANTHROPIC_AWS_WORKSPACE_ID`, `ANTHROPIC_FOUNDRY_API_KEY` / `ANTHROPIC_FOUNDRY_RESOURCE`, `ANTHROPIC_VERTEX_PROJECT_ID`, `ANTHROPIC_WORKSPACE_ID`; `CLAUDE_CODE_SKIP_{BEDROCK,VERTEX,FOUNDRY,MANTLE,ANTHROPIC_AWS}_AUTH` skip provider auth.
- Request shaping: `ANTHROPIC_CUSTOM_HEADERS`, `ANTHROPIC_BETAS`, `CLAUDE_CODE_EXTRA_BODY` (JSON merged into every request body), `ANTHROPIC_BEDROCK_SERVICE_TIER`.
- `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` — set by embedding host platforms; makes provider-selection/endpoint/auth variables in settings files (e.g. `CLAUDE_CODE_USE_BEDROCK`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`) be ignored so user settings cannot override the host's routing.
- Vertex region pins: `VERTEX_REGION_CLAUDE_*` (one per model, e.g. `VERTEX_REGION_CLAUDE_4_8_OPUS`, `VERTEX_REGION_CLAUDE_FABLE_5`).
- Network: `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`.

### API timeouts, retries, and streaming

- `API_TIMEOUT_MS` — timeout for API requests (default 600000 / 10 min; max 2147483647; values above the max overflow and fail immediately).
- `CLAUDE_CODE_MAX_RETRIES` — retries for failed API requests (default 10).
- `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY` — max read-only tools and subagents in parallel (default 10).
- `CLAUDE_CODE_MAX_TURNS` — cap agentic turns when no explicit limit is passed (`--max-turns` takes precedence; a non-positive-integer value is rejected at startup).
- Bash: `BASH_DEFAULT_TIMEOUT_MS` (default 120000), `BASH_MAX_TIMEOUT_MS` (default 600000), `BASH_MAX_OUTPUT_LENGTH`.
- Streaming watchdogs: `API_FORCE_IDLE_TIMEOUT` (override the 5-minute idle timeout that aborts a stalled stream; `0` disables, `1` keeps it on every provider — as of v2.1.169), `CLAUDE_ENABLE_BYTE_WATCHDOG` / `CLAUDE_ENABLE_BYTE_WATCHDOG_BEDROCK` / `CLAUDE_ENABLE_STREAM_WATCHDOG`, and `CLAUDE_STREAM_IDLE_TIMEOUT_MS` (timeout before the watchdog closes a stalled connection; explicit minimum 300000).
- Prompt caching: `DISABLE_PROMPT_CACHING` (+ per-model `_OPUS`/`_SONNET`/`_HAIKU`/`_FABLE`), `ENABLE_PROMPT_CACHING_1H` (1-hour TTL), `FORCE_PROMPT_CACHING_5M`.

### Context and compaction

- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` — percentage (1–100) of the auto-compaction window at which compaction triggers (can only lower the threshold; applies to main conversations and subagents).
- `CLAUDE_CODE_AUTO_COMPACT_WINDOW` — context capacity in tokens used for auto-compaction calculations (defaults to the model's context window; capped at the actual window).
- `DISABLE_AUTO_COMPACT` — disable automatic compaction near the context limit (manual `/compact` remains).
- `DISABLE_COMPACT` — disable all compaction (both automatic and the manual `/compact` command).
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS` — override the assumed context-window size (only takes effect when `DISABLE_COMPACT` is also set).

### Subagents, tasks, and agent teams

- `CLAUDE_CODE_SUBAGENT_MODEL` — model for subagents (see Model configuration).
- `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` — stall timeout for background subagents (default 600000; timer resets on each streaming progress event, then the subagent is aborted and the task marked failed).
- `TASK_MAX_OUTPUT_LENGTH` — max characters in subagent output before truncation (default 32000, max 160000; full output saved to disk).
- `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` — disable built-in subagent types (e.g. Explore, Plan); applies only in non-interactive mode.
- `CLAUDE_CODE_ENABLE_TASKS` — use structured Task tools (`TaskCreate`/`TaskUpdate`/`TaskGet`/`TaskList`) vs. legacy `TodoWrite` (Task tools default as of v2.1.142; `0` reverts). Also `CLAUDE_AUTO_BACKGROUND_TASKS`, `CLAUDE_CODE_FORK_SUBAGENT`, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`.

### MCP servers and tool search

- `MCP_TIMEOUT` — MCP server startup timeout (default 30000 / 30 s).
- `MCP_TOOL_TIMEOUT` — MCP tool execution timeout (default 100000000, ~28 h; a per-server `timeout` in `.mcp.json` overrides it).
- `MCP_CONNECTION_NONBLOCKING` — whether startup waits for MCP servers before the first query (non-blocking by default as of v2.1.142; `0` restores the blocking 5-second wait). `MCP_CONNECT_TIMEOUT_MS` bounds that blocking wait.
- `MAX_MCP_OUTPUT_TOKENS` — max tokens in MCP tool responses (default 25000; warns above 10,000).
- `ENABLE_TOOL_SEARCH` — controls MCP tool search (`true` always defer + send the beta header, `auto`/`auto:N` threshold mode, `false` load all upfront).
- Batching/transport: `MCP_SERVER_CONNECTION_BATCH_SIZE`, `MCP_REMOTE_SERVER_CONNECTION_BATCH_SIZE`, `MCP_OAUTH_CALLBACK_PORT`, `MCP_CLIENT_SECRET`, `ENABLE_CLAUDEAI_MCP_SERVERS`, `CLAUDE_AGENT_SDK_MCP_NO_PREFIX`, `CLAUDE_CODE_MCP_ALLOWLIST_ENV`.

### Telemetry and OpenTelemetry

- `CLAUDE_CODE_ENABLE_TELEMETRY` — enable OpenTelemetry collection for metrics and logging (required before configuring OTel exporters).
- `DISABLE_TELEMETRY` — opt out of telemetry (events never include user data like code, file paths, or bash commands; also disables feature-flag fetching, same effect as `DISABLE_GROWTHBOOK`).
- `DO_NOT_TRACK` — opt out of telemetry; equivalent to `DISABLE_TELEMETRY` (the cross-tool convention honored by many CLIs).
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` — equivalent to setting `DISABLE_AUTOUPDATER`, `DISABLE_FEEDBACK_COMMAND`, `DISABLE_ERROR_REPORTING`, and `DISABLE_TELEMETRY`.
- Content logging (off by default): `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_CONTENT`, `OTEL_LOG_TOOL_DETAILS`, `OTEL_LOG_RAW_API_BODIES`; metric attributes via `OTEL_METRICS_INCLUDE_*`; flush/shutdown via `CLAUDE_CODE_OTEL_FLUSH_TIMEOUT_MS`, `CLAUDE_CODE_OTEL_SHUTDOWN_TIMEOUT_MS`, `CLAUDE_CODE_PROPAGATE_TRACEPARENT`. Standard OTel exporter variables (`OTEL_METRICS_EXPORTER`, `OTEL_LOGS_EXPORTER`, `OTEL_EXPORTER_OTLP_ENDPOINT`, etc.) are also supported. See [Monitoring](https://code.claude.com/docs/en/monitoring-usage).

### Behavior toggles, environment, and tooling

- Config/env: `CLAUDE_CONFIG_DIR` (override `~/.claude`; all settings/credentials/history/plugins live there — useful for side-by-side accounts), `CLAUDE_ENV_FILE` (a shell script run before each Bash command so its exports are visible; also populated by `SessionStart`/`Setup`/`CwdChanged`/`FileChanged` hooks), `CLAUDE_CODE_TMPDIR`, `CLAUDE_CODE_SHELL`, `CLAUDE_CODE_SHELL_PREFIX`.
- Memory/context loading: `CLAUDE_CODE_DISABLE_CLAUDE_MDS`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`, `CLAUDE_CODE_DISABLE_ATTACHMENTS`.
- Customization/skills/plugins: `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`, `CLAUDE_CODE_DISABLE_POLICY_SKILLS`, `CLAUDE_CODE_SYNC_SKILLS`, `CLAUDE_CODE_DISABLE_WORKFLOWS`, plus the `CLAUDE_CODE_PLUGIN_*` family (cache/seed dirs, git timeout, HTTPS preference) and `FORCE_AUTOUPDATE_PLUGINS`.
- Subprocess detection: `CLAUDECODE` (set to `1` in spawned subprocesses, also by IDE terminals), `CLAUDE_CODE_CHILD_SESSION` (only Claude Code's own spawn path; distinguishes nested sessions), `CLAUDE_CODE_SESSION_ID`, `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`.
- Debug/diagnostics: `DEBUG`, `CLAUDE_CODE_DEBUG_LOGS_DIR`, `CLAUDE_CODE_DEBUG_LOG_LEVEL`, `IS_DEMO`, `USE_BUILTIN_RIPGREP`.
- Feature/UI: `CLAUDE_CODE_AUTO_CONNECT_IDE` (overrides the `autoConnectIde` global config), fullscreen/rendering toggles (`CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`, `CLAUDE_CODE_NO_FLICKER`, etc.), and the disable-command family (`DISABLE_AUTOUPDATER`, `DISABLE_DOCTOR_COMMAND`, `DISABLE_COST_WARNINGS`, and similar).

## See also

- [Settings](https://code.claude.com/docs/en/settings): all `settings.json` configuration, including the `env` key
- [CLI reference](https://code.claude.com/docs/en/cli-reference): launch-time flags
- [Network configuration](https://code.claude.com/docs/en/network-config): proxy and TLS setup
- [Monitoring](https://code.claude.com/docs/en/monitoring-usage): OpenTelemetry configuration

**Source**: https://code.claude.com/docs/en/env-vars
**Last Updated**: 2026-06-13
**Status**: Active
