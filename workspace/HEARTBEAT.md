# HEARTBEAT.md — Felix Heartbeat Checklist

Run this checklist on every heartbeat. Adapt the specific checks to your business.

## Task Queue + Agent Status Check (every heartbeat)
1. Run `python3 ~/.openclaw/workspace/scripts/task-queue.py ready`
2. For each ready task:
   - Check `agent-status.py is-busy <agent>` — if still busy, skip (will retry next heartbeat)
   - If idle: deliver via `sessions_send`, mark agent busy, mark task complete
3. When an agent reports back (completion message): mark them idle with `agent-status.py set <agent> idle` — this may unlock queued tasks

## Execution Check (every heartbeat)
1. Read today's plan from `memory/YYYY-MM-DD.md` under "## Today's Plan"
2. Check progress against each planned item — what's done, what's blocked, what's next
3. If something is blocked, unblock it or escalate to the user
4. If ahead of plan, pull the next priority forward
5. Log progress updates to daily notes

## CLI Dependency Check (once per day, first heartbeat)
Verify these are installed and working:
- `codex --version` → should return codex-cli version
- `claude --version` → should return Claude Code version
- `ralphy --help` → should return Ralph CLI help
If any are missing: install immediately (`npm install -g @openai/codex @anthropic-ai/claude-code`) before any dev agent tasks run.

## Site Health Check (every heartbeat)
1. Check all production sites return 200 (add your sites here once live)
2. If any site is down, **alert user immediately**
3. If it's a deployment issue you can fix, fix it first, then report

> _Add your production URLs here as projects go live:_
> ```
> # Example:
> # https://yourapp.vercel.app → 200
> ```

## Cron Job Health Check (every heartbeat)
1. Run `openclaw cron list` — verify no jobs show as disabled or missing
2. Felix-owned cron jobs: _(add your cron job IDs here after setup)_

## Long-Running Agent Health Check (every heartbeat)
1. Read `memory/YYYY-MM-DD.md` for listed active tmux sessions (under "Active Long-Running Processes")
2. For each session: `tmux -S ~/.tmux/sock has-session -t <name> 2>/dev/null`
3. If alive: `tmux -S ~/.tmux/sock capture-pane -t <name> -p | tail -5` for progress
4. **If dead or missing:** Restart it. Don't ask, just fix it.
5. **If stalled** (same output for 2+ heartbeats): Kill and restart
6. If finished successfully: Report completion and remove from daily notes

## Agent Status Discrepancy Check (every heartbeat)
Run `python3 ~/.openclaw/workspace/scripts/agent-status.py show` and cross-check:
- Any agent showing **idle** but has an active tmux session → flag as discrepancy, investigate
- Any agent showing **busy** with no active session and no recent git commits → likely stale, reset to idle
- Discrepancies should be reported to the user — don't silently fix without noting it

## Workspace Backup (every heartbeat)
Run the backup script to sync all agent workspaces to the private backup repo:
```bash
bash ~/.openclaw/workspace/scripts/backup-workspaces.sh
```
If push fails, note it — don't block on it. Backup is best-effort on each heartbeat.

## Fact Extraction (every heartbeat)
1. Check for new conversations since last extraction
2. Extract durable facts to relevant entity in `~/life/` (PARA)
3. Update `memory/YYYY-MM-DD.md` with timeline entries
4. Track extraction timestamp + access metadata

## Self-Improvement Check (every heartbeat)
1. Review any corrections received since last heartbeat — are they logged in daily notes?
2. Any correction that has appeared 3+ times → promote to MEMORY.md as a permanent rule
3. If a lesson applies to all agents → update MEMORY.md and notify relevant agents

## Nightly Deep Dive (run once per day, late night)
1. **Revenue/metrics review:**
   - Pull previous day's metrics (NOT current partial day — if running at 3 AM, "today" only has 3 hours of data)
   - ⚠️ ALWAYS use the completed previous calendar day for nightly reports
2. **Day review:**
   - What got done from today's plan?
   - What didn't get done and why?
3. **Propose tomorrow's plan:**
   - 3-5 concrete actions ranked by expected impact
   - Each item should connect to the primary goal
   - Write to next day's file under "## Today's Plan"
4. **Self-assessment:**
   - What corrections did I receive today?
   - What patterns am I seeing?
   - Am I following my own rules?
5. **Send summary to user** — key metrics, day recap, tomorrow's proposed plan
