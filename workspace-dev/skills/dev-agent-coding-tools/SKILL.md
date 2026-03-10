---
name: dev-agent-coding-tools
description: Coding task execution protocol for dev agents (Max, Wendy, Lux). Covers when to use Ralph loop vs raw Codex, correct CLI syntax, agent status marking, and failure verification. Use before starting any coding task.
---

# Dev Agent Coding Tools

## Agent Status — Mark on Every Task

Before ANY coding task:
```bash
python3 /home/node/.openclaw/workspace/scripts/agent-status.py set <AGENT> busy "brief description"
```

On completion (success OR failure — no exceptions):
```bash
python3 /home/node/.openclaw/workspace/scripts/agent-status.py set <AGENT> idle
```

## Ralph Loop vs Raw Codex

### Use Ralph (`ralphy`) when:
- Task has a PRD or spec
- Touches 3+ layers (DB + API + frontend)
- Estimated >30 minutes
- Creating new tables, routes, or integrations
- "Build X feature" tasks
- Stalled or failed twice on raw Codex

```bash
PATH=/home/linuxbrew/.linuxbrew/bin:/home/node/.npm-global/bin:$PATH ralphy --codex --prd PRD.md
PATH=/home/linuxbrew/.linuxbrew/bin:/home/node/.npm-global/bin:$PATH ralphy --codex "Task description"
PATH=/home/linuxbrew/.linuxbrew/bin:/home/node/.npm-global/bin:$PATH ralphy --codex --fast "Quick fix"
ANTHROPIC_API_KEY=$(grep ANTHROPIC_RALPH_KEY /home/node/.openclaw/workspace/.env | cut -d= -f2) PATH=/home/linuxbrew/.linuxbrew/bin:/home/node/.npm-global/bin:$PATH ralphy --claude "Task"
PATH=/home/linuxbrew/.linuxbrew/bin:/home/node/.npm-global/bin:$PATH ralphy --codex --max-iterations 10 "Task"
```

### Use raw Codex when:
- Single file fix with clear repro
- Style, copy, or config tweak
- Estimated <15 minutes
- "Fix Y" or "Change Z" tasks

```bash
codex exec --full-auto "Task description"
```

### Ask Felix when:
- Task touches another agent
- Complex architecture with no PRD and no clear answer
- Stalled after 3 Ralph iterations

## ⚠️ Wrong Flags — Do NOT Use
- `--yolo` — does not exist
- `--approval-mode` — does not exist
- `-q` — does not exist on `codex exec`
- Prompt is a **positional argument**, not a flag

## Verify Before Declaring Failure

When a Codex/Ralph process ends, always check before giving up:
1. `git log --oneline -3` — did it commit?
2. `git diff --stat` — uncommitted changes?
3. `process action:log sessionId:XXX` — actual output
