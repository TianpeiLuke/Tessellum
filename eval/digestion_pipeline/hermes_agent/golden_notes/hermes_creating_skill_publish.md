---
tags:
  - resource
  - documentation
  - hermes_agent
  - skills
  - developer_guide
keywords:
  - skill authoring guidelines
  - progressive disclosure
  - as_document media delivery
  - HERMES_SKILL_DIR template token
  - blueprints suggested cron jobs
  - hermes skills publish tap
  - skill security scanner trust levels
topics:
  - Hermes Agent
  - Developer Guide
  - Skill Authoring
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills
access_control_group: ["general"]
---

# Hermes Agent — Skill Guidelines, Blueprints & Publishing

## Overview

This is the second half of the skill-authoring procedure — the **guidelines + lifecycle** that turn a well-formed [SKILL.md](hermes_creating_skill_format.md) into a quality, shareable, and (optionally) scheduled capability. Where the format note specifies the *declarative spec* (directory layout, frontmatter, conditional activation, env/config/credential declarations), this note covers the
**authoring discipline** (the five guidelines), **where a skill should live** (bundled vs optional vs
hub), **blueprints** (a skill that also carries a schedule and becomes a runnable automation), the unified **Suggested Cron Jobs** surface a blueprint feeds, **publishing** a skill to a hub or a custom tap, and the **trust-level security scanner** every hub-installed skill passes through.

The throughline: a skill is never silently scheduled or silently trusted. Installing a blueprint adds a *suggestion*, not a cron job; accepting it is always an explicit `/suggestions accept`. And a hub-installed skill is scanned for exfiltration / injection / destructive / shell-injection patterns, with `dangerous` verdicts blocked outright. The whole lifecycle reuses the existing skills pipeline — blueprints add no new object type, store, or transport.

## Skill Guidelines

The page lists five authoring guidelines that keep skills cheap to run, portable, and trustworthy:

- **No External Dependencies.** Prefer stdlib Python, `curl`, and existing Hermes tools (`web_extract`, `terminal`, `read_file`). If a dependency is genuinely needed, document its installation steps inside the skill rather than assuming it is present.
- **Progressive Disclosure.** Put the most common workflow first; edge cases and advanced usage go at the bottom. The agent only reads what it needs for the common task, which keeps token usage low.
- **Include Helper Scripts.** For XML/JSON parsing or other complex logic, ship a helper in `scripts/` rather than expecting the LLM to write a parser inline on every run.
- **Deliver media as documents (`[[as_document]]`).** When a skill produces a high-resolution screenshot, chart, or any image where lossy preview compression would hurt, emit the literal directive `[[as_document]]` somewhere in the response (commonly the last line). The gateway strips the directive and delivers every extracted media path in that response as a **downloadable file attachment** instead of an inline image bubble.
- **Test It.** Run the skill and verify the agent actually follows the instructions.

```bash
hermes chat --toolsets skills -q "Use the X skill to do Y"
```

### Referencing bundled scripts from SKILL.md (template tokens)

When a skill is loaded, the activation message exposes the absolute skill directory as `[Skill directory: /abs/path]` and substitutes two template tokens **anywhere** in the SKILL.md body, so a skill can hand the agent a ready-to-run command with no path math and no extra `skill_view` round-trip:

| Token | Replaced with |
|---|---|
| `${HERMES_SKILL_DIR}` | Absolute path to the skill's directory |
| `${HERMES_SESSION_ID}` | The active session id (left in place if there is no session) |

```markdown
To analyse the input, run:

    node ${HERMES_SKILL_DIR}/scripts/analyse.js <input>
```

The agent sees the substituted absolute path and invokes the `terminal` tool directly. Substitution is disabled globally with `skills.template_vars: false` in `config.yaml`.

### Inline shell snippets (opt-in)

Skills can embed inline shell snippets written as `` !`cmd` `` in the SKILL.md body — e.g. `` Current date: !`date -u +%Y-%m-%d` `` or `` Git branch: !`git -C ${HERMES_SKILL_DIR} rev-parse --abbrev-ref HEAD` ``. When enabled, each snippet's stdout is inlined into the message before the agent reads it, so a skill can inject dynamic context (current date, git branch, etc.).

This is **off by default** — any snippet in a SKILL.md runs on the host without approval, so only enable it for skill sources you trust:

```yaml
# config.yaml
skills:
  inline_shell: true
  inline_shell_timeout: 10   # seconds per snippet
```

Snippets run with the skill directory as their working directory, output is capped at 4000 characters, and failures (timeouts, non-zero exits) show up as a short `[inline-shell error: ...]` marker rather than breaking the whole skill.

## Where Should the Skill Live?

Three homes, chosen by how broadly useful the skill is:

- **Bundled (`skills/`).** Ships with every Hermes install. Reserve this for skills that are *broadly useful to most users* — document handling, web research, common dev workflows, system administration — and used regularly by a wide range of people.
- **Optional (`optional-skills/`).** For skills that are official and useful but not universally needed (a paid-service integration, a heavyweight dependency). It ships with the repo, is discoverable via `hermes skills browse` (labeled "official"), and installs with built-in trust.
- **A Skills Hub.** For specialized, community-contributed, or niche skills — upload to a registry and share via `hermes skills install`.

## Blueprints: skills that are also automations

A **blueprint** is an ordinary skill that additionally declares a schedule in its frontmatter. Add a `metadata.hermes.blueprint` block and the skill becomes a shareable, runnable automation:

```yaml
metadata:
  hermes:
    tags: [blueprint, email]
    blueprint:
      schedule: "0 8 * * *"     # presence of `blueprint:` marks it runnable
      deliver: telegram          # optional (default: origin)
      prompt: "Summarize my unread email and today's calendar."  # optional
      no_agent: false            # optional
```

Because a blueprint **is** a skill, it flows through the entire skills pipeline unchanged — search, inspect, install, security scan, provenance, taps, the centralized index, and `hermes skills publish` for sharing. The blueprint layer adds no new object type, store, or transport: the blueprint is a skill, the schedule is a [cron](hermes_creating_skill_format.md) job, and sharing is the existing publish/tap/index path.

**Installing a blueprint is opt-in.** When you install a skill that carries a `blueprint:` block,
Hermes registers it as a **suggested cron job** rather than scheduling it. Installing never silently creates a recurring job — you review and accept it via `/suggestions`:

```bash
hermes skills install owner/morning-brief
# → Blueprint: 'morning-brief' is an automation (schedule 0 8 * * *).
#   Added to your suggestions — run /suggestions to schedule or dismiss it.

# then, in a session:
/suggestions             # lists pending suggestions, numbered
/suggestions accept 1    # creates the cron job
/suggestions dismiss 1   # never offer it again
```

**Sharing an automation you built.** A blueprint loaded by a cron job
(`hermes cron create --skill <name> ...`) can be exported back to a SKILL.md and published like any other skill — so an automation you tuned for yourself becomes a one-command install for someone else.

## Suggested Cron Jobs

Blueprints are one **source** of a unified Suggested Cron Jobs surface: Hermes can *propose* automations and let you accept them with one tap instead of assembling cron jobs by hand. Every proposal — wherever it came from — flows through the single `/suggestions` command:

| Source | Trigger |
|--------|---------|
| `catalog` | Curated starter automations (`/suggestions catalog`) — daily briefing, important-mail monitor, weekly review, workday-start reminder |
| `blueprint` | You installed a skill carrying a `blueprint:` block |
| `usage` | The background review noticed a recurring ask a schedule would serve |
| `integration` | You connected an account (Gmail, GitHub, ...) and the obvious automations are offered |

Accepting a suggestion calls the same `cron.jobs.create_job` the `cronjob` tool uses — there is **no second job engine**. Suggestions never auto-create jobs; acceptance is always explicit. Dismissed suggestions latch by a stable key so the same proposal is never re-offered, and the pending list is capped so it never becomes a nag wall. The **important-mail monitor** catalog entry is the poll→classify→surface pattern: it scores inbox items with a cheap classifier model (`auxiliary.monitor` in `config.yaml`) and delivers only those above an urgency threshold, staying silent otherwise.

## Publishing Skills

Publish to a hub, or expose your own repository as a tap:

```bash
# To the Skills Hub
hermes skills publish skills/my-skill --to github --repo owner/repo

# To a custom repository — add your repo as a tap; users can then search and install from it
hermes skills tap add owner/repo
```

## Security Scanning

All hub-installed skills go through a security scanner that checks for **data exfiltration patterns, prompt injection attempts, destructive commands, and shell injection**. Findings are gated by the skill's trust level:

- `builtin` — ships with Hermes (always trusted).
- `official` — from `optional-skills/` in the repo (built-in trust, no third-party warning).
- `trusted` — from `openai/skills`, `anthropics/skills`, `huggingface/skills`.
- `community` — non-dangerous findings can be overridden with `--force`; **`dangerous` verdicts
  remain blocked**.

Hermes can consume third-party skills from multiple external discovery models: direct GitHub identifiers (e.g. `openai/skills/k8s`), `skills.sh` identifiers (e.g. `skills-sh/vercel-labs/json-render/json-render-react`), and well-known endpoints served from `/.well-known/skills/index.json`. If you want your skills discoverable without a GitHub-specific installer, serve them from a well-known endpoint in addition to publishing them in a repo or marketplace.

**Source**: `inbox/hermes_agent_docs/developer-guide/creating-skills.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills
**Last Updated**: 2026-06-19
**Status**: Active
