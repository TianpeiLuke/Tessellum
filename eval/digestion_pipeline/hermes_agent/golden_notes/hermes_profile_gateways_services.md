---
tags:
  - resource
  - documentation
  - hermes_agent
  - profiles
  - gateways
keywords:
  - multi-profile gateways
  - hermes-gateways wrapper
  - per-profile bot tokens
  - token-conflict locks
  - launchd systemd service
  - gateway multiplexing
  - keep host awake
  - stale PID recovery
topics:
  - Hermes Agent
  - Profiles
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways
access_control_group: ["general"]
---

# Hermes Agent — Per-Profile Gateways as Managed Services

## Overview

This is the operational procedure for running **many Hermes profiles online at once on a single machine**, each as its own managed gateway service. A [profile](../../term_dictionary/term_hermes_profile.md) is a separate `HERMES_HOME` state directory that auto-becomes a command alias (see [hermes_profiles_multi_agent](hermes_profiles_multi_agent.md)); this page picks up where that leaves off — once you have a coder agent, a personal bot, and a research agent, how do you start them all together, supervise them across reboots, watch their logs, and recover from launchd/systemd quirks. The default per-profile model runs **one gateway process per profile**, each binding its own per-platform bot token and writing its own LaunchAgent/systemd unit; an opt-in **multiplexing** mode collapses that into a single inbound process that routes to every profile. You do not need this page if you run only one agent. Typical drivers: a personal assistant on one Telegram bot plus a coding agent on another, one agent per family member or per Slack workspace, sandbox + production instances of the same config, or a research agent + writing agent + cron-driven bot each with isolated memory and skills.

## Running a Gateway Per Profile

Each profile runs its own gateway as a separate process with its own bot token. The per-profile command alias starts it; targeting two different profiles spawns two independent processes:

```bash
coder gateway start           # starts coder's gateway
assistant gateway start       # starts assistant's gateway (separate process)
```

**Different bot tokens.** Each profile has its own `.env` file, so you configure a different Telegram/Discord/Slack bot token in each (e.g. `nano ~/.hermes/profiles/coder/.env` vs `nano ~/.hermes/profiles/assistant/.env`). Per-platform token setup itself is covered by the messaging docs — see [hermes_messaging_media_settings](hermes_messaging_media_settings.md). **Persistent services** are created with `coder gateway install` / `assistant gateway install`, which write a per-profile `hermes-gateway-<name>` systemd/launchd service so each profile gets its own service name and they run independently. Inside the official Docker image, per-profile gateways are instead supervised by s6-overlay (PID 1) and `hermes profile create` registers an s6 service slot — that supervision path is documented separately for the container deployment.

## Safety: Token-Conflict Locks

Each profile must use unique bot tokens per platform. If two profiles accidentally configure the same `(platform, token)`, the second gateway refuses to start with a clear error naming the conflicting profile — enforced for Telegram, Discord, Slack, WhatsApp, and Signal. To audit which token each profile holds:

```bash
grep -H 'TELEGRAM_BOT_TOKEN\|DISCORD_BOT_TOKEN' \
     ~/.hermes/.env ~/.hermes/profiles/*/.env
```

This rule is unchanged under multiplexing — it is just enforced inside the one shared process instead of across two.

## Quick Start: Many Profiles

The end-to-end setup is create → configure → install service → start, repeated per profile:

```bash
hermes profile create coder
hermes profile create personal-bot
hermes profile create research

coder setup
personal-bot setup
research setup

coder gateway install
personal-bot gateway install
research gateway install

coder gateway start
personal-bot gateway start
research gateway start
```

That yields three independent agents, each on its own process, restarting automatically on crash and on user login.

## Start / Stop / Restart All At Once

The CLI ships only single-profile lifecycle commands (`gateway run/start/stop/restart/status/install/uninstall`, equivalent to `hermes -p <profile> gateway <action>`). To act across every profile, wrap them in a shell loop. Put this in `~/.local/bin/hermes-gateways` and `chmod +x` it:

```sh
#!/bin/sh
set -eu

# Add or remove profile names here as you create / delete profiles.
profiles="default coder personal-bot research"

usage() {
  echo "Usage: hermes-gateways {start|stop|restart|status|list}"
}

run_for_profile() {
  profile="$1"
  action="$2"
  if [ "$profile" = "default" ]; then
    hermes gateway "$action"
  else
    hermes -p "$profile" gateway "$action"
  fi
}

action="${1:-}"
case "$action" in
  start|stop|restart|status)
    for profile in $profiles; do
      echo "==> $action $profile"
      run_for_profile "$profile" "$action"
    done
    ;;
  list)
    hermes gateway list
    ;;
  *)
    usage
    exit 2
    ;;
esac
```

Then `hermes-gateways start|stop|restart|status|list` acts across every configured profile. Note the **default** profile is targeted as `hermes gateway <action>` (no `-p`), not `hermes -p default gateway <action>` — the wrapper handles both forms.

## Alternative: One Gateway for All Profiles (Multiplexing)

Opt-in and off by default. Set `gateway.multiplex_profiles: true` on the **default** profile (it owns the multiplexer) and `hermes gateway restart`. On next start the default gateway enumerates every profile, brings up each profile's enabled platforms under that profile's own credentials, and routes each inbound message to the profile it belongs to; each turn resolves the routed profile's config, skills, memory, SOUL, **and provider keys** — credentials are never shared. Prefer it for container/VPS deployments where N units/ports/PID files are a burden, or many low-traffic profiles; stick with one-process-per-profile when you want hard process-level isolation. When on:

- Secondary profiles **must not** start their own gateway — a named-profile `gateway start` is a hard error (pass `--force` only to deliberately run a separate process). The `hermes-gateways` wrapper is therefore unused in multiplex mode.
- HTTP-inbound platforms are reached via a **`/p/<profile>/` URL prefix** on the one shared listener (e.g. `POST http://host:8644/p/coder/webhooks/<route>`), not a second port; an unknown profile returns `404`. Port-binding platforms (`webhook`, `api_server`, `msgraph_webhook`, `feishu`, `wecom_callback`, `bluebubbles`, `sms`) must be configured **only on the default profile**.
- Per-credential platforms (Telegram, Discord, Slack, Matrix, Signal, …) still need their own token per profile — the token-conflict rule above applies inside the process.
- Session keys are namespaced `agent:<profile>:…`; the default profile keeps the historical `agent:main:…` namespace byte-for-byte (no migration).
- There is one process-level PID/lock (the multiplexer, under the default home); `hermes status` reports the multiplexer and the profiles it serves, `hermes status -p <name>` slices to one. Each profile still writes its own `runtime_status.json`.

## Service Files, Logs, and Identifying What Runs

Each profile installs a uniquely named service so installations never clash; the default profile keeps the historical names (`ai.hermes.gateway.plist` / `hermes-gateway.service`):

| Platform | Path                                                              |
| -------- | ----------------------------------------------------------------- |
| macOS    | `~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist`        |
| Linux    | `~/.config/systemd/user/hermes-gateway-<profile>.service`         |

Each profile writes its own logs (`~/.hermes/logs/gateway.log` for default, `~/.hermes/profiles/<name>/logs/gateway.log` for named); stream all at once with `tail -f ~/.hermes/logs/gateway.log ~/.hermes/profiles/*/logs/gateway.log`. The CLI also has a structured viewer (`hermes logs -f`, `hermes -p coder logs -f`, `hermes logs --help` for filters/levels/JSON) — see [hermes_cli_interface](hermes_cli_interface.md). To see what is actually running: `hermes profile list` (profiles + model + gateway state), `hermes-gateways status`, `launchctl list | grep hermes` (macOS), `systemctl --user list-units 'hermes-gateway-*'` (Linux). Per-profile config lives in each `~/.hermes/profiles/<name>/` as `.env` / `config.yaml` / `SOUL.md` (see [hermes_config_files_precedence](hermes_config_files_precedence.md)); after editing `.env` or `config.yaml`, restart the affected gateway (`coder gateway restart`, or `hermes-gateways restart` for everything). `hermes update` pulls code once and syncs bundled skills into every profile (run `hermes-gateways restart` after); user-modified skills are never overwritten. The web dashboard is a machine-level surface whose sidebar profile switcher can manage any profile's config/keys/skills/MCPs/model — "Set as active" there is the sticky default for future CLI/gateway runs.

## Keeping the Host Awake

A gateway can run all day, but the OS still tries to sleep when idle. On macOS, the built-in `caffeinate` prevents sleep while it runs:

```bash
caffeinate -dis                    # block display, idle, and system sleep
caffeinate -dis -t 28800           # same, auto-exit after 8 hours
caffeinate -i -w $(cat ~/.hermes/gateway.pid) &   # awake while default gateway runs

# Persistent: run in background and forget
nohup caffeinate -dis >/dev/null 2>&1 &
disown

# Inspect / stop
pmset -g assertions | grep -iE 'caffeinate|prevent|user is active'
pkill caffeinate
```

Key flags: `-d` (display), `-i` (idle, default), `-m` (disk), `-s` (system, AC-powered only), `-u` (simulate activity), `-t N` (auto-exit after N seconds), `-w P` (exit when PID P exits). Note `caffeinate` cannot override hardware lid-close sleep on MacBooks. On Linux, inhibit suspend with `systemd-inhibit --what=idle:sleep --who=hermes --why="gateways running" sleep infinity &`, and run `sudo loginctl enable-linger "$USER"` so user services (including `hermes-gateway-<profile>.service`) keep running across SSH disconnects and reboots.

## Troubleshooting

Common recovery recipes:

- **"Could not find service in domain for user gui: 501"** — you ran `gateway start` after a `gateway stop` (which does a full `launchctl unload`, removing the service from launchd's registry). The CLI catches this on `start` and auto-reloads the plist (`↻ launchd job was unloaded; reloading service definition`). Nothing to fix.
- **Forcing a hard reset of one service** — macOS: `launchctl unload`/`load` the `~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist`; Linux: `systemctl --user restart hermes-gateway-<profile>.service`.
- **Health check** — `hermes doctor` (default) or `hermes -p <profile> doctor` (one profile).
- **Stale PID after a crash** — a profile shows `not running` but a process is still alive:

```bash
ps -ef | grep "hermes_cli.*-p <profile>"
cat ~/.hermes/profiles/<profile>/gateway.pid
kill -TERM <pid>          # graceful
kill -KILL <pid>          # if that fails after a few seconds
<profile> gateway start
```

**Source**: `inbox/hermes_agent_docs/user-guide/multi-profile-gateways.md` (+ `profiles.md` §Running gateways / §Configuring profiles dashboard) · https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways
**Last Updated**: 2026-06-19
**Status**: Active
