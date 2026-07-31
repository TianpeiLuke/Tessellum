---
tags:
  - resource
  - documentation
  - hermes_agent
  - authentication
  - microsoft_graph
keywords:
  - microsoft graph app registration
  - app-only client-credentials auth
  - MSGRAPH env vars
  - application access policy
  - teams meeting pipeline
  - client secret rotation
topics:
  - Hermes Agent
  - Microsoft Graph
  - Authentication
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/microsoft-graph-app-registration
access_control_group: ["general"]
---

# Register a Microsoft Graph Application

## Overview

This guide is the **Azure-portal prerequisite** for the Hermes Teams meeting pipeline: a step-by-step walkthrough for creating the Azure AD application registration that lets Hermes read Teams meeting transcripts, recordings, and related artifacts from Microsoft Graph. The pipeline uses **app-only (daemon / client-credentials)** authentication — no user sign-in and no interactive consent per meeting — which requires an app registration with admin-consented *application* permissions. The procedure has six steps (register the app, create a client secret, grant Graph permissions, admin-consent, optionally scope with an Application Access Policy, write the env file, and verify the token flow), plus secret rotation. The three values collected (`MSGRAPH_TENANT_ID`, `MSGRAPH_CLIENT_ID`, `MSGRAPH_CLIENT_SECRET`) land in `~/.hermes/.env` and feed the `MicrosoftGraphTokenProvider`. You need **tenant admin rights** (or an admin to consent on your behalf) to finish. This is a standalone prerequisite — safe to complete in advance of the runtime pages.

## Prerequisites

- A Microsoft 365 tenant with Teams Premium or Teams licenses that produce meeting transcripts and recordings.
- Admin access to the Azure portal at [entra.microsoft.com](https://entra.microsoft.com).
- A publicly reachable HTTPS endpoint for Graph change notifications (stood up later, in the webhook listener step).

## Step 1: Create the App Registration

1. Sign in to [entra.microsoft.com](https://entra.microsoft.com) as a tenant admin.
2. Navigate to **Identity → Applications → App registrations**.
3. Click **New registration**.
4. Fill in **Name** (`Hermes Teams Meeting Pipeline` or any recognizable name), **Supported account types** = *Accounts in this organizational directory only (Single tenant)*, and leave **Redirect URI** blank — app-only auth does not need one.
5. Click **Register**.

From the app's overview page, copy two values: the **Application (client) ID** → `MSGRAPH_CLIENT_ID`, and the **Directory (tenant) ID** → `MSGRAPH_TENANT_ID`.

## Step 2: Create a Client Secret

1. Open **Certificates & secrets** in the left nav.
2. Click **New client secret**.
3. Set **Description** `hermes-graph-secret` and an **Expires** value matching your rotation policy (6–24 months is typical).
4. Click **Add**.
5. Copy the **Value** column immediately — it is only shown once. That value is `MSGRAPH_CLIENT_SECRET`. The **Secret ID** column is *not* the secret; you want the **Value** column.

## Step 3: Grant Graph API Permissions

The pipeline uses a minimum-viable set of *application* permissions — add only what you need, since each one widens what the app can read tenant-wide. In **API permissions**, click **Add a permission → Microsoft Graph → Application permissions**, add the rows below, then click **Grant admin consent for `<your tenant>`** so the Status column flips to a green checkmark for every permission.

**Required for transcript-first summaries:** `OnlineMeetings.Read.All` (read Teams meeting metadata — subject, participants, join URL) and `OnlineMeetingTranscript.Read.All` (read Teams-generated transcripts).

**Required for recording fallback (no transcript):** `OnlineMeetingRecording.Read.All` (download recordings for offline STT) and `CallRecords.Read.All` (resolve meetings from call records when only the join URL is known).

**Required for outbound summary delivery (Graph mode only):** if `platforms.teams.extra.delivery_mode` is `graph`, add `ChannelMessage.Send` (post into Teams channels) and `Chat.ReadWrite.All` (post into 1:1/group chats, only if `chat_id` is the delivery target). Skip these if you use `incoming_webhook` delivery mode.

**Not recommended:** `OnlineMeetings.ReadWrite.All` / `Chat.ReadWrite` without `.All` (broader than needed); and *delegated* permissions — the pipeline uses the app-only client-credentials flow, so delegated permissions will not work without user sign-in.

## Step 4: (Recommended) Scope the App with an Application Access Policy

By default, application permissions like `OnlineMeetings.Read.All` grant access to **every** meeting in the tenant. For partner demos and dev tenants that is fine; for production you almost certainly want to restrict which users' meetings the app can read. Teams provides **Application Access Policies** for exactly this — a PowerShell-only surface with no portal UI. From an admin PowerShell with the MicrosoftTeams module connected (`Connect-MicrosoftTeams`):

```powershell
# Create a policy scoped to the Hermes app
New-CsApplicationAccessPolicy `
  -Identity "Hermes-Meeting-Pipeline-Policy" `
  -AppIds "<MSGRAPH_CLIENT_ID>" `
  -Description "Restrict Hermes meeting pipeline to allow-listed users"

# Grant the policy to specific users whose meetings the pipeline may read
Grant-CsApplicationAccessPolicy `
  -PolicyName "Hermes-Meeting-Pipeline-Policy" `
  -Identity "alice@example.com"

Grant-CsApplicationAccessPolicy `
  -PolicyName "Hermes-Meeting-Pipeline-Policy" `
  -Identity "bob@example.com"
```

Propagation can take up to 30 minutes after granting. Verify with `Test-CsApplicationAccessPolicy -Identity "alice@example.com" -AppId "<MSGRAPH_CLIENT_ID>"`. Without the policy, **any** user's meetings are readable — that is what the permission technically grants — so do not skip this step on a production tenant.

## Step 5: Write the Credentials to Your Env File

Put the three collected values into `~/.hermes/.env`, then lock down file permissions so only you can read the secret:

```bash
MSGRAPH_TENANT_ID=<directory-tenant-id>
MSGRAPH_CLIENT_ID=<application-client-id>
MSGRAPH_CLIENT_SECRET=<client-secret-value>

chmod 600 ~/.hermes/.env
```

## Step 6: Verify the Token Flow

Hermes ships a Graph auth smoke-test. From your Hermes install:

```python
python -c "
import asyncio
from tools.microsoft_graph_auth import MicrosoftGraphTokenProvider
provider = MicrosoftGraphTokenProvider.from_env()
token = asyncio.run(provider.get_access_token())
print('Token acquired, length:', len(token))
print(provider.inspect_token_health())
"
```

A successful run prints a long token string and a health dict showing `cached: True` with an `expires_in_seconds` value near 3600. Failures raise a `MicrosoftGraphTokenError` carrying the Azure error code:

| Azure error | Meaning | Fix |
|-------------|---------|-----|
| `AADSTS7000215: Invalid client secret` | Secret value mismatched or expired. | Generate a new secret in step 2; update `.env`. |
| `AADSTS700016: Application not found` | Wrong `MSGRAPH_CLIENT_ID` or wrong tenant. | Double-check the values from step 1 are from the same app. |
| `AADSTS90002: Tenant not found` | Typo in `MSGRAPH_TENANT_ID`. | Re-copy the Directory (tenant) ID from the app overview. |
| `insufficient_claims` at call time (not token time) | Token acquires but Graph returns 401/403. | You skipped step 3 admin-consent, or added permissions without re-consenting. Revisit API permissions and click **Grant admin consent** again. |

## Rotating the Client Secret

Azure client secrets have a hard expiry. Before yours expires: (1) create a *second* client secret in step 2 without deleting the first; (2) update `MSGRAPH_CLIENT_SECRET` in `~/.hermes/.env` with the new value; (3) restart the gateway so the new secret is picked up (`hermes gateway restart`); (4) verify with the smoke test above; (5) delete the old secret from the Azure portal. Overlapping the two secrets keeps the token flow uninterrupted across the rotation.

## Next Steps

Once credentials verify cleanly, continue with **webhook listener setup** (stand up the `msgraph_webhook` gateway platform that receives Graph change notifications), **pipeline configuration** (configure the Teams meeting pipeline runtime and operator CLI), and **outbound delivery** (wire summaries back into a Teams channel or chat). Those pages land alongside the PRs that add the corresponding runtime; this credentials setup is a standalone prerequisite.

## Related Notes

**Terms**
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth access token; relevance: app-only client-credentials is an OAuth token flow.
- [term_authentication](../../term_dictionary/term_authentication.md) — authentication concept; relevance: the registered app authenticates Hermes to Graph.
- [term_access_control](../../term_dictionary/term_access_control.md) — access control; relevance: the minimal Graph permissions + Application Access Policy are least-privilege access control.
- [term_oauth](../../term_dictionary/term_oauth.md) — OAuth framework; relevance: the client-credentials grant is an OAuth flow.
- [term_pii](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: transcripts carry PII, motivating tenant scoping.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — idempotency; relevance: overlapping secret rotation keeps the token flow idempotent.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — autonomous agents; relevance: the meeting pipeline runs the agent unattended on Graph data.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent harness; relevance: the token feeds the harness's MS-Graph tool. (+fin: term_pkce [own SP09], term_messaging_gateway [own SP11])

**Code-Repos**
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — MS-Graph tool + credential files + token provider; relevance: `MicrosoftGraphTokenProvider` smoke test and the `MSGRAPH_*`-driven tool are implemented here.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — MS-Graph webhook platform + Teams adapter; relevance: the registered app feeds the Teams meeting pipeline gateway.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — auth storage + OAuth-callback server + env write; relevance: writing the `MSGRAPH_*` env vars and the token-flow verify live here.
- [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — Teams pipeline plugin; relevance: the Teams meeting summary pipeline is a plugin consuming this app.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — `~/.hermes/` env/secret layout; relevance: the env-file + secret-rotation destinations are rooted here.

**Snippets**
- [snippet_hermes_agent_tools_msgraph](../../code_snippets/snippet_hermes_agent_tools_msgraph.md) — MS-Graph tool/auth; relevance: the registered app feeds this tool.
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — msgraph webhook platform; relevance: the change-notification listener the app powers.
- [snippet_hermes_agent_plugins_teams_pipeline](../../code_snippets/snippet_hermes_agent_plugins_teams_pipeline.md) — Teams meeting pipeline; relevance: the pipeline this app registration enables.
- [snippet_hermes_agent_plugins_platform_teams](../../code_snippets/snippet_hermes_agent_plugins_platform_teams.md) — Teams platform adapter; relevance: the outbound `graph`-mode delivery surface.
- [snippet_hermes_agent_plugins_google_meet](../../code_snippets/snippet_hermes_agent_plugins_google_meet.md) — Google-Meet pipeline; relevance: the analogous meeting pipeline for comparison.
- [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — credential storage; relevance: where the `MSGRAPH_*` secret is persisted.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — auth login/logout; relevance: the auth lifecycle the env-write participates in.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential-source resolution; relevance: the `.env` source the `MSGRAPH_*` vars resolve from.
- [snippet_hermes_agent_tools_credential_files](../../code_snippets/snippet_hermes_agent_tools_credential_files.md) — credential files; relevance: the on-disk secret layout the app's secret lands in.
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — OAuth-callback server; relevance: the OAuth-flow code the registered app exercises.

**Docs**
- [hermes_automation_blueprints_event](hermes_automation_blueprints_event.md) — event automation; relevance: the Teams/webhook meeting pipeline this app registration enables.
- [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: the allowlist/secret-rotation security tips.
- [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the OAuth parallels for authenticating remote tools.
- [hermes_migrate_from_openclaw](hermes_migrate_from_openclaw.md) — migration reference; relevance: the migrated secret/key (`SecretRef`) resolution this env-write reuses.
- [hermes_python_library_guide](hermes_python_library_guide.md) — embedding `AIAgent`; relevance: programmatic use of the `MSGRAPH_*` token from the library.
- [cc_authentication](../claude_code/cc_authentication.md) — CC auth/token model; relevance: closest analogue to the OAuth client-credentials flow.
- [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — CC remote-service OAuth; relevance: analogue to the app-only token flow.
- [cc_what_claude_can_access](../claude_code/cc_what_claude_can_access.md) — CC least-privilege access scoping; relevance: analogue to the minimal Graph permissions + Application Access Policy.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — CC security model; relevance: analogue to the least-privilege/secret-rotation guidance.
- [cc_settings_files](../claude_code/cc_settings_files.md) — CC env/secret config; relevance: analogue to writing the `MSGRAPH_*` env vars.
- [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — CC secure-deployment principles; relevance: analogue to least-privilege app registration + secret-rotation hardening.
- [cc_environment_variables](../claude_code/cc_environment_variables.md) — CC env-var configuration; relevance: analogue to persisting the `MSGRAPH_TENANT/CLIENT/SECRET` env vars.

**Source**: `inbox/hermes_agent_docs/guides/microsoft-graph-app-registration.md` · https://hermes-agent.nousresearch.com/docs/guides/microsoft-graph-app-registration
**Last Updated**: 2026-06-19
**Status**: Active
