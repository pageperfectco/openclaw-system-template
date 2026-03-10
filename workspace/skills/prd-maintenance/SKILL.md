---
name: prd-maintenance
description: Rules for keeping PRD files current in dev agent projects (Max/MSC, Wendy/WC Stats, Lux/VERILUX). Use after any feature ship, architecture change, or scope decision. PRD is the source of truth — support-docs/ derives from it.
---

# PRD Maintenance

The PRD is the source of truth for your project. **Update it whenever reality diverges from what's written.**

## What Triggers a PRD Update

- New feature shipped
- Feature cut or descoped
- Architecture decision made (new integration, new table, changed data model)
- Known limitation discovered

## Rules

- `support-docs/` derives from the PRD — if the PRD changes, review support-docs for consistency
- Reflect current reality, not original plans — strike through or remove cut features; add what was actually built
- Pierce flags PRDs that are >30 days older than the last deploy as stale and opens a `[Docs] PRD is stale` GitHub issue
