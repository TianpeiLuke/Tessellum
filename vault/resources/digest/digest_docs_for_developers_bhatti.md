---
tags:
  - resource
  - digest
  - book
  - technical_writing
  - documentation
  - developer_experience
  - software_engineering
keywords:
  - Docs for Developers
  - Jared Bhatti
  - Sarah Corleissen
  - Jen Lambourne
  - David Nunez
  - Heidi Waterhouse
  - technical writing
  - developer documentation
  - friction log
  - curse of knowledge
  - code samples
  - documentation quality
  - content types
  - editing process
  - documentation maintenance
  - user personas
topics:
  - Technical Writing
  - Developer Documentation
  - Software Engineering
  - Documentation Strategy
language: markdown
date of note: 2026-03-18
status: active
building_block: argument
author: lukexie
book_title: "Docs for Developers: An Engineer's Field Guide to Technical Writing"
book_author: "Jared Bhatti, Zachary Sarah Corleissen, Jen Lambourne, David Nunez, Heidi Waterhouse"
publisher: "Apress"
year: 2021
isbn: "978-1-4842-7216-9"
pages: 250
---

# Digest: Docs for Developers — An Engineer's Field Guide to Technical Writing

## Source

- Bhatti, J., Corleissen, Z.S., Lambourne, J., Nunez, D., & Waterhouse, H. (2021). *Docs for Developers: An Engineer's Field Guide to Technical Writing*. Apress. ~250 pages. ISBN: 978-1-4842-7216-9. Foreword by Kelsey Hightower.
- Authors represent Google, Stripe, and the Linux Foundation documentation teams.
- [Springer Nature Link](https://link.springer.com/book/10.1007/978-1-4842-7217-6)
- [Official Book Website](https://docsfordevelopers.com/)
- [Archbee Review](https://www.archbee.com/blog/book-review-docs-for-developers-an-engineers-field-guide-to-technical-writing-by-jared-bhatti-and-co-authors)
- [Bookey Summary](https://www.bookey.app/book/docs-for-developers)

## Overview

*Docs for Developers* is a practitioner's guide to creating developer documentation, written by a team of five technical writers from Google, Stripe, and the Linux Foundation. The book follows a fictional startup team ("Corg.ly") through each phase of their product launch, teaching documentation principles at each step of the software development lifecycle. Unlike *The Product is Docs* (Gales, 2020), which takes a documentation team management perspective, this book targets **individual developers and engineers** who write docs alongside code — often without dedicated technical writing support.

The core thesis is that documentation is a **software engineering skill** that follows predictable, learnable patterns. The book provides a complete lifecycle framework: understand your audience, plan content types, draft effectively, edit systematically, integrate code samples, add visuals, publish, gather feedback, measure quality, organize at scale, and maintain over time. Google's 2021 DevOps Report is cited as evidence that documentation quality correlates with successful technical implementation.

The book's distinctive contribution is treating documentation as a **development workflow** with concrete tools (friction logs, user sketches, plussing technique, multi-pass editing) rather than abstract writing advice. Each chapter ends with templates and checklists that can be adopted immediately.

## Chapter Structure

| Ch | Title | Focus |
|----|-------|-------|
| 1 | Understanding Your Audience | Curse of knowledge, user sketches, friction logs, persona validation |
| 2 | Planning Your Documentation | Content types taxonomy (9 types), planning workflows |
| 3 | Drafting Documentation | Outline-as-pseudocode, writing for skimming, templates |
| 4 | Editing Documentation | Multi-pass editing system (5 passes), plussing technique |
| 5 | Integrating Code Samples | Executable vs explanatory code, conciseness principles |
| 6 | Adding Visual Content | Screenshots, diagrams, video; creation and maintenance |
| 7 | Publishing Documentation | Content release processes, publishing timelines |
| 8 | Gathering and Integrating Feedback | Feedback channels, converting feedback to action |
| 9 | Measuring Documentation Quality | Analytics strategy, document metrics, quality signals |
| 10 | Organizing Documentation | Information architecture, navigation, findability |
| 11 | Maintaining and Deprecating Documentation | Maintenance automation, content removal protocols |
| A | When to Hire an Expert | Support deflection, localization, versioning triggers |
| B | Resources | Courses, templates, style guides, tools, communities |

## Key Frameworks / Core Concepts

### 1. Curse of Knowledge and User Research

The book's foundational concept: experts cannot intuitively perceive beginner perspectives. The antidote is structured user research before writing:

| Tool | Purpose | Method |
|------|---------|--------|
| **User Sketches** | Provisional personas for documentation | Identify goals, technical comfort, context of use |
| **User Stories** | Task-oriented documentation scoping | "As a [role], I want [goal] so that [benefit]" |
| **User Journey Maps** | Visualize full user experience | Map touchpoints, emotions, pain points across stages |
| **Friction Logs** | Identify documentation gaps firsthand | Record personal experience using the product; note every obstacle |
| **Validation** | Verify assumptions against reality | Support tickets, interviews, surveys, usage analytics |

### 2. Content Types Taxonomy (9 Types)

| Content Type | Purpose | Audience | Example |
|-------------|---------|----------|---------|
| **Code Comments** | Explain design decisions in-line | Developers reading source | `// Retry with backoff to handle rate limiting` |
| **READMEs** | Project overview + quick start | New contributors | Installation, troubleshooting, links |
| **Getting Started** | Minimal viable onboarding | First-time users | "Hello World" in 5 minutes |
| **Conceptual** | Explain ideas and architecture | All levels | "How authentication works" |
| **Procedural** | Step-by-step task guides | Task-focused users | "Deploy to production" |
| **Reference** | Exhaustive API/parameter specs | Active developers | API endpoint docs, config options |
| **Glossary** | Domain term definitions | All levels | Service-specific vocabulary |
| **Troubleshooting** | Known issues and solutions | Stuck users | Error messages → fixes |
| **Changelog** | Track updates over time | Existing users | Version history, breaking changes |

### 3. Multi-Pass Editing System (5 Passes)

Sequential editing passes, each with a distinct focus:

| Pass | Focus | Key Actions |
|------|-------|-------------|
| 1. **Technical Accuracy** | Correctness | Verify instructions work; test code samples; clarify jargon |
| 2. **Completeness** | Coverage | Confirm all necessary info exists; have new readers identify gaps |
| 3. **Structure** | Organization | Validate logical flow, headers, prerequisites, navigation |
| 4. **Clarity & Brevity** | Readability | Remove unnecessary language and jargon; simplify |
| 5. **Style Consistency** | Polish | Apply style guide; standardize terminology and formatting |

### 4. Code Sample Integration Principles

Three principles for effective code in documentation:

- **Explained**: Provide context, reasoning, and expected output — never drop code without annotation
- **Concise**: Minimal but sufficient; strip boilerplate that distracts from the concept being taught
- **Clear**: Easy to understand and directly applicable; use realistic variable names

Two categories: **executable code** (runnable, modifiable) vs **explanatory code** (educational snippets, output examples).

### 5. Plussing Technique (Constructive Feedback)

Borrowed from Pixar's creative process: when critiquing documentation, always pair criticism with a constructive suggestion for improvement. Instead of "This section is confusing," say "This section would be clearer if it started with a use case before diving into the API parameters."

### 6. Documentation Quality Measurement

| Signal Type | Metrics | Use |
|------------|---------|-----|
| **Quantitative** | Page views, time-on-page, bounce rate, search queries | Identify popular/neglected content |
| **Qualitative** | User feedback, satisfaction surveys, usability tests | Understand *why* docs succeed or fail |
| **Operational** | Support ticket deflection, time-to-resolution, MTTP | Business impact of documentation |
| **Content Health** | Staleness indicators, broken links, coverage gaps | Maintenance prioritization |

### 7. Documentation Lifecycle Model

The book's implicit lifecycle maps to the software development lifecycle:

```
Understand → Plan → Draft → Edit → Integrate Code → Add Visuals →
Publish → Gather Feedback → Measure → Organize → Maintain/Deprecate
```

Each phase has its own chapter, tools, and deliverables — treating documentation as a first-class engineering artifact with its own CI/CD.

## Key Takeaways

1. **Documentation is an engineering skill**, not a writing talent — it follows learnable patterns and systematic processes
2. **Friction logs** are the single most actionable user research tool: use your own product, record every obstacle, and let those obstacles drive your documentation roadmap
3. **Nine content types** form a complete documentation suite — most projects need at least READMEs, Getting Started, Conceptual, Procedural, and Reference
4. **Edit in five distinct passes** — trying to check accuracy, completeness, structure, clarity, and style simultaneously leads to missed issues
5. **Code samples are the entry point** — developers skip prose and jump to code; every code sample must be explained, concise, and clear
6. **The plussing technique** transforms adversarial feedback into collaborative improvement
7. **Measure documentation like you measure software** — analytics, user feedback, and operational metrics (support deflection) form a three-legged stool
8. **Organize for findability**, not for your internal team structure — readers navigate by task, not by org chart
9. **Documentation maintenance is not optional** — plan for it from day one; automate staleness detection; deprecate gracefully
10. **Know when to hire a technical writer** — the book's Appendix A provides concrete triggers (support deflection goals, large releases, localization needs)

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|-----------------|
| Writing docs after launch | Users have already formed workarounds and negative impressions | Integrate docs into Definition of Done |
| Expert writes all docs alone | Curse of knowledge; single point of failure | Collaborative drafting + new-reader review |
| One editing pass | Conflates accuracy, structure, and style concerns | Five sequential passes with distinct focus |
| Code dumps without context | Developers can't map code to their situation | Explain → Concise → Clear framework |
| Organizing by internal structure | Users don't know your team structure | Organize by user tasks and goals |
| Ignoring analytics | No signal on what works or fails | Track quantitative + qualitative + operational metrics |

## Notable Quotes

> "If developers are the superheroes of the software industry, then the lack of documentation is our kryptonite."

> "A friction log documents your personal experience using the software to identify friction points that users might encounter."

> "Setting yourself up for writing success parallels coding environment preparation — define purpose, audience, and format before writing a single word."

> "Code samples are the entry point for developer documentation. Research indicates developers skip text-based content and gravitate toward documentation with code examples."

## Relevance to Our Work

This book directly informs how we build and maintain our knowledge management system:

- **Friction logs** parallel our [Zettelkasten](../term_dictionary/term_zettelkasten.md) approach of capturing direct experience with systems — the slipbox itself is a friction log for organizational knowledge
- **Content types taxonomy** maps to our note type system: term notes (Glossary), SOPs (Procedural), area notes (Conceptual), entry points (Getting Started), how-to guides (Getting Started/Procedural)
- **Multi-pass editing** aligns with our [Technical Editing](../term_dictionary/term_technical_editing.md) practices for vault note quality
- **Documentation quality measurement** connects to our [Support Case Deflection](../term_dictionary/term_support_case_deflection.md) and [Mean Time to Productivity](../term_dictionary/term_mean_time_to_productivity.md) metrics
- **Organize for findability** is the core principle behind our entry point navigation system and [Information Architecture](../term_dictionary/term_information_architecture.md)
- **Documentation maintenance** maps to our [Documentation Debt](../term_dictionary/term_documentation_debt.md) management and incremental database updates

## References

### Source Material
- [Springer Nature: Docs for Developers](https://link.springer.com/book/10.1007/978-1-4842-7217-6) — publisher page
- [Official Book Website](https://docsfordevelopers.com/) — ToC, author bios, resources
- [Archbee Book Review](https://www.archbee.com/blog/book-review-docs-for-developers-an-engineers-field-guide-to-technical-writing-by-jared-bhatti-and-co-authors) — detailed chapter review
- [Bookey Summary](https://www.bookey.app/book/docs-for-developers) — chapter-by-chapter summary
- [Write the Docs Podcast Ep. 35](https://podcast.writethedocs.org/2021/10/31/episode-35-docs-for-developers/) — author interview

### Related Vault Notes
- [Digest: The Product is Docs](digest_product_is_docs_gales.md) — complementary book: Gales covers documentation team management; Bhatti covers individual developer documentation skills
- [Digest: Clean Code](digest_clean_code_martin.md) — Martin's code quality principles (meaningful naming, SRP) apply directly to documentation clarity and structure
- [Digest: The Pragmatic Programmer](digest_pragmatic_programmer_thomas_hunt.md) — DRY principle and "care about your craft" philosophy extend to documentation
- [Digest: Smart Notes](digest_smart_notes_ahrens.md) — Ahrens' writing-as-thinking thesis parallels Bhatti's documentation-as-engineering-skill argument
- [Digest: Building a Second Brain](digest_building_second_brain_forte.md) — Forte's CODE method (Capture, Organize, Distill, Express) parallels the documentation lifecycle
- [Digest: A System for Writing](digest_system_for_writing_doto.md) — Doto's structure notes and hub notes map to documentation organization principles

### Related Term Notes
- [Docs-as-Product](../term_dictionary/term_docs_as_product.md) — treating documentation with product management rigor
- [Docs-as-Code](../term_dictionary/term_docs_as_code.md) — version control and CI/CD for documentation
- [Content Strategy](../term_dictionary/term_content_strategy.md) — strategic planning for content creation and governance
- [Technical Editing](../term_dictionary/term_technical_editing.md) — developmental editing, copy editing, style enforcement
- [Information Architecture](../term_dictionary/term_information_architecture.md) — content organization, labeling, navigation, findability
- [Scenario-Driven Documentation](../term_dictionary/term_scenario_driven_documentation.md) — organizing content by user tasks
- [Documentation Debt](../term_dictionary/term_documentation_debt.md) — systematic tracking and paydown of documentation gaps
- [Support Case Deflection](../term_dictionary/term_support_case_deflection.md) — measuring documentation by support contacts prevented
- [Mean Time to Productivity](../term_dictionary/term_mean_time_to_productivity.md) — north-star documentation metric
- [Agile Documentation](../term_dictionary/term_agile_documentation.md) — docs integrated into sprint workflows
- [Friction Log](../term_dictionary/term_friction_log.md) — the book's most actionable user research tool for identifying documentation gaps
- [Curse of Knowledge](../term_dictionary/term_curse_of_knowledge.md) — the foundational cognitive bias that drives the book's user research methodology
- [Plussing Technique](../term_dictionary/term_plussing_technique.md) — Pixar's constructive feedback method applied to documentation review
- [Documentation Lifecycle](../term_dictionary/term_documentation_lifecycle.md) — the eleven-stage lifecycle model that structures the book's chapter progression
