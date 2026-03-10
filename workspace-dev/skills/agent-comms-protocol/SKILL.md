---
name: agent-comms-protocol
description: Communication protocol governing when and how agents contact the user. Use this skill to determine whether to escalate to the user or resolve internally. Covers user contact rules, Felix monitoring policy, and project ownership for outbound reporting.
---

# Agent Communication Protocol

## Contact the user ONLY when:
1. A final deliverable is ready for his review or sign-off, OR
2. There is a genuine blocker requiring *his* authority — not something agents can sort out between themselves

## Do NOT contact the user about:
- Intermediate status updates or progress checks
- Coordination handoffs between agents
- A blocker another agent already raised
- Anything Felix can resolve without user input

**Felix monitors silently.** Do not relay intermediate updates through Felix to the user. Work directly with other agents. Report final outputs to the user yourself if you own the project.

## Reporting Ownership (who contacts the user per project)

| Project | Owner |
|---------|-------|
| VERILUX | Lux (Alex on growth/CRO decisions) |
| MSC Montana | Max |
| WC Stats | Wendy |
| Copy requests | Kat (only for brand voice questions on new projects) |
| Security/QC findings | Pierce |
| All other cross-agent work | Resolve between agents; Felix escalates only if truly blocked |
