---
tags:
  - resource
  - documentation
  - hermes_agent
  - contributing
  - developer_guide
keywords:
  - hermes contributing
  - development setup
  - cross-platform compatibility
  - code style profile-safe paths
  - security considerations
  - conventional commits pull request process
  - get_hermes_home
topics:
  - Hermes Agent
  - Contributing
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/contributing
access_control_group: ["general"]
---

# Hermes Agent — Contributing & Dev Setup

## Overview

This is the **contributor on-ramp** for Hermes Agent: it is the procedure for setting up a development environment, understanding what the project values, and getting a pull request merged. It is the *router* that sits on top of the more specific authoring procedures — building a [built-in tool](hermes_adding_built_in_tool.md), [inference provider](hermes_adding_inference_provider.md), [platform adapter](hermes_adding_platform_adapter_plugin.md), or [skill](hermes_creating_skill_format.md) — pointing each contribution type at the right deep-dive while owning the cross-cutting concerns every contributor must respect: dev setup, code style, cross-platform compatibility, security, and the PR process.

Two facts shape everything below. First, Hermes has terminal access, so **security is a first-class review concern** (shell-injection, prompt-injection, path-traversal hardening). Second, Hermes officially supports Linux, macOS, WSL2, and native Windows, so **cross-platform discipline is mandatory** — Unix-only kernel primitives (`SIGKILL`, `os.setsid`, `termios`/`fcntl`) must be guarded or routed through centralized helpers. The recommended dev bootstrap is the *same* path users take (standard installer → work inside the cloned repo), which keeps the dev layout identical to what the CLI, updater, lazy-dependency installer, gateway, and docs all assume.

## Contribution Priorities

Contributions are valued in this order (highest first):

1. **Bug fixes** — crashes, incorrect behavior, data loss
2. **Cross-platform compatibility** — macOS, different Linux distros, WSL2
3. **Security hardening** — shell injection, prompt injection, path traversal
4. **Performance and robustness** — retry logic, error handling, graceful degradation
5. **New skills** — broadly useful ones
6. **New tools** — rarely needed; most capabilities should be skills
7. **Documentation** — fixes, clarifications, new examples

The "new tools rarely needed; most capabilities should be skills" ordering encodes the same skill-vs-tool decision that opens [Adding Tools](hermes_adding_built_in_tool.md) and [Creating Skills](hermes_creating_skill_format.md).

## Common contribution paths

The router for *where to start* by what you are building:

- **Custom/local tool without modifying Hermes core** → Build a Hermes Plugin (the plugin path).
- **New built-in core tool for Hermes itself** → [Adding Tools](hermes_adding_built_in_tool.md).
- **New skill** → [Creating Skills](hermes_creating_skill_format.md).
- **New inference provider** → [Adding Providers](hermes_adding_inference_provider.md).

## Development Setup

**Prerequisites:** Git with the `git-lfs` extension; Python 3.11+ (uv installs it if missing); `uv` (fast Python package manager); Node.js 20+ (optional — needed for browser tools and the WhatsApp bridge).

**Install with the standard installer (recommended).** For most contributors the best bootstrap is the same path users take: run the standard installer, then work inside the repository it cloned. The installer creates the Hermes venv, wires the `hermes` command, stamps the install method for `hermes update`, and clones the full git project into `$HERMES_HOME/hermes-agent` (usually `~/.hermes/hermes-agent`) — keeping the dev environment on the same layout the CLI, updater, lazy dependency installer, gateway, and docs assume.

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
cd "${HERMES_HOME:-$HOME/.hermes}/hermes-agent"

# Add dev/test extras on top of the standard install.
uv pip install -e ".[all,dev]"

# Optional: browser tools / docs site dependencies.
npm install
```

Then create branches and run tests from that checkout with `git checkout -b fix/description` and `scripts/run_tests.sh`.

**Manual clone fallback** (only if you intentionally do not want Hermes' managed install layout — e.g. a throwaway clone inside a container or CI job): create a venv with Python 3.11 via `uv venv`, install `.[all,dev]`, and make sure you run the `hermes` entrypoint *from this venv* (running system `python3 -m hermes_cli.main` can pick up unrelated system packages).

**Configure for development** — seed the profile directories, copy the example config, create `.env`, and add at minimum one LLM provider key:

```bash
mkdir -p ~/.hermes/{cron,sessions,logs,memories,skills}
cp cli-config.yaml.example ~/.hermes/config.yaml
touch ~/.hermes/.env

# Add at minimum an LLM provider key:
echo 'OPENROUTER_API_KEY=sk-or-v1-your-key' >> ~/.hermes/.env
```

**Run and verify** with `hermes doctor` then `hermes chat -q "Hello"`. If you used the manual clone fallback, run `./hermes` from the checkout or symlink the clone's venv explicitly (`ln -sf "$(pwd)/venv/bin/hermes" ~/.local/bin/hermes`). Run the test suite with `scripts/run_tests.sh`.

## Code Style

- **PEP 8** with practical exceptions (no strict line length enforcement).
- **Comments** only when explaining non-obvious intent, trade-offs, or API quirks.
- **Error handling**: catch specific exceptions; use `logger.warning()`/`logger.error()` with `exc_info=True` for unexpected errors.
- **Cross-platform**: never assume Unix (see below).
- **Profile-safe paths**: never hardcode `~/.hermes` — use `get_hermes_home()` from `hermes_constants` for code paths and `display_hermes_home()` for user-facing messages. (See AGENTS.md for the full multi-instance/profile rules.)

## Cross-Platform Compatibility

Hermes officially supports **Linux, macOS, WSL2, and native Windows (via PowerShell install)**. Native Windows uses Git Bash for shell commands. A few features require POSIX kernel primitives and are gated — e.g. the dashboard's embedded PTY terminal pane (`/chat` tab) is WSL2-only. For Windows-heavy dev, run the Windows-footgun lint (`scripts/check-windows-footguns.py`) before pushing.

Core rules when contributing code:

- **Don't add unguarded `signal.SIGKILL`** — it is not defined on Windows. Either route through `gateway.status.terminate_pid(pid, force=True)` (the centralized primitive: `taskkill /T /F` on Windows, SIGKILL on POSIX), or fall back with `getattr(signal, "SIGKILL", signal.SIGTERM)`.
- **Catch `OSError` alongside `ProcessLookupError`** on `os.kill(pid, 0)` probes — Windows raises `OSError` (WinError 87) for an already-gone PID.
- **Don't force POSIX terminal semantics** — `os.setsid`, `os.killpg`, `os.getpgid`, `os.fork` all raise on Windows; gate with `if sys.platform != "win32":` or `if os.name != "nt":`.
- **Open files with explicit `encoding="utf-8"`** — the Windows default is the system locale (often cp1252), which mojibakes/crashes on non-Latin text.
- **Use `pathlib.Path` / `os.path.join`** — never manually concat with `/`.

The four key patterns the page demonstrates are: (1) `termios`/`fcntl` are Unix-only — catch both `ImportError` and `NotImplementedError` and fall back to a numbered menu; (2) `.env` files may be saved non-UTF-8 — catch `UnicodeDecodeError` and retry with `latin-1`; (3) process management primitives differ — guard `preexec_fn=os.setsid` behind a `platform.system() != "Windows"` check; (4) path separators — use `pathlib.Path` over string concatenation. The process-management guard:

```python
import platform
if platform.system() != "Windows":
    kwargs["preexec_fn"] = os.setsid
```

## Security Considerations

Hermes has terminal access, so security matters. Existing protections span shell-injection hardening, dangerous-command detection, prompt-injection scanning, symlink-bypass prevention, skill scanning, sandboxing, and container hardening:

| Layer | Implementation |
|-------|---------------|
| **Sudo password piping** | Uses `shlex.quote()` to prevent shell injection |
| **Dangerous command detection** | Regex patterns in `tools/approval.py` with user approval flow |
| **Cron prompt injection** | Scanner blocks instruction-override patterns |
| **Write deny list** | Protected paths resolved via `os.path.realpath()` to prevent symlink bypass |
| **Skills guard** | Security scanner for hub-installed skills |
| **Code execution sandbox** | Child process runs with API keys stripped |
| **Container hardening** | Docker: all capabilities dropped, no privilege escalation, PID limits |

**When contributing security-sensitive code:** always use `shlex.quote()` when interpolating user input into shell commands; resolve symlinks with `os.path.realpath()` *before* access-control checks; don't log secrets; catch broad exceptions around tool execution; and test on all platforms if your change touches file paths or processes.

## Pull Request Process

**Branch naming** uses the type prefix that matches the change: `fix/`, `feat/`, `docs/`, `test/`, `refactor/` followed by a short `description`.

**Before submitting:** (1) run tests with `pytest tests/ -v`; (2) test manually — run `hermes` and exercise the code path you changed; (3) check cross-platform impact (macOS and different Linux distros); (4) keep PRs focused — one logical change per PR. The PR description should include *what* changed and *why*, *how to test* it, *what platforms* you tested on, and reference any related issues.

**Commit messages** use [Conventional Commits](https://www.conventionalcommits.org/) — `<type>(<scope>): <description>`:

```
fix(cli): prevent crash in save_config_value when model is a string
feat(gateway): add WhatsApp multi-user session isolation
fix(security): prevent shell injection in sudo password piping
```

Types are `fix`, `feat`, `docs`, `test`, `refactor`, `chore`; scopes are `cli`, `gateway`, `tools`, `skills`, `agent`, `install`, `whatsapp`, `security`.

## Reporting Issues, Community & License

**Report issues** via GitHub Issues, including OS, Python version, Hermes version (`hermes version`), the full error traceback, and steps to reproduce; check existing issues for duplicates first, and report security vulnerabilities privately. **Community** channels are Discord (`discord.gg/NousResearch`), GitHub Discussions (design/architecture proposals), and the Skills Hub (upload and share specialized skills). By contributing, you agree your contributions are licensed under the **MIT License**.

**Source**: `inbox/hermes_agent_docs/developer-guide/contributing.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/contributing
**Last Updated**: 2026-06-19
**Status**: Active
