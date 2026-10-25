"""Deal health score for one deal or a list of deals, from the seller's own facts.

Every point value, stage threshold and band below is an EXAMPLE DEFAULT that the user can change with
--points and --thresholds; the output labels each one "example default" or "your value". None is a benchmark.

Usage:
  python deal_health.py --json '{"stage": "proposal", "days_in_stage": 31, "champion": "confirmed",
                                 "economic_buyer": "CFO named, not engaged", "competitors": [{"name": "current tool", "incumbent": true}],
                                 "blockers": ["security review"]}'
  python deal_health.py --json deals.json            (a file path also works; {"deals": [...]} for many deals)
  options: --thresholds '{"demo": 10}'  --points '{"start": 60}'  --format text|json  --help

Fields of a deal (all optional except stage):
  stage           prospecting, discovery, demo, proposal, negotiation, closing, or stuck (then give stuck_in)
  stuck_in        the stage a stuck deal is stuck in
  days_in_stage   whole days, 0 or more (missing = not given: not scored, never read as 0)
  champion        multi_threaded, confirmed, potential or none (missing = not given: not scored)
  economic_buyer  engaged, named or unknown, or the seller's own phrase (read by whole words; "disengaged",
                  "not engaged", "no longer engaged" are not engaged); empty or missing = unknown
  economic_buyer_said  the seller's own words about the economic buyer, printed exactly as given ("you said: ...") so the
                  score block can be quoted unchanged; when economic_buyer is missing, the state is read from these words
  competitors     a list of {"name": ..., "incumbent": true|false}, or a phrase ("incumbent" as a whole word, not negated)
  blockers        a list of strings or a phrase
Exit code 0 ok, 2 bad input (a clear message, never a traceback). Standard library only; no network; writes no file.
"""
import json, math, os, re, sys

STAGES = ["prospecting", "discovery", "demo", "proposal", "negotiation", "closing"]
DEFAULT_THRESHOLDS = {"prospecting": 14, "discovery": 21, "demo": 14, "proposal": 21, "negotiation": 30, "closing": 14}
DEFAULT_POINTS = {"start": 70, "champion_multi_threaded": 15, "champion_confirmed": 10, "champion_potential": 0, "champion_none": -20,
                  "buyer_engaged": 10, "buyer_named": 5, "buyer_unknown": -10, "over_threshold": -5, "over_twice_threshold": -15,
                  "incumbent": -10, "other_competitor": -5, "blockers": -10, "at_risk_below": 50, "needs_attention_below": 70}
CHAMPION = {"multi_threaded": "multi_threaded", "multi-threaded": "multi_threaded", "confirmed": "confirmed", "confirmed_champion": "confirmed",
            "potential": "potential", "potential_champion": "potential", "none": "none", "no_champion": "none"}
UNKNOWN_RX = re.compile(r"\b(unknown|unclear|no idea|not sure who|(do not|don't|dont) know|not (yet )?(named|identified|known|found))\b")
NONE_RX = re.compile(r"^\s*(none|nil|n/?a|nothing( known)?|no (known )?(blockers?|competitors?|competition|objections?|one))\s*\.?\s*$", re.I)
NEGATIONS = {"not", "no", "never", "longer", "nobody", "isn't", "hasn't", "wasn't", "hadn't", "haven't", "aren't", "un", "barely"}


class BadInput(Exception):
    pass


def number(v, what, minimum=None):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise BadInput(f"{what} must be a number, got {json.dumps(v)}")
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        raise BadInput(f"{what} must be a real number, got {v}")
    if minimum is not None and v < minimum:
        raise BadInput(f"{what} must be {minimum} or more, got {v}")
    return v


def words(text):
    return re.findall(r"[a-z']+", text.lower())


def positive_word(text, word):
    """True when `word` appears as a whole word and none of the five words before it is a negation."""
    w = words(text)
    for i, x in enumerate(w):
        if x == word and not (set(w[max(0, i - 5):i]) & NEGATIONS):
            return True
    return False


def buyer_state(v):
    if v is None or (isinstance(v, str) and not v.strip()):
        return "unknown", "not given"
    if not isinstance(v, str):
        raise BadInput(f"economic_buyer must be text, got {json.dumps(v)}")
    t = v.strip().lower()
    if t in ("engaged", "named", "unknown"):
        return t, v
    if t in ("none", "tbd", "n/a") or UNKNOWN_RX.search(t):
        return "unknown", v
    return ("engaged" if positive_word(v, "engaged") else "named"), v


def competitor_kind(v):
    if v is None or v == "" or v == []:
        return None
    if isinstance(v, list):
        if not all(isinstance(c, dict) for c in v):
            raise BadInput("competitors must be a list of objects like {\"name\": \"...\", \"incumbent\": true}, or a phrase")
        for c in v:
            if "incumbent" in c and not isinstance(c["incumbent"], bool):
                raise BadInput("competitors[].incumbent must be true or false")
        return "incumbent" if any(c.get("incumbent") is True for c in v) else "other"
    if isinstance(v, str):
        if NONE_RX.match(v):
            return None
        return "incumbent" if positive_word(v, "incumbent") else "other"
    raise BadInput("competitors must be a list or a phrase")


def has_blockers(v):
    if v is None or v == "" or v == []:
        return False
    if isinstance(v, list):
        if not all(isinstance(b, str) for b in v):
            raise BadInput("blockers must be a list of text items or a phrase")
        return any(b.strip() for b in v)
    if isinstance(v, str):
        return bool(v.strip()) and not NONE_RX.match(v)
    raise BadInput("blockers must be a list or a phrase")


def score(deal, thresholds, t_src, points, p_src):
    if not isinstance(deal, dict):
        raise BadInput(f"each deal must be an object, got {json.dumps(deal)}")
    lines, total, missing = [], points["start"], []
    lab = lambda k: p_src[k]
    lines.append(f"start {points['start']:+d} ({lab('start')})")
    stage = deal.get("stage")
    if stage not in STAGES + ["stuck"]:
        raise BadInput(f"stage must be one of {', '.join(STAGES + ['stuck'])}, got {json.dumps(stage)}")
    # champion
    ch = deal.get("champion")
    if ch is None:
        lines.append("champion: not given (not scored; tell me multi_threaded, confirmed, potential or none)")
        missing.append("champion")
    else:
        if not isinstance(ch, str) or ch.strip().lower() not in CHAMPION:
            raise BadInput(f"champion must be multi_threaded, confirmed, potential or none, got {json.dumps(ch)}")
        c = CHAMPION[ch.strip().lower()]
        k = "champion_" + c
        total += points[k]
        lines.append(f"champion {c.replace('_', ' ')}: {points[k]:+d} ({lab(k)})")
    # economic buyer
    eb_said = deal.get("economic_buyer_said")
    if eb_said is not None and not isinstance(eb_said, str):
        raise BadInput(f"economic_buyer_said must be text (the seller's own words), got {json.dumps(eb_said)}")
    eb = deal.get("economic_buyer")
    if (eb is None or (isinstance(eb, str) and not eb.strip())) and eb_said and eb_said.strip():
        eb = eb_said
    state, said = buyer_state(eb)
    if eb_said and eb_said.strip() and eb is not eb_said:
        t = eb_said.lower()
        neg = bool(re.search(r"\bdisengaged\b", t)) or ("engaged" in words(t) and not positive_word(eb_said, "engaged"))
        pos = positive_word(eb_said, "engaged")
        unk = bool(UNKNOWN_RX.search(t))
        if (state == "engaged" and (neg or unk)) or (state != "engaged" and pos):
            raise BadInput(f"economic_buyer {json.dumps(eb)} and economic_buyer_said {json.dumps(eb_said)} conflict: "
                           "check with the seller which is right, then pass the state that matches their words")
    if said == "not given":
        missing.append("economic buyer (scored as unknown)")
    k = {"engaged": "buyer_engaged", "named": "buyer_named", "unknown": "buyer_unknown"}[state]
    total += points[k]
    shown = {"engaged": "engaged", "named": "named, not engaged", "unknown": "unknown"}[state]
    src = f'you said: "{eb_said.strip()}"' if eb_said and eb_said.strip() else f"from: {said}"
    lines.append(f"economic buyer {shown} ({src}): {points[k]:+d} ({lab(k)})")
    # days in stage
    days = deal.get("days_in_stage")
    eff_stage = stage
    if stage == "stuck":
        eff_stage = deal.get("stuck_in")
        if eff_stage is not None and eff_stage not in STAGES:
            raise BadInput(f"stuck_in must be one of {', '.join(STAGES)}, got {json.dumps(eff_stage)}")
    if days is None:
        lines.append("days in stage: not given (not scored)")
        missing.append("days in stage")
    else:
        number(days, "days_in_stage", 0)
        if eff_stage is None:
            lines.append(f"days in stage {days}: not scored, because a stuck deal needs the stage it is stuck in (stuck in which stage? give stuck_in)")
            missing.append("the stage the deal is stuck in")
        else:
            th = thresholds[eff_stage]
            src = t_src[eff_stage]
            if days > th * 2:
                total += points["over_twice_threshold"]
                lines.append(f"{days} days in {eff_stage}, more than twice the threshold of {th} days ({src}): {points['over_twice_threshold']:+d} ({lab('over_twice_threshold')})")
            elif days > th:
                total += points["over_threshold"]
                lines.append(f"{days} days in {eff_stage}, over the threshold of {th} days ({src}): {points['over_threshold']:+d} ({lab('over_threshold')})")
            else:
                lines.append(f"{days} days in {eff_stage}, within the threshold of {th} days ({src}): +0")
    # competitors and blockers
    kind = competitor_kind(deal.get("competitors"))
    if kind == "incumbent":
        total += points["incumbent"]; lines.append(f"incumbent competitor: {points['incumbent']:+d} ({lab('incumbent')})")
    elif kind == "other":
        total += points["other_competitor"]; lines.append(f"other competitor in the deal: {points['other_competitor']:+d} ({lab('other_competitor')})")
    else:
        lines.append("competitors: none given (+0)")
    if has_blockers(deal.get("blockers")):
        total += points["blockers"]; lines.append(f"known blockers: {points['blockers']:+d} ({lab('blockers')})")
    else:
        lines.append("blockers: none given (+0)")
    clamped = max(0, min(100, total))
    if clamped != total:
        lines.append(f"raw total {total} kept inside 0 to 100")
    if clamped < points["at_risk_below"]:
        status = "At Risk"
    elif clamped < points["needs_attention_below"]:
        status = "Needs Attention"
    else:
        status = "Healthy"
    return {"name": deal.get("name") or deal.get("deal_name") or "", "score": clamped, "status": status, "factors": lines, "missing": missing}


def load(raw):
    if os.path.isfile(raw):
        with open(raw, encoding="utf-8") as f:
            raw = f.read()
    def no_const(c):
        raise BadInput(f"{c} is not a number this script accepts")
    try:
        return json.loads(raw, parse_constant=no_const)
    except json.JSONDecodeError as e:
        raise BadInput(f"the input is not valid JSON ({e.msg} at line {e.lineno} column {e.colno})")


def merged(defaults, override, what):
    out, src = dict(defaults), {k: "example default" for k in defaults}
    if override is None:
        return out, src
    if not isinstance(override, dict):
        raise BadInput(f"{what} must be an object")
    for k, v in override.items():
        if k not in defaults:
            raise BadInput(f"unknown key in {what}: {k} (known: {', '.join(defaults)})")
        number(v, f"{what}.{k}", 0 if what == "thresholds" else None)
        out[k], src[k] = v, "your value"
    return out, src


def run(argv):
    if argv and (argv[0] in ("--help", "-h") or "--help" in argv):
        return 0, __doc__.strip()
    try:
        a = {"--format": "text"}
        i = 0
        while i < len(argv):
            if argv[i] not in ("--json", "--thresholds", "--points", "--format") or i + 1 >= len(argv):
                raise BadInput(f"unknown or incomplete option {argv[i]!r}; see the usage at the top of deal_health.py")
            a[argv[i]] = argv[i + 1]; i += 2
        if "--json" not in a:
            raise BadInput("give the deal with --json")
        data = load(a["--json"])
        thresholds, t_src = merged(DEFAULT_THRESHOLDS, load(a["--thresholds"]) if "--thresholds" in a else None, "thresholds")
        points, p_src = merged(DEFAULT_POINTS, load(a["--points"]) if "--points" in a else None, "points")
        if isinstance(data, dict) and "deals" in data:
            deals = data["deals"]
            if not isinstance(deals, list):
                raise BadInput("deals must be a list")
            if not deals:
                raise BadInput("0 deals given: nothing to score (a check that reads 0 items fails)")
        elif isinstance(data, dict):
            deals = [data]
        else:
            raise BadInput("give one deal as an object, or {\"deals\": [...]}")
        rows = []
        for i, d in enumerate(deals, 1):
            try:
                rows.append(score(d, thresholds, t_src, points, p_src))
            except BadInput as e:
                if len(deals) == 1:
                    raise
                nm = d.get("name") or d.get("deal_name") if isinstance(d, dict) else None
                raise BadInput(f"deal {i}" + (f" ({nm})" if nm else "") + f": {e}")
    except BadInput as e:
        return 2, f"BAD INPUT: {e}"
    if a["--format"] == "json":
        return 0, json.dumps({"deals": rows, "note": "every point value, threshold and band is an example default unless marked your value"}, indent=1)
    out = []
    for r in rows:
        out.append(f"Deal: {r['name'] or '(no name)'}")
        out.append(f"Score: {r['score']} of 100")
        out.append(f"Status: {r['status']} (bands: below {points['at_risk_below']} At Risk, below {points['needs_attention_below']} Needs Attention; {p_src['at_risk_below']})")
        if r["missing"]:
            out.append(f"INCOMPLETE: not scored because not given: {', '.join(r['missing'])}. Read the score and status as provisional until these are known.")
        out += ["  " + x for x in r["factors"]]
        out.append("")
    out.append("Every point value, threshold and band above is an example default you can change (--points, --thresholds), not a benchmark.")
    return 0, "\n".join(out)


if __name__ == "__main__":
    code, text = run(sys.argv[1:])
    print(text)
    sys.exit(code)
