from __future__ import annotations

from pathlib import Path

from .context import FileRecord


def detect_project(root: Path, files: list[FileRecord]) -> dict:
    names = {record.relative for record in files}
    detected: dict[str, object] = {"languages": [], "frameworks": [], "manifests": []}

    language_map = {
        "python": {".py"},
        "javascript": {".js", ".jsx", ".mjs", ".cjs"},
        "typescript": {".ts", ".tsx"},
        "go": {".go"},
        "rust": {".rs"},
        "php": {".php"},
        "ruby": {".rb"},
        "java": {".java"},
    }
    suffixes = {record.path.suffix.lower() for record in files}
    detected["languages"] = [
        language for language, extensions in language_map.items() if suffixes & extensions
    ]

    manifest_candidates = [
        "pyproject.toml", "requirements.txt", "package.json", "go.mod", "Cargo.toml",
        "composer.json", "Gemfile", "pom.xml", "build.gradle", "build.gradle.kts",
    ]
    detected["manifests"] = [name for name in manifest_candidates if name in names]

    joined = "\n".join(record.text[:20_000] for record in files if record.relative in {
        "package.json", "pyproject.toml", "requirements.txt", "composer.json"
    })
    framework_markers = {
        "nextjs": ["next"],
        "react": ["react"],
        "vue": ["vue"],
        "svelte": ["svelte"],
        "fastapi": ["fastapi"],
        "django": ["django"],
        "flask": ["flask"],
        "laravel": ["laravel/framework"],
        "express": ["express"],
    }
    lower = joined.lower()
    detected["frameworks"] = [
        framework for framework, markers in framework_markers.items()
        if any(marker in lower for marker in markers)
    ]

    detected["has_tests"] = any(
        "/test" in f"/{record.relative.lower()}"
        or record.path.name.lower().startswith("test_")
        or record.path.name.lower().endswith((".test.js", ".test.ts", ".spec.js", ".spec.ts"))
        for record in files
    )
    detected["has_ci"] = any(record.relative.startswith(".github/workflows/") for record in files)
    detected["has_docker"] = "Dockerfile" in names or "docker-compose.yml" in names
    detected["has_migrations"] = any(
        "migration" in record.relative.lower() or "/migrations/" in f"/{record.relative.lower()}"
        for record in files
    )
    detected["root"] = str(root)
    return detected
