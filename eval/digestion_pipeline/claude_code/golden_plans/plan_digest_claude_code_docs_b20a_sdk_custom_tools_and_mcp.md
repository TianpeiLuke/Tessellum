---
title: Sub-Plan B20A — Claude Code Docs: SDK Custom Tools & MCP
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["agent-sdk/custom-tools", "agent-sdk/mcp", "agent-sdk/tool-search"]
---

# Sub-Plan B20A: SDK Custom Tools & MCP

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 3 Agent-SDK pages that cover how an SDK application gives Claude tools: defining **custom tools** with
an in-process MCP server, **connecting to external MCP servers** (stdio / HTTP / SSE / SDK transports),
and **tool search** for scaling to large tool catalogs. P2 (Phase B) — built on the SDK cores (B19A/B19C)
and the permissions sub-plan (B20C); references the existing `term_mcp` / `term_function_calling` /
`term_context_window` vocabulary. These are procedure-heavy "how to wire it" pages (Python + TypeScript
code groups), not vocabulary pages, so they are digested as `cc_` doc notes, not term notes.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 3 pages, 7,726 measured words. **Planned: 7 notes.**

## Content Strategy

- **Prioritize**: the in-process SDK MCP server (`create_sdk_mcp_server` / `createSdkMcpServer`) + the
  `mcp__{server}__{tool}` naming + `allowedTools` access model — the load-bearing mechanics every later
  SDK note links.
- **Group**: split the dense `custom-tools.md` (4.2Kw, 19 code blocks) by stage — define/register a tool,
  control access, handle errors, return rich content; split `mcp.md` (2.6Kw, 30 code blocks) into connect
  & transport vs auth/troubleshoot. Keep `tool-search.md` (999w) as one note (its `MCP tool search` stub
  in `mcp.md` is folded in / link-out, not duplicated).
- **Skip / link-out (own other sub-plans)**: the full permission-evaluation order (`allowedTools` /
  `disallowedTools` / permission modes) → B20C `agent-sdk/permissions.md`; the CLI-scope MCP install
  (`/en/mcp#mcp-installation-scopes`) → B08A `mcp.md`; the `tool()` / `@tool` / `create_sdk_mcp_server`
  full parameter refs → B21B/B21C language reference; the API-level tool-search mechanism (platform docs)
  → external `## References`. Referenced via links, never duplicated.
- **Glossary / terms**: no new `term_dictionary` notes — MCP, function calling/tool use, context window,
  agent harness all have existing term notes that are linked (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 3 pages re-read from `inbox/claude_code_docs/agent-sdk/` (verbatim mirror of `code.claude.com/docs/en/agent-sdk/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| custom-tools | /agent-sdk/custom-tools | 4,162 | 19 | 9 | 8 | procedure |
| mcp | /agent-sdk/mcp | 2,565 | 30 | 10 | 16 | procedure |
| tool-search | /agent-sdk/tool-search | 999 | 3 | 5 | 0 | concept |

> **H2 lists (document order):**
> - **custom-tools**: Quick reference · Create a custom tool (H3 Weather tool example, Call a custom tool, Add more tools, Add tool annotations) · Control tool access (H3 Tool name format, Configure allowed tools) · Handle errors · Return images and resources (H3 Images, Resources) · Return structured data · Example: unit converter · Next steps · Related documentation
> - **mcp**: Quickstart · Add an MCP server (H3 In code, From a config file) · Allow MCP tools (H3 Tool naming convention, Auto-approve with allowedTools, Discover available tools) · Transport types (H3 stdio servers, HTTP/SSE servers, SDK MCP servers) · MCP tool search · Authentication (H3 Pass credentials via environment variables, HTTP headers for remote servers, OAuth2 authentication) · Examples (H3 List issues from a repository, Query a database) · Error handling · Troubleshooting (H3 Server shows "failed" status, Tools not being called, Connection timeouts) · Related resources
> - **tool-search**: How tool search works · Configure tool search · Optimize tool discovery · Limits · Related documentation

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **7 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_sdk_custom_tool_definition.md` | procedure | custom-tools: Quick reference, Create a custom tool (4 parts), Weather tool example, Call a custom tool, Add more tools, Add tool annotations | 600 | The four parts of a tool (name/description/input schema/handler); `@tool`/`tool()` + `create_sdk_mcp_server`/`createSdkMcpServer` in-process server; pass via `mcpServers` to `query`; `readOnlyHint` parallel-call annotation. ≤6 code (Python+TS define, call, annotation pairs). |
| 2 | `cc_sdk_tool_access_control.md` | procedure | custom-tools: Control tool access (Tool name format, Configure allowed tools) | 350 | `mcp__{server}__{tool}` name format; availability vs permission layers; `tools`/`allowedTools`/`disallowedTools` (bare vs scoped); removing built-ins. Full eval order → B20C permissions (link-out). |
| 3 | `cc_sdk_tool_error_handling.md` | procedure | custom-tools: Handle errors | 350 | `isError: true` / `"is_error": True` returns vs uncaught throw; returned errors keep the agent loop alive, throws fail `query`; HTTP-status + try/except double-catch pattern. ≤2 code. |
| 4 | `cc_sdk_tool_rich_content.md` | concept | custom-tools: Return images and resources (Images, Resources), Return structured data | 500 | The `content` block types (text/image/audio/resource/resource_link); base64 image field table; resource URI-as-label table; `structuredContent` JSON result (Python in-process limitation note). ≤4 code. |
| 5 | `cc_sdk_connect_mcp_servers.md` | procedure | mcp: Quickstart, Add an MCP server (In code, From a config file), Allow MCP tools (naming, allowedTools, Discover tools), Transport types (stdio, HTTP/SSE, SDK) | 700 | Configure `mcpServers` in code or `.mcp.json` (+`settingSources` project); `mcp__<server>__<tool>` naming + `allowedTools` wildcards; the three transports (stdio/HTTP-SSE/SDK in-process) + `http`/`streamable-http` alias; inspect `init` message for available tools. ≤6 code. |
| 6 | `cc_sdk_mcp_auth_and_errors.md` | procedure | mcp: Authentication (env vars, HTTP headers, OAuth2), Examples (GitHub, Postgres), Error handling, Troubleshooting (failed status, tools not called, timeouts) | 600 | Credentials via `env` / `${VAR}` expansion / HTTP `headers` / OAuth2 bearer (SDK does not run the flow); detect failures via `init` message `status`; troubleshoot failed/not-called/60s-timeout. ≤6 code (GitHub+Postgres+init examples). |
| 7 | `cc_sdk_tool_search.md` | concept | tool-search: How it works, Configure, Optimize discovery, Limits + mcp: MCP tool search (folded) | 500 | Withhold tool defs from context, load 3-5 on demand; `ENABLE_TOOL_SEARCH` table (unset/true/auto/auto:N/false); Vertex/proxy fallbacks; name/description optimization; 10K-tool / 3-5-result / no-Haiku limits. Applies to remote + SDK tools. ≤3 code. |

**Estimate: 7 notes** — procedure ×5 (notes 1,2,3,5,6), concept ×2 (notes 4,7). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 3 (7,726 words). New `cc_` notes: 7. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~3,600 (avg ~515/note). Code blocks: ≤6 per note (source is code-heavy; each
  note keeps the minimal representative Python+TS pair(s), not every verbatim duplicate — see Density Re-Assessment).
- **Building Block Distribution**: procedure ×5 (notes 1,2,3,5,6) · concept ×2 (notes 4,7). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_sdk_custom_tool_definition` (7 term notes)
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — what MCP is; relevance: the note builds an **in-process MCP server** with `create_sdk_mcp_server`, so MCP is the protocol the custom tool is registered under and exposed to Claude through.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — the LLM-calls-a-typed-function mechanism; relevance: defining a name/description/input-schema/handler is exactly authoring a function-calling tool, and the handler return feeds back into the loop.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — the name+description+schema spec of a tool; relevance: the note's "four parts of a tool" (name, description, input schema, handler) IS a tool descriptor, and the description is what Claude reads to decide when to call it.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the engine wrapping the model with tools; relevance: `create_sdk_mcp_server` + `mcpServers` wires the custom tool into the SDK harness that supplies tools/context/execution to Claude.
- [Structured Output](../../term_dictionary/term_structured_output.md) — schema-constrained machine-readable result; relevance: the input schema (Zod / dict / JSON Schema) constrains the arguments Claude must provide, and `structuredContent` returns schema-shaped data.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the agentic harness/product; relevance: the Agent SDK is the programmatic form of the Claude Code engine, and this note shows how to extend that engine with your own callable functions.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeated calls have no extra effect; relevance: the note's tool-annotations table includes `idempotentHint`, the property this term defines, used to describe how a tool behaves on repeated calls.

### 2. `cc_sdk_tool_access_control` (6 term notes)
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — what MCP is; relevance: the `mcp__{server_name}__{tool_name}` name format the note explains is the MCP-tool addressing scheme, and access rules are written against those MCP names.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — progressive permission/approval modes; relevance: the note's `allowedTools` pre-approval (run without a prompt) vs scoped `disallowedTools` (deny matching calls) is exactly the graduated permission model this term defines.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — typed tool invocation; relevance: the note governs which tools appear in Claude's context (availability) and which calls are approved (permission) — both gate the function-calling step.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool name/spec; relevance: the availability layer controls whether a tool's descriptor is present in Claude's context at all (`tools: []` removes built-ins), the descriptor-visibility lever the note documents.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the tool-wiring engine; relevance: the `tools`/`allowedTools`/`disallowedTools` options configure which capabilities the harness exposes and auto-approves for the model.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the agentic harness/product; relevance: this access model is the SDK form of Claude Code's allow/deny tool gating, scoping what the agent can do.

### 3. `cc_sdk_tool_error_handling` (6 term notes)
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — tool call + result loop; relevance: the note is about what the tool handler returns to the model — `isError: true` makes the failure a tool result Claude can react to, vs a throw that aborts the call.
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — what MCP is; relevance: the error contract (`is_error` in the result content) is part of the MCP `CallToolResult` shape the in-process server returns.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the loop-running engine; relevance: the note's core distinction is whether the **agent loop** (run by the harness) continues or stops — a returned error keeps it alive, an uncaught throw ends `query`.
- [ReAct (Reasoning + Acting)](../../term_dictionary/term_react.md) — reason-act-observe cycle; relevance: returning the error as an observation lets Claude observe-then-retry/switch-tool, the recovery behavior of the reason-act-observe pattern.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool spec/handler; relevance: the note is guidance on how a tool's handler (the executable half of the descriptor) should report failures back to the model.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed coding agents; relevance: surviving tool errors and course-correcting without halting is the resilience that lets an autonomous coding agent chain many actions, the behavior this error pattern protects.

### 4. `cc_sdk_tool_rich_content` (6 term notes)
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — tool result mechanism; relevance: the note specifies the shapes a tool result can take (text/image/audio/resource blocks + `structuredContent`), i.e. the return half of a function call.
- [Multimodal ML/AI](../../term_dictionary/term_multimodal.md) — models consuming images/audio/text; relevance: the note returns base64 image and audio blocks that Claude processes as visual/audio input, which is multimodal tool output.
- [Structured Output](../../term_dictionary/term_structured_output.md) — schema-shaped machine-readable result; relevance: `structuredContent` is the note's mechanism for returning exact JSON fields Claude reads instead of parsing text — a structured-output return path.
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — what MCP is; relevance: the block shapes (image/resource/`CallToolResult`) come directly from the MCP tool-result specification the note cites.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool name/spec/handler; relevance: rich-content blocks are what a tool's handler emits, extending the descriptor's output contract beyond plain text.
- [Idempotency](../../term_dictionary/term_idempotency.md) — stable repeated behavior; relevance: resources addressed by a stable URI label (so Claude can reference the same generated artifact later) connect to the idempotent-reference idea this term covers; the URI is a name, not a path the SDK re-reads.

### 5. `cc_sdk_connect_mcp_servers` (7 term notes)
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — open standard for connecting agents to external tools/data; relevance: this note is the canonical SDK how-to for connecting to MCP servers, so the MCP term is its definitional anchor.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the tool/execution engine; relevance: the `mcpServers` option and `.mcp.json` wire external servers into the SDK harness, extending the agent's tool surface beyond built-ins.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — typed tool invocation; relevance: each connected server exposes tools as `mcp__<server>__<tool>` that Claude calls — the connection plumbing behind function calling.
- [Builder MCP](../../term_dictionary/term_builder_mcp.md) — an internal MCP server example; relevance: it is a concrete instance of the stdio/HTTP MCP-server connection pattern this note teaches, grounding the abstract transport types in a real server.
- [Context Window](../../term_dictionary/term_context_window.md) — the token budget; relevance: the note flags that many connected tool definitions consume context and points to tool search — the context-cost trade-off of connecting servers.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — permission/approval model; relevance: connected MCP tools need explicit `allowedTools` permission before Claude can call them, the auto-approve-or-prompt model this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the agentic harness/product; relevance: the note contrasts SDK-level MCP config with the CLI install scopes of Claude Code, the product whose engine the SDK exposes.

### 6. `cc_sdk_mcp_auth_and_errors` (6 term notes)
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — what MCP is; relevance: the note covers authenticating and diagnosing MCP server connections (env creds, headers, OAuth2, `init` status), the operational layer of MCP servers.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — tool call lifecycle; relevance: the "tools not being called" troubleshooting and the GitHub/Postgres examples are about getting Claude to actually invoke the connected MCP tools.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the connection-managing engine; relevance: the SDK harness emits the `system`/`init` message with per-server connection status the note tells you to check before the agent works.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — permission/approval model; relevance: the GitHub/Postgres examples scope `allowedTools` to specific read tools (e.g. only `mcp__postgres__query`), the least-privilege approval this term covers.
- [Builder MCP](../../term_dictionary/term_builder_mcp.md) — an internal MCP server example; relevance: it is a real authenticated MCP server, paralleling the env-var/header credential patterns the note documents for GitHub and remote servers.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the agentic harness/product; relevance: these auth and troubleshooting steps apply to the SDK form of the Claude Code engine connecting to external services.

### 7. `cc_sdk_tool_search` (6 term notes)
- [Context Window](../../term_dictionary/term_context_window.md) — the finite token budget; relevance: tool search exists to keep tool definitions out of the context window (50 tools = 10-20K tokens) and load only 3-5 on demand — the context-budget problem this note solves.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — managing what enters the window; relevance: deferring/loading tool defs and writing discoverable names/descriptions is a context-engineering tactic for what occupies the agent's working context.
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — what MCP is; relevance: tool search applies to all registered tools whether from remote MCP servers or custom SDK MCP servers, scaling MCP tool catalogs.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — tool selection/invocation; relevance: the note cites that tool-selection accuracy degrades past 30-50 loaded tools — search narrows the function-calling candidate set to the few relevant tools.
- [Compaction](../../term_dictionary/term_compaction.md) — summarizing/freeing context; relevance: the note notes that when the SDK compacts earlier messages to free space, previously discovered tools may be removed and the agent searches again — compaction interacts with tool persistence.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool name/description spec; relevance: search matches queries against tool **names and descriptions**, so the note's optimization advice is about writing better descriptors for discoverability.

## Section Coverage Map

```
custom-tools.md
├── Quick reference (intent→action table) ─ → note 1 (folded as orientation)
├── Create a custom tool (4 parts) ──────── → note 1 (cc_sdk_custom_tool_definition)
│   ├── Weather tool example ───────────── → note 1
│   ├── Call a custom tool ─────────────── → note 1
│   ├── Add more tools ─────────────────── → note 1
│   └── Add tool annotations ───────────── → note 1
├── Control tool access ─────────────────── → note 2 (cc_sdk_tool_access_control)
│   ├── Tool name format ───────────────── → note 2
│   └── Configure allowed tools ────────── → note 2 (full eval order → B20C link-out)
├── Handle errors ───────────────────────── → note 3 (cc_sdk_tool_error_handling)
├── Return images and resources ─────────── → note 4 (cc_sdk_tool_rich_content)
│   ├── Images ─────────────────────────── → note 4
│   └── Resources ──────────────────────── → note 4
├── Return structured data ──────────────── → note 4
├── Example: unit converter ─────────────── → note 1 (enum/error pattern, summarized; → note 3)
├── Next steps ──────────────────────────── → notes 1/7 (links: tool search, permissions B20C, mcp)
└── Related documentation ───────────────── → notes (links: TS/Python ref B21B/B21C, MCP)
mcp.md
├── Quickstart ──────────────────────────── → note 5 (cc_sdk_connect_mcp_servers)
├── Add an MCP server (In code, config) ─── → note 5
├── Allow MCP tools (naming, allowed, disc) → note 5
├── Transport types (stdio, HTTP/SSE, SDK) ─ → note 5
├── MCP tool search ─────────────────────── → note 7 (folded; stub links tool-search.md)
├── Authentication (env, headers, OAuth2) ── → note 6 (cc_sdk_mcp_auth_and_errors)
├── Examples (GitHub, Postgres) ─────────── → note 6
├── Error handling ──────────────────────── → note 6
├── Troubleshooting (failed/not-called/TO) ─ → note 6
└── Related resources ───────────────────── → notes 5/6 (links: custom-tools, permissions B20C, MCP dir)
   (MCP installation scopes /en/mcp → linked out to B08A, not duplicated)
tool-search.md
├── How tool search works ───────────────── → note 7 (cc_sdk_tool_search)
├── Configure tool search (ENABLE_TOOL_SEARCH) → note 7
├── Optimize tool discovery ─────────────── → note 7
├── Limits ──────────────────────────────── → note 7
└── Related documentation ───────────────── → note 7 (links: API tool-search ref, mcp, custom-tools)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| custom-tools (4.2Kw, 19 code, 9 H2) | notes 1,2,3,4 | exceeds ≤2500w & ≤6-code caps; distinct stages — define+register (note 1), access control (note 2), error contract (note 3), rich-content returns (note 4); each keeps a minimal Python+TS pair, not all 19 verbatim blocks. unit-converter example folded into note 1 (define pattern) + note 3 (error pattern) rather than its own note. |
| mcp (2.6Kw, 30 code, 10 H2) | notes 5,6 + note 7 (tool-search stub) | 30 code blocks (mostly Python/TS/json/.mcp.json duplicates) far exceed ≤6 cap; connect+transport (note 5) vs auth+examples+troubleshoot (note 6) are different procedures; the `MCP tool search` H2 is a 2-sentence stub → folded into note 7, not its own note. CLI install scopes link out to B08A. |
| tool-search (999w, 3 code) | note 7 | within caps; single concept note; absorbs the `mcp.md#MCP tool search` stub so the concept lives in one place. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_sdk_custom_tool_definition | procedure | 600 | 6 | ✅ |
| 2 | cc_sdk_tool_access_control | procedure | 350 | 0 | ✅ |
| 3 | cc_sdk_tool_error_handling | procedure | 350 | 2 | ✅ |
| 4 | cc_sdk_tool_rich_content | concept | 500 | 4 | ✅ |
| 5 | cc_sdk_connect_mcp_servers | procedure | 700 | 6 | ✅ |
| 6 | cc_sdk_mcp_auth_and_errors | procedure | 600 | 6 | ✅ |
| 7 | cc_sdk_tool_search | concept | 500 | 3 | ✅ |

No note exceeds the caps. The source is code-heavy, so the binding cap here is **≤6 code blocks/note** —
each note keeps the minimal representative Python+TS pair(s) for the patterns it owns (the docs duplicate
every snippet in both languages; the digest does not need every verbatim block). No over-compression —
every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_sdk_custom_tool_definition cc_sdk_tool_access_control cc_sdk_tool_error_handling cc_sdk_tool_rich_content cc_sdk_connect_mcp_servers cc_sdk_mcp_auth_and_errors cc_sdk_tool_search"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] && echo "DENSITY WARNING: $n"
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

Single phase (7 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/agent-sdk/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 7 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 7 notes RECEIVES ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability (inbound in-degree ≥1, sibling+external) | every note has ≥1 inbound edge in `note_links`; cluster not an island | DB in-degree query post-execution |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 7 rows** under an "Agent SDK — Tools & MCP" cluster + increments the
BB-distribution counts (procedure ×5, concept ×2). The entry-point back-link is added to each note at finalization.

## Undigested Terms Plan (Step 4e)

B20A creates **no new `term_dictionary` notes** — every vocabulary term on these pages is covered by an
existing substantive term note (link) or is a doc-concept owned by this sub-plan's `cc_` notes (Pattern B):

| Term (page) | Disposition |
|---|---|
| MCP / Model Context Protocol | link `term_mcp` (exists) |
| Custom tool / tool / function calling / tool use | link `term_function_calling` (exists) + doc note 1 |
| Tool descriptor (name/description/schema) | link `term_tool_descriptor` (exists) |
| In-process / SDK MCP server (`create_sdk_mcp_server`) | doc note 1/5 (`cc_sdk_custom_tool_definition`, `cc_sdk_connect_mcp_servers`) |
| Tool annotations (`readOnlyHint`/`idempotentHint`/…) | doc note 1; `idempotentHint` links `term_idempotency` (exists) |
| `allowedTools` / `disallowedTools` / availability vs permission | doc note 2; full eval order → B20C permissions (link) |
| Permission model / approval | link `term_graduated_trust` (exists) |
| `isError` / error contract | doc note 3 |
| Image / audio / resource blocks (multimodal output) | doc note 4; link `term_multimodal` (exists) |
| `structuredContent` / structured result | doc note 4; link `term_structured_output` (exists) |
| Transport: stdio / HTTP / SSE / streamable-http | doc note 5 (no standalone term — config detail, not vault vocabulary) |
| OAuth2 / env-var credentials / HTTP headers | doc note 6 (auth detail, not vault vocabulary) |
| Tool search / `ENABLE_TOOL_SEARCH` | doc note 7 |
| Context window / compaction | existing term notes (link) — `term_context_window`, `term_compaction` |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 3 pages scanning emphasis/tables/captions/code
comments for newly-surfaced terms. Candidates **transport (stdio/HTTP/SSE)**, **OAuth2**, **base64 image
block**, and **`ENABLE_TOOL_SEARCH`** surfaced — all are SDK configuration details, not cross-cutting vault
vocabulary, and each is fully explained inside its owning `cc_` note (notes 5/6/4/7). None is a duplicate
of an existing term note and none warrants a new `term_dictionary` capture. **0 new B20A `term_dictionary`
captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B20A authors zero term notes, so there are no
new slugs to audit for over-generality or collision. The collision check that matters here (do the page
concepts duplicate existing notes?) was performed: `term_mcp`, `term_function_calling`,
`term_tool_descriptor`, `term_structured_output`, `term_multimodal`, `term_idempotency`, `term_context_window`,
`term_compaction`, `term_graduated_trust`, `term_agent_harness`, `term_react`, `term_autonomous_coding_agents`,
`term_builder_mcp` all exist → linked, not recreated. No `cc_` doc note duplicates an existing term note.

## Term-Note Authoring Requirements

**N/A for B20A** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim from source (keep the minimal representative Python+TS pair per pattern; do not
  fabricate or alter snippets). One BB per note. Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_mcp.md` | notes 1, 5 | MCP term → SDK in-process custom-tool server + external-server connection |
| `term_dictionary/term_function_calling.md` | notes 1, 7 | function-calling term → SDK tool definition + tool-search selection |
| `term_dictionary/term_tool_descriptor.md` | note 1 | tool-descriptor term → SDK tool's name/description/schema/handler |
| `term_dictionary/term_context_window.md` | note 7 | context-window term → tool search defers tool defs to save context |
| `term_dictionary/term_builder_mcp.md` | notes 5, 6 | Builder MCP (real MCP server) → SDK connect + auth patterns |
| `term_dictionary/term_graduated_trust.md` | note 2 | permission/approval term → SDK `allowedTools`/`disallowedTools` access model |
| `term_dictionary/term_structured_output.md` | note 4 | structured-output term → SDK `structuredContent` tool result |

## Follow-up Recommendations

- After the 7 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above (verify DB
  in-degree ≥1 for all 7 — G7/G8); queue the 7 rows for `entry_claude_code_docs.md` under "Agent SDK —
  Tools & MCP"; `/tessellum-check-broken-links`; add sibling cross-links to/from B19C (SDK streaming/IO),
  B20C (SDK permissions), and B08A (CLI MCP) once those clusters exist.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B20A, 2026-06-13)

- **Source re-read (Step 2)**: all 3 pages re-read from `inbox/claude_code_docs/agent-sdk/`; measured words
  match the master's figures (custom-tools 4,162 · mcp 2,565 · tool-search 999 = 7,726). Code-block counts
  measured (custom-tools 19, mcp 30, tool-search 3) — both code-heavy pages forced a split on the
  ≤6-code-block cap, not just the word cap. No >1.5× under-estimate of words.
- **Notes**: 7 (procedure 5, concept 2) — matches master estimate. Two source pages split (custom-tools →
  4 notes, mcp → 2 notes + tool-search stub folded into note 7); tool-search → 1 note.
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard —
  6-7 term notes per note (15 distinct `term_dictionary/` terms), each with a per-link relevancy statement;
  `cc_*` forward-refs (B20C permissions, B08A CLI MCP, B21B/B21C language refs) kept as prose/link-outs.
- **Dedup (G-B)**: BM25 + dense + filename grep across `term_dictionary/` AND `resources/documentation/`.
  No existing doc note covers SDK custom tools / MCP transport / tool search (the `claude_code/` dir does
  not exist yet; `howto_build_python_mcp_server` and `faq_create_custom_mcp_server` are internal-Amazon
  MCP guides, different sense). 15 existing term notes link-only, 0 recreated.
- **Step 2d new-term scan**: candidates surfaced (transport/OAuth2/base64/`ENABLE_TOOL_SEARCH`) → all SDK
  config details owned by their `cc_` note; **0 new B20A term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G5/G8 verification notes, Inlinks table (7 executed inbound edges).
- **28-item checklist**: PASS (term-note items N/A — B20A authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented and self-reviewed; set to `ready` after the 9-checkpoint review below passed 9/9.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8 incl G7/G8) | ✅ PASS | 8 gate rows present (single phase); G7/G8 Discoverability (inbound in-degree ≥1) included with executed Inlinks table. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B20A contributes 7 rows under "Agent SDK — Tools & MCP". |
| CP4 | Plan size ≤30 / split | ✅ PASS | 7 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches master Format Definition (derived from existing `documentation/` notes) exactly; body uses `## Overview` / source-mirrored H2 / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | Code-heavy pages split aggressively on the ≤6-code cap; all 7 notes ≤700w / ≤6 code — none borderline after the split. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w`: custom-tools 4,162 = plan; mcp 2,565 = plan; tool-search 999 = plan (total 7,726 = master). Code blocks counted via fence-pair grep. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B20A authors 0 term notes; Undigested Terms Plan routes every page term; Authoring Requirements inherited from master. |
| CP9 | Term-slug specificity + collision audit (CP8f) | ✅ PASS | N/A (0 new slugs); page-concept collision check documented (15 existing terms linked, not recreated; no `cc_` doc note duplicates a term note). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `ready`.

**Source**: https://code.claude.com/docs/en
**Last Updated**: 2026-06-13
**Status**: Active
