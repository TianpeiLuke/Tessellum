"""``tessellum runtime`` durable automatic-ingestion operations."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path

from tessellum.runtime.admission import AdmissionError, admit_path
from tessellum.runtime.executor import BackendConfig, DigestionExecutor, build_backend
from tessellum.runtime.inbox import InboxScanner
from tessellum.runtime.models import Job, JobState
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

    cancel = sub.add_parser("cancel", help="Request cooperative job cancellation.")
    cancel.add_argument("job_id")
    _add_common_paths(cancel)
    cancel.set_defaults(func=run_runtime_cancel)

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


def run_runtime_cancel(args: argparse.Namespace) -> int:
    _paths_value, store = _store(args)
    try:
        job = store.request_cancel(args.job_id)
    except KeyError:
        print(f"job not found: {args.job_id}", file=sys.stderr)
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
