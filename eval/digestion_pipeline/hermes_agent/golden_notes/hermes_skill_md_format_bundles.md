---
tags:
  - resource
  - documentation
  - hermes_agent
  - skills
  - file_format
keywords:
  - skill.md format
  - yaml frontmatter
  - media delivery directives
  - conditional activation
  - skill directory structure
  - skill bundles
topics:
  - Hermes Agent
  - Skills System
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
access_control_group: ["general"]
---

# Hermes Agent — SKILL.md Format and Skill Bundles

## Overview

This note documents the **file model** of a Hermes skill: the `SKILL.md` manifest (YAML frontmatter + markdown body), the on-disk skill-package layout, the media-delivery directives that shape how a skill's output is delivered to chat, the conditional-activation fields that show/hide a skill based on available tools, and **skill bundles** (tiny YAML aliases that group several skills under one slash command). It is the structural counterpart to the [skills system concept](hermes_skills_system.md) (what a skill IS / how it loads) and the [Skills Hub procedures](hermes_skills_hub_agent_managed.md) (how skills are installed/created). A skill is a single directory containing a required `SKILL.md`; the frontmatter is what `skills_list()` reads at Level 0 and what the agent loads at Level 1.

## SKILL.md Format

A skill is defined by a `SKILL.md` file: YAML frontmatter (metadata) followed by a markdown body (the instructions the agent loads). The frontmatter carries `name`, `description`, `version`, an optional `platforms` restriction, and a `metadata.hermes.*` block for tags, category, conditional-activation fields, and config settings:

```markdown
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
platforms: [macos, linux]     # Optional — restrict to specific OS platforms
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    fallback_for_toolsets: [web]    # Optional — conditional activation (see below)
    requires_toolsets: [terminal]   # Optional — conditional activation (see below)
    config:                          # Optional — config.yaml settings
      - key: my.setting
        description: "What this controls"
        default: "value"
        prompt: "Prompt for setup"
---

# Skill Title

## When to Use
Trigger conditions for this skill.

## Procedure
1. Step one
2. Step two

## Pitfalls
- Known failure modes and fixes

## Verification
How to confirm it worked.
```

### Platform-Specific Skills

Skills can restrict themselves to specific operating systems using the `platforms` field. The accepted values are `macos` (macOS / Darwin), `linux`, and `windows` — for example `platforms: [macos]` (macOS only, e.g. iMessage, Apple Reminders, FindMy) or `platforms: [macos, linux]`. When set, the skill is **automatically hidden** from the system prompt, `skills_list()`, and slash commands on incompatible platforms. If `platforms` is omitted, the skill loads on all platforms.

## Skill Output and Media Delivery

When a skill response (or any agent response) includes a **bare absolute path to a media file** — for example `/home/user/screenshots/diagram.png` — the gateway auto-detects it, strips it from the visible text, and delivers the file natively to the user's chat (Telegram photo, Discord attachment, etc.) instead of leaving the raw path in the message.

For audio specifically, the `[[audio_as_voice]]` directive promotes audio files to native voice-message bubbles on platforms that support them (Telegram, WhatsApp).

### Forcing document-style delivery: `[[as_document]]`

Sometimes you want the **opposite** of inline preview: the file delivered as a downloadable attachment, not a re-compressed image bubble. The classic example is a high-resolution screenshot or chart — Telegram's `sendPhoto` recompresses it to ~200 KB at 1280 px, destroying readability, whereas a 1–2 MB PNG sent via `sendDocument` keeps the original bytes intact. If a response (or any text inside it — typically the last line) contains the literal directive `[[as_document]]` (placed on its own line, after the bare media path such as `/home/user/.hermes/cache/chart-q4-2025.png`), every media path extracted from that response is delivered as a document/file attachment rather than an image bubble.

The directive is stripped before delivery, so users never see it. Granularity is intentionally **all-or-nothing per response**: emit `[[as_document]]` once and every image path in the same response is delivered as a document — mirroring the scope of `[[audio_as_voice]]`. Use it from a skill when you produce screenshots/charts the user needs as files, or when the default lossy preview would obscure detail (small text, pixel-accurate diagrams, color-sensitive renders). Platforms without a separate document path (e.g. SMS) fall back to whatever attachment mechanism they have.

## Conditional Activation (Fallback Skills)

Skills can automatically show or hide themselves based on which tools are available in the current session. This is most useful for **fallback skills** — free or local alternatives that should only appear when a premium tool is unavailable. The four conditional fields are declared under `metadata.hermes`:

```yaml
metadata:
  hermes:
    fallback_for_toolsets: [web]      # Show ONLY when these toolsets are unavailable
    requires_toolsets: [terminal]     # Show ONLY when these toolsets are available
    fallback_for_tools: [web_search]  # Show ONLY when these specific tools are unavailable
    requires_tools: [terminal]        # Show ONLY when these specific tools are available
```

| Field | Behavior |
|-------|----------|
| `fallback_for_toolsets` | Skill is **hidden** when the listed toolsets are available. Shown when they're missing. |
| `fallback_for_tools` | Same, but checks individual tools instead of toolsets. |
| `requires_toolsets` | Skill is **hidden** when the listed toolsets are unavailable. Shown when they're present. |
| `requires_tools` | Same, but checks individual tools. |

**Example:** The built-in `duckduckgo-search` skill uses `fallback_for_toolsets: [web]`. When `FIRECRAWL_API_KEY` is set the web toolset is available and the agent uses `web_search` — the DuckDuckGo skill stays hidden. If the API key is missing, the web toolset is unavailable and the DuckDuckGo skill automatically appears as a fallback. Skills without any conditional fields are always shown.

## Skill Directory Structure

A skill is a directory under `~/.hermes/skills/` (the single source of truth). The directory contains a required `SKILL.md` plus optional supporting subdirectories — `references/` (additional docs), `templates/` (output formats), `scripts/` (helper scripts callable from the skill), and `assets/` (supplementary files). Category directories group skills, and Hermes maintains hidden state files (`.hub/` for Skills Hub state, `.bundled_manifest` tracking seeded bundled skills):

```text
~/.hermes/skills/                  # Single source of truth
├── mlops/                         # Category directory
│   ├── axolotl/
│   │   ├── SKILL.md               # Main instructions (required)
│   │   ├── references/            # Additional docs
│   │   ├── templates/             # Output formats
│   │   ├── scripts/               # Helper scripts callable from the skill
│   │   └── assets/                # Supplementary files
│   └── vllm/
│       └── SKILL.md
├── devops/
│   └── deploy-k8s/                # Agent-created skill
│       ├── SKILL.md
│       └── references/
├── .hub/                          # Skills Hub state
│   ├── lock.json
│   ├── quarantine/
│   └── audit.log
└── .bundled_manifest              # Tracks seeded bundled skills
```

## Skill Bundles

Skill bundles are **tiny YAML files that group several skills under a single slash command**. When you run `/<bundle-name>`, every skill listed in the bundle loads at once — useful when a particular task always benefits from the same set of skills together. A bundle is just a YAML alias; it does **not** install the skills for you — they must already be present in `~/.hermes/skills/` or an external skill directory.

### Quick example

Create a bundle, then invoke it; the agent receives all listed skills loaded into one user message, with any text after the slash command attached as a user instruction:

```bash
# Create a bundle for backend feature work
hermes bundles create backend-dev \
  --skill github-code-review \
  --skill test-driven-development \
  --skill github-pr-workflow \
  -d "Backend feature work — review, test, PR workflow"

# Then in the CLI or any gateway platform:
/backend-dev refactor the auth middleware
```

### YAML schema

Bundles live in **`~/.hermes/skill-bundles/<slug>.yaml`**:

```yaml
name: backend-dev
description: Backend feature work — review, test, PR workflow.
skills:
  - github-code-review
  - test-driven-development
  - github-pr-workflow
instruction: |
  Always start by writing failing tests, then implement.
  Open the PR through the standard workflow with co-author tags.
```

Fields:
- `name` (optional — defaults to the filename stem) — the bundle's display name, normalized to a hyphen slug for the slash command (`Backend Dev` → `/backend-dev`).
- `description` (optional) — short text shown in `/bundles` and `hermes bundles list`.
- `skills` (required, non-empty list) — skill names or paths relative to your skills directory; use the same identifier you'd pass to `/<skill-name>`.
- `instruction` (optional) — extra guidance prepended to the loaded skill content, useful for codifying "how we always use these together."

### Managing bundles

The `hermes bundles` CLI lists, inspects, creates, overwrites (`--force`), deletes, and re-scans bundles; from inside a chat session `/bundles` lists every installed bundle and its skills:

```bash
hermes bundles list                       # List all installed bundles
hermes bundles show backend-dev           # Inspect one bundle
hermes bundles create research            # Create interactively (omit --skill to enter per line)
hermes bundles create backend-dev --skill ... --force   # Overwrite an existing bundle
hermes bundles delete backend-dev         # Delete a bundle
hermes bundles reload                     # Re-scan ~/.hermes/skill-bundles/ and report changes
```

### Behavior and when to use

- **Bundles take precedence over individual skills** when slugs collide — if a bundle and a skill are both named `research`, `/research` invokes the bundle (intentional: you opted in by naming it).
- **Missing skills are skipped, not fatal** — the bundle still loads the skills that resolve, and the agent gets a note listing what was skipped.
- **Bundles work in every surface** — interactive CLI, TUI, dashboard chat, and every gateway platform — because dispatch is centralized with individual skill commands.
- **Bundles do not invalidate the prompt cache** — they generate a fresh user message at invocation time, the same way `/<skill-name>` does, with no system-prompt mutation.

Use a bundle when you always pair the same skills for a recurring task (`/backend-dev`, `/release-prep`, `/incident-response`), want a shorter mental model than typing several `/skill` invocations, or want to ship a team-wide "task profile" by checking the bundle YAML into a shared dotfiles repo and symlinking it into `~/.hermes/skill-bundles/`.

**Source**: `inbox/hermes_agent_docs/user-guide/features/skills.md` (§SKILL.md Format, §Skill output and media delivery, §Conditional Activation, §Skill Directory Structure, §Skill Bundles) · https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
**Last Updated**: 2026-06-19
**Status**: Active
