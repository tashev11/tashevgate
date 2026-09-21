# Guardrails

- Local-first scanning must remain useful without a cloud account.
- BLOCKER findings require high-confidence evidence.
- Never expose matched secret values in reports.
- Safe fixes must be deterministic and non-destructive.
- Detection and release policy must remain separate.
- Do not claim that a clean scan proves a project is secure.
- Production mutation is out of scope for v0.1.
- Keep tests, Ruff and TashevGate self-scan green before release.
