"""Send days for a sales email sequence, and a mechanical check of a drafted sequence.

The send days per type are EXAMPLE DEFAULTS; the user's own days (--days) and count (--count) always win, and the output
labels the days "example default" or "your value". re_engagement has no example default: the user sets the days.
Event follow up and nurture sequences are not written here (b2b-events-pr-and-launches / event-follow-up-engine).

Usage:
  python sequence_days.py days --type cold_outreach [--days 1,4,9] [--count 3] [--start 2026-10-16 | --first-send 2026-10-19] [--format text|json]
  python sequence_days.py check --file draft.txt [--format text|json]
  python sequence_days.py --help

days: day N means N calendar days after the start (the trigger: the day you plan the sequence, the demo, the proposal);
day 0 is the same day. With --start, a send date on Saturday or Sunday moves to the next working day, and two emails never
share a date (the later one moves to the next working day). With --first-send, the first email goes on that date (moved to the
next working day if it is a weekend, and said so) and the later emails keep the same gaps in days; give --start or --first-send,
not both. Example defaults: cold_outreach 1, 3, 7, 12, 17;
warm_follow_up 0, 3, 7; post_demo 0, 2, 5, 10; proposal_follow_up 1, 3, 7, 12; referral_request 1, 4, 9.
check: emails start at a line "Subject: ..."; for each email the subject words and characters and the body words; problems:
long or short dashes and a hyphen with spaces on both sides used as a dash. A file with 0 emails fails.
Exit code 0 ok, 1 problems found by check, 2 bad input. Standard library only; no network; writes no file.
"""
import datetime as dt, json, re, sys

DEFAULTS = {"cold_outreach": [1, 3, 7, 12, 17], "warm_follow_up": [0, 3, 7], "post_demo": [0, 2, 5, 10],
            "proposal_follow_up": [1, 3, 7, 12], "referral_request": [1, 4, 9], "re_engagement": None}
HANDED_OFF = {"event_follow_up", "nurture"}


class BadInput(Exception):
    pass


def parse(argv, allowed):
    a, i = {}, 0
    while i < len(argv):
        k = argv[i]
        if k not in allowed or i + 1 >= len(argv):
            raise BadInput(f"unknown or incomplete option {k!r}; see the usage at the top of sequence_days.py")
        a[k] = argv[i + 1]; i += 2
    return a


def days_cmd(a):
    t = a.get("--type")
    if t in HANDED_OFF:
        raise BadInput(f"{t} sequences are not written by this skill: use b2b-events-pr-and-launches / event-follow-up-engine")
    if t not in DEFAULTS:
        raise BadInput(f"--type must be one of {', '.join(DEFAULTS)}, got {t!r}")
    count = None
    if "--count" in a:
        if not re.fullmatch(r"\d+", a["--count"].strip()) or int(a["--count"]) < 1:
            raise BadInput(f"--count must be a whole number of 1 or more, got {a['--count']!r}")
        count = int(a["--count"])
    if "--days" in a:
        raw = a["--days"]
        parts = [p.strip() for p in raw.split(",")]
        if not raw.strip() or not all(re.fullmatch(r"-?\d+", p) for p in parts):
            raise BadInput(f"--days must be whole days separated by commas, for example 1,3,7, got {raw!r}")
        days = [int(p) for p in parts]
        if any(d < 0 for d in days):
            raise BadInput(f"--days cannot hold a negative day, got {raw} (the minus sign is kept and refused)")
        if any(b <= a_ for a_, b in zip(days, days[1:])):
            raise BadInput(f"--days must increase from one email to the next, got {raw}")
        if count is not None and count != len(days):
            raise BadInput(f"--count {count} does not match the {len(days)} days given in --days")
        src = "your value"
    else:
        base = DEFAULTS[t]
        if base is None:
            raise BadInput(f"{t} has no example default send days: give --days, for example 1,8,20")
        if count is not None and count > len(base):
            raise BadInput(f"you asked for {count} emails; the example default for {t} has {len(base)} send days: give --days with {count} days")
        days = base[:count] if count else list(base)
        src = "example default"
    out = {"type": t, "days": days, "days_source": src, "count": len(days)}
    if "--start" in a and "--first-send" in a:
        raise BadInput("give --start (the trigger day) or --first-send (the date of the first email), not both")
    for opt in ("--start", "--first-send"):
        if opt not in a:
            continue
        s = a[opt].strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
            raise BadInput(f"{opt} must be a date written YYYY-MM-DD, got {s!r}")
        try:
            given = dt.date.fromisoformat(s)
        except ValueError:
            raise BadInput(f"{opt} {s!r} is not a real calendar date (refused, never rolled over)")
        first_moved_from = None
        if opt == "--first-send":
            first = given
            while first.weekday() >= 5:
                first += dt.timedelta(days=1)
            if first != given:
                first_moved_from = given.isoformat()
            out["first_send"] = first.isoformat()
            start = first - dt.timedelta(days=days[0])
        else:
            start = given
        sends, last = [], None
        for d in days:
            want = start + dt.timedelta(days=d)
            got = want
            while got.weekday() >= 5 or (last is not None and got <= last):
                got += dt.timedelta(days=1)
            moved = want.isoformat() if got != want else None
            if first_moved_from and not sends:
                moved = first_moved_from
            sends.append({"day": d, "date": got.isoformat(), "weekday": got.strftime("%A"), "moved_from": moved})
            last = got
        out["start"] = start.isoformat()
        out["sends"] = sends
    return out


DASHES = [("long dash", re.compile("[\\u2014\\u2015]")), ("short dash", re.compile("[\\u2012\\u2013]")), ("spaced hyphen used as a dash", re.compile(r"(?<=\s)-(?=\s)"))]


def check_cmd(a):
    path = a.get("--file")
    if not path:
        raise BadInput("give the drafted sequence with --file")
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        raise BadInput(f"cannot read {path!r}: {e}")
    emails, cur = [], None
    for line in text.splitlines():
        m = re.match(r"\s*subject\s*:\s*(.*)$", line, re.I)
        if m:
            cur = {"subject": m.group(1).strip(), "body": []}
            emails.append(cur)
        elif cur is not None:
            cur["body"].append(line)
    if not emails:
        raise BadInput("0 emails found: each email must start with a line \"Subject: ...\" (a check that reads 0 items fails)")
    rows, problems = [], []
    for i, e in enumerate(emails, 1):
        body = "\n".join(e["body"])
        rows.append({"email": i, "subject": e["subject"], "subject_words": len(e["subject"].split()), "subject_chars": len(e["subject"]),
                     "body_words": len(body.split())})
        for part, txt in (("subject", e["subject"]), ("body", body)):
            for name, rx in DASHES:
                for _ in rx.finditer(txt):
                    problems.append(f"email {i} {part}: {name}")
    return {"emails": rows, "problems": problems}


def run(argv):
    if argv and (argv[0] in ("--help", "-h") or "--help" in argv):
        return 0, __doc__.strip()
    try:
        if not argv or argv[0] not in ("days", "check"):
            raise BadInput("first word must be days or check; see the usage at the top of sequence_days.py")
        if argv[0] == "days":
            a = parse(argv[1:], {"--type", "--days", "--count", "--start", "--first-send", "--format"}); d = days_cmd(a)
        else:
            a = parse(argv[1:], {"--file", "--format"}); d = check_cmd(a)
    except BadInput as e:
        return 2, f"BAD INPUT: {e}"
    code = 1 if argv[0] == "check" and d["problems"] else 0
    if a.get("--format") == "json":
        return code, json.dumps(d, indent=1)
    if argv[0] == "days":
        o = [f"{d['type']}: {d['count']} emails on days {', '.join(map(str, d['days']))} ({d['days_source']})"]
        for s in d.get("sends", []):
            o.append(f"- day {s['day']}: {s['date']} {s['weekday']}" + (f" (moved from {s['moved_from']})" if s["moved_from"] else ""))
        if d["days_source"] == "example default":
            o.append("These send days are example defaults you can change (--days), not a benchmark.")
        return code, "\n".join(o)
    o = [f"email {r['email']}: subject {r['subject_words']} words, {r['subject_chars']} characters; body {r['body_words']} words" for r in d["emails"]]
    o += [f"PROBLEM {p}" for p in d["problems"]]
    o.append(f"CHECK: {len(d['emails'])} emails, {len(d['problems'])} problems")
    return code, "\n".join(o)


if __name__ == "__main__":
    code, text = run(sys.argv[1:])
    print(text)
    sys.exit(code)
