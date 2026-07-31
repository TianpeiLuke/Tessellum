---
title: Sub-Plan B13B — Claude Code Docs: CI/CD & Code Review
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["github-actions", "github-enterprise-server", "gitlab-ci-cd", "code-review", "ultraplan", "ultrareview"]
---

# Sub-Plan B13B: CI/CD & Code Review

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / 8-GATE / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 6 pages that document how Claude Code runs inside continuous-integration and code-review pipelines:
the GitHub Actions integration, the self-hosted GitHub Enterprise Server (GHES) connection, the GitLab
CI/CD integration, the managed Code Review service, and the two cloud research-preview commands
`ultraplan` (cloud planning) and `ultrareview` / `/code-review ultra` (cloud multi-agent review). P2
(Phase B) — these features are built on the P1 cores (subagents, MCP, sandboxing, permissions, cloud
sessions) which are linked, never re-defined here.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 6 pages, 12,807 measured words. **Planned: 9 notes.**

## Content Strategy

- **Prioritize**: the operator-facing procedures (how to wire `@claude` into CI, how to enable/customize
  Code Review, how to launch ultraplan/ultrareview) — these are the high-operational-relevance content.
- **Group**: keep each integration surface (GitHub Actions / GHES / GitLab) as its own procedure note;
  split `github-actions` because its Bedrock/Vertex enterprise section is a distinct multi-step procedure;
  split `code-review` into the reviewer-mechanics concept, the `CLAUDE.md`/`REVIEW.md` customization
  procedure, and the local `/code-review` command — three different BBs and audiences.
- **Skip / link-out (own other sub-plans)**: install steps → setup B17; cloud-session/diff/teleport
  internals → B12B (claude-code-on-the-web, remote-control); plan mode → B05A (permission-modes);
  Bedrock/Vertex provider setup detail → B14A (cloud model providers); analytics dashboards → B15B;
  Zero Data Retention → B16; managed/strictKnownMarketplaces settings → B03A; plugin marketplaces → B09B.
  These are referenced via links, never duplicated.
- **Terms**: no new `term_dictionary` captures — CI/CD, code-review, multi-agent, sandbox, etc. are
  existing term notes (link) or owned by their home sub-plan (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 6 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| github-actions | /github-actions | 3,285 | 8 | 12 | 19 | procedure |
| github-enterprise-server | /github-enterprise-server | 1,434 | 6 | 7 | 9 | procedure |
| gitlab-ci-cd | /gitlab-ci-cd | 2,374 | 7 | 11 | 17 | procedure |
| code-review | /code-review | 3,484 | 2 | 13 | 9 | concept/procedure |
| ultraplan | /ultraplan | 936 | 1 | 4 | 2 | procedure |
| ultrareview | /ultrareview | 1,294 | 3 | 6 | 0 | concept |

> **H2 lists (document order):**
> - **github-actions**: Why use Claude Code GitHub Actions? · What can Claude do? (H3 Claude Code Action) · Setup · Quick setup · Manual setup · Upgrading from Beta (H3 Essential changes, Breaking Changes Reference, Before and After Example) · Example use cases (H3 Basic workflow, Using skills, Custom automation with prompts, Common use cases) · Best practices (H3 CLAUDE.md configuration, Security considerations, Optimizing performance, CI costs) · Configuration examples · Using with Amazon Bedrock & Google Vertex AI (H3 Prerequisites + Steps) · Troubleshooting (H3 ×3) · Advanced configuration (H3 Action parameters, Alternative integration methods, Customizing Claude's behavior)
> - **github-enterprise-server**: What works with GitHub Enterprise Server · Admin setup (H3 GitHub App permissions, Manual setup, Network requirements) · Developer workflow (H3 Teleport sessions to your terminal) · Plugin marketplaces on GHES (H3 Add a GHES marketplace, Allowlist GHES marketplaces in managed settings) · Limitations · Troubleshooting (H3 ×3) · Related resources
> - **gitlab-ci-cd**: Why use Claude Code with GitLab? · How it works · What can Claude do? · Setup (H3 Quick setup, Manual setup) · Example use cases (H3 Turn issues into MRs, Get implementation help, Fix bugs quickly) · Using with Amazon Bedrock & Google Vertex AI · Configuration examples (H3 Basic, Bedrock job, Vertex job) · Best practices (H3 ×4) · Security and governance · Troubleshooting (H3 ×3) · Advanced configuration (H3 ×2)
> - **code-review**: How reviews work (H3 Severity levels, Rate and reply to findings, Check run output, What Code Review checks) · Set up Code Review · Manually trigger reviews · Customize reviews (H3 CLAUDE.md, REVIEW.md) · View usage · Pricing · Troubleshooting (H3 ×3) · Review a diff locally · Related resources
> - **ultraplan**: Launch ultraplan from the CLI · Review and revise the plan in your browser · Choose where to execute (H3 Execute on the web, Send the plan back to your terminal) · Related resources
> - **ultrareview**: Run ultrareview from the CLI · Pricing and free runs · Track a running review · Run ultrareview non-interactively · How ultrareview compares to /review · Related resources

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **9 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_github_actions.md` | procedure | github-actions: Why/What, Setup (Quick+Manual), Example use cases, Best practices, Configuration examples, Advanced config | 700 | Wire Claude into GitHub Actions via `/install-github-app`; `@claude` mention trigger; `claude-code-action@v1` workflow; `prompt`/`claude_args`/skills inputs; CLAUDE.md + security/cost best practices. Bedrock/Vertex → note 2. |
| 2 | `cc_github_actions_cloud_providers.md` | procedure | github-actions: Using with Amazon Bedrock & Google Vertex AI (Prerequisites + 4 Steps + 2 workflow accordions) | 650 | Run the Action on your own Bedrock/Vertex infra: custom GitHub App, OIDC/Workload-Identity-Federation auth (no static keys), required secrets, complete Bedrock + Vertex workflow YAML. Provider account setup → B14A. |
| 3 | `cc_gitlab_ci_cd.md` | procedure | gitlab-ci-cd: Why/How-it-works/What, Setup, Example use cases, Configuration examples, Best practices, Security & governance, Advanced config | 750 | `@claude` in GitLab via a `.gitlab-ci.yml` job: masked `ANTHROPIC_API_KEY`, `node:24-alpine` image, `claude -p` with `--permission-mode acceptEdits` + `--allowedTools`, `AI_FLOW_*` vars, MR flow, Bedrock/Vertex OIDC jobs. |
| 4 | `cc_github_enterprise_server.md` | procedure | github-enterprise-server: feature table, Admin setup (App permissions, Manual, Network), Developer workflow, Plugin marketplaces on GHES, Limitations, Troubleshooting | 700 | Connect Claude Code to self-hosted GHES: admin one-time GitHub App manifest setup, auto host-detection, `claude --remote`/`--teleport`, full-git-URL marketplaces + `hostPattern` allowlist, feature-support/limitations table. |
| 5 | `cc_code_review.md` | concept | code-review: intro, How reviews work (Severity, Rate/reply, Check run output, What it checks), Pricing | 650 | The managed multi-agent PR reviewer: parallel specialized agents + verification step filter false positives; severity markers (Important/Nit/Pre-existing); inline comments + neutral check run + machine-readable severity counts; per-review cost. |
| 6 | `cc_code_review_setup_and_customization.md` | procedure | code-review: Set up Code Review, Manually trigger reviews, Customize reviews (CLAUDE.md, REVIEW.md + example), View usage, Troubleshooting | 750 | Admin enables per-repo + sets Review Behavior (once / every-push / manual); `@claude review` / `@claude review once` triggers; tune flags via `CLAUDE.md` (nits) and `REVIEW.md` (highest-priority severity/skip/verification rules) with example; retrigger/spend-cap troubleshooting. |
| 7 | `cc_code_review_local_command.md` | procedure | code-review: Review a diff locally (`/code-review` command, scope, effort, targets, `--comment`/`--fix`, `/simplify` history) | 400 | The local `/code-review` slash command: reviews branch-ahead diff + working tree without the GitHub App; effort levels, target args (file/PR/branch/ref-range), `--comment`/`--fix`, `ultra` escalation, `/simplify` rename history. |
| 8 | `cc_ultraplan.md` | procedure | ultraplan: intro, Launch from CLI, Review/revise in browser, Choose where to execute (web / teleport back) | 500 | Hand a planning task to a cloud plan-mode session: launch via `/ultraplan`, keyword, or local-plan refine; status indicators + `/tasks`; browser inline-comment/emoji/outline review; execute on web (→ PR) or teleport back to terminal. Not on Bedrock/Vertex/Foundry. |
| 9 | `cc_ultrareview.md` | concept | ultrareview: intro, Run from CLI (PR mode), Pricing/free runs, Track, Non-interactive subcommand, How it compares to /review | 600 | Deep cloud multi-agent code review via `/code-review ultra`: reviewer fleet in a remote sandbox with independent reproduction/verification; branch-vs-default or PR scope; free runs then usage credits; `/tasks` tracking; `claude ultrareview` CI subcommand (exit codes, `--json`/`--timeout`); vs local `/review`. |

**Estimate: 9 notes** — procedure ×7 (notes 1,2,3,4,6,7,8), concept ×2 (notes 5, 9). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 6 (12,807 words). New `cc_` notes: 9. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~5,700 (avg ~630/note). Code blocks: per-note ≤6 (verbatim YAML/CLI snippets from source; densest is note 3 GitLab with 4 — within cap).
- **Building Block Distribution**: procedure ×7 (notes 1,2,3,4,6,7,8) · concept ×2 (notes 5, 9). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_github_actions` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding tool itself; relevance: this note documents how that tool is embedded as a GitHub Action, so the product term is the host being integrated.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — what-it-is: continuous integration / continuous delivery automation of build-test-deploy; relevance: GitHub Actions IS a CI/CD platform and this note wires Claude into that CI/CD pipeline (`@claude` on PRs, scheduled jobs).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that plan, edit across files, run commands, and open PRs autonomously; relevance: the Action turns an `@claude` mention into an autonomous run that creates a complete PR with all necessary changes.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: packaged markdown workflows invocable via `/<name>`; relevance: the note's "Using skills" section passes a `/skill-name` (or plugin-namespaced) invocation through the Action's `prompt` input.
- [MCP](../../term_dictionary/term_mcp.md) — what-it-is: Model Context Protocol for connecting external tools/data; relevance: the Action's `claude_args: --mcp-config` and "MCP Configuration" alternative dynamically load MCP servers into the CI run.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — what-it-is: persisted project instructions/preferences Claude reads each run; relevance: the note's central best practice is a repo-root `CLAUDE.md` defining standards the Action follows when creating PRs.
- [DevOps](../../term_dictionary/term_devops.md) — what-it-is: the practice of unifying dev and ops via automation/runners/secrets; relevance: the note's setup (GitHub-hosted runners, repository secrets, workflow permissions, CI costs) is squarely DevOps tooling configuration.

### 2. `cc_github_actions_cloud_providers` (7 term notes)
- [CI/CD](../../term_dictionary/term_ci_cd.md) — what-it-is: pipeline automation on hosted runners; relevance: this note configures the same GitHub Actions CI/CD job to run against enterprise model backends instead of the direct Claude API.
- [IAM](../../term_dictionary/term_iam.md) — what-it-is: identity & access management (roles, policies, trust relationships); relevance: the Bedrock path requires an IAM role with `AmazonBedrockFullAccess` and a repository-scoped trust policy that the Action assumes via OIDC.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — what-it-is: the scope of damage a compromised credential/identity can cause; relevance: the note's security guidance (repository-specific attribute conditions, dedicated per-repo service accounts, least privilege) is explicitly about minimizing blast radius of the CI identity.
- [Deny First](../../term_dictionary/term_deny_first.md) — what-it-is: a least-privilege posture granting only the minimum required access; relevance: the note repeatedly mandates granting only minimum required permissions and a single `Vertex AI User` role — the deny-first principle applied to cloud auth.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding tool; relevance: this note runs Claude Code's Action against Bedrock/Vertex (`use_bedrock`/`use_vertex`, region-prefixed model IDs), so the product term anchors what is being hosted.
- [Sandbox](../../term_dictionary/term_sandbox.md) — what-it-is: an isolated execution environment with constrained credentials/network; relevance: GitHub-hosted runners executing the Action with temporary OIDC credentials are the isolated sandbox in which the enterprise job runs.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that autonomously implement and open PRs; relevance: the Bedrock/Vertex workflows give the same autonomous `@claude` PR-creation behavior while keeping data residency/billing under enterprise control.

### 3. `cc_gitlab_ci_cd` (7 term notes)
- [CI/CD](../../term_dictionary/term_ci_cd.md) — what-it-is: pipeline automation (here `.gitlab-ci.yml` stages/jobs/runners); relevance: this note adds a `claude` job to a GitLab CI/CD pipeline triggered by MR events / web triggers — a direct CI/CD integration.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding CLI; relevance: the job installs and invokes the Claude Code CLI (`claude -p ... --permission-mode acceptEdits --allowedTools`) inside the runner.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive permission modes governing how much Claude can do without asking; relevance: the job runs with `--permission-mode acceptEdits` and an explicit `--allowedTools` allowlist — the graduated-trust permission posture applied to non-interactive CI.
- [MCP](../../term_dictionary/term_mcp.md) — what-it-is: protocol for connecting external tools; relevance: the job starts a `gitlab-mcp-server` and enables the `mcp__gitlab` tool so Claude can post comments and open MRs.
- [Sandbox](../../term_dictionary/term_sandbox.md) — what-it-is: an isolated container with restricted network/filesystem; relevance: the note states each interaction runs in a sandboxed container with strict network/filesystem rules and workspace-scoped write permissions.
- [IAM](../../term_dictionary/term_iam.md) — what-it-is: identity & access management for cloud roles; relevance: the Bedrock job exchanges a GitLab OIDC token for an assumed IAM role (`AWS_ROLE_TO_ASSUME`) with least-privilege Bedrock-invoke permissions.
- [DevOps](../../term_dictionary/term_devops.md) — what-it-is: automation of build/test/deploy with runners, masked variables, branch protection; relevance: the note's setup (masked CI/CD variables, runner billing, branch protection + approvals on AI MRs) is core GitLab DevOps configuration.

### 4. `cc_github_enterprise_server` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding tool; relevance: this note connects Claude Code to a self-hosted GHES instance so its web sessions / reviews / plugins work against internal repos.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — what-it-is: continuous-integration pipeline tooling; relevance: the feature table notes GitHub Actions on GHES requires manual workflow setup, and Checks/Actions permissions feed auto-fix — GHES CI/CD behavior differences.
- [MCP](../../term_dictionary/term_mcp.md) — what-it-is: Model Context Protocol server interface; relevance: the note's key limitation is that the GitHub MCP server does NOT work on GHES, with `gh` CLI given as the workaround.
- [IAM](../../term_dictionary/term_iam.md) — what-it-is: identity & access management (apps, OAuth, scoped permissions); relevance: admin setup creates a GitHub App with a specific permission/webhook-event matrix (Contents/PRs/Issues/Checks/Actions/Hooks/Metadata) — GHES access management.
- [Sandbox](../../term_dictionary/term_sandbox.md) — what-it-is: isolated cloud execution; relevance: `claude --remote` sessions run on Anthropic cloud infrastructure that clones the GHES repo and pushes a branch — the remote sandbox model GHES routes into.
- [Deny First](../../term_dictionary/term_deny_first.md) — what-it-is: restrict-by-default policy posture; relevance: the `strictKnownMarketplaces` `hostPattern` managed setting restricts which plugin marketplaces developers may add — a deny-by-default allowlist for the GHES host.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — what-it-is: scope of exposure of a connected system; relevance: the note's network requirements (firewall allowlist of Anthropic API IPs, self-signed CA handling, install-on-a-subset-of-repos) bound which internal systems the integration can reach.

### 5. `cc_code_review` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding tool; relevance: Code Review is Claude Code's managed PR-review service, so the product term anchors the reviewer this note describes.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — what-it-is: multiple coordinating LLM agents working on subtasks; relevance: the note's core mechanism is "a fleet of specialized agents examine the code changes," each looking for a different class of issue — a multi-agent system.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a Claude Code agent spawned with isolated context for a focused task; relevance: the parallel reviewer agents are subagents, each scoped to one issue class then their findings deduplicated and ranked.
- [Agentic Evaluation](../../term_dictionary/term_agentic_evaluation.md) — what-it-is: using agents to evaluate/verify outputs (LLM-as-judge style verification); relevance: the note's verification step checks each candidate finding against actual code behavior to filter false positives — an agentic verification/evaluation pass.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — what-it-is: coordinating multiple agents (dispatch, dedup, aggregation) into one result; relevance: the note describes parallel agents → verification → dedup → severity-ranked aggregation into one review — an orchestration pipeline.
- [Precision](../../term_dictionary/term_precision.md) — what-it-is: fraction of flagged items that are true positives; relevance: the verification step exists to raise precision (filter false positives) and findings carry severity so reviewers act on true bugs — the note's quality lens.
- [Continuous Integration / CI/CD](../../term_dictionary/term_ci_cd.md) — what-it-is: automated checks that run on PRs/pushes; relevance: Code Review posts a neutral GitHub check run alongside CI checks and exposes machine-readable severity counts a CI workflow can gate on.

### 6. `cc_code_review_setup_and_customization` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding tool; relevance: this note configures Claude Code's Code Review service per repo and customizes its behavior, so the product term is the system being tuned.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — what-it-is: the `CLAUDE.md` project-instruction mechanism Claude reads across tasks; relevance: the note shows `CLAUDE.md` violations become nit-level review findings (and outdated docs get flagged bidirectionally) — memory files shaping review.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — what-it-is: multiple coordinating review agents; relevance: `REVIEW.md` is injected as the highest-priority instruction block into the system prompt of *every agent* in the review pipeline — a per-agent customization knob.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — what-it-is: pipeline automation/triggers; relevance: the per-repo Review Behavior (once-after-PR / after-every-push / manual) and `@claude review` triggers are CI-style event configuration; skip rules defer to "anything CI already enforces."
- [Precision](../../term_dictionary/term_precision.md) — what-it-is: true-positive rate of findings; relevance: the note's tuning patterns (verification-bar evidence requirements, nit caps, severity recalibration) are precision/noise controls for the reviewer.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressively scoped permissions/severity; relevance: `REVIEW.md` lets a repo redefine what 🔴 Important means and set higher bars per path (`scripts/`: only near-certain and severe) — graduated severity thresholds.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — what-it-is: coordinating an agent pipeline's behavior end-to-end; relevance: re-review-convergence and summary-shape rules in `REVIEW.md` steer the whole review-pipeline orchestration across successive runs.

### 7. `cc_code_review_local_command` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding tool / session; relevance: `/code-review` is a slash command run inside any Claude Code session, so the product term anchors where the local review runs.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that not only find but apply code changes; relevance: the command's `--fix` flag applies the review findings directly to the working tree — autonomous remediation, not just reporting.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — what-it-is: pipeline/PR-diff review automation; relevance: the command's targets include a PR number and `main...my-feature` ref ranges (the committed diff a PR would contain), and `--comment` posts inline PR comments — pre-merge CI-adjacent review.
- [Agentic Evaluation](../../term_dictionary/term_agentic_evaluation.md) — what-it-is: agent-driven assessment of code quality; relevance: the command reports correctness bugs plus reuse/simplification/efficiency cleanups at a chosen effort level — an agentic evaluation of the diff.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — what-it-is: a fleet of cloud reviewer agents; relevance: `/code-review ultra --fix` escalates the local command to the cloud multi-agent ultrareview, linking the local and fleet paths.
- [Precision](../../term_dictionary/term_precision.md) — what-it-is: confidence/true-positive trade-off of findings; relevance: the note documents that lower effort levels return fewer high-confidence findings while `high`→`max` broaden coverage with more uncertain ones — an explicit precision/recall dial.

### 8. `cc_ultraplan` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding tool spanning CLI and web; relevance: ultraplan hands a planning task from the local Claude Code CLI to a Claude Code on the web session, so the product term anchors both ends.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that draft and execute multi-step work; relevance: ultraplan drafts the plan remotely and can autonomously implement it on the web (opening a PR) or teleport it back for local execution.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what-it-is: deliberately structuring an agent's working context; relevance: the teleport-back options (inject the plan into the current conversation / start a fresh session with only the plan as context / save to file) are explicit context-management choices.
- [Sandbox](../../term_dictionary/term_sandbox.md) — what-it-is: an isolated cloud execution environment; relevance: ultraplan runs in your account's default cloud environment (auto-created on first launch) on Anthropic cloud infrastructure — the cloud sandbox the plan is drafted in.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — what-it-is: saving recoverable states so work can be resumed; relevance: the note's "Cancel: save the plan to a file" and the printed `claude --resume` command are checkpoint/resume affordances around the planning artifact.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — what-it-is: cloud agents working while you continue locally; relevance: ultraplan's hands-off drafting keeps your terminal free while a cloud agent researches the codebase and drafts the plan in parallel — concurrent agents across surfaces.

### 9. `cc_ultrareview` (6 term notes)
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — what-it-is: a fleet of coordinating LLM agents; relevance: ultrareview launches "a fleet of reviewer agents" in a remote sandbox that explore the change in parallel — its defining multi-agent design.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: individually scoped Claude Code agents; relevance: the many reviewer agents each independently reproduce/verify a finding before it is reported — subagents with isolated verification scope.
- [Agentic Evaluation](../../term_dictionary/term_agentic_evaluation.md) — what-it-is: agent-based verification of outputs; relevance: ultrareview's headline property is that every reported finding is independently reproduced and verified — agentic evaluation to raise signal over a single-pass review.
- [Sandbox](../../term_dictionary/term_sandbox.md) — what-it-is: an isolated remote execution environment; relevance: the review runs entirely in a remote sandbox (bundled working tree or cloned PR) so no local resources are used while it runs.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding tool/CLI; relevance: `/code-review ultra` and the `claude ultrareview` subcommand are Claude Code CLI invocations that bill against usage credits and run on Claude Code on the web.
- [Precision](../../term_dictionary/term_precision.md) — what-it-is: true-positive rate / signal of findings; relevance: the note frames ultrareview as "higher signal" — independent verification focuses results on real bugs rather than style, the precision argument vs local `/review`.

## Section Coverage Map

```
github-actions.md
├── Why use Claude Code GitHub Actions? ── → note 1 (cc_github_actions)
├── What can Claude do? (Claude Code Action) → note 1
├── Setup / Quick setup / Manual setup ──── → note 1
│   └── install-github-app ──────────────── → note 1 (full install detail → setup B17)
├── Upgrading from Beta (3 H3) ──────────── → note 1 (migration table summarized)
├── Example use cases (4 H3) ────────────── → note 1
│   └── Using skills ────────────────────── → note 1 (links term_skills)
├── Best practices (4 H3) ───────────────── → note 1 (CLAUDE.md, security, perf, CI costs)
├── Configuration examples ──────────────── → note 1
├── Using with Amazon Bedrock & Vertex AI ─ → note 2 (cc_github_actions_cloud_providers)
│   └── Prerequisites + 4 Steps + 2 wf ──── → note 2 (provider account setup → B14A)
├── Troubleshooting (3 H3) ──────────────── → note 1
└── Advanced configuration (3 H3) ───────── → note 1 (action params, alt methods, customizing)
github-enterprise-server.md
├── What works with GHES (feature table) ── → note 4 (cc_github_enterprise_server)
├── Admin setup (App perms, Manual, Network) → note 4
├── Developer workflow ──────────────────── → note 4
│   └── Teleport sessions to terminal ───── → note 4 (teleport internals → B12B)
├── Plugin marketplaces on GHES ─────────── → note 4 (full marketplace guide → B09B)
│   └── Allowlist via managed settings ──── → note 4 (strictKnownMarketplaces schema → B03A)
├── Limitations ─────────────────────────── → note 4
├── Troubleshooting (3 H3) ──────────────── → note 4
└── Related resources ───────────────────── → note 4 (links; web session → B12B)
gitlab-ci-cd.md
├── Why use Claude Code with GitLab? ────── → note 3 (cc_gitlab_ci_cd)
├── How it works ────────────────────────── → note 3
├── What can Claude do? ─────────────────── → note 3
├── Setup (Quick, Manual) ───────────────── → note 3
├── Example use cases (3 H3) ────────────── → note 3
├── Using with Amazon Bedrock & Vertex AI ─ → note 3 (provider account setup → B14A)
├── Configuration examples (3 H3) ───────── → note 3 (Basic, Bedrock, Vertex jobs)
├── Best practices (4 H3) ───────────────── → note 3
├── Security and governance ─────────────── → note 3
├── Troubleshooting (3 H3) ──────────────── → note 3
└── Advanced configuration (2 H3) ───────── → note 3
code-review.md
├── intro + page-covers list ────────────── → note 5 (cc_code_review)
├── How reviews work ────────────────────── → note 5
│   ├── Severity levels ──────────────────── → note 5
│   ├── Rate and reply to findings ───────── → note 5
│   ├── Check run output ─────────────────── → note 5
│   └── What Code Review checks ──────────── → note 5
├── Set up Code Review ──────────────────── → note 6 (cc_code_review_setup_and_customization)
├── Manually trigger reviews ────────────── → note 6
├── Customize reviews (CLAUDE.md, REVIEW.md) → note 6
├── View usage ──────────────────────────── → note 6 (full dashboard → B15B analytics)
├── Pricing ─────────────────────────────── → note 5 (cost mechanics; ZDR exclusion → B16)
├── Troubleshooting (3 H3) ──────────────── → note 6
├── Review a diff locally (/code-review) ─── → note 7 (cc_code_review_local_command)
└── Related resources ───────────────────── → notes 5/6/7 (links; Commands → B03B)
ultraplan.md
├── intro ───────────────────────────────── → note 8 (cc_ultraplan)
├── Launch ultraplan from the CLI ───────── → note 8
├── Review and revise the plan in browser ─ → note 8
├── Choose where to execute (web / teleport) → note 8 (plan mode → B05A; web diff/PR → B12B)
└── Related resources ───────────────────── → note 8 (links)
ultrareview.md
├── intro ───────────────────────────────── → note 9 (cc_ultrareview)
├── Run ultrareview from the CLI (PR mode) ─ → note 9
├── Pricing and free runs ───────────────── → note 9
├── Track a running review ───────────────── → note 9
├── Run ultrareview non-interactively ────── → note 9
├── How ultrareview compares to /review ──── → note 9
└── Related resources ───────────────────── → note 9 (links; costs → B02A/B16; web → B12B)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| github-actions (3.3Kw, 12 H2) | notes 1 + 2 | the core Action setup/usage (procedure) vs the Bedrock/Vertex enterprise-auth path (distinct multi-step OIDC/WIF procedure with its own prerequisites + 2 full workflow YAML accordions) are different audiences; keeping them together would push note 1 past the word/code caps. |
| code-review (3.5Kw, 13 H2) | notes 5, 6, 7 | reviewer mechanics (concept: how the fleet works, severity, check-run) vs admin enable + `CLAUDE.md`/`REVIEW.md` customization + triggers/troubleshooting (procedure) vs the local `/code-review` slash command (procedure) differ in BB and audience; one note would exceed 2,500w. |

GHES (1.4Kw), gitlab-ci-cd (2.4Kw), ultraplan (0.9Kw), ultrareview (1.3Kw) each stay one note — all under the word cap with one dominant BB.

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_github_actions | procedure | 700 | 4 | ✅ |
| 2 | cc_github_actions_cloud_providers | procedure | 650 | 3 | ✅ |
| 3 | cc_gitlab_ci_cd | procedure | 750 | 4 | ✅ |
| 4 | cc_github_enterprise_server | procedure | 700 | 4 | ✅ |
| 5 | cc_code_review | concept | 650 | 2 | ✅ |
| 6 | cc_code_review_setup_and_customization | procedure | 750 | 1 | ✅ |
| 7 | cc_code_review_local_command | procedure | 400 | 0 | ✅ |
| 8 | cc_ultraplan | procedure | 500 | 1 | ✅ |
| 9 | cc_ultrareview | concept | 600 | 3 | ✅ |

No note approaches the caps (≤400 lines / ≤2,500 words / ≤6 code blocks). Source is prose+YAML/CLI;
each note selects ≤4 verbatim snippets (not every source fence) so no note is code-heavy. No
over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_github_actions cc_github_actions_cloud_providers cc_gitlab_ci_cd cc_github_enterprise_server cc_code_review cc_code_review_setup_and_customization cc_code_review_local_command cc_ultraplan cc_ultrareview"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] && echo "DENSITY WARNING: $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$CC"
# G5 ghost: verify every internal .md link target exists in the DB
for n in $NOTES; do f="$CC/$n.md"
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/.*\(([^)]+)\)/\1/' | while read l; do
    r=$(cd "$(dirname "$f")" && realpath -q -m "$l"); id=${r#*/the vault/}
    sqlite3 "$(python3 -c 'import sys;sys.path.insert(0,"scripts");from config import DB_PATH_STR;print(DB_PATH_STR)')" \
      "SELECT 1 FROM notes WHERE note_id='$id'" | grep -q 1 || echo "GHOST $n -> $l"
  done; done
```

## Per-Phase Validation Gate (G1–G8) — inherited from master

Single phase (9 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 9 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 9 notes RECEIVES ≥1 inbound link from an existing vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability(inbound in-degree ≥1) | same as G7, re-verified after broken-link fix: confirm in-degree ≥1 holds post-reindex | DB in-degree query (final) |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`
(created as a pre-step before the first sub-plan executes). This sub-plan **contributes its 9 rows** under a
"CI/CD & Code Review" cluster + increments the BB-distribution counts (procedure ×7, concept ×2). The parent
hub `entry_gen_ai_dev.md` (verified present) receives the back-link row for the new entry point at master finalization.

## Undigested Terms Plan (Step 4e)

b13b creates **no new `term_dictionary` notes** — every vocabulary term these 6 pages use is either an
existing substantive term note (link) or owned by its home sub-plan (Pattern B). Dedup performed across
**both** `term_dictionary/` AND `resources/documentation/` (no existing `cc_github*`, `cc_gitlab*`,
`cc_code_review*`, `cc_ultra*` notes — folder is empty pre-execution).

| Term surfaced in pages | Disposition |
|---|---|
| GitHub Actions / Action / runner / workflow | note 1/2 `cc_github_actions*` (doc concept); CI/CD → link `term_ci_cd` (exists) |
| GitLab CI/CD / `.gitlab-ci.yml` / MR | note 3 `cc_gitlab_ci_cd` (doc concept); CI/CD → link `term_ci_cd` |
| GitHub Enterprise Server (GHES) | note 4 `cc_github_enterprise_server` (doc concept) |
| Code Review (managed service) | notes 5/6/7 `cc_code_review*` (doc concept) |
| ultraplan / ultrareview / `/code-review ultra` | notes 8/9 `cc_ultraplan`, `cc_ultrareview` (doc concept) |
| `REVIEW.md` / `CLAUDE.md` | note 6 (doc concept); memory file → link `term_agentic_memory` (exists), full CLAUDE.md → B02B |
| Multi-agent / agent fleet / verification step | link `term_multi_agent`, `term_subagent`, `term_agentic_evaluation`, `term_agent_orchestration` (all exist) |
| Sandbox / sandboxed execution | link `term_sandbox` (exists); sandboxing page → B05B |
| Permission mode / `acceptEdits` / allowedTools | link `term_graduated_trust` (exists); owned by B05A |
| OIDC / Workload Identity Federation / IAM role | link `term_iam`, `term_blast_radius`, `term_deny_first` (all exist); provider setup → B14A |
| Plan mode | link to B05A `permission-modes` (home sub-plan); referenced in note 8 |
| Teleport / Remote Control / web session / cloud environment | owned by B12B (web & remote surfaces) — linked, not duplicated |
| Plugin marketplace / `hostPattern` / strictKnownMarketplaces | owned by B09B / B03A — linked, not duplicated |
| Usage credits / pricing / Zero Data Retention / analytics | owned by B02A (costs) / B16 (ZDR) / B15B (analytics) — linked |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 6 pages scanning emphasis/tables/captions/code
for newly-surfaced terms. No non-glossary term surfaced that lacks an existing note OR a home sub-plan.
`REVIEW.md` is a CC-specific doc concept (digested inline in note 6, not a `term_dictionary` term — same
treatment as `CLAUDE.md`/glossary per Pattern B). **0 new b13b `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — b13b authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the page concepts duplicate existing notes?) was
`term_agent_orchestration`, `term_sandbox`, `term_graduated_trust`, `term_iam`, `term_blast_radius`,
`term_deny_first`, `term_agentic_evaluation`, `term_precision`, `term_agentic_memory`,
`term_autonomous_coding_agents`, `term_claude_code` all exist → linked, not recreated.

## Term-Note Authoring Requirements

**N/A for b13b** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim from source (YAML workflow files, `.gitlab-ci.yml`, CLI commands, `REVIEW.md`
  example, `gh api` snippet) — select ≤4 per note, do not transcribe every fence. One BB per note.
  Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; commit + push after the phase
  (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_ci_cd.md` | notes 1, 3 | CI/CD term → Claude Code's GitHub Actions + GitLab CI/CD integrations |
| `term_dictionary/term_claude_code.md` | notes 1, 5, 8, 9 | product term → CC's CI integration, Code Review service, ultraplan, ultrareview |
| `term_dictionary/term_multi_agent.md` | notes 5, 9 | multi-agent term → Code Review fleet + ultrareview fleet |
| `term_dictionary/term_agentic_evaluation.md` | notes 5, 9 | agentic-evaluation term → Code Review/ultrareview verification step |
| `term_dictionary/term_iam.md` | note 2 | IAM term → GitHub Actions Bedrock/Vertex OIDC role setup |
| `tools/tool_autocr_reviewer.md` | note 5 | existing automated-code-review tool note → CC Code Review (comparable managed reviewer) |
| `how_to/howto_autonomous_maintenance_claude.md` | note 7 | autonomous-maintenance how-to → local `/code-review --fix` command |

## Follow-up Recommendations

- After the 9 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 9 rows for `entry_claude_code_docs.md` (CI/CD & Code Review cluster); `/tessellum-check-broken-links`; verify in-degree ≥1 for all 9 (G7/G8).
- Cross-link siblings: note 5↔6↔7 (Code Review family), note 7↔9 (`/code-review` → ultra escalation), note 8↔9 (ultraplan/ultrareview pair), notes 1↔3↔4 (CI integrations), note 2↔note "B14A cloud providers" once that sub-plan executes.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | DONE 2026-06-13 — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | READY (9/9) — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B13B, 2026-06-13)

- **Source re-read (Step 2)**: all 6 pages re-read fully from `inbox/claude_code_docs/`; measured words
  (github-actions 3,285 · github-enterprise-server 1,434 · gitlab-ci-cd 2,374 · code-review 3,484 ·
  ultraplan 936 · ultrareview 1,294 = 12,807) match the master's figure exactly. No >1.5× under-estimate;
  the two largest pages (github-actions, code-review) were split as documented.
- **Notes**: 9 (procedure 7, concept 2) — matches master estimate. Two splits documented (github-actions →
  1+2; code-review → 5+6+7); the other 4 pages stay one note each.
- **Per-Note Related Notes Mapping (Step 8)**: authored to the **≥6 relevancy-selected term-note** standard
  — 6–7 term notes per note (15 distinct `term_dictionary/` terms), each with a what-it-is + per-link
  relpaths `../../term_dictionary/`. Sibling `cc_*` cross-links recorded in Follow-up.
  multi-agent, plan-mode/cloud, sandbox/OIDC) across `term_dictionary/` AND `documentation/`; the
  `claude_code/` folder is empty pre-execution so no `cc_` collisions. All matched terms are existing →
  linked, not recreated. No DUP-merge verdicts (no notes deleted).
- **Step 2d new-term scan**: 0 new non-glossary terms requiring capture; `REVIEW.md` digested inline as a
  doc concept (note 6). **0 new B13B term captures.**
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G5/G7/G8 verification rows, Inlinks table.
- **28-item checklist**: PASS (term-note items N/A — B13B authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented and reviewed; set to `ready` after the 9/9 review sign-off below.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability (inbound in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B13B contributes 9 rows; parent hub `entry_gen_ai_dev.md` verified present for the back-link. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 9 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | Inherits master Format Definition verbatim — YAML field order, `## Overview` opener, source-mirrored H2s, `## Related Notes` indexed links, `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | All 9 notes 400–750w, ≤4 code — none borderline. The two largest source pages were proactively split (1+2, 5+6+7). |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` re-measured all 6: 3,285 / 1,434 / 2,374 / 3,484 / 936 / 1,294 = 12,807 = master figure (±0%). |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B13B authors 0 term notes; Undigested Terms Plan routes every page term to an existing note or home sub-plan; Authoring Requirements inherited (N/A). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.
