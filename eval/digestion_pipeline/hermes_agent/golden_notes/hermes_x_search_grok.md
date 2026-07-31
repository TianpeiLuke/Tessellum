---
tags:
  - resource
  - documentation
  - hermes_agent
  - web_tools
  - features
keywords:
  - x_search tool
  - xAI Grok
  - SuperGrok OAuth
  - XAI_API_KEY
  - Responses API
  - degraded result flag
  - X Twitter search
topics:
  - Hermes Agent
  - Web & Tool Surface
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/x-search
access_control_group: ["general"]
---

# Hermes Agent — X (Twitter) Search

## Overview

`x_search` is a Hermes Agent tool that lets the agent search X (Twitter) posts, profiles, and threads directly. It is **not** a Hermes-side scraper: it is backed by xAI's built-in `x_search` tool on the Responses API at `https://api.x.ai/v1/responses`, so Grok itself runs the search server-side and returns a synthesized answer with citations back to the originating posts. Operationally it is a procedure built on three moving parts: a **dual-credential resolver** (SuperGrok / X Premium+ OAuth, or a paid `XAI_API_KEY`) that auto-registers the tool, a small `x_search:` configuration block (model, timeout, retries), and a parameter set that scopes the query by handle and date, returning structured JSON that includes a `degraded` flag for unsourced answers. The documented guidance: reach for `x_search` when you specifically want current discussion, reactions, or claims **on X**; for general web pages keep using `web_search` / `web_extract`.

## Authentication

`x_search` registers when **either** xAI credential path is available:

| Credential | Source | Setup |
|------------|--------|-------|
| **SuperGrok / X Premium+ OAuth** (preferred) | Browser login at `accounts.x.ai`, refreshed automatically | `hermes auth add xai-oauth` (see the xAI Grok OAuth guide) |
| **`XAI_API_KEY`** | Paid xAI API key | Set in `~/.hermes/.env` |

Both credential paths hit the same endpoint with the same payload — the only difference is the bearer token. **When both are configured, SuperGrok OAuth wins**, so `x_search` runs against your subscription quota instead of paid API spend.

The tool's `check_fn` runs the xAI credential resolver every time the model's tool list is rebuilt. A `True` return means the bearer is fetchable AND non-empty AND (if it had expired) was successfully refreshed. Revoked tokens with a failed refresh hide the tool from the schema — the model simply can't see it.

## Enabling the tool

The tool auto-enables when xAI credentials (an OAuth token or `XAI_API_KEY`) are present. Disable it explicitly via `hermes tools` → Search → x_search if you don't want it:

```bash
hermes tools
# → 🐦 X (Twitter) Search   (press space to toggle on)
```

The picker offers two credential choices: **xAI Grok OAuth (SuperGrok / Premium+)**, which opens the browser to `accounts.x.ai` if you're not already logged in, and **xAI API key**, which prompts for `XAI_API_KEY`. Either choice satisfies the gating; the tool works identically with both, and if both end up configured, OAuth is preferred at call time.

## Configuration

The `x_search:` block in `~/.hermes/config.yaml` tunes the model, timeout, and retry behavior:

```yaml
# ~/.hermes/config.yaml
x_search:
  # xAI model used for the Responses call.
  # grok-4.20-reasoning is the recommended default; any Grok model
  # with x_search tool access works.
  model: grok-4.20-reasoning

  # Request timeout in seconds. x_search can take 60–120s for
  # complex queries — the default is generous. Minimum: 30.
  timeout_seconds: 180

  # Number of automatic retries on 5xx / ReadTimeout / ConnectionError.
  # Each retry backs off (1.5x attempt seconds, capped at 5s).
  retries: 2
```

The `model` must be a Grok model that has access to the server-side `x_search` tool. Because complex X queries can take 60–120 s, `timeout_seconds` defaults to a generous 180 (minimum 30), and `retries` (default 2) covers transient 5xx / `ReadTimeout` / `ConnectionError` failures with exponential backoff (1.5× attempt seconds, capped at 5 s).

## Tool parameters

The agent calls `x_search` with these arguments:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string (required) | What to look up on X. |
| `allowed_x_handles` | string array | Optional handles to include **exclusively** (max 10). Leading `@` is stripped. |
| `excluded_x_handles` | string array | Optional handles to exclude (max 10). Mutually exclusive with `allowed_x_handles`. |
| `from_date` | string | Optional `YYYY-MM-DD` start date. |
| `to_date` | string | Optional `YYYY-MM-DD` end date. |
| `enable_image_understanding` | boolean | Ask xAI to analyze images attached to matching posts. |
| `enable_video_understanding` | boolean | Ask xAI to analyze videos attached to matching posts. |

The tool returns JSON containing:

- `answer` — synthesized text response from Grok.
- `citations` — citations returned by the Responses API top-level field.
- `inline_citations` — `url_citation` annotations extracted from the message body (each with `url`, `title`, `start_index`, `end_index`).
- `degraded` — `true` when any narrowing filter (`allowed_x_handles`, `excluded_x_handles`, `from_date`, `to_date`) was set AND both citation channels came back empty. In that case the `answer` was synthesized from the model's own knowledge rather than the X index, so treat it as **unsourced**. `false` otherwise (including the "no filters set" case — a broad unsourced answer is just an answer, not a filter miss).
- `degraded_reason` — short string naming which filters were active, or `null` when `degraded` is `false`.
- `credential_source` — `"xai-oauth"` if OAuth resolved, `"xai"` if the API key resolved.
- `model`, `query`, `provider`, `tool`, `success`.

### Date validation

`from_date` / `to_date` are validated client-side **before** the HTTP call:

- Both, if provided, must parse as `YYYY-MM-DD`.
- When both are set, `from_date` must be on or before `to_date`.
- `from_date` must not be later than today UTC — no posts can exist in a window that hasn't started yet, so the call would be guaranteed to return zero citations.
- `to_date` in the future is allowed (callers may legitimately request "from yesterday to tomorrow" to catch posts as they arrive).

Validation failures surface as a structured `{"error": "..."}` tool result, never as an HTTP call to xAI.

## Example

Talking to the agent:

> What are people on X saying about the new Grok image features? Focus on responses from @xai.

The agent will (1) call `x_search` with `query="reactions to new Grok image features"` and `allowed_x_handles=["xai"]`, (2) get back a synthesized answer plus a list of citations linking to specific posts, and (3) reply with the answer and references.

## Troubleshooting

- **"No xAI credentials available"** — surfaced when both auth paths fail. Set `XAI_API_KEY` in `~/.hermes/.env` or run `hermes auth add xai-oauth` and complete the browser login, then restart the session so the agent re-reads the tool registry.
- **"`x_search` is not enabled for this model"** — the configured `x_search.model` lacks access to the server-side `x_search` tool. Switch to `grok-4.20-reasoning` (the default) or another Grok model that supports it; check the [xAI documentation](https://docs.x.ai/) for the current list.
- **Tool doesn't appear in the schema** — two causes: the toolset isn't enabled (run `hermes tools` and confirm `🐦 X (Twitter) Search` is checked), or no xAI credentials are present so `check_fn` returns False and the schema stays hidden (run `hermes auth status` to confirm xai-oauth login state, and check that `XAI_API_KEY` is set).
- **`degraded: true` — answer with no citations** — when `allowed_x_handles`, `excluded_x_handles`, or a date range was used and the response comes back `degraded: true`, xAI's X index returned no matching posts but Grok still produced an answer from its own training data; the answer is **unsourced**. Worth checking: a typo in the handle (strip the `@`, verify spelling and that the account exists), too-narrow or future-sliding date range (widen and retry), or an xAI index gap (retry after a few minutes, or use the `xurl` skill for direct X API reads when you need an exact handle's timeline).

**Source**: `inbox/hermes_agent_docs/user-guide/features/x-search.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/x-search
**Last Updated**: 2026-06-19
**Status**: Active
