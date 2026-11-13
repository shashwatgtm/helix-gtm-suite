# Deal health score: the method

This file states the deal health calculation exactly, so the same facts always give the same score, status and printed block. Work it out with your own code execution when it is available, following these rules to the letter; by hand otherwise, showing the formula. Every point value, stage threshold and band below is an example default the user can change; none is a benchmark. A value the user gives is labelled "your value"; every other value is labelled "example default".

## 1. Inputs for one deal

Every field is optional except stage. A field that is absent or empty (null) is "not given". Any field not listed here is ignored.

| Field | Allowed values | When not given |
|---|---|---|
| name (or deal_name) | any text, used only on the "Deal:" line | "(no name)" |
| stage | prospecting, discovery, demo, proposal, negotiation, closing, stuck | refused: the score cannot run without it |
| stuck_in | prospecting, discovery, demo, proposal, negotiation, closing; read only when stage is stuck | days in stage is not scored (rule 3.4) |
| days_in_stage | a number, 0 or more | not scored, never read as 0 |
| champion | multi_threaded, confirmed, potential, none | not scored |
| economic_buyer | engaged, named, unknown, or the seller's own phrase | scored as unknown |
| economic_buyer_said | the seller's own words about the economic buyer, copied exactly | nothing printed from it |
| competitors | a list of entries, each with a name and incumbent true or false; or a phrase | none (+0) |
| blockers | a list of text items, or a phrase | none (+0) |

Accepted spellings for champion, after trimming spaces and ignoring case: multi_threaded or multi-threaded; confirmed or confirmed_champion; potential or potential_champion; none or no_champion. Any other value is refused.

Many deals are given as one list of deals. The deals are scored one by one, in the order given, with the same points and thresholds.

## 2. Example default values

### Points

| Key | Meaning | Example default |
|---|---|---|
| start | every deal starts here | 70 |
| champion_multi_threaded | two or more champions pass the champion test | +15 |
| champion_confirmed | one champion passes the test | +10 |
| champion_potential | someone does one or two of the three | 0 |
| champion_none | nobody | -20 |
| buyer_engaged | economic buyer engaged | +10 |
| buyer_named | economic buyer named, not engaged | +5 |
| buyer_unknown | economic buyer unknown, or not given | -10 |
| over_threshold | days in stage over the stage threshold | -5 |
| over_twice_threshold | days in stage more than twice the threshold | -15 |
| incumbent | an incumbent competitor in the deal | -10 |
| other_competitor | another competitor, no incumbent | -5 |
| blockers | at least one known blocker | -10 |
| at_risk_below | a score below this is At Risk | 50 |
| needs_attention_below | a score below this, and not At Risk, is Needs Attention | 70 |

### Stage thresholds (days in stage)

| Stage | Example default |
|---|---|
| prospecting | 14 |
| discovery | 21 |
| demo | 14 |
| proposal | 21 |
| negotiation | 30 |
| closing | 14 |

### The user's own values
- The user may replace any point value or any threshold. Only the keys in the two tables above can be replaced; an unknown key is refused and the known keys are named.
- Each replacement must be a real number. A point value may be negative or have decimals. A threshold must be 0 or more.
- A replaced value is labelled "your value" on every line that uses it.

## 3. Scoring rules, in order

Start the running total at the start value. Write the factor lines in this order: start, champion, economic buyer, days in stage, competitors, blockers, then the raw total line when it applies. Keep a "missing" list in the order the items are found.

### 3.1 Start
Line: `start +70 (example default)`.

### 3.2 Champion
- Not given: add nothing. Line: `champion: not given (not scored; tell me multi_threaded, confirmed, potential or none)`. Add "champion" to the missing list.
- Given: add its points. Line: `champion <state>: <points> (<label>)`, where the state is written with spaces, not underscores: "multi threaded", "confirmed", "potential", "none".

### 3.3 Economic buyer
Step A, choose the text to read. If economic_buyer is not given or is only spaces, and economic_buyer_said holds words, read economic_buyer_said instead. economic_buyer_said, when given, must be text; anything else is refused.

Step B, the state, from the chosen text:
1. Not given, or only spaces: state unknown, and add "economic buyer (scored as unknown)" to the missing list.
2. Otherwise trim it and ignore case. Exactly "engaged", "named" or "unknown": that state.
3. Exactly "none", "tbd" or "n/a", or the text says unknown (rule 3.7): unknown.
4. Otherwise: engaged if the word "engaged" appears un-negated (rule 3.8); named in every other case. So "disengaged", "not engaged", "no longer engaged" and "has not been engaged" are all named.

Step C, the conflict check. It runs only when economic_buyer itself was given (not only spaces) and economic_buyer_said also holds words. Read economic_buyer_said:
- it reads as not engaged when the whole word "disengaged" appears, or the word "engaged" appears but every time it is negated;
- it reads as engaged when the word "engaged" appears un-negated at least once;
- it reads as unknown when it says unknown (rule 3.7).

Refuse when the state from Step B is engaged and economic_buyer_said reads as not engaged or unknown, or when the state is named or unknown and economic_buyer_said reads as engaged. Ask the seller which is right.

Step D, points and line. engaged +10, named +5, unknown -10 (example defaults). The state is shown as "engaged", "named, not engaged" or "unknown". The source in brackets is `you said: "<economic_buyer_said, trimmed>"` when economic_buyer_said holds words; otherwise `from: <economic_buyer exactly as given>`, or `from: not given` when it was not given.

Line: `economic buyer <shown state> (<source>): <points> (<label>)`.

### 3.4 Days in stage
- The stage to compare against is the deal's stage; for a stuck deal it is stuck_in. When the stage is stuck and stuck_in is given, stuck_in must be one of the six stages, or it is refused (this check comes first, even when days in stage is not given).
- Days not given: add nothing. Line: `days in stage: not given (not scored)`. Add "days in stage" to the missing list.
- Days given: they must be a number (true or false is not a number), and a negative number is refused, never read as positive.
- Stuck with no stuck_in, days given: add nothing. Line: `days in stage <days>: not scored, because a stuck deal needs the stage it is stuck in (stuck in which stage? give stuck_in)`. Add "the stage the deal is stuck in" to the missing list.
- Otherwise compare with that stage's threshold T:

| Test | Points | Line |
|---|---|---|
| days more than 2 x T | over_twice_threshold, -15 | `<days> days in <stage>, more than twice the threshold of <T> days (<T label>): -15 (<label>)` |
| days more than T, up to 2 x T | over_threshold, -5 | `<days> days in <stage>, over the threshold of <T> days (<T label>): -5 (<label>)` |
| days equal to T or less | 0 | `<days> days in <stage>, within the threshold of <T> days (<T label>): +0` |

Days exactly equal to T are within; days exactly 2 x T are "over", not "more than twice". The days and T are written as given.

### 3.5 Competitors
- Not given, empty text or an empty list: none.
- A list: every entry must be an object (a name and an incumbent flag); incumbent, when present, must be true or false. Incumbent when any entry has incumbent true; otherwise other.
- A phrase: none when the whole phrase says none (rule 3.9); incumbent when the word "incumbent" appears un-negated (rule 3.8); otherwise other. A phrase of only spaces is not empty text, so it counts as other.
- Any other kind of value is refused.

| Result | Points | Line |
|---|---|---|
| incumbent | -10 | `incumbent competitor: -10 (<label>)` |
| other | -5 | `other competitor in the deal: -5 (<label>)` |
| none | 0 | `competitors: none given (+0)` |

Only one competitor line is ever written; an incumbent and other vendors together score the incumbent points only.

### 3.6 Blockers
- Not given, empty text or an empty list: none.
- A list: every item must be text. Blockers present when at least one item holds words.
- A phrase: blockers present when it holds words and the whole phrase does not say none (rule 3.9).
- Any other kind of value is refused.

| Result | Points | Line |
|---|---|---|
| present | -10 | `known blockers: -10 (<label>)` |
| none | 0 | `blockers: none given (+0)` |

### 3.7 "Says unknown"
The text, in lower case, says unknown when any of these appears as whole words: "unknown"; "unclear"; "no idea"; "not sure who"; "do not know", "don't know" or "dont know"; "not named", "not identified", "not known" or "not found", each also with "yet" after "not" ("not yet named").

### 3.8 An un-negated word
Split the text, in lower case, into words: a word is a run of the letters a to z and the straight apostrophe ('). Every other character, including a space, a hyphen, a digit, a curly apostrophe and any letter outside a to z, splits words. The target word is un-negated at a place where it appears as a whole word and none of the up to five words before it is one of: not, no, never, longer, nobody, isn't, hasn't, wasn't, hadn't, haven't, aren't, un, barely. One un-negated place is enough.

Because only the straight apostrophe joins a word, "hasn’t" written with a curly apostrophe splits into "hasn" and "t" and does not negate.

### 3.9 "Says none" (for a whole phrase)
Ignore case, spaces at either end and one final full stop. The whole phrase is one of: "none", "nil", "na", "n/a"; "nothing" or "nothing known"; "no blocker", "no blockers", "no competitor", "no competitors", "no competition", "no objection", "no objections", "no one", each also with "known" after "no" ("no known blockers"). Anything longer, such as "no blockers so far", is not none.

## 4. Total, clamp and status

1. Raw total = start plus every point added above.
2. Score = the raw total kept inside 0 to 100: below 0 becomes 0, above 100 becomes 100. When the score differs from the raw total, add the line `raw total <raw total> kept inside 0 to 100` after the blockers line.
3. Status, from the score: below at_risk_below (50) is At Risk; otherwise below needs_attention_below (70) is Needs Attention; otherwise Healthy. A score of exactly 50 is Needs Attention; exactly 70 is Healthy.

No rounding is done. Whole numbers are written without a decimal point. A user's decimal point value is written with its decimals ("+2.5"), and the score then carries them ("62.5").

## 5. How points are written
- Every point value carries its sign: +15, +10, +5, -5, -10, -15, -20. Zero is written "+0".
- Each scored line ends with its label in brackets: "(example default)" or "(your value)".
- The threshold in a days line carries its own label in its own brackets, then the points label.

## 6. The printed block

For each deal, in this order:

```
Deal: <name, or (no name)>
Score: <score> of 100
Status: <At Risk | Needs Attention | Healthy> (bands: below <at_risk_below> At Risk, below <needs_attention_below> Needs Attention; <label of at_risk_below>)
INCOMPLETE: not scored because not given: <missing items joined by ", ">. Read the score and status as provisional until these are known.
  <factor line>
  <factor line>
  ...
<one empty line>
```

- The INCOMPLETE line appears only when the missing list is not empty.
- Each factor line starts with two spaces.
- The band label on the Status line is the label of at_risk_below only: "example default" unless the user gave at_risk_below.

After the last deal, one closing line:

`Every point value, threshold and band above is an example default you can change (give your own points or thresholds), not a benchmark.`

The block quoted in the answer runs from the "Score:" line to the last factor line, copied line for line. The "Deal:" line and the closing line may be left out whole.

### Worked example (from SKILL.md, Example 1)
Facts: stage proposal, days_in_stage 26, champion confirmed, economic_buyer named with economic_buyer_said "the CFO is named but has not been engaged yet", one competitor with incumbent true, one blocker. Arithmetic: 70 plus 10 plus 5, minus 5, minus 10, minus 10 = 60. 26 is more than 21 and not more than 42, so -5. 60 is not below 50 and is below 70: Needs Attention.

```
Score: 60 of 100
Status: Needs Attention (bands: below 50 At Risk, below 70 Needs Attention; example default)
  start +70 (example default)
  champion confirmed: +10 (example default)
  economic buyer named, not engaged (you said: "the CFO is named but has not been engaged yet"): +5 (example default)
  26 days in proposal, over the threshold of 21 days (example default): -5 (example default)
  incumbent competitor: -10 (example default)
  known blockers: -10 (example default)
```

## 7. Refusals

A refusal stops the work and is passed on as written, starting "BAD INPUT:". No score is shown for a refused deal and no value is guessed.

| Situation | Message |
|---|---|
| stage missing or not one of the seven | stage must be one of prospecting, discovery, demo, proposal, negotiation, closing, stuck, got <value> |
| stuck_in not one of the six stages | stuck_in must be one of prospecting, discovery, demo, proposal, negotiation, closing, got <value> |
| champion not an accepted value | champion must be multi_threaded, confirmed, potential or none, got <value> |
| economic_buyer not text | economic_buyer must be text, got <value> |
| economic_buyer_said not text | economic_buyer_said must be text (the seller's own words), got <value> |
| economic_buyer and economic_buyer_said conflict (rule 3.3 Step C) | economic_buyer <value> and economic_buyer_said <value> conflict: check with the seller which is right, then pass the state that matches their words |
| days_in_stage not a number, or not a real number | days_in_stage must be a number, got <value> (or: must be a real number) |
| days_in_stage negative | days_in_stage must be 0 or more, got <value> |
| competitors a list with an entry that is not an object | competitors must be a list of objects like {"name": "...", "incumbent": true}, or a phrase |
| a competitor's incumbent flag not true or false | competitors[].incumbent must be true or false |
| competitors neither a list nor a phrase | competitors must be a list or a phrase |
| blockers a list with an item that is not text | blockers must be a list of text items or a phrase |
| blockers neither a list nor a phrase | blockers must be a list or a phrase |
| a deal that is not a set of fields | each deal must be an object, got <value> |
| the list of deals is not a list | deals must be a list |
| an empty list of deals | 0 deals given: nothing to score (a check that reads 0 items fails) |
| a user point or threshold key that does not exist | unknown key in points (or thresholds): <key> (known: <the keys>) |
| a user point or threshold that is not a real number | points.<key> (or thresholds.<key>) must be a number, got <value> |
| a user threshold below 0 | thresholds.<key> must be 0 or more, got <value> |

In a list of many deals, a refusal in one deal refuses the run and names the deal by its place and name, for example "deal 2 (B): champion must be ...". Fix or drop that deal with the user's word and score the rest; never drop a deal silently.

## 8. Shape for programmatic use
When a structured result is asked for, return one object with two keys: "deals", a list with one entry per deal holding name (empty text when none), score, status, factors (the factor lines without the two leading spaces) and missing (the missing list); and "note", the text "every point value, threshold and band is an example default unless marked your value".
