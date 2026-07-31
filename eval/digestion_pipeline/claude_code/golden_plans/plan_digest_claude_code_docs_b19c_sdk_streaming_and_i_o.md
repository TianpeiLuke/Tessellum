---
title: Sub-Plan B19C — Claude Code Docs: SDK Streaming & I/O
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["agent-sdk/streaming-output", "agent-sdk/streaming-vs-single-mode", "agent-sdk/structured-outputs", "agent-sdk/user-input"]
---

# Sub-Plan B19C: SDK Streaming & I/O

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted pilot
> [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 4 Agent SDK pages that cover how data flows in and out of an SDK agent: **output streaming**
(receiving tokens/tool-call deltas in real time), the **two input modes** (persistent streaming-input vs
one-shot single-message), **structured outputs** (validated JSON via JSON Schema / Zod / Pydantic), and
**approvals & user input** (the `canUseTool` callback, tool-approval responses, and `AskUserQuestion`
clarifying questions). P2 (Phase B) — these features build on the SDK core (B19A) and reference
permissions/hooks (B20C), so they run after the P1 cores. SDK vocabulary terms route per Pattern B (see
Undigested Terms Plan), not re-digested as `term_dictionary` notes.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 8,804 measured words. **Planned: 9 notes.**

## Content Strategy

- **Prioritize**: the I/O mechanics every SDK app needs — partial-message streaming wiring, the
  streaming-vs-single-mode decision, the structured-output schema/validation contract, and the
  `canUseTool` approval flow (the largest, most procedural page).
- **Group**: keep `streaming-output` as a concept note (the StreamEvent model) + a procedure note (the
  three streaming recipes); keep `streaming-vs-single-mode` as one decision/argument note; split
  `structured-outputs` (1.9Kw) into a concept note (what/why + config) and a procedure note (schema
  definition + error handling); split the large `user-input` (4.2Kw) into approval-flow concept, approval
  procedure, and clarifying-questions procedure.
- **Skip / link-out (own other sub-plans)**: permission rules/modes & `plan` mode → B20C
  (`agent-sdk/permissions`); hooks (`PreToolUse`, `PermissionRequest`, `defer`) → B20C
  (`agent-sdk/hooks`); custom tools → B20A (`agent-sdk/custom-tools`); the agent-loop result subtypes →
  B19A (`agent-sdk/agent-loop`); model fallback → B03B (`model-config`); CLI streaming → B11 (`headless`);
  raw Claude API streaming event types → external API docs. Referenced via links, never duplicated.
- **Glossary / SDK terms**: not re-digested into `cc_` term notes — terms route to existing term notes /
  their home sub-plan (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/agent-sdk/` (verbatim mirror of
`code.claude.com/docs/en/agent-sdk/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| streaming-output | /agent-sdk/streaming-output | 1,650 | 8 | 8 | 0 | concept + procedure |
| streaming-vs-single-mode | /agent-sdk/streaming-vs-single-mode | 1,025 | 3 | 4 | 6 | argument |
| structured-outputs | /agent-sdk/structured-outputs | 1,921 | 9 | 7 | 0 | concept + procedure |
| user-input | /agent-sdk/user-input | 4,208 | 12 | 5 | 5 | concept + procedure |

> **H2 lists (document order):**
> - **streaming-output**: Enable streaming output · StreamEvent reference · Message flow · Stream text responses · Stream tool calls · Build a streaming UI · Known limitations · Next steps
> - **streaming-vs-single-mode**: Overview · Streaming Input Mode (H3 How It Works, Benefits, Implementation Example) · Single Message Input (H3 When to Use Single Message Input, Limitations, Implementation Example)
> - **structured-outputs**: Why structured outputs? · Quick start · Type-safe schemas with Zod and Pydantic · Output format configuration · Example: TODO tracking agent · Error handling · Related resources
> - **user-input**: Detect when Claude needs input · Handle tool approval requests (H3 Respond to tool requests) · Handle clarifying questions (H3 Question format incl. Option previews, Response format incl. Support free-text input, Complete example) · Limitations · Other ways to get user input (H3 Streaming input, Custom tools)

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **9 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`. Code blocks counted as Python+TypeScript
pairs kept verbatim; each note caps at ≤6.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_sdk_streaming_output.md` | concept | streaming-output: Enable streaming output, StreamEvent reference, Message flow, Known limitations | 600 | Partial-message streaming: `include_partial_messages`/`includePartialMessages` yields `StreamEvent`/`SDKPartialAssistantMessage` wrapping raw Claude API events; StreamEvent field schema; the event-type table and message-flow ordering; structured-output deltas not streamed (→ note 6). |
| 2 | `cc_sdk_stream_text_and_tool_calls.md` | procedure | streaming-output: Stream text responses, Stream tool calls, Build a streaming UI | 600 | Three recipes — accumulate `text_delta` chunks; track tool starts/`input_json_delta`/stops; combined streaming-UI flag pattern. ≤6 code blocks (3 PY+TS pairs). |
| 3 | `cc_sdk_input_modes.md` | argument | streaming-vs-single-mode: Overview, Streaming Input Mode (How It Works, Benefits), Single Message Input (When to Use, Limitations) | 600 | Decision guide: persistent streaming-input (default/recommended — images, queued msgs, interruption, multi-turn) vs one-shot single-message (stateless/lambda, `continue`/`continue_conversation`); benefits & limitations tables; when to pick which. |
| 4 | `cc_sdk_streaming_input_example.md` | procedure | streaming-vs-single-mode: Streaming Input Mode → Implementation Example; Single Message Input → Implementation Example | 450 | `ClaudeSDKClient` + async-generator message stream (text + base64 image); single-message `query()` one-shot + session continuation; the TS/Python generator-exception gotchas. |
| 5 | `cc_sdk_structured_outputs.md` | concept | structured-outputs: Why structured outputs?, Quick start, Output format configuration | 550 | What structured outputs are (validated JSON matching a JSON Schema, re-prompted on mismatch); free-form vs typed contrast; `outputFormat`/`output_format` config and `structured_output` result field; supported JSON Schema features. |
| 6 | `cc_sdk_structured_output_schemas.md` | procedure | structured-outputs: Type-safe schemas with Zod and Pydantic, Example: TODO tracking agent, Error handling | 600 | Type-safe schema definition (Zod `z.toJSONSchema`, Pydantic `.model_json_schema()`) + `safeParse`/`model_validate`; multi-step tool-use example; error handling (`error_max_structured_output_retries`, model-fallback retraction) + tips. ≤6 code blocks. |
| 7 | `cc_sdk_user_input_overview.md` | concept | user-input: intro, Detect when Claude needs input | 450 | The `canUseTool` callback model: two trigger cases (tool approval, `AskUserQuestion`); pauses execution until callback returns; can stay pending indefinitely / `defer`; hooks fire before `canUseTool`; arguments. |
| 8 | `cc_sdk_tool_approval_handling.md` | procedure | user-input: Handle tool approval requests, Respond to tool requests | 600 | Allow/Deny response types + argument table; the six response patterns (approve, approve-with-changes, approve-and-remember via `updatedPermissions`, reject, suggest-alternative, redirect); Python streaming-mode + dummy `PreToolUse` hook requirement. ≤6 code blocks. |
| 9 | `cc_sdk_clarifying_questions.md` | procedure | user-input: Handle clarifying questions (Question format, Response format, Complete example), Limitations, Other ways to get user input | 600 | `AskUserQuestion` flow: include in `tools`, parse `questions` array, collect answers, return `answers` map; question/response field tables; option previews (TS); free-text input; limits (no subagents, 1-4 Q × 2-4 opts); other input avenues (streaming input, custom tools). ≤6 code blocks. |

**Estimate: 9 notes** — concept ×3 (notes 1, 5, 7), procedure ×5 (notes 2, 4, 6, 8, 9), argument ×1 (note 3). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (8,804 words). New `cc_` notes: 9. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~5,050 (avg ~560/note). Code blocks: code-heavy source (32 code blocks total
  across pages); each note keeps only the load-bearing PY+TS pairs (≤6/note).
- **Building Block Distribution**: concept ×3 (notes 1, 5, 7) · procedure ×5 (notes 2, 4, 6, 8, 9) ·
  argument ×1 (note 3). No model/empirical_observation in this sub-plan.
- Cross-refs: **≥6 relevancy-selected term notes per note** (18 distinct `term_dictionary/` terms across

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.
> All paths verified via `ls src/.../term_dictionary/<slug>.md`.

### 1. `cc_sdk_streaming_output` (6 term notes)
- [Stream Processing](../../term_dictionary/term_stream_processing.md) — what it is: processing data incrementally as it arrives rather than in complete batches; relevance: partial-message streaming yields raw Claude API events incrementally so the app consumes deltas as they arrive instead of waiting for a complete `AssistantMessage` — the streaming-vs-batch distinction this note's whole design rests on.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what it is: the mechanism by which a model emits structured tool invocations the runtime executes; relevance: this note documents `tool_use` content-block deltas (`input_json_delta`) streaming a tool call's JSON input chunk by chunk, the streamed form of the tool-use mechanism.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what it is: Anthropic's agentic coding tool/harness; relevance: the Agent SDK whose `include_partial_messages` option and `StreamEvent`/`SDKPartialAssistantMessage` types this note documents is the programmatic interface to the Claude Code agent runtime.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what it is: the runtime that wraps an LLM with tools, context, and execution; relevance: the SDK harness is what wraps each raw Claude API stream event into a `StreamEvent` object (adding `uuid`, `session_id`, `parent_tool_use_id`) before yielding it to the caller.
- [Context Window](../../term_dictionary/term_context_window.md) — what it is: the bounded token buffer holding the model's working state; relevance: the message-flow ordering this note documents (`message_start` → content blocks → `message_stop` → `AssistantMessage` → `ResultMessage`) is the surface form of the turns accumulating in the agent's context window across the loop.
- [Structured Output](../../term_dictionary/term_structured_output.md) — what it is: validated typed data returned from a model instead of free text; relevance: the note's Known-limitations section states the structured-output JSON appears only in the final `ResultMessage.structured_output`, not as streaming deltas — the explicit boundary between streaming and structured output that this note draws.

### 2. `cc_sdk_stream_text_and_tool_calls` (6 term notes)
- [Stream Processing](../../term_dictionary/term_stream_processing.md) — what it is: incremental consumption of a data stream as elements arrive; relevance: all three recipes in this note are stream-processing handlers — accumulate `text_delta` chunks, accumulate `input_json_delta` tool input, and gate output on an `in_tool` flag — the core consume-as-you-go pattern.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what it is: structured tool invocation by the model; relevance: the Stream-tool-calls recipe tracks `content_block_start` (tool begins), `input_json_delta` (input chunks), and `content_block_stop` (complete) — the lifecycle of one streamed tool-use call.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what it is: Anthropic's agentic coding tool/harness; relevance: these recipes are written against the Claude Code Agent SDK's `query()` iterator and `StreamEvent` type, so the Claude Code term anchors the runtime the procedure targets.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what it is: the LLM runtime wrapper; relevance: the streaming-UI recipe shows status indicators (`[Using Read...]`) while the harness executes tools, surfacing the harness's tool-execution phase to the end user.
- [Context Window](../../term_dictionary/term_context_window.md) — what it is: the model's bounded working buffer; relevance: text and tool-call deltas the recipes accumulate are the incremental contents of each assistant turn being added to the running context window during a multi-step task.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what it is: agents that plan, edit code, run commands, and verify across multiple steps; relevance: the streaming-UI recipe is explicitly for "multi-step agent tasks," surfacing progress as an autonomous coding agent chains tool calls (Read/Bash/Grep) to find TODOs.

### 3. `cc_sdk_input_modes` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what it is: Anthropic's agentic coding tool/harness; relevance: this note compares the two input modes of the Claude Code Agent SDK (`query()` and `ClaudeSDKClient`), so the Claude Code term anchors the runtime whose I/O design is being chosen.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what it is: the long-lived LLM runtime; relevance: streaming input mode lets the agent "operate as a long lived process" that takes input, handles interruptions, surfaces permission requests, and manages sessions — the persistent-harness operating mode this note recommends.
- [Stream Processing](../../term_dictionary/term_stream_processing.md) — what it is: incremental data handling; relevance: streaming input mode is built around an async-generator that feeds messages and streams partial responses back — the bidirectional streaming model the note contrasts against one-shot batch queries.
- [Multimodal](../../term_dictionary/term_multimodal.md) — what it is: handling inputs across modalities like text and images together; relevance: a headline benefit of streaming input mode (and a stated limitation of single-message mode) is direct image attachments in messages, the multimodal capability that gates the mode decision.
- [Human-in-the-Loop (HITL)](../../term_dictionary/term_hitl.md) — what it is: keeping a human in the agent's decision/approval path; relevance: streaming input mode enables real-time interruption and surfaces permission requests mid-task, the interactive human-in-the-loop capabilities single-message mode cannot offer.
- [Idempotency](../../term_dictionary/term_idempotency.md) — what it is: an operation safely repeatable with the same effect; relevance: the note recommends single-message mode for stateless environments such as lambda functions, where each one-shot `query()` (with `continue`/`continue_conversation` resuming) maps to the stateless, independently-retriable execution this term describes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what it is: agents that act over many turns; relevance: the note frames streaming mode for "natural multi-turn conversations" and long-running interactive tasks vs single-message for one-shot responses — the autonomous-agent session-length trade-off behind the mode choice.

### 4. `cc_sdk_streaming_input_example` (6 term notes)
- [Stream Processing](../../term_dictionary/term_stream_processing.md) — what it is: incremental data handling via streams; relevance: the implementation uses an `AsyncGenerator`/`message_generator()` to yield messages and a `receive_response()` loop to consume streamed assistant blocks — the producer/consumer streaming pattern this term names.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what it is: Anthropic's agentic coding tool/harness; relevance: the example is built on the Claude Code SDK's `ClaudeSDKClient` (streaming) and `query()` (single-message) APIs, so the term grounds the runtime the procedure drives.
- [Multimodal](../../term_dictionary/term_multimodal.md) — what it is: combined text+image input; relevance: the streaming example reads a PNG, base64-encodes it, and yields a follow-up message with both a `text` and an `image` content block — the concrete multimodal-message construction the procedure demonstrates.
- [Multi-Modal](../../term_dictionary/term_multi_modal.md) — what it is: models/inputs spanning multiple data modalities; relevance: the example's image+text message payload exercises the multi-modal content-block format (`type: image`, `source: base64`) that the SDK accepts only in streaming input mode.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what it is: the long-lived LLM runtime; relevance: `ClaudeSDKClient` keeps the session alive across yielded messages ("Session stays alive"), the persistent-harness lifecycle the streaming example manages with `async with`.
- [Idempotency](../../term_dictionary/term_idempotency.md) — what it is: safely repeatable operations; relevance: the single-message half of the example uses `continue`/`continue_conversation` to resume a one-shot stateless `query()`, the independently-invocable execution shape this term describes for stateless environments.

### 5. `cc_sdk_structured_outputs` (7 term notes)
- [Structured Output](../../term_dictionary/term_structured_output.md) — what it is: validated typed data returned from a model instead of free text; relevance: this note IS the SDK's structured-output feature — defining a shape, getting validated JSON in `structured_output`, re-prompting on mismatch — making this term the note's canonical definitional anchor.
- [Data Contract](../../term_dictionary/term_data_contract.md) — what it is: an agreed, enforced schema between a producer and consumer of data; relevance: the JSON Schema you pass to `outputFormat`/`output_format` is exactly a data contract — the SDK validates the agent's output against it and re-prompts/errors on violation, enforcing producer-consumer agreement.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what it is: structured model invocations the runtime executes; relevance: the note stresses the agent can use any tools it needs (the tool-use loop) and *still* return schema-validated JSON at the end — structured output sits on top of the function-calling agent loop, not in place of it.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what it is: Anthropic's agentic coding tool/harness; relevance: the `outputFormat`/`output_format` option and `ResultMessage.structured_output` field this note documents are Claude Code Agent SDK surfaces, so the term anchors the runtime.
- [Uncertainty-Aware Generation](../../term_dictionary/term_uncertainty_aware_generation.md) — what it is: generation that accounts for and signals when the model may be wrong; relevance: structured outputs replace ambiguous free-form text with a validated, typed contract and surface failure explicitly (error subtype) instead of silently emitting malformed data — the reliability discipline this term promotes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what it is: agents that act autonomously over multiple steps; relevance: the note's core value prop is "typed data after multi-turn tool use" — an autonomous coding agent does the work, then hands back machine-usable structured data for downstream app logic.
- [Stream Processing](../../term_dictionary/term_stream_processing.md) — what it is: incremental stream consumption; relevance: the note draws the boundary that structured output is *not* streamed — it appears only in the final result, distinguishing it from the partial-message stream-processing path (note 1).

### 6. `cc_sdk_structured_output_schemas` (7 term notes)
- [Structured Output](../../term_dictionary/term_structured_output.md) — what it is: validated typed model output; relevance: this procedure is how you produce structured output in practice — define a Zod/Pydantic schema, convert it to JSON Schema, validate the result — so the term is the feature this note operationalizes.
- [Data Contract](../../term_dictionary/term_data_contract.md) — what it is: an enforced producer-consumer schema; relevance: Zod `z.object` and Pydantic `BaseModel` definitions are the typed data contracts this note generates JSON Schema from and validates the agent's output against with `safeParse`/`model_validate`.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what it is: structured tool invocation; relevance: the TODO-tracking example has the agent autonomously call Grep and Bash (git blame) tools, then combine results into one schema-validated object — structured output layered on a function-calling tool-use run.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what it is: agents that plan and act across many tool calls; relevance: the example agent "autonomously decides which tools to use" to find and attribute TODOs, the multi-step autonomous behavior the typed schema captures the result of.
- [Uncertainty-Aware Generation](../../term_dictionary/term_uncertainty_aware_generation.md) — what it is: generation that flags potential failure; relevance: the Error-handling section turns schema-validation failure and model-fallback retraction into an explicit `error_max_structured_output_retries` subtype to branch on, the fail-loud reliability practice this term names.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what it is: Anthropic's agentic coding tool/harness; relevance: the schema procedure and error subtypes are Claude Code Agent SDK behavior, so the term grounds the runtime the recipe targets.
- [ReAct](../../term_dictionary/term_react.md) — what it is: the interleaved reason-act-observe agent pattern; relevance: the agent in the example reasons about which tools to call, acts (Grep/Bash), observes results, and only then emits the validated schema — the ReAct cycle the structured-output procedure sits at the end of.

### 7. `cc_sdk_user_input_overview` (7 term notes)
- [Human-in-the-Loop (HITL)](../../term_dictionary/term_hitl.md) — what it is: keeping a human in the agent's decision/approval loop; relevance: this note IS the SDK's HITL surface — Claude pauses and asks the user for permission to use a tool or for clarification, and the app returns the human's decision; the term is the note's defining concept.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what it is: progressively granting an agent more autonomy as trust grows; relevance: the `canUseTool` callback fires only for tools *not* auto-approved by permission rules/modes — the human-approval rung in the graduated-trust ladder the note sits within.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what it is: structured tool invocations; relevance: the callback receives the `tool_name` and `input` of the tool Claude wants to call and gates whether that tool-use executes — an approval hook on the function-calling mechanism.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what it is: Anthropic's agentic coding tool/harness; relevance: `canUseTool`, `AskUserQuestion`, and the `defer` decision are Claude Code Agent SDK features, so the term anchors the runtime whose input model this note describes.
- [Deny-First](../../term_dictionary/term_deny_first.md) — what it is: a security posture that blocks by default until explicitly allowed; relevance: the callback pauses execution and waits indefinitely for an explicit allow/deny before any non-auto-approved tool runs — the block-until-approved default this term embodies.
- [Subagent](../../term_dictionary/term_subagent.md) — what it is: a child agent spawned with isolated context; relevance: the note's companion (note 9) flags that `AskUserQuestion` is unavailable in subagents spawned via the Agent tool, a boundary the input model defines against the subagent feature.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what it is: agents that act over many steps; relevance: the note explains Claude "sometimes needs to check in" mid-task (permission to delete files, which database to use) — the human-checkpoint pauses that punctuate an otherwise-autonomous coding agent's run.

### 8. `cc_sdk_tool_approval_handling` (7 term notes)
- [Human-in-the-Loop (HITL)](../../term_dictionary/term_hitl.md) — what it is: human approval in the agent loop; relevance: this procedure implements the HITL approval gate — display the tool request, prompt the user, and return allow/deny — the human-decision step the SDK pauses for.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what it is: progressive autonomy granting; relevance: the "approve and remember" response echoes a suggested `PermissionUpdate` (`localSettings`) back so matching calls skip the prompt next time — the mechanism by which a user graduates a tool to auto-approved.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what it is: structured tool invocation the runtime executes; relevance: every response pattern (approve, approve-with-changes via `updatedInput`, deny) gates or rewrites a specific tool-use call's parameters before execution, operating directly on the function-calling payload.
- [Deny-First](../../term_dictionary/term_deny_first.md) — what it is: block-by-default security posture; relevance: the example treats any input other than `y` as a denial and `PermissionResultDeny` blocks the tool — the deny-by-default stance the approval handler enforces.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — what it is: confining execution to a restricted environment; relevance: the "approve with changes" pattern rewrites a Bash command's path (`/tmp` → `/tmp/sandbox`) before allowing it — scoping the tool's effect into a sandbox, a concrete use of `updatedInput`.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what it is: Anthropic's agentic coding tool/harness; relevance: `PermissionResultAllow`/`PermissionResultDeny`, `updatedInput`, `updatedPermissions`, and the streaming-mode + dummy `PreToolUse` hook requirement are Claude Code Agent SDK specifics this procedure depends on.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what it is: agents that plan, edit code, and run commands across many steps; relevance: the "suggest alternative" and "redirect entirely" responses block a tool but feed guidance back so the autonomous coding agent course-corrects (e.g. archive instead of `rm`) rather than halting — steering the agent's multi-step run via the denial message.

### 9. `cc_sdk_clarifying_questions` (7 term notes)
- [Human-in-the-Loop (HITL)](../../term_dictionary/term_hitl.md) — what it is: human input in the agent loop; relevance: `AskUserQuestion` is the SDK's structured clarification channel — Claude generates multiple-choice questions, the app surfaces them, and the user's selections return to Claude — a HITL elicitation step this procedure implements.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what it is: Anthropic's agentic coding tool/harness; relevance: the `AskUserQuestion` tool, the `questions`/`answers`/`response` schema, and `toolConfig.askUserQuestion.previewFormat` are Claude Code Agent SDK features this note operationalizes.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what it is: structured tool invocation; relevance: clarifying questions arrive *as* a tool call (`AskUserQuestion`) routed through `canUseTool`, and must be included in the `tools` array — the question flow is itself a function-calling interaction.
- [Subagent](../../term_dictionary/term_subagent.md) — what it is: a child agent with isolated context; relevance: the Limitations section states `AskUserQuestion` is not available in subagents spawned via the Agent tool — a capability boundary between the main agent and subagents this note documents.
- [Multimodal](../../term_dictionary/term_multimodal.md) — what it is: presentation across modalities (text, visual); relevance: TypeScript option previews (`previewFormat: "markdown"|"html"`) attach a visual mockup to each choice so the app can render a styled preview alongside the label — a multimodal presentation of the question options.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what it is: progressive autonomy; relevance: the note ties clarifying questions to `plan` mode, where Claude gathers requirements before acting — the low-autonomy, ask-first rung of the trust ladder this question flow supports.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what it is: agents that act over many steps; relevance: clarifying questions let an autonomous coding agent resolve ambiguity (tech-stack choices, output format) mid-task instead of guessing, keeping its multi-step run aligned with user intent.

## Section Coverage Map

```
streaming-output.md
├── Enable streaming output ─────────────── → note 1 (cc_sdk_streaming_output)
├── StreamEvent reference (event table) ─── → note 1
├── Message flow (ordering block) ───────── → note 1
├── Stream text responses ───────────────── → note 2 (cc_sdk_stream_text_and_tool_calls)
├── Stream tool calls ───────────────────── → note 2
├── Build a streaming UI ────────────────── → note 2
├── Known limitations (structured output) ─ → note 1 (→ note 5/6)
└── Next steps (cards) ──────────────────── → notes 1/2 (links: input modes → note 3; structured → note 5; permissions → B20C)
streaming-vs-single-mode.md
├── Overview (two modes) ────────────────── → note 3 (cc_sdk_input_modes)
├── Streaming Input Mode ────────────────── → note 3
│   ├── How It Works (mermaid) ──────────── → note 3
│   ├── Benefits (cards) ─────────────────── → note 3
│   └── Implementation Example ──────────── → note 4 (cc_sdk_streaming_input_example)
└── Single Message Input ────────────────── → note 3
    ├── When to Use / Limitations ───────── → note 3
    └── Implementation Example ──────────── → note 4 (→ B19A agent-loop result subtypes for error_max_turns)
structured-outputs.md
├── Why structured outputs? ─────────────── → note 5 (cc_sdk_structured_outputs)
├── Quick start ─────────────────────────── → note 5
├── Type-safe schemas with Zod/Pydantic ─── → note 6 (cc_sdk_structured_output_schemas)
├── Output format configuration ─────────── → note 5
├── Example: TODO tracking agent ────────── → note 6
├── Error handling ──────────────────────── → note 6 (→ B03B model-config for model fallback)
└── Related resources (links) ───────────── → notes 5/6 (links: custom tools → B20A; external JSON Schema/API)
user-input.md
├── intro (two situations, defer) ───────── → note 7 (cc_sdk_user_input_overview) (→ B20C hooks defer/PermissionRequest)
├── Detect when Claude needs input ──────── → note 7
├── Handle tool approval requests ───────── → note 8 (cc_sdk_tool_approval_handling)
│   └── Respond to tool requests (6 tabs) ─ → note 8
├── Handle clarifying questions ─────────── → note 9 (cc_sdk_clarifying_questions)
│   ├── Question format (+ Option previews) → note 9
│   ├── Response format (+ free-text) ────── → note 9
│   └── Complete example ─────────────────── → note 9
├── Limitations ─────────────────────────── → note 9
└── Other ways to get user input ────────── → note 9 (→ B20A custom-tools; note 3 streaming input)
```
No orphaned sections. Sections owned by other sub-plans (permissions/hooks → B20C, custom tools → B20A,
agent-loop result subtypes → B19A, model fallback → B03B, CLI streaming → B11) are LINKED, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| streaming-output (1.65Kw, 8 H2, 8 code) | notes 1 (concept) + 2 (procedure) | StreamEvent model/event-table/message-flow (concept) vs the three streaming recipes (procedure) differ in BB; splitting also keeps each note ≤6 code blocks. |
| streaming-vs-single-mode (1.0Kw) | notes 3 (argument) + 4 (procedure) | mode-decision/benefits/limitations (argument) vs the two implementation examples (procedure) differ in BB; one BB per note. |
| structured-outputs (1.9Kw) | notes 5 (concept) + 6 (procedure) | what/why + config (concept) vs schema-definition + multi-step example + error handling (procedure); concept note stays small, procedure note keeps code ≤6. |
| user-input (4.2Kw >2500, 12 code) | notes 7 (concept) + 8 (procedure) + 9 (procedure) | exceeds the word cap; callback model (concept) vs tool-approval handling (procedure) vs clarifying-questions handling (procedure) are distinct BBs/topics, and three notes keep each ≤6 code blocks. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_sdk_streaming_output | concept | 600 | 2 | ✅ |
| 2 | cc_sdk_stream_text_and_tool_calls | procedure | 600 | 6 | ✅ (at cap; PY+TS pairs for the 3 recipes) |
| 3 | cc_sdk_input_modes | argument | 600 | 0 | ✅ |
| 4 | cc_sdk_streaming_input_example | procedure | 450 | 4 | ✅ |
| 5 | cc_sdk_structured_outputs | concept | 550 | 2 | ✅ |
| 6 | cc_sdk_structured_output_schemas | procedure | 600 | 6 | ✅ (at cap; Zod/Pydantic + example + error pairs) |
| 7 | cc_sdk_user_input_overview | concept | 450 | 2 | ✅ |
| 8 | cc_sdk_tool_approval_handling | procedure | 600 | 6 | ✅ (at cap; allow/deny + selected response-pattern pairs) |
| 9 | cc_sdk_clarifying_questions | procedure | 600 | 6 | ✅ (at cap; question/response JSON + complete-example pairs) |

No note exceeds the caps. The source is code-heavy, so the four procedure notes that sit at 6 code blocks
were sized precisely to stay within the ≤6 limit (load-bearing PY+TS pairs only; redundant duplicate
snippets dropped, referencing the canonical one). No over-compression — every H2/H3 maps to a note or an
explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_sdk_streaming_output cc_sdk_stream_text_and_tool_calls cc_sdk_input_modes cc_sdk_streaming_input_example cc_sdk_structured_outputs cc_sdk_structured_output_schemas cc_sdk_user_input_overview cc_sdk_tool_approval_handling cc_sdk_clarifying_questions"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($lines L / $words w / $cb code)"
done
python3 scripts/check_yaml_frontmatter.py --path "$CC"
# G5 ghost: verify every internal .md link target exists in the DB
for n in $NOTES; do f="$CC/$n.md"
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/.*\(([^)]+)\)/\1/' | while read l; do
    r=$(cd "$(dirname "$f")" && realpath -q -m "$l"); id=${r#*/the vault/}
    sqlite3 "$(python3 -c 'import sys;sys.path.insert(0,"scripts");from config import DB_PATH_STR;print(DB_PATH_STR)')" \
      "SELECT 1 FROM notes WHERE note_id='$id'" | grep -q 1 || echo "GHOST $n -> $l"
  done; done
```

## Per-Phase Validation Gate (G1–G8) — inherited from master

Single phase (9 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination; code verbatim | diff vs `inbox/claude_code_docs/agent-sdk/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 9 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 9 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (in-degree ≥1) | DB confirms in-degree ≥1 for every new note before commit (anti-island) | sqlite3 in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets
`0_entry_points/entry_claude_code_docs.md`; this sub-plan **contributes its 9 rows** under an "Agent SDK —
Streaming & I/O" cluster + increments the BB-distribution counts (concept ×3, procedure ×5, argument ×1).
The entry-point back-link is added to each note at finalization (G7/G8).

## Undigested Terms Plan (Step 4e)

b19c creates **no new `term_dictionary` notes** — SDK I/O vocabulary is covered by a b19c `cc_` concept
note, an existing substantive term note (link), or its home sub-plan (Pattern B). **Dedup performed across
`term_dictionary/` AND `resources/documentation/`** (no existing `cc_*` SDK I/O note, no streaming/
single-mode/`canUseTool`/`AskUserQuestion` term note — confirmed by filename grep + BM25/dense).

| SDK / page term | Disposition |
|---|---|
| Partial message streaming / StreamEvent | note 1 `cc_sdk_streaming_output` (doc concept) |
| `text_delta` / `input_json_delta` / content-block events | notes 1–2 (doc concept/procedure) |
| Streaming input mode / Single message input | note 3 `cc_sdk_input_modes` (doc argument) |
| `ClaudeSDKClient` / async-generator messages | note 4 (doc procedure) |
| Structured output / `output_format` / `structured_output` | note 5 `cc_sdk_structured_outputs`; link `term_structured_output` (exists) + `term_data_contract` (exists) |
| JSON Schema / Zod / Pydantic | note 6 (doc procedure) — library-specific, not a vault term; no capture |
| `canUseTool` / approval callback | notes 7–8 (doc concept/procedure); link `term_hitl`, `term_graduated_trust`, `term_deny_first` (exist) |
| `AskUserQuestion` / clarifying questions | note 9 (doc procedure) |
| Streaming (general) / Stream processing | link `term_stream_processing` (exists) |
| Image / multimodal input | link `term_multimodal` / `term_multi_modal` (exist) |
| Function calling / tool use | link `term_function_calling` (exists) |
| Permission rule/mode, plan mode, hooks (`PreToolUse`/`PermissionRequest`/`defer`), custom tools, model fallback, result subtypes | owned by home sub-plan (B20C/B20A/B19A/B03B) — captured/linked there, not B19C |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/captions/
code-comments for newly-surfaced terms. Candidates surfaced — **"async generator," "base64 image
encoding," "JSON Schema," "Zod/Pydantic"** — but each is either (a) a general programming/library concept
not warranting a vault term note, or (b) covered by an existing term (`term_stream_processing`,
`term_multimodal`, `term_structured_output`, `term_data_contract`). **0 new B19C `term_dictionary`
captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B19C authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the SDK I/O concepts duplicate existing notes?)
was performed: `term_structured_output`, `term_data_contract`, `term_stream_processing`, `term_hitl`,
`term_graduated_trust`, `term_deny_first`, `term_function_calling`, `term_multimodal`, `term_multi_modal`,
`term_claude_code`, `term_agent_harness` all exist → linked, not recreated. No `cc_*` doc note duplicates
an existing term note (the P0 failure the dedup policy guards against).

## Term-Note Authoring Requirements

**N/A for b19c** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim from the source (PY+TS pairs); keep only the load-bearing snippets so each note
  stays ≤6 code blocks. One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8).
Each new note receives ≥1 inbound link from a note **outside** `claude_code/`.

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_structured_output.md` | notes 5, 6 | structured-output term → SDK structured-output concept + schema procedure |
| `term_dictionary/term_data_contract.md` | note 5 | data-contract term → JSON-Schema-as-contract structured output |
| `term_dictionary/term_stream_processing.md` | notes 1, 2 | stream-processing term → SDK partial-message streaming + recipes |
| `term_dictionary/term_hitl.md` | notes 7, 8, 9 | HITL term → SDK approval/clarifying-question input model |
| `term_dictionary/term_graduated_trust.md` | note 8 | graduated-trust term → approve-and-remember permission persistence |
| `term_dictionary/term_multimodal.md` | note 4 | multimodal term → streaming-input image-attachment example |
| `term_dictionary/term_claude_code.md` | notes 1, 3, 5, 7 | Claude Code term → SDK streaming/input-modes/structured/input docs |
| sibling `cc_sdk_*` (B19A core, e.g. `cc_sdk_agent_loop`) | notes 1, 3, 7 | SDK core → streaming/input-modes/input I/O (added when B19A lands) |

## Follow-up Recommendations

- After the 9 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; verify DB
  in-degree ≥1 for each note (G7/G8); queue the 9 rows for `entry_claude_code_docs.md`;
  `/tessellum-check-broken-links`.
- When sibling SDK sub-plans (B19A core, B20A custom tools, B20C hooks/permissions) land, add the
  forward/back cross-links flagged as link-outs in the Section Coverage Map.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B19C, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read in full from `inbox/claude_code_docs/agent-sdk/`;
  measured words (streaming-output 1,650 · streaming-vs-single-mode 1,025 · structured-outputs 1,921 ·
  user-input 4,208 = 8,804) match the master's 8,804 figure. user-input (4,208w >2,500) forced the
  3-way split into notes 7/8/9; the other three pages split concept-vs-procedure/argument to keep each
  note single-BB and ≤6 code blocks.
- **Notes**: 9 (concept 3, procedure 5, argument 1) — exactly the master estimate. Splits documented in
  Split Decisions.
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard
  — 6–7 term notes per note (18 distinct `term_dictionary/` terms), each with a per-link what-it-is +
  confirmed correct via `os.path.normpath`. Sibling `cc_sdk_*` forward-refs kept as prose/inlink rows
  (B19A not yet built).
- **Term searches run**: BM25 + dense for each note's concepts (streaming/partial-messages, structured
  positives (e.g. `term_kappa_architecture`, `term_change_data_capture`, `term_clip`) discarded; only
  genuinely relevant terms kept.
- **Step 2d new-term scan**: candidates surfaced ("async generator," "base64 image," "JSON Schema,"
  "Zod/Pydantic") → all general/library concepts or covered by existing terms; **0 new B19C term captures**.
- **Dedup**: filename grep + BM25/dense across `term_dictionary/` AND `documentation/` — no existing
  `cc_*` SDK I/O note, no streaming/single-mode/`canUseTool`/`AskUserQuestion` term note. No `cc_` doc
  note duplicates an existing term note.
- **Sections present**: all B01A sections reproduced in order (Scope, Content Strategy, Source Pages,
  Planned Notes, Summary Statistics & BB Distribution, Per-Note Related Notes Mapping, Section Coverage
  Map, Split Decisions, Density Re-Assessment, Validation Scripts, G1–G8 gate table, Entry Point Decision,
  Undigested Terms Plan, Term-Note Authoring Requirements, Pacing Rules, Inlinks, Follow-up, Pipeline
  Status, Augmentation Report, Review Sign-Off).
- **28-item checklist**: PASS (term-note items N/A — B19C authors no terms; entry-point + undigested-terms
  inherited from master).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | ALL gates per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase) incl. G7/G8 Discoverability (in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (>30 notes → CREATE required); B19C contributes 9 rows under "Agent SDK — Streaming & I/O." |
| CP4 | Plan size ≤30 / split | ✅ PASS | 9 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order + `## Overview` / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer inherited verbatim from the master Format Definition. |
| CP6 | Borderline density → split | ✅ PASS | user-input (4.2Kw) split to 3 notes; code-heavy pages split to keep each ≤6 code blocks; four procedure notes sized precisely at the 6-code cap. None left borderline-over. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` measured: streaming-output 1,650 · streaming-vs-single-mode 1,025 · structured-outputs 1,921 · user-input 4,208 = 8,804 = master 8,804 (±0%). |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B19C authors 0 term notes; Undigested Terms Plan routes all SDK I/O terms (dedup across term_dictionary AND documentation/); Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented (11 existing terms linked, not recreated; no `cc_` doc note duplicates a term note). |
| CP9 | Discoverability / inlinks executed (G7/G8) | ✅ PASS | Inlinks table maps ≥1 inbound link from outside `claude_code/` to every one of the 9 notes; verified at finalization by DB in-degree ≥1. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
