---
tags:
  - resource
  - terminology
  - openclaw
  - tool-descriptor
  - tools
  - plugin-system
  - typescript-sdk
  - discriminated-union
keywords:
  - Tool Descriptor
  - ToolDescriptor
  - ToolOwnerRef
  - ToolExecutorRef
  - ToolAvailabilityExpression
  - ToolAvailabilitySignal
  - defineToolDescriptor
  - defineToolDescriptors
  - tool registration contract
  - openclaw tools
topics:
  - Tool registration contracts
  - Plugin systems
  - OpenClaw extensibility
  - Agent function calling
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://github.com/openclaw/openclaw/blob/main/src/tools/types.ts
access_control_group: ["general"]
---

# Tool Descriptor

## Definition

A **Tool Descriptor** is the typed, declarative record an agent host requires every callable tool to register under — a stable contract carrying `name`, `description`, an input JSON schema, and provenance/routing metadata — so that heterogeneous tool sources (built-in handlers, plugins, external MCP servers, channel actions) can be exposed to the model through one uniform shape. Every modern function-calling stack centers on this same record: Anthropic's tool-use schema uses `name` + `description` + `input_schema` (JSON Schema draft 2020-12); OpenAI's function-calling tool object uses `name` + `description` + `parameters` (also JSON Schema); the Model Context Protocol's `tools/list` reply lists tools with `name` + optional `description` + `inputSchema` (and now optional `outputSchema`); LangChain's `BaseTool` / `StructuredTool` ship `name` + `description` + `args_schema` (a Pydantic model that compiles to a JSON Schema). The descriptor is the **portable advert** an LLM reads to decide *whether* to call a tool; the runtime separately resolves *how* the call dispatches.

In **OpenClaw**, the Tool Descriptor contract is declared in `src/tools/types.ts` (97 LOC) and the companion factory module `src/tools/descriptors.ts` (11 LOC). The apex type `ToolDescriptor` carries the four standard function-calling fields (`name`, `description`, `inputSchema`, optional `outputSchema`) plus four OpenClaw-specific extensions: `owner: ToolOwnerRef` (who registered the descriptor), optional `executor?: ToolExecutorRef` (where calls dispatch), optional `availability?: ToolAvailabilityExpression` (a recursive boolean tree gating session-time visibility), and optional `annotations` / `sortKey` for UI surfaces. The four registration provenance values — `core` (built-in), `plugin` (extension-supplied), `channel` (chat-adapter action), `mcp` (external MCP server tool) — are tagged via discriminated unions and let one shared planner handle every source family without losing per-source metadata.

## Context

Tool Descriptors are the lingua franca of agent function calling. Every major LLM provider publishes one — Anthropic's [tool-use input schema](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview), OpenAI's [function-calling tools array](https://developers.openai.com/api/docs/guides/function-calling), Google Gemini's `FunctionDeclaration`, Cohere's tool spec — and each agent framework normalizes upstream variants into its own descriptor type. LangChain's [BaseTool](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.base.BaseTool.html) hides provider quirks behind a single class; LangGraph and CrewAI consume the same `BaseTool` instances; LlamaIndex has `FunctionTool` with the analogous trio. The Model Context Protocol elevates the descriptor to a wire-format primitive — the [`tools/list` response](https://modelcontextprotocol.io/specification/draft/server/tools) is literally a list of descriptors, so any MCP client can present any MCP server's tools to its model without out-of-band knowledge.

Within OpenClaw, the Tool Descriptor sits at the seam between the [Plugin SDK](term_plugin_sdk.md) (which provides `definePluginEntry` / `registerTool` authoring surfaces) and the agent runtime: every plugin's tool registration, every MCP-server-mounted tool, every channel action, and every core executor produces a `ToolDescriptor` that flows into the model catalog, the availability evaluator, and the model's `tools[]` payload. The `executor` / `owner` split — same four `kind` literals on both unions but with different per-variant fields — lets a channel-owned tool dispatch via a plugin's executor without the descriptor needing two parallel shapes; the `availability` tree lets a tool say "I'm visible only when (Slack auth is present) AND ((prod env) OR (explicit override config))" without hard-coding visibility checks across the runtime.

## Key Characteristics

- **`ToolDescriptor` apex shape** — `name: string` (stable identifier, naming convention follows the MCP rule: ASCII letters/digits/underscore/hyphen/dot, 1-128 chars), `description: string` (the load-bearing model-facing prose Anthropic and OpenAI both treat as the routing signal), `inputSchema: JsonObject` (JSON Schema draft 2020-12 matching Anthropic's `input_schema` and OpenAI's `parameters`), optional `outputSchema`, `title`, `annotations`, `sortKey`, plus the three OpenClaw extensions: `owner`, `executor?`, `availability?`. Every field is `readonly` — descriptors are shared session-time configuration the planner, evaluator, and UI all read.

- **`ToolOwnerRef` — provenance discriminated union** — answers "who registered this descriptor?" via `kind: "core" | "plugin" | "channel" | "mcp"`. The `core` variant carries no extra fields; `plugin` carries `pluginId`; `channel` carries `channelId` plus an optional `pluginId` (since a channel can be plugin-provided); `mcp` carries `serverId`. Drives audit, surface filtering ("show only first-party tools"), and trust policy (e.g., the `dangerousTools.deny` gate keyed on owner).

- **`ToolExecutorRef` — routing discriminated union** — answers "where does a call dispatch?" with the SAME four `kind` literals as `ToolOwnerRef` but DIFFERENT per-variant fields: `core` adds `executorId`, `plugin` adds `pluginId` + `toolName`, `channel` adds `channelId` + `actionId`, `mcp` adds `serverId` + `toolName`. Parallel-discriminated-union design (same vocabulary, different payloads) lets a channel-owned descriptor dispatch through a plugin's executor without contorting either union; consumers `switch (ref.kind)` independently on each.

- **`ToolAvailabilityExpression` — recursive boolean tree** — either a leaf `ToolAvailabilitySignal` (one of `always`, `auth { providerId }`, `config { path[], check? }`, `env { name }`, `plugin-enabled { pluginId }`, `context { key, equals? }`) OR a combinator `{ allOf: readonly Expression[] }` / `{ anyOf: readonly Expression[] }` whose children are themselves expressions. Recursion lets a tool encode arbitrary boolean gates ("Slack auth AND (prod env OR override config)"); the evaluator walks the tree against a `ToolAvailabilityContext` and emits per-leaf diagnostics so the UI can explain *why* a tool is hidden.

- **`ToolOwnerRef` for sealed / owner-only tools** — the owner field is also the security boundary the runtime uses to enforce "only the plugin that registered a tool may execute it" or to mask an MCP-server tool from agents whose session lacks that server. Combined with the `availability` tree, the owner ref is what makes the descriptor self-describing for both surface filtering and runtime authorization.

- **`defineToolDescriptor` / `defineToolDescriptors` — pass-through identity factories** — `descriptors.ts` (11 LOC) exports two pass-through functions whose body is literally `return descriptor;`. They have zero runtime cost but surface TypeScript's contextual-type inference at the declaration site: writing `const t = defineToolDescriptor({...})` narrows literal types (e.g., `kind: "plugin"` stays `"plugin"`, not `string`), produces compile errors at the offending field rather than the const declaration, and gives IDE autocomplete inside the object literal — the same "definer pattern" Vite's `defineConfig`, Vitest's `defineConfig`, and Solid Start's `defineRouteData` use.

- **`JsonValue` / `JsonObject` — readonly recursive JSON type** — input/output schemas are typed as `JsonObject = { readonly [key: string]: JsonValue }` where `JsonValue` recursively threads `readonly` through arrays and object signatures. Keeps the descriptor immutable at the type level so consumers (planner, evaluator, model-payload builder) can share references without defensive cloning.

- **Distinct from MCP at the wire layer, congruent at the schema layer** — OpenClaw's `ToolDescriptor` is an **in-process** TypeScript record; an MCP server's `tools/list` response is a **wire-format** JSON message. But the model-facing surface (`name` + `description` + `inputSchema`) is intentionally identical, so an MCP server's tool can be lifted into a `ToolDescriptor` with `owner: { kind: "mcp", serverId }` and `executor: { kind: "mcp", serverId, toolName }` and `inputSchema` copied verbatim — no schema translation needed.

## Related Terms

- **[Band MCP Tools Reference (a concrete tool-descriptor set)](../documentation/band/band_mcp_tools_reference.md)** — Band documentation note cataloging Band's concrete MCP toolset; relevance: Tool Descriptor defines OpenClaw's typed tool-registration contract (owner/executor refs, availability expressions), and Band's MCP tool reference IS a real-world set of tool descriptors whose key-type toolset loading is an availability-expression-style gating decision, so a reader of the descriptor contract would want Band as a concrete instantiation (and Band already cites this term, making the link reciprocal)

## Related Code Snippets

- [OpenClaw Skills — Tool Descriptor Contract](../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md): 4-pattern catalog covering `ToolDescriptor` / `ToolOwnerRef` / `ToolExecutorRef` / `ToolAvailabilityExpression` types.ts (97 LOC) + `defineToolDescriptor` descriptors.ts (11 LOC)

## References

- [OpenClaw `src/tools/types.ts`](https://github.com/openclaw/openclaw/blob/main/src/tools/types.ts) — upstream contract source for `ToolDescriptor` and the related discriminated unions (Class 2: project source)
- [OpenClaw `src/tools/descriptors.ts`](https://github.com/openclaw/openclaw/blob/main/src/tools/descriptors.ts) — `defineToolDescriptor` / `defineToolDescriptors` pass-through factories (Class 2: project source)
- [MCP Specification — Tools (`tools/list`)](https://modelcontextprotocol.io/specification/draft/server/tools) — canonical wire-format descriptor contract: `name` + `description` + `inputSchema` + naming rules and discovery semantics (Class 1: authoritative protocol spec)
- [JSON Schema Specification — 2020-12 Draft](https://json-schema.org/specification.html) — the schema language Anthropic/OpenAI/MCP all use for `input_schema` / `parameters` (Class 1: standards body)
- [Anthropic Tool Use — Overview](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview) — `name` + `description` + `input_schema` archetype used by Claude API and Claude Code (Class 2: framework docs)
- [OpenAI Function Calling Guide](https://developers.openai.com/api/docs/guides/function-calling) — `name` + `description` + `parameters` JSON-Schema tool definition (Class 2: framework docs)
- [LangChain `BaseTool` Reference](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.base.BaseTool.html) — `name` / `description` / `args_schema` (Pydantic-compiled JSON Schema) cross-provider tool abstraction (Class 2: framework docs)
