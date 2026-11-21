# travelwright

![travelwright banner](.github/images/banner.jpg)

A family trip plan built from what is already written down, not from a questionnaire. travelwright has your AI agent read the bookings in your email first (flights, hotel, rental car, rides, the confirmations your partner forwarded), the hosts' addresses in your Drive and each traveller's needs in your family notes. Then it writes a dated checklist: what to do today, carry-on, clothes, a section per person, and logistics.

Local facts in the checklist (car-seat laws, airport rides, store hours) come with a link and the date they were checked. Anything it could not check is marked unverified. Forecasts more than a week out are not made up.

## What it catches

- The hotel is not in the city you named. It reads where you actually sleep before planning around it.
- Birthdays and US holidays that fall inside the trip.
- Car seats by age and by the destination state's law, and where a rideshare or taxi can or cannot take a young child.
- Controlled medicines abroad: amphetamine medicines are banned in Japan, and the UAE needs a permit or a declaration at arrival.
- Rental car against rideshare, with the arithmetic shown, redone when you correct a fact.

## Install

As a Claude Code plugin:

    /plugin marketplace add m4bwav/travelwright
    /plugin install travelwright@travelwright

As a plain skill for any agent that reads Agent Skills (Copilot, Codex, Cursor and others), clone the repository and link `skills/travelwright` into the agent's skills folder.

The agent needs read access to your mail (the Gmail connector in Claude, for example) to find bookings. Drive and family notes are optional; without them it asks about each traveller once.

## Quick start

Ask your agent:

- "Help me pack for our trip to Denver next week."
- "Are we ready for Thanksgiving travel?"
- "What do the kids need for the flight?"

Behind the skill is `tw.py`, standard-library Python 3.9+, which you can also run yourself:

```
python skills/travelwright/scripts/tw.py extract emails.json --people <people dir> -o trip.json
python skills/travelwright/scripts/tw.py events trip.json --people <people dir>
python skills/travelwright/scripts/tw.py render trip.json --people <people dir> -o packing-plan.md
```

`extract` pulls flights, stays, rental cars and rides out of saved email JSON (Gmail connector output, raw Gmail API messages, or plain `{subject, from, date, body}`). `events` lists birthdays and US holidays inside the trip. `render` writes the checklist. Fields: [trip-schema.md](skills/travelwright/references/trip-schema.md).

## Privacy

Your family's names, medicines, addresses and booking numbers stay on your machine: in the trips folder you choose and in `~/.travelwright` (set `TRAVELWRIGHT_HOME` to move it). The skill never writes them into its own files, and nothing is sent anywhere except through the connectors your agent already uses. A test checks the repository against a private list of terms you keep in `~/.travelwright/leak-terms.txt`, so your details cannot slip into a contribution.

The email parsers are tested on made-up fixtures. Real confirmation emails vary; if one is misread, open an issue with the layout described (never the email itself).

## Tests

    TRAVELWRIGHT_HOME=~/.travelwright python -m unittest discover -s tests

## Licence

MIT. See [LICENSE](LICENSE). Security reports: [SECURITY.md](SECURITY.md).
