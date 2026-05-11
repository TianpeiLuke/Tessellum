---
tags:
  - resource
  - skill
  - procedure
  - folgezettel
  - knowledge_management
keywords:
  - manage folgezettel
  - tessellum manage folgezettel
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

# Procedure: tessellum-manage-folgezettel (Canonical Body)

This is the **single canonical body** for the `tessellum-manage-folgezettel` skill. Adapted from the parent project's `skill_slipbox_manage_folgezettel.md` for Tessellum's `tessellum fz` CLI and simpler schema (no `folgezettel_trails` / `folgezettel_edges` materialised tables — topology lives on `notes.folgezettel` + `notes.folgezettel_parent`).

## Skill description <!-- :: section_id = skill_description :: -->

Manage Folgezettel (FZ) trails in the vault. List all trails, find the next available FZ number for a parent, detect duplicates, check integrity (orphaned parents), and visualise trail topology. Use when creating a new thought/argument/counter note that needs an FZ number, or when auditing trail health.

## Setup <!-- :: section_id = setup :: -->

```bash
source .venv/bin/activate
tessellum --version
# tessellum 0.0.41
tessellum index build       # rebuild if stale
```

Default DB path is `./data/tessellum.db`. Override with `--db <path>` on the `tessellum fz` / `tessellum filter` calls below.

## Resources <!-- :: section_id = resources :: -->

- **CLI**: `tessellum fz {list|show|ancestors|descendants|path|all}` — trail topology
- **CLI**: `tessellum filter --has-folgezettel --folgezettel-prefix <N>` — direct metadata filter
- **DB**: `./data/tessellum.db` — the `notes` table has `folgezettel` + `folgezettel_parent`. There is no `folgezettel_trails` view; the explorer derives trail_id (leading numeric token) and depth (parent-chain length) in memory.

## Step 1: List All Trails <!-- :: section_id = step_1_list_all_trails :: -->

```bash
tessellum fz list
```

Reports each trail's node count, max depth (ancestor-chain length from the deepest node), and the set of building blocks the trail contains. Trails are sorted by node count descending. Use the totals line (`N nodes across M trails`) as a quick sanity check on overall vault size.

## Step 2: Show a Specific Trail Subtree <!-- :: section_id = step_2_show_a_specific_trail_subtree :: -->

Given an FZ number (e.g. `1a`), show its full subtree:

```bash
tessellum fz show 1a
```

The subtree is rooted at the resolved FZ — pass the **trail root** (`1`, `2`, ...) to see the entire trail; pass an inner node to see only its subtree. Output is indented by depth-from-root and includes the building block and second-category tag for each node.

## Step 3: Find Next Available FZ Number <!-- :: section_id = step_3_find_next_available_fz_number :: -->

Given a parent FZ (e.g. `1a`), list its existing children:

```bash
tessellum fz descendants 1a
```

The first level of indentation shows the direct children. **Numbering rules for suggesting the next FZ**:

1. Parent has no children — suggest `{parent}a` (first letter child) or `{parent}1` (first number child). Look at parent's own suffix: if parent ends in a digit (e.g. `1a1`), children use letters (`1a1a`). If parent ends in a letter (e.g. `1a`), children use numbers (`1a1`).
2. Parent has children `1a1a`, `1a1b`, `1a1c` — suggest `1a1d`.
3. Verify uniqueness — the suggested FZ MUST NOT already exist:

```bash
tessellum filter --folgezettel-prefix "$SUGGESTED_FZ" --has-folgezettel
```

If any row is returned where `FZ=<suggested>` exactly, the FZ is taken — increment and try again.

**MUST** report the suggested FZ to the user before they create the note.

## Step 4: Detect Duplicate FZ Numbers <!-- :: section_id = step_4_detect_duplicate_fz_numbers :: -->

The unified index does not enforce uniqueness; two notes can share the same FZ. List every FZ-bearing note and look for collisions:

```bash
tessellum filter --has-folgezettel --format json | \
  jq -r '.hits[] | "\(.folgezettel)\t\(.note_name)"' | sort | uniq -c -w 20 | awk '$1 > 1'
```

If duplicates are found, report each with both note names. Suggest reassigning the non-canonical note (the one NOT referenced in the relevant trail entry point).

## Step 5: Check Trail Integrity <!-- :: section_id = step_5_check_trail_integrity :: -->

### 5a. Orphaned Parents (FZ parent references non-existent FZ) <!-- :: section_id = 5a_orphaned_parents :: -->

```bash
sqlite3 ./data/tessellum.db "
SELECT note_name, folgezettel, folgezettel_parent
FROM notes
WHERE folgezettel_parent IS NOT NULL
  AND folgezettel_parent NOT IN
      (SELECT folgezettel FROM notes WHERE folgezettel IS NOT NULL);
"
```

Report each orphan with its parent reference. Either create the missing parent note or correct the `folgezettel_parent` YAML field on the child.

### 5b. Trail Statistics <!-- :: section_id = 5b_trail_statistics :: -->

```bash
sqlite3 ./data/tessellum.db "
SELECT
  COUNT(*) AS total_fz_notes,
  SUM(CASE WHEN folgezettel_parent IS NULL THEN 1 ELSE 0 END) AS roots,
  SUM(CASE WHEN folgezettel_parent IS NULL THEN 0 ELSE 1 END) AS children
FROM notes
WHERE folgezettel IS NOT NULL;
"
```

A healthy vault has `roots = number_of_trails` and `total = roots + children`. Cross-check against `tessellum fz list`.

### 5c. BB Transition Audit (optional) <!-- :: section_id = 5c_bb_transition_audit :: -->

```bash
sqlite3 ./data/tessellum.db "
SELECT p.building_block AS parent_bb, c.building_block AS child_bb, COUNT(*) AS n
FROM notes c
JOIN notes p ON c.folgezettel_parent = p.folgezettel
WHERE c.folgezettel IS NOT NULL
GROUP BY p.building_block, c.building_block
ORDER BY n DESC;
"
```

Surfaces the typed-edge distribution. Useful for spotting unusual transitions (e.g. `concept -> empirical_observation` may indicate a misclassified note).

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|-------|-------|----------|
| `No FZ note matching '<query>'` | The FZ has not been indexed, or note has no FZ field | Re-build the index: `tessellum index build` |
| `index DB not found` (exit 2) | `./data/tessellum.db` does not exist | `tessellum index build` from the vault root |
| Duplicate FZ found | Two notes share the same FZ number | Reassign the non-canonical note (Step 4) |
| Orphaned parent | Note references a parent FZ that does not exist | Create the parent note, or fix the `folgezettel_parent` YAML on the child |
| Suggested FZ already exists | Step-3 numbering collided | Increment (next letter or next number) and re-verify with `tessellum filter --folgezettel-prefix` |

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [Folgezettel Trails Master](../../0_entry_points/entry_folgezettel_trails.md) — vault-wide FZ trail index
