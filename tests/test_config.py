from pathlib import Path

from vibegate.scanner import scan


def test_rule_can_be_disabled(tmp_path: Path):
    (tmp_path / ".env").write_text("TOKEN=not-a-real-secret\n", encoding="utf-8")
    (tmp_path / ".vibegate.yml").write_text(
        "rules:\n  disabled:\n    - ENV001\n", encoding="utf-8"
    )

    result = scan(tmp_path)

    assert not any(item.rule_id == "ENV001" for item in result.findings)


def test_excluded_directory_is_not_scanned(tmp_path: Path):
    ignored = tmp_path / "node_modules"
    ignored.mkdir()
    secret = "ghp_" + ("A" * 35)
    (ignored / "bad.js").write_text(f'const x = "{secret}";\n', encoding="utf-8")

    result = scan(tmp_path)

    assert not any(item.rule_id == "SECRET002" for item in result.findings)
