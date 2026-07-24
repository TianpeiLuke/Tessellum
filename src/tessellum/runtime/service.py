"""Foreground automatic runtime service with graceful shutdown."""

from __future__ import annotations

import signal
import threading
from dataclasses import dataclass

from tessellum.runtime.inbox import InboxScanner
from tessellum.runtime.supervisor import Supervisor


@dataclass
class RuntimeService:
    scanner: InboxScanner
    supervisor: Supervisor
    scan_seconds: float = 2.0

    def run(self) -> None:
        stopped = threading.Event()

        def _stop(_signum, _frame) -> None:
            stopped.set()

        prior_term = signal.signal(signal.SIGTERM, _stop)
        prior_int = signal.signal(signal.SIGINT, _stop)
        try:
            while not stopped.is_set():
                self.scanner.scan_once()
                outcome = self.supervisor.work_once()
                if outcome.status == "idle":
                    stopped.wait(self.scan_seconds)
        finally:
            signal.signal(signal.SIGTERM, prior_term)
            signal.signal(signal.SIGINT, prior_int)
