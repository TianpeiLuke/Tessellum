---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - config
keywords:
  - openclaw config validate
  - config dry-run
  - dry-run json report
  - secretref resolvability
  - allow-exec exec refs
  - write safety rejected payload
  - openclaw.json.rejected
  - nix-mode immutable config
  - doctor --fix repair
  - tui config repair loop
topics:
  - OpenClaw
  - CLI Config Validation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/config
access_control_group: ["general"]
---

# OpenClaw — `openclaw config` Validation & Safe-Write

## Overview

This note is the validation/write-safety half of the `openclaw config` command (the `cli/config` source page); the non-interactive editing half — paths, values, `config set` modes, `config patch`, provider-builder flags, `config schema`, and `config file` — lives in the sibling note [oc_cli_config_edit](oc_cli_config_edit.md). It covers the procedures for proving a config change is safe before and after it touches `openclaw.json`: `--dry-run` (schema + SecretRef resolvability checks, the `--allow-exec` opt-in, and the `--dry-run --json` machine-readable report), the post-change write-safety model (validate-before-commit, `openclaw.json.rejected.*` payloads, symlink and `OPENCLAW_NIX_MODE=1` immutability restrictions), the standalone `config validate` command, and the TUI-assisted repair loop. Every command, flag, JSON field, and message below is reproduced verbatim from `inbox/openclaw_docs/cli/config.md`.

## Dry run

Use `--dry-run` to validate changes without writing `openclaw.json`. The flag works on builder-mode, JSON-mode, and batch-mode `config set` invocations, and on `config patch`:

```bash
openclaw config set channels.discord.token \
  --ref-provider default \
  --ref-source env \
  --ref-id DISCORD_BOT_TOKEN \
  --dry-run

openclaw config set channels.discord.token \
  --ref-provider vault \
  --ref-source exec \
  --ref-id discord/token \
  --dry-run \
  --allow-exec
```

Dry-run behavior depends on the assignment mode:

- **Builder mode**: runs SecretRef resolvability checks for changed refs/providers.
- **JSON mode** (`--strict-json`, `--json`, or batch mode): runs schema validation plus SecretRef resolvability checks.
- Policy validation also runs for known unsupported SecretRef target surfaces.
- Policy checks evaluate the **full post-change config**, so parent-object writes (for example setting `hooks` as an object) cannot bypass unsupported-surface validation.
- Exec SecretRef checks are **skipped by default** during dry-run to avoid command side effects.
- Use `--allow-exec` with `--dry-run` to opt in to exec SecretRef checks (this may execute provider commands).
- `--allow-exec` is dry-run only and errors if used without `--dry-run`.

For `config patch`, `--dry-run` likewise runs schema and SecretRef resolvability checks without writing, exec-backed SecretRefs are skipped by default, and `--allow-exec` is added when you intentionally want dry-run to execute provider commands.

### JSON output shape

`--dry-run --json` prints a machine-readable report. The documented fields are:

- `ok`: whether dry-run passed
- `operations`: number of assignments evaluated
- `checks`: whether schema/resolvability checks ran
- `checks.resolvabilityComplete`: whether resolvability checks ran to completion (false when exec refs are skipped)
- `refsChecked`: number of refs actually resolved during dry-run
- `skippedExecRefs`: number of exec refs skipped because `--allow-exec` was not set
- `errors`: structured missing-path, schema, or resolvability failures when `ok=false`

The full report shape (verbatim from source):

```json5
{
  ok: boolean,
  operations: number,
  configPath: string,
  inputModes: ["value" | "json" | "builder" | "unset", ...],
  checks: {
    schema: boolean,
    resolvability: boolean,
    resolvabilityComplete: boolean,
  },
  refsChecked: number,
  skippedExecRefs: number,
  errors?: [
    {
      kind: "missing-path" | "schema" | "resolvability",
      message: string,
      ref?: string, // present for resolvability errors
    },
  ],
}
```

A failure report carries an `errors` array; the source failure example (a missing env var) renders as:

```json
{
  "ok": false,
  "operations": 1,
  "configPath": "~/.openclaw/openclaw.json",
  "inputModes": ["builder"],
  "checks": {
    "schema": false,
    "resolvability": true,
    "resolvabilityComplete": true
  },
  "refsChecked": 1,
  "skippedExecRefs": 0,
  "errors": [
    {
      "kind": "resolvability",
      "message": "Error: Environment variable \"MISSING_TEST_SECRET\" is not set.",
      "ref": "env:default:MISSING_TEST_SECRET"
    }
  ]
}
```

### If dry-run fails

The source enumerates these failure messages and their remediation:

- `config schema validation failed`: your post-change config shape is invalid; fix path/value or provider/ref object shape.
- `Config policy validation failed: unsupported SecretRef usage`: move that credential back to plaintext/string input and keep SecretRefs on supported surfaces only.
- `SecretRef assignment(s) could not be resolved`: referenced provider/ref currently cannot resolve (missing env var, invalid file pointer, exec provider failure, or provider/source mismatch).
- `Dry run note: skipped <n> exec SecretRef resolvability check(s)`: dry-run skipped exec refs; rerun with `--allow-exec` if you need exec resolvability validation.
- For batch mode, fix failing entries and rerun `--dry-run` before writing.

## Write safety

`openclaw config set` and other OpenClaw-owned config writers validate the **full post-change config** before committing it to disk. If the new payload fails schema validation or looks like a destructive clobber, the active config is left alone and the rejected payload is saved beside it as `openclaw.json.rejected.*`.

The active config path must be a **regular file** — symlinked `openclaw.json` layouts are unsupported for writes; use `OPENCLAW_CONFIG_PATH` to point directly at the real file instead. Separately, when `OPENCLAW_NIX_MODE=1`, OpenClaw treats `openclaw.json` as immutable: read-only commands such as `config get`, `config file`, `config schema`, and `config validate` still work, but config writers refuse (in that mode, agents edit the Nix source for the install instead). The Nix-immutability refusal is documented primarily on the edit side ([oc_cli_config_edit](oc_cli_config_edit.md)); it is repeated here because it is one of the write-safety restrictions a writer enforces.

The source recommends preferring CLI writes for small edits and validating around them — dry-run, apply, then validate (`openclaw config set gateway.reload.mode hybrid --dry-run` → `openclaw config set gateway.reload.mode hybrid` → `openclaw config validate`). If a write is rejected, inspect the saved payload and fix the full config shape:

```bash
CONFIG="$(openclaw config file)"
ls -lt "$CONFIG".rejected.* 2>/dev/null | head
openclaw config validate
```

Direct editor writes are still allowed, but the running Gateway treats them as **untrusted until they validate**. Invalid direct edits fail startup or are skipped by hot reload; the Gateway does not rewrite `openclaw.json`. Run `openclaw doctor --fix` to repair prefixed/clobbered config or restore the last-known-good copy. Whole-file recovery is reserved for doctor repair: plugin schema changes or `minHostVersion` skew stay loud instead of rolling back unrelated user settings such as models, providers, auth profiles, channels, gateway exposure, tools, memory, browser, or cron config.

## Validate

`openclaw config validate` checks the current config against the active schema **without starting the gateway**:

```bash
openclaw config validate
openclaw config validate --json
```

After `openclaw config validate` is passing, you can use the local TUI to have an embedded agent compare the active config against the docs while you validate each change from the same terminal. If validation is already failing, start with `openclaw configure` or `openclaw doctor --fix` instead — `openclaw chat` does not bypass the invalid-config guard. Enter the TUI with `openclaw chat`, then inside the TUI you can shell out to the same validation commands with `!`:

```text
!openclaw config file
!openclaw docs gateway auth token secretref
!openclaw config validate
!openclaw doctor
```

The documented **typical repair loop** is: (1) **Compare with docs** — ask the agent to compare your current config with the relevant docs page and suggest the smallest fix; (2) **Apply targeted edits** — with `openclaw config set` or `openclaw configure`; (3) **Re-validate** — rerun `openclaw config validate` after each change; (4) **Doctor for runtime issues** — if validation passes but the runtime is still unhealthy, run `openclaw doctor` or `openclaw doctor --fix` for migration and repair help.

**Source**: OpenClaw documentation — `cli/config` (mirror `inbox/openclaw_docs/cli/config.md`)
**Last Updated**: 2026-06-22
**Status**: Active
