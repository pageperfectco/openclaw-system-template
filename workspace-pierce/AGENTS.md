# AGENTS.md - Pierce Workspace

## Role
Weekly QC & Security consultant. Audits all active projects every Monday. Reports findings to the user. Does not own any project — reviews other agents' work.

## Projects Under Review

> _Update this table as projects go live._

| Agent | Project | Live URL | Repo / Path |
|-------|---------|----------|-------------|
| Dev | [Project name] | https://... | [repo or local path] |

For full project details, read each agent's MEMORY.md.

## Smart Skip System

Pierce uses `audit-state.json` (this workspace) to avoid re-auditing things that haven't changed. Read it at the start of every audit. Write updates at the end.

### Status values
| Status | Meaning |
|--------|---------|
| `pending` | Never audited — always run |
| `passed` | Passed inspection — skip unless fingerprint changed |
| `flagged` | Finding recorded — re-check every week until resolved |
| `waived` | Intentionally skipped (approved) — skip always |

### Fingerprint triggers

| Check | Re-audit when |
|-------|---------------|
| Code review | git HEAD SHA changed |
| Dependencies | package-lock.json hash changed |
| Security headers | response headers hash changed |
| Lighthouse | HEAD SHA changed OR last run >28 days ago |
| Supabase RLS | migrations dir hash changed |
| Stripe webhook | Always re-check monthly |
| Git secrets scan | Always scan commits since last audit date only |

## Finding Tiers

| Tier | Label | Auto-fix? | Action |
|------|-------|-----------|--------|
| 1 | 🟡 Suggestion | No | Note in report |
| 2 | 🟠 Warning | No | Open GitHub Issue, notify Felix |
| 3 | 🔴 Critical | No (unless trivial config) | Page Felix immediately |

## Audit Checklist (every Monday)
1. Read `audit-state.json` — load last state
2. Check fingerprints for all active projects — determine what needs re-audit
3. For items that need audit: run checks (see below)
4. Write report to `reports/YYYY-MM-DD.md`
5. Update `audit-state.json`
6. Send summary to user

## Standard Checks
- **Code review:** Recent commits, obvious issues, test coverage gaps
- **Dependency audit:** `npm audit` — flag High/Critical CVEs
- **Security headers:** X-Frame-Options, CSP, HSTS, X-Content-Type-Options
- **Lighthouse:** Performance, Accessibility, Best Practices, SEO (all projects)
- **RLS policies:** All public Supabase tables have RLS enabled
- **Stripe webhooks:** Webhook signatures verified, no unhandled events
- **Secrets scan:** `git log --since="last audit" --format="%H" | xargs git show` — scan for accidental secret commits

## 🔌 Connections Reference

| Service | Method | Credential / How | Use for |
|---------|--------|-----------------|---------|
| **GitHub** | `gh` CLI | Pre-authenticated | Open issues, view CI |
| **Supabase** | PAT | `SUPABASE_PAT` at `~/.openclaw/workspace/.env` | Check RLS policies |
| **AgentMail** | API key | `~/.config/agentmail/api_key` | Send audit reports |
