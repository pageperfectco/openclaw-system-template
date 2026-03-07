# INSTALL.md — OpenClaw System Bootstrap

> **For AI agents reading this:** Follow each step in order. Do not skip sections. Confirm completion before moving on. All commands run in your sandbox — not on behalf of any other agent.

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

## Step 1 — Clone & Copy Workspace Files

Clone the repo and copy each workspace folder to `~/.openclaw/`:

```bash
git clone https://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@github.com/pageperfectco/openclaw-system-template /tmp/openclaw-system-template

cp -r /tmp/openclaw-system-template/workspace/ ~/.openclaw/workspace/
cp -r /tmp/openclaw-system-template/workspace-dev/ ~/.openclaw/workspace-dev/
cp -r /tmp/openclaw-system-template/workspace-kat/ ~/.openclaw/workspace-kat/
cp -r /tmp/openclaw-system-template/workspace-alex/ ~/.openclaw/workspace-alex/
cp -r /tmp/openclaw-system-template/workspace-nova/ ~/.openclaw/workspace-nova/
cp -r /tmp/openclaw-system-template/workspace-pierce/ ~/.openclaw/workspace-pierce/
```

> ⚠️ If `~/.openclaw/workspace/` already exists, review before overwriting — you may have existing config.

---

## Step 2 — Update IDENTITY.md and USER.md

In `~/.openclaw/workspace/`:
- **`USER.md`** — Fill in the user's name, timezone, email, and any personal context.
- **`IDENTITY.md`** — Felix's identity is pre-filled. Adjust if they want to rename.

In `~/.openclaw/workspace-dev/`:
- **`IDENTITY.md`** — Rename "Iris" to whatever fits. Update mission to match the stack.

---

## Step 3 — Connect GitHub

GitHub is required for the backup repo (Step 6) and for Iris to push code. Check if the GitHub CLI is already authenticated:

```bash
gh auth status
```

If not authenticated, run the login flow:

```bash
gh auth login
```

Follow the prompts — it will open a browser window to authorize. Once complete, verify:

```bash
gh auth status
```

Then add a GitHub Personal Access Token (PAT) to `.env` for git operations:

```bash
touch ~/.openclaw/workspace/.env
# Add: GITHUB_PAT=ghp_...your token here...
```

To create a PAT: GitHub → Settings → Developer settings → Personal access tokens → Fine-grained → New token. Scope: your repos, Contents read/write.

---

## Step 4 — Gather Remaining Credentials

Add these to `~/.openclaw/workspace/.env`:

**Minimum viable setup:**
| Service | What to get | Env var |
|---------|------------|---------|
| Vercel | Access token | `VERCEL_TOKEN` |
| OpenAI or Anthropic | API key (for Codex/Claude Code) | `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` |

**When ready to expand:**
| Service | What to get | Env var |
|---------|------------|---------|
| Stripe | Secret key | `STRIPE_SECRET_KEY` |
| Supabase | Personal access token | `SUPABASE_PAT` |
| Cloudflare | API token | `CLOUDFLARE_API_TOKEN` |
| AgentMail | API key | Store at `~/.config/agentmail/api_key` |

> Some services (Vercel, Stripe) can also be connected via Composio for richer tool access. See OpenClaw docs.

---

## Step 5 — Initialize Agent Status + Task Queue

```bash
cd ~/.openclaw/workspace
python3 scripts/agent-status.py show
python3 scripts/task-queue.py list
```

Both should run without errors. If they do, the agent dispatch system is live.

---

## Step 6 — Set Up Your Personal Backup Repo

This gives you a full git history of your workspace — so if a config change breaks something, you can revert instantly.

```bash
# Initialize workspace as a git repo
cd ~/.openclaw/workspace
git init
git add -A
git commit -m "Initial workspace setup"

# Create a private backup repo on GitHub and push
gh repo create openclaw-workspace-backup --private --source=. --remote=origin --push
```

From this point on, Felix will commit workspace changes periodically. To revert a bad change:
```bash
cd ~/.openclaw/workspace
git log --oneline -10       # find the commit to revert to
git revert HEAD             # or: git checkout <commit> -- MEMORY.md
```

> This repo is yours — it evolves with your system over time. Keep it private.

---

## Step 7 — Install Voice (STT + TTS)

This gives all agents the ability to understand your voice messages (via Whisper) and speak back with unique voices (via Edge TTS).

### Install Whisper (speech-to-text)

```bash
pip3 install openai-whisper --break-system-packages
python3 -c "import whisper; whisper.load_model('small'); print('Whisper ready')"
```

### Install Edge TTS (text-to-speech)

```bash
pip3 install edge-tts --break-system-packages
```

### Configure `openclaw.json`

Add the following to your `~/.openclaw/openclaw.json` under the root object (merge with existing keys — do not replace the whole file):

```json5
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "echoTranscript": false,
        "models": [
          {
            "type": "cli",
            "command": "/home/node/.local/bin/whisper",
            "args": ["--model", "small", "{{MediaPath}}"],
            "capabilities": ["audio"],
            "maxBytes": 25165824
          }
        ]
      }
    }
  },
  "messages": {
    "tts": {
      "auto": "tagged",
      "provider": "edge",
      "modelOverrides": { "enabled": true },
      "edge": { "enabled": true }
    }
  }
}
```

> **Note:** Each agent's `SOUL.md` already includes their assigned voice and the edge-tts command pattern. No additional config needed per agent.

### Voice roster (defaults — change any time in `SOUL.md`)

| Agent | Voice | Gender |
|-------|-------|--------|
| Felix | en-US-GuyNeural | Male |
| Iris (dev) | en-US-JennyNeural | Female |
| Kat | en-US-MichelleNeural | Female |
| Alex | en-US-DavisNeural | Male |
| Nova | en-US-AriaNeural | Female |
| Pierce | en-US-RogerNeural | Male |

---

## Step 8 — Configure Cron Jobs

```bash
openclaw cron add --label "felix:heartbeat" --schedule "*/30 * * * *" --workspace workspace --prompt "Heartbeat"
openclaw cron add --label "pierce:security" --schedule "0 9 * * 1" --workspace workspace-pierce --prompt "Run your weekly security audit"
openclaw cron add --label "nova:check" --schedule "*/15 * * * *" --workspace workspace-nova --prompt "Check inbox and handle any customer messages"
```

---

## Step 9 — Optional: Set Up Email

For outbound agent email via [AgentMail](https://agentmail.to):
1. Create an account at agentmail.to
2. Create inboxes: `felix@[yourdomain].agentmail.to`, `nova@[yourdomain].agentmail.to`
3. Save API key to `~/.config/agentmail/api_key`
4. Update inbox IDs in each agent's `AGENTS.md`

---

## Step 10 — Bootstrap

Felix's workspace has a `BOOTSTRAP.md`. Open a chat with Felix and say:

> "Start your bootstrap sequence."

Felix will walk through personalizing the setup, confirming agent connections, and running a first health check.

---

## You're Done

Tell Felix:
> "Installation complete. Run a first health check and introduce yourself."
