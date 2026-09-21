from __future__ import annotations

import re
from pathlib import Path

from ..context import FileRecord
from ..models import Finding, Severity


DEBUG_PATTERNS = [
    re.compile(r"\bDEBUG\s*=\s*(?:True|true|1)\b"),
    re.compile(r"\bdebug\s*:\s*true\b", re.IGNORECASE),
    re.compile(r"app\.run\([^\n]*debug\s*=\s*True"),
]

WILDCARD_CORS = [
    re.compile(r"allow_origins\s*=\s*\[\s*["']\*["']\s*\]"),
    re.compile(r"origin\s*:\s*["']\*["']", re.IGNORECASE),
]


def _line(text: str, start: int) -> int:
    return text.count("\n", 0, start) + 1


def scan_runtime(root: Path, files: list[FileRecord]) -> list[Finding]:
    del root
    findings: list[Finding] = []
    for record in files:
        if record.path.suffix.lower() not in {
            ".py", ".js", ".ts", ".tsx", ".jsx", ".yml", ".yaml", ".json", ".toml"
        }:
            continue
        if "/tests/" in f"/{record.relative.lower()}" or record.relative.lower().startswith("tests/"):
            continue

        for pattern in DEBUG_PATTERNS:
            for match in pattern.finditer(record.text):
                findings.append(
                    Finding(
                        rule_id="RUNTIME001",
                        title="Debug mode appears enabled",
                        severity=Severity.HIGH,
                        message="A production-relevant file appears to enable debug mode.",
                        path=record.relative,
                        line=_line(record.text, match.start()),
                        evidence=match.group(0)[:100],
                        remediation="Make debug mode environment-specific and disabled in production.",
                    )
                )

        for pattern in WILDCARD_CORS:
            for match in pattern.finditer(record.text):
                findings.append(
                    Finding(
                        rule_id="SEC001",
                        title="Wildcard CORS configuration",
                        severity=Severity.HIGH,
                        message="The application appears to accept requests from every origin.",
                        path=record.relative,
                        line=_line(record.text, match.start()),
                        evidence=match.group(0)[:100],
                        remediation="Restrict CORS to explicit trusted origins for production.",
                    )
                )

        text_lower = record.text.lower()
        if "/admin" in text_lower or "api/admin" in text_lower:
            auth_markers = (
                "require_auth", "require_role", "is_admin", "authorize", "permission",
                "current_user", "jwt", "session", "auth", "middleware",
            )
            if not any(marker in text_lower for marker in auth_markers):
                findings.append(
                    Finding(
                        rule_id="AUTH001",
                        title="Admin route without obvious authorization marker",
                        severity=Severity.MEDIUM,
                        message="An admin-looking route was found without a nearby common auth marker.",
                        path=record.relative,
                        remediation="Verify server-side authentication and role authorization for every admin route.",
                    )
                )
    return findings
