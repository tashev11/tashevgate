from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from pathlib import Path

from .config import Config

TEXT_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".env", ".md", ".txt", ".sql", ".sh", ".bash", ".zsh",
    ".ps1", ".rb", ".go", ".rs", ".java", ".kt", ".php", ".html", ".css", ".scss",
    ".vue", ".svelte", ".xml", ".properties", ".tf", ".tfvars", ".conf", ".lock",
}


@dataclass(slots=True)
class FileRecord:
    path: Path
    relative: str
    text: str


def is_excluded(relative: str, patterns: list[str]) -> bool:
    normalized = relative.replace("\\", "/")
    for raw_pattern in patterns:
        pattern = raw_pattern.replace("\\", "/")
        if pattern.endswith("/**"):
            prefix = pattern[:-3].rstrip("/")
            if normalized == prefix or normalized.startswith(prefix + "/"):
                return True
        if fnmatch.fnmatch(normalized, pattern):
            return True
    return False


def collect_files(root: Path, config: Config) -> list[FileRecord]:
    records: list[FileRecord] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if is_excluded(relative, config.exclude):
            continue
        if path.stat().st_size > config.max_file_bytes:
            continue
        special_name = path.name in {
            "Dockerfile", "Procfile", "Makefile", ".gitignore", ".dockerignore",
        } or path.name.startswith(".env")
        if path.suffix.lower() not in TEXT_EXTENSIONS and not special_name:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        records.append(FileRecord(path=path, relative=relative, text=text))
    return records
