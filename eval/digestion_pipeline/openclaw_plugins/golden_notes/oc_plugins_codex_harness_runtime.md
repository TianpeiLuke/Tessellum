---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - codex_harness
keywords:
  - codex harness runtime contract
  - openclaw owns vs codex owns
  - codex native model loop
  - native hook relay pretooluse posttooluse
  - v1 support contract codex
  - mcp elicitation codex_approval_kind
  - queue steering turn/steer
  - codex feedback upload diagnostics
  - native compaction transcript mirror
  - codex thread bindings model change
topics:
  - OpenClaw
  - Codex Harness
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/codex-harness-runtime
access_control_group: ["general"]
---

# OpenClaw — Codex Harness Runtime Contract (Ownership Boundary)

## Overview

This note captures the **Codex harness runtime contract** — the conceptual boundary describing what changes when Codex (rather than OpenClaw's embedded harness) owns the native model loop — mirroring the `plugins/codex-harness-runtime` source page. Codex mode is *not* OpenClaw with a different model call underneath: Codex owns more of the native model loop, and OpenClaw adapts its plugin, tool, session, and diagnostic surfaces around that boundary. The note covers the ownership split, thread bindings, visible-reply/heartbeat behavior, the three hook layers and relay rules, the v1 support contract, native permission/MCP-elicitation routing, queue steering, feedback upload, native compaction with OpenClaw's transcript mirror, and media delivery. For setup/routing see the harness setup note; for config fields see the harness reference notes (linked below).

## The Ownership Boundary

The runtime contract turns on a single split. **OpenClaw still owns** channel routing, session files, visible message delivery, OpenClaw dynamic tools, approvals, media delivery, and a transcript mirror. **Codex owns** the canonical native thread, native model loop, native tool continuation, and native compaction. Prompt routing follows the *selected runtime*, not just the provider string: a native Codex turn receives Codex app-server developer instructions, while an explicit OpenClaw compatibility route keeps the normal OpenClaw system prompt even when it uses Codex-flavored OpenAI auth or transport.

Native Codex keeps Codex-owned base/model instructions and project-doc behavior according to the active Codex thread config. OpenClaw starts and resumes native Codex threads with Codex's built-in personality disabled so workspace personality files and OpenClaw agent identity stay authoritative; lightweight OpenClaw runs still preserve their existing project-doc suppression. OpenClaw developer instructions cover OpenClaw runtime concerns such as source-channel delivery, OpenClaw dynamic tools, ACP delegation, adapter context, and the active agent workspace profile files. OpenClaw skill catalogs and tool-routed `MEMORY.md` pointers are projected as turn-scoped collaboration developer instructions for native Codex, while active `BOOTSTRAP.md` content and full `MEMORY.md` fallback injection still use turn input reference context.

## Thread Bindings and Model Changes

When an OpenClaw session is attached to an existing Codex thread, the next turn sends the currently selected OpenAI model, approval policy, sandbox, and service tier to app-server again. Switching from `openai/gpt-5.5` to `openai/gpt-5.2` keeps the thread binding but asks Codex to continue with the newly selected model.

## Visible Replies and Heartbeats

When a direct/source chat turn runs through the Codex harness, visible replies default to automatic final assistant delivery for internal WebChat surfaces — this keeps Codex aligned with the Pi harness prompt contract: agents reply normally, and OpenClaw posts the final text to the source conversation. Set `messages.visibleReplies: "message_tool"` when a direct/source chat should intentionally keep final assistant text private unless the agent calls `message(action="send")`.

Codex heartbeat turns also get `heartbeat_respond` in the searchable OpenClaw tool catalog by default, so the agent can record whether the wake should stay quiet or notify without encoding that control flow in final text. Heartbeat-specific initiative guidance is sent as a Codex collaboration-mode developer instruction on the heartbeat turn itself; ordinary chat turns restore Codex Default mode instead of carrying heartbeat philosophy in their normal runtime prompt. When a non-empty `HEARTBEAT.md` exists, the heartbeat collaboration-mode instructions point Codex at the file instead of inlining its contents.

## Hook Boundaries

The Codex harness has three hook layers:

| Layer | Owner | Purpose |
| --- | --- | --- |
| OpenClaw plugin hooks | OpenClaw | Product/plugin compatibility across OpenClaw and Codex harnesses. |
| Codex app-server extension middleware | OpenClaw bundled plugins | Per-turn adapter behavior around OpenClaw dynamic tools. |
| Codex native hooks | Codex | Low-level Codex lifecycle and native tool policy from Codex config. |

OpenClaw does not use project or global Codex `hooks.json` files to route OpenClaw plugin behavior. For the supported native tool and permission bridge, OpenClaw injects per-thread Codex config for `PreToolUse`, `PostToolUse`, `PermissionRequest`, and `Stop`. When Codex app-server approvals are enabled (meaning `approvalPolicy` is not `"never"`), the default injected native hook config omits `PermissionRequest` so Codex's app-server reviewer and OpenClaw's approval bridge handle real escalations after review; operators can explicitly add `permission_request` to `nativeHookRelay.events` when they need the compatibility relay. Other Codex hooks such as `SessionStart` and `UserPromptSubmit` remain Codex-level controls and are not exposed as OpenClaw plugin hooks in the v1 contract.

For OpenClaw dynamic tools, OpenClaw executes the tool after Codex asks for the call, so OpenClaw fires the plugin and middleware behavior it owns in the harness adapter. For Codex-native tools, Codex owns the canonical tool record: OpenClaw can mirror selected events, but it cannot rewrite the native Codex thread unless Codex exposes that operation through app-server or native hook callbacks. Codex app-server report-mode `PreToolUse` events defer plugin approval requests to the matching app-server approval — if an OpenClaw `before_tool_call` hook returns `requireApproval` while the native payload sets report approval mode (`openclaw_approval_mode` is `"report"`), the native hook relay records the plugin approval requirement and returns no native decision; when Codex then sends the app-server approval request for the same tool use, OpenClaw opens the plugin approval prompt and maps the decision back to Codex. Codex `PermissionRequest` events are a separate approval path that can still route through OpenClaw approvals when the runtime is configured for that bridge.

Codex app-server item notifications also provide async `after_tool_call` observations for native tool completions that are not already covered by the native `PostToolUse` relay; these observations are for telemetry and plugin compatibility only and cannot block, delay, or mutate the native tool call. Compaction and LLM lifecycle projections come from Codex app-server notifications and OpenClaw adapter state, not native Codex hook commands — OpenClaw's `before_compaction`, `after_compaction`, `llm_input`, and `llm_output` events are adapter-level observations, not byte-for-byte captures of Codex's internal request or compaction payloads. Codex native `hook/started` and `hook/completed` app-server notifications are projected as `codex_app_server.hook` agent events for trajectory and debugging; they do not invoke OpenClaw plugin hooks.

## V1 Support Contract

Supported in Codex runtime v1:

| Surface | Support | Why |
| --- | --- | --- |
| OpenAI model loop through Codex | Supported | Codex app-server owns the OpenAI turn, native thread resume, and native tool continuation. |
| OpenClaw channel routing and delivery | Supported | Telegram, Discord, Slack, WhatsApp, iMessage, and other channels stay outside the model runtime. |
| OpenClaw dynamic tools | Supported | Codex asks OpenClaw to execute these tools, so OpenClaw stays in the execution path. |
| Prompt and context plugins | Supported | OpenClaw projects OpenClaw-specific prompt/context while leaving Codex-owned base/model/project-doc prompts in the native lane; native Codex developer instructions accept only command guidance scoped to `codex_app_server`. |
| Context engine lifecycle | Supported | Assemble, ingest, and after-turn maintenance run around Codex turns; context engines do not replace native Codex compaction. |
| Dynamic tool hooks | Supported | `before_tool_call`, `after_tool_call`, and tool-result middleware run around OpenClaw-owned dynamic tools. |
| Lifecycle hooks | Supported as adapter observations | `llm_input`, `llm_output`, `agent_end`, `before_compaction`, and `after_compaction` fire with honest Codex-mode payloads. |
| Final-answer revision gate | Supported through native hook relay | Codex `Stop` is relayed to `before_agent_finalize`; `revise` asks Codex for one more model pass before finalization. |
| Native shell, patch, and MCP block or observe | Supported through native hook relay | Codex `PreToolUse`/`PostToolUse` relayed for committed native tool surfaces, including MCP payloads on Codex app-server `0.125.0`+. Blocking is supported; argument rewriting is not. |
| Native permission policy | Supported through Codex app-server approvals + compatibility native hook relay | App-server approval requests route through OpenClaw after Codex review; the `PermissionRequest` relay is opt-in because Codex emits it before guardian review. |
| App-server trajectory capture | Supported | OpenClaw records the request it sent to app-server and the app-server notifications it receives. |

Not supported in Codex runtime v1 (each has a stated future path): **native tool argument mutation** (native pre-tool hooks can block, but OpenClaw does not rewrite Codex-native tool arguments); **editable Codex-native transcript history** (Codex owns canonical native thread history; OpenClaw owns only a mirror); **`tool_result_persist` for Codex-native tool records** (that hook transforms OpenClaw-owned transcript writes, not native records); **rich native compaction metadata** (OpenClaw requests native compaction but receives no stable kept/dropped list, token delta, or summary payload); **compaction intervention** (no plugin or context-engine veto/rewrite of native compaction); and **byte-for-byte model API request capture** (Codex core builds the final OpenAI API request internally).

## Native Permissions and MCP Elicitations

For `PermissionRequest`, OpenClaw only returns explicit allow or deny decisions when policy decides — a no-decision result is *not* an allow; Codex treats it as no hook decision and falls through to its own guardian or user approval path. Codex app-server approval modes omit this native hook by default; the relay behavior applies only when `permission_request` is explicitly included in `nativeHookRelay.events` or a compatibility runtime installs it. When an operator chooses `allow-always` for a Codex native permission request, OpenClaw remembers that exact provider/session/tool input/cwd fingerprint for a bounded session window; the remembered decision is intentionally exact-match only, so a changed command, arguments, tool payload, or cwd creates a fresh approval.

Codex MCP tool approval elicitations are routed through OpenClaw's plugin approval flow when Codex marks `_meta.codex_approval_kind` as `"mcp_tool_call"`. Codex `request_user_input` prompts are sent back to the originating chat, and the next queued follow-up message answers that native server request instead of being steered as extra context; other MCP elicitation requests fail closed.

## Queue Steering

Active-run queue steering maps onto Codex app-server `turn/steer`. With the default `messages.queue.mode: "steer"`, OpenClaw batches steer-mode chat messages for the configured quiet window and sends them as one `turn/steer` request in arrival order. Codex review and manual compaction turns can reject same-turn steering; OpenClaw then waits for the active run to finish before starting the prompt. Use `/queue followup` or `/queue collect` when messages should queue by default instead of steering.

## Codex Feedback Upload

When `/diagnostics [note]` is approved for a session using the native Codex harness, OpenClaw also calls Codex app-server `feedback/upload` for relevant Codex threads — the upload asks app-server to include logs for each listed thread and spawned Codex subthreads when available. The upload goes through Codex's normal feedback path to OpenAI servers; if Codex feedback is disabled in that app-server, the command returns the app-server error. The completed diagnostics reply lists the channels, OpenClaw session ids, Codex thread ids, and local `codex resume <thread-id>` commands for the threads that were sent. If you deny or ignore the approval, OpenClaw does not print those Codex ids and does not send Codex feedback, and the upload does not replace the local Gateway diagnostics export. Use `/codex diagnostics [note]` only when you specifically want the Codex feedback upload for the currently attached thread without the full Gateway diagnostics bundle.

## Compaction and Transcript Mirror

When the selected model uses the Codex harness, native thread compaction belongs to Codex app-server: OpenClaw does not run preflight compaction for Codex turns, does not replace Codex compaction with context-engine compaction, and does not fall back to OpenClaw or public OpenAI summarization when native Codex compaction cannot be started. OpenClaw keeps a transcript mirror for channel history, search, `/new`, `/reset`, and future model or harness switching. Explicit compaction requests such as `/compact` or a plugin-requested manual compact operation start native Codex compaction with `thread/compact/start`; OpenClaw returns after starting that native operation and does not wait for completion, impose a separate OpenClaw timeout, restart the shared Codex app-server, or record the operation as an OpenClaw-completed compaction.

When a context engine requests Codex thread-bootstrap projection, OpenClaw projects tool-call names and ids, input shapes, and redacted tool-result content into the fresh Codex thread, but does not copy raw tool-call argument values. The mirror includes the user prompt, final assistant text, and lightweight Codex reasoning or plan records when the app-server emits them. Today OpenClaw only records explicit native compaction start signals when it requests compaction, and does not expose a human-readable compaction summary or an auditable list of which entries Codex kept. Because Codex owns the canonical native thread, `tool_result_persist` does not currently rewrite Codex-native tool result records — it only applies when OpenClaw is writing an OpenClaw-owned session transcript tool result.

## Media and Delivery

OpenClaw continues to own media delivery and media provider selection. Image, video, music, PDF, TTS, and media understanding use matching provider/model settings such as `agents.defaults.imageGenerationModel`, `videoGenerationModel`, `pdfModel`, and `messages.tts`. Text, images, video, music, TTS, approvals, and messaging-tool output continue through the normal OpenClaw delivery path, and media generation does not require the legacy runtime. When Codex emits a native image-generation item with a `savedPath`, OpenClaw forwards that exact file through the normal reply-media path even when the Codex turn has no assistant text.

## Related Notes

**Terms**

- **[Agent Harness](../../term_dictionary/term_agent_harness.md)** — agent runtime; relevance: the OpenClaw-owns-vs-Codex-owns boundary is the core of this concept note.
- **[Agent Steering](../../term_dictionary/term_agent_steering.md)** — mid-run steering; relevance: queue steering maps onto Codex app-server `turn/steer`.
- **[Compaction](../../term_dictionary/term_compaction.md)** — transcript compaction; relevance: Codex owns native compaction; OpenClaw keeps only a transcript mirror.
- **[Heartbeat](../../term_dictionary/term_heartbeat.md)** — wake/heartbeat turns; relevance: heartbeat turns get `heartbeat_respond` and collaboration-mode instructions.
- **[Function Calling](../../term_dictionary/term_function_calling.md)** — model tool calls; relevance: native tool continuation owned by Codex; OpenClaw dynamic tools still execute.
- **[Tool Registry](../../term_dictionary/term_tool_registry.md)** — tool catalog; relevance: hook layers and supported native-tool block/observe surfaces.
- **[MCP](../../term_dictionary/term_mcp.md)** — MCP elicitations; relevance: Codex MCP tool approval elicitations route through OpenClaw's plugin approval flow.
- **[Message Queue](../../term_dictionary/term_message_queue.md)** — queued messages; relevance: queue steering batches steer-mode chat messages into one `turn/steer`.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway; relevance: subject — what OpenClaw still owns (channels, sessions, delivery, mirror) vs Codex.

**Docs**

- **[cc_computer_use](../claude_code/cc_computer_use.md)** — native tool/elicitation; relevance: analog for native MCP elicitation/approval handling.
- **[cc_hook_events_catalog](../claude_code/cc_hook_events_catalog.md)** — hook events catalog; relevance: analog for the three hook layers (`PreToolUse`/`PostToolUse`/`PermissionRequest`/`Stop`).
- **[cc_async_hooks](../claude_code/cc_async_hooks.md)** — async hook observations; relevance: analog for `after_tool_call` async observations that cannot block.
- **[hermes_acp_internals](../hermes_agent/hermes_acp_internals.md)** — ACP runtime internals; relevance: sibling native-runtime boundary contract (what the host owns vs the agent).
- **[hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md)** — Hermes Codex runtime tools; relevance: sibling Codex native-loop tool/permission boundary.
- **[cc_built_in_tools](../claude_code/cc_built_in_tools.md)** — built-in tool surface; relevance: native shell/patch/MCP tools Codex owns vs OpenClaw dynamic tools.
- **[oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md)** — harness setup; relevance: setup of the harness whose runtime contract this defines.
- **[oc_plugins_codex_harness_reference_runtime](oc_plugins_codex_harness_reference_runtime.md)** — runtime-execution reference; relevance: the config-field mechanics behind these contract points.
- **[oc_plugins_codex_harness_diagnostics](oc_plugins_codex_harness_diagnostics.md)** — diagnostics surface; relevance: runtime-boundary summary + feedback-upload pointer.
- **[oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md)** — native plugin management; relevance: native-plugin elicitations route through this runtime's approval path.

**Repos**

- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — agent runtime; relevance: the harness adapter implementing the ownership boundary.
- **[repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md)** — session/transcript; relevance: the transcript mirror OpenClaw keeps for channel history.
- **[repo_ecosystem_claude_code_provider](../../../areas/code_repos/repo_ecosystem_claude_code_provider.md)** — native coding-agent provider; relevance: sibling native-runtime ownership-boundary impl.

## References

- [OpenClaw Docs — Codex harness runtime](https://docs.openclaw.ai/plugins/codex-harness-runtime)
- [OpenClaw Docs — Codex harness](https://docs.openclaw.ai/plugins/codex-harness)
- [OpenClaw Docs — Codex harness reference](https://docs.openclaw.ai/plugins/codex-harness-reference)
- [OpenClaw Docs — Native Codex plugins](https://docs.openclaw.ai/plugins/codex-native-plugins)
- [OpenClaw Docs — Plugin hooks](https://docs.openclaw.ai/plugins/hooks)
- [OpenClaw Docs — Plugin permission requests](https://docs.openclaw.ai/plugins/plugin-permission-requests)
- [OpenClaw Docs — Steering queue](https://docs.openclaw.ai/concepts/queue-steering)
- [OpenClaw Docs — Diagnostics export](https://docs.openclaw.ai/gateway/diagnostics)

**Source**: OpenClaw documentation — `plugins/codex-harness-runtime` (mirror `inbox/openclaw_docs/plugins/codex-harness-runtime.md`)
**Last Updated**: 2026-06-22
**Status**: Active
