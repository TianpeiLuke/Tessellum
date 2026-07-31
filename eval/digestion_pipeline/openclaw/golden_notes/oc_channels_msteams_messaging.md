---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - msteams
keywords:
  - msteams access control dmpolicy grouppolicy
  - teams rsc permissions vs microsoft graph
  - teams replystyle thread top-level
  - sending files in group chats sharepoint
  - teams polls adaptive cards presentation cards
  - msteams target formats user conversation
  - teams proactive messaging serviceurl
  - teams team channel id gotcha private channels
topics:
  - OpenClaw
  - Microsoft Teams Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/msteams
access_control_group: ["general"]
---

# OpenClaw — Microsoft Teams Messaging Behavior, Access Control, and Capabilities

## Overview

This is the day-to-day **messaging reference** for the OpenClaw Microsoft Teams channel — everything after the bot is connected (setup is `oc_channels_msteams_setup`; production auth is `oc_channels_msteams_federated_auth`). It mirrors the messaging/access half of `channels/msteams`: DM/group access control, member-info + history context, RSC manifest permissions and the RSC-vs-Graph capability split, Graph media/history, known limitations (webhook timeouts, Teams cloud/`serviceUrl`), routing/sessions, reply style, attachments, SharePoint group-chat file sending, polls + presentation cards, target formats, proactive messaging, team/channel ID gotchas, private channels, and troubleshooting. Config keys, RSC names, and target grammars below are verbatim from source.

## Access control (DMs + groups)

**DM access.** Default `channels.msteams.dmPolicy = "pairing"` — unknown senders ignored until approved. `channels.msteams.allowFrom` should use stable AAD object IDs or static sender access groups (`accessGroup:core-team`). Do not rely on UPN/display-name matching (it can change); OpenClaw disables direct name matching by default — opt in via `channels.msteams.dangerouslyAllowNameMatching: true`. The wizard resolves names to IDs via Microsoft Graph when credentials allow.

**Group access.** Default `channels.msteams.groupPolicy = "allowlist"` (blocked unless you add `groupAllowFrom`; `channels.defaults.groupPolicy` overrides when unset). `channels.msteams.groupAllowFrom` controls which senders/access groups (AAD object ID or `accessGroup:core-team`) can trigger in group chats/channels (falls back to `allowFrom`). Set `groupPolicy: "open"` for any member (still mention-gated); `groupPolicy: "disabled"` allows **no channels**.

**Teams + channel allowlist.** Scope group/channel replies by listing teams/channels under `channels.msteams.teams`; keys should use stable Teams conversation IDs from links, not mutable display names. When `groupPolicy="allowlist"` with a teams allowlist present, only listed teams/channels are accepted (mention-gated). On startup OpenClaw resolves team/channel and user allowlist names to IDs (when Graph permits) and logs the mapping; unresolved names are kept as typed but ignored for routing unless `dangerouslyAllowNameMatching: true`.

## Member info action and history context

The Graph-backed `member-info` action resolves channel member details (display name, email, role) from Microsoft Graph. It requires `Member.Read.Group` RSC (in the recommended manifest), and for cross-team lookups `User.Read.All` Graph **Application** permission with admin consent. Gated by `channels.msteams.actions.memberInfo` (default enabled when Graph credentials exist).

History context uses `channels.msteams.historyLimit` (recent channel/group messages wrapped into the prompt), falling back to `messages.groupChat.historyLimit`; set `0` to disable (default 50). Fetched thread history is filtered by sender allowlists (`allowFrom` / `groupAllowFrom`); quoted attachment context (`ReplyTo*` from Teams reply HTML) is passed as received. DM history is limited with `channels.msteams.dmHistoryLimit` (user turns); per-user overrides via `channels.msteams.dms["<user_id>"].historyLimit`.

## Current Teams RSC permissions (manifest)

The existing `resourceSpecific` permissions (all Application) apply only inside the installed team/chat. **For channels (team scope):** `ChannelMessage.Read.Group` (receive all channel messages without @mention), `ChannelMessage.Send.Group`, `Member.Read.Group`, `Owner.Read.Group`, `ChannelSettings.Read.Group`, `TeamMember.Read.Group`, `TeamSettings.Read.Group`. **For group chats:** `ChatMessage.Read.Chat` (receive all group chat messages without @mention). Add one via the Teams CLI: `teams app rsc add <teamsAppId> ChannelMessage.Read.Group --type Application`.

Manifest must-haves: `bots[].botId` and `webApplicationInfo.id` **must** match the Azure Bot App ID; `bots[].scopes` must include the surfaces used (`personal`, `team`, `groupChat`); `bots[].supportsFiles: true` is required for personal-scope file handling; `authorization.permissions.resourceSpecific` must include channel read/send for channel traffic. To update an installed app: `teams app manifest download <teamsAppId> manifest.json`, edit, then `teams app manifest upload manifest.json <teamsAppId>` (version auto-bumped); reinstall in each team and **fully quit and relaunch Teams** to clear cached metadata.

## Capabilities: RSC only vs Microsoft Graph

**With Teams RSC only** (no Graph permissions) you can read/send channel **text** and receive **personal (DM)** file attachments; you canNOT access channel/group **image or file contents** (HTML stub only), download SharePoint/OneDrive attachments, or read history beyond the live webhook event. **With RSC + Microsoft Graph Application permissions** you additionally download hosted contents (pasted images), SharePoint/OneDrive file attachments, and channel/chat history. In short: RSC is real-time listening (via webhook, app-manifest-only, must be running); Graph API is historical access (query anytime, needs admin consent + token flow). Offline catch-up needs `ChannelMessage.Read.All` (admin consent).

**Graph-enabled media + history (required for channels).** To get images/files in **channels** or fetch **history**: (1) add Graph **Application permissions** `ChannelMessage.Read.All` (channel attachments + history) and `Chat.Read.All` or `ChatMessage.Read.All` (group chats); (2) **grant admin consent**; (3) bump the **manifest version**, re-upload, **reinstall in Teams**; (4) **fully quit and relaunch Teams**. @mentions work for in-conversation users; to mention users **not in** it, add `User.Read.All` (Application) with admin consent.

## Known limitations: webhook timeouts and Teams cloud / serviceUrl

**Webhook timeouts.** Teams delivers messages via HTTP webhook; slow processing (e.g. slow LLM responses) can cause gateway timeouts, Teams retries (duplicates), or dropped replies. OpenClaw mitigates by returning quickly and replying proactively, but very slow responses may still fail.

**Teams cloud and service URL support.** The SDK-backed path is live-validated for public cloud. Inbound replies use the incoming Teams SDK turn context; out-of-context proactive operations (sends, edits, deletes, cards, polls, file-consent messages, queued long-running replies) use the stored conversation reference `serviceUrl`. Public cloud is the default (host `https://smba.trafficmanager.net/`) and needs no `channels.msteams.cloud` / `serviceUrl`. For non-public clouds, `channels.msteams.cloud` selects the Teams SDK preset (auth, JWT validation, token services, Graph scope) and `channels.msteams.serviceUrl` selects the Bot Connector boundary validated before proactive operations (see table); China/21Vianet uses the SDK `China` preset, accepts service URLs only on Azure China Bot Framework hosts (`*.botframework.azure.cn`), and disables Graph helpers until Azure China Graph routing exists.

| Teams environment | OpenClaw config | Proactive `serviceUrl` |
|---|---|---|
| Public | no cloud/serviceUrl config needed | `https://smba.trafficmanager.net/teams` |
| GCC | set `serviceUrl`; no separate SDK cloud preset | `https://smba.infra.gcc.teams.microsoft.com/teams` |
| GCC High | `cloud: "USGov"` + `serviceUrl` | `https://smba.infra.gov.teams.microsoft.us/teams` |
| DoD | `cloud: "USGovDoD"` + `serviceUrl` | `https://smba.infra.dod.teams.microsoft.us/teams` |
| China/21Vianet | `cloud: "China"` | use the incoming activity's `serviceUrl` |

When a service URL is configured OpenClaw checks the stored `serviceUrl` uses the same host before proactive operations; the default public-cloud config fails closed if a stored conversation points outside the public host. After changing cloud/serviceUrl settings, receive a fresh message so the stored reference is current.

**Formatting.** Teams markdown is more limited than Slack/Discord: basic (**bold**, _italic_, `code`, links) works, complex markdown (tables, nested lists) may not render; Adaptive Cards back polls and presentation sends.

## Routing and sessions; reply style: threads vs posts

Session keys follow the standard agent format (`/concepts/session`): DMs share the main session (`agent:<agentId>:<mainKey>`); channel/group messages use the conversation id — `agent:<agentId>:msteams:channel:<conversationId>` / `...:group:<conversationId>`.

Teams has two channel UI styles over one data model: **Posts** (classic — cards with threaded replies, recommended `replyStyle: thread`, the default) and **Threads** (Slack-like linear flow, recommended `replyStyle: top-level`). The Teams API does not expose which style a channel uses, so the wrong `replyStyle` mis-renders replies. Configure it per-channel; the value resolves most-specific-first (first non-`undefined` wins): per-channel `channels.msteams.teams.<teamId>.channels.<conversationId>.replyStyle` → per-team `...teams.<teamId>.replyStyle` → global `channels.msteams.replyStyle` → implicit default from `requireMention` (`true` → `thread`, `false` → `top-level`). Setting `requireMention: false` globally without an explicit `replyStyle` surfaces Posts-style mentions as top-level posts, so pin `replyStyle: "thread"` to avoid surprises.

With `replyStyle: "thread"`, when @mentioned inside a channel thread OpenClaw re-attaches the thread root to the outbound conversation reference (`19:…@thread.tacv2;messageid=<root>`) so the reply lands in the same thread — for live and proactive sends after the turn context expires (long-running agents, queued tool-call replies via `mcp__openclaw__message`). The thread root comes from the stored `threadId`; older references fall back to `activityId`. With `replyStyle: "top-level"`, channel-thread inbounds become new top-level posts (no thread suffix) — correct for Threads-style channels.

## Attachments, images, and sending files in group chats

In **DMs** images/attachments work via Teams bot file APIs; in **channels/groups** attachments live in M365 storage (SharePoint/OneDrive) and the webhook payload only includes an HTML stub, so **Graph API permissions are required** to download them (without Graph, channel images arrive text-only). For file-first sends use `action=upload-file` with `media` / `filePath` / `path`; optional `message` is accompanying text, `filename` overrides the uploaded name. OpenClaw downloads media only from Microsoft/Teams hostnames by default — override via `channels.msteams.mediaAllowHosts` (`["*"]` for any) — and attaches Authorization headers only for hosts in `channels.msteams.mediaAuthAllowHosts` (Graph + Bot Framework; keep strict).

Bots send DM files via the FileConsentCard flow (built-in), but **group chats/channels** need extra setup: bots have no personal OneDrive (`/me/drive` does not work for application identities), so the bot uploads to a **SharePoint site** and creates a sharing link. Setup: (1) add Graph permissions `Sites.ReadWrite.All` (Application, upload) and optionally `Chat.Read.All` (per-user sharing links); (2) grant admin consent; (3) get the site ID via Graph (`/v1.0/sites/{hostname}:/{site-path}` returns `"id": "contoso.sharepoint.com,guid1,guid2"`); (4) set `channels.msteams.sharePointSiteId`. `Sites.ReadWrite.All` alone yields an org-wide link; adding `Chat.Read.All` upgrades to a per-user link (only chat members access); missing it falls back to org-wide. Fallback: group chat + `sharePointSiteId` → SharePoint upload + link; group chat + no `sharePointSiteId` → attempt OneDrive (may fail), text only; personal chat + file → FileConsentCard; any image → base64 inline. Files land in `/OpenClawShared/` in the site's default document library.

## Polls, presentation cards, and target formats

**Polls (Adaptive Cards).** OpenClaw sends Teams polls as Adaptive Cards (no native Teams poll API). CLI: `openclaw message poll --channel msteams --target conversation:<id> ...`. Votes are recorded in OpenClaw plugin-state SQLite under `state/openclaw.sqlite`; existing `msteams-polls.json` files are imported by `openclaw doctor --fix`, not the running plugin. The gateway must stay online to record votes; polls do not auto-post result summaries and there is no poll-results CLI.

**Presentation cards.** Send semantic presentation payloads via the `message` tool, CLI, or normal reply — OpenClaw renders them as Teams Adaptive Cards from the generic presentation contract. The `presentation` parameter accepts semantic blocks (message text optional); buttons become Adaptive Card submit/URL actions, and select menus (not yet native) are downgraded to readable text.

**Target formats.** MSTeams targets use prefixes: `user:<aad-object-id>` (e.g. `user:40a1a0ed-4ff2-4164-a219-55518990c197`); `user:<display-name>` (requires Graph API, e.g. `user:John Smith`); `conversation:<conversation-id>` for group/channel; and the raw `<conversation-id>` if it contains `@thread`. Without the `user:` prefix, names default to group/team resolution, so always use `user:` for people by display name. Example send with a presentation card:

```bash
openclaw message send --channel msteams \
  --target "conversation:19:abc...@thread.tacv2" \
  --presentation '{"title":"Hello","blocks":[{"type":"text","text":"Hello!"}]}'
```

## Proactive messaging, team/channel IDs, and private channels

**Proactive messaging.** Proactive messages are only possible **after** a user has interacted, since OpenClaw stores conversation references then. See `/gateway/configuration` for `dmPolicy`/allowlist gating.

**Team and Channel IDs (common gotcha).** The `groupId` query parameter in Teams URLs is **NOT** the team ID used for config — extract IDs from the URL path: the team key is the segment after `/team/` (URL-decoded, e.g. `19:Bk4j...@thread.tacv2`; older tenants may show `@thread.skype`, also valid); the channel key is the segment after `/channel/` (URL-decoded). **Ignore** `groupId` for routing — it is the Microsoft Entra group ID, not the Bot Framework conversation ID in incoming activities.

**Private channels.** Bots have limited support: installation Limited, real-time webhook messages May not work, RSC permissions May behave differently, @mentions only If bot is accessible, Graph API history Yes (with permissions). Workarounds: use standard channels, use DMs, or Graph API for history (`ChannelMessage.Read.All`).

## Troubleshooting

**Common issues.** Images not showing in channels → Graph permissions/admin consent missing (reinstall, fully quit/reopen Teams). No responses in channel → mentions required by default; set `channels.msteams.requireMention=false`. Old manifest still shown → remove + re-add the app, fully quit Teams. 401 Unauthorized from webhook → expected when testing without Azure JWT (endpoint reachable, auth failed); test via Web Chat.

**Manifest upload errors.** "Icon file cannot be empty" → 0-byte icons; create valid PNGs (32x32 `outline.png`, 192x192 `color.png`). "webApplicationInfo.Id already in use" → still installed elsewhere; uninstall or wait 5-10 min. "Something went wrong" → upload via `https://admin.teams.microsoft.com`, open DevTools → Network, check the response body. Sideload failing → use "Upload an app to your org's app catalog".

**RSC permissions not working.** (1) Verify `webApplicationInfo.id` matches the bot App ID exactly; (2) re-upload and reinstall; (3) check whether org admin blocked RSC; (4) confirm scope — `ChannelMessage.Read.Group` for teams, `ChatMessage.Read.Chat` for group chats.

**Source**: OpenClaw documentation — `channels/msteams` (mirror `inbox/openclaw_docs/channels/msteams.md`)
**Last Updated**: 2026-06-22
**Status**: Active
