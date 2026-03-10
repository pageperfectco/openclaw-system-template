---
name: self-improvement-protocol
description: Structured self-improvement protocol for all agents. Correction detection, self-reflection after significant work, and memory promotion/demotion rules. Integrated into existing memory system — no new directories needed.
metadata:
  openclaw:
    emoji: 🧠
---

# Self-Improvement Protocol

**Every agent follows this protocol. It runs automatically — no user prompting needed.**

## 1. Correction Detection

### Triggers — Log When You Hear:

| User Says | Action |
|-----------|--------|
| "No, that's not right..." | Log correction immediately |
| "Actually, it should be..." | Log correction immediately |
| "I prefer X, not Y" | Log as preference |
| "Always do X for me" | Log as rule (promote to HOT) |
| "Never do Y" | Log as rule (promote to HOT) |
| "I told you before..." | ⚠️ Check memory first — you may have missed a prior correction |
| "Stop doing X" | Log as rule (promote to HOT) |
| "Why do you keep..." | Pattern failure — search memory, log fix |
| User praises specific approach | Log as positive pattern |
| Same instruction 3x | Auto-promote to permanent rule |

### What NOT to Log:
- One-time instructions ("do X now")
- Context-specific ("in this file, change...")
- Hypotheticals ("what if...")
- Silence (never infer from no response)

### Log Format (append to daily notes):
```markdown
### 🔄 Correction [HH:MM]
- **What happened:** [brief description]
- **What user wanted:** [the correct behavior]
- **Rule:** [extracted rule for future reference]
- **Occurrences:** 1 (promote at 3)
```

---

## 2. Self-Reflection

### When to Reflect:
- After completing a multi-step task
- After receiving feedback (positive or negative)
- After fixing a bug or mistake
- After a failed attempt at something
- During nightly deep dive

### Reflection Format (append to daily notes):
```markdown
### 🪞 Reflection [HH:MM]
- **Task:** [what was done]
- **Outcome:** [success/partial/failed]
- **What went well:** [specific positives]
- **What could improve:** [specific improvements]
- **Lesson:** [actionable takeaway]
- **Apply to:** [global / project-specific / domain-specific]
```

### Reflection Rules:
- Be specific, not generic. "Check spacing before showing user" > "be more careful"
- Focus on actionable changes, not feelings
- If the same lesson appears 3x → promote to MEMORY.md
- Keep reflections in daily notes, not a separate system

---

## 3. Memory Promotion & Demotion

### Our Existing Tiers:

| Tier | Location | Loaded | Purpose |
|------|----------|--------|---------|
| 🔥 HOT | `MEMORY.md` | Every session (auto-injected) | Permanent rules, project registry, tacit knowledge |
| 🌡️ WARM | `memory/YYYY-MM-DD.md` | On demand | Daily timeline, corrections, reflections, context |
| ❄️ COLD | `~/life/` (PARA) | On explicit query | Archived entities, historical decisions, long-term knowledge |

### Promotion Rules (WARM → HOT):
- Correction logged 3+ times → promote rule to MEMORY.md
- Pattern successfully applied 3+ times in 7 days → promote
- User explicitly says "always" or "never" → promote immediately
- Critical operational lesson (caused downtime, lost data, wrong deploy) → promote immediately

### Demotion Rules (HOT → WARM):
- Rule unused for 30+ days → move to a daily note as archived rule
- Rule contradicted by newer rule → replace in MEMORY.md, archive old
- Project completed/archived → move project entry to `~/life/archives/`

### MEMORY.md Size Management:
- Target: keep MEMORY.md under 500 lines
- When approaching limit: merge similar rules, summarize verbose entries
- Never delete confirmed preferences — archive to COLD instead
- When citing a rule from memory, briefly note the source: "(from correction 2026-03-05)"

---

## 4. Pattern Recognition

### Track These Patterns Across Sessions:

**Workflow patterns:**
- Which approaches get praised? → Reinforce
- Which approaches get corrected? → Adjust
- What order of operations works best? → Document

**Communication patterns:**
- How much detail does the user want? → Calibrate
- Do they prefer audio summaries or text? → Note preference
- When do they want proactive updates vs. being left alone? → Learn rhythm

**Technical patterns:**
- Which tools work best for which tasks? → Update tool protocols
- Common failure modes? → Add to gotchas
- Shortcuts discovered? → Share with other agents

### Pattern Promotion Flow:
```
Observed once → Note in daily log
Observed 2x → Flag as emerging pattern
Observed 3x → Promote to MEMORY.md as confirmed pattern
Contradicted → Demote or update
```

---

## 5. Cross-Agent Learning

When an agent learns something valuable that applies to others:

1. Log it in your own daily notes first
2. If it's universal (applies to all agents): report to Felix for MEMORY.md update
3. If it's domain-specific: update the relevant skill or protocol
4. Never modify another agent's workspace directly

### Shared Lessons Format (report to Felix):
```
AGENT: [your name]
LESSON: [what was learned]
APPLIES TO: [all agents / specific agents]
EVIDENCE: [what happened, 2-3 sentences]
SUGGESTED RULE: [the rule to add]
```

---

## 6. Nightly Self-Assessment (Part of Deep Dive)

Add these questions to the nightly review:

1. **What corrections did I receive today?** → Ensure all are logged
2. **What patterns am I seeing?** → Any ready for promotion?
3. **What surprised me?** → Novel situations = learning opportunities
4. **What took too long?** → Efficiency improvements
5. **What did I do well?** → Reinforce successful patterns
6. **Am I following my own rules?** → Self-compliance check

---

## 7. Boundaries

### DO:
- Learn from explicit corrections
- Track patterns across sessions
- Promote proven rules to permanent memory
- Reflect honestly on outcomes
- Share lessons across agents via Felix

### DO NOT:
- Infer preferences from silence
- Store credentials or sensitive data in memory tiers
- Modify SOUL.md or IDENTITY.md without user approval
- Self-modify safety boundaries or communication protocols
- Log personal/health information about the user
- Assume a correction applies universally without checking

### Safety Rails:
- Promotion to HOT (MEMORY.md) is always additive — never remove existing rules to make room
- When in doubt about a pattern, ask rather than assume
- Self-improvement never overrides direct user instructions
- All memory changes are visible in daily notes (audit trail)
