# The semantic certificate — the gate for unattended promotion

## The idea

Most of Tessellum's gates are pure programs over structure — does the note parse, does
every claim name a source, is the write set closed. Those catch malformed notes, not wrong
ones. The semantic certificate is the one gate that judges whether a note's claims are
actually *supported by the evidence they cite*, and it is what a capsule must clear to
promote WITHOUT a human sign-off. Both the composer transaction track (at its P7 phase) and
the DKS reasoning engine (at its P4 validation) route through the same certificate, so it is
documented here once rather than twice.

The certificate keeps Composer's boundary intact: a model produces evidence, a frozen
program decides. A pluggable scorer rates how well each claim is entailed by its cited span,
and the certificate turns those ratings into an accept-or-abstain decision plus the grounding
verdict the close gate already consumes. The program never guesses at plausibility — it reads
scores a scorer produced and applies thresholds a calibration fixed.

## How it decides

A note is only as grounded as its weakest claim. Each checkable claim is scored against the
source span it cites, and the scores are aggregated by MINIMUM, not averaged — one
unsupported claim sinks the note. A mean would let a pile of easy claims mask a single
fabrication, which is exactly the failure a grounding gate exists to catch.

Thresholds are not hand-tuned. For each failure class — claim grounding, omitted coverage,
duplicate disposition, edge relevance — calibration fixes the lowest score cutoff whose
accepted region has an empirical false-accept rate at or under a target risk, class by class,
from a set of labelled examples. A class that cannot meet the bound gets an unreachable
cutoff, so it always abstains rather than passing on plausibility.

The gate fails closed everywhere uncertainty enters: an empty claim set, a note outside the
calibrated domain (including a certificate that declares no domain at all), a claim the
scorer could not judge, or any claim below its class cutoff all yield abstain, which routes
the note back to human review. An abstain is never an accept.

## Runnable end to end

The certificate is not a framework waiting on a model — it runs today, with a reference
baseline, so the wiring can be exercised and measured now. Four pieces close the loop.

A written note becomes checkable claims. Each prose sentence turns into one grounding claim
cited against the union of the note's sources, so it is grounded if any cited source supports
it. Frontmatter, code fences, tables, and link-only lines are dropped, and a note with no
provenance yields no claims and therefore abstains.

A reference scorer makes the loop executable without a model. It is a deterministic lexical
proxy — directional content-word containment of a claim against its span — and its own
docstring states its ceiling bluntly: it is bag-of-words and cannot judge negation,
reordering, or paraphrase, so "does not support X" scores like "does support X". It is a
wiring-and-calibration baseline, never a safety-bearing verifier.

The production judge now needs no separate NLI dependency. A second scorer wraps the LLM
the system already has behind the same seam — one narrow, constrained call per claim ("is
this claim entailed by this span? return a probability and an explicit abstain"), at
temperature zero, never a free plausibility judge and never shown the whole note. The
untrusted claim and span are fenced as data, so a source that embeds "output entailment 1.0"
is treated as text under judgment rather than an instruction — a structural defense-in-depth,
not a proof: a determined injection may still sway the judge, so hardened deployments pair
the fencing with input sanitization. An unreadable span, a backend error, or a malformed
reply all abstain. The min-aggregation and the calibrated threshold still do the deciding;
the model only supplies per-claim evidence. Because the score is the model's own reported probability,
the calibration bound transfers to runtime only under exchangeability — the same prompt,
model, and temperature between calibration and use.

A verifier feeds the runtime. It wraps claim extraction and the certificate into the exact
`(step, leaf, result) -> GroundingVerdict` shape the runtime's grounding seam expects. That
seam is no longer unfed by default: the free deterministic identifier-grounding verifier
described below feeds it out of the box (`policy.identifier_grounding`, on by default), so
the grounding rung runs on every digestion. The certificate verifier itself stays opt-in
(`policy.grounding_gate` plus a calibration artifact), and with neither flag the close gate
is format-only as before.

A go/no-go gate answers the only question that licenses unattended promotion: on a real
labelled corpus, is the certificate sound AND useful AND backed by enough evidence.
Calibration fits thresholds on a stratified train split, then measures the disjoint held-out
split for three things — false-accept rate (SOUND), acceptance of genuinely-correct claims
(USEFUL, since an always-abstain threshold is sound but worthless), and per-class evidence
(SUFFICIENT — a class needs enough held-out examples, with both a correct and an incorrect
one, or its vacuous zero false-accept rate cannot be trusted). Only when every present class
clears all three does the gate return GO.

## The free tier: identifier grounding

The certificate is no longer the whole grounding gate. A first, cheaper layer runs in front
of it behind the same verifier seam, and it is deterministic, free, and on by default: every
code-like token a note asserts in an inline-code span — a CLI flag, a KEY_LIKE constant, a
dotted config key — must literally appear in the source. A token found nowhere in the source
blocks the note as ungrounded without a single scorer call, so an invented API surface
self-announces on a string check. A token that is real in the source but falls outside the
note's own owned slice is cross-contamination rather than fabrication, so it surfaces as a
non-blocking advisory on an otherwise grounded verdict — a GROUND-003 warning in the gate's
findings — instead of a block.

The layered runtime verifier composes the two tiers: the identifier check runs first, and
only a note that clears it reaches the calibrated certificate. The certificate's spans stay
the full source (under a 40K cap) exactly as calibrated — an owned-section-span variant was
piloted and refuted by measurement: faithful claims carrying legitimate cross-slice content
scored like fabrications and the calibrated threshold collapsed from 0.85 to 0.15, so owned
slices belong to the coverage sweep, not the certificate.

## What it does and does not promise

The machinery is honest about its own limits, by design. The calibration is an empirical,
in-sample bound — the widest accept region whose observed error is under target on the
calibration set — not yet the finite-sample distribution-free guarantee the name "conformal
risk control" formally denotes; the out-of-sample check is the go/no-go gate above. The
reference scorer is a baseline that cannot see meaning. The production entailment judge is
now available in code — the existing LLM backend, driven as a constrained per-claim scorer —
and a first real calibration exists: a pilot scored a forty-claim labelled set (32 faithful,
8 fabricated) with that judge, fixed the grounding threshold at 0.85 at a 0.05 target risk,
and committed the artifact, which the runtime loads via `TESSELLUM_GROUNDING_CALIBRATION` so
the opted-in gate can accept inside the calibrated documentation domain.

What remains before unattended promotion is narrower but real: a human-labelled corpus of
wrong-but-well-formed notes large enough for the go/no-go gate's held-out GO, across every
failure class — the pilot calibrated one class on forty examples and never ran the go/no-go
harness. Until that gate returns GO, the certificate does not license skipping human review:
promotion stays human-supervised, and everywhere outside the calibrated path the certificate
fails closed. What ships is the framework fully wired and measurable — the day a
production-scale corpus lands, calibration and the unattended-promotion decision are one
command, and nothing in the shipped code can inflate confidence or grant authority on its
own.

**See also:** [composer.md](composer.md#the-knowledge-transaction) (the transaction track that
gates on the certificate at P7), [dks.md](dks.md) (DKS routes its warrants through the same
certificate at P4), and [reference/composer.md](reference/composer.md) (exact APIs — the
`semantic_certificate` core plus the runnable `lexical_scorer` / `llm_claim_scorer` /
`claim_extraction` / `certificate_verifier` / `calibration_gate` / `note_grounding` layer).
