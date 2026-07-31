---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - docs_search
keywords:
  - openclaw docs command
  - live docs index search
  - docs.openclaw.ai api search
  - cloudflare hosted docs search
  - terminal docs search
  - docs cli exit codes
  - rich tty vs markdown output
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/docs
access_control_group: ["general"]
---

# OpenClaw — `openclaw docs` CLI Command (Live Docs Search)

## Overview

This note documents the `openclaw docs` CLI command, which searches the live OpenClaw documentation index from the terminal. The command calls OpenClaw's Cloudflare-hosted docs search API and renders the results in the terminal, mirroring the `cli/docs` source page. It covers the two usage forms (no-query entrypoint print vs `<query...>` search), worked examples, how the command reaches the hosted `https://docs.openclaw.ai/api/search` endpoint under a fixed 30 second timeout, the two output modes (rich-TTY bullets vs Markdown for piped/non-color output), and the two exit codes (`0` success including zero results, `1` API failure).

## Usage

`openclaw docs` searches the live OpenClaw docs index from the terminal. It has two forms — invoked with no query it prints the docs entrypoint and an example search, and invoked with a query it searches the live docs index:

```bash
openclaw docs                       # print docs entrypoint and example search
openclaw docs <query...>            # search the live docs index
```

The single argument is `[query...]`: a free-form search query where multi-word queries are joined with spaces and sent as one. With no query, `openclaw docs` prints the docs entrypoint URL plus a sample search command instead of running a search.

## Examples

The command accepts free-form multi-word queries that are joined and sent as a single search string:

```bash
openclaw docs browser existing-session
openclaw docs sandbox allowHostControl
openclaw docs gateway token secretref
```

## How It Works

`openclaw docs` calls `https://docs.openclaw.ai/api/search` and renders the JSON results. The search call uses a fixed 30 second timeout.

## Output

In a rich (TTY) terminal, results render as a heading followed by a bullet list. Each bullet shows the page title, the linked docs URL, and a short snippet on the next line. Empty results print `"No results."`.

In non-rich output (piped, `--no-color`, scripts), the same data renders as Markdown:

```markdown
# Docs search: <query>

- [Title](https://docs.openclaw.ai/...) - snippet
- [Title](https://docs.openclaw.ai/...) - snippet
```

## Exit Codes

The command exits with one of two codes:

| Code | Meaning |
| ---- | ------- |
| `0`  | Search succeeded (including zero-result responses). |
| `1`  | The hosted docs search API call failed; stderr is printed inline. |

**Source**: OpenClaw documentation — `cli/docs` (mirror `inbox/openclaw_docs/cli/docs.md`)
**Last Updated**: 2026-06-22
**Status**: Active
