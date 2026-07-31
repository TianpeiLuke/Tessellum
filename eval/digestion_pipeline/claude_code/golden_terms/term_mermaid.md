---
tags:
  - resource
  - terminology
  - documentation
  - developer_tools
keywords:
  - Mermaid
  - Mermaid.js
  - mermaid-js
  - diagram as code
  - text-to-diagram
  - flowchart
  - sequence diagram
  - class diagram
  - mmdc
  - fenced mermaid block
  - architecture diagram
  - mindmap
  - quadrant chart
  - Live Editor
topics:
  - documentation engineering
  - diagramming
  - developer tooling
  - knowledge graph visualization
language: markdown
date of note: 2026-06-25
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Mermaid - JavaScript Text-to-Diagram Rendering Tool

## Definition

**Mermaid** (also written **Mermaid.js**) is an open-source JavaScript diagramming and charting tool that renders Markdown-inspired plain-text definitions into SVG diagrams. Authors describe a diagram in a compact, declarative text syntax — for example `graph TD; A-->B;` for a flowchart or `CUSTOMER ||--o{ ORDER : places` for an entity-relationship diagram — and Mermaid's renderer dynamically produces the corresponding visual. Its founding purpose is to fight "doc-rot": by treating diagrams as version-controllable, diffable text co-located with source code, Mermaid keeps diagrams cheap to modify so that documentation can keep pace with development rather than drifting out of date. It ships as an npm package and CDN bundle, has a hosted Live Editor (mermaid.live) and a `mmdc` command-line renderer (the sibling `mermaid-cli` project), and won the 2019 JavaScript Open Source Award.

As of v11 (11.15.x), Mermaid supports a large and still-growing family of diagram types from a single declarative grammar: `flowchart`/`graph`, `sequenceDiagram`, `classDiagram`, `stateDiagram(-v2)`, entity-relationship (`erDiagram`), `userJourney`, `gantt`, `pie`, `quadrantChart`, `requirementDiagram`, `gitGraph`, `mindmap`, `timeline`, `zenuml`, and `c4` (experimental), plus a wave of newer chart/diagram kinds — `architecture`, `sankey`, `xychart`, `block`, `packet`, `kanban`, `radar`, `treemap`, `venn`, `eventmodeling`, and Wardley/Ishikawa diagrams. Rendering is configured globally through `mermaid.initialize({...})`, which controls theming (named themes plus per-diagram CSS variables), layout engines, accessibility metadata, icon registration, and a `securityLevel` that can sandbox untrusted diagram source inside an iframe to block embedded scripts — the setting that matters whenever a host renders user- or agent-supplied diagram text inline.

## Key Characteristics

- **Diagram as code**: diagrams are authored as version-controllable, diffable plain text rather than as binary image files, keeping them co-located with source and cheap to edit.
- **Markdown-inspired syntax**: a compact declarative grammar (e.g. `graph TD`, `sequenceDiagram`, `erDiagram`, `gantt`) that is readable as text and densely represented in LLM training data.
- **JavaScript renderer producing SVG**: a client-side JS engine parses the text definition and dynamically generates a scalable vector graphic, enabling theme-aware styling and responsive layout.
- **Broad and growing diagram family (v11)**: flowchart, sequence, class, state, ER, user-journey, Gantt, pie, quadrant, requirement, git graph, mindmap, timeline, ZenUML, C4 (experimental), plus newer kinds — architecture, sankey, XY chart, block, packet, kanban, radar, treemap, venn, and event-modeling — all from one tool.
- **Configuration & theming**: `mermaid.initialize({...})` controls named/CSS-variable themes, layout engines, accessibility metadata, and icon registration, so diagrams adapt to light/dark and host styling.
- **Fights doc-rot**: explicit design goal of helping documentation keep pace with development by lowering the cost of maintaining diagrams.
- **Inline fenced-block convention**: hosts detect ```` ```mermaid ```` fenced code blocks and render them in place (GitHub, GitLab).
- **Distribution surface**: npm package, jsDelivr CDN bundle, hosted Live Editor (mermaid.live), and the `mmdc` (mermaid-cli) command-line renderer.
- **Security posture for untrusted input**: a `securityLevel` setting can sandbox untrusted diagram source in an iframe to block embedded scripts — relevant when any host renders user-/agent-supplied content inline.

## References

- [Mermaid — Official Documentation (Introduction)](https://mermaid.js.org/intro/)
- [Mermaid — Diagram Syntax Index (full v11 diagram-type list)](https://mermaid.js.org/syntax/flowchart.html)
- [Mermaid — Configuration & Theming (initialize, securityLevel)](https://mermaid.js.org/config/configuration.html)
- [Mermaid Live Editor](https://mermaid.live/)
- [mermaid-js/mermaid — Official GitHub Repository](https://github.com/mermaid-js/mermaid)
- [mermaid-js/mermaid-cli — `mmdc` command-line renderer](https://github.com/mermaid-js/mermaid-cli)
