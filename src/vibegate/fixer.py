from __future__ import annotations

import re
from pathlib import Path


GITIGNORE_LINES = [
    ".env",
    ".env.*",
    "!.env.example",
    "*.pem",
    "*.key",
    ".vibegate/",
]


def ensure_gitignore(root: Path) -> list[str]:
    path = root / ".gitignore"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    existing = {line.strip() for line in current.splitlines()}
    added = [line for line in GITIGNORE_LINES if line not in existing]
    if added:
        separator = "" if not current or current.endswith("\n") else "\n"
        path.write_text(current + separator + "\n".join(added) + "\n", encoding="utf-8")
    return added


ENV_KEY = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=")


def create_env_example(root: Path) -> list[str]:
    source = root / ".env"
    target = root / ".env.example"
    if not source.exists() or target.exists():
        return []

    keys: list[str] = []
    for line in source.read_text(encoding="utf-8").splitlines():
        match = ENV_KEY.match(line)
        if match and match.group(1) not in keys:
            keys.append(match.group(1))
    if keys:
        target.write_text("\n".join(f"{key}=" for key in keys) + "\n", encoding="utf-8")
    return keys


def safe_fix(root: Path) -> dict:
    return {
        "gitignore_added": ensure_gitignore(root),
        "env_example_keys": create_env_example(root),
    }
