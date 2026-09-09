"""_accepted_extra: drop sampling kwargs the installed SDK's messages.create
does not accept, so SDK-surface drift (anthropic 1.4.0 has no `temperature`
and no **kwargs) does not turn every Bedrock call into a TypeError."""

from __future__ import annotations

from tessellum.composer.llm import _accepted_extra


class _Msgs:
    def __init__(self, fn):
        self.create = fn


class _Client:
    def __init__(self, fn):
        self.messages = _Msgs(fn)


def test_drops_unsupported_kwarg():
    # SDK like anthropic 1.4.0: create has NO temperature and NO **kwargs.
    def create(self=None, *, model, max_tokens, messages, system=None,
               stop_sequences=None):  # noqa: ANN001
        ...
    client = _Client(create)
    assert _accepted_extra(client, {"temperature": 0.0}) == {}
    assert _accepted_extra(client, {"stop_sequences": ["x"], "temperature": 0.0}) == {"stop_sequences": ["x"]}


def test_keeps_supported_kwarg():
    def create(self=None, *, model, max_tokens, messages, system=None,
               temperature=None):  # noqa: ANN001
        ...
    client = _Client(create)
    assert _accepted_extra(client, {"temperature": 0.0}) == {"temperature": 0.0}


def test_passes_through_on_var_keyword():
    # A create() that accepts **kwargs must NOT have keys stripped.
    def create(self=None, *, model, max_tokens, messages, **kwargs):  # noqa: ANN001
        ...
    client = _Client(create)
    assert _accepted_extra(client, {"temperature": 0.0}) == {"temperature": 0.0}


def test_passes_through_when_signature_unreadable():
    class _Weird:
        # a non-callable messages.create → signature() raises → pass through
        messages = _Msgs(object())
    assert _accepted_extra(_Weird(), {"temperature": 0.0}) == {"temperature": 0.0}
