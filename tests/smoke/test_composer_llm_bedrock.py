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


class _FakeMessages:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.next_response: _FakeResponse | None = None

    def create(self, **kwargs: Any) -> _FakeResponse:
        self.calls.append(kwargs)
        if self.next_response is None:
            return _FakeResponse(
                content=[_FakeTextBlock(type="text", text='{"ok": true}')],
                usage=_FakeUsage(input_tokens=7, output_tokens=3),
            )
        return self.next_response


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
