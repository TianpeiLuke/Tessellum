---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - msteams
keywords:
  - msteams federated authentication
  - certificate based bot auth
  - azure managed identity teams
  - aks workload identity openclaw
  - authType federated certificatePath
  - useManagedIdentity managedIdentityClientId
  - MSTEAMS_AUTH_TYPE env var
  - azure imds bot token
topics:
  - OpenClaw
  - Microsoft Teams Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/msteams
access_control_group: ["general"]
---

# OpenClaw — Microsoft Teams Federated Authentication (Certificate + Managed Identity)

## Overview

This note is the production-grade authentication procedure for the OpenClaw Microsoft Teams channel: how to replace the default client-secret bot credential with **federated authentication** (added in 2026.4.11). It mirrors the "Federated authentication (certificate plus managed identity)", "Environment variables", and federated `channels.msteams.*` configuration material of the `channels/msteams` source page. It covers the two federated methods — Option A certificate-based auth and Option B Azure Managed Identity (system-assigned and user-assigned) — the AKS workload-identity setup, the federated auth env-var family, and the secret-vs-certificate-vs-managed-identity comparison. It does NOT cover the initial Teams quick setup / Azure Bot registration (see `oc_channels_msteams_setup.md`) or day-to-day messaging behavior (see `oc_channels_msteams_messaging.md`).

For production deployments, OpenClaw supports federated authentication as a more secure alternative to client secrets. Two methods are available: a PEM certificate registered with the Entra ID app registration, or Azure Managed Identity for passwordless auth. When `authType` is not set, OpenClaw defaults to client-secret authentication, and existing configurations continue to work without changes.

## Option A: Certificate-based authentication

Use a PEM certificate registered with your Entra ID app registration instead of a shared client secret. Setup is two steps: (1) generate or obtain a certificate (PEM format with private key); (2) in Entra ID → App Registration → **Certificates & secrets** → **Certificates** → upload the public certificate.

Config (note there is no `appPassword`; `authType: "federated"` plus `certificatePath` replace it):

```json5
{
  channels: {
    msteams: {
      enabled: true,
      appId: "<APP_ID>",
      tenantId: "<TENANT_ID>",
      authType: "federated",
      certificatePath: "/path/to/cert.pem",
      webhook: { port: 3978, path: "/api/messages" },
    },
  },
}
```

Equivalent environment variables:

- `MSTEAMS_AUTH_TYPE=federated`
- `MSTEAMS_CERTIFICATE_PATH=/path/to/cert.pem`

`MSTEAMS_CERTIFICATE_THUMBPRINT` / `channels.msteams.certificateThumbprint` is optional and not required for auth.

## Option B: Azure Managed Identity

Use Azure Managed Identity for passwordless authentication. This is ideal for deployments on Azure infrastructure (AKS, App Service, Azure VMs) where a managed identity is available.

**How it works:** (1) The bot pod/VM has a managed identity (system-assigned or user-assigned). (2) A **federated identity credential** links the managed identity to the Entra ID app registration. (3) At runtime, OpenClaw uses `@azure/identity` to acquire tokens from the Azure IMDS endpoint (`169.254.169.254`). (4) The token is passed to the Teams SDK for bot authentication.

**Prerequisites:** Azure infrastructure with managed identity enabled (AKS workload identity, App Service, VM); a federated identity credential created on the Entra ID app registration; and network access to IMDS (`169.254.169.254:80`) from the pod/VM.

Config for a **system-assigned** managed identity (set `useManagedIdentity: true`, no `appPassword`):

```json5
{
  channels: {
    msteams: {
      enabled: true,
      appId: "<APP_ID>",
      tenantId: "<TENANT_ID>",
      authType: "federated",
      useManagedIdentity: true,
      webhook: { port: 3978, path: "/api/messages" },
    },
  },
}
```

For a **user-assigned** managed identity, additionally set `managedIdentityClientId` to the managed identity's client ID:

```json5
{
  channels: {
    msteams: {
      enabled: true,
      appId: "<APP_ID>",
      tenantId: "<TENANT_ID>",
      authType: "federated",
      useManagedIdentity: true,
      managedIdentityClientId: "<MI_CLIENT_ID>",
      webhook: { port: 3978, path: "/api/messages" },
    },
  },
}
```

Equivalent environment variables:

- `MSTEAMS_AUTH_TYPE=federated`
- `MSTEAMS_USE_MANAGED_IDENTITY=true`
- `MSTEAMS_MANAGED_IDENTITY_CLIENT_ID=<client-id>` (only for user-assigned)

## AKS Workload Identity Setup

For AKS deployments using workload identity, the procedure is five steps. (1) **Enable workload identity** on your AKS cluster. (2) **Create a federated identity credential** on the Entra ID app registration:

```bash
az ad app federated-credential create --id <APP_OBJECT_ID> --parameters '{
  "name": "my-bot-workload-identity",
  "issuer": "<AKS_OIDC_ISSUER_URL>",
  "subject": "system:serviceaccount:<NAMESPACE>:<SERVICE_ACCOUNT>",
  "audiences": ["api://AzureADTokenExchange"]
}'
```

(3) **Annotate the Kubernetes service account** with the app client ID (`azure.workload.identity/client-id`):

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-bot-sa
  annotations:
    azure.workload.identity/client-id: "<APP_CLIENT_ID>"
```

(4) **Label the pod** for workload identity injection:

```yaml
metadata:
  labels:
    azure.workload.identity/use: "true"
```

(5) **Ensure network access** to IMDS (`169.254.169.254`) — if using a NetworkPolicy, add an egress rule allowing traffic to `169.254.169.254/32` on port 80.

## Federated authentication environment variables

All federated config keys can be set via environment variables instead of `channels.msteams.*`:

- `MSTEAMS_AUTH_TYPE` (optional: `"secret"` or `"federated"`)
- `MSTEAMS_CERTIFICATE_PATH` (federated + certificate)
- `MSTEAMS_CERTIFICATE_THUMBPRINT` (optional, not required for auth)
- `MSTEAMS_USE_MANAGED_IDENTITY` (federated + managed identity)
- `MSTEAMS_MANAGED_IDENTITY_CLIENT_ID` (user-assigned MI only)

The matching `channels.msteams.*` config keys are: `authType` (`"secret"` default, or `"federated"`), `certificatePath` (path to PEM certificate file for federated + certificate auth), `certificateThumbprint` (optional, not required for auth), `useManagedIdentity` (enable managed identity auth in federated mode), and `managedIdentityClientId` (client ID for user-assigned managed identity). The base bot credentials (`appId`, `tenantId`) are still required; only `appPassword` is replaced under federated auth.

## Auth type comparison

OpenClaw exposes three bot-authentication methods; federated auth (certificate or managed identity) is the production-hardened path that removes the rotating shared secret.

| Method | Config | Pros | Cons |
| --- | --- | --- | --- |
| **Client secret** | `appPassword` | Simple setup | Secret rotation required, less secure |
| **Certificate** | `authType: "federated"` + `certificatePath` | No shared secret over network | Certificate management overhead |
| **Managed Identity** | `authType: "federated"` + `useManagedIdentity` | Passwordless, no secrets to manage | Azure infrastructure required |

**Default behavior:** When `authType` is not set, OpenClaw defaults to client secret authentication. Existing configurations continue to work without changes.

**Source**: OpenClaw documentation — `channels/msteams` (mirror `inbox/openclaw_docs/channels/msteams.md`), "Federated authentication (certificate plus managed identity)" + federated config/env sections
**Last Updated**: 2026-06-22
**Status**: Active
