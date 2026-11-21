# Changelog: travelwright

## 0.4.1 (2026-11-20)
- render shows the passport and controlled-medicine lines only for trips abroad (any flight code outside a list of large US airports, no flights, or `"abroad": true` in trip.json). The first real trip, a domestic one, printed them.

## 0.4.0 (2026-11-20)
- First run on real saved Gmail (2 bookings, 5 items). Fixed: stacked airline layouts (code, city, time, then the flight number alone on a line) gave wrong origin and destination; a hotel mail advertising "Car rental" was read as a car; stay dates written as a range ("15 Oct 2026 - 19 Oct 2026") and "Check in" with a space; addresses split over lines with map links between; 11-digit phone numbers; "is confirmed" trimmed from the stay name. Synthetic regression fixture evals/fixtures/emails-stacked.json and 3 tests.

## 0.3.1 (2026-11-20)
- UAE amphetamine medicines settled (R-20261120-5): Schedule II on the official list, allowed for the stay or one month at most with prescription and attested medical report; checklist line and test updated.

## 0.3.0 (2026-11-20)
- Documents and fees (R-20261120-4): checklist lines for REAL ID, the $45 TSA ConfirmID fee per adult without one, child ID rules and passport validity; SKILL step 5. Points and award booking ruled out of scope.
- UAE amphetamine salts: list still unreachable; plan now says get e-approval rather than declare at arrival.

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
