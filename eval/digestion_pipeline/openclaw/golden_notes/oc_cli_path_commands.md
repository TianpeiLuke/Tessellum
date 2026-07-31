---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - oc_path
keywords:
  - openclaw path command
  - oc-path plugin enable
  - path resolve find set validate emit
  - oc:// dry-run diff preview
  - path exit codes 0 1 2
  - path json human output mode
  - path recipes markdown jsonc jsonl yaml
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/path
access_control_group: ["general"]
---

# OpenClaw — Using the `openclaw path` CLI

## Overview

This procedure note covers how to use the `openclaw path` command-line tool — the bundled `oc-path` plugin's shell access to the `oc://` addressing substrate — mirroring the verb-usage half of the `cli/path` source page. It documents enabling the plugin, the five verbs (`resolve` / `find` / `set` / `validate` / `emit`), the global flags, the `--dry-run` / `--diff` preview workflow, the per-file-kind recipes, the per-subcommand reference and exit codes, and the TTY-aware output mode. The companion concept note `oc_cli_path_addressing` covers the `oc://` grammar and per-kind addressing model these verbs consume; this note is the task-oriented "how to run it" half.

## Enabling the `oc-path` plugin

`path` is provided by the bundled optional `oc-path` plugin. Enable it before first use:

```bash
openclaw plugins enable oc-path
```

The CLI mirrors the substrate's public verbs: `resolve` is concrete and single-match, `find` is the multi-match verb for wildcards / unions / predicates / positional expansion, and `set` only accepts concrete paths or insertion markers — wildcard patterns are rejected before writing.

## How it is used

The commands are meant to be copyable into shell scripts. Read one value from a human-edited config file with `openclaw path resolve 'oc://config.jsonc/plugins/github/enabled'`; preview a write without touching disk by appending `--dry-run` to a `set`; find matching records in an append-only JSONL log with `openclaw path find 'oc://session.jsonl/[event=tool_call]/name'`; address a markdown instruction by section and item (not by line number) with `openclaw path resolve 'oc://AGENTS.md/runtime-safety/openclaw-gateway'`; and validate a path in CI or a preflight script before reading or writing with `openclaw path validate 'oc://AGENTS.md/tools/$last/risk'`. Use `--json` when a caller needs structured output and `--human` when a person is inspecting the result.

## Subcommands

| Subcommand              | Purpose                                                                      |
| ----------------------- | ---------------------------------------------------------------------------- |
| `resolve <oc-path>`     | Print the concrete match at the path (or "not found").                       |
| `find <pattern>`        | Enumerate matches for a wildcard / union / predicate path.                   |
| `set <oc-path> <value>` | Write a leaf or insertion target at a concrete path. Supports `--dry-run`.   |
| `validate <oc-path>`    | Parse-only; print structural breakdown (file / section / item / field).      |
| `emit <file>`           | Round-trip a file through `parseXxx` + `emitXxx` (byte-fidelity diagnostic). |

## Global flags

| Flag            | Purpose                                                                  |
| --------------- | ------------------------------------------------------------------------ |
| `--cwd <dir>`   | Resolve the file slot against this directory (default: `process.cwd()`). |
| `--file <path>` | Override the file slot's resolved path (absolute access).                |
| `--json`        | Force JSON output (default when stdout is not a TTY).                     |
| `--human`       | Force human output (default when stdout is a TTY).                        |
| `--dry-run`     | (only on `set`) print the bytes that would be written without writing.   |
| `--diff`        | (with `set --dry-run`) print a unified diff instead of the full bytes.   |

## Examples

```bash
# Validate a path (no filesystem access)
openclaw path validate 'oc://AGENTS.md/Tools/$last/risk'

# Read a leaf
openclaw path resolve 'oc://gateway.jsonc/version'

# Wildcard search
openclaw path find 'oc://session.jsonl/*/event' --file ./logs/session.jsonl

# Dry-run a write
openclaw path set 'oc://gateway.jsonc/version' '2.0' --dry-run

# Dry-run a write as a unified diff
openclaw path set 'oc://gateway.jsonc/version' '2.0' --dry-run --diff

# Apply the write
openclaw path set 'oc://gateway.jsonc/version' '2.0'

# Byte-fidelity round-trip (diagnostic)
openclaw path emit ./AGENTS.md
```

Grammar-level examples cover quoting keys that contain `/` or `.`, deep JSON slash segments that normalize to dotted sub-segments, replacing a JSONC leaf with a parsed object via `--value-json`, predicate search over JSONC children (`oc://config.jsonc/plugins/[enabled=true]/id`), array insertion (`.../items/+1`), object-key insertion (`.../plugins/+github`), JSONL append (`oc://session.jsonl/+`), resolving the last JSONL value line (`$last`), resolving and updating a YAML workflow step, addressing and inserting markdown frontmatter (`[frontmatter]/name`, `[frontmatter]/+description`), finding markdown item fields, and validating a session-scoped path (`...?session=cron-daily`).

## Recipes by file kind

The same five verbs work across kinds; the addressing scheme dispatches on the file extension. The recipes below use the fixtures from the source page's PR description.

For **Markdown**, `resolve 'oc://x.md/[frontmatter]/tier' --human` prints `leaf @ L4: "core" (string)`, `resolve 'oc://x.md/tools/gh/gh'` prints `leaf @ L9: "GitHub CLI" (string)`, and `find 'oc://x.md/tools/*'` enumerates the item nodes (`gh` → L9, `curl` → L10, `send-email` → L11). The `[frontmatter]` predicate addresses the YAML frontmatter block; `tools` matches the `## Tools` heading via slug; and item leaves keep their slug form even when the source uses underscores (`send_email` → `send-email`). For **JSONC**, edits go through `jsonc-parser`, so comments and whitespace survive a `set` — run `--dry-run` first to inspect the bytes (a `set` of `plugins/slack/enabled` to `'true'` reports `--dry-run: would write 142 bytes`). For **JSONL**, each line is a record: address by predicate (`[event=action]`) when you do not know the line number, or by the canonical `LN` segment (`L2`) when you do. For **YAML**, the `yaml` package's `Document` API is used (not a hand-rolled parser), so parse/emit round-trips preserve comments and authoring shape while resolved paths use the same map-key / sequence-index model as JSONC; the same adapter handles `.yaml`, `.yml`, and `.lobster` files.

```bash
$ openclaw path resolve 'oc://config.jsonc/plugins/github/enabled' --file config.jsonc --human
leaf @ L4: "true" (boolean)

$ openclaw path set 'oc://config.jsonc/plugins/slack/enabled' 'true' --file config.jsonc --dry-run
--dry-run: would write 142 bytes to /…/config.jsonc
{
  "plugins": {
    "github": {"enabled": true, "role": "vcs"},
    "slack":  {"enabled": true, "role": "chat"}
  }
}
```

## Subcommand reference

**`resolve <oc-path>`** reads a single leaf or node; wildcards are rejected (use `find`). It exits `0` on a match, `1` on a clean miss, `2` on a parse error or refused pattern.

**`find <pattern>`** enumerates every match for a wildcard / predicate / union pattern. It exits `0` on at least one match, `1` on zero. File-slot wildcards are rejected with `OC_PATH_FILE_WILDCARD_UNSUPPORTED` — pass a concrete file (multi-file globbing is a follow-up feature).

**`set <oc-path> <value>`** writes a leaf. Pair with `--dry-run` to preview the bytes that would be written without touching the file, and add `--diff` for a unified diff preview. It exits `0` on a successful write, `1` if the substrate refuses (for example, a sentinel guard hit), `2` on parse errors. The `+key` insertion marker creates the named child if it does not already exist; `+nnn` and bare `+` work for indexed and append insertion respectively.

**`validate <oc-path>`** is a parse-only check with no filesystem access — useful to confirm a template path is well-formed before substituting variables, or to get the structural breakdown for debugging. With `--human` it prints the `valid:` line plus the `file:` / `section:` / `item:` slots. It exits `0` when valid, `1` when invalid (with a structured `code` and `message`), `2` on argument errors.

**`emit <file>`** round-trips a file through the per-kind parser and emitter. The output should be byte-identical to the input on a sound file — divergence indicates a parser bug or a sentinel hit. It is useful for debugging substrate behavior on real-world inputs (e.g. `openclaw path emit ./gateway.jsonc --json`).

## Exit codes

| Code | Meaning                                                                    |
| ---- | -------------------------------------------------------------------------- |
| `0`  | Success. (`resolve` / `find`: at least one match. `set`: write succeeded.) |
| `1`  | No match, or `set` rejected by the substrate (no system-level error).      |
| `2`  | Argument or parse error.                                                   |

## Output mode

`openclaw path` is TTY-aware: human-readable output on a terminal, JSON when stdout is piped or redirected. `--json` and `--human` override the auto-detection.

## Notes

`set` writes bytes through the substrate's emit path, which applies the redaction-sentinel guard automatically: a leaf carrying `__OPENCLAW_REDACTED__` (verbatim or as a substring) is refused at write time. JSONC parsing and leaf edits use the plugin-local `jsonc-parser` dependency, so comments and formatting are preserved on ordinary leaf writes instead of going through a hand-rolled parser/re-render path. `path` does not know about LKG: if the file is LKG-tracked, the next observe call decides whether to promote / recover, and `set --batch` for atomic multi-set through the LKG promote/recover lifecycle is planned alongside the LKG-recovery substrate.

**Source**: OpenClaw documentation — `cli/path` (mirror `inbox/openclaw_docs/cli/path.md`)
**Last Updated**: 2026-06-22
**Status**: Active
