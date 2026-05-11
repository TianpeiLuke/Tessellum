---
tags:
  - resource
  - skill
  - procedure
  - folgezettel
  - knowledge_management
keywords:
  - append to trail
  - tessellum append to trail
  - in-vault skill canonical
topics:
  - Skill Procedures
  - Vault Tools
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
pipeline_metadata: none
---

# Procedure: tessellum-append-to-trail (Canonical Body)

This is the **single canonical body** for the `tessellum-append-to-trail` skill. Adapted from the parent project's `skill_slipbox_append_to_trail.md` for Tessellum's `tessellum fz` CLI, simpler `notes` schema, and per-trail entry-point convention (`entry_<topic>_trail.md`).

## Skill description <!-- :: section_id = skill_description :: -->

Append any note to a Folgezettel trail. Finds the proposed parent, assigns the next FZ number, creates or updates the note with FZ YAML fields, adds an inlink from the parent, and updates the trail's entry point (FZ tree + summary table). If no trail exists, creates a new root. Works for any building block.

## Setup <!-- :: section_id = setup :: -->

```bash
source .venv/bin/activate
tessellum --version
# tessellum 0.0.41
tessellum index build       # ensure the unified index is current
```

Default DB: `./data/tessellum.db`. Vault root: `./vault/`. Override per-invocation with `--db` / vault path arguments where the CLI accepts them.

## Resources <!-- :: section_id = resources :: -->

- **CLI**: `tessellum fz {ancestors|descendants|path|show|list|all}` — trail traversal
- **CLI**: `tessellum filter --has-folgezettel --folgezettel-prefix <N>` — direct metadata filter
- **CLI**: `tessellum format check <path>` — validate the new/updated note before commit
- **CLI**: `tessellum index build` — refresh the DB after writing the note
- **Spec**: [DEVELOPING.md § Folgezettel-trail notes](../../../DEVELOPING.md) — the YAML pair (`folgezettel` + `folgezettel_parent`) rules enforced by TESS-001/002

### Entry-Point Mapping <!-- :: section_id = entry_point_mapping :: -->

Tessellum convention: one entry point per trail subject, named `entry_<topic>_trail.md`. The master index is `entry_folgezettel_trails.md`. Use `tessellum fz ancestors <FZ>` to find the trail root, then look up the entry point by topic.

| Trail Root(s) | Entry Point | Has FZ Tree | Has Table |
|---|---|---|---|
| 1 (Architecture / CQRS) | `0_entry_points/entry_architecture_trail.md` | ✅ | ✅ |
| 2 (Dialectic / DKS) | `0_entry_points/entry_dialectic_trail.md` | ✅ | ✅ |
| 3 (Retrieval / System D) | `0_entry_points/entry_retrieval_trail.md` | ✅ | ✅ |
| New trail | Create new `entry_<topic>_trail.md` and link it from `entry_folgezettel_trails.md` | — | — |

The mapping above is current at v0.0.41; expand it as new trails are introduced.

## Step 1: Identify the Parent and Context <!-- :: section_id = step_1_identify_the_parent_and_context :: -->

### 1a. If user specifies a parent FZ number <!-- :: section_id = 1a_user_specifies_parent_fz :: -->

Show the parent's current descendants and ancestors for context:

```bash
tessellum fz descendants "$PARENT_FZ"
tessellum fz ancestors   "$PARENT_FZ"
```

### 1b. If user provides a topic but no parent <!-- :: section_id = 1b_user_provides_topic :: -->

Search the index for related FZ notes by keyword:

```bash
tessellum search "<topic keywords>" --hybrid --has-folgezettel
```

Present the FZ candidates and ask the user to confirm the parent.

### 1c. If user wants a new root trail <!-- :: section_id = 1c_user_wants_new_root :: -->

Find the next available trail root (an integer FZ with no parent):

```bash
tessellum fz list
```

The next root = `max(trail_id) + 1`.

## Step 2: Assign the Next FZ Number <!-- :: section_id = step_2_assign_the_next_fz_number :: -->

List the parent's existing children:

```bash
tessellum fz descendants "$PARENT_FZ"
```

(The first level of indentation is the direct-child set.)

**Numbering rules**:
1. No children yet — append `a` (letter) or `1` (number). Check the parent's own suffix to match convention: if parent ends in a digit (e.g. `1a1`), children use letters (`1a1a`). If parent ends in a letter (e.g. `1a`), children use numbers (`1a1`).
2. Existing children `1a1a`, `1a1b`, `1a1c` — next is `1a1d`.
3. Verify uniqueness — the suggested FZ MUST NOT already exist:

```bash
tessellum filter --folgezettel-prefix "$SUGGESTED_FZ" --has-folgezettel
```

If a row is returned with `FZ=<suggested>` exactly, the FZ is taken — increment and try again.

**MUST present the suggested FZ to the user and get confirmation before proceeding.**

## Step 3: Create or Update the Note <!-- :: section_id = step_3_create_or_update_the_note :: -->

### 3a. New note — determine file location <!-- :: section_id = 3a_new_note_location :: -->

The note's directory depends on its **building block**, NOT the FZ trail:

| Building Block | Typical Location |
|---|---|
| `argument`, `counter_argument` | `vault/resources/analysis_thoughts/` |
| `empirical_observation` | `vault/archives/experiments/` |
| `concept` (term) | `vault/resources/term_dictionary/` |
| `model` | `vault/areas/models/` |
| `procedure` (SOP / skill) | `vault/resources/skills/` |
| `procedure` (how-to) | `vault/resources/how_to/` |
| `navigation` (entry point) | `vault/0_entry_points/` |
| Project-specific | `vault/projects/<project>/` |

Ask the user for the building block if not obvious from context.

### 3b. Existing note — add FZ fields to YAML <!-- :: section_id = 3b_existing_note_add_fz_yaml :: -->

If the note already exists but has no FZ fields, add them to the YAML frontmatter:

```yaml
folgezettel: "<assigned_fz>"
folgezettel_parent: "<parent_fz>"
```

Insert these after the `building_block` field (or at the end of the YAML block before the closing `---`). Both fields are required together — TESS-001/TESS-002 will flag a half-pair.

### 3c. New note — create with FZ fields <!-- :: section_id = 3c_new_note_create_with_fz :: -->

Author the note with standard YAML frontmatter that includes the pair:

```yaml
folgezettel: "<assigned_fz>"
folgezettel_parent: "<parent_fz>"
```

The title SHOULD include the FZ number: `# <Title> (FZ <number>)`.

### 3d. Add a link to the parent in the body <!-- :: section_id = 3d_add_parent_inlink :: -->

In the new/updated note's "Related Notes" (or equivalent) section, link the parent:

```markdown
- **Parent**: [FZ <parent_fz>: <parent_title>](<relative_path_to_parent>)
```

## Step 4: Add Inlink from Parent <!-- :: section_id = step_4_add_inlink_from_parent :: -->

Open the parent note, find its "Related Notes" section (or equivalent — "Related Programs", "Related Models", ...):

```bash
grep -n "## Related" vault/<parent_path>
```

Add the new child inside the existing section:

```markdown
- [FZ <child_fz>: <child_title>](<relative_path_to_child>) — <one-line summary>
```

**CRITICAL**: Place the inlink INSIDE the existing Related section, NOT appended to the file footer.

## Step 5: Update the Entry Point <!-- :: section_id = step_5_update_the_entry_point :: -->

### 5a. Determine which entry point to update <!-- :: section_id = 5a_determine_entry_point :: -->

```bash
tessellum fz ancestors "$ASSIGNED_FZ" | head -3
```

The root FZ number determines the entry point (see [Entry-Point Mapping](#entry-point-mapping) above).

### 5b. Update the FZ tree (ASCII art) <!-- :: section_id = 5b_update_fz_tree :: -->

Find the parent's line in the FZ tree:

```bash
grep -n "$PARENT_FZ" vault/0_entry_points/<entry_point>.md | head -5
```

Insert the new node as a child. Follow the existing indentation pattern:
- Each depth level uses consistent spacing
- Use `├──` for non-last children, `└──` for last child
- If the new note makes a previously-last child no longer last, change its `└──` to `├──`

**Tree topology rules**:
- Siblings at the same level are ordered by FZ number (numeric-aware: `1b` < `1b2` < `1c`)
- The new node goes after all existing siblings of the same parent

### 5c. Update the summary table <!-- :: section_id = 5c_update_summary_table :: -->

Find the table section and insert a new row after the parent's last descendant row:

```markdown
| **<fz>** | [<title>](<relative_path>) | <building_block> | <one-line summary> |
```

The row goes in FZ order — after the last row whose FZ is a descendant of the same parent, and before the next sibling subtree.

### 5d. Update the master FZ index <!-- :: section_id = 5d_update_master_index :: -->

`entry_folgezettel_trails.md` aggregates per-trail counts. Bump the relevant trail's node count (e.g. "Trail 1: 6 nodes" → "Trail 1: 7 nodes") and the totals line at the top.

## Step 6: Validate and Finalize <!-- :: section_id = step_6_validate_and_finalize :: -->

### 6a. Validate the new/updated note <!-- :: section_id = 6a_validate_note :: -->

```bash
tessellum format check vault/<note_path>
```

Fix any errors (broken links, missing YAML fields, TESS-001/002 half-pair).

### 6b. Refresh the index <!-- :: section_id = 6b_refresh_index :: -->

```bash
tessellum index build
```

### 6c. Verify the FZ node is indexed <!-- :: section_id = 6c_verify_fz_indexed :: -->

```bash
tessellum filter --folgezettel-prefix "$ASSIGNED_FZ" --has-folgezettel
```

The new FZ should appear with the correct `folgezettel_parent`.

### 6d. Verify trail connectivity <!-- :: section_id = 6d_verify_connectivity :: -->

```bash
tessellum fz ancestors "$ASSIGNED_FZ"
```

The ancestor chain should show a connected path from root to the new note.

## Step 7: Commit and Push <!-- :: section_id = step_7_commit_and_push :: -->

Stage only the modified files:

```bash
git add vault/<new_note_path> vault/<parent_note_path> vault/0_entry_points/<entry_point>.md data/tessellum.db
```

Commit with a descriptive message:

```bash
git commit -m "Add FZ <number>: <title> to <trail_name> trail

- <building_block> note appended under FZ <parent>
- Updated <entry_point> (tree + table)
- Added inlink from parent"
```

Push to mainline:

```bash
git push
```

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|-------|-------|----------|
| FZ number already exists | Collision with existing note | Increment and try next available |
| Parent FZ not found | Typo, or parent not in the index | `tessellum filter --has-folgezettel \| grep <partial>` to find alternatives |
| Entry point has no FZ tree | Trail not yet tracked | Create a new `entry_<topic>_trail.md` and add the trail to `entry_folgezettel_trails.md` |
| `tessellum format check` reports errors | Broken links or missing YAML pair | Fix before committing (Step 6a) |
| Tree indentation mismatch | Inconsistent spacing in entry point | Read surrounding lines and match exactly |
| TESS-001 / TESS-002 fired | Half-pair `folgezettel`/`folgezettel_parent` | Add the missing field, or remove both |

## Checklist <!-- :: section_id = checklist :: -->

Before marking complete, verify:
- [ ] FZ number is unique (no duplicates in DB)
- [ ] YAML has both `folgezettel` and `folgezettel_parent` fields
- [ ] Note title includes FZ number
- [ ] Parent note has inlink to the new child (inside Related section)
- [ ] Entry-point FZ tree updated (correct indentation, sibling ordering)
- [ ] Entry-point table updated (row in correct FZ order)
- [ ] `entry_folgezettel_trails.md` master index counts bumped
- [ ] `tessellum format check` passes with 0 errors on the changed files
- [ ] `tessellum index build` succeeds
- [ ] `tessellum fz ancestors <new_fz>` shows a connected path from root
- [ ] Changes committed and pushed

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [Folgezettel Trails Master](../../0_entry_points/entry_folgezettel_trails.md) — vault-wide FZ trail index
