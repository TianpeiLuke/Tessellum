---
title: Sub-Plan B13A — Claude Code Docs: Chat, Browser & Computer Use
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["slack", "chrome", "computer-use"]
---

# Sub-Plan B13A: Chat, Browser & Computer Use

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 3 surface pages that let Claude Code reach **outside the terminal**: delegating coding tasks from a
**Slack** workspace, automating a **Chrome** browser, and controlling the macOS GUI via **computer use**.
P2 (Phase B) — these are feature surfaces built on the Phase A cores (agentic loop, MCP, permissions,
web sessions), which they link rather than redefine. Each page is a self-contained "how to use surface X"
guide combining a concept overview, a setup procedure, and (for browser/computer use) a safety/trust
discussion.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 3 pages, 5,286 measured words. **Planned: 6 notes.**

## Content Strategy

- **Prioritize**: the three "how Claude reaches outside the terminal" surfaces and their distinct
  trust boundaries — Slack (delegation to web sessions, channel-gated access), Chrome (browser tools via
  a native-messaging extension, login-state sharing), computer use (machine-wide screen control,
  per-app approval). These are the load-bearing operational facts a team needs.
- **Group**: each page splits along the **concept vs procedure** seam — a "what it is / how it works"
  concept note plus a "set it up / troubleshoot it" procedure note. `computer-use` additionally yields an
  **argument** note for its safety/trust-boundary case (per-app approval + guardrails), keeping one BB per note.
- **Skip / link-out (own other sub-plans)**: Claude Code on the web / session sharing → B12B
  (`claude-code-on-the-web.md`); VS Code browser automation → B12A (`vs-code.md`); computer use in the
  **Desktop** app → B12A (`desktop.md`); MCP server mechanics → B08A (`mcp.md`); sandboxing contrast →
  B05B (`sandboxing.md`); permission modes → B05A; CLI `--chrome`/`-p` flags full ref → B03B
  (`cli-reference.md`); data/privacy → B16 (`data-usage.md`). These are referenced via links, never duplicated.
- **Glossary**: no glossary page here; new non-glossary terms surfaced by Step 2d are routed per
  Pattern B (existing term note / home sub-plan), not inlined.

## Source Pages (Measured 2026-06-13, re-read)

All 3 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| slack | /slack | 1,853 | 0 | 11 | 16 | concept + procedure |
| chrome | /chrome | 1,581 | 9 | 6 | 14 | concept + procedure |
| computer-use | /computer-use | 1,852 | 5 | 10 | 10 | concept + procedure + argument |

> **H2 lists (document order):**
> - **slack**: Use cases · Prerequisites · Setting up Claude Code in Slack (Steps) · How it works (H3 Automatic detection, Context gathering, Session flow) · User interface elements (H3 App Home, Message actions, Repository selection) · Access and permissions (H3 User-level access, Workspace-level access, Channel-based access control) · What's accessible where · Best practices (H3 Writing effective requests, When to use Slack vs. web) · Troubleshooting (H3 Sessions not starting, Repository not showing, Wrong repository selected, Authentication errors, Session expiration) · Current limitations · Related resources
> - **chrome**: Capabilities · Prerequisites · Get started in the CLI (Steps; H3 Enable Chrome by default, Manage site permissions) · Example workflows (H3 Test a local web application, Debug with console logs, Automate form filling, Draft content in Google Docs, Extract data from web pages, Run multi-site workflows, Record a demo GIF) · Troubleshooting (H3 Extension not detected, Browser not responding, Connection drops during long sessions, Windows-specific issues, Common error messages) · See also
> - **computer-use**: What you can do with computer use · When computer use applies · Enable computer use (Steps) · Approve apps per session · How Claude works on your screen (H3 One session at a time, Apps are hidden while Claude works, Screenshots are downscaled automatically, Stop at any time) · Safety and the trust boundary · Example workflows (H3 Validate a native build, Reproduce a layout bug, Test a simulator flow) · Differences from the Desktop app · Troubleshooting (H3 in-use lock, permissions prompt, doesn't appear in /mcp) · See also

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **6 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_claude_code_in_slack.md` | concept | slack: intro, Use cases, How it works (detection/context/session flow), UI elements, What's accessible where, Best practices, Current limitations | 600 | What Claude Code in Slack is — @mention a coding task, intelligent routing to a web session; detection + thread/channel context gathering; the 6-step session flow; message actions (View Session / Create PR / Retry as Code / Change Repo); Slack-vs-web guidance; GitHub-only/one-PR limits. Setup → note 2; access model → note 2. |
| 2 | `cc_slack_setup_and_routing.md` | procedure | slack: Prerequisites, Setting up Claude Code in Slack (5 Steps), Access and permissions, Troubleshooting | 600 | Prerequisites table (plan, web access, GitHub, Slack link); the 5 setup Steps (install app, connect account, configure web, choose routing mode Code-only/Code+Chat, `/invite @Claude`); user/workspace/channel access control; troubleshooting (sessions not starting, repo not showing, wrong repo, auth, expiration). |
| 3 | `cc_chrome_browser_automation.md` | concept | chrome: intro, Capabilities, Example workflows | 550 | What the Chrome integration is — browser tools via the Claude-in-Chrome extension; opens visible tabs, shares login state, pauses on login/CAPTCHA; 7 capabilities (live debug, design verify, web-app testing, authenticated apps, data extraction, task automation, session recording); ≤6 representative workflow prompts (the 7th summarized as prose to honor the ≤6-code cap). Setup → note 4. |
| 4 | `cc_chrome_setup_and_troubleshooting.md` | procedure | chrome: Prerequisites, Get started in the CLI (+ Enable by default, Manage site permissions), Troubleshooting | 600 | Prerequisites (Chrome/Edge, extension ≥1.0.36, CC ≥2.0.73, direct Anthropic plan; not via third-party providers); start with `claude --chrome` or `/chrome`; enable-by-default trade-off (context cost); site permissions inherited from the extension; troubleshooting (extension not detected + native-messaging-host paths, browser not responding, idle service worker, Windows EADDRINUSE, common-error table). |
| 5 | `cc_computer_use.md` | concept | computer-use: intro, What you can do, When computer use applies, Enable computer use (Steps), How Claude works on your screen, Example workflows, Differences from the Desktop app, Troubleshooting | 700 | What CLI computer use is (research preview, macOS, Pro/Max, interactive only); the GUI-task use cases; the precision ladder (MCP → Bash → Chrome → computer use); enable via `/mcp` + macOS Accessibility/Screen-Recording grants; how it runs (machine-wide lock, apps hidden, terminal excluded, screenshots downscaled, Esc to stop); CLI-vs-Desktop differences table; troubleshooting. Safety/trust case → note 6. |
| 6 | `cc_computer_use_safety.md` | argument | computer-use: Approve apps per session, Safety and the trust boundary | 450 | The argument that computer use runs on your real desktop (unlike the sandboxed Bash tool) so the trust boundary is different — and why the built-in guardrails are sufficient: per-app per-session approval, sentinel warnings for shell/filesystem/system-settings apps, view-only/click-only/full-control tiers, terminal excluded from screenshots, global Esc consumed against injection, single-session lock file. |

**Estimate: 6 notes** — concept ×3 (notes 1,3,5), procedure ×2 (notes 2,4), argument ×1 (note 6). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 3 (5,286 words). New `cc_` notes: 6. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~3,500 (avg ~580/note). Code blocks: ≤6/note (verbatim command + example-prompt blocks from source).
- **Building Block Distribution**: concept ×3 (notes 1,3,5) · procedure ×2 (notes 2,4) · argument ×1 (note 6). No model/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_claude_code_in_slack` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents a surface of Claude Code itself (the Slack chat entry point that spawns a Claude Code web session), so the product term is its definitional anchor.
- [Delegated Work](../../term_dictionary/term_delegated_work.md) — The note's whole premise is delegating a coding task by @mentioning Claude and letting it run asynchronously while you continue other work — the delegated-work pattern this term names.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Once routed, the Slack request becomes an autonomous Claude Code session that investigates, edits across files, and opens a PR without per-step steering — the autonomous-coding-agent behavior this term defines.
- [Agentic AI](../../term_dictionary/term_agentic_ai.md) — The note's intelligent intent-routing (detect coding intent, gather thread context, pick a repo, act) is an applied agentic-AI workflow, grounding the chat-to-action behavior here.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — The note's review step (status updates, then a completion @mention with View Session / Create PR buttons for the human to approve) is the human-in-the-loop checkpoint this term describes.
- [Access Control](../../term_dictionary/term_access_control.md) — The note's channel-based access model (Claude only responds where invited; admins gate usage via channel membership) is an access-control mechanism this term covers.

### 2. `cc_slack_setup_and_routing` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This is the setup/access procedure for a Claude Code surface (the Slack app routing to Claude Code web sessions), so the product term anchors what is being configured.
- [Access Control](../../term_dictionary/term_access_control.md) — The note's core content is the three-tier access model (user-level plan limits, workspace admin install/removal, channel-invite gating) — concrete access-control configuration.
- [Authentication](../../term_dictionary/term_authentication.md) — The setup hinges on linking the Slack account to the Claude account and connecting GitHub, and the troubleshooting section's auth-error fixes are about re-authenticating — the authentication flow this term defines.
- [Delegated Work](../../term_dictionary/term_delegated_work.md) — The routing-mode choice (Code-only vs Code+Chat) configures how messages are dispatched to a delegated coding session, the delegated-work setup this term frames.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Channel-membership gating plus per-user repository scoping is a graduated-access posture (Claude can only reach repos and channels explicitly granted), aligning with this term's progressive-trust model.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — The Code+Chat "Retry as Code" / "Change Repo" controls keep a human in the routing loop to correct Claude's automatic decisions, the human-in-the-loop pattern this term names.

### 3. `cc_chrome_browser_automation` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents Claude Code's Chrome browser-automation surface, so the product term is its anchor.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The browser tools are exposed as the `claude-in-chrome` MCP server (the note tells you to run `/mcp` and select it to list the tools), so MCP is the mechanism delivering these capabilities.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Each browser action (navigate, click, type, read console/DOM, screenshot) is a tool call whose result feeds the next decision — the function-calling/tool-use loop this term defines, here bound to browser tools.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The note's signature workflow — build the code, then open it in the browser to test/debug and fix what broke — is the build-test-fix autonomy this term describes, extended to the browser.
- [Agentic AI](../../term_dictionary/term_agentic_ai.md) — Chaining browser actions across tabs and sites to complete a goal (extract data, run multi-site workflows) is an applied agentic-AI behavior, grounding the note's example workflows.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The Chrome extension plus native-messaging bridge is the harness layer that wires browser tools into the model, the tool/execution-environment wiring this term covers.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — The note states Claude pauses and asks the user to handle login pages and CAPTCHAs manually — an explicit human-in-the-loop handoff this term names.

### 4. `cc_chrome_setup_and_troubleshooting` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This is the install/config/troubleshooting procedure for Claude Code's Chrome surface, so the product term anchors what is being set up.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The browser tools are an MCP server (`claude-in-chrome`), and an idle MCP service-worker connection is a documented failure mode — MCP is central to both setup and troubleshooting here.
- [Context Window](../../term_dictionary/term_context_window.md) — The note's enable-by-default warning is explicitly a context trade-off (browser tools always loaded increase context usage), tying the setup choice to the context-window concept.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Site-level permissions inherited from the Chrome extension (which sites Claude may browse/click/type on) are a graduated-trust allowlist configured during setup.
- [Authentication](../../term_dictionary/term_authentication.md) — The integration shares the browser's existing login state so Claude can reach sites you're already signed into — leveraging the user's authenticated sessions, the auth concept this term defines.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Troubleshooting centers on the native-messaging-host config file and extension service worker — the harness/bridge plumbing that connects the agent to the browser, which this term frames.

### 5. `cc_computer_use` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents Claude Code's CLI computer-use surface (screen control on macOS), so the product term is its anchor.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Computer use ships as a built-in MCP server named `computer-use` that you enable in `/mcp`, and MCP servers are the most-precise tool Claude tries before falling back to screen control — MCP is both the delivery mechanism and the top of the precision ladder.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Computer use is a tool category (open apps, click, type, screenshot) whose results feed back into the conversation — the function-calling/tool-use loop this term defines, here as screen actions.
- [Agentic AI](../../term_dictionary/term_agentic_ai.md) — Driving a GUI the way a human would (compile, launch, click through every control, screenshot results in one conversation) is an applied agentic-AI behavior, grounding the note's capabilities.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The signature flow — write the Swift, compile, launch, verify by clicking through the UI — is the autonomous build-and-validate loop this term describes, extended to native apps.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — The note contrasts computer use against the sandboxed Bash tool (computer use runs on your real desktop, not isolated), making the sandbox concept the explicit foil that defines computer use's different trust boundary.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The machine-wide lock, app-hiding, screenshot downscaling, and terminal-exclusion are the execution-environment plumbing the harness manages around the model, which this term frames.

### 6. `cc_computer_use_safety` (8 term notes)
- [Sandboxing](../../term_dictionary/term_sandbox.md) — The note's central argument opens by contrasting computer use with the sandboxed Bash tool — computer use is *not* sandboxed, it runs on your actual desktop — making the sandbox concept the baseline the trust-boundary case is argued against.
- [Guardrails](../../term_dictionary/term_guardrails.md) — The note's thesis is that built-in guardrails reduce risk without configuration (per-app approval, sentinel warnings, terminal exclusion, global Esc, lock file) — it is literally an enumeration of guardrails, the term's exact subject.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The per-app per-session approval model and the view-only / click-only / full-control tiers are a graduated-trust scheme — control is granted incrementally, not all at once, the pattern this term defines.
- [Deny-First](../../term_dictionary/term_deny_first.md) — Computer use is off by default and grants no app access until you approve each one per session — a deny-by-default posture, the principle this term names.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — The sentinel warnings (shell-equivalent terminals, file-reading Finder, system-settings access) exist precisely to let you judge the blast radius before approving — the impact-scoping concept this term defines.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — Every safeguard routes through a human decision (Allow-for-this-session / Deny prompts, Esc to abort) — the human-in-the-loop control this term names.
- [Prompt Injection](../../term_dictionary/term_guardrails.md) — The note flags prompt injection from on-screen content and consumes the Esc key so injection can't dismiss the stop dialog; the guardrails term covers these injection-mitigation safeguards. <!-- no dedicated term_prompt_injection note exists in DB; mapped to term_guardrails which covers injection defenses -->
- [Reversibility-Weighted Risk](../../term_dictionary/term_reversibility_weighted_risk.md) — The note's tier system (browsers/trading view-only, terminals/IDEs click-only, everything else full control) scales control by how consequential/irreversible an app's actions are — the reversibility-weighted-risk framing this term defines.

> **Mapping note:** No `term_prompt_injection`, `term_browser_automation`, `term_gui_automation`,
> `term_web_scraping`, or `term_tool_use` note exists in the DB (verified absent 2026-06-13). Prompt-injection
> coverage is carried by `term_guardrails`; tool-use coverage by `term_function_calling`. The line above that
> labels a `term_guardrails` link "Prompt Injection" is intentional and counts only **once** toward note 6's
> distinct-term total (7 distinct terms; 8 lines) — it is annotated, not a ghost.

## Section Coverage Map

```
slack.md
├── Use cases ──────────────────────────── → note 1 (cc_claude_code_in_slack)
├── Prerequisites ──────────────────────── → note 2 (cc_slack_setup_and_routing)
├── Setting up Claude Code in Slack ─────── → note 2
│   └── Choose your routing mode (table) ── → note 2
├── How it works (detection/context/flow) → note 1
├── User interface elements ────────────── → note 1
├── Access and permissions ─────────────── → note 2
├── What's accessible where ────────────── → note 1 (→ B12B web session sharing)
├── Best practices ─────────────────────── → note 1
├── Troubleshooting ────────────────────── → note 2
├── Current limitations ────────────────── → note 1
└── Related resources (cards) ──────────── → notes 1/2 (links; → B12B claude-code-on-the-web)
chrome.md
├── Capabilities ───────────────────────── → note 3 (cc_chrome_browser_automation)
├── Prerequisites ──────────────────────── → note 4 (cc_chrome_setup_and_troubleshooting)
├── Get started in the CLI ─────────────── → note 4
│   ├── Enable Chrome by default ───────── → note 4
│   └── Manage site permissions ────────── → note 4
├── Example workflows (7 H3) ───────────── → note 3 (≤6 code; 7th summarized prose)
├── Troubleshooting (incl. error table) ── → note 4
└── See also ───────────────────────────── → notes 3/4 (links; → B12A vs-code, B16 data-usage, note 5 computer-use)
computer-use.md
├── What you can do with computer use ──── → note 5 (cc_computer_use)
├── When computer use applies (ladder) ─── → note 5
├── Enable computer use (Steps) ────────── → note 5
├── Approve apps per session ───────────── → note 6 (cc_computer_use_safety)
├── How Claude works on your screen ────── → note 5
│   └── (lock / hidden apps / downscale / Esc) → note 5
├── Safety and the trust boundary ──────── → note 6
├── Example workflows ──────────────────── → note 5
├── Differences from the Desktop app ───── → note 5 (→ B12A desktop.md)
├── Troubleshooting ────────────────────── → note 5
└── See also ───────────────────────────── → notes 5/6 (links; → B12A desktop, note 3 chrome, B08A mcp, B05B sandboxing)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| slack (1,853w, 11 H2 mixed) | notes 1 (concept) + 2 (procedure) | One BB per note: "what it is / how it works / UI / best practices / limits" is concept; "prerequisites / setup Steps / access config / troubleshooting" is procedure. Single note would mix BBs. |
| chrome (1,581w, 9 code) | notes 3 (concept) + 4 (procedure) | One BB per note AND code-cap: 9 code fences total exceed ≤6/note; concept note keeps capabilities + ≤6 workflow examples, procedure note keeps setup + troubleshooting (2 setup code blocks). |
| computer-use (1,852w, 10 H2) | notes 5 (concept) + 6 (argument) | The "Safety and the trust boundary" + "Approve apps per session" sections make an argument (computer use is not sandboxed, but its guardrails are sufficient) distinct in BB from the concept/how-it-works body. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_claude_code_in_slack | concept | 600 | 0 | ✅ |
| 2 | cc_slack_setup_and_routing | procedure | 600 | 0 | ✅ |
| 3 | cc_chrome_browser_automation | concept | 550 | ≤6 | ✅ |
| 4 | cc_chrome_setup_and_troubleshooting | procedure | 600 | 2 | ✅ |
| 5 | cc_computer_use | concept | 700 | 3 | ✅ |
| 6 | cc_computer_use_safety | argument | 450 | 0 | ✅ |

No note approaches the word/line caps. The only code-cap risk is the chrome concept note (source has 7 workflow
example blocks); plan caps it at ≤6 verbatim blocks with the 7th summarized as prose. No over-compression —
every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_claude_code_in_slack cc_slack_setup_and_routing cc_chrome_browser_automation cc_chrome_setup_and_troubleshooting cc_computer_use cc_computer_use_safety"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] && echo "DENSITY WARNING: $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$CC"
# G5 ghost: verify every internal .md link target exists in the DB
for n in $NOTES; do f="$CC/$n.md"
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/.*\(([^)]+)\)/\1/' | while read l; do
    r=$(cd "$(dirname "$f")" && realpath -q -m "$l"); id=${r#*/the vault/}
    sqlite3 "$(python3 -c 'import sys;sys.path.insert(0,"scripts");from config import DB_PATH_STR;print(DB_PATH_STR)')" \
      "SELECT 1 FROM notes WHERE note_id='$id'" | grep -q 1 || echo "GHOST $n -> $l"
  done; done
```

## Per-Phase Validation Gate (G1–G8) — inherited from master

Single phase (6 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met (chrome concept ≤6 code); every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 6 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 6 notes RECEIVES ≥1 inbound link from a vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability(intra) | sibling `cc_*` cross-links resolve and the cluster is internally reachable (no intra-folder island) | DB in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 6 rows** under a "Surfaces — Chat / Browser / Computer Use" cluster + increments
the BB-distribution counts (concept ×3, procedure ×2, argument ×1).

## Undigested Terms Plan (Step 4e)

b13a creates **no new `term_dictionary` notes**. There is no glossary page in this sub-plan; all surfaced
vocabulary is either an existing substantive term note (link) or owned by a home sub-plan (Pattern B). Dedup
checked across **both** `term_dictionary/` AND `resources/documentation/`.

| Surfaced term/concept | Disposition |
|---|---|
| Claude Code in Slack / routing mode | doc concept — notes 1/2 (no term note) |
| Claude in Chrome / browser automation | doc concept — notes 3/4 (no `term_browser_automation` note exists; not a cross-cutting vocabulary term → no capture) |
| Computer use / screen control | doc concept — notes 5/6 (no `term_gui_automation`/`term_computer_use` note; covered by `term_function_calling` + `term_agentic_ai`) |
| MCP / `claude-in-chrome` / `computer-use` server | link `term_mcp` (exists) |
| Native messaging host | doc detail — note 4 (infra detail, not a vocabulary term → no capture) |
| Prompt injection | link `term_guardrails` (covers injection defenses; **no `term_prompt_injection` note exists** — master assigns Prompt injection → B16; B13A links the existing guardrails note, does not pre-create B16's term) |
| Sandbox / sandboxing | link `term_sandbox` (exists) |
| Sentinel warning / per-app approval / trust tier | doc detail — note 6; concepts covered by `term_guardrails` / `term_graduated_trust` / `term_blast_radius` (link) |
| Tool use / function calling | link `term_function_calling` (exists; **no `term_tool_use` note**) |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 3 pages scanning emphasis/tables/captions/code for
newly-surfaced terms. Candidates evaluated: "native messaging host", "service worker", "sentinel warning",
"routing mode". None is a cross-cutting vault vocabulary term with no doc-page home — each is an
implementation detail digested inline in its `cc_` note. **0 new B13A `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B13A authors zero term notes, so there are no
slugs to audit. Collision check performed for the linked terms: `term_mcp`, `term_sandbox`,
`term_function_calling`, `term_guardrails`, `term_graduated_trust`, `term_blast_radius`, `term_deny_first`,
`term_claude_code`, `term_delegated_work`, `term_human_in_the_loop`, `term_authentication`,
`term_access_control`, `term_agentic_ai`, `term_autonomous_coding_agents`, `term_agent_harness`,
`term_context_window`, `term_reversibility_weighted_risk` all exist → linked, not recreated.

## Term-Note Authoring Requirements

**N/A for b13a** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (Slack page has none; Chrome/computer-use command + example-prompt blocks copied exactly,
  capped at ≤6/note). One BB per note. Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 3, 5 | product term → its Slack / Chrome / computer-use surfaces |
| `term_dictionary/term_mcp.md` | notes 3, 5 | MCP term → the two surfaces delivered as MCP servers (`claude-in-chrome`, `computer-use`) |
| `term_dictionary/term_sandbox.md` | note 6 | sandbox term → computer-use safety note that contrasts the non-sandboxed trust boundary |
| `term_dictionary/term_guardrails.md` | note 6 | guardrails term → computer-use guardrail enumeration |
| `term_dictionary/term_delegated_work.md` | note 1 | delegated-work term → Slack delegation surface |
| `documentation/tutorials/tutorial_claude_code_*` | note 5 (if a CC tutorial exists) | getting-started tutorial → computer-use surface (confirm target at finalization; else use `term_claude_code` row above) |

## Follow-up Recommendations

- After the 6 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above and verify
  in-degree ≥1 for each note (G7/G8); add sibling cross-links to B12B (`cc_claude_code_on_the_web`),
  B12A (`cc_vs_code`, `cc_desktop`), B05B (`cc_sandboxing`), B08A (`cc_mcp`) once those land; queue the 6
  rows for `entry_claude_code_docs.md`; `/tessellum-check-broken-links`.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B13A, 2026-06-13)

- **Source re-read (Step 2)**: all 3 pages re-read from `inbox/claude_code_docs/`; measured words/code/H2/H3
  recorded (slack 1,853w / 0 code / 11 H2 / 16 H3 · chrome 1,581w / 9 code / 6 H2 / 14 H3 · computer-use
  1,852w / 5 code / 10 H2 / 10 H3 = 5,286 words, matching the master's figure). No >1.5× under-estimate;
  no re-split forced beyond the three documented.
- **Notes**: 6 (concept 3, procedure 2, argument 1) — exactly the master estimate. Each page split along the
  concept/procedure seam; computer-use additionally yields the safety argument note.
  ghosts (G5 PASS)**; relpaths `../../term_dictionary/`. Browser-specific terms (`term_browser_automation`,
  `term_web_scraping`, `term_playwright`) and `term_prompt_injection`/`term_tool_use` confirmed **absent**
  in the DB — mapped to existing on-sense terms (`term_guardrails`, `term_function_calling`) rather than to
  ghosts.
- **Step 2d new-term scan**: candidates (native messaging host, service worker, sentinel warning, routing
  mode) all implementation details digested inline; **0 new B13A term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G5/G7/G8 verification rows, mapping-note disclosure for the annotated guardrails link.
- **28-item checklist**: PASS (term-note items N/A — B13A authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented; advanced to Review.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B13A contributes 6 rows. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 6 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches existing `documentation/` notes exactly; body uses `## Overview` / source-mirrored H2s / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer convention. |
| CP6 | Borderline density → split | ✅ PASS | All 6 notes 450–700w; only code-cap risk (chrome concept) explicitly capped at ≤6 with 7th workflow summarized as prose. None borderline on words/lines. |
| CP7 | Source words measured (not guessed) | ✅ PASS | Re-measured: slack 1,853 · chrome 1,581 · computer-use 1,852 = 5,286 = master figure. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B13A authors 0 term notes; Undigested Terms Plan routes all surfaced terms (dedup across term_dictionary AND documentation/); Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented (17 existing terms linked, not recreated); absent browser/injection/tool-use terms confirmed and mapped to existing on-sense terms, not pre-created. |
| CP9 | Discoverability / anti-island (G7/G8) | ✅ PASS | Inlinks table lists ≥1 inbound link per note from outside `claude_code/` (term + tutorial notes), executed at finalization with DB in-degree ≥1 verification; sibling cross-links queued. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.
