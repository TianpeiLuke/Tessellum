# `tessellum.format` — Note Format & Validation

## The Mental Model

A Tessellum note is a small mosaic tile — a *tessellum* — carrying one epistemic claim. Before that tile can be indexed, retrieved, or woven into a Folgezettel trail, something has to decide whether it is *well-formed*: whether its YAML frontmatter obeys the spec, whether its links point at real notes, and whether its typed edges are the edges the ontology allows. That is what `tessellum.format` does. It defines what a note *is*, and it judges each note on its own terms.

The judgement is deliberately narrow. Every rule here is a pure function of a single note's text on disk — its frontmatter, its body, and (for two rules) the notes its links happen to point at. There is no database, no index, no query. This is the write-side of the CQRS split: it validates the prescriptive substrate (System P, what you author), never the descriptive retrieval layer (System D, what queries return). A note is well-formed or not for reasons entirely local to itself, which is what makes the validator fast, cacheable, and safe to run on a single file in an editor save-hook.

## The Model

The layer is a short pipeline of pure functions. Text on disk becomes a frozen `Note`; the `Note` becomes a flat list of `Issue`s; the list collapses to a single pass/fail bit.

```
path/str/Note ──parse──▶ Note (frozen) ──validate──▶ list[Issue] ──▶ is_valid()
                              │                          │
                              ├─ raw_frontmatter ────────┤  scan YAML text for links
                              ├─ frontmatter (dict) ─────┤  required / type / enum / format
                              └─ body ───────────────────┤  body-link lint
                                                          │  + 2 rules that read link targets
                                                          ▼
                                        is_valid() = no ERROR-severity Issue
```

The parser is the gateway. It splits the `---` fences, loads the YAML into a dict, and — this is the load-bearing choice — *keeps the original frontmatter text alongside the parsed dict*. Parsing is lossy: once YAML is a Python object, the `[[wiki]]` and `[](markdown)` link syntax is gone. A rule that must forbid links *inside* YAML has to read the source text, not the dict. So the `Note` carries both.

Everything downstream is a rule group appended, in a fixed order, to one growing list of `Issue`s. Most rules never leave the note: they read a frontmatter field and check its presence, type, value, or format. Two rules reach one hop further — they resolve a body link on the filesystem and read the *target* note's building-block type — but even these take no database. Resolution is nothing more than `note.path.parent / link`. The reach is one directory hop, not a graph traversal.

An `Issue` carries a severity, a stable rule ID, an optional field locator, and a message. Severity is the whole story of pass versus fail. `is_valid()` is `True` exactly when no issue is an ERROR; warnings and infos are lint signals that never fail a note. This single distinction — ERROR gates, everything else advises — is the spine of the design.

## How Validation Flows

The entry point, `validate`, accepts a path, a raw string, or an already-parsed `Note`. If it is not already a `Note`, it parses one. Then it walks its rule groups in a fixed sequence and returns the concatenated issues. The order is stable so that output is diffable and reproducible; nothing about correctness depends on it, but everything about readable reports does.

The frontmatter rules come first and form the bulk of the gate. Seven fields are *required* — `tags`, `keywords`, `topics`, `language`, `date of note`, `status`, `building_block` — and a missing one is always an ERROR. On top of presence, each field that is present is checked for type, and closed-enum fields are checked for membership. The `tags` field carries the most contract: its first element must be a PARA bucket, its second is the note's canonical *second category*, and every element must be lowercase-slug-shaped. The two-tag minimum is not arbitrary. `tags[1]` is the single source of truth for second category — which is precisely why a separate `note_second_category` field is *forbidden*: a duplicated field could disagree with `tags[1]`, and the indexer already reads the second category from `tags[1]` automatically.

Not every frontmatter shortfall is fatal. Missing a required field is an ERROR, but merely having *too few* keywords or topics is a WARNING — the spec recommends three keywords and two topics, but a thin note is a lint target, not a broken one. This is the severity model doing its work: the gate enforces structure, the warnings nudge quality.

The building-block enum is special in one respect that matters more than it looks. Its valid values are not defined in the format spec at all — they are re-exported from the BB ontology (`tessellum.bb`). The validator imports the value set rather than restating it, so the format layer can never drift out of sync with the ontology it is meant to enforce. When someone adds a ninth building-block type, the validator accepts it the moment the ontology does, with no edit here.

After the frontmatter, two Tessellum-specific structural rules run. The **folgezettel pair** rule enforces both-or-neither: a note may declare its trail position and its parent, or neither, but not one alone — a positioned note with no parent (or a parent with no position) can't be placed in a trail. The **forbidden-field** rule rejects the redundant second-category field described above. Then a rule scans the *raw* frontmatter text, line by line, for link syntax and forbids it: links belong in the body, where they can be resolved and typed, not buried in YAML values where they are invisible to the graph.

The body rules come last, and here severity flips almost entirely to advisory. The **link checker** walks every markdown link in the body — after stripping fenced code so examples don't get flagged — and emits warnings for links that miss a `.md` extension, use an absolute path, point at a file that doesn't exist on disk, or, at the note level, for a note with no internal links at all (an orphan). Every one of these is a WARNING. A note with broken links or no links still validates. The checker also carries a substantial skip list — external URLs, anchors, images and other non-markdown files, placeholder targets, directory links, template-ish prefixes — so that only genuine internal-note links are ever judged. Templates, which are scaffolds meant to be orphans until copied, are exempt from the orphan check entirely.

## The Two Graph-Aware Rules

Two rules are different in kind. They are the only rules that look beyond the single note, and they exist to make the *typed graph* observable in the corpus rather than merely implied.

**TESS-004** is the one body rule that can fail a note. When a note is an *active* counter-argument, it must link, in its body, to at least one note whose type is `argument`. The rule resolves each internal link on disk, parses the target, and reads its building-block type; if none is an argument, it errors. The insight is structural: a counter-argument that doesn't name the argument it attacks is a claim floating free of its target. The typed dialectical edge should be *readable in the text*, not inferred by a downstream tool. The rule deliberately stops short of the stronger invariant — that the linked argument is the *specific* one the counter's folgezettel-parent points to — because the validator has no index to check that against. The stronger check lives in the indexer and the DKS runtime at write time; TESS-004 is the static, single-note backstop.

**TESS-005** is the softer companion. For an active BB-typed note, it inspects each link to a *differently*-typed note and asks whether that source-to-target type pair appears anywhere in the BB schema, in either direction. If the pair has no declared epistemic relationship at all, it emits a WARNING. It is a warning, never an error, for a deep reason: the schema describes *epistemic transitions*, but a real corpus is full of legitimate links that aren't transitions — term lookups, skill pointers, sibling cross-references. Those are documentation, not bugs. TESS-005 doesn't presume to know which is which; it surfaces the undeclared pair and leaves three doors open — retarget the link, accept it as documentation, or propose a new edge in the schema. The link may be evidence that the *schema* is missing an edge, not that the note is wrong.

One subtlety keeps TESS-005 honest as the ontology evolves. A note may record the schema version it was authored against, and when it does, TESS-005 validates against the schema *as of that version*, frozen at creation, tagging its message accordingly. A note written under an older ontology is judged by the ontology it knew, not by a schema that has since grown new edges. Only notes that record no version fall back to the live schema.

**TESS-005 has a softer cousin still — TESS-010, an advisory below even a warning.** Each building block carries a contract of sections it should have — a term note a Definition and Examples, a how-to Setup, Steps, and Validation — declared once in the ontology. When a note adopts the section layout yet omits one of its type's required headers, TESS-010 emits an INFO note: a nudge, never a failure. It fires only on notes that opted in — a template or stub scaffold is exempt, and so is a freeform note with no sections at all, because declining the layout is a choice, not a defect. Like everything else, it reads its section contract from the same ontology, so it can never demand a header the building-block spec doesn't.

Both rules share the authoring-state exemption that runs through the whole layer: they fire only for `status: active` notes. Templates, drafts, and stubs are works in progress; the gate waits until a note is promoted before it demands the note honor its typed contract.

## Design Decisions & Why

The severity model is the design's center of gravity. Exactly one body rule — TESS-004 — can turn a note red; every other body signal is a warning. So a note fails validation only for a *structural* reason: a missing or malformed frontmatter field, a broken folgezettel pair, a forbidden field, a link smuggled into YAML, or an active counter-argument that doesn't name its argument. Broken links, orphans, and undeclared typed edges advise but never block. This is what lets the validator run everywhere without being tyrannical — the gate protects the substrate's structure, the warnings improve its quality, and the two roles never blur.

No rule calls a database, and no rule calls an LLM. Every judgement is a deterministic function of text on disk. That determinism is what makes the layer cheap enough to run on every save, safe to cache, and trivially reproducible in CI — the same note always yields the same issues. The two graph-aware rules stretch this to exactly one filesystem hop, and no further, precisely to preserve it.

Keeping the ontology as the single source of truth is a drift-prevention decision. Building-block values, and the schema TESS-004/005 consult, both come from `tessellum.bb`. The format layer restates neither. An ontology change propagates to the validator for free, and the validator can never enforce a taxonomy the ontology has abandoned.

Finally, the layer draws a firm line between *what it can know* and *what it should enforce*. A single-note validator with no index cannot verify that a counter attacks the *right* argument, only that it attacks *an* argument; it cannot know whether an undeclared typed edge is a mistake or a missing schema rule. So it enforces the local, checkable half and defers the global half to the systems that hold the index. Every rule respects that boundary — which is why the whole layer stays pure.

**Reference:** [reference/format.md](reference/format.md) — API, symbols, and signatures.
