---
tags:
  - resource
  - terminology
  - agentic_ai
  - developer_tools
  - autonomous_agents
keywords:
  - skills hub
  - hermes skills hub
  - skill registry
  - skill install
  - skill tap
  - agentskills.io
keywords_secondary:
  - skills.sh
  - browse.sh
  - skill marketplace
topics:
  - Agentic AI
  - Skill Distribution
  - Developer Tools
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
---

# Skills Hub

## Definition

The **Skills Hub** is the Hermes Agent's multi-source install registry for discovering, inspecting, installing, updating, and auditing agent **skills** (on-demand knowledge documents in the [agentskills.io](https://agentskills.io/specification) format). Rather than a single centralized store, it is a federation that spans nine source types — official optional skills, the Vercel-operated `skills.sh` directory, `well-known` website endpoints, direct GitHub repos and taps, ClawHub, the Claude marketplace, LobeHub, Browserbase's `browse.sh` catalog, and bare single-file `SKILL.md` URLs — all reached through one `hermes skills` command surface and the `/skills` slash command.

The Hub solves the *distribution* problem for agent skills: where to find reusable procedural-knowledge packages and how to bring them onto disk safely. Every install routes through a security scanner and a trust-level policy before the skill lands in `~/.hermes/skills/`, where it becomes a first-class slash command. The Hub is the human-driven complement to the agent's own `skill_manage` procedural-memory writes — one supplies skills from the outside world, the other authors them from the agent's own experience.

## Context

The Skills Hub lives in the Hermes Agent skills subsystem (`tools/skills_hub.py`). It is documented on the Hermes "Skills System" page alongside progressive disclosure, the SKILL.md format, and the skill curator. Hub-installed skills share the single `~/.hermes/skills/` source-of-truth directory with bundled and agent-created skills, and the Hub maintains its own state under `~/.hermes/.hub/` (`lock.json`, `quarantine/`, `audit.log`, `taps.json`).

## Key Characteristics

- **Nine federated sources** — `official`, `skills-sh` (Vercel's directory), `well-known` (sites serving `/.well-known/skills/index.json`), `github` (repos + custom taps, default taps include `openai/skills`, `anthropics/skills`, `huggingface/skills`, `NVIDIA/skills`), `clawhub`, `claude-marketplace`, `lobehub`, `browse-sh` (Browserbase's site-automation catalog), and `url` (single-file `SKILL.md`).
- **One command surface** — `hermes skills browse | search | inspect | install | list | check | update | audit | uninstall | reset | publish | tap | snapshot`, mirrored as the `/skills` slash command on the CLI and every messaging platform.
- **Security scanning before install** — every hub skill is scanned for data exfiltration, prompt injection, destructive commands, and supply-chain signals; `inspect` surfaces upstream metadata (repo URL, weekly installs, audit status).
- **Trust-level policy** — four levels (`builtin`, `official`, `trusted`, `community`) gate how permissive the install policy is; `--force` can override non-dangerous findings for `community` sources but **cannot** override a `dangerous` verdict.
- **Provenance-based update lifecycle** — the Hub stores each skill's source identifier plus an upstream content hash, so `hermes skills check`/`update` detect drift and reinstall only changed skills.
- **Custom taps** — any GitHub repo of `SKILL.md` directories becomes a shareable source via `hermes skills tap add <owner/repo>`; new taps default to `community` trust and `path: skills/`, configurable in `taps.json`.
- **Standards-compatible** — installs conform to the agentskills.io open standard (`SKILL.md` + optional `references/`, `scripts/`, `assets/`), so skills authored for Claude Code, Cursor, Codex, and other agents can be consumed.
- **Per-profile scoping** — each Hermes profile has its own `HERMES_HOME`, so installs and the `.bundled_manifest`/`reset` lifecycle are isolated per profile.

## Related Terms


## References

- [Hermes Agent — Skills System (Skills Hub)](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [agentskills.io — Specification](https://agentskills.io/specification)
- [skills.sh — The Agent Skills Directory (Vercel)](https://skills.sh/)
- [vercel-labs/skills (GitHub)](https://github.com/vercel-labs/skills)
- [browse.sh — Browserbase site-automation skills catalog](https://browse.sh/)

---

**Last Updated**: 2026-06-19
**Status**: Active
