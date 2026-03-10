---
name: pierce-issue-workflow
description: Procedure for closing GitHub issues opened by Pierce (QC/security agent). Use when a Pierce audit issue has been fixed and is ready to close. Requires verified live evidence before closing — never close on assumption.
---

# Pierce Issue Workflow

**HARD RULE: Never close a Pierce GitHub issue without verified evidence the fix is live.**

## Before Closing Any Pierce Issue

1. **Commit the fix** — change committed and pushed
2. **Deploy** — fix deployed to the live URL
3. **Verify live** — run the actual check (curl headers, grep code, npm audit) and confirm it passes
4. **Post evidence** — add a comment with verification output before closing

## Required Comment Format

```
Fix deployed. Verification:
$ curl -sI https://mysite.vercel.app | grep -i "strict-transport"
strict-transport-security: max-age=63072000; includeSubDomains; preload ✅
Commit: abc1234
```

**If you close without evidence, a GitHub Action will auto-reopen the issue and flag you.** Do not close until the live check passes.
