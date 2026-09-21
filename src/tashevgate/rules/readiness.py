from __future__ import annotations

from pathlib import Path

from ..context import FileRecord
from ..models import Finding, Severity

LOCKFILE_MAP = {
    "package.json": {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb"},
    "pyproject.toml": {"uv.lock", "poetry.lock", "Pipfile.lock"},
    "requirements.txt": set(),
    "go.mod": {"go.sum"},
    "Cargo.toml": {"Cargo.lock"},
    "composer.json": {"composer.lock"},
    "Gemfile": {"Gemfile.lock"},
}


def scan_readiness(root: Path, files: list[FileRecord], detected: dict) -> list[Finding]:
    del root
    findings: list[Finding] = []
    names = {record.relative for record in files}

    gitignore = next((record for record in files if record.relative == ".gitignore"), None)
    if gitignore is None:
        findings.append(
            Finding(
                rule_id="GIT001",
                title="No .gitignore",
                severity=Severity.HIGH,
                message="The project has no .gitignore, increasing the risk of committing secrets and build output.",
                remediation="Create .gitignore with .env, private keys, dependencies and build artifacts.",
                auto_fixable=True,
            )
        )
    elif ".env" not in gitignore.text:
        findings.append(
            Finding(
                rule_id="GIT002",
                title=".env is not ignored",
                severity=Severity.HIGH,
                message=".gitignore does not appear to protect .env files.",
                path=".gitignore",
                remediation="Add .env and .env.* while explicitly allowing .env.example.",
                auto_fixable=True,
            )
        )

    if not bool(detected.get("has_tests")):
        findings.append(
            Finding(
                rule_id="TEST001",
                title="No automated tests detected",
                severity=Severity.MEDIUM,
                message="No common test directory or test filename pattern was detected.",
                remediation="Add at least critical-path tests for auth, writes, payments and core business flows.",
            )
        )

    if not bool(detected.get("has_ci")):
        findings.append(
            Finding(
                rule_id="CI001",
                title="No CI workflow detected",
                severity=Severity.MEDIUM,
                message="No GitHub Actions workflow was found.",
                remediation="Run TashevGate, tests and build checks on every pull request.",
                auto_fixable=True,
            )
        )

    for manifest, acceptable in LOCKFILE_MAP.items():
        if manifest not in names or not acceptable:
            continue
        if not names.intersection(acceptable):
            findings.append(
                Finding(
                    rule_id="DEP001",
                    title="Dependency lock file missing",
                    severity=Severity.HIGH,
                    message=f"{manifest} exists but no corresponding lock file was detected.",
                    path=manifest,
                    remediation="Generate and commit the package manager lock file for reproducible builds.",
                )
            )

    if bool(detected.get("has_migrations")):
        docs = "\n".join(
            record.text.lower()
            for record in files
            if record.path.suffix.lower() == ".md" or record.path.name.lower().startswith("readme")
        )
        if not ("rollback" in docs and "backup" in docs):
            findings.append(
                Finding(
                    rule_id="RECOVERY001",
                    title="Database changes lack documented backup + rollback",
                    severity=Severity.HIGH,
                    message="Migrations were detected but documentation does not mention both backup and rollback.",
                    remediation="Document and test pre-deploy backup plus rollback/recovery procedures.",
                )
            )
    return findings
