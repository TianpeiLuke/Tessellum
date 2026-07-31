---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - skills
keywords:
  - openclaw skill.md format
  - skill frontmatter keys
  - metadata.openclaw gating
  - requires bins anybins env config
  - command-dispatch tool
  - installer specs brew node
  - skills.entries config overrides
  - primaryEnv apiKey secretref
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

# OpenClaw — Authoring a SKILL.md: Frontmatter, Gating, and Config Overrides

## Overview

This note is the authoring-side procedure for an OpenClaw skill: how to write a `SKILL.md`, declare its frontmatter, gate it with `metadata.openclaw`, attach installer specs, and override it from config. It mirrors the **SKILL.md format**, **Optional frontmatter keys**, **Gating** (with **Installer specs**), and **Config overrides** sections of the `tools/skills` source page. The companion note `oc_tools_skills_loading` covers the discovery/precedence/snapshot lifecycle and the broader `skills.*` config tree lives in `oc_tools_skills_config`; this note stays on the per-skill authoring/declaration surface.

## SKILL.md format

A skill lives in a directory containing a `SKILL.md` file with YAML frontmatter and a markdown body. Every skill needs at minimum a `name` and `description` in the frontmatter; the markdown body is the instruction text the agent reads. The minimal form:

```markdown
---
name: image-lab
description: Generate or edit images via a provider-backed image workflow
---

When the user asks to generate an image, use the `image_generate` tool...
```

OpenClaw follows the [AgentSkills](https://agentskills.io) spec. The frontmatter parser supports **single-line keys only** — `metadata` must be a single-line JSON object. Use `{baseDir}` in the body to reference the skill folder path. The skill's `name` field also drives its slash command and allowlist key (or the directory name when `name` is missing).

### Optional frontmatter keys

These top-level frontmatter keys are optional. `homepage` (string) is the URL shown as "Website" in the macOS Skills UI (also supported via `metadata.openclaw.homepage`). The remaining keys control how the skill is exposed and invoked:

- **`user-invocable`** (boolean, default `true`) — when `true`, the skill is exposed as a user-invocable slash command.
- **`disable-model-invocation`** (boolean, default `false`) — when `true`, OpenClaw keeps the skill's instructions out of the agent's normal prompt; the skill is still available as a slash command when `user-invocable` is also `true`.
- **`command-dispatch`** (`"tool"`) — when set to `tool`, the slash command bypasses the model and dispatches directly to a registered tool.
- **`command-tool`** (string) — the tool name to invoke when `command-dispatch: tool` is set.
- **`command-arg-mode`** (`"raw"`, default `raw`) — for tool dispatch, forwards the raw args string to the tool with no core parsing; the tool receives `{ command: "<raw args>", commandName: "<slash command>", skillName: "<skill name>" }`.

## Gating

OpenClaw filters skills at load time using `metadata.openclaw` (single-line JSON in the frontmatter). A skill with no `metadata.openclaw` block is always eligible unless explicitly disabled. A gated skill example:

```markdown
---
name: image-lab
description: Generate or edit images via a provider-backed image workflow
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"], "config": ["browser.enabled"] },
        "primaryEnv": "GEMINI_API_KEY",
      },
  }
---
```

The `metadata.openclaw` keys are: **`always`** (boolean) — when `true`, always include the skill and skip all other gates; **`emoji`** (string) — optional emoji shown in the macOS Skills UI; **`homepage`** (string) — optional URL shown as "Website" in the macOS Skills UI; **`os`** (`"darwin" | "linux" | "win32"`) — platform filter, when set the skill is only eligible on the listed OSes; and **`primaryEnv`** (string) — the env var name associated with `skills.entries.<name>.apiKey`. The `install` key (object array) holds optional installer specs used by the macOS Skills UI (brew / node / go / uv / download), detailed below.

The `requires` block declares the eligibility predicates checked at load time: **`requires.bins`** (string[]) — each binary must exist on `PATH`; **`requires.anyBins`** (string[]) — at least one binary must exist on `PATH`; **`requires.env`** (string[]) — each env var must exist in the process or be provided via config; and **`requires.config`** (string[]) — each `openclaw.json` path must be truthy. Legacy `metadata.clawdbot` blocks are still accepted when `metadata.openclaw` is absent, so older installed skills keep their dependency gates and installer hints; new skills should use `metadata.openclaw`.

### Installer specs

Installer specs (the `metadata.openclaw.install` array) tell the macOS Skills UI how to install a dependency. A brew installer example:

```markdown
---
name: gemini
description: Use Gemini CLI for coding assistance and Google search lookups.
metadata:
  {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["gemini"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gemini-cli",
              "bins": ["gemini"],
              "label": "Install Gemini CLI (brew)",
            },
          ],
      },
  }
---
```

**Installer selection rules:** When multiple installers are listed, the gateway picks one preferred option (brew when available, otherwise node). If all installers are `download`, OpenClaw lists each entry so you can see all available artifacts. Specs can include `os: ["darwin"|"linux"|"win32"]` to filter by platform. Node installs honor `skills.install.nodeManager` in `openclaw.json` (default: npm; options: npm / pnpm / yarn / bun) — this only affects skill installs; the Gateway runtime should still be Node. The overall gateway installer preference order is: Homebrew → uv → configured node manager → go → download.

**Per-installer details:** For **Homebrew**, OpenClaw does not auto-install Homebrew or translate brew formulas into system package commands; in Linux containers without `brew`, brew-only installers are hidden — use a custom image or install the dependency manually. For **Go**, if `go` is missing and `brew` is available, the gateway installs Go via Homebrew first and sets `GOBIN` to Homebrew's `bin`. For **Download**, the fields are `url` (required), `archive` (`tar.gz` | `tar.bz2` | `zip`), `extract` (default: auto when archive detected), `stripComponents`, and `targetDir` (default: `~/.openclaw/tools/<skillKey>`).

**Sandboxing notes:** `requires.bins` is checked on the **host** at skill load time. If an agent runs in a sandbox, the binary must also exist **inside the container**. Install it via `agents.defaults.sandbox.docker.setupCommand` or a custom image; `setupCommand` runs once after container creation and requires network egress, a writable root FS, and a root user in the sandbox.

## Config overrides

Toggle and configure bundled or managed skills under `skills.entries` in `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    entries: {
      "image-lab": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" },
        env: { GEMINI_API_KEY: "GEMINI_KEY_HERE" },
        config: {
          endpoint: "https://example.invalid",
          model: "nano-pro",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

The per-entry fields are: **`enabled`** (boolean) — `false` disables the skill even when bundled or installed (the `coding-agent` bundled skill is opt-in: set `skills.entries.coding-agent.enabled: true` and ensure one of `claude`, `codex`, `opencode`, or another supported CLI is installed and authenticated); **`apiKey`** (`string | { source, provider, id }`) — convenience field for skills that declare `metadata.openclaw.primaryEnv`, supporting a plaintext string or a SecretRef object; **`env`** (`Record<string, string>`) — environment variables injected for the agent run, only injected when the variable is not already set in the process; and **`config`** (object) — an optional bag for custom per-skill configuration fields. A separate **`allowBundled`** (string[]) is an optional allowlist for **bundled** skills only: when set, only bundled skills in the list are eligible, while managed and workspace skills are unaffected.

Config keys match the **skill name** by default. If a skill defines `metadata.openclaw.skillKey`, use that key under `skills.entries`. Quote hyphenated names — JSON5 allows quoted keys.

**Source**: OpenClaw documentation — `tools/skills` (mirror `inbox/openclaw_docs/tools/skills.md`)
**Last Updated**: 2026-06-22
**Status**: Active
