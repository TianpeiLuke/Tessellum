---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - secrets
keywords:
  - openclaw secret placeholder conventions
  - secret-scanner-safe placeholders
  - example-openai-key-not-real
  - env var placeholder docs
  - avoid sk- xoxb- akia prefixes
  - placeholder hygiene credential docs
  - obviously fake credential examples
topics:
  - OpenClaw
  - Secret Placeholder Conventions
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/reference/secret-placeholder-conventions
access_control_group: ["general"]
---

# OpenClaw — Secret Placeholder Conventions for Docs

## Overview

This note states OpenClaw's doc-hygiene argument that credential placeholders in documentation and examples must be human-readable yet must NOT resemble real secrets, so that secret-detection (scanner) tooling does not flag — and operators do not accidentally copy — fake values that look live. It mirrors the `reference/secret-placeholder-conventions` page in full: the recommended placeholder style, the patterns to avoid in docs, and a good/better worked example for env-wiring snippets. The page is a thin (`137`-word) leaf reference that the provider/channel/auth setup docs and config-snippet pages (e.g. memory API-key resolution and gateway secrets) follow when they show credential wiring.

## The Claim: Use Placeholders That Are Human-Readable but Do Not Resemble Real Secrets

The page's governing rule is a single sentence: "Use placeholders that are human-readable but do not resemble real secrets." The argument behind it is that documentation is scanned by secret-detection tooling and is read by operators who copy snippets verbatim; a placeholder that *looks* like a live credential creates two failure modes — a false positive in the scanner (flagging a doc as leaking a secret) and the risk that a reader treats the fake value as a usable real value. The convention resolves both by making placeholders obviously fake while still legible enough to communicate what credential is being wired.

## Recommended Style

The page recommends three practices for credential placeholders:

- **Prefer descriptive values** like `example-openai-key-not-real` or `example-discord-bot-token` — names that read as plainly fake and self-document which credential they stand in for.
- **For shell snippets, prefer `${OPENAI_API_KEY}`** over inline token-like strings — i.e. reference the environment variable rather than pasting a literal value, which both avoids any real-looking token and demonstrates the actual env-wiring pattern.
- **Keep examples obviously fake and scoped to purpose** — bound each placeholder to its provider, channel, or auth type so the example stays specific without embedding anything that resembles a real secret.

## Avoid These Patterns in Docs

The page enumerates the patterns to keep OUT of docs because they resemble live credentials:

- **Literal PEM private-key header or footer text** — the begin/end markers of a real private key.
- **Prefixes that resemble live credentials**, for example `sk-...`, `xoxb-...`, `AKIA...` — the recognizable opening tokens of OpenAI keys, Slack bot tokens, and AWS access key IDs, respectively. Even a truncated, fake value carrying one of these prefixes reads as live to a scanner.
- **Realistic-looking bearer tokens copied from runtime logs** — anything lifted from a real run, which is exactly the kind of value a scanner is built to catch and an operator might mistake for usable.

## Example

The page closes with a good/better pair for an env-wiring snippet — the "good" form uses an obviously-fake descriptive value, and the "better" form (when the doc is specifically about env wiring) references the environment variable so no literal value appears at all:

```bash
# Good
export OPENAI_API_KEY="example-openai-key-not-real"

# Better (when the doc is about env wiring)
export OPENAI_API_KEY="${OPENAI_API_KEY}"
```

**Source**: OpenClaw documentation — `reference/secret-placeholder-conventions` (mirror `inbox/openclaw_docs/reference/secret-placeholder-conventions.md`)
**Last Updated**: 2026-06-22
**Status**: Active
