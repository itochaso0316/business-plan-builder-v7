---
command: /intake
purpose: Normalize an incoming request before build work starts.
inputs:
  - user request
  - task id
  - target files or directories
outputs:
  - request summary
  - scope and non-scope
  - risk flags
  - plan-needed decision
guardrails:
  - Read CLAUDE.md, PARALLEL_SPRINT.md, and project-memory/current-state.md first.
  - If theme and pages overlap, escalate to lane planning before implementation.
  - Keep scope narrow and identify acceptance criteria early.
---

# /intake

Use this command at the start of a task to produce:

1. Request summary
2. Target area
3. Dependency and lane risk
4. Whether plan/lane split is required
5. Acceptance criteria
6. QA and ship-check considerations

For `misao-delivery`, always call out:
- medical advertising risk
- AI-looking UI risk
- whether `pages/` status workflow is affected
- whether `news` Query Loop / `clinic` taxQuery rules apply
