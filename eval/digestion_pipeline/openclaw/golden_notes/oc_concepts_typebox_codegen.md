---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - typebox
keywords:
  - openclaw typebox codegen
  - protocol:gen protocol:check
  - add a method end-to-end
  - gateway protocol schema change
  - system.echo worked example
  - ajv validator compile
  - swift gateway models codegen
  - when you change schemas checklist
topics:
  - OpenClaw
  - TypeBox Codegen
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/typebox
access_control_group: ["general"]
---

# OpenClaw — TypeBox Protocol Codegen Workflow

## Overview

This note is the **procedure** half of OpenClaw's `concepts/typebox` page: how to regenerate and extend the TypeBox-defined Gateway WebSocket protocol. It covers the `pnpm protocol:gen` / `protocol:gen:swift` / `protocol:check` codegen pipeline, the end-to-end worked example that adds a `system.echo` request (schema → AJV validation → server handler → registration → scope classification → regenerate → tests/docs), and the five-step "When you change schemas" checklist. The companion data-model note `oc_concepts_typebox_protocol` documents the frame/schema model these steps regenerate from; this note documents the actions a developer takes. Every command, file path, and code snippet below is copied verbatim from the local mirror page.

## Current pipeline

OpenClaw exposes three `pnpm` scripts that drive protocol generation. Schemas are TypeScript-first (the single source of truth), and these scripts derive the runtime/cross-language artifacts from them:

- `pnpm protocol:gen` — writes JSON Schema (draft-07) to `dist/protocol.schema.json`.
- `pnpm protocol:gen:swift` — generates Swift gateway models.
- `pnpm protocol:check` — runs both generators and verifies the output is committed.

`protocol:check` is the gate: because it both regenerates and verifies that the regenerated output matches what is committed, it fails if a schema change was made without committing the regenerated `dist/protocol.schema.json` and `GatewayModels.swift`.

## Worked example: add a method end-to-end

The page walks through adding a new `system.echo` request that returns `{ ok: true, text }`. The procedure is five numbered steps.

### Step 1 — Schema (source of truth)

Add the param and result schemas to `packages/gateway-protocol/src/schema.ts`:

```ts
export const SystemEchoParamsSchema = Type.Object(
  { text: NonEmptyString },
  { additionalProperties: false },
);

export const SystemEchoResultSchema = Type.Object(
  { ok: Type.Boolean(), text: NonEmptyString },
  { additionalProperties: false },
);
```

Then add both to the `ProtocolSchemas` registry and export their static types:

```ts
  SystemEchoParams: SystemEchoParamsSchema,
  SystemEchoResult: SystemEchoResultSchema,

export type SystemEchoParams = Static<typeof SystemEchoParamsSchema>;
export type SystemEchoResult = Static<typeof SystemEchoResultSchema>;
```

The schemas use `additionalProperties: false` (strict payloads) and `NonEmptyString` (the convention for IDs and method/event names) — the same patterns enforced across the protocol.

### Step 2 — Validation

In `packages/gateway-protocol/src/index.ts`, export an AJV validator compiled from the new schema:

```ts
export const validateSystemEchoParams = ajv.compile<SystemEchoParams>(SystemEchoParamsSchema);
```

### Step 3 — Server behavior

Add a handler in `src/gateway/server-methods/system.ts`:

```ts
export const systemHandlers: GatewayRequestHandlers = {
  "system.echo": ({ params, respond }) => {
    const text = String(params.text ?? "");
    respond(true, { ok: true, text });
  },
};
```

Register it in `src/gateway/server-methods.ts` (which already merges `systemHandlers`), then add `"system.echo"` to the `listGatewayMethods` input in `src/gateway/server-methods-list.ts`. If the method is callable by operator or node clients, also classify it in `src/gateway/method-scopes.ts` so that scope enforcement and the `hello-ok` feature advertising stay aligned.

### Step 4 — Regenerate

Run the verifying generator:

```bash
pnpm protocol:check
```

### Step 5 — Tests + docs

Add a server test in `src/gateway/server.*.test.ts` and note the method in docs.

## When you change schemas

For any schema change (not just a brand-new method), the page gives a five-step checklist that captures the same discipline as the worked example:

1. Update the TypeBox schemas.
2. Register the method/event in `src/gateway/server-methods-list.ts`.
3. Update `src/gateway/method-scopes.ts` when the new RPC needs operator or node scope classification.
4. Run `pnpm protocol:check`.
5. Commit the regenerated schema + Swift models.

The pattern is the same in both: edit the TS source of truth, register the method/event in the discovery list, classify scope when operator/node-callable, regenerate via `protocol:check`, and commit the regenerated `dist/protocol.schema.json` + `GatewayModels.swift` so `protocol:check` stays green.

**Source**: OpenClaw documentation — `concepts/typebox` (mirror `inbox/openclaw_docs/concepts/typebox.md`)
**Last Updated**: 2026-06-22
**Status**: Active
