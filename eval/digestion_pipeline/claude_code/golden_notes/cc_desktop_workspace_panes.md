---
tags:
  - resource
  - documentation
  - claude_code
  - desktop
  - workspace
keywords:
  - claude desktop workspace
  - pane layout
  - integrated terminal
  - file pane
  - view modes
  - keyboard shortcuts
  - usage ring
  - computer use
  - app permission tiers
topics:
  - Claude Code
  - Desktop
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/desktop
access_control_group: ["general"]
---

# Claude Desktop — Arrange Your Workspace and Computer Use

## Overview

The Claude Desktop **Code tab** presents a session as a set of draggable, resizable **panes** — chat, diff, preview, terminal, file, plan, tasks, and subagent — that you arrange into any layout. Around the panes sit an integrated terminal that shares the session's working directory and environment, an in-app file editor, three transcript **view modes**, a full keyboard-shortcut set, and a usage ring that shows context-window and plan usage. This note documents how to arrange that workspace.

The same surface also exposes **computer use**, a research-preview capability that lets Claude open native apps and control your screen when no more precise tool (connector, Bash, Chrome) can reach a task. Computer use is off by default, requires explicit enabling plus macOS system permissions, and gates each app behind a per-session approval with a fixed access tier. (The full computer-use reference lives at https://code.claude.com/docs/en/computer-use.)

## Arrange your workspace

The Code tab is built around panes you can arrange in any layout: chat, diff, preview, terminal, file, plan, tasks, and subagent. Drag a pane by its header to reposition it, or drag a pane edge to resize it. Press **Cmd+\\** on macOS or **Ctrl+\\** on Windows to close the focused pane. Open additional panes from the **Views** menu in the session toolbar.

> The pane layout, terminal, file editor, and view modes in this section require Claude Desktop v1.2581.0 or later. Open **Claude → Check for Updates** on macOS or **Help → Check for Updates** on Windows to update.

### Run commands in the terminal

The integrated terminal lets you run commands alongside your session without switching to another app. Open it from the **Views** menu or press **Ctrl+`** on macOS or Windows. The terminal opens in your session's working directory and shares the same environment as Claude, so commands like `npm test` or `git status` see the same files Claude is editing. To open a second terminal tab, click **+** in the terminal pane header or right-click a folder in the chat to choose **Open in terminal**. The terminal is available in local sessions only.

### Open and edit files

Click a file path in the chat or diff viewer to open it in the file pane. HTML, PDF, image, and video paths open in the preview pane instead. Make spot edits and click **Save** to write them back. If the file changed on disk since you opened it, the pane warns you and lets you override or discard. Click **Discard** to revert your edits, or click the path in the pane header to copy the absolute path.

The file pane is available in local and SSH sessions. For cloud sessions, ask Claude to make the change.

### Open files in other apps

Right-click any file path in the chat, diff viewer, or file pane to open a context menu:

- **Attach as context**: add the file to your next prompt
- **Open in**: open the file in an installed editor such as VS Code, Cursor, or Zed
- **Show in Finder** on macOS, **Show in Explorer** on Windows: open the containing folder
- **Copy path**: copy the absolute path to your clipboard

### Switch view modes

View modes control how much detail appears in the chat transcript. Switch modes from the **Transcript view** dropdown next to the send button, or press **Ctrl+O** on macOS or Windows to cycle through them.

| Mode | What it shows |
| --- | --- |
| **Normal** | Tool calls collapsed into summaries, with full text responses |
| **Verbose** | Every tool call, file read, and intermediate step Claude takes |
| **Summary** | Only Claude's final responses and the changes it made |

Use Verbose when debugging why Claude took a particular action. Use Summary when you're running multiple sessions and want to scan results quickly.

### Keyboard shortcuts

Press **Cmd+/** on macOS or **Ctrl+/** on Windows to see all shortcuts available in the Code tab. On Windows, use **Ctrl** in place of **Cmd** for the shortcuts below. Session cycling, the terminal toggle, and the view-mode toggle use **Ctrl** on every platform. These shortcuts apply only to the Code tab; the terminal-based interactive-mode shortcuts (such as `Shift+Tab` to cycle modes) do not apply in Desktop.

| Shortcut | Action |
| --- | --- |
| `Cmd` `/` | Show keyboard shortcuts |
| `Cmd` `N` | New session |
| `Cmd` `W` | Close session |
| `Ctrl` `Tab` / `Ctrl` `Shift` `Tab` | Next or previous session |
| `Cmd` `Shift` `]` / `Cmd` `Shift` `[` | Next or previous session |
| `Esc` | Stop Claude's response |
| `Cmd` `Shift` `D` | Toggle diff pane |
| `Cmd` `Shift` `P` | Toggle preview pane |
| `Cmd` `Shift` `S` | Select an element in preview |
| `Ctrl` `` ` `` | Toggle terminal pane |
| `Cmd` `\` | Close focused pane |
| `Cmd` `;` | Open side chat |
| `Ctrl` `O` | Cycle view modes |
| `Cmd` `Shift` `M` | Open permission mode menu |
| `Cmd` `Shift` `I` | Open model menu |
| `Cmd` `Shift` `E` | Open effort menu |
| `1`–`9` | Select item in an open menu |

### Check usage

Click the usage ring next to the model picker to see your current context window usage and your plan usage for the period. Context usage is per session; plan usage is shared across all your Claude Code surfaces.

## Let Claude use your computer

Computer use lets Claude open your apps, control your screen, and work directly on your machine the way you would. Ask Claude to test a native app in a mobile simulator, interact with a desktop tool that has no CLI, or automate something that only works through a GUI.

> Computer use is a research preview on macOS and Windows that requires a Pro or Max plan. It is not available on Team or Enterprise plans. The Claude Desktop app must be running.

Computer use is off by default; enable it in Settings before Claude can control your screen. On macOS, you also need to grant Accessibility and Screen Recording permissions. Unlike the sandboxed Bash tool (https://code.claude.com/docs/en/sandboxing), computer use runs on your actual desktop with access to whatever you approve. Claude checks each action and flags potential prompt injection from on-screen content, but the trust boundary is different.

### When computer use applies

Claude has several ways to interact with an app or service, and computer use is the broadest and slowest. It tries the most precise tool first:

- If you have a connector for a service, Claude uses the connector.
- If the task is a shell command, Claude uses Bash.
- If the task is browser work and you have Claude in Chrome set up, Claude uses that.
- If none of those apply, Claude uses computer use.

The per-app access tiers reinforce this: browsers are capped at view-only, and terminals and IDEs at click-only, steering Claude toward the dedicated tool even when computer use is active. Screen control is reserved for things nothing else can reach, like native apps, hardware control panels, mobile simulators, or proprietary tools without an API.

### Enable computer use

Computer use is off by default. If you ask Claude to do something that needs it while it's off, Claude tells you it could do the task if you enable computer use in Settings.

1. **Update the desktop app** — Make sure you have the latest version, then restart the app.
2. **Turn on the toggle** — Go to **Settings > General** (under **Desktop app**), find the **Computer use** toggle, and turn it on. On Windows, the toggle takes effect immediately and setup is complete; on macOS, continue to the next step. If you don't see the toggle, confirm you're on macOS or Windows with a Pro or Max plan, then update and restart the app.
3. **Grant macOS permissions** — On macOS, grant two system permissions before the toggle takes effect: **Accessibility** (lets Claude click, type, and scroll) and **Screen Recording** (lets Claude see what's on your screen). The Settings page shows the current status of each permission; if either is denied, click the badge to open the relevant System Settings pane.

### App permissions

The first time Claude needs to use an app, a prompt appears in your session. Click **Allow for this session** or **Deny**. Approvals last for the current session, or 30 minutes in Dispatch-spawned sessions. The prompt also shows what level of control Claude gets for that app. These tiers are fixed by app category and can't be changed:

| Tier | What Claude can do | Applies to |
| --- | --- | --- |
| View only | See the app in screenshots | Browsers, trading platforms |
| Click only | Click and scroll, but not type or use keyboard shortcuts | Terminals, IDEs |
| Full control | Click, type, drag, and use keyboard shortcuts | Everything else |

Apps with broad reach, like terminals, Finder or File Explorer, and System Settings or Settings, show an extra warning in the prompt so you know what approving them grants.

You can configure two settings in **Settings > General** (under **Desktop app**):

- **Denied apps**: add apps here to reject them without prompting. Claude may still affect a denied app indirectly through actions in an allowed app, but it can't interact with the denied app directly.
- **Unhide apps when Claude finishes**: while Claude is working, your other windows are hidden so it interacts with only the approved app. When Claude finishes, hidden windows are restored unless you turn this setting off.

**Source**: https://code.claude.com/docs/en/desktop
**Last Updated**: 2026-06-13
**Status**: Active
