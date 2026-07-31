---
tags:
  - resource
  - terminology
  - openclaw
  - skills
  - skill-manifest
  - markdown-frontmatter
  - plugin-system
  - agent-framework
keywords:
  - Skill Manifest
  - SKILL.md
  - skill manifest format
  - metadata.openclaw.requires
  - metadata.openclaw.install
  - YAML frontmatter
  - bundled skill
  - ClawHub registry
  - Anthropic Skills
  - AIM Skills
  - Cursor rules
  - .mdc
topics:
  - OpenClaw skills authoring
  - Agent skill manifests
  - Markdown frontmatter contracts
  - Plugin systems
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://github.com/openclaw/openclaw/tree/main/skills
access_control_group: ["general"]
---

# Skill Manifest

## Definition

A **Skill Manifest** is the on-disk authoring contract for a bundled agent skill — a single Markdown file (`SKILL.md`) that pairs a free-form Markdown body with an optional YAML frontmatter header, where the body becomes the prompt-side documentation the agent reads when the skill is selected and the frontmatter declares the skill's runtime identity and prerequisites. The format follows the broader convention of [Markdown with YAML frontmatter](https://en.wikipedia.org/wiki/Markdown) (popularized by Jekyll, Hugo, and Obsidian for content metadata), adapted to a tooling concern — the YAML block is parsed first to register the skill with the host, then the body is surfaced as prompt material when the agent invokes the skill.

In **OpenClaw**, the Skill Manifest is the format every directory under `skills/<name>/SKILL.md` must follow. The loader recognizes three top-level frontmatter keys — `name` (string; slug surfaced to the agent, must equal the directory name), `description` (string; one-line imperative summary used in tool listings), and `metadata` (object; namespaced runtime hints scoped under `metadata.openclaw.{requires,install}` so unrelated tooling can inject their own metadata without collision). Two manifest shapes are sanctioned — a *full* manifest with frontmatter declaring binary prerequisites and install recipes (e.g., `clawhub/SKILL.md` requires the `clawhub` CLI on PATH and lists an npm install recipe), and a *frontmatter-less* manifest that starts directly at the H1 for pure-documentation skills (e.g., `canvas/SKILL.md`, which teaches prose-only conventions and needs no external binary). The format positions OpenClaw alongside [Anthropic's Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills), [AIM Skills](https://agentskills.io/), and [Cursor rules (`.mdc` files)](https://docs.cursor.com/context/rules) — all four are Markdown-body-plus-frontmatter contracts for agent extension, differing only in which frontmatter keys are recognized and where prompts are surfaced.

## Context

The "Markdown body plus YAML frontmatter" pattern is now the dominant authoring surface for agent skills across the agent-framework ecosystem. Anthropic's [Claude Code Skills](https://docs.claude.com/en/docs/claude-code/skills) ship as `SKILL.md` files with frontmatter declaring `name` and `description`; the [open Agent Skills standard](https://agentskills.io/) adopted by Amazon's AIM publishes the same contract; [Cursor's rules system](https://docs.cursor.com/context/rules) stores `.mdc` files with frontmatter for `description`, `globs`, and `alwaysApply` plus a Markdown body. The OpenClaw Skill Manifest is OpenClaw's instance of this pattern — its differentiator is the `metadata.openclaw` namespace, which carries OpenClaw-specific runtime hints (binary prerequisites + install recipes) under a vendor-scoped key so the same file can in principle carry other vendors' frontmatter without conflict.

Skills authored against the OpenClaw manifest format are distributed via the [ClawHub registry](https://github.com/openclaw/clawhub) — a search-install-update-sync-publish CLI registry whose own `clawhub/SKILL.md` is the canonical example of a *full* manifest declaring `requires.bins: [clawhub]` plus an npm install recipe. The Canvas skill (`canvas/SKILL.md`) is the canonical example of a *frontmatter-less* manifest — it teaches the agent how to use the runtime-implemented canvas tool and needs no external binary, so the file starts at the H1 and the loader defaults `name` to the directory name and `description` to the first paragraph. Authors writing new manifests choose between the two shapes based on whether the skill wraps an external binary (full frontmatter) or teaches prose conventions over a built-in tool (frontmatter-less). Within OpenClaw's broader extension surface, the Skill Manifest is the *prompt-side* contract, complementary to the `Plugin Manifest` (`package.json` + `openclaw.plugin.json`) which is the *code-side* loading contract for compiled plugins.

## Key Characteristics

- **`SKILL.md` filename convention** — every bundled skill is a directory `skills/<name>/` whose entry file MUST be named `SKILL.md` (uppercase). The directory name is the slug — `skills/clawhub/SKILL.md` registers as `clawhub`. Frontmatter `name`, if present, MUST equal the directory name; a mismatch means the loader registers a slug that does not resolve from the on-disk path.
- **Optional YAML frontmatter block** — delimited by `---` lines opening and closing the block; opening `---` MUST be the file's first line and closing `---` MUST be alone on a line. Inside, three top-level keys are recognized — `name` (string slug), `description` (one-line imperative summary surfaced verbatim in tool listings), and `metadata` (object). Frontmatter is opt-in — pure-documentation skills omit the block entirely; do NOT write empty `---\n---\n`, which the loader treats as a parse error rather than defaults.
- **`metadata.openclaw.requires` prerequisite declaration** — sub-object under the vendor-namespaced `metadata.openclaw` key with `bins:` listing executable NAMES (not absolute paths — names resolved via PATH) that must be present for the skill to be exposed. Runtime probes PATH at session start; missing binaries cause the skill to be hidden rather than fail at use time.
- **`metadata.openclaw.install` recipe list** — list (NEVER a bare object, even with one recipe) of install-recipe objects, each with `id` (stable identifier within the manifest), `kind` (well-known installer type — `node`, `brew`, `pip`), a kind-specific payload (`package`), `bins` (names the recipe will put on PATH, MUST be a superset of `requires.bins`), and `label` (human-readable string surfaced in install prompts). Multiple recipes coexist in one list so a skill can offer parallel install paths (npm + brew + manual).
- **Inline-flow vs block-style YAML** — `metadata` may use either inline-flow JSON-like braces (as in `clawhub/SKILL.md`, where the entire metadata payload sits visually compact) or block-style YAML with two-space indents. Both forms are equally valid; choice is stylistic.
- **Markdown body conventions** — body is free-form Markdown surfaced as prompt content when the agent invokes the skill. Convention is an H1 title (human-readable, distinct from the slug), one-paragraph description immediately under the H1, then H2 sections (`## Overview`, `## How It Works`, `## Configuration`, `## Workflow`, `## Debugging`, `## Tips`). Workflow sections use numbered H3 subsections (`### 1. ...`, `### 2. ...`) to preserve explicit ordering. All commands and examples go in fenced code blocks with explicit language tags (` ```bash `, ` ```json `, ` ```markdown `) so the agent's prompt formatter can highlight and extract them.
- **Frontmatter-less manifest shape** — for pure-documentation skills (no external binary, no metadata to declare), omit the frontmatter block entirely; the file's first non-blank line is the H1. The loader applies defaults: `name = <dirname>`, `description = <first paragraph>`, `metadata = {}`. This is the documented opt-out — the `canvas/` skill uses this shape.
- **ClawHub registry distribution** — once authored, manifests are published to the ClawHub registry via the `clawhub` CLI (`search`, `install`, `update`, `sync`, `publish`). The registry validates the manifest before publish — `name`/`description` required for non-frontmatter-less skills, `requires.bins` superset checked against each install recipe's `bins`.
- **Version + compatibility declarations** — version metadata is NOT carried inside `SKILL.md` itself; it lives in the sibling `package.json` (when the skill is part of an OpenClaw plugin) or is implicit in the ClawHub registry record. Skill Manifests are *content* contracts; compatibility is handled by the companion [Plugin Manifest](term_plugin_manifest.md) (`openclaw.compat.pluginApi` semver gate + `openclaw.build.openclawVersion` declaration in `package.json`).

## Related Terms

- **[OpenClaw — ClawHub On-Disk Skill Folder Format](../documentation/openclaw/oc_clawhub_skill_format.md)** — This note is the procedure for the **on-disk ClawHub skill folder format** — the layout, required and optional files, GitHub import rules, allowed file types…

## Related Code Snippets

- [OpenClaw Skills — SKILL.md Bundled Skill Manifest Format](../code_snippets/snippet_openclaw_skills_manifest_format.md): 4-pattern catalog covering frontmatter shape, `metadata.openclaw` declarations, frontmatter-less manifest, and body conventions (lifts from `skills/clawhub/SKILL.md` and `skills/canvas/SKILL.md`)

## References

- [Anthropic Claude Code — Skills documentation](https://docs.claude.com/en/docs/claude-code/skills) — Anthropic's `SKILL.md` + YAML frontmatter contract for Claude Code skills; direct industry analogue (Class 2: framework docs)
- [Agent Skills open standard (agentskills.io)](https://agentskills.io/) — the open standard Anthropic published and AIM Skills adopted; same Markdown-plus-frontmatter family OpenClaw's Skill Manifest belongs to (Class 2: open standard)
- [Cursor — Rules (`.mdc` files)](https://docs.cursor.com/context/rules) — Cursor's analogous authoring format with frontmatter (`description`, `globs`, `alwaysApply`) + Markdown body for editor-side agent rules (Class 2: framework docs)
- [Markdown — Wikipedia](https://en.wikipedia.org/wiki/Markdown) — foundational definition of Markdown and its frontmatter-extension conventions used by static-site generators and now agent skills (Class 1: Wikipedia foundational)
- [YAML 1.2 specification](https://yaml.org/spec/1.2.2/) — the data-language spec the frontmatter block parses against; defines block-style vs inline-flow forms (Class 1: authoritative spec)
