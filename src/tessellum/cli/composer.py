"""``tessellum composer …`` — Composer pipeline operations.

Seven subcommands:

    validate <skill>          Validate each step's contract block (schema).
    compile <skill>           Compile to a typed DAG with contract checks.
    run <skill>               Execute the compiled pipeline against leaves.
    batch <jobs.json>         Run many ``(skill, leaves)`` jobs in parallel.
    eval <scenarios>          Run scenario assertions + LLMJudge rubric.
    scaffold-sidecar <skill>  Print starter ```yaml``` contract blocks to paste into a single-file canonical.
    digest --source <json>    Run plan → augment → review →[sign-off]→ execute.

The DKS runtime (Dialectic Knowledge System) is a peer subcommand at
``tessellum dks``. It uses Composer's LLMBackend abstractions but is
otherwise independent.

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
    AgentVerdict,
    BatchJob,
    CompilerError,
    ContractViolation,
    EvalError,
    LLMBackend,
    LLMJudge,
    Manifest,
    MockBackend,
    PipelineValidationError,
    RunBudget,
    SignOffPolicy,
    build_close_gate,
    build_wave_gate,
    compile_skill,
    get_assembler,
    make_llm_fixer,
    partition_unchanged_leaves,
    load_pipeline,
    load_scenarios,
    run_batch,
    run_digestion_pipeline,
    run_eval,
    run_pipeline,
    run_pipeline_dynamic,
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
        help="Validate a skill canonical's inline contract blocks.",
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
        help="Execute a compiled pipeline against leaves (mock LLM by default).",
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
        choices=["mock", "anthropic", "bedrock"],
        default="mock",
        help="LLM backend (default: mock — no network). `anthropic` requires "
        "the [agent] extras + ANTHROPIC_API_KEY. `bedrock` requires the "
        "[agent] extras + an AWS_PROFILE that can invoke Bedrock (set "
        "AWS_PROFILE before running; the backend embeds no credentials).",
    )
    run_cmd.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region for --backend=bedrock (default: us-east-1).",
    )
    run_cmd.add_argument(
        "--aws-profile",
        default=None,
        help="AWS_PROFILE to select for --backend=bedrock. When omitted, "
        "the ambient credential chain is used as-is.",
    )
    run_cmd.add_argument(
        "--model",
        default=None,
        help="Model ID for --backend=anthropic|bedrock. Default: "
        "claude-sonnet-4-6 for anthropic; us.anthropic.claude-sonnet-4-6 "
        "(the cross-region inference profile) for bedrock — a bare "
        "foundation-model id fails on-demand Bedrock invocation.",
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
    run_cmd.add_argument(
        "--progress",
        action="store_true",
        help="Emit per-step start/finish lines to stderr. Off by default. "
        "Useful for long multi-leaf runs where the user wants to see "
        "what step is currently running.",
    )
    # ── v4 dynamic scheduler (opt-in; serial run_pipeline stays the default) ──
    run_cmd.add_argument(
        "--dynamic",
        action="store_true",
        help="Use the wave-parallel v4 scheduler (run_pipeline_dynamic) instead "
        "of the serial reference path. Opt-in; the serial run_pipeline stays "
        "the default and is byte-identical. Enables --workers/--manifest/"
        "--close-gate/--max-invocations/--max-cost/--stats below.",
    )
    run_cmd.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Leaf-level worker-pool size for --dynamic (default: 4). Ignored "
        "without --dynamic.",
    )
    run_cmd.add_argument(
        "--manifest",
        type=Path,
        help="Resume-manifest path for --dynamic. Records per-leaf/per-attempt "
        "rows + claim/done state (crash-safe resume projection). Ignored "
        "without --dynamic.",
    )
    run_cmd.add_argument(
        "--fix-with-backend",
        action="store_true",
        help="On a close-gate FAIL, repair the note in place with an LLM fixer "
        "(the same --backend), up to --max-fix-rounds, with checkpoint + "
        "revert-to-BEST. Requires --dynamic + --close-gate.",
    )
    run_cmd.add_argument(
        "--max-fix-rounds",
        type=int,
        default=1,
        help="Max close-gate repair rounds for --fix-with-backend (default: 1).",
    )
    run_cmd.add_argument(
        "--close-gate",
        action="store_true",
        help="Enable the per-session close-gate for --dynamic: each note that a "
        "session writes must pass format (+ grounding) before it closes "
        "`done`, else `blocked`. Ignored without --dynamic.",
    )
    run_cmd.add_argument(
        "--max-invocations",
        type=int,
        help="Global run-level invocation budget for --dynamic (the "
        "runaway-fan-out breaker). A refused spend halts the leaf with a "
        "typed BUDGET_EXHAUSTED outcome. Ignored without --dynamic.",
    )
    run_cmd.add_argument(
        "--max-cost",
        type=float,
        help="Global run-level cost budget for --dynamic. Ignored without "
        "--dynamic.",
    )
    run_cmd.add_argument(
        "--stats",
        type=Path,
        help="Write a statistics.json rollup (per-stage counts + duration) for "
        "--dynamic. Ignored without --dynamic.",
    )
    run_cmd.add_argument(
        "--wave-gate",
        action="store_true",
        help="Enable the per-wave post-batch gate for --dynamic: a cross-set "
        "sweep (e.g. duplicate target paths across sessions) run once after "
        "the wave. Offending results are flagged errored. Ignored without "
        "--dynamic.",
    )
    run_cmd.add_argument(
        "--context-strategy",
        choices=["full_source", "windowed"],
        default=None,
        help="Enable fail-soft context bounding for --dynamic: an oversized "
        "rendered prompt is truncated (`full_source`) or head+tail windowed "
        "(`windowed`) + warned, instead of the hard-cap validation error. "
        "Ignored without --dynamic; omit for the hard-cap behaviour.",
    )
    run_cmd.add_argument(
        "--context-max-chars",
        type=int,
        default=None,
        help="Char budget for --context-strategy (default: the assembler's "
        "built-in cap). Ignored without --context-strategy.",
    )
    run_cmd.add_argument(
        "--skip-unchanged",
        type=Path,
        default=None,
        help="`$0` change-detection pre-gate: a JSON fingerprint store "
        "({leaf_id: fingerprint}). Before running, leaves whose content is "
        "unchanged since the recorded fingerprint are skipped (not "
        "dispatched); the store is rewritten with fresh fingerprints after. "
        "A new/changed/unkeyed leaf always runs (fail-open). Ignored "
        "without --dynamic.",
    )
    run_cmd.add_argument(
        "--skip-unchanged-key",
        default=None,
        help="Leaf field to fingerprint for --skip-unchanged (default: the "
        "whole leaf minus its positional id).",
    )
    run_cmd.set_defaults(func=run_composer_run_cli)

    batch_cmd = composer_sub.add_parser(
        "batch",
        help="Run many (skill, leaves) jobs in parallel with resume.",
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
        help="Run scenario assertions + LLMJudge rubric on skills.",
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
        help="Print starter ```yaml``` contract blocks (one per section anchor) "
        "to paste into a single-file skill canonical.",
    )
    scaffold_cmd.add_argument(
        "skill",
        type=Path,
        help="Skill canonical (markdown) with <!-- :: section_id = X :: --> anchors.",
    )
    scaffold_cmd.add_argument(
        "--stdout",
        action="store_true",
        help="Print only the contract blocks (suppress the trailing guidance "
        "note on stderr).",
    )
    scaffold_cmd.set_defaults(func=run_composer_scaffold_cli)

    digest_cmd = composer_sub.add_parser(
        "digest",
        help="Run the native plan → augment → review →[sign-off]→ execute "
        "digestion pipeline over a source.",
    )
    digest_cmd.add_argument(
        "--skills-dir",
        type=Path,
        default=Path("vault") / "resources" / "skills",
        help="Directory with the 4 skill_tessellum_*_digestion phase skills "
        "(default: ./vault/resources/skills).",
    )
    digest_cmd.add_argument(
        "--source",
        type=Path,
        required=True,
        help="JSON file: the source leaf for the plan phase (the plan_doc seed).",
    )
    digest_cmd.add_argument(
        "--vault", type=Path, default=Path("vault"),
        help="Vault root for materializer file paths (default: ./vault).",
    )
    digest_cmd.add_argument(
        "--backend", choices=["mock", "anthropic", "bedrock"], default="mock",
        help="LLM backend (default: mock).",
    )
    digest_cmd.add_argument("--model", default=None, help="Model id for anthropic|bedrock.")
    digest_cmd.add_argument("--region", default="us-east-1", help="AWS region for bedrock.")
    digest_cmd.add_argument("--aws-profile", default=None, help="AWS_PROFILE for bedrock.")
    digest_cmd.add_argument(
        "--mock-responses", type=Path,
        help="JSON pattern→response map for --backend=mock.",
    )
    digest_cmd.add_argument(
        "--require-agent-signoff", action="store_true",
        help="Enable the reviewer-agent rung at review→ready (else program-gate "
        "only). Without an injected agent the CLI uses a conservative "
        "auto-approver only when the review verdict is ready.",
    )
    digest_cmd.add_argument("--dry-run", action="store_true", help="Skip filesystem writes.")
    digest_cmd.add_argument(
        "--format", dest="output_format", choices=["human", "json"], default="human",
    )
    digest_cmd.set_defaults(func=run_composer_digest_cli)


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


def _emit_empty_run(compiled, output_format: str) -> None:
    """Emit a clean zero-invocation result (all leaves skipped by the
    ``$0`` pre-gate). Mirrors the normal output shape with empty results."""
    if output_format == "json":
        print(
            json.dumps(
                {
                    "skill_name": compiled.skill_name,
                    "started_at": None,
                    "duration_seconds": 0.0,
                    "leaf_count": 0,
                    "step_invocation_count": 0,
                    "error_count": 0,
                    "trace_path": None,
                    "step_results": [],
                },
                indent=2,
            )
        )
    else:
        print(
            f"ran {compiled.skill_name}  (0 step invocation(s); "
            f"all leaves skipped by --skip-unchanged)"
        )


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
                "tessellum composer run: --mock-responses must be a JSON object "
                "mapping pattern→response",
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
            backend = AnthropicBackend(model=args.model or "claude-sonnet-4-6")
        except ImportError as e:
            print(
                "tessellum composer run: --backend=anthropic requires the "
                "[agent] extras: pip install tessellum[agent]",
                file=sys.stderr,
            )
            print(f"  ({e})", file=sys.stderr)
            return 2
    elif args.backend == "bedrock":
        if args.mock_responses is not None:
            print(
                "tessellum composer run: --mock-responses is ignored when "
                "--backend=bedrock",
                file=sys.stderr,
            )
        try:
            from tessellum.composer import BedrockBackend
            backend = BedrockBackend(
                model=args.model or "us.anthropic.claude-sonnet-4-6",
                region=args.region,
                aws_profile=args.aws_profile,
            )
        except ImportError as e:
            print(
                "tessellum composer run: --backend=bedrock requires the "
                "[agent] extras: pip install tessellum[agent]",
                file=sys.stderr,
            )
            print(f"  ({e})", file=sys.stderr)
            return 2
    else:
        backend = MockBackend(responses=responses)
    vault_root = args.vault.expanduser().resolve()
    runs_dir = None if args.no_trace else args.runs_dir.expanduser().resolve()

    if getattr(args, "dynamic", False):
        # ── v4 wave-parallel path (opt-in) ──────────────────────────────────
        # Assemble only the machinery the flags request; everything defaults
        # off so `--dynamic` alone is a straight parallel run with parity to
        # the serial path.

        # `$0` change-detection pre-gate (leaf-admission layer): drop leaves
        # whose content is unchanged since the recorded fingerprint BEFORE
        # dispatch, then rewrite the store. Runs here (not mid-DAG) so it
        # never interferes with upstream accumulation.
        skip_store_path = getattr(args, "skip_unchanged", None)
        if skip_store_path is not None:
            store_path = skip_store_path.expanduser().resolve()
            prior_fps: dict = {}
            if store_path.is_file():
                try:
                    prior_fps = json.loads(store_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    prior_fps = {}  # fail-open: a bad store runs everything
            leaves, skipped_leaves, fresh_fps = partition_unchanged_leaves(
                leaves,
                prior_fps,
                source_key=getattr(args, "skip_unchanged_key", None),
            )
            store_path.parent.mkdir(parents=True, exist_ok=True)
            store_path.write_text(
                json.dumps(fresh_fps, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            if skipped_leaves:
                print(
                    f"tessellum composer run: --skip-unchanged skipped "
                    f"{len(skipped_leaves)} unchanged leaf(s); running "
                    f"{len(leaves)}.",
                    file=sys.stderr,
                )
            # If the pre-gate filtered EVERY leaf out, there is nothing to
            # run. Emit a clean zero-invocation result and return — do NOT
            # fall through to run_pipeline_dynamic, whose empty-leaves path
            # would synthesize a `corpus` leaf and re-run the step.
            if skipped_leaves and not leaves:
                _emit_empty_run(compiled, args.output_format)
                return 0

        manifest = (
            Manifest.load(args.manifest.expanduser().resolve())
            if getattr(args, "manifest", None) is not None
            else None
        )
        close_gate = build_close_gate() if getattr(args, "close_gate", False) else None
        budget = None
        if getattr(args, "max_invocations", None) is not None or getattr(
            args, "max_cost", None
        ) is not None:
            budget = RunBudget(
                max_invocations=args.max_invocations,
                max_cost=args.max_cost,
            )
        informed_fixer = None
        max_fix_rounds = 0
        if getattr(args, "fix_with_backend", False):
            if close_gate is None:
                print(
                    "tessellum composer run: --fix-with-backend requires "
                    "--close-gate (there is no gate to repair against).",
                    file=sys.stderr,
                )
                return 2
            informed_fixer = make_llm_fixer(backend, budget=budget)
            max_fix_rounds = getattr(args, "max_fix_rounds", 1)
        stats_path = (
            args.stats.expanduser().resolve()
            if getattr(args, "stats", None) is not None
            else None
        )
        wave_gate = build_wave_gate() if getattr(args, "wave_gate", False) else None
        context_assembler = None
        if getattr(args, "context_strategy", None) is not None:
            if args.context_max_chars is not None:
                context_assembler = get_assembler(
                    args.context_strategy, max_chars=args.context_max_chars
                )
            else:
                context_assembler = get_assembler(args.context_strategy)
        run = run_pipeline_dynamic(
            compiled,
            leaves=leaves,
            backend=backend,
            vault_root=vault_root,
            dry_run=args.dry_run,
            runs_dir=runs_dir,
            max_workers=getattr(args, "workers", 4),
            manifest=manifest,
            close_gate=close_gate,
            informed_fixer=informed_fixer,
            max_fix_rounds=max_fix_rounds,
            budget=budget,
            stats_path=stats_path,
            wave_gate=wave_gate,
            context_assembler=context_assembler,
        )
        # The manifest is a rebuildable projection; persist the final state so
        # a later run can resume from it (the write-side already saved per-leaf
        # when a manifest path was set, but a path-less Manifest.load with a
        # real path also benefits from a final flush).
        if manifest is not None and manifest.path is not None:
            manifest.save()
    else:
        run = run_pipeline(
            compiled,
            leaves=leaves,
            backend=backend,
            vault_root=vault_root,
            dry_run=args.dry_run,
            runs_dir=runs_dir,
            progress=getattr(args, "progress", False),
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
                "tessellum composer batch: --backend=anthropic requires the "
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
            # Default canned response gives every default dim a score of 4 —
            # useful as a sanity check that the rubric pipeline runs
            # end-to-end. Driven by DEFAULT_RUBRIC_DIMENSIONS so adding a
            # new rubric dimension does not require editing the CLI in
            # lockstep.
            from tessellum.composer import DEFAULT_RUBRIC_DIMENSIONS

            judge_responses = {
                "Rubric dimensions to score": json.dumps(
                    {d: {"score": 4, "justification": "ok"} for d in DEFAULT_RUBRIC_DIMENSIONS}
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


# ── tessellum composer digest ──────────────────────────────────────────────


def _build_backend_for(args) -> "LLMBackend | int":
    """Construct the LLM backend for a run/digest command (or return an exit
    code on failure). Shared 3-way (mock | anthropic | bedrock) logic."""
    responses = None
    if getattr(args, "mock_responses", None) is not None:
        try:
            responses = json.loads(
                args.mock_responses.expanduser().resolve().read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as e:
            print(f"tessellum composer: --mock-responses load failed: {e}", file=sys.stderr)
            return 2
    if args.backend == "anthropic":
        try:
            from tessellum.composer import AnthropicBackend
            return AnthropicBackend(model=args.model or "claude-sonnet-4-6")
        except ImportError as e:
            print(f"tessellum composer: --backend=anthropic needs [agent] extras ({e})",
                  file=sys.stderr)
            return 2
    if args.backend == "bedrock":
        try:
            from tessellum.composer import BedrockBackend
            return BedrockBackend(
                model=args.model or "us.anthropic.claude-sonnet-4-6",
                region=args.region, aws_profile=args.aws_profile,
            )
        except ImportError as e:
            print(f"tessellum composer: --backend=bedrock needs [agent] extras ({e})",
                  file=sys.stderr)
            return 2
    return MockBackend(responses=responses)


def run_composer_digest_cli(args: argparse.Namespace) -> int:
    skills_dir: Path = args.skills_dir.expanduser().resolve()
    if not skills_dir.is_dir():
        print(f"tessellum composer digest: {skills_dir} is not a directory", file=sys.stderr)
        return 2
    source_path: Path = args.source.expanduser().resolve()
    if not source_path.is_file():
        print(f"tessellum composer digest: --source {source_path} not found", file=sys.stderr)
        return 2
    try:
        source_leaf = json.loads(source_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"tessellum composer digest: --source is not valid JSON: {e}", file=sys.stderr)
        return 2
    if not isinstance(source_leaf, dict):
        print("tessellum composer digest: --source must be a JSON object", file=sys.stderr)
        return 2
    # M0: the plan skill references {{leaf.member_count}} / {{leaf.members}}; a
    # single-source CLI leaf is a corpus of one, so default those keys (never
    # emit a <missing leaf.members> sentinel into the plan prompt). A leaf that
    # already carries them (a multi-doc bundle leaf) is left untouched.
    source_leaf.setdefault("member_count", 1)
    source_leaf.setdefault("members", [])

    backend = _build_backend_for(args)
    if isinstance(backend, int):
        return backend

    policy = SignOffPolicy(use_agent=args.require_agent_signoff, use_human=False)
    # Conservative CLI auto-approver: when the agent rung is enabled headless,
    # approve (the program gate already vetted plan-structure + review verdict).
    agent_judge = (
        (lambda: AgentVerdict(approved=True, confidence=1.0, reason="cli auto-approve"))
        if args.require_agent_signoff
        else None
    )

    result = run_digestion_pipeline(
        skills_dir=skills_dir,
        source_leaf=source_leaf,
        backend=backend,
        vault_root=args.vault.expanduser().resolve(),
        dry_run=args.dry_run,
        sign_off_policy=policy,
        agent_judge=agent_judge,
    )

    if args.output_format == "json":
        print(json.dumps({
            "completed": result.completed,
            "stopped_at": result.stopped_at,
            "sign_off": (
                {"decision": result.sign_off.decision, "rung": result.sign_off.deciding_rung}
                if result.sign_off else None
            ),
            "phases": [
                {"phase": p.phase, "ran": p.ran, "error_count": p.error_count}
                for p in result.phases
            ],
        }, indent=2))
    else:
        print("digestion pipeline: plan → augment → review →[sign-off]→ execute")
        for p in result.phases:
            print(f"  {'OK ' if p.error_count == 0 else 'ERR'}  {p.phase:8s}  errors={p.error_count}")
        if result.sign_off:
            print(f"  sign-off: {result.sign_off.decision} (via {result.sign_off.deciding_rung})")
        print(f"  → completed={result.completed}"
              + (f"  stopped_at={result.stopped_at}" if result.stopped_at else ""))
    return 0 if result.completed else 1


# ── tessellum composer scaffold-sidecar ────────────────────────────────────


def run_composer_scaffold_cli(args: argparse.Namespace) -> int:
    """Print starter ```yaml``` contract blocks for a single-file skill.

    Reads ``<!-- :: section_id = X :: -->`` markers in the canonical and
    emits one CORE-step contract block per section, chained by ``depends_on``
    (each step waits on the previous one). Materializer defaults to
    ``no_op``; aggregation defaults to ``per_leaf``. The author pastes each
    block beneath its section heading, then writes the step's prompt prose.
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

    # Single-file world: there is no separate sidecar to write. Emit the
    # per-section ```yaml``` contract blocks for the author to paste beneath
    # each heading in the canonical.
    blocks = _render_contract_blocks(skill_path.stem, section_ids)
    print(blocks, end="" if blocks.endswith("\n") else "\n")
    if not args.stdout:
        print(
            f"\n# {len(section_ids)} section(s) in {skill_path.name}: "
            f"{', '.join(section_ids)}",
            file=sys.stderr,
        )
        print(
            "# Paste each contract block beneath its heading, write the prompt "
            f"prose, then `tessellum composer validate {skill_path.name}`.",
            file=sys.stderr,
        )
    return 0


def _render_contract_blocks(skill_stem: str, section_ids: list[str]) -> str:
    """Emit one ```yaml``` contract block per section, to paste under each
    anchor in the single-file canonical (one CORE step per section, chained
    linearly via depends_on). This is authoring guidance printed to stdout;
    the author pastes each block beneath its section heading.
    """
    out: list[str] = [
        f"# Contract blocks for {skill_stem}.md — paste each ```yaml``` block",
        "# directly beneath its matching `<!-- :: section_id = X :: -->`",
        "# heading, then write the step's prompt prose after it.",
        "",
    ]
    for i, sid in enumerate(section_ids):
        depends = f"[{section_ids[i - 1]}]" if i > 0 else "[]"
        out.extend(
            [
                f"## <heading> <!-- :: section_id = {sid} :: -->",
                "",
                "```yaml",
                "role: CORE                  # CORE | DEFERRED | INFRA",
                "aggregation: per_leaf       # per_leaf | cross_leaf | corpus_wide",
                "batchable: false",
                f"depends_on: {depends}",
                "materializer: no_op         # a key from MATERIALIZER_CONTRACTS",
                f"output_key: {sid}_output",
                "```",
                "",
                f'TODO: write the prompt for "{sid}". Reference {{{{leaf.X}}}}'
                " per-leaf data and {{upstream.Y}} outputs from previous steps.",
                "",
            ]
        )
    return "\n".join(out)
