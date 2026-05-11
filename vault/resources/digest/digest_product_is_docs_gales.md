---
tags:
  - resource
  - digest
  - book
  - technical_writing
  - documentation
  - software_engineering
  - product_development
keywords:
  - The Product is Docs
  - Christopher Gales
  - Splunk Documentation Team
  - technical documentation
  - technical writing
  - docs as product
  - audience definition
  - content strategy
  - documentation metrics
  - support case deflection
  - mean time to productivity
  - agile documentation
  - scenario-driven documentation
  - docs-as-code
  - collaborative authoring
topics:
  - Technical Writing
  - Documentation Strategy
  - Software Engineering
  - Product Development
language: markdown
date of note: 2026-03-18
status: active
building_block: argument
author: lukexie
book_title: "The Product is Docs: Writing technical documentation in a product development group"
book_author: "Christopher Gales and Splunk Documentation Team"
publisher: "Independently Published"
year: 2020
isbn: "978-1973589402"
pages: 187
---

# Digest: The Product is Docs — Treating Documentation as a Product in Software Development

## Source

- Gales, C. & Splunk Documentation Team. (2020). *The Product is Docs: Writing technical documentation in a product development group* (2nd ed.). Independently Published. 187 pages. ISBN: 978-1973589402.
- First edition published 2017; revised and expanded 2020. All proceeds go to charity.
- Originated from a Splunk hack week project where the documentation team wrote 90 pages of rough drafts in five days, which formed the basis for the entire book.
- Rating: 4.05/5 on Goodreads (127 ratings).

**Sources that contributed to this digest:**
- [Splunk Blog — The Product is Docs](https://www.splunk.com/en_us/blog/splunklife/the-product-is-docs.html) — official announcement and overview
- [Amazon — The Product is Docs (2020)](https://www.amazon.com/Product-Docs-technical-documentation-development/dp/1973589400) — product page
- [Goodreads — The Product is Docs](https://www.goodreads.com/book/show/37563319-the-product-is-docs) — reviews and community assessment
- [Goodreads Quotes — The Product is Docs](https://www.goodreads.com/work/quotes/59176050) — notable quotes from the book

## Overview

*The Product is Docs* is a practitioner's guide written collectively by the Splunk documentation team, structured as short, independent essays on the reality of creating technical documentation in fast-moving product development organizations. The book's central thesis is that **documentation should be treated as a product** — with the same rigor applied to audience research, quality metrics, release processes, and cross-functional collaboration that product teams apply to software itself.

Unlike theoretical treatises on writing craft, this book addresses the *organizational and process* dimensions of documentation work: how to define audiences, measure documentation success, work effectively with engineering and support teams, hire and train writers, manage content in agile environments, and make strategic decisions about what to document. The authors write from direct experience, offering concrete practices that the Splunk documentation team applies daily, with the explicit goal of provoking discussion and inspiring colleagues to examine their processes and assumptions with fresh eyes.

The book is designed for modular reading — each chapter stands alone as an independent essay, allowing readers to start with whatever topic is most relevant. It targets information developers, documentation managers, and anyone in product development who collaborates with documentation teams, across organizations of all sizes.

## Chapter Structure

The book is organized around 15 topic areas, each presented as an independent essay. The 2020 edition revised and expanded the original 2017 content.

| # | Topic Area | Focus |
|---|-----------|-------|
| 1 | **Agile Documentation** | Integrating documentation into agile sprints, continuous delivery, adapting the Agile Manifesto for docs |
| 2 | **Audience Definition** | Creating audience profiles specifically for technical documentation (distinct from UX personas or marketing profiles) |
| 3 | **Collaboration** | Working with cross-functional teams: engineering, product management, UX, QA |
| 4 | **Community Engagement** | Building and leveraging user communities for documentation feedback and contribution |
| 5 | **Documentation Decisions** | Strategic decisions about what to document, depth of coverage, format choices |
| 6 | **Third-Party Products** | Documenting integrations, APIs, and third-party product dependencies |
| 7 | **Hiring and Training** | Recruiting technical writers, onboarding, developing documentation skills |
| 8 | **Content Organization** | Information architecture, content structure, findability, navigation |
| 9 | **Research** | User research for documentation, understanding how customers use docs |
| 10 | **Scenario-Driven Information** | Writing task-based, scenario-oriented documentation (vs. feature-oriented) |
| 11 | **Technical Editing** | Editing practices, style guides, consistency, quality standards |
| 12 | **Verification** | Accuracy verification, technical review processes, testing documentation |
| 13 | **Tools** | Documentation toolchains, publishing systems, collaborative authoring platforms |
| 14 | **Working with Other Teams** | Deep dive into relationships with support, engineering, QA, product management |
| 15 | **Measuring Success** | Documentation metrics, support case deflection, mean time to productivity |

## Key Frameworks / Core Concepts

### 1. Documentation as Product

The foundational principle: documentation is not a secondary artifact of software development but a **product in its own right**. This means applying product thinking to docs — defining customers (audiences), measuring success (metrics), iterating based on feedback (research), and managing releases (content lifecycle). Just as software has product managers, documentation should have strategic ownership with clear goals and accountability.

### 2. Audience Definition Framework

The book argues that existing audience definition models (UX personas, marketing segments) are inadequate for technical documentation. Technical documentation audiences require a different framework that accounts for:

- **Skill level**: novice, intermediate, advanced, expert
- **Goal orientation**: learning vs. doing vs. troubleshooting vs. evaluating
- **Context of use**: installation, configuration, daily operation, emergency response
- **Product familiarity**: new user, experienced user, migrating user, administrator

This was identified as a gap in existing literature — no good models existed specifically for technical documentation audience definitions.

### 3. Documentation Success Metrics

The book proposes a hierarchy of documentation metrics, emphasizing that measurement must support business decisions rather than precise counting:

| Metric | What It Measures | Difficulty | Value |
|--------|-----------------|------------|-------|
| **Support case deflection** | Docs preventing support contacts | Very high (measures absence of action) | Gold standard but hard to capture |
| **Mean time to productivity** | How fast docs make customers productive | High (requires instrumentation) | Best single metric per Mark Baker (*Every Page is Page One*) |
| **Customer satisfaction surveys** | Direct customer assessment of doc quality | Medium (survey design matters) | Good signal but contextual |
| **Page views / engagement** | Usage patterns and content popularity | Low (easy to collect) | Necessary but not sufficient |
| **Task completion rate** | Whether users can complete documented tasks | Medium (requires usability testing) | Strong signal for scenario-driven docs |

Key insight: "The very idea of 'success' is contextual. You must establish a clear definition of what constitutes success" — and that definition changes with organizational context.

### 4. Cross-Functional Collaboration Model

The book devotes significant attention to how technical writers should work with other teams:

| Team | Collaboration Pattern | Key Challenge |
|------|----------------------|---------------|
| **Engineering** | Embed with dev teams; attend standups; review specs early | "The boundary between writers and developers is thin and permeable" |
| **Product Management** | Align on roadmap; co-define audience; share customer insights | Writers bring unique customer perspective |
| **QA** | Share test cases; verify documentation accuracy; mutual review | Complementary verification perspectives |
| **Customer Support** | Mine support cases for doc gaps; track deflection; share common questions | Support case analysis as documentation research |
| **UX** | Coordinate on user workflows; share research findings; align terminology | Overlapping concern for user experience |

### 5. Scenario-Driven Documentation

Rather than organizing documentation by feature (feature-oriented), the book advocates **scenario-driven information design** — structuring content around real-world tasks and use cases. "A well-written scenario keeps this motivation in mind and identifies product features in the context of how they solve the problem posed in the scenario." This approach maps to the user's goal orientation rather than the product's feature taxonomy.

### 6. Agile Documentation Integration

The book adapts agile principles specifically for documentation work:

- Documentation is part of the **definition of done** for user stories
- Writers participate in sprint ceremonies (planning, standup, retrospective)
- Content follows **continuous delivery** — published incrementally, not in waterfall releases
- Documentation debt is tracked alongside technical debt
- Feedback loops from users drive documentation iteration

### 7. Hiring and Skills Framework

The book argues that exceptional technical writers share two traits: **resourcefulness and eagerness** — "a real appetite for discovery, as the job is fundamentally a relationship business, more like investigative journalism." The ideal hire can "write clear sentences and organize information well, but isn't afraid to break a rule or two."

## Key Takeaways

1. **Treat documentation as a product**: Apply product management thinking — define audiences, measure success, iterate based on feedback, manage releases strategically
2. **Mean time to productivity is the north-star metric**: Mark Baker's insight that "the faster your documentation makes your customers productive, the more successful it is" should guide documentation strategy
3. **Support case deflection is gold but elusive**: The classic documentation metric is "surprisingly difficult to capture because it involves measuring an absence of action"
4. **Scenario-driven beats feature-driven**: Organize content around user tasks and goals, not product feature lists
5. **Technical writing is investigative journalism**: The best writers are resourceful relationship-builders who discover information through persistent cross-functional collaboration
6. **The writer-developer boundary is permeable**: Don't maintain artificial separation — embed with engineering teams, understand the code, attend standups
7. **Documentation debt is real debt**: Track it, prioritize it, and pay it down systematically, just like technical debt
8. **Audience definition for docs is unique**: Don't reuse UX personas or marketing segments — create documentation-specific audience profiles based on skill level, goals, and context
9. **Measurement supports decisions, not precision**: "Measurement isn't about precise counting, and measurement has to support a business decision"
10. **Modular essays beat monolithic manuals**: The book itself models its advice — short, independent chapters that readers can consume in any order

## Common Mistakes and Anti-Patterns

- **Feature-dump documentation**: Listing every feature without connecting them to user scenarios or tasks
- **Metric vanity**: Collecting page views without connecting them to business outcomes
- **Siloed writing**: Writers working in isolation from engineering, support, and product teams
- **One-audience-fits-all**: Writing documentation without differentiating between audience segments
- **Waterfall docs in an agile world**: Waiting to write documentation until a feature is "complete" rather than iterating continuously
- **Hiring for writing alone**: Seeking only writing craft skills while ignoring the investigative and relationship-building skills that make writers effective in product organizations

## Notable Quotes

> "The faster your documentation makes your customers productive, the more successful it is." — citing Mark Baker, *Every Page is Page One*

> "Support case deflection is a surprisingly difficult metric to capture because it involves measuring an absence of action."

> "The very idea of 'success' is contextual. You must establish a clear definition of what constitutes success."

> "Let's move beyond the stereotypes and recognize that the boundary between writers and developers is thin and permeable."

> "So what makes a technical writer exceptional? Resourcefulness and eagerness are essential. Look for someone who can write clear sentences and organize information well, but who isn't afraid to break a rule or two."

## Relevance to Our Work

The vault itself is a documentation product — the Abuse Slipbox is a knowledge system serving the Buyer Abuse Prevention team, and many of the book's principles apply directly to how we structure, measure, and maintain it:

- **Audience definition**: The vault serves multiple audiences (new hires, data scientists, applied scientists, SDEs, PMs) with different skill levels and goals — exactly the segmentation framework the book advocates
- **Scenario-driven organization**: Entry points like `entry_new_hire_curriculum.md` and role-based guides exemplify the scenario-driven approach over feature-dumping
- **Documentation metrics**: The vault's PageRank scoring, link density, and ghost note tracking are analogs of the book's documentation success metrics
- **Atomicity as product quality**: The vault's atomicity principles (one concept per note, building blocks) parallel the book's emphasis on modular, task-oriented content
- **Cross-functional embedding**: The vault captures knowledge from across teams (BAP, AIT, PR) — the book's collaboration model explains why writers embedded in teams produce better documentation

## References

### Source Material
- [Gales, C. & Splunk Documentation Team. *The Product is Docs* (2020). Amazon](https://www.amazon.com/Product-Docs-technical-documentation-development/dp/1973589400) — print edition
- [Splunk Blog — The Product is Docs](https://www.splunk.com/en_us/blog/splunklife/the-product-is-docs.html) — official announcement and development story
- [Goodreads — The Product is Docs](https://www.goodreads.com/book/show/37563319-the-product-is-docs) — community reviews and ratings
- [Goodreads Quotes — The Product is Docs](https://www.goodreads.com/work/quotes/59176050) — 14 notable quotes from the book

### Related Vault Notes
- [Digest: How to Take Smart Notes (Ahrens)](digest_smart_notes_ahrens.md) — complementary perspective on knowledge documentation; Ahrens focuses on personal knowledge management writing, Gales on team-based product documentation
- [Digest: Building a Second Brain (Forte)](digest_building_second_brain_forte.md) — Forte's CODE method for personal knowledge management parallels Gales's product lifecycle for documentation
- [Digest: A System for Writing (Doto)](digest_system_for_writing_doto.md) — Doto's structure notes and hub notes map to the book's content organization and information architecture concerns
- [Digest: Clean Code (Martin)](digest_clean_code_martin.md) — Martin's code quality principles (SRP, meaningful naming, small functions) have direct analogs in documentation quality (single-topic pages, clear headings, atomic content)
- [Digest: The Pragmatic Programmer (Thomas & Hunt)](digest_pragmatic_programmer_thomas_hunt.md) — DRY principle and orthogonality apply to documentation architecture; "documentation debt" parallels technical debt
- [Zettelkasten](../term_dictionary/term_zettelkasten.md) — the vault's foundational methodology; Gales's modular essay structure mirrors Zettelkasten's atomic note principle
- [Deep Modules](../term_dictionary/term_deep_modules.md) — Ousterhout's concept of hiding complexity behind simple interfaces applies to documentation: each page should have a simple entry point hiding detailed content
- [Screaming Architecture](../term_dictionary/term_screaming_architecture.md) — Martin's principle that architecture should reveal intent; the book's scenario-driven approach makes documentation "scream" its use cases
- [Boy Scout Rule](../term_dictionary/term_boy_scout_rule.md) — continuous improvement principle directly applicable to documentation maintenance
- [DRY](../term_dictionary/term_dry.md) — Don't Repeat Yourself applies to documentation content reuse and single-source publishing
- [Single Responsibility Principle (SRP)](../term_dictionary/term_srp.md) — one topic per page/note mirrors SRP; the book's modular essay structure embodies this
- [Agile](../term_dictionary/term_agile.md) — the book's agile documentation integration framework builds on agile methodology principles
- [Digest: Docs for Developers (Bhatti)](digest_docs_for_developers_bhatti.md) — complementary book: Gales covers documentation team management; Bhatti covers individual developer documentation skills with concrete tools (friction logs, multi-pass editing, plussing technique)

**Last Updated**: March 18, 2026
**Status**: Active
