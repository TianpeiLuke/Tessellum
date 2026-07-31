---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - lobster
keywords:
  - openclaw lobster
  - lobster workflow runtime
  - typed workflow dsl
  - approval gates resume token
  - lobster run resume tool
  - in-process embedded runner
  - small cli json pipes
  - lobster output envelope
  - openprose lobster
topics:
  - OpenClaw
  - Lobster
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/tools/lobster
access_control_group: ["general"]
---

# OpenClaw — Lobster Typed Workflow Runtime

## Overview

This note explains the OpenClaw **Lobster** tool: a workflow shell that lets OpenClaw run a multi-step tool sequence as a single, deterministic operation with explicit approval checkpoints and resumable state. It mirrors the `tools/lobster` source page — covering why Lobster exists (one call instead of many; built-in approvals; resumability), why it is a small DSL rather than a plain program, the in-process embedded runner, the small-CLI + JSON-pipes + approvals pattern, JSON-only LLM steps via `llm-task` (and the embedded-runner `openclaw.invoke` limitation), `.lobster` workflow files, install and enablement, the `run`/`resume` tool parameters and optional inputs, the three-status output envelope, the approval flow, OpenProse pairing, the safety model, troubleshooting, and a community case study. Lobster is one authoring layer above detached background work; for flow orchestration above individual tasks the page points to Task Flow (`openclaw tasks flow`) and the task activity ledger (`openclaw tasks`).

## Why Lobster (one call instead of many)

Complex workflows today require many back-and-forth tool calls; each call costs tokens and the LLM has to orchestrate every step. Lobster moves that orchestration into a typed runtime so OpenClaw runs **one Lobster tool call and gets a structured result** instead of many. Two further properties define it: approvals are built in — side effects (send email, post comment) **halt the workflow until explicitly approved** — and workflows are resumable, so a halted workflow returns a token that you approve and resume **without re-running everything**. The source frames the value via its "Hook": the assistant can build the tools that manage itself — ask for a workflow and get a CLI plus pipelines that run as one call, with deterministic pipelines, explicit approvals, and resumable state as "the missing piece."

## Why a DSL instead of plain programs

Lobster is intentionally small; the goal is "not a new language" but a predictable, AI-friendly pipeline spec with first-class approvals and resume tokens. The page gives five reasons a DSL is preferred over a plain program: **approve/resume is built in** (a normal program can prompt a human but cannot *pause and resume* with a durable token without you inventing that runtime yourself); **determinism + auditability** (pipelines are data, so they are easy to log, diff, replay, and review); **constrained surface for AI** (a tiny grammar plus JSON piping reduces "creative" code paths and makes validation realistic); **safety policy baked in** (timeouts, output caps, sandbox checks, and allowlists are enforced by the runtime, not each script); and **still programmable** (each step can call any CLI or script — if you want JS/TS, generate `.lobster` files from code).

## How it works (in-process embedded runner)

OpenClaw runs Lobster workflows **in-process** using an embedded runner: no external CLI subprocess is spawned; the workflow engine executes inside the gateway process and returns a JSON envelope directly. If the pipeline pauses for approval, the tool returns a `resumeToken` so you can continue later.

## Pattern: small CLI + JSON pipes + approvals

The intended pattern is to build tiny commands that speak JSON, then chain them into a single Lobster call (the source uses example command names you swap for your own):

```bash
inbox list --json
inbox categorize --json
inbox apply --json
```

These chain into one `run` call, ending in an `approve` step that previews changes from stdin and prompts the operator before any side effect. AI triggers the workflow; Lobster executes the steps; approval gates keep side effects explicit and auditable. The page also shows mapping input items into per-item tool calls with `openclaw.invoke ... --each --item-key message`, e.g. piping `gog.gmail.search --query 'newer_than:1d'` into `openclaw.invoke --tool message --action send`.

## JSON-only LLM steps (llm-task)

For workflows that need a **structured LLM step**, enable the optional `llm-task` plugin tool and call it from Lobster; this keeps the workflow deterministic while still letting you classify/summarize/draft with a model. The tool is enabled by setting `plugins.entries.llm-task.enabled: true` and adding it to an agent's `tools.alsoAllow`. See `oc_tools_llm_task` for the full `llm-task` parameter and output contract; the embedded-runner caveat is below.

### Important limitation: embedded Lobster vs `openclaw.invoke`

The bundled Lobster plugin runs workflows **in-process** inside the gateway, and in that embedded mode `openclaw.invoke` does **not** automatically inherit a gateway URL/auth context for nested OpenClaw CLI tool calls. That means the pattern `openclaw.invoke --tool llm-task --action json --args-json '{ ... }'` is **not currently reliable in the embedded runner**, and the source's full `openclaw.invoke ... --tool llm-task` example should be used only when running the **standalone Lobster CLI** in an environment where `openclaw.invoke` is already configured with the correct gateway/auth context. If you are using the embedded Lobster plugin today, the page advises preferring either a direct `llm-task` tool call **outside** Lobster, or non-`openclaw.invoke` steps inside the Lobster pipeline until a supported embedded bridge is added.

## Workflow files (.lobster)

Lobster can run YAML/JSON workflow files with `name`, `args`, `steps`, `env`, `condition`, and `approval` fields; in OpenClaw tool calls you set `pipeline` to the file path. A representative file ties steps together by piping prior output and gating a side-effecting step on an approval:

```yaml
name: inbox-triage
args:
  tag:
    default: "family"
steps:
  - id: collect
    command: inbox list --json
  - id: categorize
    command: inbox categorize --json
    stdin: $collect.stdout
  - id: approve
    command: inbox apply --approve
    stdin: $categorize.stdout
    approval: required
  - id: execute
    command: inbox apply --execute
    stdin: $categorize.stdout
    condition: $approve.approved
```

Two notes from the source govern data flow and gating: `stdin: $step.stdout` and `stdin: $step.json` pass a prior step's output, and `condition` (or `when`) can gate steps on `$step.approved`.

## Install and enable

Bundled Lobster workflows run in-process, so **no separate `lobster` binary is required** — the embedded runner ships with the Lobster plugin. If you need the standalone Lobster CLI for development or external pipelines, install it from the Lobster repo and ensure `lobster` is on `PATH`. Lobster is an **optional** plugin tool (not enabled by default). The recommended, additive, safe enablement is:

```json
{
  "tools": {
    "alsoAllow": ["lobster"]
  }
}
```

The same can be set per-agent under `agents.list[].tools.alsoAllow`. The page warns to **avoid `tools.allow: ["lobster"]`** unless you intend to run in restrictive allowlist mode, and notes that allowlists are opt-in for optional plugins: `alsoAllow` enables only the named optional plugin tools while preserving the normal core tool set, whereas `tools.allow` restricts core tools to the listed core tools or groups.

## Tool parameters (run / resume / optional inputs)

The tool has two actions. **`run`** runs a pipeline in tool mode (a pipeline string, or a workflow file path with `argsJson`). **`resume`** continues a halted workflow after approval, taking the `token` and an `approve` boolean:

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

A `run` call accepts the pipeline plus optional inputs such as `cwd`, `timeoutMs`, and `maxStdoutBytes`; a workflow-file run additionally takes `argsJson` (a JSON string passed to `lobster run --args-json`). The optional inputs and their defaults are: `cwd` — relative working directory for the pipeline (must stay within the gateway working directory); `timeoutMs` — abort the workflow if it exceeds this duration (default `20000`); `maxStdoutBytes` — abort the workflow if output exceeds this size (default `512000`); and `argsJson` — JSON string passed to `lobster run --args-json` (workflow files only).

## Output envelope and approvals

Lobster returns a JSON envelope with one of three statuses: `ok` (finished successfully), `needs_approval` (paused; `requiresApproval.resumeToken` is required to resume), and `cancelled` (explicitly denied or cancelled). The tool surfaces the envelope in both `content` (pretty JSON) and `details` (raw object). A truncated `needs_approval` envelope from the email-triage example:

```json
{
  "ok": true,
  "status": "needs_approval",
  "output": [{ "summary": "5 need replies, 2 need action" }],
  "requiresApproval": {
    "type": "approval_request",
    "prompt": "Send 2 draft replies?",
    "items": [],
    "resumeToken": "..."
  }
}
```

When `requiresApproval` is present, inspect the prompt and decide: `approve: true` resumes and continues side effects; `approve: false` cancels and finalizes the workflow. Use `approve --preview-from-stdin --limit N` to attach a JSON preview to approval requests without custom jq/heredoc glue. Resume tokens are now compact — Lobster stores workflow resume state under its state dir and hands back a small token key.

## OpenProse pairing

OpenProse pairs well with Lobster: use `/prose` to orchestrate multi-agent prep, then run a Lobster pipeline for deterministic approvals. If a Prose program needs Lobster, allow the `lobster` tool for sub-agents via `tools.subagents.tools`.

## Safety

The source lists four safety properties of the runtime: **Local in-process only** — workflows execute inside the gateway process; no network calls from the plugin itself. **No secrets** — Lobster doesn't manage OAuth; it calls OpenClaw tools that do. **Sandbox-aware** — disabled when the tool context is sandboxed. **Hardened** — timeouts and output caps are enforced by the embedded runner.

## Troubleshooting

The page maps each runner error to a fix: `lobster timed out` → increase `timeoutMs`, or split a long pipeline; `lobster output exceeded maxStdoutBytes` → raise `maxStdoutBytes` or reduce output size; `lobster returned invalid JSON` → ensure the pipeline runs in tool mode and prints only JSON; and `lobster failed` → check gateway logs for the embedded runner error details.

## Case study: community workflows

The source cites one public example: a "second brain" CLI plus Lobster pipelines that manage three Markdown vaults (personal, partner, shared). The CLI emits JSON for stats, inbox listings, and stale scans; Lobster chains those commands into workflows like `weekly-review`, `inbox-triage`, `memory-consolidation`, and `shared-task-sync`, each with approval gates. AI handles judgment (categorization) when available and falls back to deterministic rules when not. The thread and repo links are in References.

**Source**: OpenClaw documentation — `tools/lobster` (mirror `inbox/openclaw_docs/tools/lobster.md`)
**Last Updated**: 2026-06-22
**Status**: Active
