from __future__ import annotations

import re
from pathlib import Path

from ..context import FileRecord
from ..models import Finding, Severity


SECRET_PATTERNS = [
    ("SECRET001", "OpenAI-compatible secret key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("SECRET002", "GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("SECRET003", "AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("SECRET004", "Stripe live secret", re.compile(r"\bsk_live_[A-Za-z0-9]{16,}\b")),
    ("SECRET005", "Telegram bot token", re.compile(r"\b\d{6,12}:[A-Za-z0-9_-]{30,}\b")),
    (
        "SECRET006",
        "Private key committed",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
]

PUBLIC_SECRET = re.compile(
    r"\b(?:NEXT_PUBLIC_|VITE_|REACT_APP_)[A-Z0-9_]*(?:SECRET|TOKEN|PASSWORD|PRIVATE|API_KEY)[A-Z0-9_]*\b"
)


def _line_number(text: str, start: int) -> int:
    return text.count("\n", 0, start) + 1


def _safe_path(path: str) -> bool:
    lower = path.lower()
    return (
        lower.endswith((".example", ".sample", ".template"))
        or ".example." in lower
        or "/fixtures/" in f"/{lower}"
    )


def scan_secrets(root: Path, files: list[FileRecord]) -> list[Finding]:
    del root
    findings: list[Finding] = []
    for record in files:
        name = record.path.name.lower()
        if name.startswith(".env") and name not in {".env.example", ".env.sample", ".env.template"}:
            findings.append(
                Finding(
                    rule_id="ENV001",
                    title="Environment file is inside the project",
                    severity=Severity.BLOCKER,
                    message="A real .env-style file may contain production credentials.",
                    path=record.relative,
                    remediation="Remove it from version control, rotate exposed values, and keep only .env.example.",
                    auto_fixable=False,
                )
            )

        if _safe_path(record.relative):
            continue

        for rule_id, title, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(record.text):
                findings.append(
                    Finding(
                        rule_id=rule_id,
                        title=title,
                        severity=Severity.BLOCKER,
                        message="A value matching a high-confidence secret pattern was found.",
                        path=record.relative,
                        line=_line_number(record.text, match.start()),
                        evidence="[redacted secret]",
                        remediation="Rotate the secret, remove it from Git history, and inject it at runtime.",
                    )
                )

        for match in PUBLIC_SECRET.finditer(record.text):
            findings.append(
                Finding(
                    rule_id="ENV002",
                    title="Secret-looking value is exposed to frontend runtime",
                    severity=Severity.BLOCKER,
                    message=f"{match.group(0)} uses a public frontend environment-variable prefix.",
                    path=record.relative,
                    line=_line_number(record.text, match.start()),
                    evidence=match.group(0),
                    remediation="Move the secret to server-only configuration and call it through a backend API.",
                )
            )
    return findings
