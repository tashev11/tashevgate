# Agent instructions

Before modifying TashevGate:

1. Read `.tashevos/STATE.md`.
2. Read `.tashevos/PROJECT.md`.
3. Read `.tashevos/GUARDRAILS.md`.
4. Read RULES.md for detection semantics.
5. Run `make check` before finishing.
6. Update `.tashevos/STATE.md` after meaningful work.

Never add real secret fixtures. Generate synthetic values in tests at runtime.
Do not weaken a BLOCKER rule merely to make self-scan green; fix the false-positive mechanism or the project.
