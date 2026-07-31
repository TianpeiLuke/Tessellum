---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - skills
keywords:
  - openclaw skill loading order
  - skill precedence sources
  - per-agent vs shared skills
  - agent skill allowlists
  - plugin skills extraDirs
  - installing skills from clawhub
  - skill snapshot and refresh
  - skill token impact formula
  - skills.load watch
  - untrusted skill security
topics:
  - OpenClaw
  - Skills
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/skills
access_control_group: ["general"]
---

# OpenClaw — Skill Loading, Precedence, and Scoping

## Overview

This note is the procedure for how OpenClaw **discovers, prioritizes, scopes, installs, and snapshots skills** — the markdown instruction files (each a directory with a `SKILL.md`) that teach an agent how and when to use tools. It covers the 6-level loading-precedence order, per-agent vs shared roots, agent allowlists, plugin-shipped skills, the Skill Workshop pointer, ClawHub/Git/local install commands, the security/path-containment rules, host-scoped environment injection, session snapshot/refresh behavior, and the deterministic token-impact formula — mirroring the lifecycle half of the `tools/skills` source page. The SKILL.md authoring format, the `metadata.openclaw` gating block, installer specs, and `skills.entries` config overrides are documented in the sibling note `oc_tools_skills_format_gating`; the full `skills.*` config schema is in `oc_tools_skills_config`.

## Loading order

OpenClaw loads bundled skills plus any local overrides and filters them at load time based on environment, config, and binary presence. It loads from the following sources, **highest precedence first** — when the same skill name appears in multiple places, the highest source wins:

| Priority    | Source                 | Path                                    |
| ----------- | ---------------------- | --------------------------------------- |
| 1 — highest | Workspace skills       | `<workspace>/skills`                    |
| 2           | Project agent skills   | `<workspace>/.agents/skills`            |
| 3           | Personal agent skills  | `~/.agents/skills`                      |
| 4           | Managed / local skills | `~/.openclaw/skills`                    |
| 5           | Bundled skills         | shipped with the install                |
| 6 — lowest  | Extra directories      | `skills.load.extraDirs` + plugin skills |

Skill roots support grouped layouts: OpenClaw discovers a skill whenever a `SKILL.md` appears anywhere under a configured root — both `<workspace>/skills/research/SKILL.md` and `<workspace>/skills/personal/research/SKILL.md` are found as `"research"`. The folder path is for organization only; the skill's name, slash command, and allowlist key all come from the `name` frontmatter field (or the directory name when `name` is missing). Codex CLI's native `$CODEX_HOME/skills` directory is **not** an OpenClaw skill root — run `openclaw migrate plan codex` to inventory those skills, then `openclaw migrate codex` to copy them into your OpenClaw workspace.

## Per-agent vs shared skills

In multi-agent setups each agent has its own workspace, so the path you place a skill under determines its visibility. Use the scope that matches the desired audience:

| Scope          | Path                         | Visible to                  |
| -------------- | ---------------------------- | --------------------------- |
| Per-agent      | `<workspace>/skills`         | Only that agent             |
| Project-agent  | `<workspace>/.agents/skills` | Only that workspace's agent |
| Personal-agent | `~/.agents/skills`           | All agents on this machine  |
| Shared managed | `~/.openclaw/skills`         | All agents on this machine  |
| Extra dirs     | `skills.load.extraDirs`      | All agents on this machine  |

## Agent allowlists

Skill **location** (precedence) and skill **visibility** (which agent can use it) are separate controls. Allowlists restrict which skills an agent sees regardless of where they are loaded from, configured under `agents`:

```json5
{
  agents: {
    defaults: {
      skills: ["github", "weather"], // shared baseline
    },
    list: [
      { id: "writer" }, // inherits github, weather
      { id: "docs", skills: ["docs-search"] }, // replaces defaults entirely
      { id: "locked-down", skills: [] }, // no skills
    ],
  },
}
```

The allowlist rules are: omit `agents.defaults.skills` to leave all skills unrestricted by default; omit `agents.list[].skills` to inherit `agents.defaults.skills`; set `agents.list[].skills: []` to expose no skills for that agent; and a non-empty `agents.list[].skills` list is the **final** set — it does not merge with defaults. The effective allowlist applies across prompt building, slash-command discovery, sandbox sync, and skill snapshots.

## Plugins and skills

Plugins can ship their own skills by listing `skills` directories in `openclaw.plugin.json` (paths relative to the plugin root). Plugin skills load when the plugin is enabled — for example, the browser plugin ships a `browser-automation` skill for multi-step browser control. Plugin skill directories merge at the same low-precedence level as `skills.load.extraDirs`, so a same-named bundled, managed, agent, or workspace skill overrides them. Gate them via `metadata.openclaw.requires.config` on the plugin's config entry.

## Skill Workshop

Skill Workshop is a proposal queue between the agent and your active skill files: when the agent spots reusable work it drafts a proposal instead of writing directly to `SKILL.md`, and you review and approve before anything changes. The CLI surface is `openclaw skills workshop list`, `openclaw skills workshop inspect <proposal-id>`, and `openclaw skills workshop apply <proposal-id>`. The full lifecycle, CLI reference, and configuration live in the dedicated Skill Workshop note (`oc_tools_skill_workshop`, to06 planned).

## Installing from ClawHub

ClawHub (`https://clawhub.ai`) is the public skills registry. Use `openclaw skills` commands for install and update, or the `clawhub` CLI for publish and sync:

| Action                             | Command                                                |
| ---------------------------------- | ------------------------------------------------------ |
| Install a skill into the workspace | `openclaw skills install <slug>`                       |
| Install from a Git repository      | `openclaw skills install git:owner/repo@ref`           |
| Install a local skill directory    | `openclaw skills install ./path/to/skill --as my-tool` |
| Install for all local agents       | `openclaw skills install <slug> --global`              |
| Update all workspace skills        | `openclaw skills update --all`                         |
| Update a shared managed skill      | `openclaw skills update <slug> --global`               |
| Update all shared managed skills   | `openclaw skills update --all --global`                |
| Verify a skill's trust envelope    | `openclaw skills verify <slug>`                        |
| Print the generated Skill Card     | `openclaw skills verify <slug> --card`                 |
| Publish / sync via ClawHub CLI     | `clawhub sync --all`                                   |

`openclaw skills install` installs into the active workspace `skills/` directory by default; add `--global` to install into the shared `~/.openclaw/skills` directory, visible to all local agents unless agent allowlists narrow it. Git and local installs expect `SKILL.md` at the source root, and the slug comes from `SKILL.md` frontmatter `name` when valid, then falls back to the directory or repository name (override with `--as <slug>`); `openclaw skills update` tracks ClawHub installs only, so Git or local sources must be reinstalled to refresh them. For verification, `openclaw skills verify <slug>` asks ClawHub for the skill's `clawhub.skill.verify.v1` trust envelope, installed ClawHub skills verify against the version and registry recorded in `.clawhub/origin.json`, ClawHub skill pages expose the latest security scan state (with detail pages for VirusTotal, ClawScan, and static analysis), the command exits non-zero when ClawHub marks verification as failed, and publishers recover false positives through the ClawHub dashboard or `clawhub skill rescan <slug>`. Gateway clients that need non-ClawHub delivery can stage a zip skill archive with `skills.upload.begin`, `skills.upload.chunk`, and `skills.upload.commit`, then install with `skills.install({ source: "upload", ... })` — this path is off by default and requires `skills.install.allowUploadedArchives: true` in `openclaw.json` (normal ClawHub installs never need that setting).

## Security

Treat third-party skills as **untrusted code**: read them before enabling, and prefer sandboxed runs for untrusted inputs and risky tools (see Sandboxing for agent-side controls). Three security boundaries govern skill loading. **Path containment:** workspace, project-agent, and extra-dir skill discovery only accepts skill roots whose resolved realpath stays inside the configured root, unless `skills.load.allowSymlinkTargets` explicitly trusts a target root, and Skill Workshop writes through those trusted targets only when `skills.workshop.allowSymlinkTargetWrites` is enabled; managed `~/.openclaw/skills` and personal `~/.agents/skills` may contain symlinked skill folders, but every `SKILL.md` realpath must still stay inside its resolved skill directory. **Operator install policy:** configure `security.installPolicy` to run a trusted local policy command before skill installs continue — the policy receives metadata and the staged source path, applies to ClawHub, uploaded, Git, local, update, and dependency-installer paths, and fails closed when the command cannot return a valid decision (full schema in `oc_tools_skills_config`). **Secret injection scope:** `skills.entries.*.env` and `skills.entries.*.apiKey` inject secrets into the **host** process for that agent turn only — not into the sandbox — so keep secrets out of prompts and logs.

## Environment injection

When an agent run starts, OpenClaw performs four steps in order: (1) **reads skill metadata** — resolves the effective skill list for the agent, applying gating rules, allowlists, and config overrides; (2) **injects env and API keys** — applies `skills.entries.<key>.env` and `skills.entries.<key>.apiKey` to `process.env` for the duration of the run; (3) **builds the system prompt** — compiles eligible skills into a compact XML block injected into the system prompt; and (4) **restores the environment** — restores the original environment after the run ends. Env injection is scoped to the **host** agent run, not the sandbox: inside a sandbox `env` and `apiKey` have no effect (see `oc_tools_skills_config` for passing secrets into sandboxed runs). For the bundled `claude-cli` backend, OpenClaw also materializes the same eligible skill snapshot as a temporary Claude Code plugin and passes it via `--plugin-dir`; other CLI backends use the prompt catalog only.

## Snapshots and refresh

OpenClaw snapshots eligible skills **when a session starts** and reuses that list for all subsequent turns in the session, so changes to skills or config take effect on the next new session. Skills refresh mid-session in two cases — the skills watcher detects a `SKILL.md` change, or a new eligible remote node connects — and the refreshed list is picked up on the next agent turn; if the effective agent allowlist changes, OpenClaw refreshes the snapshot to keep visible skills aligned. By default OpenClaw watches skill folders and bumps the snapshot when `SKILL.md` files change, configured under `skills.load`:

```json5
{
  skills: {
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills"],
      allowSymlinkTargets: ["~/Projects/manager/skills"],
      watch: true,
      watchDebounceMs: 250,
    },
  },
}
```

Use `allowSymlinkTargets` for intentional symlinked layouts where a skill root symlink points outside the configured root (for example `<workspace>/skills/manager -> ~/Projects/manager/skills`), and enable `skills.workshop.allowSymlinkTargetWrites` only when Skill Workshop should also apply proposals through those trusted symlinked paths. For remote macOS nodes, if the Gateway runs on Linux but a **macOS node** is connected with `system.run` allowed, OpenClaw can treat macOS-only skills as eligible when the required binaries are present on that node, and the agent should run those skills via the `exec` tool with `host=node`; offline nodes do **not** make remote-only skills visible, and if a node stops answering bin probes OpenClaw clears its cached bin matches.

## Token impact

When skills are eligible, OpenClaw injects a compact XML block into the system prompt and the cost is deterministic:

```text
total = 195 + Σ (97 + len(name) + len(description) + len(filepath))
```

The base overhead (only when ≥ 1 skill) is ~195 characters; each skill adds ~97 characters plus your `name`, `description`, and `location` field lengths; XML escaping expands `& < > " '` into entities, adding a few characters per occurrence; and at ~4 chars/token, 97 chars ≈ 24 tokens per skill before field lengths. Keep descriptions short and descriptive to minimize prompt overhead.

**Source**: OpenClaw documentation — `tools/skills` (mirror `inbox/openclaw_docs/tools/skills.md`)
**Last Updated**: 2026-06-22
**Status**: Active
