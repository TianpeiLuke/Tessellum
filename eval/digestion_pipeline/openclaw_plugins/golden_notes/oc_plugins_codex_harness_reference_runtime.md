---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - codex_harness
keywords:
  - codex harness runtime reference
  - sandboxed native execution
  - sandboxExecServer preview
  - codex auth environment isolation
  - CODEX_HOME per-agent isolation
  - codex dynamic tools searchable direct
  - codexDynamicToolsExclude
  - item/tool/call timeout watchdog
  - turnCompletionIdleTimeoutMs
  - postToolRawAssistantCompletionIdleTimeoutMs
topics:
  - OpenClaw
  - Codex Harness
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/codex-harness-reference
access_control_group: ["general"]
---

# OpenClaw — Codex Harness Runtime-Execution Reference

## Overview

This note models the runtime-execution half of the bundled `codex` plugin reference — the mechanics OpenClaw enforces while a Codex app-server turn actually runs, as opposed to the declarative config fields (covered by `oc_plugins_codex_harness_reference_config`). It mirrors four sections of the `plugins/codex-harness-reference` source page: **Sandboxed native execution** (the fail-closed sandbox-exec preview), **Auth and environment isolation** (auth-selection order, ChatGPT-subscription key stripping, `CODEX_HOME`/`HOME` scoping, `clearEnv`), **Dynamic tools** (`searchable` vs `direct` loading and the excluded native-duplicate tools), and **Timeouts** (the per-call `item/tool/call` watchdog, the turn-completion idle guards, and replay safety). Every field name, default, env var, and tool name is reproduced verbatim from the source page.

## Sandboxed Native Execution

The stable default is **fail-closed**: when an OpenClaw sandbox is active, OpenClaw disables the native Codex execution surfaces that would otherwise run from the Codex app-server host. To try Codex's remote-environment support backed by OpenClaw's sandbox, set the preview opt-in `appServer.experimental.sandboxExecServer: true`; this path requires Codex app-server `0.132.0` or newer.

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            experimental: {
              sandboxExecServer: true,
            },
          },
        },
      },
    },
  },
}
```

When the flag is on and the current OpenClaw session is sandboxed, OpenClaw starts a local loopback exec-server backed by the active sandbox, registers it with Codex app-server, and starts the Codex thread and turn with that OpenClaw-owned environment. If the app-server cannot register the environment, the run fails closed instead of silently falling back to host execution. This preview path is **local-only**: a remote WebSocket app-server cannot reach the loopback exec-server unless it runs on the same host, so OpenClaw rejects that combination. (Background from the Approval and sandbox modes section: when an OpenClaw sandbox is active without this flag, the local Codex app-server still runs on the Gateway host, so OpenClaw disables Codex native Code Mode, user MCP servers, and app-backed plugin execution for that turn, and exposes shell access only through OpenClaw sandbox-backed dynamic tools such as `sandbox_exec` and `sandbox_process`.)

## Auth and Environment Isolation

Auth is selected in this order:

1. An explicit OpenClaw Codex auth profile for the agent.
2. The app-server's existing account in that agent's Codex home.
3. For local stdio app-server launches only, `CODEX_API_KEY`, then `OPENAI_API_KEY`, when no app-server account is present and OpenAI auth is still required.

When OpenClaw sees a ChatGPT subscription-style Codex auth profile, it removes `CODEX_API_KEY` and `OPENAI_API_KEY` from the spawned Codex child process. That keeps Gateway-level API keys available for embeddings or direct OpenAI models without making native Codex app-server turns bill through the API by accident. Explicit Codex API-key profiles and the local stdio env-key fallback use app-server login instead of inherited child-process env. WebSocket app-server connections do not receive Gateway env API-key fallback; use an explicit auth profile or the remote app-server's own account.

Stdio app-server launches inherit OpenClaw's process environment by default. OpenClaw owns the Codex app-server account bridge and sets `CODEX_HOME` to a per-agent directory under that agent's OpenClaw state, keeping Codex config, accounts, plugin cache/data, and thread state scoped to the OpenClaw agent instead of leaking in from the operator's personal `~/.codex` home. OpenClaw does **not** rewrite `HOME` for normal local app-server launches, so Codex-run subprocesses such as `openclaw`, `gh`, `git`, cloud CLIs, and shell commands see the normal process home and can find user-home config and tokens. Codex may also discover `$HOME/.agents/skills` and `$HOME/.agents/plugins/marketplace.json`; that `.agents` discovery is intentionally shared with the operator home and is separate from isolated `~/.codex` state. OpenClaw plugins and OpenClaw skill snapshots still flow through OpenClaw's own plugin registry and skill loader, while personal Codex `~/.codex` assets do not — to bring useful Codex CLI skills or plugins into an OpenClaw agent, inventory them explicitly:

```bash
openclaw migrate codex --dry-run
openclaw migrate apply codex --yes
```

If a deployment needs additional environment isolation, add those variables to `appServer.clearEnv`:

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            clearEnv: ["CODEX_API_KEY", "OPENAI_API_KEY"],
          },
        },
      },
    },
  },
}
```

`appServer.clearEnv` only affects the spawned Codex app-server child process. OpenClaw removes `CODEX_HOME` and `HOME` from this list during local launch normalization: `CODEX_HOME` stays per-agent, and `HOME` stays inherited so subprocesses can use normal user-home state.

## Dynamic Tools

Codex dynamic tools default to `searchable` loading. OpenClaw does not expose dynamic tools that duplicate Codex-native workspace operations — the excluded native-duplicate tools are:

- `read`
- `write`
- `edit`
- `apply_patch`
- `exec`
- `process`
- `update_plan`

Most remaining OpenClaw integration tools — such as messaging, media, cron, browser, nodes, gateway, `heartbeat_respond`, and `web_search` — are available through Codex tool search under the `openclaw` namespace, which keeps the initial model context smaller. `sessions_yield` and message-tool-only source replies stay direct because those are turn-control contracts. `sessions_spawn` stays searchable so Codex's native `spawn_agent` remains the primary Codex subagent surface, while explicit OpenClaw or ACP delegation is still available through the `openclaw` dynamic-tool namespace. Set `codexDynamicToolsLoading: "direct"` only when connecting to a custom Codex app-server that cannot search deferred dynamic tools or when debugging the full tool payload. (Additional native dynamic-tool names can be omitted from Codex turns via `codexDynamicToolsExclude`, documented in the config-surface reference.)

## Timeouts

OpenClaw-owned dynamic tool calls are bounded independently from `appServer.requestTimeoutMs`. Each Codex `item/tool/call` request uses the first available timeout in this order:

- A positive per-call `timeoutMs` argument.
- For `image_generate`, `agents.defaults.imageGenerationModel.timeoutMs`.
- For `image_generate` without a configured timeout, the 120 second image-generation default.
- For the media-understanding `image` tool, `tools.media.image.timeoutSeconds` converted to milliseconds, or the 60 second media default. For image understanding, this applies to the request itself and is not reduced by earlier preparation work.
- The 90 second dynamic-tool default.

This watchdog is the outer dynamic `item/tool/call` budget; provider-specific request timeouts run inside that call and keep their own timeout semantics. Dynamic tool budgets are capped at `600000` ms. On timeout, OpenClaw aborts the tool signal where supported and returns a failed dynamic-tool response to Codex so the turn can continue instead of leaving the session in `processing`.

After Codex accepts a turn — and after OpenClaw responds to a turn-scoped app-server request — the harness expects Codex to make current-turn progress and eventually finish the native turn with `turn/completed`. If the app-server goes quiet for `appServer.turnCompletionIdleTimeoutMs`, OpenClaw best-effort interrupts the Codex turn, records a diagnostic timeout, and releases the OpenClaw session lane so follow-up chat messages are not queued behind a stale native turn. Most non-terminal notifications for the same turn disarm that short watchdog because Codex has proven the turn is still alive.

Tool handoffs use a longer post-tool idle budget: after OpenClaw returns an `item/tool/call` response, after native tool items such as `commandExecution` complete, after raw `custom_tool_call_output` completions, and after post-tool raw assistant progress, raw reasoning completions, or reasoning progress. This guard uses `appServer.postToolRawAssistantCompletionIdleTimeoutMs` when configured and defaults to five minutes otherwise; that same post-tool budget also extends the progress watchdog for the silent synthesis window before Codex emits the next current-turn event. Reasoning completions, commentary `agentMessage` completions, and pre-tool raw reasoning or assistant progress can be followed by an automatic final reply, so they use the post-progress reply guard instead of releasing the session lane immediately. Only final/non-commentary completed `agentMessage` items and pre-tool raw assistant completions arm the assistant-output release: if Codex then goes quiet without `turn/completed`, OpenClaw best-effort interrupts the native turn and releases the session lane.

Replay-safe stdio app-server failures — including turn-completion idle timeouts without assistant, tool, active-item, or side-effect evidence — are retried once on a fresh app-server attempt. Unsafe timeouts instead retire the stuck app-server client, release the OpenClaw session lane, and clear the stale native thread binding rather than being replayed automatically. Completion-watch timeouts surface Codex-specific timeout text: replay-safe cases say the response may be incomplete, while unsafe cases tell the user to verify current state before retrying. Public timeout diagnostics include structural fields such as the last app-server notification method, raw assistant response item id/type/role, active request/item counts, and armed watch state; when the last notification is a raw assistant response item they also include a bounded assistant text preview, but they do not include raw prompt or tool content.

## Related Notes

**Terms**

- **[Sandbox](../../term_dictionary/term_sandbox.md)** — execution isolation; relevance: sandboxed native exec — active OpenClaw sandboxing disables native Codex exec surfaces / `experimental.sandboxExecServer`.
- **[Authentication](../../term_dictionary/term_authentication.md)** — credential verification; relevance: auth-selection order and ChatGPT-subscription key stripping.
- **[OAuth Token](../../term_dictionary/term_oauth_token.md)** — OAuth credential; relevance: subscription auth profile vs `CODEX_API_KEY`/`OPENAI_API_KEY` env fallback.
- **[Function Calling](../../term_dictionary/term_function_calling.md)** — model tool calls; relevance: OpenClaw dynamic-tool bridging into the app-server `item/tool/call`.
- **[Tool Registry](../../term_dictionary/term_tool_registry.md)** — tool catalog; relevance: `searchable` vs `direct` dynamic-tool loading and excluded native-duplicate tools.
- **[Guardian](../../term_dictionary/term_guardian.md)** — review gate; relevance: guardian-reviewed approvals and bwrap/AppArmor host-policy notes.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway; relevance: subject — auth/env isolation between OpenClaw and Codex home (`CODEX_HOME`).
- **[Agent Harness](../../term_dictionary/term_agent_harness.md)** — agent runtime; relevance: runtime-execution reference for the Codex harness.

**Docs**

- **[cc_sdk_custom_tool_definition](../claude_code/cc_sdk_custom_tool_definition.md)** — custom tool definition; relevance: analog for OpenClaw dynamic-tool registration/bridging into the harness.
- **[cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md)** — sandbox FS/network isolation; relevance: analog for `networkProxy`/sandboxed-exec network/filesystem isolation.
- **[cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md)** — sandbox runtime/containers; relevance: analog for the sandbox-backed exec-server preview path.
- **[hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md)** — Hermes Codex runtime tools; relevance: sibling dynamic-tool/native-tool runtime surface.
- **[pi_security_model](../pi/pi_security_model.md)** — security/isolation model; relevance: analog for auth/env isolation and key-stripping posture.
- **[cc_sdk_tool_approval_handling](../claude_code/cc_sdk_tool_approval_handling.md)** — tool approval handling; relevance: analog for per-call timeout/approval and dynamic-tool watchdog.
- **[oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md)** — the declarative config half of the reference; relevance: where the `appServer.*`/`discovery`/`codexDynamicToolsExclude` field definitions live.
- **[oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md)** — the prose runtime contract these mechanics implement; relevance: ownership-boundary contract behind the exec/isolation/timeout mechanics.
- **[oc_plugins_codex_harness_deployment](oc_plugins_codex_harness_deployment.md)** — deployments that toggle sandboxed exec/isolation; relevance: which deployment shapes enable `sandboxExecServer`/`clearEnv`.
- **[oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md)** — `clearEnv`/`CODEX_HOME` isolation introduced from setup auth; relevance: the auth quickstart whose profiles this note's selection order consumes.

**Repos**

- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — agent runtime; relevance: dynamic-tool bridging + timeout watchdog code.
- **[repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md)** — sandbox/exec security; relevance: sandboxed-native-exec, `sandbox_exec`/`sandbox_process`, env isolation.

**Snippets**

- **[snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md)** — tool catalog; relevance: `searchable` vs `direct` dynamic-tool loading and the `openclaw` namespace.
- **[snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md)** — tool policy; relevance: excluded native-duplicate tools (`read`/`write`/`exec`/`apply_patch`).
- **[snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md)** — exec/filesystem policy; relevance: sandbox-active disables native Code Mode / routes through sandbox tools.
- **[snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md)** — dangerous-tool deny; relevance: fail-closed when sandbox exec cannot register.
- **[snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md)** — exec orchestrator; relevance: `sandbox_exec`/`sandbox_process` execution path.
- **[snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md)** — exec runtime audit; relevance: sandboxed native execution boundary.
- **[snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md)** — credential/secret resolution; relevance: auth-profile vs env-key selection and stripping.
- **[snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md)** — auth-profile ordering; relevance: the 3-step auth-selection order this note documents.
- **[snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md)** — runtime env; relevance: `CODEX_HOME`/`HOME`/`clearEnv` child-process env normalization.
- **[snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md)** — MCP loopback; relevance: local loopback exec-server registration with app-server.
- **[snippet_openclaw_agents_context_window_guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md)** — context-window/timeout guard; relevance: per-phase timeout watchdog semantics.
- **[snippet_hermes_agent_core_tool_dispatch_helpers](../../code_snippets/snippet_hermes_agent_core_tool_dispatch_helpers.md)** — tool dispatch helpers; relevance: analog for dynamic-tool dispatch/timeout into a runtime.

## References

- [OpenClaw Docs — Codex harness reference](https://docs.openclaw.ai/plugins/codex-harness-reference)
- [OpenClaw Docs — Codex harness](https://docs.openclaw.ai/plugins/codex-harness)
- [OpenClaw Docs — Codex harness runtime](https://docs.openclaw.ai/plugins/codex-harness-runtime)
- [OpenClaw Docs — Native Codex plugins](https://docs.openclaw.ai/plugins/codex-native-plugins)
- [OpenClaw Docs — Codex Computer Use](https://docs.openclaw.ai/plugins/codex-computer-use)
- [OpenClaw Docs — OpenAI provider](https://docs.openclaw.ai/providers/openai)
- [OpenClaw Docs — Configuration reference](https://docs.openclaw.ai/gateway/configuration-reference)

**Source**: OpenClaw documentation — `plugins/codex-harness-reference` (mirror `inbox/openclaw_docs/plugins/codex-harness-reference.md`), sections "Sandboxed native execution", "Auth and environment isolation", "Dynamic tools", "Timeouts"
**Last Updated**: 2026-06-22
**Status**: Active
