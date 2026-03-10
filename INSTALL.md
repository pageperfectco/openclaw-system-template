# INSTALL.md — OpenClaw System Bootstrap

> **For AI agents reading this:** Follow each step in order. Do not skip sections. Confirm completion before moving on. All commands run in your sandbox — not on behalf of any other agent.

---

## What This Installs

A 6-agent OpenClaw system:
- **Felix** — CEO/Orchestrator (main agent)
- **Iris** — Developer (rename to whatever fits your stack)
- **Kat** — Copywriter
- **Alex** — Growth / CRO
- **Pierce** — QC & Security
- **Silas** — SEO Lead

---

## Step 1 — Clone & Copy Workspace Files

```bash
git clone https://github.com/pageperfectco/openclaw-system-template /tmp/openclaw-system-template

cp -r /tmp/openclaw-system-template/workspace/ ~/.openclaw/workspace/
cp -r /tmp/openclaw-system-template/workspace-dev/ ~/.openclaw/workspace-dev/
cp -r /tmp/openclaw-system-template/workspace-kat/ ~/.openclaw/workspace-kat/
cp -r /tmp/openclaw-system-template/workspace-alex/ ~/.openclaw/workspace-alex/
cp -r /tmp/openclaw-system-template/workspace-pierce/ ~/.openclaw/workspace-pierce/
cp -r /tmp/openclaw-system-template/workspace-silas/ ~/.openclaw/workspace-silas/
```

> ⚠️ If `~/.openclaw/workspace/` already exists, review before overwriting — you may have existing config.

---

## Step 2 — Update IDENTITY.md and USER.md

In `~/.openclaw/workspace/`:
- **`USER.md`** — Fill in the user's name, timezone, email, and any personal context.
- **`IDENTITY.md`** — Felix's identity is pre-filled. Adjust if you want to rename.

In `~/.openclaw/workspace-dev/`:
- **`IDENTITY.md`** — Rename "Iris" to whatever fits your stack. Update mission to match.

In each agent workspace (`workspace-kat/`, `workspace-alex/`, `workspace-pierce/`, `workspace-silas/`):
- **`IDENTITY.md`** — Review and adjust the agent name/role if desired.

---

## Step 3 — Connect GitHub

GitHub is required for the backup repo (Step 6) and for Iris to push code. Check if the GitHub CLI is already authenticated:

```bash
gh auth status
```

If not authenticated:

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

## Step 5 — Configure Per-Agent Models

Edit `~/.openclaw/openclaw.json` to set models. The pattern: orchestrator on Opus, everyone else on Sonnet.

In the `agents` section, set the global default to Sonnet and give Felix an explicit Opus override:

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "anthropic/claude-sonnet-4-6"
    }
  },
  "list": [
    { "id": "main",  "default": true, "name": "Felix",  "workspace": "/home/node/.openclaw/workspace",        "model": "anthropic/claude-opus-4-6" },
    { "id": "dev",   "name": "Iris",   "workspace": "/home/node/.openclaw/workspace-dev" },
    { "id": "kat",   "name": "Kat",    "workspace": "/home/node/.openclaw/workspace-kat" },
    { "id": "alex",  "name": "Alex",   "workspace": "/home/node/.openclaw/workspace-alex" },
    { "id": "pierce","name": "Pierce", "workspace": "/home/node/.openclaw/workspace-pierce" },
    { "id": "silas", "name": "Silas",  "workspace": "/home/node/.openclaw/workspace-silas" }
  ]
}
```

Iris, Kat, Alex, Pierce, and Silas inherit Sonnet from the default — no `model` field needed on their entries. Felix gets Opus explicitly. This avoids any mid-session model switching, which would double-process the triggering message.

---

## Step 6 — Restart the Gateway

After copying workspace files and updating `openclaw.json`, restart the gateway so all new agents load:

```bash
openclaw gateway restart
```

Verify it's running:

```bash
openclaw gateway status
```

---

## Step 7 — Initialize Agent Status + Task Queue

```bash
cd ~/.openclaw/workspace
python3 scripts/agent-status.py show
python3 scripts/task-queue.py list
```

Both should run without errors. If they do, the agent dispatch system is live.

---

## Step 8 — Set Up Your Personal Backup Repo

This gives you a full git history of your workspace — so if a config change breaks something, you can revert instantly.

```bash
# Create a private backup repo on GitHub
gh repo create openclaw-workspaces-backup --private

# Clone it to the expected location
git clone https://github.com/[your-username]/openclaw-workspaces-backup ~/.openclaw/workspaces-backup

# Run a first backup
bash ~/.openclaw/workspace/scripts/backup-workspaces.sh
```

From this point on, Felix will commit workspace changes every heartbeat. To revert a bad change:
```bash
cd ~/.openclaw/workspaces-backup
git log --oneline -10       # find the commit to revert to
git revert HEAD             # or: git checkout <commit> -- workspace/MEMORY.md
```

> This repo is yours — it evolves with your system over time. Keep it private.

---

## Step 9 — Install Coding Agent CLIs

These CLIs are required for Iris (and any dev agent) to run coding tasks. Install them all upfront.

```bash
# Codex CLI (OpenAI) — raw code execution agent
npm install -g @openai/codex

# Claude Code (Anthropic) — alternative coding agent
npm install -g @anthropic-ai/claude-code

# Ralphy — Ralph orchestration loop for multi-step coding tasks with PRD validation
npm install -g ralphy
```

Verify they're all working:

```bash
codex --version
claude --version
ralphy --help
```

> **What is Ralphy?** It's the Ralph orchestration loop — used when a task is complex enough to need iterative cycles, a PRD spec, or validation gates. Dev agents prefer it over raw Codex for anything multi-step. Without it installed, they'll fall back to raw Codex, which is less reliable for large tasks.

---

## Step 10 — Install Voice (STT + TTS)

This gives all agents the ability to understand your voice messages (via Whisper) and speak back with unique voices (via Edge TTS).

### Install faster-whisper (speech-to-text)

```bash
pip3 install faster-whisper --break-system-packages
```

Test it (first run downloads the model — ~150MB for `base`):

```bash
python3 ~/.openclaw/workspace/scripts/transcribe.py /path/to/any/audio.mp3
```

> **Why faster-whisper instead of openai-whisper?** CTranslate2 backend uses ~4x less RAM — works reliably in memory-constrained sandboxes. Uses int8 quantization with no accuracy penalty for speech.

### Install Edge TTS (text-to-speech)

```bash
pip3 install edge-tts --break-system-packages
```

Test it:

```bash
edge-tts --voice en-US-GuyNeural --rate +20% --text "Felix online." --write-media /tmp/test-tts.mp3
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
            "command": "python3",
            "args": ["/home/node/.openclaw/workspace/scripts/transcribe.py", "{{MediaPath}}"],
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

### Voice roster (defaults — change any time in the agent's `SOUL.md`)

| Agent | Voice | Gender |
|-------|-------|--------|
| Felix | en-US-GuyNeural | Male |
| Iris (dev) | en-US-JennyNeural | Female |
| Kat | en-US-MichelleNeural | Female |
| Alex | en-US-DavisNeural | Male |
| Pierce | en-US-RogerNeural | Male |

---

## Step 11 — Configure Cron Jobs

```bash
# Felix heartbeat — runs every 30 minutes
openclaw cron add --label "felix:heartbeat" --schedule "*/30 * * * *" --workspace workspace --prompt "Heartbeat"

# Pierce daily security audit — runs at 7 AM in your timezone (adjust as needed)
openclaw cron add --agent pierce --name "pierce-daily-security-audit" --cron "0 7 * * *" --tz "America/Denver" --session isolated --message "Run your daily security audit across all active projects: check all new commits since yesterday, scan for secrets/credentials in code, review dependency vulnerabilities (npm audit / pip audit), verify security headers on all live sites, check RLS on any new Supabase tables, and review open GitHub security issues. Report findings ranked by severity. Open GitHub issues for Tier 2+ findings. Page Felix immediately for Tier 3 critical findings."

# Pierce weekly Lighthouse/UX audit — runs every Monday at 7 AM
openclaw cron add --agent pierce --name "pierce-weekly-lighthouse-ux" --cron "0 7 * * 1" --tz "America/Denver" --session isolated --message "Run your weekly Lighthouse and UX/UI audit across all active projects: run Lighthouse on all live sites, record scores in MEMORY.md, flag any drop >5 points from last week. Review each site for UX/UI improvements: layout issues, accessibility gaps, mobile responsiveness, broken links, slow assets. Document findings and open GitHub issues for anything worth fixing. Focus purely on UX/UI quality and performance — no security checks today."

# Alex hourly growth check (optional — enable when projects are live)
# openclaw cron add --agent alex --name "alex:growth" --cron "0 * * * *" --tz "America/Denver" --session isolated --message "Review active tests, check metrics, report any significant movements."
```

> ⚠️ Update the timezone (`America/Denver`) to match your local timezone.

---

## Step 12 — Install Recommended Skills

Skills extend what agents can do. Install from [ClawHub](https://clawhub.com):

**Required (install these first):**
```bash
# Audio reply — agents respond with voice messages
clawhub install audio-reply --all-workspaces

# Self-improvement — correction detection + memory promotion
clawhub install self-improvement-protocol --all-workspaces

# Agent comms — governs when/how agents contact the user
clawhub install agent-comms-protocol --all-workspaces
```

**Highly recommended:**
```bash
# Web automation protocol — decision tree for web scraping/automation
clawhub install web-automation-protocol --all-workspaces

# Coding sessions — long-lived agents in tmux with completion hooks
clawhub install coding-sessions --workspace workspace-dev

# Felix orchestration — PRD-First Rule, stall detection, delegation logic
clawhub install felix-orchestration --workspace workspace

# Dev agent coding tools — Codex/Ralph syntax reference
clawhub install dev-agent-coding-tools --workspace workspace-dev

# Copy workflow — how to brief Kat properly
clawhub install kat-copy-workflow --all-workspaces

# Pierce issue workflow — how to close Pierce-opened GitHub issues
clawhub install pierce-issue-workflow --workspace workspace
```

**Optional (add when needed):**
```bash
clawhub install research --all-workspaces       # Grok + X/Twitter search
clawhub install here-now --workspace workspace   # Instant web publishing
clawhub install x-api --workspace workspace-alex # X/Twitter via v2 API
clawhub install postiz --workspace workspace-alex # Social media scheduler
clawhub install screenshot --all-workspaces      # Screen capture
clawhub install 2captcha --workspace workspace    # CAPTCHA solving
```

> Not all skill slugs above may match the exact ClawHub names — search ClawHub if a command fails.

---

## Step 13 — Set Up Email (Optional)

For outbound agent email via [AgentMail](https://agentmail.to):
1. Create an account at agentmail.to
2. Create an inbox for Felix: `felix@[yourdomain].agentmail.to`
3. Save API key: `echo "your-key-here" > ~/.config/agentmail/api_key`
4. Update the inbox ID in `workspace/AGENTS.md` and `workspace/MEMORY.md`
5. Optionally create inboxes for other agents (Kat, Alex) and update their AGENTS.md

---

## Step 14 — Bootstrap

Felix's workspace has a `BOOTSTRAP.md`. Open a chat with Felix and say:

> "Start your bootstrap sequence."

Felix will walk through personalizing the setup, confirming agent connections, and running a first health check.

---

## You're Done

Tell Felix:
> "Installation complete. Run a first health check and introduce yourself."
