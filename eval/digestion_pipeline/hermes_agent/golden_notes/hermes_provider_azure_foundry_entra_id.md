---
tags:
  - resource
  - documentation
  - hermes_agent
  - providers
  - authentication
keywords:
  - microsoft entra id keyless auth
  - DefaultAzureCredential resolution order
  - azure foundry RBAC azure ai user
  - managed identity workload identity service principal
  - azure entra id env vars
topics:
  - Hermes Agent
  - Providers & Setup
  - Microsoft Entra ID
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/guides/azure-foundry
access_control_group: ["general"]
---

# Hermes Agent — Azure Foundry: Microsoft Entra ID (Keyless Auth)

## Overview

This is the **keyless authentication model** for Hermes Agent's `azure-foundry` provider — the production-recommended alternative to a static `AZURE_FOUNDRY_API_KEY`. Instead of a long-lived key, Hermes uses Microsoft Entra ID: `azure-identity`'s `DefaultAzureCredential` mints a **fresh JWT per request** and the upstream Foundry resource authorizes the call via **per-resource RBAC** (the `Azure AI User` role, shown as `Foundry User` in tenants mid-rename). Microsoft recommends this path for production Foundry workloads, and Hermes supports it across **both** wire formats — OpenAI-style (`api_mode: chat_completions` / `codex_responses` for GPT-4/5, Llama, Mistral, DeepSeek) and Anthropic-style (`api_mode: anthropic_messages` for Claude). Both surfaces use the same Microsoft RBAC and the same documented inference scope, `https://ai.azure.com/.default`.

The model has three load-bearing parts: (1) the **credential resolution chain** `DefaultAzureCredential` walks on each token request; (2) the **SDK-contract split** — the OpenAI SDK accepts a native callable that mints JWTs, while the Anthropic SDK does not, so Hermes installs an `httpx` request event hook to rewrite the bearer header per request; and (3) the **deployment-pattern matrix** (local `az login`, managed identity, workload identity, service principal, sovereign clouds). This note is the auth-model deep-dive; the wizard procedure that selects this mode lives in the sibling [setup note](hermes_provider_azure_foundry_setup.md).

## Why use Entra ID?

- No long-lived API keys to rotate or revoke.
- RBAC-driven access — grant or remove `Azure AI User` on the Foundry resource, no config rewrite needed.
- Access and audit logs are segmented by assignee instead of all callers sharing one static key.
- Single auth surface for Azure VMs, AKS pods, App Service, Functions, Container Apps, and Foundry Agent Service via managed identity.
- Workload identity and service-principal flows for CI/CD pipelines.

Under the hood, OpenAI-style endpoints use the OpenAI Python SDK's native callable `api_key=` contract — the SDK mints a fresh JWT per request automatically. Anthropic-style endpoints use an `httpx.Client` with a request event hook installed by `agent.azure_identity_adapter.build_bearer_http_client`, because the Anthropic SDK does not accept a callable `auth_token` natively. The hook rewrites `Authorization: Bearer <fresh-jwt>` per outbound request. Same Microsoft RBAC, same Foundry scope — the SDK contract is the only difference.

## One-time setup (Azure side)

1. In the Azure Portal, open your Foundry resource → **Access control (IAM)** → **Add → Add role assignment**.
2. Pick the **Azure AI User** role (or **Foundry User** if your tenant has the renamed role).
3. Assign it to:
   - **Your user account** for local development with `az login`.
   - **A managed identity or workload identity** for Azure-hosted compute (recommended for production).
   - **A Foundry Agent Service hosted agent's agent identity** when Hermes runs inside a hosted agent.
   - **A service principal** for CI/CD pipelines when workload identity is not available.
4. Wait ~5 minutes for the role to propagate.

Azure CLI equivalent:

```bash
az role assignment create \
  --assignee <principal-or-agent-identity-client-id> \
  --role "Azure AI User" \
  --scope <foundry-resource-id>
```

## One-time setup (Hermes side)

```bash
hermes model
# → Select "Azure Foundry"
# → Enter your endpoint URL
# → Authentication: 2 (Microsoft Entra ID)
# → (optional) user-assigned managed identity client ID
# → (optional) Azure tenant ID
# → Hermes probes DefaultAzureCredential() and reports which inner
#    credential succeeded (e.g. AzureCliCredential, ManagedIdentityCredential)
```

The wizard runs a **bounded preflight probe (10 s timeout)**. On failure it offers to "save anyway, validate later" — useful when configuring on a machine that doesn't yet have credentials but will at runtime (e.g. preparing config for a managed-identity deployment). `azure-identity` is installed automatically on first use via Hermes' lazy-install path; to pre-install, run `pip install azure-identity`.

## Configuration written to `config.yaml`

```yaml
model:
  provider: azure-foundry
  base_url: https://my-resource.openai.azure.com/openai/v1
  api_mode: chat_completions
  auth_mode: entra_id
  default: gpt-4o
  context_length: 128000
  entra:
    scope: https://ai.azure.com/.default        # only when overriding the default
```

Hermes manages only **one** Entra-specific knob in `config.yaml`: `scope`, the OAuth resource scope. It defaults to Microsoft's documented inference scope (`https://ai.azure.com/.default`); override it only if your resource was provisioned against a non-standard audience. Everything else — tenant, service-principal secret, federated token file, sovereign-cloud authority, broker preferences — is read by `azure-identity` directly from the standard `AZURE_*` environment variables (see the resolution order below). Set those in `~/.hermes/.env` or your deployment environment exactly as Microsoft's SDK reference describes. **No secrets land in `~/.hermes/.env` for Entra mode** — `azure-identity` caches tokens in-process (and where available, in your OS keychain / `~/.IdentityService`).

## Credential resolution order

`azure-identity`'s `DefaultAzureCredential` walks this chain on each token request, stopping at the first credential that returns a token:

1. **Environment credential** — `AZURE_TENANT_ID` + `AZURE_CLIENT_ID` + `AZURE_CLIENT_SECRET` (or `AZURE_CLIENT_CERTIFICATE_PATH` / `AZURE_FEDERATED_TOKEN_FILE`).
2. **Workload Identity** — `AZURE_FEDERATED_TOKEN_FILE` (AKS federated tokens / OIDC).
3. **Managed Identity** — IMDS endpoint (`169.254.169.254`) for virtual machines; `IDENTITY_ENDPOINT` for App Service / Functions / Container Apps. Foundry Agent Service hosted agents use the hosted agent's agent identity.
4. **Visual Studio Code** — Azure account extension.
5. **Azure CLI** — `az login` session.
6. **Azure Developer CLI** — `azd auth login`.
7. **Azure PowerShell** — `Connect-AzAccount`.
8. **Broker** (Windows / WSL only) — Web Account Manager.

Interactive browser credential is excluded by default for unattended Hermes runs; use Azure CLI, Azure Developer CLI, managed identity, workload identity, or service-principal credentials instead.

## Deployment patterns

**Local development** — `az login`, then `hermes model` (pick Azure Foundry → Entra ID), then `hermes` uses your `az login` token.

**Azure VM / Functions / App Service / Container Apps (system-assigned managed identity):**

1. Enable system-assigned identity on the compute resource.
2. Grant the identity `Azure AI User` (or `Foundry User`) on the Foundry resource.
3. Set `model.auth_mode: entra_id` in `config.yaml` — no env vars needed.

**User-assigned managed identity** — set `AZURE_CLIENT_ID` to the user-assigned identity's client ID so `DefaultAzureCredential` picks the right one.

**Foundry Agent Service hosted agent** — create the hosted agent and grant *that agent's* identity `Azure AI User` (or `Foundry User`) on the Foundry resource. Hermes uses `ManagedIdentityCredential` from inside the hosted agent; the role assignment belongs on the agent identity, not just the parent project or your user.

**AKS Workload Identity (replaces AAD Pod Identity)** — annotate the pod's service account with the workload-identity client ID; the pod's federated token file is auto-detected via `AZURE_FEDERATED_TOKEN_FILE`; `model.auth_mode: entra_id` works without further config changes.

**Service principal in CI** — set `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` in the runner env.

**Sovereign clouds (Government, China)** — export `AZURE_AUTHORITY_HOST` (e.g. `https://login.microsoftonline.us` for Azure Government, `https://login.partner.microsoftonline.cn` for Azure China). `azure-identity` reads it directly.

## Health checks

`hermes doctor` runs a 10 s probe against `DefaultAzureCredential` when `model.auth_mode: entra_id`, reporting which inner credential won (env vars present, managed identity endpoint reachable, etc.).

`hermes auth` shows a structured status block:

```
azure-foundry (Microsoft Entra ID):
  Endpoint: https://my-resource.openai.azure.com/openai/v1
  Scope: https://ai.azure.com/.default
  Status: configured; live token probe is skipped here
```

## Limitations

- **Anthropic-style endpoints use an httpx event hook.** The Anthropic Python SDK does not accept a callable `auth_token` natively (≤ 0.86.0). Hermes installs a request event hook on a custom `httpx.Client` that mints a fresh JWT per outbound request and rewrites `Authorization: Bearer <jwt>`. This is functionally equivalent to the OpenAI SDK's native `Callable[[], str]` contract but adds one indirection layer. If the Anthropic SDK adds first-class callable-auth support in a future release, Hermes will switch to it transparently.
- **Batch jobs and `multiprocessing.Pool`.** The Entra token provider is a closure that cannot be pickled across process boundaries. `batch_runner.py` automatically drops the callable from the worker config and lets each worker process rebuild its own provider from `config.yaml` — no user action required, but each worker pays one chain walk at startup.
- **No bearer JWT persistence in `auth.json`.** Hermes does not duplicate `azure-identity`'s internal token cache; cold starts walk the credential chain on first inference.

## Environment variables

| Variable | Purpose |
|----------|---------|
| `AZURE_TENANT_ID` | Entra ID tenant for service-principal flows |
| `AZURE_CLIENT_ID` | Entra ID client ID (service principal, workload identity, or user-assigned managed identity) |
| `AZURE_CLIENT_SECRET` | Service principal secret |
| `AZURE_CLIENT_CERTIFICATE_PATH` | Service principal cert (alternative to secret) |
| `AZURE_FEDERATED_TOKEN_FILE` | Workload Identity federated token path (AKS) |
| `AZURE_AUTHORITY_HOST` | Sovereign cloud authority host override |
| `IDENTITY_ENDPOINT` / `MSI_ENDPOINT` | Managed Identity endpoint for App Service, Functions, and Container Apps; VMs usually use IMDS instead |

The Azure SDK reads the `AZURE_*` env vars directly. Hermes never inspects them other than to report which sources are present in `hermes doctor` output.

## Troubleshooting (Entra-specific)

- **"Credential chain exhausted" or 401 after switching to `auth_mode: entra_id`.** Run `az login` to refresh your developer session; verify the `Azure AI User` (or `Foundry User`) role assignment took effect with `az role assignment list --assignee <user-or-identity-id>` (propagation can take up to 5 minutes); for user-assigned managed identities, check `AZURE_CLIENT_ID` matches the identity attached to the compute resource; run `hermes doctor` for the probe result + remediation hint.
- **Wizard preflight hangs or times out.** The 10 s preflight is a soft check — choose "Save anyway and validate later" and run `hermes doctor` after deploying to the target environment. Common causes: unreachable token service or stale local login state. Prefer workload identity in CI, set the service-principal trio when using a service principal, or run `az login` locally.
- **401 on Anthropic-style endpoint with Entra ID.** Verify the same `Azure AI User` (or `Foundry User`) role is assigned (it covers both `/openai/v1` and `/anthropic` paths). If the OpenAI-style probe works but `claude-*` requests fail at runtime, the most common cause is a stale `model.entra.scope` left from an earlier wizard run — delete the `entra.scope` line so the runtime falls back to the default `https://ai.azure.com/.default` scope.

**Source**: https://hermes-agent.nousresearch.com/docs/guides/azure-foundry
**Last Updated**: 2026-06-19
**Status**: Active
