---
command: /memory-sync
purpose: Merge reviewed session drafts into project-memory sources of truth.
inputs:
  - draft files under project-memory/agent-os/session-drafts/
  - reviewed decisions
outputs:
  - synced memory targets
  - skipped targets
  - follow-up notes
guardrails:
  - Review draft content before applying.
  - Do not overwrite unrelated in-progress edits.
  - Prefer append/update in the smallest safe area.
---

# /memory-sync

Phase 1 behavior:

1. Read session drafts from `project-memory/agent-os/session-drafts/`
2. Compare each draft with the matching source-of-truth file
3. Apply only reviewed sections
4. Preserve any unrelated dirty worktree changes
5. Record what was synced and what was deferred

Default targets:
- `project-memory/current-state.md`
- `project-memory/next-actions.md`
- `project-memory/decision-log.md`
- `project-memory/open-questions.md`
