# trip.json

Written by `tw.py extract`. Every item starts `verified: false`; the agent sets it true only after it has checked the fields against the source email.

```json
{
  "trip": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
  "items": [
    {"kind": "flight", "airline": "", "flight": "UA 1234", "date": "", "from": "AUS", "to": "DEN",
     "depart": "7:05 AM", "arrive": "8:40 AM", "confirmation": "", "source": "", "verified": false},
    {"kind": "stay", "name": "", "check_in": "", "check_out": "", "check_in_time": "", "check_out_time": "",
     "address": "", "phone": "", "confirmation": "", "source": "", "verified": false},
    {"kind": "car", "company": "", "pickup": "", "dropoff": "", "confirmation": "", "source": "", "verified": false},
    {"kind": "ride", "company": "", "date": "", "paid": true, "confirmation": "", "source": "", "verified": false}
  ],
  "skipped": ["file#index subject of each message that held no booking"],
  "events": [{"date": "", "event": "Thanksgiving", "kind": "holiday|birthday"}]
}
```

- `source` is `<file>#<index> <subject>`, so the agent can reopen the message.
- A missing field is `null`; `render` lists them under Open questions.
- Email input: one message or a list; each message is the Gmail connector's output, the raw Gmail API shape (`payload`), or `{subject, from, date, body}`. HTML is stripped.
- Birthdays come from `- Birthdate: YYYY-MM-DD` (or `Mon D`) lines in the people folder's markdown pages; `?` is skipped.

Optional `"abroad": true|false` at the top level overrides the guess `render` makes (since 0.4.1): a trip counts as abroad when any flight code is outside the built-in list of large US airports, or when it has no flights. Domestic trips skip the passport and controlled-medicine lines. Set it by hand for a small US airport or a drive across a border.
