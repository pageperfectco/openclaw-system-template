---
name: tmux-agents
description: Pattern for running long-lived AI coding agents (Codex, Claude, Ralph) in persistent tmux sessions that survive gateway restarts. Use when launching any process that runs longer than 5 minutes. Covers stable socket setup, session creation, completion hooks, and stall detection.
---

# tmux Agents

Background exec processes die on gateway restart. Use tmux for anything >5 minutes.

## Stable Socket

**Always use `~/.tmux/sock`** — the default `/tmp` socket gets reaped by the OS.

## Launch a Session

```bash
tmux -S ~/.tmux/sock new -d -s <session-name> "cd <project-dir> && \
  PATH=/home/linuxbrew/.linuxbrew/bin:/home/node/.npm-global/bin:$PATH \
  ralphy --codex --prd PRD.md; \
  EXIT_CODE=$?; echo \"EXITED: $EXIT_CODE\"; \
  openclaw system event --text \"<session-name> finished (exit $EXIT_CODE)\" --mode now; \
  sleep 999999"
```

The completion hook fires a wake event → agent gets pinged immediately.  
The `sleep 999999` keeps the shell alive so output remains readable.

## Check Progress

```bash
tmux -S ~/.tmux/sock capture-pane -t <session-name> -p | tail -20
```

## Check if Alive

```bash
tmux -S ~/.tmux/sock has-session -t <session-name> 2>/dev/null && echo "alive" || echo "dead"
```

## Kill a Session

```bash
tmux -S ~/.tmux/sock kill-session -t <session-name>
```

## Rules

- Log session name in daily notes (`memory/YYYY-MM-DD.md`) so it survives context compaction
- On heartbeat: check sessions listed in daily notes — if dead, restart without asking
- If stalled (same output for 2+ heartbeats): kill and restart
- On success: report completion and remove from daily notes
