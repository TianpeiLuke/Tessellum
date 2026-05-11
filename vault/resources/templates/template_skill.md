---
tags:
  - resource
  - template
  - skill
  - procedure
keywords:
  - skill template
  - skill canonical body
  - in-vault skill
  - thin header pattern
  - typed-contract skill
topics:
  - Note Format
  - Templates
  - Skill Architecture
language: markdown
date of note: 2026-05-10
status: template
building_block: procedure
related_skill_headers:
  - .claude/skills/<skill-name>/SKILL.md
  - .kiro/skills/<skill-name>/SKILL.md
pipeline_metadata: none
---

# Procedure: <skill-name> (Canonical Body)

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to `vault/resources/skills/skill_<name>.md` (use snake_case for the name).
2. The thin headers under `.claude/skills/<name>/SKILL.md` and
   `.kiro/skills/<name>/SKILL.md` will point at this canonical body — create
   them after authoring this file.
3. If the skill has typed-contract pipeline steps, also create
   `vault/resources/skills/skill_<name>.pipeline.yaml` and update
   `pipeline_metadata:` field above to point at it; otherwise keep `none`.
4. Update YAML frontmatter — `note_second_category: skill` (still used here for
   skill notes specifically; the parent vault relies on this field for skill
   discovery, so it's kept distinct from the tags-based convention).
5. Fill the H2 sections below. Each H2 must include the
   `<!-- :: section_id = X :: -->` marker — this is parsed by the composer
   pipeline for typed-contract validation.
6. Remove this commentary block.

EPISTEMIC FUNCTION (Doing): a skill canonical body codifies an executable
procedure that an agent can dispatch. It answers "How do we act on this?"
specifically in an agent-runtime context. Distinct from a `how_to` note (which
is for human readers); skills are agent-readable + agent-executable.

The "in-vault skill" pattern (FZ 12 in the parent project): the canonical body
lives in the vault; thin per-ecosystem headers (Claude / Kiro / etc.) point at
it. This deduplicates the body across N ecosystems and lets multiple agent
runtimes share the same procedural ground truth.
-->

## Skill description <!-- :: section_id = skill_description :: -->

<One paragraph describing what the skill does. This text gets surfaced as the
skill's metadata description in Claude Code, Kiro CLI, and other agent
runtimes. Be specific about what triggers the skill: "Use when the user asks
to <X>" or "Use when capturing a new <Y>".>

## Setup <!-- :: section_id = setup :: -->

<Bash setup commands the skill expects to run on first invocation. Common
pattern: resolve paths from `scripts/config.py` rather than hardcoding.>

```bash
SCRIPTS_DIR="./scripts"
DB_PATH=$(python3 -c "import sys; sys.path.insert(0,'$SCRIPTS_DIR'); from config import DB_PATH_STR; print(DB_PATH_STR)")
VAULT_PATH=$(python3 -c "import sys; sys.path.insert(0,'$SCRIPTS_DIR'); from config import VAULT_PATH_STR; print(VAULT_PATH_STR)")
```

## Resources <!-- :: section_id = resources :: -->

<Optional. Files / databases / endpoints the skill depends on.>

- **Database**: `$DB_PATH` for searching the unified index
- **Vault**: `$VAULT_PATH` for reading / writing notes
- **Reference example**: `<path-to-an-example-output>`

## Step 1: <First action> <!-- :: section_id = step_1_first_action :: -->

<What to do, with executable code or queries.>

```bash
# command or query
```

<Expected outcome / how the agent verifies this step succeeded.>

## Step 2: <Second action> <!-- :: section_id = step_2_second_action :: -->

<...>

## Step 3: <Third action> <!-- :: section_id = step_3_third_action :: -->

<...>

## Output <!-- :: section_id = output :: -->

<What the skill produces — file written, DB updated, channel message sent,
return value structure, etc.>

The skill emits:

- **File**: `<vault-relative path>` written / updated
- **DB rows**: <which tables get rows>
- **Notification**: <if applicable, what gets reported back to the user>

## Validation <!-- :: section_id = validation :: -->

<How the agent confirms the skill ran correctly.>

```bash
# Sanity check
grep -q "<expected-marker>" "<output-file>" || echo "MISSING marker"
```

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|---|---|---|
| `<error message>` | <root cause> | <how to fix> |

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [Skill Catalog](../../0_entry_points/entry_skill_catalog.md) — full vault skill index; this skill's row in the catalog has a back-link to this canonical body
- [Templates](README.md) — back to the templates directory
