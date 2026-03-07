# INSTALL.md — OpenClaw System Bootstrap

> **For AI agents reading this:** Follow each step in order. Do not skip sections. Confirm completion before moving on.

---

## What This Installs

A 6-agent OpenClaw system:
- **Felix** — CEO/Orchestrator (main agent)
- **Iris** — Developer (or rename to whatever fits your stack)
- **Kat** — Copywriter
- **Alex** — Growth / CRO
- **Nova** — Customer Success
- **Pierce** — QC & Security

---

## Step 1 — Copy Workspace Files

Copy each workspace folder from this repo to `~/.openclaw/`:

```bash
cp -r workspace/ ~/.openclaw/workspace/
cp -r workspace-dev/ ~/.openclaw/workspace-dev/
cp -r workspace-kat/ ~/.openclaw/workspace-kat/
cp -r workspace-alex/ ~/.openclaw/workspace-alex/
cp -r workspace-nova/ ~/.openclaw/workspace-nova/
cp -r workspace-pierce/ ~/.openclaw/workspace-pierce/
```

> ⚠️ If `~/.openclaw/workspace/` already exists, review before overwriting — you may have existing config.

---

## Step 2 — Update IDENTITY.md and USER.md

In `~/.openclaw/workspace/`:
- **`USER.md`** — Fill in your name, timezone, email, and any personal context.
- **`IDENTITY.md`** — Felix's identity is pre-filled. Adjust if you want to rename.

In `~/.openclaw/workspace-dev/`:
- **`IDENTITY.md`** — Rename "Dev" to whatever fits (e.g. "Sam", "Rex", "Cody"). Update mission to match your stack.

---

## Step 3 — Gather Credentials

You'll need these services connected. For each one, get the credential and add it to `~/.openclaw/workspace/.env`:

```bash
touch ~/.openclaw/workspace/.env
```

**Minimum viable setup (start here):**
| Service | What to get | Env var |
|---------|------------|---------|
| GitHub | Personal access token (PAT) | `GITHUB_PAT` |
| Vercel | Access token | `VERCEL_TOKEN` |
| OpenAI or Anthropic | API key (for Codex/Claude Code) | `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` |

**When you're ready to expand:**
| Service | What to get | Env var |
|---------|------------|---------|
| Stripe | Secret key | `STRIPE_SECRET_KEY` |
| Supabase | Personal access token | `SUPABASE_PAT` |
| Cloudflare | API token | `CLOUDFLARE_API_TOKEN` |
| AgentMail | API key | Store at `~/.config/agentmail/api_key` |

> **Note:** Some services (Vercel, Stripe, GitHub) can also be connected via Composio for richer tool access. See OpenClaw docs for Composio connection setup.

---

## Step 4 — Initialize Agent Status + Task Queue

```bash
cd ~/.openclaw/workspace
python3 scripts/agent-status.py show
python3 scripts/task-queue.py list
```

Both should run without errors. If they do, your agent dispatch system is live.

---

## Step 5 — Configure Cron Jobs

Open OpenClaw settings and create these cron jobs:

| Job | Agent | Schedule | Description |
|-----|-------|----------|-------------|
| Felix heartbeat | Felix | Every 30-60 min (your choice) | Task queue checks, site health, agent monitoring |
| Pierce security | Pierce | Weekly (e.g. Monday 9 AM) | Security audit |
| Nova customer check | Nova | Every 15-30 min | Customer support inbox check |

In OpenClaw CLI:
```bash
openclaw cron add --label "felix:heartbeat" --schedule "*/30 * * * *" --workspace workspace --prompt "Heartbeat"
openclaw cron add --label "pierce:security" --schedule "0 9 * * 1" --workspace workspace-pierce --prompt "Run your weekly security audit"
openclaw cron add --label "nova:check" --schedule "*/15 * * * *" --workspace workspace-nova --prompt "Check inbox and handle any customer messages"
```

---

## Step 6 — Read BOOTSTRAP.md

Felix's workspace has a `BOOTSTRAP.md` with first-run instructions. Open a chat with Felix and say:

> "Start your bootstrap sequence."

Felix will walk you through personalizing the setup, confirming agent connections, and running a first health check.

---

## Step 7 — Optional: Set Up Email

For outbound agent email, the system is pre-configured for [AgentMail](https://agentmail.to):
1. Create an account at agentmail.to
2. Create inboxes: `felix@[yourdomain].agentmail.to`, `nova@[yourdomain].agentmail.to`
3. Save API key to `~/.config/agentmail/api_key`
4. Update inbox IDs in each agent's `AGENTS.md`

---

## You're Done

Tell Felix:
> "Installation complete. Run a first health check and introduce yourself."

He'll verify the setup, tell you what's working, and propose your first plan.
