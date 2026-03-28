---
command: /qa
purpose: Run repo-standard quality review before approval.
inputs:
  - changed files
  - lane scope
  - relevant source-of-truth docs
outputs:
  - verdict
  - blockers
  - warnings
  - required follow-ups
guardrails:
  - Preserve existing misao-delivery QA culture; this document standardizes the contract only.
  - Review both editorial and implementation risk.
---

# /qa

Minimum review contract for `misao-delivery`:

1. Scope matches the planned lane
2. No direct publish path was introduced
3. Medical advertising or overclaim language is absent
4. UI remains calm, credible, and non-AI-looking
5. `pages/` updates include status workflow consideration
6. `news` sections include `clinic` taxQuery where required
7. Desktop and mobile behavior has been considered

Output format:
- Verdict: `pass` | `pass-with-warnings` | `block`
- Blockers: flat list with file references
- Warnings: flat list with file references
- Recommended next action
