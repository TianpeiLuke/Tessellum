---
tags:
  - resource
  - template
  - procedure
keywords:
  - procedure template
  - procedure skeleton
  - how-to template
  - skill template
  - note format
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-05-10
status: template
building_block: procedure
---

# How To: <Procedure Name>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy this file to the appropriate vault subdirectory.
   Most procedure notes live in `vault/resources/how_to/howto_<topic>.md`.
   Skill canonicals live in `vault/resources/skills/skill_<name>.md`.
2. Rename the file with the appropriate prefix (`howto_`, `skill_`, etc.).
3. Update YAML frontmatter — tags[1] is usually `how_to` or `skill`.
4. Fill the H2 sections. Required: Setup, Steps, Validation, References.
5. Remove this commentary block.

EPISTEMIC FUNCTION (Doing): a procedure note codifies how to act — an executable
sequence. It answers "How do we act on this?" The reader should be able to
follow the steps without prior context.
-->

## Overview

<One-paragraph: what does this procedure accomplish, who is it for, and when
should they reach for it? The reader should be able to tell within 5 seconds
whether this procedure solves their problem.>

## Prerequisites

<Tools, accounts, credentials, environment, or prior knowledge needed before
Step 1. If a precondition is non-obvious or commonly missed, call it out
explicitly.>

- <Prerequisite 1: e.g., "Python 3.11+ installed">
- <Prerequisite 2: e.g., "AWS account with X permission">
- <Prerequisite 3: e.g., "completed `tessellum init` for your vault">

## Setup

<Optional. Commands to run BEFORE the procedure proper, to bring the
environment to a known state. Different from Prerequisites: Setup is what you
do to satisfy Prerequisites.>

```bash
# Setup commands
```

## Steps

<Numbered steps. Each step should be testable — the reader can confirm completion
before moving on. Aim for one logical action per step. If a step has multiple
sub-actions, give it sub-bullets.>

### 1. <First step name>

<What to do. If the step has a command, code block here.>

```bash
<command>
```

<Expected outcome / how to verify this step worked.>

### 2. <Second step name>

<...>

### 3. <Third step name>

<...>

## Validation

<How to confirm the procedure succeeded end-to-end. A single command, query, or
test that returns a yes/no answer is ideal.>

```bash
<verification command>
# Expected output: <what success looks like>
```

## Failure Modes

<Optional but recommended. Document common failure scenarios with their cause
and recovery. This is what differentiates a good procedure from a checklist.>

| Symptom | Cause | Recovery |
|---|---|---|
| <error message> | <what went wrong> | <how to fix> |

## References

- Related Term — <how it relates>
- [Source documentation](https://example.com) — <what's there>
