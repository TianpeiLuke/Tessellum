#!/bin/bash
# R3.3 (FZ 20k9c1a1a1b7c2k2a1c): the promoted service-path eval harness —
# one golden slice through the LITERAL production entrypoint.
# Usage: sweep_service_path.sh <slice_name>
set -e
SLICE=$1
ROOT=runs/eval/sweep_${SLICE}
rm -rf "$ROOT"
mkdir -p "$ROOT/vault/resources/skills" "$ROOT/inbox"
cp vault/resources/skills/skill_tessellum_{plan_digestion,augment_digestion_plan,review_digestion_plan,execute_digestion_plan}.md "$ROOT/vault/resources/skills/"
# Phase-1 instrument fix (FZ b7c2k2a3a): seed the eval vault so N6 measures
# the system, not the harness — a small term-dictionary convention set + a
# prebuilt index (related_notes_db resolves; the enrichment runs; writers can
# actually earn the xref floor). N3 needs NO seeding (BB_SPECS is in code —
# openclaw scored N3=1.0 on an empty vault; the earlier 'harness artifact'
# claim for N3 was wrong and is corrected in the trail).
# N6 v2 (FZ k2a4a): seed the FULL term dictionary — a 5-term semantic tier
# cannot host any term-link floor; the metric must have headroom to measure.
mkdir -p "$ROOT/vault/resources/term_dictionary"
cp vault/resources/term_dictionary/term_*.md "$ROOT/vault/resources/term_dictionary/" 2>/dev/null || true
PYTHONPATH=src python3 -m tessellum.cli.main runtime init --root "$ROOT" > /dev/null
mkdir -p "$ROOT/data"
PYTHONPATH=src python3 -m tessellum.cli.main index build --vault "$ROOT/vault" --db "$ROOT/data/tessellum.db" --no-dense > /dev/null 2>&1 || true
python3 - "$SLICE" "$ROOT" <<'PYEOF'
import sys
from pathlib import Path
slice_name, root = sys.argv[1], sys.argv[2]
pages = sorted(Path(f"eval/digestion_pipeline/{slice_name}/input_pages").glob("*.md*"))
corpus = "\n\n".join(p.read_text(encoding="utf-8") for p in pages)
out = Path(root) / "inbox" / "general" / f"{slice_name}.md"
out.write_text(corpus, encoding="utf-8")
print(f"{slice_name}: {len(pages)} pages, {len(corpus)} chars")
PYEOF
PYTHONPATH=src python3 -m tessellum.cli.main runtime submit "$ROOT/inbox/general/${SLICE}.md" --profile converge --root "$ROOT" | python3 -c "import json,sys; print('job:', json.load(sys.stdin)['job_id'])"
PYTHONPATH=src python3 -m tessellum.cli.main runtime work --backend anthropic --model claude-sonnet-4-6 --root "$ROOT"
