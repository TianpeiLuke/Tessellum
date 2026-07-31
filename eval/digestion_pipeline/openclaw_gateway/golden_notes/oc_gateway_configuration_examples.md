---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - configuration
keywords:
  - openclaw configuration examples
  - openclaw.json json5 config
  - recommended starter config
  - secure dm mode dmscope
  - api key minimax fallback
  - trusted node auto-approval
  - local models only config
  - shared skill baseline
topics:
  - OpenClaw
  - Gateway Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/configuration-examples
access_control_group: ["general"]
---

# OpenClaw — Gateway Configuration Examples

## Overview

This note is a procedure reference of copy-paste, schema-accurate OpenClaw config recipes, mirroring the `gateway/configuration-examples` source page. All examples are JSON5 written to `~/.openclaw/openclaw.json` and aligned with the current config schema (for the exhaustive field reference, see [Configuration](https://docs.openclaw.ai/gateway/configuration)). It covers the Quick-start starters (absolute minimum + recommended starter), a major-options Expanded example, the Common patterns (symlinked sibling skill repo, shared skill baseline with one override, multi-platform, trusted node network auto-approval, secure DM mode, Anthropic API key + MiniMax fallback, work bot, local models only), and the closing Tips. JSON5 lets you use comments and trailing commas; regular JSON works too.

## Quick start

**Absolute minimum** — the smallest config that lets you DM the bot. Set the agent workspace and one channel allowlist, save to `~/.openclaw/openclaw.json`, and you can DM the bot from that number:

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

**Recommended starter** — adds a primary model (`agents.defaults.model.primary: "anthropic/claude-sonnet-4-6"`), a single named agent in `agents.list` with an `identity` (`name`/`theme`/`emoji`), a WhatsApp `groups: { "*": { requireMention: true } }` rule, and a `messages` block. Note the group-chat default `visibleReplies: "message_tool"` (opt-in; visible output requires `message(action=send)`) and `unmentionedInbound: "room_event"`:

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "anthropic/claude-sonnet-4-6" },
    },
    list: [
      {
        id: "main",
        identity: { name: "Clawd", theme: "helpful assistant", emoji: "🦞" },
      },
    ],
  },
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  messages: {
    visibleReplies: "automatic",
    groupChat: {
      visibleReplies: "message_tool",
      unmentionedInbound: "room_event",
    },
  },
}
```

## Expanded example (major options)

The Expanded example demonstrates most top-level config sections at once; reproduce only the sections you need. The full source recipe wires together: `env` (inline vars + `shellEnv` with `enabled`/`timeoutMs`); `auth` profile metadata (`profiles` keyed `provider:label` with `mode: "api_key"|"oauth"`, secrets live in `auth-profiles.json`) plus per-provider `order` arrays; `logging` (`level`, `file`, `consoleLevel`, `consoleStyle`, `redactSensitive: "tools"`); `messages` formatting (`messagePrefix`, `responsePrefix`, `ackReaction`/`ackReactionScope`, `groupChat.historyLimit`) and a message `queue` (`mode: "followup"`, `debounceMs`, `cap`, `drop: "summarize"`, and `byChannel` per-channel modes such as `discord: "collect"`); `tools.media` (audio/video with `enabled`, `maxBytes`, `models`, `timeoutSeconds`); `session` behavior (`scope`, `dmScope: "per-channel-peer"`, `reset` with `mode`/`atHour`/`idleMinutes`, `resetByChannel`, `store`, `maintenance` with `pruneAfter`/`maxEntries`/`resetArchiveRetention`, `sendPolicy`); per-channel blocks (`whatsapp`, `telegram`, `discord` `guilds`/`channels`, `slack` with `botToken`/`appToken` and `slashCommand`); `agents.defaults` runtime (`model.primary` + `fallbacks`, `imageModel`, model `alias` map, `skills` baseline, `thinkingDefault`/`verboseDefault`/`reasoningDefault`/`elevatedDefault`, `blockStreaming*`, `humanDelay`, `timeoutSeconds: 600`, `maxConcurrent`, `heartbeat`, `memorySearch`, and a `sandbox` block with `mode: "non-main"`, `scope: "session"`, and a `docker` sub-block); `agents.list` per-agent overrides; a top-level `tools` policy (`allow`/`deny`, `exec` timeouts, `elevated.allowFrom` per channel); `models` custom providers (`mode: "merge"`, `providers."custom-proxy"` with `baseUrl`/`apiKey`/`api`/`headers`/`models`); `cron` (`enabled`, `store`, `maxConcurrentRuns: 8`, `sessionRetention`, `runLog`); `hooks` webhooks (`path`, `token`, `presets: ["gmail"]`, `mappings`, a `gmail` sub-block with `topic`/`subscription`/`tailscale`); `gateway` (`mode: "local"`, `port: 18789`, `bind: "loopback"`, `controlUi`, `auth.mode: "token"`, `tailscale`, `remote`, `reload`); and `skills` (`allowBundled`, `load.extraDirs`/`allowSymlinkTargets`, `install.nodeManager`, `entries`). The illustrative sandbox + custom-provider slice:

```json5
sandbox: {
  mode: "non-main",
  scope: "session", // preferred over legacy perSession: true
  workspaceRoot: "~/.openclaw/sandboxes",
  docker: {
    image: "openclaw-sandbox:bookworm-slim",
    workdir: "/workspace",
    readOnlyRoot: true,
    tmpfs: ["/tmp", "/var/tmp", "/run"],
    network: "none",
    user: "1000:1000",
  },
},
// ...
models: {
  mode: "merge",
  providers: {
    "custom-proxy": {
      baseUrl: "http://localhost:4000/v1",
      apiKey: "LITELLM_KEY",
      api: "openai-responses",
      authHeader: true,
      headers: { "X-Proxy-Region": "us-west" },
      models: [{ id: "llama-3.1-8b", name: "Llama 3.1 8B", contextWindow: 128000, maxTokens: 32000 }],
    },
  },
},
```

## Common patterns

**Symlinked sibling skill repo** — use this when a built-in skill root contains a symlink into a sibling repo (e.g. `~/.agents/skills/manager -> ~/Projects/manager/skills`). Under `skills.load`, set `extraDirs: ["~/Projects/manager/skills"]` to scan the sibling repo as an explicit skill root, and `allowSymlinkTargets: ["~/Projects/manager/skills"]` to let symlinked skill folders resolve into that trusted real target root without allowing arbitrary symlink escapes. To let Skill Workshop apply write through the same trusted symlink target, set `skills.workshop.allowSymlinkTargetWrites: true`.

**Shared skill baseline with one override** — `agents.defaults.skills` is the shared baseline, `agents.list[].skills` replaces that baseline for one agent, and `skills: []` makes an agent see no skills:

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      skills: ["github", "weather"],
    },
    list: [
      { id: "main", default: true },
      { id: "docs", workspace: "~/.openclaw/workspace-docs", skills: ["docs-search"] },
    ],
  },
}
```

**Multi-platform setup** — one config fronting WhatsApp, Telegram, and Discord at once, each with its own `allowFrom`/token. Telegram and Discord set `enabled: true` plus their `botToken`/`token`; Discord scopes DMs via `dm: { allowFrom: [...] }`.

**Trusted node network auto-approval** — keep device pairing manual unless you control the network path. For a dedicated lab or tailnet subnet, opt in to first-time node device auto-approval with exact CIDRs or IPs under `gateway.nodes.pairing.autoApproveCidrs` (e.g. `["192.168.1.0/24", "fd00:1234:5678::/64"]`). This remains off when unset, only applies to fresh `role: node` pairing with no requested scopes, and operator/browser clients plus role/scope/metadata/public-key upgrades still require manual approval.

**Secure DM mode (shared inbox / multi-user DMs)** — if more than one person can DM your bot (multiple `allowFrom` entries, pairing approvals for multiple people, or `dmPolicy: "open"`), enable secure DM mode with `session.dmScope: "per-channel-peer"` so DMs from different senders don't share one context by default. For Discord/Slack/Google Chat/Microsoft Teams/Mattermost/IRC, sender authorization is ID-first by default; only enable direct mutable name/email/nick matching with each channel's `dangerouslyAllowNameMatching: true` if you explicitly accept that risk:

```json5
{
  session: { dmScope: "per-channel-peer" },
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15555550123", "+15555550124"],
    },
    discord: {
      enabled: true,
      token: "YOUR_DISCORD_BOT_TOKEN",
      dm: { enabled: true, allowFrom: ["123456789012345678", "987654321098765432"] },
    },
  },
}
```

**Anthropic API key + MiniMax fallback** — declare an `auth.profiles."anthropic:api"` (`mode: "api_key"`) with an `order.anthropic` list, register a custom `models.providers.minimax` (`baseUrl: "https://api.minimax.io/anthropic"`, `api: "anthropic-messages"`, `apiKey: "${MINIMAX_API_KEY}"`), then set `agents.defaults.model.primary: "anthropic/claude-opus-4-6"` with `fallbacks: ["minimax/MiniMax-M2.7"]` so MiniMax is the failover target.

**Work bot (restricted access)** — a restricted-access agent with `agents.defaults.elevatedDefault: "off"`, a `WorkBot` identity, and a Slack channel allowlist (`#engineering`/`#general` each `{ allow: true, requireMention: true }`).

**Local models only** — point `agents.defaults.model.primary` at a local model (`"lmstudio/my-local-model"`) and register a `models.providers.lmstudio` custom provider (`mode: "merge"`) targeting a self-hosted OpenAI-compatible endpoint (`baseUrl: "http://127.0.0.1:1234/v1"`, `api: "openai-responses"`) with the local model declared in `models[]`:

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace", model: { primary: "lmstudio/my-local-model" } } },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [{ id: "my-local-model", name: "Local Model", contextWindow: 196608, maxTokens: 8192 }],
      },
    },
  },
}
```

## Tips

If you set `dmPolicy: "open"`, the matching `allowFrom` list must include `"*"`. Provider IDs differ (phone numbers, user IDs, channel IDs) — use the provider docs to confirm the format. Optional sections to add later: `web`, `browser`, `ui`, `discovery`, `plugins`, `talk`, `signal`, `imessage`. See [Providers](https://docs.openclaw.ai/providers) and [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting) for deeper setup notes.

## Related Notes

**Terms**

- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — the gateway product; relevance: the configs being exemplified target OpenClaw.
- **[Skills](../../term_dictionary/term_skills.md)** — agent skill bundles; relevance: shared-skill-baseline / symlinked-sibling-skill-repo patterns are example recipes.
- **[Skill Manifest](../../term_dictionary/term_skill_manifest.md)** — skill declaration; relevance: the symlinked skill repo pattern relies on skill manifests.
- **[Claude](../../term_dictionary/term_claude.md)** — Anthropic model family; relevance: the Anthropic-API-key example pattern.
- **[Model Failover](../../term_dictionary/term_model_failover.md)** — provider switchover; relevance: the "API key + MiniMax fallback" recipe.
- **[Access Control](../../term_dictionary/term_access_control.md)** — authorization policy; relevance: work-bot restricted-access + secure-DM example patterns.
- **[DM Policy](../../term_dictionary/term_dm_policy.md)** — direct-message access rules; relevance: the secure-DM (shared inbox / multi-user DM) recipe.
- **[LLM](../../term_dictionary/term_llm.md)** — large language model; relevance: the local-models-only recipe.
- **[Chatbot](../../term_dictionary/term_chatbot.md)** — conversational bot; relevance: the multi-platform bot setup recipe.

**Docs**

- **[Claude Code — Settings Reference](../claude_code/cc_settings_reference.md)** — full settings map; relevance: the field vocabulary the expanded example uses.
- **[Claude Code — Settings Files](../claude_code/cc_settings_files.md)** — config layering; relevance: the shared-baseline + override pattern.
- **[Hermes — Profile Distribution Model](../hermes_agent/hermes_profile_distribution_model.md)** — shareable config profiles; relevance: analog to the shared-skill-baseline + multi-platform recipes.
- **[Hermes — Local/Self-Hosted LLM](../hermes_agent/hermes_local_self_hosted_llm.md)** — local-models setup; relevance: the local-models-only recipe.
- **[Hermes — Secrets (Bitwarden)](../hermes_agent/hermes_secrets_bitwarden.md)** — API-key/secret handling in config; relevance: the API-key example + secure secret storage.
- **[Pi — Cloud Providers](../pi/pi_cloud_providers.md)** — provider/fallback config; relevance: the API-key + fallback recipe.
- **[oc_gateway_configuration_overview](oc_gateway_configuration_overview.md)** — the page these examples support (planned, this series); relevance: examples realize the overview's edit paths.
- **[oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md)** — fields used in the expanded example (planned, this series); relevance: the field-level reference for each recipe key.
- **[oc_gateway_config_tools_policy](oc_gateway_config_tools_policy.md)** — tool-policy in the work-bot recipe (planned, this series); relevance: the restricted-tool patterns the work-bot recipe applies.
- **[oc_gateway_config_custom_providers](oc_gateway_config_custom_providers.md)** — provider config in the fallback recipe (planned, this series); relevance: the custom-provider/base-URL fields the fallback recipe uses.

**Repos**

- **[repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md)** — gateway runtime; relevance: consumes these example configs.
- **[repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md)** — skills layer; relevance: skill baseline/override patterns in the examples.
- **[repo_openclaw](../../../areas/code_repos/repo_openclaw.md)** — monorepo; relevance: the config root the examples write.

**Snippets**

- **[snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md)** — wizard-generated config; relevance: produces starter configs like the recommended-starter recipe.
- **[snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md)** — runtime config assembly; relevance: how an example config becomes runtime state.
- **[snippet_example_engine_agent_config_builder](../../code_snippets/snippet_example_engine_agent_config_builder.md)** — config builder; relevance: cross-engine view of composing a multi-section config.
- **[snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md)** — skill manifest format; relevance: the shared-skill-baseline / symlinked-skill-repo recipe.
- **[snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md)** — OpenAI provider config; relevance: the API-key provider example.
- **[snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md)** — local Ollama config; relevance: the local-models-only recipe.
- **[snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md)** — fallback activation; relevance: the API-key + fallback recipe behavior.
- **[snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md)** — model catalog; relevance: the multi-provider/model fields the expanded example sets.
- **[snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md)** — tool policy; relevance: the restricted-tool work-bot recipe.
- **[snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md)** — CLI routing; relevance: the `openclaw config set` one-liners that build these examples.

## References

- [OpenClaw Docs — Configuration examples](https://docs.openclaw.ai/gateway/configuration-examples)
- [OpenClaw Docs — Configuration](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Docs — Configuration reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw Docs — Providers](https://docs.openclaw.ai/providers)
- [OpenClaw Docs — Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)

**Source**: OpenClaw documentation — `gateway/configuration-examples` (mirror `inbox/openclaw_docs/gateway/configuration-examples.md`)
**Last Updated**: 2026-06-22
**Status**: Active
