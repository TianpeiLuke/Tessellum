---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - skills
keywords:
  - openclaw skills config schema
  - skills.load skills.install skills.entries
  - security.installPolicy operator install policy
  - skills.workshop limits approvalPolicy
  - allowBundled bundled skill allowlist
  - agent allowlists agents.defaults.skills
  - symlinked skill roots allowSymlinkTargets
  - sandboxed skills env vars docker
  - skill loading order precedence
topics:
  - OpenClaw
  - Skills Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/skills-config
access_control_group: ["general"]
---

# OpenClaw — The `skills.*` Config Schema Reference

## Overview

This note is the procedure reference for OpenClaw's skill configuration tree, mirroring the `tools/skills-config` source page. Most skill configuration lives under `skills` in `~/.openclaw/openclaw.json`, while agent-specific visibility lives under `agents.defaults.skills` and `agents.list[].skills`. It walks every config surface the page documents in order: `skills.load` (discovery/watching), `skills.install` (installer preferences), `security.installPolicy` (the operator trusted-command allow/block protocol), `skills.allowBundled`, `skills.entries` (per-skill enablement/secrets/env), agent allowlists, `skills.workshop` (proposal limits), symlinked-skill-root containment, passing secrets into a sandbox, and the loading-order reminder. Every field name, default, and JSON5 block is copied verbatim from the mirror; this note documents config (link-outs handle the runtime lifecycle and SKILL.md authoring).

## Top-Level Layout

Most skills configuration lives under `skills` in `~/.openclaw/openclaw.json`. Agent-specific visibility lives under `agents.defaults.skills` and `agents.list[].skills`. A representative top-level block:

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills"],
      allowSymlinkTargets: ["~/Projects/manager/skills"],
      watch: true,
      watchDebounceMs: 250,
    },
    install: {
      preferBrew: true,
      nodeManager: "npm",
      allowUploadedArchives: false,
    },
    workshop: {
      autonomous: { enabled: false },
      allowSymlinkTargetWrites: false,
      approvalPolicy: "pending",
      maxPending: 50,
      maxSkillBytes: 40000,
    },
    entries: {
      "image-lab": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" },
        env: { GEMINI_API_KEY: "GEMINI_KEY_HERE" },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

Note (source): for built-in image generation, use `agents.defaults.imageGenerationModel` plus the core `image_generate` tool instead of `skills.entries`. Skill entries are for custom or third-party skill workflows only.

## Loading (`skills.load`)

- `skills.load.extraDirs` (`string[]`) — additional skill directories to scan, at the **lowest** precedence (after bundled and plugin skills). Paths are expanded with `~` support.
- `skills.load.allowSymlinkTargets` (`string[]`) — trusted real target directories that symlinked skill folders may resolve into, even when the symlink lives outside the configured root. Use this for intentional sibling-repo layouts such as `<workspace>/skills/manager -> ~/Projects/manager/skills`. Keep this list narrow — do not point at broad roots like `~` or `~/Projects`.
- `skills.load.watch` (`boolean`, default `true`) — watch skill folders and refresh the skills snapshot when `SKILL.md` files change. Covers nested files under grouped skill roots.
- `skills.load.watchDebounceMs` (`number`, default `250`) — debounce window for skill watcher events in milliseconds.

## Install (`skills.install`)

- `skills.install.preferBrew` (`boolean`, default `true`) — prefer Homebrew installers when `brew` is available.
- `skills.install.nodeManager` (`"npm" | "pnpm" | "yarn" | "bun"`, default `"npm"`) — Node package manager preference for skill installs. This only affects skill installs — the Gateway runtime should still use Node (Bun is not recommended for WhatsApp/Telegram). Use `openclaw setup --node-manager` for npm, pnpm, or bun; set `"yarn"` manually for Yarn-backed skill installs.
- `skills.install.allowUploadedArchives` (`boolean`, default `false`) — allow trusted `operator.admin` Gateway clients to install private zip archives staged through `skills.upload.*`. Normal ClawHub installs do not need this setting.

## Operator Install Policy (`security.installPolicy`)

Use `security.installPolicy` when operators need a trusted local command to approve or block skill and plugin installs with host-specific policy. The policy runs after OpenClaw has staged source material and before the install or update continues. It applies to ClawHub skills, uploaded skills, Git/local skills, skill dependency installers, and plugin install/update sources.

```json5
{
  security: {
    installPolicy: {
      enabled: true,
      // Omit targets to cover every supported target.
      targets: ["skill", "plugin"],
      exec: {
        source: "exec",
        command: "/usr/local/bin/openclaw-install-policy",
        args: ["--json"],
        timeoutMs: 10000,
        noOutputTimeoutMs: 10000,
        maxOutputBytes: 1048576,
        passEnv: ["OPENCLAW_STATE_DIR", "PATH"],
        env: { POLICY_MODE: "strict" },
        trustedDirs: ["/usr/local/bin"],
      },
    },
  },
}
```

- `security.installPolicy.enabled` (`boolean`, default `false`) — enables operator-owned install policy. When enabled without a valid `exec` command, installs **fail closed**.
- `security.installPolicy.targets` (`("skill" | "plugin")[]`) — optional target filter. When omitted, policy applies to **every** supported target so new installs do not unexpectedly fail open.
- `security.installPolicy.exec.command` (`string`) — absolute path to the trusted policy executable. OpenClaw runs it **without a shell** and validates the path before use.
- `security.installPolicy.exec.args` (`string[]`) — static arguments passed after `command`.
- `security.installPolicy.exec.timeoutMs` (`number`, default `10000`) — maximum wall-clock runtime for one policy decision.
- `security.installPolicy.exec.noOutputTimeoutMs` (`number`, default `timeoutMs`) — maximum time without stdout or stderr output before the policy fails closed.
- `security.installPolicy.exec.maxOutputBytes` (`number`, default `1048576`) — maximum combined stdout and stderr bytes accepted from the policy process.
- `security.installPolicy.exec.env` (`Record<string, string>`) — literal environment variables provided to the policy process.
- `security.installPolicy.exec.passEnv` (`string[]`) — environment variable names copied from the OpenClaw process into the policy process. Only named variables are passed.
- `security.installPolicy.exec.trustedDirs` (`string[]`) — optional allowlist of directories that may contain the policy executable.
- `security.installPolicy.exec.allowInsecurePath` (`boolean`, default `false`) — bypasses command path ownership and permission checks. Use only when the path is protected by another mechanism.
- `security.installPolicy.exec.allowSymlinkCommand` (`boolean`, default `false`) — allows the configured command path to be a symlink. The resolved target must still satisfy the other path checks. Interpreter script arguments must be direct regular files, not symlinks.

### Policy Protocol (stdin/stdout)

The policy receives one JSON object on stdin with `protocolVersion: 1`, `openclawVersion`, `targetType`, `targetName`, `sourcePath`, `sourcePathKind`, optional structured `source`, structured `origin`, and `request`. It must write one JSON object on stdout: `{ "protocolVersion": 1, "decision": "allow" }` or `{ "protocolVersion": 1, "decision": "block", "reason": "..." }`. Non-zero exit, timeout, malformed JSON, missing fields, or unsupported protocol versions **fail closed**.

OpenClaw does not execute install policy during normal Gateway startup. Installs and updates fail closed when policy is enabled but unavailable. `openclaw doctor` performs static validation, and `openclaw doctor --deep` executes a synthetic install probe against the configured command. Bulk updates apply policy per target: a blocked skill or plugin update fails that target without disabling the policy or skipping later targets in the batch.

Example stdin object the policy receives:

```json
{
  "protocolVersion": 1,
  "openclawVersion": "2026.6.1",
  "targetType": "skill",
  "targetName": "weather",
  "sourcePath": "/var/folders/.../openclaw-skill-clawhub/root",
  "sourcePathKind": "directory",
  "source": {
    "kind": "clawhub",
    "authority": "openclaw",
    "mutable": false,
    "network": true
  },
  "origin": {
    "type": "clawhub",
    "registry": "https://clawhub.openclaw.ai",
    "slug": "weather",
    "version": "1.0.0"
  },
  "request": {
    "kind": "skill-install",
    "mode": "install",
    "requestedSpecifier": "clawhub:weather@1.0.0"
  },
  "skill": {
    "installId": "clawhub"
  }
}
```

## Bundled skill allowlist (`skills.allowBundled`)

- `skills.allowBundled` (`string[]`) — optional allowlist for **bundled** skills only. When set, only bundled skills in the list are eligible. Managed, agent-level, and workspace skills are unaffected.

## Per-skill entries (`skills.entries`)

Keys under `entries` match the skill `name` by default. If a skill defines `metadata.openclaw.skillKey`, use that key instead. Quote hyphenated names (JSON5 allows quoted keys).

- `skills.entries.<key>.enabled` (`boolean`) — `false` disables the skill even when bundled or installed. The `coding-agent` bundled skill is opt-in — set it to `true` and ensure one of `claude`, `codex`, `opencode`, or another supported CLI is installed and authenticated.
- `skills.entries.<key>.apiKey` (`string | { source, provider, id }`) — convenience field for skills that declare `metadata.openclaw.primaryEnv`. Supports a plaintext string or a SecretRef: `{ source: "env", provider: "default", id: "VAR_NAME" }`.
- `skills.entries.<key>.env` (`Record<string, string>`) — environment variables injected for the agent run. Only injected when the variable is **not already set** in the process.
- `skills.entries.<key>.config` (`object`) — optional bag for custom per-skill configuration fields.

## Agent allowlists (`agents`)

Use agent config when you want the same machine/workspace skill roots but a different **visible** skill set per agent.

```json5
{
  agents: {
    defaults: {
      skills: ["github", "weather"], // shared baseline
    },
    list: [
      { id: "writer" }, // inherits github, weather
      { id: "docs", skills: ["docs-search"] }, // replaces defaults entirely
      { id: "locked-down", skills: [] }, // no skills
    ],
  },
}
```

- `agents.defaults.skills` (`string[]`) — shared baseline allowlist inherited by agents that omit `agents.list[].skills`. Omit entirely to leave skills unrestricted by default.
- `agents.list[].skills` (`string[]`) — explicit final skill set for that agent. Explicit lists **replace** inherited defaults — they do not merge. Set to `[]` to expose no skills for that agent.

## Workshop (`skills.workshop`)

- `skills.workshop.autonomous.enabled` (`boolean`, default `false`) — when `true`, agents can create pending proposals from durable conversation signals after successful turns. User-prompted skill creation always goes through Skill Workshop regardless of this setting.
- `skills.workshop.approvalPolicy` (`"pending" | "auto"`, default `"pending"`) — `pending` requires operator approval before agent-initiated apply, reject, or quarantine. `auto` allows those actions without approval.
- `skills.workshop.allowSymlinkTargetWrites` (`boolean`, default `false`) — allow Skill Workshop apply to write through workspace skill symlinks whose real target is already trusted by `skills.load.allowSymlinkTargets`. Keep this disabled unless generated proposal applies should mutate that shared skill root.
- `skills.workshop.maxPending` (`number`, default `50`) — maximum pending and quarantined proposals retained per workspace.
- `skills.workshop.maxSkillBytes` (`number`, default `40000`) — maximum proposal body size in bytes. Proposal descriptions are hard-capped at 160 bytes because they appear in discovery and listing output.

## Symlinked skill roots

By default, workspace, project-agent, extra-dir, and bundled skill roots are containment boundaries. A symlinked skill folder under `<workspace>/skills` that resolves outside the root is **skipped with a log message**. To allow an intentional symlink layout, declare the trusted target via `extraDirs` + `allowSymlinkTargets`; then `<workspace>/skills/manager -> ~/Projects/manager/skills` is accepted after realpath resolution. `extraDirs` scans the sibling repo directly, while `allowSymlinkTargets` preserves the symlinked path for existing layouts. Skill Workshop apply does not write through those symlinks by default — to let Workshop apply mutate skills under already-trusted symlink targets, opt in separately with `skills.workshop.allowSymlinkTargetWrites: true`. Managed `~/.openclaw/skills` and personal `~/.agents/skills` directories already accept skill-directory symlinks (per-skill `SKILL.md` containment still applies).

## Sandboxed skills and env vars

Warning (source): `skills.entries.<skill>.env` and `apiKey` apply to **host** runs only. Inside a sandbox they have no effect — a skill that depends on `GEMINI_API_KEY` will fail with `apiKey not configured` unless the sandbox is given the variable separately. Pass secrets into a Docker sandbox with:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          env: { GEMINI_API_KEY: "your-key-here" },
        },
      },
    },
  },
}
```

Note (source): users with Docker daemon access can inspect `sandbox.docker.env` values through Docker metadata. Use a mounted secret file, a custom image, or another delivery path when that exposure is not acceptable.

## Loading order reminder

```text
workspace/skills      (highest)
workspace/.agents/skills
~/.agents/skills
~/.openclaw/skills
bundled skills
skills.load.extraDirs (lowest)
```

Changes to skills and config take effect on the next new session when the watcher is enabled, or on the next agent turn when the watcher detects a change.

**Source**: OpenClaw documentation — `tools/skills-config` (mirror `inbox/openclaw_docs/tools/skills-config.md`)
**Last Updated**: 2026-06-22
**Status**: Active
