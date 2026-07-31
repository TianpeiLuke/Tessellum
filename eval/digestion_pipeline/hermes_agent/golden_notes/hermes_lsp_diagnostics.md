---
tags:
  - resource
  - documentation
  - hermes_agent
  - lsp
  - diagnostics
keywords:
  - LSP diagnostics
  - language server protocol
  - post-write lint check
  - semantic diagnostics
  - baseline diff
  - lazy-spawned servers
topics:
  - Hermes Agent
  - Code Editing
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/lsp
access_control_group: ["general"]
---

# Hermes Agent — LSP Semantic Diagnostics

## Overview

LSP diagnostics is the **semantic-feedback layer** Hermes wires into its file-editing tools: it runs full language servers — pyright, gopls, rust-analyzer, typescript-language-server, clangd, and ~20 more — as background subprocesses and feeds their diagnostics into the post-write lint check used by `write_file` and `patch`. When the agent edits a file, it sees exactly the errors that edit introduced — not just syntax errors, but **type errors, undefined names, missing imports, and project-wide semantic issues** the language server detects. This is the same architecture top-tier coding agents use, but Hermes ships it self-contained: no editor host required, no plugins to install, no separate daemon to manage. The model is defined by four properties — it is git-workspace-gated, layered (fast in-process syntax check first, LSP second), baseline-diffed (only NEW diagnostics surface), and never-breaks-a-write (every LSP failure path falls back silently to the syntax-only result).

## When LSP runs

LSP is gated on **git workspace detection**. When the agent's working directory (or the file being edited) is inside a git repository, LSP runs against that workspace. When neither is in a git repo, LSP stays dormant — useful for messaging gateways where the cwd is the user's home directory and there's no project to diagnose.

The check is layered: in-process syntax check first (microseconds), then LSP diagnostics second when syntax is clean. A flaky or missing language server can never break a write — every LSP failure path falls back silently to the syntax-only result.

Concretely, on every successful `write_file` or `patch`:

1. Hermes captures a baseline of current diagnostics for the file.
2. Performs the write.
3. Re-queries the language server, filters out diagnostics that were already in the baseline, and surfaces only the new ones.

The agent sees output like:

```
{
  "bytes_written": 42,
  "dirs_created": false,
  "lint": {"status": "ok", "output": ""},
  "lsp_diagnostics": "LSP diagnostics introduced by this edit:\n<diagnostics file=\"/path/to/foo.py\">\nERROR [42:5] Cannot find name 'foo' [reportUndefinedVariable] (Pyright)\nERROR [50:1] Argument of type \"str\" is not assignable to \"int\" [reportArgumentType] (Pyright)\n</diagnostics>"
}
```

The `lint` field carries the syntax-check result (microsecond in-process parse via `ast.parse`, `json.loads`, etc.); the `lsp_diagnostics` field carries the semantic diagnostics from the real language server. These are two channels with independent signals — the agent sees a syntax-clean file with semantic problems as `lint: ok` plus a populated `lsp_diagnostics`.

## Supported languages

Hermes ships a registry of ~25 language servers. Each entry maps a language (by file extension) to a server binary and an auto-install recipe (`npm`, `go install`, or `manual`). The npm-installable set includes Python (`pyright-langserver`), TypeScript/JavaScript/JSX/TSX (`typescript-language-server`), Vue (`@vue/language-server`), Svelte (`svelte-language-server`), Astro (`@astrojs/language-server`), Bash/Zsh (`bash-language-server`), YAML (`yaml-language-server`), PHP (`intelephense`), and Dockerfile (`dockerfile-language-server-nodejs`). Go (`gopls`) installs via `go install`. The remaining servers are `manual`: Rust (`rust-analyzer`, rustup), C/C++ (`clangd`, LLVM), Lua (`lua-language-server`), OCaml (`ocaml-lsp`, opam), Terraform (`terraform-ls`), Dart (`dart language-server`), Haskell (`haskell-language-server`, ghcup), Julia (`julia` + LanguageServer.jl), Clojure (`clojure-lsp`), Nix (`nixd`), Zig (`zls`), Gleam (`gleam lsp`), Elixir (`elixir-ls`), Prisma (`prisma language-server`), Kotlin (`kotlin-language-server`), and Java (`jdtls`).

For `manual` entries, install the server through whatever toolchain manager makes sense for that language (rustup, ghcup, opam, brew, …); Hermes auto-detects the binary on PATH or in `<HERMES_HOME>/lsp/bin/`. A few servers ship alongside a peer dependency that npm won't auto-pull — the current case is `typescript-language-server`, which requires the `typescript` SDK importable from the same `node_modules` tree, so Hermes installs both packages together when you run `hermes lsp install typescript` or auto-install fires on first use.

## CLI

```
hermes lsp status          # service state + per-server install status
hermes lsp list            # registry, optionally --installed-only
hermes lsp install <id>    # eagerly install one server
hermes lsp install-all     # try every server with a known recipe
hermes lsp restart         # tear down running clients
hermes lsp which <id>      # print resolved binary path
```

`hermes lsp status` is the best starting point — it shows which languages will get semantic diagnostics today and which need a binary installed.

## Configuration

The defaults work for typical setups; nothing to set if the binaries are on PATH. The `lsp:` config block carries a master toggle, the diagnostics wait mode/timeout, the missing-binary install strategy (`auto` installs into `<HERMES_HOME>/lsp/bin`, `manual` only uses PATH binaries), and a `servers:` map of per-server overrides.

```yaml
# config.yaml
lsp:
  enabled: true
  wait_mode: document      # "document" or "full"
  wait_timeout: 5.0
  install_strategy: auto   # auto = install via npm/pip/go install; manual = PATH only
  servers:
    pyright:
      disabled: false
      command: ["/abs/path/to/pyright-langserver", "--stdio"]
      env: { PYRIGHT_LOG_LEVEL: "info" }
      initialization_options:
        python:
          analysis:
            typeCheckingMode: "strict"
    typescript:
      disabled: true       # skip TS even when its extensions match
```

The per-server keys are: `disabled: true` (skip this server entirely even when its extensions match a file); `command: [bin, ...args]` (pin a custom binary path, bypassing auto-install); `env: {KEY: value}` (extra env vars passed to the spawned process); and `initialization_options: {...}` (merged into the LSP `initializationOptions` payload sent in the `initialize` handshake — server-specific, consult the language server's docs).

## Installation locations

When `install_strategy: auto`, Hermes installs binaries into `<HERMES_HOME>/lsp/bin/`. NPM packages land in `<HERMES_HOME>/lsp/node_modules/` with bin symlinks one level up. Go binaries come from `go install` with `GOBIN` pointed at the staging dir. Nothing is ever installed to `/usr/local/`, `~/.local/`, or any other shared location — the staging dir is fully Hermes-owned and is removed when you reset the profile.

## Performance characteristics

LSP servers are **lazy-spawned** on first use. Editing a Python file in a project that's never seen `.py` traffic spawns pyright; the spawn takes 1-3 seconds for most servers (rust-analyzer can take 10+ on a cold project). Subsequent edits in the same workspace re-use the running server.

The LSP layer adds a few milliseconds to clean writes when no diagnostics are emitted. When diagnostics are emitted, the wait budget is `wait_timeout` seconds — typically the server responds in tens of milliseconds for pyright/tsserver and a few seconds for rust-analyzer mid-indexing.

Servers are kept alive for the life of the Hermes process. There's no idle-timeout reaper — the cost of restarting the server's index on every write would be far higher than holding the daemon.

## Disabling

Set `lsp.enabled: false` in `config.yaml` to disable the entire subsystem. The post-write check falls back to the in-process syntax check (`ast.parse` for Python, `json.loads` for JSON, etc.) which ships unchanged from earlier versions. To disable a single language without disabling the whole layer, set `disabled: true` under that server (e.g. `lsp.servers.rust-analyzer.disabled: true`).

## Troubleshooting

- **`hermes lsp status` shows a server as "missing"** — the binary isn't on PATH and isn't in `<HERMES_HOME>/lsp/bin/`. Run `hermes lsp install <server_id>` to attempt an auto-install, or install the binary manually through the language's normal toolchain.
- **`Backend warnings` section in `hermes lsp status`** — some servers are thin wrappers around an external CLI for actual diagnostics; they spawn cleanly and accept requests but never emit errors when the sidecar binary is missing. The most common case is `bash-language-server`, which delegates to `shellcheck`. Install the named tool through your OS package manager (`apt install shellcheck`, `brew install shellcheck`, `scoop install shellcheck`). The same warning is logged once at server spawn time in `~/.hermes/logs/agent.log`.
- **Server starts but never returns diagnostics** — check `~/.hermes/logs/agent.log` for `[agent.lsp.client]` entries; both stderr from the language server and protocol errors land there. Some servers (rust-analyzer especially) need to finish a project-wide index before they emit per-file diagnostics; the first edit after server start may complete with no diagnostics, subsequent edits picking them up.
- **Server crashed** — a crashed server is added to the broken-set and won't be retried for the rest of the session. Run `hermes lsp restart` to clear the set; the next edit re-spawns.
- **Editing a file outside any git repo** — by design, LSP only runs inside a git repository. If the project isn't yet initialized, run `git init` to enable LSP diagnostics. Otherwise the in-process syntax-only fallback applies.

**Source**: `inbox/hermes_agent_docs/user-guide/features/lsp.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/lsp
**Last Updated**: 2026-06-19
**Status**: Active
