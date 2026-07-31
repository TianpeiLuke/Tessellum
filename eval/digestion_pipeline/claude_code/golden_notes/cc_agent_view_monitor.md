---
tags:
  - resource
  - documentation
  - claude_code
  - agent_view
  - monitoring
keywords:
  - agent view
  - claude agents
  - background session
  - session state icons
  - peek and reply
  - attach to session
  - pull request status
  - row summaries
  - keyboard shortcuts
topics:
  - Claude Code
  - Agent View
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-view
access_control_group: ["general"]
---

# Claude Code — Monitor Sessions with Agent View

## Overview

**Agent view**, opened with `claude agents`, is one screen for all your background sessions — what's running, what needs your input, and what's done. You dispatch new sessions, watch their state at a glance instead of scrolling through transcripts, and step in only when one needs you. Each background session is a full Claude Code conversation that keeps running without a terminal attached, so you can open it, reply, and leave whenever you want. Use it when you have several independent tasks Claude can work on without you watching every step — dispatch a bug fix, a pull request review, and a flaky-test investigation as three rows, keep working in another window, and check back when a row shows it needs you or has a result.

Agent view is in **research preview** and requires Claude Code v2.1.139 or later (`claude --version`); the interface and keyboard shortcuts may change as the feature evolves. This note covers the monitoring surface — the dispatch→peek→attach loop, session state, and organization. Dispatching agents (from view/session/shell) is covered in [cc_dispatch_background_agents](cc_dispatch_background_agents.md), and the supervisor process that hosts sessions in [cc_background_session_hosting](cc_background_session_hosting.md). To compare agent view with subagents, agent teams, and worktrees, see [cc_run_agents_in_parallel](cc_run_agents_in_parallel.md).

## Quick Start: The Agent View Loop

The core loop is: dispatch a task, watch its row update as Claude works, peek to check on it and reply, and attach for the full conversation. The session keeps running after you close agent view.

1. **Open agent view** — run `claude agents` from your shell. Agent view opens with an input at the bottom and a table that fills in as sessions start. Press `Esc` to return to your shell; sessions keep running while you're away and reappear next time you open agent view.
2. **Dispatch a session** — type a prompt describing a task and press `Enter`. A new background session starts and appears as a row showing whether it's working, waiting on you, or done. Every prompt starts its *own* new session (a second prompt launches a second session alongside the first, not a follow-up), so you can run several in parallel. Each session uses your subscription quota independently.
3. **Peek and reply** — select a row with the arrow keys and press `Space` to open the peek panel, which shows the session's most recent output or the question it's waiting on. Type a reply and press `Enter` to send without leaving agent view.
4. **Attach and detach** — press `Enter` or `→` on a row to attach for the full conversation; the session takes over the terminal as a full interactive session. Press `←` on an empty prompt to detach and return to the table.
5. **Bring an existing session in** — run `/bg` inside an already-open session, or press `←` on an empty prompt to background it and open agent view in one step.

You can use `claude agents` as your primary entry point instead of `claude`: dispatch every task from agent view, attach when you want the full conversation, and press `←` to return to the table.

## The Session List

Running `claude agents` takes over the full terminal and lists every session grouped by state, with pinned sessions and the ones that need you at the top. Each row shows the session's name, current activity, and how long ago it last changed. By default the list shows every background session you've started across all your projects — a session in one repository and another in a different worktree both appear regardless of which directory you opened agent view from. To narrow to one project, pass `--cwd` (requires v2.1.141+):

```bash
claude agents --cwd ~/projects/my-app
```

A session that has moved into a worktree under `~/projects/my-app/.claude/worktrees/` still counts as belonging to `~/projects/my-app`. Interactive sessions you have open in other terminals don't appear until you background them. **[Subagents](../../term_dictionary/term_subagent.md) and teammates a session spawns aren't listed as separate rows** — only full background sessions are rows.

### Read Session State

Each row starts with an icon whose **color and animation** show the session's state:

| State | Icon shows as | What it means |
|---|---|---|
| Working | Animated | Claude is actively running tools or generating a response |
| Needs input | Yellow | Claude is waiting on a specific question or permission decision from you |
| Idle | Dimmed | The session has nothing to do and is ready for your next prompt |
| Completed | Green | The task finished successfully |
| Failed | Red | The task ended with an error |
| Stopped | Grey | The session was stopped with `Ctrl+X` or `claude stop` |

Separately, the icon's **shape** shows whether the underlying process is running: `✻` or animated `✽` means the session process is alive and replies immediately; `∙` means the process has exited (you can still peek, reply, or attach, and Claude restarts from where it left off); `✢` is a `/loop` session sleeping between iterations, with its run count and a countdown shown in the row. The `PR #N` label that can appear at the right edge is the pull request the session opened, not part of the state icon (a count such as `3 PRs` appears for multiple). The terminal tab title shows the awaiting-input count while agent view is open (e.g. `2 awaiting input · claude agents`). Background sessions don't need any terminal open to keep working, and session state persists on disk through auto-updates and supervisor restarts, and across machine sleep.

### Row Summaries

The one-line summary in each row is generated by a Haiku-class model (see https://code.claude.com/docs/en/model-config) so the row can tell you what the session is doing, what it needs, or what it produced without opening the transcript. While a session is actively working, the summary refreshes at most once every 15 seconds, plus once when each turn ends. From v2.1.161, when the session is running two or more parallel work items (subagents, background shell commands, or monitors), a `done/total` count such as `2/5` appears before the summary text. Each refresh is one short Haiku-class request through your normal provider; on third-party providers (Bedrock, Vertex AI, Microsoft Foundry, custom gateways) it falls back to the session's main model when no Haiku model is configured (set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to choose the model there).

### Pull Request Status

When a session opens a pull request, a `PR #1234` label appears at the right edge of the row, linked in terminals that support hyperlinks; the label persists when you send a follow-up. The number is **colored by status**:

| Color | Pull request status |
|---|---|
| Yellow | Waiting on checks or review, or checks failed |
| Green | Checks passed and no review is blocking |
| Purple | Merged |
| Grey | Draft or closed |

For most tasks this column is where you pick up the result: review and merge the pull request when its number turns green. For multiple PRs, the count label is colored by the open pull request that most needs attention; open the peek panel to see them all.

## Peek and Reply

Press `Space` on a selected row to open the peek panel. It shows what the session needs from you, its most recent output, and any pull requests it opened — most of the time this is enough and you never need the full transcript. From v2.1.161, when the session is running parallel work items, the panel also names the longest-running one and how long it has been going. Type a reply and press `Enter` to send it to that session. When the session asks a multiple-choice question the panel shows the options and you can press a number key to pick one; for other blocked sessions, press `Tab` to fill the input with a suggested reply you can edit before sending. Prefix a reply with `!` to send a Bash command instead. Use `↑`/`↓` to peek at adjacent sessions without closing the panel, or `→` to attach.

## Attach to a Session

Press `Enter` or `→` on a selected row to attach; agent view is replaced by the full interactive session, and Claude posts a short recap of what happened while you were away. While attached, the session behaves like any other Claude Code session. Attached sessions always render in fullscreen mode (regardless of your `tui` setting) because a background session has no terminal scrollback to append to — scroll with `PgUp`, `PgDn`, or the mouse wheel, and press `Ctrl+O` for transcript mode.

Press `←` on an empty prompt to detach and return to agent view; if a dialog has focus and isn't responding to `←`, press `Ctrl+Z` to detach immediately. `Ctrl+C` keeps its standard interrupt behavior while attached (cancels a running response or `!` shell command rather than detaching); pressing it twice on an empty prompt detaches. **Detaching never stops a background session** — `←`, `Ctrl+Z`, `/exit`, and double `Ctrl+C`/`Ctrl+D` all leave it running; to end a session from inside it, run `/stop`. Pressing `←` on an empty prompt works from any Claude Code session, not only ones attached from agent view: it backgrounds the current session and opens agent view with that row selected. You can turn this shortcut off in `/config` (the `leftArrowOpensAgents` setting).

## Organize and Filter the List

Agent view groups sessions so the ones that need input are at the top, with `Ready for review` and `Needs input` above `Working` and `Completed`. These group names **don't map one-to-one to the states** above: a session moves to `Ready for review` when it has an open pull request, and `Completed` collects finished, failed, and stopped sessions together. Press `Ctrl+S` to group by directory instead (your choice persists across runs). Within a group: `Ctrl+T` pins a session to the top and keeps its process running while idle; `Shift+↑`/`Shift+↓` reorders; `Ctrl+R` renames; `Enter` on a group header collapses it. To remove a session, press `Ctrl+X` to stop it and `Ctrl+X` again within two seconds to delete it (deleting also removes a worktree Claude created for the session, including uncommitted changes, so push or commit first; the transcript stays available via `claude --resume`). Older completed sessions fold into a `… N more` row; failures and sessions with an open pull request always stay visible.

Type in the dispatch input to **filter** instead of dispatching:

| Filter | Shows |
|---|---|
| `a:<name>` | Sessions running the named agent |
| `s:<state>` | Sessions in the given state, such as `s:working`; also accepts `s:blocked` for everything waiting on you |
| `#<number>` or a PR URL | The session working on that pull request |
| Any other URL | The session whose first prompt contained that URL |

### Keyboard Shortcuts

Press `?` in agent view to see every shortcut in context. The key ones: `↑`/`↓` move between rows; `Enter` attaches (or dispatches if there's text in the input); `Space` opens/closes the peek panel; `Shift+Enter` dispatches and attaches immediately; `→` attaches; `Alt+1`..`Alt+9` attach to session 1–9 in the focused session's directory; `Tab` browses all subagents on an empty input (otherwise applies the highlighted suggestion); `Ctrl+S` switches grouping; `Ctrl+T` pins/unpins; `Ctrl+R` renames; `Ctrl+G` opens the dispatch prompt in your `$VISUAL`/`$EDITOR`; `Ctrl+X` stops (press again within two seconds to delete); `Shift+↑`/`Shift+↓` reorders; `Esc` closes the peek panel, clears the input, or exits; `Ctrl+C` clears the input (twice to exit); `?` shows all shortcuts.

## Limitations

Agent view is in research preview with the following limitations:

- **Rate limits apply** — background sessions consume your subscription usage the same as interactive sessions, so running ten agents in parallel uses quota roughly ten times as fast as running one.
- **Sessions are local** — background sessions run on your machine; they are preserved across sleep but stop if the machine shuts down (they then show as failed, and attaching/peeking/replying restarts them from where they left off).
- **Claude-created worktrees are deleted with the session in agent view** — merge or push changes before deleting a session that edited files in its own worktree. `claude rm` keeps a worktree that has uncommitted changes; a worktree you created yourself is left in place.

**Source**: https://code.claude.com/docs/en/agent-view
**Last Updated**: 2026-06-13
**Status**: Active
