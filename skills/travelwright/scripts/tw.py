#!/usr/bin/env python3
"""travelwright tw.py: booking emails to trip.json, trip.json to a dated checklist.

Standard library only (Python 3.9+). Prints JSON unless told to write a file.

  tw.py extract <email.json>... [-o trip.json]   flights, hotels, cars, rides from saved emails
  tw.py events  <trip.json> --people <dir>       birthdays and US holidays inside the trip dates
  tw.py render  <trip.json> [--people <dir>] [-o checklist.md] [--today YYYY-MM-DD]

An email JSON file is either one message or a list of them. Each message may be the Gmail
connector's get_message output or a plain {"subject", "from", "date", "body"} object; HTML
bodies are stripped to text. Nothing leaves the machine.
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import sys

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
AIRLINES = {"AA": "American", "UA": "United", "DL": "Delta", "WN": "Southwest", "B6": "JetBlue",
            "AS": "Alaska", "NK": "Spirit", "F9": "Frontier", "HA": "Hawaiian", "SY": "Sun Country",
            "AC": "Air Canada", "BA": "British Airways", "LH": "Lufthansa", "AF": "Air France"}
AIRLINE_NAMES = {v.lower(): k for k, v in AIRLINES.items()}
HOTEL_WORDS = re.compile(r"\b(hotel|inn|suites|resort|lodge|airbnb|vrbo|check-?in|check-?out)\b", re.I)
CAR_WORDS = re.compile(r"\b(rental car|car rental|pick-?up location|hertz|avis|enterprise|national|budget|alamo|sixt|thrifty|dollar rent)\b", re.I)
RIDE_WORDS = re.compile(r"\b(uber|lyft|car service|shuttle|limo|chauffeur|blacklane|carmel)\b", re.I)
FLIGHT_WORDS = re.compile(r"\b(flight|depart|boarding|itinerary|seat|terminal|gate)\b", re.I)
CONF = re.compile(r"(?i:confirmation|record locator|booking|reservation|conf\.?)\s*(?i:code|number|no\.?|id|#)?\s*[:#]?\s*([A-Z0-9]{5,12})\b")
FLIGHT_NO = re.compile(r"\b(" + "|".join(AIRLINES) + r")\s?(\d{1,4})\b")
IATA = re.compile(r"\b([A-Z]{3})\b")
NOT_IATA = {"THE", "AND", "FOR", "YOU", "ARE", "NOT", "ALL", "PDT", "PST", "EST", "EDT", "CST", "CDT",
            "MST", "MDT", "USD", "PM", "AM", "SAT", "SUN", "MON", "TUE", "WED", "THU", "FRI", "JAN",
            "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "TSA", "FAQ",
            "WIFI", "APP", "NEW", "VIA", "PRE", "CHK", "ONE", "TWO", "QTY", "TAX", "FEE", "PNR"}
TIME = re.compile(r"\b(\d{1,2}:\d{2}\s?(?:[AaPp]\.?[Mm]\.?)?)")
PHONE = re.compile(r"\(?\b\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b")
ADDRESS = re.compile(r"\b\d{1,6}\s+[A-Z0-9][\w.' -]{2,40}?\s(?:St|Street|Rd|Road|Ave|Avenue|Blvd|Boulevard|Dr|Drive|Ln|Lane|Way|Pl|Place|Pkwy|Parkway|Hwy|Highway|Ct|Court)\b\.?[^\n]{0,60}?\b[A-Z]{2}\s\d{5}\b")


def strip_html(s):
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</(p|div|tr|td|li|h\d)>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t ]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def message_parts(m):
    """Return subject, sender, date, body text for the shapes the Gmail connector and users give."""
    if "payload" in m:  # raw Gmail API shape
        hdr = {h["name"].lower(): h["value"] for h in m["payload"].get("headers", [])}
        body = m.get("snippet", "")
        def walk(p):
            out = []
            data = p.get("body", {}).get("data")
            if data:
                import base64
                out.append(base64.urlsafe_b64decode(data + "==").decode("utf-8", "replace"))
            for c in p.get("parts", []) or []:
                out += walk(c)
            return out
        body = "\n".join(walk(m["payload"])) or body
        return hdr.get("subject", ""), hdr.get("from", ""), hdr.get("date", ""), body
    get = lambda *ks: next((m[k] for k in ks if isinstance(m.get(k), str) and m.get(k)), "")
    body = get("body", "text", "plainText", "plain_text", "content", "htmlBody", "html", "snippet")
    return get("subject", "Subject"), get("from", "sender", "From"), get("date", "Date", "internalDate"), body


def load_messages(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        for k in ("messages", "results", "items"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
        else:
            data = [data]
    return data


def parse_date(s, year_hint=None):
    """Parse '2026-11-21', 'Nov 21, 2026', 'Saturday, November 21', '11/21/2026'. Return ISO or None."""
    s = s.strip()
    m = re.search(r"\b(20\d\d)-(\d\d)-(\d\d)\b", s)
    if m:
        return "%s-%s-%s" % m.groups()
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(20\d\d|\d\d)\b", s)
    if m:
        mo, d, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        y = y + 2000 if y < 100 else y
        return _iso(y, mo, d)
    m = re.search(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{1,2})(?!\d)(?:st|nd|rd|th)?(?:,?\s+(20\d\d))?", s, re.I)
    if m:
        y = int(m.group(3)) if m.group(3) else year_hint
        return _iso(y, MONTHS[m.group(1).lower()[:3]], int(m.group(2))) if y else None
    m = re.search(r"\b(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?(?:\s+(20\d\d))?", s, re.I)
    if m:
        y = int(m.group(3)) if m.group(3) else year_hint
        return _iso(y, MONTHS[m.group(2).lower()[:3]], int(m.group(1))) if y else None
    return None


def _iso(y, mo, d):
    try:
        return dt.date(y, mo, d).isoformat()
    except ValueError:
        return None


def year_of(datestr):
    m = re.search(r"\b(20\d\d)\b", datestr or "")
    if m:
        return int(m.group(1))
    if (datestr or "").isdigit():  # internalDate in ms
        return dt.datetime.utcfromtimestamp(int(datestr) / 1000).year
    return dt.date.today().year


def dates_in(text, year):
    seen, out = set(), []
    for m in re.finditer(r"(?:\b20\d\d-\d\d-\d\d\b|\b\d{1,2}/\d{1,2}/(?:20)?\d\d\b|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2}(?!\d)(?:st|nd|rd|th)?(?:,?\s+20\d\d)?|\b\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?(?:\s+20\d\d)?)", text, re.I):
        d = parse_date(m.group(0), year)
        if d and d not in seen:
            seen.add(d)
            out.append((m.start(), d))
    return out


def date_near(text, pos, year, window=300):
    before, after = None, None
    for p, d in dates_in(text, year):
        if p <= pos and pos - p <= window:
            before = d
        elif p > pos and after is None:
            after = d
    return before or after


def first(rx, text, group=1):
    m = rx.search(text)
    return m.group(group).strip() if m else None


def labelled(text, *labels, rx=None):
    for lab in labels:
        m = re.search(lab + r"\s*[:\-]?\s*([^\n]{3,80})", text, re.I)
        if m:
            val = m.group(1).strip()
            if rx:
                mm = rx.search(val)
                if mm:
                    return mm.group(0)
                continue
            return val
    return None


def extract_flights(text, year, conf, source):
    legs, seen = [], set()
    for m in FLIGHT_NO.finditer(text):
        key = (m.group(1), m.group(2))
        if key in seen:
            continue
        seen.add(key)
        seg = text[m.start(): m.start() + 260]
        codes = [c for c in IATA.findall(seg) if c not in NOT_IATA and c not in AIRLINES]
        times = TIME.findall(seg)
        legs.append({
            "kind": "flight", "airline": AIRLINES[m.group(1)], "flight": "%s %s" % key,
            "date": date_near(text, m.start(), year),
            "from": codes[0] if codes else None, "to": codes[1] if len(codes) > 1 else None,
            "depart": times[0].strip() if times else None, "arrive": times[1].strip() if len(times) > 1 else None,
            "confirmation": conf, "source": source, "verified": False})
    return legs


def extract_stay(text, year, conf, source, subject):
    cin = labelled(text, r"check-?in(?: date)?", r"arrival(?: date)?", r"arriving")
    cout = labelled(text, r"check-?out(?: date)?", r"departure(?: date)?", r"departing")
    name = None
    for line in [subject] + text.split("\n")[:40]:
        mm = re.search(r"([A-Z][\w&'.-]*(?:\s+[A-Z&][\w&'.-]*){0,7}\s(?:Hotel|Inn|Suites|Resort|Lodge)(?:[\w &'.-]{0,40})?)", line)
        if mm:
            name = re.sub(r"\s+", " ", mm.group(1)).strip(" -")
            break
    tin = re.search(r"check-?in[^\n]{0,40}?(\d{1,2}(?::\d{2})?\s?[AaPp][Mm])", text, re.I)
    tout = re.search(r"check-?out[^\n]{0,40}?(\d{1,2}(?::\d{2})?\s?[AaPp][Mm])", text, re.I)
    return {"kind": "stay", "name": name or (subject[:80] if subject else None),
            "check_in": parse_date(cin, year) if cin else None, "check_out": parse_date(cout, year) if cout else None,
            "check_in_time": tin.group(1) if tin else None, "check_out_time": tout.group(1) if tout else None,
            "address": first(ADDRESS, text, 0), "phone": first(PHONE, text, 0),
            "confirmation": conf, "source": source, "verified": False}


def extract_car(text, year, conf, source):
    pu = labelled(text, r"pick-?up(?: date| time)?")
    do = labelled(text, r"(?:drop-?off|return)(?: date| time)?")
    company = first(re.compile(r"\b(Hertz|Avis|Enterprise|National|Budget|Alamo|Sixt|Thrifty|Dollar)\b"), text)
    return {"kind": "car", "company": company, "pickup": parse_date(pu, year) if pu else None,
            "dropoff": parse_date(do, year) if do else None, "confirmation": conf, "source": source, "verified": False}


def extract_ride(text, year, conf, source):
    when = date_near(text, 0, year, window=10**6)
    company = first(re.compile(r"\b(Uber|Lyft|Blacklane|Carmel|shuttle|car service)\b", re.I), text)
    paid = bool(re.search(r"\b(paid|charged|receipt|total charged|prepaid)\b", text, re.I))
    return {"kind": "ride", "company": company, "date": when, "paid": paid,
            "confirmation": conf, "source": source, "verified": False}


def extract(paths):
    items, skipped = [], []
    for path in paths:
        for i, m in enumerate(load_messages(path)):
            subject, sender, date, body = message_parts(m)
            text = strip_html(body) if "<" in body and ">" in body else body
            whole = subject + "\n" + text
            year = year_of(date)
            conf = first(CONF, whole)
            source = "%s#%d %s" % (os.path.basename(path), i, subject[:60])
            got = []
            if FLIGHT_NO.search(whole) and FLIGHT_WORDS.search(whole):
                got += extract_flights(whole, year, conf, source)
            if not got and CAR_WORDS.search(whole):
                got.append(extract_car(whole, year, conf, source))
            is_stay = re.search(r"check-?in|check-?out", whole, re.I)
            if not got and RIDE_WORDS.search(whole) and not is_stay:
                got.append(extract_ride(whole, year, conf, source))
            if not got and HOTEL_WORDS.search(whole):
                got.append(extract_stay(whole, year, conf, source, subject))
            if got:
                items += got
            else:
                skipped.append(source)
    dates = [d for it in items for d in (it.get("date"), it.get("check_in"), it.get("check_out"),
                                         it.get("pickup"), it.get("dropoff")) if d]
    return {"trip": {"start": min(dates) if dates else None, "end": max(dates) if dates else None},
            "items": items, "skipped": skipped,
            "note": "Every item is unverified until checked against the email; read the source before relying on it."}


# ---- events: birthdays and holidays inside the trip ----

def nth_weekday(y, mo, weekday, n):
    d = dt.date(y, mo, 1)
    d += dt.timedelta(days=(weekday - d.weekday()) % 7)
    if n > 0:
        return d + dt.timedelta(weeks=n - 1)
    last = dt.date(y, mo + 1, 1) - dt.timedelta(days=1) if mo < 12 else dt.date(y, 12, 31)
    return last - dt.timedelta(days=(last.weekday() - weekday) % 7)


def us_holidays(y):
    return {
        dt.date(y, 1, 1): "New Year's Day", nth_weekday(y, 1, 0, 3): "Martin Luther King Jr. Day",
        nth_weekday(y, 2, 0, 3): "Presidents' Day", nth_weekday(y, 5, 0, -1): "Memorial Day",
        dt.date(y, 6, 19): "Juneteenth", dt.date(y, 7, 4): "Independence Day",
        nth_weekday(y, 9, 0, 1): "Labor Day", dt.date(y, 10, 31): "Halloween",
        nth_weekday(y, 11, 3, 4): "Thanksgiving", nth_weekday(y, 11, 3, 4) + dt.timedelta(days=1): "Black Friday",
        dt.date(y, 12, 24): "Christmas Eve", dt.date(y, 12, 25): "Christmas Day", dt.date(y, 12, 31): "New Year's Eve",
    }


def read_birthdays(people_dir):
    out = []
    if not people_dir or not os.path.isdir(people_dir):
        return out
    for fn in sorted(os.listdir(people_dir)):
        if not fn.endswith(".md"):
            continue
        with open(os.path.join(people_dir, fn), "r", encoding="utf-8") as f:
            text = f.read()
        name = (re.search(r"^#\s+(.+)$", text, re.M) or [None, fn[:-3]])[1].strip()
        m = re.search(r"^\s*[-*]?\s*(?:birthdate|birthday|born|dob)\s*:\s*(.+)$", text, re.I | re.M)
        if not m or m.group(1).strip().startswith("?"):
            continue
        raw = m.group(1)
        full = re.search(r"\b(19\d\d|20\d\d)-(\d\d)-(\d\d)\b", raw)
        if full:
            out.append({"name": name, "month": int(full.group(2)), "day": int(full.group(3)), "year": int(full.group(1))})
            continue
        md = re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{1,2})", raw, re.I)
        if md:
            out.append({"name": name, "month": MONTHS[md.group(1).lower()[:3]], "day": int(md.group(2)), "year": None})
    return out


def events(trip, people_dir):
    start, end = trip["trip"].get("start"), trip["trip"].get("end")
    if not (start and end):
        return []
    s, e = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    out = []
    for y in range(s.year, e.year + 1):
        for d, name in us_holidays(y).items():
            if s <= d <= e:
                out.append({"date": d.isoformat(), "event": name, "kind": "holiday"})
        for b in read_birthdays(people_dir):
            try:
                d = dt.date(y, b["month"], b["day"])
            except ValueError:
                continue
            if s <= d <= e:
                age = " (turns %d)" % (y - b["year"]) if b["year"] else ""
                out.append({"date": d.isoformat(), "event": "%s's birthday%s" % (b["name"], age), "kind": "birthday"})
    return sorted(out, key=lambda x: x["date"])


# ---- render ----

def day(iso):
    return dt.date.fromisoformat(iso).strftime("%a %b %d").replace(" 0", " ") if iso else "date unknown"


def render(trip, people_dir=None, today=None):
    today = today or dt.date.today().isoformat()
    t = trip["trip"]
    lines = ["# Trip checklist (%s to %s)" % (day(t.get("start")), day(t.get("end"))), "",
             "Built %s from booking emails. Lines marked (unverified) came from text matching; check them against the email." % today, ""]
    ev = trip.get("events") or events(trip, people_dir)
    if ev:
        lines += ["## Inside the trip dates", ""] + ["- **%s**: %s" % (day(e["date"]), e["event"]) for e in ev] + [""]
    lines += ["## Logistics (from email)", ""]
    for it in trip["items"]:
        flag = "" if it.get("verified") else " (unverified)"
        k = it["kind"]
        if k == "flight":
            lines.append("- %s: %s %s %s to %s, departs %s, arrives %s; confirmation %s%s" % (
                day(it.get("date")), it.get("airline"), it.get("flight"), it.get("from") or "?", it.get("to") or "?",
                it.get("depart") or "?", it.get("arrive") or "?", it.get("confirmation") or "?", flag))
        elif k == "stay":
            lines.append("- Stay: %s, %s to %s (check-in %s, check-out %s); %s; phone %s; confirmation %s%s" % (
                it.get("name") or "?", day(it.get("check_in")), day(it.get("check_out")), it.get("check_in_time") or "?",
                it.get("check_out_time") or "?", it.get("address") or "address not found", it.get("phone") or "?",
                it.get("confirmation") or "?", flag))
        elif k == "car":
            lines.append("- Car: %s, pick up %s, return %s; confirmation %s%s" % (
                it.get("company") or "?", day(it.get("pickup")), day(it.get("dropoff")), it.get("confirmation") or "?", flag))
        elif k == "ride":
            lines.append("- Ride: %s on %s, %s%s" % (it.get("company") or "?", day(it.get("date")),
                                                     "already paid" if it.get("paid") else "payment not seen", flag))
    first_flight = next((i for i in trip["items"] if i["kind"] == "flight" and i.get("date")), None)
    lines += ["", "## Today (%s)" % day(today), ""]
    if first_flight:
        lines.append("- [ ] Check in online 24 hours before %s %s; save boarding passes offline." % (first_flight["flight"], day(first_flight["date"])))
    check_ins = {i.get("check_in") for i in trip["items"] if i["kind"] == "stay"}
    late = [i for i in trip["items"] if i["kind"] == "flight" and i.get("date") in check_ins
            and (i.get("arrive") or "").upper().replace(".", "").endswith("PM")
            and re.match(r"(1[01]|9):", i.get("arrive") or "")]
    if late:
        lines.append("- [ ] Late arrival: call the stay and ask them to hold the room (a no-show can cancel the rest).")
    for e in ev:
        if e["kind"] == "birthday":
            lines.append("- [ ] %s: gift packed or shipped, plan for the day." % e["event"])
    lines += ["- [ ] Count every daily medicine for the trip length plus spares; leave school-only ones home.",
              "- [ ] Flying abroad with controlled medicines (ADHD stimulants, strong painkillers)? Japan: do not carry amphetamine medicines at all, even with a prescription; others need a permit ahead. UAE: get e-approval before the trip or declare at arrival with the prescription and a medical report.",
              "- [ ] Download shows, games and offline maps.", "",
              "## Carry-on", "", "- [ ] IDs, boarding passes, chargers, medicines in original bottles, snacks, a change of clothes per child.", "",
              "## Clothes", "", "- [ ] Check the forecast the morning you leave (weather.gov); say so if no forecast exists yet.", "",
              "## Per person", "", "- [ ] One line per traveller from their FamilyTree page: medicines, diet, sensory needs, car seat by age at travel.", "",
              "## Open questions", ""]
    for it in trip["items"]:
        missing = [k for k, v in it.items() if v is None and k not in ("verified",)]
        if missing:
            lines.append("- %s %s: not found in email: %s" % (it["kind"], it.get("flight") or it.get("name") or it.get("company") or "", ", ".join(missing)))
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="tw.py", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("extract"); a.add_argument("emails", nargs="+"); a.add_argument("-o", "--out")
    a.add_argument("--people", help="FamilyTree people folder: adds events to trip.json")
    b = sub.add_parser("events"); b.add_argument("trip"); b.add_argument("--people", required=True)
    c = sub.add_parser("render"); c.add_argument("trip"); c.add_argument("--people"); c.add_argument("-o", "--out")
    c.add_argument("--today")
    args = ap.parse_args(argv)
    if args.cmd == "extract":
        trip = extract(args.emails)
        if args.people:
            trip["events"] = events(trip, args.people)
        out = json.dumps(trip, indent=2, ensure_ascii=False)
        if args.out:
            os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
            with open(args.out, "w", encoding="utf-8", newline="\n") as f:
                f.write(out + "\n")
            print(json.dumps({"wrote": args.out, "items": len(trip["items"]), "skipped": len(trip["skipped"]), "trip": trip["trip"]}))
        else:
            print(out)
    elif args.cmd == "events":
        with open(args.trip, encoding="utf-8") as f:
            print(json.dumps(events(json.load(f), args.people), indent=2, ensure_ascii=False))
    else:
        with open(args.trip, encoding="utf-8") as f:
            md = render(json.load(f), args.people, args.today)
        if args.out:
            os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
            with open(args.out, "w", encoding="utf-8", newline="\n") as f:
                f.write(md)
            print(json.dumps({"wrote": args.out}))
        else:
            print(md, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
