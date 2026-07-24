"""Policy-bound tool execution independent of Composer's tool-free backend."""

from __future__ import annotations

import hashlib
import json
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import jsonschema


class ToolPolicyError(PermissionError):
    pass


@dataclass(frozen=True)
class ToolSpec:
    name: str
    input_schema: dict
    handler: Callable[[dict[str, Any]], Any]
    read_only: bool = True
    timeout_seconds: float = 30.0
    max_output_bytes: int = 1_000_000


@dataclass(frozen=True)
class ToolCallResult:
    call_id: str
    tool_name: str
    value: Any
    result_hash: str
    duration_ms: float


class ToolBroker:
    def __init__(
        self,
        *,
        allowed: set[str],
        workspace_root: Path | str,
        max_calls: int = 20,
    ) -> None:
        self.allowed = frozenset(allowed)
        self.workspace_root = Path(workspace_root).expanduser().resolve()
        self.max_calls = max_calls
        self._calls = 0
        self._tools: dict[str, ToolSpec] = {}
        self._lock = threading.Lock()

    def register(self, spec: ToolSpec) -> None:
        if not spec.read_only:
            raise ToolPolicyError(
                "mutating tools require a transactional executor; "
                "the standalone broker accepts read-only tools only"
            )
        with self._lock:
            self._tools[spec.name] = spec

    def call(self, name: str, arguments: dict[str, Any]) -> ToolCallResult:
        with self._lock:
            if name not in self.allowed or name not in self._tools:
                raise ToolPolicyError(f"tool not authorized: {name}")
            if self._calls >= self.max_calls:
                raise ToolPolicyError("tool invocation budget exhausted")
            spec = self._tools[name]
        jsonschema.validate(arguments, spec.input_schema)
        self._reject_unsafe_paths(arguments)
        with self._lock:
            if self._calls >= self.max_calls:
                raise ToolPolicyError("tool invocation budget exhausted")
            self._calls += 1
        started = time.monotonic()
        pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="tool-broker")
        future = pool.submit(spec.handler, arguments)
        try:
            value = future.result(timeout=spec.timeout_seconds)
        except TimeoutError as exc:
            future.cancel()
            # Python cannot kill a running thread. Wait before returning so a
            # timed-out trusted read cannot continue after the caller recovers.
            pool.shutdown(wait=True, cancel_futures=True)
            raise ToolPolicyError(f"tool timed out: {name}") from exc
        except BaseException:
            pool.shutdown(wait=True, cancel_futures=True)
            raise
        else:
            pool.shutdown(wait=True)
        encoded = json.dumps(value, sort_keys=True, default=str).encode("utf-8")
        if len(encoded) > spec.max_output_bytes:
            raise ToolPolicyError(f"tool output exceeds byte limit: {name}")
        return ToolCallResult(
            call_id=uuid.uuid4().hex,
            tool_name=name,
            value=value,
            result_hash=hashlib.sha256(encoded).hexdigest(),
            duration_ms=(time.monotonic() - started) * 1000.0,
        )

    def _reject_unsafe_paths(self, value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key.endswith("path") and isinstance(child, str):
                    resolved = Path(child).expanduser().resolve()
                    try:
                        resolved.relative_to(self.workspace_root)
                    except ValueError as exc:
                        raise ToolPolicyError(
                            f"path escapes workspace: {child}"
                        ) from exc
                self._reject_unsafe_paths(child)
        elif isinstance(value, list):
            for child in value:
                self._reject_unsafe_paths(child)
