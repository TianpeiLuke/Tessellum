---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - copilot
keywords:
  - openclaw copilot sdk harness
  - "@openclaw/copilot plugin"
  - agentRuntime id copilot
  - github-copilot provider runtime
  - copilotHome per-agent isolation
  - gitHubToken auth precedence
  - transcript mirroring dual-write
  - btw pi fallback
  - copilot doctor probes
  - overridesBuiltInTool skipPermission
topics:
  - OpenClaw
  - Plugins
  - Agent Runtimes
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/copilot
access_control_group: ["general"]
---

# OpenClaw — Copilot SDK Harness Plugin

## Overview

This note is the procedure for running OpenClaw embedded agent turns through the external `@openclaw/copilot` plugin — the GitHub Copilot SDK harness — instead of the built-in PI harness, mirroring the `plugins/copilot` source page. The plugin lets the Copilot CLI (`@github/copilot-sdk`) own the low-level agent loop (native tool execution, native compaction via `infiniteSessions`, CLI-managed thread state under `copilotHome`), while OpenClaw still owns chat channels, session files, model selection, bridged dynamic tools, approvals, media delivery, the visible transcript mirror, `/btw` side questions, and `openclaw doctor`. It walks the opt-in lifecycle: requirements, install, pinning a model to `agentRuntime: { id: "copilot" }`, supported providers, auth precedence, the configuration surface, compaction, transcript mirroring, the `/btw` PI fallback, doctor probes, MVP limitations, and how permissions stay at PI parity through the tool wrapper.

## Requirements

Four prerequisites must hold before opting an agent in. (1) OpenClaw with the `@openclaw/copilot` plugin installed. (2) If your config uses `plugins.allow`, it must include `copilot` (the manifest id declared by the plugin) — a restrictive allowlist listing the npm-style `@openclaw/copilot` package name leaves the plugin blocked and the runtime will not load even with `agentRuntime.id: "copilot"`. (3) A GitHub Copilot subscription that can drive the Copilot CLI, or a `gitHubToken` env / auth-profile entry for headless / cron runs. (4) A writable `copilotHome` — defaults to `~/.openclaw/agents/<agentId>/copilot` for full per-agent isolation; the platform default (`%APPDATA%\copilot` on Windows, `$XDG_CONFIG_HOME/copilot` or `~/.config/copilot` elsewhere) is the doctor probe fallback when no explicit home is set. Running `openclaw doctor` executes the plugin doctor contract; doctor failures are the canonical way to confirm the environment is ready.

## Plugin install

The Copilot runtime is an external plugin, so the core `openclaw` package does not carry the `@github/copilot-sdk` dependency or its platform-specific `@github/copilot-<platform>-<arch>` CLI binary; together they add roughly 260 MB, so install them only for agents that opt into this runtime:

```bash
openclaw plugins install @openclaw/copilot
```

The wizard installs the plugin the first time you select a `github-copilot/*` model **and** your config opts the model (or its provider) into the Copilot agent runtime via `agentRuntime: { id: "copilot" }`; without the opt-in, OpenClaw uses its built-in GitHub Copilot provider and never installs the runtime plugin. The harness resolves the SDK in this order: (1) `import("@github/copilot-sdk")` from the installed `@openclaw/copilot` package, then (2) the well-known fallback dir `~/.openclaw/npm-runtime/copilot/` (the legacy on-demand install target). A missing SDK surfaces a single error with code `COPILOT_SDK_MISSING` plus the reinstall command above.

## Quickstart

Pin one model — or one provider — to the harness. The minimal model-scoped config:

```json5
{
  agents: {
    defaults: {
      model: "github-copilot/auto",
      models: {
        "github-copilot/auto": {
          agentRuntime: { id: "copilot" },
        },
      },
    },
  },
}
```

Both routes are equivalent: use `agentRuntime.id` on a single model entry when only that model should route through the harness, and on a provider when every model under it should. `github-copilot/auto` is the portable starting point — named Copilot models are account- and organization-policy-dependent, so only pin one after confirming the authenticated Copilot CLI exposes it.

## Supported providers

The harness advertises support for exactly the canonical `github-copilot` provider (the same id owned by `extensions/github-copilot`). Anything outside that single-provider set falls through `selection.ts`'s `auto_pi` branch back to PI, so a model on an unsupported provider silently runs on the built-in PI harness rather than the Copilot CLI.

## Auth

Per-agent auth precedence, applied during `runCopilotAttempt`, has five ordered steps: (1) **Explicit `useLoggedInUser: true`** on the attempt input, using the Copilot CLI's logged-in user resolved under the agent's `copilotHome`. (2) **Explicit `gitHubToken`** on the attempt input (with `profileId` + `profileVersion`), for direct CLI invocations and tests bypassing auth-profile resolution. (3) **Contract-resolved `resolvedApiKey` + `authProfileId`** from the `EmbeddedRunAttemptParams` shape — the **production main path**: core resolves the configured `github-copilot` auth profile (via `src/infra/provider-usage.auth.ts:resolveProviderAuths`) before invoking the harness, which consumes both fields directly, making a `github-copilot:<profile>` auth profile work end-to-end for headless / cron / multi-profile setups without env vars. (4) **Env-var fallback** for direct CLI / dogfood runs with no auth profile configured. (5) **Default `useLoggedInUser`** when no token signal is available.

The env-var fallback checks four vars in precedence order, mirroring the shipped `github-copilot` provider (`extensions/github-copilot/auth.ts`) and the documented Copilot SDK setup: (1) `OPENCLAW_GITHUB_TOKEN` — harness-specific override, pins a token without disturbing system-wide `gh` / Copilot CLI config; (2) `COPILOT_GITHUB_TOKEN` — standard Copilot SDK / CLI env var; (3) `GH_TOKEN` — standard `gh` CLI env var; (4) `GITHUB_TOKEN` — generic GitHub token fallback. The first non-empty value wins, empty strings are absent, the synthesised pool profile id is `env:<NAME>`, and `profileVersion` is a non-reversible sha256 fingerprint of the token, so rotating the env value cleanly busts the client pool.

Each agent gets a dedicated `copilotHome` so Copilot CLI tokens, sessions, and config do not leak between agents on the same machine: the default is `<agentDir>/copilot` when the host hands the harness an agent directory (isolating SDK state from OpenClaw's `models.json` / `auth-profiles.json`), else `~/.openclaw/agents/<agentId>/copilot`; override with `copilotHome: <path>` for a custom location such as a shared mount for migration. `probeCopilotAuthShape` (see Doctor and probes) is the pure shape check validating which mode will be used — not a live SDK handshake.

## Configuration surface

The harness reads config from per-attempt input (`runCopilotAttempt({...})`) plus env defaults inside `extensions/copilot/src/`. The fields: `copilotHome` — per-agent CLI state directory (defaults above); `model` — a string or `{ provider, id, api? }` (when omitted, OpenClaw uses normal model selection and verifies the resolved provider is supported); `reasoningEffort` — `"low" | "medium" | "high" | "xhigh"`, mapped from OpenClaw's `ThinkLevel` / `ReasoningLevel` resolution in `auto-reply/thinking.ts`; `infiniteSessionConfig` — optional override for the SDK `infiniteSessions` block driven by `harness.compact` (defaults safe as-is); `hooksConfig` — optional native Copilot SDK `SessionHooks` config for tool/MCP, user-prompt, session, and error callbacks, separate from OpenClaw's portable lifecycle hooks; `permissionPolicy` — optional override for the SDK's `onPermissionRequest` handler for built-in SDK tool kinds (`shell`, `write`, `read`, `url`, `mcp`, `memory`, `hook`), defaulting to `rejectAllPolicy` as a safety net (in practice never invoked because every bridged tool is registered `overridesBuiltInTool: true` + `skipPermission: true`, so 100% of tool calls flow through the wrapped `execute()`); `enableSessionTelemetry` — optional SDK session telemetry flag.

OpenClaw plugin hooks need no Copilot-specific attempt configuration: the harness runs `before_prompt_build` (and the legacy `before_agent_start` hook), `llm_input`, `llm_output`, and `agent_end` through the standard harness helpers, successful SDK compactions also run `before_compaction` and `after_compaction`, and bridged tools run `before_tool_call` and report `after_tool_call` — `hooksConfig` remains only for native SDK-only callbacks with no portable equivalent. Other plugins, channels, and core code only see the standard `AgentHarnessAttemptParams` / `AgentHarnessAttemptResult` shape.

## Compaction

When `harness.compact` runs, the Copilot SDK harness performs three steps: (1) resumes the tracked SDK session without continuing pending work, (2) calls the SDK's session-scoped history compaction RPC, and (3) returns the SDK compaction outcome without writing compatibility marker files under the workspace. The OpenClaw-side transcript mirror (below) keeps receiving the post-compaction messages, so user-facing chat history stays consistent.

## Transcript mirroring

`runCopilotAttempt` dual-writes each turn's mirrorable messages into the OpenClaw audit transcript via `extensions/copilot/src/dual-write-transcripts.ts`. The mirror is per-session scoped (`copilot:${sessionId}`) and uses a per-message identity (`${role}:${sha256_16(role,content)}`) so re-emits of prior-turn entries collide with existing on-disk keys and do not duplicate. Two layers of failure containment ensure a transcript write failure cannot fail the attempt — an internal best-effort wrapper and a defense-in-depth `.catch(...)` at the attempt level — with failures logged but not surfaced.

## Side questions (`/btw`)

`/btw` is **not** native on this harness: `createCopilotAgentHarness()` deliberately leaves `harness.runSideQuestion` undefined, so OpenClaw's `/btw` dispatcher (`src/agents/btw.ts`) falls through to the same in-tree PI fallback it uses for every non-Codex runtime — the configured model provider is called directly with a short side-question prompt and streamed back via `streamSimple` (no CLI session, no extra pool slot). This reserves Copilot CLI sessions for the agent's main turn loop and keeps `/btw` identical to other PI-backed runtimes; the contract is asserted in `extensions/copilot/harness.test.ts` under `describe("runSideQuestion")`.

## Doctor and probes

`extensions/copilot/doctor-contract-api.ts` is auto-loaded by `src/plugins/doctor-contract-registry.ts` and contributes an empty `legacyConfigRules` (no retired fields at MVP), a no-op `normalizeCompatibilityConfig` (a stable in-tree home for future field retirements), and one `sessionRouteStateOwners` entry claiming provider `github-copilot`, runtime `copilot`, CLI session key `copilot`, and auth profile prefix `github-copilot:`. `extensions/copilot/src/doctor-probes.ts` exports three imperative probes hosts (including `openclaw doctor`) can call to verify the environment:

| Probe | What it checks | Reasons it can fail |
| --- | --- | --- |
| `probeCopilotCliVersion` | `copilot --version` exits 0 with a non-empty version string | `non-zero-exit`, `empty-version`, `spawn-failed`, `spawn-error`, `probe-timeout` |
| `probeCopilotHomeWritable` | `mkdir -p copilotHome` + write + rm a marker file | `copilothome-not-writable` (with the underlying fs error in `details.rawError`) |
| `probeCopilotAuthShape` | At least one of `useLoggedInUser`, `gitHubToken`, or `profileId`+`profileVersion` | `no-auth-source` |

Each probe accepts a DI seam (`spawnFn`, `fsApi`) so tests need not spawn the real Copilot CLI or touch the host fs.

## Limitations

The harness has four documented MVP limitations. (1) It only claims the canonical `github-copilot` provider — additional providers (BYOK or otherwise) should land in follow-up PRs shipping the adapter alongside the wire-up. (2) It does not deliver TUI; PI's TUI is unaffected and remains the fallback for runtimes without a peer surface. (3) PI session state is not migrated when an agent switches to `copilot` — selection is per attempt, and existing PI sessions remain valid. (4) **Interactive `ask_user` is not yet wired**: the SDK's `onUserInputRequest` handler is intentionally not registered, which per the SDK contract hides the `ask_user` tool from the model entirely, so agents under this harness make best-judgment decisions from the initial prompt rather than asking clarifying questions mid-turn — a follow-up will port the codex pattern at `extensions/codex/src/app-server/user-input-bridge.ts` to route SDK `UserInputRequest`s through the OpenClaw channel/TUI prompt path.

## Permissions and ask_user

Permission enforcement for bridged OpenClaw tools happens **inside the tool wrapper**, not via the SDK's `onPermissionRequest` callback: the same `wrapToolWithBeforeToolCallHook` PI uses (`src/agents/pi-tools.before-tool-call.ts`) is applied by `createOpenClawCodingTools` to every coding tool, so loop detection, trusted plugin policies, before-tool-call hooks, and two-phase plugin approvals via the gateway (`plugin.approval.request`) run on the exact same code path as native PI attempts. To let that wrapper own the decision, the SDK Tool from `convertOpenClawToolToSdkTool` is marked `overridesBuiltInTool: true` (replaces the Copilot CLI's built-in tool of the same name — edit, read, write, bash — so every invocation routes back to OpenClaw) and `skipPermission: true` (tells the SDK not to fire `onPermissionRequest({kind: "custom-tool"})`, since the wrapped `execute()` does the richer policy check internally — an SDK-level prompt would either short-circuit enforcement if allow-all or block every call if reject-all, neither matching PI parity).

The in-tree codex harness uses the same split: bridged tools are wrapped (`extensions/codex/src/app-server/dynamic-tools.ts`) while codex-app-server native approval kinds (`item/commandExecution/requestApproval`, `item/fileChange/requestApproval`, `item/permissions/requestApproval`) route through `plugin.approval.request` (`extensions/codex/src/app-server/approval-bridge.ts`); the Copilot equivalent — fail-closed `rejectAllPolicy` for any non-`custom-tool` kind reaching `onPermissionRequest` — is the same safety net, not firing in practice since `overridesBuiltInTool: true` displaces every built-in. For PI-equivalent decisions the harness forwards the full PI attempt-tool context to `createOpenClawCodingTools` — identity (`senderIsOwner`, `memberRoleIds`, `ownerOnlyToolAllowlist`), channel/routing (`groupId`, `currentChannelId`, `replyToMode`), auth (`authProfileStore`), run identity (`sessionKey`/`runSessionKey`, `runId`), model context (`modelApi`, `modelContextWindowTokens`, `modelCompat`, `modelHasVision`), run hooks (`onToolOutcome`, `onYield`) — without these, owner-only allowlists silently deny-by-default, plugin-trust policies cannot resolve scope, and `session_status: "current"` resolves to a stale sandbox key. The bridge builder is `extensions/copilot/src/tool-bridge.ts`, mirroring the PI call at `src/agents/pi-embedded-runner/run/attempt.ts:1029-1117`; two PI fields are intentionally **not** forwarded at MVP (follow-ups): `sandbox` (no `resolveSandboxContext` routing yet) and the PI tool-search/code-mode machinery (`toolSearchCatalogRef`, `includeCoreTools`, `includeToolSearchControls`, `toolSearchCatalogExecutor`, `toolConstructionPlan`), with no SDK-boundary analog.

### Session-level GitHub token

The Copilot SDK contract distinguishes the **client-level** GitHub token (`CopilotClientOptions.gitHubToken`, authenticating the CLI process itself) from the **session-level** token (`SessionConfig.gitHubToken`, which determines content exclusion, model routing, and quota for that session and is honored on both `createSession` and `resumeSession`). The harness resolves auth once via `resolveCopilotAuth` and sets both fields when the mode is `gitHubToken` (an explicit `auth.gitHubToken` or a contract-resolved `resolvedApiKey` from a configured `github-copilot` auth profile); when the mode is `useLoggedInUser`, the session-level field is omitted so the SDK keeps deriving identity from the logged-in user. `ask_user` is intentionally hidden — see Limitations.

**Source**: OpenClaw documentation — `plugins/copilot` (mirror `inbox/openclaw_docs/plugins/copilot.md`)
**Last Updated**: 2026-06-22
**Status**: Active
