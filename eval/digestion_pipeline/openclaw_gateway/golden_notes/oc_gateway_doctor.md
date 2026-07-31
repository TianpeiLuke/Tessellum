---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - doctor
keywords:
  - openclaw doctor
  - config migration repair tool
  - doctor --fix --lint --yes
  - read-only lint mode ci preflight
  - legacy config key migrations
  - session lock transcript repair
  - model auth health oauth expiry
  - dreams ui backfill reset
topics:
  - OpenClaw
  - Gateway Doctor
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/doctor
access_control_group: ["general"]
---

# OpenClaw — `openclaw doctor` Repair and Migration Tool

## Overview

This note is the procedure for `openclaw doctor`, the repair + migration tool that fixes stale config/state, checks health, and provides actionable repair steps for an OpenClaw Gateway. It mirrors the `gateway/doctor` source page: the quick-start invocation plus the headless/automation modes, the read-only lint mode contract (modes table, JSON output fields, exit codes, severity/scoping flags), the "What it does" check/migration catalog summarized across six areas, the Control-UI Dreams backfill/reset actions (doctor-style RPC, not CLI doctor), and the detailed behavior for the numbered config/state/gateway/auth checks. `doctor` is the recovery path when strict config validation refuses to start the gateway.

## Quick start

The base command runs interactively, performing health checks and prompting before any change:

```bash
openclaw doctor
```

To review changes before writing, open the config file first with `cat ~/.openclaw/openclaw.json`.

### Headless and automation modes

`doctor` exposes mode flags for non-interactive and CI use. Each is a documented `openclaw doctor` invocation:

- `--yes` — accept defaults without prompting (including restart/service/sandbox repair steps when applicable).
- `--fix` — apply recommended repairs without prompting (repairs + restarts where safe); `--repair` is an alias.
- `--lint` — run structured health checks for CI or preflight automation. This mode is read-only: it does not prompt, repair, migrate config, restart services, or touch state.
- `--fix --force` — apply aggressive repairs too (overwrites custom supervisor configs).
- `--non-interactive` — run without prompts and only apply safe migrations (config normalization + on-disk state moves); skips restart/service/sandbox actions that require human confirmation. Legacy state migrations run automatically when detected.
- `--deep` — scan system services for extra gateway installs (launchd/systemd/schtasks).

## Read-only lint mode

`openclaw doctor --lint` is the automation-friendly sibling of `openclaw doctor --fix`. Both use doctor health checks, but their posture differs across three modes:

| Mode | Prompts | Writes config/state | Output | Use it for |
| --- | --- | --- | --- | --- |
| `openclaw doctor` | yes | no | friendly health report | a human checking status |
| `openclaw doctor --fix` | sometimes | yes, with repair policy | friendly repair log | applying approved repairs |
| `openclaw doctor --lint` | no | no | structured findings | CI, preflight, and review gates |

Modernized health checks may provide an optional `repair()` implementation; `doctor --fix` applies those repairs when they exist and otherwise uses the existing repair flow for checks not yet migrated. The structured repair contract separates reporting from detection: `detect()` reports findings, while `repair()` can report changes, config/file diffs, and non-file side effects — keeping the path open for a future `doctor --fix --dry-run` and diff output without making lint checks plan mutations.

Lint JSON output includes: `ok` (any visible finding met the threshold), `checksRun`, `checksSkipped` (skipped by `--only`/`--skip`), and `findings` (diagnostics with `checkId`, `severity`, `message`, and optional `path`, `line`, `column`, `ocPath`, `fixHint`). Exit codes: `0` (no findings at/above threshold), `1` (findings met the threshold), `2` (runtime failure before findings could emit). Use `--severity-min info|warning|error` to control print + non-zero exit, `--only <id>` for narrow preflight gates, and `--skip <id>` to exclude a noisy check. These lint-output options (`--json`, `--severity-min`, `--only`, `--skip`) must be paired with `--lint`; regular doctor and repair runs reject them.

```bash
openclaw doctor --lint
openclaw doctor --lint --severity-min warning
openclaw doctor --lint --json
openclaw doctor --lint --only core/doctor/gateway-config --json
```

## What it does (summary)

The source page groups doctor's checks into six accordion areas; this is the BB-specific summary catalog (not a field-by-field reproduction).

- **Health, UI, and updates** — optional pre-flight update for git installs (interactive only); UI protocol freshness check; health check + restart prompt; skills + plugin status summary.
- **Config and migrations** — config normalization for legacy values; Talk config migration from legacy flat `talk.*` into `talk.provider` + `talk.providers.<provider>`; browser/Chrome MCP migration checks; OpenCode provider override warnings (`models.providers.opencode` / `models.providers.opencode-go`); legacy OpenAI Codex provider/profile migration (`openai-codex` → `openai`); OAuth TLS prerequisites check for Codex OAuth profiles; plugin/tool allowlist warnings when `plugins.allow` is restrictive; legacy on-disk state migration (sessions/agent dir/WhatsApp auth); plugin manifest contract-key migration (`*Providers` → `contracts`); cron store migration; legacy whole-agent runtime-policy cleanup; stale plugin config cleanup (preserved as inert when `plugins.enabled=false`).
- **State and integrity** — session lock inspection + stale lock cleanup; transcript repair for duplicated prompt-rewrite branches from `2026.4.24` builds; wedged subagent restart-recovery tombstone detection; state integrity + permissions checks; config file permission checks (chmod 600); model auth health (OAuth expiry/refresh/cooldown); extra workspace dir detection (`~/openclaw`).
- **Gateway, services, and supervisors** — sandbox image repair; legacy service migration + extra gateway detection; Matrix legacy state migration (`--fix`/`--repair`); gateway runtime checks; channel status warnings; WhatsApp responsiveness checks; Codex route repair for legacy `openai-codex/*` refs; supervisor config audit (launchd/systemd/schtasks); embedded proxy env cleanup (`HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY`); runtime best-practice checks (Node vs Bun); gateway port collision diagnostics (default `18789`). Channel-specific permission checks live under `openclaw channels capabilities`.
- **Auth, security, and pairing** — security warnings for open DM policies; gateway auth checks for local token mode (offers token generation; does not overwrite token `SecretRef`); device pairing trouble detection (pending requests, role/scope upgrades, token/identity drift).
- **Workspace and shell** — systemd linger check (Linux); bootstrap file size check; skills readiness check (`--fix` can disable unavailable skills in `skills.entries`); shell completion check/install; memory search embedding readiness check; source install checks; writes updated config + wizard metadata.

## Dreams UI backfill and reset

The Control UI Dreams scene includes **Backfill**, **Reset**, and **Clear Grounded** actions for the grounded dreaming workflow. These use gateway doctor-style RPC methods, but they are **not** part of `openclaw doctor` CLI repair/migration. **Backfill** scans historical `memory/YYYY-MM-DD.md` files in the active workspace, runs the grounded REM diary pass, and writes reversible backfill entries into `DREAMS.md`. **Reset** removes only those marked backfill diary entries from `DREAMS.md`. **Clear Grounded** removes only staged grounded-only short-term entries that came from historical replay and have not accumulated live recall or daily support yet.

By themselves these actions do **not** edit `MEMORY.md`, do not run full doctor migrations, and do not automatically stage grounded candidates into the live short-term promotion store unless you explicitly run the staged CLI path first. To let grounded historical replay influence the normal deep promotion lane, use the CLI flow instead, which stages grounded durable candidates into the short-term dreaming store while keeping `DREAMS.md` as the review surface:

```bash
openclaw memory rem-backfill --path ./memory --stage-short-term
```

## Detailed behavior and rationale

The source page documents numbered checks (0–19, with lettered sub-checks). This section captures their load-bearing behavior, keeping config keys verbatim.

**0. Optional update (git installs)** — for a git checkout running interactively, doctor offers to update (fetch/rebase/build) before running.

**1. Config normalization** — legacy value shapes (e.g. `messages.ackReaction` without a channel-specific override) are normalized into the current schema, including legacy Talk flat fields: doctor rewrites old `talk.voiceId` / `talk.voiceAliases` / `talk.modelId` / `talk.outputFormat` / `talk.apiKey` into `talk.provider` + `talk.providers.<provider>`, and legacy realtime selectors (`talk.mode`, `talk.transport`, `talk.brain`, `talk.model`, `talk.voice`) into `talk.realtime`. It also warns when `plugins.allow` is non-empty and tool policy uses wildcard or plugin-owned entries: `tools.allow: ["*"]` only matches tools from plugins that actually load and does not bypass the exclusive plugin allowlist.

**2. Legacy config key migrations** — when the config contains deprecated keys, other commands refuse to run and ask you to run `openclaw doctor`; doctor explains the legacy keys found, shows the migration, and rewrites `~/.openclaw/openclaw.json`. Gateway startup refuses legacy formats and asks you to run `openclaw doctor --fix` (it does not rewrite `openclaw.json` on startup). Sample migrations: `routing.allowFrom` → `channels.whatsapp.allowFrom`; `routing.queue` → `messages.queue`; `routing.bindings` → top-level `bindings`; `routing.agents`/`routing.defaultAgentId` → `agents.list` + `agents.list[].default`; `routing.agentToAgent` → `tools.agentToAgent`; `identity` → `agents.list[].identity`; `agent.*` → `agents.defaults` + `tools.*`; remove `agents.defaults.llm`; `browser.profiles.*.driver: "extension"` → `"existing-session"`; `models.providers.*.api: "openai"` → `"openai-completions"`; remove retired `channels.webchat`/`gateway.webchat`. Multi-account guidance warns when `channels.<channel>.accounts` lack `defaultAccount`/`accounts.default` or `defaultAccount` names an unknown ID.

**2b–2g (config sub-checks)** — **2b** warns when `models.providers.opencode`/`opencode-zen`/`opencode-go` overrides shadow the built-in OpenCode catalog from `openclaw/plugin-sdk/llm`. **2c** normalizes removed-Chrome-extension browser config to host-local Chrome MCP attach (`driver: "extension"` → `"existing-session"`, removes `browser.relayBindHost`), warns below Chrome 144, and checks remote-debugging readiness (doctor cannot enable the Chrome-side setting). **2d** probes the OpenAI authorization endpoint for Codex OAuth profiles to verify the local Node/OpenSSL TLS stack (e.g. macOS Homebrew Node fix `brew postinstall ca-certificates`; `--deep` runs even if healthy). **2e** warns about legacy transport settings under `models.providers.openai-codex` that shadow the built-in Codex OAuth path. **2f** Codex route repair: `--fix`/`--repair` rewrites `openai-codex/gpt-*` → `openai/gpt-*` across primary/fallback/image/video models, heartbeat/subagent/compaction overrides, hooks, channel overrides, and session route pins; moves intent to `agentRuntime.id: "codex"` and migrates `openai-codex:*` auth profiles to `openai:*`. **2g** clears auto-created stale session route state (e.g. `modelOverrideSource: "auto"` pins) when the owning route is gone; explicit user/legacy choices are reported but left untouched.

**3. Legacy state migrations (disk layout)** — best-effort, idempotent moves: sessions+transcripts from `~/.openclaw/sessions/` to `~/.openclaw/agents/<agentId>/sessions/`; agent dir from `~/.openclaw/agent/` to `~/.openclaw/agents/<agentId>/agent/`; WhatsApp auth (Baileys) from `~/.openclaw/credentials/*.json` (except `oauth.json`) to `~/.openclaw/credentials/whatsapp/<accountId>/...`. WhatsApp auth migrates only via doctor. **3a** moves deprecated plugin-manifest capability keys (`speechProviders`, `realtimeTranscriptionProviders`, `realtimeVoiceProviders`, `mediaUnderstandingProviders`, `imageGenerationProviders`, `videoGenerationProviders`, `webFetchProviders`, `webSearchProviders`) into `contracts`. **3b** migrates the cron store (`~/.openclaw/cron/jobs.json` or `cron.store`): `jobId` → `id`, `schedule.cron` → `schedule.expr`, top-level payload/delivery fields → `payload`/`delivery`, `notify: true` fallback jobs → explicit webhook delivery from `cron.webhook`; malformed rows are quarantined to `jobs-quarantine.json`. **3c** reports + removes stale session write-lock files (dead/orphaned/recycled/malformed-old/non-OpenClaw owners) in `--fix`/`--repair`, leaving live OpenClaw-owned locks. **3d** repairs the duplicated transcript branch shape from the `2026.4.24` rewrite bug, backing up each JSONL file.

**4. State integrity checks** — the state directory is the operational brainstem. Doctor warns on: state dir missing; state dir permissions (offers repair + `chown` hint); macOS cloud-synced state dir (iCloud Drive / `~/Library/CloudStorage/...`); Linux SD/eMMC state dir (`mmcblk*`); Linux volatile state dir (`tmpfs`/`ramfs` — Docker `overlay` is not flagged); session dirs missing (`ENOENT` risk); transcript mismatch; main session "1-line JSONL"; multiple state dirs (`~/.openclaw` / `OPENCLAW_STATE_DIR`); remote-mode reminder (`gateway.mode=remote`); config file permissions (tighten to `600`).

**5. Model auth health (OAuth expiry)** — inspects auth-store OAuth profiles, warns on expiring/expired tokens and refreshes when safe (refresh prompts TTY-only; `--non-interactive` skips). On permanent failure (`refresh_token_reused`, `invalid_grant`) it prints the exact `openclaw models auth login --provider ...` command. Reports profiles unusable via short cooldowns (rate limits/timeouts) or longer disables (billing/credit). macOS Keychain legacy Codex OAuth tokens migrate inline into `auth-profiles.json` only via `openclaw doctor --fix`.

**6–11 (validation, sandbox, plugins, services, workspace)** — **6** validates `hooks.gmail.model` against the catalog/allowlist. **7** repairs/builds Docker sandbox images. **7b** removes legacy plugin dependency staging state in `--fix`/`--repair`, relinks the host `openclaw` package into managed plugins declaring `peerDependencies.openclaw`, and reinstalls missing downloadable plugins. **8** detects legacy gateway services and offers cleanup/install on the current port. **8b** runs startup Matrix migration in `--fix`/`--repair` (skipped read-only). **8c** inspects device-pairing state and prints exact next steps (`openclaw devices list`/`approve <requestId>`/`rotate --device <deviceId> --role <role>`/`remove <deviceId>`) without auto-approving or auto-rotating. **9** warns on open DM policies. **10** ensures systemd lingering. **11** prints workspace status; **11b** checks bootstrap size vs `agents.defaults.bootstrapMaxChars`/`bootstrapTotalMaxChars`; **11d** removes dangling channel config when `--fix` removes a missing channel plugin; **11c** checks/installs shell completion (`openclaw completion --write-state`).

**12–19 (gateway auth, health, supervisor, runtime, finalize)** — **12** checks local gateway token auth (offers generation; does not overwrite `gateway.auth.token` SecretRef; `openclaw doctor --generate-gateway-token` forces generation only when no token SecretRef exists). **12b** uses a read-only SecretRef summary for targeted repairs (e.g. Telegram `allowFrom` `@username`). **13** health check + restart offer; **13b** memory-search embedding readiness (QMD binary / local model / remote provider key / legacy `memorySearch.provider: "auto"` rewritten to `"openai"`; verify with `openclaw memory status --deep`). **14** channel status probe when healthy. **15** audits supervisor config (launchd/systemd/schtasks): `--yes` accepts defaults, `--fix` applies without prompts (`--repair` alias), `--fix --force` overwrites custom configs, and `OPENCLAW_SERVICE_REPAIR_POLICY=external` keeps doctor read-only for the service lifecycle. **16** inspects service runtime + port collisions (default `18789`). **17** warns on Bun / version-managed Node paths and offers migration to system Node. **18** persists config + wizard metadata. **19** suggests a workspace memory system + git backup.

## Related Notes

**Terms**

- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — the gateway product; relevance: the product `doctor` repairs/migrates.
- **[JSON Schema](../../term_dictionary/term_json_schema.md)** — schema validation; relevance: doctor diagnoses/fixes the validation failures that block startup.
- **[Health Check](../../term_dictionary/term_health_check.md)** — liveness probe; relevance: the health check + restart prompt doctor runs.
- **[OAuth Token](../../term_dictionary/term_oauth_token.md)** — credential token; relevance: model-auth health — OAuth expiry refresh + cooldown reporting.
- **[Cron](../../term_dictionary/term_cron.md)** — scheduled jobs; relevance: legacy cron-store migration.
- **[Sandbox](../../term_dictionary/term_sandbox.md)** — isolated execution; relevance: sandbox image repair when sandboxing is enabled.
- **[Plugin Manifest](../../term_dictionary/term_plugin_manifest.md)** — plugin declaration; relevance: legacy plugin-manifest contract-key migration (`*Providers` → `contracts`).
- **[Authentication](../../term_dictionary/term_authentication.md)** — identity verification; relevance: device-pairing trouble detection + gateway auth checks.

**Docs**

- **[Claude Code — Debug Your Configuration](../claude_code/cc_debug_your_configuration.md)** — config diagnosis/repair; relevance: the closest analog to doctor's config-normalization/lint pass.
- **[Claude Code — Settings Files](../claude_code/cc_settings_files.md)** — config files + migrations; relevance: the legacy-config-key migration surface doctor rewrites.
- **[Claude Code — Authentication](../claude_code/cc_authentication.md)** — auth/credential health; relevance: doctor's model-auth health + OAuth refresh checks.
- **[Hermes — CLI Commands (Ops/Maintenance/Auth)](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md)** — ops/doctor-style CLI; relevance: direct analog to `openclaw doctor` repair/lint commands.
- **[Hermes — Migrate From OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md)** — config/state migration; relevance: the legacy on-disk state + config migrations doctor performs.
- **[Hermes — Cron Internals](../hermes_agent/hermes_cron_internals.md)** — cron job model; relevance: the legacy cron-store migration doctor applies.
- **[oc_gateway_configuration_overview](oc_gateway_configuration_overview.md)** — validation-failure → `doctor --fix` path (planned, this series); relevance: doctor is the recovery path when strict validation fails.
- **[oc_gateway_diagnostics_export](oc_gateway_diagnostics_export.md)** — companion diagnostics tool (planned, this series); relevance: doctor + diagnostics are the paired support tools.
- **[oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md)** — cron/auth-storage fields (planned, this series); relevance: the fields doctor migrates/repairs.
- **[oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md)** — provider/model runtime fields (planned, this series); relevance: the Codex-route/provider-runtime cleanup doctor performs.

**Repos**

- **[repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md)** — gateway runtime; relevance: gateway runtime/service/port checks doctor runs.
- **[repo_openclaw](../../../areas/code_repos/repo_openclaw.md)** — monorepo; relevance: config normalization + legacy migrations.
- **[repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md)** — session runtime; relevance: session lock/transcript repair.
- **[repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md)** — security layer; relevance: config-permission chmod 600 + auth health checks.

**Snippets**

- **[snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md)** — doctor check primitives; relevance: the check/repair primitive model doctor uses.
- **[snippet_hermes_agent_cli_doctor_entry_early_checks](../../code_snippets/snippet_hermes_agent_cli_doctor_entry_early_checks.md)** — doctor early checks; relevance: the quick-start/pre-flight checks.
- **[snippet_hermes_agent_cli_doctor_auth_dirs](../../code_snippets/snippet_hermes_agent_cli_doctor_auth_dirs.md)** — doctor auth/dir checks; relevance: auth-storage + config-dir permission checks.
- **[snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md)** — doctor connectivity checks; relevance: the model-auth/connectivity health checks.
- **[snippet_hermes_agent_cli_doctor_late_sections_summary](../../code_snippets/snippet_hermes_agent_cli_doctor_late_sections_summary.md)** — doctor summary output; relevance: the "What it does (summary)" catalog rendering.
- **[snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md)** — Dreams diary repair/cron; relevance: directly implements the Dreams UI backfill/reset doctor-style RPC.
- **[snippet_hermes_agent_cli_config_migrate](../../code_snippets/snippet_hermes_agent_cli_config_migrate.md)** — config migration; relevance: the legacy-config-key migrations doctor applies.
- **[snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md)** — config validation; relevance: the read-only lint mode validating config.
- **[snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md)** — startup runtime attach; relevance: gateway runtime/service checks (installed-but-not-running).
- **[snippet_hermes_agent_gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md)** — session lifecycle; relevance: session lock inspection + stale-lock cleanup.

## References

- [OpenClaw Docs — Doctor](https://docs.openclaw.ai/gateway/doctor)
- [OpenClaw Docs — Gateway runbook](https://docs.openclaw.ai/gateway)
- [OpenClaw Docs — Gateway troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)
- [OpenClaw Docs — Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace)

**Source**: OpenClaw documentation — `gateway/doctor` (mirror `inbox/openclaw_docs/gateway/doctor.md`)
**Last Updated**: 2026-06-22
**Status**: Active
