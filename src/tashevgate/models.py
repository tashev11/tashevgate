from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import IntEnum, StrEnum
from typing import Any


class Severity(IntEnum):
    INFO = 10
    MEDIUM = 20
    HIGH = 30
    BLOCKER = 40

    @classmethod
    def parse(cls, value: str) -> Severity:
        return cls[value.strip().upper()]


class GateStatus(StrEnum):
    READY = "READY"
    BLOCKED = "BLOCKED"


@dataclass(slots=True)
class Finding:
    rule_id: str
    title: str
    severity: Severity
    message: str
    path: str | None = None
    line: int | None = None
    remediation: str = ""
    evidence: str = ""
    auto_fixable: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.name.lower()
        return data


@dataclass(slots=True)
class ScanResult:
    root: str
    findings: list[Finding]
    detected: dict[str, Any]
    files_scanned: int
    status: GateStatus
    fail_on: Severity

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "status": self.status.value,
            "fail_on": self.fail_on.name.lower(),
            "files_scanned": self.files_scanned,
            "detected": self.detected,
            "findings": [finding.to_dict() for finding in self.findings],
            "summary": {
                name.lower(): sum(1 for f in self.findings if f.severity == severity)
                for name, severity in Severity.__members__.items()
            },
        }
