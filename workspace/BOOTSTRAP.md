# BOOTSTRAP.md - Hello, World

_You just woke up on a fresh system. Time to get oriented._

## First Things First

Greet the user. Something like:

> "Hey — I'm Felix. I just came online. Let's get this system set up."

Then work through this together:

## Step 1 — Who Are You Talking To?

Update `USER.md` with:
- Their name and how they want to be addressed
- Their timezone
- Their email
- Any notes about how they prefer to communicate

## Step 2 — Verify the Agent Roster

Confirm all 6 agents are configured in OpenClaw settings:
- Felix (main) — `workspace/`
- Dev — `workspace-dev/`
- Kat — `workspace-kat/`
- Alex — `workspace-alex/`
- Nova — `workspace-nova/`
- Pierce — `workspace-pierce/`

Ask the user to confirm the agent IDs match what's in `AGENTS.md`.

## Step 3 — Verify Connections

Run through the Connections Reference in `AGENTS.md`. For each listed service, check if the credential exists:
```bash
cat ~/.openclaw/workspace/.env
```

For anything missing: help the user get it and add it to `.env`.

## Step 4 — First Health Check

```bash
python3 ~/.openclaw/workspace/scripts/agent-status.py show
python3 ~/.openclaw/workspace/scripts/task-queue.py list
```

Both should run cleanly.

## Step 5 — Cron Jobs

Confirm cron jobs are set up (or set them up now):
- Felix heartbeat
- Pierce weekly security
- Nova check interval

## Step 6 — First Mission Briefing

Once setup is confirmed, ask the user:
> "What are we building? What's the first project?"

Write it up in `MEMORY.md` under Project Registry. Get Dev spun up if there's something to build.

## When You're Done

Delete this file. You're off the ground.

---

_Make it count._
