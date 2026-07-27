"""LLM backend abstraction.

A backend is *just* a callable — given an :class:`LLMRequest` (system
prompt + user prompt + max_tokens), return an :class:`LLMResponse`
(content + timing + diagnostic metadata). All backends declared in
:data:`tessellum.composer.contracts.BACKEND_CONTRACTS` should match
this shape; the compiler validates the contract; the executor invokes
the ``call`` method.

Three backends ship:

- :class:`MockBackend` — canned responses, no network. Makes the
  executor + scheduler testable end-to-end without API keys.
- :class:`AnthropicBackend` — production Anthropic Messages API
  client. Available with the ``[agent]`` extras::

      pip install tessellum[agent]

  and ``ANTHROPIC_API_KEY`` in the environment.
- :class:`BedrockBackend` — the same Claude Messages surface via Amazon
  Bedrock (``anthropic.AnthropicBedrock``), authenticated by the ambient
  AWS credential chain (``AWS_PROFILE``) rather than an API key. The right
  choice for AWS-internal deployments.
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
        max_tokens: Cap on response length. Defaults to 16000 — the digestion
            steps that emit a full plan body (``write_plan``), the planned-notes
            table + coverage map (``decompose``), or a complete note body
            (``dispatch_notes``) routinely exceed a few thousand output tokens;
            the previous 4000 default truncated their JSON mid-string, so the
            response failed to parse. 16000 is comfortably above what these
            steps need and well within the model's output limit.
        temperature: Sampling temperature. ``None`` (default) → the provider
            default is used (unchanged behavior for every existing caller).
            A caller that needs reproducible / low-variance output (e.g. the
            calibrated entailment scorer, where calibration↔runtime score
            stability is a load-bearing assumption) sets ``0.0``.
    """

    system_prompt: str
    user_prompt: str
    max_tokens: int = 16000
    temperature: float | None = None


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
            default (16000) — sized for full plan/note-body generation
            (see :class:`LLMRequest`).
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
        default_max_tokens: int = 16000,
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
        # temperature only passed when the caller set it — omitting it preserves
        # the provider default (byte-identical for every existing caller).
        extra = {} if request.temperature is None else {"temperature": request.temperature}
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=request.system_prompt,
            messages=[{"role": "user", "content": request.user_prompt}],
            **extra,
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


class BedrockBackend:
    """Amazon Bedrock backend for Claude models (AWS-authenticated).

    A sibling of :class:`AnthropicBackend` that talks to Bedrock instead
    of the Anthropic API. It uses ``anthropic.AnthropicBedrock``, which
    exposes the **identical** ``messages.create`` surface — so the
    ``call`` body + :func:`_extract_text` are shared behaviour, only the
    client and authentication differ. Authentication is via the ambient
    AWS credential chain (``AWS_PROFILE`` / env / instance role) rather
    than an API key, so no secret is passed or stored here.

    Lazily imports ``anthropic`` so importing this module doesn't require
    the ``[agent]`` extras; instantiation triggers the dependency check.

    Attributes:
        backend_id: Always ``"bedrock"``.
        model: A Bedrock model ID. **Use a cross-region inference-profile
            id** (prefixed ``us.`` / ``eu.`` / ``apac.``, e.g.
            ``"us.anthropic.claude-sonnet-4-6"``) — bare foundation-model
            ids reject on-demand invocation with a 400. The default is the
            ``us.`` Sonnet profile.
        region: AWS region for the Bedrock endpoint.
        client: The ``anthropic.AnthropicBedrock`` instance.

    Auth: the backend reads the ambient AWS credential chain — no account
    id, role, or secret is embedded here. Point ``AWS_PROFILE`` at a
    profile that can invoke Bedrock (e.g. refreshed via your org's
    federated-credential tool into a named profile) before running::

        export AWS_PROFILE=<your-bedrock-profile>

    Example::

        from tessellum.composer import BedrockBackend, run_pipeline
        backend = BedrockBackend(model="us.anthropic.claude-sonnet-4-6",
                                 region="us-east-1")
        run = run_pipeline(compiled, leaves=leaves, backend=backend, ...)
    """

    backend_id: str = "bedrock"

    def __init__(
        self,
        *,
        model: str = "us.anthropic.claude-sonnet-4-6",
        region: str = "us-east-1",
        aws_profile: str | None = None,
        default_max_tokens: int = 16000,
        client: object | None = None,
    ) -> None:
        """Construct a Bedrock-backed LLM backend.

        Args:
            model: Bedrock model / inference-profile id. Prefer the
                cross-region profile form (``us.anthropic.…``) — the bare
                foundation-model id fails on-demand invocation with a 400.
            region: AWS region (default ``us-east-1``).
            aws_profile: If set, selects a specific credentials profile by
                setting ``AWS_PROFILE`` before the client reads the chain
                (a convenience for the ``ada ... --profile X`` workflow).
                When ``None``, the ambient credential chain is used as-is.
            default_max_tokens: Caps response length when the request
                leaves it at the default.
            client: Optional pre-built ``anthropic.AnthropicBedrock`` (or a
                fake) — used by tests. When ``None``, one is constructed.

        Raises:
            ImportError: If the ``anthropic`` package isn't installed
                (``pip install tessellum[agent]``).
        """
        if client is None:
            if aws_profile is not None:
                import os

                os.environ["AWS_PROFILE"] = aws_profile
            try:
                from anthropic import AnthropicBedrock  # type: ignore[import-not-found]
            except ImportError as e:  # pragma: no cover — environment-dep
                raise ImportError(
                    "BedrockBackend requires the `anthropic` package. "
                    "Install with: pip install tessellum[agent]"
                ) from e
            self.client = AnthropicBedrock(aws_region=region)
        else:
            self.client = client
        self.model = model
        self.region = region
        self.default_max_tokens = default_max_tokens

    def call(self, request: LLMRequest) -> LLMResponse:
        start = time.monotonic()
        max_tokens = request.max_tokens or self.default_max_tokens
        # temperature only passed when the caller set it — omitting it preserves
        # the provider default (byte-identical for every existing caller).
        extra = {} if request.temperature is None else {"temperature": request.temperature}
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=request.system_prompt,
            messages=[{"role": "user", "content": request.user_prompt}],
            **extra,
        )
        elapsed_ms = (time.monotonic() - start) * 1000.0
        content = _extract_text(response)
        metadata = {
            "model": getattr(response, "model", self.model),
            "region": self.region,
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


class PooledBackend:
    """Wraps an inner backend with a :class:`CredentialPool` — leases a key
    per call, rotates + benches a key that a provider rejects.

    This is the *which-key* dimension complementing the retry ladder's
    *when-to-retry* dimension. On each :meth:`call` it leases the
    least-used available key from the pool, applies it to the inner
    backend via the injected ``key_applier``, and dispatches. On a clean
    return it releases the lease. On a raised exception it classifies the
    cause (:func:`classify_rotation_cause`) and reports it to the pool —
    a persistent rate-limit / quota / auth fault **benches + releases**
    the key (so the next attempt leases a *different* one), while a
    transient blip keeps the lease — then **re-raises** so the executor's
    retry ladder handles the retry as usual. Multi-worker safe: the pool's
    per-key leasing under a lock stops two workers from double-driving one
    key onto a shared 429 wall.

    ``key_applier`` is injected because *how* a key attaches is
    provider-specific (an API-key env var vs an AWS profile) and must not
    leak into this module. It receives ``(inner_backend, key_id)`` and
    mutates/configures the inner backend to use that key before the call.

    Attributes:
        backend_id: ``"pooled:<inner.backend_id>"``.
        inner: The wrapped backend that actually calls the provider.
        pool: The :class:`CredentialPool` of key ids.
        worker_id: This worker's id (for lease ownership). Defaults to a
            per-instance uuid.

    Example::

        pool = CredentialPool(key_ids=("k1", "k2", "k3"))
        def apply(inner, key_id):        # deployment-specific
            inner.client = anthropic.Anthropic(api_key=SECRETS[key_id])
        backend = PooledBackend(AnthropicBackend(client=...), pool, apply)
    """

    def __init__(
        self,
        inner: "LLMBackend",
        pool,
        key_applier,
        *,
        worker_id: str | None = None,
        clock=None,
    ) -> None:
        """Construct a pooled backend.

        Args:
            inner: The backend that performs the actual provider call.
            pool: A :class:`tessellum.composer.credential_pool.CredentialPool`.
            key_applier: ``(inner, key_id) -> None`` — attaches the leased
                key to ``inner`` before the call (provider-specific).
            worker_id: Lease-ownership id. Defaults to a fresh uuid.
            clock: Zero-arg ``() -> float`` epoch-seconds source (for the
                pool's cooldown timestamps). Defaults to ``time.monotonic``.
        """
        import uuid as _uuid

        self.inner = inner
        self.pool = pool
        self._apply = key_applier
        self.worker_id = worker_id or _uuid.uuid4().hex
        self._clock = clock or time.monotonic
        self.backend_id = f"pooled:{getattr(inner, 'backend_id', 'inner')}"

    def call(self, request: LLMRequest) -> LLMResponse:
        from tessellum.composer.credential_pool import classify_rotation_cause

        now = self._clock()
        key_id = self.pool.lease(self.worker_id, now)
        self._apply(self.inner, key_id)
        try:
            response = self.inner.call(request)
        except Exception as e:  # noqa: BLE001 — rotate/bench then re-raise
            cause = classify_rotation_cause(f"{type(e).__name__}: {e}")
            # report_failure benches+releases on a hard cause; on a transient
            # cause it keeps the lease, so release it explicitly to return
            # the key to the pool for the retry.
            benched = self.pool.report_failure(key_id, self.worker_id, cause, self._clock())
            if not benched:
                self.pool.release(key_id, self.worker_id)
            raise
        self.pool.release(key_id, self.worker_id)
        # Tag which key served the call (diagnostics; key ids are not secrets).
        return LLMResponse(
            content=response.content,
            elapsed_ms=response.elapsed_ms,
            backend_id=self.backend_id,
            metadata={**response.metadata, "credential_key": key_id},
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
    "BedrockBackend",
    "PooledBackend",
]
