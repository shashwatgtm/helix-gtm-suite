#!/usr/bin/env python3
"""Number lock, link and date check for a newsletter issue and its derived assets.

The main file is the issue. Each curated item in it starts with a "### "
heading and must carry an http or https link. Derived assets (share card
text, subject lines, a LinkedIn teaser) are extra files.

It prints:
- items in the issue with no link, and a problem when the issue has 0 curated
  items ("0 curated items found: each item must start with a '### ' heading"),
  unless --deep-dive is given for a deep dive issue (one topic, no curated
  items); an empty issue is a problem either way;
- every number in each file, with the word after it;
- numbers in a derived asset that do not appear in the issue (possible drift);
- labels (such as "agents" or "%") that carry different numbers across files;
- a weekday written next to a date that does not match the date;
- dashes, and character counts per "## " or "### " section in each file, with
  per line counts for short sections such as subject line options.

It does not open links. Opening each link is a separate step, done with the
chat's web tools, and reported per link.

Standard library only. Usage:
  python3 asset_check.py issue.md --derived card.txt --derived teaser.txt [--deep-dive] [--json]
"""
import argparse
import datetime as _dt
import json
import re
import sys

URL_RE = re.compile(r"https?://\S+")
DASH_RE = re.compile("[\u2012\u2013\u2014\u2015]|(?<=\\s)-(?=\\s)|\\s--\\s")
NUM_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)([ \t]?%|\+)?(?:[ \t]+([A-Za-z]+))?")
STOP = {"and", "or", "the", "a", "an", "to", "of", "in", "on", "at", "for", "with", "by", "from", "as", "is"}
YEARISH = re.compile(r"^(19|20)\d\d$")
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DATE_RES = [
    re.compile(r"\b(?P<wd>mon|tue|wed|thu|fri|sat|sun)[a-z]*\.?,?\s+(?P<d>\d{1,2})(?:st|nd|rd|th)?\s+(?P<m>[a-z]{3,9})\.?,?\s+(?P<y>\d{4})\b", re.IGNORECASE),
    re.compile(r"\b(?P<wd>mon|tue|wed|thu|fri|sat|sun)[a-z]*\.?,?\s+(?P<m>[a-z]{3,9})\.?\s+(?P<d>\d{1,2})(?:st|nd|rd|th)?,?\s+(?P<y>\d{4})\b", re.IGNORECASE),
]


def utf8_output():
    """Write UTF-8, so a rupee sign, a Unicode minus or a curly quote never stops the script on a Windows console or pipe
    set to code page 1252 (S2, version 1.0.2). A stream that cannot be reconfigured (a test buffer) is left as it is."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def strip_urls(text):
    return URL_RE.sub(" ", text)


def weekday_errors(text):
    out = []
    for rx in DATE_RES:
        for m in rx.finditer(text):
            mname = m.group("m").lower()
            mon = next((i + 1 for i, full in enumerate(MONTHS) if full.startswith(mname[:3])), None)
            if not mon:
                continue
            try:
                real = _dt.date(int(m.group("y")), mon, int(m.group("d"))).strftime("%A")
            except ValueError:
                out.append({"span": m.group(0), "problem": "not a real date"})
                continue
            said = next((w for w in WEEKDAYS if w.startswith(m.group("wd").lower()[:3])), "")
            if said and said.capitalize() != real:
                out.append({"span": m.group(0), "problem": f"that date is a {real}"})
    return out


def numbers_in(text):
    out = []
    for m in NUM_RE.finditer(strip_urls(text)):
        value = m.group(1).replace(",", "")
        suffix = (m.group(2) or "").strip()
        label = (m.group(3) or "").lower()
        if label in STOP:
            label = ""
        if suffix == "%":
            label = "%"
        out.append({"value": value + ("+" if suffix == "+" else ""), "label": label})
    return out


FENCE_RE = re.compile(r"(?ms)^(```|~~~).*?^\1[^\n]*$")


def item_blocks(issue):
    """The curated items: blocks that start with a '### ' line outside a code fence."""
    return re.split(r"(?m)^### ", FENCE_RE.sub("", issue))[1:]


def items_without_link(issue):
    blocks = item_blocks(issue)
    missing = []
    for b in blocks:
        title = b.splitlines()[0].strip() if b.strip() else "(empty item)"
        if not URL_RE.search(b):
            missing.append(title)
    return missing, len(blocks)


def field_counts(text):
    """Characters per '## ' or '### ' section, plus per line counts for short sections (subject lines, titles)."""
    out, name, buf = [], None, []

    def close():
        body = "\n".join(buf).strip()
        lines = [l.strip() for l in body.splitlines() if l.strip()]
        entry = {"field": name, "characters": len(body)}
        if 1 < len(lines) <= 8:
            entry["lines"] = [{"text": l, "characters": len(l)} for l in lines]
        out.append(entry)

    for line in text.splitlines():
        if line.startswith("## ") or line.startswith("### "):
            if name is not None:
                close()
            name, buf = line.lstrip("#").strip(), []
        else:
            buf.append(line)
    if name is not None:
        close()
    return out


ZERO_ITEMS = "0 curated items found: each item must start with a '### ' heading"


def check(issue, derived, deep_dive=False):
    """issue: str. derived: dict name -> str. deep_dive: the issue is one topic with no curated items."""
    files = {"issue": issue, **derived}
    rep = {"items": 0, "items_without_link": [], "numbers": {}, "drift": [], "label_conflicts": [],
           "weekday_errors": [], "dashes": {}, "field_counts": {}, "characters": {}}
    rep["items_without_link"], rep["items"] = items_without_link(issue)
    issue_values = {n["value"] for n in numbers_in(issue)}
    by_label = {}
    for name, text in files.items():
        nums = numbers_in(text)
        rep["numbers"][name] = [n["value"] + ((" " + n["label"]) if n["label"] and n["label"] != "%" else ("%" if n["label"] == "%" else "")) for n in nums]
        rep["characters"][name] = len(text.strip())
        fc = field_counts(text)
        if fc:
            rep["field_counts"][name] = fc
        d = [strip_urls(text)[max(0, m.start() - 12):m.end() + 12] for m in DASH_RE.finditer(strip_urls(text))]
        if d:
            rep["dashes"][name] = d
        for w in weekday_errors(text):
            rep["weekday_errors"].append({"file": name, **w})
        for n in nums:
            if YEARISH.match(n["value"]):
                continue
            if name != "issue" and n["value"] not in issue_values:
                rep["drift"].append({"file": name, "value": n["value"], "label": n["label"]})
            if n["label"]:
                by_label.setdefault(n["label"], {}).setdefault(n["value"], set()).add(name)
    for label, values in sorted(by_label.items()):
        if len(values) > 1:
            rep["label_conflicts"].append({"label": label, "values": {v: sorted(f) for v, f in sorted(values.items())}})
    problems = []
    if not issue.strip():
        problems.append("the issue is empty")
    if rep["items"] == 0 and not deep_dive:
        problems.append(ZERO_ITEMS)
    untitled = sum(1 for b in item_blocks(issue) if not (b.splitlines() or [""])[0].strip())
    if untitled:
        problems.append(f"{untitled} item heading(s) with no title: write the item's headline after '### '")
    if problems:   # the key is added only when there is a problem, so a passing report is the same as before
        rep["problems"] = problems
    rep["pass"] = not (problems or rep["items_without_link"] or rep["drift"] or rep["label_conflicts"] or rep["weekday_errors"] or rep["dashes"])
    return rep


def read(path):
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        return fh.read()


def main(argv=None):
    utf8_output()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("issue", help="the issue text; curated items start with '### '")
    ap.add_argument("--derived", action="append", default=[], help="a derived asset file (repeat)")
    ap.add_argument("--deep-dive", action="store_true", help="the issue is a deep dive (one topic, no '### ' curated items)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        rep = check(read(a.issue), {p: read(p) for p in a.derived}, a.deep_dive)
    except OSError as e:
        print(f"cannot read a file: {e}")
        return 2
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0 if rep["pass"] else 1
    print(f"curated items: {rep['items']}; without a link: {rep['items_without_link'] or 'none'}")
    for name, nums in rep["numbers"].items():
        print(f"{name}: {rep['characters'][name]} characters; numbers: {', '.join(nums) if nums else 'none'}")
        for fc in rep["field_counts"].get(name, []):
            print(f"  field {fc['field']}: {fc['characters']} characters")
            for ln in fc.get("lines", []):
                print(f"    {ln['characters']:>4} | {ln['text']}")
    for d in rep["drift"]:
        print(f"DRIFT: {d['file']} has {d['value']} {d['label']} which is not in the issue")
    for c in rep["label_conflicts"]:
        print(f"CONFLICT: '{c['label']}' carries " + "; ".join(f"{v} in {', '.join(fs)}" for v, fs in c["values"].items()))
    for w in rep["weekday_errors"]:
        print(f"DATE: {w['file']}: {w['span']!r}: {w['problem']}")
    for name, d in rep["dashes"].items():
        print(f"DASH: {name}: {d}")
    for pr in rep.get("problems", []):
        print(f"PROBLEM: {pr}")
    print("PASS" if rep["pass"] else "FIX the items above, then run again")
    return 0 if rep["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
