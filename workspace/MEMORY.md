# MEMORY.md — Tacit Knowledge + Project Registry

This file is auto-injected every session. It stores two things:
1. **Tacit knowledge** — patterns about how we operate
2. **Project registry** — every active project, so nothing is ever lost across sessions, channels, or gateway restarts

---

## 👥 Agent Roster
| Agent | Role | Workspace | Cron |
|-------|------|-----------|------|
| Felix | CEO/Orchestrator | `workspace` | heartbeat |
| Iris | Developer | `workspace-dev` | — |
| Kat | Copywriter | `workspace-kat` | On-demand |
| Alex | Chief Growth Officer | `workspace-alex` | TBD |
| Nova | Customer Success | `workspace-nova` | Every 15 min |
| Pierce | QC & Security | `workspace-pierce` | Weekly |

> ⚠️ **When registering a new project agent, also add them to this roster.** Other agents auto-discover new projects from here.

---

## 🗂 Project Registry

> _No projects yet. Add your first project below when it's created._
>
> **Template:**
> ### [Project Name]
> - **Status:** 🚧 In progress / ✅ Live
> - **URL:** https://...
> - **Agent:** [who owns it]
> - **Built:** YYYY-MM-DD
> - **Stack:** [tech stack]
> - **Deploy:** [how it deploys]
> - **Cron:** [cron job ID + schedule, if any]
> - **Details:** [agent's MEMORY.md path]

---

## Project Registry Rules
- Add every new project here before closing the session
- Include: status, URL, purpose, key file paths, cron job ID + schedule, deploy method, any gotchas
- Never let a project exist only in daily notes or conversation history

## ⚠️ Project Setup Check — MANDATORY Before Every Change or Comment
Before making changes to any project OR saying anything about how it's deployed/hosted/structured:
1. **Read the project's entry in this registry first** — deploy method, URLs, key paths
2. **If the registry entry is incomplete or unclear**, check the actual project: `cat vercel.json`, `ls .herenow/`, `cat package.json`, etc.
3. **Never infer deploy target from config file presence alone**
4. **After confirming**, update the registry if anything was missing or wrong

---

## Vercel Access
- **Personal access token** stored at: `VERCEL_TOKEN` in `~/.openclaw/workspace/.env`
- **Always check `workspace/.env` for VERCEL_TOKEN before asking or re-authenticating**
- For new projects: use `npx vercel --prod --token $VERCEL_TOKEN --yes`
- Composio Vercel connection is `limited: true` — **cannot create projects**, only manage existing ones. Use token directly for create/deploy operations.

## Agent Status + Task Queue

### Agent Status
- **File:** `~/.openclaw/workspace/agent-status.json`
- **Script:** `python3 ~/.openclaw/workspace/scripts/agent-status.py`
- **Felix MUST update this** whenever dispatching or completing agent tasks
- `set <agent> busy "task"` when sending work · `set <agent> idle` when they complete

### Dispatch Protocol (MANDATORY)
Before sending ANY task to an agent:
1. `python3 scripts/agent-status.py is-busy <agent>`
2. If **idle** → send via `sessions_send`, mark busy
3. If **busy** → add to task queue with `--after` dependency, tell user it's queued

### Task Queue
- **File:** `~/.openclaw/workspace/task-queue.json`
- **Script:** `python3 ~/.openclaw/workspace/scripts/task-queue.py`
- **Usage:** `add --agent <id> --task "description" [--after "dependency-label"]`
- Checked every heartbeat — ready tasks are fired automatically
- Use `--after` to queue tasks that depend on another completing

## Email
- Always use AgentMail for outbound email.
- Felix's sending inbox: `[YOUR_FELIX_INBOX]@agentmail.to`
- API key: `~/.config/agentmail/api_key`
- Every outbound email MUST include: `\n\n---\n⚡ Felix is an AI agent. This email was sent autonomously.`

## Integration Checks
- **Never** infer connectivity from local CLI installs or `~/.config/` directories alone.
- **Always** use `composio_manage_connections` to verify Vercel/Stripe/etc.
- Checking `which vercel` or `ls ~/.config/stripe/` will always return nothing — that is expected.

## Silent Replies
When you have nothing to say, respond with ONLY: NO_REPLY
