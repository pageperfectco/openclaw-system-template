---
name: felix-orchestration
description: Felix's orchestrator decision protocol for delegating coding tasks to dev agents. Use when deciding whether to run code directly, delegate to a dev agent, write a PRD first, or escalate. Covers the PRD-First Rule, stall detection thresholds, and TDD prompting standards.
---

# Felix Orchestration Protocol

## Decision Matrix — What to Run and When

| Situation | Action |
|-----------|--------|
| Quick fix, 1 file, clear scope | `codex exec --full-auto` directly |
| Multi-step, single project, no cross-agent deps | `ralphy --codex --prd PRD.md` directly |
| Feature touching multiple agents | Write PRD first → delegate to dev agent → wire other side on completion |
| Cross-agent coordination (shared interface, webhook) | Felix owns the spec, dev agent builds, Felix wires the other side |
| Daniel asks a dev to build something complex | Check if they used Ralph — nudge if not |

## PRD-First Rule

Write a PRD in the dev agent's workspace **before delegating** when the task is:
- Multi-agent (touches 2+ agent surfaces or systems)
- Estimated >1 hour of dev work
- Has a shared interface between two systems

No PRD = no delegation for complex tasks. A 20-line spec prevents 2 hours of rework.

## Stall Detection

When delegating to a dev agent, check in if no completion message within:
- Simple task: ~15 min
- Ralph loop build: ~45 min
- Complex PRD build: ~90 min

Check in proactively. Don't wait for Daniel to ask.

## TDD-First

For backend logic, always instruct Codex to write failing tests first, then implement to pass. All tests must pass before committing.

## Execution Reference

For Ralph commands, Codex syntax, wrong flags, and verify-before-fail: see `dev-agent-coding-tools` skill.
