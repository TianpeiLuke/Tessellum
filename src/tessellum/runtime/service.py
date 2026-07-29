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
    # T4 (FZ 20k9d6a) liveness: actively reap stranded leases on idle cycles.
    # claim_next reclaims lazily (before each claim), but with no incoming work
    # a dead worker's in_progress leaf would sit stranded — so on an idle cycle
    # (nothing to claim) we sweep expired leases so they requeue/dead-letter
    # instead of deadlocking. 0 disables the active sweep (lazy reclaim only).
    reap_seconds: float = 30.0

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
                    # No claimable work → this is exactly when a stranded lease
                    # would otherwise sit unreclaimed. Sweep, then wait.
                    if self.reap_seconds > 0:
                        self.supervisor.store.reap_expired_leases()
                    stopped.wait(self.scan_seconds)
        finally:
            signal.signal(signal.SIGTERM, prior_term)
            signal.signal(signal.SIGINT, prior_int)
