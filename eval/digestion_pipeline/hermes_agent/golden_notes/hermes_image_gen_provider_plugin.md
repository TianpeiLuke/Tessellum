---
tags:
  - resource
  - documentation
  - hermes_agent
  - plugins
  - developer_guide
keywords:
  - image generation provider plugin
  - ImageGenProvider ABC
  - image_generate tool
  - kind backend plugin
  - save_b64_image base64 vs URL
  - success_response error_response
topics:
  - Hermes Agent
  - Plugin Authoring
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/image-gen-provider-plugin
access_control_group: ["general"]
---

# Building an Image Generation Provider Plugin

## Overview

An **image-generation provider plugin** is a drop-in directory that registers a backend servicing every `image_generate` tool call — DALL·E, gpt-image, Grok, Flux, Imagen, Stable Diffusion, fal, Replicate, a local ComfyUI rig, anything. It is one of Hermes' `kind: backend` plugins (alongside web-search and video-gen, the more specialized memory/context-engine ABCs being their own kinds). The built-in providers (OpenAI, OpenAI-Codex, xAI) all ship as plugins, so adding a new backend — or overriding a bundled one — means dropping a directory under `plugins/image_gen/<name>/` with zero repo edits. The authoring contract is small: subclass the `ImageGenProvider` ABC, implement the `name` property and `generate()` method, return a dict built with the `success_response()`/`error_response()` helpers, handle base64-vs-URL output via `save_b64_image()`, and expose a `register(ctx)` entry point. This note is the per-kind *procedure*; the *concept* of a provider plugin lives in [term_provider_plugin](../../term_dictionary/term_provider_plugin.md).

## How discovery works

Hermes scans for image-gen backends in three places:

1. **Bundled** — `<repo>/plugins/image_gen/<name>/` (auto-loaded with `kind: backend`, always available)
2. **User** — `~/.hermes/plugins/image_gen/<name>/` (opt-in via `plugins.enabled`)
3. **Pip** — packages declaring a `hermes_agent.plugins` entry point

Each plugin's `register(ctx)` function calls `ctx.register_image_gen_provider(...)`, putting it into the registry in `agent/image_gen_registry.py`. The active provider is picked by `image_gen.provider` in `config.yaml`; `hermes tools` walks users through selection. The `image_generate` tool wrapper asks the registry for the active provider and dispatches there. If no provider is registered, the tool surfaces a helpful error pointing at `hermes tools`.

## Directory structure

```
plugins/image_gen/my-backend/
├── __init__.py      # ImageGenProvider subclass + register()
└── plugin.yaml      # Manifest with kind: backend
```

A bundled plugin is complete at this point. User plugins at `~/.hermes/plugins/image_gen/<name>/` must be added to `plugins.enabled` in `config.yaml` (or run `hermes plugins enable <name>`).

## The ImageGenProvider ABC

Subclass `agent.image_gen_provider.ImageGenProvider`. The only required members are the `name` property and the `generate()` method — everything else has sane defaults. The `capabilities()` method declares whether the backend honors image-to-image / editing: the tool layer surfaces this in the dynamic schema so the model knows when `image_url` is honored (default is text-only, `{"modalities": ["text"], "max_reference_images": 0}`). Inside `generate()`, the presence of `image_url` (or `reference_image_urls`) routes the call to image-to-image vs text-to-image, reported via the `modality` field of `success_response`.

```python
# plugins/image_gen/my-backend/__init__.py
from typing import Any, Dict, List, Optional
import os

from agent.image_gen_provider import (
    DEFAULT_ASPECT_RATIO,
    ImageGenProvider,
    error_response,
    normalize_reference_images,
    resolve_aspect_ratio,
    save_b64_image,
    success_response,
)


class MyBackendImageGenProvider(ImageGenProvider):
    @property
    def name(self) -> str:
        # Stable id used in image_gen.provider config. Lowercase, no spaces.
        return "my-backend"

    def is_available(self) -> bool:
        # Return False if credentials or deps are missing.
        if not os.environ.get("MY_BACKEND_API_KEY"):
            return False
        try:
            import my_backend_sdk  # noqa: F401
        except ImportError:
            return False
        return True

    def default_model(self) -> Optional[str]:
        return "my-model-fast"

    def capabilities(self) -> Dict[str, Any]:
        # Declare image-to-image / editing support; default is text-only.
        return {"modalities": ["text", "image"], "max_reference_images": 4}

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = DEFAULT_ASPECT_RATIO,
        *,
        image_url: Optional[str] = None,
        reference_image_urls: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        prompt = (prompt or "").strip()
        aspect_ratio = resolve_aspect_ratio(aspect_ratio)
        if not prompt:
            return error_response(
                error="Prompt is required", error_type="invalid_input",
                provider=self.name, prompt="", aspect_ratio=aspect_ratio,
            )
        # Routing: image_url/reference_image_urls set => image-to-image; else text.
        sources = []
        if image_url:
            sources.append(image_url)
        sources.extend(normalize_reference_images(reference_image_urls) or [])
        modality = "image" if sources else "text"
        # Model selection precedence: env var -> config -> default.
        model_id = kwargs.get("model") or self.default_model() or "my-model-fast"
        try:
            import my_backend_sdk
            client = my_backend_sdk.Client(api_key=os.environ["MY_BACKEND_API_KEY"])
            if modality == "image":
                result = client.edit(prompt=prompt, model=model_id, image_urls=sources)
            else:
                result = client.generate(prompt=prompt, model=model_id, aspect_ratio=aspect_ratio)
            # URL string -> return as `image`; base64 -> save via save_b64_image()
            if result.get("image_b64"):
                image = str(save_b64_image(result["image_b64"], prefix=self.name, extension="png"))
            else:
                image = result["image_url"]
            return success_response(
                image=image, model=model_id, prompt=prompt,
                aspect_ratio=aspect_ratio, provider=self.name, modality=modality,
            )
        except Exception as exc:
            return error_response(
                error=str(exc), error_type=type(exc).__name__, provider=self.name,
                model=model_id, prompt=prompt, aspect_ratio=aspect_ratio,
            )


def register(ctx) -> None:
    """Plugin entry point — called once at load time."""
    ctx.register_image_gen_provider(MyBackendImageGenProvider())
```

Optional members not shown above: `display_name` (label in `hermes tools`, defaults to `name.title()`), `list_models()` (catalog for the model picker), and `get_setup_schema()` (picker metadata + env-var prompts for setup).

## plugin.yaml

```yaml
name: my-backend
version: 1.0.0
description: My image backend — text-to-image via My Backend SDK
author: Your Name
kind: backend
requires_env:
  - MY_BACKEND_API_KEY
```

`kind: backend` is what routes the plugin to the image-gen registration path. `requires_env` is prompted during `hermes plugins install`.

## ABC reference

Full contract in `agent/image_gen_provider.py`. The members you'll typically override:

| Member | Required | Default | Purpose |
|---|---|---|---|
| `name` | ✅ | — | Stable id used in `image_gen.provider` config |
| `display_name` | — | `name.title()` | Label shown in `hermes tools` |
| `is_available()` | — | `True` | Gate for missing creds/deps |
| `list_models()` | — | `[]` | Catalog for `hermes tools` model picker |
| `default_model()` | — | first from `list_models()` | Fallback when no model is configured |
| `get_setup_schema()` | — | minimal | Picker metadata + env-var prompts |
| `generate(prompt, aspect_ratio, **kwargs)` | ✅ | — | The call |

## Response format and base64 vs URL output

`generate()` must return a dict built via `success_response()` or `error_response()` (both live in `agent/image_gen_provider.py`). The tool wrapper JSON-serializes the dict and hands it to the LLM; errors are surfaced as the tool result and the LLM decides how to explain them.

```python
# Success
success_response(
    image=<url-or-absolute-path>, model=<model-id>, prompt=<echoed-prompt>,
    aspect_ratio="landscape" | "square" | "portrait",
    provider=<your-provider-name>, extra={...},  # optional backend-specific
)
# Error
error_response(
    error="human-readable message",
    error_type="provider_error" | "invalid_input" | "<exception class name>",
    provider=<your-provider-name>, model=<model-id>,
    prompt=<prompt>, aspect_ratio=<resolved aspect>,
)
```

Some backends return image URLs (fal, Replicate); others return base64 payloads (OpenAI gpt-image-2). For the base64 case, `save_b64_image()` writes to `$HERMES_HOME/cache/images/<prefix>_<timestamp>_<uuid>.<ext>` and returns the absolute `Path`; pass that path (as `str`) as `image=` in `success_response()`. Gateway delivery (Telegram photo bubble, Discord attachment) recognizes both URLs and absolute paths.

## User overrides and testing

Drop a user plugin at `~/.hermes/plugins/image_gen/<name>/` with the same `name` property as a bundled one and enable it via `hermes plugins enable <name>` — the registry is last-writer-wins, so your version replaces the built-in. This is useful for pointing an `openai` plugin at a private proxy or swapping in a custom model catalog. To test:

```bash
export HERMES_HOME=/tmp/hermes-imggen-test
mkdir -p $HERMES_HOME/plugins/image_gen/my-backend
# …copy __init__.py + plugin.yaml into that dir…
export MY_BACKEND_API_KEY=your-test-key
hermes plugins enable my-backend
echo "image_gen:" >> $HERMES_HOME/config.yaml
echo "  provider: my-backend" >> $HERMES_HOME/config.yaml
hermes -z "Generate an image of a corgi in a spacesuit"
```

Or interactively: `hermes tools` → "Image Generation" → select `my-backend` → enter API key if prompted.

## Reference implementations and distribute via pip

- **`plugins/image_gen/openai/__init__.py`** — gpt-image-2 at low/medium/high tiers as three virtual model IDs sharing one API model with different `quality` params (tiered models under one backend + `config.yaml` precedence chain).
- **`plugins/image_gen/xai/__init__.py`** — Grok Imagine via xAI (URL output, simpler catalog).
- **`plugins/image_gen/openai-codex/__init__.py`** — Codex-style Responses API variant reusing the OpenAI SDK with a different routing base URL.

For pip distribution, declare a `hermes_agent.plugins` entry point pointing at a package that exposes a top-level `register` function:

```toml
# pyproject.toml
[project.entry-points."hermes_agent.plugins"]
my-backend-imggen = "my_backend_imggen_package"
```

The general plugin guide's "Distribute via pip" section covers the full setup.

**Source**: `inbox/hermes_agent_docs/developer-guide/image-gen-provider-plugin.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/image-gen-provider-plugin
**Last Updated**: 2026-06-19
**Status**: Active
