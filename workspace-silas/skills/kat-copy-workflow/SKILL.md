---
name: kat-copy-workflow
description: Workflow for requesting customer-facing copy from Kat. Use when any agent needs copy written — landing pages, emails, CTAs, product descriptions, onboarding text, social posts, button labels, or any text a customer reads. Never write customer-facing copy yourself.
---

# Kat Copy Workflow

**HARD RULE: Do not write customer-facing copy yourself.** All copy a customer reads must come from Kat.

## Before Requesting

Check `~/.openclaw/workspace-kat/copy-library/[project]/` — approved copy for your surface may already exist. If it does, use it (or ask Kat for a light update).

## How to Request (trigger Kat directly — no Felix or Daniel involvement)

1. Read the brief template: `~/.openclaw/workspace-kat/copy-queue/BRIEF-TEMPLATE.md`
2. Write a complete brief to: `~/.openclaw/workspace-kat/copy-queue/YYYY-MM-DD-[project]-[surface]-[name].md`
3. Trigger Kat:
   ```
   sessions_send(agentId="kat", message="New brief in your queue: [filename]. Needed by [date].")
   ```

## After Kat Delivers

Kat notifies you via `sessions_send`. Find copy at `~/.openclaw/workspace-kat/copy-delivered/[filename]`.

Implement exactly as written. If a hard structural constraint requires deviation, note it.

## Exception

If Kat emails Daniel for brand voice input on a new project, that's the only time Daniel is in the loop. Everything else runs between you and Kat.
