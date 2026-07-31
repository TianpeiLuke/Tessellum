---
tags:
  - resource
  - documentation
  - hermes_agent
  - trajectory
  - training_data
keywords:
  - sharegpt trajectory format
  - trajectory jsonl
  - tool_stats normalization
  - think reasoning markup
  - tool_call tool_response xml
  - huggingface dataset loading
  - save_trajectories
topics:
  - Hermes Agent
  - Trajectory Format
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/trajectory-format
access_control_group: ["general"]
---

# Hermes Agent — Trajectory Format

## Overview

The trajectory format is the **ShareGPT-compatible JSONL data model** Hermes Agent uses to persist completed conversations as training data, debugging artifacts, and reinforcement-learning datasets. Each conversation turn is serialized into one self-contained JSON object per line, with the actual dialogue stored in a `conversations` array that maps the agent's API roles (`system`/`user`/`assistant`/`tool`) onto ShareGPT's `from` roles (`system`/`human`/`gpt`/`tool`). The implementation lives in `agent/trajectory.py`, `run_agent.py` (the `_save_trajectory` path), and `batch_runner.py`.

This note documents the two on-disk JSONL variants (the CLI/interactive entry and the batch-runner entry with `tool_stats`/`tool_error_counts`), the ShareGPT role mapping and a complete example, the four normalization rules that the save-time converter applies (`<think>` reasoning markup, XML-wrapped `<tool_call>`/`<tool_response>`, and the regenerated system message), how trajectories are loaded as plain JSONL or as HuggingFace datasets, and the `agent.save_trajectories` controls that govern when files are written. It describes *how the format behaves*; for *how it is implemented*, it links down to the `repo_hermes_agent_trajectory_research` repo note and the `trajectory_*` / `batch_runner*` snippet corpus.

## File Naming Convention

Trajectories are written to files in the current working directory:

| File | When |
|------|------|
| `trajectory_samples.jsonl` | Conversations that completed successfully (`completed=True`) |
| `failed_trajectories.jsonl` | Conversations that failed or were interrupted (`completed=False`) |

The batch runner (`batch_runner.py`) writes to a custom output file per batch (e.g., `batch_001_output.jsonl`) with additional metadata fields. The filename can be overridden via the `filename` parameter in `save_trajectory()`.

## JSONL Entry Format

Each line in the file is a self-contained JSON object. There are two variants. The **CLI/interactive format** (from `_save_trajectory`) carries the conversation, a timestamp, the model identifier, and the completion flag:

```json
{
  "conversations": [ ... ],
  "timestamp": "2026-03-30T14:22:31.456789",
  "model": "anthropic/claude-sonnet-4.6",
  "completed": true
}
```

The **batch-runner format** (from `batch_runner.py`) adds RL-pipeline metadata — the prompt index and source, partial/api-call accounting, and the per-tool statistics that make the dataset HuggingFace-loadable:

```json
{
  "prompt_index": 42,
  "conversations": [ ... ],
  "metadata": { "prompt_source": "gsm8k", "difficulty": "hard" },
  "completed": true,
  "partial": false,
  "api_calls": 7,
  "toolsets_used": ["code_tools", "file_tools"],
  "tool_stats": {
    "terminal": {"count": 3, "success": 3, "failure": 0},
    "read_file": {"count": 2, "success": 2, "failure": 0},
    "write_file": {"count": 0, "success": 0, "failure": 0}
  },
  "tool_error_counts": {
    "terminal": 0,
    "read_file": 0,
    "write_file": 0
  }
}
```

The `tool_stats` and `tool_error_counts` dictionaries are normalized to include **ALL possible tools** (from `model_tools.TOOL_TO_TOOLSET_MAP`) with zero defaults, ensuring a consistent schema across entries for HuggingFace dataset loading.

## Conversations Array (ShareGPT Format)

The `conversations` array uses ShareGPT role conventions, mapping each API role onto a ShareGPT `from` value:

| API Role | ShareGPT `from` |
|----------|-----------------|
| system | `"system"` |
| user | `"human"` |
| assistant | `"gpt"` |
| tool | `"tool"` |

A complete entry threads a system prompt, a human question, an assistant turn that reasons in `<think>` and emits a `<tool_call>`, a `tool` turn carrying the `<tool_response>`, and a final assistant answer:

```json
{
  "conversations": [
    {
      "from": "system",
      "value": "You are a function calling AI model. You are provided with function signatures within <tools> </tools> XML tags. You may call one or more functions to assist with the user query. ... Here are the available tools:\n<tools>\n[{\"name\": \"terminal\", \"description\": \"Execute shell commands\", \"parameters\": {\"type\": \"object\", \"properties\": {\"command\": {\"type\": \"string\"}}}, \"required\": null}]\n</tools>\n..."
    },
    {
      "from": "human",
      "value": "What Python version is installed?"
    },
    {
      "from": "gpt",
      "value": "<think>\nThe user wants to know the Python version. I should run python3 --version.\n</think>\n<tool_call>\n{\"name\": \"terminal\", \"arguments\": {\"command\": \"python3 --version\"}}\n</tool_call>"
    },
    {
      "from": "tool",
      "value": "<tool_response>\n{\"tool_call_id\": \"call_abc123\", \"name\": \"terminal\", \"content\": \"Python 3.11.6\"}\n</tool_response>"
    },
    {
      "from": "gpt",
      "value": "<think>\nGot the version. I can now answer the user.\n</think>\nPython 3.11.6 is installed on this system."
    }
  ],
  "timestamp": "2026-03-30T14:22:31.456789",
  "model": "anthropic/claude-sonnet-4.6",
  "completed": true
}
```

## Normalization Rules

The save-time converter applies four normalization rules so every entry has a uniform shape regardless of how the underlying model produced it.

**Reasoning content markup.** ALL reasoning is normalized into `<think>` tags. (1) **Native thinking tokens** (the `msg["reasoning"]` field from providers like Anthropic and OpenAI o-series) are wrapped as `<think>\n{reasoning}\n</think>\n` and prepended before the content. (2) **REASONING_SCRATCHPAD XML** — emitted when native thinking is disabled and the model reasons via system-prompt-instructed XML — has its `<REASONING_SCRATCHPAD>` tags converted to `<think>` via `convert_scratchpad_to_think()`. (3) **Empty think blocks**: every `gpt` turn is guaranteed a `<think>` block; if no reasoning was produced, an empty block `<think>\n</think>\n` is inserted so the training-data format stays consistent.

**Tool call normalization.** Tool calls from the API format (with `tool_call_id`, function name, and arguments as a JSON string) are converted to XML-wrapped JSON — a `<tool_call>` block wrapping `{"name": "terminal", "arguments": {...}}`, as shown in the complete example above. Arguments are parsed from JSON strings back to objects (not double-encoded); if JSON parsing fails (which should not happen, since arguments are validated during the conversation) an empty `{}` is used with a warning logged; and multiple tool calls in one assistant turn produce multiple `<tool_call>` blocks within a single `gpt` message.

**Tool response normalization.** All tool results following an assistant message are grouped into a single `tool` turn with XML-wrapped JSON responses — each a `<tool_response>` block wrapping `{"tool_call_id": ..., "name": ..., "content": ...}` (see the `tool` turn in the complete example above). If a tool's content looks like JSON (starts with `{` or `[`) it is parsed so the `content` field holds a JSON object/array rather than a string; multiple tool results are joined with newlines in one message; and the tool name is matched by position against the parent assistant's `tool_calls` array.

**System message.** The system message is generated at save time (not taken from the conversation). It follows the Hermes function-calling prompt template — a preamble explaining the function-calling protocol, a `<tools>` XML block of JSON tool definitions, the `FunctionCall` schema reference, and a `<tool_call>` example. Tool definitions include `name`, `description`, `parameters`, and `required` (set to `null` to match the canonical format).

## Loading Trajectories

Trajectories are standard JSONL — load them with any JSON-lines reader, then filter by completion and extract the `conversations` for training:

```python
import json

def load_trajectories(path: str):
    """Load trajectory entries from a JSONL file."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries

# Filter to successful completions only
successful = [e for e in load_trajectories("trajectory_samples.jsonl")
              if e.get("completed")]

# Extract just the conversations for training
training_data = [e["conversations"] for e in successful]
```

For HuggingFace, the files load directly via the `json` builder. The normalized `tool_stats` schema is what guarantees every entry shares the same columns, preventing Arrow schema-mismatch errors during dataset loading:

```python
from datasets import load_dataset

ds = load_dataset("json", data_files="trajectory_samples.jsonl")
```

## Controlling Trajectory Saving

In the CLI, trajectory saving is off by default and enabled through config or flag:

```yaml
# config.yaml
agent:
  save_trajectories: true  # default: false
```

It can also be set via the `--save-trajectories` flag. When the agent initializes with `save_trajectories=True`, the `_save_trajectory()` method is called at the end of each conversation turn. The batch runner always saves trajectories (that is its primary purpose), and samples with **zero reasoning across all turns** are automatically discarded by the batch runner to avoid polluting training data with non-reasoning examples.

**Source**: `inbox/hermes_agent_docs/developer-guide/trajectory-format.md`
**Last Updated**: 2026-06-19
**Status**: Active
