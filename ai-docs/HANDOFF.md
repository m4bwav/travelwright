# HANDOFF: travelwright

State 2026-11-20: v0.3.1 released (PR #3: UAE amphetamine medicines settled, Schedule II, one month max with prescription and attested report) and installed as travelwright@mark-local. Repo is PUBLIC: run the leak test before every push.

- Public repo history restarts at one root commit (e6d6eaa). The old private history (PRs #1-#7, tags v0.1.0-v0.1.3, a medicine name from the leak list in PR #2's diff) lives in PRIVATE m4bwav/travelwright-private-archive; never make that public. Local clone has it as remote `archive`.
- Gate tests on exit code and last line OK; never pipe into tail/head before a commit. Leak list includes common medicine names: say 'ADHD stimulants' in public files.
- Waits on Mark: one click to create the wiki: save any page at https://github.com/m4bwav/travelwright/wiki/_new (browser tool was not connected). Then push ../travelwright.wiki (see ai-docs/notes/2026-11-20-github-wiki.md).
- Next, in order: (1) push the wiki once it exists (check with `git ls-remote https://github.com/m4bwav/travelwright.wiki.git`; still not found 2026-11-20) and run `live`; (2) on a real booked trip, run `tw.py extract` on real saved Gmail output and fix the parsers (fixture-tested only).
- Continue prompt: [plugin-backlog/ai-docs/plans/2026-11-20-travelwright-continue-prompt.md](../../plugin-backlog/ai-docs/plans/2026-11-20-travelwright-continue-prompt.md)
