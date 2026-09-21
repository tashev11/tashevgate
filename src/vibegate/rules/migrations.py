from __future__ import annotations

import re
from pathlib import Path

from ..config import Config
from ..context import FileRecord
from ..models import Finding, Severity


DESTRUCTIVE_SQL = re.compile(
    r"\b(?:DROP\s+(?:TABLE|DATABASE|SCHEMA|COLUMN)|TRUNCATE\s+TABLE|DELETE\s+FROM\s+[^;\n]+(?:;|$))",
    flags=re.IGNORECASE,
)


def scan_migrations(root: Path, files: list[FileRecord], config: Config) -> list[Finding]:
    del root
    findings: list[Finding] = []
    if config.allow_destructive_migrations:
        return findings

    for record in files:
        lower = record.relative.lower()
        if record.path.suffix.lower() != ".sql" and "migration" not in lower:
            continue
        for match in DESTRUCTIVE_SQL.finditer(record.text):
            line = record.text.count("\n", 0, match.start()) + 1
            snippet = " ".join(match.group(0).split())[:120]
            findings.append(
                Finding(
                    rule_id="MIG001",
                    title="Destructive database migration",
                    severity=Severity.BLOCKER,
                    message="A migration contains a destructive SQL operation.",
                    path=record.relative,
                    line=line,
                    evidence=snippet,
                    remediation=(
                        "Use an expand/migrate/contract strategy or explicitly approve destructive migrations "
                        "after backup and rollback validation."
                    ),
                )
            )
    return findings
