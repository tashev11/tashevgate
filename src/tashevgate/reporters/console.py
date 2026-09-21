from __future__ import annotations

from ..models import ScanResult

ICONS = {
    "blocker": "⛔",
    "high": "🔴",
    "medium": "🟡",
    "info": "ℹ️",
}


def render_console(result: ScanResult) -> str:
    lines = [
        "",
        f"TashevGate · {result.status.value}",
        f"Scanned {result.files_scanned} files · gate threshold: {result.fail_on.name.lower()}",
        "",
    ]
    if not result.findings:
        lines.append("✅ No findings.")
        return "\n".join(lines)

    for finding in result.findings:
        severity = finding.severity.name.lower()
        location = ""
        if finding.path:
            location = f" · {finding.path}"
            if finding.line:
                location += f":{finding.line}"
        lines.append(f"{ICONS[severity]} {severity.upper()} {finding.rule_id}{location}")
        lines.append(f"   {finding.title}: {finding.message}")
        if finding.remediation:
            lines.append(f"   Fix: {finding.remediation}")
        lines.append("")

    counts = result.to_dict()["summary"]
    lines.append(
        "Summary: "
        + " · ".join(f"{key}={value}" for key, value in counts.items() if value)
    )
    return "\n".join(lines)
