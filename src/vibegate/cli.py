from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

from . import __version__
from .fixer import safe_fix
from .init_project import initialize
from .reporters.console import render_console
from .reporters.markdown import render_markdown
from .reporters.sarif import render_sarif
from .rules_catalog import RULES
from .scanner import scan


def _write_or_print(content: str, output: str | None) -> None:
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path}")
    else:
        print(content)


def _check(args: argparse.Namespace) -> int:
    try:
        result = scan(args.path, args.config, args.fail_on)
    except ValueError as exc:
        print(f"VibeGate error: {exc}", file=sys.stderr)
        return 3

    if args.format == "console":
        _write_or_print(render_console(result), args.output)
    elif args.format == "markdown":
        _write_or_print(render_markdown(result), args.output)
    elif args.format == "json":
        _write_or_print(json.dumps(result.to_dict(), indent=2), args.output)
    else:
        _write_or_print(json.dumps(render_sarif(result), indent=2), args.output)

    return 2 if result.status.value == "BLOCKED" else 0


def _init(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    result = initialize(root)
    print(json.dumps(result, indent=2))
    return 0


def _fix(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    result = safe_fix(root)
    print(json.dumps(result, indent=2))
    return 0


def _doctor(_: argparse.Namespace) -> int:
    print(f"VibeGate {__version__}")
    print(f"Python {platform.python_version()}")
    print(f"Platform {platform.platform()}")
    print("CLI ready.")
    return 0


def _explain(args: argparse.Namespace) -> int:
    rule_id = args.rule_id.upper()
    item = RULES.get(rule_id)
    if not item:
        print(f"Unknown rule: {rule_id}", file=sys.stderr)
        return 1
    severity, description = item
    print(f"{rule_id} · {severity}\n{description}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="vibegate", description="Production gate for AI-built software")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="Scan a project and enforce the release gate")
    check.add_argument("path", nargs="?", default=".")
    check.add_argument("--config")
    check.add_argument("--fail-on", choices=["blocker", "high", "medium", "info"])
    check.add_argument("--format", choices=["console", "markdown", "json", "sarif"], default="console")
    check.add_argument("--output")
    check.set_defaults(func=_check)

    init = sub.add_parser("init", help="Add VibeGate config and GitHub workflow")
    init.add_argument("path", nargs="?", default=".")
    init.set_defaults(func=_init)

    fix = sub.add_parser("fix", help="Apply only safe, deterministic fixes")
    fix.add_argument("path", nargs="?", default=".")
    fix.set_defaults(func=_fix)

    explain = sub.add_parser("explain", help="Explain a rule")
    explain.add_argument("rule_id")
    explain.set_defaults(func=_explain)

    doctor = sub.add_parser("doctor", help="Show local VibeGate environment")
    doctor.set_defaults(func=_doctor)

    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
