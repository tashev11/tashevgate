from __future__ import annotations

from ..models import ScanResult


def render_markdown(result: ScanResult) -> str:
    status = "🟢 READY" if result.status.value == "READY" else "🔴 BLOCKED"
    lines = [
        "# TashevGate report",
        "",
        f"**Release status:** {status}",
        "",
        f"- Files scanned: **{result.files_scanned}**",
        f"- Blocking threshold: **{result.fail_on.name.lower()}**",
        f"- Root: `{result.root}`",
        "",
        "## Findings",
        "",
    ]
    if not result.findings:
        lines.append("No findings.")
        return "\n".join(lines) + "\n"

    lines.extend([
        "| Severity | Rule | Location | Finding |",
        "|---|---|---|---|",
    ])
    for finding in result.findings:
        location = finding.path or "project"
        if finding.line:
            location += f":{finding.line}"
        title = finding.title.replace("|", "\\|")
        lines.append(
            f"| {finding.severity.name} | `{finding.rule_id}` | `{location}` | {title} |"
        )

    lines.extend(["", "## Remediation", ""])
    for finding in result.findings:
        lines.append(f"### {finding.rule_id} · {finding.title}")
        lines.append("")
        lines.append(finding.message)
        if finding.remediation:
            lines.extend(["", f"**Fix:** {finding.remediation}"])
        lines.append("")
    return "\n".join(lines)
