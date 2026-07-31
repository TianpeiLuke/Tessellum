---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - cli
keywords:
  - clawhub cli skills
  - clawhub install pin update
  - clawhub skill publish
  - clawhub scan clawscan
  - clawhub login whoami token
  - clawhub search explore inspect
  - clawhub lockfile lock.json
  - clawhub skill rename merge transfer
topics:
  - OpenClaw
  - ClawHub CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/cli
access_control_group: ["general"]
---

# OpenClaw — ClawHub CLI: Skill Workflows (`clawhub`)

## Overview

This note is the procedure reference for the `clawhub` CLI's **skill workflows** — the install, discovery, lifecycle, publish, scan, and moderation commands that operate on ClawHub skills — mirroring the skill half of the `clawhub/cli` source page. It covers global install + flags + HTTP proxy + config-file location; the auth commands `login` / `whoami` / `token`; discovery via `star` / `unstar` / `search` / `explore` / `inspect`; the install lifecycle `install` / `uninstall` / `list` / `pin` / `unpin` / `update` and its lockfile; `skill publish` (with ClawHub's reusable GitHub Actions workflow); `scan` / `scan download` (ClawScan); and the moderation/ownership commands `delete` / `undelete` / `hide` / `unhide` / `skill rename` / `skill merge` / `transfer`. The `clawhub package …`, `publisher`, `trusted-publisher`, and install-telemetry commands are the package half and live in the sibling note `oc_clawhub_cli_packages`.

## Install and Verify

The CLI package is `clawhub` and its bin is `clawhub`. Install it globally with npm (`npm i -g clawhub`) or pnpm (`pnpm add -g clawhub`), then verify and authenticate with the three top-level commands:

```bash
npm i -g clawhub
# or
pnpm add -g clawhub
clawhub --help
clawhub login
clawhub whoami
```

## Global Flags, HTTP Proxy, and Config File

The CLI accepts these global flags across commands: `--workdir <dir>` (working directory; default cwd, falling back to the Clawdbot workspace if configured); `--dir <dir>` (install dir under workdir, default `skills`); `--site <url>` (base URL for browser login, default `https://clawhub.ai`); `--registry <url>` (API base URL, default discovered, else `https://clawhub.ai`); and `--no-input` (disable prompts). Environment equivalents are `CLAWHUB_SITE`, `CLAWHUB_REGISTRY`, and `CLAWHUB_WORKDIR` (each with a legacy `CLAWDHUB_*` alias).

For systems behind corporate proxies or restricted networks, the CLI respects the standard HTTP proxy environment variables `HTTPS_PROXY` / `https_proxy`, `HTTP_PROXY` / `http_proxy`, and `NO_PROXY` / `no_proxy`. When any of these is set the CLI routes outbound requests through the specified proxy — `HTTPS_PROXY` for HTTPS requests, `HTTP_PROXY` for plain HTTP — and `NO_PROXY` / `no_proxy` bypasses the proxy for specific hosts or domains. This is required where direct outbound connections are blocked (e.g. Docker containers, a Hetzner VPS with proxy-only internet, corporate firewalls); when no proxy variable is set, behavior is unchanged (direct connections).

The config file stores your API token plus the cached registry URL, at an OS-specific path: macOS `~/Library/Application Support/clawhub/config.json`; Linux/XDG `$XDG_CONFIG_HOME/clawhub/config.json` or `~/.config/clawhub/config.json`; Windows `%APPDATA%\clawhub\config.json`. As a legacy fallback, if `clawhub/config.json` does not exist yet but `clawdhub/config.json` does, the CLI reuses the legacy path. The path can be overridden with `CLAWHUB_CONFIG_PATH` (legacy `CLAWDHUB_CONFIG_PATH`).

## Auth Commands: `login` / `whoami` / `token`

`login` (alias `auth login`) defaults to opening a browser to `<site>/cli/auth` and completing via a loopback callback; headless mode is `clawhub login --token clh_...`; the remote/headless interactive mode `clawhub login --device` prints a code and waits while you authorize it at `<site>/cli/device`. `whoami` verifies the stored token via `/api/v1/whoami`. `token` prints the stored API token to stdout, which is useful for piping a local login token into CI secret-setup commands. The full token lifecycle (creation, per-OS storage, revocation) is documented in the sibling note `oc_clawhub_auth`.

## Discovery: `star` / `unstar` / `search` / `explore` / `inspect`

`star <skill>` / `unstar <skill>` add or remove a skill from your highlights, calling `POST /api/v1/stars/<slug>` and `DELETE /api/v1/stars/<slug>` respectively, with `--yes` to skip confirmation. `search <query...>` calls `/api/v1/search?q=...` and returns the skill slug, owner handle, display name, and relevance score; search favors exact slug/name token matches before download popularity (a standalone slug token such as `map` matches `personal-map` more strongly than the substring inside `amap`), and popularity is only a small ranking prior, not a guarantee of top placement. If a skill should appear but does not, run `clawhub inspect @owner/slug` while logged in to check owner-visible moderation diagnostics before renaming metadata.

`explore` lists the newest skills via `/api/v1/skills?limit=...&sort=createdAt` (sorted by `createdAt` desc), with flags `--limit <n>` (1-200, default 25), `--sort newest|updated|rating|installs|installsAllTime|trending` (default `newest`), and `--json`; its output line is `<slug>  v<version>  <age>  <summary>` (summary truncated to 50 chars). `inspect @owner/slug` fetches skill metadata and version files without installing, with `--version <version>` (default latest), `--tag <tag>` (e.g. `latest`), `--versions` (list version history, first page), `--limit <n>` (max versions, 1-200), `--files` (list files for the selected version), `--file <path>` (fetch raw file content; text files only, 200KB limit), and `--json`.

## Install Lifecycle: `install` / `uninstall` / `list` / `pin` / `unpin` / `update`

`install @owner/slug` resolves the latest version for the named owner and skill, downloads the zip via `/api/v1/download`, and extracts into `<workdir>/<dir>/<slug>`. It refuses to overwrite pinned skills (run `clawhub unpin <skill>` first) and writes two lockfiles: `<workdir>/.clawhub/lock.json` and `<skill>/.clawhub/origin.json` (each with a legacy `.clawdhub` path). `uninstall <skill>` removes `<workdir>/<dir>/<slug>` and deletes the lockfile entry, sends best-effort telemetry while logged in so current install counts can be deactivated, asks for confirmation interactively, and requires `--yes` when non-interactive (`--no-input`). `list` reads `<workdir>/.clawhub/lock.json` (legacy `.clawdhub`) and shows `pinned` next to skills frozen with `clawhub pin`, including the optional reason.

`pin <skill>` marks an installed skill as pinned in the lockfile; `--reason <text>` records why it is frozen. Pinned skills are skipped by `update --all`, rejected by a direct `update <skill>`, and also reject `install --force` so the local bytes cannot be replaced accidentally. `unpin <skill>` removes the lockfile pin so future updates can modify the skill. `update [@owner/slug]` / `update --all` computes a fingerprint from the local files: if the fingerprint matches a known version there is no prompt; if it does not match, the command refuses by default and overwrites only with `--force` (or via a prompt when interactive). Pinned skills are never updated by `--force` — `update <skill>` fails fast for a pinned skill and tells you to run `clawhub unpin <skill>` first, and `update --all` skips pinned slugs and prints a summary of what stayed frozen.

## Publishing: `skill publish`

`skill publish <path>` (legacy alias `publish <path>`) compares the local bundle fingerprint with ClawHub and exits successfully when the content is already published. New skills default to version `1.0.0` and changed skills default to the next patch version; `--version <version>` explicitly selects a version and publishes even when the content matches an existing version. `--dry-run` resolves the publish without uploading, and `--json` prints a machine-readable result. `--owner <handle>` publishes under an org/user publisher handle when the actor has publisher access, and `--migrate-owner` moves an existing skill to `--owner` while publishing a new version (requiring admin/owner access on both publishers). Owner and review behavior is explained in `docs/publishing.md`. Publishing a skill means it is released under `MIT-0` on ClawHub; published skills are free to use, modify, and redistribute without attribution, and ClawHub does not support paid skills or per-skill pricing.

```bash
clawhub skill publish ./my-skill --dry-run
clawhub skill publish ./my-skill
clawhub skill publish ./my-skill --version 2.0.0
```

ClawHub's reusable [`skill-publish.yml`](https://github.com/openclaw/clawhub/blob/main/.github/workflows/skill-publish.yml) GitHub Actions workflow calls `skill publish` for one `skill_path`, or for each immediate skill folder under `root` (default `skills`); it skips unchanged skills and uses the same automatic patch-version behavior. Set `dry_run: true` to preview without a token, while real publishes require the `clawhub_token` secret. Note that V1 skill publishing uses `clawhub_token` — GitHub OIDC trusted publishing is package-only for now.

## Security Scanning: `scan` / `scan download`

`scan --slug <slug>` requires `clawhub login`, runs ClawHub ClawScan through `POST /api/v1/skills/-/scan`, then polls until the scan is terminal; scans are asynchronous and may take time, and while queued the terminal spinner shows the current prioritized scan position and how many scans are ahead. Published scans require ownership or publisher-management access (moderators/admins use the same backend through `clawhub-admin`). `--update` is valid only with `--slug` and writes successful published scan results back to the selected version; `--output <file.zip>` downloads the full report archive containing `manifest.json`, `clawscan.json`, `skillspector.json`, `static-analysis.json`, `virustotal.json`, and `README.md`; `--json` prints the full poll response for automation. Local path scans are no longer supported — upload a new version, then use `scan download` to retrieve the stored scan results for that submitted version.

```bash
clawhub scan --slug gifgrep
clawhub scan --slug gifgrep --version 1.2.3
clawhub scan --slug gifgrep --update --output report.zip
```

`scan download <name>` also requires `clawhub login` and downloads the stored scan report ZIP for a submitted skill or plugin version, including versions that were blocked or hidden by ClawHub security checks. Skill downloads use the skill slug and default to `--kind skill`; plugin downloads use the package name and require `--kind plugin`. `--version` is required so authors inspect the exact submitted version that ClawHub blocked, and `--output <file.zip>` chooses the destination path. ClawHub ships an official reusable GitHub Actions workflow at [`/.github/workflows/skill-publish.yml`](https://github.com/openclaw/clawhub/blob/6f28659e7bfb5ae21e1bcc2d6896fea9c0a7f698/.github/workflows/skill-publish.yml) for skill repos and catalog repos.

## Moderation and Ownership: `delete` / `undelete` / `hide` / `unhide` / `rename` / `merge` / `transfer`

`delete <skill>` without `--version` soft-deletes a skill (owner, moderator, or admin) via `DELETE /api/v1/skills/{slug}`; owner-initiated soft deletes reserve the slug for 30 days and the command prints the expiry time. With `--version <version>` it permanently deletes one owned non-latest version through a fail-closed, version-specific route — deleted versions cannot be restored or republished, so publish a replacement before deleting the current latest version, and platform staff do not bypass ownership for this version-only flow. `--reason <text>` (alias `--note <text>`) records a moderation note on a whole-skill soft-delete and audit log, and `--yes` skips confirmation. `undelete <skill>` restores a hidden skill (owner, moderator, or admin) via `POST /api/v1/skills/{slug}/undelete`; there is no version undelete (permanently deleted versions cannot be restored), and it accepts the same `--reason`/`--note`/`--yes` flags. `hide <skill>` is an alias for `delete` and `unhide <skill>` is an alias for `undelete` (owner, moderator, or admin in each case).

`skill rename <skill> <new-name>` renames an owned skill and keeps the previous slug as a redirect alias (via `POST /api/v1/skills/{slug}/rename`, `--yes` to skip confirmation). `skill merge <source> <target>` merges one owned skill into another owned skill — the source slug stops listing publicly and becomes a redirect alias to the target (via `POST /api/v1/skills/{sourceSlug}/merge`, `--yes` to skip confirmation). `transfer` is the ownership-transfer workflow: transfers to user handles create a pending request that the recipient accepts, while transfers to org/publisher handles apply immediately only when the actor has admin access to both the current owner and destination publisher. Its subcommands are `transfer request <skill> <handle> [--message "..."] [--yes]`, `transfer list [--outgoing]`, `transfer accept <skill> [--yes]`, `transfer reject <skill> [--yes]`, and `transfer cancel <skill> [--yes]`; the backing endpoints are `POST /api/v1/skills/{slug}/transfer`, `.../transfer/accept`, `.../transfer/reject`, `.../transfer/cancel`, plus `GET /api/v1/transfers/incoming` and `GET /api/v1/transfers/outgoing`.

**Source**: OpenClaw documentation — `clawhub/cli` (mirror `inbox/openclaw_docs/clawhub/cli.md`), skill-CLI half
**Last Updated**: 2026-06-22
**Status**: Active
