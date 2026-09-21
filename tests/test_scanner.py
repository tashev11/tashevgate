from pathlib import Path

from tashevgate.models import GateStatus
from tashevgate.scanner import scan


def base_project(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(".env\n.env.*\n", encoding="utf-8")
    (tmp_path / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_app.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("name: CI\n", encoding="utf-8")


def test_high_confidence_secret_blocks_release(tmp_path: Path):
    base_project(tmp_path)
    secret = "sk-proj-" + ("A" * 30)
    (tmp_path / "app.py").write_text(f'KEY = "{secret}"\n', encoding="utf-8")

    result = scan(tmp_path)

    assert result.status == GateStatus.BLOCKED
    assert any(item.rule_id == "SECRET001" for item in result.findings)


def test_real_env_file_blocks_release(tmp_path: Path):
    base_project(tmp_path)
    (tmp_path / ".env").write_text("APP_MODE=production\n", encoding="utf-8")

    result = scan(tmp_path)

    assert result.status == GateStatus.BLOCKED
    assert any(item.rule_id == "ENV001" for item in result.findings)


def test_public_frontend_secret_name_blocks(tmp_path: Path):
    base_project(tmp_path)
    public_name = "VITE_STRIPE_" + "SECRET_KEY"
    (tmp_path / "frontend.ts").write_text(
        f"const k = import.meta.env.{public_name};\n", encoding="utf-8"
    )

    result = scan(tmp_path)

    assert result.status == GateStatus.BLOCKED
    assert any(item.rule_id == "ENV002" for item in result.findings)


def test_slow_readiness_warnings_do_not_block_default_gate(tmp_path: Path):
    (tmp_path / "app.py").write_text("print('hello')\n", encoding="utf-8")

    result = scan(tmp_path)

    assert result.status == GateStatus.READY
    assert any(item.severity.name in {"HIGH", "MEDIUM"} for item in result.findings)


def test_fail_on_high_blocks_high_findings(tmp_path: Path):
    (tmp_path / "app.py").write_text("print('hello')\n", encoding="utf-8")

    result = scan(tmp_path, fail_on="high")

    assert result.status == GateStatus.BLOCKED
