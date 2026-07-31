---
tags:
  - resource
  - documentation
  - hermes_agent
  - prompt_assembly
  - agent_internals
keywords:
  - system prompt assembly
  - cached prompt tiers
  - stable context volatile
  - SOUL.md identity
  - context file priority
  - prompt injection security scan
  - api-call-time ephemeral layers
topics:
  - Hermes Agent
  - Prompt Assembly
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly
access_control_group: ["general"]
---

# Hermes Agent — Prompt Assembly

## Overview

Prompt assembly is the Hermes subsystem that builds the agent's system prompt while keeping it cache-stable. Its defining design choice is a deliberate separation between **cached system prompt state** and **ephemeral API-call-time additions** — a split that simultaneously governs token usage, provider-side prompt-caching effectiveness, session continuity, and memory correctness. The cached portion is assembled by `agent/prompt_builder.py` (and `agent/system_prompt.py`) into three ordered tiers — **stable → context → volatile** — and is held byte-stable so a provider can cache the prefix across turns; everything that must change per-call (ephemeral system prompts, prefill messages, gateway/Honcho recall, `pre_llm_call` plugin context) is appended *outside* the cached prefix so it never invalidates the cache. The primary files are `run_agent.py`, `agent/prompt_builder.py`, and `tools/memory_tool.py`. This note documents *how* that assembly behaves; the user-facing identity/memory/context-file editing surface lives in the user guide, and prompt caching itself is detailed in the compression-and-caching note.

## Cached system prompt layers

The cached system prompt is assembled as three ordered tiers (see `agent/system_prompt.py`) and joined `stable → context → volatile`:

1. **stable** — identity (`SOUL.md` or fallback), tool/model guidance, skills prompt, environment hints, platform hints
2. **context** — caller-supplied `system_message` plus project context files (`.hermes.md` / `AGENTS.md` / `CLAUDE.md` / `.cursorrules`)
3. **volatile** — built-in memory snapshot (`MEMORY.md`), user profile snapshot (`USER.md`), external memory-provider block, timestamp/session/model/provider line

This ordering matters for precedence discussions: skills live in the **stable** tier and memory/profile snapshots live in the **volatile** tier, but both are still part of the cached system prompt — they are not injected as ad-hoc mid-turn overlays. When `skip_context_files` is set (e.g., subagent delegation), `SOUL.md` is not loaded and the hardcoded `DEFAULT_AGENT_IDENTITY` is used instead.

A simplified view of the assembled prompt when all layers are present (comments show each section's source):

```
# Layer 1: Agent Identity (from ~/.hermes/SOUL.md)
You are Hermes, an AI assistant created by Nous Research.
...
# Layer 5: Frozen MEMORY snapshot
## Persistent Memory
- User prefers Python 3.12, uses pyproject.toml
...
# Layer 7: Skills index
## Skills (mandatory)
Before replying, scan the skills below. If one clearly matches
your task, load it with skill_view(name) and follow its instructions.
<available_skills>
  software-development:
    - code-review: Structured code review workflow
  research:
    - arxiv: Search and summarize arXiv papers
</available_skills>
# Layer 8: Context files (from project directory)
# Project Context
## AGENTS.md
This is the atlas project. Use pytest for testing.
# Layer 9: Timestamp + session
Current time: 2026-03-30T14:30:00-07:00
Session: abc123
# Layer 10: Platform hint
You are a CLI AI Agent. Try not to use markdown but simple text
renderable inside a terminal.
```

## Customizing platform hints

The platform hint (Layer 10) is the per-surface guidance Hermes injects for Telegram, WhatsApp, Slack, CLI, and other platforms (e.g. "you are on a terminal, avoid Markdown"). Built-in defaults live in `PLATFORM_HINTS` (`agent/system_prompt.py`); plugin-provided platforms supply theirs through the platform registry. An administrator can append to or replace a *single* platform's hint from `config.yaml` via the top-level `platform_hints` key without touching any other platform:

```yaml
platform_hints:
  whatsapp:
    append: >
      When tabular output would be useful, invoke the table_formatting
      skill instead of emitting a Markdown table.
  slack:
    replace: "You are on Slack. Keep responses tight and avoid wide tables."
  telegram: "Prefer short messages; split long answers."   # shorthand = append
```

`append` keeps the built-in hint and adds text after it; `replace` substitutes it entirely; a bare string is shorthand for `append`; `replace` wins over `append` when both are present. A malformed entry is ignored defensively and falls back to the unmodified default, so a bad config value can never break prompt assembly or leak across platforms. The override is resolved when the system prompt is built (session start, and again on compaction since that rebuilds the prompt), producing a byte-stable hint for a fixed config — so it lives in the **stable** tier alongside the built-in hint and does not break prompt caching.

## How SOUL.md appears in the prompt

`SOUL.md` lives at `~/.hermes/SOUL.md` and serves as the agent's identity — the very first section of the system prompt. The loading logic in `prompt_builder.py` works as follows:

```python
# From agent/prompt_builder.py (simplified)
def load_soul_md() -> Optional[str]:
    soul_path = get_hermes_home() / "SOUL.md"
    if not soul_path.exists():
        return None
    content = soul_path.read_text(encoding="utf-8").strip()
    content = _scan_context_content(content, "SOUL.md")  # Security scan
    content = _truncate_content(content, "SOUL.md")       # Cap defaults to 20k chars, configurable
    return content
```

When `load_soul_md()` returns content, it replaces the hardcoded `DEFAULT_AGENT_IDENTITY`. `build_context_files_prompt()` is then called with `skip_soul=True` to prevent SOUL.md from appearing twice (once as identity, once as a context file). If `SOUL.md` does not exist, the system falls back to a built-in identity block ("You are Hermes Agent, an intelligent AI assistant created by Nous Research...").

## How context files are injected

`build_context_files_prompt()` uses a **priority system** — only one project context type is loaded (first match wins):

```python
# From agent/prompt_builder.py (simplified)
def build_context_files_prompt(cwd=None, skip_soul=False):
    cwd_path = Path(cwd).resolve()
    # Priority: first match wins — only ONE project context loaded
    project_context = (
        _load_hermes_md(cwd_path)       # 1. .hermes.md / HERMES.md (walks to git root)
        or _load_agents_md(cwd_path)    # 2. AGENTS.md (cwd only)
        or _load_claude_md(cwd_path)    # 3. CLAUDE.md (cwd only)
        or _load_cursorrules(cwd_path)  # 4. .cursorrules / .cursor/rules/*.mdc
    )
    sections = []
    if project_context:
        sections.append(project_context)
    # SOUL.md from HERMES_HOME (independent of project context)
    if not skip_soul:
        soul_content = load_soul_md()
        if soul_content:
            sections.append(soul_content)
    if not sections:
        return ""
    return (
        "# Project Context\n\n"
        "The following project context files have been loaded "
        "and should be followed:\n\n"
        + "\n".join(sections)
    )
```

### Context file discovery details

| Priority | Files | Search scope | Notes |
|----------|-------|-------------|-------|
| 1 | `.hermes.md`, `HERMES.md` | CWD up to git root | Hermes-native project config |
| 2 | `AGENTS.md` | CWD only | Common agent instruction file |
| 3 | `CLAUDE.md` | CWD only | Claude Code compatibility |
| 4 | `.cursorrules`, `.cursor/rules/*.mdc` | CWD only | Cursor compatibility |

All context files are **security scanned** (checked for prompt-injection patterns — invisible unicode, "ignore previous instructions", credential-exfiltration attempts), **truncated** at `context_file_max_chars` characters (default 20,000) using a 70/20 head/tail ratio with a truncation marker, and have **YAML frontmatter stripped** (`.hermes.md` frontmatter is reserved for future config overrides). `SOUL.md` is loaded separately via `load_soul_md()` for the identity slot, and `AGENTS.md` subdirectories are discovered progressively during the session via `agent/subdirectory_hints.py`.

## API-call-time-only layers

These are intentionally *not* persisted as part of the cached system prompt: `ephemeral_system_prompt`, prefill messages, gateway-derived session-context overlays, and later-turn Honcho/external recall injected into the current-turn user message. `pre_llm_call` plugin context also lands in this API-call-time path: it is appended to the current turn's **user message**, not written into the cached system prompt; when multiple plugins return context, Hermes concatenates those blocks. This separation keeps the stable prefix stable for caching.

## Memory snapshots

Local memory and user-profile data are captured in the system prompt's **volatile tier**. Mid-session writes update disk state but do not mutate the already-built cached system prompt until a rebuild path runs (new session, or explicit invalidation/rebuild flow such as a compression-triggered rebuild).

## Supported prompt customization surfaces

Most users should treat `agent/prompt_builder.py` as implementation code, not a configuration surface — the supported customization path is to change the prompt *inputs* Hermes already loads rather than editing Python templates in place. Use these surfaces first:

- `~/.hermes/SOUL.md` — replace the built-in default identity block with your own agent persona and standing behavior.
- `~/.hermes/MEMORY.md` and `~/.hermes/USER.md` — durable cross-session facts and user-profile data snapshotted into new sessions.
- Project context files (`.hermes.md`, `HERMES.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`) — inject repo-specific working rules.
- Skills — package reusable workflows without editing core prompt code.
- Optional system-prompt config / API overrides — deployment-specific instruction text without forking Hermes.
- Ephemeral overlays (`HERMES_EPHEMERAL_SYSTEM_PROMPT`, prefill messages) — turn-scoped guidance that should not become part of the cached prefix.

Edit `agent/prompt_builder.py` only when intentionally maintaining a fork or contributing upstream — that file assembles the prompt plumbing, cache boundaries, and injection order for every session, so direct edits are global product changes, not per-user customization.

## Why prompt assembly is split this way

The architecture is intentionally optimized to preserve provider-side prompt caching, avoid mutating history unnecessarily, keep memory semantics understandable, and let gateway/ACP/CLI add context without poisoning persistent prompt state.

**Source**: `inbox/hermes_agent_docs/developer-guide/prompt-assembly.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly
**Last Updated**: 2026-06-19
**Status**: Active
