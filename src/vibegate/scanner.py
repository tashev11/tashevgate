from __future__ import annotations

from pathlib import Path

from .config import Config, load_config
from .context import collect_files
from .detect import detect_project
from .models import Finding, GateStatus, ScanResult, Severity
from .rules.migrations import scan_migrations
from .rules.readiness import scan_readiness
from .rules.runtime import scan_runtime
from .rules.secrets import scan_secrets


def _apply_policy(findings: list[Finding], config: Config) -> list[Finding]:
    result: list[Finding] = []
    for finding in findings:
        if finding.rule_id in config.disabled_rules:
            continue
        override = config.severity_overrides.get(finding.rule_id)
        if override is not None:
            finding.severity = override
        result.append(finding)
    return result


def scan(root: str | Path = ".", config_path: str | None = None, fail_on: str | None = None) -> ScanResult:
    path = Path(root).resolve()
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Project directory does not exist: {path}")

    config = load_config(path, config_path)
    threshold = Severity.parse(fail_on) if fail_on else config.fail_on
    files = collect_files(path, config)
    detected = detect_project(path, files)

    findings: list[Finding] = []
    findings.extend(scan_secrets(path, files))
    findings.extend(scan_readiness(path, files, detected))
    findings.extend(scan_migrations(path, files, config))
    findings.extend(scan_runtime(path, files))
    findings = _apply_policy(findings, config)
    findings.sort(key=lambda item: (-int(item.severity), item.rule_id, item.path or "", item.line or 0))

    blocked = any(finding.severity >= threshold for finding in findings)
    return ScanResult(
        root=str(path),
        findings=findings,
        detected=detected,
        files_scanned=len(files),
        status=GateStatus.BLOCKED if blocked else GateStatus.READY,
        fail_on=threshold,
    )
