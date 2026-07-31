---
tags:
  - resource
  - documentation
  - hermes_agent
  - skills
  - knowledge_memory
keywords:
  - hermes skills system
  - on-demand knowledge documents
  - progressive disclosure
  - blank slate no-skills
  - secure setup on load
  - external skill directories
  - agentskills.io
topics:
  - Hermes Agent
  - Skills
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
access_control_group: ["general"]
---

# Hermes Agent — Skills System

## Overview

A Hermes **skill** is an on-demand knowledge document the agent loads only when it actually needs it. Skills follow a **progressive disclosure** pattern (a three-level load ladder) to minimize token usage and are compatible with the [agentskills.io](https://agentskills.io/specification) open standard. All skills live in the single source-of-truth directory `~/.hermes/skills/` — bundled skills are copied there on fresh install, and hub-installed plus agent-created skills also land there; the agent can modify or delete any of them. Hermes can additionally scan **external skill directories** alongside the local one, and a profile can opt out of bundled skills entirely (blank slate). This note covers what a skill IS and how it loads; the SKILL.md file model is in [hermes_skill_md_format_bundles](hermes_skill_md_format_bundles.md) and the install/create/maintain procedures are in [hermes_skills_hub_agent_managed](hermes_skills_hub_agent_managed.md).

## What a Skill Is

Skills are on-demand knowledge documents the agent can load when needed. They follow a progressive disclosure pattern to minimize token usage and are compatible with the agentskills.io open standard.

All skills live in **`~/.hermes/skills/`** — the primary directory and source of truth. On fresh install, bundled skills are copied from the repo. Hub-installed and agent-created skills also go here. The agent can modify or delete any skill. Hermes can also be pointed at external skill directories — additional folders scanned alongside the local one (see [External Skill Directories](#external-skill-directories)).

## Starting with a Blank Slate

By default every profile is seeded with the bundled skill catalog, and each `hermes update` adds any newly bundled skills. To create a profile with **no bundled skills** that stays empty across updates, there are three paths — install-time (`--no-skills`), profile-create-time, and a runtime toggle on an already-installed profile:

```bash
hermes skills opt-out            # stop future seeding — nothing on disk is touched
hermes skills opt-out --remove   # also delete UNMODIFIED bundled skills (confirms first)
hermes skills opt-in --sync      # undo: remove the marker and re-seed now
```

All three paths write a `.no-bundled-skills` marker into the profile directory. While the marker is present, the installer, `hermes update`, and any skill sync all skip bundled-skill seeding for that profile. Deleting the marker (or running `hermes skills opt-in`) re-enables seeding. **Safe by default:** `hermes skills opt-out` only stops *future* seeding — it never deletes anything already on disk. The optional `--remove` flag deletes bundled skills **only** when they are unmodified (byte-identical to the version Hermes installed); skills you have edited, hub-installed skills, and skills you wrote yourself are always kept.

## Using Skills

Every installed skill is automatically available as a slash command (`/gif-search funny cats`, `/plan design a rollout`, etc.). Running `/<skill-name>` loads the skill's instructions; running just the skill name (`/excalidraw`) loads it and lets the agent ask what you need. The bundled `plan` skill is a good example: `/plan [request]` loads instructions telling Hermes to inspect context, write a markdown implementation plan instead of executing the task, and save the result under `.hermes/plans/` relative to the active workspace/backend working directory.

Skills can also be reached through natural conversation:

```bash
hermes chat --toolsets skills -q "What skills do you have?"
hermes chat --toolsets skills -q "Show me the axolotl skill"
```

## Progressive Disclosure

Skills use a token-efficient loading pattern with three levels — the agent only loads the full skill content when it actually needs it:

```
Level 0: skills_list()           → [{name, description, category}, ...]   (~3k tokens)
Level 1: skill_view(name)        → Full content + metadata       (varies)
Level 2: skill_view(name, path)  → Specific reference file       (varies)
```

Level 0 is the always-resident index (a compact `{name, description, category}` list, ~3k tokens); Level 1 expands one skill's full content + metadata on demand; Level 2 reaches into a specific reference file within that skill. This lazy expansion is what keeps the skill catalog from consuming the context window.

## Secure Setup on Load

Skills can declare required environment variables without disappearing from discovery. When a missing value is encountered, Hermes asks for it securely — but **only when the skill is actually loaded in the local CLI**; you can skip setup and keep using the skill. Messaging surfaces never ask for secrets in chat — they tell you to use `hermes setup` or `~/.hermes/.env` locally instead.

```yaml
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: Tenor API key
    help: Get a key from https://developers.google.com/tenor
    required_for: full functionality
```

Once set, declared env vars are **automatically passed through** to `execute_code` and `terminal` sandboxes — the skill's scripts can use `$TENOR_API_KEY` directly. For non-skill env vars, the `terminal.env_passthrough` config option is used instead (config detail belongs to the configuration sub-plan).

### Skill Config Settings

Skills can also declare non-secret config settings (paths, preferences) stored in `config.yaml` under `metadata.hermes.config` (key/description/default/prompt). Settings are stored under `skills.config` in your config.yaml; `hermes config migrate` prompts for unconfigured settings and `hermes config show` displays them. When a skill loads, its resolved config values are injected into the context so the agent knows the configured values automatically. (Full Skill Settings config reference is owned by the configuration sub-plan; the SKILL.md frontmatter schema is in [hermes_skill_md_format_bundles](hermes_skill_md_format_bundles.md).)

## External Skill Directories

If you maintain skills outside of Hermes — for example a shared `~/.agents/skills/` directory used by multiple AI tools — you can tell Hermes to scan those directories too by adding `external_dirs` under the `skills` section in `~/.hermes/config.yaml`. Paths support `~` expansion and `${VAR}` environment-variable substitution:

```yaml
skills:
  external_dirs:
    - ~/.agents/skills
    - /home/shared/team-skills
    - ${SKILLS_REPO}/skills
```

### How it works

- **Create locally, update in place**: new agent-created skills are written to `~/.hermes/skills/`. Existing skills are modified where they are found, including skills under `external_dirs`, when the agent uses `skill_manage` actions such as `patch`, `edit`, `write_file`, `remove_file`, or `delete`.
- **External dirs are not a write-protection boundary**: if an external skill directory is writable by the Hermes process, agent-managed skill updates can change files in it. Use filesystem permissions or a separate profile/toolset setup if shared external skills must stay read-only.
- **Local precedence**: if the same skill name exists in both the local dir and an external dir, the local version wins (shadows the external one).
- **Full integration**: external skills appear in the system-prompt index, `skills_list`, `skill_view`, and as `/skill-name` slash commands — no different from local skills.
- **Non-existent paths are silently skipped**: if a configured directory doesn't exist, Hermes ignores it without errors, which is useful for optional shared directories that may not be present on every machine.

**Source**: `inbox/hermes_agent_docs/user-guide/features/skills.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
**Last Updated**: 2026-06-19
**Status**: Active
