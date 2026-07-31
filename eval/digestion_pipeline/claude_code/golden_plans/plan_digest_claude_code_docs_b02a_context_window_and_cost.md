---
title: Sub-Plan B02A — Claude Code Docs: Context Window & Cost
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["context-window", "prompt-caching", "costs"]
---

# Sub-Plan B02A: Context Window & Cost

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 3 pages that cover the resource economics of a Claude Code session: what fills the **context window**
and what each load costs, how **prompt caching** keeps repeated context fast/cheap (and which actions
invalidate it), and how to **track and reduce token cost**. P1 (Phase A) — every later sub-plan that
discusses extensions references the per-feature context-cost and caching vocabulary defined here, so it
runs early. The `context-window` page is mostly a large embedded React simulation (JSX, not prose); the
digest captures only the prose breakdown and the two reference tables, never the simulation source.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 3 pages, 12,414 raw words (≈6,640 prose words
after excluding the context-window JSX component). **Planned: 8 notes.**

## Content Strategy

- **Prioritize**: the context-cost-per-feature and cache-invalidation vocabulary every extension sub-plan
  (B06 skills, B07 hooks, B08 MCP, B10 subagents/teams) links back to (P1).
- **Group**: split the large `prompt-caching` page (3,763w, 9 H2 / 19 H3) by concept boundary — cache
  *mechanism* (prefix/layers) vs *invalidating* actions vs *cache-preserving* actions vs *lifetime/scope*.
  Split `costs` (2,103w) by BB — cost *tracking* (procedure) vs cost *reduction* (argument). Keep the small
  `context-window` prose as an anatomy note + a compaction-survival note.
- **Skip / link-out (own other sub-plans)**: extended-thinking/effort detail → B03B (`model-config`);
  fast-mode → B04A (`fast-mode`); permission deny rules → B05A (`permissions`); MCP tool search →
  B08A (`mcp`); hooks reference → B07A (`hooks`); memory/CLAUDE.md → B02B (`memory`); sessions/resume →
  B02B (`sessions`); checkpointing/`/rewind` → B02B (`checkpointing`); LLM gateway / Bedrock-Vertex cache
  location → B14A; SDK cost-tracking → B21A. These are referenced via links, never duplicated.
- **Dedup**: `term_prompt_caching` (a Bedrock/generic concept term) and `term_context_window`,
  `term_compaction` exist → **link, do not recreate** (see Undigested Terms Plan). The `cc_` doc notes
  document Claude Code's *product behavior* (its automatic caching, its compaction survival rules), a
  distinct same-concept-different-sense from the generic terms.

## Source Pages (Measured 2026-06-13, re-read)

All 3 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| context-window | /context-window | 6,548 (≈774 prose) | 0¹ | 5 | 0 | model/concept |
| prompt-caching | /prompt-caching | 3,763 | 0 | 9 | 19 | concept |
| costs | /costs | 2,103 | 4 | 5 | 14 | procedure/argument |

> ¹ `context-window.md` lines 9–1569 are a single embedded React/JSX simulation component (`export const
> ContextWindow = …`), NOT documentation prose. `grep -c '^```'` counts 0 fenced blocks. The digest uses
> only the prose at L1571–1627 (≈774 words) plus the two markdown tables (compaction survival; the
> takeaway facts the simulation encodes are paraphrased, the JSX is never transcribed).

> **H2 lists (document order):**
> - **context-window**: What the timeline shows · What survives compaction · When your context fills up · Check your own session · Related resources
> - **prompt-caching**: How the cache is organized (H3 Where the cache lives) · Actions that invalidate the cache (H3 Switching models, Changing effort level, Turning on fast mode, Connecting/disconnecting an MCP server, Enabling/disabling a plugin, Denying an entire tool, Compacting the conversation, Upgrading Claude Code) · Actions that keep the cache (H3 Editing files, Editing CLAUDE.md mid-session, Changing output style, Changing permission mode, Invoking skills and commands, Running /recap, Rewinding the conversation) · Cache lifetime (H3 On a Claude subscription, On an API key or third-party provider, Override the TTL) · Cache scope · Check cache performance · Subagents and the cache · Disable prompt caching · Related resources
> - **costs**: Track your costs (H3 Using the /usage command) · Managing costs for teams (H3 Rate limit recommendations, Agent team token costs) · Reduce token usage (H3 Manage context proactively, Choose the right model, Reduce MCP server overhead, Install code intelligence plugins, Offload processing to hooks and skills, Move instructions from CLAUDE.md to skills, Adjust extended thinking, Delegate verbose operations to subagents, Manage agent team costs, Write specific prompts, Work efficiently on complex tasks) · Background token usage · Understanding changes in Claude Code behavior

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **8 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_context_window_anatomy.md` | model | context-window: What the timeline shows; Check your own session | 500 | What fills the window (system prompt, auto memory, CLAUDE.md, skill descriptions, MCP names, file reads, rules, hooks, your prompts); auto vs visible-in-terminal; `/context` + `/memory` to inspect. Links `term_context_window`; 200K vs 1M variant → B03B. |
| 2 | `cc_what_survives_compaction.md` | concept | context-window: What survives compaction; When your context fills up | 450 | Per-mechanism survival table (system prompt re-injected, CLAUDE.md/memory re-injected from disk, path-rules lost, invoked skills capped 5K/25K); auto-compaction at the limit; `/compact` focus, `/clear`, subagent delegation. Links `term_compaction`. |
| 3 | `cc_prompt_caching_mechanism.md` | concept | prompt-caching: intro; How the cache is organized | 500 | Prefix matching (exact, recomputes everything after a change); the 3-layer ordering (system prompt / project context / conversation); model + effort level as cache-key dimensions. Links `term_prompt_caching`. |
| 4 | `cc_cache_invalidation_actions.md` | concept | prompt-caching: Actions that invalidate the cache (8 H3) | 600 | The 8 actions that cause an uncached turn: switch model, change effort, fast mode on, connect/disconnect MCP server, enable/disable plugin, deny a whole tool, compact, upgrade. Per-action "why". Detail link-outs to B03B/B04A/B05A/B08A. |
| 5 | `cc_cache_preserving_actions.md` | concept | prompt-caching: Actions that keep the cache (7 H3); Subagents and the cache; Check cache performance; Disable prompt caching | 550 | Cache-safe actions (file edits, mid-session CLAUDE.md/output-style edits — and why those edits don't apply, permission mode, skills/commands, `/recap`, `/rewind`); subagent builds its own cache, fork inherits parent's; `cache_*_input_tokens` fields; disable env vars. |
| 6 | `cc_cache_lifetime_and_scope.md` | concept | prompt-caching: Cache lifetime (3 H3); Cache scope | 450 | TTL (5-min default vs 1-hour); per-auth TTL selection (subscription auto-1h, API/Bedrock/Vertex 5m, `ENABLE_PROMPT_CACHING_1H`, `FORCE_PROMPT_CACHING_5M`); machine+directory scope (worktrees miss each other; parallel same-dir sessions share). |
| 7 | `cc_cost_tracking.md` | procedure | costs: intro/benchmarks; Track your costs; Managing costs for teams; Background token usage; Understanding changes | 600 | How CC bills (API tokens); `/usage` session block + plan breakdown; team controls (workspace spend limits, `/usage-credits`, the auto "Claude Code" workspace, rate-limit TPM/RPM table, agent-team scaling); background token usage; version check. |
| 8 | `cc_reduce_token_usage.md` | argument | costs: Reduce token usage (11 H3) | 650 | The strategy set: manage context proactively (`/clear`, custom compaction), right model, reduce MCP overhead, code-intelligence plugins, offload to hooks/skills, CLAUDE.md→skills, adjust extended thinking, delegate to subagents, agent-team cost (~7×), specific prompts, plan-mode/course-correct. One PreToolUse filter-hook example (≤2 code blocks). |

**Estimate: 8 notes** — model ×1 (note 1), concept ×4 (notes 2,3,4,5,6 → concept 5), procedure ×1 (note 7), argument ×1 (note 8). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 3 (12,414 raw / ≈6,640 prose words). New `cc_` notes: 8. New `term_dictionary` notes: 0 (Pattern B — CC vocab digested as `cc_` doc notes; existing terms linked).
- Est. total digest words: ~4,300 (avg ~535/note). Code blocks: ~2 total (the one PreToolUse filter-hook example in note 8, optionally the `/usage` text block paraphrased; cap ≤6/note honored).
- **Building Block Distribution**: model ×1 (note 1) · concept ×5 (notes 2,3,4,5,6) · procedure ×1 (note 7) · argument ×1 (note 8). No empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links (notes 1–8 cross-link) + the entry-point back-link (`entry_claude_code_docs.md`, at

### 1. `cc_context_window_anatomy` (7 term notes)
- [Context Window](../../term_dictionary/term_context_window.md) — The token-limited buffer this note anatomizes; the note enumerates exactly what consumes that buffer (system prompt, memory, CLAUDE.md, file reads, hooks), making the term the central concept it documents.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The note's whole point is what to put in (and keep out of) the window; deciding what loads automatically vs on-demand is the discipline of context engineering that this term names.
- [Tokenization](../../term_dictionary/term_tokenization.md) — Every line item in the note is measured in tokens (system prompt 4,200, file read 2,400, etc.); tokenization is the unit-of-account the note's whole accounting rests on.
- [Compaction](../../term_dictionary/term_compaction.md) — The note ends the timeline at `/compact`, which fires when the anatomized loads fill the window; compaction is the mechanism that reclaims the space this note shows being consumed.
- [Subagent](../../term_dictionary/term_subagent.md) — The note's biggest context-saving move is delegating large file reads to a subagent whose reads fill its own window, not the main one — the isolation behavior this term defines.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — Auto memory (MEMORY.md), one of the always-loaded startup items the note tallies (first 200 lines / 25KB), is the concrete agentic-memory mechanism the note charges to context.
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents Claude Code's own session context window — what its harness loads at startup and as it works — so the product term anchors the subject.

### 2. `cc_what_survives_compaction` (6 term notes)
- [Compaction](../../term_dictionary/term_compaction.md) — This note IS the per-mechanism rulebook for what compaction keeps vs drops, so the compaction term is its definitional anchor.
- [Context Window](../../term_dictionary/term_context_window.md) — Compaction exists to fit a long history back inside the context window; the note frames every survival rule as a response to the window filling up.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The note's actionable advice (drop `paths:` frontmatter or move rules to root CLAUDE.md so they persist; put key instructions at the top of SKILL.md) is context engineering for survival across compaction.
- [Skills](../../term_dictionary/term_skills.md) — The note gives skills a special survival rule (invoked bodies re-injected, capped at 5,000 tokens/skill and 25,000 total, oldest dropped first, truncated from the start), so skills are a first-class subject here.
- [Subagent](../../term_dictionary/term_subagent.md) — Among the "when context fills up" remedies the note lists, delegating large reads to a subagent keeps content out of the main window entirely, avoiding the need to compact it.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The survival behavior documented is Claude Code's automatic and `/compact` summarization implementation, so the product term grounds the note.

### 3. `cc_prompt_caching_mechanism` (7 term notes)
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — This note documents Claude Code's use of prompt caching; the term defines the generic prefix-caching mechanism (cached KV of repeated prefixes billed at reduced rates) the note builds on.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — The note explains that the API reuses already-processed prefix work rather than recomputing it — that reuse is the cached key-value attention state this term defines.
- [Caching](../../term_dictionary/term_caching.md) — The note's prefix-match-against-recently-processed-content model is a direct application of the general caching pattern (store computed results, serve on a key match) this term defines.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Ordering request content so rarely-changing layers (system prompt, project context) come first to maximize prefix reuse is exactly the prompt/context-engineering choice this term covers.
- [Tokenization](../../term_dictionary/term_tokenization.md) — Cache hits and misses are measured in input tokens reprocessed vs reused; tokenization is the unit the note's cost/speed argument is denominated in.
- [Gist Token](../../term_dictionary/term_gist_token.md) — Gist tokens are a complementary prefix-compression technique for reusing fixed context; the note's prefix-reuse goal is the same problem gisting addresses, contextualizing the caching approach.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents how Claude Code orders its request (system prompt / project context / conversation) for cache friendliness, a product-specific behavior the term anchors.

### 4. `cc_cache_invalidation_actions` (7 term notes)
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — This note enumerates the actions that bust Claude Code's prompt cache; the prompt-caching term defines the mechanism being invalidated.
- [Cache Invalidation](../../term_dictionary/term_cache_invalidation.md) — The note IS a catalog of cache-invalidation triggers (model switch, effort change, MCP toggle, compaction, upgrade); the term names the general problem the note instantiates for Claude Code.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — Each invalidating action forces a full re-read of the conversation history with no cache hits — i.e., the cached KV prefix is discarded and recomputed, the term's core object.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Connecting/disconnecting an MCP server is one of the eight invalidation triggers; whether it invalidates depends on deferred vs prefix-loaded tools, an MCP-specific behavior the term grounds.
- [Compaction](../../term_dictionary/term_compaction.md) — Compacting the conversation is one of the listed invalidation actions (it replaces history with a shorter summary that no longer shares the old prefix), so compaction is directly in scope.
- [Subagent](../../term_dictionary/term_subagent.md) — The note contrasts a subagent (own cache, no parent invalidation) with the invalidating actions; subagents are the cache-isolation alternative referenced against the invalidation list.
- [Claude Code](../../term_dictionary/term_claude_code.md) — All eight invalidation behaviors are Claude Code product behaviors (the `/model`, `/effort`, `/compact`, plugin, deny-rule, upgrade flows), so the product term anchors the note.

### 5. `cc_cache_preserving_actions` (6 term notes)
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — This note lists the actions that keep Claude Code's cache warm; the term defines the cache being preserved.
- [Cache Invalidation](../../term_dictionary/term_cache_invalidation.md) — The note is the inverse-list companion to cache invalidation — actions that append rather than alter the prefix — so the invalidation term frames the contrast the note draws.
- [Subagent](../../term_dictionary/term_subagent.md) — The note's "Subagents and the cache" section explains a subagent builds its own cache (5-min TTL, no parent disruption) while a fork inherits the parent's prefix — core subagent caching behavior.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — The note's `cache_read_input_tokens` / `cache_creation_input_tokens` performance fields measure cached KV prefix reuse vs recomputation, the term's subject.
- [Caching](../../term_dictionary/term_caching.md) — The cache-safe actions (append-only edits, `/rewind` reading an earlier warm entry) are general caching behaviors (hit on unchanged key, append without invalidating) this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents why Claude Code's mid-session CLAUDE.md/output-style edits are cache-safe but don't apply, and the disable env vars — product-specific behaviors the term anchors.

### 6. `cc_cache_lifetime_and_scope` (6 term notes)
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — This note documents the TTL and scope of Claude Code's prompt cache; the term defines the caching mechanism whose lifetime and boundaries it details.
- [Eviction Policy](../../term_dictionary/term_eviction_policy.md) — Cache entries expiring after a period of inactivity (TTL reset on each hit) is a time-based eviction policy; the term names the general class of "when does a cache entry get dropped" rule the note specifies.
- [Caching](../../term_dictionary/term_caching.md) — TTL, warm-vs-cold entries, and scope (which requests share a cache) are foundational caching concepts; the note applies them to Claude Code, so the general term grounds it.
- [Cache Invalidation](../../term_dictionary/term_cache_invalidation.md) — TTL expiry is the passive counterpart to active invalidation; the note ties "first turn after stepping away is slow" to expiry, the time-driven side of the invalidation term.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — The cached prefix that expires after the TTL is the stored KV attention state; the note's "recompute the full input" on a cold cache is KV recomputation, the term's object.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Machine+directory scoping (worktrees miss each other; parallel same-dir sessions share), per-auth TTL selection, and the override env vars are Claude Code product behaviors the term anchors.

### 7. `cc_cost_tracking` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents Claude Code's own cost model (API-token billing, `/usage`, the auto "Claude Code" workspace), so the product term is its subject.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — The note's team-management core is the TPM/RPM per-user rate-limit recommendation table and org-level rate-limit caps; the term defines the throttling concept those recommendations configure.
- [Tokenization](../../term_dictionary/term_tokenization.md) — Costs are charged "by API token consumption" and the `/usage` breakdown is in tokens; tokenization is the billing unit the note tracks throughout.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — The "Agent team token costs" subsection explains token usage scales with the number of active teammates (each its own context window) — the multi-agent fan-out cost the term frames.
- [Observability of Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — `/usage` attributing recent usage to skills/subagents/plugins/MCP servers, plus the OpenTelemetry cost export, is agent-system observability — the term's exact subject applied to cost.
- [Bedrock](../../term_dictionary/term_bedrock.md) — The note states Claude Code sends no cost metrics on Bedrock/Vertex/Foundry and points to LiteLLM for spend tracking; Bedrock is the provider boundary the team-cost guidance hinges on.
- [Inference Profile](../../term_dictionary/term_inference_profile.md) — On Bedrock the workspace/profile is how cost and rate limits are attributed; the inference-profile term grounds the cloud-provider cost-attribution context the note describes.

### 8. `cc_reduce_token_usage` (7 term notes)
- [Context Window](../../term_dictionary/term_context_window.md) — The note's thesis is "token costs scale with context size"; every strategy (clear, right model, offload, delegate) is about keeping the context window small, the term's subject.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The whole note is a context-engineering playbook (move CLAUDE.md to skills, preprocess with hooks, write specific prompts, delegate verbose reads) — the discipline this term names.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — The "Adjust extended thinking" strategy tunes the reasoning/thinking-token budget (effort level, `MAX_THINKING_TOKENS`); extended thinking is the chain-of-thought reasoning whose cost the note trades off.
- [Inference Scaling Law](../../term_dictionary/term_inference_scaling_law.md) — The thinking-budget trade-off (more reasoning tokens improve hard tasks but cost more) is exactly the test-time/inference-compute scaling relationship this term formalizes.
- [Subagent](../../term_dictionary/term_subagent.md) — "Delegate verbose operations to subagents" is a primary cost strategy — verbose output stays in the subagent's context, only a summary returns; the term defines that isolation.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — The "Manage agent team costs" strategy notes agent teams use ~7× more tokens (each teammate its own window); the multi-agent cost behavior the term frames.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — The note credits automatic prompt caching with reducing cost for repeated content (system prompts) as a built-in optimization beneath the manual strategies; the term defines that mechanism.

## Section Coverage Map

```
context-window.md
├── (embedded React simulation L9–1569) ── → NOT digested (JSX component, not prose); facts paraphrased in note 1
├── intro prose (L1571) ────────────────── → note 1 (cc_context_window_anatomy)
├── What the timeline shows ────────────── → note 1
├── What survives compaction (table) ───── → note 2 (cc_what_survives_compaction)
├── When your context fills up ─────────── → note 2 (→ B02B memory/sessions for /clear, subagent → note 1)
├── Check your own session (/context,/memory) → note 1
└── Related resources (cards) ──────────── → notes 1/2 (links) + link-out (features-overview B01A, memory B02B, sub-agents B10A, best-practices B01B)
prompt-caching.md
├── intro + disable pointer ────────────── → note 3 (cc_prompt_caching_mechanism)
├── How the cache is organized (layers) ── → note 3
│   └── Where the cache lives ──────────── → note 6 (provider cache location; Bedrock/Vertex/gateway → B14A link-out)
├── Actions that invalidate the cache ──── → note 4 (cc_cache_invalidation_actions)
│   ├── Switching models ───────────────── → note 4 (detail → B03B model-config)
│   ├── Changing effort level ──────────── → note 4 (detail → B03B model-config)
│   ├── Turning on fast mode ───────────── → note 4 (detail → B04A fast-mode)
│   ├── Connecting/disconnecting MCP ───── → note 4 (detail → B08A mcp)
│   ├── Enabling/disabling a plugin ────── → note 4 (detail → B09A plugins)
│   ├── Denying an entire tool ─────────── → note 4 (detail → B05A permissions)
│   ├── Compacting the conversation ────── → note 4 (→ note 2)
│   └── Upgrading Claude Code ──────────── → note 4 (→ B17 setup auto-update)
├── Actions that keep the cache ────────── → note 5 (cc_cache_preserving_actions)
│   ├── Editing files / CLAUDE.md / output style → note 5 (CLAUDE.md/output-style detail → B02B/B06)
│   ├── Changing permission mode ───────── → note 5 (→ B05A permission-modes)
│   ├── Invoking skills and commands ───── → note 5 (→ B06)
│   ├── Running /recap ─────────────────── → note 5 (→ B04A interactive-mode)
│   └── Rewinding the conversation ─────── → note 5 (→ B02B checkpointing)
├── Cache lifetime (+ subscription/API/override) → note 6 (cc_cache_lifetime_and_scope)
├── Cache scope ────────────────────────── → note 6
├── Check cache performance (token fields) → note 5
├── Subagents and the cache ────────────── → note 5 (→ B10A sub-agents)
├── Disable prompt caching (env vars) ──── → note 5
└── Related resources (cards) ──────────── → notes 3/5 (links) + link-out
costs.md
├── intro + per-dev benchmark figures ──── → note 7 (cc_cost_tracking)
├── Track your costs (/usage) ──────────── → note 7
├── Managing costs for teams ───────────── → note 7
│   ├── Rate limit recommendations (table) → note 7
│   └── Agent team token costs ─────────── → note 7 (→ B10A agent-teams)
├── Reduce token usage (11 strategies) ─── → note 8 (cc_reduce_token_usage)
│   ├── Manage context proactively ─────── → note 8
│   ├── Choose the right model ──────────── → note 8 (→ B03B model-config)
│   ├── Reduce MCP server overhead ─────── → note 8 (→ B08A mcp)
│   ├── Code intelligence plugins ──────── → note 8 (→ B09 discover-plugins)
│   ├── Offload to hooks and skills ────── → note 8 (→ B07A hooks / B06 skills)
│   ├── Move CLAUDE.md to skills ────────── → note 8 (→ B02B memory / B06)
│   ├── Adjust extended thinking ───────── → note 8 (detail → B03B model-config)
│   ├── Delegate verbose ops to subagents → note 8 (→ B10A)
│   ├── Manage agent team costs (~7×) ──── → note 8 (→ B10A)
│   ├── Write specific prompts ──────────── → note 8
│   └── Work efficiently (plan/rewind) ─── → note 8 (→ B05A plan mode / B02B rewind)
├── Background token usage ─────────────── → note 7
└── Understanding changes in CC behavior ─ → note 7
```
No orphaned sections (the React simulation is explicitly out-of-scope source code, not a doc section).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| context-window (≈774 prose w, 5 H2 + JSX sim) | notes 1,2 + link-outs | the simulation is source code, not prose; the prose splits cleanly into anatomy (model: what loads/costs) vs compaction survival (concept: survival rules). |
| prompt-caching (3,763w >2500, 9 H2 / 19 H3) | notes 3,4,5,6 | exceeds density cap; four distinct concepts — cache *mechanism* (prefix/layers), *invalidating* actions, *preserving* actions+perf+subagent, *lifetime/scope* — each its own concept note ≤600w. |
| costs (2,103w, 5 H2 / 14 H3) | notes 7,8 | split by BB: cost *tracking* (procedure — `/usage`, team controls, rate-limit table) vs cost *reduction* (argument — the 11 when-to-do-X strategies). |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_context_window_anatomy | model | 500 | 0 | ✅ |
| 2 | cc_what_survives_compaction | concept | 450 | 0 (1 md table) | ✅ |
| 3 | cc_prompt_caching_mechanism | concept | 500 | 0 (1 md table) | ✅ |
| 4 | cc_cache_invalidation_actions | concept | 600 | 0 | ✅ |
| 5 | cc_cache_preserving_actions | concept | 550 | 0 (1 md table) | ✅ |
| 6 | cc_cache_lifetime_and_scope | concept | 450 | 0 | ✅ |
| 7 | cc_cost_tracking | procedure | 600 | 1 (`/usage` text block) + 1 md table | ✅ |
| 8 | cc_reduce_token_usage | argument | 650 | 2 (PreToolUse filter-hook JSON+bash) | ✅ |

No note approaches the caps (max ~650w / ≤2 code blocks vs ≤2500w / ≤6). The large `prompt-caching` page is
the only over-cap source and is split four ways. No over-compression — every H2/H3 maps to a note or an
explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_context_window_anatomy cc_what_survives_compaction cc_prompt_caching_mechanism cc_cache_invalidation_actions cc_cache_preserving_actions cc_cache_lifetime_and_scope cc_cost_tracking cc_reduce_token_usage"
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
| G2-Grounding | faithful to source page (prose only; React sim NOT transcribed), no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 8 notes RECEIVES ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1, verified) | DB confirms in-degree ≥1 for all 8 notes after inlinks applied; no graph island | sqlite3 in-degree count |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`
(created as a pre-step before the first sub-plan executes); this sub-plan **contributes its 8 rows** under a
"Context & Cost" cluster + increments the BB-distribution counts (model 1, concept 5, procedure 1, argument 1).

## Undigested Terms Plan (Step 2d)

b02a creates **no new `term_dictionary` notes** — Claude Code vocabulary on these pages is digested as `cc_`
doc notes or linked to existing substantive term notes (master Pattern B; dedup across `term_dictionary`
AND `documentation/`):

| Page term / concept | Disposition |
|---|---|
| Context window | link `term_context_window` (exists, substantive) |
| Compaction / auto-compaction | link `term_compaction` (exists) |
| Prompt caching / prefix cache / KV cache | link `term_prompt_caching` + `term_kv_cache` + `term_caching` (exist) — `cc_` notes 3–6 are the *Claude-Code-product* docs (distinct sense) |
| Cache invalidation / TTL / eviction | link `term_cache_invalidation` + `term_eviction_policy` (exist) |
| Token / tokenization | link `term_tokenization` (exists) |
| Extended thinking / effort level | folded into note 8; reasoning concept → link `term_chain_of_thought` + `term_inference_scaling_law` (exist); CC `/effort` detail owned by B03B |
| Subagent / fork | link `term_subagent` (exists); fork detail owned by B10A |
| Agent teams | link `term_multi_agent` (exists); page owned by B10A |
| MCP tool search / deferred tools | link `term_mcp` (exists); detail owned by B08A |
| Rate limit (TPM/RPM) | link `term_rate_limiting` (exists) |
| Fast mode / model-config / permissions / plugins | owned by home sub-plan (B04A / B03B / B05A / B09A) — captured/linked there |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 3 pages scanning emphasis/tables/captions/the
React simulation event descriptions for newly-surfaced non-glossary terms. Candidates considered:
"effort level" (→ B03B), "fast mode" (→ B04A), "LiteLLM / LLM gateway" (→ B14A), "OpenTelemetry exporter"
(→ B15B monitoring), "code intelligence plugins" (→ B09 discover-plugins, already routed by B01A's scan),
"usage credits / workspace spend limit" (Claude Code billing-config, folded into note 7 prose, no
standalone term). **None has a B02A doc-page home AND no existing note** → **0 new B02A `term_dictionary`
captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B02A authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do these pages' concepts duplicate existing notes?)
was performed and is the reason `cc_prompt_caching_mechanism` is NOT a duplicate of `term_prompt_caching`:
the term is the generic/Bedrock concept (`building_block: concept`, "## Definition"), the `cc_` notes are
Claude Code's product behavior (automatic caching, invalidation actions, TTL selection) — same concept,
different sense, so the master's Pattern B (CC vocab → `cc_` doc note + link existing term) applies and no
merge/delete is warranted. `term_context_window`, `term_compaction`, `term_kv_cache`, `term_caching`,
`term_cache_invalidation`, `term_eviction_policy` likewise linked, not recreated.

## Term-Note Authoring Requirements

**N/A for b02a** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- **The `context-window.md` React simulation (L9–1569) is source code — never transcribe it.** Paraphrase
  the facts it encodes (representative token counts are illustrative; say so) from the prose breakdown.
- Code blocks verbatim where used (note 7 `/usage` text, note 8 PreToolUse filter-hook). One BB per note.
  Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 inbound in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_context_window.md` | notes 1, 2, 8 | context-window term → CC anatomy / compaction survival / token-reduction |
| `term_dictionary/term_prompt_caching.md` | notes 3, 4, 5, 6 | prompt-caching term → CC caching mechanism / invalidation / preserving / lifetime |
| `term_dictionary/term_compaction.md` | notes 2, 4 | compaction term → CC survival rules / compaction-as-invalidation |
| `term_dictionary/term_rate_limiting.md` | note 7 | rate-limiting term → CC team TPM/RPM cost guidance |
| `term_dictionary/term_chain_of_thought.md` | note 8 | extended-thinking reasoning → CC thinking-budget cost trade-off |
| `documentation/tutorials/tutorial_claude_code_04_configuration.md` | notes 7, 8 | config tutorial → cost tracking / token-reduction config |

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above and DB-verify
  in-degree ≥1 for all 8 (G8); queue the 8 rows for `entry_claude_code_docs.md` under a "Context & Cost"
  cluster; `/tessellum-check-broken-links`.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13 — READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B02A, 2026-06-13)

- **Source re-read (Step 2)**: all 3 pages re-read from `inbox/claude_code_docs/`; measured raw words match
  the master figure (context-window 6,548 · prompt-caching 3,763 · costs 2,103 = 12,414). Critical finding:
  `context-window.md` is ≈774 prose words + a 1,561-line embedded React simulation (the raw word count is
  6.5× the prose). Recorded explicitly; the simulation is out-of-scope source code, paraphrased not
  transcribed. No >1.5× under-estimate vs note plan; no re-split forced beyond the three documented.
- **Notes**: 8 (model 1, concept 5, procedure 1, argument 1) — matches master estimate. The over-cap
  `prompt-caching` page is split four ways; `costs` split by BB into tracking (procedure) vs reduction
  (argument).
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard —
  6–7 term notes per note (18 distinct `term_dictionary/` terms), each with a per-link relevancy statement;
  deferred to finalization.
- **Step 2d new-term scan**: candidates (effort level, fast mode, LLM gateway/LiteLLM, OpenTelemetry,
  usage credits) all owned by other sub-plans or folded into note prose; **0 new B02A term captures**.
- **Dedup (Step 2b/G-B)**: `term_prompt_caching` (Bedrock/generic concept) confirmed NOT a duplicate of the
  `cc_` product-doc notes (different sense per master Pattern B); `term_context_window`, `term_compaction`,
  `term_kv_cache`, `term_caching`, `term_cache_invalidation`, `term_eviction_policy` linked, not recreated.
  No `claude_code/` doc dir exists yet (B01A unexecuted) → no `cc_` collision.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G5/G7/G8 verification rows, the React-simulation out-of-scope note.
- **28-item checklist**: PASS (term-note items N/A — B02A authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented and reviewed in-session; set to `ready` after the 9/9 self-review below.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step | ✅ PASS | Per-Note Related Notes Mapping present; **≥6 relevancy-selected term notes/note** (6–7 each, per-link relevancy stated), all DB/disk-verified. Entry-point back-link deferred to finalization (hub created pre-step). |
| CP2 | 8-GATE per batch (G1–G8 incl. G7/G8) | ✅ PASS | 8 gate rows present (single phase) including G7 + G8 Discoverability (inbound in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B02A contributes 8 rows under "Context & Cost". |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes); body uses `## Overview` opener / source-mirrored H2 / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | All 8 notes 450–650w, ≤2 code blocks — none borderline; the only over-cap source (prompt-caching 3,763w) is split four ways. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` measured: context-window 6,548 (≈774 prose, JSX excluded), prompt-caching 3,763, costs 2,103 = 12,414 = master figure; H2/H3 counted via grep. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B02A authors 0 term notes; Undigested Terms Plan routes every page concept (link existing / home sub-plan); Authoring Requirements inherited. |
| CP8f/CP9 | Term-slug specificity + collision audit (dedup across term_dictionary AND documentation/) | ✅ PASS | N/A (0 new slugs); collision audit documented — `cc_prompt_caching_mechanism` ≠ `term_prompt_caching` (product-doc vs generic-concept sense, master Pattern B); 6 existing terms linked, not recreated; no `cc_` collision (no `claude_code/` dir yet). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
