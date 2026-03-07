# MEMORY.md — Dev Tacit Knowledge + Project Registry

## Active Projects

> _No projects yet. Add each project as it's created._
>
> **Template:**
> ### [Project Name]
> - **Repo:** github.com/[owner]/[repo]
> - **URL:** https://...
> - **Stack:** [tech]
> - **Deploy:** [how]
> - **Key files:** [any important paths]
> - **Notes:** [gotchas, decisions made, etc.]

## Development Standards
- TDD-first: write failing tests, then implement
- All tests must pass before committing
- Commit after every meaningful chunk — don't batch unrelated changes
- PR over direct push for anything non-trivial

## Tools
- **Codex:** `codex exec --full-auto "task"`
- **Ralph loop:** `ralphy --codex --prd PRD.md`
- Verify before declaring failure: `git log --oneline -3` + `git diff --stat`
