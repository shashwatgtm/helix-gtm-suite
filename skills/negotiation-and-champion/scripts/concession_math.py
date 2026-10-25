"""Concession arithmetic for a new deal negotiation, on the seller's own figures only.

No default price, discount or gap exists in this script: every figure comes from the user and is shown as "your figures".
Money may be typed as 4000000, 40,00,000, 4,000,000, "40 lakh" or "1.2 crore"; results are printed in the same plain units.

Usage:
  python concession_math.py discount --value 4000000 --discount 20 [--trade "three year term=150000" ...] [--format text|json]
  python concession_math.py multiyear --annual 1000000 --discounts 0,5,10 [--format text|json]
  python concession_math.py gap --value 1000000 --gap-percent 30 [--format text|json]
  python concession_math.py --help

discount: revenue at risk = value x discount / 100; value after discount; each trade the seller asks for in return with the worth
the seller puts on it (a negative worth is a cost and keeps its minus sign); the net after the trades.
multiyear: the list price per year against the price after each year's discount; totals and the amount given up.
gap: the amount of a price gap the user typed as a percentage of the deal value (never looked up or guessed).
Refused with a clear message: a discount below 0 or above 100, a negative or missing deal value, NaN, Infinity, text that is not
a number, a trade without "label=worth". Exit code 0 ok, 2 bad input. Standard library only; no network; writes no file.
"""
import json, math, re, sys

UNITS = {"lakh": 100000, "lakhs": 100000, "lac": 100000, "crore": 10000000, "crores": 10000000, "cr": 10000000}


class BadInput(Exception):
    pass


def money(raw, what, allow_negative=False):
    if raw is None:
        raise BadInput(f"{what} not given: it is reported missing, never read as 0")
    s = str(raw).strip().lower().replace("₹", "").replace("$", "").replace("rs.", "").replace("inr", "").strip()
    m = re.fullmatch(r"([+-]?[\d,]*\.?\d+)\s*([a-z]*)", s)
    if not m or (m.group(2) and m.group(2) not in UNITS):
        raise BadInput(f"{what} must be a number (for example 4000000, 40,00,000 or 40 lakh), got {raw!r}")
    num = float(m.group(1).replace(",", ""))
    if math.isnan(num) or math.isinf(num):
        raise BadInput(f"{what} must be a real number, got {raw!r}")
    num *= UNITS.get(m.group(2), 1)
    if num < 0 and not allow_negative:
        raise BadInput(f"{what} cannot be negative, got {raw} (the minus sign is kept and refused, never dropped)")
    return int(num) if float(num).is_integer() else round(num, 2)


def percent(raw, what):
    if raw is None:
        raise BadInput(f"{what} not given")
    s = str(raw).strip().rstrip("%").strip()
    if not re.fullmatch(r"[+-]?\d*\.?\d+", s):
        raise BadInput(f"{what} must be a percentage from 0 to 100, got {raw!r}")
    v = float(s)
    if v < 0 or v > 100:
        raise BadInput(f"{what} must be from 0 to 100, got {raw}")
    return int(v) if v.is_integer() else v


def r2(x):
    x = round(x, 2)
    return int(x) if float(x).is_integer() else x


def show(x):
    return f"{x:,.2f}".rstrip("0").rstrip(".") if isinstance(x, float) else f"{x:,}"


def parse(argv, allowed, multi=()):
    a, i = {k: [] for k in multi}, 0
    while i < len(argv):
        k = argv[i]
        if k not in allowed or i + 1 >= len(argv):
            raise BadInput(f"unknown or incomplete option {k!r}; see the usage at the top of concession_math.py")
        if k in multi:
            a[k].append(argv[i + 1])
        else:
            a[k] = argv[i + 1]
        i += 2
    return a


def discount(a):
    if "--value" not in a:
        raise BadInput("deal value not given: give --value (it is never read as 0)")
    v = money(a["--value"], "the deal value")
    d = percent(a.get("--discount"), "the discount")
    risk = r2(v * d / 100)
    trades = []
    for t in a["--trade"]:
        if "=" not in t:
            raise BadInput(f"a trade must be written label=worth, for example \"three year term=150000\", got {t!r}")
        label, worth = t.rsplit("=", 1)
        if not label.strip():
            raise BadInput(f"a trade needs a label before the = sign, got {t!r}")
        trades.append({"trade": label.strip(), "worth": money(worth, f"the worth of {label.strip()!r}", allow_negative=True)})
    after = r2(v - risk)
    return {"value": v, "discount_percent": d, "revenue_at_risk": risk, "value_after_discount": after, "trades": trades,
            "net_after_trades": r2(after + sum(t["worth"] for t in trades)) if trades else None,
            "label": "your figures; the worth of each trade is the value you put on it"}


def multiyear(a):
    v = money(a.get("--annual"), "the annual value")
    raw = a.get("--discounts", "")
    parts = [p.strip() for p in raw.split(",")]
    if not raw.strip() or not all(parts):
        raise BadInput(f"--discounts must list one percentage per year separated by commas, got {raw!r}")
    ds = [percent(p, f"the discount for year {i}") for i, p in enumerate(parts, 1)]
    rows = [{"year": i, "list": v, "discount_percent": d, "after": r2(v - v * d / 100)} for i, d in enumerate(ds, 1)]
    tot_list, tot_after = r2(v * len(ds)), r2(sum(r["after"] for r in rows))
    return {"annual": v, "years": len(ds), "by_year": rows, "total_at_list": tot_list, "total_after": tot_after, "given_up": r2(tot_list - tot_after),
            "label": "your figures"}


def gap(a):
    v = money(a.get("--value"), "the deal value")
    if "--gap-percent" not in a:
        raise BadInput("competitor gap not given: type the gap the buyer told you as --gap-percent (it is never looked up or guessed)")
    g = percent(a["--gap-percent"], "the gap")
    amt = r2(v * g / 100)
    return {"value": v, "gap_percent": g, "gap_amount": amt, "competitor_price_if_gap_holds": r2(v - amt),
            "label": "your figures; the gap is what the buyer said, not checked"}


def run(argv):
    if argv and (argv[0] in ("--help", "-h") or "--help" in argv):
        return 0, __doc__.strip()
    try:
        if not argv or argv[0] not in ("discount", "multiyear", "gap"):
            raise BadInput("first word must be discount, multiyear or gap; see the usage at the top of concession_math.py")
        cmd = argv[0]
        if cmd == "discount":
            a = parse(argv[1:], {"--value", "--discount", "--trade", "--format"}, ("--trade",)); d = discount(a)
        elif cmd == "multiyear":
            a = parse(argv[1:], {"--annual", "--discounts", "--format"}); d = multiyear(a)
        else:
            a = parse(argv[1:], {"--value", "--gap-percent", "--format"}); d = gap(a)
    except BadInput as e:
        return 2, f"BAD INPUT: {e}"
    if a.get("--format") == "json":
        return 0, json.dumps(d, indent=1)
    if cmd == "discount":
        o = [f"Deal value {show(d['value'])}, discount asked {d['discount_percent']}% (your figures).",
             f"Revenue at risk: {show(d['revenue_at_risk'])}", f"Value after discount: {show(d['value_after_discount'])}"]
        for t in d["trades"]:
            o.append(f"Trade asked in return: {t['trade']}, worth {show(t['worth'])} (your estimate)")
        if d["trades"]:
            o.append(f"Net after the discount and the trades: {show(d['net_after_trades'])}")
    elif cmd == "multiyear":
        o = [f"Annual value {show(d['annual'])} over {d['years']} years (your figures)."]
        o += [f"Year {r['year']}: {show(r['list'])} at list, {r['discount_percent']}% off, {show(r['after'])} after" for r in d["by_year"]]
        o += [f"Total at list: {show(d['total_at_list'])}", f"Total after discounts: {show(d['total_after'])}", f"Given up over the term: {show(d['given_up'])}"]
    else:
        o = [f"Deal value {show(d['value'])}; the buyer says the other offer is {d['gap_percent']}% lower (your figures, not checked).",
             f"Gap amount: {show(d['gap_amount'])}", f"The other offer if that gap holds: {show(d['competitor_price_if_gap_holds'])}"]
    return 0, "\n".join(o)


if __name__ == "__main__":
    code, text = run(sys.argv[1:])
    print(text)
    sys.exit(code)
