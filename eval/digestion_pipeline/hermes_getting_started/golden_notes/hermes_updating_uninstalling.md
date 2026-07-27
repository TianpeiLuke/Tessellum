---
tags:
  - resource
  - documentation
  - hermes_agent
  - getting_started
  - lifecycle
keywords:
  - hermes update
  - auto-rollback
  - pre-update backup
  - hermes uninstall
  - post-update validation
  - sighup survival
topics:
  - Hermes Agent
  - Getting Started
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/getting-started/updating
access_control_group: ["general"]
---

# Hermes Agent — Updating & Uninstalling

## Overview

This is the **lifecycle procedure** for keeping a Hermes Agent install current and for removing it cleanly. Updating is one command — `hermes update` — that branches on how you installed: git installs pull the latest `main` and reinstall dependencies, while pip installs upgrade to the latest **tagged** PyPI release. The update path is engineered to be safe-by-default: a lightweight pre-update snapshot, post-pull syntax validation with automatic git rollback if startup files break, config migration, gateway auto-restart, and `SIGHUP` survival so a dropped terminal can't leave a half-installed environment. Uninstalling mirrors the install type (git / pip / manual) and optionally preserves `~/.hermes/` for a future reinstall.

## Updating

`hermes update` updates to the latest version with a single command. The behavior depends on install type.

**Git installs** pull the latest code from `main`, update dependencies, and prompt you to configure any new options added since your last update:

```bash
hermes update
```

**pip installs** track **tagged versions** (major and minor releases), not every commit on `main`. Check and upgrade with `hermes update --check` (see if a newer release is on PyPI) then `hermes update` (runs `pip install --upgrade hermes-agent`). You can upgrade manually with `pip install --upgrade hermes-agent` (or `uv pip install --upgrade hermes-agent`).

`hermes update` automatically detects new configuration options and prompts you to add them. If you skipped that prompt, run `hermes config check` to see missing options, then `hermes config migrate` to interactively add them.

## What Happens During an Update (git installs)

When you run `hermes update`, the following steps occur in order:

1. **Pairing-data snapshot** — a lightweight pre-update state snapshot is saved (covers `~/.hermes/pairing/`, Feishu comment rules, and other state files modified at runtime). Recoverable via the snapshot restore flow, or by extracting the most recent quick-snapshot zip Hermes wrote next to your `~/.hermes/` directory.
2. **Git pull** — pulls the latest code from the `main` branch and updates submodules.
3. **Post-pull syntax validation + auto-rollback** — after the pull, Hermes compiles the eight critical files every `hermes` invocation imports at startup. If any fails to parse (e.g. an orphan merge-conflict marker, an accidentally truncated file), Hermes runs `git reset --hard <pre-pull-sha>` to roll the install back so your shell stays bootable. Re-run `hermes update` once the upstream fix lands.
4. **Dependency install** — runs `uv pip install -e ".[all]"` to pick up new or changed dependencies.
5. **Config migration** — detects new config options added since your version and prompts you to set them.
6. **Gateway auto-restart** — running gateways are refreshed after the update completes so the new code takes effect immediately. Service-managed gateways (systemd on Linux, launchd on macOS) are restarted through the service manager; manual gateways are relaunched automatically when Hermes can map the running PID back to a profile.

## Update Flags

**`--branch`** — by default `hermes update` tracks `origin/main`. Pass `--branch <name>` to update against a different branch (QA channels, feature branches, release-candidate testing):

```bash
hermes update --branch release-candidate
hermes update --check --branch experimental   # preview behindness only
```

If your local checkout is on a different branch, Hermes auto-stashes uncommitted work, switches HEAD to the target branch, then pulls. Branches that don't exist locally are auto-tracked from `origin/<name>` (`git checkout -B <name> origin/<name>`). Branches that don't exist anywhere fail cleanly — your stashed changes are restored before exit. The `main`-only fork-upstream sync logic is automatically skipped on non-`main` branches.

**`--check`** (preview-only) — reports whether an update is available before pulling: for git installs it fetches and compares commits against `origin/main`; for pip installs it queries PyPI for the latest release. No files are modified, no gateway is restarted. Useful in scripts and cron jobs that gate on "is there an update".

**`--backup`** (full pre-update backup) — for high-value profiles (production gateways, shared team installs) you can opt into a full pre-pull backup of `HERMES_HOME` (config, auth, sessions, skills, pairing):

```bash
hermes update --backup
```

Make it the default for every run via config (`updates.pre_update_backup: true`). `--backup` was always-on in earlier builds but was adding minutes to every update on large homes, so it's now opt-in. The lightweight pairing-data snapshot still runs unconditionally.

## Local Changes on Non-Interactive Updates

In a terminal, Hermes stashes uncommitted source-tree changes, pulls, then **asks** whether to restore them. When the update runs **without a terminal** — from the desktop/chat app's "Update" button or a gateway-triggered update — there's no prompt, so the `updates.non_interactive_local_changes` setting decides:

```yaml
# ~/.hermes/config.yaml
updates:
  non_interactive_local_changes: stash   # default: keep + auto-restore
  # non_interactive_local_changes: discard  # throw local source edits away
```

- `stash` (default) — auto-stash, pull, then auto-restore your changes on top of the updated code. Nothing is lost; restore conflicts are preserved in a git stash for manual recovery.
- `discard` — auto-stash and drop the stash after the pull, so the update lands on a clean tree. Use only on machines where you never keep local edits. It stash-drops (not `git reset --hard` + `git clean -fd`), so ignored paths like `node_modules`, `venv`, and build outputs are never touched.

In the desktop app this is **Settings → Advanced → In-App Update Local Changes**.

## Windows: Another `hermes.exe` Is Running

On Windows, `hermes update` refuses to run if it detects another `hermes.exe` process holding the venv's entry-point executable open — most commonly the Desktop app's spawned backend, an open `hermes` REPL in another terminal, or a running gateway. Close the listed processes and re-run. If you're sure the concurrent process won't interfere (rare — usually only an antivirus shim mis-attribution), pass `--force` to skip the check; the updater then retries the `.exe` rename with exponential backoff and, on stubborn locks, schedules the replacement for next reboot via `MoveFileEx(MOVEFILE_DELAY_UNTIL_REBOOT)`. Expected successful output walks the visible phases: `📥 Pulling latest code...` (`Already up to date.` or `Updating abc1234..def5678`), `📦 Updating dependencies...` → `✅ Dependencies updated`, `🔍 Checking for new config options...` (`✅ Config is up to date` or `Found 2 new options — running migration...`), `🔄 Restarting gateways...` → `✅ Gateway restarted`, ending with `✅ Hermes Agent updated successfully!`.

## Recommended Post-Update Validation

`hermes update` handles the main path, but a quick validation confirms everything landed cleanly:

1. `git status --short` — if the tree is unexpectedly dirty, inspect before continuing.
2. `hermes doctor` — checks config, dependencies, and service health.
3. `hermes --version` — confirm the version bumped as expected.
4. If you use the gateway: `hermes gateway status`.
5. If `doctor` reports npm audit issues: run `npm audit fix` in the flagged directory.

If `git status --short` shows unexpected changes, stop and inspect — this usually means local modifications were reapplied on top of the updated code, or a dependency step refreshed lockfiles.

## Terminal Disconnect Mid-Update

`hermes update` protects itself against accidental terminal loss. The update ignores `SIGHUP`, so closing your SSH session or terminal window no longer kills it mid-install; `pip` and `git` child processes inherit this protection, so the Python environment cannot be left half-installed by a dropped connection. All output is mirrored to `~/.hermes/logs/update.log`; if your terminal disappears, reconnect and inspect the log with `tail -f ~/.hermes/logs/update.log` to see whether the update finished and whether the gateway restart succeeded. `Ctrl-C` (SIGINT) and system shutdown (SIGTERM) are still honored — those are deliberate cancellations, not accidents. You no longer need to wrap `hermes update` in `screen` or `tmux` to survive a terminal drop.

## Updating from Messaging Platforms & Manually

Check your current version with `hermes version` and compare against the GitHub releases page. You can also update directly from Telegram, Discord, Slack, WhatsApp, or Teams by sending `/update` — this pulls the latest code, updates dependencies, and restarts running gateways (the bot briefly goes offline during the restart, typically 5–15 seconds). For a manual install (not via the quick installer):

```bash
cd /path/to/hermes-agent
export VIRTUAL_ENV="$(pwd)/venv"
git pull origin main
uv pip install -e ".[all]"          # reinstall, picks up new dependencies
hermes config check
hermes config migrate               # interactively add any missing options
```

## Rollback

If an update introduces a problem, roll back to a previous commit (`git log --oneline -10` to list versions, then `git checkout <commit-hash>` and `uv pip install -e ".[all]"`, finally `hermes gateway restart` if running), or to a specific release tag (`git checkout vX.Y.Z` then `uv pip install -e ".[all]"`; find tags via `git tag --sort=-version:refname`). Rolling back may cause config incompatibilities if new options were added — run `hermes config check` afterward and remove any unrecognized options from `config.yaml` if you hit errors.

**Note for Nix users**: Nix-flake installs are managed through the Nix package manager (`nix flake update hermes-agent` to update the input, `nix profile upgrade hermes-agent` to rebuild). Nix installations are immutable, so rollback is handled by Nix's generation system (`nix profile rollback`). See the Nix Setup page for details.

## Uninstalling

Uninstall mirrors the install type. All paths optionally preserve `~/.hermes/` for a future reinstall.

```bash
# Git installs — uninstaller offers to keep ~/.hermes/ config files
hermes uninstall

# pip installs
pip uninstall hermes-agent
rm -rf ~/.hermes            # Optional — keep if you plan to reinstall

# Manual install
rm -f ~/.local/bin/hermes
rm -rf /path/to/hermes-agent
rm -rf ~/.hermes            # Optional — keep if you plan to reinstall
```

If you installed the gateway as a system service, stop and disable it first: `hermes gateway stop`, then on Linux `systemctl --user disable hermes-gateway` or on macOS `launchctl remove ai.hermes.gateway`.

## Related Notes

**Terms**
- [term_regular_checkpointing](../../term_dictionary/term_regular_checkpointing.md) — pre-update snapshot; relevance: §pairing-data snapshot + `--backup`.
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — preserved sessions; relevance: backup covers sessions, uninstall keeps `~/.hermes/`.
- [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — package being updated; relevance: `hermes update` subject.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent category; relevance: framing of the updated tool.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled checks; relevance: §`--check` in scripts/cron jobs.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — preserved auth; relevance: `--backup` covers auth tokens.
- [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — gateway service; relevance: §Gateway auto-restart (systemd/launchd).
- [term_checkpoint](../../term_dictionary/term_checkpoint.md) — rollback point; relevance: §auto-rollback `git reset --hard <pre-pull-sha>` + §Rollback.

**Code-Repos**
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — update/uninstall commands; relevance: implements `hermes update` (flags `--check`/`--branch`/`--backup`/`--force`), `config migrate`, `hermes uninstall`.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — git/pip install + installer; relevance: git-pull/auto-rollback, install-method auto-detection, PyPI tagged releases.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — startup-critical files; relevance: §post-pull syntax validation compiles the eight startup imports.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway restart + `/update`; relevance: §Gateway auto-restart and §Updating from Messaging Platforms.
- [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — scheduled update checks; relevance: `hermes update --check` gating in cron jobs.

**Snippets**
- [snippet_hermes_agent_cli_main_cmd_update](../../code_snippets/snippet_hermes_agent_cli_main_cmd_update.md) — `hermes update` command; relevance: the update internals (git-pull, auto-rollback).
- [snippet_hermes_agent_cli_banner_update](../../code_snippets/snippet_hermes_agent_cli_banner_update.md) — startup update banner; relevance: §`--check` available-update detection.
- [snippet_hermes_agent_cli_config_migrate](../../code_snippets/snippet_hermes_agent_cli_config_migrate.md) — config migrate; relevance: post-update `config migrate`.
- [snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md) — config validate; relevance: §Post-Update Validation.
- [snippet_hermes_agent_cli_uninstall](../../code_snippets/snippet_hermes_agent_cli_uninstall.md) — uninstall; relevance: §Uninstalling per install type.
- [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — `hermes doctor`; relevance: §Post-Update Validation `doctor`.
- [snippet_hermes_agent_cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — setup verify; relevance: post-update plain-chat re-validation.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — logging setup; relevance: update/rollback diagnostics output.
- [snippet_hermes_agent_cli_backup_save](../../code_snippets/snippet_hermes_agent_cli_backup_save.md) — `--backup` snapshot; relevance: §pre-update pairing-data snapshot.
- [snippet_hermes_agent_cli_backup_restore](../../code_snippets/snippet_hermes_agent_cli_backup_restore.md) — backup restore; relevance: §Rollback / auto-rollback restore.

**Docs**
- [hermes_installation](hermes_installation.md) — install ref; relevance: install-method auto-detection drives the update command.
- [hermes_install_nix_quickstart](hermes_install_nix_quickstart.md) — Nix install; relevance: §Note for Nix users (`nix flake update`/`profile upgrade`/`rollback`).
- [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — first chat; relevance: post-update plain-chat re-validation.
- [hermes_nixos_container_mode](hermes_nixos_container_mode.md) — container update; relevance: cross-ref for NixOS container update path.
- [hermes_install_nixos_module](hermes_install_nixos_module.md) — NixOS module; relevance: declarative update vs CLI update.
- [hermes_checkpoints](hermes_checkpoints_rollback.md) — checkpoints/rollback; relevance: §Snapshots and rollback link-out.
- [cc_update_and_release_channels](../claude_code/cc_update_and_release_channels.md) — analogous update; relevance: parallels git vs tagged-release update.
- [cc_uninstall](../claude_code/cc_uninstall.md) — analogous uninstall; relevance: parallels §Uninstalling per install type.
- [cc_checkpointing](../claude_code/cc_checkpointing.md) — analogous rollback; relevance: parallels auto-rollback/snapshot.
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — analogous post-install verify; relevance: parallels §Recommended Post-Update Validation (`doctor`/`--version`).

**Source**: `inbox/hermes_agent_docs/getting-started/updating.md` · https://hermes-agent.nousresearch.com/docs/getting-started/updating
**Last Updated**: 2026-06-19
**Status**: Active
