---
tags:
  - resource
  - skill
  - procedure
  - folgezettel
  - knowledge_management
keywords:
  - traverse folgezettel
  - tessellum traverse folgezettel
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

# Procedure: tessellum-traverse-folgezettel (Canonical Body)

This is the **single canonical body** for the `tessellum-traverse-folgezettel` skill. Per-runtime thin-headers (`.claude/skills/...`, `.kiro/skills/...`) can be wired later as needed; this file is the single source of truth for the procedure. Adapted from the parent project's `skill_slipbox_traverse_folgezettel.md` for Tessellum's `tessellum fz` CLI.

## Skill description <!-- :: section_id = skill_description :: -->

Traverse Folgezettel trails before and after a given note. Shows the full ancestor chain (root to note) and all possible continuation paths (note to descendants). Use when exploring how an idea developed, finding what led to a conclusion, or discovering where a thought trail branches next.

## Setup <!-- :: section_id = setup :: -->

```bash
source .venv/bin/activate
tessellum --version
# tessellum 0.0.41
```

The trail explorer reads the unified index. Build it first if it does not exist:

```bash
tessellum index build
```

## Resources <!-- :: section_id = resources :: -->

- **CLI**: `tessellum fz {list|show|ancestors|descendants|path|all}` (sub-subcommand of the main CLI)
- **Library**: trail traversal is implemented in [`src/tessellum/cli/fz.py`](../../../src/tessellum/cli/fz.py) over the `notes.folgezettel` + `notes.folgezettel_parent` columns. Tessellum has no pre-materialised `folgezettel_trails` view — topology is derived in-memory.
- **Index DB**: defaults to `./data/tessellum.db`; override with `--db <path>` on every sub-subcommand.

## Step 1: Resolve the Note <!-- :: section_id = step_1_resolve_the_note :: -->

Given a user query (FZ number or exact note_name file-stem), confirm the note exists:

```bash
tessellum fz ancestors "$USER_INPUT"
```

If the note has no FZ, an informational line is printed and exit code is 0. To find candidate FZ notes by partial name:

```bash
tessellum filter --has-folgezettel | grep -i "$USER_INPUT"
```

Report the resolved note: FZ number, note_name, building block, depth in the chain.

## Step 2: Show the Trail Before (Ancestors) <!-- :: section_id = step_2_show_the_trail_before_ancestors :: -->

Display the full ancestor chain from root to the target note:

```bash
tessellum fz ancestors "$FZ_NUMBER"
```

Present as an indented chain showing:
- FZ number
- Note name (as a markdown link if presenting in markdown)
- Building block type
- The intellectual transition at each step (what changed from parent to child)

**Reading guide for the user**: "Read these notes in order to understand how the thinking evolved to reach this point."

## Step 3: Show the Trail After (Continuations) <!-- :: section_id = step_3_show_the_trail_after_continuations :: -->

Display all descendants — the possible paths forward:

```bash
tessellum fz descendants "$FZ_NUMBER"
```

If there are multiple branches, explain what each branch explores:
- Count direct children (immediate next steps)
- For each child, show subtree size and BB type
- Highlight notable synthesis or counter-argument nodes

**Reading guide for the user**: "These are the directions the thinking went after this note. Pick the branch that matches your interest."

## Step 4: Show Siblings (Alternative Paths) <!-- :: section_id = step_4_show_siblings_alternative_paths :: -->

Show notes at the same level (same parent) — parallel investigations:

```bash
tessellum fz path "$FZ_NUMBER"
```

The "Siblings (same parent ...)" section lists what other directions were explored from the same parent. (Trail roots have no parent, so this section is empty for FZ `1`, `2`, etc.)

## Step 5: Summarize <!-- :: section_id = step_5_summarize :: -->

Present a structured summary:

```markdown
## Trail for FZ {number}: {note_name}

### Before (Ancestors — {depth} steps from root)
{indented ancestor chain with BB types}

### After (Continuations — {N} descendants across {M} branches)
{indented descendant tree}

### Siblings ({K} parallel investigations from same parent)
{sibling list}

### Reading Recommendation
- To understand context: read ancestors top-down
- To explore further: {recommend the most promising branch based on BB diversity or depth}
```

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|-------|-------|----------|
| `No FZ note matching '<query>'` | Wrong FZ number, wrong note_name, or note has no FZ field | Use `tessellum filter --has-folgezettel` and search by partial name |
| `index DB not found at ...` (exit 2) | DB has not been built yet | Run `tessellum index build` |
| `missing sub-subcommand` (exit 2) | `tessellum fz` called with no operation | Append one of `list`, `show <FZ>`, `ancestors <FZ>`, `descendants <FZ>`, `path <FZ>`, `all` |

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [Folgezettel Trails Master](../../0_entry_points/entry_folgezettel_trails.md) — vault-wide FZ trail index
