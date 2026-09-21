from pathlib import Path

from vibegate.scanner import scan


def prepare(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(".env\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_ok.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "ci.yml").write_text("name: CI\n", encoding="utf-8")


def test_destructive_migration_blocks(tmp_path: Path):
    prepare(tmp_path)
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    (migrations / "002_drop.sql").write_text(
        "ALTER TABLE users DROP COLUMN legacy_name;\n", encoding="utf-8"
    )

    result = scan(tmp_path)

    assert any(item.rule_id == "MIG001" for item in result.findings)
    assert result.status.value == "BLOCKED"


def test_destructive_migration_can_be_explicitly_allowed(tmp_path: Path):
    prepare(tmp_path)
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    (migrations / "002_drop.sql").write_text("DROP TABLE old_users;\n", encoding="utf-8")
    (tmp_path / ".vibegate.yml").write_text(
        "rules:\n  allow_destructive_migrations: true\n", encoding="utf-8"
    )

    result = scan(tmp_path)

    assert not any(item.rule_id == "MIG001" for item in result.findings)
