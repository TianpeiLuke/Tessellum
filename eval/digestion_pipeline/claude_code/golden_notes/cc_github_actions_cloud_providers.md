---
tags:
  - resource
  - documentation
  - claude_code
  - github_actions
  - cloud_providers
keywords:
  - github actions bedrock vertex
  - claude code action enterprise
  - oidc authentication github actions
  - workload identity federation
  - use_bedrock use_vertex
  - aws_role_to_assume
  - custom github app token
  - data residency billing control
topics:
  - Claude Code
  - CI/CD
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/github-actions
access_control_group: ["general"]
---

# Claude Code GitHub Actions — Amazon Bedrock & Google Vertex AI

## Overview

For enterprise environments, you can run [Claude Code GitHub Actions](cc_github_actions.md) against your own cloud infrastructure — **Amazon Bedrock** or **Google Vertex AI** — instead of the direct Claude API. This approach gives you control over **data residency and billing** while maintaining the same `@claude` PR-creation functionality. The procedure has four steps: create a custom GitHub App (recommended for third-party providers), configure secure cloud-provider authentication via **OIDC** (Bedrock) or **Workload Identity Federation** (Vertex), add the required repository secrets, and create workflow files that select the backend with `use_bedrock` / `use_vertex`.

The defining security property is that no static cloud credentials are stored: GitHub Actions authenticates to AWS or GCP with temporary, automatically-rotated credentials obtained through identity federation. Provider account setup detail (enabling Bedrock, configuring the GCP project) is covered by the cloud model providers documentation; this note covers wiring that backend into the Action.

## Prerequisites

Before setting up Claude Code GitHub Actions with cloud providers:

**For Google Cloud Vertex AI:**

1. A Google Cloud Project with Vertex AI enabled
2. Workload Identity Federation configured for GitHub Actions
3. A service account with the required permissions
4. A GitHub App (recommended) or use the default `GITHUB_TOKEN`

**For Amazon Bedrock:**

1. An AWS account with Amazon Bedrock enabled
2. GitHub OIDC Identity Provider configured in AWS
3. An IAM role with Bedrock permissions
4. A GitHub App (recommended) or use the default `GITHUB_TOKEN`

## Step 1 — Create a custom GitHub App (recommended for 3P providers)

For best control and security when using third-party providers like Vertex AI or Bedrock, create your own GitHub App:

1. Go to `https://github.com/settings/apps/new`.
2. Fill in the basic information — **GitHub App name** (e.g. "YourOrg Claude Assistant") and **Homepage URL**.
3. Configure app settings: under **Webhooks**, uncheck "Active" (not needed for this integration).
4. Set the required **Repository permissions**: Contents — Read & Write; Issues — Read & Write; Pull requests — Read & Write.
5. Click "Create GitHub App".
6. After creation, click "Generate a private key" and save the downloaded `.pem` file.
7. Note your **App ID** from the app settings page.
8. Install the app to your repository: from the app's settings page click "Install App", select your account or organization, choose "Only select repositories" and select the specific repository, then click "Install".
9. Add the private key as a repository secret named `APP_PRIVATE_KEY` with the contents of the `.pem` file.
10. Add the App ID as a repository secret named `APP_ID`.

This app is used with the [`actions/create-github-app-token`](https://github.com/actions/create-github-app-token) action to generate authentication tokens in your workflows.

**Alternative for Claude API or if you don't want to set up your own app:** install the official Anthropic app from `https://github.com/apps/claude` — no additional authentication configuration is needed.

## Step 2 — Configure cloud provider authentication

Both providers follow the same security note: **use repository-specific configurations and grant only the minimum required permissions.**

### Amazon Bedrock

Configure AWS to allow GitHub Actions to authenticate securely without storing credentials:

1. **Enable Amazon Bedrock** — request access to Claude models; for cross-region models, request access in all required regions.
2. **Set up a GitHub OIDC Identity Provider** — Provider URL `https://token.actions.githubusercontent.com`, Audience `sts.amazonaws.com`.
3. **Create an IAM Role for GitHub Actions** — trusted entity type Web identity; identity provider `token.actions.githubusercontent.com`; permissions `AmazonBedrockFullAccess` policy; configure the trust policy for your specific repository.

After setup you need **`AWS_ROLE_TO_ASSUME`** — the ARN of the IAM role you created. OIDC is more secure than static AWS access keys because credentials are temporary and automatically rotated.

### Google Vertex AI

Configure Google Cloud to allow GitHub Actions to authenticate securely without storing credentials:

1. **Enable APIs** in your GCP project — IAM Credentials API, Security Token Service (STS) API, Vertex AI API.
2. **Create Workload Identity Federation resources** — create a Workload Identity Pool; add a GitHub OIDC provider with issuer `https://token.actions.githubusercontent.com`, attribute mappings for repository and owner, and (security recommendation) repository-specific attribute conditions.
3. **Create a Service Account** — grant only the `Vertex AI User` role; (security recommendation) create a dedicated service account per repository.
4. **Configure IAM bindings** — allow the Workload Identity Pool to impersonate the service account; (security recommendation) use repository-specific principal sets.

After setup you need **`GCP_WORKLOAD_IDENTITY_PROVIDER`** (the full provider resource name) and **`GCP_SERVICE_ACCOUNT`** (the service account email). Workload Identity Federation eliminates the need for downloadable service account keys, improving security.

## Step 3 — Add required secrets

Add these secrets to your repository (Settings → Secrets and variables → Actions):

- **Claude API (Direct):** `ANTHROPIC_API_KEY`; plus `APP_ID` and `APP_PRIVATE_KEY` if using your own GitHub App.
- **Google Cloud Vertex AI:** `GCP_WORKLOAD_IDENTITY_PROVIDER` and `GCP_SERVICE_ACCOUNT`; plus `APP_ID` and `APP_PRIVATE_KEY` if using your own app.
- **Amazon Bedrock:** `AWS_ROLE_TO_ASSUME`; plus `APP_ID` and `APP_PRIVATE_KEY` if using your own app.

## Step 4 — Create workflow files

Each workflow checks out the repo, generates a GitHub App token, authenticates to the cloud provider, and runs `anthropics/claude-code-action@v1` with the provider flag set. Note the Bedrock model ID carries a **region prefix** (e.g. `us.anthropic.claude-sonnet-4-6`); for Vertex the project ID is auto-retrieved from the auth step so it need not be hardcoded.

### Amazon Bedrock workflow

Required GitHub secrets: `AWS_ROLE_TO_ASSUME` (ARN of the IAM role for Bedrock access), `APP_ID`, `APP_PRIVATE_KEY`.

```yaml theme={null}
name: Claude PR Action

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

jobs:
  claude-pr:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
    runs-on: ubuntu-latest
    env:
      AWS_REGION: us-west-2
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
          aws-region: us-west-2

      - uses: anthropics/claude-code-action@v1
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          use_bedrock: "true"
          claude_args: '--model us.anthropic.claude-sonnet-4-6 --max-turns 10'
```

### Google Vertex AI workflow

Required GitHub secrets: `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT`, `APP_ID`, `APP_PRIVATE_KEY`.

```yaml theme={null}
name: Claude PR Action

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

jobs:
  claude-pr:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Authenticate to Google Cloud
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

      - uses: anthropics/claude-code-action@v1
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          trigger_phrase: "@claude"
          use_vertex: "true"
          claude_args: '--model claude-sonnet-4-5@20250929 --max-turns 10'
        env:
          ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
          CLOUD_ML_REGION: us-east5
          VERTEX_REGION_CLAUDE_4_5_SONNET: us-east5
```

## Action parameters relevant to providers

The provider backend is selected by two Action inputs (both optional, default to the direct Claude API): `use_bedrock` — "Use Amazon Bedrock instead of Claude API"; `use_vertex` — "Use Google Vertex AI instead of Claude API". `anthropic_api_key` is required for the direct Claude API but **not** for Bedrock/Vertex. The full input list and the quick-setup/`@claude` core integration are documented in [GitHub Actions](cc_github_actions.md).

## Troubleshooting authentication errors

For Bedrock/Vertex, check the credentials configuration and ensure secrets are named correctly in workflows. (For direct Claude API, confirm the API key is valid and has sufficient permissions.)

**Source**: https://code.claude.com/docs/en/github-actions
**Last Updated**: 2026-06-13
**Status**: Active
