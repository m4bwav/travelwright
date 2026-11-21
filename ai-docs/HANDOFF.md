# HANDOFF: travelwright

State 2026-11-20: v0.3.0 released (PR #2: REAL ID, ConfirmID, passports; points out of scope) and installed as travelwright@mark-local. Repo is PUBLIC: run the leak test before every push.

- Public repo history restarts at one root commit (e6d6eaa). The old private history (PRs #1-#7, tags v0.1.0-v0.1.3, a medicine name from the leak list in PR #2's diff) lives in PRIVATE m4bwav/travelwright-private-archive; never make that public. Local clone has it as remote `archive`.
- Gate tests on exit code and last line OK; never pipe into tail/head before a commit.
- Waits on Mark: one click to create the wiki: save any page at https://github.com/m4bwav/travelwright/wiki/_new (browser tool was not connected). Then push ../travelwright.wiki (see ai-docs/notes/2026-11-20-github-wiki.md).
- Next, in order: (1) push the wiki once it exists and run `live`; (2) per-medicine status of amphetamine salts on the UAE list: MOHAP PDF (mohap.gov.ae/Handlers/DownloadPDF.ashx?id=29858) reset the connection from here and u.ae gave 404; try fetchwright or Chrome; (3) on a real booked trip, run `tw.py extract` on real saved Gmail output and fix the parsers (fixture-tested only).
- Continue prompt: [plugin-backlog/ai-docs/plans/2026-11-20-travelwright-continue-prompt.md](../../plugin-backlog/ai-docs/plans/2026-11-20-travelwright-continue-prompt.md)
