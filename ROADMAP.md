# Roadmap

## v0.1 — deterministic local release gate

- [x] secret and private-key detection
- [x] public frontend secret detection
- [x] real .env detection
- [x] destructive migration blocker
- [x] tests / CI / lock-file readiness checks
- [x] backup + rollback documentation check
- [x] debug / CORS / admin-route heuristics
- [x] configurable gate policy
- [x] console, Markdown, JSON and SARIF
- [x] safe fixer
- [x] GitHub Action
- [x] self-scan tests

## v0.2 — framework-aware evidence

- [ ] Next.js route/auth adapter
- [ ] FastAPI/Django/Flask auth adapters
- [ ] Supabase RLS checks
- [ ] Firebase rules checks
- [ ] Prisma / Alembic / Django migration awareness
- [ ] Dockerfile and Compose production rules
- [ ] Terraform/IaC dangerous-default rules
- [ ] dependency vulnerability and license adapter
- [ ] baseline/diff mode for pull requests

## v0.3 — staging sandbox

- [ ] detect build/start commands
- [ ] ephemeral application runtime
- [ ] disposable database
- [ ] browser registration/login/password-reset smoke flows
- [ ] API permission probes
- [ ] migration upgrade/downgrade test
- [ ] backup/restore proof
- [ ] performance smoke baseline
- [ ] screenshots and evidence bundle

## v0.4 — release guardian

- [ ] production preflight
- [ ] tagged restore point
- [ ] backup verification
- [ ] deployment adapter
- [ ] post-deploy health/E2E checks
- [ ] automatic rollback on failed proof
- [ ] audit trail

## Later — Vibe Certificate

A verifiable release-evidence artifact for GitHub projects, based on explicit checks rather than a marketing score.
