#!/usr/bin/env python3
"""Count and lock check for personal brand assets.

Give it one text file where each asset starts with a "## " heading, for example:

  ## Headline
  ...
  ## Short bio
  ...

For every field it prints characters, words, dashes found and numbers found.
When a field holds draft labels ("[Draft for you to confirm: ...]" or the
"[Principal to confirm]" marker), it also prints the count without them: the
label words and brackets are removed and the drafted words kept, because that
is the text the person will publish. Limits are checked on that count. Open
"[User to add: ...]" placeholders are counted, since filling them changes the
count.
Across fields it lists every number with the word after it, and flags a
label (such as "years") that carries different numbers in different fields,
so the person can keep titles and figures identical across assets. It also
checks that a weekday written next to a date is right.

Limits are never assumed. Pass the limits the person or the platform's own
help page gave, for example --limit "Headline=220" --limit "About=2600".
A limit is a whole number of characters for a field that is a "## " heading in the file;
anything else (a word target, a sign, a non ASCII digit, more than 9 digits) is bad input (exit 2)
with a plain message.

Standard library only. Reads a file path or "-" for stdin. Writes nothing.
"""
import argparse
import datetime as _dt
import json
import re
import sys

# The drafted words may hold one level of brackets, such as [Name] or a [User to add: ...] placeholder.
DRAFT_RE = re.compile(r"\[Draft for you to confirm:\s*((?:[^\[\]]|\[[^\[\]]*\])*)\]", re.IGNORECASE)
MARKER_RE = re.compile(r"\s*\[Principal to confirm\]", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"\[User to add:[^\[\]]*\]", re.IGNORECASE)
DASH_RE = re.compile("[\u2012\u2013\u2014\u2015]|(?<=\\s)-(?=\\s)|\\s--\\s")
NUM_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)([ \t]?%|\+)?(?:[ \t]+([A-Za-z]+))?")
STOP_UNITS = {"and", "or", "the", "a", "an", "to", "of", "in", "on", "at", "for", "with", "by", "from", "as"}
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"])}
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


def month_of(name):
    name = name.lower()
    for full, num in MONTHS.items():
        if full == name or full[:3] == name[:3] and len(name) >= 3 and full.startswith(name[:3]):
            return num
    return None


def weekday_errors(text):
    out = []
    for rx in DATE_RES:
        for m in rx.finditer(text):
            mon = month_of(m.group("m"))
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


def split_fields(text):
    fields, name, buf = [], None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if name is not None:
                fields.append((name, "\n".join(buf).strip()))
            name, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if name is not None:
        fields.append((name, "\n".join(buf).strip()))
    if not fields:
        fields = [("Text", text.strip())]
    return fields


def numbers_in(body):
    out = []
    for m in NUM_RE.finditer(body):
        value, suffix, unit = m.group(1), (m.group(2) or "").strip(), (m.group(3) or "").lower()
        if unit in STOP_UNITS:
            unit = ""
        out.append({"value": value + suffix, "label": unit})
    return out


def without_labels(body):
    """The text the person will publish: draft labels and markers removed, drafted words kept."""
    out = DRAFT_RE.sub(lambda m: m.group(1).strip(), body)
    out = MARKER_RE.sub("", out)
    return re.sub(r"[ \t]{2,}", " ", out).strip()


def check(text, limits=None):
    limits = {k.lower(): v for k, v in (limits or {}).items()}
    report = {"fields": [], "label_conflicts": [], "weekday_errors": weekday_errors(text)}
    by_label = {}
    for name, body in split_fields(text):
        nums = numbers_in(body)
        entry = {
            "field": name,
            "characters": len(body),
            "words": len(re.findall(r"\S+", body)),
            "final_characters": len(without_labels(body)),
            "final_words": len(re.findall(r"\S+", without_labels(body))),
            "draft_labels": len(DRAFT_RE.findall(body)) + len(MARKER_RE.findall(body)),
            "placeholders_open": len(PLACEHOLDER_RE.findall(body)),
            "dashes": [body[max(0, m.start() - 12):m.end() + 12] for m in DASH_RE.finditer(body)],
            "numbers": [n["value"] + (" " + n["label"] if n["label"] else "") for n in nums],
        }
        lim = limits.get(name.lower())
        if lim is not None:
            entry["limit"] = lim
            entry["over_limit_by"] = max(0, entry["final_characters"] - lim)
        report["fields"].append(entry)
        for n in nums:
            if n["label"]:
                by_label.setdefault(n["label"], {}).setdefault(n["value"], set()).add(name)
    for label, values in sorted(by_label.items()):
        if len(values) > 1:
            report["label_conflicts"].append({
                "label": label,
                "values": {v: sorted(f) for v, f in sorted(values.items())},
            })
    return report


def parse_limits(items):
    """Run 33A: a limit that is not a whole number of characters ("Short bio=50w", "=fifty", "=-5", "=12.5", no "=") is bad
    input with a plain message and exit code 2, never a traceback. Limits are characters; a word target is checked by reading
    the word count this script prints."""
    out = {}
    for it in items or []:
        k, sep, v = it.partition("=")
        v = v.strip()
        if not sep or not k.strip() or not (v.isascii() and v.isdigit()) or len(v) > 9:
            print(f"bad --limit {it!r}: use Field=number of characters, for example --limit \"Headline=220\" "
                  f"(a word target is not a limit: compare it with the word count this script prints)")
            raise SystemExit(2)
        out[k.strip()] = int(v)
    return out


def main(argv=None):
    utf8_output()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="text file with '## Field' headings, or - for stdin")
    ap.add_argument("--limit", action="append", help="Field=max characters, from the person or the platform's help page")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.path == "-":
        text = sys.stdin.read()
    else:
        with open(a.path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    limits = parse_limits(a.limit)
    rep = check(text, limits)
    found = {f["field"].lower() for f in rep["fields"]}
    missing = [k for k in limits if k.lower() not in found]
    if missing:
        # run 33A: a limit for a field that is not a "## " heading in the file is a typo, never a silent pass
        print(f"bad --limit: no field named {', '.join(repr(m) for m in missing)} in the file; fields are: {', '.join(f['field'] for f in rep['fields']) or 'none'}")
        return 2
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0
    for f in rep["fields"]:
        line = f"{f['field']}: {f['characters']} characters, {f['words']} words"
        if f["draft_labels"]:
            line += f"; without the draft labels: {f['final_characters']} characters, {f['final_words']} words"
        if "limit" in f:
            line += f", limit {f['limit']}" + (f", OVER by {f['over_limit_by']}" if f["over_limit_by"] else ", within limit")
        print(line)
        if f["placeholders_open"]:
            print(f"  placeholders still open: {f['placeholders_open']} (the count changes when they are filled)")
        if f["dashes"]:
            print(f"  dashes: {f['dashes']}")
        if f["numbers"]:
            print(f"  numbers: {', '.join(f['numbers'])}")
    if rep["label_conflicts"]:
        print("Check these: the same label carries different numbers across fields")
        for c in rep["label_conflicts"]:
            print(f"  {c['label']}: " + "; ".join(f"{v} in {', '.join(fs)}" for v, fs in c["values"].items()))
    else:
        print("No label carries two different numbers across fields.")
    for w in rep["weekday_errors"]:
        print(f"Date problem: {w['span']!r}: {w['problem']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
