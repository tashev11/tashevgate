from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .models import Severity

DEFAULT_EXCLUDES = [
    ".git/**",
    "node_modules/**",
    "vendor/**",
    ".venv/**",
    "venv/**",
    "dist/**",
    "build/**",
    "coverage/**",
    "*.min.js",
    "*.map",
]


@dataclass(slots=True)
class Config:
    fail_on: Severity = Severity.BLOCKER
    max_file_bytes: int = 1_000_000
    exclude: list[str] = field(default_factory=lambda: list(DEFAULT_EXCLUDES))
    disabled_rules: set[str] = field(default_factory=set)
    severity_overrides: dict[str, Severity] = field(default_factory=dict)
    allow_destructive_migrations: bool = False
    reports_directory: str = ".tashevgate"


def load_config(root: Path, explicit: str | None = None) -> Config:
    target = Path(explicit) if explicit else root / ".tashevgate.yml"
    if not target.exists():
        return Config()

    raw = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    gate = raw.get("gate", {})
    scan = raw.get("scan", {})
    rules = raw.get("rules", {})
    reports = raw.get("reports", {})

    overrides = {
        str(rule_id): Severity.parse(str(severity))
        for rule_id, severity in (rules.get("severity_overrides", {}) or {}).items()
    }

    return Config(
        fail_on=Severity.parse(str(gate.get("fail_on", "blocker"))),
        max_file_bytes=int(scan.get("max_file_bytes", 1_000_000)),
        exclude=list(scan.get("exclude", DEFAULT_EXCLUDES)),
        disabled_rules={str(item) for item in rules.get("disabled", [])},
        severity_overrides=overrides,
        allow_destructive_migrations=bool(rules.get("allow_destructive_migrations", False)),
        reports_directory=str(reports.get("directory", ".tashevgate")),
    )
