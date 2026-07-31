---
tags:
  - resource
  - terminology
  - agentic_ai
  - training_data
  - agent_systems
keywords:
  - agent trajectory
  - trajectory record
  - ShareGPT trajectory
  - trajectory dataset
  - agent rollout record
  - conversation trajectory
  - trajectory_samples.jsonl
topics:
  - agentic_ai
  - training_data
  - agent_telemetry
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Agent Trajectory - Recorded Agent-Session Artifact

## Definition

An **agent trajectory** is the concrete, serialized record of one complete agent session — the temporally ordered transcript of every system prompt, user message, model reasoning step, tool call, tool result, and final response that an LLM agent produced from session start to termination, persisted as a self-contained, replayable training/evaluation artifact. Where the abstract [trajectory](term_trajectory.md) concept names the *mathematical object* (the state-action(-reward) sequence $\tau = (s_0, a_0, r_1, s_1, \ldots, s_T)$ that a [policy](term_policy.md) traces through an environment), the *agent trajectory* names the *engineered data structure* that operationalizes it for modern LLM agents: a row-per-turn JSONL file in a chat schema (typically ShareGPT/conversational), enriched with a session header (model, timestamp, completion flag) and run-level metadata (API-call count, per-tool success/failure stats, toolsets used).

In the Hermes Agent (Nous Research) framework the trajectory is the literal training-data unit of a *data flywheel*: each agent run is captured by a `recorder` → normalized against a `schema` → redacted and written by an `exporter` into `trajectory_samples.jsonl` (successful runs) or `failed_trajectories.jsonl`, then compressed for storage and consumed downstream for [supervised fine-tuning](term_fine_tuning.md), [knowledge distillation](term_knowledge_distillation.md), [imitation learning](term_imitation_learning.md), offline RL, and evaluation. The defining property is that the agent trajectory is the *recorded substrate* — high-fidelity but high-volume — that training and memory pipelines read, as opposed to the abstract sequence they reason about.

## Context

The Hermes "Trajectory Format" developer guide frames trajectory capture as the *clearest dual-use signal* in Hermes: a usable personal agent for end users AND a data-collection harness for the model org. The recorder/schema/exporter/redactor pipeline plus the 65 KB `trajectory_compressor.py` implement this surface; the [self-evolving agent](term_self_evolving_agent.md) and analytics loops read aggregated trajectories to drive skill self-improvement.

The serialization follows the **ShareGPT** convention: the `conversations` array maps API roles to a `from` field (`system`, `human`, `gpt`, `tool`), every assistant (`gpt`) turn is guaranteed a `<think>` reasoning block (normalized from native thinking tokens or a `REASONING_SCRATCHPAD`, with an empty block inserted when no reasoning was produced), tool calls become XML-wrapped `<tool_call>` JSON, and tool results become grouped `<tool_response>` turns — a schema chosen for direct HuggingFace dataset loading. The same construct underlies offline-RL action-orchestration work, where one logged interaction journey (a sequence of $(o_t, a_t, o_{t+1}, r_t, d_t)$ transition tuples) is the trajectory record from which a [POMDP](term_pomdp.md) policy is learned; and it is the raw material that [workflow memory](term_workflow_memory.md) and [episodic memory](term_episodic_memory.md) compress rather than replay verbatim.

## Key Characteristics

- **Concrete artifact, not abstract object**: an agent trajectory is a file (JSONL line), not a probability-theoretic sequence — it is what `term_trajectory` looks like once serialized for storage, training, and replay.
- **Row-per-turn + session header**: each line is one self-contained session; richer variants (e.g., a batch runner) add `prompt_index`, `metadata`, `api_calls`, `toolsets_used`, and normalized `tool_stats`/`tool_error_counts` with zero-defaults for consistent dataset schema.
- **ShareGPT role mapping**: API roles `system / user / assistant / tool` are rewritten to ShareGPT `from` values `system / human / gpt / tool`.
- **Reasoning normalization**: every `gpt` turn carries a `<think>...</think>` block; native thinking tokens and XML scratchpads are folded into one canonical form, and empty blocks are inserted to keep the format uniform for training.
- **Completion-gated routing**: successful runs (`completed = true`) and failed/interrupted runs (`completed = false`) are written to separate files, so curators can filter to clean training data.
- **Redaction before export**: a redactor scrubs PII and secrets ([PII](term_pii.md)) before any trajectory is shipped upstream — a prerequisite for using user-generated runs as training data.
- **High-volume, compression-driven**: long-horizon agents produce gigabytes of trajectories with redundant tool calls; a compressor protects the head (setup) and tail (recent) turns and summarizes a compressible middle region to a single human-role summary to hit a target token budget.
- **Reusable across the flywheel**: the same trajectory corpus feeds SFT, distillation, imitation/offline RL, off-policy evaluation, analytics, and experience-based memory.

## Related Terms


## References

- [Hermes Agent Docs — Trajectory Format (ShareGPT JSONL trajectory schema)](https://hermes-agent.nousresearch.com/docs/developer-guide/trajectory-format/)
- [Nous Research — Hermes Agent (GitHub)](https://github.com/nousresearch/hermes-agent)
- [Hugging Face TRL — SFT Trainer (conversational / ShareGPT dataset format, tool-calling fine-tuning)](https://huggingface.co/docs/trl/en/sft_trainer)
- [ShareGPT conversational dataset format (role conventions used for agent trajectories)](https://huggingface.co/docs/trl/en/dataset_formats)
- [Wikipedia — Reinforcement learning (trajectories as the unit of agent experience)](https://en.wikipedia.org/wiki/Reinforcement_learning)
