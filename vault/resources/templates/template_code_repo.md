---
tags:
  - area
  - code_repo
  - template
keywords:
  - code repo template
  - repository note skeleton
  - main and sub-note structure
  - repo documentation
topics:
  - Note Format
  - Templates
  - Code Documentation
language: markdown
date of note: 2026-05-10
status: template
building_block: model
code_repo_url: https://example.com/owner/repo
---

# Repository: <Name> — <One-Line Description>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy this file to vault/areas/code_repos/repo_<slug>.md
   (or use `tessellum capture code_repo <slug>`).
2. Fill in the YAML frontmatter — especially `code_repo_url` (point at the
   public source repo, e.g. GitHub / GitLab / sourcehut).
3. The repo note is the *parent*: a 'main' note that surveys the repo. Each
   major module gets its own *sub-note* `repo_<slug>_<module>.md` that
   declares the parent in its body via `**Parent**: repo_<slug>.md`.
4. Required sections: Overview, Code Structure, References.
5. Add `## Architecture` only when the repo has 3+ subsystems worth diagramming.
6. Add `## Sub-Notes` only when you've authored sub-notes (one row per module).
7. Status field: change `template` → `active` once authored.
8. Remove this commentary block.

EPISTEMIC FUNCTION (Defining): a code-repo note positions a repository within
the vault — what it does, where its parts live, what it depends on, and which
other notes connect to it. It's a navigational anchor, not a code mirror.
-->

## Overview

<2-3 sentences: what the repository does, who it's for, what makes it worth a
note in the vault.>

| Attribute | Value |
| --------- | ----- |
| Repo URL | `https://github.com/<owner>/<repo>` |
| Language | <python\|rust\|typescript\|...> |
| License | <MIT\|Apache-2.0\|GPL-3.0\|...> |
| Owner | <maintainer or organization> |
| Key dependencies | <library_a, library_b, ...> |
| Install | `pip install <pkg>` (or `cargo add`, `npm i`, etc.) |

## Architecture

<!-- Optional — include only when the repo has 3+ subsystems worth diagramming.
     Use ASCII or Mermaid; keep it skimmable. Drop if not applicable. -->

```
<repo>/
├── <subsystem_a>/    # role
├── <subsystem_b>/    # role
└── <subsystem_c>/    # role
```

## Sub-Notes

<!-- Optional — one row per module that has its own sub-note. The sub-note's
     body declares `**Parent**: repo_<slug>.md` so the relationship resolves
     in both directions. Drop this section if no sub-notes exist yet. -->

| Module | Sub-note | One-line description |
| ------ | -------- | -------------------- |
| <module_a> | [`repo_<slug>_<module_a>.md`](repo_<slug>_<module_a>.md) | <description> |
| <module_b> | [`repo_<slug>_<module_b>.md`](repo_<slug>_<module_b>.md) | <description> |

## Code Structure

<Tree-style directory listing 2-3 levels deep. Include line counts only when
they're load-bearing (e.g., to motivate which modules deserve sub-notes).>

```
<repo>/
├── src/
│   ├── <package>/
│   │   ├── __init__.py
│   │   ├── <module_a>.py
│   │   └── <module_b>.py
│   └── ...
├── tests/
├── docs/
└── pyproject.toml
```

## Key Contributors

<!-- Optional — drop if not applicable. -->

| Contributor | Primary contributions |
| ----------- | --------------------- |
| <name> | <area of code> |

## References

### Related Terms

- [`term_<concept>.md`](../../resources/term_dictionary/term_<concept>.md) — <relationship>

### Related Code Repos

- [`repo_<other>.md`](repo_<other>.md) — <relationship>

### Related Code Snippets

- [`snippet_<repo>_<component>.md`](../../resources/code_snippets/snippet_<repo>_<component>.md) — <component>

### External Links

- Source: `https://github.com/<owner>/<repo>`
- Documentation: `https://<docs-url>`

<!-- Minimum: 1 term link + 1 external link (the repo URL). Add related
     repos, snippets, papers, teams, projects when applicable. -->
