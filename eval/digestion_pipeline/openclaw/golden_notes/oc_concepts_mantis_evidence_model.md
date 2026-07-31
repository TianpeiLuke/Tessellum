---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - mantis
keywords:
  - mantis evidence model
  - mantis-evidence.json schema
  - mantis-summary.json
  - mantis artifact kinds
  - timeline desktopScreenshot motionPreview
  - pr evidence publisher
  - mantis artifact directory
  - redaction discipline
topics:
  - OpenClaw
  - Mantis Evidence Model
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/concepts/mantis
access_control_group: ["general"]
---

# OpenClaw — Mantis Evidence and Artifact Data Model

## Overview

This note models the **Mantis evidence/artifact data model**: the structured data a Mantis run produces, validates, and hands off to GitHub. It covers the stable per-run artifact directory layout, the machine-readable `mantis-summary.json` source-of-truth, the `mantis-evidence.json` manifest schema (`schemaVersion` / `comparison` / `artifacts`) that bridges scenario code to PR comments, the supported artifact-kind taxonomy, and the reusable PR-evidence publisher plus its redaction discipline. It mirrors the `Evidence model`, `GitHub artifacts and PR comments`, and the inline `mantis-evidence.json` schema + artifact-kinds sections of the `concepts/mantis` source page; the architecture (lifecycle, machines, secrets) lives in `oc_concepts_mantis_architecture` and the CLI/scenario authoring lives in `oc_concepts_mantis_cli_scenarios`.

## Evidence Directory Layout

Every Mantis run writes a stable artifact directory keyed by `<run-id>`. The directory is the on-disk container all other evidence objects reference:

```text
.artifacts/qa-e2e/mantis/<run-id>/
  mantis-report.md
  mantis-summary.json
  baseline/
    summary.json
    discord-message.json
    screenshot-message-row.png
    gateway-debug/
  candidate/
    summary.json
    discord-message.json
    screenshot-message-row.png
    gateway-debug/
  comparison.json
  run.log
```

The two top-level evidence objects play distinct roles: `mantis-summary.json` is the **machine-readable source of truth**, while `mantis-report.md` (the Markdown report) is for PR comments and human review. Each lane (`baseline/`, `candidate/`) holds its own `summary.json`, the transport-specific message JSON (e.g. `discord-message.json`), a `screenshot-message-row.png`, and a `gateway-debug/` directory; `comparison.json` records the oracle comparison and `run.log` the run trace.

## The `mantis-summary.json` Fields

`mantis-summary.json` is the run's machine-readable record. The source page requires the summary to include (verbatim from the page's field list):

- refs and SHAs tested
- transport and scenario id
- machine provider and machine id or lease id
- credential source without secret values
- baseline result
- candidate result
- whether the bug reproduced on baseline
- whether the candidate fixed it
- artifact paths
- sanitized setup or cleanup issues

The `credential source without secret values` requirement is load-bearing: the summary records *which* credential source (env vs the Convex pool) was used, never the secret material itself — consistent with the architecture's secret-handling rules.

## The `mantis-evidence.json` Manifest Schema

Every PR-publishing scenario writes `mantis-evidence.json` next to its report. The source page states this schema is the **handoff between scenario code and GitHub comments**. The verbatim example schema:

```json
{
  "schemaVersion": 1,
  "id": "discord-status-reactions",
  "title": "Mantis Discord Status Reactions QA",
  "summary": "Human-readable top summary for the PR comment.",
  "scenario": "discord-status-reactions-tool-only",
  "comparison": {
    "baseline": { "sha": "...", "status": "fail", "expected": "queued-only" },
    "candidate": { "sha": "...", "status": "pass", "expected": "queued -> thinking -> done" },
    "pass": true
  },
  "artifacts": [
    {
      "kind": "timeline",
      "lane": "baseline",
      "label": "Baseline queued-only",
      "path": "baseline/timeline.png",
      "targetPath": "baseline.png",
      "alt": "Baseline Discord timeline",
      "width": 420
    }
  ]
}
```

The top-level fields are `schemaVersion`, `id`, `title`, `summary`, `scenario`, `comparison`, and `artifacts`. The `comparison` object carries a `baseline` and a `candidate` sub-object (each with `sha`, `status`, and an `expected` string), plus a top-level boolean `pass`. Each entry in the `artifacts` array carries `kind`, `lane`, `label`, `path`, `targetPath`, `alt`, and `width`.

### Path Semantics and Optional Entries

The manifest distinguishes two path fields with different bases: artifact `path` values are **relative to the manifest directory**, while `targetPath` values are **relative paths under the configured Mantis R2/S3 artifact prefix**. The publisher enforces two safety/availability rules on these entries: it **rejects path traversal**, and it **skips entries marked `"required": false`** when optional previews or videos are unavailable.

## Supported Artifact Kinds

The `kind` field draws from a fixed taxonomy. The supported artifact kinds (verbatim from source):

- `timeline`: deterministic scenario screenshot, usually before/after.
- `desktopScreenshot`: VNC/browser desktop screenshot.
- `motionPreview`: inline animated GIF generated from the desktop recording.
- `motionClip`: motion-trimmed MP4 that removes static lead-in and tail.
- `fullVideo`: full MP4 recording for deep inspection.
- `metadata`: JSON/log sidecar.
- `report`: Markdown report.

These kinds map onto distinct display roles: `timeline` is the deterministic before/after proof that stays inline for quick review, `desktopScreenshot` is the VNC/browser-desktop capture, the `motionPreview` GIF and `motionClip` MP4 are the lightweight motion-trimmed previews embedded/linked in the comment, `fullVideo` is the full desktop MP4 kept for deep inspection, and `metadata` / `report` are the sidecar and Markdown evidence.

## The Reusable PR-Evidence Publisher

The reusable publisher is `scripts/mantis/publish-pr-evidence.mjs`. Workflows call it with the manifest, target PR, artifact target root, comment marker, Actions artifact URL, run URL, and request source. The publisher's behavior, in order: it uploads declared artifacts to the configured Mantis R2/S3 bucket, builds a **summary-first PR comment** with inline images/previews and linked videos, then **updates the existing marker comment or creates one**. The workflows publish to the `openclaw-crabbox-artifacts` bucket with public URLs under `https://artifacts.openclaw.ai`, providing bucket, region, and public URL values directly.

The reusable publisher requires these secrets (verbatim names):

- `MANTIS_ARTIFACT_R2_ACCESS_KEY_ID`
- `MANTIS_ARTIFACT_R2_SECRET_ACCESS_KEY`
- `MANTIS_ARTIFACT_R2_BUCKET`
- `MANTIS_ARTIFACT_R2_ENDPOINT`
- `MANTIS_ARTIFACT_R2_REGION`
- `MANTIS_ARTIFACT_R2_PUBLIC_BASE_URL`

## GitHub Artifacts and the PR Comment Shape

Mantis workflows upload the **full evidence bundle** as a short-lived GitHub Actions artifact. When a workflow runs for a bug report or fix PR, it also publishes redacted inline media to the configured Mantis R2/S3 bucket and **upserts a comment on that bug or fix PR** with inline before/after screenshots — the primary proof must not be posted only on a generic QA automation PR, and raw logs, observed messages, and other bulky evidence stay in the Actions artifact. Production workflows post comments with the **Mantis GitHub App**, not `github-actions[bot]`; the app id and private key are stored as the `MANTIS_GITHUB_APP_ID` and `MANTIS_GITHUB_APP_PRIVATE_KEY` GitHub Actions secrets. The workflow uses a **hidden marker as the upsert key**, updates that comment when the token can edit it, and creates a new Mantis-owned comment when an older bot-owned marker cannot be edited.

The PR comment should be short and visual. The source's example comment shape:

```md
Mantis Discord Status Reactions QA

Summary: Mantis reran the reported Discord status-reaction bug against the known
bad baseline and the candidate fix. The baseline reproduced the bug, while the
candidate showed the expected queued -> thinking -> done sequence.

- Scenario: `discord-status-reactions-tool-only`
- Run: <workflow run link>
- Artifact: <artifact link>
- Baseline: `<status>` at `<sha>`
- Candidate: `<status>` at `<sha>`

| Baseline            | Candidate           |
| ------------------- | ------------------- |
| <inline screenshot> | <inline screenshot> |
```

When the run fails because the harness failed (not the candidate), the comment must say that instead of implying the candidate failed — preserving the architecture's "Bug reproduced vs Harness failure" distinction at the evidence layer.

## Redaction Discipline

Screenshots are **evidence, not secrets**, but they still need redaction discipline because private channel names, user names, or message content may appear. For public PRs, the source recommends preferring GitHub Actions artifact links over inline images until the redaction story is stronger. This evidence-layer redaction complements the run-level secret rules (never printing tokens, keys, cookies, auth profiles, or VNC passwords) documented in the Mantis architecture note.

**Source**: OpenClaw documentation — `concepts/mantis` (mirror `inbox/openclaw_docs/concepts/mantis.md`), Evidence model + GitHub artifacts/PR comments + `mantis-evidence.json` schema sections
**Last Updated**: 2026-06-22
**Status**: Active
