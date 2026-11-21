---
name: travelwright
description: "Plan a family trip from what is already written down: read bookings in email first (flights, hotel, car, rides, forwarded confirmations), hosts' addresses in Drive, people's needs in the family tree, then write a dated checklist (today, carry-on, clothes, per person, logistics) with local facts sourced and unverified lines flagged. tw.py extract, events, render. Use on 'help me pack for our trip', 'plan our trip to X', 'what do we need for the flight', 'make a packing list for the family', 'are we ready for Thanksgiving travel'. Not for booking or price shopping alone, a single weather question, or general research about a place."
---

# Travelwright

A trip plan built from the bookings and family facts the agent can already reach, not from questions the user has answered before.

## Step 0

`TW` means `python "<this folder>/scripts/tw.py"` (Python 3.9+, stdlib, prints JSON). Private notes and the leak-term list live in `TRAVELWRIGHT_HOME` (default `~/.travelwright`). The checklist goes in the user's trips folder (ask once, then record it in the home's `config.json`), never in this repository.

## Order of work

1. **Bookings first, plan second.** The city the user names may not be where they sleep. Before writing anything, search email for the bookings and read where the stay actually is. Gmail query that works: `(hotel OR reservation OR booking OR confirmation OR airbnb OR flight) (<city> OR <state> OR <airport codes>) newer_than:120d`. Check forwarded mail: one partner often books and forwards to the other.
2. **Save, then extract.** Write the matching messages to a JSON file in the scratchpad and run `TW extract <file> --people <family people dir> -o trip.json`. Long flight emails (80K+ characters) go through the script, never read whole. Then open each item's source email and set `verified: true` only for fields you checked.
3. **Hosts and places.** Hosts' addresses: Drive (an address list sheet) or the family tree. Work out the real distances between stay, hosts and the places named.
4. **People.** For each traveller read their family tree page: age at travel, medicines (and which are school-only), diet, sensory needs, car seat by age and the destination state's law. Abroad, flag controlled medicines as 'do not carry' where banned (amphetamines to Japan) and name the permit route where one exists (UAE e-approval or declare at arrival); see RESEARCH.
5. **Dates.** `TW events` lists birthdays and US holidays inside the trip; plan for each.
6. **Render and finish.** `TW render trip.json --people <dir> -o <trips folder>/<date>-<place>/packing-plan.md`, then fill in the per-person and local sections by hand.

## Rules

1. **Source every local fact** (law, store, shuttle, train time) with a link and the date checked; mark the rest unverified. Laws and rules: [RESEARCH.md](RESEARCH.md).
2. **No fake forecasts.** Beyond about a week out, say no forecast exists yet and point to weather.gov; give typical weather as typical.
3. **Show the arithmetic** for cost comparisons (rideshare against rental: rides a day × days × fare, plus airport legs; rental: days × rate + taxes + parking + car seats), and recompute it when the user gives a new fact.
4. **User corrections win.** Record them in the trip file at once (already paid, don't pack X) and do not ask again.
5. **Privacy.** Family names, medicines, addresses and confirmations stay in the trips folder and the home. Never write them in this plugin's files.

## Maintenance

Evergreen unit: [evergreen.json](evergreen.json), [RESEARCH.md](RESEARCH.md), [LEARNINGS.md](LEARNINGS.md), [CHANGELOG.md](CHANGELOG.md), [TESTS.md](TESTS.md). trip.json fields: [references/trip-schema.md](references/trip-schema.md). Refresh with evergreen-refresh when due. Record lessons with evergreen-learn; anything about the user's own family goes in the home, not here.
