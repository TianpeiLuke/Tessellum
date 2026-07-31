---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - typescript
keywords:
  - claude agent sdk install
  - npm install anthropic-ai claude-agent-sdk
  - native cli binary not found
  - pathtoclaudecodeexecutable
  - bun build compile
  - extractfrombunfs
  - single executable
  - cross compile
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/typescript
access_control_group: ["general"]
---

# Agent SDK (TypeScript) — Installation

## Overview

The TypeScript Agent SDK is installed as a single npm package, `@anthropic-ai/claude-agent-sdk`. The package bundles a **native Claude Code binary** for your platform as an *optional dependency* (for example `@anthropic-ai/claude-agent-sdk-darwin-arm64`), so you do not install Claude Code separately. Two install-time edge cases need explicit handling: a package manager that skips optional dependencies (recoverable via `pathToClaudeCodeExecutable`), and compiling to a single-file executable with `bun build --compile` (recoverable via the `extractFromBunfs()` helper).

This note documents only the install/build *procedure* and its recovery paths. The `query()` entry point that consumes the installed SDK is covered in [Agent SDK (TypeScript) — query() Entry Point](cc_sdk_typescript_query_function.md); the `Options` object (including `pathToClaudeCodeExecutable`) in [Agent SDK (TypeScript) — Options](cc_sdk_typescript_options.md).

## Installation

```bash
npm install @anthropic-ai/claude-agent-sdk
```

The SDK bundles a native Claude Code binary for your platform as an optional dependency such as `@anthropic-ai/claude-agent-sdk-darwin-arm64`. You do not need to install Claude Code separately.

**`Native CLI binary not found` recovery.** If your package manager skips optional dependencies, the SDK throws `Native CLI binary for <platform> not found`. In that case, set the `pathToClaudeCodeExecutable` option (a field on `Options`) to a separately installed `claude` binary instead.

## Compile to a single executable

When you compile your application into a single-file executable with `bun build --compile`, the SDK cannot resolve the bundled CLI binary at runtime. `require.resolve` does not work inside the compiled executable's `$bunfs` virtual filesystem, so the SDK throws the same `Native CLI binary for <platform> not found` error.

The workaround is to embed the platform binary as a file asset, extract it to a real path at startup with `extractFromBunfs()`, and pass that path to `pathToClaudeCodeExecutable`. The `extractFromBunfs()` helper requires `@anthropic-ai/claude-agent-sdk` **v0.3.144 or later**. The example below builds for macOS on Apple Silicon:

```typescript
import binPath from "@anthropic-ai/claude-agent-sdk-darwin-arm64/claude" with { type: "file" };
import { extractFromBunfs } from "@anthropic-ai/claude-agent-sdk/extract";
import { query } from "@anthropic-ai/claude-agent-sdk";

const cliPath = extractFromBunfs(binPath);

for await (const message of query({
  prompt: "Hello",
  options: { pathToClaudeCodeExecutable: cliPath },
})) {
  console.log(message);
}
```

`extractFromBunfs()` copies the embedded binary out of the compiled executable's virtual filesystem to a per-user temp directory and returns the real path. **Outside a compiled executable it returns the input path unchanged**, so the same code runs in development without modification.

### Platform matching and cross-compilation

Each compiled executable embeds a single platform's binary. Match the platform package in the import to your `--target`:

* To cross-compile, install the non-matching platform package, for example `npm install @anthropic-ai/claude-agent-sdk-linux-x64 --force`.
* On Windows, the binary subpath is `claude.exe`, for example `@anthropic-ai/claude-agent-sdk-win32-x64/claude.exe`.

**Source**: https://code.claude.com/docs/en/agent-sdk/typescript
**Last Updated**: 2026-06-13
**Status**: Active
