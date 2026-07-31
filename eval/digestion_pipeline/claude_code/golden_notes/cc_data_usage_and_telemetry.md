---
tags:
  - resource
  - documentation
  - claude_code
  - data_usage
  - telemetry
keywords:
  - data usage policy
  - data training policy
  - development partner program
  - data retention
  - telemetry services
  - webfetch domain safety check
  - encryption at rest
  - feedback command
  - session quality survey
topics:
  - Claude Code
  - Data Usage
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/data-usage
access_control_group: ["general"]
---

# Claude Code — Data Usage and Telemetry

## Overview

This note documents Anthropic's data usage policies for Claude Code: who can train on your data, how long data is retained by account type, how Claude Code's data flows to external services during install and runtime, and which telemetry/feedback connections run by default per API provider. The governing principle is a split between **consumer** accounts (Free, Pro, Max — opt-in training, longer retention) and **commercial** accounts (Team, Enterprise, API, third-party platforms, Claude Gov — no training by default, shorter retention).

All prompts and model outputs are encrypted in transit via TLS 1.2+; encryption at rest depends on the model provider. Non-essential connections (telemetry, error reporting, `/feedback`) are individually opt-out via environment variables, and most are off by default on non-Anthropic providers. Detailed environment-variable semantics are owned by the env-vars reference (B03A); provider-specific encryption specifics are owned by B14A; the OpenTelemetry collector path is owned by monitoring (B15B).

## Data Policies

### Data training policy

- **Consumer users (Free, Pro, Max plans)**: You choose whether your data is used to improve future Claude models. When the setting is on, Anthropic trains new models using data from Free, Pro, and Max accounts — including when you use Claude Code from those accounts.
- **Commercial users (Team and Enterprise plans, API, 3rd-party platforms, Claude Gov)**: Anthropic does **not** train generative models using code or prompts sent to Claude Code under commercial terms, unless the customer has chosen to provide their data (for example, via the Development Partner Program).

### Development Partner Program

If you explicitly opt in to provide training materials — such as via the Development Partner Program — Anthropic may use those materials to train its models. An organization admin can expressly opt in for their organization. The program is available **only for Anthropic first-party API**, not for Bedrock or Vertex users.

### Feedback using `/feedback`

If you send feedback about Claude Code via the `/feedback` command, Anthropic may use it to improve its products and services. Transcripts shared via `/feedback` are retained for **5 years**.

### Session quality surveys

The "How is Claude doing this session?" prompt records **only your rating** (including selecting "Dismiss") — no conversation transcripts, inputs, outputs, or other session data. Unlike thumbs up/down feedback or `/feedback` reports, this is a simple product-satisfaction metric. A separate optional follow-up ("Can Anthropic look at your session transcript…?") may appear: selecting **Yes** uploads the conversation transcript, any subagent transcripts, and the raw session log (known API key and token patterns redacted before upload; source code and file contents uploaded as-is, retained up to 6 months); **No** declines; **Don't ask again** stops the follow-up permanently. Nothing uploads unless you select **Yes**. Organizations under zero data retention, where product feedback is disabled by policy, or where `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set, never see this follow-up. Survey responses do not impact data-training preferences and cannot train AI models. (Survey opt-out env vars are detailed in the [env-vars reference](https://code.claude.com/docs/en/settings).)

### Data retention

Retention depends on account type and preferences:

- **Consumer users**: 5-year retention if you allow data use for model improvement; **30-day** retention if you don't. Privacy settings can be changed at any time.
- **Commercial users (Team, Enterprise, API)**: standard **30-day** retention. [Zero data retention](cc_zero_data_retention.md) is available to qualified accounts for Claude Code on Claude for Enterprise (not in the standard Enterprise plan; enabled per-organization by your account team after confirming eligibility).
- **Local caching**: Claude Code clients store session transcripts locally in **plaintext** under `~/.claude/projects/` for **30 days** by default (for session resumption); adjust with `cleanupPeriodDays`.

You can delete individual Claude Code on the web sessions at any time; deletion permanently removes the session's event data. Full terms are in the Commercial Terms of Service (Team/Enterprise/API) or Consumer Terms (Free/Pro/Max) and the Privacy Policy.

## Data Access

For first-party users, data logging is documented for **local** Claude Code and **remote** Claude Code (see the data-flow sections below). [Remote Control](https://code.claude.com/docs/en/remote-control) sessions follow the **local** data flow because all execution happens on your machine. For remote Claude Code, Claude accesses only the repository where you **initiate** the session — not repositories you have connected but not started a session in.

## Data Flow and Dependencies

### Local Claude Code

Claude Code runs locally and sends data over the network to interact with the LLM. This data includes all user prompts and model outputs, **encrypted in transit via TLS 1.2+**. Claude Code is compatible with most popular VPNs and LLM proxies. **Encryption at rest depends on your model provider**:

| Provider | Encryption at rest |
|---|---|
| Anthropic API | Infrastructure-level disk encryption (AES-256). Enable Zero Data Retention for no server-side persistence. |
| Amazon Bedrock | AES-256 with AWS-managed keys. Customer-managed keys available via AWS KMS. |
| Google Cloud Vertex AI | Google-managed encryption keys. CMEK available. |
| Microsoft Foundry | Requests route to Anthropic infrastructure with AES-256 disk encryption. |

(Provider-specific encryption-at-rest details are owned by B14A; API security-control / logging artifacts are in the Anthropic Trust Center.)

### Cloud execution

When using [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web), sessions run in Anthropic-managed VMs instead of locally:

- **Code and data storage**: your repository is cloned to an isolated VM; code and session data follow your account type's retention and usage policies.
- **Credentials**: GitHub authentication is handled through a secure proxy; your GitHub credentials never enter the sandbox.
- **Network traffic**: all outbound traffic goes through a security proxy for audit logging and abuse prevention.
- **Session data**: prompts, code changes, and outputs follow the same data policies as local usage.

## Telemetry Services

- **Operational metrics** (latency, reliability, usage patterns): logged from users' machines to Anthropic — **does not include any code or file paths**; encrypted in transit and at rest. Opt out with the `DISABLE_TELEMETRY` environment variable.
- **Error logging**: sent to Sentry; encrypted in transit (TLS) and at rest (256-bit AES). Opt out with `DISABLE_ERROR_REPORTING`.
- **`/feedback` reports**: a copy of your conversation history (including code) is sent to Anthropic; you choose how much history to include (default current session only, or other same-project sessions from the last 24 hours or 7 days). Encrypted in transit via TLS, stored in Google Cloud Storage (encrypted at rest by default); optionally creates a GitHub issue in the public repository. Opt out with `DISABLE_FEEDBACK_COMMAND=1`.
- **Third-party providers / no credentials**: when using Bedrock, Vertex, or with no Anthropic credentials configured, `/feedback` writes the report to a local archive under `~/.claude/feedback-bundles/` instead of sending it. Known API key and token patterns are redacted before the archive is written; nothing leaves your machine until you send the file to your Anthropic representative or attach it to a support request.

## Default Behaviors by API Provider

By default, error reporting, telemetry, and bug reporting are **disabled** when using Bedrock, Vertex, Foundry, or Claude Platform on AWS. **Session quality surveys** and the **WebFetch domain safety check** are exceptions and run regardless of provider. `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` opts out of all non-essential traffic (including surveys) at once but does **not** affect the WebFetch check (which has its own opt-out). All environment variables can be checked into `settings.json`.

By provider default: on **Claude API**, Metrics / Sentry / `/feedback` are **on** (disable via `DISABLE_TELEMETRY=1` / `DISABLE_ERROR_REPORTING=1` / `DISABLE_FEEDBACK_COMMAND=1`); on **Vertex / Bedrock / Foundry / Claude Platform on AWS** they are **off** unless the respective use flag is set (`CLAUDE_CODE_USE_VERTEX` / `CLAUDE_CODE_USE_BEDROCK` / `CLAUDE_CODE_USE_FOUNDRY` / `CLAUDE_CODE_USE_ANTHROPIC_AWS`). Session quality surveys default **on** for all providers (disable via `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`), and the WebFetch domain safety check defaults **on** for all providers (disable via `skipWebFetchPreflight: true` in settings). As of v2.1.126, when a host sets `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`, metrics default **on** for Vertex/Bedrock/Foundry and follow the standard `DISABLE_TELEMETRY` opt-out, while Sentry and `/feedback` remain off by default on those providers. (Full env-var semantics → [env-vars reference](https://code.claude.com/docs/en/settings); OpenTelemetry collector → [monitoring](https://code.claude.com/docs/en/monitoring-usage).)

### WebFetch domain safety check

Before fetching a URL, the WebFetch tool sends the requested **hostname only** (not the full URL, path, or page contents) to `api.anthropic.com` to check it against an Anthropic-maintained safety blocklist; results are cached per hostname for **five minutes**. This check runs regardless of model provider and is **not** affected by `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. If your network blocks `api.anthropic.com`, WebFetch requests fail until you allowlist the domain or set `skipWebFetchPreflight: true`. Disabling the check means WebFetch attempts any URL without consulting the blocklist, so combine it with [WebFetch permission rules](https://code.claude.com/docs/en/permissions#webfetch) to restrict reachable domains.

**Source**: https://code.claude.com/docs/en/data-usage
**Last Updated**: 2026-06-13
**Status**: Active
