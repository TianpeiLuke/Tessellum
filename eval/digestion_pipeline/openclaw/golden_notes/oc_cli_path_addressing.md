---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - path_addressing
keywords:
  - oc:// addressing scheme
  - openclaw path substrate
  - kind-dispatched file addressing
  - oc-path plugin
  - markdown jsonc jsonl yaml addressing
  - oc:// path grammar predicates unions wildcards
  - byte-fidelity mutation contract
  - redaction-sentinel guard
topics:
  - OpenClaw
  - Path Addressing
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/cli/path
access_control_group: ["general"]
---

# OpenClaw — The `oc://` Addressing Substrate

## Overview

This note models the `oc://` addressing substrate behind `openclaw path`: one kind-dispatched path scheme for inspecting and editing addressable OpenClaw workspace files (markdown, jsonc, jsonl, yaml/yml/lobster). It covers the *concept* half of the `cli/path` source page — why the substrate exists, the four-stage parse → adapter → resolve → emit model, the full `oc://` path grammar (slots, quoting, predicates, unions, wildcards, positional/ordinal/insertion markers, session scope, reserved/control chars), per-kind addressing models, and the byte-fidelity mutation contract. The companion verb-usage procedure (enabling the plugin, the `resolve`/`find`/`set`/`validate`/`emit` commands, flags, recipes, and exit codes) lives in `oc_cli_path_commands`.

The substrate is provided by the bundled optional `oc-path` plugin and gives self-hosters, plugin authors, and editor extensions a stable, kind-agnostic way to read, find, or update a narrow location without hand-rolling per-file parsers.

## Why the Substrate Exists

OpenClaw state is spread across human-edited markdown, commented JSONC config, append-only JSONL logs, and YAML workflow/spec files. Shell scripts, hooks, and agents often need one small value from those files: a frontmatter key, a plugin setting, a log record field, a YAML step, or a bullet item under a named section. The `oc://` scheme gives those callers a stable *logical address* instead of a one-off grep, regex, or parser per file kind — the same path can be validated, resolved, searched, dry-run, and written, which makes narrow automation easier to review and safer to replay. It is especially useful for updating one leaf while preserving the rest of the file's comments, line endings, and surrounding formatting.

The substrate is meant for cases where the thing you want has a logical address but the physical file shape varies — e.g. a hook reading one setting from commented JSONC without losing comments when it writes the value back, a maintenance script finding every matching event field in a JSONL log without a custom parser, an editor extension jumping to a markdown section or bullet item by slug, or an agent dry-running a tiny workspace edit before applying it. It is *not* intended for ordinary whole-file edits, rich config migrations, or memory-specific writes; those should use the owner command or plugin. The CLI mirrors the substrate's public verbs: `resolve` is concrete and single-match, `find` is the multi-match verb for wildcards/unions/predicates/positional expansion, and `set` only accepts concrete paths or insertion markers (wildcard patterns are rejected before writing).

## How It Works (Parse → Adapter → Resolve → Emit)

The substrate does four things. (1) It **parses** the `oc://` address into slots: file, section, item, field, and optional session. (2) It **chooses the file-kind adapter** from the target extension (`.md`, `.jsonc`, `.jsonl`, `.yaml`, `.yml`, `.lobster`, and related aliases). (3) It **resolves** the slots against that file kind's AST — markdown headings/items, JSONC object keys/array indexes, JSONL line records, or YAML map/sequence nodes. (4) For `set`, it **emits** edited bytes through the same adapter so the untouched parts of the file keep their comments, line endings, and nearby formatting where the kind supports it.

`resolve` and `set` require one concrete target. `find` is the exploratory verb: it expands wildcards, unions, predicates, and ordinals into the concrete matches that can be inspected before choosing one to write.

## `oc://` Path Grammar

The canonical path shape is:

```
oc://FILE/SECTION/ITEM/FIELD?session=SCOPE
```

**Slot rules:** `field` requires `item`, and `item` requires `section`. Across all four slots, the grammar provides the following constructs:

- **Quoted segments** — `"a/b.c"` survives `/` and `.` separators. Content is byte-literal; `"` and `\` are not allowed inside quotes. The file slot is also quote-aware: `oc://"skills/email-drafter"/Tools/$last` treats `skills/email-drafter` as a single file path.
- **Predicates** — `[k=v]`, `[k!=v]`, `[k<v]`, `[k<=v]`, `[k>v]`, `[k>=v]`. Numeric ops require both sides to coerce to finite numbers.
- **Unions** — `{a,b,c}` matches any of the alternatives.
- **Wildcards** — `*` (single sub-segment) and `**` (zero-or-more, recursive). `find` accepts these; `resolve` and `set` reject them as ambiguous.
- **Positional** — `$first` / `$last` resolve to the first / last index or declared key.
- **Ordinal** — `#N` for Nth match by document order.
- **Insertion markers** — `+`, `+key`, `+nnn` for keyed / indexed insertion (use with `set`).
- **Session scope** — `?session=cron-daily` etc. Orthogonal to slot nesting. Session values are raw, not percent-decoded; they may not contain control characters or reserved query delimiters (`?`, `&`, `%`).

**Reserved and control characters:** reserved characters (`?`, `&`, `%`) outside quoted, predicate, or union segments are rejected. Control characters (U+0000-U+001F, U+007F) are rejected anywhere, including the `session` query value.

**Canonicalization guarantee:** `formatOcPath(parseOcPath(path)) === path` is guaranteed for canonical paths. Non-canonical query parameters are ignored except for the first non-empty `session=` value.

## Addressing by File Kind

The same scheme dispatches on the file extension, giving each kind its own addressing model:

| Kind              | Addressing model                                                                                    |
| ----------------- | --------------------------------------------------------------------------------------------------- |
| Markdown          | H2 sections by slug, bullet items by slug or `#N`, frontmatter via `[frontmatter]`.                 |
| JSONC/JSON        | Object keys and array indexes; dots split nested sub-segments unless quoted.                        |
| JSONL             | Top-level line addresses (`L1`, `L2`, `$first`, `$last`), then JSONC-style descent inside the line. |
| YAML/YML/.lobster | Map keys and sequence indexes; comments and flow style are handled by the YAML document API.        |

`resolve` returns a structured match — `root`, `node`, `leaf`, or `insertion-point` — with a 1-based line number. Leaf values are surfaced as text plus a `leafType` so plugin authors can render previews without depending on the per-kind AST shape.

## Mutation Contract

`set` writes one concrete target, with byte-fidelity guarantees that depend on the file kind:

- **Markdown** — frontmatter values and `- key: value` item fields are string leaves. Markdown insertions append sections, frontmatter keys, or section items and render a canonical markdown shape for the changed file.
- **JSONC/JSON** — leaf writes coerce the string value to the existing leaf type (`string`, finite `number`, `true`/`false`, or `null`). Use `--value-json` when a JSONC/JSON/JSONL leaf replacement should parse `<value>` as JSON and may change shape, such as replacing a string SecretRef shorthand with an object. JSONC object and array insertions parse `<value>` as JSON and use the `jsonc-parser` edit path for ordinary leaf writes, preserving comments and nearby formatting.
- **JSONL** — leaf writes coerce like JSONC inside a line. Whole-line replacement and append parse `<value>` as JSON. Rendered JSONL preserves the file's dominant LF/CRLF line-ending convention.
- **YAML/YML/.lobster** — leaf writes coerce to the existing scalar type (`string`, finite `number`, `true`/`false`, or `null`). YAML insertions use the bundled `yaml` package's document API for map/sequence updates. Malformed YAML documents with parser errors are refused before mutation with `parse-error`.

The substrate preserves byte-identical output for parse/emit round-trips, but a mutation can canonicalize the edited region or file depending on kind. The redaction-sentinel guard is applied automatically on the emit path: a leaf carrying `__OPENCLAW_REDACTED__` (verbatim or as a substring) is refused at write time. The substrate does not know about LKG (last-known-good); if a file is LKG-tracked, the next observe call decides whether to promote/recover, and `set --batch` for atomic multi-set through the LKG promote/recover lifecycle is planned but not yet available.

**Source**: OpenClaw documentation — `cli/path` (mirror `inbox/openclaw_docs/cli/path.md`)
**Last Updated**: 2026-06-22
**Status**: Active
