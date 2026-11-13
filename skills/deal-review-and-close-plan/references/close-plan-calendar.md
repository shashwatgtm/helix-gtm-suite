# Close plan calendar, account plan dates and weekday checks: the method

This file states the date calculations exactly, so the same inputs always give the same dates. There are three jobs: the working day close plan, the 30, 60 and 90 day account plan dates, and the weekday check for any suggested date. Work them out with your own code execution, following these rules to the letter. With no code execution, give no computed calendar, weekday or count of weeks (SKILL.md, Platform mode): use the user's own dates or "to be set with the buyer", and you may show the formula the dates will follow. Never write a weekday by mental arithmetic. Every phase weight, account plan offset and warning threshold below is an example default the user can change; none is a benchmark.

## 1. Shared rules

### Dates
- Every date is written YYYY-MM-DD: four digits, two digits, two digits. Spaces at either end are ignored. Any other form (31/12, "Friday next week") is first turned into a calendar date and confirmed with the user, then used.
- A date that does not exist (2027-02-30, 2026-13-01) is refused, never rolled over to another day.
- A date, or a date plus a number of days, past the year 9999 is refused.

### Today
- Today is the date the user states, or the real current date when they state none. Write the date used in the answer.

### Working days
- A working day is Monday to Friday and not one of the user's holidays.
- Saturday and Sunday are never working days.
- Holidays are dates the user gives, each a real YYYY-MM-DD date. No public holiday is ever assumed.
- Moving forward: from a date that is not a working day, step one calendar day later until a working day is reached. Moving back: the same, one calendar day earlier each step. A working day does not move.

### How a date is written in text
- Long form, in the close plan header: `2026-10-14 (Wednesday 14 October 2026)`, the weekday and month in full, the day without a leading zero.
- Short form, everywhere else: the YYYY-MM-DD date, with the weekday in full where the line shape below shows it.

## 2. The close plan

### Inputs

| Input | Allowed values | When not given |
|---|---|---|
| close | the target close date | refused: give the target close date |
| today | a date (section 1) | the real current date |
| stage | discovery, evaluation, proposal, negotiation, procurement | evaluation (always give it; never rely on this default) |
| sector | logistics tech, logistics, fintech, saas, vertical saas, ai native, ites, telecom, software, cybersecurity, investment, other (case ignored) | other |
| holidays | a list of dates | none |
| owner led | yes, only when the buyer's owner signs and the buyer has no procurement step | no |
| weights | the user's own weight for any phase in this plan | example defaults |
| steps | the buyer's steps, as a list of step names per phase in this plan | no milestones |

### Refusals (checked in this order)
1. The close date is missing, written in the wrong form, or does not exist.
2. The close date, as given, is before today: refused, "the close date <close> is in the past (today is <today>); give a future date". A close date equal to today is allowed.
3. The stage or the sector is not one of the allowed values.
4. A holiday is not a real date.
5. A weight names a phase not in this plan, or is not a number above 0 (0, a negative number, true or false are refused).
6. A step list names a phase not in this plan, or is empty, or holds an item that is not text with words in it.
7. Fewer working days than phases (step 4 below): refused, "only <n> working days from <start> to <close> for <p> phases (<phases>): move the close date, or start from a later stage".

Pass any refusal on as written, starting "BAD INPUT:", and ask for what is needed. Never plan to a refused date.

### Step 1. Start and close
- Start = today, moved forward to a working day.
- Close = the close date, moved back to a working day.
- Notes, in this order, only when they apply: "the close date <given close> is not a working day, so it moved back to <close>"; "today <today> is not a working day, so the plan starts on <start>".

### Step 2. Phases
- The phases run from the plan stage to the end of this list: discovery, evaluation, proposal, negotiation, procurement; then "close" is always added last.
- Owner led: drop negotiation and procurement, and add the note "owner led: negotiation and procurement phases dropped (the owner signs, no procurement step)".
- Map a deal stage to the plan stage: prospecting or discovery is discovery; demo, proof of concept or evaluation is evaluation; proposal is proposal; negotiation is negotiation; closing is procurement; stuck is the stage it is stuck in, mapped the same way.

### Step 3. Weights (example defaults)

| Phase | Example default weight |
|---|---|
| evaluation | 4; 5 when the sector is ites, telecom or investment |
| discovery, proposal, negotiation, procurement | 2 |
| close | 1 |

A weight the user gives replaces the default for that phase and is labelled "your value"; it may have decimals. Do not tell the user which sectors get the larger evaluation weight; say only that phase weights are example defaults.

### Step 4. Working days in the plan
- n = the number of working days from start to close, counting both ends.
- p = the number of phases, including close.
- Calendar days = the number of calendar days from start to close, counting both ends.
- When n is less than p, refuse (refusal 7).

### Step 5. Phase lengths
1. W = the sum of the weights of all phases, close included.
2. Floor: 2 when n is at least 2 x p; otherwise 1.
3. For each phase except close, in order: length = n x (the phase weight) / W, rounded to the nearest whole number, then raised to the floor if it is lower. Work with exact fractions, never a shortened decimal. An exact half rounds to the even neighbour: 2.5 becomes 2, 3.5 becomes 4, 8.5 becomes 8, 9.5 becomes 10.
4. While these lengths add up to more than n minus 1 (close must keep at least one day): take the longest phase (the first one in plan order when several share the longest length) and take one day off it. Stop when the sum is n minus 1 or less, or when the longest phase is down to 1 day.
5. Close = n minus the sum of the other lengths.

### Step 6. Phase dates
List the n working days from start to close in order. The first phase takes the first lengths-worth of days, the next phase the next ones, and so on; close takes the rest. Each phase runs from its first to its last working day.

### Step 7. Milestones
For a phase of length L with m steps (in the order given), step k (k = 1 to m) is due on working day number ceiling(k x L / m) of that phase, counting the phase's first working day as day 1. The last step always lands on the phase's last day. When there are more steps than days, several steps share a day.

### Step 8. Warnings (example default thresholds)
- n under 10: "only <n> working days to the close: under 10 working days (example default threshold); agree with the buyer which steps can run in parallel".
- An evaluation phase under 8 working days: "evaluation has <days> working days, under 8 (example default threshold): confirm the buyer can finish the evaluation in that time".

### The printed plan, line by line

```
Close plan: <n> working days from <start, long form> to <close, long form> (<calendar days> calendar days).
Holidays removed: <each user holiday from start to close, both ends counted, in date order, joined by ", ">
- <phase>: <L> working days, <first day> to <last day> (weight <weight>, <example default | your value>)
    due <date> (<weekday>): <step>
WARNING: <warning>
Note: <note>
Phase weights are example defaults you can change (give your own weights), not a benchmark; the buyer's own steps and dates win.
```

- The Holidays removed line appears only when at least one user holiday falls from start to close.
- One phase line per phase, in plan order; "working day" without the s when L is 1. The weight is written as given.
- Each milestone line starts with four spaces and sits under its phase.
- WARNING lines in the order of step 8, then Note lines in the order the notes were made (close moved, start moved, owner led), then the closing line.

### Worked example (from SKILL.md, Example 1)
Inputs: today 2026-10-14, close 2026-11-27, stage proposal, sector fintech, no holidays; steps: proposal (proposal reviewed with the champion; business case to the CFO), negotiation (terms agreed), procurement (vendor registration; security questionnaire returned; questionnaire reviewed; questionnaire approved), close (signature).

1. Start: Wednesday 14 October is a working day. Close: Friday 27 November is a working day.
2. Phases: proposal, negotiation, procurement, close. p = 4.
3. Weights: 2, 2, 2, 1. W = 7.
4. n: 14 to 16 October is 3 days, then five full weeks from 19 October to 20 November is 25 days, then 23 to 27 November is 5 days: 33 working days. Calendar days: 14 October to 27 November is 45.
5. Floor 2, since 33 is at least 8. Each of the three phases: 33 x 2 / 7 = 66 / 7 = 9.43, rounded to 9. Sum 27, which is not more than 32, so nothing is trimmed. Close: 33 minus 27 = 6.
6. Proposal: 14 to 26 October (14, 15, 16, 19, 20, 21, 22, 23, 26). Negotiation: 27 October to 6 November. Procurement: 9 to 19 November. Close: 20 to 27 November.
7. Proposal, L 9, m 2: ceiling(9 / 2) = 5, the 5th working day, Tuesday 20 October; ceiling(18 / 2) = 9, Monday 26 October. Negotiation, L 9, m 1: day 9, Friday 6 November. Procurement, L 9, m 4: ceiling(9 / 4) = 3, Wednesday 11 November; ceiling(18 / 4) = 5, Friday 13 November; ceiling(27 / 4) = 7, Tuesday 17 November; day 9, Thursday 19 November. Close, L 6, m 1: day 6, Friday 27 November.
8. No warning: 33 is not under 10, and there is no evaluation phase.

```
Close plan: 33 working days from 2026-10-14 (Wednesday 14 October 2026) to 2026-11-27 (Friday 27 November 2026) (45 calendar days).
- proposal: 9 working days, 2026-10-14 to 2026-10-26 (weight 2, example default)
    due 2026-10-20 (Tuesday): proposal reviewed with the champion
    due 2026-10-26 (Monday): business case to the CFO
- negotiation: 9 working days, 2026-10-27 to 2026-11-06 (weight 2, example default)
    due 2026-11-06 (Friday): terms agreed
- procurement: 9 working days, 2026-11-09 to 2026-11-19 (weight 2, example default)
    due 2026-11-11 (Wednesday): vendor registration
    due 2026-11-13 (Friday): security questionnaire returned
    due 2026-11-17 (Tuesday): questionnaire reviewed
    due 2026-11-19 (Thursday): questionnaire approved
- close: 6 working days, 2026-11-20 to 2026-11-27 (weight 1, example default)
    due 2026-11-27 (Friday): signature
Phase weights are example defaults you can change (give your own weights), not a benchmark; the buyer's own steps and dates win.
```

## 3. The 30, 60 and 90 day account plan dates

### Inputs
- today: a date (section 1); the real current date when not given. The start of the account plan is today itself, not moved.
- offsets: whole numbers of calendar days, each 1 or more, in increasing order with no repeats. Example default: 30, 60, 90. The user's own offsets are labelled "your value". Anything else (0, a decimal, a repeat, a smaller number after a larger one, an empty list) is refused: "offsets must be increasing whole days of 1 or more".

### Rule
For each offset: the date = today plus that many calendar days. When it falls on a Saturday or Sunday, move it back to the Friday before. Holidays are not applied to account plan dates.

### The printed dates, line by line

```
Account plan dates (start <today>):
- day <offset> (<example default | your value>): <due date> <weekday>
- day <offset> (<label>): <due date> <weekday>, moved back from <date before moving> (weekend)
The 30, 60 and 90 day offsets are example defaults you can change (give your own offsets).
```

The ", moved back from ..." part appears only on a date that moved. The closing line is the same whichever offsets were used.

Example: start 2026-10-14. Day 30: 2026-11-13 Friday. Day 60: 2026-12-13 is a Sunday, so 2026-12-11 Friday, moved back from 2026-12-13 (weekend). Day 90: 2027-01-12 Tuesday.

## 4. The weekday check for suggested dates

Use it for every suggested action date outside a close plan. Dates inside a close plan take their weekday from the plan.

### Inputs
- dates: one or more dates. No dates at all is refused: "0 dates given (a check that reads 0 items fails)". A date that does not exist, or a blank entry in the list, is refused.
- today: a date (section 1); the real current date when not given.
- holidays: a list of dates, optional.

### Rule, for each date in the order given
1. Its weekday.
2. Whether it is a working day (section 1). When it is not, the next working day, moving forward, and whether the date is one of the user's holidays.
3. Whether it is before today: "in the past". Today itself is not in the past.

### The printed lines, one per date

```
<date> <weekday>
<date> <weekday> (not a working day; next working day <date> <weekday>)
<date> <weekday> (not a working day, your holiday; next working day <date> <weekday>)
<date> <weekday> (in the past: today is <today>)
```

The "in the past" part is added after the working day part when both apply, for example `2026-10-17 Saturday (not a working day; next working day 2026-10-19 Monday) (in the past: today is 2026-10-18)`.

## 5. Shape for programmatic use
When a structured result is asked for, return the same facts as fields, in the same order every time:
- Close plan: today, start, close, working_days, calendar_days, holidays_removed, phases (each with phase, days, start, end, weight, weight_source and milestones, each milestone with step and due), warnings, notes, and the label "phase weights are example defaults unless marked your value; dates are working days Monday to Friday minus your holidays".
- Account plan: today, milestones (each with offset_days, offset_source, due, weekday and moved_from, empty when the date did not move), and the label "offsets are example defaults unless marked your value".
- Weekday check: today, dates (each with date, weekday, working_day, next_working_day, empty when it is a working day, holiday and past), and the label "working days are Monday to Friday minus your holidays".
