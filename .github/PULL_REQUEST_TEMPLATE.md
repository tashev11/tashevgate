## Change

What problem does this solve?

## Rule quality

- [ ] New/changed detection has tests
- [ ] BLOCKER evidence is high-confidence
- [ ] Reports do not expose secret values
- [ ] Safe fixes are deterministic and non-destructive
- [ ] RULES.md/docs updated when needed

## Verification

- [ ] `ruff check src tests`
- [ ] `pytest -q`
- [ ] `vibegate check . --fail-on blocker`
