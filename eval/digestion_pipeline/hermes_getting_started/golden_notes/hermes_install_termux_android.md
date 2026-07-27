---
tags:
  - resource
  - documentation
  - hermes_agent
  - getting_started
  - installation
keywords:
  - hermes termux install
  - android cli agent
  - termux extra
  - android_api_level
  - one-line installer
  - phone install limitations
topics:
  - Hermes Agent
  - Getting Started
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/getting-started/termux
access_control_group: ["general"]
---

# Hermes on Android with Termux

## Overview

This is the **tested install path for running Hermes Agent directly on an Android phone** through [Termux](https://termux.dev/). It produces a working local CLI on the phone plus the core extras currently known to install cleanly on Android — the CLI, cron, PTY/background terminal, Telegram gateway (best-effort), MCP, Honcho memory, and ACP. The recommended mobile install is intentionally narrower than the desktop/server install: it deliberately omits desktop/server-style dependencies (voice, browser/Playwright, Docker isolation) that are not published or not yet validated for Android. The result is a capable phone-native CLI agent rather than the full feature set.

## What is supported in the tested path?

The tested Termux bundle installs:

- the Hermes CLI
- cron support
- PTY/background terminal support
- Telegram gateway support (manual / best-effort background runs)
- MCP support
- Honcho memory support
- ACP support

Concretely, it maps to:

```bash
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

## What is not part of the tested path yet?

A few features still need desktop/server-style dependencies that are not published for Android, or have not been validated on phones yet:

- `.[all]` is not supported on Android today
- the `voice` extra is blocked by `faster-whisper -> ctranslate2`, and `ctranslate2` does not publish Android wheels
- automatic browser / Playwright bootstrap is skipped in the Termux installer
- Docker-based terminal isolation is not available inside Termux
- Android may still suspend Termux background jobs, so gateway persistence is best-effort rather than a normal managed service

That does not stop Hermes from working well as a phone-native CLI agent — it just means the recommended mobile install is intentionally narrower than the desktop/server install.

## Option 1: One-line installer

Hermes ships a Termux-aware installer path:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

On Termux, the installer automatically: uses `pkg` for system packages; creates the venv with `python -m venv`; attempts the broad `.[termux-all]` extra first and falls back to the smaller `.[termux]` extra (then a base install) — the curl installer matches this order automatically; links `hermes` into `$PREFIX/bin` so it stays on your Termux PATH; and skips the untested browser / WhatsApp bootstrap. Use the manual path below if you want the explicit commands or need to debug a failed install.

## Option 2: Manual install (fully explicit)

The manual path runs seven steps. First, update Termux and install system packages, which provide the build toolchain Android needs:

```bash
pkg update
pkg install -y git python clang rust make pkg-config libffi openssl nodejs ripgrep ffmpeg
```

Source rationale for the packages: `python` (runtime + venv support); `git` (clone/update the repo); `clang`, `rust`, `make`, `pkg-config`, `libffi`, `openssl` (needed to build a few Python dependencies on Android); `nodejs` (optional Node runtime for experiments beyond the tested core path); `ripgrep` (fast file search); `ffmpeg` (media / TTS conversions).

Then clone Hermes (`git clone https://github.com/NousResearch/hermes-agent.git && cd hermes-agent`) and create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
python -m pip install --upgrade pip setuptools wheel
```

`ANDROID_API_LEVEL` is important for Rust / maturin-based packages such as `jiter`. Next, install the tested Termux bundle (or `-e '.'` for the minimal core agent, also with `-c constraints-termux.txt`):

```bash
python -m pip install -e '.[termux]' -c constraints-termux.txt
```

Finally, put `hermes` on the Termux PATH, then verify and start it:

```bash
ln -sf "$PWD/venv/bin/hermes" "$PREFIX/bin/hermes"
hermes version
hermes doctor
hermes
```

`$PREFIX/bin` is already on PATH in Termux, so the symlink makes the `hermes` command persist across new shells without re-activating the venv every time.

## Recommended follow-up setup

After install, configure a model with `hermes model` (or set keys directly in `~/.hermes/.env`), and re-run the full interactive setup wizard later with `hermes setup`.

The tested Termux path skips Node/browser bootstrap on purpose. To experiment with browser tooling later, install optional Node dependencies manually (`pkg install nodejs-lts` then `npm install`). The browser tool automatically includes Termux directories (`/data/data/com.termux/files/usr/bin`) in its PATH search, so `agent-browser` and `npx` are discovered without extra PATH configuration. Treat browser / WhatsApp tooling on Android as experimental until documented otherwise.

## Troubleshooting

- **`No solution found` when installing `.[all]`** — use the tested Termux bundle (`.[termux]`) instead. The blocker is the `voice` extra: `voice` pulls `faster-whisper`, which depends on `ctranslate2`, which does not publish Android wheels.
- **`uv pip install` fails on Android** — use the Termux path with the stdlib venv + `pip` instead (create the venv, export `ANDROID_API_LEVEL`, upgrade pip/setuptools/wheel, then `pip install -e '.[termux]' -c constraints-termux.txt`).
- **`jiter` / `maturin` complains about `ANDROID_API_LEVEL`** — set the API level explicitly before installing: `export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"`.
- **`hermes doctor` says ripgrep or Node is missing** — install them with Termux packages: `pkg install ripgrep nodejs`.
- **Build failures while installing Python packages** — make sure the build toolchain is installed (`pkg install clang rust make pkg-config libffi openssl`) and retry.

## Known limitations on phones

- Docker backend is unavailable
- local voice transcription via `faster-whisper` is unavailable in the tested path
- browser automation setup is intentionally skipped by the installer
- some optional extras may work, but only `.[termux]` and `.[termux-all]` are currently documented as the tested Android bundles

If you hit a new Android-specific issue, the source asks you to open a GitHub issue with your Android version, `termux-info`, `python --version`, `hermes doctor`, and the exact install command and full error output.

## Related Notes

**Terms**
- [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — package installed on phone; relevance: page's subject.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — phone-native CLI agent; relevance: framing of the Android use case.
- [term_mcp](../../term_dictionary/term_mcp.md) — MCP; relevance: §supported — MCP works in `.[termux]`.
- [term_cron](../../term_dictionary/term_cron.md) — cron; relevance: §supported — cron in the tested bundle.
- [term_voice_wake](../../term_dictionary/term_voice_wake.md) — voice; relevance: §unsupported — voice blocked by ctranslate2 (no Android wheels).
- [term_agentic_memory](../../term_dictionary/term_agentic_memory.md) — Honcho memory; relevance: §supported — Honcho memory in `.[termux]`.
- [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — terminal backend; relevance: §limitations — Docker backend unavailable on phones.
- [term_python](../../term_dictionary/term_python.md) — runtime + venv; relevance: manual path builds a `python -m venv` + `pip install -e '.[termux]'`.

**Code-Repos**
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — installer + extras; relevance: Termux-aware `install.sh`, `.[termux]`/`.[termux-all]` extras, `pkg`/`pyproject` paths.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI + doctor; relevance: `hermes version`, `hermes doctor`, `hermes setup` post-install.
- [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP support; relevance: MCP is in the tested Termux path.
- [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — cron support; relevance: cron is a supported Termux extra.
- [repo_hermes_agent_acp](../../../areas/code_repos/repo_hermes_agent_acp.md) — ACP support; relevance: ACP listed as supported in the tested bundle.

**Snippets**
- [snippet_hermes_agent_setup_hermes_sh](../../code_snippets/snippet_hermes_agent_setup_hermes_sh.md) — Termux-aware `install.sh`; relevance: one-line install path on Android.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer + extras; relevance: `.[termux]`/`.[termux-all]` extras selection.
- [snippet_hermes_agent_core_bootstrap_utf8](../../code_snippets/snippet_hermes_agent_core_bootstrap_utf8.md) — startup bootstrap; relevance: phone-native venv startup.
- [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — `hermes doctor`; relevance: §Troubleshooting verify.
- [snippet_hermes_agent_cli_memory_setup](../../code_snippets/snippet_hermes_agent_cli_memory_setup.md) — memory setup; relevance: §supported Honcho memory in the tested bundle.
- [snippet_hermes_agent_acp_entry](../../code_snippets/snippet_hermes_agent_acp_entry.md) — ACP entry; relevance: §supported — ACP works in `.[termux]`.
- [snippet_hermes_agent_cron_helpers](../../code_snippets/snippet_hermes_agent_cron_helpers.md) — cron helpers; relevance: §supported — cron in the tested extra.
- [snippet_hermes_agent_mcp_serve_hermes_as_server](../../code_snippets/snippet_hermes_agent_mcp_serve_hermes_as_server.md) — MCP surface; relevance: §supported — MCP works on Termux.
- [snippet_hermes_agent_tools_lazy_deps](../../code_snippets/snippet_hermes_agent_tools_lazy_deps.md) — lazy optional deps; relevance: §unsupported — voice/Docker deps skipped (no Android wheels).
- [snippet_hermes_agent_honcho_session_lifecycle](../../code_snippets/snippet_hermes_agent_honcho_session_lifecycle.md) — Honcho sessions; relevance: §supported Honcho memory extra runtime.

**Docs**
- [hermes_installation](hermes_installation.md) — main install; relevance: Termux is the Android variant of it.
- [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — first chat; relevance: post-install `hermes model`/chat.
- [hermes_install_nix_quickstart](hermes_install_nix_quickstart.md) — Nix install; relevance: sibling alternative-platform install.
- [hermes_updating_uninstalling](hermes_updating_uninstalling.md) — update; relevance: keeping the phone install current.
- [hermes_mcp](hermes_mcp_concept_config.md) — MCP; relevance: the supported Termux MCP extra.
- [hermes_honcho](hermes_memory_providers_honcho.md) — Honcho memory; relevance: the supported Termux memory extra.
- [cc_install](../claude_code/cc_install.md) — analogous install; relevance: parallel per-platform install flow.
- [cc_install_failures_reference](../claude_code/cc_install_failures_reference.md) — analogous failure ref; relevance: parallels §Troubleshooting (`No solution found`, build failures).
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — analogous diagnostics; relevance: parallels `hermes doctor` verify.
- [cc_execution_environments](../claude_code/cc_execution_environments.md) — analogous constrained runtime; relevance: parallels the narrower phone-native capability set.

**Source**: `inbox/hermes_agent_docs/getting-started/termux.md` · https://hermes-agent.nousresearch.com/docs/getting-started/termux
**Last Updated**: 2026-06-19
**Status**: Active
