---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - user_input
keywords:
  - askuserquestion
  - clarifying questions
  - canusetool callback
  - questions array
  - answers map
  - multiselect
  - option previews
  - free-text input
  - plan mode
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/user-input
access_control_group: ["general"]
---

# Handle Clarifying Questions (AskUserQuestion)

## Overview

When Claude needs more direction on a task with multiple valid approaches, it calls the **`AskUserQuestion`** tool, which triggers your `canUseTool` callback with `toolName` set to `AskUserQuestion`. The input carries Claude's questions as multiple-choice options; your job is to display them, collect the user's selections, and return them. This is the SDK's structured clarification channel — Claude generates the questions and options, and you present them and return the picks. Clarifying questions are especially common in [`plan` mode](https://code.claude.com/docs/en/agent-sdk/permissions#plan-mode-plan), where Claude explores the codebase and asks questions before proposing a plan.

This procedure shows how to wire `AskUserQuestion` into your `tools` array, parse the `questions` input, collect answers, and return the `answers` map — plus option previews, free-text input, limits, and other input avenues. It is the clarifying-questions half of the user-input flow; the tool-approval half (allow/deny `canUseTool` responses) is covered in [`cc_sdk_tool_approval_handling`](cc_sdk_tool_approval_handling.md) and the callback model in [`cc_sdk_user_input_overview`](cc_sdk_user_input_overview.md).

## The five-step flow

1. **Pass a `canUseTool` callback** in your query options. By default `AskUserQuestion` is available. If you specify a `tools` array to restrict Claude's capabilities (for example, a read-only agent with only `Read`, `Glob`, and `Grep`), you **must include `AskUserQuestion`** in that array — otherwise Claude won't be able to ask clarifying questions.
2. **Detect `AskUserQuestion`** — in the callback, check if `toolName == "AskUserQuestion"` to handle it differently from other tools (route to a dedicated handler), and handle other tools normally.
3. **Parse the question input** — the input contains Claude's questions in a `questions` array. Each question has a `question` (text to display), `options` (the choices), and `multiSelect` (whether multiple selections are allowed).
4. **Collect answers from the user** — present the questions and collect selections; how you do this depends on your application (terminal prompt, web form, mobile dialog, etc.).
5. **Return answers to Claude** — build the `answers` object as a record where each key is the `question` text and each value is the selected option's `label`. For multi-select questions, pass an array of labels or join them with `", "`. If you support free-text input, use the user's custom text as the value.

## Question format

The input contains Claude's generated questions in a `questions` array. Each question has these fields:

| Field | Description |
| --- | --- |
| `question` | The full question text to display |
| `header` | Short label for the question (max 12 characters) |
| `options` | Array of 2-4 choices, each with `label` and `description`. TypeScript: optionally `preview` |
| `multiSelect` | If `true`, users can select multiple options |

The structure your callback receives:

```json
{
  "questions": [
    {
      "question": "How should I format the output?",
      "header": "Format",
      "options": [
        { "label": "Summary", "description": "Brief overview of key points" },
        { "label": "Detailed", "description": "Full explanation with examples" }
      ],
      "multiSelect": false
    }
  ]
}
```

### Option previews (TypeScript)

`toolConfig.askUserQuestion.previewFormat` adds a `preview` field to each option so your app can show a visual mockup alongside the label. Without this setting, Claude does not generate previews and the field is absent.

| `previewFormat` | `preview` contains |
| --- | --- |
| unset (default) | Field is absent. Claude does not generate previews. |
| `"markdown"` | ASCII art and fenced code blocks |
| `"html"` | A styled `<div>` fragment (the SDK rejects `<script>`, `<style>`, and `<!DOCTYPE>` before your callback runs) |

The format applies to all questions in the session. Claude includes `preview` on options where a visual comparison helps (layout choices, color schemes) and omits it where one wouldn't (yes/no confirmations, text-only choices). Check for `undefined` before rendering.

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Help me choose a card layout",
  options: {
    toolConfig: {
      askUserQuestion: { previewFormat: "html" }
    },
    canUseTool: async (toolName, input) => {
      // input.questions[].options[].preview is an HTML string or undefined
      return { behavior: "allow", updatedInput: input };
    }
  }
})) {
  // ...
}
```

## Response format

Return an `answers` object mapping each question's `question` field to the selected option's `label`:

| Field | Description |
| --- | --- |
| `questions` | Pass through the original questions array (required for tool processing) |
| `answers` | Object where keys are question text and values are selected labels |
| `response` | Optional freeform reply the user typed instead of answering the structured questions |

For multi-select questions, pass an array of labels or join them with `", "`. For per-question free text such as an "Other" option, put the user's text in `answers[question]`. Set `response` only when your UI lets the user dismiss the question card and type a general reply that isn't an answer to any specific question. When `response` is set, Claude receives "The user responded: …" instead of the per-question answer list.

```json
{
  "questions": [
    // ...
  ],
  "answers": {
    "How should I format the output?": "Summary",
    "Which sections should I include?": ["Introduction", "Conclusion"]
  }
}
```

### Support free-text input

Claude's predefined options won't always cover what users want. To let users type their own answer: display an additional "Other" choice after Claude's options that accepts text input, and use the user's custom text as the answer value (not the word "Other"). The complete example below shows a full implementation.

## Complete example

When asked to help decide on a tech stack for a mobile app, Claude might ask about cross-platform vs native, backend preferences, or target platforms — questions that help Claude make decisions matching the user's preferences rather than guessing. This terminal example: (1) routes the request when `toolName == "AskUserQuestion"`; (2) loops through the `questions` array printing each question with numbered options; (3) collects input (a number to select, or free text directly); (4) maps answers (numeric → option's label; free text → text directly); (5) returns both the original `questions` array and the `answers` mapping.

```python Python
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query
from claude_agent_sdk.types import HookMatcher, PermissionResultAllow


def parse_response(response: str, options: list) -> str:
    """Parse user input as option number(s) or free text."""
    try:
        indices = [int(s.strip()) - 1 for s in response.split(",")]
        labels = [options[i]["label"] for i in indices if 0 <= i < len(options)]
        return ", ".join(labels) if labels else response
    except ValueError:
        return response


async def handle_ask_user_question(input_data: dict) -> PermissionResultAllow:
    """Display Claude's questions and collect user answers."""
    answers = {}

    for q in input_data.get("questions", []):
        print(f"\n{q['header']}: {q['question']}")

        options = q["options"]
        for i, opt in enumerate(options):
            print(f"  {i + 1}. {opt['label']} - {opt['description']}")
        if q.get("multiSelect"):
            print("  (Enter numbers separated by commas, or type your own answer)")
        else:
            print("  (Enter a number, or type your own answer)")

        response = input("Your choice: ").strip()
        answers[q["question"]] = parse_response(response, options)

    return PermissionResultAllow(
        updated_input={
            "questions": input_data.get("questions", []),
            "answers": answers,
        }
    )


async def can_use_tool(
    tool_name: str, input_data: dict, context
) -> PermissionResultAllow:
    # Route AskUserQuestion to our question handler
    if tool_name == "AskUserQuestion":
        return await handle_ask_user_question(input_data)
    # Auto-approve other tools for this example
    return PermissionResultAllow(updated_input=input_data)


async def prompt_stream():
    yield {
        "type": "user",
        "message": {
            "role": "user",
            "content": "Help me decide on the tech stack for a new mobile app",
        },
    }


# Required workaround: dummy hook keeps the stream open for can_use_tool
async def dummy_hook(input_data, tool_use_id, context):
    return {"continue_": True}


async def main():
    async for message in query(
        prompt=prompt_stream(),
        options=ClaudeAgentOptions(
            can_use_tool=can_use_tool,
            hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[dummy_hook])]},
        ),
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";
import * as readline from "readline/promises";

// Helper to prompt user for input in the terminal
async function prompt(question: string): Promise<string> {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const answer = await rl.question(question);
  rl.close();
  return answer;
}

// Parse user input as option number(s) or free text
function parseResponse(response: string, options: any[]): string {
  const indices = response.split(",").map((s) => parseInt(s.trim()) - 1);
  const labels = indices
    .filter((i) => !isNaN(i) && i >= 0 && i < options.length)
    .map((i) => options[i].label);
  return labels.length > 0 ? labels.join(", ") : response;
}

// Display Claude's questions and collect user answers
async function handleAskUserQuestion(input: any) {
  const answers: Record<string, string> = {};

  for (const q of input.questions) {
    console.log(`\n${q.header}: ${q.question}`);

    const options = q.options;
    options.forEach((opt: any, i: number) => {
      console.log(`  ${i + 1}. ${opt.label} - ${opt.description}`);
    });
    if (q.multiSelect) {
      console.log("  (Enter numbers separated by commas, or type your own answer)");
    } else {
      console.log("  (Enter a number, or type your own answer)");
    }

    const response = (await prompt("Your choice: ")).trim();
    answers[q.question] = parseResponse(response, options);
  }

  // Return the answers to Claude (must include original questions)
  return {
    behavior: "allow",
    updatedInput: { questions: input.questions, answers }
  };
}

async function main() {
  for await (const message of query({
    prompt: "Help me decide on the tech stack for a new mobile app",
    options: {
      canUseTool: async (toolName, input) => {
        // Route AskUserQuestion to our question handler
        if (toolName === "AskUserQuestion") {
          return handleAskUserQuestion(input);
        }
        // Auto-approve other tools for this example
        return { behavior: "allow", updatedInput: input };
      }
    }
  })) {
    if ("result" in message) console.log(message.result);
  }
}

main();
```

## Limitations

- **Subagents**: `AskUserQuestion` is not currently available in subagents spawned via the Agent tool.
- **Question limits**: each `AskUserQuestion` call supports 1-4 questions with 2-4 options each.

## Other ways to get user input

The `canUseTool` callback and `AskUserQuestion` tool cover most approval and clarification scenarios, but the SDK offers other input avenues:

- **Streaming input** — use [streaming input](cc_sdk_input_modes.md) when you need to interrupt the agent mid-task (send a cancel signal or change direction while Claude is working), provide additional context without waiting for Claude to ask, or build chat interfaces that let users send follow-up messages during long-running operations. Ideal for conversational UIs where users interact throughout execution, not just at approval checkpoints.
- **Custom tools** — use [custom tools](https://code.claude.com/docs/en/agent-sdk/custom-tools) when you need to collect structured input (forms, wizards, multi-step workflows beyond `AskUserQuestion`'s multiple-choice format), integrate external approval systems (ticketing, workflow, or approval platforms), or implement domain-specific interactions (code review interfaces, deployment checklists). Custom tools give full control but require more implementation work than the built-in `canUseTool` callback.

**Source**: https://code.claude.com/docs/en/agent-sdk/user-input
**Last Updated**: 2026-06-13
**Status**: Active
