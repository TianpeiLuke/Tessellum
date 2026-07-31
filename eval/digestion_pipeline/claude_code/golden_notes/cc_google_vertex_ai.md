---
tags:
  - resource
  - documentation
  - claude_code
  - cloud_providers
  - google_vertex_ai
keywords:
  - google vertex ai
  - claude_code_use_vertex
  - cloud_ml_region
  - vertex ai model garden
  - gcp credentials
  - setup-vertex wizard
  - pin model versions
  - aiplatform.user role
  - 1m token context window
  - vertex region overrides
topics:
  - Claude Code
  - Cloud Model Providers
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/google-vertex-ai
access_control_group: ["general"]
---

# Claude Code on Google Vertex AI

## Overview

This note is the end-to-end procedure for pointing Claude Code at **Google Vertex AI** instead of the default Anthropic API, so Claude models run inside your own GCP project (centralized GCP billing, IAM, and quota). It covers the interactive `/setup-vertex` login wizard, the scripted manual env-var path for CI / enterprise rollouts, region selection (`CLOUD_ML_REGION`), GCP credential configuration and auto-refresh, model pinning, startup model checks, the `roles/aiplatform.user` IAM grant, the 1M token context window, and troubleshooting.

Two paths exist: the **sign-in wizard** for individual users with their own GCP credentials, and the **manual setup** (environment variables) for deploying across a team — where you should pin model versions before rolling out. The full environment-variable catalog lives in the [Environment variables reference](https://code.claude.com/docs/en/env-vars) and the alias/pin reference in [Model configuration](https://code.claude.com/docs/en/model-config); this note links out to both rather than duplicating them.

## Prerequisites

Before configuring Claude Code with Vertex AI, ensure you have:

- A Google Cloud Platform (GCP) account with billing enabled
- A GCP project with Vertex AI API enabled
- Access to desired Claude models (for example, Claude Sonnet 4.6)
- Google Cloud SDK (`gcloud`) installed and configured
- Quota allocated in desired GCP region

## Sign in with Vertex AI

If you have Google Cloud credentials, the login wizard handles the Claude Code side (you complete the GCP-side prerequisites once per project). The Vertex AI setup wizard requires **Claude Code v2.1.98 or later** (`claude --version` to check). The three wizard steps are:

1. **Enable Claude models in your GCP project** — enable the Vertex AI API for your project, then request access to the Claude models you want in the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden).
2. **Start Claude Code and choose Vertex AI** — run `claude`; at the login prompt, select **3rd-party platform**, then **Google Vertex AI**.
3. **Follow the wizard prompts** — choose how you authenticate to Google Cloud (Application Default Credentials from `gcloud`, a service account key file, or credentials already in your environment). The wizard detects your project and region, verifies which Claude models your project can invoke, lets you pin them, and saves the result to the `env` block of your [user settings file](https://code.claude.com/docs/en/settings), so you don't export environment variables yourself.

After signing in, run `/setup-vertex` any time to reopen the wizard and change credentials, project, region, or model pins.

## Region configuration

Claude Code supports Vertex AI **global**, **multi-region**, and **regional** endpoints. Set `CLOUD_ML_REGION` to `global`, a multi-region location such as `eu` or `us`, or a specific region such as `us-east5`. Claude Code selects the correct Vertex AI hostname for each form, including the `aiplatform.eu.rep.googleapis.com` and `aiplatform.us.rep.googleapis.com` hosts for multi-region locations.

Vertex AI may not support the Claude Code default models on every endpoint type — model availability varies across specific regions, multi-region locations, and global endpoints. You may need to switch to a supported location or specify a supported model.

## Set up manually

To configure Vertex AI through environment variables instead of the wizard (for example in CI or a scripted enterprise rollout), follow these steps.

### 1. Enable Vertex AI API

Enable the Vertex AI API in your GCP project:

```bash
# Set your project ID
gcloud config set project YOUR-PROJECT-ID

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. Request model access

Request access to Claude models in Vertex AI: navigate to the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden), search for "Claude" models, request access to the desired Claude models (for example, Claude Sonnet 4.6), and wait for approval (may take 24-48 hours).

### 3. Configure GCP credentials

Claude Code uses standard Google Cloud authentication (see [Google Cloud authentication documentation](https://cloud.google.com/docs/authentication)). Claude Code v2.1.121 or later supports [X.509 certificate-based Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates) through the same Application Default Credentials chain; set `GOOGLE_APPLICATION_CREDENTIALS` to the path of your credential configuration file.

Claude Code uses `ANTHROPIC_VERTEX_PROJECT_ID` as the project ID for Vertex AI requests. The `GCLOUD_PROJECT` and `GOOGLE_CLOUD_PROJECT` environment variables and the credential file referenced by `GOOGLE_APPLICATION_CREDENTIALS` take precedence over it. If none of these are set, the project ID is resolved from your `gcloud` configuration or the attached service account.

**Advanced credential configuration.** Claude Code supports automatic credential refresh for GCP through the `gcpAuthRefresh` setting. When Claude Code detects that your GCP credentials are expired or cannot be loaded, it runs the configured command to obtain new credentials before retrying the request:

```json
{
  "gcpAuthRefresh": "gcloud auth application-default login",
  "env": {
    "ANTHROPIC_VERTEX_PROJECT_ID": "your-project-id"
  }
}
```

The command's output is displayed to the user, but interactive input isn't supported — this works well for browser-based authentication flows where the CLI shows a URL you complete in the browser. The refresh command times out after three minutes if authentication does not complete. If you set `gcpAuthRefresh` in project settings such as `.claude/settings.json`, the command runs only after you accept the workspace trust prompt.

### 4. Configure Claude Code

Set the following environment variables:

```bash
# Enable Vertex AI integration
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Optional: Override the Vertex endpoint URL for custom endpoints or gateways
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1

# Optional: Request 1-hour prompt cache TTL instead of the 5-minute default
export ENABLE_PROMPT_CACHING_1H=1

# When CLOUD_ML_REGION=global, override region for models that don't support global endpoints
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

Most model versions have a corresponding `VERTEX_REGION_CLAUDE_*` variable (see the [Environment variables reference](https://code.claude.com/docs/en/env-vars) for the full list). [Prompt caching](https://code.claude.com/docs/en/prompt-caching) is enabled automatically; set `DISABLE_PROMPT_CACHING=1` to disable it, or `ENABLE_PROMPT_CACHING_1H=1` for a 1-hour cache TTL (1-hour-TTL cache writes are billed at a higher rate). For heightened rate limits, contact Google Cloud support. When using Vertex AI, the `/logout` command is unavailable since authentication is handled through Google Cloud credentials.

Claude Code disables [MCP tool search](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search) by default on Vertex AI, so MCP tool definitions load upfront. Vertex AI supports tool search for Claude Sonnet 4.5 and later and Claude Opus 4.5 and later; set `ENABLE_TOOL_SEARCH=true` to enable it on those models. Earlier models on Vertex AI do not accept the required beta header, and requests fail if you enable tool search with them.

### 5. Pin model versions

Pin specific model versions when deploying to multiple users. Without pinning, model aliases such as `sonnet` and `opus` resolve to Claude Code's built-in default for Vertex AI, which can lag the newest release and may not yet be enabled in your project. Claude Code falls back to the previous version at startup when the default is unavailable, but pinning lets you control when your users move to a new model.

Set these environment variables to specific Vertex AI model IDs. Without `ANTHROPIC_DEFAULT_OPUS_MODEL`, the `opus` alias on Vertex resolves to Opus 4.6; set it to the Opus 4.8 ID to use the latest model:

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

When no pinning variables are set, Claude Code uses these defaults — Primary model `claude-sonnet-4-5@20250929`; Small/fast model: same as the primary model. Background tasks such as session title generation use the small/fast model, normally a Haiku-class model, but on Vertex AI Claude Code defaults this to the primary model because Haiku may not be enabled in every project or region. To use Haiku for background tasks, set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to a model ID available in your project. To customize models further, set `ANTHROPIC_MODEL` (e.g. `claude-opus-4-8`) alongside `ANTHROPIC_DEFAULT_HAIKU_MODEL`. See [Model configuration](https://code.claude.com/docs/en/model-config#pin-models-for-third-party-deployments) for the full list of environment variables.

## Startup model checks

When Claude Code starts with Vertex AI configured, it verifies that the models it intends to use are accessible in your project. This check requires Claude Code v2.1.98 or later.

- If you have pinned a model version older than the current Claude Code default, and your project can invoke the newer version, Claude Code prompts you to update the pin. Accepting writes the new model ID to your user settings file and restarts Claude Code. Declining is remembered until the next default version change.
- If you have not pinned a model and the current default is unavailable in your project, Claude Code falls back to the previous version for the current session and shows a notice. The fallback is not persisted. Enable the newer model in Model Garden or pin a version to make the choice permanent.

## IAM configuration

The `roles/aiplatform.user` role includes the required permissions:

- `aiplatform.endpoints.predict` — required for model invocation and token counting

For more restrictive permissions, create a custom role with only the permission above. Create a dedicated GCP project for Claude Code to simplify cost tracking and access control.

## 1M token context window

Claude Opus 4.6 and later, and Sonnet 4.6, support the [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) on Vertex AI. Claude Code automatically enables the extended context window when you select a 1M model variant. The setup wizard offers a 1M context option when it pins models; to enable it for a manually pinned model instead, append `[1m]` to the model ID.

## Troubleshooting

- **"Could not load the default credentials" errors** — run `gcloud auth application-default login` to set up Application Default Credentials, set `GOOGLE_APPLICATION_CREDENTIALS` to a service account key file path, or see Configure GCP credentials above for all options.
- **Quota issues** — check current quotas or request a quota increase through Cloud Console.
- **"model not found" 404 errors** — confirm the model is Enabled in Model Garden; verify it is available in the location you specified (some models are offered only on `global` or multi-region locations such as `eu` and `us`, not in specific regions); if using `CLOUD_ML_REGION=global`, check that your models support global endpoints in Model Garden under "Supported features". For models that don't support global endpoints, either specify a supported model via `ANTHROPIC_MODEL` or `ANTHROPIC_DEFAULT_HAIKU_MODEL`, or set a region or multi-region location using `VERTEX_REGION_<MODEL_NAME>` environment variables.
- **429 errors** — for regional endpoints, ensure the primary model and small/fast model are supported in your selected region; consider switching to `CLOUD_ML_REGION=global` for better availability.

**Source**: https://code.claude.com/docs/en/google-vertex-ai
**Last Updated**: 2026-06-13
**Status**: Active
