"""``tessellum runtime`` durable automatic-ingestion operations."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path

from tessellum.composer.manifest import Manifest
from tessellum.runtime.admission import AdmissionError, admit_path
from tessellum.runtime.executor import BackendConfig, DigestionExecutor, build_backend
from tessellum.runtime.inbox import InboxScanner
from tessellum.runtime.models import Job, JobState, TERMINAL_STATES
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.routing import LANE_HINTS
from tessellum.runtime.service import RuntimeService
from tessellum.runtime.store import RuntimeStore, TransitionError
from tessellum.runtime.supervisor import Supervisor


def _add_common_paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--db", type=Path, default=None)


def _add_backend(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--backend", choices=["mock", "anthropic", "bedrock"], default="mock")
    parser.add_argument("--model")
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--aws-profile")
    parser.add_argument("--mock-responses", type=Path)


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    runtime = subparsers.add_parser(
        "runtime",
        help="Durable automatic inbox ingestion and job operations.",
    )
    sub = runtime.add_subparsers(dest="runtime_command", required=True)

    init = sub.add_parser("init", help="Initialize runtime DB and inbox lanes.")
    _add_common_paths(init)
    init.set_defaults(func=run_runtime_init)

    submit = sub.add_parser("submit", help="Durably submit one existing inbox file.")
    submit.add_argument("path", type=Path)
    submit.add_argument("--settle-seconds", type=float, default=0.0)
    submit.add_argument(
        "--profile", default=None,
        help="Runtime policy profile for this job (default/fast/inspect/converge).",
    )
    _add_common_paths(submit)
    submit.set_defaults(func=run_runtime_submit)

    work = sub.add_parser("work", help="Claim and execute one durable job.")
    work.add_argument("--no-index", action="store_true")
    _add_common_paths(work)
    _add_backend(work)
    work.set_defaults(func=run_runtime_work)

    serve = sub.add_parser("serve", help="Continuously scan inbox and supervise jobs.")
    serve.add_argument("--scan-seconds", type=float, default=2.0)
    serve.add_argument("--settle-seconds", type=float, default=1.0)
    serve.add_argument("--no-index", action="store_true")
    _add_common_paths(serve)
    _add_backend(serve)
    serve.set_defaults(func=run_runtime_serve)

    get = sub.add_parser("get", help="Get one durable job.")
    get.add_argument("job_id")
    get.add_argument("--events", action="store_true")
    _add_common_paths(get)
    get.set_defaults(func=run_runtime_get)

    list_cmd = sub.add_parser("list", help="List durable jobs.")
    list_cmd.add_argument("--state", action="append", choices=[s.value for s in JobState])
    list_cmd.add_argument("--limit", type=int, default=100)
    _add_common_paths(list_cmd)
    list_cmd.set_defaults(func=run_runtime_list)

    status = sub.add_parser(
        "status",
        help="Live task-manager view: per-job phase + per-leaf digestion status.",
    )
    status.add_argument(
        "--job", help="Drill into ONE job: its phase, per-leaf manifest rows, event tail."
    )
    status.add_argument(
        "--watch", action="store_true", help="Re-poll and redraw every --interval seconds."
    )
    status.add_argument("--interval", type=float, default=2.0)
    status.add_argument("--limit", type=int, default=100)
    status.add_argument("--json", action="store_true", help="Emit JSON (implies no --watch redraw loop).")
    _add_common_paths(status)
    status.set_defaults(func=run_runtime_status)

    cancel = sub.add_parser("cancel", help="Request cooperative job cancellation.")
    cancel.add_argument("job_id")
    cancel.add_argument(
        "--force", action="store_true",
        help="Fence the worker out (bump lease generation) + mark cancelled — "
             "the escalation when a worker ignores the cooperative signal.",
    )
    _add_common_paths(cancel)
    cancel.set_defaults(func=run_runtime_cancel)

    plan = sub.add_parser(
        "plan", help="Show the accepted plan of an inspected (paused) job."
    )
    plan.add_argument("job_id")
    _add_common_paths(plan)
    plan.set_defaults(func=run_runtime_plan)

    promote = sub.add_parser(
        "promote", help="Promote an inspected (paused) job into its execute wave."
    )
    promote.add_argument("job_id")
    _add_common_paths(promote)
    promote.set_defaults(func=run_runtime_promote)

    reject = sub.add_parser(
        "reject", help="Reject an inspected (paused) job — discard its plan, cancel."
    )
    reject.add_argument("job_id")
    _add_common_paths(reject)
    reject.set_defaults(func=run_runtime_reject)

    retry = sub.add_parser(
        "retry",
        help="Create a linked retry of a cancelled or dead-letter job.",
    )
    retry.add_argument("job_id")
    _add_common_paths(retry)
    retry.set_defaults(func=run_runtime_retry)

    doctor = sub.add_parser("doctor", help="Check runtime paths and capabilities.")
    _add_common_paths(doctor)
    doctor.set_defaults(func=run_runtime_doctor)


def _paths(args: argparse.Namespace) -> RuntimePaths:
    paths = RuntimePaths.discover(args.root)
    if args.db is not None:
        paths = RuntimePaths(
            **{
                **asdict(paths),
                "db": args.db.expanduser().resolve(),
            }
        )
    return paths


def _store(args: argparse.Namespace) -> tuple[RuntimePaths, RuntimeStore]:
    paths = _paths(args)
    paths.ensure_runtime_dirs()
    return paths, RuntimeStore.open(paths.db)


def _backend_config(args: argparse.Namespace) -> BackendConfig:
    responses = None
    if getattr(args, "mock_responses", None) is not None:
        responses = json.loads(args.mock_responses.read_text(encoding="utf-8"))
    return BackendConfig(
        kind=args.backend,
        model=args.model,
        region=args.region,
        aws_profile=args.aws_profile,
        mock_responses=responses,
    )


def _job_payload(job: Job) -> dict:
    return {
        "job_id": job.job_id,
        "state": job.state.value,
        "lane": job.request.lane,
        "source_event_id": job.request.source_event_id,
        "payload_ref": job.request.payload_ref,
        "capability": job.capability,
        "attempts": job.attempts,
        "commit_attempts": job.commit_attempts,
        "cancel_requested": job.cancel_requested,
        "last_error": job.last_error,
        "result_path": job.result_path,
        "supersedes_job_id": job.supersedes_job_id,
        "lease": (
            None
            if job.lease is None
            else {
                "owner_id": job.lease.owner_id,
                "generation": job.lease.generation,
                "expires_at": job.lease.expires_at,
            }
        ),
    }


def run_runtime_init(args: argparse.Namespace) -> int:
    paths, _store_instance = _store(args)
    paths.inbox.mkdir(parents=True, exist_ok=True)
    for lane in LANE_HINTS:
        (paths.inbox / lane).mkdir(parents=True, exist_ok=True)
    print(json.dumps({"db": str(paths.db), "inbox": str(paths.inbox)}, indent=2))
    return 0


def run_runtime_submit(args: argparse.Namespace) -> int:
    paths, store = _store(args)
    try:
        job, created = admit_path(
            args.path,
            paths=paths,
            store=store,
            settle_seconds=args.settle_seconds,
            policy_profile=getattr(args, "profile", None),
        )
    except (AdmissionError, OSError) as exc:
        print(f"tessellum runtime submit: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({**_job_payload(job), "created": created}, indent=2))
    return 0


def _supervisor(args: argparse.Namespace) -> tuple[RuntimePaths, RuntimeStore, Supervisor]:
    paths, store = _store(args)
    backend = build_backend(_backend_config(args))
    executor = DigestionExecutor(
        paths=paths,
        backend=backend,
        cancellation_check=lambda: False,
    )
    return paths, store, Supervisor(
        store=store,
        paths=paths,
        executor=executor,
        rebuild_index=not args.no_index,
    )


def run_runtime_work(args: argparse.Namespace) -> int:
    _paths_value, _store_value, supervisor = _supervisor(args)
    outcome = supervisor.work_once()
    print(json.dumps(asdict(outcome), indent=2))
    return 1 if outcome.status in {"dead_letter", "lease_lost"} else 0


def run_runtime_serve(args: argparse.Namespace) -> int:
    paths, store, supervisor = _supervisor(args)
    scanner = InboxScanner(
        paths=paths,
        store=store,
        settle_seconds=args.settle_seconds,
    )
    RuntimeService(
        scanner=scanner,
        supervisor=supervisor,
        scan_seconds=args.scan_seconds,
    ).run()
    return 0


def run_runtime_get(args: argparse.Namespace) -> int:
    _paths_value, store = _store(args)
    job = store.get(args.job_id)
    if job is None:
        print(f"job not found: {args.job_id}", file=sys.stderr)
        return 1
    payload = _job_payload(job)
    if args.events:
        payload["events"] = [asdict(event) for event in store.events(job.job_id)]
    print(json.dumps(payload, indent=2))
    return 0


def run_runtime_list(args: argparse.Namespace) -> int:
    _paths_value, store = _store(args)
    states = None if not args.state else [JobState(value) for value in args.state]
    print(
        json.dumps(
            [_job_payload(job) for job in store.list(states=states, limit=args.limit)],
            indent=2,
        )
    )
    return 0


def _leaf_status_for_job(paths: RuntimePaths, job_id: str) -> dict | None:
    """The per-leaf digestion status for a job, from its durable manifest
    (``runs/artifacts/<job_id>/manifest.json``) — the surface the execute wave
    delta-patches. Returns ``None`` when no manifest exists yet (a job still in
    the plan/augment/review phases hasn't fanned out to leaves). Read-only:
    loads a COPY, never writes (T1, FZ 20k9d6a)."""
    manifest_path = paths.job_artifacts(job_id) / "manifest.json"
    if not manifest_path.is_file():
        return None
    manifest = Manifest.load(manifest_path)
    now = time.time()
    leaves = []
    for leaf_id, entry in sorted(manifest.entries.items()):
        leaves.append({
            "leaf_id": leaf_id,
            "status": entry.status,
            "attempts": len(entry.attempts),
            "heartbeat_age": (round(now - entry.heartbeat, 1)
                              if entry.heartbeat is not None else None),
            "run_id": entry.run_id,
            "blocked_by": list(entry.blocked_by),
        })
    return {"counts": manifest.status_counts(), "leaves": leaves}


def _composer_status_for_job(paths: RuntimePaths, job_id: str) -> dict | None:
    """J1 (FZ 20k9c1a1a1b7c2k2): the composer-grain episodic view — the same
    surface the executor writes under the job dir (``runs/``): the latest
    plan-of-record checkpoint (which phase fold the run last completed) and the
    attempts-journal tail (per-attempt retry-ladder evidence). This is what
    turns a silent multi-phase wedge (the third eval run's ~65-minute
    credential wall) into a live, attempt-grain diagnosis. Read-only and
    fail-soft: absent files (a pre-J1 job, or a run before its first fold) →
    ``None``."""
    runs = paths.job_artifacts(job_id) / "runs"
    out: dict = {}
    try:
        checkpoints = sorted(p.name for p in (runs / "checkpoints").glob("*.json"))
    except OSError:
        checkpoints = []
    if checkpoints:
        out["checkpoint"] = checkpoints[-1].rsplit(".", 1)[0]
        out["checkpoints"] = len(checkpoints)
    try:
        lines = (runs / "attempts.jsonl").read_text(encoding="utf-8").splitlines()
    except OSError:
        lines = []
    if lines:
        kinds: dict = {}
        last_failure = None
        for line in lines:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            kind = str(rec.get("kind"))
            kinds[kind] = kinds.get(kind, 0) + 1
            if kind != "success":
                last_failure = {
                    "step": rec.get("section_id"),
                    "kind": kind,
                    "attempt": rec.get("attempt"),
                    "error": (str(rec.get("error"))[:120]
                              if rec.get("error") is not None else None),
                }
        out["attempts"] = {"total": len(lines), "kinds": kinds}
        if last_failure is not None:
            out["attempts"]["last_failure"] = last_failure
    return out or None


def _status_row(job: Job, now: float) -> dict:
    """A compact per-job status row: phase (state), age, lease + expiry flag."""
    lease = job.lease
    expired = lease is not None and lease.expires_at < now
    return {
        "job_id": job.job_id,
        "phase": job.state.value,
        "lane": job.request.lane,
        "attempts": job.attempts,
        "cancel_requested": job.cancel_requested,
        "lease_owner": None if lease is None else lease.owner_id,
        "lease_expires_in": (None if lease is None else round(lease.expires_at - now, 1)),
        "lease_expired": expired,
        "generation": job.execution_generation,
        "last_error": job.last_error,
    }


def _render_status(paths: RuntimePaths, store: RuntimeStore, args: argparse.Namespace) -> dict:
    now = time.time()
    if args.job:
        job = store.get(args.job)
        if job is None:
            return {"error": f"job not found: {args.job}"}
        row = _status_row(job, now)
        row["leaves"] = _leaf_status_for_job(paths, job.job_id)
        row["composer"] = _composer_status_for_job(paths, job.job_id)
        row["events"] = [
            {"seq": e.sequence, "type": e.event_type, "at": e.at, "detail": e.detail}
            for e in store.events(job.job_id, limit=args.limit)
        ]
        return row
    # Aggregate: active (non-terminal) jobs first, most-recent first.
    jobs = store.list(limit=args.limit)
    active = [j for j in jobs if j.state not in TERMINAL_STATES]
    terminal = [j for j in jobs if j.state in TERMINAL_STATES]
    return {
        "now": now,
        "active": [_status_row(j, now) for j in active],
        "terminal_recent": [_status_row(j, now) for j in terminal[:10]],
        "counts": {"active": len(active), "terminal": len(terminal)},
    }


def _print_status_human(snapshot: dict) -> None:
    if "error" in snapshot:
        print(snapshot["error"], file=sys.stderr)
        return
    if "phase" in snapshot:  # single-job drill-down
        print(f"job {snapshot['job_id']}  phase={snapshot['phase']}  "
              f"attempts={snapshot['attempts']}  gen={snapshot['generation']}"
              + ("  CANCEL-REQUESTED" if snapshot["cancel_requested"] else ""))
        lease_owner = snapshot["lease_owner"]
        if lease_owner is not None:
            flag = "  EXPIRED" if snapshot["lease_expired"] else ""
            print(f"  lease: {lease_owner}  expires_in={snapshot['lease_expires_in']}s{flag}")
        comp = snapshot.get("composer")
        if comp:
            att = comp.get("attempts") or {}
            bits = []
            if comp.get("checkpoint"):
                bits.append(f"checkpoint={comp['checkpoint']} ({comp['checkpoints']} folds)")
            if att:
                bits.append(f"attempts={att['total']} {att['kinds']}")
            print("  composer: " + "  ".join(bits))
            failure = att.get("last_failure")
            if failure:
                print(f"    last-failure: [{failure['kind']}] {failure['step']}"
                      f"  attempt={failure['attempt']}  {failure['error'] or ''}")
        leaves = snapshot.get("leaves")
        if leaves is None:
            print("  leaves: (none yet — job is pre-execute)")
        else:
            print(f"  leaves: {leaves['counts']}")
            for lf in leaves["leaves"]:
                hb = f" hb={lf['heartbeat_age']}s" if lf["heartbeat_age"] is not None else ""
                print(f"    [{lf['status']:11}] {lf['leaf_id']}  attempts={lf['attempts']}{hb}")
        evs = snapshot.get("events") or []
        if evs:
            print(f"  recent events (last {min(5, len(evs))}):")
            for e in evs[-5:]:
                print(f"    #{e['seq']} {e['type']}")
        return
    # aggregate
    c = snapshot["counts"]
    print(f"jobs: {c['active']} active, {c['terminal']} terminal")
    for r in snapshot["active"]:
        flag = "  EXPIRED-LEASE" if r["lease_expired"] else ""
        cr = "  CANCEL-REQ" if r["cancel_requested"] else ""
        print(f"  {r['phase']:11} {r['job_id']}  lane={r['lane']}  "
              f"attempts={r['attempts']}{flag}{cr}")
    if not snapshot["active"]:
        print("  (no active jobs)")


def run_runtime_status(args: argparse.Namespace) -> int:
    paths, store = _store(args)
    if args.json or not args.watch:
        snapshot = _render_status(paths, store, args)
        if args.json:
            print(json.dumps(snapshot, indent=2))
        else:
            _print_status_human(snapshot)
        return 1 if "error" in snapshot else 0
    # --watch: redraw until interrupted (read-only polling never perturbs a run).
    try:
        while True:
            snapshot = _render_status(paths, store, args)
            print("\033[2J\033[H", end="")  # clear + home
            print(f"tessellum runtime status  (watch, every {args.interval}s — Ctrl-C to stop)\n")
            _print_status_human(snapshot)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        return 0


def run_runtime_cancel(args: argparse.Namespace) -> int:
    _paths_value, store = _store(args)
    try:
        if getattr(args, "force", False):
            job = store.force_cancel(args.job_id)
        else:
            job = store.request_cancel(args.job_id)
    except KeyError:
        print(f"job not found: {args.job_id}", file=sys.stderr)
        return 1
    print(json.dumps(_job_payload(job), indent=2))
    return 0


def run_runtime_plan(args: argparse.Namespace) -> int:
    paths, store = _store(args)
    job = store.get(args.job_id)
    if job is None:
        print(f"job not found: {args.job_id}", file=sys.stderr)
        return 1
    plan_path = paths.job_artifacts(job.job_id) / "plan.json"
    if not plan_path.is_file():
        print(f"no accepted plan for job {args.job_id} (not inspected/paused yet)",
              file=sys.stderr)
        return 1
    print(plan_path.read_text(encoding="utf-8"))
    return 0


def run_runtime_promote(args: argparse.Namespace) -> int:
    _paths_value, store = _store(args)
    try:
        job = store.promote_paused(args.job_id)
    except KeyError:
        print(f"job not found: {args.job_id}", file=sys.stderr)
        return 1
    except TransitionError as exc:
        print(f"tessellum runtime promote: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(_job_payload(job), indent=2))
    return 0


def run_runtime_reject(args: argparse.Namespace) -> int:
    _paths_value, store = _store(args)
    try:
        job = store.reject_paused(args.job_id)
    except KeyError:
        print(f"job not found: {args.job_id}", file=sys.stderr)
        return 1
    except TransitionError as exc:
        print(f"tessellum runtime reject: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(_job_payload(job), indent=2))
    return 0


def run_runtime_retry(args: argparse.Namespace) -> int:
    _paths_value, store = _store(args)
    try:
        job = store.retry_terminal(args.job_id)
    except (KeyError, TransitionError) as exc:
        print(f"tessellum runtime retry: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(_job_payload(job), indent=2))
    return 0


def run_runtime_doctor(args: argparse.Namespace) -> int:
    paths, store = _store(args)
    checks = {
        "runtime_db": paths.db.is_file(),
        "vault": paths.vault.is_dir(),
        "inbox": paths.inbox.is_dir(),
        "skills": paths.skills.is_dir(),
        "index_parent_writable": (
            paths.index_db.parent.is_dir()
            and os.access(paths.index_db.parent, os.W_OK)
        ),
        "jobs_readable": isinstance(store.list(limit=1), list),
    }
    print(json.dumps({"paths": {k: str(v) for k, v in asdict(paths).items()}, "checks": checks}, indent=2))
    return 0 if all(checks.values()) else 1
