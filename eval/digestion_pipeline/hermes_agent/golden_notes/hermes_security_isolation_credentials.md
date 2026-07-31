---
tags:
  - resource
  - documentation
  - hermes_agent
  - security
  - isolation
keywords:
  - container isolation
  - docker security flags
  - environment variable passthrough
  - mcp credential filtering
  - ssrf protection
  - supply-chain advisory
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

# Hermes Agent — Security: Isolation & Credential Containment

## Overview

This is the **isolation + credential-containment** half of the Hermes Agent defense-in-depth security model — the boundary governing *how execution is sandboxed* and *how credentials stay inside it*, vs. the approval/authorization boundary governing *who and what may run* (see [hermes_security_command_approval](hermes_security_command_approval.md)). It covers Docker container hardening, the six-backend security comparison, environment-variable passthrough and its per-sandbox filter matrix, credential-file mounting, MCP credential filtering/redaction, the website blocklist and SSRF protection, the production gateway deployment checklist plus SSH network isolation, and the supply-chain advisory scanner with lazy-install of optional deps. The container is the security boundary — a container backend lets Hermes skip the dangerous-command check entirely, since destructive commands inside a container cannot harm the host.

## Container Isolation

The `docker` terminal backend applies strict hardening to every container.

### Docker Security Flags

Every container runs with these flags (`tools/environments/docker.py`):

```python
_BASE_SECURITY_ARGS = [
    "--cap-drop", "ALL",                          # Drop ALL Linux capabilities
    "--cap-add", "DAC_OVERRIDE",                  # Root can write to bind-mounted dirs
    "--cap-add", "CHOWN",                         # Package managers need file ownership
    "--cap-add", "FOWNER",                        # Package managers need file ownership
    "--security-opt", "no-new-privileges",         # Block privilege escalation
    "--pids-limit", "256",                         # Limit process count
    "--tmpfs", "/tmp:rw,nosuid,size=512m",         # Size-limited /tmp
    "--tmpfs", "/var/tmp:rw,noexec,nosuid,size=256m",  # No-exec /var/tmp
]
```

`SETUID`/`SETGID` are **not** in the base list — added only when the container starts as root and an init/entrypoint must drop privileges (the s6 path), skipped when it already runs as a non-root `--user`. The `/run` tmpfs is split out and mounted per-image (`noexec` by default, `exec` only for s6-overlay images that exec from `/run`).

### Resource Limits

Configurable in `~/.hermes/config.yaml`:

```yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  docker_forward_env: []  # Explicit allowlist only; empty keeps secrets out of the container
  container_cpu: 1        # CPU cores
  container_memory: 5120  # MB (default 5GB)
  container_disk: 51200   # MB (default 50GB, requires overlay2 on XFS)
  container_persistent: true  # Persist filesystem across sessions
```

### Filesystem Persistence

- **Persistent** (`container_persistent: true`): bind-mounts `/workspace` and `/root` from `~/.hermes/sandboxes/docker/<task_id>/`.
- **Ephemeral** (`false`): tmpfs workspace, lost on cleanup.

For production gateways the source recommends the `docker`, `modal`, or `daytona` backend to isolate agent commands from the host, eliminating dangerous-command approval. Adding names to `terminal.docker_forward_env` injects those vars into the container (useful for task credentials like `GITHUB_TOKEN`), but code in the container can then read and exfiltrate them. Deep Docker/image-build detail is in [hermes_docker](hermes_docker_run_modes.md); full `terminal.*` keys in [hermes_terminal_backends](hermes_terminal_backends.md).

## Terminal Backend Security Comparison

The six backends differ in isolation and whether the dangerous-command check runs (a container backend skips it — the container is the boundary):

| Backend | Isolation | Dangerous Cmd Check | Best For |
|---------|-----------|-------------------|----------|
| **local** | None — runs on host | Yes | Development, trusted users |
| **ssh** | Remote machine | Yes | Running on a separate server |
| **docker** | Container | Skipped (container is boundary) | Production gateway |
| **singularity** | Container | Skipped | HPC environments |
| **modal** | Cloud sandbox | Skipped | Scalable cloud isolation |
| **daytona** | Cloud sandbox | Skipped | Persistent cloud workspaces |

The six-backend model is owned by [hermes_terminal_backends](hermes_terminal_backends.md) (SP02).

## Environment Variable Passthrough

Both `execute_code` and `terminal` strip sensitive env vars from child processes to prevent credential exfiltration by LLM-generated code; skills declaring `required_environment_variables` legitimately need them. Two mechanisms allow specific vars through the sandbox filters.

**1. Skill-scoped passthrough (automatic).** When a skill is loaded (via `skill_view` or `/skill`) and declares `required_environment_variables` in its `SKILL.md` frontmatter (e.g. `TENOR_API_KEY`), any of those vars actually set are auto-registered as passthrough; missing vars (still setup-needed) are **not** registered. After loading, the var reaches `execute_code`, `terminal` (local), **and remote backends (Docker, Modal)**. Since v0.5.1 Docker's `forward_env` is merged with skill passthrough, so skill-declared env vars are forwarded into Docker/Modal without adding them to `docker_forward_env`.

**2. Config-based passthrough (manual).** For vars not declared by a skill, add them to `terminal.env_passthrough`:

```yaml
terminal:
  env_passthrough:
    - MY_CUSTOM_KEY
    - ANOTHER_TOKEN
```

### Credential File Passthrough (OAuth tokens, etc.)

Some skills need **files** (not just env vars) — e.g. Google Workspace stores OAuth tokens as `google_token.json` under the active profile's `HERMES_HOME`. Skills declare these via `required_credential_files`; when loaded, Hermes checks they exist and registers them for mounting: **Docker** read-only bind mounts (`-v host:container:ro`); **Modal** mounted at creation + synced before each command (handles mid-session OAuth); **Local** no action. They can also be listed manually under `terminal.credential_files` (paths relative to `~/.hermes/`, mounted to `/root/.hermes/`); this list is read by `tools/credential_files.py` (the credential-files module, not the core terminal backend, so it is not in the bundled `DEFAULT_CONFIG` snapshot).

### What Each Sandbox Filters

| Sandbox | Default Filter | Passthrough Override |
|---------|---------------|---------------------|
| **execute_code** | Blocks vars with `KEY`/`TOKEN`/`SECRET`/`PASSWORD`/`CREDENTIAL`/`PASSWD`/`AUTH` in name; only safe-prefix vars allowed | Passthrough vars bypass both checks |
| **terminal** (local) | Blocks Hermes infra vars (provider keys, gateway tokens, tool API keys) | Passthrough vars bypass the blocklist |
| **terminal** (Docker) | No host env vars by default | Passthrough + `docker_forward_env` forwarded via `-e` |
| **terminal** (Modal) | No host env/files by default | Credential files mounted; env passthrough via sync |
| **MCP** | Blocks all but safe system vars + configured `env` | Not affected by passthrough (use MCP `env` config) |

### Security Considerations

- Passthrough only affects vars you or your skills explicitly declare — the default posture is unchanged for arbitrary code.
- Credential files are mounted **read-only** into Docker; Skills Guard scans skill content for suspicious env-access before install.
- Missing/unset vars are never registered (cannot leak what does not exist).
- Hermes infrastructure secrets (provider API keys, gateway tokens) must never be added to `env_passthrough` — they have dedicated mechanisms.

## MCP Credential Handling

MCP (Model Context Protocol) server subprocesses receive a **filtered environment**. Only `PATH, HOME, USER, LANG, LC_ALL, TERM, SHELL, TMPDIR` (plus `XDG_*` vars) are passed from the host to MCP stdio subprocesses; all other env vars (API keys, tokens, secrets) are **stripped**. Variables in the MCP server's `env` config pass through (e.g. `GITHUB_PERSONAL_ACCESS_TOKEN` under `mcp_servers.github.env` — only that key reaches the subprocess). The broader MCP feature page is owned by SP09 ([hermes_mcp](hermes_mcp_concept_config.md)).

### Credential Redaction

MCP-tool error messages are sanitized before reaching the LLM — replaced with `[REDACTED]`: GitHub PATs (`ghp_...`), OpenAI-style keys (`sk-...`), Bearer tokens, and `token=`/`key=`/`API_KEY=`/`password=`/`secret=` parameters.

### Website Access Policy

Restrict which websites the agent reaches via its web/browser tools — blocking internal services, admin panels, or sensitive URLs. `security.website_blocklist` takes `enabled: true`, a `domains` list (globs like `*.internal.company.com`), and `shared_files` (e.g. `/etc/hermes/blocked-sites.txt`). A blocked URL returns a policy error; enforced across `web_search`, `web_extract`, `browser_navigate`, and all URL-capable tools. Config owned by SP02 ([hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md)).

### SSRF Protection

All URL-capable tools (web search/extract, vision, browser) validate URLs before fetch to prevent Server-Side Request Forgery (SSRF). Blocked:

- **Private networks** (RFC 1918): `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
- **Loopback**: `127.0.0.0/8`, `::1`; **Link-local**: `169.254.0.0/16` (incl. cloud metadata `169.254.169.254`)
- **CGNAT / shared** (RFC 6598): `100.64.0.0/10` (Tailscale, WireGuard VPNs)
- **Cloud metadata hostnames**: `metadata.google.internal`, `metadata.goog`; reserved/multicast/unspecified addresses

SSRF protection is always active for internet-facing use; DNS failures are blocked (fail-closed) and redirect chains re-validated at each hop. A global opt-out exists for setups that legitimately need private/internal URL access (home networks resolving `home.arpa`, LAN-only Ollama endpoints, internal wikis, cloud-metadata debugging):

```yaml
security:
  allow_private_urls: true   # default: false
```

When on, web/browser/vision fetches and gateway media downloads no longer reject those ranges. **This is a deliberate trust boundary** — enable only where the agent running prompt-injected URLs against the local network is acceptable; public gateways leave it off. The host-substring guard (blocking lookalike Unicode domain tricks even when the IP is public) stays on.

## Best Practices for Production Deployment

### Gateway Deployment Checklist

1. **Explicit allowlists** — never `GATEWAY_ALLOW_ALL_USERS=true` in production.
2. **Container backend** — `terminal.backend: docker`.
3. **Resource limits** — appropriate CPU/memory/disk caps.
4. **Secrets securely** — API keys in `~/.hermes/.env` with proper permissions.
5. **DM pairing** — codes over hardcoded user IDs.
6. **Review allowlist** — periodically audit `command_allowlist`.
7. **Set `terminal.cwd`** — keep the agent out of sensitive directories.
8. **Non-root** — never run the gateway as root.
9. **Monitor logs** — `~/.hermes/logs/` for unauthorized access.
10. **Keep updated** — `hermes update` for security patches.

### Securing API Keys

Set permissions on `.env` (`chmod 600 ~/.hermes/.env`), keep separate keys per service, and never commit `.env` to version control.

### Network Isolation

For maximum security, run the gateway on a separate machine/VM with `terminal.backend: ssh`, then provide host details in `~/.hermes/.env`:

```bash
# ~/.hermes/.env
TERMINAL_SSH_HOST=agent-worker.local
TERMINAL_SSH_USER=hermes
TERMINAL_SSH_KEY=~/.ssh/hermes_agent_key
```

SSH details live in `.env` (not `config.yaml`) so they are not checked in or shared with profile exports, keeping messaging connections separate from command execution. The `ssh` backend keys are owned by SP02 ([hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md)).

## Supply-chain advisory checking

A built-in scanner (`hermes_cli/security_advisories.py`) flags packages in the active venv matching a curated catalog of known-compromised versions (supply-chain worms like the May 2026 `mistralai 2.4.6` poisoning). It runs at CLI startup (one-line warning pointing to `hermes doctor`), under `hermes doctor` (every active advisory + 2-4 step remediation), and at gateway startup (logged to `gateway.log`; first message gets an operator banner). Each advisory has a stable id; once acted on it is dismissed with `hermes doctor --ack <advisory-id>` (persisted to `config.security.acked_advisories`). Old advisories are intentionally **not** removed — keeping them warns fresh installs about poisoned versions still cached in a private mirror. The check is stdlib-only (one `importlib.metadata.version()` lookup per advisory), safe on every startup.

### Lazy install of optional dependencies

Many features (Mistral TTS, ElevenLabs, Honcho memory, Bedrock, Slack, Matrix, …) depend on packages not every user needs. Hermes installs these **lazily** on first use rather than eagerly under `hermes-agent[all]` (`tools/lazy_deps.py`), isolating each backend so one poisoned/unavailable transitive dep cannot break unrelated features and avoiding unused packages. A backend calls `ensure("feature.name")` on first import; if deps are missing, `ensure` checks `security.allow_lazy_installs` (default `true`) and runs a venv-scoped `pip install` of the allowlisted specs. If it fails or lazy installs are disabled, it raises `FeatureUnavailable` with the pip stderr and a pointer at `hermes tools`. Guarantees:

| Guarantee | What it means |
|---|---|
| Venv-scoped only | Installs target `sys.executable` in the active venv — never the system Python |
| PyPI by name only | Specs accept `"package>=1.0,<2"` syntax. No `--index-url`, `git+https://`, or file: paths — a malicious `config.yaml` cannot redirect the install |
| Allowlist | Only specs in the in-tree `LAZY_DEPS` map install via this path; a typo in a feature name does NOT get install-anything semantics |
| Opt-out | `security.allow_lazy_installs: false` disables runtime installs (restricted/strict postures) |
| No silent retries | Failures surface as `FeatureUnavailable` — no caching of bad state, no retry storms |

When disabled, backends needing optional deps tell the user to install manually or pick another backend via `hermes tools`.

**Source**: `inbox/hermes_agent_docs/user-guide/security.md` · https://hermes-agent.nousresearch.com/docs/user-guide/security
**Last Updated**: 2026-06-19
**Status**: Active
