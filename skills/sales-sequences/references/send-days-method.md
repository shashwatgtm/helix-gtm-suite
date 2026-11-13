# Send days and draft check: the method

This file sets out two fixed calculations: "days" (the send days and dates of a sequence) and "check" (the counts and dash check of a drafted sequence). Follow the rules exactly. When code execution is available, write your own calculation from these rules and run it; otherwise work it out by hand and say "counted by hand per the method". Either way the printed lines must match the shapes below character for character.

Nothing here is a benchmark. The send days per type are example defaults; the user's own days and count always win. Event follow up and nurture sequences are not written by this skill (b2b-events-pr-and-launches / event-follow-up-engine).

## Part 1. Days

### Inputs

| Input | Required | Meaning |
|---|---|---|
| type | yes | One of cold_outreach, warm_follow_up, post_demo, proposal_follow_up, referral_request, re_engagement. |
| the user's days | no | Whole days, in order, for example 1, 4, 9. |
| the user's count | no | How many emails. |
| start date | no | The trigger day (the demo, the proposal, the day the sequence is planned), written YYYY-MM-DD. |
| first send date | no | The date the first email goes out, written YYYY-MM-DD. |

Give a start date or a first send date, never both. With neither, the output has no dates, only the days.

### Example default send days

| Type | Example default days | Emails |
|---|---|---|
| cold_outreach | 1, 3, 7, 12, 17 | 5 |
| warm_follow_up | 0, 3, 7 | 3 |
| post_demo | 0, 2, 5, 10 | 4 |
| proposal_follow_up | 1, 3, 7, 12 | 4 |
| referral_request | 1, 4, 9 | 3 |
| re_engagement | none: the user sets the days | none |

Day N means N calendar days after the start date. Day 0 is the start date itself.

### Rules, in this order

Stop at the first rule that refuses. A refusal is printed as one line that starts "BAD INPUT: " and nothing else is printed.

1. Type is event_follow_up or nurture: refuse with `BAD INPUT: <type> sequences are not written by this skill: use b2b-events-pr-and-launches / event-follow-up-engine`.
2. Type is not one of the six types in the table: refuse with `BAD INPUT: the type must be one of cold_outreach, warm_follow_up, post_demo, proposal_follow_up, referral_request, re_engagement, got '<type>'`.
3. A count is given: with spaces around it removed it must be made of digits only and be 1 or more. Otherwise refuse with `BAD INPUT: the count must be a whole number of 1 or more, got '<count as given>'`.
4. The user gave days:
   1. Split the days at each comma and remove spaces around each piece. If the whole entry is empty, or any piece is not a whole number (digits, with an optional minus sign in front), refuse with `BAD INPUT: the days must be whole days separated by commas, for example 1,3,7, got '<days as given>'`. An empty piece, as in 1,,3, is refused here.
   2. Any day below 0: refuse with `BAD INPUT: the days cannot hold a negative day, got <days as given> (the minus sign is kept and refused)`.
   3. Each day must be larger than the one before it. Otherwise refuse with `BAD INPUT: the days must increase from one email to the next, got <days as given>`.
   4. A count is also given and it differs from the number of days: refuse with `BAD INPUT: the count <count> does not match the <number of days> days given in the days`. This is the count and days mismatch refusal: never pick one for the user.
   5. The days are the user's, written as whole numbers (leading zeros dropped, so 07 is written 7). The source label is "your value".
5. The user gave no days:
   1. Type is re_engagement: refuse with `BAD INPUT: re_engagement has no example default send days: give your own days, for example 1,8,20`.
   2. A count is given and it is larger than the number of example default days for the type: refuse with `BAD INPUT: you asked for <count> emails; the example default for <type> has <number of default days> send days: give your own days with <count> days`.
   3. The days are the first <count> example default days for the type (all of them when no count is given). The source label is "example default".
6. The count of emails is the number of days.
7. Both a start date and a first send date are given: refuse with `BAD INPUT: give the start date (the trigger day) or the first send date (the date of the first email), not both`.
8. The date given (start or first send) must be written as four digits, a hyphen, two digits, a hyphen, two digits, after spaces around it are removed. Otherwise refuse with `BAD INPUT: <option> must be a date written YYYY-MM-DD, got '<date as given>'`. If it has that shape but is not a real calendar date (for example 2026-02-30), refuse with `BAD INPUT: <option> '<date>' is not a real calendar date (refused, never rolled over)`. In both lines, <option> is `the start date` for a start date and `the first send date` for a first send date.

Print these refusal lines and the closing label line below exactly as written here.

### Working out the dates

Only when a start date or a first send date is given.

1. With a first send date: if it falls on a Saturday or Sunday, move it forward one day at a time until it is a Monday to Friday; note the date as given, because the first email will say it was moved from it. The start date is then this (possibly moved) first send date minus the first day number. Example: first send Monday 19 October 2026 and first day 1 give start Sunday 18 October 2026. So the first email lands on the first send date and the later emails keep the same gaps in days from it.
2. With a start date: use it as given (it may be a weekend day; it is not itself a send day).
3. For each day, in order:
   1. The wanted date is the start date plus that many calendar days.
   2. Begin at the wanted date. While the date is a Saturday or a Sunday, or it is on or before the date already given to the previous email, move it forward one day. The result is this email's send date. So weekend dates move to the next working day, and two emails never share a date (the later one moves to the next working day).
   3. If the send date differs from the wanted date, the email is "moved from" the wanted date.
   4. For the first email with a first send date that was moved off a weekend, the "moved from" date is the first send date as the user gave it.
   5. The weekday label is the full English name of the send date's weekday: Monday, Tuesday, Wednesday, Thursday, Friday.
4. If any date needed falls outside the years 1 to 9999, refuse with `BAD INPUT: a send date goes past the year 9999; give a nearer start date or fewer days`.

Check every weekday by calculation (a calendar function in code execution, or a calendar read by hand), never by memory.

### Printed output (text)

Line by line:

| Line | Exact shape | When |
|---|---|---|
| 1 | `<type>: <count> emails on days <day 1>, <day 2>, ... (<source label>)` | Always. Days are joined by a comma and one space. "emails" stays plural even for 1. The source label is "example default" or "your value". |
| One per email | `- day <N>: <YYYY-MM-DD> <Weekday>` | Only when a start or first send date was given, in day order. |
| Same line, added | ` (moved from <YYYY-MM-DD>)` | Added to the end of an email's line when its send date was moved. |
| Last | `These send days are example defaults you can change (give your own days), not a benchmark.` | Only when the source label is "example default". |

### Printed output (JSON, for API or programmatic use)

One object, indented by one space per level, every list item and every key on its own line, in this key order:

| Key | Value | When |
|---|---|---|
| type | the type, as text | always |
| days | the list of day numbers | always |
| days_source | "example default" or "your value" | always |
| count | the number of emails | always |
| first_send | the (possibly moved) first send date, YYYY-MM-DD | only with a first send date |
| start | the start date, YYYY-MM-DD | only with a start or first send date |
| sends | a list with one object per email: day (number), date (YYYY-MM-DD), weekday (full English name), moved_from (the date it moved from, or null) | only with a start or first send date |

The JSON output has no closing label line.

### The worked example, walked through

Input: cold_outreach, count 4, first send date 2026-10-19 (Monday 19 October 2026).

Days: the first 4 example default days, 1, 3, 7, 12; source "example default". The first send date is a Monday, so it is not moved. Start date = 19 October minus 1 day = Sunday 18 October 2026.

| Day | Wanted date | Rule applied | Send date |
|---|---|---|---|
| 1 | 2026-10-19 Monday | working day, after no earlier email | 2026-10-19 Monday |
| 3 | 2026-10-21 Wednesday | working day, after 19 October | 2026-10-21 Wednesday |
| 7 | 2026-10-25 Sunday | weekend, moved to the next working day | 2026-10-26 Monday (moved from 2026-10-25) |
| 12 | 2026-10-30 Friday | working day, after 26 October | 2026-10-30 Friday |

Printed text, line by line:

| Line | Text |
|---|---|
| 1 | `cold_outreach: 4 emails on days 1, 3, 7, 12 (example default)` |
| 2 | `- day 1: 2026-10-19 Monday` |
| 3 | `- day 3: 2026-10-21 Wednesday` |
| 4 | `- day 7: 2026-10-26 Monday (moved from 2026-10-25)` |
| 5 | `- day 12: 2026-10-30 Friday` |
| 6 | `These send days are example defaults you can change (give your own days), not a benchmark.` |

## Part 2. Check

### Input

The drafted sequence as plain text, read as UTF-8. If it cannot be read, refuse with `BAD INPUT: cannot read <file>: <reason>`.

### Splitting the draft into emails

1. Break the text into lines at every line break.
2. A line is a subject line when, after any white space at its start, it begins with the word "subject" in any mix of capitals, then any white space, then a colon. The subject is everything after the colon, with white space at both ends removed. "Subject:", "subject :" and "SUBJECT:" all count; "Subject line:" does not.
3. Each subject line starts a new email. Every line after it, up to the next subject line or the end of the text, is that email's body; the body is those lines joined with a line break between each (blank lines included).
4. Lines before the first subject line belong to no email and are not counted or checked.
5. No subject line at all: refuse with `BAD INPUT: 0 emails found: each email must start with a line "Subject: ..." (a check that reads 0 items fails)`.

Emails are numbered 1, 2, 3 in the order they appear.

### Counts per email

| Count | How it is counted |
|---|---|
| subject words | The number of pieces left when the subject is split at every run of white space. Punctuation stays with its word, so "rep's" is one word and "[User" is one word. |
| subject characters | Every character of the subject after spaces at both ends are removed, spaces and punctuation included. Each Unicode character counts as one. An empty subject is 0 words and 0 characters. |
| body words | The number of pieces left when the whole body is split at every run of white space (spaces, tabs and line breaks). Punctuation stays with its word; a placeholder such as "[User to add: first name]," counts as 4 words; a lone hyphen counts as a word. |

White space here means any white space character: a space, a tab, a line break, a no break space and the other Unicode spaces.

### The dash check

Run on the subject and on the body of each email separately. Each instance found is one problem.

| Problem name | What is counted |
|---|---|
| long dash | Every em dash (U+2014) and every horizontal bar (U+2015). |
| short dash | Every en dash (U+2013) and every figure dash (U+2012). |
| spaced hyphen used as a dash | Every plain hyphen (the keyboard hyphen, U+002D) that has a white space character directly before it and directly after it, is not the first or last character of the subject or body, and has some text other than white space before it on its own line. |

So a hyphen that opens a line, as in a bullet list ("- item", also when spaces come before the hyphen), is not a dash. A hyphen inside a word ("follow-up") is not a dash. A hyphen at the very start or very end of the subject or body text is not counted. Other characters, such as the minus sign (U+2212) and the non breaking hyphen (U+2011), are not checked here; the voice check still bans dashes of any kind.

Problems are listed email by email; within an email, subject before body; within each, long dashes, then short dashes, then spaced hyphens.

### Printed output (text)

Line by line:

| Line | Exact shape | When |
|---|---|---|
| One per email | `email <n>: subject <words> words, <characters> characters; body <words> words` | Always, in email order. "words" and "characters" stay plural even for 1. |
| One per problem | `PROBLEM email <n> <subject or body>: <problem name>` | One line for each instance found, in the order above. |
| Last | `CHECK: <number of emails> emails, <number of problems> problems` | Always. "emails" and "problems" stay plural even for 1. |

The result passes when there are 0 problems. The "CHECK: N emails" number must equal the number of send days; if it does not, fix the draft and check again.

### Printed output (JSON, for API or programmatic use)

One object, indented by one space per level, every list item and every key on its own line: "emails", a list with one object per email (email, the number; subject, the subject text; subject_words; subject_chars; body_words, in that key order), then "problems", a list of the problem texts without the word PROBLEM (for example "email 1 body: long dash"). Characters outside plain ASCII in a subject are written as \u escapes.

### Worked check

Emails 1 and 2 of the abridged example in SKILL.md, with the subject lines "Subject: Mornings on manual dialling" and "Subject: Which calls become meetings" and the bodies as quoted there (without the quote marks):

| Email | Subject words | Subject characters | Body words | Problems |
|---|---|---|---|---|
| 1 | 4 (Mornings, on, manual, dialling) | 27 (24 letters and 3 spaces) | 55 | 0 |
| 2 | 4 (Which, calls, become, meetings) | 27 (24 letters and 3 spaces) | 47 | 0 |

Printed text, line by line:

| Line | Text |
|---|---|
| 1 | `email 1: subject 4 words, 27 characters; body 55 words` |
| 2 | `email 2: subject 4 words, 27 characters; body 47 words` |
| 3 | `CHECK: 2 emails, 0 problems` |

## Results in short

| Mode | Result | Meaning |
|---|---|---|
| days or check | a "BAD INPUT: " line | The input was refused; pass the line on as written and ask the user for what is missing. |
| days | the days block | Copy it exactly, every line including the closing label line. |
| check | 0 problems | The draft passes the mechanical check. |
| check | 1 or more problems | Fix every problem and check again. |
