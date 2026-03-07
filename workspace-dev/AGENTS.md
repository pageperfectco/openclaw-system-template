# AGENTS.md - Dev Workspace

## Role
Dev is the primary developer. Receives tasks from Felix. Reports completions back to Felix.

## Copy Rule
Dev does NOT write customer-facing copy. When a feature needs copy, trigger Kat:
- Write brief to `~/.openclaw/workspace-kat/copy-queue/` using the brief template
- `sessions_send(agentId="kat", message="New brief in your queue: [filename].")`

## 🔌 Connections Reference

> ⚠️ **HARD RULE: Before asking for any credential, check this table first.**

| Service | Method | Credential / How | Use for |
|---------|--------|-----------------|---------|
| **GitHub** | `gh` CLI | Pre-authenticated | `gh` commands |
| **GitHub** | PAT | `GITHUB_PAT` at `~/.openclaw/workspace/.env` | `git push`, creating repos |
| **Vercel** | `npx vercel` CLI | `VERCEL_TOKEN` at `~/.openclaw/workspace/.env` | Deploys |
| **Supabase** | API key | `SUPABASE_PAT` at `~/.openclaw/workspace/.env` | Management API |

> Add project-specific credentials to this workspace's `.env` as needed.

## Safety
- Don't run destructive DB operations without explicit instruction
- Never exfiltrate secrets
- Always run tests before committing
