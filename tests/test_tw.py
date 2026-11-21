import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "travelwright")
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import tw  # noqa: E402

FIX = os.path.join(SKILL, "evals", "fixtures")
EMAILS = os.path.join(FIX, "emails.json")
PEOPLE = os.path.join(FIX, "people")


class Extract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trip = tw.extract([EMAILS])
        cls.items = cls.trip["items"]

    def test_kinds_and_skip(self):
        self.assertEqual([i["kind"] for i in self.items], ["flight", "flight", "stay", "ride"])
        self.assertEqual(len(self.trip["skipped"]), 1)  # the deals newsletter

    def test_flight_legs_take_preceding_date(self):
        f1, f2 = self.items[0], self.items[1]
        self.assertEqual((f1["flight"], f1["date"], f1["from"], f1["to"]), ("UA 1234", "2026-04-10", "AUS", "DEN"))
        self.assertEqual((f2["flight"], f2["date"], f2["from"], f2["to"]), ("UA 987", "2026-04-12", "DEN", "AUS"))
        self.assertEqual(f1["confirmation"], "QWERTY")

    def test_stay_from_forwarded_email(self):
        s = self.items[2]
        self.assertEqual(s["name"], "Pinecrest Suites Denver Airport")
        self.assertEqual((s["check_in"], s["check_out"]), ("2026-04-10", "2026-04-12"))
        self.assertEqual(s["confirmation"], "55512345")
        self.assertIn("Denver CO 80249", s["address"])

    def test_ride_mentioning_suites_is_not_a_stay(self):
        r = self.items[3]
        self.assertEqual(r["kind"], "ride")
        self.assertTrue(r["paid"])

    def test_everything_unverified(self):
        self.assertTrue(all(i["verified"] is False for i in self.items))

    def test_trip_window(self):
        self.assertEqual(self.trip["trip"], {"start": "2026-04-10", "end": "2026-04-12"})


class ExtractStacked(unittest.TestCase):
    """Real-mail layouts (synthetic values): stacked airline legs, IHG-style stay with a car ad."""
    @classmethod
    def setUpClass(cls):
        cls.trip = tw.extract([os.path.join(FIX, "emails-stacked.json")])
        cls.items = cls.trip["items"]

    def test_kinds(self):
        self.assertEqual([i["kind"] for i in self.items], ["flight"] * 3 + ["stay"])

    def test_stacked_legs(self):
        got = [(i["flight"], i["date"], i["from"], i["to"], i["depart"], i["arrive"]) for i in self.items[:3]]
        self.assertEqual(got, [
            ("AA 2201", "2026-10-15", "SAT", "DFW", "6:10 AM", "7:15 AM"),
            ("AA 2302", "2026-10-15", "DFW", "BOS", "8:40 AM", "1:05 PM"),
            ("AA 2403", "2026-10-19", "BOS", "SAT", "5:20 PM", "9:35 PM")])
        self.assertEqual(self.items[0]["confirmation"], "QZPLMK")

    def test_stay_not_car(self):
        s = self.items[3]
        self.assertEqual(s["name"], "Example Inn & Suites Riverside - Millbrook North")
        self.assertEqual((s["check_in"], s["check_out"]), ("2026-10-15", "2026-10-19"))
        self.assertEqual((s["check_in_time"], s["check_out_time"]), ("3:00 pm", "11:00 am"))
        self.assertEqual(s["address"], "123 Sample Mill Road Riverside MA 01999 United States")
        self.assertEqual(s["phone"], "15555550123")
        self.assertEqual(s["confirmation"], "10203040")


class Dates(unittest.TestCase):
    def test_parse_forms(self):
        self.assertEqual(tw.parse_date("Saturday, November 21", 2026), "2026-11-21")
        self.assertEqual(tw.parse_date("11/27/26"), "2026-11-27")
        self.assertEqual(tw.parse_date("21 Nov 2026"), "2026-11-21")
        self.assertIsNone(tw.parse_date("Nov 31", 2026))

    def test_thanksgiving(self):
        h = tw.us_holidays(2026)
        self.assertEqual(h[tw.dt.date(2026, 11, 26)], "Thanksgiving")
        self.assertEqual(h[tw.dt.date(2026, 11, 27)], "Black Friday")

    def test_events_birthday_and_unknown(self):
        ev = tw.events({"trip": {"start": "2026-04-10", "end": "2026-04-12"}}, PEOPLE)
        self.assertEqual(ev, [{"date": "2026-04-11", "event": "Alex Sample's birthday (turns 8)", "kind": "birthday"}])

    def test_events_holiday(self):
        ev = tw.events({"trip": {"start": "2026-11-21", "end": "2026-11-27"}}, None)
        self.assertEqual([e["event"] for e in ev], ["Thanksgiving", "Black Friday"])


class Render(unittest.TestCase):
    def test_checklist(self):
        md = tw.render(tw.extract([EMAILS]), PEOPLE, today="2026-04-08")
        self.assertIn("## Today (Wed Apr 8)", md)
        self.assertIn("Alex Sample's birthday (turns 8)", md)
        self.assertIn("(unverified)", md)
        self.assertNotIn("Late arrival", md)  # 9:45 PM is the return leg, not the check-in day

    def test_abroad_controlled_medicine_line(self):
        md = tw.render(tw.extract([EMAILS]), PEOPLE, today="2026-04-08")
        self.assertIn("Japan: do not carry amphetamine", md)
        self.assertIn("UAE:", md)
        self.assertIn("one month's supply", md)

    def test_id_and_passport_lines(self):
        md = tw.render(tw.extract([EMAILS]), PEOPLE, today="2026-04-08")
        self.assertIn("ConfirmID costs $45", md)
        self.assertIn("Children under 18 with an adult need no ID", md)
        self.assertIn("6 months left", md)

    def test_late_arrival_on_check_in_day(self):
        trip = {"trip": {"start": "2026-11-21", "end": "2026-11-27"}, "items": [
            {"kind": "flight", "airline": "X", "flight": "AA 1", "date": "2026-11-21", "arrive": "11:44 PM", "verified": False},
            {"kind": "stay", "name": "H", "check_in": "2026-11-21", "verified": False}]}
        self.assertIn("Late arrival", tw.render(trip, today="2026-11-20"))

    def test_cli_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            t = os.path.join(d, "trip.json")
            out = os.path.join(d, "new-trip-dir", "checklist.md")  # render makes the folder
            py = [sys.executable, os.path.join(SKILL, "scripts", "tw.py")]
            r = subprocess.run(py + ["extract", EMAILS, "--people", PEOPLE, "-o", t], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(json.loads(r.stdout)["items"], 4)
            r = subprocess.run(py + ["render", t, "-o", out, "--today", "2026-04-08"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            with open(out, encoding="utf-8") as f:
                self.assertIn("# Trip checklist", f.read())


if __name__ == "__main__":
    unittest.main()
