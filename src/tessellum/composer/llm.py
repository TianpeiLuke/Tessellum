"""LLM backend abstraction.

A backend is *just* a callable — given an :class:`LLMRequest` (system
prompt + user prompt + max_tokens), return an :class:`LLMResponse`
(content + timing + diagnostic metadata). All backends declared in
:data:`tessellum.composer.contracts.BACKEND_CONTRACTS` should match
this shape; the compiler validates the contract; the executor invokes
the ``call`` method.

Four backends ship:

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
- :class:`ClineBackend` — one-shot completions through the ``cline`` CLI
  (a subprocess; no SDK, no key). Reaches whatever provider ``cline auth``
  is logged into — by default the cline gateway fronting DeepSeek's free
  tier — so digestion and the answer-level eval stay runnable when every
  paid key is out of credit.
"""

from __future__ import annotations

import inspect
import json
import math
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Protocol

from tessellum.composer.error_taxonomy import is_auth as _is_auth


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



# R2.3 (FZ 20k9c1a1a1b7c2k2a1b): the transport timeout constants — hoisted so
# the timing assertion table (runtime/timing.py) can bind the step watchdog to
# them instead of three files sharing a coincidental 300.
CONNECT_TIMEOUT_S: float = 30.0
READ_TIMEOUT_S: float = 300.0
"""Per CHUNK GAP on a stream — a healthy multi-minute generation is unaffected;
a silent stream raises within this bound for the ladder to classify."""
WRITE_TIMEOUT_S: float = 60.0
POOL_TIMEOUT_S: float = 60.0


def _anthropic_httpx_module(anthropic_mod):
    """Return the httpx module the installed anthropic SDK is built against.

    anthropic >= the httpx2 migration imports ``httpx2`` and rejects
    ``httpx.Timeout``; older releases use ``httpx``. Prefer whichever the SDK's
    own base client references, then fall back by import order.
    """
    import importlib
    base = getattr(anthropic_mod, "_base_client", None)
    for attr in ("httpx", "httpx2"):
        mod = getattr(base, attr, None) if base is not None else None
        if mod is not None and hasattr(mod, "Timeout"):
            return mod
    for name in ("httpx2", "httpx"):
        try:
            mod = importlib.import_module(name)
        except ImportError:
            continue
        # only accept the module the SDK will not reject
        try:
            anthropic_mod.Anthropic(api_key="probe", max_retries=0,
                                    timeout=mod.Timeout(1.0))
            return mod
        except TypeError:
            continue
        except Exception:
            return mod   # constructed past the timeout check; that is the match
    import httpx  # last resort; matches every SDK that predates httpx2
    return httpx


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
            # The SDK rejects a Timeout object from the WRONG httpx: newer
            # releases vendor `httpx2` and raise "`httpx.Timeout` is from the
            # `httpx` package, but this SDK uses `httpx2`" on a plain
            # `import httpx`. Resolve the transport module the installed SDK
            # actually uses rather than hard-coding either name.
            httpx = _anthropic_httpx_module(anthropic)
            # J3 finding 5 (FZ 20k9c1a1a1b7c2k2): the first live runtime wave
            # wedged for 60+ minutes on FOUR silent stalled HTTPS streams —
            # ESTABLISHED sockets, no data, no timeout firing, every worker
            # thread parked, zero CPU (E7's API-side sibling: an unattended
            # run must never be able to hang unboundedly on one request).
            # Explicit httpx timeouts bound every phase of a request — read
            # is PER CHUNK GAP on a stream, so a healthy multi-minute
            # generation is unaffected while a silent stream raises within
            # 300s and the retry ladder (which owns ALL retry semantics —
            # hence max_retries=0, the SDK's hidden internal retries would
            # double the blip-rider's budget) classifies + retries it.
            self.client = anthropic.Anthropic(
                api_key=api_key,
                max_retries=0,
                timeout=httpx.Timeout(
                    connect=CONNECT_TIMEOUT_S, read=READ_TIMEOUT_S,
                    write=WRITE_TIMEOUT_S, pool=POOL_TIMEOUT_S,
                ),
            )
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
        response = _messages_create_or_stream(
            self.client, model=self.model, max_tokens=max_tokens,
            system_prompt=request.system_prompt, user_prompt=request.user_prompt,
            extra=extra,
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
        credential_refresh: "Callable[[], None] | None" = None,
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
            credential_refresh: Optional zero-arg callable that renews the
                ambient AWS credentials (e.g. re-invokes ``ada credentials
                update``). **P1 / FZ 20k9c1a1a1b7c2g (E7/D4):** federated
                Bedrock creds are short-lived (~15–30 min); a long digestion
                run (the big streamed writers legitimately take minutes each)
                outlives one window and a late phase fails with a 403
                ``security token expired``. When set, ``call`` catches an
                auth-class failure, invokes this hook, **rebuilds the client**
                so it re-reads the renewed profile, and retries the request
                ONCE. Fail-soft: if the hook raises or the retry still fails,
                the original error propagates (no retry-budget burn on a
                known-expired token). ``None`` → prior behaviour (no refresh).

        Raises:
            ImportError: If the ``anthropic`` package isn't installed
                (``pip install tessellum[agent]``).
        """
        self.model = model
        self.region = region
        self.aws_profile = aws_profile
        self.default_max_tokens = default_max_tokens
        self.credential_refresh = credential_refresh
        self._injected_client = client is not None
        self.client = client if client is not None else self._build_client()

    def _build_client(self) -> object:
        """Construct a fresh ``AnthropicBedrock`` reading the ambient (possibly
        just-renewed) AWS credential chain. Rebuilt after a credential refresh so
        the new token is picked up (P1)."""
        if self.aws_profile is not None:
            import os

            os.environ["AWS_PROFILE"] = self.aws_profile
        try:
            from anthropic import AnthropicBedrock  # type: ignore[import-not-found]
        except ImportError as e:  # pragma: no cover — environment-dep
            raise ImportError(
                "BedrockBackend requires the `anthropic` package. "
                "Install with: pip install tessellum[agent]"
            ) from e
        return AnthropicBedrock(aws_region=self.region)

    def call(self, request: LLMRequest) -> LLMResponse:
        start = time.monotonic()
        max_tokens = request.max_tokens or self.default_max_tokens
        # temperature only passed when the caller set it — omitting it preserves
        # the provider default (byte-identical for every existing caller).
        extra = {} if request.temperature is None else {"temperature": request.temperature}
        try:
            response = _messages_create_or_stream(
                self.client, model=self.model, max_tokens=max_tokens,
                system_prompt=request.system_prompt, user_prompt=request.user_prompt,
                extra=extra,
            )
        except Exception as e:  # noqa: BLE001
            # P1 (E7/D4): on an AUTH failure (expired federated token mid-run),
            # renew creds via the hook, rebuild the client so it re-reads the new
            # token, and retry ONCE. Fail-soft — re-raise the ORIGINAL error if
            # there is no hook, the client was injected (a test fake), the refresh
            # raises, or the retry still fails, so a non-auth error or a truly-dead
            # credential doesn't silently loop.
            if (
                self.credential_refresh is None
                or self._injected_client
                or not _is_auth_error(e)
            ):
                raise
            try:
                self.credential_refresh()
                self.client = self._build_client()
                response = _messages_create_or_stream(
                    self.client, model=self.model, max_tokens=max_tokens,
                    system_prompt=request.system_prompt, user_prompt=request.user_prompt,
                    extra=extra,
                )
            except Exception:
                raise e from None
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


# ── ClineBackend — one-shot completions through the `cline` CLI ──────────────

DEFAULT_CLINE_MODEL = "deepseek/deepseek-v4-flash"
"""The provider model id ``cline -m`` gets by default: DeepSeek V4 Flash on
the cline gateway's free tier — the one LLM path that costs nothing."""

DEFAULT_CLINE_TIMEOUT_S: float = 90.0
"""Per-call subprocess timeout. Deliberately SHORT: a wedged cline hub daemon
makes every call hang indefinitely, and a long per-call timeout turns that
into a run that never finishes rather than one that fails and is retried."""

# A single argv string is capped at 128KB on Linux (MAX_ARG_STRLEN); a
# digestion prompt carrying a whole source document can exceed that. Above this
# bound the prompt's tail is piped on stdin instead — cline concatenates an
# argv prompt with piped stdin as ``f"{argv} {stdin.strip()}"``, so the split
# lands on a single space and the model sees the original prompt.
_CLINE_ARGV_PROMPT_MAX_BYTES = 100_000

# Mirrors executor._PROVIDER_ERROR_BODY_MAX_CHARS (not imported: executor
# imports this module). A relayed refusal is a sentence; a real answer that
# merely MENTIONS "401 Unauthorized" is long, and must not be raised as one.
_CLINE_REFUSAL_ECHO_MAX_CHARS = 600


class ClineBackendError(RuntimeError):
    """The ``cline`` CLI did not produce a usable answer.

    Raised — never returned as content — so the executor's retry ladder and
    :func:`~tessellum.composer.error_taxonomy.classify_reason` see a real
    exception. The message carries the taxonomy token for the cause
    (``Unauthorized`` → ``auth``; ``rate limit`` → ``rate_limit``;
    ``timed out`` → ``stall``/transient) so the ladder picks the right rung.
    """


def _cline_run_result(stdout: str) -> dict | None:
    """The LAST ``{"type": "run_result", ...}`` JSON line in ``stdout``.

    cline ``--json`` streams one JSON object per line: reasoning / text chunks
    as the model produces them, then a final ``run_result`` carrying the
    answer (``text``), ``finishReason``, ``model`` and usage. Non-JSON lines
    and any other message type are skipped, so a reasoning model's scratchpad
    is never mistaken for the answer.
    """
    result: dict | None = None
    for raw in stdout.splitlines():
        line = raw.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and obj.get("type") == "run_result":
            result = obj
    return result


def _cline_failure_signal(stdout: str, stderr: str) -> str:
    """The parts of cline's output where a FAILURE is reported.

    All of stderr (in ``--json`` mode cline writes ``{"type": "error",
    "message": ...}`` lines there), plus every stdout line that is not a JSON
    message or is a ``type: "error"`` one. Streamed model text is excluded on
    purpose: a note ABOUT ``401 Unauthorized`` must not be raised as one.
    """
    parts: list[str] = [stderr]
    for raw in stdout.splitlines():
        line = raw.strip()
        if not line:
            continue
        if not line.startswith("{"):
            parts.append(line)
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            parts.append(line)
            continue
        if isinstance(obj, dict) and obj.get("type") == "error":
            parts.append(line)
    return "\n".join(parts)


def _cline_refusal_marker(text: str) -> str | None:
    """The provider-fault token present in ``text`` (taxonomy-classifiable), or None.

    Covers what cline ACTUALLY emits when the gateway rejects a call, not just
    the two tokens the reference harness happened to see. A live probe returned
    ``{"error":{"code":"INFERENCE_CAP_ERROR","message":"Error 429: Daily free
    limit reached ..."}}`` as the run_result text with ``finishReason: "error"``
    -- neither "unauthorized" nor "rate limit" appears in it, so the first cut
    of this function let it through as content. The returned token is chosen
    so ``error_taxonomy.classify_reason`` maps it: 429 -> rate_limit.
    """
    low = text.lower().lstrip()
    if "unauthorized" in low:
        return "Unauthorized"
    if ("rate limit" in low or "rate_limit" in low or "ratelimit" in low
            or "429" in low or "daily free limit" in low or "inference_cap" in low
            or "too many requests" in low):
        return "rate limit 429"
    if low.startswith('{"error"') or low.startswith("{'error'"):
        return "rate limit 429"        # a gateway error envelope is never an answer
    if "insufficient balance" in low or "credits balance" in low or "billing" in low:
        return "quota insufficient balance"
    return None


def _split_prompt_for_argv(prompt: str) -> tuple[str, str | None]:
    """``(argv_prompt, stdin_tail)`` — the tail is ``None`` when the whole
    prompt fits one argv string.

    Two facts about the installed cline (3.0.61, read from the binary) decide
    the shape of this function. First, it joins the argv prompt and a piped
    stdin tail with a DOUBLE NEWLINE -- ``f"{prompt}\n\n{stdin.strip()}"`` --
    not a space, so the cut must land on an existing paragraph break or the
    join inserts a spurious one mid-table, mid-fence or mid-line. Second, the
    128KB per-argument cap (``MAX_ARG_STRLEN``) is Linux-only; macOS has no
    per-arg limit, so spilling there turns a prompt that would have arrived
    intact into an altered one. The spill is therefore gated on Linux.
    """
    encoded = prompt.encode("utf-8")
    if len(encoded) <= _CLINE_ARGV_PROMPT_MAX_BYTES or not sys.platform.startswith("linux"):
        return prompt, None
    head = encoded[:_CLINE_ARGV_PROMPT_MAX_BYTES].decode("utf-8", errors="ignore")
    cut = head.rfind("\n\n")
    if cut <= 0:
        cut = head.rfind("\n")
    if cut <= 0:
        cut = head.rfind(" ")
    if cut <= 0:
        cut = len(head)
    tail = prompt[cut:].strip()
    return prompt[:cut].rstrip("\n"), (tail or None)


class ClineBackend:
    """One-shot completion through the ``cline`` CLI (a subprocess, no SDK).

    WHY: every other real backend needs a paid key or an AWS role. ``cline``
    logs into the cline gateway with its own OAuth flow and fronts DeepSeek's
    free tier, so this is the one path that keeps digestion — and the
    answer-level eval of Tessellum's own output — runnable at zero cost when
    the Anthropic key is out of credit. Ported from the benchmark harness'
    ``ask_cline`` (``slipbox-benchmark-eval/scripts/answer_eval.py``), which
    learned every rule below the hard way.

    cline is an agent, not a completion endpoint, so three flags force it to
    behave as one: ``--cwd`` points at an EMPTY sandbox so a stray tool call
    cannot touch the repo; ``--auto-approve false`` stops it acting on one;
    ``-s`` replaces its coding system prompt with the request's. It still
    bills ~7,000 tokens of tool schemas per call regardless — constant, but
    the reason a run is not cheap.

    NEVER pass ``--data-dir``. Credentials live in the default
    ``~/.cline/data``; pointing ``--data-dir`` at any other path creates empty
    state whose every call returns ``Unauthorized`` — which silently hung two
    benchmark runs before the cause was found. Isolation is enforced by
    ``--cwd`` instead, which is what actually bounds file access.

    Output is JSON lines on stdout; the answer is the ``text`` of the final
    ``run_result`` line (its ``finishReason`` becomes ``stop_reason``).
    Streamed reasoning lines are ignored. cline reports failures as
    ``{"type": "error"}`` lines on STDERR in ``--json`` mode, so both streams
    are scanned for ``Unauthorized`` / ``rate limit`` and the call RAISES
    :class:`ClineBackendError` on them (and on a non-zero exit with empty
    stdout, on a missing ``run_result``, and on timeout) — never returns the
    error text as content, so the executor's retry ladder and
    ``error_taxonomy.classify_reason`` see a real exception. The executor's
    own 200-body guard remains the backstop for anything subtler.

    stdin is ``/dev/null`` unless the prompt overflows argv: cline reads a
    non-TTY stdin to EOF, so an inherited open pipe (an orchestrator, cron)
    would otherwise stall every call until the timeout.

    ``max_tokens`` / ``temperature``: cline exposes NO flag for either (see
    ``cline --help``), so ``LLMRequest.max_tokens`` and ``.temperature`` are
    not honoured — the provider's defaults apply. The requested cap is echoed
    in ``metadata["max_tokens_requested"]`` for the trace.

    Attributes:
        backend_id: Always ``"cline"``.
        model: Provider model id passed as ``-m``.
        provider: cline provider id passed as ``-P``.
        sandbox: The EMPTY directory handed to ``--cwd`` (created on demand).
        timeout_s: Per-call subprocess timeout; also passed to cline as ``-t``.
        cline_bin: Resolved absolute path of the cline executable.

    Example::

        from tessellum.composer import ClineBackend, run_pipeline
        backend = ClineBackend()          # deepseek/deepseek-v4-flash via cline
        run = run_pipeline(compiled, leaves=leaves, backend=backend, ...)
    """

    backend_id: str = "cline"

    def __init__(
        self,
        *,
        model: str = DEFAULT_CLINE_MODEL,
        provider: str = "cline",
        sandbox: Path | None = None,
        timeout_s: float = DEFAULT_CLINE_TIMEOUT_S,
        cline_bin: str = "cline",
    ) -> None:
        """Construct a cline-backed LLM backend.

        Args:
            model: Provider model id (``cline -m``). Default: DeepSeek V4
                Flash — the free tier.
            provider: cline provider id (``cline -P``). Default ``"cline"``,
                the cline gateway; must be one ``cline auth`` is logged into.
            sandbox: EMPTY directory for ``--cwd``. ``None`` → a fixed
                ``tessellum-cline-sandbox`` under the system temp dir, shared
                across workers (cline keys sessions per run, so sharing is
                safe; ``--cwd`` is what bounds file access, not state).
            timeout_s: Per-call subprocess timeout — keep it SHORT (see
                :data:`DEFAULT_CLINE_TIMEOUT_S`). Passed to cline as ``-t``
                rounded up to whole seconds.
            cline_bin: The executable: a name on ``PATH`` or an absolute
                path. Resolved here so a missing install fails at
                construction, like the SDK-backed siblings, not mid-run.

        Raises:
            FileNotFoundError: If ``cline_bin`` cannot be resolved.
        """
        resolved = shutil.which(cline_bin)
        if resolved is None:
            raise FileNotFoundError(
                f"ClineBackend requires the `cline` CLI (looked for {cline_bin!r}). "
                "Install it, put it on PATH (or pass cline_bin=<absolute path>), "
                "and log in with `cline auth`."
            )
        self.cline_bin: str = resolved
        self.model = model
        self.provider = provider
        self.sandbox: Path = (
            Path(sandbox).expanduser()
            if sandbox is not None
            else Path(tempfile.gettempdir()) / "tessellum-cline-sandbox"
        )
        self.timeout_s = float(timeout_s)

    def build_command(self, request: LLMRequest) -> tuple[list[str], str | None]:
        """``(argv, stdin_text)`` for one request — exposed for inspection.

        ``stdin_text`` is ``None`` (stdin will be ``/dev/null``) unless the
        user prompt overflows one argv string, in which case its tail is
        piped and cline re-joins the two on a single space.
        """
        argv_prompt, stdin_tail = _split_prompt_for_argv(request.user_prompt)
        argv = [
            self.cline_bin,
            "-P", self.provider,
            "--cwd", str(self.sandbox),
            "--auto-approve", "false",
            "-t", str(max(1, math.ceil(self.timeout_s))),
            "--json",
            "-s", request.system_prompt,
        ]
        if self.model:
            argv += ["-m", self.model]
        argv.append(argv_prompt)
        return argv, stdin_tail

    def call(self, request: LLMRequest) -> LLMResponse:
        start = time.monotonic()
        self.sandbox.mkdir(parents=True, exist_ok=True)
        argv, stdin_tail = self.build_command(request)
        stdin_kw: dict = (
            {"input": stdin_tail} if stdin_tail is not None
            else {"stdin": subprocess.DEVNULL}
        )
        try:
            proc = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
                cwd=str(self.sandbox),
                **stdin_kw,
            )
        except subprocess.TimeoutExpired as e:
            raise ClineBackendError(
                f"cline timed out after {self.timeout_s:g}s (model={self.model}); "
                "a wedged cline hub daemon hangs every call -- restart it "
                "before retrying"
            ) from e
        except OSError as e:
            raise ClineBackendError(f"cline could not be launched: {e}") from e
        elapsed_ms = (time.monotonic() - start) * 1000.0
        stdout, stderr = proc.stdout or "", proc.stderr or ""

        result = _cline_run_result(stdout)
        text = (result.get("text") or "").strip() if result is not None else ""

        # A substantive answer wins: a full note body that mentions "401
        # Unauthorized" is content, and a warning line printed on the way to
        # one is not a refusal. Anything shorter is checked as a relayed
        # error — the exact shape the --data-dir failure took.
        if len(text) <= _CLINE_REFUSAL_ECHO_MAX_CHARS:
            signal = _cline_failure_signal(stdout, stderr)
            marker = _cline_refusal_marker(signal) or _cline_refusal_marker(text)
            if marker is None and text.lower().startswith("error:"):
                marker = "error"
            if marker is not None:
                excerpt = (text or signal).strip()[:200]
                raise ClineBackendError(
                    f"cline backend refused the call ({marker}; rc={proc.returncode}): "
                    f"{excerpt}"
                )
        if result is None:
            if proc.returncode != 0 and not stdout.strip():
                raise ClineBackendError(
                    f"cline exited rc={proc.returncode} with empty stdout: "
                    f"{stderr.strip()[:200]}"
                )
            raise ClineBackendError(
                f"cline gave no run_result (rc={proc.returncode}): "
                f"{stderr.strip()[:200] or stdout.strip()[-200:]}"
            )
        stop_reason = result.get("finishReason") or result.get("stop_reason")
        if not text:
            raise ClineBackendError(
                f"cline returned an empty run_result (rc={proc.returncode}, "
                f"finishReason={stop_reason!r}): {stderr.strip()[:200]}"
            )
        # A run_result whose finishReason is "error" is a FAILED call whatever
        # its text says. Verified live: a daily-cap 429 arrives exactly this way,
        # with the JSON envelope as the text and total_cost 0. Returning it as
        # content is the failure this backend exists to prevent, and one that
        # answer_eval.py -- which calls backend.call() directly, bypassing the
        # executor's body guard -- would then score as an answer.
        if isinstance(stop_reason, str) and stop_reason.lower() == "error":
            marker = _cline_refusal_marker(text) or "rate limit 429"
            raise ClineBackendError(
                f"cline run_result finishReason='error' ({marker}): {text.strip()[:200]}"
            )

        metadata: dict = {
            "model": result.get("model") or self.model,
            "provider": self.provider,
            "elapsed": round(elapsed_ms / 1000.0, 3),
            "max_tokens_requested": request.max_tokens,
        }
        if stop_reason is not None:
            metadata["stop_reason"] = stop_reason
        usage = result.get("aggregateUsage") or result.get("usage") or {}
        if isinstance(usage, dict) and usage.get("totalCost") is not None:
            metadata["total_cost"] = usage.get("totalCost")
        return LLMResponse(
            content=text,
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


# The Anthropic SDK refuses a NON-streaming request whose max_tokens implies a
# possible >10-min response: it raises ``ValueError: Streaming is required …``
# BEFORE sending (_base_client._calculate_nonstreaming_timeout: the guard trips
# when ``3600 * max_tokens / 128_000 > 600`` → ``max_tokens > 21_333``). Our
# big-output writers set ``max_tokens=32000`` (E14/R3), which trips it. So above
# the ceiling we route through the streaming API and accumulate the final message
# — same ``Message`` shape ``_extract_text`` + the metadata read already expect.
# Below the ceiling we keep ``messages.create`` (byte-identical for every prior
# caller, all of which use the 16000 default).
_NONSTREAMING_MAX_TOKENS = 21_000  # conservatively under the SDK's 21_333 guard


def _accepted_extra(client: object, extra: dict) -> dict:
    """Keep only the ``extra`` kwargs the client's ``messages.create`` accepts.

    anthropic SDK versions differ in their sampling-param surface — 1.4.0 has no
    ``temperature`` and its ``create`` takes no ``**kwargs``, so an unrecognised
    key raises ``TypeError`` and (on Bedrock) fails every call. This introspects
    the signature once per call and drops unsupported keys. If the signature
    exposes ``**kwargs`` (VAR_KEYWORD) or cannot be read, ``extra`` is returned
    unchanged — the SDK will absorb or validate it as before.
    """
    try:
        sig = inspect.signature(client.messages.create)  # type: ignore[attr-defined]
    except (TypeError, ValueError, AttributeError):
        return extra
    params = sig.parameters
    if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values()):
        return extra
    kept = {k: v for k, v in extra.items() if k in params}
    return kept


def _messages_create_or_stream(
    client: object,
    *,
    model: str,
    max_tokens: int,
    system_prompt: str,
    user_prompt: str,
    extra: dict,
) -> object:
    """Call the Anthropic Messages API, streaming iff ``max_tokens`` would trip
    the SDK's non-streaming 10-minute guard. Returns the final ``Message``."""
    messages = [{"role": "user", "content": user_prompt}]
    # SDK-surface drift: `messages.create` accepts different sampling params
    # across anthropic versions (1.4.0 has no `temperature` at all, and its
    # `create` takes no `**kwargs`, so passing one raises TypeError). Drop any
    # `extra` key the installed SDK's signature does not accept — the provider
    # default is used for it — so a temperature-setting caller (e.g. the answer
    # eval) does not turn every Bedrock call into a transport failure. When the
    # signature can't be introspected or accepts arbitrary kwargs, pass through.
    if extra:
        extra = _accepted_extra(client, extra)
    if max_tokens > _NONSTREAMING_MAX_TOKENS:
        # Streaming path: the context manager accumulates the final Message,
        # which carries the same content/stop_reason/usage a create() returns.
        with client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages,
            **extra,
        ) as stream:
            return stream.get_final_message()
    return client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=messages,
        **extra,
    )


def _is_auth_error(exc: Exception) -> bool:
    """True if an exception is an auth/credential failure (expired token, 403,
    unauthorized, access/permission denied) — the class the P1 credential-refresh
    retry targets.

    P18 (FZ 20k9c1a1a1b7c2f): defers to the canonical
    :func:`~tessellum.composer.error_taxonomy.is_auth`, the SAME token heuristic
    ``executor.classify_error`` and ``credential_pool.classify_rotation_cause``
    project their ``auth`` class from — so the three agree by construction. This
    previously hand-mirrored a subset that OMITTED ``accessdenied``, so a bare
    ``AccessDenied`` (auth in the pool) was not-auth here and the refresh never
    fired on the exact failure it exists to catch."""
    return _is_auth(f"{type(exc).__name__}: {exc}")


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
    "ClineBackend",
    "ClineBackendError",
    "PooledBackend",
]
