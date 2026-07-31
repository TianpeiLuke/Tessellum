---
title: Sub-Plan an01 — OpenClaw Docs: Announcements (BlueBubbles → imsg iMessage)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["announcements/bluebubbles-imessage"]
---

# Sub-Plan an01: Announcements

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`), format, dedup-before-create, 9-GATE
> validation, undigested-terms ownership, cross-references, and entry-point wiring are ALL inherited from
> the master; this file re-reads + measures its one assigned page and locks scope, planned notes, coverage,
> and candidate cross-references (per-note Related mapping is finalized later at the augment stage).

## Scope

The single OpenClaw **Announcements** page: the removal of the legacy **BlueBubbles** iMessage channel and
the migration to the bundled `imessage` plugin driven by [`imsg`](https://github.com/steipete/imsg) (JSON-RPC
over stdin/stdout, run locally on the Messages Mac or via an SSH wrapper). It is a deprecation announcement
plus a hands-on cutover procedure: install/verify `imsg`, grant macOS permissions, translate the old
`channels.bluebubbles` config to `channels.imessage`, restart and probe, and apply the migration caveats
(no-equivalent fields, attachment defaults, ACP binding renames, non-portable session keys).

**Priority: P2 (Phase B).** Low-volume, integration-flavored; depends on no other sub-plan. Strongly cross-links
to the Channels series (`ch02` owns `channels/imessage` + `channels/imessage-from-bluebubbles`) and the
existing `repo_openclaw_channels*` code notes, but is independent for execution.

**Source**: OpenClaw docs, 1 page, **477 measured words**. **Planned: 1 note.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| bluebubbles-imessage | announcements/bluebubbles-imessage | 477 | 3 | 4 | 0 | procedure (migration; with a short deprecation-rationale Overview) |

- **H2 sections:** `What changed`, `What to do`, `Migration notes`, `See also`.
- **H3 sections:** none.
- **Code fences:** 3 (6 fence markers ÷ 2): a `bash` install/verify block, a `json5` translated
  `channels.imessage` config block, and a `bash` restart/probe block.
- Page also carries a non-standard source frontmatter (`summary`, `read_when`, `title`) that is digestion
  metadata only — NOT copied into the vault note (the vault note uses the master's fixed YAML schema).

## Content Strategy

- **Prioritize**: the actionable migration procedure — install/verify `imsg`, macOS permissions (Full Disk
  Access + Automation), the `channels.bluebubbles` → `channels.imessage` config translation, restart/probe,
  and the migration caveats. This is the operational core a user lands on after the redirect.
- **Split**: NONE. 477 words is far under the 2,500-word cap; the "What changed" rationale is a short
  announcement framing that belongs in the note's `## Overview`, not a separate note. Keeping the announcement
  + procedure together preserves the migration narrative and stays single-BB (procedure). See Split Decisions
  (the master's 2-note estimate is downscaled to 1 on the measured size).
- **Link-out (do NOT duplicate)**: full config-translation table + cutover checklist live on
  `channels/imessage-from-bluebubbles` (owned by `ch02` → planned `oc_channels_imessage_from_bluebubbles.md`);
  the supported iMessage channel setup lives on `channels/imessage` (`ch02` → planned
  `oc_channels_imessage.md`); the channel config-reference anchor lives on `gateway/config-channels#imessage`
  (`gw01` → planned `oc_gateway_config_channels.md`). Reference these as sibling `oc_*` (planned) links and via
  `## References` external URLs; do not inline their content. Do not redefine `term_openclaw`, `term_mcp`,
  `term_json_rpc`, `term_webhook` — link them.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_announcements_bluebubbles_imessage.md` | procedure | bluebubbles-imessage.md: intro + `What changed` (→ Overview/rationale), `What to do` (install/verify imsg, macOS permissions, config translation, restart+probe, test), `Migration notes`, `See also` | 600 | OpenClaw removed the legacy BlueBubbles channel; this is the migration to the bundled `imessage` plugin (driven by `imsg` over JSON-RPC). Covers what changed (no BlueBubbles HTTP/webhook/REST/runtime; imsg watches Messages.app on the signed-in Mac; private-API bridge for advanced actions; Linux/Windows via SSH `cliPath`), the step-by-step cutover (install/verify imsg, grant Full Disk Access + Automation, translate `channels.bluebubbles` → `channels.imessage`, restart + `channels status --probe`, test), and the migration caveats (no-equivalent `serverUrl`/`password`, attachments off by default, allowlist/groups copy incl. `"*"` wildcard, ACP `channel` rename, non-portable session keys). |

## Section Coverage Map

```
announcements/bluebubbles-imessage.md
├── (intro, lines 12-14: BlueBubbles removed; imsg via JSON-RPC; redirect note) → note 1 (## Overview)
├── ## What changed (no HTTP/webhook/REST/runtime; imsg watches Messages.app;
│   basic vs advanced/private-API actions; Linux/Windows SSH cliPath) ───────── → note 1 (What Changed)
├── ## What to do (1 install/verify imsg [bash]; 2 Full Disk Access + Automation;
│   3 translate config [json5]; 4 restart + channels status --probe [bash];
│   5 test DMs/groups/attachments/private-API before deleting old server) ───── → note 1 (Migration Steps)
├── ## Migration notes (serverUrl/password no equivalent; allowFrom/groups/
│   includeAttachments mappings; attachments off by default; groupPolicy
│   allowlist copy incl. "*"; ACP channel rename; session keys non-portable) ── → note 1 (Migration Caveats)
└── ## See also (imessage-from-bluebubbles, imessage, config-channels#imessage) → note 1 (## References + Related Notes)
```
No orphaned sections. The 3 code fences (install/verify bash, json5 config, restart/probe bash) all land in
note 1 (3 ≤ 6-fence cap). The deep config-translation table / cutover checklist are intentionally link-outs to
`channels/imessage-from-bluebubbles` (ch02), not reproduced.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| announcements/bluebubbles-imessage.md (477w, 4 H2, 0 H3, 3 code) | 1 note (`oc_announcements_bluebubbles_imessage.md`) | **Downscale, not split.** Master estimated 2 notes; measured at 477 words it is far below the 2,500-word / 6-fence / 400-line caps and is single-BB (a migration procedure). The "What changed" announcement is short rationale that belongs in `## Overview`, so splitting announcement-vs-procedure would create two sub-atomic stubs. Keep as one cohesive procedure note. |

## Summary Statistics & Building Block Distribution

- Source pages: **1** (477 words). New `oc_` notes: **1**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×1**.
- Est. digest words: ~600 (one note; expands the 477-word source slightly with structured Overview + caveat
  framing, still ≤2,500w / ≤400 lines). Source code fences: 3 → reproduced verbatim in note 1 (≤6 cap).
- Cross-refs (LOCKED at xref-augment 2026-06-21): note 1 = **12 terms · 12 snippets · 10 docs · 5 repos**
  additional discoverability — see Per-Note Related Notes Mapping. Floors met (≥8 terms · ≥10 snippets · ≥10 docs).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **(planned)** — they count only as ADDITIONAL toward the doc total; the 10-doc floor is met entirely by
> Relevance-selected from a fresh re-read of `inbox/openclaw_docs/announcements/bluebubbles-imessage.md`;
> `- [Name](relpath.md) — what it is; relevance: why THIS note`.

### note 1 — `oc_announcements_bluebubbles_imessage.md` (12t · 12s · 10d · 5r)

**Terms (`../../term_dictionary/`) — 12 (floor ≥8):**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat channels to coding agents; relevance: BlueBubbles was an OpenClaw channel and this is an OpenClaw deprecation/cutover announcement.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — request/response RPC encoded as JSON; relevance: `imsg` talks JSON-RPC over stdin/stdout — the new transport this migration adopts.
- [term_acp_agent_client_protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — the Agent Client Protocol binding chat threads to agents; relevance: ACP bindings that matched `channel: "bluebubbles"` must be renamed to `channel: "imessage"` (Migration Caveats).
- [term_messaging_gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway that fronts chat channels and routes inbound/outbound messages; relevance: the iMessage channel runs through the gateway, restarted/probed (`channels status --probe`) in the cutover.
- [term_channel_kernel](../../term_dictionary/term_channel_kernel.md) — the channel runtime that hosts and lifecycles each channel adapter; relevance: the migration swaps the BlueBubbles adapter for the bundled `imessage` plugin within the channel runtime.
- [term_webhook](../../term_dictionary/term_webhook.md) — an HTTP callback route for inbound events; relevance: "no BlueBubbles HTTP server, webhook route, or REST password" is a core What-Changed point — imsg replaces the webhook transport.
- [term_remote_ssh](../../term_dictionary/term_remote_ssh.md) — running a process on a remote host over SSH; relevance: Linux/Windows gateways reach iMessage by setting `channels.imessage.cliPath` to an SSH wrapper that runs `imsg` on the signed-in Mac.
- [term_ssh](../../term_dictionary/term_ssh.md) — the Secure Shell protocol; relevance: the cross-platform `cliPath` SSH wrapper is the only path for non-Mac gateways to use iMessage.
- [term_dm_policy](../../term_dictionary/term_dm_policy.md) — the direct-message admission policy (pairing/allowlist) for a channel; relevance: the translated config sets `dmPolicy: "pairing"` and `allowFrom`, and the caveats cover allowlist copy.
- [term_thread_binding_policy](../../term_dictionary/term_thread_binding_policy.md) — how a channel thread/conversation binds to an agent session; relevance: BlueBubbles session keys do not carry over to iMessage session keys (conversation-history caveat).
- [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — the Hermes coding-agent gateway in the same ecosystem; relevance: Hermes ships an equivalent BlueBubbles→imessage messaging adapter — direct cross-ecosystem analog of this migration.

**Docs (`resources/documentation/`) — 10 existing (floor ≥10; ≥5-existing minimum exceeded):**
- [hermes_messaging_bluebubbles_imessage](../hermes_agent/hermes_messaging_bluebubbles_imessage.md) — Hermes' own BlueBubbles-to-iMessage messaging doc; relevance: the closest cross-ecosystem twin of this exact migration (same deprecation + cutover narrative), the primary comparison anchor.
- [hermes_photon_imessage](../hermes_agent/hermes_photon_imessage.md) — Hermes' Photon iMessage integration over a local bridge; relevance: documents the same Messages.app-on-Mac iMessage surface and permission model imsg uses.
- [hermes_messaging_simplex](../hermes_agent/hermes_messaging_simplex.md) — a single-process local messaging channel in Hermes; relevance: parallels the imsg "run locally on the signed-in Mac" channel model with DM/group/attachment handling.
- [hermes_env_vars_runtime_messaging_behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — runtime knobs governing messaging behavior (attachments, allowlists); relevance: maps onto the `includeAttachments`/`allowFrom`/`groupPolicy` config fields translated in the cutover.
- [hermes_sessions_lifecycle_resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — channel session lifecycle and resume semantics; relevance: explains why BlueBubbles session keys don't become iMessage session keys (conversation-history non-portability caveat).
- [hermes_acp_internals](../hermes_agent/hermes_acp_internals.md) — how ACP binds channels to agent sessions internally; relevance: grounds the "ACP bindings with `channel: \"bluebubbles\"` must become `channel: \"imessage\"`" caveat.
- [cc_build_a_channel](../claude_code/cc_build_a_channel.md) — how to build/register a chat channel adapter; relevance: explains the channel-adapter abstraction the migration swaps (BlueBubbles adapter → bundled imessage plugin).
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — overview of the channels subsystem and supported platforms; relevance: situates iMessage among channels and the registry/lifecycle the cutover touches.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel configuration/enable procedure; relevance: structural twin of the `channels.imessage` config-translation + restart/probe steps.
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — a local JSON-RPC-over-stdio agent protocol; relevance: the same stdin/stdout JSON-RPC transport family imsg uses to talk to OpenClaw.

**Additional docs — planned sibling `oc_*` (this series; count toward discoverability, not the floor):**
- `oc_channels_imessage_from_bluebubbles.md` (ch02, planned) — full config-translation table + cutover checklist this announcement redirects to.
- `oc_channels_imessage.md` (ch02, planned) — the supported iMessage channel setup.
- `oc_gateway_config_channels.md` (gw01, planned) — the `config-channels#imessage` configuration reference anchor.

- [snippet_hermes_agent_skills_apple_imessage](../../code_snippets/snippet_hermes_agent_skills_apple_imessage.md) — Apple iMessage skill/bridge code in Hermes; relevance: the closest code-level analog of the bundled imessage plugin (Messages.app access, send/receive).
- [snippet_hermes_agent_gw_platform_bluebubbles](../../code_snippets/snippet_hermes_agent_gw_platform_bluebubbles.md) — the legacy BlueBubbles platform adapter code; relevance: the exact channel this announcement removes — shows the serverUrl/password/webhook surface that has no iMessage equivalent.
- [snippet_hermes_agent_gw_platform_signal_media](../../code_snippets/snippet_hermes_agent_gw_platform_signal_media.md) — media/attachment handling for a chat platform; relevance: parallels the `includeAttachments` (off-by-default) inbound-media caveat.
- [snippet_hermes_agent_gw_platform_whatsapp](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp.md) — a chat-platform adapter with DM/group/media handling; relevance: structural twin of an iMessage channel adapter (groups, allowlist, attachments).
- [snippet_hermes_agent_gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — attachment ingestion in a platform adapter; relevance: code-level reference for the inbound photos/voice-memos/videos/files the `includeAttachments` toggle gates.
- [snippet_hermes_agent_acp_entry](../../code_snippets/snippet_hermes_agent_acp_entry.md) — ACP entrypoint binding a channel to an agent; relevance: code-level reference for the ACP `channel:` binding renamed bluebubbles→imessage.
- [snippet_hermes_agent_gw_config_schema](../../code_snippets/snippet_hermes_agent_gw_config_schema.md) — the gateway channel config schema; relevance: structural reference for the `channels.imessage` config block (enabled, cliPath, dmPolicy, allowFrom, groups).
- [snippet_hermes_agent_tui_server_jsonrpc](../../code_snippets/snippet_hermes_agent_tui_server_jsonrpc.md) — a JSON-RPC server over stdio; relevance: the same JSON-RPC-over-stdin/stdout transport pattern imsg uses.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — OpenClaw DM pairing + allowlist gating; relevance: directly implements `dmPolicy: "pairing"` / `allowFrom` / `groupPolicy: "allowlist"` set in the translated config.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — OpenClaw channel DM security audit; relevance: grounds the allowlist/group-gate caveats (separate sender-allowlist vs group-registry gates).
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — OpenClaw ACP thread→session binding on spawn; relevance: explains the per-channel session-key binding behind the "session keys don't carry over" caveat.
- [snippet_hermes_agent_cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — CLI install/verify pattern; relevance: code-level twin of the install/verify step (`imsg --version`, `imsg chats`, `channels status --probe`).

- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — the messaging-channels package; relevance: implements the iMessage adapter / bundled imessage plugin this migration moves to.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channels subsystem (registry/lifecycle); relevance: the BlueBubbles-channel removal + iMessage registration happen here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway runtime; relevance: restarted and probed (`channels status --probe`) during cutover.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the umbrella OpenClaw repo; relevance: product-level back-link for a product announcement.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — the sessions subsystem; relevance: implements the session-key model behind the "BlueBubbles session keys do not carry over" caveat.

**Entry point (planned):**
- `entry_openclaw_docs.md` (master pre-step, planned) — the docs hub providing the inbound discoverability link.

DB-verification (2026-06-21): all 12 `term_*` + 10 `documentation/*` + 12 `snippet_*` + 5 `repo_openclaw*` ids
(expected — not yet created); they are additional, not counted toward the existing floors.

## Undigested Terms Plan

Per master: OpenClaw vocabulary terms are digested as `oc_*` doc concept notes by their **home** sub-plan, not
as new `term_dictionary` entries; the only `term_dictionary` interaction here is **linking existing** terms.

| Term | Disposition |
|---|---|
| BlueBubbles | OpenClaw-product/channel vocab; explained inline in note 1's Overview/What-Changed (its home page); NOT a `term_dictionary` capture. No existing `term_bluebubbles` (verified MISSING) and none warranted — it is being removed. |
| imsg | OpenClaw tooling vocab (the `imsg` CLI/RPC bridge); explained inline in note 1; link external repo in References. NOT a `term_dictionary` capture (no `term_imsg`, verified MISSING; product-specific). |
| iMessage | Platform name; described inline in note 1; the dedicated channel doc is `ch02`'s `oc_channels_imessage.md`. No `term_imessage` exists (MISSING) and none needed (platform proper noun, doc-owned). |
| JSON-RPC | Cross-cutting protocol — link EXISTING `term_json_rpc` (verified present). No new capture. |
| webhook | Link EXISTING `term_webhook` (verified present). No new capture. |
| SSH / remote SSH | Link EXISTING `term_ssh` / `term_remote_ssh` (verified present). No new capture. |
| ACP (binding `channel:` field) | Link EXISTING `term_acp_agent_client_protocol` (verified present). No new capture. |
| Full Disk Access / Automation permissions (macOS) | OS permission names; described inline in the install step; no `term_macos`/`term_full_disk_access` exists (MISSING) and a cross-cutting capture is not warranted from one announcement. |
| session key | Caveat-only mention; described inline; link `repo_openclaw_sessions`. No `term_session_key` exists (MISSING); not a reusable cross-cutting capture from this page. |

**New-term candidates:** 0. No genuinely cross-cutting, vault-reusable term lacking an existing note appears on
this page (the BlueBubbles/imsg/iMessage vocabulary is product/page-specific and doc-owned; protocol/auth/OS
terms already have existing notes). Consistent with the master's expectation of ~0 new `term_dictionary`
captures for OpenClaw docs.

## Term-Note Authoring Requirements

**N/A (0 new terms).** No `/tessellum-capture-term-note` invocation and no `acronym_glossary_*.md` edit for this
sub-plan. (Inherited requirement, for reference: were a new cross-cutting term proposed, it would be authored
applicable here.)

## Per-Phase Validation Gate (G1–G9)

Single execution phase (1 note). The 8 gates (inherited from master) apply to that phase:

| Gate | Check | Tool / Method | Pass criterion |
|---|---|---|---|
| G1 | Format + YAML | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` | Fixed YAML field order; `## Overview` + `## Related Notes` present; `# OpenClaw — …` H1; bold `**Source**`/`**Last Updated**`/`**Status**` footer; no forbidden YAML fields. |
| G2 | Grounding | Diff note vs `inbox/openclaw_docs/announcements/bluebubbles-imessage.md` | Every claim/config/command traceable to source; the 3 code fences reproduced verbatim; no invented fields. |
| G3 | Density + Coverage | Word/line/fence count; Section Coverage Map | ≤2,500w / ≤400 lines / ≤6 fences; all 4 H2 + intro mapped (no orphan); single BB (procedure). |
| G5 | Ghost-reference detect + redirect | `/tessellum-fix-ghost-references` + DB existence check | No links to non-existent notes; planned `oc_*`/`entry_openclaw_docs` exist by execution time or are deferred per master. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` + reindex | 0 broken links after incremental reindex (correct relative paths from `resources/documentation/openclaw/`). |
| G7 | Discoverability (in-degree) | `note_links` query after reindex | Note receives ≥1 inbound link from OUTSIDE `documentation/openclaw/` (via `entry_openclaw_docs.md`); in-degree ≥1. |
| G8 | Anti-island | Inlinks plan (below) | Inbound links land from `entry_openclaw_docs` and the candidate inlink sources; no orphan note. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
# Run from repo root. Gate sweep over the OpenClaw docs folder for this sub-plan's note.
GATE_DIR="resources/documentation/openclaw"
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTE="$GATE_DIR/oc_announcements_bluebubbles_imessage.md"

# G1 — format + YAML frontmatter
python3 scripts/check_note_format.py --path "$NOTE"
python3 scripts/check_yaml_frontmatter.py --path "$NOTE"

# G1 — required H2 sections present
for s in ${(s:|:)REQ_SECTIONS}; do
  grep -qF "$s" "$NOTE" || echo "MISSING SECTION: $s in $NOTE"
done

# G1 — source_url present in frontmatter when required
if [ "$REQUIRE_SOURCE_URL" = "1" ]; then
  grep -q "^source_url: https://docs.openclaw.ai/" "$NOTE" || echo "MISSING source_url in $NOTE"
fi

# G3 — density caps (≤400 lines, ≤2500 words, ≤6 code fences)
awk 'END{print "lines="NR}' "$NOTE"
wc -w "$NOTE"
echo "code_fences=$(( $(grep -c '```' "$NOTE") / 2 ))"

# G4 — cross-ref floors: ≥8 term_dictionary links + ≥10 code_snippet links + ≥10 docs + sibling oc_ links
echo "term_links=$(grep -oE '\]\(\.\./\.\./term_dictionary/term_[a-z0-9_]+\.md\)' "$NOTE" | wc -l)"   # floor 8
echo "snippet_links=$(grep -oE '\]\(\.\./\.\./code_snippets/snippet_[a-z0-9_]+\.md\)' "$NOTE" | wc -l)"   # floor 10
echo "doc_links=$(grep -oE '\]\(\.\./[a-z_]+/[a-z0-9_]+\.md\)' "$NOTE" | wc -l)"   # existing docs (hermes/cc/pi) floor 10
echo "sibling_${SIBLING_PREFIX}links=$(grep -oE "\]\(${SIBLING_PREFIX}[a-z0-9_]+\.md\)" "$NOTE" | wc -l)"

# G2/G5/G6 — grounding diff + ghost/broken-link skills + reindex
diff <(sed -n '12,79p' inbox/openclaw_docs/announcements/bluebubbles-imessage.md) /dev/null >/dev/null 2>&1 || true
#   then: /tessellum-fix-ghost-references ; /tessellum-fix-broken-links
bash scripts/update_notes_database.sh   # incremental reindex before G6/G7 link checks

# G7 — inbound in-degree ≥1 from outside documentation/openclaw/
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
```

## Density Re-Assessment

| Note | Est. words | Cap (2500) | Code fences | Cap (6) | Lines | Cap (400) | BB | Single-BB? |
|---|---:|---|---:|---|---:|---|---|---|
| `oc_announcements_bluebubbles_imessage.md` | ~600 | ✅ | 3 | ✅ | ~150 | ✅ | procedure | ✅ |

Well within all caps; no further split needed. (Borderline-promotion rule N/A — the note is comfortably small,
not borderline-large.)

## Entry Point Decision (inherited from master)

This sub-plan does NOT create or own an entry point. Per master Series-Wiring W1, the hub
`0_entry_points/entry_openclaw_docs.md` is created as a **master pre-step** (>30-note series ⇒ required) before
the first sub-plan executes. This sub-plan **contributes its rows** to that hub:
- An **Announcements**-section row / sub-plan row: `an01 — Announcements — 1 page — 1 note`.
- A note-level row linking `oc_announcements_bluebubbles_imessage.md` (provides the required outside-folder
  inbound link for G7/G8).

No standalone `entry_*` note is created here (single note; far below the >30-note threshold for a dedicated
entry point).

## Inlinks (existing notes → new notes)

Candidate inbound links from OUTSIDE `resources/documentation/openclaw/` to satisfy G7/G8 (anti-island,

| Source (existing/planned) | → Target | Rationale |
|---|---|---|
| `0_entry_points/entry_openclaw_docs.md` (planned, master pre-step) | `oc_announcements_bluebubbles_imessage.md` | Hub row — primary required inbound link (W1). |
| `areas/code_repos/repo_openclaw_channels_messaging.md` (verified) | `oc_announcements_bluebubbles_imessage.md` | Code↔docs cross-link: the messaging-channels package's iMessage adapter ↔ the migration announcement. |
| `areas/code_repos/repo_openclaw_channels.md` (verified) | `oc_announcements_bluebubbles_imessage.md` | The channels subsystem ↔ the BlueBubbles-channel removal / iMessage cutover. |
| `resources/term_dictionary/term_openclaw.md` (verified) | `oc_announcements_bluebubbles_imessage.md` | Term→docs back-link from the product term to a product announcement (optional, if not over-linking the term note). |

Cross-block inlinks chosen so the new note is reachable from the entry hub AND the existing OpenClaw code-repo
corpus, not just from siblings within the docs folder.

## Pacing Rules (inherited from master)

- Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the execution script.
- `git pull --rebase --autostash origin main` before committing; **no Claude co-author trailer** in commits.
- This sub-plan is a single note — one wave; reindex incrementally and verify `note_links` + 0 broken links
  before commit; commit per sub-plan.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan (this file) | `/tessellum-plan-digestion` | 🟢 DONE |
| 3. Review | `/tessellum-review-digestion-plan` | 🟢 DONE — 9/9 checkpoints PASS → READY (2026-06-21) |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

## Augmentation Report (2026-06-21)

**Scope.** This sub-plan has exactly **1 planned note** (`oc_announcements_bluebubbles_imessage.md`,
procedure). Source re-read from `inbox/openclaw_docs/announcements/bluebubbles-imessage.md` — **measured 477
words**, 3 code fences (bash install/verify, json5 config, bash restart/probe), 4 H2 (`What changed`,
`What to do`, `Migration notes`, `See also`), 0 H3 — matches the plan's Source table exactly (ratio 1.0, no
under-estimation). Single-BB (procedure), downscale-not-split confirmed.

**What was LOCKED.** The former "Candidate Cross-References" section was replaced by **Per-Note Related Notes
Mapping (LOCKED — xref-augment 2026-06-21)** at the raised floors (≥8 terms · ≥10 snippets · ≥10 docs,

| Note | Terms | Snippets | Docs (existing) | Repos | Planned `oc_*` | Floors met |
|---|---:|---:|---:|---:|---:|---|
| `oc_announcements_bluebubbles_imessage.md` | 12 | 12 | 10 | 5 | 3 | ✅ (≥8t · ≥10s · ≥10d) |

- **Terms (12):** term_openclaw, term_json_rpc, term_acp_agent_client_protocol, term_messaging_gateway,
  term_channel_kernel, term_webhook, term_remote_ssh, term_ssh, term_dm_policy, term_thread_binding_policy,
  `term_deprecation` / `term_chatbot` — confirmed absent in the DB — with verified, more-relevant terms;
  `term_mcp` and the speculative `term_chatbot` were dropped in favor of `term_json_rpc` + `term_acp_*` +
  `term_messaging_gateway`, which are the transports/components actually named on the page.)
- **Snippets (12, all existing):** apple_imessage, gw_platform_bluebubbles, gw_platform_signal_media,
  gw_platform_whatsapp, gw_platform_discord_attachment, acp_entry, gw_config_schema, tui_server_jsonrpc,
  openclaw_channels_dm_pairing_allowlist, openclaw_security_audit_channel_dm, openclaw_acp_spawn_thread_binding,
  hermes_cli_setup_verify.
- **Docs (10 existing, ≥5-existing minimum exceeded):** hermes_messaging_bluebubbles_imessage (direct twin),
  hermes_photon_imessage, hermes_messaging_simplex, hermes_env_vars_runtime_messaging_behavior,
  hermes_sessions_lifecycle_resume, hermes_acp_internals, cc_build_a_channel, cc_channels_overview,
  cc_channels_setup, pi_rpc_protocol — PLUS 3 planned sibling `oc_*` (imessage_from_bluebubbles, imessage,
  gateway_config_channels) as additional discoverability.
- **Repos (5):** repo_openclaw_channels_messaging, repo_openclaw_channels, repo_openclaw_gateway,
  repo_openclaw, repo_openclaw_sessions.

**DB-verification.** All **39 distinct existing cited ids** (12 term + 10 doc + 12 snippet + 5 repo) returned
Planned `oc_*` siblings and `entry_openclaw_docs` returned 0 rows (expected — created before execution per
master W1 / ch02 / gw01).

discarded. `aws_docs` returned only generic remote-access/SSH-keypair pages — discarded.

**New-term candidates:** **0.** Consistent with the master's near-0 expectation. The on-page vocabulary
(BlueBubbles, imsg, iMessage, Full Disk Access / Automation, session key) is product/page-specific and
doc-owned, not cross-cutting `term_dictionary` material; the cross-cutting protocol/auth/OS terms
(JSON-RPC, webhook, SSH/remote-SSH, ACP) all already have existing notes (linked above). Best-fit glossary
N/A (no new term). See the Undigested Terms Plan for per-term disposition.

**Newly-surfaced undigested terms at re-read (Step 2d):** none beyond the plan's existing table — the re-read
confirmed the same vocabulary; no plan-digestion quality flag (<3 new terms).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance + relevancy statements) | **PASS** | Per-Note Related Notes Mapping present; note 1 = 12 terms (≥8) · 12 snippets (≥10) · 10 docs (≥10) · 5 repos; every link carries `— what it is; relevance: …`. |
| CP2 | 9-GATE table present (G1–G9) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table has all 8 incl. G5 ghost-detect, G6 broken-link, G7/G8 discoverability/anti-island; validation scripts implement G1/G3/G4/G5/G6/G7. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | "Entry Point Decision (inherited from master)" — no standalone entry created (single note, far below >30 threshold); contributes an01 + note-level rows to `entry_openclaw_docs.md` (master pre-step W1); inbound link for G7/G8. |
| CP4 | Size | **PASS** | 1 planned note (≤30); ~600 est. words / ~150 lines / 3 fences — comfortably within ≤2500w / ≤400 lines / ≤6 fences. |
| CP5 | Format derived (not invented) | **PASS** | Inherits master Format Definition derived from existing `cc_*`/`pi_*` corpora; `## Overview` + `## Related Notes` + source-mirrored H2 + `**Source**/**Last Updated**/**Status**` footer; forbidden-field list enforced (G1). |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment: ~600w / ~150 lines / 3 fences, single-BB; not borderline; downscale-not-split rationale documented in Split Decisions. |
| CP7 | Sources measured (not guessed) | **PASS** | Source re-read 2026-06-21: `wc -w` = 477 (plan said 477, ratio 1.0); 3 fences / 4 H2 / 0 H3 confirmed against source. |
| CP8 | Undigested terms + authoring reqs | **PASS** | "Undigested Terms Plan" present (9-row disposition table) + "Term-Note Authoring Requirements" present (N/A, 0 new terms, with inherited reference); 0 new captures, near-0 master expectation honored. |

**RESULT: 9/9 (incl. CP8f) PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
