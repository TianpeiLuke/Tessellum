from __future__ import annotations

import json

from tessellum.cli.main import main


def test_runtime_init_submit_get_and_cancel(tmp_path, capsys) -> None:
    assert main(["runtime", "init", "--root", str(tmp_path)]) == 0
    capsys.readouterr()
    source = tmp_path / "inbox" / "papers" / "paper.md"
    source.write_text("evidence", encoding="utf-8")

    assert main(["runtime", "submit", str(source), "--root", str(tmp_path)]) == 0
    submitted = json.loads(capsys.readouterr().out)
    assert submitted["created"] is True
    job_id = submitted["job_id"]

    assert main(["runtime", "get", job_id, "--events", "--root", str(tmp_path)]) == 0
    fetched = json.loads(capsys.readouterr().out)
    assert fetched["state"] == "admitted"
    assert fetched["events"][0]["event_type"] == "admitted"

    assert main(["runtime", "cancel", job_id, "--root", str(tmp_path)]) == 0
    cancelled = json.loads(capsys.readouterr().out)
    assert cancelled["cancel_requested"] is True


def test_runtime_doctor_reports_absolute_paths(tmp_path, capsys) -> None:
    main(["runtime", "init", "--root", str(tmp_path)])
    capsys.readouterr()
    code = main(["runtime", "doctor", "--root", str(tmp_path)])
    result = json.loads(capsys.readouterr().out)
    assert result["paths"]["root"] == str(tmp_path.resolve())
    assert code == 1
