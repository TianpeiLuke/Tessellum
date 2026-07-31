---
tags:
  - resource
  - documentation
  - hermes_agent
  - security
  - command_approval
keywords:
  - dangerous command approval
  - yolo mode hardline blocklist
  - approval modes manual smart off
  - gateway user authorization
  - dm pairing system
  - tirith pre-exec scanning
topics:
  - Hermes Agent
  - Security
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/security
access_control_group: ["general"]
---

# Hermes Agent — Command Approval & User Authorization

## Overview

This is the "who and what may run a command" half of Hermes Agent's defense-in-depth security model. It documents the seven-layer security overview, the dangerous-command approval engine (three modes, YOLO bypass, the always-on hardline blocklist, approval-trigger patterns, and the CLI/messaging approval flows), the messaging-gateway user-authorization check order and DM pairing system, the Tirith content-level pre-exec scanner, and the context-file prompt-injection scanner. The companion isolation/credential-containment boundary (container sandboxing, env-var filtering, MCP credential handling, SSRF, production checklist) lives in the sibling note [hermes_security_isolation_credentials](hermes_security_isolation_credentials.md). Config blocks named here (`approvals:`, `security:`, `command_allowlist`) are defined in the SP02 settings reference.

## Overview (Seven Security Layers)

The security model has seven layers:

1. **User authorization** — who can talk to the agent (allowlists, DM pairing)
2. **Dangerous command approval** — human-in-the-loop for destructive operations
3. **Container isolation** — Docker/Singularity/Modal sandboxing with hardened settings
4. **MCP credential filtering** — environment variable isolation for MCP subprocesses
5. **Context file scanning** — prompt injection detection in project files
6. **Cross-session isolation** — sessions cannot access each other's data or state; cron job storage paths are hardened against path traversal attacks
7. **Input sanitization** — working directory parameters in terminal tool backends are validated against an allowlist to prevent shell injection

Layers 3–4 (container isolation, MCP credential filtering) are documented in detail in [hermes_security_isolation_credentials](hermes_security_isolation_credentials.md); this note covers layers 1, 2, 5, plus Tirith.

## Dangerous Command Approval

Before executing any command, Hermes checks it against a curated list of dangerous patterns. If a match is found, the user must explicitly approve it.

### Approval Modes

The approval system supports three modes, configured via `approvals.mode` in `~/.hermes/config.yaml`:

```yaml
approvals:
  mode: manual                    # manual | smart | off
  timeout: 60                     # seconds to wait for user response (default: 60)
  cron_mode: deny                 # deny | approve — what cron jobs do when they hit a dangerous command
  mcp_reload_confirm: true        # /reload-mcp asks before invalidating the MCP tool cache
  destructive_slash_confirm: true # /clear, /new, /reset, /undo prompt before discarding state
```

The mode behaviors: **manual** (default) always prompts on dangerous commands; **smart** uses an auxiliary LLM to assess risk (low-risk commands like `python -c "print('hello')"` auto-approved, genuinely dangerous commands auto-denied, uncertain cases escalate to a manual prompt); **off** disables all approval checks — equivalent to `--yolo`, all commands execute without prompts (use only in trusted environments such as CI/CD or containers). The full `approvals.*` key reference (`cron_mode`, `mcp_reload_confirm`, `destructive_slash_confirm`) is defined in the SP02 config note. Cron headless behavior (`cron_mode: deny|approve`) is detailed in the SP06 cron note.

### YOLO Mode

YOLO mode bypasses **all** dangerous command approval prompts for the current session. It can be activated three ways: the CLI flag (`hermes --yolo` or `hermes chat --yolo`), the `/yolo` slash command (a toggle that flips on/off each use — each use prints `⚡ YOLO mode ON — all commands auto-approved. Use with caution.` or `⚠ YOLO mode OFF — dangerous commands will require approval.`), and the `HERMES_YOLO_MODE=1` environment variable (which the slash/flag set internally and which is checked before every command execution).

When YOLO is active, Hermes shows two persistent visual reminders: a red banner line at session start (`⚠ YOLO mode — all approval prompts bypassed`, hidden when off) and a `⚠ YOLO` fragment in the status bar across all width tiers, updated live as you toggle. YOLO disables all dangerous-command safety checks for the session **except** the hardline blocklist (below). For destructive session slash commands (`/clear`, `/new`/`/reset`, `/undo`, `/quit --delete`), the CLI also prompts for confirmation before running them.

### Hardline Blocklist (Always-On Floor)

Some commands are so catastrophic — irreversible filesystem wipes, fork bombs, direct block-device writes — that Hermes refuses to run them **regardless** of `--yolo`/`/yolo`, `approvals.mode: off`, cron headless `approve` mode, or a user explicitly clicking "allow always". The blocklist is the floor below `--yolo`: it trips **before** the approval layer even sees the command, with no override flag (kept in sync with `tools/approval.py::UNRECOVERABLE_BLOCKLIST`). Patterns currently covered (not exhaustive):

| Pattern | Why it's hardline |
|---|---|
| `rm -rf /` and obvious variants | Wipes the filesystem root |
| `rm -rf --no-preserve-root /` | The explicit "yes I mean root" variant |
| `:(){ :\|:& };:` (bash fork bomb) | Pegs the host until reboot |
| `mkfs.*` on a mounted root device | Formats the live system |
| `dd if=/dev/zero of=/dev/sd*` | Zeroes a physical disk |
| Piping untrusted URLs to `sh` at the rootfs top level | Remote-code-execution attack vector too broad to approve |

If you hit the blocklist, the tool call returns an explanatory error to the agent and nothing runs. A legitimate workflow that needs one of these commands must run it outside the agent.

### Approval Timeout & What Triggers Approval

When a dangerous command prompt appears, the user has a configurable amount of time to respond (`approvals.timeout`, default 60 seconds). If no response is given within the timeout, the command is **denied** by default (fail-closed).

The following patterns trigger approval prompts (defined in `tools/approval.py`): recursive deletes (`rm -r`/`rm --recursive`, `rm ... /`), unsafe permission changes (`chmod 777/666`/`o+w`/`a+w`, recursive variants, `chown -R root`), filesystem/device writes (`mkfs`, `dd if=`, `> /dev/sd`), destructive SQL (`DROP TABLE/DATABASE`, `DELETE FROM` without WHERE, `TRUNCATE TABLE`), system-config overwrites (`> /etc/`, `cp`/`mv`/`install` to `/etc/`, `sed -i` on `/etc/`), service/process control (`systemctl stop/restart/disable/mask`, `kill -9 -1`, `pkill -9`, fork-bomb patterns), shell/script execution via flag (`bash -c`/`sh -c`/`zsh -c`/`ksh -c` incl. combined `-lc`, `python -e`/`perl -e`/`ruby -e`/`node -c`), pipe-to-shell (`curl ... | sh`, `wget ... | sh`, `bash <(curl ...)`), sensitive-file overwrites via `tee`/redirection to `/etc/`, `~/.ssh/`, `~/.hermes/.env`, destructive find/xargs (`xargs rm`, `find -exec rm`, `find -delete`), self-termination prevention (`pkill`/`killall hermes/gateway`), and `gateway run` with `&`/`disown`/`nohup`/`setsid`.

**Container bypass**: When running in `docker`, `singularity`, `modal`, or `daytona` backends, dangerous command checks are **skipped** because the container itself is the security boundary — see the backend security comparison in [hermes_security_isolation_credentials](hermes_security_isolation_credentials.md).

### Approval Flow (CLI)

In the interactive CLI, dangerous commands show an inline approval prompt:

```
  ⚠️  DANGEROUS COMMAND: recursive delete
      rm -rf /tmp/old-project

      [o]nce  |  [s]ession  |  [a]lways  |  [d]eny

      Choice [o/s/a/D]:
```

The four options: **once** (allow this single execution), **session** (allow this pattern for the rest of the session), **always** (add to the permanent allowlist saved to `config.yaml`), and **deny** (default — block the command).

### Approval Flow (Gateway/Messaging)

On messaging platforms, the agent sends the dangerous command details to the chat and waits for the user to reply: **yes**, **y**, **approve**, **ok**, or **go** to approve; **no**, **n**, **deny**, or **cancel** to deny. The `HERMES_EXEC_ASK=1` environment variable is automatically set when running the gateway.

### Permanent Allowlist

Commands approved with "always" are saved to `~/.hermes/config.yaml`, loaded at startup, and silently approved in all future sessions:

```yaml
# Permanently allowed dangerous command patterns
command_allowlist:
  - rm
  - systemctl
```

Use `hermes config edit` to review or remove patterns from your permanent allowlist.

## User Authorization (Gateway)

When running the messaging gateway, Hermes controls who can interact with the bot through a layered authorization system.

### Authorization Check Order

The `_is_user_authorized()` method checks in this order:

1. **Per-platform allow-all flag** (e.g., `DISCORD_ALLOW_ALL_USERS=true`)
2. **DM pairing approved list** (users approved via pairing codes)
3. **Platform-specific allowlists** (e.g., `TELEGRAM_ALLOWED_USERS=12345,67890`)
4. **Global allowlist** (`GATEWAY_ALLOWED_USERS=12345,67890`)
5. **Global allow-all** (`GATEWAY_ALLOW_ALL_USERS=true`)
6. **Default: deny**

### Platform Allowlists

Allowed user IDs are set as comma-separated values in `~/.hermes/.env`: `TELEGRAM_ALLOWED_USERS`, `DISCORD_ALLOWED_USERS`, `WHATSAPP_ALLOWED_USERS`, `SLACK_ALLOWED_USERS` (per-platform), `GATEWAY_ALLOWED_USERS` (cross-platform), `DISCORD_ALLOW_ALL_USERS=true` (per-platform allow-all, use with caution), and `GATEWAY_ALLOW_ALL_USERS=true` (global allow-all, use with extreme caution). If **no allowlists are configured** and `GATEWAY_ALLOW_ALL_USERS` is unset, **all users are denied** and the gateway logs a startup warning. Per-platform allowlist setup detail is owned by the SP11-13 messaging notes.

### DM Pairing System

For more flexible authorization, Hermes includes a code-based pairing system. Instead of requiring user IDs upfront, an unknown user who DMs the bot receives a one-time 8-character pairing code; the bot owner runs `hermes pairing approve <platform> <code>` on the CLI, and the user is permanently approved for that platform. The `unauthorized_dm_behavior` config key controls handling: `pair` (default — reply with a pairing code) or `ignore` (silently drop), with platform sections overriding the global default (e.g. keep pairing on Telegram while keeping WhatsApp silent).

**Security features** (based on OWASP + NIST SP 800-63-4 guidance): an 8-char code from a 32-char unambiguous alphabet (no 0/O/1/I); cryptographic randomness (`secrets.choice()`); 1-hour code TTL; rate limiting of 1 request per user per 10 minutes; max 3 pending codes per platform; a 1-hour lockout after 5 failed approval attempts; `chmod 0600` on all pairing data files; and codes are never logged to stdout.

```bash
# List pending and approved users
hermes pairing list
# Approve a pairing code
hermes pairing approve telegram ABC12DEF
# Revoke a user's access
hermes pairing revoke telegram 123456789
# Clear all pending codes
hermes pairing clear-pending
```

**Storage:** Pairing data is stored in `~/.hermes/pairing/` with per-platform JSON files: `{platform}-pending.json` (pending requests), `{platform}-approved.json` (approved users), and `_rate_limits.json` (rate limit and lockout tracking).

## Tirith Pre-Exec Security Scanning

Hermes integrates [tirith](https://github.com/sheeki03/tirith) for content-level command scanning before execution, detecting threats that pattern matching alone misses: homograph URL spoofing (internationalized domain attacks), pipe-to-interpreter patterns (`curl | bash`, `wget | sh`), and terminal injection attacks. Tirith auto-installs from GitHub releases on first use with SHA-256 checksum verification (and cosign provenance verification if cosign is available).

```yaml
# In ~/.hermes/config.yaml
security:
  tirith_enabled: true       # Enable/disable tirith scanning (default: true)
  tirith_path: "tirith"      # Path to tirith binary (default: PATH lookup)
  tirith_timeout: 5          # Subprocess timeout in seconds
  tirith_fail_open: true     # Allow execution when tirith is unavailable (default: true)
```

When `tirith_fail_open` is `true` (default), commands proceed if tirith is not installed or times out; set to `false` in high-security environments to block commands when tirith is unavailable. Tirith ships prebuilt binaries for Linux (x86_64/aarch64) and macOS (x86_64/arm64); on platforms with no prebuilt binary (Windows, etc.) it is silently skipped (pattern-matching guards still run; use WSL to enable it on Windows). Tirith's verdict integrates with the approval flow: safe commands pass through, while both suspicious and blocked commands trigger user approval with the full tirith findings (severity, title, description, safer alternatives) — the default choice is deny to keep unattended scenarios secure.

## Context File Injection Protection

Context files (AGENTS.md, .cursorrules, SOUL.md) are scanned for prompt injection before being included in the system prompt. The scanner checks for: instructions to ignore/disregard prior instructions; hidden HTML comments with suspicious keywords; attempts to read secrets (`.env`, `credentials`, `.netrc`); credential exfiltration via `curl`; and invisible Unicode characters (zero-width spaces, bidirectional overrides). Blocked files show a warning:

```
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

**Source**: `inbox/hermes_agent_docs/user-guide/security.md` · https://hermes-agent.nousresearch.com/docs/user-guide/security
**Last Updated**: 2026-06-19
**Status**: Active
