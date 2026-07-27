"""BedrockBackend smoke — Claude via Amazon Bedrock (no real network).

Tests inject a fake client via the ``client=`` constructor arg so the
SDK isn't needed and no AWS call happens. Bedrock-specific coverage: the
cross-region inference-profile default model, region metadata, and the
``aws_profile`` env-selection convenience — on top of the shared
``messages.create`` / text-extraction behaviour it inherits.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from tessellum.composer import (
    BedrockBackend,
    LLMRequest,
    LLMResponse,
)


@dataclass
class _FakeTextBlock:
    type: str
    text: str


@dataclass
class _FakeUsage:
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class _FakeResponse:
    content: list
    model: str = "us.anthropic.claude-sonnet-4-6"
    stop_reason: str = "end_turn"
    usage: _FakeUsage = field(default_factory=_FakeUsage)


class _FakeStream:
    """Context manager mirroring the SDK's ``messages.stream()`` — exposes
    ``get_final_message()`` returning the accumulated ``Message``."""

    def __init__(self, response: _FakeResponse) -> None:
        self._response = response

    def __enter__(self) -> "_FakeStream":
        return self

    def __exit__(self, *exc: Any) -> None:
        return None

    def get_final_message(self) -> _FakeResponse:
        return self._response


class _FakeMessages:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.stream_calls: list[dict[str, Any]] = []
        self.next_response: _FakeResponse | None = None

    def _resp(self) -> _FakeResponse:
        if self.next_response is None:
            return _FakeResponse(
                content=[_FakeTextBlock(type="text", text='{"ok": true}')],
                usage=_FakeUsage(input_tokens=7, output_tokens=3),
            )
        return self.next_response

    def create(self, **kwargs: Any) -> _FakeResponse:
        self.calls.append(kwargs)
        return self._resp()

    def stream(self, **kwargs: Any) -> _FakeStream:
        self.stream_calls.append(kwargs)
        return _FakeStream(self._resp())


class _FakeClient:
    def __init__(self) -> None:
        self.messages = _FakeMessages()


def test_bedrock_backend_id() -> None:
    backend = BedrockBackend(client=_FakeClient())
    assert backend.backend_id == "bedrock"


def test_bedrock_default_model_is_cross_region_profile() -> None:
    # The default MUST be the `us.`-prefixed inference profile — the bare
    # foundation-model id fails on-demand Bedrock invocation with a 400.
    backend = BedrockBackend(client=_FakeClient())
    assert backend.model == "us.anthropic.claude-sonnet-4-6"
    assert backend.model.startswith("us.")


def test_bedrock_default_region() -> None:
    backend = BedrockBackend(client=_FakeClient())
    assert backend.region == "us-east-1"


def test_bedrock_custom_model_and_region() -> None:
    backend = BedrockBackend(
        client=_FakeClient(), model="us.anthropic.claude-opus-4-7", region="us-west-2"
    )
    assert backend.model == "us.anthropic.claude-opus-4-7"
    assert backend.region == "us-west-2"


def test_bedrock_call_returns_llm_response() -> None:
    backend = BedrockBackend(client=_FakeClient())
    response = backend.call(LLMRequest(system_prompt="sys", user_prompt="user"))
    assert isinstance(response, LLMResponse)
    assert response.content == '{"ok": true}'
    assert response.backend_id == "bedrock"


def test_bedrock_call_passes_request_fields() -> None:
    fake = _FakeClient()
    backend = BedrockBackend(client=fake, model="us.anthropic.claude-haiku-4-5-20251001")
    backend.call(LLMRequest(system_prompt="sys", user_prompt="user", max_tokens=1500))
    call = fake.messages.calls[0]
    assert call["model"] == "us.anthropic.claude-haiku-4-5-20251001"
    assert call["system"] == "sys"
    assert call["max_tokens"] == 1500
    assert call["messages"] == [{"role": "user", "content": "user"}]


def test_bedrock_metadata_includes_region_and_tokens() -> None:
    backend = BedrockBackend(client=_FakeClient(), region="us-east-1")
    response = backend.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert response.metadata["region"] == "us-east-1"
    assert response.metadata["stop_reason"] == "end_turn"
    assert response.metadata["input_tokens"] == 7
    assert response.metadata["output_tokens"] == 3


def test_bedrock_extracts_multi_block_text() -> None:
    fake = _FakeClient()
    fake.messages.next_response = _FakeResponse(
        content=[
            _FakeTextBlock(type="text", text="hello "),
            _FakeTextBlock(type="text", text="bedrock"),
        ]
    )
    backend = BedrockBackend(client=fake)
    assert backend.call(LLMRequest(system_prompt="s", user_prompt="u")).content == "hello bedrock"


def test_bedrock_skips_non_text_blocks() -> None:
    fake = _FakeClient()
    fake.messages.next_response = _FakeResponse(
        content=[
            _FakeTextBlock(type="tool_use", text="ignored"),
            _FakeTextBlock(type="text", text="kept"),
        ]
    )
    backend = BedrockBackend(client=fake)
    assert backend.call(LLMRequest(system_prompt="s", user_prompt="u")).content == "kept"


def test_bedrock_aws_profile_sets_env(monkeypatch) -> None:
    """Passing aws_profile with a real (SDK) construction path sets
    AWS_PROFILE before the client reads the credential chain."""
    import os

    monkeypatch.delenv("AWS_PROFILE", raising=False)
    # Inject a client so no real AnthropicBedrock is built, but the
    # aws_profile env-set happens only on the client=None path — so assert
    # the injected-client path does NOT touch the env (no surprise mutation).
    BedrockBackend(client=_FakeClient(), aws_profile="should-not-apply")
    assert os.environ.get("AWS_PROFILE") is None


def test_bedrock_records_elapsed_ms() -> None:
    backend = BedrockBackend(client=_FakeClient())
    assert backend.call(LLMRequest(system_prompt="s", user_prompt="u")).elapsed_ms >= 0


# ── P1 (FZ 20k9c1a1a1b7c2g / E7/D4): mid-run credential auto-refresh ─────────

class _ExpiredThenOkMessages:
    """First call raises a 403 expired-token error; after the credential-refresh
    hook fires and the client is rebuilt, the next client's call succeeds."""

    def __init__(self, *, expired: bool) -> None:
        self.expired = expired
        self.calls = 0

    def create(self, **kwargs: Any) -> _FakeResponse:
        self.calls += 1
        if self.expired:
            raise RuntimeError(
                "PermissionDeniedError: Error code: 403 - "
                "{'message': 'The security token included in the request is expired'}"
            )
        return _FakeResponse(content=[_FakeTextBlock(type="text", text='{"ok": true}')])


class _ExpiredThenOkClient:
    def __init__(self, *, expired: bool) -> None:
        self.messages = _ExpiredThenOkMessages(expired=expired)


def test_bedrock_refreshes_credentials_and_retries_on_auth_error() -> None:
    """P1 (E7/D4): an expired-token 403 mid-run triggers the credential_refresh
    hook + a client rebuild + a single retry that succeeds."""
    expired_client = _ExpiredThenOkClient(expired=True)
    healthy_client = _ExpiredThenOkClient(expired=False)
    refreshed = {"n": 0}

    backend = BedrockBackend(client=expired_client)
    # Simulate a self-built client (so the P1 path is enabled) with a refresh hook
    # that "renews creds" and a _build_client that returns the healthy client.
    backend._injected_client = False
    backend.credential_refresh = lambda: refreshed.__setitem__("n", refreshed["n"] + 1)
    backend._build_client = lambda: healthy_client

    resp = backend.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert refreshed["n"] == 1, "credential_refresh must be invoked exactly once"
    assert backend.client is healthy_client, "client must be rebuilt after refresh"
    assert resp.content == '{"ok": true}', "the retry after refresh must succeed"


def test_bedrock_no_refresh_hook_reraises_auth_error() -> None:
    """Without a refresh hook (or with an injected client), an auth error
    propagates unchanged — no silent swallow, prior behaviour preserved."""
    backend = BedrockBackend(client=_ExpiredThenOkClient(expired=True))
    with pytest.raises(RuntimeError, match="security token .* expired"):
        backend.call(LLMRequest(system_prompt="s", user_prompt="u"))


def test_bedrock_refresh_not_triggered_on_non_auth_error() -> None:
    """A non-auth error must NOT trigger the refresh/retry (don't mask real
    bugs); it re-raises and the hook is never called."""
    class _BoomMessages:
        def create(self, **kwargs: Any):
            raise ValueError("some non-auth failure")

    class _BoomClient:
        def __init__(self) -> None:
            self.messages = _BoomMessages()

    called = {"n": 0}
    backend = BedrockBackend(client=_BoomClient())
    backend._injected_client = False
    backend.credential_refresh = lambda: called.__setitem__("n", called["n"] + 1)
    with pytest.raises(ValueError, match="non-auth failure"):
        backend.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert called["n"] == 0, "non-auth error must not trigger a credential refresh"


# ── E15 (FZ 20k9c1a1a1b7c2g): stream above the SDK non-streaming ceiling ─────

def test_bedrock_small_max_tokens_uses_create_not_stream() -> None:
    """At/below the non-streaming ceiling the backend uses messages.create —
    byte-identical to prior behaviour (all existing callers use ≤16000)."""
    fake = _FakeClient()
    backend = BedrockBackend(client=fake)
    backend.call(LLMRequest(system_prompt="s", user_prompt="u", max_tokens=16000))
    assert len(fake.messages.calls) == 1
    assert len(fake.messages.stream_calls) == 0


def test_bedrock_large_max_tokens_routes_to_stream() -> None:
    """Above the SDK's ~21.3K non-streaming ceiling (the big-output writers set
    32000, E14/R3), the backend MUST stream — else messages.create raises
    'Streaming is required for operations that may take longer than 10 minutes'
    before sending. Asserts the stream path + that the final message is used."""
    fake = _FakeClient()
    backend = BedrockBackend(client=fake)
    resp = backend.call(LLMRequest(system_prompt="s", user_prompt="u", max_tokens=32000))
    assert len(fake.messages.stream_calls) == 1, "large max_tokens must use messages.stream()"
    assert len(fake.messages.calls) == 0, "must NOT call the guarded messages.create()"
    assert fake.messages.stream_calls[0]["max_tokens"] == 32000
    assert resp.content == '{"ok": true}'  # get_final_message() text extracted normally
    assert resp.metadata["stop_reason"] == "end_turn"


def test_bedrock_real_import_path() -> None:
    """If the anthropic SDK is available, BedrockBackend without client=
    constructs (AnthropicBedrock is lazily built; no network yet). The
    aws_profile arg sets AWS_PROFILE. Skip if the SDK is absent."""
    pytest.importorskip("anthropic")
    import os

    prior = os.environ.get("AWS_PROFILE")
    try:
        backend = BedrockBackend(aws_profile="test-bedrock-profile", region="us-east-1")
        assert backend.backend_id == "bedrock"
        assert os.environ["AWS_PROFILE"] == "test-bedrock-profile"
    finally:
        if prior is None:
            os.environ.pop("AWS_PROFILE", None)
        else:
            os.environ["AWS_PROFILE"] = prior
