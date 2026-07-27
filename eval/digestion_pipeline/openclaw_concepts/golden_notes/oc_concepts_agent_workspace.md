---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - agent_workspace
keywords:
  - openclaw agent workspace
  - workspace default location
  - workspace file map AGENTS SOUL USER
  - git backup private repo
  - do not commit secrets gitignore
  - moving workspace new machine
  - agents.defaults.workspace
  - sandbox workspace root
topics:
  - OpenClaw
  - Agent Workspace
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/agent-workspace
access_control_group: ["general"]
---

# OpenClaw — Setting Up and Backing Up the Agent Workspace

## Overview

This procedure note documents the OpenClaw **agent workspace** — the agent's home directory and the only working directory used for file tools and workspace context — following the `concepts/agent-workspace` source page. It covers the default location and how to override it (`agents.defaults.workspace`), the standard workspace file map (AGENTS / SOUL / USER / IDENTITY / TOOLS / HEARTBEAT / BOOT / BOOTSTRAP / memory / MEMORY / skills / canvas), what deliberately lives under `~/.openclaw/` instead of the workspace, the recommended private-git backup workflow, secret hygiene, and migrating a workspace to a new machine. The workspace is the default cwd, not a hard sandbox — keep it private and treat it as memory; it is separate from `~/.openclaw/`, which stores config, credentials, and sessions.

> **Warning (from source):** The workspace is the **default cwd**, not a hard sandbox. Tools resolve relative paths against the workspace, but absolute paths can still reach elsewhere on the host unless sandboxing is enabled. If you need isolation, use `agents.defaults.sandbox` (and/or per-agent sandbox config). When sandboxing is enabled and `workspaceAccess` is not `"rw"`, tools operate inside a sandbox workspace under `~/.openclaw/sandboxes`, not your host workspace.

## Default location

The workspace default is `~/.openclaw/workspace`. If `OPENCLAW_PROFILE` is set and not `"default"`, the default becomes `~/.openclaw/workspace-<profile>`. Override the location in `~/.openclaw/openclaw.json`:

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
    },
  },
}
```

Running `openclaw onboard`, `openclaw configure`, or `openclaw setup` will create the workspace and seed the bootstrap files if they are missing. Sandbox seed copies only accept regular in-workspace files; symlink/hardlink aliases that resolve outside the source workspace are ignored. If you already manage the workspace files yourself, disable bootstrap file creation with `skipBootstrap`:

```json5
{ agents: { defaults: { skipBootstrap: true } } }
```

## Extra workspace folders

Older installs may have created `~/openclaw`. Keeping multiple workspace directories around can cause confusing auth or state drift, because only one workspace is active at a time. The source recommendation is to keep a single active workspace: if you no longer use the extra folders, archive or move them to Trash (for example `trash ~/openclaw`); if you intentionally keep multiple workspaces, make sure `agents.defaults.workspace` points to the active one. `openclaw doctor` warns when it detects extra workspace directories.

## Workspace file map

These are the standard files OpenClaw expects inside the workspace (verbatim from the source AccordionGroup):

| File / folder | Role | Loading / lifecycle |
|---|---|---|
| `AGENTS.md` | Operating instructions for the agent and how it should use memory — rules, priorities, and "how to behave" details. | Loaded at the start of every session. |
| `SOUL.md` | Persona, tone, and boundaries. | Loaded every session. Guide: SOUL.md personality guide. |
| `USER.md` | Who the user is and how to address them. | Loaded every session. |
| `IDENTITY.md` | The agent's name, vibe, and emoji. | Created/updated during the bootstrap ritual. |
| `TOOLS.md` | Notes about local tools and conventions. Does NOT control tool availability; it is only guidance. | Guidance only. |
| `HEARTBEAT.md` | Optional tiny checklist for heartbeat runs. Keep it short to avoid token burn. | Optional. |
| `BOOT.md` | Optional startup checklist run automatically on gateway restart (when internal hooks are enabled). Keep it short; use the message tool for outbound sends. | Optional, on gateway restart. |
| `BOOTSTRAP.md` | One-time first-run ritual. Only created for a brand-new workspace. Delete it after the ritual is complete. | One-time, first run. |
| `memory/YYYY-MM-DD.md` | Daily memory log (one file per day). Recommended to read today + yesterday on session start. | Per-day. |
| `MEMORY.md` | Curated long-term memory: durable facts, preferences, decisions, and short summaries. Keep detailed logs in `memory/YYYY-MM-DD.md` so memory tools can retrieve them on demand without injecting them into every prompt. | Only load in the main, private session (not shared/group contexts). |
| `skills/` | Workspace-specific skills. Highest-precedence skill location for that workspace. Overrides project agent skills, personal agent skills, managed skills, bundled skills, and `skills.load.extraDirs` when names collide. | Optional. |
| `canvas/` | Canvas UI files for node displays (for example `canvas/index.html`). | Optional. |

If any bootstrap file is missing, OpenClaw injects a "missing file" marker into the session and continues. Large bootstrap files are truncated when injected; adjust limits with `agents.defaults.bootstrapMaxChars` (default: `20000`) and `agents.defaults.bootstrapTotalMaxChars` (default: `60000`). `openclaw setup` can recreate missing defaults without overwriting existing files.

## What is NOT in the workspace

These live under `~/.openclaw/` and should NOT be committed to the workspace repo:

- `~/.openclaw/openclaw.json` (config)
- `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` (model auth profiles: OAuth + API keys)
- `~/.openclaw/agents/<agentId>/agent/codex-home/` (per-agent Codex runtime account, config, skills, plugins, and native thread state)
- `~/.openclaw/credentials/` (channel/provider state plus legacy OAuth import data)
- `~/.openclaw/agents/<agentId>/sessions/` (session transcripts + metadata)
- `~/.openclaw/skills/` (managed skills)

If you need to migrate sessions or config, copy them separately and keep them out of version control.

## Git backup (recommended, private)

Treat the workspace as private memory: put it in a **private** git repo so it is backed up and recoverable. Run these steps on the machine where the Gateway runs (that is where the workspace lives).

**Step 1 — Initialize the repo.** If git is installed, brand-new workspaces are initialized automatically. If this workspace is not already a repo, run:

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"
```

**Step 2 — Add a private remote.** Create a new **private** repository (GitHub or GitLab), do NOT initialize it with a README (avoids merge conflicts), then add the remote and push. Via the web UI, copy the HTTPS remote URL and run the three `git` commands below; alternatively, with the GitHub CLI (`gh`), create and push the private repo in one step (the `gh` lines):

```bash
# Web UI path (copy the private repo's HTTPS remote URL first):
git branch -M main
git remote add origin <https-url>
git push -u origin main
# GitHub CLI path (alternative — creates + pushes the private repo in one step):
gh auth login
gh repo create openclaw-workspace --private --source . --remote origin --push
```

**Step 3 — Ongoing updates.** Stage, commit, and push memory changes as the workspace evolves:

```bash
git status
git add .
git commit -m "Update memory"
git push
```

## Do not commit secrets

Even in a private repo, avoid storing secrets in the workspace: API keys, OAuth tokens, passwords, or private credentials; anything under `~/.openclaw/`; and raw dumps of chats or sensitive attachments. If you must store sensitive references, use placeholders and keep the real secret elsewhere (password manager, environment variables, or `~/.openclaw/`). The source suggests this `.gitignore` starter:

```gitignore
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

## Moving the workspace to a new machine

Follow these four steps to migrate a backed-up workspace to a new host:

1. **Clone the repo** to the desired path (default `~/.openclaw/workspace`).
2. **Update config** — set `agents.defaults.workspace` to that path in `~/.openclaw/openclaw.json`.
3. **Seed missing files** — run `openclaw setup --workspace <path>` to seed any missing files.
4. **Copy sessions (optional)** — if you need sessions, copy `~/.openclaw/agents/<agentId>/sessions/` from the old machine separately.

## Advanced notes

Multi-agent routing can use different workspaces per agent (see Channel routing for routing configuration). If `agents.defaults.sandbox` is enabled, non-main sessions can use per-session sandbox workspaces under `agents.defaults.sandbox.workspaceRoot`.

## Related Notes

**Terms**

- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway product; relevance: `~/.openclaw/workspace` is the OpenClaw agent home.
- **[Persona](../../term_dictionary/term_persona.md)** — agent personality; relevance: SOUL.md persona file in the workspace map.
- **[Steering Files](../../term_dictionary/term_steering_files.md)** — AGENTS/TOOLS/USER files; relevance: the workspace bootstrap-file map.
- **[Skills](../../term_dictionary/term_skills.md)** — loadable capabilities; relevance: `<workspace>/skills` highest-precedence skill location.
- **[Session Persistence](../../term_dictionary/term_session_persistence.md)** — durable sessions; relevance: sessions kept under `~/.openclaw/`, NOT the workspace.
- **[Session ID](../../term_dictionary/term_sessionid.md)** — session identifier; relevance: per-agent sessions folder migration.
- **[Sandbox](../../term_dictionary/term_sandbox.md)** — isolation; relevance: workspace is default cwd, NOT a hard sandbox (Warning callout).
- **[OAuth Token](../../term_dictionary/term_oauth_token.md)** — stored credential; relevance: auth-profiles.json kept out of the workspace repo (secret hygiene).

**Docs**

- **[oc_concepts_agent](oc_concepts_agent.md)** — runtime contract (planned, this series); relevance: bootstrap-file injection from this workspace.
- **[oc_concepts_active_memory_config](oc_concepts_active_memory_config.md)** — transcript persistence (planned, this series); relevance: transcript paths under the sessions folder.
- **[oc_concepts_soul](../openclaw/oc_concepts_soul.md)** — SOUL.md guide (planned, co07); relevance: persona workspace file detail.
- **[oc_concepts_memory](../openclaw/oc_concepts_memory.md)** — memory model (planned, co03); relevance: MEMORY.md / memory/YYYY-MM-DD.md log files.
- **[oc_concepts_session](../openclaw/oc_concepts_session.md)** — session storage (planned, co06); relevance: where sessions live vs the workspace.
- **[cc_claude_md_files](../claude_code/cc_claude_md_files.md)** — CLAUDE.md files; relevance: the closest analog to AGENTS.md workspace file.
- **[cc_dot_claude_directory](../claude_code/cc_dot_claude_directory.md)** — `.claude/` directory; relevance: the workspace-vs-config-dir split analog.
- **[cc_settings_files](../claude_code/cc_settings_files.md)** — settings files; relevance: config kept separate from the working tree (secret hygiene).
- **[hermes_personality_soul](../hermes_agent/hermes_personality_soul.md)** — Hermes SOUL.md; relevance: persona file equivalent.
- **[hermes_context_files](../hermes_agent/hermes_context_files.md)** — Hermes context files; relevance: AGENTS/USER/TOOLS workspace-file analog.
- **[pi_session_file_format](../pi/pi_session_file_format.md)** — Pi session format; relevance: session-storage layout kept out of workspace.
- **[hermes_session_storage](../hermes_agent/hermes_session_storage.md)** — Hermes session storage; relevance: session-dir migration analog.

**Repos**

- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — agent runtime; relevance: resolves/creates the workspace + bootstrap files.
- **[repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md)** — sessions; relevance: the sessions dir kept outside the workspace.
- **[repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md)** — skills; relevance: `<workspace>/skills` loading.

**Snippets**

- **[snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md)** — agent identity; relevance: IDENTITY.md workspace file.
- **[snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md)** — bootstrap budget; relevance: bootstrapMaxChars trimming of workspace files.
- **[snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md)** — session-key utils; relevance: sessions-folder layout outside workspace.
- **[snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md)** — memory root files; relevance: MEMORY.md / memory/ daily-log files in the map.
- **[snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md)** — auth-profile portability; relevance: auth-profiles.json kept out of the repo (migration).
- **[snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md)** — credential order; relevance: credentials under ~/.openclaw, not workspace.
- **[snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md)** — skills planner; relevance: workspace-skills precedence.
- **[snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md)** — context injection; relevance: workspace files injected into Project Context.
- **[snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md)** — setup config; relevance: `openclaw setup` seeds workspace bootstrap files.
- **[snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md)** — setup imports; relevance: workspace seeding/migration on a new machine.
- **[snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md)** — migration import; relevance: moving a workspace to a new machine.
- **[snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md)** — session chat type; relevance: per-agent session paths referenced in migration.

## References

- [OpenClaw Docs — Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace)
- [OpenClaw Docs — Sandboxing](https://docs.openclaw.ai/gateway/sandboxing)
- [OpenClaw Docs — SOUL.md personality guide](https://docs.openclaw.ai/concepts/soul)
- [OpenClaw Docs — Memory](https://docs.openclaw.ai/concepts/memory)
- [OpenClaw Docs — Internal hooks](https://docs.openclaw.ai/automation/hooks)
- [OpenClaw Docs — Heartbeat](https://docs.openclaw.ai/gateway/heartbeat)
- [OpenClaw Docs — Session](https://docs.openclaw.ai/concepts/session)
- [OpenClaw Docs — Channel routing](https://docs.openclaw.ai/channels/channel-routing)
- [OpenClaw Docs — Standing orders](https://docs.openclaw.ai/automation/standing-orders)

**Source**: OpenClaw documentation — `concepts/agent-workspace` (mirror `inbox/openclaw_docs/concepts/agent-workspace.md`)
**Last Updated**: 2026-06-22
**Status**: Active
