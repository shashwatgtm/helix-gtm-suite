#!/usr/bin/env python3
"""Deterministic voice scan for text written for a reader.

Finds dashes, banned words and phrases, banned patterns, exclamation marks,
short fragments, emoji, Unicode bold, arrows and checkmarks, encoding errors
and wrong weekdays next to dates, line by line. Also reports word and
character counts and an approximate reading grade.

Standard library only. Reads a file path or "-" for stdin. Writes nothing.

Usage:
  python3 voice_scan.py draft.txt
  python3 voice_scan.py draft.txt --skip-quotes      # leave quoted source text alone
  python3 voice_scan.py draft.txt --json             # machine readable
  python3 voice_scan.py draft.txt --strict           # exit 1 when a "banned" flag exists
"""
import argparse
import datetime as _dt
import json
import re
import sys

# Severity "banned": always flag. Severity "review": flag for a human decision,
# because the word has a legitimate literal use.
BANNED_PHRASES = [
    # consolidated playbook voice list
    "game-changer", "game changer", "game-changing", "game changing", "leverage", "leveraging", "leveraged",
    "dive in", "dive into", "dive deep", "delve", "delves", "delving", "tapestry",
    "elevate", "elevated", "elevates", "unlock", "unlocks", "unlocking", "seamless", "seamlessly",
    "landed hard", "resonated", "resonates", "struck a chord", "genuine unlock", "genuinely", "honestly",
    "straightforward", "revolutionize", "revolutionise", "supercharge", "harness", "empower", "empowers",
    "in today's world", "in the ever-evolving landscape", "ever-evolving", "to the next level",
    "it's important to note", "testament to", "the rise of", "keep coming back to", "sat with me",
    "rubric", "move the needle", "here's the thing",
    # context bank list
    "groundbreaking", "revolutionary", "transformative", "comprehensive", "robust", "holistic",
    "synergy", "synergies", "paradigm shift",
    # event rulebook list
    "next-level", "next level",
    # stock openers
    "humbled to share", "humbled and honored", "thrilled to announce", "thrilled to share",
    "excited to announce", "excited to share",
]
REVIEW_WORDS = {
    "landscape": "allowed only as a domain modifier, for example 'competitive landscape'",
    "navigate": "banned for abstract things; fine for a literal route",
    "navigating": "banned for abstract things; fine for a literal route",
    "dynamic": "banned as praise; fine as a technical term such as 'dynamic pricing'",
    "mechanics": "banned as a vague label; fine when literal",
    "just": "banned as filler; keep only when it carries meaning",
    "thought leader": "never applied to oneself",
    "thought leadership": "never applied to oneself",
    "incredible": "hyperbole",
    "unprecedented": "hyperbole",
    "massive": "hyperbole",
    "mind-blowing": "hyperbole",
}

DASH_RE = re.compile(r"[\u2012\u2013\u2014\u2015]|(?<=\s)-(?=\s)|(?<=\w)--(?=\w)|\s--\s")
EXCLAIM_RE = re.compile(r"!")
URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMOJI_RE = re.compile("(?:(?![\u2713\u2714\u2705\u274C\u2611\u2612\u27A1])[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF\u2600-\u26FF\u2700-\u27BF])+\uFE0F?")
UNICODE_BOLD_RE = re.compile("[\U0001D400-\U0001D7FF]+")
ARROW_RE = re.compile("[\u2190-\u21ff\u27a1\u2b05-\u2b0d]|(?<!\\w)(?:->|=>)(?!\\w)")
CHECK_RE = re.compile("[\u2713\u2714\u2705\u274c\u2611\u2612]")
ENCODING_RE = re.compile("\ufffd|\u00e2\u20ac|\u00c3[\u0080-\u00bf]")
NOT_X_Y_RE = re.compile(
    r"\b(?:that|it|this)(?:'s|\u2019s| is| was)\s+not\b[^.!?\n]{1,80}[.!?]\s+(?:that|it|this)(?:'s|\u2019s| is| was)\b"
    r"|\b(?:that|it|this) (?:isn't|wasn't|isn\u2019t|wasn\u2019t)\b[^.!?\n]{1,80}[.!?]\s+(?:that|it|this)(?:'s|\u2019s| is| was)\b",
    re.IGNORECASE,
)
NOT_JUST_RE = re.compile(
    r"\b(?:not|no longer|isn't|aren't|wasn't|weren't|isn\u2019t|aren\u2019t|wasn\u2019t|weren\u2019t|don't|doesn't|didn't|don\u2019t|doesn\u2019t|didn\u2019t|do not|does not)\s+(?:just|only|merely|simply)\b"
    r"[^.!?\n;:\u2014\u2013]{1,80}(?:[.;:!?]|\s[\u2014\u2013]|\s-\s|,)\s*(?:but\s+)?(?:it|they|we|this|that|you)(?:'s|\u2019s|'re|\u2019re)?\b",
    re.IGNORECASE,
)
MONDAY_RE = re.compile(r"\b(?:start|starting|begin|try|do)\b[^.!?\n]{0,40}\b(?:on|from|this|next)\s+Monday\b|\bMonday morning\b", re.IGNORECASE)
OLD_NEW_RE = re.compile(r"\bold (?:thinking|way)\b[\s\S]{0,200}?\bnew (?:thinking|way)\b", re.IGNORECASE)
THOUGHT_LEADER_SELF_RE = re.compile(r"\b(?:I am|I'm|I\u2019m|as a|me as a|position me as a?)\s+(?:an?\s+)?thought leader", re.IGNORECASE)

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
WD_ABBR = {w[:3]: w for w in WEEKDAYS}
MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"])}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})
DATE_RES = [
    # Thursday, 13 May 2026 / Thu 13 May 2026
    re.compile(r"\b(?P<wd>mon|tue|wed|thu|fri|sat|sun)[a-z]*\.?,?\s+(?P<d>\d{1,2})(?:st|nd|rd|th)?\s+(?P<m>[a-z]{3,9})\.?,?\s+(?P<y>\d{4})\b", re.IGNORECASE),
    # Thursday, May 13, 2026
    re.compile(r"\b(?P<wd>mon|tue|wed|thu|fri|sat|sun)[a-z]*\.?,?\s+(?P<m>[a-z]{3,9})\.?\s+(?P<d>\d{1,2})(?:st|nd|rd|th)?,?\s+(?P<y>\d{4})\b", re.IGNORECASE),
]


def utf8_output():
    """Write UTF-8, so a rupee sign, a Unicode minus or a curly quote never stops the script on a Windows console or pipe
    set to code page 1252 (S2, version 1.0.2). A stream that cannot be reconfigured (a test buffer) is left as it is."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def weekday_errors(text):
    out = []
    for rx in DATE_RES:
        for m in rx.finditer(text):
            mon = MONTHS.get(m.group("m").lower()) or MONTHS.get(m.group("m").lower()[:3])
            if not mon:
                continue
            try:
                real = _dt.date(int(m.group("y")), mon, int(m.group("d"))).strftime("%A")
            except ValueError:
                out.append((m.group(0), "not a real date"))
                continue
            said = WD_ABBR.get(m.group("wd").lower()[:3], "").capitalize()
            if said and said != real:
                out.append((m.group(0), f"that date is a {real}"))
    return out


def mask_urls(line):
    """Blank out URLs so their characters are not read as prose."""
    return URL_RE.sub(lambda m: " " * len(m.group(0)), line)


def mask_quotes(line):
    """Blank out text inside double quotes so source quotes are not edited."""
    return re.sub(r"\"[^\"]*\"|\u201c[^\u201d]*\u201d", lambda m: " " * len(m.group(0)), line)


def count_syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee", "ye")) and n > 1:
        n -= 1
    return max(1, n)


def sentences_of(text):
    parts = re.split(r"(?<=[.!?])\s+|\n{2,}", text)
    return [p.strip() for p in parts if re.search(r"[A-Za-z]", p or "")]


def reading_grade(text):
    sents = sentences_of(text)
    words = re.findall(r"[A-Za-z][A-Za-z'\u2019-]*", text)
    if not sents or not words:
        return None
    syl = sum(count_syllables(w) for w in words)
    grade = 0.39 * (len(words) / len(sents)) + 11.8 * (syl / len(words)) - 15.59
    return round(grade, 1)


def band(grade):
    if grade is None:
        return "not enough text"
    if grade < 10:
        return "secondary school"
    if grade < 13:
        return "upper secondary"
    if grade < 17:
        return "graduate"
    return "above graduate"


def is_heading_or_label(line):
    s = line.strip()
    return s.startswith("#") or bool(re.match(r"^[A-Z][A-Za-z /]{0,30}:\s", s)) or s.startswith(("|", "-", "*", ">"))


def scan(text, skip_quotes=False):
    flags = []
    lines = text.splitlines()

    def add(n, kind, severity, span, rule):
        flags.append({"line": n, "kind": kind, "severity": severity, "span": span, "rule": rule})

    first_seen = second_seen = False
    for n, raw in enumerate(lines, 1):
        line = mask_urls(mask_quotes(raw) if skip_quotes else raw)
        # curly apostrophes (from word processors and social editors) match the
        # straight ones in the banned list; one character for one, so spans stay aligned
        low = line.lower().replace("’", "'").replace("‘", "'")
        lead = len(line) - len(line.lstrip())
        for m in DASH_RE.finditer(line):
            if m.group(0) == "-" and m.start() == lead:
                continue  # a markdown list marker, not a dash in prose
            add(n, "dash", "banned", raw[max(0, m.start() - 15):m.end() + 15].strip(), "no long, short or spaced dashes")
        for ph in BANNED_PHRASES:
            for m in re.finditer(r"(?<![\w-])" + re.escape(ph) + r"(?![\w-])", low):
                add(n, "banned word", "banned", raw[m.start():m.end()], f"banned word or phrase: {ph}")
        for w, why in REVIEW_WORDS.items():
            for m in re.finditer(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", low):
                add(n, "review word", "review", raw[m.start():m.end()], why)
        if THOUGHT_LEADER_SELF_RE.search(line):
            add(n, "self label", "banned", THOUGHT_LEADER_SELF_RE.search(line).group(0), "'thought leader' applied to oneself")
        for m in EXCLAIM_RE.finditer(line):
            add(n, "exclamation", "banned", raw[max(0, m.start() - 20):m.end()].strip(), "no exclamation marks in published text")
        for rx, kind, rule in (
            (EMOJI_RE, "emoji", "no emoji"),
            (UNICODE_BOLD_RE, "unicode bold", "no Unicode bold or italic letters"),
            (ARROW_RE, "arrow", "no arrows in prose"),
            (CHECK_RE, "checkmark", "no checkmarks or cross marks"),
            (ENCODING_RE, "encoding", "broken character encoding; ask for a clean copy"),
        ):
            for m in rx.finditer(line):
                add(n, kind, "banned", raw[max(0, m.start() - 10):m.end() + 10].strip(), rule)
        for m in MONDAY_RE.finditer(line):
            add(n, "lazy line", "banned", m.group(0), "lazy 'start on Monday' line")
        stripped = line.strip()
        if re.match(r"^first\b[,:]?", stripped, re.IGNORECASE):
            first_seen = n
        if re.match(r"^(second|secondly)\b[,:]?", stripped, re.IGNORECASE) and first_seen:
            second_seen = True
            add(n, "enumeration", "banned", stripped[:40], "no 'First... Second... Third...' enumeration in prose")
    joined = mask_urls(mask_quotes(text) if skip_quotes else text)
    for m in NOT_X_Y_RE.finditer(joined):
        n = joined[:m.start()].count("\n") + 1
        add(n, "not X, Y", "banned", m.group(0)[:90], "contrast LLMism: 'That's not X. That's Y'")
    for m in NOT_JUST_RE.finditer(joined):
        n = joined[:m.start()].count("\n") + 1
        add(n, "not X, Y", "banned", m.group(0)[:90], "contrast LLMism variant: 'not just X. They are Y'")
    for m in OLD_NEW_RE.finditer(joined):
        n = joined[:m.start()].count("\n") + 1
        add(n, "old/new", "review", m.group(0)[:60], "'Old thinking / New thinking' framing")
    # fragments and rhetorical questions, prose lines only
    prose_lines = [(i, l) for i, l in enumerate(lines, 1) if l.strip() and not is_heading_or_label(l)]
    last_para_line = prose_lines[-1][0] if prose_lines else 0
    for n, raw in prose_lines:
        line = mask_quotes(raw) if skip_quotes else raw
        for s in re.split(r"(?<=[.!?])\s+", line.strip()):
            words = re.findall(r"[A-Za-z0-9'\u2019]+", s)
            if 0 < len(words) <= 3 and s.endswith((".", "!")):
                add(n, "fragment", "review", s, "staccato fragment of 1 to 3 words")
            if s.endswith("?") and n != last_para_line:
                add(n, "question", "review", s[:80], "rhetorical question in the body; a real open question at the close is fine")
    for span, why in weekday_errors(text):
        n = text[:text.find(span)].count("\n") + 1
        add(n, "date", "banned", span, why)
    flags.sort(key=lambda f: (f["line"], f["kind"]))
    grade = reading_grade(mask_quotes(text) if skip_quotes else text)
    stats = {
        "characters": len(text.rstrip("\n")),
        "words": len(re.findall(r"\S+", text)),
        "sentences": len(sentences_of(text)),
        "approx_reading_grade": grade,
        "approx_band": band(grade),
        "banned_flags": sum(1 for f in flags if f["severity"] == "banned"),
        "review_flags": sum(1 for f in flags if f["severity"] == "review"),
    }
    return {"stats": stats, "flags": flags}


def main(argv=None):
    utf8_output()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="text file to scan, or - for stdin")
    ap.add_argument("--skip-quotes", action="store_true", help="ignore text inside double quotes (source quotes)")
    ap.add_argument("--json", action="store_true", help="print JSON")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any banned flag is found")
    a = ap.parse_args(argv)
    if a.path == "-":
        text = sys.stdin.read()
    else:
        with open(a.path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    res = scan(text, skip_quotes=a.skip_quotes)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        s = res["stats"]
        print(f"characters {s['characters']} | words {s['words']} | sentences {s['sentences']} | "
              f"approximate reading grade {s['approx_reading_grade']} ({s['approx_band']}, an estimate)")
        print(f"banned flags {s['banned_flags']} | review flags {s['review_flags']}")
        for f in res["flags"]:
            print(f"line {f['line']:>3} | {f['severity']:<6} | {f['kind']:<12} | {f['span']!r} | {f['rule']}")
        if not res["flags"]:
            print("no flags")
    if a.strict and res["stats"]["banned_flags"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
