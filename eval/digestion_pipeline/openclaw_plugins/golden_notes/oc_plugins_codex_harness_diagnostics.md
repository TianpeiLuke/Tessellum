---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - codex_harness
keywords:
  - codex harness diagnostics
  - codex slash command
  - codex status
  - inspect codex threads locally
  - codex resume thread
  - gateway diagnostics export
  - codex feedback upload
  - native hook relay unavailable
  - codex harness troubleshooting
topics:
  - OpenClaw
  - Codex Harness
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/codex-harness
access_control_group: ["general"]
---

# OpenClaw — Operating a Codex-Harness Deployment (Commands & Diagnostics)

## Overview

This procedure note covers the day-2 operations of an enabled Codex app-server harness on OpenClaw: the `/codex` chat slash commands the bundled `codex` plugin registers, the `/diagnostics` vs `/codex diagnostics` feedback-upload split, how to inspect a bad Codex run by opening the native thread locally with `codex resume`, the summary of which surfaces OpenClaw still owns vs which Codex owns (runtime-boundary pointer), and the troubleshooting flow for the common Codex-harness failures. It mirrors the `Commands and diagnostics`, `Inspect Codex threads locally`, `Computer Use` (pointer), `Runtime boundaries` (summary), and `Troubleshooting` sections of the `plugins/codex-harness` source page; enablement/config lives in the setup note, deployment shapes and app-server policy in the deployment note, and the full config/runtime field reference in the reference notes.

## Commands and diagnostics

The bundled plugin registers `/codex` as a slash command on any channel that supports OpenClaw text commands. The common forms are:

- `/codex status` checks app-server connectivity, models, account, rate limits, MCP servers, and skills.
- `/codex models` lists live Codex app-server models.
- `/codex threads [filter]` lists recent Codex app-server threads.
- `/codex resume <thread-id>` attaches the current OpenClaw session to an existing Codex thread.
- `/codex compact` asks Codex app-server to compact the attached thread.
- `/codex review` starts Codex native review for the attached thread.
- `/codex diagnostics [note]` asks before sending Codex feedback for the attached thread.
- `/codex account` shows account and rate-limit status.
- `/codex mcp` lists Codex app-server MCP server status.
- `/codex skills` lists Codex app-server skills.

For most support reports, start with `/diagnostics [note]` in the conversation where the bug happened. It creates one Gateway diagnostics report and, for Codex harness sessions, asks for approval to send the relevant Codex feedback bundle. See [Diagnostics export](https://docs.openclaw.ai/gateway/diagnostics) for the privacy model and group chat behavior. Use `/codex diagnostics [note]` only when you specifically want the Codex feedback upload for the currently attached thread without the full Gateway diagnostics bundle.

### Inspect Codex threads locally

The fastest way to inspect a bad Codex run is often to open the native Codex thread directly:

```bash
codex resume <thread-id>
```

Get the thread id from the completed `/diagnostics` reply, `/codex binding`, or `/codex threads [filter]`. For upload mechanics and runtime-level diagnostics boundaries, see the runtime contract (Codex feedback upload) covered in the runtime note.

## Computer Use (pointer)

Computer Use is operated through its own setup guide and is not re-documented here. The short version: OpenClaw does not vendor the desktop-control app or execute desktop actions itself — it prepares Codex app-server, verifies that the `computer-use` MCP server is available, and then lets Codex own the native MCP tool calls during Codex-mode turns. Diagnostics for it surface through `/codex computer-use status` (see Troubleshooting below).

## Runtime boundaries (summary)

The Codex harness changes the low-level embedded agent executor only; the full hook-layer / V1-surface / permission contract lives in the runtime note. The summary boundary, as you operate a deployment, is:

- OpenClaw dynamic tools are supported. Codex asks OpenClaw to execute those tools, so OpenClaw remains in the execution path.
- Codex-native shell, patch, MCP, and native app tools are owned by Codex. OpenClaw can observe or block selected native events through the supported relay, but it does not rewrite native tool arguments.
- Codex owns native compaction. OpenClaw keeps a transcript mirror for channel history, search, `/new`, `/reset`, and future model or harness switching, but it does not replace Codex compaction with an OpenClaw or context-engine summarizer.
- Media generation, media understanding, TTS, approvals, and messaging-tool output continue through the matching OpenClaw provider/model settings.
- `tool_result_persist` applies to OpenClaw-owned transcript tool results, not Codex-native tool result records.

## Troubleshooting

Work through these against the symptom you observe; each maps to a documented Codex-harness failure mode.

- **Codex does not appear as a normal `/model` provider:** that is expected for new configs. Select an `openai/gpt-*` model, enable `plugins.entries.codex.enabled`, and check whether `plugins.allow` excludes `codex`.
- **OpenClaw uses the built-in harness instead of Codex:** make sure the model ref is `openai/gpt-*` on the official OpenAI provider and that the Codex plugin is installed and enabled. If you need strict proof while testing, set provider or model `agentRuntime.id: "codex"`. A forced Codex runtime fails instead of falling back to OpenClaw.
- **OpenAI Codex runtime falls back to the API-key path:** collect a redacted gateway excerpt that shows the model, runtime, selected provider, and failure. Ask affected collaborators to run the read-only log-grep command below on their OpenClaw host. Useful excerpts usually include `openai/gpt-5.5` or `openai/gpt-5.4`, `Runtime: OpenAI Codex`, `agentRuntime.id` or `harnessRuntime`, `candidateProvider: "openai"`, and a `401`, `Incorrect API key`, or `No API key` result. A corrected run should show the OpenAI OAuth path instead of a plain OpenAI API-key failure.

```bash
(
  pattern='openai/gpt-5\.[45]|openai[-]codex|agentRuntime(\.id)?|harnessRuntime|Runtime: OpenAI Codex|legacy OpenAI Codex prefix|resolveSelectedOpenAIRuntimeProvider|candidateProvider[": ]+openai|status[": ]+401|Incorrect API key|No API key|api-key path|API-key path|OAuth'

  if ls /tmp/openclaw/openclaw-*.log >/dev/null 2>&1; then
    grep -E -i -n "$pattern" /tmp/openclaw/openclaw-*.log 2>/dev/null || true
  else
    journalctl --user -u openclaw-gateway --since today --no-pager 2>/dev/null \
      | grep -E -i "$pattern" || true
  fi
) | sed -E \
    -e 's/(Authorization: Bearer )[A-Za-z0-9._~+\/-]+/\1[REDACTED]/Ig' \
    -e 's/(Bearer )[A-Za-z0-9._~+\/-]+/\1[REDACTED]/Ig' \
    -e 's/(api[_ -]?key[=: ]+)[^ ,}"]+/\1[REDACTED]/Ig' \
    -e 's/(OPENAI_API_KEY[=: ]+)[^ ,}"]+/\1[REDACTED]/Ig' \
    -e 's/sk-[A-Za-z0-9_-]{12,}/sk-[REDACTED]/g' \
    -e 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/[EMAIL-REDACTED]/g' \
  | tail -200
```

- **Legacy Codex model refs config remains:** run `openclaw doctor --fix`. Doctor rewrites legacy model refs to `openai/*`, removes stale session and whole-agent runtime pins, and preserves existing auth-profile overrides.
- **The app-server is rejected:** use Codex app-server `0.125.0` or newer. Same-version prereleases or build-suffixed versions such as `0.125.0-alpha.2` or `0.125.0+custom` are rejected because OpenClaw tests the stable `0.125.0` protocol floor.
- **`/codex status` cannot connect:** check that the bundled `codex` plugin is enabled, that `plugins.allow` includes it when an allowlist is configured, and that any custom `appServer.command`, `url`, `authToken`, or headers are valid.
- **Model discovery is slow:** lower `plugins.entries.codex.config.discovery.timeoutMs` or disable discovery (see the reference-config note's Model discovery section).
- **WebSocket transport fails immediately:** check `appServer.url`, `authToken`, headers, and that the remote app-server speaks the same Codex app-server protocol version.
- **Native shell or patch tools are blocked with `Native hook relay unavailable`:** the Codex thread is still trying to use a native hook relay id that OpenClaw no longer has registered. This is a native Codex hook transport problem, not an ACP backend, provider, GitHub, or shell-command failure. Start a fresh session in the affected chat with `/new` or `/reset`, then retry a harmless command. If that works once but the next native tool call fails again, treat `/new` as a temporary workaround only: copy the prompt into a fresh session after restarting the Codex app-server or OpenClaw Gateway so old threads are dropped and native hook registrations are recreated.
- **A non-Codex model uses the built-in harness:** that is expected unless provider or model runtime policy routes it to another harness. Plain non-OpenAI provider refs stay on their normal provider path in `auto` mode.
- **Computer Use is installed but tools do not run:** check `/codex computer-use status` from a fresh session. If a tool reports `Native hook relay unavailable`, use the native hook relay recovery above.

## Related Notes

**Terms**

- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway; relevance: `/codex` chat commands and `/diagnostics` are OpenClaw runtime surfaces.
- **[Agent Harness](../../term_dictionary/term_agent_harness.md)** — agent runtime; relevance: diagnostics inspect a Codex-harness deployment.
- **[Compaction](../../term_dictionary/term_compaction.md)** — transcript compaction; relevance: `/codex compact` starts native Codex compaction.
- **[Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md)** — coding-agent runtime; relevance: `codex resume <thread-id>` inspects native Codex threads.
- **[Function Calling](../../term_dictionary/term_function_calling.md)** — model tool calls; relevance: `/codex mcp`/`/codex skills` list the tool surfaces of a thread.
- **[Tool Registry](../../term_dictionary/term_tool_registry.md)** — tool catalog; relevance: `/codex status` reports MCP servers and skills.
- **[MCP](../../term_dictionary/term_mcp.md)** — MCP servers; relevance: `/codex mcp` lists Codex app-server MCP server status.
- **[Trajectory](../../term_dictionary/term_trajectory.md)** — recorded agent run trace; relevance: diagnostics/feedback upload and app-server trajectory capture for debugging.

**Docs**

- **[hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md)** — Hermes Codex runtime tools; relevance: sibling `/codex`-style command/tool inspection surface.
- **[cc_manage_your_session](../claude_code/cc_manage_your_session.md)** — session management; relevance: analog for resuming/inspecting agent threads.
- **[cc_sessions](../claude_code/cc_sessions.md)** — session model; relevance: the thread/session inspection (`/codex threads`, `codex resume`) maps to session lifecycle.
- **[cc_hook_session_lifecycle_events](../claude_code/cc_hook_session_lifecycle_events.md)** — session lifecycle events; relevance: `/new`/`/reset` recovery flow referenced in troubleshooting.
- **[hermes_cli_commands_session_ops](../hermes_agent/hermes_cli_commands_session_ops.md)** — CLI session ops; relevance: analog for the `/codex`/`/diagnostics` chat-command surface.
- **[oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md)** — runtime-boundary summary; the full boundary contract lives here.
- **[oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md)** — `/status`/`/codex status` verification originate in setup.
- **[oc_plugins_codex_computer_use](oc_plugins_codex_computer_use.md)** — `/codex computer-use status` is part of the diagnostics surface.
- **[oc_plugins_codex_harness_reference_runtime](oc_plugins_codex_harness_reference_runtime.md)** — timeout diagnostics fields reference.
- **[oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md)** — `/codex plugins list` diagnostics overlap.

**Repos**

- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — agent runtime; relevance: `/codex` command + diagnostics handlers live here.
- **[repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md)** — session/thread state; relevance: thread binding and transcript-mirror inspection.

**Snippets**

- **[snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md)** — CLI command catalog; relevance: registration of `/codex` slash commands.
- **[snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md)** — session lifecycle; relevance: `/new`/`/reset` thread-binding refresh.
- **[snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md)** — transcript events; relevance: the transcript-mirror inspection surface.
- **[snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md)** — compact/reset; relevance: `/codex compact` and `/reset` mechanics.
- **[snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md)** — reset helpers; relevance: clearing stale native thread bindings on reset.
- **[snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md)** — doctor repair; relevance: `openclaw doctor --fix` legacy-ref repair referenced in troubleshooting.
- **[snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md)** — usage/latency status; relevance: `/codex status` rate-limit/account reporting.
- **[snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md)** — event ledger; relevance: app-server trajectory/event capture for diagnostics.
- **[snippet_hermes_agent_cli_codex_migrate](../../code_snippets/snippet_hermes_agent_cli_codex_migrate.md)** — Codex CLI migrate; relevance: analog for Codex thread/diagnostics CLI ops.
- **[snippet_hermes_agent_cli_hermescli_session_handlers](../../code_snippets/snippet_hermes_agent_cli_hermescli_session_handlers.md)** — CLI session handlers; relevance: analog for `/codex threads`/`resume` session handlers.
- **[snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md)** — chat abort; relevance: interrupting a stale native turn (timeout/abort) during diagnostics.

## References

- [OpenClaw Docs — Codex harness](https://docs.openclaw.ai/plugins/codex-harness)
- [OpenClaw Docs — Codex harness runtime (Codex feedback upload)](https://docs.openclaw.ai/plugins/codex-harness-runtime#codex-feedback-upload)
- [OpenClaw Docs — Codex harness reference (Model discovery)](https://docs.openclaw.ai/plugins/codex-harness-reference#model-discovery)
- [OpenClaw Docs — Codex Computer Use (Troubleshooting)](https://docs.openclaw.ai/plugins/codex-computer-use#troubleshooting)
- [OpenClaw Docs — Diagnostics export](https://docs.openclaw.ai/gateway/diagnostics)
- [OpenClaw Docs — Status](https://docs.openclaw.ai/cli/status)
- [OpenClaw Docs — Agent runtimes](https://docs.openclaw.ai/concepts/agent-runtimes)

**Source**: OpenClaw documentation — `plugins/codex-harness` (mirror `inbox/openclaw_docs/plugins/codex-harness.md`), sections Commands and diagnostics, Inspect Codex threads locally, Computer Use (pointer), Runtime boundaries (summary), Troubleshooting
**Last Updated**: 2026-06-22
**Status**: Active
