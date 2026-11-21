# Learnings: travelwright

Lessons that save time or prevent a wrong plan. Owner-specific facts go in `TRAVELWRIGHT_HOME`, not here.

- L-001 `bookings-before-plan` (2026-11-20): the user named a city, but the hotel in email was an hour away near the hosts. A plan written from the city name had to be redone. Read the bookings first.
- L-002 `gmail-booking-query` (2026-11-20): `(hotel OR reservation OR booking OR confirmation OR airbnb OR flight) (<city> OR <state> OR <airport codes>) newer_than:120d` found every booking. Confirmations were forwarded between partners, so search the forwarded copies too.
- L-003 `long-flight-emails` (2026-11-20): airline emails run 80K+ characters. Pull fields with tw.py extract (or jq/python with `PYTHONIOENCODING=utf-8` on Windows) instead of reading them whole.
- L-004 `family-facts-on-disk` (2026-11-20): ages, birthdays, medicines, sensory and diet needs were already on the family tree pages. Read them before asking. A birthday and a holiday both fell inside the trip.
- L-005 `school-only-meds` (2026-11-20): some medicines are taken only on school days; ask once or check the page, and leave them out of the packing list.
- L-006 `already-paid` (2026-11-20): the user had already paid for the airport ride. Check ride and transfer receipts before telling them to book one.
- L-007 `car-seat-age-at-travel` (2026-11-20): car-seat rules depend on the child's age on the travel date and on the destination state's law.
- L-008 `no-forecast-yet` (2026-11-20): five days out no real forecast turned up in search. Say so, give typical weather, point to weather.gov.
- L-009 `recompute-costs` (2026-11-20): the user wanted Uber against rental recomputed each time they gave a new fact. Show the arithmetic.
- L-010 `ride-with-hotel-name` (2026-11-20, build): a ride receipt naming a "Suites" hotel was read as a stay. Classify rides before stays unless the text has check-in or check-out.
