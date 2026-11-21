# HANDOFF: travelwright

State 2026-11-20: v0.2.0 is the first PUBLIC release (https://github.com/m4bwav/travelwright/releases/tag/v0.2.0), installed as travelwright@mark-local.

- Public repo history restarts at one root commit (e6d6eaa). The old private history (PRs #1-#7, tags v0.1.0-v0.1.3, a medicine name from the leak list in PR #2's diff) lives in PRIVATE m4bwav/travelwright-private-archive; never make that public. Local clone has it as remote `archive`.
- Gate tests on exit code and last line OK; never pipe into tail/head before a commit.
- Waits on Mark: one click to create the wiki: save any page at https://github.com/m4bwav/travelwright/wiki/_new (browser tool was not connected). Then push ../travelwright.wiki (see ai-docs/notes/2026-11-20-github-wiki.md).
- Next, in order: (1) push the wiki once it exists and run `live`; (2) scope still open: documents (passports, REAL ID), points and fees; (3) per-medicine status of amphetamine salts on the UAE list; (4) on a real booked trip, run `tw.py extract` on real saved Gmail output and fix the parsers (fixture-tested only).
- Continue prompt: [plugin-backlog/ai-docs/plans/2026-11-20-travelwright-continue-prompt.md](../../plugin-backlog/ai-docs/plans/2026-11-20-travelwright-continue-prompt.md)
