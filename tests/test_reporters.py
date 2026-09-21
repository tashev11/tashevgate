from pathlib import Path

from tashevgate.reporters.markdown import render_markdown
from tashevgate.reporters.sarif import render_sarif
from tashevgate.scanner import scan


def test_reports_render(tmp_path: Path):
    secret = "AKIA" + ("A" * 16)
    (tmp_path / "app.py").write_text(f'KEY="{secret}"\n', encoding="utf-8")

    result = scan(tmp_path)
    markdown = render_markdown(result)
    sarif = render_sarif(result)

    assert "BLOCKED" in markdown
    assert sarif["version"] == "2.1.0"
    assert sarif["runs"][0]["results"][0]["ruleId"] == "SECRET003"
