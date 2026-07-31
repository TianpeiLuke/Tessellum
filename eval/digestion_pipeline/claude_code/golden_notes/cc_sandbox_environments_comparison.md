---
tags:
  - resource
  - documentation
  - claude_code
  - sandboxing
  - isolation
keywords:
  - sandbox environments
  - isolation decision matrix
  - choose an approach
  - sandboxed bash tool
  - sandbox runtime
  - dev container
  - virtual machine
  - isolation vs permission modes
topics:
  - Claude Code
  - Sandboxing
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/sandbox-environments
access_control_group: ["general"]
---

# Choose a Claude Code Sandbox Environment

## Overview

Isolating Claude Code limits what a session can read, write, and reach on the network. This matters most when you let Claude work with fewer permission prompts, run it unattended, or point it at code you do not fully trust. Claude Code can run in several kinds of isolated environments, ranging from a lightweight per-command sandbox to a fully separate virtual machine.

This note is the **decision matrix**: it compares the available isolation approaches by what each one isolates, whether it requires Docker, and how much setup it involves; maps a goal to the right approach; and explains how an isolation boundary layers with [permission modes](https://code.claude.com/docs/en/permission-modes). The whole-process setup walkthroughs (runtime, containers, VM, web) live in [Sandbox Runtime and Containers](cc_sandbox_runtime_and_containers.md); the built-in per-command Bash tool is covered by the sibling notes starting with [Sandboxed Bash Tool Setup](cc_sandboxed_bash_tool_setup.md).

## Compare sandboxing approaches

The first two approaches in the table below run on the host operating system without containers. The rest place Claude Code inside a container or virtual machine.

| Approach | What is isolated | Requires Docker | Setup effort |
| :--- | :--- | :--- | :--- |
| Sandboxed Bash tool | Bash commands and their child processes | No | Minimal on macOS; low on Linux and WSL2 |
| Sandbox runtime | The whole Claude Code process, including file tools, MCP servers, and hooks | No | Low |
| Dev container | Full development environment | Yes | Medium |
| Custom container | Full development environment | Yes | Medium to high |
| Virtual machine | Full operating system | No | High |
| Claude Code on the web | Full operating system, hosted by Anthropic | No | None; requires a Claude subscription and GitHub |

The [sandboxed Bash tool](cc_sandboxed_bash_tool_setup.md) is built into Claude Code and restricts only Bash commands. Built-in file tools, MCP servers, and hooks still run directly on your host. Every other approach in the table puts the **whole Claude Code process** inside the isolation boundary, so file tools, MCP servers, and hooks are restricted too.

Sandbox isolation reduces the impact of a breach, but it does not eliminate risk. Any approach that allows network egress can still leak data the agent can read, and any approach that mounts your project directory writable can still modify that code (see [Sandbox Limitations and Troubleshooting](cc_sandbox_limitations_and_troubleshooting.md)). Isolation also does not change what is sent to the model: your prompts and the files Claude reads are transmitted to the Anthropic API or your configured provider with or without a sandbox (see [Data usage](https://code.claude.com/docs/en/data-usage)).

## Choose an approach

Match your goal to a row below, then read the detail section for the approach.

| You want to | Start with |
| :--- | :--- |
| Reduce permission prompts during everyday work on your own machine | The sandboxed Bash tool, enabled with `/sandbox` |
| Let Claude work unattended with `--dangerously-skip-permissions` or auto mode | The preconfigured dev container, any container or VM, or the sandbox runtime |
| Isolate MCP servers and hooks as well as Bash, without Docker | The sandbox runtime |
| Work on an untrusted repository | A dedicated virtual machine, or Claude Code on the web if you have a Claude subscription and a connected GitHub account |
| Standardize a sandboxed environment across a team | The preconfigured dev container, copied into your repository |
| Use Claude Code from a device with no local setup | Claude Code on the web, which requires a Claude subscription and a connected GitHub account |
| Require isolation for every developer in your organization | [Enforce isolation across an organization](cc_sandbox_org_enforcement.md) |
| Work on a native Windows host | A container or VM, or run the Bash sandbox inside WSL2 |

The setup details for the runtime, dev container, custom container, VM, and web approaches are in [Sandbox Runtime and Containers](cc_sandbox_runtime_and_containers.md). The dev container has its own page ([devcontainer](https://code.claude.com/docs/en/devcontainer)); Claude Code on the web has its own page ([claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web)). The built-in Bash tool is covered by [Sandboxed Bash Tool Setup](cc_sandboxed_bash_tool_setup.md) and its sibling notes.

## How isolation relates to permission modes

[Permission modes](https://code.claude.com/docs/en/permission-modes) decide whether a tool call runs and whether you are prompted first. Isolation restricts what a command can access once it runs. The two work together: when a permission mode lets actions run without asking you, an isolation boundary limits what those actions can reach.

- **`--dangerously-skip-permissions`** removes per-action review other than explicit [ask rules](https://code.claude.com/docs/en/permissions), so an isolation boundary is the **only** thing limiting what Claude can do. Always run it inside a container, a VM, or the sandbox runtime, so that file tools, MCP servers, and hooks are also inside the boundary.
- **Auto mode** replaces the prompt with a classifier that reviews actions and blocks ones that escalate beyond the request, target unrecognized infrastructure, or appear driven by hostile content Claude read. The classifier is a per-action control, not an isolation boundary, so an isolation boundary still adds defense in depth for unattended runs — but is not required the way it is for `--dangerously-skip-permissions`.

The [sandboxed Bash tool](cc_sandboxed_bash_tool_setup.md) on its own constrains only Bash, so it is not sufficient for fully unattended runs in either mode. You can **layer** approaches: running the sandboxed Bash tool inside a container or VM gives you OS-level command restrictions on top of the outer environment boundary. For how the Bash sandbox itself interacts with permission rules and modes, see [Sandbox vs Permissions](cc_sandbox_vs_permissions.md).

**Source**: https://code.claude.com/docs/en/sandbox-environments
**Last Updated**: 2026-06-13
**Status**: Active
