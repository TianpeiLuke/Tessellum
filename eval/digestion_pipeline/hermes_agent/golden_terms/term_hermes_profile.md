---
tags:
  - resource
  - terminology
  - hermes_agent
  - autonomous_agents
  - multi_agent
keywords:
  - Hermes Profile
  - HERMES_HOME
  - multi-agent instance
  - profile alias
  - profile distribution
  - home_mode
topics:
  - Autonomous Coding Agents
  - Agent Instance Isolation
  - Multi-Agent Operations
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Hermes Profile

## Definition

A **Hermes profile** is a separate Hermes agent home directory — an isolated, independently configured instance of the Hermes autonomous agent that runs on the same machine as other profiles without sharing state. Each profile owns its own directory containing its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills, cron jobs, and state database, so a single host can run distinct agents (a coding assistant, a personal bot, a research agent) side by side without mixing up their identity, credentials, or conversation history.

The problem profiles solve is **multi-agent operation on one machine**: rather than maintaining separate installs or VMs per agent, a profile scopes all Hermes state to a `HERMES_HOME`-pointed directory and auto-registers a command alias for it. Creating a profile named `coder` immediately yields `coder chat`, `coder setup`, `coder gateway start`, etc. — each alias is just `hermes -p coder ...` under the hood. The default profile is simply `~/.hermes` itself; named profiles live under `~/.hermes/profiles/<name>/`.

## Context

The Hermes profile is a first-class concept of the **Hermes Agent** (an open-source autonomous coding / assistant agent harness by Nous Research). It is surfaced across the entire Hermes operational surface:

- **CLI** — `hermes profile create/use/list/show/rename/export/import/delete`, the `-p`/`--profile` flag, and tab completion target a profile.
- **Gateways / services** — each profile runs its own gateway process (or is served by a single multiplexing gateway) with its own bot tokens and its own LaunchAgent/systemd service unit.
- **Web dashboard** — a machine-level profile switcher selects which profile to configure or chat with.
- **Distributions** — a whole profile can be packaged as a shareable git-repo distribution and installed on other machines with `hermes profile install <git-url>`.

Profiles are operated by anyone running more than one Hermes agent: individual power users, teams shipping a reviewed internal agent, and authors publishing community or product agents.

## Key Characteristics

- **`HERMES_HOME`-scoped state**: a wrapper script sets `HERMES_HOME=~/.hermes/profiles/<name>` before launching; 119+ files resolve paths via `get_hermes_home()`, so config, `.env`, `SOUL.md`, memories, sessions, skills, state DB, gateway PID, logs, and cron jobs all scope to the profile automatically.
- **Auto command alias**: creating a profile installs an executable at `~/.local/bin/<name>` that works with every Hermes subcommand. A sticky default (`hermes profile use <name>`) makes plain `hermes` target a profile — explicitly analogized in the docs to `kubectl config use-context`.
- **NOT a sandbox and NOT a workspace**: a profile isolates *Hermes state*, not filesystem access (the agent retains the user's filesystem permissions on the `local` backend) and not the working directory (that is `terminal.cwd`). Profile isolation is an organizational boundary, not a security boundary.
- **`HERMES_HOME` vs OS `HOME`**: on host installs Hermes keeps the real OS `HOME` so external CLIs (`git`, `ssh`, `gh`, `npm`) find their existing credentials; per-profile CLI identities are opt-in via `terminal.home_mode: profile` (which sets `HOME={HERMES_HOME}/home`), with `HERMES_REAL_HOME` still exposed to subprocesses.
- **Clone variants (idempotent copies)**: `--clone` copies config/`.env`/`SOUL.md`/skills (fresh sessions/memory); `--clone-all` copies everything except per-profile history; `--clone-from <src>` selects the source directly. `export`/`import` produce full archive backups.
- **Per-profile credentials**: each profile's `.env` holds its own API keys and bot tokens; token-conflict safety blocks two profiles from polling the same Telegram/Discord/Slack/WhatsApp/Signal token.
- **Distributable**: a profile is packaged as a git repo via a `distribution.yaml` manifest; on install/update distribution-owned paths (SOUL/skills/cron/mcp.json) are replaced while user-owned paths (memories, sessions, `auth.json`, `.env`, state) are never shipped or touched.

## Related Terms


## References
- [Hermes Profiles: Running Multiple Agents](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Hermes Profile Distributions: Share a Whole Agent](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions)
- [Hermes Running Many Gateways at Once](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways)
- [Kubernetes — Configure Access to Multiple Clusters (`kubectl config use-context`)](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)

---

**Last Updated**: 2026-06-19
**Status**: Active
