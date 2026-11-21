# Tests: travelwright

- Unit and leak: `TRAVELWRIGHT_HOME=<private home> python -m unittest discover -s tests` from the repo root. 14 tests (extract, dates, events, render, CLI round trip, leak). The leak test skips with a warning when the variable is unset.
- Evals: [evals/evals.json](evals/evals.json): 5 triggers, 5 decoys, 1 action case on the fixture emails (made-up Denver trip).
  - 2026-11-20, A1 with the skill, run 1 (fresh tester agent): PASS. 4 items (flights 04-10 and 04-12, stay 55512345, paid ride), deals email skipped, birthday named, every line unverified, no late-arrival warning, nothing written in the repo.
  - 2026-11-20, A1 with the skill, run 2: PASS. 4 items, deals email skipped, Apr 11 birthday named, lines unverified, no late-arrival warning, nothing in the repo.
  - 2026-11-20, A1 with the skill, run 3: PASS (with a bug). Same items and birthday; the agent checked each item against its email and set verified true (allowed by the skill). First render failed because tw.py did not create the output folder; fixed in 0.1.3 (extract and render make the folder; CLI round-trip test covers it).
  - 2026-11-20, A1 baseline without the skill: hand-written checklist with the same bookings, birthday and gaps, but no trip.json, no structured events, no tw.py. Verdict: the skill's added value is the structured trip.json and repeatable render; a capable model alone gets the content. Evidence point (trip.json) fails without the skill.
  - 2026-11-20, triggers and decoys (fresh tester, routing judged from the skill list): 5/5 triggers chose travelwright; 5/5 decoys did not (flight price, weather, Brooklyn history: none; nephew's birthday: family-tree; reschedule: schedule-manager).
  - Owed: nothing for this suite; rerun after the first real Gmail extract.
