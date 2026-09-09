#!/usr/bin/env python3
"""Reader-side answer eval for a digested vault: can a model ANSWER from what
Tessellum retrieves, and does it COMMIT when the answer is in front of it?

Why this exists
---------------
``score.py`` scores note CONSTRUCTION — coverage, density, grounding, fidelity,
the N-gates. It has no reader, no answer scoring, no refusal metric. A benchmark
arc on the same digestion pipeline showed a vault can hit every construction
target and still lose to plain chunking, entirely on reader refusal: the notes
retrieved the answer MORE often than chunks and extracted it MORE accurately,
and lost because the reader declined to commit. Construction gates were
uniformly green while that happened. This harness is what makes that visible,
and it is what every other improvement must be measured against.

What it measures
----------------
For each question, retrieve a context from an indexed vault through
Tessellum's own retrieval, hand it to a reader through Tessellum's own
``LLMBackend`` layer with a FIXED system prompt that offers an explicit
abstention token, and score the reply. Reported per arm:

  entity / polarity   accuracy on the two gold strata, NEVER pooled into one
                      headline: polarity (yes/no) is near chance and dominated
                      by the model's yes-prior; entity is the informative one.
  refused             share of answerable questions the reader abstained on.
  abstain@null        share of unanswerable questions it correctly abstained on.
  P(refuse | answer in context) vs P(refuse | absent)
                      refusal on questions whose answer WAS in the context is
                      the recoverable headroom, and the number that moves.
  transport           calls whose reply was a provider error, excluded from
                      every metric rather than scored as content.

Two baselines sit in the same table because neither stratum is interpretable
without them: ``_majority`` (per-stratum modal gold, no model call) and
``_closed_book`` (the reader with no context). An arm that fails to beat
closed-book has not shown that retrieval contributed anything.

Scoring rules, each of which corrects a specific defect seen in an earlier
scorer (see the docstrings on the functions):

  is_refusal    leading-token test, not substring.
  normalise     punctuation -> SPACE, not deletion.
  tok_contains  contiguous TOKEN-subsequence containment, not substring.
  gold_class    polarity vs entity stratification.
  transport_reason
                a provider error arriving AS the response text is transport.
  candidate pool
                scales with the token budget (``max(40, budget // 24)``).

Golden format
-------------
No question/answer golden existed in this eval set (``golden_facts.json`` is
structural), so a slice may carry a ``questions.json`` beside it::

    {"slice": "claude_code_mcp",
     "questions": [
       {"qid": "q01", "question": "…?", "gold": "claude mcp add",
        "evidence_notes": ["cc_mcp_quickstart.md"]},
       {"qid": "q13", "question": "Is local the default scope?", "gold": "yes"},
       {"qid": "q18", "question": "…?", "null": true}
     ]}

``gold`` is one short span (a name, a command, a path, a number, or
yes/no/true/false — the polarity stratum is detected from it). ``null: true``
marks an unanswerable question (tests abstention; ``gold`` is ignored).
``evidence_notes`` is optional: vault-relative note ids that contain the
answer, used only for the evidence-recall diagnostic. A bare JSON list of the
same objects is accepted too.

Usage
-----
    python eval/digestion_pipeline/answer_eval.py eval/digestion_pipeline/claude_code_mcp \
        --arms golden=eval/digestion_pipeline/claude_code_mcp/golden_notes \
        --backend anthropic --model claude-sonnet-4-6 --budget 2048 \
        --json /tmp/answers.json

An arm is ``name=VAULT_DIR[:strategy]`` (indexed into ``--db-dir``) or
``name=index.db[:strategy]``; strategy is ``hybrid`` (default), ``bm25``,
``dense`` or ``router``. ``--backend mock`` answers INSUFFICIENT to everything
and is the dry run. Exit 0 normally, 1 when any arm lost more than 5% of its
calls to transport (its metrics are then not comparable to a clean run), 2 when
the questions file is missing or malformed.

Requires the ``tessellum`` package (unlike ``score.py``): retrieval and the
reader are Tessellum's own. ``tiktoken`` is optional — without it the token
budget is approximated as words × 1.3 and a warning is printed once.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sqlite3
import string
import sys
import tempfile
import warnings
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Literal, Sequence

_REPO = Path(__file__).resolve().parents[2]
try:  # a checkout without an editable install: fall back to src/
    import tessellum  # noqa: F401
except ImportError:  # pragma: no cover — environment-dependent
    sys.path.insert(0, str(_REPO / "src"))

from tessellum.composer.context_assembler import _fts5_safe_query  # noqa: E402
from tessellum.composer.error_taxonomy import classify_reason  # noqa: E402
from tessellum.composer.llm import (  # noqa: E402
    LLMBackend,
    LLMRequest,
    LLMResponse,
    MockBackend,
)
from tessellum.indexer import build  # noqa: E402
from tessellum.retrieval import bm25_search, dense_search, hybrid_search, route  # noqa: E402

REFUSAL_TOKEN = "INSUFFICIENT"
POLARITY = {"yes": "yes", "true": "yes", "no": "no", "false": "no"}
Strategy = Literal["hybrid", "bm25", "dense", "router"]
STRATEGIES: tuple[str, ...] = ("hybrid", "bm25", "dense", "router")
Condition = Literal["tokens", "slots"]

# FIXED across every arm, condition and run. The only thing that varies between
# arms is the retrieved context, so any difference in answer quality is
# attributable to the retrieval representation and not to prompting.
SYSTEM_PROMPT = (
    "You are a question-answering system. Answer strictly from the context you "
    "are given, never from prior knowledge.\n"
    "- Reply with the shortest span that answers the question: a name, a "
    "command, a path, a number, a date, or yes/no.\n"
    "- Do not explain, do not restate the question, do not cite the context.\n"
    f"- If the context does not contain the answer, reply with exactly: {REFUSAL_TOKEN}\n"
    "- Never call a tool. Reply with the answer text only."
)

USER_TEMPLATE = "Context:\n{context}\n\nQuestion: {question}\nAnswer:"

# Bootstrap resamples and the seed both fixed so two runs over the same answer
# files print the same interval.
BOOTSTRAP_RESAMPLES = 4000
BOOTSTRAP_SEED = 20260902

# Above this share of transport-failed calls an arm's survivors are a biased
# sample (the failures cluster in time, not at random over questions).
MAX_TRANSPORT_FRACTION = 0.05


# ─────────────────────────────────────────────────────────────── scoring ────


def normalise(s: str) -> str:
    """Lower-case, map punctuation to SPACE, drop articles, collapse whitespace.

    Punctuation is replaced, not deleted: deletion turned ``Sam Bankman-Fried``
    into the single token ``sambankmanfried``, so a model that wrote the name
    with a space scored zero against it.
    """
    s = s.lower().strip()
    s = "".join(" " if c in string.punctuation else c for c in s)
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return " ".join(s.split())


def gold_class(gold: str) -> str:
    """``"polarity"`` for a yes/no/true/false gold, else ``"entity"``.

    Reported as two strata, never pooled: about two thirds of answerable golds
    in a typical set are polarity, and that stratum is near chance for a model
    with a yes-prior while entity is near ceiling. A pooled headline hides both.
    """
    return "polarity" if normalise(gold) in POLARITY else "entity"


def is_refusal(ans: str) -> bool:
    """Refusal when the answer LEADS with the refusal token, or is empty.

    The model is told to reply with exactly ``INSUFFICIENT`` and in practice
    complies but often appends an explanation, which is still a refusal. The
    opposite case is what a substring test gets wrong: "The context is
    insufficient, but the answer is Apple" supplies an answer, and a substring
    test once reported 0.69 over-refusal alongside 0.53 contains on one run.
    """
    n = normalise(ans)
    if not n:
        return True
    toks = n.split()
    if toks and toks[0] == "answer":
        toks = toks[1:]
    return bool(toks) and toks[0] == REFUSAL_TOKEN.lower()


def tok_contains(ans: str, gold: str) -> bool:
    """True iff the normalised gold is a contiguous TOKEN subsequence of the answer.

    Character substring is wrong here: roughly a quarter of gold answers are
    the two-character string ``no``, which appears inside ``not``, ``north``
    and ``known``, so a character test scored almost any verbose answer as
    correct.
    """
    g, a = normalise(gold).split(), normalise(ans).split()
    if not g:
        return False
    return any(a[i : i + len(g)] == g for i in range(len(a) - len(g) + 1))


def verdict(ans: str) -> str | None:
    """The yes/no the model actually committed to, from its leading token."""
    for line in ans.splitlines():
        n = normalise(line)
        if n:
            return POLARITY.get(n.split()[0])
    return None


def correct(ans: str, gold: str) -> float:
    """One binary outcome per question, appropriate to the gold's class.

    Polarity is scored by the extracted verdict rather than string equality,
    so a correct answer with a justification attached is not marked wrong. The
    gold is mapped through the same yes/no table as the verdict, so a
    ``true``/``false`` gold is comparable to a ``yes``/``no`` reply.
    """
    if is_refusal(ans):
        return 0.0
    if gold_class(gold) == "polarity":
        return float(verdict(ans) == POLARITY[normalise(gold)])
    return float(tok_contains(ans, gold))


# ───────────────────────────────────────────────────────── transport guard ────

# A relayed provider error is short; a real answer that merely MENTIONS billing
# can be long. Bodies above this length are never classified as transport.
_TRANSPORT_MAX_CHARS = 600

# Signatures of a provider / gateway error as they appear IN A RESPONSE BODY.
# Deliberately stricter than error_taxonomy.classify_reason, which is tuned for
# exception messages and matches the bare word "insufficient" — fine for an
# exception, fatal here, because "INSUFFICIENT" is also the abstention token a
# well-behaved reader emits on purpose. "Insufficient balance. Your Cline
# Credits balance is $-0.04" begins with the same word, and a whole run once
# scored as 74% deliberate abstention when the provider had simply stopped.
# Every pattern needs the billing / quota / gateway vocabulary, never the bare
# adjective; and the timeout form is the past-tense phrase a gateway relays
# ("timed out"), not "timeout", which is a legitimate answer span (MCP_TIMEOUT).
_TRANSPORT_SIGNATURE_RE = re.compile(
    "|".join(
        (
            r"insufficient\s+(balance|credits?|funds|quota)",
            r"credits?\s+balance",
            r"balance\s+is\s+too\s+low",
            r"out\s+of\s+credits",
            r"\bbilling\b",
            r"\bquota\b",
            r"payment\s+required",
            r"inference_cap",
            r"daily\s+(free\s+)?limit",
            r"\b(402|429)\b",
            r"rate[\s_-]?limit",
            r"too\s+many\s+requests",
            r"\bthrottl",
            r"\bunauthori[sz]ed\b",
            r"invalid\s+(api[\s_-]?)?key",
            r"authentication\s+(failed|error)",
            r"security\s+token",
            r"\btimed\s+out\b",
            r"\bread\s?timeout\b|\bconnect\s?timeout\b",
            r"connection\s+(reset|refused|aborted)",
            r"\beconnreset\b",
            r"\b50[234]\b\s*(bad\s+gateway|service\s+unavailable|gateway\s+time)",
            r"failed\s+to\s+(create|generate)\s+stream",
            r"inference\s+request\s+failed",
            r"failed\s+to\s+invoke\s+model",
            r'"error"\s*:\s*\{',
        )
    ),
    re.I,
)


def transport_reason(text: str | None) -> str | None:
    """Return a reason label if ``text`` IS a relayed provider error, else ``None``.

    Reuses :func:`tessellum.composer.error_taxonomy.classify_reason` for the
    label, behind two gates it does not have — the body must be SHORT and carry
    an explicit billing / quota / gateway signature — because on its own it
    maps the bare abstention token ``INSUFFICIENT`` to ``quota``. An empty body
    is a dropped call, not a refusal, and is reported as ``"empty"``.
    """
    if text is None or not text.strip():
        return "empty"
    t = text.strip()
    if len(t) > _TRANSPORT_MAX_CHARS:
        return None
    if not _TRANSPORT_SIGNATURE_RE.search(t):
        return None
    reason = classify_reason(t)
    return reason if reason != "unknown" else "transport"


# ─────────────────────────────────────────────────────────── token budget ────

_tokeniser: Callable[[str], int] | None = None


def _load_tokeniser() -> Callable[[str], int]:
    try:
        import tiktoken  # type: ignore[import-not-found]

        enc = tiktoken.get_encoding("cl100k_base")
        return lambda s: len(enc.encode(s, disallowed_special=()))
    except Exception:  # noqa: BLE001 — optional dependency / offline
        warnings.warn(
            "tiktoken unavailable; token budget approximated as words * 1.3",
            stacklevel=2,
        )
        return lambda s: int(len(s.split()) * 1.3)


def count_tokens(text: str) -> int:
    """cl100k_base token count when tiktoken is importable, else words × 1.3."""
    global _tokeniser
    if _tokeniser is None:
        _tokeniser = _load_tokeniser()
    return _tokeniser(text)


def candidate_pool(condition: str, *, k: int, budget: int) -> int:
    """How many ranked notes to consider before filling the budget.

    The pool must scale with the budget, not sit at a constant. A fixed 40
    penalises fine-grained notes specifically: 40 atoms carry about a quarter
    the text of 40 coarse notes, so a fine-grained vault saturated at 40 units
    and stopped improving past an 8K budget while the coarse one kept climbing.
    That is a harness ceiling, not a property of the notes.
    """
    return k if condition == "slots" else max(40, budget // 24)


# ────────────────────────────────────────────────────────────── questions ────


@dataclass(frozen=True)
class Question:
    qid: str
    question: str
    gold: str = ""
    null: bool = False
    evidence_notes: tuple[str, ...] = ()

    @property
    def cls(self) -> str:
        return "null" if self.null else gold_class(self.gold)


def load_questions(path: Path | str) -> list[Question]:
    """Read a ``questions.json`` (object with ``questions`` or a bare list)."""
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    rows = data.get("questions") if isinstance(data, dict) else data
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{p}: expected a non-empty list of questions")
    out: list[Question] = []
    seen: set[str] = set()
    for i, r in enumerate(rows):
        qid = str(r.get("qid") or f"q{i + 1:03d}")
        if qid in seen:
            raise ValueError(f"{p}: duplicate qid {qid!r}")
        seen.add(qid)
        text = (r.get("question") or "").strip()
        if not text:
            raise ValueError(f"{p}: question {qid!r} has no text")
        null = bool(r.get("null"))
        gold = "" if null else (r.get("gold") or "").strip()
        if not null and not gold:
            raise ValueError(f"{p}: question {qid!r} needs a gold or null: true")
        out.append(
            Question(
                qid=qid,
                question=text,
                gold=gold,
                null=null,
                evidence_notes=tuple(r.get("evidence_notes") or ()),
            )
        )
    return out


# ─────────────────────────────────────────────────────────────── retrieval ────


@dataclass(frozen=True)
class RetrievedContext:
    """What an arm handed the reader for one question."""

    context: str
    note_ids: list[str]
    tokens: int


def index_has_dense(db_path: Path | str) -> bool:
    """True iff the index carries dense vectors (``notes_vec`` non-empty)."""
    try:
        import sqlite_vec  # type: ignore[import-not-found]

        conn = sqlite3.connect(str(db_path))
        try:
            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            conn.enable_load_extension(False)
            return conn.execute("SELECT count(*) FROM notes_vec").fetchone()[0] > 0
        finally:
            conn.close()
    except Exception:  # noqa: BLE001 — no extension / no table → no dense
        return False


def load_bodies(db_path: Path | str) -> dict[str, str]:
    """Evidence-only note text per note_id.

    ``notes_fts.body`` is what the indexer stored after
    :func:`tessellum.format.parser.strip_scaffolding` — Related Notes / Source
    / References already removed — so the reader's budget goes on prose, not
    on lists of links it cannot follow.
    """
    conn = sqlite3.connect(str(db_path))
    try:
        return {nid: body or "" for nid, body in conn.execute("SELECT note_id, body FROM notes_fts")}
    finally:
        conn.close()


class VaultArm:
    """One retrieval arm: an indexed vault plus the Tessellum strategy that ranks it.

    Retrieval goes through Tessellum's public API (:func:`hybrid_search`,
    :func:`bm25_search`, :func:`dense_search`, :func:`route`). The raw question
    is passed as the dense query and the FTS5-safe ``OR``-bag as the lexical
    query, the same split ``composer.related_notes`` uses. One deviation is
    recorded rather than hidden: when the index has no dense vectors, the
    ``hybrid`` strategy calls ``bm25_search`` directly — exactly what
    ``hybrid_search`` degrades to, minus a multi-second encoder load per
    process — and ``dense_available`` is reported on the arm.
    """

    def __init__(
        self,
        name: str,
        db_path: Path | str,
        *,
        strategy: str = "hybrid",
        count: Callable[[str], int] = count_tokens,
    ) -> None:
        if strategy not in STRATEGIES:
            raise ValueError(f"unknown strategy {strategy!r}; known: {', '.join(STRATEGIES)}")
        self.name = name
        self.db_path = Path(db_path)
        self.strategy = strategy
        self.bodies = load_bodies(self.db_path)
        self.tokens = {nid: count(body) for nid, body in self.bodies.items()}
        self.dense_available = index_has_dense(self.db_path)

    @classmethod
    def from_vault(
        cls,
        name: str,
        vault_dir: Path | str,
        db_path: Path | str,
        *,
        strategy: str = "hybrid",
        with_dense: bool = True,
        count: Callable[[str], int] = count_tokens,
    ) -> "VaultArm":
        """Index ``vault_dir`` into ``db_path`` (overwriting) and wrap it."""
        build(vault_dir, db_path, force=True, with_dense=with_dense)
        return cls(name, db_path, strategy=strategy, count=count)

    def describe(self) -> str:
        if self.strategy == "hybrid" and not self.dense_available:
            return "hybrid (bm25-only: index has no dense vectors)"
        return self.strategy

    def rank(self, question: str, want: int) -> list[str]:
        """Ranked note ids for ``question`` from Tessellum's retrieval."""
        fts = _fts5_safe_query(question)
        if not fts or want <= 0:
            return []
        if self.strategy == "bm25" or (self.strategy == "hybrid" and not self.dense_available):
            hits = bm25_search(self.db_path, fts, k=want, snippet_length=None)
        elif self.strategy == "hybrid":
            hits = hybrid_search(self.db_path, fts, dense_query=question, k=want)
        elif self.strategy == "dense":
            hits = dense_search(self.db_path, question, k=want)
        else:  # router
            _, hits = route(self.db_path, fts, dense_query=question, k=want)
        return [h.note_id for h in hits]

    def build_context(
        self,
        question: str,
        *,
        condition: str = "tokens",
        k: int = 10,
        budget: int = 2048,
    ) -> RetrievedContext:
        """Assemble the context handed to the reader.

        ``tokens``: notes in rank order until the token budget is full — an
        over-running note is skipped and filling continues with the next, so
        a single large note cannot end the fill early. ``slots``: the top
        ``k`` notes however many tokens they cost.
        """
        want = candidate_pool(condition, k=k, budget=budget)
        picked: list[str] = []
        used = 0
        for nid in self.rank(question, want):
            t = self.tokens.get(nid, 0)
            if condition == "slots":
                if len(picked) >= k:
                    break
            else:
                if used >= budget:
                    break
                if used + t > budget:
                    continue
            picked.append(nid)
            used += t
        return RetrievedContext(
            context="\n\n---\n\n".join(self.bodies[n] for n in picked),
            note_ids=picked,
            tokens=used,
        )


# ────────────────────────────────────────────────────────────────── reader ────


def make_request(context: str, question: str, *, max_tokens: int = 128) -> LLMRequest:
    """The one request shape every arm uses: fixed prompt, temperature 0."""
    return LLMRequest(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=USER_TEMPLATE.format(context=context, question=question),
        max_tokens=max_tokens,
        temperature=0.0,
    )


@dataclass
class AnswerRecord:
    """One scored reply. ``transport`` set ⇒ excluded from every metric."""

    qid: str
    question: str
    gold: str
    null: bool
    cls: str
    answer: str
    refused: bool
    correct: float
    transport: str | None
    stop_reason: str | None
    note_ids: list[str] = field(default_factory=list)
    context_tokens: int = 0
    answer_in_context: bool | None = None
    evidence_hit: bool | None = None
    elapsed_ms: float = 0.0
    backend_id: str = ""


def score_response(
    q: Question,
    response: LLMResponse | None,
    ctx: RetrievedContext | None = None,
    *,
    error: str | None = None,
) -> AnswerRecord:
    """Turn one reply into a record. A raised backend error or a provider
    error arriving as the reply text are both transport, never content."""
    text = response.content if response is not None else ""
    meta = response.metadata if response is not None else {}
    transport = f"raised: {error[:120]}" if error else transport_reason(text)
    refused = False if transport else is_refusal(text)
    got = 0.0 if (transport or q.null) else correct(text, q.gold)
    in_ctx = None
    ev_hit = None
    if ctx is not None and not q.null:
        # Answer presence is an ENTITY-stratum notion: a literal yes/no token
        # in the context says nothing about a polarity question, so the
        # refusal diagnosis is computed on entity golds only.
        if q.cls == "entity":
            in_ctx = tok_contains(ctx.context, q.gold)
        if q.evidence_notes:
            ev_hit = any(n in ctx.note_ids for n in q.evidence_notes)
    return AnswerRecord(
        qid=q.qid,
        question=q.question,
        gold=q.gold,
        null=q.null,
        cls=q.cls,
        answer=text,
        refused=refused,
        correct=got,
        transport=transport,
        stop_reason=meta.get("stop_reason"),
        note_ids=list(ctx.note_ids) if ctx else [],
        context_tokens=ctx.tokens if ctx else 0,
        answer_in_context=in_ctx,
        evidence_hit=ev_hit,
        elapsed_ms=response.elapsed_ms if response is not None else 0.0,
        backend_id=response.backend_id if response is not None else "",
    )


def answer_one(
    backend: LLMBackend,
    q: Question,
    ctx: RetrievedContext,
    *,
    max_answer_tokens: int = 128,
) -> AnswerRecord:
    try:
        resp = backend.call(make_request(ctx.context, q.question, max_tokens=max_answer_tokens))
    except Exception as e:  # noqa: BLE001 — a raised call is transport, recorded not fatal
        return score_response(q, None, ctx, error=f"{type(e).__name__}: {e}")
    return score_response(q, resp, ctx)


def run_arm(
    arm: VaultArm,
    questions: Sequence[Question],
    backend: LLMBackend,
    *,
    condition: str = "tokens",
    k: int = 10,
    budget: int = 2048,
    max_answer_tokens: int = 128,
) -> list[AnswerRecord]:
    return [
        answer_one(
            backend,
            q,
            arm.build_context(q.question, condition=condition, k=k, budget=budget),
            max_answer_tokens=max_answer_tokens,
        )
        for q in questions
    ]


def run_closed_book(
    questions: Sequence[Question],
    backend: LLMBackend,
    *,
    max_answer_tokens: int = 128,
) -> list[AnswerRecord]:
    """The reader with no context at all: what it answers from prior knowledge
    (or its yes-prior). An arm that fails to beat this has shown nothing."""
    empty = RetrievedContext(context="", note_ids=[], tokens=0)
    out = []
    for q in questions:
        r = answer_one(backend, q, empty, max_answer_tokens=max_answer_tokens)
        r.answer_in_context = None
        r.evidence_hit = None
        out.append(r)
    return out


def majority_baseline(questions: Sequence[Question]) -> tuple[list[AnswerRecord], dict[str, str]]:
    """Per-STRATUM modal gold, no model call.

    The majority is computed per stratum because the two strata have different
    modes: a single constant answer scores zero on one of them and understates
    the floor. On a small curated slice the entity stratum has few distinct
    golds and its mode can be a large share of it.
    """
    modes: dict[str, str] = {}
    for cls in ("entity", "polarity"):
        golds = [normalise(q.gold) for q in questions if q.cls == cls]
        modes[cls] = Counter(golds).most_common(1)[0][0] if golds else ""
    records = []
    for q in questions:
        ans = modes.get(q.cls, "")
        records.append(
            AnswerRecord(
                qid=q.qid,
                question=q.question,
                gold=q.gold,
                null=q.null,
                cls=q.cls,
                answer=ans,
                refused=False,
                correct=0.0 if q.null else correct(ans, q.gold),
                transport=None,
                stop_reason=None,
                backend_id="_majority",
            )
        )
    return records, modes


# ───────────────────────────────────────────────────────────── statistics ────


def _mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def summarise(records: Sequence[AnswerRecord]) -> dict:
    """Per-arm metrics over the records that were NOT transport failures."""
    ok = [r for r in records if r.transport is None]
    ent = [r for r in ok if r.cls == "entity"]
    pol = [r for r in ok if r.cls == "polarity"]
    nul = [r for r in ok if r.null]
    answerable = ent + pol
    e_acc, p_acc = _mean([r.correct for r in ent]), _mean([r.correct for r in pol])
    strata = [x for x in (e_acc, p_acc) if x == x]  # drop NaN
    present = [r.refused for r in answerable if r.answer_in_context is True]
    absent = [r.refused for r in answerable if r.answer_in_context is False]
    ev = [r.evidence_hit for r in answerable if r.evidence_hit is not None]
    p_present = _mean([float(x) for x in present])
    n_transport = len(records) - len(ok)
    return {
        "n": len(records),
        "n_scored": len(ok),
        "n_transport": n_transport,
        "transport_fraction": n_transport / len(records) if records else 0.0,
        "transport_reasons": dict(Counter(r.transport for r in records if r.transport)),
        "n_entity": len(ent),
        "entity": e_acc,
        "n_polarity": len(pol),
        "polarity": p_acc,
        "macro": _mean(strata),
        "refused": _mean([float(r.refused) for r in answerable]),
        "n_null": len(nul),
        "abstain_null": _mean([float(r.refused) for r in nul]),
        "mean_notes": _mean([float(len(r.note_ids)) for r in ok]),
        "mean_context_tokens": _mean([float(r.context_tokens) for r in ok]),
        "truncated": sum(1 for r in ok if r.stop_reason == "max_tokens"),
        "evidence_recall": _mean([float(x) for x in ev]),
        "refusal_diagnosis": {
            "n_present": len(present),
            "p_refuse_answer_present": p_present,
            "n_absent": len(absent),
            "p_refuse_answer_absent": _mean([float(x) for x in absent]),
            # refusals on questions whose answer was already in the context:
            # the recoverable headroom.
            "wasted_refusals": int(round(len(present) * p_present)) if present else 0,
        },
    }


def paired_bootstrap(
    deltas: Sequence[float],
    *,
    n_resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[float, float]:
    """95% percentile interval of the mean of per-question deltas (pure Python)."""
    d = list(deltas)
    if not d:
        return 0.0, 0.0
    rng = random.Random(seed)
    n = len(d)
    means = sorted(sum(rng.choices(d, k=n)) / n for _ in range(n_resamples))

    def pct(p: float) -> float:
        i = min(max(int(round(p / 100 * (len(means) - 1))), 0), len(means) - 1)
        return means[i]

    return pct(2.5), pct(97.5)


def compare(
    base: Sequence[AnswerRecord],
    other: Sequence[AnswerRecord],
    *,
    seed: int = BOOTSTRAP_SEED,
) -> dict:
    """``other - base`` on SHARED, answerable, non-transport questions, per stratum."""
    bx = {r.qid: r for r in base if r.transport is None and not r.null}
    ox = {r.qid: r for r in other if r.transport is None and not r.null}
    out: dict = {}
    for cls in ("entity", "polarity", "both"):
        shared = [q for q in bx if q in ox and (cls == "both" or bx[q].cls == cls)]
        if not shared:
            continue
        d = [ox[q].correct - bx[q].correct for q in shared]
        lo, hi = paired_bootstrap(d, seed=seed)
        out[cls] = {
            "n": len(shared),
            "delta": _mean(d),
            "ci": [lo, hi],
            "significant": bool(lo > 0 or hi < 0),
        }
    return out


# ────────────────────────────────────────────────────────────────── driver ────


def run(
    questions: Sequence[Question],
    arms: dict[str, VaultArm],
    backend: LLMBackend,
    *,
    condition: str = "tokens",
    k: int = 10,
    budget: int = 2048,
    max_answer_tokens: int = 128,
    closed_book: bool = True,
    pairs: Sequence[str] = (),
) -> dict:
    """Answer every question under every arm plus the baselines; return the report.

    The report is JSON-serialisable: ``arms`` (per-arm summary + per-question
    records), ``comparisons`` (paired bootstrap for each ``a:b`` in ``pairs``),
    and the run settings.
    """
    records: dict[str, list[AnswerRecord]] = {}
    describe: dict[str, str] = {}
    for name, arm in arms.items():
        records[name] = run_arm(
            arm, questions, backend, condition=condition, k=k, budget=budget,
            max_answer_tokens=max_answer_tokens,
        )
        describe[name] = arm.describe()
    maj, modes = majority_baseline(questions)
    records["_majority"] = maj
    describe["_majority"] = "per-stratum modal gold, no model call"
    if closed_book:
        records["_closed_book"] = run_closed_book(
            questions, backend, max_answer_tokens=max_answer_tokens
        )
        describe["_closed_book"] = "reader with no context"

    # Every real arm is compared against both baselines automatically; explicit
    # pairs add arm-vs-arm comparisons.
    wanted = list(pairs)
    for name in arms:
        wanted.append(f"_majority:{name}")
        if closed_book:
            wanted.append(f"_closed_book:{name}")
    comparisons = {}
    for pair in wanted:
        x, _, y = pair.partition(":")
        if x in records and y in records and x != y:
            comparisons[pair] = compare(records[x], records[y])

    return {
        "settings": {
            "condition": condition,
            "k": k,
            "budget": budget,
            "max_answer_tokens": max_answer_tokens,
            "backend_id": getattr(backend, "backend_id", type(backend).__name__),
            "n_questions": len(questions),
            "majority_answers": modes,
        },
        "arms": {
            name: {
                "retrieval": describe[name],
                **summarise(recs),
                "per_question": [asdict(r) for r in recs],
            }
            for name, recs in records.items()
        },
        "comparisons": comparisons,
    }


def format_report(report: dict) -> str:
    """The console tables: strata + refusal diagnosis + paired comparisons."""
    arms = report["arms"]
    w = max(len(n) for n in arms)
    lines = []
    s = report["settings"]
    lines.append(
        f"{s['n_questions']} questions   backend={s['backend_id']}   "
        f"condition={s['condition']} "
        + (f"budget={s['budget']}" if s["condition"] == "tokens" else f"k={s['k']}")
    )
    lines.append(
        "majority baseline answers: "
        + ", ".join(f"{c}={v!r}" for c, v in s["majority_answers"].items())
    )
    lines.append("")
    lines.append(
        f"{'arm':<{w}}  {'n_ent':>6}{'entity':>8}  {'n_pol':>6}{'polarity':>9}"
        f"{'macro':>8}{'refuse':>8}{'abstain@null':>14}{'notes':>7}{'tokens':>8}{'trunc':>6}{'transport':>10}"
    )
    for n, a in arms.items():
        lines.append(
            f"{n:<{w}}  {a['n_entity']:>6}{a['entity']:>8.3f}  {a['n_polarity']:>6}{a['polarity']:>9.3f}"
            f"{a['macro']:>8.3f}{a['refused']:>8.3f}{a['abstain_null']:>14.3f}"
            f"{a['mean_notes']:>7.1f}{a['mean_context_tokens']:>8.0f}{a['truncated']:>6}{a['n_transport']:>10}"
        )
    lines.append("")
    lines.append("Refusal given what the reader actually received")
    lines.append(
        f"{'arm':<{w}}{'P(ref|absent)':>15}{'P(ref|present)':>16}{'present':>9}{'wasted':>8}{'ev.recall':>11}"
    )
    for n, a in arms.items():
        d = a["refusal_diagnosis"]
        lines.append(
            f"{n:<{w}}{d['p_refuse_answer_absent']:>15.3f}{d['p_refuse_answer_present']:>16.3f}"
            f"{d['n_present']:>9}{d['wasted_refusals']:>8}{a['evidence_recall']:>11.3f}"
        )
    for n, a in arms.items():
        if a["transport_fraction"] > MAX_TRANSPORT_FRACTION:
            lines.append(
                f"\n!! {n}: {a['n_transport']}/{a['n']} calls were transport failures "
                f"({a['transport_fraction']:.1%}, {a['transport_reasons']}). Metrics are on "
                f"survivors only and are NOT comparable to a clean run. Re-run before using them."
            )
    for pair, per_cls in report["comparisons"].items():
        x, _, y = pair.partition(":")
        lines.append(f"\n{y} - {x}")
        for cls, c in per_cls.items():
            sig = "significant" if c["significant"] else "ns"
            lines.append(
                f"   {cls:<9} n={c['n']:<5}{c['delta']:+.3f}   [{c['ci'][0]:+.3f}, {c['ci'][1]:+.3f}]  {sig}"
            )
    return "\n".join(lines)


def _make_backend(name: str, model: str | None, region: str) -> LLMBackend:
    if name == "mock":
        return MockBackend(default=REFUSAL_TOKEN)
    if name == "anthropic":
        from tessellum.composer.llm import AnthropicBackend

        return AnthropicBackend(model=model or "claude-sonnet-4-6")
    if name == "bedrock":
        from tessellum.composer.llm import BedrockBackend

        return BedrockBackend(model=model or "us.anthropic.claude-sonnet-4-6", region=region)
    raise SystemExit(f"unknown backend {name!r}")


def _parse_arm_spec(spec: str) -> tuple[str, Path, str]:
    name, _, rest = spec.partition("=")
    if not name or not rest:
        raise SystemExit(f"bad --arms entry {spec!r}; expected name=PATH[:strategy]")
    path_s, _, strat = rest.rpartition(":")
    if strat and strat in STRATEGIES and path_s:
        return name, Path(path_s), strat
    return name, Path(rest), "hybrid"


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("slice_dir", type=Path, help="curated-slice dir holding questions.json")
    ap.add_argument("--questions", type=Path, help="questions file (default <slice_dir>/questions.json)")
    ap.add_argument(
        "--arms", nargs="*", default=[],
        help="name=VAULT_DIR_or_INDEX_DB[:strategy]  (default: golden=<slice_dir>/golden_notes)",
    )
    ap.add_argument("--db-dir", type=Path, help="where to write index DBs (default: a temp dir)")
    ap.add_argument("--no-dense", action="store_true", help="index without dense vectors (BM25-only)")
    ap.add_argument("--backend", choices=["mock", "anthropic", "bedrock"], default="mock")
    ap.add_argument("--model", default=None)
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--condition", choices=["tokens", "slots"], default="tokens")
    ap.add_argument("--budget", type=int, default=2048, help="context token budget (tokens condition)")
    ap.add_argument("--k", type=int, default=10, help="notes per context (slots condition)")
    ap.add_argument("--max-answer-tokens", type=int, default=128)
    ap.add_argument("--no-closed-book", action="store_true", help="skip the closed-book baseline")
    ap.add_argument("--pairs", nargs="*", default=[], help="extra a:b paired comparisons")
    ap.add_argument("--json", type=Path, help="write the full report here")
    args = ap.parse_args(argv)

    qpath = args.questions or (args.slice_dir / "questions.json")
    if not qpath.exists():
        print(f"error: {qpath} not found (see the module docstring for the format)", file=sys.stderr)
        return 2
    try:
        questions = load_questions(qpath)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    specs = args.arms or [f"golden={args.slice_dir / 'golden_notes'}"]
    db_dir = args.db_dir or Path(tempfile.mkdtemp(prefix="answer_eval_"))
    arms: dict[str, VaultArm] = {}
    for spec in specs:
        name, path, strat = _parse_arm_spec(spec)
        if path.is_dir():
            arms[name] = VaultArm.from_vault(
                name, path, db_dir / f"{name}.db", strategy=strat, with_dense=not args.no_dense
            )
        elif path.is_file():
            arms[name] = VaultArm(name, path, strategy=strat)
        else:
            print(f"error: arm {name!r}: {path} is neither a vault dir nor an index DB", file=sys.stderr)
            return 2
        print(f"  {name}: {len(arms[name].bodies)} notes, retrieval={arms[name].describe()}")

    backend = _make_backend(args.backend, args.model, args.region)
    report = run(
        questions, arms, backend,
        condition=args.condition, k=args.k, budget=args.budget,
        max_answer_tokens=args.max_answer_tokens,
        closed_book=not args.no_closed_book, pairs=args.pairs,
    )
    report["slice"] = args.slice_dir.name
    print()
    print(format_report(report))
    print()
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=1), encoding="utf-8")
        print(f"wrote {args.json}")
    degraded = [n for n, a in report["arms"].items() if a["transport_fraction"] > MAX_TRANSPORT_FRACTION]
    return 1 if degraded else 0


if __name__ == "__main__":
    raise SystemExit(main())
