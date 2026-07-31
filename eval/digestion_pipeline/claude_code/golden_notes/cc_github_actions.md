---
tags:
  - resource
  - documentation
  - claude_code
  - github_actions
  - ci_cd
keywords:
  - github actions
  - claude-code-action
  - install-github-app
  - claude mention trigger
  - claude_args
  - prompt input
  - skills in actions
  - claude.md guidelines
  - ci costs
topics:
  - Claude Code
  - GitHub Actions
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/github-actions
access_control_group: ["general"]
---

# Claude Code GitHub Actions

## Overview

Claude Code GitHub Actions brings AI-powered automation to your GitHub workflow: a simple `@claude` mention in any PR or issue lets Claude analyze code, create pull requests, implement features, and fix bugs while following your project's standards. Your code stays on GitHub's runners, and the integration is built on top of the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) so you can also build custom automation workflows beyond GitHub Actions.

This note documents how to wire the Action into a repository (quick + manual setup), the `@claude` trigger, the `claude-code-action@v1` workflow shape, the `prompt` / `claude_args` / skills inputs, best practices (`CLAUDE.md`, security, cost), and advanced configuration. Running the Action against your own Amazon Bedrock or Google Vertex AI infrastructure is a distinct multi-step procedure documented in [cc_github_actions_cloud_providers](cc_github_actions_cloud_providers.md). For automatic reviews posted on every PR without a trigger, see [cc_code_review](cc_code_review.md).

## Why use Claude Code GitHub Actions?

- **Instant PR creation**: describe what you need, and Claude creates a complete PR with all necessary changes.
- **Automated code implementation**: turn issues into working code with a single command.
- **Follows your standards**: Claude respects your `CLAUDE.md` guidelines and existing code patterns.
- **Simple setup**: get started in minutes with the installer and API key.
- **Secure by default**: your code stays on GitHub's runners.

## What can Claude do?

The **Claude Code Action** lets you run Claude Code within your GitHub Actions workflows, so you can build any custom workflow on top of Claude Code (action repository: `github.com/anthropics/claude-code-action`).

## Setup

### Quick setup

The easiest way to set up the action is through Claude Code in the terminal — open `claude` and run `/install-github-app`. This command guides you through setting up the GitHub app and required secrets. Note:

- You must be a repository admin to install the GitHub app and add secrets.
- The GitHub app will request read & write permissions for Contents, Issues, and Pull requests.
- This quickstart method is only available for direct Claude API users. If you use Amazon Bedrock or Google Vertex AI, see [cc_github_actions_cloud_providers](cc_github_actions_cloud_providers.md).

### Manual setup

If `/install-github-app` fails or you prefer manual setup:

1. **Install the Claude GitHub app** to your repository (`github.com/apps/claude`). It requires these repository permissions: **Contents** Read & write (to modify repository files), **Issues** Read & write (to respond to issues), **Pull requests** Read & write (to create PRs and push changes).
2. **Add `ANTHROPIC_API_KEY`** to your repository secrets.
3. **Copy the workflow file** from `examples/claude.yml` into your repository's `.github/workflows/`.

After either path, test the action by tagging `@claude` in an issue or PR comment.

## Upgrading from Beta

Claude Code GitHub Actions v1.0 introduces **breaking changes** that require updating workflow files to upgrade from the beta. The GA version simplifies configuration while adding features like automatic mode detection. Essential changes all beta users must make:

1. **Update the action version**: change `@beta` to `@v1`.
2. **Remove mode configuration**: delete `mode: "tag"` or `mode: "agent"` (now auto-detected).
3. **Update prompt inputs**: replace `direct_prompt` with `prompt`.
4. **Move CLI options**: convert `max_turns`, `model`, `custom_instructions`, etc. to `claude_args`.

Breaking-changes reference: `mode` is removed (auto-detected); `direct_prompt` → `prompt`; `override_prompt` → `prompt` with GitHub variables; `custom_instructions` → `claude_args: --append-system-prompt`; `max_turns` → `claude_args: --max-turns`; `model` → `claude_args: --model`; `allowed_tools` → `claude_args: --allowedTools`; `disallowed_tools` → `claude_args: --disallowedTools`; `claude_env` → `settings` JSON format. The action now automatically detects whether to run in interactive mode (responds to `@claude` mentions) or automation mode (runs immediately with a prompt) based on your configuration.

## Example use cases

### Basic workflow

```yaml theme={null}
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # Responds to @claude mentions in comments
```

### Using skills

The `prompt` input accepts a [skill](https://code.claude.com/docs/en/skills) invocation as well as plain text:

- For a skill in your repository's `.claude/skills/` directory, run `actions/checkout` before the action step and pass `/skill-name`.
- For a skill packaged in a plugin, install the plugin with the `plugin_marketplaces` and `plugins` inputs and pass the namespaced `/plugin-name:skill-name`.

The following workflow installs the `code-review` plugin and runs its skill on each new or updated pull request:

```yaml theme={null}
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          plugin_marketplaces: "https://github.com/anthropics/claude-code.git"
          plugins: "code-review@claude-code-plugins"
          prompt: "/code-review:code-review ${{ github.repository }}/pull/${{ github.event.pull_request.number }}"
```

### Custom automation with prompts

A scheduled (`cron`) job can run Claude immediately with a `prompt` (and optionally a `claude_args` such as `"--model opus"`), for example to generate a daily summary of yesterday's commits and open issues.

### Common use cases

In issue or PR comments, mention `@claude` with the task, for example:

```text theme={null}
@claude implement this feature based on the issue description
@claude how should I implement user authentication for this endpoint?
@claude fix the TypeError in the user dashboard component
```

Claude automatically analyzes the context and responds appropriately.

## Best practices

- **`CLAUDE.md` configuration**: create a `CLAUDE.md` file in your repository root to define code style guidelines, review criteria, project-specific rules, and preferred patterns. This file guides Claude's understanding of your project standards.
- **Security considerations**: never commit API keys directly to your repository. Always use GitHub Secrets for API keys — add your key as a repository secret named `ANTHROPIC_API_KEY` and reference it in workflows as `anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`; limit action permissions to only what's necessary; and review Claude's suggestions before merging.
- **Optimizing performance**: use issue templates to provide context, keep your `CLAUDE.md` concise and focused, and configure appropriate timeouts.
- **CI costs**: Claude Code runs on **GitHub-hosted runners**, which consume your GitHub Actions minutes; each Claude interaction also consumes **API tokens** based on prompt/response length and task complexity. To optimize: use specific `@claude` commands to reduce unnecessary API calls, configure appropriate `--max-turns` in `claude_args`, set workflow-level timeouts to avoid runaway jobs, and consider GitHub's concurrency controls to limit parallel runs.

## Configuration examples

The Claude Code Action v1 simplifies configuration with unified parameters:

```yaml theme={null}
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Your instructions here" # Optional
    claude_args: "--max-turns 5" # Optional CLI arguments
```

Key features: a **unified prompt interface** (use `prompt` for all instructions), **Skills** (invoke installed skills directly from the prompt), **CLI passthrough** (any Claude Code CLI argument via `claude_args`), and **flexible triggers** (works with any GitHub event). When responding to issue/PR comments, Claude automatically responds to `@claude` mentions; for other events, use the `prompt` parameter to provide instructions.

## Troubleshooting

- **Claude not responding to `@claude` commands**: verify the GitHub App is installed correctly, check that workflows are enabled, ensure the API key is set in repository secrets, and confirm the comment contains `@claude` (not `/claude`).
- **CI not running on Claude's commits**: ensure you're using the GitHub App or custom app (not the Actions user), check workflow triggers include the necessary events, and verify app permissions include CI triggers.
- **Authentication errors**: confirm the API key is valid and has sufficient permissions. For Bedrock/Vertex, check credentials configuration and ensure secrets are named correctly in workflows.

## Advanced configuration

### Action parameters

The Claude Code Action v1 uses a simplified configuration. Key inputs: `prompt` (instructions for Claude — plain text or a skill name; optional), `claude_args` (CLI arguments passed to Claude Code; optional), `plugin_marketplaces` (newline-separated plugin marketplace Git URLs; optional), `plugins` (newline-separated plugin names to install before execution; optional), `anthropic_api_key` (Claude API key; required for direct Claude API, not for Bedrock/Vertex), `github_token` (GitHub token for API access; optional), `trigger_phrase` (custom trigger phrase, default `"@claude"`; optional), `use_bedrock` and `use_vertex` (use Amazon Bedrock / Google Vertex AI instead of the Claude API; optional). When `prompt` is omitted for issue/PR comments, Claude responds to the trigger phrase.

### Pass CLI arguments

The `claude_args` parameter accepts any Claude Code CLI arguments, for example:

```yaml theme={null}
claude_args: "--max-turns 5 --model claude-sonnet-4-6 --mcp-config /path/to/config.json"
```

Common arguments: `--max-turns` (maximum conversation turns, default 10), `--model` (model to use, e.g. `claude-sonnet-4-6`), `--mcp-config` (path to MCP configuration), `--allowedTools` (comma-separated list of allowed tools; the `--allowed-tools` alias also works), and `--debug` (enable debug output).

### Alternative integration methods

While `/install-github-app` is the recommended approach, you can also use a **Custom GitHub App** (for organizations needing branded usernames or custom authentication — create your own app with the required permissions and use `actions/create-github-app-token` to generate tokens), **Manual GitHub Actions** (direct workflow configuration for maximum flexibility), or **MCP Configuration** (dynamic loading of Model Context Protocol servers).

### Customizing Claude's behavior

You can configure Claude's behavior in two ways: **`CLAUDE.md`** — define coding standards, review criteria, and project-specific rules in a `CLAUDE.md` file at the repository root, which Claude follows when creating PRs and responding to requests (see [Memory documentation](https://code.claude.com/docs/en/memory)); and **Custom prompts** — use the `prompt` parameter in the workflow file to provide workflow-specific instructions, customizing Claude's behavior for different workflows or tasks.

**Source**: https://code.claude.com/docs/en/github-actions
**Last Updated**: 2026-06-13
**Status**: Active
