"""Working day calendar for a mutual close plan, and the dates of a 30, 60 and 90 day account plan.

Every phase weight and every account plan offset is an EXAMPLE DEFAULT that the user can change; the output labels
each one "example default" or "your value". Working days are Monday to Friday minus the holidays the user gives.

Usage:
  python close_plan.py plan --close 2026-12-15 [--today 2026-10-14] [--stage evaluation] [--sector ites]
                            [--holidays 2026-11-09,2026-11-10] [--owner-led] [--weights '{"evaluation": 5}']
                            [--steps '{"evaluation": ["security review", "pilot"], "procurement": ["vendor registration"]}'] [--format text|json]
  python close_plan.py account [--today 2026-10-14] [--offsets 30,60,90] [--format text|json]
  python close_plan.py dates --dates 2026-10-16,2026-10-20 [--today 2026-10-14] [--holidays 2026-11-09] [--format text|json]
  python close_plan.py --help

plan: the start is today (or --today) moved to the next working day; the close is moved back to a working day.
Phases run from the current stage (discovery, evaluation, proposal, negotiation, procurement) to "close"; --owner-led drops
negotiation and procurement (a founder or owner signs and there is no procurement step). Phase length = the working days times
the phase weight divided by all weights, rounded, at least 2 days when there are at least 2 days per phase (else 1); the last
phase takes the remainder. Example default weights: evaluation 4 (5 for ites, telecom, investment), other stages 2, close 1.
Milestone k of n in a phase is due ceil(k x length / n) working days into the phase (the last one on the phase's last day).
Warnings: under 10 working days in all; evaluation under 8 working days. Refused: a past or impossible close date.
account: start plus each offset in calendar days (example default 30, 60, 90), moved back to the nearest working day.
dates: the weekday of each date given (for suggested action dates outside a plan), whether it is a working day, and the next
working day when it is not; a date before today (or --today) is flagged "in the past". 0 dates fails; an impossible date is refused.
Exit code 0 ok, 2 bad input (a clear message, never a traceback). Standard library only; no network; writes no file.
"""
import datetime as dt, json, math, re, sys

STAGES = ["discovery", "evaluation", "proposal", "negotiation", "procurement"]
LONG_EVAL = {"ites", "telecom", "investment"}
SECTORS = {"logistics tech", "logistics", "fintech", "saas", "vertical saas", "ai native", "ites", "telecom", "software", "cybersecurity", "investment", "other"}


class BadInput(Exception):
    pass


def date(s, what):
    if not isinstance(s, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s.strip()):
        raise BadInput(f"{what} must be a date written YYYY-MM-DD, got {s!r}")
    try:
        return dt.date.fromisoformat(s.strip())
    except ValueError:
        raise BadInput(f"{what} {s!r} is not a real calendar date (it is refused, never rolled over to another day)")


def nonconst(c):
    raise BadInput(f"{c} is not a number this script accepts")


def js(raw, what):
    try:
        return json.loads(raw, parse_constant=nonconst)
    except json.JSONDecodeError as e:
        raise BadInput(f"{what} is not valid JSON ({e.msg})")


def is_work(d, hol):
    return d.weekday() < 5 and d not in hol


def fwd(d, hol):
    while not is_work(d, hol):
        d += dt.timedelta(days=1)
    return d


def back(d, hol):
    while not is_work(d, hol):
        d -= dt.timedelta(days=1)
    return d


def workdays(a, b, hol):
    out, d = [], a
    while d <= b:
        if is_work(d, hol):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def fmt(d):
    return f"{d.isoformat()} ({d.strftime('%A')} {d.day} {d.strftime('%B %Y')})"


def parse_opts(argv, allowed, flags=()):
    a, i = {}, 0
    while i < len(argv):
        k = argv[i]
        if k in flags:
            a[k] = True; i += 1; continue
        if k not in allowed or i + 1 >= len(argv):
            raise BadInput(f"unknown or incomplete option {k!r}; see the usage at the top of close_plan.py")
        a[k] = argv[i + 1]; i += 2
    return a


def plan(a):
    today = date(a["--today"], "--today") if "--today" in a else dt.date.today()
    if "--close" not in a:
        raise BadInput("give the target close date with --close YYYY-MM-DD")
    close_raw = date(a["--close"], "--close")
    if close_raw < today:
        raise BadInput(f"the close date {close_raw.isoformat()} is in the past (today is {today.isoformat()}); give a future date")
    stage = a.get("--stage", "evaluation")
    if stage not in STAGES:
        raise BadInput(f"--stage must be one of {', '.join(STAGES)}, got {stage!r}")
    sector = a.get("--sector", "other").strip().lower()
    if sector not in SECTORS:
        raise BadInput(f"--sector must be one of {', '.join(sorted(SECTORS))}, got {sector!r}")
    hol = set()
    if a.get("--holidays"):
        hol = {date(h, "a holiday") for h in a["--holidays"].split(",")}
    notes = []
    start = fwd(today, hol)
    close = back(close_raw, hol)
    if close != close_raw:
        notes.append(f"the close date {close_raw.isoformat()} is not a working day, so it moved back to {close.isoformat()}")
    if start != today:
        notes.append(f"today {today.isoformat()} is not a working day, so the plan starts on {start.isoformat()}")
    phases = STAGES[STAGES.index(stage):]
    if "--owner-led" in a:
        phases = [p for p in phases if p not in ("negotiation", "procurement")]
        notes.append("owner led: negotiation and procurement phases dropped (the owner signs, no procurement step)")
    phases = phases + ["close"]
    weights = {p: (4 if p == "evaluation" else 1 if p == "close" else 2) for p in phases}
    if "evaluation" in weights and sector in LONG_EVAL:
        weights["evaluation"] = 5
    wsrc = {p: "example default" for p in phases}
    if "--weights" in a:
        w = js(a["--weights"], "--weights")
        if not isinstance(w, dict):
            raise BadInput("--weights must be an object like {\"evaluation\": 5}")
        for k, v in w.items():
            if k not in weights:
                raise BadInput(f"--weights names a phase not in this plan: {k!r} (phases: {', '.join(phases)})")
            if isinstance(v, bool) or not isinstance(v, (int, float)) or math.isnan(v) or math.isinf(v) or v <= 0:
                raise BadInput(f"the weight of {k} must be a number above 0, got {v!r}")
            weights[k], wsrc[k] = v, "your value"
    steps = {}
    if "--steps" in a:
        s = js(a["--steps"], "--steps")
        if not isinstance(s, dict):
            raise BadInput("--steps must be an object of phase: [step, ...]")
        for k, v in s.items():
            if k not in weights:
                raise BadInput(f"--steps names a phase not in this plan: {k!r} (phases: {', '.join(phases)})")
            if not isinstance(v, list) or not v or not all(isinstance(x, str) and x.strip() for x in v):
                raise BadInput(f"the steps of {k} must be a non empty list of text items")
            steps[k] = v
    days = workdays(start, close, hol)
    n, p = len(days), len(phases)
    if n < p:
        raise BadInput(f"only {n} working days from {start.isoformat()} to {close.isoformat()} for {p} phases ({', '.join(phases)}): move the close date, or start from a later stage")
    total = sum(weights.values())
    floor_len = 2 if n >= 2 * p else 1
    lens = [max(round(n * weights[ph] / total), floor_len) for ph in phases[:-1]]
    while sum(lens) > n - 1:   # the close phase keeps at least one day; trim the longest phase first
        i = max(range(len(lens)), key=lambda j: lens[j])
        if lens[i] <= 1:
            break
        lens[i] -= 1
    lens.append(n - sum(lens))
    out, k = [], 0
    for ph, ln in zip(phases, lens):
        seg = days[k:k + ln]; k += ln
        ms = []
        for j, st in enumerate(steps.get(ph, []), 1):
            off = math.ceil(j * ln / len(steps[ph])) - 1
            ms.append({"step": st, "due": seg[min(off, ln - 1)].isoformat()})
        out.append({"phase": ph, "days": ln, "start": seg[0].isoformat(), "end": seg[-1].isoformat(), "weight": weights[ph], "weight_source": wsrc[ph], "milestones": ms})
    warnings = []
    if n < 10:
        warnings.append(f"only {n} working days to the close: under 10 working days (example default threshold); agree with the buyer which steps can run in parallel")
    ev = next((x for x in out if x["phase"] == "evaluation"), None)
    if ev and ev["days"] < 8:
        warnings.append(f"evaluation has {ev['days']} working days, under 8 (example default threshold): confirm the buyer can finish the evaluation in that time")
    return {"today": today.isoformat(), "start": start.isoformat(), "close": close.isoformat(), "working_days": n,
            "calendar_days": (close - start).days + 1, "holidays_removed": sorted(h.isoformat() for h in hol if start <= h <= close),
            "phases": out, "warnings": warnings, "notes": notes,
            "label": "phase weights are example defaults unless marked your value; dates are working days Monday to Friday minus your holidays"}


def account(a):
    today = date(a["--today"], "--today") if "--today" in a else dt.date.today()
    raw = a.get("--offsets")
    src = "example default"
    if raw is None:
        offs = [30, 60, 90]
    else:
        src = "your value"
        parts = [x.strip() for x in raw.split(",")]
        if not raw.strip() or not all(re.fullmatch(r"\d+", x) for x in parts):
            raise BadInput(f"--offsets must be whole days of 1 or more separated by commas, got {raw!r}")
        offs = [int(x) for x in parts]
        if any(x < 1 for x in offs) or offs != sorted(set(offs)):
            raise BadInput(f"--offsets must be increasing whole days of 1 or more, got {raw!r}")
    ms = []
    for o in offs:
        d = today + dt.timedelta(days=o)
        b = back(d, set())
        ms.append({"offset_days": o, "offset_source": src, "due": b.isoformat(), "weekday": b.strftime("%A"), "moved_from": d.isoformat() if b != d else None})
    return {"today": today.isoformat(), "milestones": ms, "label": "offsets are example defaults unless marked your value"}


def dates_cmd(a):
    raw = a.get("--dates")
    if raw is None or not raw.strip():
        raise BadInput("0 dates given: give --dates YYYY-MM-DD,YYYY-MM-DD (a check that reads 0 items fails)")
    today = date(a["--today"], "--today") if "--today" in a else dt.date.today()
    hol = set()
    if a.get("--holidays"):
        hol = {date(h, "a holiday") for h in a["--holidays"].split(",")}
    rows = []
    for part in raw.split(","):
        d = date(part, "a date in --dates")
        work = is_work(d, hol)
        rows.append({"date": d.isoformat(), "weekday": d.strftime("%A"), "working_day": work,
                     "next_working_day": None if work else fwd(d, hol).isoformat(), "holiday": d in hol, "past": d < today})
    return {"today": today.isoformat(), "dates": rows, "label": "working days are Monday to Friday minus your holidays"}


def text_plan(d):
    o = [f"Close plan: {d['working_days']} working days from {fmt(dt.date.fromisoformat(d['start']))} to {fmt(dt.date.fromisoformat(d['close']))} ({d['calendar_days']} calendar days)."]
    if d["holidays_removed"]:
        o.append("Holidays removed: " + ", ".join(d["holidays_removed"]))
    for p in d["phases"]:
        o.append(f"- {p['phase']}: {p['days']} working day{'s' if p['days'] != 1 else ''}, {p['start']} to {p['end']} (weight {p['weight']}, {p['weight_source']})")
        for m in p["milestones"]:
            o.append(f"    due {m['due']} ({dt.date.fromisoformat(m['due']).strftime('%A')}): {m['step']}")
    for w in d["warnings"]:
        o.append("WARNING: " + w)
    for n in d["notes"]:
        o.append("Note: " + n)
    o.append("Phase weights are example defaults you can change (--weights), not a benchmark; the buyer's own steps and dates win.")
    return "\n".join(o)


def run(argv):
    if argv and (argv[0] in ("--help", "-h") or "--help" in argv):
        return 0, __doc__.strip()
    try:
        if not argv or argv[0] not in ("plan", "account", "dates"):
            raise BadInput("first word must be plan, account or dates; see the usage at the top of close_plan.py (or --help)")
        if argv[0] == "dates":
            a = parse_opts(argv[1:], {"--dates", "--today", "--holidays", "--format"})
            d = dates_cmd(a)
        elif argv[0] == "plan":
            a = parse_opts(argv[1:], {"--close", "--today", "--stage", "--sector", "--holidays", "--weights", "--steps", "--format"}, {"--owner-led"})
            d = plan(a)
        else:
            a = parse_opts(argv[1:], {"--today", "--offsets", "--format"})
            d = account(a)
    except BadInput as e:
        return 2, f"BAD INPUT: {e}"
    if a.get("--format") == "json":
        return 0, json.dumps(d, indent=1)
    if argv[0] == "plan":
        return 0, text_plan(d)
    if argv[0] == "dates":
        lines = []
        for r in d["dates"]:
            extra = ""
            if not r["working_day"]:
                nxt = dt.date.fromisoformat(r["next_working_day"])
                extra = f" (not a working day{', your holiday' if r['holiday'] else ''}; next working day {nxt.isoformat()} {nxt.strftime('%A')})"
            if r["past"]:
                extra += f" (in the past: today is {d['today']})"
            lines.append(f"{r['date']} {r['weekday']}{extra}")
        return 0, "\n".join(lines)
    lines = ["Account plan dates (start " + d["today"] + "):"]
    for m in d["milestones"]:
        lines.append(f"- day {m['offset_days']} ({m['offset_source']}): {m['due']} {m['weekday']}" + (f", moved back from {m['moved_from']} (weekend)" if m["moved_from"] else ""))
    lines.append("The 30, 60 and 90 day offsets are example defaults you can change (--offsets).")
    return 0, "\n".join(lines)


if __name__ == "__main__":
    code, text = run(sys.argv[1:])
    print(text)
    sys.exit(code)
