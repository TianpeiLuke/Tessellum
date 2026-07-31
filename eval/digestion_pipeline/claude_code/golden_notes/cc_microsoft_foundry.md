---
tags:
  - resource
  - documentation
  - claude_code
  - cloud_model_providers
  - microsoft_foundry
keywords:
  - microsoft foundry
  - azure claude code
  - claude_code_use_foundry
  - anthropic_foundry_resource
  - microsoft entra id
  - azure rbac
  - pin model versions
  - api key authentication
topics:
  - Claude Code
  - Cloud Model Providers
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/microsoft-foundry
access_control_group: ["general"]
---

# Claude Code on Microsoft Foundry

## Overview

This note is the end-to-end procedure for pointing Claude Code at **Microsoft Foundry**, the Azure-hosted deployment surface for Claude models, instead of the default Anthropic API. The setup is **environment-variable-only**: unlike Amazon Bedrock and Google Vertex AI, Foundry has **no interactive setup wizard**, so the env vars in the Setup steps below are the only configuration path.

The procedure has five steps — provision an Azure Foundry resource with Claude deployments, configure Azure credentials (API key or Microsoft Entra ID), enable Foundry in Claude Code, pin model versions, and run Claude Code — followed by Azure RBAC role guidance and Entra-token troubleshooting. The full env-var catalog and the `pin-models-for-third-party-deployments` reference live in [Model configuration](https://code.claude.com/docs/en/model-config); the prompt-caching mechanism lives in [Prompt caching](https://code.claude.com/docs/en/prompt-caching).

## Prerequisites

Before configuring Claude Code with Microsoft Foundry, ensure you have:

- An Azure subscription with access to Microsoft Foundry
- RBAC permissions to create Microsoft Foundry resources and deployments
- Azure CLI installed and configured (optional — only needed if you don't have another mechanism for getting credentials)

If you are deploying Claude Code to multiple users, **pin your model versions** (Setup step 4) before rolling out.

## Setup

### 1. Provision Microsoft Foundry resource

First, create a Claude resource in Azure:

1. Navigate to the [Microsoft Foundry portal](https://ai.azure.com/)
2. Create a new resource, noting your resource name
3. Create deployments for the Claude models: **Claude Opus**, **Claude Sonnet**, and **Claude Haiku**

### 2. Configure Azure credentials

Claude Code supports **two authentication methods** for Microsoft Foundry; choose the one that best fits your security requirements.

**Option A: API key authentication.** In the Microsoft Foundry portal, navigate to your resource, go to the **Endpoints and keys** section, copy the **API Key**, and set the environment variable:

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Option B: Microsoft Entra ID authentication.** When `ANTHROPIC_FOUNDRY_API_KEY` is **not** set, Claude Code automatically uses the Azure SDK [default credential chain](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview), which supports a variety of methods for authenticating local and remote workloads. On local environments you commonly use the Azure CLI by running `az login`.

When using Microsoft Foundry, the `/logout` command is unavailable, since authentication is handled through Azure credentials.

### 3. Configure Claude Code

Set the following environment variables to enable Microsoft Foundry. Provide either the resource name (`ANTHROPIC_FOUNDRY_RESOURCE`) or the full base URL (`ANTHROPIC_FOUNDRY_BASE_URL`):

```bash theme={null}
# Enable Microsoft Foundry integration
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure resource name (replace {resource} with your resource name)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Or provide the full base URL:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

### 4. Pin model versions

**Pin specific model versions for every deployment.** Without pinning, model aliases such as `sonnet` and `opus` resolve to Claude Code's built-in default for Foundry, which can lag the newest release and may not yet be available in your account. **Foundry has no startup model check, so requests fail when the default is unavailable.** When you create Azure deployments, select a specific model version rather than "auto-update to latest."

Set the model variables to match the deployment names you created in step 1. Without `ANTHROPIC_DEFAULT_OPUS_MODEL`, the `opus` alias on Foundry resolves to Opus 4.6; set it to the Opus 4.8 ID to use the latest model:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

Background tasks such as session title generation use the **small/fast model**, normally a Haiku-class model. On Foundry, Claude Code defaults this to the **primary model** because not every account has a Haiku deployment. To use Haiku for background tasks, set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to a Haiku deployment available in your account (as shown above). For current and legacy model IDs, see the Models overview; for the full env-var list, see [Model configuration](https://code.claude.com/docs/en/model-config).

[Prompt caching](https://code.claude.com/docs/en/prompt-caching) is enabled automatically. To request a 1-hour cache TTL instead of the 5-minute default, set the following variable; cache writes with a 1-hour TTL are billed at a higher rate:

```bash theme={null}
export ENABLE_PROMPT_CACHING_1H=1
```

### 5. Run Claude Code

With the environment variables set, start Claude Code from your project directory by running `claude`. Claude Code reads `CLAUDE_CODE_USE_FOUNDRY` and the other Foundry variables from the environment and connects to your Azure resource on the first prompt. Unlike Bedrock and Vertex AI, Foundry has no interactive setup wizard, so the environment variables in steps 3 and 4 are the only configuration path.

## Azure RBAC configuration

The `Azure AI User` and `Cognitive Services User` default roles include all required permissions for invoking Claude models. For more restrictive permissions, create a custom role with the following:

```json theme={null}
{
  "permissions": [
    {
      "dataActions": [
        "Microsoft.CognitiveServices/accounts/providers/*"
      ]
    }
  ]
}
```

For details, see the [Microsoft Foundry RBAC documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Troubleshooting

If you receive an error `Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed`:

- Configure Entra ID on the environment, or set `ANTHROPIC_FOUNDRY_API_KEY`.

## Additional resources

- [Microsoft Foundry documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
- [Microsoft Foundry models](https://ai.azure.com/explore/models)
- [Microsoft Foundry pricing](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)

**Source**: https://code.claude.com/docs/en/microsoft-foundry
**Last Updated**: 2026-06-13
**Status**: Active
