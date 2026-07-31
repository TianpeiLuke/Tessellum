---
tags:
  - resource
  - documentation
  - claude_code
  - settings
  - reference
keywords:
  - settings.json reference
  - available settings keys
  - global config settings
  - worktree settings
  - managed-settings-only keys
  - claude.json
  - model selection keys
  - skill listing settings
topics:
  - Claude Code
  - Settings
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/settings
access_control_group: ["general"]
---

# Claude Code — Settings Reference (settings.json keys)

## Overview

This note is the field-by-field reference for the keys Claude Code reads from configuration. It covers three key surfaces: the large **`settings.json` Available settings** table (the canonical option list), the **Global config settings** stored in `~/.claude.json` (not `settings.json`), and the **Worktree settings** (`worktree.*`) that govern `--worktree`. Each key is given a one-line purpose; deep semantics for the model family, permissions, sandbox, hooks, and plugins are documented in their owning notes and linked out rather than duplicated here.

Several keys are **(Managed settings only)** — they are honored only when delivered through the managed tier (see [Managed Settings](cc_managed_settings.md)) and cannot be set by user/project/local scope. Keys also carry minimum-version requirements where noted in source.

## Available settings (`settings.json`)

`settings.json` supports the keys below. Deeper semantics for model/effort/thinking → see [model-config](https://code.claude.com/docs/en/model-config); permission rules → [Permission & Attribution Settings](cc_permission_and_attribution_settings.md); `sandbox.*` → [Sandbox Settings](cc_sandbox_settings.md); hook-gating → [Hook Configuration Settings](cc_hook_configuration_settings.md); subagent/plugin → [Subagent & Plugin Settings](cc_subagent_and_plugin_settings.md) and [Managed Plugin Policy Settings](cc_managed_plugin_policy_settings.md).

**Model, thinking, and effort**

- `model` — Override the default model. `--model` and `ANTHROPIC_MODEL` override it for one session.
- `availableModels` — Restrict which models users can select for the main session, subagents, and the advisor.
- `enforceAvailableModels` (v2.1.175+) — When `true` and `availableModels` is non-empty in managed/policy settings, constrains the Default model to the allowlist too.
- `modelOverrides` — Map Anthropic model IDs to provider-specific IDs (e.g., Bedrock inference-profile ARNs).
- `fallbackModel` — Fallback model(s) to try in order when the primary is overloaded; chains capped at three. Does **not** merge across files — the highest-precedence file defining it supplies the whole chain.
- `advisorModel` (v2.1.98+) — Model for the server-side advisor tool; written by `/advisor`, unset to disable.
- `effortLevel` — Persist the effort level (`"low"`/`"medium"`/`"high"`/`"xhigh"`); written by `/effort`.
- `alwaysThinkingEnabled` — Enable extended thinking by default for all sessions.
- `showThinkingSummaries` — Show extended-thinking summaries in interactive sessions (no effect in `-p`/SDK/IDE).
- `ultracode` — Turn on ultracode for the session; session-only, not read from `settings.json`.

**Permissions, attribution, sandbox, hooks (deep semantics linked out)**

- `permissions` — Permission rules object (`allow`/`ask`/`deny`/`additionalDirectories`/`defaultMode`/…). See [Permission & Attribution Settings](cc_permission_and_attribution_settings.md).
- `allowManagedPermissionRulesOnly` (managed only) — Only managed-settings permission rules apply.
- `attribution` — Customize git-commit and PR attribution; takes precedence over deprecated `includeCoAuthoredBy`.
- `includeCoAuthoredBy` — **Deprecated**: use `attribution` instead.
- `sandbox` — Bash-sandboxing object (`enabled`, `filesystem.*`, `network.*`, …). See [Sandbox Settings](cc_sandbox_settings.md).
- `hooks` — Custom commands run at lifecycle events. See [Hook Configuration Settings](cc_hook_configuration_settings.md).
- `disableAllHooks` — Disable all hooks and any custom status line.
- `allowManagedHooksOnly` / `allowedHttpHookUrls` / `httpHookAllowedEnvVars` — Hook gating (see [Hook Configuration Settings](cc_hook_configuration_settings.md)).
- `fileSuggestion` — Custom script for `@` file autocomplete. See [Permission & Attribution Settings](cc_permission_and_attribution_settings.md).
- `statusLine` — Configure a custom status line.

**MCP server approval (deep semantics → managed/MCP notes)**

- `enableAllProjectMcpServers` — Auto-approve all MCP servers in project `.mcp.json` files.
- `enabledMcpjsonServers` — Allowlist of specific `.mcp.json` MCP servers to approve.
- `disabledMcpjsonServers` — Specific `.mcp.json` MCP servers to reject.
- `allowedMcpServers` / `deniedMcpServers` / `allowManagedMcpServersOnly` / `allowAllClaudeAiMcps` — Managed-settings-only MCP allow/deny/lockdown. See [Managed Settings](cc_managed_settings.md).

**Skills, memory, and context lifecycle**

- `disableBundledSkills` — Disable the skills/workflows that ship with Claude Code (plugin/`.claude/skills/`/`.claude/commands/` skills unaffected).
- `skillOverrides` (v2.1.129+) — Per-skill visibility overrides keyed by skill name (`"on"`/`"name-only"`/`"user-invocable-only"`/`"off"`); not for plugin skills.
- `maxSkillDescriptionChars` (v2.1.105+) — Per-skill cap on combined `description`+`when_to_use` text in the skill listing (default `1536`).
- `skillListingBudgetFraction` (v2.1.105+) — Fraction of the context window reserved for the skill listing (default `0.01`).
- `disableSkillShellExecution` — Disable inline shell execution in skills/custom commands from user/project/plugin/additional-directory sources.
- `disableWorkflows` — Disable dynamic workflows and bundled workflow commands.
- `workflowKeywordTriggerEnabled` (v2.1.157+) — Whether `ultracode` in a prompt triggers a dynamic workflow.
- `useAutoModeDuringPlan` — Whether plan mode uses auto-mode semantics; not read from shared project settings.
- `showClearContextOnPlanAccept` — Show the "clear context" option on the plan-accept screen (default `false`).
- `autoMemoryEnabled` / `autoMemoryDirectory` — Enable auto memory and set its storage directory.
- `claudeMd` (managed only) — CLAUDE.md-style instructions injected as org-managed memory.
- `claudeMdExcludes` — Glob patterns/absolute paths of `CLAUDE.md` files to skip when loading memory.
- `includeGitInstructions` — Include built-in commit/PR workflow instructions and git-status snapshot in the system prompt (default `true`).
- `outputStyle` — Output style that adjusts the system prompt.
- `language` — Claude's preferred response and voice-dictation language.
- `cleanupPeriodDays` — Session files older than this are deleted at startup (default 30, min 1; `0` rejected).
- `plansDirectory` — Where plan files are stored (default `~/.claude/plans`).

**Auth, credentials, and login enforcement**

- `apiKeyHelper` — Custom `/bin/sh` script to generate an auth value sent as `X-Api-Key` and `Authorization: Bearer`.
- `forceLoginMethod` — Restrict login to `claudeai` or `console`; in managed settings, blocks API-key/auth-token/`apiKeyHelper` sessions at startup.
- `forceLoginOrgUUID` — Require login to belong to a specific Anthropic org (UUID or array of UUIDs).
- `awsAuthRefresh` / `awsCredentialExport` / `gcpAuthRefresh` — Cloud-provider credential refresh/export scripts.
- `forceRemoteSettingsRefresh` (managed only) — Block startup until remote managed settings are freshly fetched.

**Updates and version pinning**

- `autoUpdatesChannel` — Release channel: `"stable"` or `"latest"` (default).
- `minimumVersion` — Floor preventing auto-updates/`claude update` from installing below it (never blocks startup).
- `requiredMinimumVersion` / `requiredMaximumVersion` (managed only) — Hard floor/ceiling that blocks startup outside the range; `claude update`/`install`/`doctor` keep working to recover.

**Plugins, marketplaces, channels (deep semantics → plugin notes)**

- `strictKnownMarketplaces` / `blockedMarketplaces` / `strictPluginOnlyCustomization` (managed only) — Marketplace allow/blocklist and customization lockdown. See [Managed Plugin Policy Settings](cc_managed_plugin_policy_settings.md).
- `pluginSuggestionMarketplaces` (managed only) — Marketplaces whose plugins can surface as contextual install suggestions.
- `pluginTrustMessage` (managed only) — Custom text appended to the plugin trust warning.
- `allowedChannelPlugins` / `channelsEnabled` (managed only) — Channel-plugin allowlist and org channel enablement.

**UI, terminal, and interaction**

- `autoScrollEnabled`, `editorMode`, `viewMode`, `tui`, `prefersReducedMotion`, `syntaxHighlightingDisabled`, `terminalProgressBarEnabled`, `wheelScrollAccelerationEnabled` (v2.1.174+) — Rendering/input options.
- `spinnerTipsEnabled`, `spinnerTipsOverride`, `spinnerVerbs`, `showTurnDuration`, `awaySummaryEnabled` — Spinner/status presentation.
- `preferredNotifChannel` — Task-complete/permission-prompt notification method.
- `companyAnnouncements` — Startup announcement(s), cycled at random if multiple.
- `defaultShell` — Default shell for input-box `!` commands (`"bash"` default, or `"powershell"`).
- `voice` / `voiceEnabled` (legacy alias) — Voice-dictation settings.
- `prUrlTemplate` — URL template for the PR badge in footer/tool-result summaries.
- `respectGitignore` — Whether the `@` file picker respects `.gitignore` (default `true`).
- `teammateMode` — How agent-team teammates display (`auto`/`in-process`/`tmux`).
- `sshConfigs` — SSH connections shown in the Desktop environment dropdown (read from managed/user only).

**Disable/lockdown toggles and other**

- `disableAgentView` — Turn off background agents and agent view.
- `disableAutoMode` — Prevent auto mode from being activated (`"disable"`).
- `disableBypassPermissionsMode` — Prevent `bypassPermissions` mode (disables `--dangerously-skip-permissions`).
- `disableDeepLinkRegistration` — Prevent registering the `claude-cli://` protocol handler.
- `disableRemoteControl` (v2.1.128+) — Disable Remote Control.
- `skipWebFetchPreflight` — Skip the WebFetch domain safety check (for egress-restricted environments).
- `fastModePerSessionOptIn` — Fast mode does not persist across sessions when `true`.
- `feedbackSurveyRate` — Probability (0–1) the session-quality survey appears.
- `policyHelper` (v2.1.136+) — Admin-deployed executable that computes managed settings dynamically. See [Managed Settings](cc_managed_settings.md).
- `otelHeadersHelper` — Script to generate dynamic OpenTelemetry headers.
- `parentSettingsBehavior` (v2.1.133+, managed only) — Whether host-supplied managed settings apply under an admin tier (`"first-wins"` default / `"merge"`).
- `agent` — Run the main thread as a named subagent and set the default dispatched agent. See [Subagent & Plugin Settings](cc_subagent_and_plugin_settings.md).
- `wslInheritsWindowsSettings` (Windows managed only) — WSL reads managed settings from the Windows policy chain too.
- `env` — Environment variables applied to every session and spawned subprocesses. See [Environment Variables](cc_environment_variables.md).

## Global config settings (`~/.claude.json`)

These settings live in `~/.claude.json`, not `settings.json`; **adding them to `settings.json` triggers a schema validation error.** (Versions before v2.1.119 also stored `autoScrollEnabled`, `editorMode`, `showTurnDuration`, `teammateMode`, and `terminalProgressBarEnabled` here.)

- `autoConnectIde` — Auto-connect to a running IDE when Claude Code starts from an external terminal (default `false`).
- `autoInstallIdeExtension` — Auto-install the Claude Code IDE extension from a VS Code terminal (default `true`).
- `externalEditorContext` — Prepend Claude's previous response as `#`-commented context when opening the external editor with `Ctrl+G` (default `false`).
- `teammateDefaultModel` — Default model for agent-team teammates when the spawn prompt doesn't specify one; `null` inherits the lead's `/model`.

## Worktree settings (`worktree.*`)

Configure how `--worktree` creates and manages git worktrees.

- `worktree.baseRef` — Which ref new worktrees branch from. `"fresh"` (default) branches from `origin/<default-branch>`; `"head"` branches from the current local `HEAD`. Applies to `--worktree`, the `EnterWorktree` tool, and subagent isolation.
- `worktree.symlinkDirectories` — Directories to symlink from the main repo into each worktree to avoid duplicating large directories.
- `worktree.sparsePaths` — Directories to check out per worktree via git sparse-checkout (listed dirs plus root-level files only).
- `worktree.bgIsolation` (v2.1.143+) — Isolation mode for background sessions. `"worktree"` (default) blocks `Edit`/`Write` in the main checkout until `EnterWorktree`; `"none"` lets background jobs edit the working copy directly.

To copy gitignored files like `.env` into new worktrees, use a `.worktreeinclude` file in the project root instead of a setting.

## Example `settings.json`

```JSON
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

**Source**: https://code.claude.com/docs/en/settings
**Last Updated**: 2026-06-13
**Status**: Active
