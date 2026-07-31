---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - performance
keywords:
  - openclaw release performance sweep
  - install footprint audit
  - npm package size
  - shrinkwrap boundary
  - supply-chain dependency count
  - cold warm agent turn
  - kova agent turn
  - napi-rs canvas fanout
  - v2026.5.28 cleanup
topics:
  - OpenClaw
  - Release Performance
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/reference/release-performance-sweep
access_control_group: ["general"]
---

# OpenClaw — Release Performance Sweep (May 2026 Perf, Package-Size, Dependency, and Shrinkwrap Evidence)

## Overview

This note captures the **argument and evidence** behind the May-2026 OpenClaw performance, package-size, dependency, and shrinkwrap cleanup, mirroring the `reference/release-performance-sweep` page (the technical companion to the public blog post). The central claims it argues from measured data are: (1) the cleanup between `v2026.5.27` and `v2026.5.28` made the agent materially faster (**5.1x faster cold turn** vs the earlier-April baseline) and the install materially smaller; (2) **shrinkwrap itself was never the problem — the bad package shape was**; and (3) **dependency count is an operational security metric, not only an install-size metric**. The page combines four audits (a release performance sweep, earlier-April published context, an install-footprint sweep, and an npm package-size sweep) and explicitly cautions that the per-tag numbers are *trend evidence and regression-hunting signal, not release-gate statistics*.

## Thesis and Evidence Caveats

The page argues from measurement, and it front-loads its own evidentiary limits so the numbers are read as trend signal rather than guarantees. Four audits are combined: (a) a **Release performance sweep** of GitHub Releases from `v2026.5.28` back through stable `v2026.4.23`, run via the `OpenClaw Performance` workflow with `profile=smoke` on the mock-provider lane — most tag rows are one sample, but the `v2026.5.27` and `v2026.5.28` rows use the latest repeat-3 release-branch artifacts; (b) **Earlier April context** from published `clawgrit-reports` mock-provider baselines (`v2026.4.1`–`v2026.5.2`), used *only* to avoid treating the broken late-April releases as the public performance baseline; (c) an **Install footprint sweep** using fresh `npm install --ignore-scripts` into temporary packages, with `du -sk node_modules` for size and a `node_modules` walk for package-instance counts; and (d) an **npm package size sweep** using `npm pack openclaw@<version> --dry-run --json` to record compressed tarball size, unpacked size, and file count. A Warning on the page states plainly that the main sweep uses one smoke sample per tag (except the repeat-3 `v2026.5.27`/`v2026.5.28` rows) and that the earlier-April context uses published repeat-3 medians — so the deltas are trend evidence and regression-hunting signal, **not** release-gate statistics.

## Snapshot

Performance coverage spans **77 requested releases**, **74 artifact-backed points**, and **3 unavailable CI runs**; the latest stable measured point is `v2026.5.28`. The headline snapshot cards summarize the argued outcome: a **5.1x faster cold turn** (`v2026.4.14`: 9.8s → `v2026.5.28`: 1.9s); a **17.9MB published tarball** (latest stable, down from the 43.3MB March package-size peak); a **361.7MiB fresh install** for `v2026.5.28` (a sharp cut to the nested OpenClaw dependency tree, though a smaller 259.7MiB nested tree still remains in the local install audit); and a **300-package dependency graph** (unique package name/version roots in a fresh install with scripts disabled).

## Install Footprint Timeline

The timeline frames four reference points that the supply-chain argument leans on. The **monthly dependency-count high** was **645 dependencies** at `2026.2.26`. **Shrinkwrap was introduced** at `2026.5.22`, which produced a **1,020.6MB install** and exposed a package-shape problem: **911.8MB landed under nested `openclaw/node_modules`**. The **latest stable** `2026.5.28` cuts fresh install size by **52.8% from `2026.5.27`** (to 361.7MiB) but still installs a 259.7MiB nested OpenClaw tree, and its **dependency graph** of **300 package roots** is **71 fewer** unique package name/version roots than `2026.5.27`. The page's Tip states the nuanced claim directly: *"Shrinkwrap was not the problem by itself. The bad package shape was."* — `v2026.5.28` still ships shrinkwrap, but the nested tree is much smaller and the all-platform canvas fanout is gone in the local audit.

## What Changed In 5.28

The cleanup between `v2026.5.27` and `v2026.5.28` **reduced the default-install graph instead of removing the capabilities themselves** — a key qualifier in the argument, since it means the speed/size wins did not come at a feature cost. Four changes: the **root default graph** shrank (unique package name/version roots fell from **371 → 300**; package instances fell from **372 → 301**); the **nested tree** (`openclaw/node_modules`) fell from **656.1MiB → 259.7MiB** in the same local install audit; the **all-platform `@napi-rs/canvas` native package cone stopped landing** in the default install; and the **supply-chain surface** shrank — "fewer default packages means fewer tarballs, maintainers, native binaries, install-time behaviors, and transitive update paths to trust by default."

## Headline Numbers

The page is explicit that the **late-April broken rows must not be used as public performance baselines**: `v2026.4.23` and `v2026.4.29` are useful regression evidence, but the large `14x`-style deltas mostly describe the *recovery from a bad release line*, not real improvement. For the blog narrative scale it uses the earlier-April published baseline (`v2026.4.14` from the published `clawgrit-reports` mock-provider run; that run used repeat 3 and failed only because the diagnostic timeline was not emitted, so its cold/warm/RSS medians are still useful as rough scale — narrative context, not a release-gate statistic).

| Metric | Earlier April baseline | `v2026.5.28` | Delta |
| --- | ---: | ---: | ---: |
| Cold agent turn | 9,819ms | 1,908ms | 80.6% lower, 5.1x faster |
| Warm agent turn | 7,458ms | 1,870ms | 74.9% lower, 4.0x faster |
| Agent peak RSS | 686.2MB | 581.0MB | 15.3% lower |

Within the May sweep, the latest release-branch row moved materially from `v2026.5.2` (cold 3,897ms → 1,908ms, 51.0% lower; warm 3,610ms → 1,870ms, 48.2% lower; agent peak RSS 613.7MB → 581.0MB, 5.3% lower), and compared with the previous stable release `v2026.5.27` (cold 2,231ms → 1,908ms, 14.5% lower; warm 2,226ms → 1,870ms, 16.0% lower; agent peak RSS 649.0MB → 581.0MB, 10.5% lower).

### Install footprint

| Metric | Baseline | `v2026.5.28` | Delta |
| --- | ---: | ---: | ---: |
| Install size from `2026.5.22` peak | 1,020.6MB | 361.7MiB | 64.6% lower |
| Install size from latest release `2026.5.27` | 767.1MiB | 361.7MiB | 52.8% lower |
| Dependencies from monthly high `2026.2.26` | 645 | 300 | 53.5% lower |
| Dependencies from latest release `2026.5.27` | 371 | 300 | 19.1% lower |
| Nested `openclaw/node_modules` from `2026.5.22` | 911.8MB | 259.7MiB | 71.5% lower |
| Nested `openclaw/node_modules` from `2026.5.27` | 656.1MiB | 259.7MiB | 60.4% lower |

### npm package size

The npm-package-size sweep (`npm pack openclaw@<version> --dry-run --json`) traces compressed tarball size, unpacked size, and file count from the early rebranded package to latest stable: `2026.1.30` (12.8MB / 33.5MB / 4,607 files, early rebranded package), `2026.2.26` (23.6MB / 82.9MB / 10,125, feature growth), `2026.3.31` (43.3MB / 182.6MB / 21,037, **package-size high point**), `2026.4.29` (22.9MB / 74.6MB / 9,309, package pruning visible), `2026.5.12` (23.4MB / 80.1MB / 12,035, **major external-plugin split**), `2026.5.22` (17.2MB / 76.9MB / 12,386, docs/assets excluded from package), `2026.5.27` (17.8MB / 79.0MB / 12,509, previous stable package), and `2026.5.28` (17.9MB / 81.0MB / **9,082** files, latest stable package). `2026.5.12` is the visible **plugin-extraction milestone** in the changelog: Amazon Bedrock, Bedrock Mantle, Slack, OpenShell sandbox, Anthropic Vertex, Matrix, and WhatsApp moved out of the core dependency path so their dependency cones install with those plugins instead of every core install.

## Kova agent turn summary

The argument distinguishes two April stories: earlier April was "slow but recognizable," while late April became "a regression cliff," and `v2026.5.2` is where the mock-provider lane first drops into the 3–5s range and starts passing consistently in the supplied sweep. The earlier published context rows (`v2026.4.10` through `v2026.4.22`) all show **Kova FAIL** with cold turns 9,630–22,314ms. The supplied sweep then shows the cliff and recovery: `v2026.4.23`–`v2026.4.29` all **FAIL** with cold turns escalating to 47,847ms, 48,264ms, 81,080ms, 76,771ms, 60,902ms, and 94,031ms (agent peak RSS peaking at **3,613.7MB** at `v2026.4.29`); then from `v2026.5.2` onward every row **PASSES** — `v2026.5.2` (3,897ms / 3,610ms / 613.7MB), `v2026.5.7` (3,923ms / 3,693ms), `v2026.5.12` (7,248ms / 6,629ms / 834.8MB), `v2026.5.18` (3,301ms), `v2026.5.20` (3,413ms), `v2026.5.22` (4,494ms), `v2026.5.26` (2,626ms), `v2026.5.27-beta.1` (2,575ms), `v2026.5.27` (2,231ms), and `v2026.5.28` (**1,908ms cold / 1,870ms warm / 581.0MB RSS**).

## Source probes

Source probes were skipped for **17 successful older refs** because those source trees did not yet have the required probe entry points (agent-turn metrics still exist for those refs). The representative source-probe table tracks default `readyz` p50, 50-plugins `readyz` p50, CLI health p50, and plugin max RSS across `v2026.4.29` through `v2026.5.28`. The latest stable `v2026.5.28` reports default `readyz` p50 **1,457ms**, 50-plugins `readyz` p50 **1,474ms**, CLI health p50 **623ms**, and plugin max RSS **386.1MB**. The page flags the **`v2026.5.22` CLI-health spike (5,095ms)** as visible in this table *even though the agent-turn lane still passed* — the explicit lesson is to keep the source probes when investigating targeted CLI or gateway regressions, because a healthy agent-turn lane can mask a CLI/gateway regression.

## Install footprint audit

Dependency samples use one stable release per month, plus the `2026.5.22` shrinkwrap-introduction event and the latest `2026.5.28` release. The audit tracks installed deps, fresh install size, OpenClaw package size, nested `openclaw/node_modules`, root-shrinkwrap presence, and canvas install behavior. Pre-shrinkwrap rows (`2026.1.30`–`2026.4.29`) carry **no root shrinkwrap** and tiny-to-zero nested trees (Jan 605 deps / 438.4MB / 2.4MB nested; Apr `2026.4.29` 392 deps / 335.0MB / 0MB nested, "none installed" canvas). The shrinkwrap event row `2026.5.22` (401 deps / **1,020.6MB** install / 911.8MB nested / shrinkwrap **yes** / "nested: all 12 `@napi-rs/canvas` packages") and the following `2026.5.26` (371 deps / 767.5MB / 656.4MB nested) and `2026.5.27` (371 deps / 767.1MiB / 656.1MiB nested) all materialize the **full 12-package canvas cone**. The latest `2026.5.28` (300 deps / **361.7MiB** install / 259.7MiB nested / shrinkwrap **yes** / canvas "none installed") demonstrates the cleanup while keeping shrinkwrap.

### Shrinkwrap boundary

The shrinkwrap-boundary cards isolate the cause-and-effect the argument hinges on: `2026.5.20` had **no root shrinkwrap and no large nested OpenClaw dependency tree**; `2026.5.22` **added root shrinkwrap and installed 911.8MB** under nested `openclaw/node_modules`; `2026.5.28` **keeps shrinkwrap and still installs 259.7MiB** under the nested tree; and `2026.5.28` **no longer installs any `@napi-rs/canvas` packages** in the local fresh-install audit. Published-tarball inspection verifies the boundary by listing each version's published-stable status and root `npm-shrinkwrap.json` presence: `2026.5.20` (published, no shrinkwrap, last stable before shrinkwrap), `2026.5.22` (published, shrinkwrap introduced), through `2026.5.26`/`2026.5.27` (published, shrinkwrap yes, nested tree still present) to `2026.5.28` (published, shrinkwrap yes, nested tree much smaller); intervening `2026.5.21`/`.23`/`.24`/`.25` had no stable npm release (`n/a`). The page restates the **important distinction** in bold: *shrinkwrap itself is not the problem* — `v2026.5.28` still ships root shrinkwrap; the problem was the **package shape** that made npm materialize a large nested OpenClaw dependency tree and all 12 `@napi-rs/canvas` platform packages. For a plain-English explanation of shrinkwrap and the maintainer-level package checks, the page links the npm-shrinkwrap reference.

## Supply-chain interpretation

The page's strongest argument is that **dependency count is an operational security metric, not only an install-size metric**: every package expands the set of maintainers, tarballs, transitive updates, optional native binaries, and install-time behaviors that operators must trust. From this premise it states the cleanup direction as a set of prescriptive principles: keep heavy and optional capabilities outside the default core install; make plugin packages own their runtime dependency graph; avoid runtime package-manager repair during Gateway startup; preserve deterministic installs without causing all-platform native-package materialization; keep install scripts disabled in package-acceptance and measurement paths; and catch nested dependency trees and native optional-dependency explosions before publishing. These principles tie the perf/size evidence back to a trust-surface-reduction conclusion: fewer default packages is argued as a security win, not merely a smaller download.

**Source**: OpenClaw documentation — `reference/release-performance-sweep` (mirror `inbox/openclaw_docs/reference/release-performance-sweep.md`)
**Last Updated**: 2026-06-22
**Status**: Active
