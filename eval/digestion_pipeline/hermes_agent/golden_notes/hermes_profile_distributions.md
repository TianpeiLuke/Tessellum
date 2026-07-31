---
tags:
  - resource
  - documentation
  - hermes_agent
  - profiles
  - distribution
keywords:
  - profile distribution
  - distribution.yaml manifest
  - hermes profile install
  - hermes profile update
  - .env.EXAMPLE
  - git-repo agent packaging
  - profile info
  - env_requires
topics:
  - Hermes Agent
  - Profile Distributions
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
access_control_group: ["general"]
---

# Hermes Profile Distributions

## Overview

A **profile distribution** is a whole Hermes agent — personality (`SOUL.md`), skills, cron jobs, MCP connections, and config — packaged as a **git repository** so anyone with repo access can install the complete agent with one command, update it in place, and keep their own memories, sessions, and API keys untouched. If a [profile](hermes_profiles_multi_agent.md) is a local agent, a distribution is that agent made shareable. This note covers the procedural **author → install → update** lifecycle: writing the `distribution.yaml` manifest, pushing to git and tagging versions, the `hermes profile install`/`update`/`info`/`delete` installer flow, the five use-case patterns, and the operator recipes. The data partition (distribution-owned vs user-owned), the hard-excluded never-shipped paths, the unsigned trust boundary, and the under-the-hood internals are the [distribution data & trust model](hermes_profile_distribution_model.md) (Note 4) — referenced, not duplicated here.

## What this means

Before distributions, sharing a Hermes agent meant sending someone the `SOUL.md`, a list of skills to install, a secrets-stripped `config.yaml`, a description of wired-up MCP servers, any cron jobs, and env-var instructions — then hoping they assembled it correctly, and repeating the whole handoff on every version bump. With distributions, all of that lives in one git repo:

```
my-research-agent/
├── distribution.yaml    # manifest: name, version, env-var requirements
├── SOUL.md              # the agent's personality / system prompt
├── config.yaml          # model, temperature, reasoning, tool defaults
├── skills/              # bundled skills that come with the agent
├── cron/                # scheduled tasks the agent runs
└── mcp.json             # MCP servers the agent connects to
```

Recipients run `hermes profile install github.com/you/my-research-agent --alias` (one command) and they have the whole agent. They fill in their own API keys (`.env.EXAMPLE` → `.env`), then run `my-research-agent chat` or address it through any messaging gateway. When the author pushes a new version, installers run `hermes profile update my-research-agent` — their memories and sessions stay put.

## Why git?

The docs considered tarballs, HTTP archives, and a custom format; git won on every axis:

- **Zero build step for authors.** Push to GitHub; consumers install — no "pack, upload, update the index" loop.
- **Tags, branches, and commits are already the versioning system.** A tag push does what "pack + upload a release" does elsewhere.
- **Updates are a fetch**, not a re-download of the whole archive.
- **Transparent.** Users browse the repo, read diffs between versions, open issues, fork to customize.
- **Private repos work for free.** SSH keys, `git credential` helpers, GitHub CLI stored credentials — whatever auth the terminal already has applies transparently.
- **Reproducibility is a commit SHA** — the same thing pip and npm record.

The tradeoff: recipients need git installed, which on any 2026 Hermes machine is already true.

## When should you use a distribution?

**Good fits:** sharing a specialized agent (compliance monitor, code reviewer, research assistant, support bot) with a team or community; deploying the same agent to multiple machines without copying files manually; iterating on an agent so recipients pick up new versions with one command; building an agent as a product with opinionated defaults, curated skills, and tuned prompts.

**Not a fit:** backing up a profile on your own machine (use [`hermes profile export` / `import`](hermes_profiles_multi_agent.md) instead — link-out to SP20 `profile-commands` for the full reference); sharing API keys (`auth.json`/`.env` are deliberately excluded — each installer brings their own credentials); sharing memories/sessions/conversation history (user data, never shipped — see the [distribution model](hermes_profile_distribution_model.md)).

## For authors: publishing a distribution

The author flow is four steps. **Step 1 — Start from a working profile**: build and refine the agent like any other profile, then dogfood it.

```bash
hermes profile create research-bot
research-bot setup                    # configure model, API keys
# Edit ~/.hermes/profiles/research-bot/SOUL.md
# Install skills, wire up MCP servers, schedule cron jobs, etc.
research-bot chat                     # dogfood until it feels right
```

**Step 2 — Add a `distribution.yaml`** at the profile root. `env_requires` tells installers which env vars the agent needs; these are checked against the installer's shell and existing `.env` so they aren't nagged about keys they already have. Every field except `name` has a sensible default:

```yaml
name: research-bot
version: 1.0.0
description: "Autonomous research assistant with arXiv and web tools"
hermes_requires: ">=0.12.0"
author: "Your Name"
license: "MIT"

# Tell installers which env vars the agent needs. These are checked against
# the installer's shell and existing .env file so they don't get nagged
# about keys they already have configured.
env_requires:
  - name: OPENAI_API_KEY
    description: "OpenAI API key (for model access)"
    required: true
  - name: SERPAPI_KEY
    description: "SerpAPI key for web search"
    required: false
    default: ""
```

**Step 3 — Push to a git repo**, then **Step 4 — Tag versioned releases** each time the agent reaches a stable point:

```bash
cd ~/.hermes/profiles/research-bot
git init
git add .
git commit -m "v1.0.0"
git remote add origin git@github.com:you/research-bot.git
git tag v1.0.0
git push -u origin main --tags
```

The repo is now a distribution. On later releases, bump `version:` in `distribution.yaml`, `git add` the changed files, `git commit`, `git tag v1.1.0`, and `git push --tags`; recipients who run `hermes profile update research-bot` pull the latest. The repo contains everything in the profile directory **except the paths excluded from distributions** (`auth.json`, `.env`, `memories/`, `sessions/`, `state.db*`, `logs/`, `workspace/`, `*_cache/`, `local/`) — those stay on the author's machine; a `.gitignore` can exclude additional paths. The full exclude invariant and the distribution-owned-vs-user-owned partition are documented in the [distribution model](hermes_profile_distribution_model.md). A complete authored repo also typically carries `mcp.json`, multiple `skills/<name>/SKILL.md`, `cron/*.json` scheduled tasks, and an optional human-facing `README.md`.

## For installers: using a distribution

**Install** with `hermes profile install github.com/you/research-bot --alias` clones, previews, checks env, and copies. What happens: (1) clones the repo into a temporary directory; (2) reads `distribution.yaml` and shows the manifest (name, version, description, author, required env vars); (3) checks each required env var against your shell environment and the target profile's existing `.env`, marking each `✓ set` or `needs setting`; (4) asks for confirmation (`-y` / `--yes` skips); (5) copies distribution-owned files into `~/.hermes/profiles/research-bot/` (or wherever the manifest's `name` resolves); (6) writes `.env.EXAMPLE` with required keys commented out; (7) with `--alias`, creates a wrapper so you can run `research-bot chat` directly.

**Source types** — any git URL works (GitHub shorthand, full HTTPS, SSH, self-hosted GitLab/Gitea/Forgejo, private repos via your configured git auth, or a local directory during development). **Override the profile name** with `--name` so two users can install the same distribution under different local names:

```bash
hermes profile install github.com/acme/support-bot --name support-us --alias
hermes profile install github.com/acme/support-bot --name support-eu --alias
```

**Fill in env vars**: copy the generated `.env.EXAMPLE` to `.env` and paste real keys; required keys already exported in your shell (e.g. `OPENAI_API_KEY` in `~/.zshrc`) are marked `✓ set` at install and need not be duplicated. **Check what you installed** with `hermes profile info research-bot` (prints version, description, author, requires, source URL, install timestamp, and env vars); `hermes profile list` adds a `Distribution` column (e.g. `research-bot@1.0.0`) so hand-built vs repo-sourced profiles are distinguishable at a glance.

**Update** re-clones from the recorded source URL, replaces distribution-owned files (SOUL, skills, cron, `mcp.json`), **preserves** your tuned `config.yaml` (pass `--force-config` to overwrite), and **never touches** user data (memories, sessions, auth, `.env`, logs, state):

```bash
hermes profile update research-bot
```

**Remove** with `hermes profile delete research-bot`; the delete prompt surfaces distribution provenance (name@version, installed-from URL) before requiring you to type the profile name to confirm, so you never delete an agent without knowing where to re-install it. The exact preserve/replace partition is in the [distribution model](hermes_profile_distribution_model.md).

## Use cases and patterns

Five patterns, each the same git workflow applied to a different audience:

- **Personal — sync one agent across machines.** Push the profile from your laptop, `hermes profile install` on your workstation, then `git commit && push` + `hermes profile update` to propagate iterations. Memories stay per-machine (laptop and workstation don't collide).
- **Team — ship a reviewed internal agent.** The lead builds, tags, and pushes a PR-reviewer to the company's internal git host; each engineer installs with `--alias` and fills in their own (separately billed) API key via `.env.EXAMPLE`. A `v1.1` ship → everyone runs `hermes profile update` and is current within minutes.
- **Community — publish a public agent.** Write a solid `README.md` (GitHub shows it on the repo page), tag, push to a public repo, and tweet the install command; users send issues and PRs, and customizers fork via the standard git workflow.
- **Product — ship an opinionated agent.** Distribute a Hermes-on-top product (e.g. a compliance-telemetry harness) with a `distribution.yaml` declaring license and `env_requires` (license key + provider key + optional MCP URL); customers install with one command, the preview tells them which keys to have ready, updates roll out on each tagged release, and their compliance data never leaves their machine.
- **Ephemeral — one-off scripts on shared infra.** Build a temporary incident-diagnosis agent, push a private repo, have on-call engineers install it, and `hermes profile delete` when the incident resolves. The install-delete cycle is cheap enough to be disposable.

## Recipes

- **Pin to a specific version** — git ref pinning (`#v1.2.0`) is *planned but not in the initial release*; install currently tracks the default branch, so track your installed version via `hermes profile info <name>` and hold off on updates until ready.
- **Check what version you're on vs. latest** — compare `hermes profile info research-bot | grep Version` against `git ls-remote --tags <repo-url> | tail -5`.
- **Keep local config customizations through updates** — the default already preserves `config.yaml`; to be safe, write tweaks to a file in the distribution-untouched `local/` namespace (`~/.hermes/profiles/research-bot/local/my-overrides.yaml`) and reference it from `config.yaml` or SOUL.
- **Force a clean re-install / reset config** — `hermes profile delete <name> --yes` then `hermes profile install …` for a from-scratch reinstall (loses memories/sessions too), or `hermes profile update <name> --force-config --yes` to update and reset `config.yaml` to the distribution default.
- **Fork and customize** — fork the repo on GitHub, install your fork, iterate locally, commit/push to the fork; pull upstream the usual git way.
- **Test a distribution before pushing** — install from a local directory with `--name research-bot-test` (no git push needed), then delete and re-install until it's right.

For local backup/restore (distinct from distribution), use `hermes profile export` / `import` — full flag reference lives in the SP20 `profile-commands` doc.

**Source**: `inbox/hermes_agent_docs/user-guide/profile-distributions.md` · https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
**Last Updated**: 2026-06-19
**Status**: Active
