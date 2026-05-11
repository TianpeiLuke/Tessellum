---
tags:
  - resource
  - analysis
  - skill_design
  - building_blocks
  - routing
keywords:
  - building block mapping
  - second category
  - directory routing
  - content classification
  - note type routing
topics:
  - skill architecture
  - content routing principles
language: markdown
date of note: 2026-04-15
status: active
building_block: argument
folgezettel: "10b"
folgezettel_parent: "10"
---

# Analysis: Building Block × Category × Directory Mapping Principles (FZ 10b)

## Thesis

The vault's routing from (building_block, content_domain) → (directory, note_type) follows discoverable patterns. By analyzing the empirical distribution of 6,186 active notes across 8 building blocks, 30+ second categories, and 15+ directories, we can extract routing principles that generalize to any new input data type.

**Source**: [Universal Content Digestion Skill (FZ 10)](thought_universal_content_digestion_skill.md)

---

## Empirical Mapping: Building Block → Primary Categories

| Building Block | Count | Top Categories (by frequency) |
|---------------|-------|-------------------------------|
| **concept** | 1,504 | terminology (1,308), tutorials (64), code_snippet (49), faq (29) |
| **model** | 1,252 | models (177), code_repo (164), table (120), team (83), rulesets (78), tool (68), etl_job (63) |
| **empirical_observation** | 1,223 | mtr (892), papers (139), slack_slipbot (129), tutorials (20) |
| **procedure** | 1,045 | sop (582), code_snippet (130), tutorials (91), how_to (66), role_guideline (62) |
| **argument** | 696 | analysis (425), papers (198), digest (58) |
| **navigation** | 202 | index (89), tutorials (48), sub_entry (28) |
| **hypothesis** | 175 | research (87), papers (81) |
| **counter_argument** | 89 | papers (76), analysis (13) |

## Principle 1: Building Block Determines the "What" — Category Determines the "Where"

The building block tells you **what kind of knowledge** the note contains. The category tells you **what domain** it belongs to. Together they determine the directory:

```
building_block + content_domain → directory + filename_pattern
```

Examples:
- concept + terminology → `resources/term_dictionary/term_*.md`
- concept + tutorial → `resources/documentation/tutorials/tutorial_*_01_*.md`
- procedure + sop → `resources/policy_sops/sop_*.md`
- procedure + tutorial → `resources/documentation/tutorials/tutorial_*_03_*.md`
- model + team → `resources/teams/team_*.md`
- model + code_repo → `areas/code_repos/repo_*.md`
- empirical_observation + mtr → `resources/documentation/mtr/mtr_*.md`
- argument + analysis → `resources/analysis_thoughts/thought_*.md`

## Principle 2: One Building Block Can Route to Many Directories

No building block maps to a single directory. The content domain is the discriminator:

| Building Block | Directories (count) |
|---------------|-------------------|
| concept | 10 (term_dictionary, tutorials, code_snippets, faqs, wiki, how_to, digest, papers, areas, other) |
| model | 12 (areas, tools, code_snippets, papers, teams, analysis, tutorials, mtr, faqs, policy_sops, projects, other) |
| procedure | 10 (policy_sops, code_snippets, how_to, tutorials, faqs, areas, tools, projects, mtr, other) |
| empirical_observation | 7 (mtr, papers, archives, tutorials, faqs, areas, projects) |
| argument | 9 (analysis_thoughts, papers, digest, faqs, areas, tutorials, how_to, mtr, projects) |

**Implication**: The router cannot use building block alone. It needs (building_block, content_domain) as a composite key.

## Principle 3: Dominant Attractors — Most Notes Cluster in One Category

Despite routing to many directories, each building block has a **dominant attractor** — one category that captures the majority:

| Building Block | Dominant Category | % of Total |
|---------------|------------------|-----------|
| concept | terminology | 87% |
| empirical_observation | mtr | 73% |
| procedure | sop | 56% |
| argument | analysis | 61% |
| counter_argument | papers | 85% |
| hypothesis | research + papers | 96% |
| navigation | index | 44% |
| model | (no single dominant) | max 14% (models) |

**Implication**: For a universal router, the **default** route for each building block should be its dominant attractor. The content domain overrides the default only when it matches a specific non-default pattern.

**Exception**: `model` has no dominant attractor — it's the most polymorphic building block, appearing across 12 directories. Model-typed content requires the content domain signal to route correctly.

## Principle 4: Content Domain Signals for Routing

The content domain can be detected from:

| Signal | Example | Routes To |
|--------|---------|-----------|
| **Heading keywords** | "How to", "Steps to" | how_to/ |
| **Source type** | Quip MTR doc | mtr/ |
| **Source type** | Wiki URL | wiki/ or tutorials/ |
| **Source type** | Code repo | code_repos/ or code_snippets/ |
| **Entity names** | Team names, LDAP groups | teams/ |
| **Entity names** | Table names, DDL | tables/ |
| **Entity names** | ETL job names, Cradle profiles | etl_jobs/ |
| **Entity names** | Intent names, CORBEL | intents/ |
| **Entity names** | Ruleset names, RMP | rulesets/ |
| **Question pattern** | "What is...", "How do I..." | faqs/ |
| **Temporal markers** | "Week N", "Q1 2026", monthly | mtr/ or archives/ |
| **Code blocks** | Python, Java, SQL | code_snippets/ |

## Principle 5: The Routing Table is a Decision Tree

Combining principles 1-4, the routing logic is:

```
1. Classify building_block (from content patterns)
2. Detect content_domain (from source type + heading keywords + entity names)
3. Route:
   IF content_domain matches a specific pattern → use specific directory
   ELSE → use building_block's dominant attractor
4. Generate filename from (directory_convention, entity_name, date)
```

For the universal digestion skill, this means:
- **Step 2 (classify)** produces building_block per segment
- **Step 3 (plan)** detects content_domain from source metadata + segment content
- **Step 4 (route)** applies the decision tree to determine directory + filename + capture skill

## Principle 6: New Input Types Map to Existing Patterns

When encountering a new input type (e.g., SharePoint PDF, Word doc SOP, Broadcast video transcript), the router doesn't need new rules — it maps to existing patterns:

| New Input | Building Block | Content Domain | Routes To (existing) |
|-----------|---------------|---------------|---------------------|
| SharePoint 12-steps PDF | procedure | tutorial | tutorials/ |
| Word doc SOP | procedure | how_to | how_to/ |
| BAE QTR Word doc | empirical_observation | mtr | mtr/ |
| Quip wiki FAQ table | concept | faq | faqs/ |
| Broadcast video transcript | empirical_observation | mtr or analysis | mtr/ or analysis_thoughts/ |
| Slack thread | empirical_observation | slack | archives/slack_history/ |

**The routing table is extensible without modification** — new source types produce the same (building_block, content_domain) pairs that already have routes.

---

## Open Questions

- **OQ46**: Should the model building block be split into sub-types (system_model, data_model, org_model) to improve routing precision?
- **OQ47**: Can content domain detection be automated via a lightweight classifier (keyword matching vs LLM)?
- **OQ48**: How should the router handle content that legitimately spans two categories (e.g., a tutorial that is also an SOP)?

- [FZ 7g: Building Block Ontology](thought_building_block_ontology_relationships.md) — the ontology that the routing decision tree operationalizes
- [FZ 7c: Building Block Vault Health](analysis_building_block_vault_health.md) — distribution diagnostic that the dominant attractor analysis extends

### Forward Extensions (FZ 10d1e1a family — operationalizing this routing rule)

- **[FZ 10d1e1a4](thought_deferred_subcategory_routing_via_add_to_plan_skill.md)** — Operationalizes this BB × category × directory mapping at *add-to-plan* time via the new `slipbox-plan-add-subcategory` sub-skill. The mapping table is the lookup the sub-skill consults; sub-category becomes a content-aware deferred decision rather than a planning-time commitment.
- **[FZ 10d1e1a5 ★](thought_synthesis_knowledge_auto_digest_architecture.md)** — Central design synthesis treats this mapping as one of the parameterizations of the per-source-type YAML configuration; the routing rule lands in the orchestrator's `output_path_resolve` step.
---

## Related Notes

- [Thought: Universal Content Digestion Skill (FZ 10)](thought_universal_content_digestion_skill.md)
- [Analysis: Classify/Route Skill Limitations (FZ 10a)](thought_classify_route_skill_limitations.md)
- [Term: Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md)


