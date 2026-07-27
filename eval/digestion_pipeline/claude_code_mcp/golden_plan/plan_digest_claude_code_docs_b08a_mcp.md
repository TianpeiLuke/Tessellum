---
title: Sub-Plan B08A — Claude Code Docs: MCP
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["mcp", "mcp-quickstart", "managed-mcp"]
---

# Sub-Plan B08A: MCP (Model Context Protocol)

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 3 MCP pages that document how Claude Code connects to external tools and data via the Model Context
Protocol: the full reference (`mcp.md`), the end-to-end connection walkthrough (`mcp-quickstart.md`), and
the organization-level access controls (`managed-mcp.md`). P1 (Phase A) — MCP is a foundational extension
vocabulary that later sub-plans (B08B channels, B09 plugins, B10 subagents, B16 security, B20A SDK MCP)
reference, so this runs early. Glossary/MCP-vocabulary terms are routed per Pattern B (see Undigested
Terms Plan), not re-digested into term notes; the existing `term_mcp` term note is LINKED, never recreated.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 3 pages, 12,813 measured words. **Planned: 8 notes.**

## Content Strategy

- **Prioritize**: the transport/scope/auth/tool-search concepts that the channels (B08B), plugins (B09), and SDK-MCP (B20A) sub-plans link (P1).
- **Group**: `mcp.md` is large (6,822w, 41 code blocks) and must be split aggressively by concept (what-it-is / scopes / tool-search) vs procedure (transports / management / auth). `mcp-quickstart.md` is the single procedure walkthrough. `managed-mcp.md` is the admin/policy procedure.
- **Code-block discipline**: `mcp.md` carries 41 code blocks; every note caps at ≤6, so worked examples are kept compact (one representative block per concept) and repeated CLI variants are folded into prose, never re-listed verbatim.
- **Skip / link-out (own other sub-plans)**: Channels detail → B08B (`channels.md`, `channels-reference.md`); Plugins bundling → B09A (`plugins.md`, `plugins-reference.md`); permission rules → B05A (`permissions.md`); prompt-injection threat model → B16 (`security.md`); OpenTelemetry export schema → B15B (`monitoring-usage.md`); admin-setup enforcement → B14B (`admin-setup.md`, `server-managed-settings.md`); IDE/desktop/web surfaces → B12 (`desktop.md`, `vs-code.md`, `claude-code-on-the-web.md`). These are referenced via links, never duplicated.
- **MCP vocabulary**: not captured as new term notes — `term_mcp` (and the existing tool-use/auth/security terms) are LINKED; MCP-specific concepts (transports, scopes, tool search) are digested as `cc_` doc concept/procedure notes (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 3 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| mcp | /mcp | 6,822 | 41 | 14 | 27 | concept/procedure |
| mcp-quickstart | /mcp-quickstart | 3,072 | 4 | 8 | 5 | procedure |
| managed-mcp | /managed-mcp | 2,919 | 4 | 6 | 9 | procedure |

> **H2 lists (document order):**
> - **mcp**: What you can do with MCP · Find and build MCP servers · Installing MCP servers (H3 Option 1 HTTP, Option 2 SSE, Option 3 stdio, Option 4 WebSocket, Managing your servers, Dynamic tool updates, Automatic reconnection, Push messages with channels, Plugin-provided MCP servers) · MCP installation scopes (H3 Local scope, Project scope, User scope, Scope hierarchy and precedence, Environment variable expansion) · Practical examples (H3 Sentry, GitHub, PostgreSQL) · Authenticate with remote MCP servers (H3 Fixed OAuth callback port, Pre-configured OAuth credentials, Override OAuth metadata discovery, Restrict OAuth scopes, Dynamic headers) · Add MCP servers from JSON configuration · Import MCP servers from Claude Desktop · Use MCP servers from Claude.ai · Use Claude Code as an MCP server · MCP output limits and warnings (H3 Raise the limit for a specific tool) · Respond to MCP elicitation requests · Use MCP resources (H3 Reference MCP resources) · Scale with MCP Tool Search (H3 How it works, For MCP server authors, Configure tool search, Exempt a server from deferral) · Use MCP prompts as commands (H3 Execute MCP prompts) · Managed MCP configuration
> - **mcp-quickstart**: Before you begin · Add and verify a server · Where servers are saved (H3 Find your configuration on disk) · Change server scope (H3 Use a server in all your projects, Share a server with your team) · Additional MCP server examples (H3 Add a local server, Connect a server that requires sign-in) · Edit .mcp.json directly · Connect from other surfaces · Troubleshooting · Next steps
> - **managed-mcp**: Choose a pattern · Exclusive control with managed-mcp.json (H3 Authenticate with per-user credentials, Validate the configuration, Disable MCP entirely, Allow claude.ai connectors alongside the managed set) · Policy-based control with allowlists and denylists (H3 Match servers by URL/command/name, How a server is evaluated, Example configuration, Restrict the allowlist to managed settings only) · How restrictions appear to users · Monitor MCP usage · Configuration summary · Related resources

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **8 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_mcp_overview.md` | concept | mcp: intro, What you can do with MCP, Find and build MCP servers | 450 | What MCP is and why connect a server (links `term_mcp`); the six task categories (issue trackers, monitoring, databases, designs, workflows, external events); the Anthropic Directory, the prompt-injection trust warning (→ B16), and the `mcp-server-dev` scaffolding plugin (→ B09). |
| 2 | `cc_mcp_quickstart.md` | procedure | mcp-quickstart: Before you begin, Add and verify, Additional examples, Connect from other surfaces, Troubleshooting, Next steps + mcp: Practical examples | 600 | End-to-end connect→verify→use→remove flow for one server; `claude mcp list` status indicators; local stdio (Playwright) and OAuth (Sentry) variants; worked Sentry/GitHub/PostgreSQL examples; surface entry points (→ B12); troubleshooting symptom table. |
| 3 | `cc_mcp_transports.md` | procedure | mcp: Installing MCP servers (Options 1-4, the `--` separator note), Add from JSON, Import from Claude Desktop | 550 | The four transports — HTTP (recommended), SSE (deprecated), stdio (local subprocess, `CLAUDE_PROJECT_DIR`, `--` separator), WebSocket — with `claude mcp add`/`add-json` syntax; importing from Claude Desktop. |
| 4 | `cc_mcp_server_management.md` | procedure | mcp: Managing your servers, Dynamic tool updates, Automatic reconnection, Push messages with channels, Plugin-provided MCP servers, MCP output limits and warnings | 550 | `claude mcp list/get/remove` + `/mcp`; pending-approval states; `list_changed` dynamic refresh; exponential-backoff reconnection; the `claude/channel` push capability (→ B08B); plugin-bundled servers and their `mcp__plugin_*` tool names (→ B09); output-token warning/limit env vars. |
| 5 | `cc_mcp_installation_scopes.md` | concept | mcp: MCP installation scopes (Local/Project/User, Scope hierarchy and precedence, Environment variable expansion) + mcp-quickstart: Where servers are saved | 500 | The three scopes (local/project/user), where each is stored (`~/.claude.json` vs `.mcp.json`), team sharing via version control, the 5-level precedence order, and `${VAR}` / `${VAR:-default}` expansion in `.mcp.json`. |
| 6 | `cc_mcp_authentication.md` | procedure | mcp: Authenticate with remote MCP servers (OAuth flow, callback port, pre-configured creds, metadata discovery, restrict scopes, dynamic headers), Use Claude Code as an MCP server, Use MCP servers from Claude.ai | 600 | OAuth 2.0 for remote servers (401/403 discovery, `/mcp` browser flow); fixed `--callback-port`; pre-configured `--client-id`/`--client-secret`; `authServerMetadataUrl`; `oauth.scopes` pinning; `headersHelper` for non-OAuth schemes; claude.ai connectors; running Claude Code itself as a stdio MCP server. |
| 7 | `cc_mcp_tool_search.md` | concept | mcp: Scale with MCP Tool Search (How it works, For authors, Configure, Exempt from deferral), Use MCP resources, Use MCP prompts as commands, Respond to MCP elicitation requests | 600 | Tool Search defers tool definitions to keep context low (`ENABLE_TOOL_SEARCH` modes, `alwaysLoad` exemption, `tool_reference` model requirement); links `term_context_window`; @-mention MCP resources; `/mcp__server__prompt` commands; elicitation form/URL dialogs. |
| 8 | `cc_managed_mcp_configuration.md` | procedure | managed-mcp: all H2/H3 (Choose a pattern, managed-mcp.json exclusive control, allowlists/denylists, How a server is evaluated, restrictions UX, Monitor usage, Configuration summary) + mcp: Managed MCP configuration | 650 | Admin control of MCP: the seven restriction patterns; `managed-mcp.json` fixed-set/disable-all deployment + system paths; `allowedMcpServers`/`deniedMcpServers` matching by URL/command/name; the three-step evaluation order (merge → denylist → allowlist); `allowManagedMcpServersOnly`; what users see when blocked; OTEL usage monitoring (→ B15B). |

**Estimate: 8 notes** — concept ×3 (notes 1, 5, 7), procedure ×5 (notes 2, 3, 4, 6, 8). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 3 (12,813 words). New `cc_` notes: 8. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~4,500 (avg ~560/note). Code blocks: ≤6/note (source is code-heavy; worked examples kept to one representative block each).
- **Building Block Distribution**: concept ×3 (notes 1, 5, 7) · procedure ×5 (notes 2, 3, 4, 6, 8). No model/argument/empirical_observation in this sub-plan.
- Cross-refs: **≥6 relevancy-selected term notes per note** (24 distinct `term_dictionary/` terms across the 8 notes' Related Notes mappings, all DB-verified, 0 ghosts) + sibling `cc_*` links + entry-point back-link at finalization.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> **Standard:** ≥6 relevancy-selected `term_dictionary/` term notes per note (all DB-verified, **0 ghosts**),
> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.
> All targets verified present on disk 2026-06-13 via `ls .../term_dictionary/<slug>.md`.

### 1. `cc_mcp_overview` (7 term notes)
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open standardized protocol letting LLMs connect to external data sources and tools; relevance: this note IS the Claude Code overview of MCP, so the term note is its canonical definitional anchor (do NOT recreate, link only).
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — LLM capability to invoke external functions/APIs via structured tool calls; relevance: MCP servers expose their capabilities as tools Claude calls, so MCP is a tool-use delivery mechanism this overview frames.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI coding tool; relevance: the note documents Claude Code's own MCP connectivity, so the product term grounds what is being extended.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — software infrastructure wrapping an LLM with tools/context/execution; relevance: MCP servers plug into the harness's tool layer, expanding what the harness can do beyond built-in tools.
- [OWASP Top 10 for LLM Applications](../../term_dictionary/term_owasp_llm.md) — security framework for the most critical LLM-deployment vulnerabilities; relevance: the note's trust warning that servers fetching external content can expose you to prompt-injection risk is exactly an OWASP-LLM threat class.
- [Skills](../../term_dictionary/term_skills.md) — packaged expertise extending agent capabilities for specific workflows; relevance: the note contrasts MCP (external tool connection) with skills (packaged knowledge) as complementary extension layers and cites the `mcp-server-dev` scaffolding skill/plugin.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — AI systems that write/modify/reason about code with minimal intervention; relevance: connecting MCP servers lets the agent read and act on external systems directly instead of working from pasted data, the autonomous operating mode this term defines.

### 2. `cc_mcp_quickstart` (6 term notes)
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open AI-tool integration protocol; relevance: this note is the hands-on walkthrough for connecting one MCP server end to end, so the term grounds every step.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI tool; relevance: the entire procedure uses the `claude mcp` CLI subcommands, so the host tool term anchors the walkthrough.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — LLM tool-invocation capability; relevance: the "Use the server" step shows Claude calling the new server's tools, with output labeled by server name — a concrete tool-use event.
- [OAuth 2.0 Token](../../term_dictionary/term_oauth_token.md) — RFC 6749 access/refresh token model; relevance: the "Connect a server that requires sign-in" Sentry example walks through the OAuth browser sign-in, the token-based auth this term defines.
- [VS Code](../../term_dictionary/term_vscode.md) — Microsoft's source-code editor (an IDE surface); relevance: the "Connect from other surfaces" section names VS Code as one place to add MCP servers besides the CLI.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity before granting resource access; relevance: the status table's `! Needs authentication` state and the sign-in flow are authentication steps this term defines, distinct from the token specifics.

### 3. `cc_mcp_transports` (6 term notes)
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open AI-tool integration protocol with defined transports; relevance: this note documents the four MCP transports (HTTP/SSE/stdio/WebSocket) the protocol specifies, so the term is the direct parent concept.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI tool; relevance: the note details Claude Code's `claude mcp add`/`add-json` flags for each transport, so the host tool term anchors the commands.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — LLM tool-invocation capability; relevance: every transport's purpose is to expose a server's tools to Claude for tool calls, the mechanism this term defines.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — architecture where program flow is driven by emitted events; relevance: the WebSocket transport holds a persistent bidirectional connection so a server can push events to Claude unprompted, an event-driven integration pattern.
- [OAuth 2.0 Token](../../term_dictionary/term_oauth_token.md) — RFC 6749 access/refresh token model; relevance: the note notes HTTP supports OAuth and the `--transport` flag while WebSocket supports neither, tying transport choice to the auth model.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — infrastructure wrapping an LLM with tools and execution environment; relevance: stdio servers are spawned as subprocesses by the harness (which sets `CLAUDE_PROJECT_DIR` in their environment), so the transport is a harness-managed integration surface.

### 4. `cc_mcp_server_management` (6 term notes)
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open AI-tool integration protocol; relevance: this note covers managing connected MCP servers (list/get/remove, dynamic updates, reconnection), so the term is the parent concept.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI tool; relevance: the note documents Claude Code's server-lifecycle commands (`claude mcp list/get/remove`, `/mcp`) and reconnection behavior.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — event-driven program flow; relevance: the "Push messages with channels" capability lets a server push CI/monitoring/chat events into the session via `claude/channel`, an event-driven integration the note introduces (full detail → B08B).
- [Skills](../../term_dictionary/term_skills.md) — packaged agent expertise; relevance: plugin-bundled MCP servers (covered here) are distributed alongside skills as part of a plugin's components, and the note's plugin-tool-naming scheme parallels skill `allowed-tools` references.
- [Subagent](../../term_dictionary/term_subagent.md) — delegated child agent with its own tool set; relevance: the note states the full `mcp__plugin_*` tool name is what you reference in a subagent's `tools` field, tying server management to subagent tool grants.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — LLM tool-invocation capability; relevance: the `/mcp` panel's tool-count display, the output-token warnings, and `list_changed` tool refresh all concern the tool calls a managed server exposes.

### 5. `cc_mcp_installation_scopes` (6 term notes)
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open AI-tool integration protocol; relevance: this note documents the three MCP installation scopes and their precedence, a Claude-Code-specific layer over the MCP server concept.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI tool; relevance: the note details where Claude Code stores scoped configs (`~/.claude.json` vs `.mcp.json`) and how it resolves duplicates.
- [Access Control](../../term_dictionary/term_access_control.md) — granting/denying requests to use information services; relevance: project scope gates teammate access via version-controlled `.mcp.json` with an approval prompt, an access-control mechanism over shared tools.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — designing systems that supply the right info/tools at the right time; relevance: choosing a scope decides which projects load which servers' tools, a context-provisioning decision this discipline covers.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — infrastructure wrapping an LLM with tools/config; relevance: scopes determine which servers the harness loads per project, part of its configuration layer.
- [Data Governance](../../term_dictionary/term_data_governance.md) — policies/roles/standards for managing data assets; relevance: the note's `${VAR}` expansion lets teams share `.mcp.json` while keeping secrets/machine-specific paths out of version control, a governance practice for shared config.

### 6. `cc_mcp_authentication` (7 term notes)
- [OAuth 2.0 Token](../../term_dictionary/term_oauth_token.md) — RFC 6749 access/refresh token model; relevance: this note's core subject is OAuth 2.0 for remote MCP servers — callback ports, client IDs/secrets, scope pinning, refresh — exactly what this term defines.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity before granting access; relevance: the note covers the full authentication surface for MCP servers (OAuth, static bearer headers, `headersHelper` for SSO/Kerberos), the identity-verification step this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open AI-tool integration protocol; relevance: the note documents how Claude Code authenticates to MCP servers and how Claude Code itself can run as an MCP server, both MCP-protocol operations.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI tool; relevance: the note details Claude Code's `/mcp` auth flow, `--callback-port`/`--client-id` flags, and `claude mcp serve` mode.
- [AgentCore Identity](../../term_dictionary/term_agentcore_identity.md) — inbound/outbound auth abstractions for agentic AI systems; relevance: the note's `headersHelper` and OAuth-on-behalf-of-user patterns address the same agent-identity challenge (an agent authenticating to external services as the user) this term frames.
- [AAA (Authentication, Authorization, Accounting)](../../term_dictionary/term_aaa.md) — an identity/access security framework for service communication; relevance: the note's `oauth.scopes` pinning to a security-approved subset is an authorization-scoping control of the kind AAA governs for service-to-service calls.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — control preventing server-side request forgery via untrusted URLs; relevance: the note's metadata-discovery override (`authServerMetadataUrl` must be `https://`) and per-user credential isolation are guardrails against the request-redirection/credential-leak risks this term addresses.

### 7. `cc_mcp_tool_search` (7 term notes)
- [Context Window](../../term_dictionary/term_context_window.md) — finite token memory an LLM processes per interaction; relevance: Tool Search exists to keep MCP context usage low by deferring tool definitions until needed, so the context-window budget is the constraint this whole note optimizes against.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open AI-tool integration protocol; relevance: the note covers MCP-specific features (deferred tools, @-mention resources, `/mcp__*` prompts, elicitation), all surfaced through connected MCP servers.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — LLM tool-invocation via structured calls; relevance: Tool Search changes when tool definitions load into context (deferred vs upfront), directly shaping the tool-use mechanism this term defines.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — supplying the right info/tools at the right time; relevance: deferring tool schemas and loading only what Claude needs is a textbook context-engineering optimization, the discipline this term names.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — the typed declarative record (name/description/schema) every callable tool registers under; relevance: Tool Search defers exactly these tool descriptors and truncates descriptions/server-instructions at 2KB, so the descriptor is the unit being searched and loaded.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI tool; relevance: the note documents Claude Code's `ENABLE_TOOL_SEARCH` settings, `ToolSearch`/`WaitForMcpServers` tools, and `alwaysLoad` exemption.
- [Structured Output](../../term_dictionary/term_structured_output.md) — constraining LLM generation to a predefined schema; relevance: MCP elicitation requests (covered here) show server-defined form fields whose schema constrains the user's structured response, mirroring the schema-constrained I/O this term covers.

### 8. `cc_managed_mcp_configuration` (7 term notes)
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open AI-tool integration protocol; relevance: this note is the admin reference for restricting which MCP servers users can connect to, so the term is the direct parent concept.
- [Access Control](../../term_dictionary/term_access_control.md) — granting/denying requests to use information services; relevance: the entire page is access control over MCP servers — fixed-set deployment, allowlists, denylists — the granting/denying this term defines.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny permission pattern where actions are blocked unless explicitly allowed; relevance: `managed-mcp.json` exclusive control and an empty/populated `allowedMcpServers` implement default-deny (nothing loads unless on the list), the pattern this term names.
- [Fine-Grained Access Control (FGAC)](../../term_dictionary/term_fgac.md) — row/column/cell-level data-access controls; relevance: matching servers by exact `serverUrl`/`serverCommand`/`serverName` with wildcard URL patterns is fine-grained, per-server access control of the kind this term describes.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI tool; relevance: the note details Claude Code's managed-settings precedence, system config paths, and the enterprise-policy errors users see.
- [DM Policy / Allowlist](../../term_dictionary/term_dm_policy.md) — per-channel security gate deciding whether an inbound sender may interact, via allowlist; relevance: the note's `allowedMcpServers`/`deniedMcpServers` evaluation (denylist-wins, allowlist-gates) is the same allowlist/denylist gate pattern this term implements for messaging adapters.
- [Data Governance](../../term_dictionary/term_data_governance.md) — org policies/roles/standards for managing data assets securely and compliantly; relevance: centrally controlling which MCP servers (and thus which external data flows) an organization permits is a data-governance enforcement this term frames, including the OTEL usage-monitoring it recommends.

## Section Coverage Map

```
mcp.md
├── intro (what MCP is / when to connect) ── → note 1 (cc_mcp_overview)
├── What you can do with MCP ─────────────── → note 1
├── Find and build MCP servers ───────────── → note 1 (Directory, trust warning → B16, mcp-server-dev → B09)
├── Installing MCP servers
│   ├── Option 1: HTTP server ───────────── → note 3 (cc_mcp_transports)
│   ├── Option 2: SSE server (deprecated) ── → note 3
│   ├── Option 3: local stdio server ─────── → note 3
│   ├── Option 4: WebSocket server ───────── → note 3
│   ├── Managing your servers ───────────── → note 4 (cc_mcp_server_management)
│   ├── Dynamic tool updates ────────────── → note 4
│   ├── Automatic reconnection ──────────── → note 4
│   ├── Push messages with channels ─────── → note 4 (intro; full detail → B08B channels.md)
│   └── Plugin-provided MCP servers ─────── → note 4 (intro; full detail → B09A plugins-reference.md)
├── MCP installation scopes ──────────────── → note 5 (cc_mcp_installation_scopes)
│   ├── Local / Project / User scope ────── → note 5
│   ├── Scope hierarchy and precedence ──── → note 5
│   └── Environment variable expansion ──── → note 5
├── Practical examples (Sentry/GitHub/PG) ── → note 2 (cc_mcp_quickstart)
├── Authenticate with remote MCP servers ─── → note 6 (cc_mcp_authentication)
│   ├── Fixed OAuth callback port ───────── → note 6
│   ├── Pre-configured OAuth credentials ── → note 6
│   ├── Override OAuth metadata discovery ── → note 6
│   ├── Restrict OAuth scopes ───────────── → note 6
│   └── Dynamic headers (headersHelper) ──── → note 6
├── Add MCP servers from JSON configuration → note 3
├── Import MCP servers from Claude Desktop ── → note 3
├── Use MCP servers from Claude.ai ───────── → note 6
├── Use Claude Code as an MCP server ─────── → note 6
├── MCP output limits and warnings ───────── → note 4
│   └── Raise the limit for a specific tool → note 4
├── Respond to MCP elicitation requests ──── → note 7 (cc_mcp_tool_search)
├── Use MCP resources (@ mentions) ───────── → note 7
│   └── Reference MCP resources ─────────── → note 7
├── Scale with MCP Tool Search ───────────── → note 7
│   ├── How it works ────────────────────── → note 7
│   ├── For MCP server authors ──────────── → note 7
│   ├── Configure tool search ───────────── → note 7
│   └── Exempt a server from deferral ───── → note 7
├── Use MCP prompts as commands ──────────── → note 7
│   └── Execute MCP prompts ─────────────── → note 7
└── Managed MCP configuration (pointer) ──── → note 8 (cc_managed_mcp_configuration)
mcp-quickstart.md
├── Before you begin ─────────────────────── → note 2
├── Add and verify a server ──────────────── → note 2
├── Where servers are saved ──────────────── → note 5 (config-on-disk detail) + note 2 (intro)
│   └── Find your configuration on disk ──── → note 5
├── Change server scope ──────────────────── → note 5
│   ├── Use a server in all your projects ── → note 5
│   └── Share a server with your team ────── → note 5
├── Additional MCP server examples ───────── → note 2
│   ├── Add a local server (Playwright) ──── → note 2
│   └── Connect a server that requires sign-in → note 2 (→ note 6 for auth detail)
├── Edit .mcp.json directly ──────────────── → note 3 (JSON entry) + note 5 (scope)
├── Connect from other surfaces ──────────── → note 2 (→ B12 surfaces)
├── Troubleshooting ──────────────────────── → note 2
└── Next steps (links) ───────────────────── → notes 1/8 (links)
managed-mcp.md
├── Choose a pattern ─────────────────────── → note 8 (cc_managed_mcp_configuration)
├── Exclusive control with managed-mcp.json → note 8
│   ├── Authenticate with per-user credentials → note 8 (→ note 6 for the auth mechanisms)
│   ├── Validate the configuration ──────── → note 8
│   ├── Disable MCP entirely ────────────── → note 8
│   └── Allow claude.ai connectors ──────── → note 8
├── Policy-based control allow/denylists ─── → note 8
│   ├── Match servers by URL/command/name ── → note 8
│   ├── How a server is evaluated ───────── → note 8
│   ├── Example configuration ───────────── → note 8
│   └── Restrict allowlist to managed only ─ → note 8
├── How restrictions appear to users ─────── → note 8
├── Monitor MCP usage ────────────────────── → note 8 (intro; OTEL schema → B15B monitoring-usage.md)
├── Configuration summary ────────────────── → note 8
└── Related resources (links) ────────────── → note 8 (links: → B14B admin-setup, B16 security)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| mcp.md (6,822w, 41 code blocks, 14 H2) | notes 1,3,4,5,6,7 + pointer to note 8 | far over 2,500w / 6-code caps; distinct BBs — concept (what-it-is / scopes / tool-search) vs procedure (transports / management / auth); channels+plugins owned by B08B/B09 (linked, not duplicated). |
| mcp.md: Installing MCP servers (9 code blocks alone) | transports (note 3) vs management (note 4) | the four-transport "how to add" is distinct from the lifecycle/management/output operations; together they would exceed the 6-code cap, so split by sub-task. |
| mcp.md: Practical examples (13 code blocks) | folded into note 2 (cc_mcp_quickstart), one representative block per service | the worked Sentry/GitHub/PostgreSQL examples are repetitive CLI variants of the quickstart flow; co-locating with the walkthrough avoids a thin examples-only note and keeps note 2 ≤6 code by showing one block per service + prose. |
| mcp-quickstart.md (3,072w) | note 2 (procedure) + scope detail → note 5 | the connect/verify/use walkthrough is one procedure; the config-on-disk/scope content overlaps mcp.md scopes and is consolidated in note 5 to avoid duplication. |
| managed-mcp.md (2,919w) | note 8 (single procedure) | cohesive admin/policy procedure; under caps as one note (~650w, ≤6 code by keeping one representative JSON block + tables). |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_mcp_overview | concept | 450 | 1 | ✅ |
| 2 | cc_mcp_quickstart | procedure | 600 | 6 | ✅ |
| 3 | cc_mcp_transports | procedure | 550 | 5 | ✅ |
| 4 | cc_mcp_server_management | procedure | 550 | 4 | ✅ |
| 5 | cc_mcp_installation_scopes | concept | 500 | 3 | ✅ |
| 6 | cc_mcp_authentication | procedure | 600 | 6 | ✅ |
| 7 | cc_mcp_tool_search | concept | 600 | 4 | ✅ |
| 8 | cc_managed_mcp_configuration | procedure | 650 | 4 | ✅ |

No note approaches the word/line caps. The source is code-heavy (41 blocks in mcp.md), so every note is held to ≤6 code blocks by keeping one representative block per concept and folding repeated CLI/JSON variants into prose — verified per note above. No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_mcp_overview cc_mcp_quickstart cc_mcp_transports cc_mcp_server_management cc_mcp_installation_scopes cc_mcp_authentication cc_mcp_tool_search cc_managed_mcp_configuration"
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

Single phase (8 notes, all P1). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 8 notes RECEIVES ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | DB in-degree ≥1 confirmed for all 8 notes after inlinks applied | sqlite3 in-degree query on `note_links` |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 8 rows** under an "MCP" cluster + increments the BB-distribution counts
(concept ×3, procedure ×5). The entry-point back-link into each note is added at finalization (G7/G8).

## Undigested Terms Plan (Step 2d)

b08a creates **0 new `term_dictionary` captures** — MCP-vocabulary terms are covered by a b08a `cc_`
concept/procedure note, an existing substantive term note (link), or their home sub-plan (Pattern B).
**Dedup performed across BOTH `term_dictionary/` AND `resources/documentation/`** (master Dedup Policy): the
existing `term_mcp` term note is substantive → LINKED, never recreated as a `cc_` note.

| Term surfaced in pages | Disposition |
|---|---|
| MCP / Model Context Protocol | link `term_mcp` (exists, substantive) — also digested as `cc_mcp_overview` doc concept |
| MCP server / transport (HTTP/SSE/stdio/WebSocket) | note 3 `cc_mcp_transports` (doc concept; no term note — too narrow/product-specific) |
| Installation scope (local/project/user) | note 5 `cc_mcp_installation_scopes` (doc concept) |
| Tool Search / `tool_reference` / `alwaysLoad` | note 7 `cc_mcp_tool_search` (doc concept) |
| OAuth / callback port / client ID / scopes | link `term_oauth_token`, `term_authentication`, `term_aaa` (exist); mechanics → note 6 |
| `headersHelper` / dynamic headers | note 6 `cc_mcp_authentication` (doc procedure) |
| MCP resources / @ mentions / MCP prompts / elicitation | note 7 (doc concept); elicitation schema links `term_structured_output` (exists) |
| Channel / `claude/channel` push | link to B08B (`channels.md`); intro only in note 4 — Channel term owned by B08B per master |
| Plugin-provided MCP server / `mcp__plugin_*` | link to B09A (`plugins-reference.md`); intro only in note 4 — Plugin term owned by B09A per master |
| `managed-mcp.json` / allowedMcpServers / deniedMcpServers / allowManagedMcpServersOnly | note 8 (doc procedure); links `term_access_control`, `term_deny_first`, `term_fgac`, `term_dm_policy` (exist) |
| Prompt injection (trust warning) | link to B16 (`security.md`); links `term_owasp_llm`, `term_jailbreak` (exist) — owned by B16 per master |
| Elicitation hook | link to B07A (`hooks.md`) — Hook owned by B07A/B07B per master |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 3 pages scanning emphasis/tables/captions/code
for newly-surfaced terms. Candidates considered: "WebSocket transport", "elicitation", "Client ID Metadata
Document (CIMD)", "Dynamic Client Registration", "`tool_reference` blocks". All are product/protocol
mechanics digested inline in the `cc_` notes above, not cross-cutting vocabulary warranting a `term_dictionary`
capture, and none duplicate an existing term. **0 new B08A `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B08A authors zero term notes, so there are no
new slugs to audit. The collision check that matters here (do the MCP concepts duplicate existing notes?)
was performed across `term_dictionary/` AND `documentation/`: `term_mcp`, `term_function_calling`,
`term_oauth_token`, `term_authentication`, `term_aaa`, `term_access_control`, `term_deny_first`, `term_fgac`,
`term_owasp_llm`, `term_context_window`, `term_agent_harness`, `term_claude_code` all exist → linked, not
recreated. No existing `cc_mcp_*` doc note exists in `documentation/claude_code/` (dir not yet created),
so no doc-note duplication.

## Term-Note Authoring Requirements

**N/A for b08a** — it authors zero term notes (all routed above). The full requirements (YAML, file
naming, required H2 sections, multi-source research, cross-domain Related Terms, glossary template,
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim from source; keep each note ≤6 code blocks (fold repeated CLI/JSON variants into prose). One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 inbound in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_mcp.md` | notes 1, 3, 5, 8 | MCP term → CC docs overview / transports / scopes / managed config (its canonical Claude Code treatment) |
| `term_dictionary/term_oauth_token.md` | note 6 | OAuth-token term → CC MCP authentication flow |
| `term_dictionary/term_function_calling.md` | note 7 | tool-use term → CC MCP Tool Search (deferred tool loading) |
| `term_dictionary/term_access_control.md` | note 8 | access-control term → CC managed MCP allowlist/denylist |
| `term_dictionary/term_claude_code.md` | notes 1, 2 | Claude Code term → MCP overview + quickstart |
| `documentation/org_docs/org_concepts_plugins_claude_code.md` | note 1 | Claude Code plugins/concepts doc → MCP overview |

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above (verify in-degree ≥1 per note — G7/G8); queue the 8 rows for `entry_claude_code_docs.md` under an "MCP" cluster; `/tessellum-check-broken-links`.
- Cross-link to siblings once they land: B08B channels (from note 4), B09A plugins (from note 4), B16 security/prompt-injection (from note 1), B20A SDK MCP (from notes 3/6), B15B monitoring (from note 8).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY** — see Review Sign-Off below (9/9) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B08A, 2026-06-13)

- **Source re-read (Step 2)**: all 3 pages re-read in full from `inbox/claude_code_docs/`; measured words confirm the master's figures (mcp 6,822 · mcp-quickstart 3,072 · managed-mcp 2,919 = 12,813). Code blocks measured (mcp 41, mcp-quickstart 4, managed-mcp 4) — drove the transports/management split and the ≤6-code-per-note discipline. No >1.5× under-estimate; no re-split forced beyond the documented ones.
- **Notes**: 8 (concept 3, procedure 5) — matches master estimate. Splits: mcp.md → 6 notes + a pointer to the admin note; Installing-MCP-servers split into transports (note 3) vs management (note 4) to stay under the 6-code cap; practical examples folded into the quickstart (note 2); managed-mcp.md → one cohesive admin note (note 8).
- **Per-Note Related Notes Mapping (Step 8)**: authored to the **≥6 relevancy-selected term-note** standard — 6-7 term notes per note (24 distinct `term_dictionary/` terms), each with a per-link what-it-is + relevance-to-this-note statement; **all DB-verified on disk, 0 ghosts (G5 PASS)**; relpaths `../../term_dictionary/`. Sibling `cc_*` cross-links (notes 4→B08B/B09, 1→B16, etc.) kept as planned forward refs.
- **Step 2d new-term scan**: candidates considered (WebSocket transport, elicitation, CIMD, Dynamic Client Registration, `tool_reference`); all product/protocol mechanics digested inline, none cross-cutting vocabulary, none duplicating existing terms → **0 new B08A term captures**.
- **Dedup (master policy, both dirs)**: `term_mcp` (and 11 other existing terms) substantive → LINKED not recreated; no existing `cc_mcp_*` doc note → no doc-note duplication.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), code-block-budget column in Density Re-Assessment, G7/G8 gate rows.
- **28-item checklist**: PASS (term-note items N/A — B08A authors no terms; entry-point + undigested-terms inherited from master).
- **Status**: augmented and self-reviewed; set to `ready` after the 9-checkpoint self-review below passed 9/9.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP1 | Related Notes step | ✅ PASS | Per-Note Related Notes Mapping present; **≥6 relevancy-selected term notes/note** (6–7 each, per-link relevancy stated), all DB-verified on disk (0 ghosts). Entry-point back-link deferred to finalization (hub `entry_claude_code_docs.md` created then). |
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability (inbound in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B08A contributes 8 rows under an "MCP" cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches existing `documentation/` notes exactly; body uses `## Overview` / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer convention from the master Format Definition. |
| CP6 | Borderline density → split | ✅ PASS | All 8 notes 450–650w; the code-heavy source (41 blocks) drove an explicit ≤6-code-per-note split (transports vs management; examples folded into quickstart). None borderline after split. |
| CP7 | Source words measured (not guessed) | ✅ PASS | Spot-check: mcp measured 6,822 = master 6,822; mcp-quickstart 3,072 = 3,072; managed-mcp 2,919 = 2,919. Within ±0%. Code blocks measured per section to drive splits. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B08A authors 0 term notes; Undigested Terms Plan routes MCP vocabulary (dedup across BOTH term_dictionary AND documentation/); Authoring Requirements inherited from master. |
| CP9 / CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); MCP-concept collision check documented across both dirs (12 existing terms linked, not recreated; no existing `cc_mcp_*` doc note). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.
