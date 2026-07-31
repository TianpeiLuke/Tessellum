---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - skill_format
keywords:
  - clawhub skill frontmatter
  - SKILL.md frontmatter metadata
  - metadata.openclaw runtime metadata
  - requires env bins anyBins config
  - primaryEnv envVars required
  - install specs brew node go uv
  - declaration behavior coherence
  - optional environment variables
topics:
  - OpenClaw
  - ClawHub Skill Format
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/clawhub/skill-format
access_control_group: ["general"]
---

# OpenClaw — ClawHub `SKILL.md` Frontmatter Schema

## Overview

This note models the **`SKILL.md` frontmatter schema** a ClawHub publisher declares at the top of their skill's `SKILL.md` — the YAML block the registry (and security analysis) reads on publish to learn what a skill needs to run. It covers the basic identity fields (`name` / `description` / `version`), the `metadata.openclaw` runtime block (with the `metadata.clawdbot` / `metadata.clawdis` aliases), the full field reference (`requires.env` / `bins` / `anyBins` / `config`, `primaryEnv`, `envVars`, `always`, `skillKey`, `emoji`, `homepage`, `os`, `install`, `nix`, `config`), the `install` dependency specs (`brew` / `node` / `go` / `uv`), optional environment variables via `envVars` with `required: false`, the declaration↔behavior coherence rule the security analysis enforces, and a complete example — mirroring the "Frontmatter metadata" half of the `clawhub/skill-format` source page. The complementary on-disk folder/format, slug, versioning, license, and limit rules are documented in the sibling **[oc_clawhub_skill_format](oc_clawhub_skill_format.md)** note.

## Frontmatter metadata

Skill metadata is declared in the YAML frontmatter at the top of your `SKILL.md`. This tells the registry (and security analysis) what your skill needs to run. The `SKILL.md` itself is Markdown with optional YAML frontmatter; the server extracts metadata from frontmatter during publish, and `description` is used as the skill summary in the UI/search.

### Basic frontmatter

The minimal identity block declares the skill name, a short description (which becomes the search/UI summary), and a semver version:

```yaml
---
name: my-skill
description: Short summary of what this skill does.
version: 1.0.0
---
```

### Runtime metadata (`metadata.openclaw`)

Declare your skill's runtime requirements under `metadata.openclaw` (aliases: `metadata.clawdbot`, `metadata.clawdis`). Use `requires.env` for environment variables that must be present before the skill can run, and use `envVars` when you need per-variable metadata, including optional variables with `required: false`:

```yaml
---
name: my-skill
description: Manage tasks via the Todoist API.
metadata:
  openclaw:
    requires:
      env:
        - TODOIST_API_KEY
      bins:
        - curl
    primaryEnv: TODOIST_API_KEY
---
```

### Full field reference

The `metadata.openclaw` block accepts the following fields (types and descriptions verbatim from the source page):

| Field | Type | Description |
| --- | --- | --- |
| `requires.env` | `string[]` | Required environment variables your skill expects. |
| `requires.bins` | `string[]` | CLI binaries that must all be installed. |
| `requires.anyBins` | `string[]` | CLI binaries where at least one must exist. |
| `requires.config` | `string[]` | Config file paths your skill reads. |
| `primaryEnv` | `string` | The main credential env var for your skill. |
| `envVars` | `array` | Environment variable declarations with `name`, optional `required`, and optional `description`. Set `required: false` for optional env vars. |
| `always` | `boolean` | If `true`, skill is always active (no explicit install needed). |
| `skillKey` | `string` | Override the skill's invocation key. |
| `emoji` | `string` | Display emoji for the skill. |
| `homepage` | `string` | URL to the skill's homepage or docs. |
| `os` | `string[]` | OS restrictions (e.g. `["macos"]`, `["linux"]`). |
| `install` | `array` | Install specs for dependencies (see below). |
| `nix` | `object` | Nix plugin spec (see README). |
| `config` | `object` | Clawdbot config spec (see README). |

The distinction between the three binary keys is exact: `requires.bins` lists CLI binaries that must **all** be installed, while `requires.anyBins` lists binaries where **at least one** must exist; `requires.config` lists config file paths the skill reads. `primaryEnv` names the skill's main credential env var, and `always: true` makes the skill always active without an explicit install. The `nix` and `config` objects defer their detailed shape to the README ("see README").

### Install specs

If your skill needs dependencies installed, declare them in the `install` array. Each entry is an install spec whose `kind` selects the installer; `formula` (brew) or `package` (node) names the dependency and `bins` lists the binaries it provides:

```yaml
metadata:
  openclaw:
    install:
      - kind: brew
        formula: jq
        bins: [jq]
      - kind: node
        package: typescript
        bins: [tsc]
```

Supported install kinds: `brew`, `node`, `go`, `uv`.

### Optional environment variables

Declare optional environment variables under `metadata.openclaw.envVars` and set `required: false`. Do not add optional entries to `requires.env`, because `requires.env` means the skill cannot run without them. Each `envVars` entry has a `name`, an optional `required` flag, and an optional `description`:

```yaml
metadata:
  openclaw:
    primaryEnv: TODOIST_API_KEY
    envVars:
      - name: TODOIST_API_KEY
        required: true
        description: Todoist API token used for authenticated requests.
      - name: TODOIST_PROJECT_ID
        required: false
        description: Optional default project ID when the user does not specify one.
```

### Why this matters

ClawHub's security analysis checks that what your skill declares matches what it actually does — the declaration↔behavior coherence rule. If your code references `TODOIST_API_KEY` but your frontmatter doesn't declare it under `requires.env`, `primaryEnv`, or `envVars`, the analysis will flag a metadata mismatch. Keeping declarations accurate helps your skill pass review and helps users understand what they're installing. This is the schema the scan stack reads when computing an audit's coherence question (declared metadata vs actual behavior), so an accurate frontmatter is what lets a release earn a clean audit status.

### Example: complete frontmatter

A complete `SKILL.md` frontmatter combines the identity fields, the `requires` block, `primaryEnv`, per-variable `envVars` (required and optional), and display fields (`emoji`, `homepage`):

```yaml
---
name: todoist-cli
description: Manage Todoist tasks, projects, and labels from the command line.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - TODOIST_API_KEY
      bins:
        - curl
    primaryEnv: TODOIST_API_KEY
    envVars:
      - name: TODOIST_API_KEY
        required: true
        description: Todoist API token.
      - name: TODOIST_PROJECT_ID
        required: false
        description: Optional default project ID.
    emoji: "✅"
    homepage: https://github.com/example/todoist-cli
---
```

**Source**: OpenClaw documentation — `clawhub/skill-format` (mirror `inbox/openclaw_docs/clawhub/skill-format.md`), Frontmatter metadata sections
**Last Updated**: 2026-06-22
**Status**: Active
