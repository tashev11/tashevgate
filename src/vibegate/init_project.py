from __future__ import annotations

from pathlib import Path

from .fixer import ensure_gitignore

DEFAULT_CONFIG = """version: 1

gate:
  fail_on: blocker

scan:
  max_file_bytes: 1000000
  exclude:
    - ".git/**"
    - "node_modules/**"
    - "vendor/**"
    - ".venv/**"
    - "dist/**"
    - "build/**"
    - "coverage/**"
    - "*.min.js"
    - "*.map"

rules:
  disabled: []
  severity_overrides: {}
  allow_destructive_migrations: false

reports:
  directory: ".vibegate"
"""

WORKFLOW = """name: VibeGate

on:
  pull_request:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  security-events: write

jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: tashev11/vibegate@v0.1.0
        with:
          path: "."
          fail-on: "blocker"
      - name: Upload SARIF
        if: always()
        continue-on-error: true
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: .vibegate/vibegate.sarif
"""


def initialize(root: Path) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    created: list[str] = []

    config = root / ".vibegate.yml"
    if not config.exists():
        config.write_text(DEFAULT_CONFIG, encoding="utf-8")
        created.append(".vibegate.yml")

    workflow = root / ".github" / "workflows" / "vibegate.yml"
    if not workflow.exists():
        workflow.parent.mkdir(parents=True, exist_ok=True)
        workflow.write_text(WORKFLOW, encoding="utf-8")
        created.append(".github/workflows/vibegate.yml")

    gitignore_added = ensure_gitignore(root)
    return {"created": created, "gitignore_added": gitignore_added}
