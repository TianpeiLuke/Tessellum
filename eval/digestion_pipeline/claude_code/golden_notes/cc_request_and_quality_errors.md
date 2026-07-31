---
tags:
  - resource
  - documentation
  - claude_code
  - errors
  - request_errors
keywords:
  - prompt is too long
  - request too large
  - error during compaction
  - thinking budget exceeds output limit
  - tool use or thinking block mismatch
  - usage policy refusal
  - responses lower quality
  - claude code request errors
topics:
  - Claude Code
  - Errors
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/errors
access_control_group: ["general"]
---

# Claude Code — Request and Quality Errors

## Overview

Request errors mean the API received your request but rejected its content — the prompt or attachment is too large, an image or PDF could not be processed, a gateway stripped a beta header, the selected model is wrong or out of plan, an extended-thinking configuration is invalid, the conversation reached an inconsistent tool/thinking-block state, or content triggered a Usage Policy check. This note is the symptom -> cause -> fix lookup for those request-content errors, plus the no-error case "Responses seem lower quality than usual," and how to report an error that is not listed.

These errors and recovery commands apply across the CLI, the Desktop app, and Claude Code on the web, since all three wrap the same Claude Code CLI. For server-side and account-quota errors see [Server and usage-limit errors](cc_server_and_usage_limit_errors.md); for authentication and network failures see [Authentication and network errors](cc_authentication_and_network_errors.md).

## Prompt is too long

The conversation plus attached files exceeds the model's context window.

```text
Prompt is too long
```

**What to do:**

- Run `/compact` to summarize earlier turns and free space, or `/clear` to start fresh.
- Run `/context` to see a breakdown of what is consuming the window: system prompt, tools, memory files, and messages.
- Disable MCP servers you are not using with `/mcp disable <name>` to remove their tool definitions from context.
- Trim large `CLAUDE.md` memory files, or move instructions into path-scoped rules that load only when relevant.
- Subagents inherit every MCP tool definition from the parent session, which can fill their context window before the first turn. Disable MCP servers you are not using before spawning subagents.
- Auto-compact is on by default and normally prevents this error. If you have set `DISABLE_AUTO_COMPACT`, re-enable it or run `/compact` manually before the window fills.

## Error during compaction: Conversation too long

`/compact` itself failed because there is not enough free context to hold the summary it produces. This can happen when the window is already full at the moment auto-compact triggers, or when you run `/compact` after seeing `Prompt is too long`.

```text
Error during compaction: Conversation too long. Press esc twice to go up a few messages and try again.
```

**What to do:**

- Press Esc twice to open the message list and step back several turns. This drops the most recent messages from context. Then run `/compact` again.
- If stepping back does not free enough space, run `/clear` to start a fresh session. Your previous conversation is preserved and can be reopened with `/resume`.

## Request too large

The raw request body exceeded the API's byte limit before tokenization, usually because of a large pasted file or attachment. This is a size limit on the HTTP request, separate from the context window limit (Prompt is too long).

```text
Request too large (max 30 MB). Double press esc to go back and remove or shrink the attached content.
```

**What to do:**

- Press Esc twice and step back past the turn that added the oversized content.
- Reference large files by path instead of pasting their contents, so Claude can read them in chunks.
- For images, see Image was too large below.

## Image, resize, and PDF errors

Three families of attachment errors share the same shape — the API or the native image processor rejected the file:

- **Image was too large** — a pasted or attached image exceeds the API's size or dimension limits (`Image was too large. Double press esc to go back and try again with a smaller image.`; `API Error: 400 ... image dimensions exceed max allowed size`). From v2.1.142, Claude Code replaces the unprocessable image with a text placeholder and retries; on earlier versions press Esc twice and step back past the turn where the image was added. The API accepts images up to 8000 pixels on the longest edge for a single image, or 2000 pixels when many images are in context. Resize before pasting, or take a tighter screenshot of the relevant region.
- **Unable to resize image** — Claude Code could not downscale the image before sending (image processor failed to load or returned an error; messages cite the 2000x2000px limit or a failed dimension read). If asked to convert, convert to PNG, JPEG, GIF, or WebP and re-attach; if a size/dimension limit is reported, resize or recompress below the limit first.
- **PDF errors** — the attached PDF could not be processed (`PDF too large (max 100 pages, 32 MB).`; `PDF is password protected.`; `The PDF file was not valid.`). For oversized PDFs, ask Claude to read a page range with the Read tool, or extract text with a tool like `pdftotext` and reference the output file by path. For protected or invalid PDFs, remove the password or re-export the file, then try again.

## Extra inputs are not permitted

A proxy or LLM gateway between Claude Code and the API stripped the `anthropic-beta` request header, so the API rejected fields that depend on it. Claude Code sends beta-only fields such as `context_management`, `effort`, and tool `input_examples` alongside an `anthropic-beta` header that enables them; when a gateway forwards the body but drops the header, the API sees fields it does not recognize.

```text
API Error: 400 ... Extra inputs are not permitted ... context_management
API Error: 400 ... Extra inputs are not permitted ... tools.0.custom.input_examples
API Error: 400 ... Unexpected value(s) for the `anthropic-beta` header
```

**What to do:**

- Configure your gateway to forward the `anthropic-beta` header.
- As a fallback, set `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` before launching. This disables features that require the beta header so requests succeed through a gateway that cannot forward it.

## Model selection errors

Two errors mean the configured model cannot be used:

- **There's an issue with the selected model** — the configured model name was not recognized or your account lacks access (`There's an issue with the selected model (claude-...). It may not exist or you may not have access to it. Run /model to pick a different model.`). In the interactive CLI run `/model`; in non-interactive mode (`-p`) pass `--model` with a valid alias or ID, or set `ANTHROPIC_MODEL` (the hint shows `Run --model`); in the Agent SDK set `model` on `Options` and handle the structured `model_not_found` error. Prefer an alias such as `sonnet` or `opus` over a full versioned ID so it does not go stale. If a stale model keeps coming back, check in priority order: the `--model` flag, the `ANTHROPIC_MODEL` env var, then `model` in `.claude/settings.local.json`, your project's `.claude/settings.json`, and `~/.claude/settings.json`.
- **Claude Opus is not available with the Claude Pro plan** — your active plan does not include the selected model (`Claude Opus is not available with the Claude Pro plan · Select a different model in /model`). Run `/model` and select a model your plan includes. If you upgraded recently and still see it, run `/logout` then `/login` — the stored token reflects your plan at sign-in, so upgrading on the web does not take effect in an existing session until you re-authenticate.

## Extended thinking errors

Two errors come from an invalid extended-thinking (reasoning) configuration:

- **thinking.type.enabled is not supported for this model** — your Claude Code version is older than the minimum for Opus 4.7 or Opus 4.8; the CLI sent a thinking configuration the model no longer accepts (`API Error: 400 ... "thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.`). Run `claude update` and restart — Opus 4.7 needs v2.1.111+, Opus 4.8 needs v2.1.154+ — or run `/model` and select Opus 4.6 or Sonnet instead.
- **Thinking budget exceeds output limit** — the configured thinking budget exceeds the maximum response length, leaving no room for the answer (`API Error: 400 ... max_tokens must be greater than thinking.budget_tokens`). Claude Code adjusts these automatically on the Anthropic API; you typically see this on Amazon Bedrock or Google Vertex AI when `MAX_THINKING_TOKENS` is set higher than the provider's output limit, or when plan mode raises the budget. Lower `MAX_THINKING_TOKENS`, or raise `CLAUDE_CODE_MAX_OUTPUT_TOKENS` above the thinking budget.

## Tool use or thinking block mismatch

The conversation history reached the API in an inconsistent state, usually after a tool call was interrupted or a turn was edited mid-stream. All three variants mean the same thing: the sequence of `tool_use`, `tool_result`, and `thinking` blocks in history no longer matches what the API expects.

```text
API Error: 400 due to tool use concurrency issues. Run /rewind to recover the conversation.
API Error: 400 ... unexpected `tool_use_id` found in `tool_result` blocks
API Error: 400 ... thinking blocks ... cannot be modified
```

**What to do:**

- If you are using Opus 4.7 or Opus 4.8, run `claude update` first. Versions before v2.1.156 can trigger this error during normal tool use, and `/rewind` does not clear it.
- Run `/rewind`, or press Esc twice, to step back to a checkpoint before the corrupted turn and continue from there.

## Usage Policy refusal

The API declined to respond because content in the conversation triggered a Usage Policy check. The message includes a Request ID you can quote to support if you believe the refusal is incorrect. The check evaluates the full conversation, not only your latest prompt, so sending a new message in the same session usually re-triggers the same refusal — and the same applies after reopening the session with `--continue` or `--resume`, since the transcript on disk still contains the triggering content.

```text
API Error: Claude Code is unable to respond to this request, which appears to violate our Usage Policy (https://www.anthropic.com/legal/aup). Please double press esc to edit your last message or start a new session for Claude Code to assist with a different task.
```

**What to do:**

- Press Esc twice or run `/rewind` to step back to a checkpoint before the turn that triggered the refusal, then rephrase or take a different approach.
- If you cannot identify which turn caused it, run `/clear` to start a fresh conversation in the same project. Your previous conversation is preserved on disk and remains available in `/resume`.
- In non-interactive mode (`-p`), where rewind is unavailable, retry with a rephrased prompt in a new session without `--continue`. Policy checks vary by model, so switching to a different model with `--model` may also resolve the refusal in some cases.

## Responses seem lower quality than usual

If Claude's answers seem less capable than you expect but no error is shown, the cause is usually conversation state rather than the model itself. Claude Code does not silently change model versions, but it can switch to a fallback model in three specific cases: a configured `--fallback-model` takes over after an availability error (for that turn only, with a transcript notice); a Bedrock or Vertex AI startup check finds your default model unavailable; or automatic model fallback on Fable 5 moves the session to the default Opus model with a transcript notice.

Check these first:

- **Model selection**: run `/model` to confirm you are on the model you expect. A previous `/model` choice or an `ANTHROPIC_MODEL` environment variable may have you on a smaller model than intended.
- **Effort level**: run `/effort` to check the current reasoning level and raise it for hard debugging or design work. Defaults vary by model, so check before assuming you are below the maximum.
- **Context pressure**: run `/context` to see how full the window is. If it is near capacity, run `/compact` at a natural breakpoint or `/clear` to start fresh.
- **Stale instructions**: large or outdated `CLAUDE.md` files and MCP tool definitions consume context and can steer responses. `/doctor` flags oversized memory files and subagent definitions; `/context` shows MCP tool token usage.

When a response goes wrong, rewinding usually works better than replying with corrections. Press Esc twice or run `/rewind` to step back to before the bad turn, then rephrase the prompt with more specifics — correcting in-thread keeps the wrong attempt in context, which can anchor later answers to it. If quality still seems off, run `/feedback` and describe what you expected versus what you got; feedback submitted this way includes the conversation transcript.

## Report an error

This page covers errors from the Claude API. For errors from other Claude Code components, see the relevant guide: MCP server connect/authenticate failures route to MCP, hook script failures route to Debug hooks, and permission/filesystem errors during install route to [Troubleshoot installation and login](https://code.claude.com/docs/en/troubleshoot-install).

If an error is not listed or the suggested fix does not help:

- Run `/feedback` inside Claude Code to send the transcript and a description to Anthropic. The command also offers to open a prefilled GitHub issue. On Bedrock, Vertex AI, Foundry, and other third-party providers, `/feedback` saves a local archive you can send to your Anthropic account representative instead.
- Run `/doctor` to check for local configuration problems.
- Check [status.claude.com](https://status.claude.com) for active incidents.
- Search existing issues on GitHub.

**Source**: https://code.claude.com/docs/en/errors
**Last Updated**: 2026-06-13
**Status**: Active
