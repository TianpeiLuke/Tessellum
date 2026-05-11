"""LLM backend abstraction.

A backend is *just* a callable — given an :class:`LLMRequest` (system
prompt + user prompt + max_tokens), return an :class:`LLMResponse`
(content + timing + diagnostic metadata). All backends declared in
:data:`tessellum.composer.contracts.BACKEND_CONTRACTS` should match
this shape; the compiler validates the contract; the executor invokes
the ``call`` method.

Two backends ship:

- :class:`MockBackend` — canned responses, no network. Makes the
  executor + scheduler testable end-to-end without API keys.
- :class:`AnthropicBackend` — production Anthropic Messages API
  client. Available with the ``[agent]`` extras::

      pip install tessellum[agent]

  and ``ANTHROPIC_API_KEY`` in the environment.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class LLMRequest:
    """One request to a backend.

    Attributes:
        system_prompt: The system role prompt (typically static across
            a step's invocations).
        user_prompt: The rendered user prompt — placeholders resolved
            by the executor.
        max_tokens: Cap on response length.
    """

    system_prompt: str
    user_prompt: str
    max_tokens: int = 4000


@dataclass(frozen=True)
class LLMResponse:
    """One response from a backend.

    Attributes:
        content: The raw response text (the executor parses it according
            to the step's materializer wire_format).
        elapsed_ms: Wall-clock time of the call.
        backend_id: ``MockBackend`` → ``"mock"``; ``AnthropicBackend``
            → ``"anthropic"``; etc.
        metadata: Free-form diagnostics (token counts, model name,
            ``stop_reason``, etc.). Surfaces in the run trace.
    """

    content: str
    elapsed_ms: float
    backend_id: str
    metadata: dict = field(default_factory=dict)


class LLMBackend(Protocol):
    """Protocol any LLM backend must satisfy."""

    backend_id: str

    def call(self, request: LLMRequest) -> LLMResponse:  # pragma: no cover
        ...


class MockBackend:
    """Canned-response backend for testing the executor without an API.

    Constructed with a ``responses`` dict mapping *substring patterns*
    to canned response strings. On each ``call``, scans the
    ``user_prompt`` for the first matching pattern and returns its
    canned response. Falls back to ``default`` if no pattern matches.

    Attributes:
        backend_id: Always ``"mock"``.
        responses: ``{substring_pattern: response_text}`` — first match
            wins (insertion order).
        default: Returned when no pattern matches the prompt.
        calls: Recorded ``LLMRequest``s for assertion in tests.
    """

    backend_id: str = "mock"

    def __init__(
        self,
        responses: dict[str, str] | None = None,
        *,
        default: str = "{}",
    ) -> None:
        self.responses: dict[str, str] = dict(responses) if responses else {}
        self.default: str = default
        self.calls: list[LLMRequest] = []

    def call(self, request: LLMRequest) -> LLMResponse:
        start = time.monotonic()
        self.calls.append(request)
        for pattern, response in self.responses.items():
            if pattern in request.user_prompt:
                return LLMResponse(
                    content=response,
                    elapsed_ms=(time.monotonic() - start) * 1000.0,
                    backend_id=self.backend_id,
                    metadata={"pattern_matched": pattern, "mock": True},
                )
        return LLMResponse(
            content=self.default,
            elapsed_ms=(time.monotonic() - start) * 1000.0,
            backend_id=self.backend_id,
            metadata={"pattern_matched": None, "mock": True},
        )


class AnthropicBackend:
    """Anthropic Messages API backend.

    Lazily imports ``anthropic`` so importing :mod:`tessellum.composer.llm`
    doesn't require the ``[agent]`` extras to be installed. The actual
    SDK import happens in ``__init__`` — instantiation is what triggers
    the dependency check.

    Attributes:
        backend_id: Always ``"anthropic"``.
        model: The Anthropic model ID (e.g. ``"claude-opus-4-7"``,
            ``"claude-sonnet-4-6"``, ``"claude-haiku-4-5-20251001"``).
        default_max_tokens: Used when ``LLMRequest.max_tokens`` is the
            default (4000) — kept identical for now; expose if profiling
            shows it matters.
        client: The ``anthropic.Anthropic`` instance. Reads
            ``ANTHROPIC_API_KEY`` from the environment by default.

    Example::

        from tessellum.composer import AnthropicBackend, run_pipeline
        backend = AnthropicBackend(model="claude-sonnet-4-6")
        run = run_pipeline(compiled, leaves=leaves, backend=backend, ...)
    """

    backend_id: str = "anthropic"

    def __init__(
        self,
        *,
        model: str = "claude-sonnet-4-6",
        api_key: str | None = None,
        default_max_tokens: int = 4000,
        client: object | None = None,
    ) -> None:
        """Construct an Anthropic-backed LLM backend.

        Args:
            model: Anthropic model ID. Defaults to Sonnet 4.6 — fast +
                capable, the right default for most Composer workloads.
                Pass an Opus model when reasoning depth matters.
            api_key: API key. Defaults to ``ANTHROPIC_API_KEY`` env var.
            default_max_tokens: Caps response length when the request
                doesn't specify (most ``LLMRequest``s leave the default).
            client: Optional pre-built ``anthropic.Anthropic`` instance —
                useful for tests (pass a fake client). When ``None``
                (default), constructs one from ``api_key``.

        Raises:
            ImportError: If the ``anthropic`` package isn't installed
                (``pip install tessellum[agent]``).
        """
        if client is None:
            try:
                import anthropic  # type: ignore[import-not-found]
            except ImportError as e:  # pragma: no cover — environment-dep
                raise ImportError(
                    "AnthropicBackend requires the `anthropic` package. "
                    "Install with: pip install tessellum[agent]"
                ) from e
            self.client = anthropic.Anthropic(api_key=api_key)
        else:
            self.client = client
        self.model = model
        self.default_max_tokens = default_max_tokens

    def call(self, request: LLMRequest) -> LLMResponse:
        start = time.monotonic()
        max_tokens = request.max_tokens or self.default_max_tokens
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=request.system_prompt,
            messages=[{"role": "user", "content": request.user_prompt}],
        )
        elapsed_ms = (time.monotonic() - start) * 1000.0
        content = _extract_text(response)
        metadata = {
            "model": getattr(response, "model", self.model),
            "stop_reason": getattr(response, "stop_reason", None),
        }
        usage = getattr(response, "usage", None)
        if usage is not None:
            metadata["input_tokens"] = getattr(usage, "input_tokens", None)
            metadata["output_tokens"] = getattr(usage, "output_tokens", None)
        return LLMResponse(
            content=content,
            elapsed_ms=elapsed_ms,
            backend_id=self.backend_id,
            metadata=metadata,
        )


def _extract_text(response: object) -> str:
    """Pull the text out of an Anthropic Messages API response.

    The SDK returns ``response.content`` as a list of content blocks
    (``TextBlock`` for ordinary replies, plus tool-use blocks etc.).
    We concatenate text blocks; non-text blocks are skipped.
    """
    blocks = getattr(response, "content", None)
    if blocks is None:
        return ""
    parts: list[str] = []
    for block in blocks:
        # Two access patterns: SDK objects use attribute access, our
        # test fakes may use dict access. Support both.
        block_type = getattr(block, "type", None)
        if block_type is None and isinstance(block, dict):
            block_type = block.get("type")
        if block_type == "text":
            text = getattr(block, "text", None)
            if text is None and isinstance(block, dict):
                text = block.get("text", "")
            if text:
                parts.append(text)
    return "".join(parts)


__all__ = [
    "LLMRequest",
    "LLMResponse",
    "LLMBackend",
    "MockBackend",
    "AnthropicBackend",
]
