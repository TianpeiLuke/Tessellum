"""Wave 4 smoke — AnthropicBackend (no real network).

Tests inject a fake client object via the ``client=`` constructor arg so
the SDK doesn't need to be installed and no network call happens.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from tessellum.composer import (
    AnthropicBackend,
    LLMRequest,
    LLMResponse,
)


# ── Fake SDK objects ──────────────────────────────────────────────────────


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
    model: str = "claude-sonnet-4-6"
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
                usage=_FakeUsage(input_tokens=10, output_tokens=5),
            )
        return self.next_response


class _FakeClient:
    def __init__(self) -> None:
        self.messages = _FakeMessages()


# ── Tests ─────────────────────────────────────────────────────────────────


def test_anthropic_backend_id() -> None:
    fake = _FakeClient()
    backend = AnthropicBackend(client=fake)
    assert backend.backend_id == "anthropic"


def test_anthropic_default_model() -> None:
    fake = _FakeClient()
    backend = AnthropicBackend(client=fake)
    assert backend.model == "claude-sonnet-4-6"


def test_anthropic_custom_model() -> None:
    fake = _FakeClient()
    backend = AnthropicBackend(client=fake, model="claude-opus-4-7")
    assert backend.model == "claude-opus-4-7"


def test_anthropic_call_returns_llm_response() -> None:
    fake = _FakeClient()
    backend = AnthropicBackend(client=fake)
    request = LLMRequest(system_prompt="sys", user_prompt="user")
    response = backend.call(request)
    assert isinstance(response, LLMResponse)
    assert response.content == '{"ok": true}'
    assert response.backend_id == "anthropic"


def test_anthropic_call_passes_request_fields() -> None:
    fake = _FakeClient()
    backend = AnthropicBackend(client=fake, model="claude-haiku-4-5-20251001")
    request = LLMRequest(system_prompt="sys", user_prompt="user", max_tokens=2000)
    backend.call(request)
    call = fake.messages.calls[0]
    assert call["model"] == "claude-haiku-4-5-20251001"
    assert call["system"] == "sys"
    assert call["max_tokens"] == 2000
    assert call["messages"] == [{"role": "user", "content": "user"}]


def test_anthropic_metadata_includes_token_counts() -> None:
    fake = _FakeClient()
    backend = AnthropicBackend(client=fake)
    response = backend.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert response.metadata["model"] == "claude-sonnet-4-6"
    assert response.metadata["stop_reason"] == "end_turn"
    assert response.metadata["input_tokens"] == 10
    assert response.metadata["output_tokens"] == 5


def test_anthropic_extracts_multi_block_text() -> None:
    fake = _FakeClient()
    fake.messages.next_response = _FakeResponse(
        content=[
            _FakeTextBlock(type="text", text="hello "),
            _FakeTextBlock(type="text", text="world"),
        ]
    )
    backend = AnthropicBackend(client=fake)
    response = backend.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert response.content == "hello world"


def test_anthropic_skips_non_text_blocks() -> None:
    """Tool-use or other non-text blocks should be skipped, not crash."""
    fake = _FakeClient()
    fake.messages.next_response = _FakeResponse(
        content=[
            _FakeTextBlock(type="tool_use", text="ignored"),
            _FakeTextBlock(type="text", text="kept"),
        ]
    )
    backend = AnthropicBackend(client=fake)
    response = backend.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert response.content == "kept"


def test_anthropic_handles_dict_blocks() -> None:
    """The text extractor accepts dict-shaped blocks for fakes."""
    fake = _FakeClient()
    fake.messages.next_response = _FakeResponse(
        content=[
            {"type": "text", "text": "from dict"},
        ]
    )
    backend = AnthropicBackend(client=fake)
    response = backend.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert response.content == "from dict"


def test_anthropic_records_elapsed_ms() -> None:
    fake = _FakeClient()
    backend = AnthropicBackend(client=fake)
    response = backend.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert response.elapsed_ms >= 0


def test_anthropic_real_import_path() -> None:
    """If anthropic SDK is available, AnthropicBackend without `client=` should
    construct (no network call yet — no .call() invocation). Skip otherwise."""
    pytest.importorskip("anthropic")
    backend = AnthropicBackend(api_key="dummy-key-for-construction")
    assert backend.backend_id == "anthropic"
