from __future__ import annotations

from pathlib import Path
import threading

import pytest

from tessellum.runtime.tool_broker import ToolBroker, ToolPolicyError, ToolSpec


def test_broker_enforces_allowlist_schema_path_and_budget(tmp_path: Path) -> None:
    broker = ToolBroker(allowed={"read"}, workspace_root=tmp_path, max_calls=1)
    broker.register(
        ToolSpec(
            name="read",
            input_schema={
                "type": "object",
                "required": ["path"],
                "properties": {"path": {"type": "string"}},
            },
            handler=lambda args: Path(args["path"]).read_text(),
        )
    )
    note = tmp_path / "note.md"
    note.write_text("ok", encoding="utf-8")
    result = broker.call("read", {"path": str(note)})
    assert result.value == "ok"
    with pytest.raises(ToolPolicyError, match="budget"):
        broker.call("read", {"path": str(note)})


def test_broker_rejects_unauthorized_and_escaping_paths(tmp_path: Path) -> None:
    broker = ToolBroker(allowed={"read"}, workspace_root=tmp_path)
    broker.register(
        ToolSpec(
            name="read",
            input_schema={"type": "object"},
            handler=lambda args: args,
        )
    )
    with pytest.raises(ToolPolicyError, match="authorized"):
        broker.call("write", {})
    with pytest.raises(ToolPolicyError, match="escapes"):
        broker.call("read", {"source_path": "/etc/passwd"})


def test_broker_rejects_mutating_tools(tmp_path: Path) -> None:
    broker = ToolBroker(allowed={"write"}, workspace_root=tmp_path)
    with pytest.raises(ToolPolicyError, match="read-only"):
        broker.register(
            ToolSpec(
                name="write",
                input_schema={"type": "object"},
                handler=lambda args: args,
                read_only=False,
            )
        )


def test_broker_budget_is_atomic_across_threads(tmp_path: Path) -> None:
    broker = ToolBroker(allowed={"read"}, workspace_root=tmp_path, max_calls=1)
    release = threading.Event()
    broker.register(
        ToolSpec(
            name="read",
            input_schema={"type": "object"},
            handler=lambda _args: release.wait(1),
        )
    )
    errors: list[Exception] = []

    def call() -> None:
        try:
            broker.call("read", {})
        except Exception as exc:  # noqa: BLE001 - asserted below
            errors.append(exc)

    first = threading.Thread(target=call)
    second = threading.Thread(target=call)
    first.start()
    second.start()
    second.join(timeout=1)
    release.set()
    first.join(timeout=1)

    assert len(errors) == 1
    assert isinstance(errors[0], ToolPolicyError)
