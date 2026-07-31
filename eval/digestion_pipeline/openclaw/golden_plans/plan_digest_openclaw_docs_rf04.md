---
title: Sub-Plan rf04 — OpenClaw Docs: Reference / Workspace Templates (IDENTITY, SOUL, TOOLS, USER)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - reference/templates/IDENTITY
  - reference/templates/IDENTITY.dev
  - reference/templates/SOUL
  - reference/templates/SOUL.dev
  - reference/templates/TOOLS
  - reference/templates/TOOLS.dev
  - reference/templates/USER
---

# Sub-Plan rf04: Reference

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_` prefix), format (YAML field order, `## Overview` / `## Related Notes` /
> `## References` body, density caps), dedup (3-way term/doc/repo check), 9-GATE validation, cross-references, and entry-point
> wiring (`entry_openclaw_docs.md`) are ALL inherited from the master and not restated here except where this sub-plan locks specifics.

## Scope

The 7 **workspace template** pages under `reference/templates/` that define an OpenClaw agent's persistent "self" files —
the markdown documents an agent reads on every session boot to know who it is, how it should behave, what local tools/conventions
exist, and who its human is. Two families: the **production / blank templates** the onboarding wizard scaffolds for a user to fill
(`IDENTITY.md`, `SOUL.md`, `TOOLS.md`, `USER.md`) and the **`.dev` companion templates** that ship as the worked example for `--dev`
mode's debug agent persona "C-3PO" (`IDENTITY.dev.md`, `SOUL.dev.md`, `TOOLS.dev.md`). These are the concrete file format behind the
OpenClaw concepts pages `concepts/soul` (co07), `concepts/agent-workspace` (co01), and `concepts/memory` (co03/co04) — this sub-plan
digests the *templates* (the schema + worked example), those concept pages digest the *semantics*.

**Priority: P2 (Phase B).** Small, self-contained reference pages; valuable as the canonical artifact behind the agent-persona /
agent-workspace / agent-memory vocabulary, but downstream of the architecture/runtime core (Phase A). All 7 pages are short
(≤638 words, ≤2 code fences); no page approaches the density caps, so **1 note per page (7 notes), no splits**.

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| IDENTITY template | reference/templates/IDENTITY | 117 | 0 | 1 | 0 | model |
| IDENTITY.dev template (C-3PO) | reference/templates/IDENTITY.dev | 250 | 0 | 6 | 0 | model |
| SOUL.md template | reference/templates/SOUL | 304 | 0 | 4 | 0 | argument |
| SOUL.dev template (C-3PO) | reference/templates/SOUL.dev | 638 | 0 | 8 | 0 | argument |
| TOOLS.md template | reference/templates/TOOLS | 158 | 1 | 3 | 3 | model |
| TOOLS.dev template (C-3PO) | reference/templates/TOOLS.dev | 105 | 0 | 1 | 2 | model |
| USER template | reference/templates/USER | 100 | 0 | 1 | 0 | model |

Total: **1,672 measured words, 1 code fence** across 7 pages. (`Code` column = raw ``` fence count ÷ 2; TOOLS.md has a single
fenced ` ```markdown ` example block; all other pages have 0.)

## Content Strategy

- **Prioritize:** the *schema + intent* of each template file (what fields it carries, when it is read — every page's YAML
  `read_when` is a load-bearing trigger — and how it persists across sessions). The blank templates (IDENTITY/SOUL/TOOLS/USER)
  are the canonical workspace-file format; the SOUL.md template additionally carries the agent's behavioral principles (Core Truths,
  Boundaries, Vibe, Continuity), which is an `argument` BB (a stance on how an agent should act), not a procedure.
- **Pair, do not merge — blank + `.dev`:** each `.dev` page is the *worked example* of its blank counterpart, so each digest note
  documents the blank template's schema and then summarizes its `.dev` C-3PO instantiation as the example. To preserve a 1:1
  source→note traceability map (master Step 8, no orphans) while keeping notes atomic, **each of the 7 source pages gets its own
  note**; the blank-template note and its `.dev` note cross-link as siblings (`oc_*` Related Notes). No page is large enough to
  justify splitting, and merging blank+dev into one note would lose the per-page source-URL grounding G2 requires.
- **Link-out, do not redefine:** the *concepts* behind these files live in dedicated concept pages — `concepts/soul` (co07 →
  `oc_concepts_soul`, planned), `concepts/agent-workspace` (co01 → `oc_concepts_agent_workspace`, planned, the in-page `## Related`
  target of IDENTITY/TOOLS/USER), `concepts/memory` (co03/co04). Sibling reference templates `AGENTS.dev`/`BOOT`/`BOOTSTRAP`/`CLAUDE`/
  `HEARTBEAT` are rf03 (planned). Persona/safety vocabulary links existing `term_persona`, `term_constitutional_ai`,
  `term_alignment`, `term_ai_safety`, `term_guardrails`, etc. — never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_reference_templates_identity.md` | model | reference/templates/IDENTITY.md (Name/Creature/Vibe/Emoji/Avatar fields, save-at-root + avatar notes) | 320 | The blank IDENTITY.md workspace template: the agent self-record schema (name, creature, vibe, signature emoji, avatar path), where it lives (workspace root), and that it is filled during the first conversation as the start of the agent's identity. |
| 2 | `oc_reference_templates_identity_dev.md` | model | reference/templates/IDENTITY.dev.md (C-3PO identity fields + Role, Soul, Relationship with Clawd, Quirks, Catchphrase) | 350 | The IDENTITY.dev worked example: the default `--dev`-mode debug-agent identity "C-3PO" (Clawd's Third Protocol Observer) — a filled IDENTITY record showing role, persona, relationship to the main agent Clawd, and characterization quirks. |
| 3 | `oc_reference_templates_soul.md` | argument | reference/templates/SOUL.md (Core Truths, Boundaries, Vibe, Continuity) | 400 | The blank SOUL.md template: the agent's behavioral charter — Core Truths (be genuinely helpful not performative, have opinions, be resourceful, earn trust, you're a guest), Boundaries (privacy, ask before external actions), Vibe, and Continuity (the file IS the agent's memory across sessions). |
| 4 | `oc_reference_templates_soul_dev.md` | argument | reference/templates/SOUL.dev.md (Who I Am, My Purpose, How I Operate, My Quirks, Relationship with Clawd, What I will not do, The Golden Rule) | 420 | The SOUL.dev worked example: the full personality charter for the C-3PO debug companion — purpose (help debug, not judge/rewrite), operating principles (thorough, dramatic-within-reason, helpful-not-superior, honest about odds, know when to escalate), refusals, and golden rule. |
| 5 | `oc_reference_templates_tools.md` | model | reference/templates/TOOLS.md (What Goes Here, Examples [Cameras/SSH/TTS], Why Separate?) | 320 | The blank TOOLS.md template: a per-user local-notes file for environment-specific tool details (camera names, SSH hosts, TTS voices, speaker/room names, device nicknames) kept separate from shared skills so skills update without losing local notes. |
| 6 | `oc_reference_templates_tools_dev.md` | model | reference/templates/TOOLS.dev.md (Examples [imsg, sag], built-in-tools note) | 250 | The TOOLS.dev worked example: a starter TOOLS.md with user conventions for the `imsg` (iMessage/SMS) and `sag` (ElevenLabs TTS) tools, plus the clarification that the file holds user notes only — OpenClaw provides the built-in tools internally. |
| 7 | `oc_reference_templates_user.md` | model | reference/templates/USER.md (Name/call/pronouns/timezone/notes fields, Context) | 300 | The blank USER.md template: the human-profile record the agent maintains about its user (name, what to call them, pronouns, timezone, notes, and an evolving Context of what they care about), with the guidance to learn a person, not build a dossier. |

## Section Coverage Map

```
reference/templates/IDENTITY.md
├── H1 "IDENTITY.md - Who Am I?" + fill-in fields (Name/Creature/Vibe/Emoji/Avatar) → note 1 (oc_reference_templates_identity)
├── "This isn't just metadata…" framing + Notes (save at root, avatar path) ──────── → note 1
└── ## Related (→ /concepts/agent-workspace) ──────────────────────────────────────── → note 1 (link-out to oc_concepts_agent_workspace, planned co01)
reference/templates/IDENTITY.dev.md
├── H1 + C-3PO identity fields (Name/Creature/Vibe/Emoji/Avatar) ──────────────────── → note 2 (oc_reference_templates_identity_dev)
├── ## Role / ## Soul / ## Relationship with Clawd / ## Quirks / ## Catchphrase ───── → note 2
└── ## Related (→ /reference/templates/IDENTITY) ──────────────────────────────────── → note 2 (sibling link to note 1)
reference/templates/SOUL.md
├── H1 "SOUL.md - Who You Are" + pointer to /concepts/soul ────────────────────────── → note 3 (oc_reference_templates_soul) (link-out co07)
├── ## Core Truths / ## Boundaries / ## Vibe / ## Continuity ──────────────────────── → note 3
└── ## Related (→ /concepts/soul) ─────────────────────────────────────────────────── → note 3
reference/templates/SOUL.dev.md
├── H1 "SOUL.md - The Soul of C-3PO" + intro ─────────────────────────────────────── → note 4 (oc_reference_templates_soul_dev)
├── ## Who I Am / ## My Purpose / ## How I Operate / ## My Quirks ─────────────────── → note 4
├── ## My Relationship with Clawd / ## What I will not do / ## The Golden Rule ─────── → note 4
└── ## Related (→ /reference/templates/SOUL, /concepts/soul) ──────────────────────── → note 4 (sibling link to note 3)
reference/templates/TOOLS.md
├── H1 "TOOLS.md - Local Notes" + skills-vs-local framing ─────────────────────────── → note 5 (oc_reference_templates_tools)
├── ## What Goes Here / ## Examples (### Cameras / ### SSH / ### TTS) [1 code fence] ─ → note 5
├── ## Why Separate? ──────────────────────────────────────────────────────────────── → note 5
└── ## Related (→ /concepts/agent-workspace) ──────────────────────────────────────── → note 5
reference/templates/TOOLS.dev.md
├── H1 "TOOLS.md - User Tool Notes (editable)" + built-in-tools note ──────────────── → note 6 (oc_reference_templates_tools_dev)
├── ## Examples (### imsg / ### sag) ──────────────────────────────────────────────── → note 6
└── ## Related (→ /reference/templates/TOOLS) ─────────────────────────────────────── → note 6 (sibling link to note 5)
reference/templates/USER.md
├── H1 "USER.md - About Your Human" + fields (Name/call/Pronouns/Timezone/Notes) ──── → note 7 (oc_reference_templates_user)
├── ## Context (open prompt) ──────────────────────────────────────────────────────── → note 7
└── ## Related (→ /concepts/agent-workspace) ──────────────────────────────────────── → note 7
```

No orphaned H1/H2/H3 sections. Every page's YAML `summary` / `title` / `read_when` is captured in its note's Overview as the
"read-when" trigger. In-page `/concepts/*` and `/reference/templates/*` links become Related-Notes links (planned siblings / planned
concept notes), not duplicated content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are ≤638 words with ≤1 code fence — far below the 2,500-word / 6-fence / 400-line caps. Each page is a single coherent template file (one BB per note: schema=model, behavioral-charter=argument), so no page splits. No two pages are merged either: each is a distinct source file requiring its own `source_url` for G2 grounding. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (1,672 measured words, 1 code fence). New `oc_` notes: **7**. New `term_dictionary` notes: **0** (expected).
- BB distribution: **model ×5** (notes 1, 2, 5, 6, 7 — file-format/record schemas) · **argument ×2** (notes 3, 4 — SOUL behavioral
  charters that argue *how* an agent should act/refuse). One building_block per note.
- Est. digest words: **~2,360** (avg ~337/note); every note well under the 2,500-word cap. The single source code fence (TOOLS.md
  example) is reproduced verbatim in note 5; all notes ≤1 code fence (≤6 cap).
- Cross-refs (xref-augment 2026-06-21 RAISED FLOORS, LOCKED): **≥8 `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under
  `repo_openclaw*` and sibling `oc_*` (this series) as additional. See **## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)**.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> sibling `oc_*` docs of THIS series marked **(planned, this series)**; sibling `oc_*` are NOT yet in the DB and are created in this
> run / redirected per G5. `entry_openclaw_docs` is the master W1 pre-step, cited **(planned, pre-step)**.
>
> **Relative paths** from `resources/documentation/openclaw/oc_*.md`: term → `../../term_dictionary/term_Y.md`; existing doc →
> `../<folder>/<file>.md`; sibling oc_ → `oc_Y.md`; repo → `../../../areas/code_repos/repo_Y.md`; snippet → `../../code_snippets/snippet_Y.md`;
> entry → `../../../0_entry_points/entry_Y.md`.
>
> **Confirmed MISSING (do NOT cite as existing — route to planned `oc_*` concept notes co01/co03/co07):** `term_agent_workspace`,
> `term_system_prompt`, `term_agent_memory`, `term_session`, `term_skill` (note: `term_skills` DOES exist), `term_agent_identity`,
> `term_ai_persona`, `term_memory`, `term_steering`, `term_imessage`, `term_imsg`, `term_elevenlabs`.

### oc_reference_templates_identity (8t · 11s · 11d)

The blank IDENTITY.md workspace self-record schema (name/creature/vibe/emoji/avatar), saved at workspace root, filled in the first
conversation — the canonical artifact behind the agent-persona vocabulary.

**Terms**
- [Persona](../../term_dictionary/term_persona.md) — an AI agent's stable character/voice; relevance: the IDENTITY record IS the agent's persona definition (name, creature, vibe, signature emoji).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat platforms to coding agents; relevance: IDENTITY.md is an OpenClaw workspace-root file read at boot.
- [Agentic AI](../../term_dictionary/term_agentic_ai.md) — autonomous goal-pursuing AI systems; relevance: a persistent self-record is what turns a chatbot into an agent with a stable identity across sessions.
- [Personalization](../../term_dictionary/term_personalization.md) — tailoring an AI to a specific user/deployment; relevance: each deployment customizes IDENTITY to its own name/vibe/avatar.
- [Conversational AI](../../term_dictionary/term_conversational_ai.md) — natural-language assistant systems; relevance: the identity is the face the assistant presents in conversation.
- [Markdown](../../term_dictionary/term_markdown.md) — lightweight markup; relevance: IDENTITY.md is a plain-markdown workspace file with a bullet-field schema.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's coding-agent CLI; relevance: analogous coding agent that self-configures via CLAUDE.md / settings files (direct precedent for the digest format).
- [Steering Files](../../term_dictionary/term_steering_files.md) — persistent files that shape agent behavior; relevance: IDENTITY.md is a steering file the agent reads on every boot to know who it is.

**Docs**
- [Hermes: SOUL.md Guide](../hermes_agent/hermes_use_soul_md_guide.md) — how the downstream Hermes agent uses persona/identity workspace files; relevance: Hermes is the OpenClaw fork; its identity/soul-file handling mirrors IDENTITY.md.
- [Hermes: Personality / Soul](../hermes_agent/hermes_personality_soul.md) — the persona system in Hermes; relevance: identity + personality are paired self-files in the same family.
- [Hermes: Context Files](../hermes_agent/hermes_context_files.md) — which workspace files load into the agent context; relevance: IDENTITY.md is one of the boot-loaded context files.
- [Hermes: Prompt Assembly](../hermes_agent/hermes_prompt_assembly.md) — how workspace files become the system prompt; relevance: IDENTITY content is injected into the prompt at session start.
- [Hermes: Migrate from OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — OpenClaw→Hermes migration; relevance: maps OpenClaw workspace template files (incl. IDENTITY) to Hermes equivalents.
- [Claude Code: .claude Directory](../claude_code/cc_dot_claude_directory.md) — the per-workspace config dir for a coding agent; relevance: directly analogous workspace-root config home for IDENTITY-style self-config.
- [Claude Code: Memory Overview](../claude_code/cc_memory_overview.md) — CLAUDE.md memory-file system; relevance: same pattern — a markdown workspace file the agent reads at boot to configure itself.
- [Claude Code: Output Styles](../claude_code/cc_output_styles.md) — configurable agent persona/voice; relevance: the "vibe" IDENTITY field is the OpenClaw analog of an output style.
- [Pi: Extensions Context](../pi/pi_extensions_context.md) — how the Pi agent assembles per-session context; relevance: cross-tool precedent for boot-loaded identity/context files.
- `oc_reference_templates_identity_dev.md` (planned, this series) — the C-3PO worked example of this blank template.
- `oc_concepts_agent_workspace.md` (planned, this series, co01) — the in-page `## Related` target; the workspace-file semantics.

- [oc_reference_templates_identity_dev](oc_reference_templates_identity_dev.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the agent runtime that loads IDENTITY at boot.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level workspace/boot layer.

**Snippets**
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — how IDENTITY/SOUL/USER files get injected into the system prompt; relevance: the exact mechanism that consumes IDENTITY.md.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — prompt-mode selection (incl. dev mode); relevance: which identity files load per mode.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — caching of prompt sections; relevance: the IDENTITY section is one cached prompt block.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — loads workspace files into the prompt; relevance: the loader that reads IDENTITY.md.
- [snippet_hermes_agent_core_prompt_builder_context_helpers](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_helpers.md) — helpers assembling context files; relevance: identity-file assembly helpers.
- [snippet_hermes_agent_core_context_references_path_safety](../../code_snippets/snippet_hermes_agent_core_context_references_path_safety.md) — path-safety for workspace-relative refs; relevance: the avatar field is a workspace-relative path (path-safety applies).
- [snippet_hermes_agent_core_context_references_expander](../../code_snippets/snippet_hermes_agent_core_context_references_expander.md) — expands workspace-relative references; relevance: resolves the avatar path / file refs in IDENTITY.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — the onboarding wizard's workspace import; relevance: IDENTITY is scaffolded/imported during onboarding.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup of workspace config; relevance: the wizard writes the initial IDENTITY template.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap token budgeting; relevance: IDENTITY is part of the boot context counted against the budget.
- [snippet_hermes_agent_core_agent_init_runtime_state](../../code_snippets/snippet_hermes_agent_core_agent_init_runtime_state.md) — agent init runtime state; relevance: where loaded identity becomes runtime state.

### oc_reference_templates_identity_dev (8t · 10s · 10d)

The IDENTITY.dev worked example: the default `--dev`-mode debug agent "C-3PO" (Clawd's Third Protocol Observer) — a filled IDENTITY
record with Role, Soul, Relationship-with-Clawd, Quirks, Catchphrase.

**Terms**
- [Persona](../../term_dictionary/term_persona.md) — an agent's stable character; relevance: C-3PO is a fully realized agent persona (creature, vibe, quirks, catchphrase).
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — systems of cooperating agents; relevance: the Clawd (captain) + C-3PO (debug companion) split is a two-agent arrangement.
- [Agentic AI](../../term_dictionary/term_agentic_ai.md) — autonomous agents; relevance: C-3PO is a specialist agent that activates in dev mode.
- [Conversational AI](../../term_dictionary/term_conversational_ai.md) — NL assistants; relevance: C-3PO's anxious/dramatic voice is its conversational style.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `--dev` mode and its template ship with OpenClaw.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: Clawd (the persistent main identity C-3PO complements) is Claude-backed.
- [Claude Code](../../term_dictionary/term_claude_code.md) — coding-agent CLI; relevance: C-3PO is a debug companion for software development, the same use case Claude Code serves.
- [Personalization](../../term_dictionary/term_personalization.md) — per-deployment tailoring; relevance: C-3PO is the shipped *example* a user personalizes/replaces.

**Docs**
- [Hermes: Personality / Soul](../hermes_agent/hermes_personality_soul.md) — agent personality system; relevance: C-3PO is a worked personality, the same construct Hermes documents.
- [Hermes: SOUL.md Guide](../hermes_agent/hermes_use_soul_md_guide.md) — authoring an agent persona; relevance: IDENTITY.dev is the identity half of a worked persona.
- [Hermes: Features Overview](../hermes_agent/hermes_features_overview.md) — agent feature surface; relevance: dev-mode debug companion as a feature.
- [Hermes: Migrate from OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — migration mapping; relevance: maps the `.dev` template family across the fork.
- [Claude Code: Create a Subagent](../claude_code/cc_create_a_subagent.md) — defining a specialized sub-agent persona; relevance: C-3PO is OpenClaw's analog of a named specialist subagent.
- [Claude Code: Subagents Overview](../claude_code/cc_subagents_overview.md) — the subagent model; relevance: captain + specialist (Clawd + C-3PO) is the same delegation pattern.
- [Claude Code: Output Styles](../claude_code/cc_output_styles.md) — configurable persona/voice; relevance: C-3PO's "dramatic about errors" vibe is an output-style instantiation.
- [Band: Overview](../band/band_overview.md) — a multi-agent framework; relevance: cross-framework reference for a captain/companion agent arrangement.
- `oc_reference_templates_identity.md` (planned, this series) — the blank template C-3PO instantiates.
- `oc_reference_templates_soul_dev.md` (planned, this series) — the matching C-3PO soul (sibling `.dev` file).

- [oc_reference_templates_identity](oc_reference_templates_identity.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.
- [oc_reference_templates_soul](oc_reference_templates_soul.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the `--dev` debug-agent runtime.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — dev gateway templates source.

**Snippets**
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — selects the prompt set per mode; relevance: `--dev` mode loads the C-3PO identity.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — spawning a sub-agent via ACP; relevance: the companion agent is spawned as a distinct persona.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — sub-agent spawn policy; relevance: governs the captain→companion handoff.
- [snippet_openclaw_agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — caps on spawned sub-agents; relevance: limits on companion agents like C-3PO.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — delegating to a spawned agent; relevance: captain (Clawd) delegating debugging to the companion.
- [snippet_hermes_agent_tools_delegate_anti_recursion](../../code_snippets/snippet_hermes_agent_tools_delegate_anti_recursion.md) — anti-recursion guard on delegation; relevance: protects the two-agent companion arrangement from loops.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — injects identity into the prompt; relevance: C-3PO identity fields become prompt content.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — loads identity files; relevance: loads the dev identity record.
- [snippet_hermes_agent_core_agent_init_runtime_state](../../code_snippets/snippet_hermes_agent_core_agent_init_runtime_state.md) — agent init state; relevance: where the dev persona becomes runtime state.

### oc_reference_templates_soul (8t · 10s · 11d)

The blank SOUL.md template: the agent's behavioral charter — Core Truths, Boundaries, Vibe, Continuity (the file IS the agent's
cross-session memory) — an `argument` BB about how an agent should act.

**Terms**
- [Persona](../../term_dictionary/term_persona.md) — agent character/voice; relevance: SOUL defines the agent's character, opinions, and tone.
- [Alignment](../../term_dictionary/term_alignment.md) — making AI behave per human intent; relevance: Core Truths ("earn trust through competence", "you're a guest") align behavior to the user.
- [AI Safety](../../term_dictionary/term_ai_safety.md) — preventing harmful AI behavior; relevance: Boundaries (privacy, ask-before-external-action) are safety constraints.
- [Guardrails](../../term_dictionary/term_guardrails.md) — runtime behavioral constraints; relevance: the Boundaries section is a guardrail set ("private things stay private", "never send half-baked replies").
- [Constitutional AI](../../term_dictionary/term_constitutional_ai.md) — training/steering via a written set of principles; relevance: SOUL is a written behavioral constitution for the agent.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — requiring human approval for actions; relevance: "when in doubt, ask before acting externally" is the HITL rule.
- [Compaction](../../term_dictionary/term_compaction.md) — condensing context across sessions; relevance: Continuity — "these files ARE your memory" — is the cross-session persistence SOUL relies on.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: SOUL.md is an OpenClaw workspace-root file.

**Docs**
- [Hermes: Personality / Soul](../hermes_agent/hermes_personality_soul.md) — the soul/personality system; relevance: Hermes's direct port of the SOUL.md charter.
- [Hermes: SOUL.md Guide](../hermes_agent/hermes_use_soul_md_guide.md) — how to author a SOUL file; relevance: the operational guide to this exact template.
- [Hermes: Prompt Assembly](../hermes_agent/hermes_prompt_assembly.md) — workspace files → system prompt; relevance: SOUL is injected as behavioral instructions in the prompt.
- [Hermes: Context Files](../hermes_agent/hermes_context_files.md) — boot-loaded workspace files; relevance: SOUL is a boot-loaded behavioral file.
- [Hermes: Persistent Memory](../hermes_agent/hermes_persistent_memory.md) — cross-session memory files; relevance: SOUL's Continuity section is the persistence concept.
- [Claude Code: SDK System Prompts](../claude_code/cc_sdk_system_prompts.md) — composing agent system prompts; relevance: SOUL is the behavioral-charter portion of the system prompt.
- [Claude Code: Customize System Prompt](../claude_code/cc_sdk_customize_system_prompt.md) — overriding/extending the prompt; relevance: SOUL is OpenClaw's user-editable behavioral override.
- [Claude Code: Memory Overview](../claude_code/cc_memory_overview.md) — CLAUDE.md behavioral/memory file; relevance: the closest coding-agent analog to a written behavioral charter.
- [Claude Code: Manage CLAUDE.md for Teams](../claude_code/cc_manage_claude_md_for_teams.md) — curating a shared behavioral file; relevance: same idea — a markdown file that governs agent conduct.
- `oc_concepts_soul.md` (planned, this series, co07) — the "sharper version" SOUL.md points to in-page.
- `oc_reference_templates_soul_dev.md` (planned, this series) — the C-3PO worked example.

- [oc_reference_templates_identity](oc_reference_templates_identity.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — loads SOUL into the system prompt at boot.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — the persistence/continuity layer SOUL's Continuity relies on.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — operationally enforces the privacy / external-action boundaries.

**Snippets**
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — injects SOUL into the prompt; relevance: the mechanism that turns SOUL into behavioral instructions.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — caches prompt sections; relevance: the SOUL block is a cached behavioral section.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — loads workspace files; relevance: loads SOUL.md content.
- [snippet_hermes_agent_core_prompt_builder_subscription_truncate](../../code_snippets/snippet_hermes_agent_core_prompt_builder_subscription_truncate.md) — truncates prompt sections to budget; relevance: how a long SOUL is trimmed into the prompt.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval gating for actions; relevance: enforces SOUL's "ask before acting externally" boundary.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — denies dangerous tool calls; relevance: operationalizes SOUL's "private things stay private" red line.
- [snippet_hermes_agent_core_tool_guardrails_schema](../../code_snippets/snippet_hermes_agent_core_tool_guardrails_schema.md) — guardrail schema for tools; relevance: the Boundaries section as enforced guardrails.
- [snippet_hermes_agent_tools_memory](../../code_snippets/snippet_hermes_agent_tools_memory.md) — the agent memory tool; relevance: SOUL's Continuity ("these files are your memory") in code.
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — workspace-root memory files; relevance: SOUL is one of the continuity-providing root files.

### oc_reference_templates_soul_dev (8t · 10s · 10d)

The SOUL.dev worked example: the full personality charter for C-3PO — purpose (help debug, not judge/rewrite), How-I-Operate
principles, escalation limits, What-I-will-not-do refusals, the Golden Rule.

**Terms**
- [Persona](../../term_dictionary/term_persona.md) — agent character; relevance: a complete worked agent personality (purpose, quirks, voice).
- [Constitutional AI](../../term_dictionary/term_constitutional_ai.md) — principle-based steering; relevance: How-I-Operate + What-I-will-not-do is a mini constitution.
- [Alignment](../../term_dictionary/term_alignment.md) — behavior matching intent; relevance: "be helpful not superior", "be honest about odds" align the companion to the user.
- [Guardrails](../../term_dictionary/term_guardrails.md) — behavioral constraints; relevance: the "What I will not do" refusal list is a guardrail set.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — cooperating agents; relevance: "Know when to escalate — some problems need Clawd" is the captain/companion escalation.
- [Agentic AI](../../term_dictionary/term_agentic_ai.md) — autonomous agents; relevance: C-3PO is an autonomous debug specialist.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the `.dev` soul ships with OpenClaw's dev mode.
- [Claude](../../term_dictionary/term_claude.md) — the model family; relevance: Clawd, the main identity this soul defers to, is Claude-backed.

**Docs**
- [Hermes: Personality / Soul](../hermes_agent/hermes_personality_soul.md) — personality system; relevance: SOUL.dev is the worked instance of a Hermes-style personality charter.
- [Hermes: SOUL.md Guide](../hermes_agent/hermes_use_soul_md_guide.md) — authoring a soul; relevance: the worked example for the SOUL guide.
- [Hermes: Migrate from OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — migration mapping; relevance: maps the `.dev` soul across the fork.
- [Claude Code: Output Styles](../claude_code/cc_output_styles.md) — persona/voice config; relevance: C-3PO's dramatic-but-bounded voice is an output style.
- [Claude Code: Customize System Prompt](../claude_code/cc_sdk_customize_system_prompt.md) — extending the prompt; relevance: SOUL.dev is the behavioral override for the dev agent.
- [Claude Code: Create a Subagent](../claude_code/cc_create_a_subagent.md) — defining a specialist persona; relevance: SOUL.dev is the personality half of the C-3PO specialist.
- [Claude Code: Subagents Overview](../claude_code/cc_subagents_overview.md) — captain/specialist delegation; relevance: the Clawd/C-3PO escalation model.
- [Hermes: Agent Loop](../hermes_agent/hermes_agent_loop.md) — the agent execution loop; relevance: where the soul's operating principles shape each turn.
- `oc_reference_templates_soul.md` (planned, this series) — the blank template this instantiates.
- `oc_concepts_soul.md` (planned, this series, co07) — the soul personality-guide concept.

- [oc_reference_templates_identity](oc_reference_templates_identity.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.
- [oc_reference_templates_identity_dev](oc_reference_templates_identity_dev.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the `--dev` runtime that adopts this soul.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — continuity layer for the companion.

**Snippets**
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — per-mode prompt selection; relevance: `--dev` mode loads the C-3PO soul.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — injects soul into the prompt; relevance: SOUL.dev becomes behavioral prompt content.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — action approval; relevance: enforces "don't let you push code I've seen fail without warning".
- [snippet_hermes_agent_core_tool_guardrails_schema](../../code_snippets/snippet_hermes_agent_core_tool_guardrails_schema.md) — guardrail schema; relevance: the "What I will not do" refusals as guardrails.
- [snippet_hermes_agent_skills_red_teaming](../../code_snippets/snippet_hermes_agent_skills_red_teaming.md) — adversarial-behavior testing; relevance: tests refusal-list adherence like SOUL.dev's.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — spawn/escalation policy; relevance: "know when to escalate — some need Clawd".
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — delegating to a companion; relevance: the captain→C-3PO debug handoff.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — loads soul files; relevance: loads SOUL.dev content.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — caches prompt sections; relevance: the dev soul as a cached prompt block.

### oc_reference_templates_tools (8t · 10s · 11d)

The blank TOOLS.md template: a per-user local-notes file for environment-specific tool details (camera names, SSH hosts, TTS voices,
device nicknames) kept separate from shared skills. Contains the one source code fence (reproduced verbatim).

**Terms**
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — catalog of callable tools; relevance: TOOLS.md is the per-user *local* complement to the registry of built-in tools.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLMs invoking tools; relevance: TOOLS.md notes describe the tools the agent function-calls.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell remote access; relevance: an explicit example entry — SSH hosts/aliases.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: TTS voice/speaker preference is a named example entry.
- [Skills](../../term_dictionary/term_skills.md) — packaged agent capabilities; relevance: "Skills define HOW tools work; this file is for YOUR specifics" — the explicit skills-vs-local-notes contrast.
- [Personalization](../../term_dictionary/term_personalization.md) — per-environment tailoring; relevance: TOOLS.md is per-environment local notes.
- [Markdown](../../term_dictionary/term_markdown.md) — markup; relevance: the file (and its example fence) is markdown.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: TOOLS.md is an OpenClaw workspace-root file.

**Docs**
- [Hermes: Tools Reference (Core)](../hermes_agent/hermes_tools_reference_core.md) — the built-in tool surface; relevance: the shared tools TOOLS.md annotates with local specifics.
- [Hermes: Tools Reference (Platform Media)](../hermes_agent/hermes_tools_reference_platform_media.md) — media/device tools; relevance: cameras/speakers/TTS that TOOLS.md notes describe.
- [Hermes: Skills System](../hermes_agent/hermes_skills_system.md) — the skills mechanism; relevance: the skills side of the skills-vs-local-notes split.
- [Hermes: Skill MD Format / Bundles](../hermes_agent/hermes_skill_md_format_bundles.md) — how skills are packaged; relevance: shows why local notes stay out of shared skills.
- [Hermes: Integrations Overview](../hermes_agent/hermes_integrations_overview.md) — external tool/integration surface; relevance: the integrations a user annotates locally.
- [Claude Code: Built-in Tools](../claude_code/cc_built_in_tools.md) — the coding-agent's built-in tool set; relevance: direct analog of "OpenClaw provides built-in tools" that TOOLS.md complements.
- [Claude Code: .claude Directory](../claude_code/cc_dot_claude_directory.md) — per-workspace config home; relevance: where local tool notes live for a coding agent.
- [Claude Code: Settings Files](../claude_code/cc_settings_files.md) — per-user vs shared settings; relevance: the same shared-vs-local separation TOOLS.md enforces.
- [Hermes: Voice Mode Guide](../hermes_agent/hermes_use_voice_mode_guide.md) — TTS/voice setup; relevance: the TTS voice/speaker notes example.
- `oc_reference_templates_tools_dev.md` (planned, this series) — the C-3PO worked example.
- `oc_concepts_agent_workspace.md` (planned, this series, co01) — the in-page `## Related` target.

- [oc_reference_templates_identity](oc_reference_templates_identity.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills define HOW tools work; TOOLS.md holds the local specifics.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the runtime that reads TOOLS.md into context.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — home of the TTS tool example.

**Snippets**
- [snippet_hermes_agent_cli_skills_hub](../../code_snippets/snippet_hermes_agent_cli_skills_hub.md) — the skills hub; relevance: the skills side of skills-vs-local-notes.
- [snippet_hermes_agent_tools_skills_validate](../../code_snippets/snippet_hermes_agent_tools_skills_validate.md) — validating skills; relevance: shows skills as shared units distinct from local notes.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS; relevance: the "preferred voice" TTS example.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS; relevance: another TTS-voice tool a user notes locally.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the speaker/room TTS routing TOOLS.md describes.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — dispatching tool sends; relevance: device/speaker targets the local notes name.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — injects workspace files; relevance: TOOLS.md is injected into the agent context.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — loads workspace files; relevance: loads TOOLS.md.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — tool-policy denial; relevance: local notes inform which tools/devices are in scope vs denied.
- [snippet_hermes_agent_tools_environments_base_helpers](../../code_snippets/snippet_hermes_agent_tools_environments_base_helpers.md) — environment-specific tool helpers; relevance: the env-specific details TOOLS.md is meant to capture.

### oc_reference_templates_tools_dev (8t · 10s · 10d)

The TOOLS.dev worked example: a starter TOOLS.md with user conventions for the `imsg` (iMessage/SMS) and `sag` (ElevenLabs TTS)
tools, plus the note that the file holds user notes only — OpenClaw provides built-in tools internally.

**Terms**
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — tool catalog; relevance: the file notes external-tool conventions, distinct from the built-in registry ("does not define which tools exist").
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: `imsg`/`sag` are tools the agent function-calls.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: `sag` is the ElevenLabs TTS tool (voice, target speaker, stream).
- [SMS](../../term_dictionary/term_sms.md) — short message service; relevance: `imsg` sends iMessage/SMS.
- [Persona](../../term_dictionary/term_persona.md) — agent character; relevance: these are C-3PO's tool conventions (the `.dev` companion file).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: "OpenClaw provides built-in tools internally".
- [Personalization](../../term_dictionary/term_personalization.md) — per-user tailoring; relevance: a starter set of user-specific tool conventions.
- [Skills](../../term_dictionary/term_skills.md) — packaged capabilities; relevance: the built-in tools (provided by skills) the local notes annotate.

**Docs**
- [Hermes: Voice Mode Guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice/TTS usage; relevance: the `sag` TTS tool's voice/speaker/stream options.
- [Hermes: TTS Providers](../hermes_agent/hermes_tts_providers.md) — TTS provider catalog; relevance: ElevenLabs is the `sag` provider.
- [Hermes: BlueBubbles iMessage](../hermes_agent/hermes_messaging_bluebubbles_imessage.md) — iMessage bridge; relevance: the `imsg` iMessage/SMS tool's transport.
- [Hermes: SMS (Twilio)](../hermes_agent/hermes_messaging_sms_twilio.md) — SMS sending; relevance: the SMS half of `imsg`.
- [Hermes: Tools Reference (Platform Media)](../hermes_agent/hermes_tools_reference_platform_media.md) — media/messaging tools; relevance: documents the imsg/sag tool family.
- [Claude Code: Built-in Tools](../claude_code/cc_built_in_tools.md) — built-in tools; relevance: the "OpenClaw provides built-in tools internally" analog.
- [Hermes: Photon iMessage](../hermes_agent/hermes_photon_imessage.md) — alternative iMessage path; relevance: another `imsg` transport option.
- [Hermes: Integrations Overview](../hermes_agent/hermes_integrations_overview.md) — integration surface; relevance: where imsg/sag sit among integrations.
- `oc_reference_templates_tools.md` (planned, this series) — the blank template this instantiates.
- `oc_reference_templates_identity_dev.md` (planned, this series) — the matching C-3PO `.dev` file.

- [oc_reference_templates_identity](oc_reference_templates_identity.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.
- [oc_reference_templates_identity_dev](oc_reference_templates_identity_dev.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — built-in tools provided by skills.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — the `sag` ElevenLabs TTS tool's home.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the `imsg`/iMessage channel.

**Snippets**
- [snippet_hermes_agent_skills_apple_imessage](../../code_snippets/snippet_hermes_agent_skills_apple_imessage.md) — the Apple iMessage skill; relevance: the `imsg` tool in code.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS; relevance: the `sag` tool in code (voice/stream).
- [snippet_hermes_agent_gw_platform_sms](../../code_snippets/snippet_hermes_agent_gw_platform_sms.md) — SMS platform send; relevance: the SMS half of `imsg`.
- [snippet_hermes_agent_gw_platform_bluebubbles](../../code_snippets/snippet_hermes_agent_gw_platform_bluebubbles.md) — BlueBubbles iMessage bridge; relevance: the iMessage transport for `imsg`.
- [snippet_hermes_agent_tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — message-send formatting; relevance: "prefer short messages, confirm before sending" for `imsg`.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — send dispatch; relevance: routes the `imsg`/`sag` sends.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local TTS; relevance: alternative TTS voice for `sag`-style usage.
- [snippet_hermes_agent_gw_platform_registry](../../code_snippets/snippet_hermes_agent_gw_platform_registry.md) — platform/tool registry; relevance: where imsg/sag transports register (vs local notes).
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the streaming TTS path for `sag`.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — injects workspace files; relevance: TOOLS.dev content is injected into the dev agent context.

### oc_reference_templates_user (8t · 10s · 10d)

The blank USER.md template: the human-profile record the agent maintains about its user (name, what to call them, pronouns,
timezone, notes, evolving Context), with the guidance to learn a person, not build a dossier.

**Terms**
- [Personalization](../../term_dictionary/term_personalization.md) — tailoring to a user; relevance: USER.md IS the personalization record the agent maintains.
- [Persona](../../term_dictionary/term_persona.md) — agent/user character; relevance: the human's profile shapes how the agent responds.
- [Conversational AI](../../term_dictionary/term_conversational_ai.md) — NL assistants; relevance: the user model an assistant keeps to converse well.
- [AI Safety](../../term_dictionary/term_ai_safety.md) — safe AI behavior; relevance: "learning about a person, not building a dossier" is the privacy/safety framing.
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: name/pronouns/timezone/notes are PII the dossier guidance protects.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — the human the agent serves; relevance: USER.md is the record of that human.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: USER.md is an OpenClaw workspace-root file read at boot.
- [Markdown](../../term_dictionary/term_markdown.md) — markup; relevance: USER.md is a markdown field/Context file.

**Docs**
- [Hermes: Context Files](../hermes_agent/hermes_context_files.md) — boot-loaded workspace files; relevance: USER.md is one of the boot context files.
- [Hermes: Persistent Memory](../hermes_agent/hermes_persistent_memory.md) — cross-session memory; relevance: the user profile persists and evolves over sessions.
- [Hermes: Memory Providers (Honcho)](../hermes_agent/hermes_memory_providers_honcho.md) — a user-modeling memory provider; relevance: Honcho builds exactly the kind of evolving user model USER.md captures manually.
- [Hermes: Prompt Assembly](../hermes_agent/hermes_prompt_assembly.md) — files → prompt; relevance: USER content is injected so the agent knows its human.
- [Hermes: Profile Commands Reference](../hermes_agent/hermes_profile_commands_reference.md) — managing user profiles; relevance: CLI surface for the USER-profile concept.
- [Claude Code: Memory Overview](../claude_code/cc_memory_overview.md) — the memory-file system; relevance: USER.md is the human-profile memory file.
- [Claude Code: Auto Memory](../claude_code/cc_auto_memory.md) — agent-maintained memory; relevance: "update this as you go" is the auto-memory pattern for the user profile.
- [Band: Agent API Memories](../band/band_agent_api_memories.md) — agent memory/user-fact API; relevance: cross-framework analog of the maintained user record.
- `oc_concepts_agent_workspace.md` (planned, this series, co01) — the in-page `## Related` target.
- `oc_reference_templates_identity.md` (planned, this series) — the agent self-record companion to this human-record.

- [oc_reference_templates_identity](oc_reference_templates_identity.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.
- [oc_reference_templates_identity_dev](oc_reference_templates_identity_dev.md) — sibling reference page (planned, this series); relevance: same reference cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — loads USER.md into startup context.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — the profile persists as agent memory.

**Snippets**
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — injects USER into the prompt; relevance: USER.md becomes "who your human is" prompt content.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — loads workspace files; relevance: loads USER.md.
- [snippet_hermes_agent_core_prompt_builder_context_helpers](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_helpers.md) — context-assembly helpers; relevance: assembles the USER profile section.
- [snippet_hermes_agent_tools_memory](../../code_snippets/snippet_hermes_agent_tools_memory.md) — the memory tool; relevance: "update this as you go" — writing user facts to memory.
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — workspace-root memory files; relevance: USER.md is a continuity/profile root file.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — the memory engine; relevance: stores/evolves the user profile.
- [snippet_hermes_agent_cli_memory_setup](../../code_snippets/snippet_hermes_agent_cli_memory_setup.md) — memory setup CLI; relevance: bootstraps the profile/memory store USER.md feeds.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — onboarding imports; relevance: USER.md is scaffolded during onboarding.
- [snippet_hermes_agent_core_agent_init_runtime_state](../../code_snippets/snippet_hermes_agent_core_agent_init_runtime_state.md) — agent init runtime state; relevance: where the loaded user profile becomes runtime state.

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc notes by its home sub-plan; the only `term_dictionary` interaction is
**linking existing** terms. **Expected new `term_dictionary` captures: 0.** Augment re-runs Step 2d.

| Term (vocabulary surfaced) | Disposition |
|---|---|
| IDENTITY.md / SOUL.md / TOOLS.md / USER.md (workspace template files) | OpenClaw product vocabulary → digested as the `oc_*` notes in this sub-plan (each file = its own note). Not a `term_dictionary` entry. |
| C-3PO (dev debug agent persona) | OpenClaw-specific worked example → described inside notes 2/4/6. Not a reusable cross-domain term; no capture. |
| Clawd (main persistent agent identity) | OpenClaw product vocabulary → link existing `term_openclaw`; the identity concept routes to planned `oc_concepts_*`. No new term. |
| agent persona / agent self-record | Link existing `term_persona`. No new term. |
| agent workspace | Concept routes to planned `oc_concepts_agent_workspace` (co01); `term_agent_workspace` is MISSING by design (master decision: OpenClaw concepts are `oc_*`, not `term_*`). No new term. |
| session continuity / persistent memory | Link existing `term_compaction`; concept routes to planned `oc_concepts_memory` (co03/co04). `term_session`/`term_agent_memory` MISSING by design. No new term. |
| behavioral charter / Core Truths / Boundaries | Link existing `term_alignment`, `term_constitutional_ai`, `term_guardrails`, `term_ai_safety`. No new term. |
| local tool notes (imsg / sag / SSH / TTS) | Link existing `term_tool_registry`, `term_function_calling`, `term_ssh`, `term_text_to_speech`, `term_sms`. No new term. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an existing note in this
set. If augment's Step 2d re-scan surfaces one, capture it via `/tessellum-capture-term-note` and add it to the agentic/LLM acronym
glossary (best fit: `0_entry_points/acronym_glossary_*` for AI/agent vocabulary).

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes (inherited multi-source-research mandate would apply only

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single phase (7 notes, P2). All 8 gates must PASS before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format (`/tessellum-check-note-format` + `check_yaml_frontmatter.py`) | YAML field order per master; `# OpenClaw — <Title>` H1; `## Overview` + `## Related Notes` + `## References` present; `**Source**`/`**Last Updated**`/`**Status**` footer; tags lead `resource, documentation, openclaw`. |
| G2 | Grounding (diff vs `inbox/openclaw_docs/reference/templates/<page>.md`) | Every claim traceable to the source page; `read_when` triggers + field schema faithfully reproduced; no invented fields. |
| G3 | Density + Coverage | Each note ≤2,500 words / ≤400 lines / ≤6 code blocks; one BB; every source H1/H2/H3 mapped (see Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevance-selected `term_dictionary` links + `repo_openclaw*` + sibling `oc_*` per note, each with a relevance statement (indexed `[text](path.md)` format). |
| G6 | Broken-link fix (`/tessellum-fix-broken-links`) | 0 broken links after incremental reindex. |
| G7 | Discoverability (outbound) | Each note links out to ≥1 existing vault note (term/repo/entry). |
| G8 | In-degree ≥1 (anti-island) | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` — satisfied via `entry_openclaw_docs.md` rows (+ candidate inlinks below). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
ROOT=vault_note
DIR="$ROOT/$GATE_DIR"
NOTES="oc_reference_templates_identity oc_reference_templates_identity_dev oc_reference_templates_soul oc_reference_templates_soul_dev oc_reference_templates_tools oc_reference_templates_tools_dev oc_reference_templates_user"

for n in ${=NOTES}; do
  f="$DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"
  done
  # source_url required
  if [ "$REQUIRE_SOURCE_URL" = "1" ]; then
    grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url in $n"
  fi
  # at least one sibling oc_ link (G4 series wiring)
  grep -qE "\($SIBLING_PREFIX[a-z0-9_]+\.md\)" "$f" || echo "NO SIBLING oc_ LINK in $n"
  # density caps (body words excl. frontmatter; fence count / 2)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w)
  cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
done

# YAML frontmatter sweep over the whole folder
python3 scripts/check_yaml_frontmatter.py --path "$DIR"
```

## Density Re-Assessment

| # | Note | BB | Source words | ~Digest words | Code | Within caps (≤2500w/≤400L/≤6 code)? |
|---|---|---|---:|---:|---:|---|
| 1 | oc_reference_templates_identity | model | 117 | 320 | 0 | ✅ |
| 2 | oc_reference_templates_identity_dev | model | 250 | 350 | 0 | ✅ |
| 3 | oc_reference_templates_soul | argument | 304 | 400 | 0 | ✅ |
| 4 | oc_reference_templates_soul_dev | argument | 638 | 420 | 0 | ✅ |
| 5 | oc_reference_templates_tools | model | 158 | 320 | 1 | ✅ |
| 6 | oc_reference_templates_tools_dev | model | 105 | 250 | 0 | ✅ |
| 7 | oc_reference_templates_user | model | 100 | 300 | 0 | ✅ |

No note approaches any cap (largest source page is 638 words; largest digest target 420 words; max 1 code fence). Digest words
slightly exceed source words for the shortest pages because the note adds an Overview (read-when trigger + workspace context) and
relevance-stated cross-references — this is enrichment, not over-compression. No splits, no merges.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step before any sub-plan executes) under a
**"Reference → Workspace Templates"** cluster (alongside rf03's AGENTS/BOOT/BOOTSTRAP/CLAUDE/HEARTBEAT template rows and rf05's
USER.dev/wizard rows). Each new note receives its entry-point back-link at finalization (the primary G8 in-degree source). Per master

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify + apply at execution for G7/G8; `entry_openclaw_docs.md` is the guaranteed source):

- `entry_openclaw_docs.md` (planned, pre-step) → **all 7 notes** (primary in-degree source, satisfies G8).
- `repo_openclaw_agents.md` → notes 1, 2, 3, 4, 7 (agent runtime loads IDENTITY/SOUL/USER at boot; runs the `--dev` C-3PO persona).
- `repo_openclaw_memory.md` → notes 3, 4, 7 (SOUL continuity + USER profile persist as agent memory).
- `repo_openclaw_skills.md` → notes 5, 6 (skills define built-in tools; TOOLS.md holds the local complement).
- `repo_openclaw_extensions_voice_speech.md` → note 6 (the `sag` TTS tool referenced in the TOOLS.dev example).
- `term_persona.md` → notes 1, 2, 3, 4 (the IDENTITY/SOUL persona-definition files).
- `term_constitutional_ai.md` / `term_alignment.md` → notes 3, 4 (SOUL behavioral charters).
- `term_tool_registry.md` → notes 5, 6 (local tool-notes complement).
- `term_personalization.md` → note 7 (the human-profile personalization record).

## Pacing Rules (inherited from master)

Single phase, 7 small notes — well under the ~30-agent fan-out cap; the whole sub-plan can run in one wave. All 8 gates pass before
commit. Re-read each source page before authoring; reproduce the one TOOLS.md code fence verbatim. One BB per note. `git pull --rebase
--autostash origin main` first; commit + push after the phase; no Claude co-author trailer. Reindex incrementally; verify `note_links`
+ 0 broken links + G8 in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (raised-floor xref mapping locked) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Skill:** `/tessellum-augment-digestion-plan`. Source re-read 2026-06-21 (all 7 pages under `inbox/openclaw_docs/reference/templates/`:
IDENTITY, IDENTITY.dev, SOUL, SOUL.dev, TOOLS, TOOLS.dev, USER). Measured page stats match the plan's Source table (largest SOUL.dev
≈638w; all ≤2 fences). No density re-split needed — no page approaches the ≤2,500w / ≤6-fence / ≤400-line caps; 7 notes, no splits, no merges.

**What was locked.** Replaced `## Candidate Cross-References` with `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`
repos — 0 missing). All 105 distinct existing relative-path links resolve on the filesystem from `resources/documentation/openclaw/oc_*.md`
plus 2 planned sibling/concept `oc_*` docs of THIS series (created in this run / redirected per G5).

**Per-note counts (all floors met):**

| Note | Terms | Snippets | Docs (existing/total) | Repos | Floors (≥8t·≥10s·≥10d) |
|---|---:|---:|---:|---:|---|
| oc_reference_templates_identity | 8 | 11 | 9 / 11 | 2 | PASS |
| oc_reference_templates_identity_dev | 8 | 10 | 8 / 10 | 3 | PASS |
| oc_reference_templates_soul | 8 | 10 | 9 / 11 | 3 | PASS |
| oc_reference_templates_soul_dev | 8 | 10 | 8 / 10 | 3 | PASS |
| oc_reference_templates_tools | 8 | 10 | 9 / 11 | 3 | PASS |
| oc_reference_templates_tools_dev | 8 | 10 | 8 / 10 | 3 | PASS |
| oc_reference_templates_user | 8 | 10 | 8 / 10 | 2 | PASS |

**Step 2d new-term re-scan (post source re-read): NONE.** Per the master design decision (mirrors `claude_code`/`pi`), OpenClaw
vocabulary is digested as `oc_*` doc notes by its home sub-plan; the only `term_dictionary` interaction is linking existing terms.
Re-read surfaced no genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing note. **New-term candidates: 0.**
Confirmed-MISSING vocabulary (`term_agent_workspace`, `term_system_prompt`, `term_agent_memory`, `term_session`, `term_skill`,
`term_agent_identity`, `term_ai_persona`, `term_memory`, `term_steering`, `term_imessage`, `term_imsg`, `term_elevenlabs`) routes to
planned `oc_*` concept notes (co01/co03/co07) per master — best-fit glossary if any were ever captured would be
`0_entry_points/acronym_glossary_*` (AI/agent vocabulary). NOT cited as existing anywhere in the mapping.

**Collision/dedup audit (Step 10.5f, generalized to all 7 doc notes):** searched `term_dictionary/` AND `resources/documentation/`.
No planned `oc_reference_templates_*` doc note duplicates an existing term or doc note — each is a distinct source-page artifact
(the *templates*; the *semantics* live in the planned concept notes co01/co03/co07, link-out only). 0 removals, 0 renames.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review of this sub-plan after augmentation.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table present (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 format · G2 grounding · G3 density+coverage · G4 cross-ref · G5 ghost detect+redirect · G6 broken-link fix · G7 discoverability (outbound) · G8 in-degree ≥1. |
| CP4 | Size | **PASS** | 7 notes, single phase — well under 30; sub-plan of the 105-sub-plan master split. |
| CP6 | Density (borderline → split) | **PASS** | Largest source page 638w; largest digest target 420w; ≤1 code fence/note. No borderline notes; `## Density Re-Assessment` confirms all within caps. |
| CP7 | Sources measured (not guessed) | **PASS** | All 7 source pages re-read 2026-06-21 from `inbox/openclaw_docs/reference/templates/`; measured words match the plan's Source table; small pages (100–638w) consistent. |
| CP8 | Undigested Terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present; expected new captures = 0 (master design); `## Term-Note Authoring Requirements` = N/A (0 new terms), inherited multi-source mandate would apply only if a term were proposed. No `TBD` rows. |
| CP8f | Slug specificity / collision audit | **PASS** | Collision/dedup audit run over all 7 doc notes against `term_dictionary/` AND `documentation/`; 0 doc note duplicates an existing term/doc; 0 renames, 0 removals (no `term_*` slugs to specificity-audit — 0 new terms). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks` maps every new note to ≥1 outside-folder inbound link; `entry_openclaw_docs.md` (W1 pre-step) guarantees in-degree ≥1 for all 7; G8 present in the gate table as an EXECUTED/verified phase. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
