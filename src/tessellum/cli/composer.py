"""``tessellum composer …`` — Composer pipeline operations.

Seven subcommands as of v0.0.43:

    validate <skill>          Schema + cross-file consistency (Wave 1a / 1b).
    compile <skill>           Compile to a typed DAG with contract checks (Wave 2).
    run <skill>               Execute the compiled pipeline against leaves (Wave 3).
    batch <jobs.json>         Run many (skill, leaves) jobs in parallel (Wave 5a).
    eval <scenarios>          Run scenario assertions + LLMJudge rubric (Wave 5b).
    scaffold-sidecar <skill>  Generate a starter pipeline sidecar from a canonical's section anchors.
    dks <observations.jsonl>  Run a multi-cycle DKS session (Phase 3, v0.0.43+).

Exit codes:
    0  every skill validates / compiles / runs clean
    1  at least one skill fails (validation, compilation, or execution)
    2  invocation error (path doesn't exist, etc.)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tessellum.composer import (
    BatchJob,
    CompilerError,
    ContractViolation,
    DKSObservation,
    DKSRunner,
    EvalError,
    LLMBackend,
    LLMJudge,
    MockBackend,
    PipelineValidationError,
    aggregate_warrant_changes,
    allocate_cycle_fz,
    compile_skill,
    load_pipeline,
    load_scenarios,
    run_batch,
    run_eval,
    run_pipeline,
    to_dag_json,
)


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    composer = subparsers.add_parser(
        "composer",
        help="Composer pipeline operations (validate, compile, ...).",
    )
    composer_sub = composer.add_subparsers(dest="composer_command", required=True)

    validate = composer_sub.add_parser(
        "validate",
        help="Validate a skill canonical's pipeline sidecar against the spec.",
    )
    validate.add_argument(
        "skill",
        type=Path,
        help="Skill canonical (markdown file) or directory to recurse over.",
    )
    validate.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    validate.set_defaults(func=run_composer_validate)

    compile_cmd = composer_sub.add_parser(
        "compile",
        help="Compile a skill canonical to a typed DAG (zero LLM calls).",
    )
    compile_cmd.add_argument(
        "skill",
        type=Path,
        help="Skill canonical (markdown file).",
    )
    compile_cmd.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Write the compiled DAG to this path as JSON. Default: stdout.",
    )
    compile_cmd.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human; use json for machine consumption).",
    )
    compile_cmd.add_argument(
        "--no-prompts",
        action="store_true",
        help="Omit prompt_section_text from JSON output (smaller files).",
    )
    compile_cmd.set_defaults(func=run_composer_compile)

    run_cmd = composer_sub.add_parser(
        "run",
        help="Execute a compiled pipeline against leaves (Wave 3 — mock LLM by default).",
    )
    run_cmd.add_argument("skill", type=Path, help="Skill canonical (markdown).")
    run_cmd.add_argument(
        "--leaves",
        type=Path,
        help="JSON file with a list of leaf dicts (one per per_leaf invocation). "
        "Default: empty (corpus-wide steps run once with synthetic leaf).",
    )
    run_cmd.add_argument(
        "--vault",
        type=Path,
        default=Path("vault"),
        help="Vault root for materializer file paths (default: ./vault).",
    )
    run_cmd.add_argument(
        "--mock-responses",
        type=Path,
        help="JSON file mapping prompt-substring patterns to canned response "
        "text. Used by the default MockBackend.",
    )
    run_cmd.add_argument(
        "--backend",
        choices=["mock", "anthropic"],
        default="mock",
        help="LLM backend (default: mock — no network). `anthropic` requires "
        "the [agent] extras (`pip install tessellum[agent]`) and the "
        "ANTHROPIC_API_KEY environment variable.",
    )
    run_cmd.add_argument(
        "--model",
        default="claude-sonnet-4-6",
        help="Anthropic model ID (only used when --backend=anthropic). "
        "Default: claude-sonnet-4-6.",
    )
    run_cmd.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip filesystem writes; structured outputs still flow downstream.",
    )
    run_cmd.add_argument(
        "--no-trace",
        action="store_true",
        help="Skip writing a JSON trace to runs/composer/.",
    )
    run_cmd.add_argument(
        "--runs-dir",
        type=Path,
        default=Path("runs") / "composer",
        help="Where to write the trace (default: ./runs/composer/).",
    )
    run_cmd.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    run_cmd.set_defaults(func=run_composer_run_cli)

    batch_cmd = composer_sub.add_parser(
        "batch",
        help="Run many (skill, leaves) jobs in parallel with resume (Wave 5a).",
    )
    batch_cmd.add_argument(
        "jobs",
        type=Path,
        help="JSON file with a list of jobs. Each entry: "
        '{"job_id": "...", "skill": "path/skill.md", '
        '"leaves": [...], "vault": "vault/", "runs_dir": "runs/composer/"}',
    )
    batch_cmd.add_argument(
        "--parallelism",
        type=int,
        default=4,
        help="Max concurrent jobs (default: 4). Pass 1 for sequential.",
    )
    batch_cmd.add_argument(
        "--no-resume",
        action="store_true",
        help="Force re-run jobs whose result file already exists.",
    )
    batch_cmd.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip filesystem writes within each job's pipeline.",
    )
    batch_cmd.add_argument(
        "--mock-responses",
        type=Path,
        help="JSON file mapping prompt-substring patterns to canned response "
        "text. Used by the default MockBackend (shared across all jobs).",
    )
    batch_cmd.add_argument(
        "--backend",
        choices=["mock", "anthropic"],
        default="mock",
        help="LLM backend (default: mock). `anthropic` requires [agent] extras.",
    )
    batch_cmd.add_argument(
        "--model",
        default="claude-sonnet-4-6",
        help="Anthropic model ID (only used when --backend=anthropic).",
    )
    batch_cmd.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    batch_cmd.set_defaults(func=run_composer_batch_cli)

    eval_cmd = composer_sub.add_parser(
        "eval",
        help="Run scenario assertions + LLMJudge rubric on skills (Wave 5b).",
    )
    eval_cmd.add_argument(
        "scenarios_dir",
        type=Path,
        help="Directory containing *.scenario.yaml files.",
    )
    eval_cmd.add_argument(
        "--backend",
        choices=["mock", "anthropic"],
        default="mock",
        help="Pipeline LLM backend (default: mock).",
    )
    eval_cmd.add_argument(
        "--judge-backend",
        choices=["none", "mock", "anthropic"],
        default="mock",
        help="LLMJudge backend (default: mock — canned scores; "
        "use `anthropic` for real grading; `none` to skip rubric).",
    )
    eval_cmd.add_argument(
        "--mock-responses",
        type=Path,
        help="JSON file mapping prompt-substring patterns to canned response "
        "text. Used by the pipeline MockBackend.",
    )
    eval_cmd.add_argument(
        "--judge-mock-responses",
        type=Path,
        help="JSON file mapping prompt-substring patterns to canned judge "
        "responses. Used by the LLMJudge MockBackend.",
    )
    eval_cmd.add_argument(
        "--model",
        default="claude-sonnet-4-6",
        help="Anthropic model ID for --backend=anthropic / --judge-backend=anthropic.",
    )
    eval_cmd.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip filesystem writes within each scenario's pipeline.",
    )
    eval_cmd.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    eval_cmd.set_defaults(func=run_composer_eval_cli)

    scaffold_cmd = composer_sub.add_parser(
        "scaffold-sidecar",
        help="Generate a starter pipeline sidecar from a canonical's section anchors.",
    )
    scaffold_cmd.add_argument(
        "skill",
        type=Path,
        help="Skill canonical (markdown) with <!-- :: section_id = X :: --> anchors.",
    )
    scaffold_cmd.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Where to write the sidecar (default: <skill>.pipeline.yaml).",
    )
    scaffold_cmd.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the sidecar if it already exists.",
    )
    scaffold_cmd.add_argument(
        "--stdout",
        action="store_true",
        help="Print the sidecar to stdout instead of writing it.",
    )
    scaffold_cmd.set_defaults(func=run_composer_scaffold_cli)

    dks_cmd = composer_sub.add_parser(
        "dks",
        help="Run a multi-cycle DKS (Dialectic Knowledge System) session over a JSONL of observations.",
    )
    dks_cmd.add_argument(
        "observations",
        type=Path,
        help="JSONL file — one observation object per line "
        '({"summary": "...", optional "timestamp", "mode", "parent_fz"}).',
    )
    dks_cmd.add_argument(
        "--initial-warrants",
        type=Path,
        help="Optional JSON file with a list of starting warrant objects "
        '(each: {"claim", "data", "warrant", "backing"?, "qualifier"?, "rebuttal"?}).',
    )
    dks_cmd.add_argument(
        "--backend",
        choices=["mock", "anthropic"],
        default="mock",
        help="LLM backend (default: mock — no network). `anthropic` requires "
        "the [agent] extras (`pip install tessellum[agent]`) and the "
        "ANTHROPIC_API_KEY environment variable.",
    )
    dks_cmd.add_argument(
        "--model",
        default="claude-sonnet-4-6",
        help="Anthropic model ID (only used when --backend=anthropic).",
    )
    dks_cmd.add_argument(
        "--mock-responses",
        type=Path,
        help="JSON file mapping prompt-substring patterns to canned response text "
        "(MockBackend only).",
    )
    dks_cmd.add_argument(
        "--runs-dir",
        type=Path,
        default=Path("runs") / "dks",
        help="Where to write per-cycle + aggregate trace JSON (default: ./runs/dks/). "
        "Pass --no-trace to skip writing.",
    )
    dks_cmd.add_argument(
        "--no-trace",
        action="store_true",
        help="Skip writing trace files to --runs-dir.",
    )
    dks_cmd.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    dks_cmd.set_defaults(func=run_composer_dks_cli)


def run_composer_validate(args: argparse.Namespace) -> int:
    target: Path = args.skill.expanduser().resolve()

    if not target.exists():
        print(
            f"tessellum composer validate: {target} does not exist",
            file=sys.stderr,
        )
        return 2

    if target.is_dir():
        skills = sorted(p for p in target.glob("skill_*.md"))
    elif target.is_file() and target.suffix == ".md":
        skills = [target]
    else:
        print(
            f"tessellum composer validate: {target} is neither a markdown "
            f"file nor a directory",
            file=sys.stderr,
        )
        return 2

    if not skills:
        if args.output_format == "json":
            print(json.dumps({"skills": [], "summary": _empty_summary()}, indent=2))
        else:
            print(
                f"tessellum composer validate: no skill_*.md files under {target}",
                file=sys.stderr,
            )
        return 0

    if args.output_format == "json":
        return _emit_json(skills, target)
    return _emit_human(skills, target)


def _empty_summary() -> dict:
    return {"total": 0, "passed": 0, "failed": 0}


def _relative(path: Path, base: Path) -> str:
    try:
        if base.is_dir():
            return str(path.relative_to(base))
        return str(path.relative_to(base.parent))
    except ValueError:
        return str(path)


def _emit_human(skills: list[Path], base: Path) -> int:
    failed = 0
    for skill in skills:
        rel = _relative(skill, base)
        try:
            pipeline = load_pipeline(skill)
        except PipelineValidationError as e:
            print(f"FAIL {rel}")
            for line in str(e).splitlines():
                print(f"     {line}")
            failed += 1
            continue

        if pipeline is None:
            print(f"OK   {rel} (pipeline_metadata: none)")
        else:
            steps = len(pipeline.pipeline)
            print(f"OK   {rel} ({steps} step{'s' if steps != 1 else ''})")

    print()
    print(
        f"validated {len(skills)} skill(s); "
        f"{len(skills) - failed} passed, {failed} failed"
    )
    return 1 if failed else 0


def _emit_json(skills: list[Path], base: Path) -> int:
    results: list[dict] = []
    failed = 0
    for skill in skills:
        rel = _relative(skill, base)
        try:
            pipeline = load_pipeline(skill)
        except PipelineValidationError as e:
            failed += 1
            results.append(
                {
                    "skill": rel,
                    "status": "fail",
                    "has_pipeline": None,
                    "step_count": None,
                    "error": str(e),
                }
            )
            continue

        results.append(
            {
                "skill": rel,
                "status": "ok",
                "has_pipeline": pipeline is not None,
                "step_count": len(pipeline.pipeline) if pipeline else 0,
                "error": None,
            }
        )

    payload = {
        "skills": results,
        "summary": {
            "total": len(skills),
            "passed": len(skills) - failed,
            "failed": failed,
        },
    }
    print(json.dumps(payload, indent=2))
    return 1 if failed else 0


# ── tessellum composer compile ─────────────────────────────────────────────


def run_composer_compile(args: argparse.Namespace) -> int:
    target: Path = args.skill.expanduser().resolve()

    if not target.exists():
        print(
            f"tessellum composer compile: {target} does not exist",
            file=sys.stderr,
        )
        return 2

    if not (target.is_file() and target.suffix == ".md"):
        print(
            f"tessellum composer compile: {target} is not a markdown file",
            file=sys.stderr,
        )
        return 2

    try:
        compiled = compile_skill(target)
    except PipelineValidationError as e:
        print(f"tessellum composer compile: {target.name} validation FAILED")
        print(f"  {e}", file=sys.stderr)
        return 1
    except ContractViolation as e:
        print(f"tessellum composer compile: {target.name} contract violation")
        print(f"  {e}", file=sys.stderr)
        return 1
    except CompilerError as e:
        print(f"tessellum composer compile: {target.name} compiler error")
        print(f"  {e}", file=sys.stderr)
        return 1

    if args.output_format == "json" or args.output is not None:
        payload = to_dag_json(compiled, include_prompts=not args.no_prompts)
        text = json.dumps(payload, indent=2)
        if args.output is not None:
            args.output.expanduser().resolve().write_text(text + "\n", encoding="utf-8")
            print(
                f"compiled {compiled.skill_name} → {args.output} "
                f"({compiled.step_count} step(s))"
            )
        else:
            print(text)
        return 0

    # Human-readable summary.
    print(f"compiled {compiled.skill_name}")
    print(f"  pipeline_version: {compiled.pipeline_version}")
    print(f"  steps: {compiled.step_count}")
    if compiled.step_count == 0:
        print("  (skill declares pipeline_metadata: none — no DAG)")
        return 0
    print()
    for i, step in enumerate(compiled.steps, 1):
        flags = []
        if step.batchable:
            flags.append("batchable")
        flag_str = f"  [{', '.join(flags)}]" if flags else ""
        deps = (
            f"  ← {', '.join(step.depends_on)}"
            if step.depends_on
            else ""
        )
        materializer = step.materializer_key or "(no materializer)"
        print(
            f"  {i}. {step.section_id}  "
            f"[{step.role}/{step.aggregation}]"
            f"  ⇒ {materializer}{flag_str}{deps}"
        )
    return 0


# ── tessellum composer run ─────────────────────────────────────────────────


def run_composer_run_cli(args: argparse.Namespace) -> int:
    skill_path: Path = args.skill.expanduser().resolve()

    if not skill_path.exists():
        print(
            f"tessellum composer run: {skill_path} does not exist",
            file=sys.stderr,
        )
        return 2
    if not (skill_path.is_file() and skill_path.suffix == ".md"):
        print(
            f"tessellum composer run: {skill_path} is not a markdown file",
            file=sys.stderr,
        )
        return 2

    # Compile.
    try:
        compiled = compile_skill(skill_path)
    except (PipelineValidationError, ContractViolation, CompilerError) as e:
        print(
            f"tessellum composer run: {skill_path.name} failed to compile",
            file=sys.stderr,
        )
        print(f"  {e}", file=sys.stderr)
        return 1

    if compiled.step_count == 0:
        print(
            f"tessellum composer run: skill {skill_path.name} declares "
            f"pipeline_metadata: none — nothing to run.",
        )
        return 0

    # Load leaves (if any).
    leaves: list[dict] = []
    if args.leaves is not None:
        try:
            raw = args.leaves.expanduser().resolve().read_text(encoding="utf-8")
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError) as e:
            print(
                f"tessellum composer run: --leaves {args.leaves} could not be "
                f"loaded: {e}",
                file=sys.stderr,
            )
            return 2
        if not isinstance(data, list):
            print(
                f"tessellum composer run: --leaves must contain a JSON list of "
                f"leaf dicts, got {type(data).__name__}",
                file=sys.stderr,
            )
            return 2
        leaves = data

    # Load mock responses (if provided).
    responses: dict[str, str] = {}
    if args.mock_responses is not None:
        try:
            raw = args.mock_responses.expanduser().resolve().read_text(encoding="utf-8")
            responses = json.loads(raw)
        except (OSError, json.JSONDecodeError) as e:
            print(
                f"tessellum composer run: --mock-responses {args.mock_responses} "
                f"could not be loaded: {e}",
                file=sys.stderr,
            )
            return 2
        if not isinstance(responses, dict):
            print(
                f"tessellum composer run: --mock-responses must be a JSON object "
                f"mapping pattern→response",
                file=sys.stderr,
            )
            return 2

    backend: LLMBackend
    if args.backend == "anthropic":
        if args.mock_responses is not None:
            print(
                "tessellum composer run: --mock-responses is ignored when "
                "--backend=anthropic",
                file=sys.stderr,
            )
        try:
            from tessellum.composer import AnthropicBackend
            backend = AnthropicBackend(model=args.model)
        except ImportError as e:
            print(
                f"tessellum composer run: --backend=anthropic requires the "
                f"[agent] extras: pip install tessellum[agent]",
                file=sys.stderr,
            )
            print(f"  ({e})", file=sys.stderr)
            return 2
    else:
        backend = MockBackend(responses=responses)
    vault_root = args.vault.expanduser().resolve()
    runs_dir = None if args.no_trace else args.runs_dir.expanduser().resolve()

    run = run_pipeline(
        compiled,
        leaves=leaves,
        backend=backend,
        vault_root=vault_root,
        dry_run=args.dry_run,
        runs_dir=runs_dir,
    )

    if args.output_format == "json":
        payload = {
            "skill_name": run.skill_name,
            "started_at": run.started_at,
            "duration_seconds": run.duration_seconds,
            "leaf_count": len(run.leaves),
            "step_invocation_count": len(run.step_results),
            "error_count": run.error_count,
            "trace_path": str(run.trace_path) if run.trace_path else None,
            "step_results": [
                {
                    "section_id": r.section_id,
                    "leaf_id": r.leaf_id,
                    "elapsed_ms": r.elapsed_ms,
                    "error": r.error,
                    "files_written": [str(p) for p in r.materialized.files_written],
                    "files_applied": [str(p) for p in r.materialized.files_applied],
                }
                for r in run.step_results
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"ran {run.skill_name}  "
            f"({len(run.step_results)} step invocation(s); "
            f"{run.error_count} error(s); {run.duration_seconds*1000:.1f}ms)"
        )
        for r in run.step_results:
            tag = f"[{r.leaf_id}]" if r.leaf_id else ""
            status = "OK" if r.error is None else "FAIL"
            print(f"  {status}  {r.section_id}  {tag}  {r.elapsed_ms:.1f}ms")
            if r.error:
                print(f"        ↳ {r.error}")
            if r.materialized.files_written:
                for p in r.materialized.files_written:
                    print(f"        wrote {p}")
            if r.materialized.files_applied:
                for p in r.materialized.files_applied:
                    print(f"        applied {p}")
        if run.trace_path:
            print()
            print(f"trace: {run.trace_path}")

    return 1 if run.error_count else 0


# ── tessellum composer batch ───────────────────────────────────────────────


def run_composer_batch_cli(args: argparse.Namespace) -> int:
    jobs_path: Path = args.jobs.expanduser().resolve()
    if not jobs_path.is_file():
        print(
            f"tessellum composer batch: {jobs_path} does not exist or is not a file",
            file=sys.stderr,
        )
        return 2

    try:
        raw = jobs_path.read_text(encoding="utf-8")
        spec = json.loads(raw)
    except (OSError, json.JSONDecodeError) as e:
        print(
            f"tessellum composer batch: failed to read {jobs_path}: {e}",
            file=sys.stderr,
        )
        return 2

    if not isinstance(spec, list):
        print(
            f"tessellum composer batch: jobs file must be a JSON list, "
            f"got {type(spec).__name__}",
            file=sys.stderr,
        )
        return 2

    jobs: list[BatchJob] = []
    for i, entry in enumerate(spec):
        if not isinstance(entry, dict):
            print(
                f"tessellum composer batch: jobs[{i}] must be a JSON object",
                file=sys.stderr,
            )
            return 2
        job_id = entry.get("job_id")
        skill = entry.get("skill")
        if not job_id:
            print(
                f"tessellum composer batch: jobs[{i}] missing `job_id`",
                file=sys.stderr,
            )
            return 2
        if not skill:
            print(
                f"tessellum composer batch: jobs[{i}] missing `skill`",
                file=sys.stderr,
            )
            return 2
        jobs.append(
            BatchJob(
                job_id=str(job_id),
                skill_path=Path(skill).expanduser().resolve(),
                leaves=tuple(entry.get("leaves") or ()),
                vault_root=Path(entry.get("vault") or "vault").expanduser().resolve(),
                runs_dir=(
                    Path(entry["runs_dir"]).expanduser().resolve()
                    if entry.get("runs_dir")
                    else None
                ),
            )
        )

    if not jobs:
        print("tessellum composer batch: no jobs to run.")
        return 0

    # Backend selection (mirrors `run` semantics).
    backend: LLMBackend
    if args.backend == "anthropic":
        try:
            from tessellum.composer import AnthropicBackend
            backend = AnthropicBackend(model=args.model)
        except ImportError as e:
            print(
                f"tessellum composer batch: --backend=anthropic requires the "
                f"[agent] extras: pip install tessellum[agent]",
                file=sys.stderr,
            )
            print(f"  ({e})", file=sys.stderr)
            return 2
    else:
        responses: dict[str, str] = {}
        if args.mock_responses is not None:
            try:
                responses = json.loads(
                    args.mock_responses.expanduser().resolve().read_text(
                        encoding="utf-8"
                    )
                )
            except (OSError, json.JSONDecodeError) as e:
                print(
                    f"tessellum composer batch: --mock-responses unreadable: {e}",
                    file=sys.stderr,
                )
                return 2
        backend = MockBackend(responses=responses)

    result = run_batch(
        jobs,
        backend=backend,
        parallelism=max(args.parallelism, 1),
        dry_run=args.dry_run,
        resume=not args.no_resume,
    )

    if args.output_format == "json":
        payload = {
            "completed": list(result.completed),
            "skipped": list(result.skipped),
            "failed": list(result.failed),
            "jobs": [
                {
                    "job_id": j.job_id,
                    "status": j.status,
                    "error": j.error,
                    "result_path": str(j.result_path) if j.result_path else None,
                    "step_invocation_count": (
                        len(j.run_result.step_results) if j.run_result else None
                    ),
                    "error_count": (
                        j.run_result.error_count if j.run_result else None
                    ),
                }
                for j in result.jobs
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"batch: {len(result.completed)} completed, "
            f"{len(result.skipped)} skipped, {len(result.failed)} failed."
        )
        for j in result.jobs:
            tag = j.status.upper()
            extra = ""
            if j.run_result is not None:
                extra = (
                    f"  ({len(j.run_result.step_results)} step(s); "
                    f"{j.run_result.error_count} error(s); "
                    f"{j.run_result.duration_seconds*1000:.1f}ms)"
                )
            print(f"  {tag:9s} {j.job_id}{extra}")
            if j.error:
                print(f"            ↳ {j.error}")

    return 1 if result.failed else 0


# ── tessellum composer eval ────────────────────────────────────────────────


def _load_mock_responses(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    raw = path.expanduser().resolve().read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("mock-responses file must be a JSON object")
    return data


def _make_anthropic_backend_or_exit(model: str) -> LLMBackend:
    """Helper: try to construct AnthropicBackend; exits with helpful message if missing."""
    try:
        from tessellum.composer import AnthropicBackend
        return AnthropicBackend(model=model)
    except ImportError as e:
        print(
            "tessellum composer eval: --backend=anthropic requires the "
            "[agent] extras: pip install tessellum[agent]",
            file=sys.stderr,
        )
        print(f"  ({e})", file=sys.stderr)
        raise SystemExit(2) from e


def run_composer_eval_cli(args: argparse.Namespace) -> int:
    scenarios_dir: Path = args.scenarios_dir.expanduser().resolve()
    if not scenarios_dir.is_dir():
        print(
            f"tessellum composer eval: {scenarios_dir} is not a directory",
            file=sys.stderr,
        )
        return 2

    try:
        scenarios = load_scenarios(scenarios_dir)
    except EvalError as e:
        print(f"tessellum composer eval: {e}", file=sys.stderr)
        return 2

    if not scenarios:
        print(f"tessellum composer eval: no *.scenario.yaml files in {scenarios_dir}")
        return 0

    # Pipeline backend.
    backend: LLMBackend
    if args.backend == "anthropic":
        backend = _make_anthropic_backend_or_exit(args.model)
    else:
        try:
            responses = _load_mock_responses(args.mock_responses)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            print(
                f"tessellum composer eval: --mock-responses unreadable: {e}",
                file=sys.stderr,
            )
            return 2
        backend = MockBackend(responses=responses)

    # Judge backend.
    judge: LLMJudge | None
    if args.judge_backend == "none":
        judge = None
    elif args.judge_backend == "anthropic":
        judge_backend = _make_anthropic_backend_or_exit(args.model)
        judge = LLMJudge(judge_backend)
    else:
        try:
            judge_responses = _load_mock_responses(args.judge_mock_responses)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            print(
                f"tessellum composer eval: --judge-mock-responses unreadable: {e}",
                file=sys.stderr,
            )
            return 2
        if not judge_responses:
            # Default canned response gives every dim a score of 4 — useful
            # as a sanity check that the rubric pipeline runs end-to-end.
            judge_responses = {
                "Rubric dimensions to score": json.dumps(
                    {
                        "relevance": {"score": 4, "justification": "ok"},
                        "completeness": {"score": 4, "justification": "ok"},
                        "accuracy": {"score": 4, "justification": "ok"},
                        "clarity": {"score": 4, "justification": "ok"},
                        "structural_integrity": {"score": 4, "justification": "ok"},
                    }
                )
            }
        judge = LLMJudge(MockBackend(responses=judge_responses))

    result = run_eval(
        scenarios,
        backend=backend,
        judge=judge,
        dry_run=args.dry_run,
    )

    if args.output_format == "json":
        payload = {
            "passed": result.passed_count,
            "failed": result.failed_count,
            "errored": result.error_count,
            "mean_score_by_dim": result.mean_score_by_dim,
            "scenarios": [
                {
                    "name": s.scenario_name,
                    "overall_passed": s.overall_passed,
                    "error": s.error,
                    "assertions": [
                        {
                            "kind": a.assertion.kind,
                            "target": a.assertion.target,
                            "passed": a.passed,
                            "message": a.message,
                        }
                        for a in s.assertions
                    ],
                    "judge_scores": [
                        {
                            "dimension": j.dimension,
                            "score": j.score,
                            "justification": j.justification,
                        }
                        for j in s.judge_scores
                    ],
                }
                for s in result.scenarios
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"eval: {result.passed_count} passed, "
            f"{result.failed_count} failed, "
            f"{result.error_count} errored (of {len(result.scenarios)} scenarios)"
        )
        for s in result.scenarios:
            tag = "PASS" if s.overall_passed else ("ERROR" if s.error else "FAIL")
            print(f"  {tag:6s} {s.scenario_name}")
            if s.error:
                print(f"            ↳ {s.error}")
            for a in s.assertions:
                if not a.passed:
                    print(f"            ✗ {a.assertion.kind}({a.assertion.target}): {a.message}")
            for j in s.judge_scores:
                print(f"            • {j.dimension}: {j.score}/5  {j.justification}")
        if result.mean_score_by_dim:
            print()
            print("Mean scores:")
            for d, mean in result.mean_score_by_dim.items():
                print(f"  {d}: {mean:.2f}")

    return 1 if (result.failed_count or result.error_count) else 0


# ── tessellum composer scaffold-sidecar ────────────────────────────────────


def run_composer_scaffold_cli(args: argparse.Namespace) -> int:
    """Generate a starter pipeline sidecar from a canonical's anchors.

    Reads ``<!-- :: section_id = X :: -->`` markers in the canonical and
    emits one CORE step per section, chained by ``depends_on`` (each step
    waits on the previous one). Materializer defaults to ``no_op``;
    aggregation defaults to ``per_leaf``. The author then fills in real
    materializers, schemas, and prompt templates.
    """
    from tessellum.composer.skill_extractor import (
        SkillExtractionError,
        list_section_ids,
    )

    skill_path: Path = args.skill.expanduser().resolve()
    if not skill_path.is_file() or skill_path.suffix != ".md":
        print(
            f"tessellum composer scaffold-sidecar: {skill_path} is not a markdown file",
            file=sys.stderr,
        )
        return 2

    try:
        section_ids = list_section_ids(skill_path)
    except SkillExtractionError as e:
        print(
            f"tessellum composer scaffold-sidecar: {e}", file=sys.stderr
        )
        return 1

    if not section_ids:
        print(
            f"tessellum composer scaffold-sidecar: no `<!-- :: section_id = X :: -->` "
            f"anchors found in {skill_path.name}.",
            file=sys.stderr,
        )
        return 1

    sidecar_text = _render_sidecar(skill_path.stem, section_ids)

    if args.stdout:
        print(sidecar_text, end="")
        return 0

    output: Path = (
        args.output.expanduser().resolve()
        if args.output is not None
        else skill_path.with_suffix(".pipeline.yaml")
    )
    if output.exists() and not args.force:
        print(
            f"tessellum composer scaffold-sidecar: {output} already exists. "
            f"Pass --force to overwrite, or --stdout to print without writing.",
            file=sys.stderr,
        )
        return 2

    output.write_text(sidecar_text, encoding="utf-8")
    print(f"scaffolded {output}")
    print(f"  {len(section_ids)} step(s) from {len(section_ids)} section anchor(s):")
    for sid in section_ids:
        print(f"    - {sid}")
    print()
    print(f"  next: fill in materializer / expected_output_schema / prompt_template per step,")
    print(f"        then `tessellum composer validate {skill_path}`")
    return 0


def _render_sidecar(skill_stem: str, section_ids: list[str]) -> str:
    """Emit a placeholder pipeline.yaml body covering ``section_ids`` in order."""
    lines = [
        "# Scaffolded by `tessellum composer scaffold-sidecar`.",
        "# One CORE step per `<!-- :: section_id = X :: -->` anchor in",
        f"# the canonical {skill_stem}.md, chained linearly via depends_on.",
        "#",
        "# Next steps:",
        "#   1. Pick a materializer per step (no_op / body_markdown_to_file /",
        "#      body_markdown_frontmatter_to_file / edits_apply_to_files /",
        "#      edits_apply_xml_tags).",
        "#   2. Add `expected_output_schema:` for any step whose materializer",
        "#      has required fields (the validator will tell you which).",
        "#   3. Replace placeholder prompt_template content with your prompts.",
        "#   4. Validate: `tessellum composer validate <this_skill.md>`",
        '',
        'version: "1.0"',
        'pipeline:',
    ]

    for i, sid in enumerate(section_ids):
        depends = f"[{section_ids[i - 1]}]" if i > 0 else "[]"
        lines.extend(
            [
                f"  - section_id: {sid}",
                f"    role: CORE                  # CORE | DEFERRED | INFRA",
                f"    aggregation: per_leaf       # per_leaf | cross_leaf | corpus_wide",
                f"    batchable: false",
                f"    depends_on: {depends}",
                f"    materializer: no_op         # pick a wire format from MATERIALIZER_CONTRACTS",
                f"    output_key: {sid}_output",
                f'    prompt_template: |',
                f'      TODO: fill in the prompt for "{sid}".',
                f'      You may reference {{{{leaf.X}}}} per-leaf data and',
                f'      {{{{upstream.Y}}}} outputs from previous steps.',
                f"",
            ]
        )

    return "\n".join(lines)


# ── tessellum composer dks ─────────────────────────────────────────────────


def run_composer_dks_cli(args: argparse.Namespace) -> int:
    """Drive a multi-cycle DKS session over a JSONL of observations.

    Phase 3 of plans/plan_dks_implementation.md. Loads N observations,
    allocates a fresh FZ root per observation (or honors an explicit
    mode/parent_fz pair from the JSONL), runs ``DKSRunner``, and writes
    per-cycle + aggregate trace JSON to ``--runs-dir``.
    """
    from datetime import datetime, timezone

    obs_path: Path = args.observations.expanduser().resolve()
    if not obs_path.is_file():
        print(
            f"tessellum composer dks: {obs_path} does not exist or is not a file",
            file=sys.stderr,
        )
        return 2

    try:
        raw = obs_path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"tessellum composer dks: failed to read {obs_path}: {e}", file=sys.stderr)
        return 2

    # Parse JSONL — one observation per non-blank line.
    observation_specs: list[dict] = []
    for lineno, line in enumerate(raw.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            entry = json.loads(stripped)
        except json.JSONDecodeError as e:
            print(
                f"tessellum composer dks: {obs_path}:{lineno} invalid JSON: {e}",
                file=sys.stderr,
            )
            return 2
        if not isinstance(entry, dict):
            print(
                f"tessellum composer dks: {obs_path}:{lineno} must be a JSON object, "
                f"got {type(entry).__name__}",
                file=sys.stderr,
            )
            return 2
        if "summary" not in entry or not isinstance(entry["summary"], str):
            print(
                f"tessellum composer dks: {obs_path}:{lineno} missing required string field 'summary'",
                file=sys.stderr,
            )
            return 2
        observation_specs.append(entry)

    # Empty file → exit 0 with a friendly note (no cycles to run).
    if not observation_specs:
        if args.output_format == "json":
            print(json.dumps({"cycles": [], "warrant_changes": [], "summary": {
                "cycle_count": 0, "closed_loop_count": 0, "added": 0, "revised": 0, "superseded": 0,
            }}, indent=2))
        else:
            print(f"tessellum composer dks: {obs_path} has no observations — nothing to run.")
        return 0

    # Build observations with allocated FZ roots.
    existing_trails: list[str] = []
    observations: list[DKSObservation] = []
    for i, spec in enumerate(observation_specs):
        mode = spec.get("mode", "fresh")
        if mode not in ("fresh", "extend", "branch"):
            print(
                f"tessellum composer dks: observation #{i + 1} has invalid mode={mode!r}; "
                f"expected one of fresh|extend|branch",
                file=sys.stderr,
            )
            return 2
        parent_fz = spec.get("parent_fz")
        try:
            fz = allocate_cycle_fz(
                tuple(existing_trails),
                mode=mode,
                parent_fz=parent_fz,
            )
        except ValueError as e:
            print(
                f"tessellum composer dks: observation #{i + 1} FZ allocation failed: {e}",
                file=sys.stderr,
            )
            return 2
        existing_trails.append(fz)
        observations.append(
            DKSObservation(
                folgezettel=fz,
                summary=spec["summary"],
                timestamp=spec.get("timestamp"),
            )
        )

    # Load initial warrants (optional).
    initial_warrants: tuple = ()
    if args.initial_warrants is not None:
        from tessellum.composer.dks import DKSWarrant

        wpath = args.initial_warrants.expanduser().resolve()
        if not wpath.is_file():
            print(
                f"tessellum composer dks: --initial-warrants {wpath} not found",
                file=sys.stderr,
            )
            return 2
        try:
            w_data = json.loads(wpath.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(
                f"tessellum composer dks: --initial-warrants unreadable: {e}",
                file=sys.stderr,
            )
            return 2
        if not isinstance(w_data, list):
            print(
                f"tessellum composer dks: --initial-warrants must be a JSON list",
                file=sys.stderr,
            )
            return 2
        try:
            initial_warrants = tuple(
                DKSWarrant(
                    claim=str(w.get("claim", "")),
                    data=str(w.get("data", "")),
                    warrant=str(w.get("warrant", "")),
                    backing=str(w.get("backing", "")),
                    qualifier=str(w.get("qualifier", "")),
                    rebuttal=str(w.get("rebuttal", "")),
                )
                for w in w_data
            )
        except (TypeError, AttributeError) as e:
            print(
                f"tessellum composer dks: --initial-warrants malformed entries: {e}",
                file=sys.stderr,
            )
            return 2

    # Backend selection (mirrors `composer run` semantics).
    backend: LLMBackend
    if args.backend == "anthropic":
        try:
            from tessellum.composer import AnthropicBackend

            backend = AnthropicBackend(model=args.model)
        except ImportError as e:
            print(
                "tessellum composer dks: --backend=anthropic requires the "
                "[agent] extras: pip install tessellum[agent]",
                file=sys.stderr,
            )
            print(f"  ({e})", file=sys.stderr)
            return 2
    else:
        responses: dict[str, str] = {}
        if args.mock_responses is not None:
            try:
                responses = json.loads(
                    args.mock_responses.expanduser().resolve().read_text(encoding="utf-8")
                )
            except (OSError, json.JSONDecodeError) as e:
                print(
                    f"tessellum composer dks: --mock-responses unreadable: {e}",
                    file=sys.stderr,
                )
                return 2
            if not isinstance(responses, dict):
                print(
                    f"tessellum composer dks: --mock-responses must be a JSON object",
                    file=sys.stderr,
                )
                return 2
        backend = MockBackend(responses=responses)

    runner = DKSRunner(
        observations=tuple(observations),
        backend=backend,
        initial_warrants=initial_warrants,
    )
    result = runner.run()

    # Write traces (one per cycle + one aggregate) unless --no-trace.
    trace_paths: list[Path] = []
    aggregate_path: Path | None = None
    if not args.no_trace:
        runs_dir = args.runs_dir.expanduser().resolve()
        runs_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        for cycle in result.cycles:
            tp = runs_dir / f"{ts}_cycle_{cycle.cycle_id}.json"
            tp.write_text(
                json.dumps(_serialize_cycle(cycle), indent=2) + "\n",
                encoding="utf-8",
            )
            trace_paths.append(tp)

        aggregate_path = runs_dir / f"{ts}_aggregate.json"
        aggregate_path.write_text(
            json.dumps(
                _serialize_run(result, trace_paths, observation_specs, ts),
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    # Stdout report.
    counts = aggregate_warrant_changes(result.warrant_changes)
    if args.output_format == "json":
        payload = {
            "cycle_count": result.cycle_count,
            "closed_loop_count": result.closed_loop_count,
            "duration_seconds": result.elapsed_ms / 1000.0,
            "summary": counts,
            "cycles": [_serialize_cycle(c) for c in result.cycles],
            "warrant_changes": [
                _serialize_change(c) for c in result.warrant_changes
            ],
            "trace_paths": [str(p) for p in trace_paths],
            "aggregate_path": str(aggregate_path) if aggregate_path else None,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"dks: {result.cycle_count} cycle(s); "
            f"{result.closed_loop_count} closed loop; "
            f"{counts['added']} added, {counts['revised']} revised, "
            f"{counts['superseded']} superseded; "
            f"{result.elapsed_ms:.1f}ms"
        )
        for c in result.cycles:
            tag = "CLOSED" if c.closed_loop else " SHORT"
            print(
                f"  {tag}  FZ {c.cycle_id}  "
                f"nodes={len(c.folgezettel_nodes)}  "
                f"{c.elapsed_ms:.1f}ms"
            )
        if trace_paths:
            print()
            print(f"  traces: {len(trace_paths)} cycle file(s) + aggregate")
            print(f"  aggregate: {aggregate_path}")

    return 0


def _serialize_cycle(cycle) -> dict:
    """Flatten a DKSCycleResult to a JSON-safe dict for trace files."""
    def _w(w):
        if w is None:
            return None
        return {
            "claim": w.claim,
            "data": w.data,
            "warrant": w.warrant,
            "backing": w.backing,
            "qualifier": w.qualifier,
            "rebuttal": w.rebuttal,
        }

    def _arg(a):
        return {
            "folgezettel": a.folgezettel,
            "warrant": _w(a.warrant),
            "evidence": a.evidence,
        }

    out = {
        "cycle_id": cycle.cycle_id,
        "mode": cycle.mode,
        "closed_loop": cycle.closed_loop,
        "elapsed_ms": cycle.elapsed_ms,
        "backend_id": cycle.backend_id,
        "folgezettel_nodes": list(cycle.folgezettel_nodes),
        "observation": {
            "folgezettel": cycle.observation.folgezettel,
            "summary": cycle.observation.summary,
            "timestamp": cycle.observation.timestamp,
        },
        "argument_a": _arg(cycle.argument_a),
        "argument_b": _arg(cycle.argument_b),
        "contradicts": (
            None
            if cycle.contradicts is None
            else {
                "attacker_fz": cycle.contradicts.attacker_fz,
                "attacked_fz": cycle.contradicts.attacked_fz,
                "reason": cycle.contradicts.reason,
            }
        ),
        "counter": (
            None
            if cycle.counter is None
            else {
                "folgezettel": cycle.counter.folgezettel,
                "attacked_fz": cycle.counter.attacked_fz,
                "broken_component": cycle.counter.broken_component,
                "counter_claim": cycle.counter.counter_claim,
                "reason": cycle.counter.reason,
                "strength": cycle.counter.strength,
            }
        ),
        "pattern": (
            None
            if cycle.pattern is None
            else {
                "folgezettel": cycle.pattern.folgezettel,
                "description": cycle.pattern.description,
                "observed": list(cycle.pattern.observed),
            }
        ),
        "rule_revision": (
            None
            if cycle.rule_revision is None
            else {
                "folgezettel": cycle.rule_revision.folgezettel,
                "revised_warrant": _w(cycle.rule_revision.revised_warrant),
                "supersedes": cycle.rule_revision.supersedes,
            }
        ),
    }
    return out


def _serialize_change(change) -> dict:
    return {
        "cycle_id": change.cycle_id,
        "kind": change.kind,
        "revision_fz": change.revision_fz,
        "superseded_fz": change.superseded_fz,
        "warrant": (
            None
            if change.warrant is None
            else {
                "claim": change.warrant.claim,
                "data": change.warrant.data,
                "warrant": change.warrant.warrant,
                "backing": change.warrant.backing,
                "qualifier": change.warrant.qualifier,
                "rebuttal": change.warrant.rebuttal,
            }
        ),
    }


def _serialize_run(
    result,
    trace_paths: list[Path],
    observation_specs: list[dict],
    timestamp: str,
) -> dict:
    counts = aggregate_warrant_changes(result.warrant_changes)
    return {
        "timestamp": timestamp,
        "cycle_count": result.cycle_count,
        "closed_loop_count": result.closed_loop_count,
        "duration_seconds": result.elapsed_ms / 1000.0,
        "backend_id": result.backend_id,
        "summary": counts,
        "observation_specs": observation_specs,
        "cycle_traces": [str(p) for p in trace_paths],
        "warrant_changes": [_serialize_change(c) for c in result.warrant_changes],
        "final_warrants": [
            {
                "claim": w.claim,
                "data": w.data,
                "warrant": w.warrant,
                "backing": w.backing,
                "qualifier": w.qualifier,
                "rebuttal": w.rebuttal,
            }
            for w in result.final_warrants
        ],
    }
