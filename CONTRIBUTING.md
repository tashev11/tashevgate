# Contributing

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
make check
```

A rule change should include tests covering both a positive finding and an important non-finding where practical.

## Rule design principles

- Prefer high-confidence evidence over noisy guesses.
- BLOCKER rules require especially strong evidence.
- Never include a detected secret value in ordinary report evidence.
- Keep rule IDs stable.
- Separate detection from release policy.
- Auto-fixes must be deterministic and safe without hidden application rewrites.

## Pull requests

Keep changes focused and update RULES.md for new user-visible checks.
