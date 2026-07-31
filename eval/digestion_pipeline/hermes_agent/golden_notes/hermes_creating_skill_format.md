---
tags:
  - resource
  - documentation
  - hermes_agent
  - skills
  - developer_guide
keywords:
  - creating a hermes skill
  - SKILL.md format
  - skill vs tool decision
  - conditional skill activation
  - required_environment_variables
  - required_credential_files
  - skills config settings
  - secure setup on load
topics:
  - Hermes Agent
  - Developer Guide
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills
access_control_group: ["general"]
---

# Hermes Agent — Creating a Skill (SKILL.md Format)

## Overview

A **Hermes skill** is the preferred, code-free way to add a new capability to the agent: a directory under `skills/<category>/<name>/` whose required `SKILL.md` carries YAML frontmatter plus instruction prose, optionally accompanied by `scripts/` and `references/`. Unlike a built-in tool, a skill needs no change to the agent and is shareable with the community — the agent loads it by reading its instructions and following them with existing tools (`terminal`, `web_extract`, `read_file`). This note is the **declarative-spec half** of the skill-authoring procedure: it covers the skill-vs-tool decision, the directory layout, the full SKILL.md frontmatter schema (`name`/`description`/`version`/`platforms`/`metadata.hermes` tags + conditional `requires_*`/`fallback_for_*`/`config`/`blueprint`), environment-variable + credential-file declarations, secure on-load secret prompting with sandbox passthrough, and `config.yaml` `skills.config` settings. The authoring *lifecycle* — guidelines, blueprints, Suggested Cron Jobs, publishing, and the security scanner — is the sibling note [hermes_creating_skill_publish](hermes_creating_skill_publish.md).

## Should it be a Skill or a Tool?

Make it a **Skill** when:
- The capability can be expressed as instructions + shell commands + existing tools.
- It wraps an external CLI or API the agent can call via `terminal` or `web_extract`.
- It does not need custom Python integration or API-key management baked into the agent.
- Examples: arXiv search, git workflows, Docker management, PDF processing, email via CLI tools.

Make it a **Tool** when:
- It requires end-to-end integration with API keys, auth flows, or multi-component configuration.
- It needs custom processing logic that must execute precisely every time.
- It handles binary data, streaming, or real-time events.
- Examples: browser automation, TTS, vision analysis.

The tool path is documented separately in [hermes_adding_built_in_tool](hermes_adding_built_in_tool.md); skills are the default unless one of the tool conditions applies.

## Skill Directory Structure

Bundled skills live in `skills/` organized by category. Official optional skills use the same structure in `optional-skills/`. Only `SKILL.md` is required; `scripts/` (helper scripts) and `references/` are optional.

```text
skills/
├── research/
│   └── arxiv/
│       ├── SKILL.md              # Required: main instructions
│       └── scripts/              # Optional: helper scripts
│           └── search_arxiv.py
├── productivity/
│   └── ocr-and-documents/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
└── ...
```

## SKILL.md Format

The frontmatter declares identity, platform restriction, and the `metadata.hermes` block (tags, related skills, conditional activation, config, blueprint); the body is the instruction prose the agent reads. The full schema:

```markdown
---
name: my-skill
description: Brief description (shown in skill search results)
version: 1.0.0
author: Your Name
license: MIT
platforms: [macos, linux]          # Optional — restrict to specific OS platforms
                                   #   Valid: macos, linux, windows
                                   #   Omit to load on all platforms (default)
metadata:
  hermes:
    tags: [Category, Subcategory, Keywords]
    related_skills: [other-skill-name]
    requires_toolsets: [web]            # Optional — only show when these toolsets are active
    requires_tools: [web_search]        # Optional — only show when these tools are available
    fallback_for_toolsets: [browser]    # Optional — hide when these toolsets are active
    fallback_for_tools: [browser_navigate]  # Optional — hide when these tools exist
    config:                              # Optional — config.yaml settings the skill needs
      - key: my.setting
        description: "What this setting controls"
        default: "sensible-default"
        prompt: "Display prompt for setup"
    blueprint:                              # Optional — marks this skill a runnable automation
      schedule: "0 9 * * *"              #   cron expr / "every 2h" / ISO timestamp
      deliver: origin                    #   optional (default origin)
      prompt: "Task instruction for each run"  # optional
      no_agent: false                    # optional
required_environment_variables:          # Optional — env vars the skill needs
  - name: MY_API_KEY
    prompt: "Enter your API key"
    help: "Get one at https://example.com"
    required_for: "API access"
---

# Skill Title

Brief intro.

## When to Use
Trigger conditions — when should the agent load this skill?

## Quick Reference
Table of common commands or API calls.

## Procedure
Step-by-step instructions the agent follows.

## Pitfalls
Known failure modes and how to handle them.

## Verification
How the agent confirms it worked.
```

The `blueprint` block (schedule-in-frontmatter automation) is the on-ramp to Suggested Cron Jobs covered in [hermes_creating_skill_publish](hermes_creating_skill_publish.md).

### Platform-Specific Skills

Skills can restrict themselves to specific operating systems with the `platforms` field. When set, the skill is automatically hidden from the system prompt, `skills_list()`, and slash commands on incompatible platforms; if omitted or empty, the skill loads on all platforms (backward compatible). See `skills/apple/` for macOS-only examples.

```yaml
platforms: [macos]            # macOS only (e.g., iMessage, Apple Reminders)
platforms: [macos, linux]     # macOS and Linux
platforms: [windows]          # Windows only
```

### Conditional Skill Activation

Skills declare dependencies on tools or toolsets to control whether they appear in the system prompt for a given session. `requires_*` hides a skill unless the dependency is present; `fallback_for_*` hides it when a (better) capability is already present.

| Field | Behavior |
|-------|----------|
| `requires_toolsets` | Skill is **hidden** when ANY listed toolset is **not** available |
| `requires_tools` | Skill is **hidden** when ANY listed tool is **not** available |
| `fallback_for_toolsets` | Skill is **hidden** when ANY listed toolset **is** available |
| `fallback_for_tools` | Skill is **hidden** when ANY listed tool **is** available |

**Use case for `fallback_for_*`:** a workaround skill — e.g. a `duckduckgo-search` skill with `fallback_for_tools: [web_search]` shows only when the API-keyed `web_search` tool is not configured. **Use case for `requires_*`:** a skill that only makes sense alongside certain tools — e.g. a web-scraping workflow with `requires_toolsets: [web]` won't clutter the prompt when web tools are disabled.

### Environment Variable Requirements

Skills declare the environment variables they need under `required_environment_variables`. When the skill is loaded via `skill_view`, its required vars are automatically registered for passthrough into sandboxed execution environments (`terminal`, `execute_code`).

```yaml
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: "Tenor API key"               # Shown when prompting user
    help: "Get your key at https://tenor.com"  # Help text or URL
    required_for: "GIF search functionality"   # What needs this var
```

Each entry supports `name` (required — the env var name), `prompt` (optional — text when asking the user), `help` (optional — help text or URL for obtaining the value), and `required_for` (optional — which feature needs the var). Users can also manually configure passthrough variables in `config.yaml` under `terminal.env_passthrough`. Legacy `prerequisites.env_vars` remains a backward-compatible alias.

## Secure Setup on Load

Use `required_environment_variables` when a skill needs an API key or token. Missing values do **not** hide the skill from discovery — instead, Hermes prompts for them securely when the skill is loaded in the local CLI. The user can skip setup and keep loading the skill; **Hermes never exposes the raw secret value to the model**, and gateway/messaging sessions show local setup guidance instead of collecting secrets in-band.

**Sandbox passthrough.** When a skill is loaded, any declared `required_environment_variables` that are set are automatically passed through to `execute_code` and `terminal` sandboxes — including remote backends like Docker and Modal — so the skill's scripts can read `$TENOR_API_KEY` (or `os.environ["TENOR_API_KEY"]`) with no extra user configuration. The hardened sandbox/passthrough mechanics are covered in [hermes_contributing_dev_setup](hermes_contributing_dev_setup.md).

### Config Settings (config.yaml)

Skills declare non-secret settings stored in `config.yaml` under the `skills.config` namespace — for paths, preferences, and other non-sensitive values (as opposed to secrets, which go in `.env`).

```yaml
metadata:
  hermes:
    config:
      - key: myplugin.path
        description: Path to the plugin data directory
        default: "~/myplugin-data"
        prompt: Plugin data directory path
      - key: myplugin.domain
        description: Domain the plugin operates on
        default: ""
        prompt: Plugin domain (e.g., AI/ML research)
```

Each entry supports `key` (required — dotpath, e.g. `myplugin.path`), `description` (required), `default` (optional), and `prompt` (optional — shown during `hermes config migrate`, falling back to `description`). At runtime: values are stored under `config.yaml` `skills.config.<key>`; `hermes config migrate` scans enabled skills and prompts for unconfigured settings (also shown under "Skill Settings" in `hermes config show`); when a skill loads, its resolved config is appended to the skill message as a `[Skill config (...)]` block so the agent sees the values without reading `config.yaml`; and users can set values directly with `hermes config set skills.config.myplugin.path ~/my-data`. Rule of thumb: `required_environment_variables` for **secrets**; `config` for **paths/preferences**.

### Credential File Requirements (OAuth tokens, etc.)

Skills using OAuth or file-based credentials declare files to mount into remote sandboxes via `required_credential_files`. This is for credentials stored as **files** (not env vars) — typically OAuth token files produced by a setup script.

```yaml
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
  - path: google_client_secret.json
    description: Google OAuth2 client credentials
```

Each entry supports `path` (required — relative to `~/.hermes/`) and `description` (optional). When loaded, Hermes checks the files exist; missing files trigger `setup_needed`, while existing files are automatically mounted into Docker containers as read-only bind mounts, synced into Modal sandboxes (at creation and before each command, so mid-session OAuth works), and available on the local backend with no special handling. Rule of thumb: `required_environment_variables` for simple string keys/tokens; `required_credential_files` for OAuth token files, client secrets, service-account JSON, or certificates. See `skills/productivity/google-workspace/SKILL.md` for a complete example using both.

**Source**: `inbox/hermes_agent_docs/developer-guide/creating-skills.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills
**Last Updated**: 2026-06-19
**Status**: Active
