---
tags:
  - resource
  - terminology
  - tools
  - agentic_ai
keywords:
  - Browser Automation
  - browser tool
  - CDP
  - accessibility tree
  - headless browser
  - agentic browsing
  - web automation
topics:
  - Agentic AI Tooling
  - Web Automation
  - Autonomous Coding Agents
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Browser Automation

## Definition

**Browser automation** is the programmatic control of a real web browser — navigating to URLs, reading
page structure, and interacting with elements (clicking, typing, scrolling, submitting forms) — without a human driving the keyboard and mouse. Classically it is the foundation of web UI testing and scraping (WebDriver / Selenium, Puppeteer, Playwright) and increasingly the way **autonomous coding agents** and LLM "computer-use" agents reach beyond a static training cutoff to perform live web tasks: logging in, filling out forms, scraping dynamic JavaScript-rendered content, and handling multi-step flows. The problem it solves is that a large fraction of the world's information and actions live behind interactive, session-stateful, JavaScript-heavy pages that a one-shot HTTP fetch cannot reach.

In the agentic setting the page is typically presented to the model not as raw pixels but as an
**accessibility tree** — a text snapshot of the page's semantic structure in which each interactive element
is assigned a stable reference ID (e.g. `@e1`, `@e2`) that the agent cites when it asks the tool to click or type. This text-first representation is far more token-efficient and reliable for an LLM than pixel coordinates, with a screenshot+vision path reserved for cases (CAPTCHAs, charts, visual verification) where the text tree is insufficient. The browser itself is driven over the **Chrome DevTools Protocol (CDP)** — a JSON-over-WebSocket command/event protocol (`Page`, `Runtime`, `DOM`, `Network`, `Target`, … domains) that instruments and controls Chromium-family browsers — or through a vendor's cloud-browser API.

## Context

In **Hermes Agent** (Nous Research's autonomous coding agent, the source of this note), browser automation is a first-class toolset exposing ~12 `browser_*` tools (`browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_scroll`, `browser_vision`, `browser_console`, `browser_cdp`, `browser_dialog`, …) over six interchangeable backends: three cloud providers (Browserbase, Browser Use, Firecrawl), local anti-detection browsing (Camofox, a Firefox fork with C++ fingerprint spoofing), a local Chromium-family browser attached via CDP (`/browser connect`), and a default local mode driven by the `agent-browser` CLI. Each task gets an isolated session with automatic inactivity cleanup; a persistent CDP "supervisor" (one WebSocket per task) watches `Page`/`Runtime`/`Target` events to surface native dialogs and the iframe tree. The same pattern recurs across the agent-tooling ecosystem — Claude Code's Chrome automation tool, and the broader category of **computer-use** agents — so the concept is cross-cutting, not Hermes-specific.

Browser automation is the heavier, interactive counterpart to non-interactive web tooling: agents are steered toward cheaper `web_search` / `web_extract` for plain information retrieval, and toward the browser tool only when a task genuinely requires interaction (auth, form fill, dynamic content). It contrasts with desktop-level **computer use** (which controls the whole OS GUI by pixel/coordinate or accessibility API) and with the generic source-code-navigation idea (`term_code_browser`) — those are different concepts that share the word "browser."

## Key Characteristics

- **Multi-backend / provider-agnostic.** A single tool surface routes to cloud browsers, a local anti-detection browser, or an attached local Chromium via CDP; cloud providers can auto-fall-back to a local sidecar for private/loopback URLs (hybrid routing).
- **Accessibility-tree-not-pixels.** The default page representation is a compact, summarizable text snapshot of interactive elements with stable `@e` ref IDs — token-efficient and robust to layout shifts — with a screenshot + vision-model path as the fallback for visual content.
- **CDP-driven, with a raw passthrough.** Control runs over the Chrome DevTools Protocol; a `browser_cdp` escape hatch exposes arbitrary CDP verbs (e.g. `Target.getTargets`, `Runtime.evaluate`, `Network.getAllCookies`) for operations the higher-level tools do not cover, including cross-origin (OOPIF) iframe-scoped evaluation via a `frame_id`.
- **Session isolation, recording, and cleanup.** Each task runs in its own browser session; sessions can be recorded to video, are reaped after an inactivity timeout, and are emergency-cleaned on process exit.
- **Stealth and anti-detection.** Randomized fingerprints, residential proxies, and CAPTCHA solving on the cloud side; local fingerprint spoofing via Camofox — used to look like a real human browser rather than a bot.
- **Native-dialog handling.** A persistent CDP supervisor detects blocking `alert`/`confirm`/`prompt` dialogs and lets the agent respond explicitly, instead of silently hanging the page's JS thread.
- **Known limits.** Text-based interaction (no pixel coordinates), large-snapshot truncation/summarization, provider-plan-dependent session timeouts, per-session cloud cost, and (in the Hermes implementation) no file downloads.

## Related Terms

- **[OpenClaw — Managed Browser: Overview, Quick Start, and Configuration](../documentation/openclaw/oc_tools_browser_overview.md)** — This note is the operator/agent procedure for the **OpenClaw-managed browser**: a dedicated Chrome/Brave/Edge/Chromium profile the agent controls, isolated…

## References

- [Hermes Agent — Browser Automation](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Browserbase Documentation](https://docs.browserbase.com/)
- [Playwright — Browser automation library](https://playwright.dev/)
- [Test automation (Wikipedia)](https://en.wikipedia.org/wiki/Test_automation)

---

**Last Updated**: 2026-06-19
**Status**: Active
