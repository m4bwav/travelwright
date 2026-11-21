# HANDOFF: travelwright

State 2026-11-20: v0.1.3 released (PR #6: eval suite complete, tw.py makes output folders), installed as travelwright@mark-local.

- Gate tests with `tail -1 | grep -qx OK`, never `| tail && ...` (masked a red leak test once).
- Done: skill, tw.py extract/events/render, 15 unit tests + leak test (terms in ~/.travelwright/leak-terms.txt), A1 PASS runs 1-3, no-skill baseline recorded, triggers 5/5 and decoys 5/5 (TESTS.md).
- Next, in order: (1) scope from the backlog still open: documents (passports, REAL ID), points and fees; (2) open research: per-medicine status of amphetamine salts on the UAE list; (3) when a real trip is booked: try `tw.py extract` on real saved Gmail connector output from the next trip and fix the parsers it trips on (only fixture-tested so far).
- Waits on Mark: nothing.
- Continue prompt: [plugin-backlog/ai-docs/plans/2026-11-20-travelwright-continue-prompt.md](../../plugin-backlog/ai-docs/plans/2026-11-20-travelwright-continue-prompt.md)
