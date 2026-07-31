---
tags:
  - resource
  - documentation
  - claude_code
  - ci_cd
  - gitlab
keywords:
  - gitlab ci/cd
  - gitlab-ci.yml claude job
  - anthropic_api_key masked variable
  - claude -p permission-mode acceptedits
  - allowedtools mcp__gitlab
  - ai_flow variables
  - merge request automation
  - bedrock vertex oidc gitlab
language: markdown
topics:
  - Claude Code
  - CI/CD
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/gitlab-ci-cd
access_control_group: ["general"]
---

# Claude Code GitLab CI/CD

## Overview

Claude Code for GitLab CI/CD (currently in **beta**, maintained by GitLab) lets you run Claude inside isolated GitLab CI jobs that commit results back through merge requests (MRs). You wire it in by adding one `claude` job to `.gitlab-ci.yml` and storing your API key as a masked CI/CD variable; an `@claude` mention in an issue, MR, or review thread (via a webhook/listener that calls the pipeline trigger API) then runs Claude to analyze context, write changes in a branch, and open an MR. The integration is built on the Claude Code CLI and Agent SDK, runs in sandboxed containers with workspace-scoped write permissions, and supports the Claude API, Amazon Bedrock, or Google Vertex AI as the model backend.

This note covers the GitLab integration end to end: why/how it works, quick and manual setup, example use cases, the configuration-example jobs (Claude API, Bedrock, Vertex), best practices, security and governance, troubleshooting, and advanced configuration.

## Why use Claude Code with GitLab?

- **Instant MR creation** — describe what you need and Claude proposes a complete MR with changes and explanation.
- **Automated implementation** — turn issues into working code with a single command or mention.
- **Project-aware** — Claude follows your `CLAUDE.md` guidelines and existing code patterns.
- **Simple setup** — add one job to `.gitlab-ci.yml` and a masked CI/CD variable.
- **Enterprise-ready** — choose Claude API, Amazon Bedrock, or Google Vertex AI to meet data residency and procurement needs.
- **Secure by default** — runs in your GitLab runners with your branch protection and approvals.

## How it works

Claude Code uses GitLab CI/CD to run AI tasks in isolated jobs and commit results back via MRs:

1. **Event-driven orchestration** — GitLab listens for your chosen triggers (for example, a comment that mentions `@claude` in an issue, MR, or review thread). The job collects context from the thread and repository, builds prompts from that input, and runs Claude Code.
2. **Provider abstraction** — use the provider that fits your environment: Claude API (SaaS), Amazon Bedrock (IAM-based access, cross-region options), or Google Vertex AI (GCP-native, Workload Identity Federation).
3. **Sandboxed execution** — each interaction runs in a container with strict network and filesystem rules. Claude Code enforces workspace-scoped permissions to constrain writes. Every change flows through an MR so reviewers see the diff and approvals still apply.

Pick regional endpoints to reduce latency and meet data-sovereignty requirements while using existing cloud agreements.

## What can Claude do?

- Create and update MRs from issue descriptions or comments
- Analyze performance regressions and propose optimizations
- Implement features directly in a branch, then open an MR
- Fix bugs and regressions identified by tests or comments
- Respond to follow-up comments to iterate on requested changes

## Setup

### Quick setup

The fastest way to get started is to add a minimal job to `.gitlab-ci.yml` and set your API key as a masked variable.

1. **Add a masked CI/CD variable** — go to **Settings** → **CI/CD** → **Variables** and add `ANTHROPIC_API_KEY` (masked, protected as needed).
2. **Add a Claude job to `.gitlab-ci.yml`** (see the basic job below).

After adding the job and your `ANTHROPIC_API_KEY` variable, test by running the job manually from **CI/CD** → **Pipelines**, or trigger it from an MR to let Claude propose updates in a branch and open an MR if needed. To run on Amazon Bedrock or Google Vertex AI instead of the Claude API, see the provider section below for authentication and environment setup.

### Manual setup (recommended for production)

If you prefer a more controlled setup or need enterprise providers:

1. **Configure provider access** — **Claude API**: create and store `ANTHROPIC_API_KEY` as a masked CI/CD variable. **Amazon Bedrock**: configure GitLab → AWS OIDC and create an IAM role for Bedrock. **Google Vertex AI**: configure Workload Identity Federation for GitLab → GCP.
2. **Add project credentials for GitLab API operations** — use `CI_JOB_TOKEN` by default, or create a Project Access Token with `api` scope and store it as `GITLAB_ACCESS_TOKEN` (masked) if using a PAT.
3. **Add the Claude job to `.gitlab-ci.yml`** (see configuration examples).
4. **(Optional) Enable mention-driven triggers** — add a project webhook for "Comments (notes)" to your event listener (if you use one); have the listener call the pipeline trigger API with variables like `AI_FLOW_INPUT` and `AI_FLOW_CONTEXT` when a comment contains `@claude`.

## Example use cases

- **Turn issues into MRs** — in an issue comment, `@claude implement this feature based on the issue description`. Claude analyzes the issue and codebase, writes changes in a branch, and opens an MR for review.
- **Get implementation help** — in an MR discussion, `@claude suggest a concrete approach to cache the results of this API call`. Claude proposes changes, adds code with appropriate caching, and updates the MR.
- **Fix bugs quickly** — in an issue or MR comment, `@claude fix the TypeError in the user dashboard component`. Claude locates the bug, implements a fix, and updates the branch or opens a new MR.

## Configuration examples

### Basic `.gitlab-ci.yml` (Claude API)

The `claude` job uses the `node:24-alpine3.21` image, fetches the repo, installs the CLI in `before_script`, optionally starts a GitLab MCP server, then invokes `claude -p` with `--permission-mode acceptEdits` and an explicit `--allowedTools` allowlist. The `${AI_FLOW_INPUT:-...}` form lets a web/API trigger supply the prompt while keeping a default. Claude Code reads `ANTHROPIC_API_KEY` from the CI/CD variables.

```yaml theme={null}
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Summarize recent changes and suggest improvements'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  # Claude Code will use ANTHROPIC_API_KEY from CI/CD variables
```

### Amazon Bedrock job example (OIDC)

For enterprise environments you can run Claude entirely on your own cloud infrastructure with the same developer experience. The Bedrock path requires Amazon Bedrock enabled with model access, GitLab configured as an OIDC identity provider in AWS IAM, and an IAM role with least-privilege Bedrock-invoke permissions whose trust policy is restricted to your GitLab project and protected refs. Store `AWS_ROLE_TO_ASSUME` (role ARN) and `AWS_REGION` as CI/CD variables. The job exchanges the GitLab OIDC token (`CI_JOB_JWT_V2`) for temporary AWS credentials via `aws sts assume-role-with-web-identity` — no static keys.

```yaml theme={null}
claude-bedrock:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apk add --no-cache bash curl jq git python3 py3-pip
    - pip install --no-cache-dir awscli
    - curl -fsSL https://claude.ai/install.sh | bash
    # Exchange GitLab OIDC token for AWS credentials
    - export AWS_WEB_IDENTITY_TOKEN_FILE="${CI_JOB_JWT_FILE:-/tmp/oidc_token}"
    - if [ -n "${CI_JOB_JWT_V2}" ]; then printf "%s" "$CI_JOB_JWT_V2" > "$AWS_WEB_IDENTITY_TOKEN_FILE"; fi
    - >
      aws sts assume-role-with-web-identity
      --role-arn "$AWS_ROLE_TO_ASSUME"
      --role-session-name "gitlab-claude-$(date +%s)"
      --web-identity-token "file://$AWS_WEB_IDENTITY_TOKEN_FILE"
      --duration-seconds 3600 > /tmp/aws_creds.json
    - export AWS_ACCESS_KEY_ID="$(jq -r .Credentials.AccessKeyId /tmp/aws_creds.json)"
    - export AWS_SECRET_ACCESS_KEY="$(jq -r .Credentials.SecretAccessKey /tmp/aws_creds.json)"
    - export AWS_SESSION_TOKEN="$(jq -r .Credentials.SessionToken /tmp/aws_creds.json)"
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Implement the requested changes and open an MR'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    AWS_REGION: "us-west-2"
```

Model IDs for Bedrock include region-specific prefixes (for example, `us.anthropic.claude-sonnet-4-6`); pass the desired model via your job configuration or prompt if your workflow supports it.

### Google Vertex AI job example (Workload Identity Federation)

The Vertex path uses the `gcr.io/google.com/cloudsdktool/google-cloud-cli:slim` image and authenticates via Workload Identity Federation (no downloaded keys). Prerequisites: Vertex AI API enabled, WIF configured to trust GitLab OIDC, and a service account with Vertex AI permissions. Store `GCP_WORKLOAD_IDENTITY_PROVIDER` (full provider resource name), `GCP_SERVICE_ACCOUNT` (service account email), and `CLOUD_ML_REGION` (Vertex region, e.g. `us-east5`). The `before_script` runs `gcloud auth login --cred-file` with an `external_account` credential that impersonates the service account; the `claude -p` invocation matches the other jobs. With WIF you do not need to store service account keys — use repository-specific trust conditions and least-privilege service accounts. (Full provider account setup is out of scope here; see the source.)

## Best practices

- **CLAUDE.md configuration** — create a `CLAUDE.md` file at the repository root to define coding standards, review criteria, and project-specific rules; Claude reads it during runs and follows your conventions when proposing changes.
- **Security considerations** — never commit API keys or cloud credentials. Add `ANTHROPIC_API_KEY` as a masked variable (protect if needed), prefer provider-specific OIDC (no long-lived keys), limit job permissions and network egress, and review Claude's MRs like any other contributor.
- **Optimizing performance** — keep `CLAUDE.md` focused and concise, provide clear issue/MR descriptions to reduce iterations, configure sensible job timeouts to avoid runaway runs, and cache npm/package installs in runners where possible.
- **CI costs** — Claude runs on your GitLab runners (consuming compute minutes; see your plan's runner billing) and each interaction consumes tokens based on prompt/response size (see Anthropic pricing). To optimize, use specific `@claude` commands to reduce unnecessary turns, set appropriate `max_turns` and job timeout values, and limit concurrency to control parallel runs.

## Security and governance

- Each job runs in an isolated container with restricted network access.
- Claude's changes flow through MRs so reviewers see every diff.
- Branch protection and approval rules apply to AI-generated code.
- Claude Code uses workspace-scoped permissions to constrain writes.
- Costs remain under your control because you bring your own provider credentials.

## Troubleshooting

- **Claude not responding to `@claude` commands** — verify the pipeline is being triggered (manually, MR event, or via a note-event listener/webhook); ensure CI/CD variables (`ANTHROPIC_API_KEY` or cloud provider settings) are present and unmasked; check the comment contains `@claude` (not `/claude`) and that the mention trigger is configured.
- **Job can't write comments or open MRs** — ensure `CI_JOB_TOKEN` has sufficient permissions, or use a Project Access Token with `api` scope; check the `mcp__gitlab` tool is enabled in `--allowedTools`; confirm the job runs in the MR context or has enough context via `AI_FLOW_*` variables.
- **Authentication errors** — for the Claude API, confirm `ANTHROPIC_API_KEY` is valid and unexpired; for Bedrock/Vertex, verify OIDC/WIF configuration, role impersonation, and secret names, and confirm region and model availability.

## Advanced configuration

- **Common parameters and variables** — `prompt` / `prompt_file` (instructions inline via `-p` or via a file), `max_turns` (limit back-and-forth iterations), `timeout_minutes` (limit total execution time), `ANTHROPIC_API_KEY` (required for the Claude API, not used for Bedrock/Vertex), and provider-specific environment (`AWS_REGION`, project/region vars for Vertex). Exact flags may vary by version of `@anthropic-ai/claude-code`; run `claude --help` in your job to see supported options.
- **Customizing Claude's behavior** — two primary ways: (1) `CLAUDE.md` to define coding standards, security requirements, and project conventions that Claude reads during runs; (2) custom prompts passed via `prompt`/`prompt_file` in the job, using different prompts for different jobs (e.g. review, implement, refactor).

**Source**: https://code.claude.com/docs/en/gitlab-ci-cd
**Last Updated**: 2026-06-13
**Status**: Active
