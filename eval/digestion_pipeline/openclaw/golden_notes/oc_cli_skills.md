---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - skills
keywords:
  - openclaw skills command
  - openclaw skills install slug git local
  - openclaw skills verify clawhub provenance
  - skill workshop propose apply reject quarantine
  - openclaw skills list eligible check
  - clawhub skill verify v1 envelope
  - global vs agent workspace skills directory
topics:
  - OpenClaw
  - CLI Skills
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/skills
access_control_group: ["general"]
---

# OpenClaw — The `openclaw skills` CLI Command

## Overview

This note documents the procedure for running `openclaw skills`, the CLI surface that inspects local skills, searches ClawHub, installs skills from ClawHub / Git / local directories, verifies ClawHub skills, and updates ClawHub-tracked installs. It mirrors the `cli/skills` source page: the full `## Commands` set (`search` / `install` / `update` / `verify` / `list` / `info` / `check` plus `workshop`), the install-source and slug-resolution rules, the `--global` / `--agent` workspace-targeting model, `verify` provenance behavior, the per-flag Notes, and the `## Skill Workshop` proposal lifecycle. The code-side engine (`repo_openclaw_skills`) is linked, not recreated.

## Commands

`openclaw skills` groups the subcommands below. The page's command reference is:

```bash
openclaw skills search "calendar"
openclaw skills search --limit 20 --json
openclaw skills install <slug>
openclaw skills install <slug> --version <version>
openclaw skills install git:owner/repo
openclaw skills install git:owner/repo@main
openclaw skills install ./path/to/skill --as custom-name
openclaw skills install <slug> --force
openclaw skills install <slug> --agent <id>
openclaw skills install <slug> --global
openclaw skills update <slug>
openclaw skills update <slug> --global
openclaw skills update --all
openclaw skills update --all --agent <id>
openclaw skills update --all --global
openclaw skills verify <slug>
openclaw skills verify <slug> --version <version>
openclaw skills verify <slug> --tag <tag>
openclaw skills verify <slug> --card
openclaw skills verify <slug> --global
openclaw skills list
openclaw skills list --eligible
openclaw skills list --json
openclaw skills list --verbose
openclaw skills list --agent <id>
openclaw skills info <name>
openclaw skills info <name> --json
openclaw skills info <name> --agent <id>
openclaw skills check
openclaw skills check --agent <id>
openclaw skills check --json
```

`search`, `update`, and `verify` use ClawHub directly. `list` is the default action when no subcommand is provided. `list`, `info`, and `check` inspect the local skills visible to the current workspace and config, and write their rendered output to stdout — with `--json`, the machine-readable payload stays on stdout for pipes and scripts. `list --eligible` filters to ready skills; `check` (optionally `--agent <id>`) reports which ready skills are actually visible to that agent's prompt or command surface. `search [query...]` accepts an optional query — omit it to browse the default ClawHub search feed — and `search --limit <n>` caps returned results.

## Install Sources and Slug Resolution

`install <slug>` installs a ClawHub skill; `install git:owner/repo[@ref]` clones a Git skill; and `install ./path` copies a local skill directory. Branch refs may contain slashes, such as `git:owner/repo@feature/foo`. Git and local directory installs expect `SKILL.md` at the source root: `install ./path/to/skill` installs a local directory whose root contains `SKILL.md`. The install slug comes from `SKILL.md` frontmatter `name` when it is valid, then the source directory or repository name; use `--as <slug>` to override the inferred slug for Git and local directory installs. Skill installs do not support npm package specs or zip/archive paths.

Per-source flag scope is explicit: `install --version <version>` applies only to ClawHub skill slugs (`--version` is ClawHub-only), and `install --force` overwrites an existing workspace skill folder for the same slug. `openclaw skills update` updates ClawHub-tracked installs only — `update <slug>` updates a single tracked skill, while `update --all` updates tracked ClawHub installs in the selected workspace (or, with `--global`, in the shared managed skills directory). Gateway-backed skill dependency installs triggered from onboarding or Skills settings use the separate `skills.install` request path instead of this CLI path.

## Workspace Targeting (`--global` / `--agent`)

By default, `install`, `update`, and `verify` target the active workspace `skills/` directory; with `--global`, they target the shared managed skills directory. Workspace-backed commands resolve the target workspace in this order: from `--agent <id>`, then the current working directory when it is inside a configured agent workspace, then the default agent. `--agent <id>` targets one configured agent workspace and overrides current working directory inference, while `--global` targets the shared managed skills directory and **cannot be combined with `--agent <id>`**. For `update --all`, add `--agent <id>` to scope to one agent workspace or `--global` to scope to the shared managed skills directory.

## Verify and Provenance

`verify <slug>` prints ClawHub's `clawhub.skill.verify.v1` JSON envelope by default; there is no `--json` flag because JSON is already the default. When ClawHub returns server-resolved source provenance, the verify JSON also includes a commit-pinned `openclaw.verifiedSourceUrl` — unavailable or self-declared source URLs stay only in the raw provenance envelope and are not promoted. `verify` uses `.clawhub/origin.json` for installed ClawHub skills, so it verifies the installed version against the registry it came from; `--version` and `--tag` override the version selector but keep that installed registry when origin metadata exists. `verify --card` prints the generated Skill Card Markdown instead of JSON; the command exits non-zero when ClawHub returns `ok: false` or `decision: "fail"`, and unsigned signatures are informational unless ClawHub policy changes. Installed ClawHub bundles can include a generated `skill-card.md`; OpenClaw treats verification as a ClawHub server decision and does not reject an installed skill just because that generated card changes the bundle fingerprint.

## Skill Workshop

`openclaw skills workshop` manages pending skill proposals in the selected workspace. Proposals are **not active skills until applied**. For proposal storage, support-file safeguards, Gateway methods, and approval policy, the page defers to the [Skill Workshop](https://docs.openclaw.ai/tools/skill-workshop) doc. The proposal lifecycle commands are:

```bash
openclaw skills workshop propose-create \
  --name "qa-check" \
  --description "Repeatable QA checklist" \
  --proposal ./PROPOSAL.md
openclaw skills workshop propose-create \
  --name "qa-check" \
  --description "Repeatable QA checklist" \
  --proposal-dir ./qa-check-proposal
openclaw skills workshop propose-update qa-check --proposal ./PROPOSAL.md
openclaw skills workshop list
openclaw skills workshop inspect <proposal-id>
openclaw skills workshop revise <proposal-id> --proposal ./PROPOSAL.md
openclaw skills workshop apply <proposal-id>
openclaw skills workshop reject <proposal-id> --reason "Duplicate"
openclaw skills workshop quarantine <proposal-id> --reason "Needs security review"
```

`propose-create` registers a new proposal from a `--proposal ./PROPOSAL.md` file or a `--proposal-dir` directory (with `--name` and `--description`); `propose-update <name>` revises an existing skill via a proposal file. `list` enumerates pending proposals, `inspect <proposal-id>` shows one, and `revise <proposal-id>` replaces its proposal content. The terminal transitions are `apply <proposal-id>` (promote to an active skill), `reject <proposal-id> --reason "..."`, and `quarantine <proposal-id> --reason "..."` (hold for security review).

**Source**: OpenClaw documentation — `cli/skills` (mirror `inbox/openclaw_docs/cli/skills.md`)
**Last Updated**: 2026-06-22
**Status**: Active
