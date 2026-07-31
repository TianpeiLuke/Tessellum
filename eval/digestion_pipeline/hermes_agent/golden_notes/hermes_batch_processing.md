---
tags:
  - resource
  - documentation
  - hermes_agent
  - batch_processing
  - automation
keywords:
  - batch processing
  - batch_runner.py
  - ShareGPT trajectory
  - toolset distributions
  - content-based resume
  - training data generation
topics:
  - Hermes Agent
  - Batch Processing
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/batch-processing
access_control_group: ["general"]
---

# Hermes Agent — Batch Processing

## Overview

Batch processing is the offline **trajectory-generation data model** of Hermes Agent: a way to run the agent across hundreds or thousands of prompts in parallel and capture each run as structured, ShareGPT-format trajectory data. It is driven by `batch_runner.py`, which reads a JSONL dataset of prompts, runs every prompt through a full isolated agent session with tool access, and writes back a conversation trace plus tool-call statistics and reasoning-coverage metrics for each one. The primary purpose is **training data generation** — producing trajectories that can be used to fine-tune or evaluate tool-using models. The shape of this note is a data model, not a procedure: it describes the dataset format, the parallelism + distribution-sampling mechanism, the trajectory JSON schema, the content-based checkpoint/resume flow, the quality filters, and the aggregate statistics that come out the other end. Per-prompt sandbox container backends (Docker/Modal/Singularity), model/provider selection, and the Nous Portal subscription that bundles cost-at-scale are configured elsewhere and linked rather than re-documented here.

## Quick Start

`batch_runner.py` is invoked directly with flags. A basic run names the output directory, picks a model, and sets worker parallelism; `--resume` continues an interrupted run; `--list_distributions` enumerates the toolset distributions:

```bash
# Basic batch run
python batch_runner.py \
    --dataset_file=data/prompts.jsonl \
    --batch_size=10 \
    --run_name=my_first_run \
    --model=anthropic/claude-sonnet-4.6 \
    --num_workers=4

# Resume an interrupted run
python batch_runner.py \
    --dataset_file=data/prompts.jsonl \
    --batch_size=10 \
    --run_name=my_first_run \
    --resume

# List available toolset distributions
python batch_runner.py --list_distributions
```

For predictable cost at scale, the source recommends a Nous Portal subscription (set up via `hermes setup --portal`, then point `--model` at a Nous model), which bundles model access plus web search, image gen, TTS, and cloud browsers under one bill rather than juggling rate limits across multiple vendor accounts.

## Dataset Format

The input dataset is a JSONL file (one JSON object per line). Each entry must have a `prompt` field; entries can optionally include a per-prompt container `image`/`docker_image` (works with Docker, Modal, and Singularity backends) and a `cwd` working-directory override for the task's terminal session:

```jsonl
{"prompt": "Write a Python function that finds the longest palindromic substring"}
{"prompt": "Create a REST API endpoint for user authentication using Flask"}
{"prompt": "Debug this error: TypeError: cannot unpack non-iterable NoneType object"}
```

## Configuration Options

The runner exposes a flag surface for I/O, parallelism, and model selection. Required flags are `--dataset_file`, `--batch_size`, and `--run_name` (the run name keys the output dir and checkpoint). Key defaults: `--distribution="default"`, `--model=claude-sonnet-4.6`, `--base_url=https://openrouter.ai/api/v1`, `--max_turns=10` (max tool-calling iterations per prompt), `--num_workers=4` (parallel worker processes), `--resume=false`. `--api_key` falls back to an env var; `--max_samples` caps how many dataset rows are processed; `--max_tokens` overrides the model default.

- **Provider Routing (OpenRouter):** `--providers_allowed`, `--providers_ignored`, `--providers_order` (comma-separated provider lists), and `--provider_sort` (`"price"` / `"throughput"` / `"latency"`) steer which OpenRouter providers serve the run.
- **Reasoning Control:** `--reasoning_effort` (`none`, `minimal`, `low`, `medium`, `high`, `xhigh`) and `--reasoning_disabled` (completely disable reasoning/thinking tokens).
- **Advanced:** `--ephemeral_system_prompt` (used during execution but NOT saved to trajectories), `--log_prefix_chars` (log-preview length, default 100), and `--prefill_messages_file` (JSON file of prefill messages for few-shot priming).

## Toolset Distributions

Each prompt gets a randomly sampled set of toolsets from a **distribution**, ensuring the training data covers diverse tool combinations (`--list_distributions` shows all available distributions). In the current implementation a distribution assigns a probability to **each individual toolset**: the sampler flips each toolset independently, then guarantees at least one toolset is enabled. This independent-per-toolset sampling is explicitly different from a hand-authored table of prebuilt toolset combinations.

## Output Format

All output goes to `data/<run_name>/`: a combined `trajectories.jsonl` (all batches merged), individual `batch_N.jsonl` files, a `checkpoint.json` resume file, and a `statistics.json` aggregate. Each line in `trajectories.jsonl` is a JSON object capturing the run, its conversation, and per-tool stats:

```json
{
  "prompt_index": 42,
  "conversations": [
    {"from": "human", "value": "Write a function..."},
    {"from": "gpt", "value": "I'll create that function...",
     "tool_calls": [...]},
    {"from": "tool", "value": "..."},
    {"from": "gpt", "value": "Here's the completed function..."}
  ],
  "metadata": {
    "batch_num": 2,
    "timestamp": "2026-01-15T10:30:00",
    "model": "anthropic/claude-sonnet-4.6"
  },
  "completed": true,
  "partial": false,
  "api_calls": 3,
  "toolsets_used": ["terminal", "file"],
  "tool_stats": {
    "terminal": {"count": 2, "success": 2, "failure": 0},
    "read_file": {"count": 1, "success": 1, "failure": 0}
  },
  "tool_error_counts": {
    "terminal": 0,
    "read_file": 0
  }
}
```

The `conversations` field uses a ShareGPT-like format with `from` and `value` fields. Tool stats are normalized to include all possible tools with zero defaults, ensuring a consistent schema across entries for HuggingFace datasets compatibility.

## Checkpointing

The batch runner has robust checkpointing for fault tolerance. The checkpoint file is saved after each batch completes, tracking which prompt indices are done. **Content-based resume** is the distinctive property: on `--resume` the runner scans existing batch files and matches completed prompts by their actual text content (not just indices), enabling recovery even if the dataset order changes. Only successfully completed prompts are marked done — failed prompts are retried on resume. On completion, all batch files (including from previous runs) are merged into a single `trajectories.jsonl`.

The resume flow is a scan→filter→re-batch→process→merge collect-then-process data flow:

1. Scan all `batch_*.jsonl` files for completed prompts (by content matching)
2. Filter the dataset to exclude already-completed prompts
3. Re-batch the remaining prompts
4. Process only the remaining prompts
5. Merge all batch files (old + new) into final output

## Quality Filtering

The runner applies automatic quality filtering. The **no-reasoning filter** discards samples where zero assistant turns contain reasoning (no `<REASONING_SCRATCHPAD>` or native thinking tokens). The **corrupted-entry filter** removes entries with hallucinated tool names (not in the valid tool list) during the final merge. **Reasoning statistics** track the percentage of turns with/without reasoning across the entire run.

## Statistics

After completion the runner prints comprehensive statistics — tool usage (call counts, success/failure rates per tool), reasoning coverage (percentage of assistant turns with reasoning), samples discarded (count filtered for lacking reasoning), and total duration. Statistics are also saved to `statistics.json` for programmatic analysis.

## Use Cases

- **Training data generation:** generate diverse tool-use trajectories for fine-tuning (`--distribution=default`, higher `--max_turns`, more `--num_workers`).
- **Model evaluation:** run a fixed eval suite across standardized prompts (`--run_name=eval_*`, a target `--model`) to measure how well a model uses tools.
- **Per-prompt container images:** for benchmarks requiring specific environments, each prompt can specify its own `image` (and optional `cwd`); the batch runner verifies Docker images are accessible before running each prompt.

**Source**: `inbox/hermes_agent_docs/user-guide/features/batch-processing.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/batch-processing
**Last Updated**: 2026-06-19
**Status**: Active
