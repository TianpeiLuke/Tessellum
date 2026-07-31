---
tags:
  - resource
  - documentation
  - hermes_agent
  - troubleshooting
  - faq
keywords:
  - messaging gateway troubleshooting
  - performance and context compression
  - mcp issue fixes
  - hermes profiles isolation
  - workflow patterns recipes
  - backup vs profile export
topics:
  - Hermes Agent
  - Troubleshooting
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/reference/faq
access_control_group: ["general"]
---

# Hermes Agent — FAQ: Messaging, Performance, Profiles & Workflows

## Overview

This is the **operate-and-scale half of the Hermes Agent troubleshooting FAQ** — the fixes and recipes you reach for once the agent is already installed and answering, when you are running it as a multi-user messaging bot, tuning its context/token behavior, isolating work across profiles, or chaining models and chats into repeatable workflows. It is the companion to the first-run half (install / provider / terminal); together they mirror the source `reference/faq.md` page. Concretely it covers four problem domains: the **Messaging Issues** / **Performance Issues** / **MCP Issues** troubleshooting sections, the **Profiles** Q&A, and the **Workflows & Patterns** recipe gallery (plus the "Still Stuck?" escalation pointers). Each entry is a symptom → cause → fix triple driven by `hermes gateway`/`config`/`profile` commands and `config.yaml` edits; the underlying concepts (the messaging gateway, MCP, context compression, sessions, cron) are owned by their feature pages and linked from Related Notes rather than re-explained here.

## Messaging Issues

The messaging gateway lets multiple users reach one Hermes instance over Telegram, Discord, Slack, WhatsApp, or Home Assistant. Most failures are state (gateway not running), authorization (allowlist), or transport (token / webhook / PATH) problems:

- **Bot not responding** — the gateway isn't running, isn't authorized, or your user isn't on the allowlist. Check with `hermes gateway status`, start it with `hermes gateway start`, and inspect `~/.hermes/logs/gateway.log`.
- **Messages not delivering** — network issues, an expired bot token, or webhook misconfiguration. Re-verify the token with `hermes gateway setup`, tail the gateway log, and for webhook platforms (Slack, WhatsApp) make sure your server is publicly reachable.
- **Allowlist confusion** — three authorization modes decide who gets in: **Allowlist** (only listed user IDs), **DM pairing** (first DM claims exclusive access), and **Open** (anyone — not recommended for production). Configured under the gateway's settings in `config.yaml`.
- **Gateway won't start** — missing deps, a port conflict, or a bad token. Install `pip install "hermes-agent[messaging]"`, check the port with `lsof -i :8080`, and re-verify config with `hermes config show`.
- **WSL: gateway keeps disconnecting / `hermes gateway start` fails** — WSL's systemd support is unreliable, so prefer foreground mode (`hermes gateway run`, `tmux`, or `nohup`); enabling `systemd=true` in `/etc/wsl.conf` + `wsl --shutdown` is an optional fallback.
- **macOS: Node.js / ffmpeg not found by gateway** — launchd services inherit a minimal PATH that omits Homebrew/nvm/cargo, breaking the WhatsApp bridge (`node`) or voice transcription (`ffmpeg`). The gateway snapshots your shell PATH at `hermes gateway install`; re-run it after installing tools so the plist captures the updated PATH.

```bash
hermes gateway status                          # is the gateway running?
hermes gateway start                           # start it
cat ~/.hermes/logs/gateway.log | tail -50      # read recent errors
```

## Performance Issues

Slowness and runaway token use trace back to model choice, network distance, and a context that has grown too large. The primary lever Hermes gives you is `/compress`, which summarizes conversation history while preserving key context:

- **Slow responses** — a large model, a distant API server, or a heavy system prompt with many tools. Try a faster/smaller model (`hermes chat --model openrouter/meta-llama/llama-3.1-8b-instruct`), reduce active toolsets (`hermes chat -t "terminal"`), check provider latency, and for local models ensure enough GPU VRAM.
- **High token usage** — long conversations, verbose prompts, or accumulating tool calls. Run `/compress` to shrink history and `/usage` to inspect session token consumption; using `/compress` regularly during long sessions reduces tokens significantly while keeping context.
- **Session getting too long** — extended conversations approach context limits. `/compress` the current session, start a fresh one with `hermes chat`, or resume a prior session later with `hermes chat --continue`.

```bash
/compress    # summarize history → fewer tokens, key context kept
/usage       # show this session's token usage
```

## MCP Issues

MCP (Model Context Protocol) servers expose external tools to the agent; failures are usually a missing binary/runtime, tool-discovery/filtering, or a slow/crashed server. The full server-config schema and policy keys live in the MCP Config Reference:

- **MCP server not connecting** — the server binary isn't found, the command path is wrong, or a runtime is missing. Ensure MCP deps (`uv pip install -e ".[mcp]"` from `~/.hermes/hermes-agent`), confirm `node`/`npx` for npm-based servers, and test the server manually (`npx -y @modelcontextprotocol/server-filesystem /tmp`). Verify the `mcp_servers` block in `~/.hermes/config.yaml`.
- **Tools not showing up** — the server started but discovery failed, tools were filtered out, or the server lacks the expected capability. Check logs for connection errors, confirm the server answers `tools/list`, review the server's `tools.include`/`tools.exclude`/`tools.resources`/`tools.prompts`/`enabled` settings, remember resource/prompt utility tools register only when the session supports those capabilities, and run `/reload-mcp` after config changes.
- **MCP timeout errors** — the server is too slow or crashed mid-execution. Increase the server's timeout if supported, confirm the process is alive, check connectivity for remote HTTP servers, and inspect the server's own logs (a mid-request crash surfaces in Hermes as a timeout).

```bash
hermes config show | grep -A 12 mcp_servers    # inspect configured MCP servers
hermes chat                                     # restart / reload after config edits
```

## Profiles

Profiles are a managed isolation layer on top of `HERMES_HOME`. Each profile is just a directory under `~/.hermes/profiles/` with its own state, and Hermes handles the plumbing the manual `HERMES_HOME=...` approach makes you do by hand:

- **Profiles vs `HERMES_HOME`** — profiles create the directory structure, generate shell aliases (`hermes-work`), track the active profile in `~/.hermes/active_profile`, sync skill updates across all profiles automatically, and integrate with tab completion.
- **Shared bot token?** — no. Each messaging platform requires exclusive access to a bot token; two profiles using the same token simultaneously means the second gateway fails to connect. Create a separate bot per profile (Telegram: ask @BotFather for additional bots).
- **Shared memory/sessions?** — no. Each profile has its own memory store, session database, and skills directory; they are fully isolated. To seed a new profile from an existing one, use `hermes profile create newname --clone-all` (or `--clone-from <profile>`).
- **`hermes update` scope** — pulls the latest code and reinstalls dependencies **once** (not per-profile), then syncs updated skills to all profiles. Run it once per machine.
- **How many profiles?** — no hard limit; the practical ceiling is disk space and how many concurrent gateways your system handles. Idle profiles use no resources, so running dozens is fine.

## Workflows & Patterns

Recipes that combine the primitives above into repeatable patterns. Several are framed as "scenario → solution," sometimes flagging a current limitation and giving workarounds:

- **Multi-model workflows** — use **delegation config** so subagents run on a different model than your main chat. Set `delegation.model`/`delegation.provider` in `config.yaml`; a `delegate_task` subagent then picks it up automatically. For one-off switches, use `/model <name>` mid-session.
- **Per-chat binding on one WhatsApp number** — not supported: the WhatsApp bridge (Baileys) uses one authenticated session per number. Workarounds: single profile with personality switching (`AGENTS.md` / `/personality`), cron jobs for specialized chats, separate WhatsApp numbers per profile, or Telegram/Discord which bind per-chat more naturally.
- **Hiding logs/reasoning in Telegram** — set `display.tool_progress` in `config.yaml` (`off` / `new` / `all` / `verbose`); `off` or `new` suits messaging. Restart the gateway after editing, or toggle per-session with `/verbose` when `display.tool_progress_command: true`.
- **Telegram slash-command limit** — Telegram caps at 100 slash commands. Disable unneeded skills per-platform with `hermes skills config`, which writes `skills.platform_disabled.telegram`, then restart the gateway so the command menu rebuilds. (Skill descriptions are truncated to 40 chars in the Telegram menu.)
- **Shared thread sessions** — Hermes keys sessions by user ID on most platforms for privacy. To share one conversation across users, prefer **Slack** (thread-keyed) or a **Discord channel** (channel-keyed), or designate one operator relaying questions.
- **Exporting / moving** — `hermes backup` zips the entire `~/.hermes/` (config, keys, memories, skills, sessions, profiles) for full-machine migration; `hermes profile export <name>` makes a `.tar.gz` of one profile (credentials stripped for safe sharing); `hermes import` / `hermes profile import` restore them.
- **`hermes backup` vs `hermes profile export`** — backup = global `.zip` **including** `.env`/`auth.json` (full migration); profile export = single-profile `.tar.gz` **excluding** credentials (porting/sharing).
- **Permission denied on shell reload** — a shell-config permissions issue (`chmod 644 ~/.zshrc`), not Hermes-specific; or open a new terminal to pick up PATH changes.
- **Error 400 on first run** — usually a model-name mismatch (model doesn't exist on your provider or the key lacks access). Re-check `hermes config show`, re-run `hermes model`, or test with a known-good model; on OpenRouter, ensure the key has credits.

```yaml
# config.yaml — route subagents to a different model than the main chat
delegation:
  model: "google/gemini-3-flash-preview"   # subagents use this model
  provider: "openrouter"                    # provider for subagents
```

When an issue isn't covered, the **Still Stuck?** section points to GitHub Issues, the Nous Research Discord, and bug-report guidance (include OS, `python3 --version`, `hermes --version`, and the full error).

```text
hermes backup            → entire ~/.hermes (.zip, credentials INCLUDED)  — full migration
hermes profile export X  → single profile (.tar.gz, credentials EXCLUDED) — share/port
```

**Source**: `inbox/hermes_agent_docs/reference/faq.md` · https://hermes-agent.nousresearch.com/docs/reference/faq
**Last Updated**: 2026-06-19
**Status**: Active
