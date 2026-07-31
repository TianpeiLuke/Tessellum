---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - modernization
keywords:
  - openclaw application modernization plan
  - small reviewable slices
  - frontend delivery standards skill
  - phased engineering plan
  - control ui first slice
  - pnpm check changed
  - type contract test hardening
  - required vs optional polish
topics:
  - OpenClaw
  - Application Modernization
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/reference/application-modernization-plan
access_control_group: ["general"]
---

# OpenClaw — Application Modernization Plan

## Overview

This note captures the argument OpenClaw's `reference/application-modernization-plan` page makes: how to move the application toward a cleaner, faster, more maintainable product *without* breaking current workflows or hiding risk in broad refactors. The thesis is that modernization should land as small, reviewable slices with proof for each touched surface — never as one sweeping rewrite. It mirrors every section the page contains: the Goal, six engineering Principles, the six sequenced Phases (baseline audit → product/UX cleanup → frontend tightening → performance/reliability → type/contract/test hardening → docs/release readiness), the Recommended first slice (a scoped Control UI + onboarding pass), and the embedded **Frontend Delivery Standards** `SKILL.md` (operating rules, implementation checklist, visual quality gates, handoff format) intended to be installed as a repo-local OpenClaw skill at `.agents/skills/openclaw-frontend/SKILL.md`.

## Goal and Guiding Principles

The stated **Goal** is to "move the application toward a cleaner, faster, more maintainable product without breaking current workflows or hiding risk in broad refactors," with the explicit constraint that "the work should land as small, reviewable slices with proof for each touched surface." The plan's central claim — its argument — is that incrementalism with evidence is preferable to broad refactors, because broad refactors both break workflows and *hide* risk.

Six **Principles** carry that argument:

- Preserve current architecture unless a boundary is demonstrably causing churn, performance cost, or user-visible bugs.
- Prefer the smallest correct patch for each issue, then repeat.
- Separate required fixes from optional polish so maintainers can land high value work without waiting on subjective decisions.
- Keep plugin-facing behavior documented and backwards compatible.
- Verify shipped behavior, dependency contracts, and tests before claiming a regression is fixed.
- Make the main user path better first: onboarding, auth, chat, provider setup, plugin management, and diagnostics.

## Phase 1: Baseline Audit

Inventory the current application *before* changing it. The work: identify the top user workflows and the code surfaces that own them; list dead affordances, duplicate settings, unclear error states, and expensive render paths; capture current validation commands for each surface; mark issues as required, recommended, or optional; and document known blockers that need owner review, especially API, security, release, and plugin contract changes. **Definition of done**: one issue list with repo-root file references; each issue carrying severity, owner surface, expected user impact, and a proposed validation path; and no speculative cleanup items mixed into required fixes.

## Phase 2: Product and UX Cleanup

Prioritize visible workflows and remove confusion. Tighten onboarding copy and empty states around model auth, gateway status, and plugin setup; remove or disable dead affordances where no action is possible; keep important actions visible across responsive widths instead of hiding them behind fragile layout assumptions; consolidate repeated status language so errors have one source of truth; and add progressive disclosure for advanced settings while keeping core setup fast. **Recommended validation**: a manual happy path for first-run setup and existing user startup; focused tests for any routing, config persistence, or status derivation logic; and browser screenshots for changed responsive surfaces.

## Phase 3: Frontend Architecture Tightening

Improve maintainability without a broad rewrite. Move repeated UI state transformations into narrow typed helpers; keep data fetching, persistence, and presentation responsibilities separate; prefer existing hooks, stores, and component patterns over new abstractions; split oversized components only when it reduces coupling or clarifies tests; and avoid introducing broad global state for local panel interactions. **Required guardrails**: do not change public behavior as a side effect of file splitting; keep accessibility behavior intact for menus, dialogs, tabs, and keyboard navigation; and verify that loading, empty, error, and optimistic states still render.

## Phase 4: Performance and Reliability

Target measured pain rather than broad theoretical optimization. Measure startup, route transition, large list, and chat transcript costs; replace repeated expensive derived data with memoized selectors or cached helpers where profiling proves value; reduce avoidable network or filesystem scans on hot paths; keep deterministic ordering for prompt, registry, file, plugin, and network inputs before model payload construction; and add lightweight regression tests for hot helpers and contract boundaries. **Definition of done**: each performance change records baseline, expected impact, actual impact, and remaining gap; and no perf patch lands solely on intuition when cheap measurement is available.

## Phase 5: Type, Contract, and Test Hardening

Raise correctness at the boundary points users and plugin authors depend on. Replace loose runtime strings with discriminated unions or closed code lists; validate external inputs with existing schema helpers or zod; add contract tests around plugin manifests, provider catalogs, gateway protocol messages, and config migration behavior; keep compatibility paths in doctor or repair flows instead of startup-time hidden migrations; and avoid test-only coupling to plugin internals (use SDK facades and documented barrels). **Recommended validation**: `pnpm check:changed`; targeted tests for every changed boundary; and `pnpm build` when lazy boundaries, packaging, or published surfaces change.

## Phase 6: Documentation and Release Readiness

Keep user-facing docs aligned with behavior. Update docs with behavior, API, config, onboarding, or plugin changes; add changelog entries only for user-visible changes; keep plugin terminology user-facing (use internal package names only where needed for contributors); and confirm release and install instructions still match the current command surface. **Definition of done**: relevant docs are updated in the same branch as behavior changes; generated docs or API drift checks pass when touched; and the handoff names any skipped validation and why it was skipped.

## Recommended First Slice

The plan recommends starting with a **scoped Control UI and onboarding pass**: audit first-run setup, provider auth readiness, gateway status, and plugin setup surfaces; remove dead actions and clarify failure states; add or update focused tests for status derivation and config persistence; and run `pnpm check:changed`. The argument for choosing this slice first: "This gives high user value with limited architecture risk" — it advances the main-user-path principle while keeping blast radius small.

## Frontend Skill Update (embedded SKILL.md)

The page closes with reusable guidance to update the frontend-focused `SKILL.md` supplied with the modernization task. If adopting this guidance as a repo-local OpenClaw skill, the instruction is to create `.agents/skills/openclaw-frontend/SKILL.md` first, keep the frontmatter that belongs in that target skill, then add or replace the body guidance with the following content (reproduced verbatim — operating rules, implementation checklist, visual quality gates, and handoff format):

```markdown
# Frontend Delivery Standards

Use this skill when implementing or reviewing user-facing React, Next.js,
desktop webview, or app UI work.

## Operating rules

- Start from the existing product workflow and code conventions.
- Prefer the smallest correct patch that improves the current user path.
- Separate required fixes from optional polish in the handoff.
- Do not build marketing pages when the request is for an application surface.
- Keep actions visible and usable across supported viewport sizes.
- Remove dead affordances instead of leaving controls that cannot act.
- Preserve loading, empty, error, success, and permission states.
- Use existing design-system components, hooks, stores, and icons before adding
  new primitives.

## Implementation checklist

1. Identify the primary user task and the component or route that owns it.
2. Read the local component patterns before editing.
3. Patch the narrowest surface that solves the issue.
4. Add responsive constraints for fixed-format controls, toolbars, grids, and
   counters so text and hover states cannot resize the layout unexpectedly.
5. Keep data loading, state derivation, and rendering responsibilities clear.
6. Add tests when logic, persistence, routing, permissions, or shared helpers
   change.
7. Verify the main happy path and the most relevant edge case.

## Visual quality gates

- Text must fit inside its container on mobile and desktop.
- Toolbars may wrap, but controls must remain reachable.
- Buttons should use familiar icons when the icon is clearer than text.
- Cards should be used for repeated items, modals, and framed tools, not for
  every page section.
- Avoid one-note color palettes and decorative backgrounds that compete with
  operational content.
- Dense product surfaces should optimize for scanning, comparison, and repeated
  use.

## Handoff format

Report:

- What changed.
- What user behavior changed.
- Required validation that passed.
- Any validation skipped and the concrete reason.
- Optional follow-up work, clearly separated from required fixes.
```

The handoff format is the plan's accountability mechanism: it forces every slice to declare what changed, what user behavior changed, which required validation passed, any skipped validation *and the concrete reason*, and optional follow-up kept clearly separate from required fixes — closing the loop on the "separate required fixes from optional polish" and "verify before claiming fixed" principles.

**Source**: OpenClaw documentation — `reference/application-modernization-plan` (mirror `inbox/openclaw_docs/reference/application-modernization-plan.md`)
**Last Updated**: 2026-06-22
**Status**: Active
