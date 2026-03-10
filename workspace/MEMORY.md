# MEMORY.md — Tacit Knowledge + Project Registry

This file is auto-injected every session. It stores two things:
1. **Tacit knowledge** — patterns about how we operate
2. **Project registry** — every active project, so nothing is ever lost across sessions, channels, or gateway restarts

---

## 👥 Agent Roster
| Agent | Role | Workspace | Cron |
|-------|------|-----------|------|
| Felix | CEO/Orchestrator | `workspace` | heartbeat (every 30 min) |
| Iris | Developer | `workspace-dev` | — |
| Kat | Copywriter | `workspace-kat` | On-demand |
| Alex | Chief Growth Officer | `workspace-alex` | Hourly (optional) |
| Pierce | QC & Security | `workspace-pierce` | Daily 7 AM security · Monday 7 AM Lighthouse/UX |

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
2. **If the registry entry is incomplete or unclear**, check the actual project: `cat vercel.json`, `cat package.json`, `cat run.sh`, etc.
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

## Audio Transcription
- **Use `faster-whisper`** (CTranslate2 backend) — NOT regular `openai-whisper` (OOMs in resource-constrained environments)
- Script: `python3 ~/.openclaw/workspace/scripts/transcribe.py <audio_file> [--model base]`
- Default model: `base` (int8 quantized) — fast and accurate for most use cases
- `tiny` available for speed at slight accuracy cost
- Always convert ogg→wav via ffmpeg first (handled automatically by the script)

## Per-Agent Model Configuration
Set the right model per agent in `openclaw.json` — not dynamically mid-session (that would double-process the triggering message before switching takes effect).

**Pattern:** Orchestrator on a heavy model, specialists on a lighter one.

In `~/.openclaw/openclaw.json`:
- `agents.defaults.model.primary` → `"anthropic/claude-sonnet-4-6"` (all agents inherit this)
- Felix's agent entry → add `"model": "anthropic/claude-opus-4-6"` to override

Example agent list entries:
```json
{ "id": "main", "default": true, "name": "Felix", "workspace": "...", "model": "anthropic/claude-opus-4-6" },
{ "id": "dev",  "name": "Iris",  "workspace": "..." }
```
Iris, Kat, Alex, Pierce all inherit Sonnet from defaults — no `model` field needed.

## Self-Improvement Protocol
All agents follow the `self-improvement-protocol` skill:
- **Correction Detection:** Log corrections when user says "no, that's not right", "always do X", "never do Y"
- **3x Rule:** Same instruction 3 times → auto-promote to permanent rule in MEMORY.md
- **Self-Reflection:** After every significant task, log what worked and what didn't in daily notes
- **Nightly Assessment:** Part of the nightly deep dive — review corrections, promote patterns, flag drift
- **Cross-Agent Lessons:** If a lesson applies to all agents, report to Felix for MEMORY.md update
- **Never infer from silence.** Only log explicit corrections.

## Web Automation Stack
When any agent needs to interact with websites or scrape data, follow the `web-automation-protocol` skill. Decision tree:
1. **Direct API** — check if the site has an API first
2. **web_fetch** — simple page reads, no JS required
3. **Unbrowse** — structured data extraction, API discovery (preferred over browser for most tasks)
4. **browser tool** — when you need real UI interaction
5. **browser + proxy** — bot-protected sites
6. **browser + proxy + 2Captcha** — CAPTCHA-blocked sites

Relevant installed tools (after setup):
- **Unbrowse** — OpenClaw built-in, API-first web extraction
- **2Captcha CLI** (`solve-captcha`) — if installed; API key at `~/.config/2captcha/api-key`
- **Mobile Proxy** — if configured; config at `~/.config/litport/proxy.conf`

## Installed Skills (recommended — install from ClawHub)
| Skill | Purpose | Priority |
|-------|---------|---------|
| `audio-reply` | Mandatory audio reply procedure (edge-tts voice messages) | ⭐ Required |
| `self-improvement-protocol` | Correction detection, self-reflection, memory rules | ⭐ Required |
| `agent-comms-protocol` | When/how agents contact the user vs. resolve internally | ⭐ Required |
| `web-automation-protocol` | When/how to use Unbrowse, proxy, 2Captcha, browser | High |
| `coding-sessions` | Long-lived AI coding agents in tmux with completion hooks | High |
| `felix-orchestration` | Delegation decisions, PRD-First Rule, stall detection | High |
| `dev-agent-coding-tools` | Codex/Ralph syntax, coding tools reference | High |
| `kat-copy-workflow` | Procedure for routing copy to Kat | High |
| `pierce-issue-workflow` | Closing Pierce-opened GitHub issues | High |
| `prd-maintenance` | Keeping PRDs current after feature ships | Medium |
| `support-docs-standard` | Required support-docs/ structure for projects | Medium |
| `tmux-agents` | Persistent tmux sessions for long-running processes | Medium |
| `screenshot` | Screenshot capture across platforms | Medium |
| `research` | Web + X/Twitter search via xAI | Medium |
| `here-now` | Instant web publishing | Medium |
| `postiz` | Social media scheduling across 28+ channels | Optional |
| `x-api` | Post/read/reply on X/Twitter via v2 API | Optional |
| `2captcha` | CAPTCHA solving for web automation | Optional |

## Silent Replies
When you have nothing to say, respond with ONLY: NO_REPLY
