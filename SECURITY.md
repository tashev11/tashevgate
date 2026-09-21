# Security policy

## Reporting

Do not put real credentials, private keys or sensitive repository contents into a public GitHub issue. Open a minimal issue requesting a private reporting path if necessary.

## Scanner behavior

TashevGate reads project files locally. v0.1 does not require uploading source code to an external service.

High-confidence secret findings redact the matched secret in normal output. Even so, treat generated reports as potentially sensitive because file paths and configuration findings can reveal project structure.

## Safe fixer

`tashevgate fix` is intentionally limited to deterministic operations. When generating `.env.example`, it copies environment-variable names only and never the original values.

## Git history

Removing a secret from the current file is not enough if it was committed. Rotate the credential and purge it from repository history using an appropriate history-rewrite process.

## Production

v0.1 does not deploy or mutate production infrastructure. Future production adapters must be opt-in, auditable and designed around least privilege and rollback.
