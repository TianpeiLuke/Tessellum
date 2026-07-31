---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - doctor
keywords:
  - openclaw doctor
  - doctor lint fix repair
  - health check findings
  - detect repair contract
  - healthfinding severity
  - post-upgrade plugin probes
  - launchctl env overrides
  - secretref allow-exec
topics:
  - OpenClaw
  - CLI doctor
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/doctor
access_control_group: ["general"]
---

# OpenClaw — `openclaw doctor` Health Checks and Guided Repairs

## Overview

This note is the procedure reference for the `openclaw doctor` CLI command, mirroring the `cli/doctor` source page. `doctor` is the OpenClaw health surface: one command that inspects, explains, and (optionally) repairs problems with the gateway, channels, plugins, skills, model routing, local state, or config migrations. It documents the three postures (inspect / repair / lint), every option, lint exit codes and JSON findings, the `detect()`/`repair()` structured-health-check contract, `--only`/`--skip` check selection, `--post-upgrade` plugin-compatibility probes, the Notes catalog of repair behaviors, and the macOS `launchctl` env-override gotcha. Code-side counterparts (`repo_openclaw_*`, `snippet_openclaw_*`) are linked, not redefined.

## Why Use It

Use `openclaw doctor` when the gateway, channels, plugins, skills, model routing, local state, or config migrations misbehave and you want one command that explains what is wrong. Doctor has three postures:

| Posture | Command | Behavior |
| ------- | ------- | -------- |
| Inspect | `openclaw doctor` | Human-oriented checks and guided prompts. |
| Repair | `openclaw doctor --fix` | Applies supported repairs, using prompts unless non-interactive repair is safe. |
| Lint | `openclaw doctor --lint` | Read-only structured findings for CI, preflight, and review gates. |

Prefer `--lint` when automation needs a stable result; prefer `--fix` when a human operator wants doctor to edit config or state. For channel-specific permissions use the channel probes instead of `doctor` — `openclaw channels capabilities --channel discord --target channel:<channel-id>` reports the bot's effective channel permissions, and `openclaw channels status --probe` audits configured Discord channels and voice auto-join targets.

## Examples

```bash
openclaw doctor
openclaw doctor --lint
openclaw doctor --lint --json
openclaw doctor --lint --severity-min warning
openclaw doctor --lint --allow-exec
openclaw doctor --deep
openclaw doctor --fix
openclaw doctor --fix --non-interactive
openclaw doctor --generate-gateway-token
openclaw doctor --post-upgrade
openclaw doctor --post-upgrade --json
```

## Options

Every documented flag, copied from source:

- `--no-workspace-suggestions`: disable workspace memory/search suggestions.
- `--yes`: accept defaults without prompting.
- `--repair`: apply recommended non-service repairs without prompting; gateway service installs and rewrites still require interactive confirmation or explicit gateway commands.
- `--fix`: alias for `--repair`.
- `--force`: apply aggressive repairs, including overwriting custom service config when needed.
- `--non-interactive`: run without prompts; safe migrations and non-service repairs only.
- `--generate-gateway-token`: generate and configure a gateway token.
- `--allow-exec`: allow doctor to execute configured exec SecretRefs while verifying secrets.
- `--deep`: scan system services for extra gateway installs and report recent Gateway supervisor restart handoffs.
- `--lint`: run modernized health checks in read-only mode and emit diagnostic findings.
- `--post-upgrade`: run post-upgrade plugin compatibility probes; emits findings to stdout; exits code 1 if any error-level findings are present.
- `--json`: with `--lint`, emit JSON findings instead of human output; with `--post-upgrade`, emit a JSON envelope (`{ probesRun, findings }`).
- `--severity-min <level>`: with `--lint`, drop findings below `info`, `warning`, or `error`.
- `--skip <id>`: with `--lint`, skip a check id; repeatable.
- `--only <id>`: with `--lint`, run only a check id; repeatable.

## Lint Mode

`openclaw doctor --lint` is the read-only automation posture: it uses the structured health-check path, does not prompt, and does not repair or rewrite config/state. Use it in CI, preflight, and review workflows for machine-readable findings. Lint-output options (`--json`, `--severity-min`, `--only`, `--skip`) are only accepted with `--lint`.

```bash
openclaw doctor --lint --only core/doctor/gateway-config --json
```

Human output is compact — `doctor --lint: ran 6 check(s), 1 finding(s)` plus a per-finding line such as `[warning] core/doctor/gateway-config gateway.mode - gateway.mode is unset; gateway start will be blocked.` and an indented `fix:` hint. JSON output is the scripting surface:

```json
{
  "ok": false,
  "checksRun": 5,
  "checksSkipped": 0,
  "findings": [
    {
      "checkId": "core/doctor/gateway-config",
      "severity": "warning",
      "message": "gateway.mode is unset; gateway start will be blocked.",
      "path": "gateway.mode",
      "fixHint": "Run `openclaw configure` and set Gateway mode (local/remote), or `openclaw config set gateway.mode local`."
    }
  ]
}
```

Exit behavior: `0` = no findings at or above the threshold; `1` = at least one finding meets it; `2` = command/runtime failure before lint findings can be produced. `--severity-min` controls both visible findings and the exit threshold — e.g. `openclaw doctor --lint --severity-min error` can print no findings and exit `0` even when lower-severity `info`/`warning` findings exist.

## Structured Health Checks

Modern doctor checks use a small structured contract: `detect(ctx, scope?) -> HealthFinding[]` and an optional `repair?(ctx, findings) -> HealthRepairResult`. `detect()` powers `doctor --lint`; `repair()` is only considered by `doctor --fix` / `doctor --repair`. Checks that have not migrated use the legacy doctor contribution flow. The split is intentional — `detect()` owns diagnosis, `repair()` owns reporting what it changed or would change. Repair contexts can carry `dryRun`/`diff` requests, and repair results can return structured `diffs` for config/file edits plus `effects` for service, process, package, state, or other side effects — letting converted checks grow toward `doctor --fix --dry-run` without moving mutation planning into `detect()`.

`repair()` reports whether it attempted the repair with `status: "repaired" | "skipped" | "failed"` (omitted status means `repaired`). On `skipped`/`failed`, doctor reports the reason and does not run validation for that check. After a successful structured repair, doctor re-runs `detect()` with the repaired findings as scope (checks can use selected findings, paths, or `ocPath` values for focused validation); if the finding is still present, doctor reports a repair warning rather than treating the change as silently complete.

A `HealthFinding` includes these fields:

| Field | Purpose |
| ----- | ------- |
| `checkId` | Stable id for skip/only filters and CI allowlists. |
| `severity` | `info`, `warning`, or `error`. |
| `message` | Human-readable problem statement. |
| `path` | Config, file, or logical path when available. |
| `line` / `column` | Source location when available. |
| `ocPath` | Precise `oc://` address when a check can point to one. |
| `fixHint` | Suggested operator action or repair summary. |

Modernized core checks stay attached to the ordered doctor contribution that owns their human `doctor` / `doctor --fix` behavior. The shared structured health registry is the extension point: bundled and plugin-backed checks run after core checks once their owning package registers them in the active command path, and the `openclaw/plugin-sdk/health` subpath exposes the same contract for extension consumers.

## Check Selection

Use `--only` and `--skip` when a workflow wants a focused gate, e.g. `openclaw doctor --lint --skip core/doctor/skills-readiness`. Both accept full check ids and may be repeated. If an `--only` id is not registered, no check runs for it; use the command's `checksRun` and `checksSkipped` fields to verify a focused gate is selecting the checks you expect.

## Post-Upgrade Mode

`openclaw doctor --post-upgrade` runs plugin compatibility probes intended to be chained after a build or upgrade. Findings are emitted to stdout; it exits code 1 if any finding has `level: "error"`. Add `--json` for a machine-readable envelope (`{ probesRun, findings }`) suitable for CI, the community `fork-upgrade` skill, and other post-upgrade smoke tooling. If the installed plugin index is missing or malformed, JSON mode still emits that envelope with a `plugin.index_unavailable` error finding.

## Notes (Repair Behaviors and Gotchas)

Doctor's posture interactions, migrations, and repair behaviors:

- **Nix mode** (`OPENCLAW_NIX_MODE=1`): read-only checks still work, but `doctor --fix`, `--repair`, `--yes`, and `--generate-gateway-token` are disabled because `openclaw.json` is immutable — edit the Nix source.
- **Interactive prompts** (keychain/OAuth fixes) only run when stdin is a TTY and `--non-interactive` is unset; headless runs (cron, Telegram, no terminal) skip prompts. Non-interactive runs also skip eager plugin loading so headless health checks stay fast.
- `--lint` is stricter than `--non-interactive`: always read-only, never prompts, never applies safe migrations. Run `doctor --fix` / `doctor --repair` to make changes.
- By default doctor does not execute `exec` SecretRefs while checking secrets — use `--allow-exec` only when you intentionally want those resolvers run. If `gateway.auth.token`/`gateway.auth.password` are SecretRef-managed and unavailable, doctor reports a read-only warning and writes no plaintext fallback credentials. If channel SecretRef inspection fails in a fix path, doctor continues and warns rather than exiting early.
- `--fix` (alias `--repair`) writes a backup to `~/.openclaw/openclaw.json.bak` and drops unknown config keys, listing each removal. `doctor --fix --non-interactive` reports missing or stale gateway service definitions but won't install/rewrite them outside update repair mode — run `openclaw gateway install` for a missing service, or `openclaw gateway install --force` to replace the launcher.
- **State integrity**: doctor detects orphan transcript files in the sessions directory; archiving them as `.deleted.<timestamp>` requires interactive confirmation (`--fix`, `--yes`, headless runs leave them in place).
- **Cron migrations**: doctor scans `~/.openclaw/cron/jobs.json` (or `cron.store`) for legacy cron job shapes and rewrites them before importing canonical rows into SQLite. It reports cron jobs with explicit `payload.model` overrides (provider namespace counts, mismatches against `agents.defaults.model`) so non-inheriting jobs surface in auth/billing investigations. On Linux it warns when the crontab still runs the unmaintained `~/.openclaw/bin/ensure-whatsapp.sh`.
- **WhatsApp**: when enabled, doctor checks for a degraded Gateway event loop with local `openclaw-tui` clients still running; `doctor --fix` stops only verified local TUI clients so replies aren't queued behind stale TUI refresh loops.
- **Model-ref migrations**: doctor rewrites legacy `openai-codex/*` model refs to canonical `openai/*` across primary models, fallbacks, image/video generation, heartbeat/subagent/compaction overrides, hooks, channel model overrides, and stale session route pins; `--fix` also migrates legacy `openai-codex:*` auth profiles and `auth.order.openai-codex` entries to `openai:*`, moves Codex intent onto provider/model-scoped `agentRuntime.id: "codex"` entries, removes stale runtime pins, and keeps repaired OpenAI agent refs on Codex auth routing.
- **Plugin repair**: doctor cleans legacy plugin dependency staging state and relinks the host `openclaw` package for managed npm plugins declaring it as a peer dependency; repairs missing downloadable plugins referenced by config (`plugins.entries`, channels, provider/search settings, agent runtimes), skipping package-manager repair until a package swap completes. It removes missing plugin ids from `plugins.allow`/`plugins.deny`/`plugins.entries` plus dangling channel/heartbeat/model-override config when discovery is healthy, and quarantines invalid plugin config by disabling the affected `plugins.entries.<id>` entry and removing its bad `config` payload.
- **Service ownership**: set `OPENCLAW_SERVICE_REPAIR_POLICY=external` when another supervisor owns the gateway lifecycle — doctor still reports health and applies non-service repairs but skips service install/start/restart/bootstrap and legacy cleanup. On Linux it ignores inactive extra gateway-like systemd units and won't rewrite metadata for a running systemd gateway service.
- **Talk config**: doctor auto-migrates legacy flat Talk config (`talk.voiceId`, `talk.modelId`) into `talk.provider` + `talk.providers.<provider>`; repeat `doctor --fix` runs no longer report Talk normalization when the only difference is key order.
- **Memory / owner / Codex**: doctor includes a memory-search readiness check (recommending `openclaw configure --section model` when embedding credentials are missing); warns when no command owner is configured (set `commands.ownerAllowFrom`); notes when Codex-mode agents are configured and personal Codex CLI assets exist (`openclaw migrate plan codex`); and removes the retired `plugins.entries.codex.config.codexDynamicToolsProfile`.
- **Skills / sandbox**: doctor warns when skills allowed for the default agent are unavailable (missing bins, env vars, config, or OS requirements); `doctor --fix` can disable them with `skills.entries.<skill>.enabled=false`. If sandbox mode is enabled but Docker is unavailable, it warns with remediation (`install Docker` or `openclaw config set agents.defaults.sandbox.mode off`); legacy sandbox registry files (`~/.openclaw/sandbox/containers.json`, `browsers.json`, `containers/`, `browsers/`) are migrated into SQLite by `--fix`, with invalid files quarantined.
- **Token env fallbacks**: after state-directory migrations doctor warns when enabled default Telegram/Discord accounts depend on env fallback and `TELEGRAM_BOT_TOKEN`/`DISCORD_BOT_TOKEN` is unavailable. Telegram `allowFrom` username auto-resolution (`doctor --fix`) requires a resolvable Telegram token; if inspection is unavailable doctor warns and skips that pass.

## macOS: `launchctl` env overrides

If you previously ran `launchctl setenv OPENCLAW_GATEWAY_TOKEN ...` (or `...PASSWORD`), that value overrides your config file and can cause persistent "unauthorized" errors. Inspect and clear the overrides:

```bash
launchctl getenv OPENCLAW_GATEWAY_TOKEN
launchctl unsetenv OPENCLAW_GATEWAY_TOKEN
launchctl unsetenv OPENCLAW_GATEWAY_PASSWORD
```

**Source**: OpenClaw documentation — `cli/doctor` (mirror `inbox/openclaw_docs/cli/doctor.md`)
**Last Updated**: 2026-06-22
**Status**: Active
