---
tags:
  - resource
  - documentation
  - claude_code
  - desktop
  - quickstart
keywords:
  - desktop app quickstart
  - code tab
  - chat cowork code tabs
  - install claude desktop
  - first coding session
  - local remote ssh environment
  - review and accept changes
  - coming from the cli
topics:
  - Claude Code
  - Desktop
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/desktop-quickstart
access_control_group: ["general"]
---

# Get Started with the Claude Code Desktop App

## Overview

The desktop app gives you Claude Code with a graphical interface built for running multiple sessions side by side: a sidebar for managing parallel work, a drag-and-drop layout with an integrated terminal and file editor, visual diff review, live app preview, GitHub PR monitoring with auto-merge, and scheduled tasks — no terminal required. This note is the getting-started walkthrough: download and install the app, open the **Code** tab, and run a first coding session, then a "try next" tour into the full desktop reference.

The desktop app requires a Pro, Max, Team, or Enterprise subscription. It is available for macOS (universal Intel/Apple Silicon build) and Windows (x64, plus an ARM64 installer); it is **not available on Linux** — use the [CLI](https://code.claude.com/docs/en/quickstart) instead.

## The Three Tabs

The desktop app has three tabs:

- **Chat**: General conversation with no file access, similar to claude.ai.
- **Cowork**: An autonomous background agent that works on tasks in a cloud VM with its own environment. It can run independently while you do other work.
- **Code**: An interactive coding assistant with direct access to your local files. You review and approve each change in real time.

Chat and Cowork are covered in the Claude Desktop support articles. This page focuses on the **Code** tab.

## Install

1. **Install and sign in** — Download the installer for your platform and run it. Launch Claude from your Applications folder on macOS or the Start menu on Windows, then sign in with your Anthropic account.
2. **Open the Code tab** — Click the **Code** tab at the top center. If clicking Code prompts you to upgrade, you need to subscribe to a paid plan first. If it prompts you to sign in online, complete the sign-in and restart the app. If you see a 403 error, see the [authentication troubleshooting](https://code.claude.com/docs/en/desktop#403-or-authentication-errors-in-the-code-tab) section.

The desktop app includes Claude Code — you don't need to install Node.js or the CLI separately. To use `claude` from the terminal, install the CLI separately (see [Get started with the CLI](https://code.claude.com/docs/en/quickstart)).

## Start Your First Session

With the Code tab open, choose a project and give Claude something to do.

1. **Choose an environment and folder** — Select **Local** to run Claude on your machine using your files directly. Click **Select folder** and choose your project directory. (Start with a small project you know well — it's the fastest way to see what Claude Code can do. On Windows, Git must be installed for local sessions to work; most Macs include Git by default.) You can also select:
   - **Remote**: Run sessions on Anthropic's cloud infrastructure that continue even if you close the app. Cloud sessions use the same infrastructure as Claude Code on the web.
   - **SSH**: Connect to a remote machine over SSH, such as your own servers, cloud VMs, or dev containers. Desktop installs Claude Code on the remote machine automatically the first time you connect.
2. **Choose a model** — Select a model from the dropdown next to the send button (see [models](https://code.claude.com/docs/en/model-config#available-models) for a comparison). You can change the model later from the same dropdown.
3. **Tell Claude what to do** — Type what you want Claude to do, for example: `Find a TODO comment and fix it`, `Add tests for the main function`, or `Create a CLAUDE.md with instructions for this codebase`. A session is a conversation with Claude about your code; each session tracks its own context and changes, so you can work on multiple tasks without them interfering with each other.
4. **Review and accept changes** — By default, the Code tab starts in **Ask permissions mode**, where Claude proposes changes and waits for your approval before applying them. You'll see (1) a diff view showing exactly what will change in each file, (2) Accept/Reject buttons to approve or decline each change, and (3) real-time updates as Claude works through your request. If you reject a change, Claude asks how you'd like to proceed differently. Your files aren't modified until you accept.

## Now What?

After your first edit, here are things to try next (each links into the full desktop reference):

- **Interrupt and steer.** Redirect Claude at any point. Click the stop button to interrupt immediately, or type a correction and press **Enter** to send it without stopping the running action — you don't have to wait for it to finish or start over.
- **Give Claude more context.** Type `@filename` in the prompt box to pull a specific file into the conversation, attach images and PDFs using the attachment button, or drag and drop files directly into the prompt.
- **Use skills for repeatable tasks.** Type `/` or click **+** → **Slash commands** to browse built-in commands, custom skills, and plugin skills. Skills are reusable prompts you can invoke whenever you need them, like code review checklists or deployment steps.
- **Review changes before committing.** After Claude edits files, a `+12 -1` indicator appears. Click it to open the diff view, review modifications file by file, and comment on specific lines (Claude reads your comments and revises). Click **Review code** to have Claude evaluate the diffs itself and leave inline suggestions.
- **Adjust how much control you have.** Your permission mode controls the balance: Ask permissions (default) requires approval before every edit, Auto accept edits auto-accepts file edits for faster iteration, and Plan mode lets Claude map out an approach without touching any files (useful before a large refactor).
- **Add plugins for more capabilities.** Click the **+** button next to the prompt box and select **Plugins** to browse and install plugins that add skills, agents, MCP servers, and more.
- **Arrange your workspace.** Drag the chat, diff, terminal, file, and preview panes into whatever layout you want. Open the terminal with **Ctrl+`** to run commands alongside your session, or click a file path to open it in the file pane.
- **Preview your app.** Click the **Preview** dropdown to run your dev server directly in the desktop. Claude can view the running app, test endpoints, inspect logs, and iterate on what it sees.
- **Track your pull request.** After opening a PR, Claude Code monitors CI check results and can automatically fix failures or merge the PR once all checks pass.
- **Put Claude on a schedule.** Set up [scheduled tasks](cc_desktop_scheduled_tasks.md) to run Claude automatically on a recurring basis: a daily code review every morning, a weekly dependency audit, or a briefing that pulls from your connected tools.
- **Scale up when you're ready.** Open parallel sessions from the sidebar to work on multiple tasks at once, each in its own Git worktree, and open the tasks pane to watch the subagents and background commands a session has running. Open a side chat to ask a question without derailing the main thread. Send long-running work to the cloud so it continues even if you close the app, or continue a session on the web or in your IDE if a task takes longer than expected. Connect external tools like GitHub, Slack, and Linear to bring your workflow together.

## Coming from the CLI?

Desktop runs the same engine as the CLI with a graphical interface. You can run both simultaneously on the same project, and they share configuration (CLAUDE.md files, MCP servers, hooks, skills, and settings). For a full comparison of features, flag equivalents, and what's not available in Desktop, see [CLI comparison](https://code.claude.com/docs/en/desktop#coming-from-the-cli).

## What's Next

- [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop): permission modes, parallel sessions, diff view, connectors, and enterprise configuration
- [Troubleshooting](https://code.claude.com/docs/en/desktop#troubleshooting): solutions to common errors and setup issues
- [Best practices](https://code.claude.com/docs/en/best-practices): tips for writing effective prompts and getting the most out of Claude Code
- [Common workflows](https://code.claude.com/docs/en/common-workflows): tutorials for debugging, refactoring, testing, and more

**Source**: https://code.claude.com/docs/en/desktop-quickstart
**Last Updated**: 2026-06-13
**Status**: Active
