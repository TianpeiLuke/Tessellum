---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - exec_approvals
keywords:
  - openclaw safe bins
  - tools.exec.safeBins stdin-only
  - safeBinProfiles custom profile
  - safe bin argv validation denied flags
  - safeBinTrustedDirs trusted binary directories
  - interpreter runtime command binding
  - deny on ambiguity exec approval
  - shell chaining wrappers multiplexers allowlist
  - safe bins versus allowlist
topics:
  - OpenClaw
  - Exec Approvals
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/exec-approvals-advanced
access_control_group: ["general"]
---

# OpenClaw — Exec Approvals Advanced: Safe Bins and Interpreter Binding

## Overview

This note covers the advanced exec-approval fast-path documented on the first half of the `tools/exec-approvals-advanced` source page: the `tools.exec.safeBins` stdin-only allow path, its deterministic argv validation and denied-flag profiles, trusted binary directories, shell chaining/wrapper/multiplexer unwrapping, the safe-bins-versus-allowlist distinction, and the conservative interpreter/runtime file-binding model with its async-followup delivery behavior. It is a configuration/operations procedure for narrowing which host commands skip an approval prompt while keeping a fail-closed boundary. Approval forwarding to chat channels, native approval delivery, the macOS IPC flow, and the page's FAQ are companion topics covered in `oc_tools_exec_approvals_forwarding`; the core policy and approval flow live in `oc_tools_exec_approvals_policy` and `oc_tools_exec_approvals_operations`.

## Safe bins (stdin-only)

`tools.exec.safeBins` defines a small list of **stdin-only** binaries (for example `cut`) that can run in allowlist mode **without** explicit allowlist entries. Safe bins reject positional file args and path-like tokens, so they can only operate on the incoming stream — treat this as a narrow fast-path for stream filters, not a general trust list.

Default safe bins are: `cut`, `uniq`, `head`, `tail`, `tr`, `wc`.

`grep` and `sort` are **not** in the default list. If you opt them in, keep explicit allowlist entries for their non-stdin workflows. For `grep` in safe-bin mode, provide the pattern with `-e`/`--regexp`; the positional pattern form is rejected so file operands cannot be smuggled as ambiguous positionals.

A standing warning applies: do **not** add interpreter or runtime binaries (for example `python3`, `node`, `ruby`, `bash`, `sh`, `zsh`) to `safeBins`. If a command can evaluate code, execute subcommands, or read files by design, prefer explicit allowlist entries and keep approval prompts enabled. Custom safe bins must define an explicit profile in `tools.exec.safeBinProfiles.<bin>`.

### Argv validation and denied flags

Validation is deterministic from argv shape only (no host filesystem existence checks), which prevents file-existence oracle behavior from allow/deny differences. File-oriented options are denied for default safe bins; long options are validated fail-closed — unknown flags and ambiguous abbreviations are rejected.

Denied flags by safe-bin profile:

- `grep`: `--dereference-recursive`, `--directories`, `--exclude-from`, `--file`, `--recursive`, `-R`, `-d`, `-f`, `-r`
- `jq`: `--argfile`, `--from-file`, `--library-path`, `--rawfile`, `--slurpfile`, `-L`, `-f`
- `sort`: `--compress-program`, `--files0-from`, `--output`, `--random-source`, `--temporary-directory`, `-T`, `-o`
- `wc`: `--files0-from`

Safe bins also force argv tokens to be treated as **literal text** at execution time (no globbing and no `$VARS` expansion) for stdin-only segments, so patterns like `*` or `$HOME/...` cannot be used to smuggle file reads.

### Trusted binary directories

Safe bins must resolve from trusted binary directories (system defaults plus optional `tools.exec.safeBinTrustedDirs`). `PATH` entries are never auto-trusted. Default trusted directories are intentionally minimal: `/bin`, `/usr/bin`. If your safe-bin executable lives in package-manager/user paths (for example `/opt/homebrew/bin`, `/usr/local/bin`, `/opt/local/bin`, `/snap/bin`), add them explicitly to `tools.exec.safeBinTrustedDirs`.

### Shell chaining, wrappers, and multiplexers

Shell chaining (`&&`, `||`, `;`) is allowed when every top-level segment satisfies the allowlist (including safe bins or skill auto-allow). Redirections remain unsupported in allowlist mode. Command substitution (`$()` / backticks) is rejected during allowlist parsing, including inside double quotes; use single quotes if you need literal `$()` text.

On macOS companion-app approvals, raw shell text containing shell control or expansion syntax (`&&`, `||`, `;`, `|`, `` ` ``, `$`, `<`, `>`, `(`, `)`) is treated as an allowlist miss unless the shell binary itself is allowlisted.

For shell wrappers (`bash|sh|zsh ... -c/-lc`), request-scoped env overrides are reduced to a small explicit allowlist: `TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`.

For `allow-always` decisions in allowlist mode, known dispatch wrappers (`env`, `flock`, `nice`, `nohup`, `stdbuf`, `timeout`) persist the inner executable path instead of the wrapper path. Shell multiplexers (`busybox`, `toybox`) are unwrapped for shell applets (`sh`, `ash`, etc.) the same way. If a wrapper or multiplexer cannot be safely unwrapped, no allowlist entry is persisted automatically.

If you allowlist interpreters like `python3` or `node`, prefer `tools.exec.strictInlineEval=true` so inline eval still requires an explicit approval. In strict mode, `allow-always` can still persist benign interpreter/script invocations, but inline-eval carriers are not persisted automatically.

### Safe bins versus allowlist

| Topic            | `tools.exec.safeBins`                                  | Allowlist (`exec-approvals.json`)                                                  |
| ---------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| Goal             | Auto-allow narrow stdin filters                        | Explicitly trust specific executables                                              |
| Match type       | Executable name + safe-bin argv policy                 | Resolved executable path glob, or bare command-name glob for PATH-invoked commands |
| Argument scope   | Restricted by safe-bin profile and literal-token rules | Path match by default; optional `argPattern` can restrict parsed argv              |
| Typical examples | `head`, `tail`, `tr`, `wc`                             | `jq`, `python3`, `node`, `ffmpeg`, custom CLIs                                     |
| Best use         | Low-risk text transforms in pipelines                  | Any tool with broader behavior or side effects                                     |

Configuration location: `safeBins` comes from config (`tools.exec.safeBins` or per-agent `agents.list[].tools.exec.safeBins`); `safeBinTrustedDirs` likewise (`tools.exec.safeBinTrustedDirs` or per-agent `agents.list[].tools.exec.safeBinTrustedDirs`); `safeBinProfiles` likewise (`tools.exec.safeBinProfiles` or per-agent `agents.list[].tools.exec.safeBinProfiles`), where per-agent profile keys override global keys. Allowlist entries instead live in the host-local approvals file under `agents.<id>.allowlist` (or via Control UI / `openclaw approvals allowlist ...`).

Two operator diagnostics back this surface: `openclaw security audit` warns with `tools.exec.safe_bins_interpreter_unprofiled` when interpreter/runtime bins appear in `safeBins` without explicit profiles, and `openclaw doctor --fix` can scaffold missing custom `safeBinProfiles.<bin>` entries as `{}` (review and tighten afterward). Interpreter/runtime bins are not auto-scaffolded.

A custom profile pins positional bounds and explicit value/denied flags:

```json5
{
  tools: {
    exec: {
      safeBins: ["jq", "myfilter"],
      safeBinProfiles: {
        myfilter: {
          minPositional: 0,
          maxPositional: 0,
          allowedValueFlags: ["-n", "--limit"],
          deniedFlags: ["-f", "--file", "-c", "--command"],
        },
      },
    },
  },
}
```

If you explicitly opt `jq` into `safeBins`, OpenClaw still rejects the `env` builtin in safe-bin mode, so `jq -n env` cannot dump the host process environment without an explicit allowlist path or approval prompt.

## Interpreter/runtime commands

Approval-backed interpreter/runtime runs are intentionally conservative:

- Exact argv/cwd/env context is always bound.
- Direct shell script and direct runtime file forms are best-effort bound to one concrete local file snapshot.
- Common package-manager wrapper forms that still resolve to one direct local file (for example `pnpm exec`, `pnpm node`, `npm exec`, `npx`) are unwrapped before binding.
- If OpenClaw cannot identify exactly one concrete local file for an interpreter/runtime command (for example package scripts, eval forms, runtime-specific loader chains, or ambiguous multi-file forms), approval-backed execution is denied instead of claiming semantic coverage it does not have.
- For those workflows, prefer sandboxing, a separate host boundary, or an explicit trusted allowlist/full workflow where the operator accepts the broader runtime semantics.

When approvals are required, the exec tool returns immediately with an approval id; use that id to correlate later approved-run system events (`Exec finished`, and `Exec running` when configured). If no decision arrives before the timeout, the request is treated as an approval timeout and surfaced as a terminal host-command denial. For main-agent async approvals with an originating session, OpenClaw also resumes that session with an internal followup so the agent observes that the command did not run instead of later repairing a missing result.

### Followup delivery behavior

After an approved async exec finishes, OpenClaw sends a followup `agent` turn to the same session. Denied async approvals use the same main-session followup path for the denial status, but they do not register elevated runtime handoffs and they do not run the command. Denials without a resumable main session are either suppressed or reported through a safe direct route when one exists. The external-vs-session delivery decision follows four rules:

- If a valid external delivery target exists (deliverable channel plus target `to`), followup delivery uses that channel.
- In webchat-only or internal-session flows with no external target, followup delivery stays session-only (`deliver: false`).
- If a caller explicitly requests strict external delivery with no resolvable external channel, the request fails with `INVALID_REQUEST`.
- If `bestEffortDeliver` is enabled and no external channel can be resolved, delivery is downgraded to session-only instead of failing.

**Source**: OpenClaw documentation — `tools/exec-approvals-advanced` (mirror `inbox/openclaw_docs/tools/exec-approvals-advanced.md`), Safe bins + Interpreter/runtime sections
**Last Updated**: 2026-06-22
**Status**: Active
