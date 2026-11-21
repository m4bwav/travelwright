# Changelog: travelwright

## 0.2.0 (2026-11-20)
- Public release: README for new users (install, quick start, privacy), banner, marketplace.json for `/plugin marketplace add m4bwav/travelwright`, plugin metadata.
- History restarted at one root commit so no private test term from the early private history ships.

## 0.1.3 (2026-11-20)
- tw.py extract and render create the output folder (found in eval A1 run 3).
- Evals complete: A1 runs 2-3 PASS, no-skill baseline recorded, 5/5 triggers and 5/5 decoys route correctly.

## 0.1.2 (2026-11-20)
- UAE controlled-medicine rules verified (R-20261120-3): e-approval before travel or declare at arrival with prescription and medical report.
- Checklist and SKILL now flag amphetamine medicines to Japan as 'do not carry' and name the UAE permit route; new unit test.

## 0.1.1 (2026-11-20)
- First research refresh (R-20261120-2): Uber Car Seat is now a convertible seat (rear-facing possible), NYC taxi car-seat exemption confirmed, Japan amphetamine ban confirmed.

## 0.1.0 (2026-11-20)
- New skill: intake from email, Drive and the family tree, then a dated checklist.
- tw.py: `extract` (flights, stays, cars, rides from saved email JSON to trip.json), `events` (birthdays and US holidays inside the trip), `render` (checklist markdown).
- Evergreen layer: RESEARCH seed (car seats, TSA, cannabis and medicine rules, rideshare against rental, weather), LEARNINGS seeded with 10 lessons, TESTS and evals with a fixture email set.
