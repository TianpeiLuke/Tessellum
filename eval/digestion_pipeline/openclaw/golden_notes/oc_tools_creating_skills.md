---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - skills
keywords:
  - openclaw creating skills
  - skill.md frontmatter reference
  - openclaw skills list
  - skill conditional activation gating
  - skill workshop propose-create
  - publishing to clawhub
  - baseDir skill body
  - disable-model-invocation command-dispatch
topics:
  - OpenClaw
  - Skills Authoring
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/creating-skills
access_control_group: ["general"]
---

# OpenClaw — Creating and Publishing Agent Skills

## Overview

This note is the end-to-end **procedure** for authoring OpenClaw agent skills, mirroring the `tools/creating-skills` source page. A skill teaches the agent how and when to use tools; each skill is a directory containing a `SKILL.md` file with YAML frontmatter plus markdown instructions, and OpenClaw loads skills from several roots in a defined precedence order. The procedure walks the create→write→verify→test loop, the full `SKILL.md` frontmatter reference (required + optional fields and the `{baseDir}` token), gating a skill with conditional activation, proposing a skill through the Skill Workshop for operator review, publishing to ClawHub, and the authoring best practices.

## Create your first skill

The first-skill walkthrough has four steps:

1. **Create the skill directory.** Skills live in your workspace `skills/` folder. Create a directory for the new skill with `mkdir -p ~/.openclaw/workspace/skills/hello-world`. You can group skills in subfolders for organization — the skill is still named by the `SKILL.md` frontmatter, not by the folder path, so `mkdir -p ~/.openclaw/workspace/skills/personal/hello-world` still produces a skill named `hello-world` invoked as `/hello-world`.
2. **Write `SKILL.md`** inside the directory. The frontmatter defines metadata; the body gives the agent instructions (see the starter template below).
3. **Verify the skill loaded** with `openclaw skills list`. OpenClaw watches `SKILL.md` files under skills roots by default. If the watcher is disabled or you are continuing an existing session, start a new one so the agent receives the refreshed list — either `/new` from chat (archives the current session and starts fresh) or `openclaw gateway restart`.
4. **Test it** by sending a message that should trigger the skill, e.g. `openclaw agent --message "give me a greeting"`, or by opening a chat and asking the agent directly. Use `/skill hello-world` to invoke it explicitly by name.

A minimal `SKILL.md` starter — frontmatter metadata followed by markdown instructions the agent reads:

```markdown
---
name: hello-world
description: A simple skill that prints a greeting.
---

# Hello World

When the user asks for a greeting, use the `exec` tool to run:
echo "Hello from your custom skill!"
```

The naming rules for that frontmatter: use lowercase letters, digits, and hyphens for `name`; keep the directory name and frontmatter `name` aligned; and keep `description` to one line under 160 characters, since it is shown to the agent and in slash-command discovery.

## SKILL.md reference

### Required fields

| Field         | Description                                                     |
| ------------- | --------------------------------------------------------------- |
| `name`        | Unique slug using lowercase letters, digits, and hyphens        |
| `description` | One-line description shown to the agent and in discovery output |

### Optional frontmatter keys

| Field                      | Default | Description                                                                      |
| -------------------------- | ------- | -------------------------------------------------------------------------------- |
| `user-invocable`           | `true`  | Expose the skill as a user slash command                                         |
| `disable-model-invocation` | `false` | Keep the skill out of the agent's system prompt (still runs via `/skill`)        |
| `command-dispatch`         | —       | Set to `tool` to route the slash command directly to a tool, bypassing the model |
| `command-tool`             | —       | Tool name to invoke when `command-dispatch: tool` is set                         |
| `command-arg-mode`         | `raw`   | For tool dispatch, forwards the raw args string to the tool                      |
| `homepage`                 | —       | URL shown as "Website" in the macOS Skills UI                                    |

For gating fields (`requires.bins`, `requires.env`, etc.) see the Skills — Gating reference.

### Using `{baseDir}`

Use `{baseDir}` in the skill body to reference files inside the skill directory without hardcoding paths — for example, `Run the helper script at` ``{baseDir}/scripts/run.sh`` `.`

## Adding conditional activation

Gate a skill so it only loads when its dependencies are available. Gating goes in the `metadata.openclaw` frontmatter object — for example, a Gemini-search skill that requires the `gemini` binary on `PATH` and the `GEMINI_API_KEY` env var:

```markdown
---
name: gemini-search
description: Search using Gemini CLI.
metadata: { "openclaw": { "requires": { "bins": ["gemini"] }, "primaryEnv": "GEMINI_API_KEY" } }
---
```

The gating options available under `requires` / `metadata.openclaw`:

| Key | Description |
| --- | --- |
| `requires.bins` | All binaries must exist on `PATH` |
| `requires.anyBins` | At least one binary must exist on `PATH` |
| `requires.env` | Each env var must exist in the process or config |
| `requires.config` | Each `openclaw.json` path must be truthy |
| `os` | Platform filter: `["darwin"]`, `["linux"]`, `["win32"]` |
| `always` | Set `true` to skip all gates and always include the skill |

The full reference is in Skills — Gating. To wire an API key to a skill, add a skill entry in `openclaw.json`; the key is injected into the host process for that agent turn only and does **not** reach the sandbox (see the sandboxed-env-vars reference):

```json5
{
  skills: {
    entries: {
      "gemini-search": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" },
      },
    },
  },
}
```

## Propose via Skill Workshop

For agent-drafted skills, or when you want operator review before a skill goes live, use Skill Workshop proposals instead of writing `SKILL.md` directly. Propose a brand-new skill with `openclaw skills workshop propose-create --name "hello-world" --description "A simple skill that prints a greeting." --proposal ./PROPOSAL.md`, or propose an update to an existing skill with `openclaw skills workshop propose-update hello-world --proposal ./PROPOSAL.md --description "Updated greeting skill"`. Use `--proposal-dir ./hello-world-proposal/` when the proposal includes support files; that directory must contain `PROPOSAL.md`, and support files can go in `assets/`, `examples/`, `references/`, `scripts/`, or `templates/`. After review, inspect and apply the proposal with `openclaw skills workshop inspect <proposal-id>` followed by `openclaw skills workshop apply <proposal-id>`. See the Skill Workshop reference for the full proposal lifecycle.

## Publishing to ClawHub

Publishing a skill to ClawHub is a three-step procedure:

1. **Ensure your `SKILL.md` is complete** — make sure `name`, `description`, and any `metadata.openclaw` gating fields are set, and add a `homepage` URL if you have a project page.
2. **Install the ClawHub skill** with `openclaw skills install clawhub-publish`; the ClawHub skill documents the current publish-command shape and required metadata.
3. **Publish** with `clawhub publish`. See ClawHub — Publishing for the full flow.

## Best practices

The page's authoring tips: **be concise** — instruct the model on *what* to do, not how to be an AI; **safety first** — if your skill uses `exec`, ensure prompts do not allow arbitrary command injection from untrusted input; **test locally** — use `openclaw agent --message "..."` before sharing; and **use ClawHub** — browse community skills at `clawhub.ai` before building from scratch.

**Source**: OpenClaw documentation — `tools/creating-skills` (mirror `inbox/openclaw_docs/tools/creating-skills.md`)
**Last Updated**: 2026-06-22
**Status**: Active
