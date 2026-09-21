from pathlib import Path

from tashevgate.fixer import safe_fix
from tashevgate.init_project import initialize


def test_safe_fix_never_copies_secret_values(tmp_path: Path):
    (tmp_path / ".env").write_text(
        "API_KEY=super-secret-value\nDATABASE_URL=postgres://secret\n", encoding="utf-8"
    )

    result = safe_fix(tmp_path)
    example = (tmp_path / ".env.example").read_text(encoding="utf-8")

    assert result["env_example_keys"] == ["API_KEY", "DATABASE_URL"]
    assert "super-secret-value" not in example
    assert "postgres://secret" not in example
    assert "API_KEY=" in example


def test_init_creates_config_workflow_and_gitignore(tmp_path: Path):
    result = initialize(tmp_path)

    assert ".tashevgate.yml" in result["created"]
    assert ".github/workflows/tashevgate.yml" in result["created"]
    assert (tmp_path / ".gitignore").exists()
    assert ".env" in (tmp_path / ".gitignore").read_text(encoding="utf-8")
