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
wiring-and-calibration baseline, never a safety-bearing verifier. The real NLI or SummaC
model drops into the same seam in production.

A verifier feeds the runtime. It wraps claim extraction and the certificate into the exact
`(step, leaf, result) -> GroundingVerdict` shape the previously-unfed grounding seam expects,
so wiring it in makes a digestion's grounding gate actually consult the certificate. It is
opt-in, and the default path stays byte-identical.

A go/no-go gate answers the only question that licenses unattended promotion: on a real
labelled corpus, is the certificate sound AND useful AND backed by enough evidence.
Calibration fits thresholds on a stratified train split, then measures the disjoint held-out
split for three things — false-accept rate (SOUND), acceptance of genuinely-correct claims
(USEFUL, since an always-abstain threshold is sound but worthless), and per-class evidence
(SUFFICIENT — a class needs enough held-out examples, with both a correct and an incorrect
one, or its vacuous zero false-accept rate cannot be trusted). Only when every present class
clears all three does the gate return GO.

## What it does and does not promise

The machinery is honest about its own limits, by design. The calibration is an empirical,
in-sample bound — the widest accept region whose observed error is under target on the
calibration set — not yet the finite-sample distribution-free guarantee the name "conformal
risk control" formally denotes; the out-of-sample check is the go/no-go gate above. The
shipped scorer is a baseline that cannot see meaning. And a production entailment model plus
a human-labelled corpus of wrong-but-well-formed notes remain an external, non-code
prerequisite.

So until that corpus arrives and the go/no-go gate returns GO on it, the certificate does not
license skipping human review: promotion stays human-supervised and the certificate fails
closed. What ships is the framework fully wired and measurable — the day a real model and
corpus land, calibration and the unattended-promotion decision are one command, and nothing
in the shipped code can inflate confidence or grant authority on its own.

**See also:** [composer.md](composer.md#the-knowledge-transaction) (the transaction track that
gates on the certificate at P7), [dks.md](dks.md) (DKS routes its warrants through the same
certificate at P4), and [reference/composer.md](reference/composer.md) (exact APIs — the
`semantic_certificate` core plus the runnable `lexical_scorer` / `claim_extraction` /
`certificate_verifier` / `calibration_gate` layer).
