---
command: /ship-check
purpose: Confirm approval readiness and boundary safety before human approval flow.
inputs:
  - qa result
  - changed files
  - approval path
outputs:
  - readiness verdict
  - approval blockers
  - ship notes
guardrails:
  - Do not publish directly.
  - Keep Slack and existing human approval flow outside the OS.
---

# /ship-check

Run this after `/qa` passes or after warnings are accepted.

Checklist:
1. Changed files stay inside intended scope
2. Human approval path is still intact
3. No publish action or hidden automation was added
4. `project-memory/` update candidates are captured
5. `pages/` changes note `generate-status-xlsx.py` if relevant

Output format:
- Verdict: `ready-for-approval` | `needs-fix`
- Boundary notes
- Remaining operator actions
