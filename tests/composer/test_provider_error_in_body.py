"""A provider error relayed as a 200 body must be raised, not parsed as content.

Reproduces the failure that scored an empty wallet as a 74%-refusal vault: a
gateway returned "Insufficient balance. Your Cline Credits balance is $-0.04"
as the completion text of every call, nothing raised, and the string was
handed downstream as a note body.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from tessellum.composer.executor import (        # noqa: E402
    ProviderErrorInBody,
    _call_backend_with_timeout,
    _provider_error_in_body,
    classify_error,
)
from tessellum.composer.llm import LLMRequest, LLMResponse   # noqa: E402


class _Canned:
    def __init__(self, text: str):
        self.text = text

    def call(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(content=self.text, elapsed_ms=1.0, backend_id="canned")


def _req() -> LLMRequest:
    try:
        return LLMRequest(system_prompt="s", user_prompt="u")
    except TypeError:
        return LLMRequest(system_prompt="s", user_prompt="u")  # tolerate either field name


@pytest.mark.parametrize("body,expect", [
    ("Insufficient balance. Your Cline Credits balance is $-0.04", "quota"),
    ('{"error":{"code":"INFERENCE_CAP_ERROR","message":"Error 429: Daily free limit reached"}}', "rate_limit"),
    ("Your credit balance is too low to access the API. Please go to Plans & Billing.", "quota"),
])
def test_relayed_provider_errors_are_detected(body, expect):
    reason = _provider_error_in_body(body)
    assert reason is not None, body
    # classify_error folds quota into rate_limit; either is a fault, never content
    assert classify_error(body) in ("rate_limit", "auth", "transport", "crash", expect)


def test_real_note_content_is_not_flagged():
    note = ("# Google ad load\n\nThe Age reported on 2023-10-22 that Google's ad load "
            "varies with the request. The company's billing team was not involved. " * 6)
    assert _provider_error_in_body(note) is None, "a long real note must never be flagged"


def test_short_legitimate_answers_are_not_flagged():
    # INSUFFICIENT and "Insufficient information." are the abstention protocol,
    # not billing failures -- the exception-tuned taxonomy matches the bare word,
    # which is exactly why the body guard has its own stricter patterns.
    for ok in ("Sam Bankman-Fried", "INSUFFICIENT", "Insufficient information.",
               "INSUFFICIENT\n\nThe context does not contain it.", "Yes.", "No", "Google"):
        assert _provider_error_in_body(ok) is None, ok


def test_choke_point_raises_instead_of_returning_the_body():
    with pytest.raises(ProviderErrorInBody) as ei:
        _call_backend_with_timeout(
            _Canned("Insufficient balance. Your Cline Credits balance is $-0.04"),
            _req(), timeout_seconds=5)
    assert "quota" in str(ei.value) or "rate_limit" in str(ei.value)


def test_choke_point_passes_real_content_through():
    r = _call_backend_with_timeout(_Canned("TITLE: x\nBODY:\nreal note\nEND"), _req(), 5)
    assert r is not None and "real note" in r.content
