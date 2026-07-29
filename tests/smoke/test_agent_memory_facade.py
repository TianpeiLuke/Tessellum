"""A5.3 (FZ 20k9c1a1a1b7c2k1a) — the AgentMemory facade: a naming pass with
NO new behavior; every method delegates to the seam that owns its tier."""
from __future__ import annotations

from pathlib import Path

from tessellum.composer.agent_memory import AgentMemory


def _mem(tmp_path: Path) -> AgentMemory:
    skills = tmp_path / "skills"
    skills.mkdir()
    (skills / "skill_demo.md").write_text(
        "# D\n\n## S <!-- :: section_id = s1 :: -->\n\n"
        "```yaml\nrole: CORE\naggregation: corpus_wide\nbatchable: false\n"
        "depends_on: []\nmaterializer: no_op\noutput_key: o\n```\n\nBody.\n",
        encoding="utf-8",
    )
    return AgentMemory(
        artifacts_dir=tmp_path / "artifacts",
        runs_dir=tmp_path / "runs",
        index_db=None,
        skills_dir=skills,
    )


def test_working_tier_delegates_to_the_artifact_store(tmp_path: Path) -> None:
    mem = _mem(tmp_path)
    store = mem.working_put({"plan_text": "# Of-record plan"})
    assert "plan_text" in store
    assert mem.working_get("plan_text") == "# Of-record plan"
    assert mem.working_get("nope") is None


def test_episodic_tier_appends_timestamped_records(tmp_path: Path) -> None:
    mem = _mem(tmp_path)
    mem.episodic_append("decisions", {"what": "tested the facade"})
    recs = mem.episodic_read("decisions")
    assert len(recs) == 1 and recs[0]["what"] == "tested the facade"
    assert "at" in recs[0]
    assert mem.episodic_read("absent") == []


def test_semantic_tier_bootstrap_posture(tmp_path: Path) -> None:
    assert _mem(tmp_path).semantic_search("anything") == []


def test_procedural_tier_compiles_skills(tmp_path: Path) -> None:
    pipeline = _mem(tmp_path).procedural_load("skill_demo")
    assert pipeline.steps[0].section_id == "s1"
