---
tags:
  - resource
  - skill
  - procedure
  - capture
  - code_repo
  - documentation
keywords:
  - capture code repo note
  - tessellum-capture-code-repo-note
  - in-vault skill canonical
topics:
  - Skill Procedures
  - Vault Tools
language: markdown
date of note: 2026-04-28
status: active
building_block: procedure
pipeline_metadata: ./skill_tessellum_capture_code_repo_note.pipeline.yaml
---

# Procedure: tessellum-capture-code-repo-note (Canonical Body)

This is the **single canonical body** for the `tessellum-capture-code-repo-note` skill. This skill is invoked directly by Tessellum's composer (see `tessellum composer compile / run`); no ecosystem shims are needed.

## Skill description <!-- :: section_id = skill_description :: -->

Research and create a code repository documentation note with main+sub-note structure from GitHub. Reads repo tree, README, key source files to document architecture, modules, and design patterns. Creates main note in areas/code_repos/ and sub-notes per major module. Updates entry_code_repos.md and adds inlinks from related vault notes. Use when the user asks to document an internal code repository.

## Setup <!-- :: section_id = setup :: -->

```bash
VAULT_PATH="."   # run from your vault root
# `tessellum search` and `tessellum index build` resolve paths from CWD
```

## Resources <!-- :: section_id = resources :: -->

- **Code repo notes**: `$REPO_DIR/` (areas/code_repos/)
- **Entry point**: `$ENTRY_POINT` (0_entry_points/entry_code_repos.md)
- **Database**: `$DB_PATH` for vault search
- **Reference shape**: `$REPO_DIR/repo_<example>.md` — typical layout is one main note + N module sub-notes (each declaring `**Parent**: repo_<example>.md`)

## Step 1: Check for Existing Notes <!-- :: section_id = step_1_check_for_existing_notes :: -->

```bash
sqlite3 "$DB_PATH" "SELECT note_id FROM notes WHERE note_name LIKE '%repo_<repo_slug>%' ORDER BY note_id"
ls "$REPO_DIR"/repo_<repo_slug>*.md 2>/dev/null
```

If notes already exist, ask the user: update existing notes or skip? Do NOT create duplicates.

## Step 2: Read Repository Structure <!-- :: section_id = step_2_read_repository_structure :: -->

Fetch the repo tree, README, and recent commits from GitHub.

## Step 3: Identify Modules for Sub-Notes <!-- :: section_id = step_3_identify_modules_for_sub_notes :: -->

A module deserves a sub-note if it has 3+ source files and represents a distinct functional concern.

## Step 4: Search Vault for Context <!-- :: section_id = step_4_search_vault_for_context :: -->

Search broadly across vault categories — terms, MTRs, FAQs, how-tos, tools, analysis, teams, projects — for related content. Also search internal wiki / docs for background.

## Step 5: Write Main Note <!-- :: section_id = step_5_write_main_note :: -->

Create `$REPO_DIR/repo_<repo_slug>.md`.

**File naming**: `repo_<lowercase_underscored>.md`

**Required YAML frontmatter**:
- tags: area, code_repo, <domain_tag>
- keywords, topics, language, date of note, last_updated, owner
- status: active, building_block: model
- code_repo_url: https://github.com/<owner>/<REPO_NAME>

**Required sections**:

| Section | Required | Content |
|---------|----------|---------|
| `# Repository: <Name> (<one-line>)` | Yes | H1 title |
| `## Overview` | Yes | 2-3 sentences + attribute table (repo URL, language, owner, deps, install) |
| `## Architecture` | If 3+ subsystems | ASCII box diagram of subsystems |
| `## Sub-Notes` | Yes | Index: `### <Module> (repo_<slug>_<module>.md)` with 1-2 sentence descriptions |
| `## Code Structure` | Yes | Tree-style directory listing 2-3 levels deep |
| `## Key Contributors` | If known | Table: contributor alias, primary contributions |
| `## References` | Yes | `### Related Terms`, `### Related Code Repos`, `### External Links` |

## Step 6: Write Sub-Notes with Full References <!-- :: section_id = step_6_write_sub_notes_with_full_references :: -->

For each module, create `$REPO_DIR/repo_<repo_slug>_<module>.md`.

**Required YAML frontmatter**:
- tags: code_repo, <repo_tag>, <module_tag>
- keywords, topics, language, date of note
- status: active, building_block: model

**Required sections**:

| Section | Required | Content |
|---------|----------|---------|
| `# Code Repo: <Name> — <Module>` | Yes | H1 title |
| `**Parent**: repo_<slug>.md` | Yes | Text backlink to main note |
| `## Overview` | Yes | 1-2 sentences |
| `## Module Structure` | Yes | Tree-style file listing |
| `## Key Components` | Yes | Major classes/functions with signatures and purpose (NOT implementation) |
| `## Cross-Module Connections` | Yes | Consumed by / depends on |
| `## References` | Yes | Include ALL applicable: Related Terms, Related Teams, Related Projects, Related Code Repos, Related FAQs & How-Tos, Related MTR Notes, Related Tools |

Read 2-3 key source files per module via GitHub blobs. Focus on public API signatures and design patterns.

**Batch Validation**: Create sub-notes in batches of 3-5. After each batch, validate:

| Check | Pass Criteria |
|-------|---------------|
| Content faithful | Architecture descriptions match actual code structure |
| Code references | File paths and class/function names match the repository |
| YAML valid | Frontmatter has all required fields, parent_note set, sub_note tag present |
| Links valid | All relative paths to parent note, terms, and areas resolve correctly |

**If any check fails**: fix immediately before proceeding to the next batch.

## Step 7: Update Entry Point <!-- :: section_id = step_7_update_entry_point :: -->

Update `$ENTRY_POINT` with BOTH a full section AND a Quick Reference Table row.

### 7a. Add full section under the appropriate category <!-- :: section_id = 7a_add_full_section_under_the_appropriate_category :: -->

Find the right category heading (ML Pipeline, Data Definition, GenAI & Automation, MCP Server, Evaluation Configuration) and add a full subsection with attribute table (Code URL, Documentation, Language, Key Features, Related).

### 7b. Add row to Quick Reference Table <!-- :: section_id = 7b_add_row_to_quick_reference_table :: -->

### 7c. Update ToC if a new category was created <!-- :: section_id = 7c_update_toc_if_a_new_category_was_created :: -->

## Step 8: Add Inlinks from Related Notes <!-- :: section_id = step_8_add_inlinks_from_related_notes :: -->

After creating all notes, find existing vault notes that mention the repo or its key concepts but don't yet link to the new repo notes.

**Goal**: Add 10-20 inlinks across terms, FAQs, how-tos, MTRs, tools, and team notes.

### 8a. Find candidates <!-- :: section_id = 8a_find_candidates :: -->

```bash
grep -rl "<RepoName>\|<key_concept>" "$VAULT_PATH/resources/" "$VAULT_PATH/areas/" "$VAULT_PATH/projects/" --include="*.md" | grep -v "repo_<repo_slug>" | head -30
```

Also query DB for notes with matching keywords (sorted by PageRank).

### 8b. Filter candidates <!-- :: section_id = 8b_filter_candidates :: -->

A note qualifies if it mentions the repo/concept, does NOT already link to `repo_<repo_slug>`, and is active. Prioritize: terms > tools > FAQs/how-tos > MTRs > teams > analysis.

### 8c. Add inlinks ABOVE footer <!-- :: section_id = 8c_add_inlinks_above_footer :: -->

Add `### Related Code Repos` section. **CRITICAL**: Insert BEFORE the `---` separator that precedes `**Last Updated**`. Never append after footer.

## Step 9: Update Database <!-- :: section_id = step_9_update_database :: -->

```bash
tessellum index build
```

**BM25 alternative** (recommended over grep — ranked results, searches body text):

```bash
tessellum search --bm25 "<KEYWORDS>" --top-k 20 --json
```

With filters:

```bash
tessellum search --bm25 "<KEYWORDS>" --subcategory <TYPE> --top-k 20 --json
```

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|-------|-------|----------|
| Repo not found | Wrong name on GitHub | Ask user to verify repo name |
| Empty/minimal repo | Few source files | Create main note only, skip sub-notes |
| No README | Repo lacks documentation | Infer purpose from code structure and commits |
| Private repo (403) | No access | Ask user for access or provide tree manually |
| Existing notes | Repo already documented | Update existing notes rather than creating duplicates |
| Inlink after footer | Appended below `**Last Updated**` | Move inlink above the `---` separator line |

---

## Important Constraints <!-- :: section_id = important_constraints :: -->

1. **File paths, class names, and function names MUST match the actual code** — do not rename or abbreviate
2. **Config values and dependency names MUST be exact** from package Config or pom.xml
3. **Code examples MUST be verbatim** if included — do not edit or "improve" source code
4. **Synthesis fields are agent-written**: Architecture descriptions, module purpose, design pattern analysis are summaries — write clearly but must accurately reflect the actual code structure
5. **Do NOT describe functionality that doesn't exist in the code** — only document what you read

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [Master TOC](../../0_entry_points/entry_master_toc.md) — full vault skill index, organized by C.O.D.E. stage; this skill's row in the catalog has a back-link to this canonical body
