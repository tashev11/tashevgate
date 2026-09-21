# Built-in rules

| Rule | Default | Meaning |
|---|---|---|
| SECRET001 | BLOCKER | OpenAI-compatible secret key detected |
| SECRET002 | BLOCKER | GitHub token detected |
| SECRET003 | BLOCKER | AWS access key detected |
| SECRET004 | BLOCKER | Stripe live secret detected |
| SECRET005 | BLOCKER | Telegram bot token detected |
| SECRET006 | BLOCKER | Private key detected |
| ENV001 | BLOCKER | Real .env-style file detected |
| ENV002 | BLOCKER | Secret-looking public frontend env variable |
| MIG001 | BLOCKER | Destructive SQL migration |
| GIT001 | HIGH | Missing .gitignore |
| GIT002 | HIGH | .env not protected by .gitignore |
| DEP001 | HIGH | Manifest without corresponding lock file |
| RECOVERY001 | HIGH | Migrations without documented backup + rollback |
| RUNTIME001 | HIGH | Debug mode appears enabled |
| SEC001 | HIGH | Wildcard CORS |
| TEST001 | MEDIUM | No automated tests detected |
| CI001 | MEDIUM | No GitHub Actions workflow detected |
| AUTH001 | MEDIUM | Admin-looking route without obvious authorization marker |

## Important limitations

Rules are evidence, not a proof that a project is secure.

`AUTH001` is intentionally MEDIUM because authorization can live in middleware or framework configuration outside the route file. Conversely, the absence of an AUTH001 finding does not prove access control is correct.

`MIG001` is strict by default because destructive production data changes deserve explicit review. Teams that have an established migration safety process may use:

```yaml
rules:
  allow_destructive_migrations: true
```

Prefer narrow rule exceptions over disabling the whole gate.
