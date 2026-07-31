---
tags:
  - resource
  - documentation
  - hermes_agent
  - model_catalog
  - reference
keywords:
  - model catalog manifest
  - model-catalog.json
  - openrouter nous portal model lists
  - manifest schema and fetch behavior
  - per-provider override url
  - in-repo snapshot fallback
topics:
  - Hermes Agent
  - Reference
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/reference/model-catalog
access_control_group: ["general"]
---

# Hermes Agent — Model Catalog Reference

## Overview

The **model catalog** is a remotely-hosted JSON manifest that drives Hermes' curated model-picker lists for **OpenRouter** and **Nous Portal**. Rather than baking those lists into the binary, Hermes fetches them at runtime from a manifest hosted alongside the docs site, so maintainers can update the picker without shipping a new `hermes-agent` release. The manifest is deliberately fail-safe: when it is unreachable (offline, network blocked, hosting failure, or a schema-version Hermes doesn't understand), Hermes silently falls back to the in-repo snapshot bundled with the installed CLI. The manifest never breaks the picker — worst case you see whatever list shipped with your version.

This note is the Hermes-specific *manifest reference*: the live URL, the per-model JSON schema, the fetch/cache decision table, the `config.yaml` knobs (including per-provider override URLs), and how maintainers regenerate the manifest from the in-repo model lists. It is the reference enumeration only — the generic notion of a catalog of available models is the [term_model_catalog](../../term_dictionary/term_model_catalog.md) concept, and provider/model selection prose is owned by the configuring-models and providers pages it links into.

## Live manifest URL

```
https://hermes-agent.nousresearch.com/docs/api/model-catalog.json
```

It is published on every merge to `main` via the existing `deploy-site.yml` GitHub Pages pipeline. The source of truth lives in the repo at `website/static/api/model-catalog.json`.

## Schema

```json
{
  "version": 1,
  "updated_at": "2026-04-25T22:00:00Z",
  "metadata": {},
  "providers": {
    "openrouter": {
      "metadata": {},
      "models": [
        {"id": "moonshotai/kimi-k2.6", "description": "recommended", "metadata": {}},
        {"id": "openai/gpt-5.4",       "description": ""}
      ]
    },
    "nous": {
      "metadata": {},
      "models": [
        {"id": "anthropic/claude-opus-4.7"},
        {"id": "moonshotai/kimi-k2.6"}
      ]
    }
  }
}
```

Field notes (verbatim from the source):

- **`version`** — integer schema version. Future schemas bump this; Hermes refuses manifests with versions it doesn't understand and falls back to the hardcoded snapshot.
- **`metadata`** — free-form dict at the manifest, provider, and model level. Any keys. Hermes ignores unknown fields, so you can annotate entries (`"tier": "paid"`, `"tags": [...]`, etc.) without coordinating a schema change.
- **`description`** — OpenRouter-only. Drives picker badge text (`"recommended"`, `"free"`, or empty). Nous Portal doesn't use this — free-tier gating is determined live from the Portal's pricing endpoint.
- **Pricing and context length** are NOT in the manifest. Those come from live provider APIs (`/v1/models` endpoints, models.dev) at fetch time.

## Fetch behavior

| When | What happens |
|---|---|
| `/model` or `hermes model` | Fetches if disk cache is stale, else uses cache |
| Disk cache fresh (< TTL) | No network hit |
| Network failure with cache | Silent fallback to cache, one log line |
| Network failure, no cache | Silent fallback to in-repo snapshot |
| Manifest fails schema validation | Treated as unreachable |

Cache location: `~/.hermes/cache/model_catalog.json`.

## Config

```yaml
model_catalog:
  enabled: true
  url: https://hermes-agent.nousresearch.com/docs/api/model-catalog.json
  ttl_hours: 1
  providers: {}
```

Set `enabled: false` to disable remote fetch entirely and always use the in-repo snapshot.

### Per-provider override URLs

Third parties can self-host their own curation list using the same schema. Point a provider at a custom URL:

```yaml
model_catalog:
  providers:
    openrouter:
      url: https://example.com/my-openrouter-curation.json
```

The overriding manifest only needs to populate the provider block(s) it cares about. Other providers continue to resolve against the master URL.

## Updating the manifest

Maintainers re-generate the manifest from the in-repo hardcoded lists, keeping it in sync after editing `OPENROUTER_MODELS` or `_PROVIDER_MODELS["nous"]` in `hermes_cli/models.py`:

```bash
python scripts/build_model_catalog.py
```

Then PR the resulting change to `website/static/api/model-catalog.json` to `main`. The docs site auto-deploys on merge and the new manifest is live within a few minutes. You can also hand-edit the JSON directly for fine-grained metadata changes that don't belong in the in-repo snapshot — the generator script is a convenience, not the single source of truth.

**Source**: `inbox/hermes_agent_docs/reference/model-catalog.md` · https://hermes-agent.nousresearch.com/docs/reference/model-catalog
**Last Updated**: 2026-06-19
**Status**: Active
