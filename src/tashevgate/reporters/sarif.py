from __future__ import annotations

from ..models import ScanResult

LEVELS = {
    "BLOCKER": "error",
    "HIGH": "error",
    "MEDIUM": "warning",
    "INFO": "note",
}


def render_sarif(result: ScanResult) -> dict:
    unique_rules: dict[str, dict] = {}
    sarif_results: list[dict] = []

    for finding in result.findings:
        unique_rules.setdefault(
            finding.rule_id,
            {
                "id": finding.rule_id,
                "name": finding.title,
                "shortDescription": {"text": finding.title},
                "help": {"text": finding.remediation or finding.message},
            },
        )
        item: dict = {
            "ruleId": finding.rule_id,
            "level": LEVELS[finding.severity.name],
            "message": {"text": finding.message},
        }
        if finding.path:
            region = {}
            if finding.line:
                region["startLine"] = finding.line
            item["locations"] = [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": finding.path},
                        **({"region": region} if region else {}),
                    }
                }
            ]
        sarif_results.append(item)

    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "TashevGate",
                        "informationUri": "https://github.com/tashev11/tashevgate",
                        "rules": list(unique_rules.values()),
                    }
                },
                "results": sarif_results,
            }
        ],
    }
