# Issue structure

The user's own template or design always wins. When they have one, reproduce it exactly and change only the content; never invent a new layout. When they have none, use the default below.

## 1. Default issue (B2B, curated with commentary)

| Part | What goes in it | Length default |
|---|---|---|
| Subject line | what the reader gets, in plain words; no clickbait, no fake urgency; never a stronger claim than the body, and an attributed claim stays attributed | check the length the user's email platform shows before cutting; count by script |
| Preview text | extends the subject with one more fact from the issue, under the same guard as the subject line | count by script |
| Masthead | newsletter name, issue number, date with weekday checked | one line |
| Editor's note | a personal note from the writer: what they noticed this fortnight, from their own work | two to four sentences, the writer's words or [User to add: ...] |
| Lead story | the most important item for these readers; when the user or their editor picks the lead, up to three candidates first, and the issue waits for their choice | up to about five lines |
| Other stories | two to five more items | two to three lines each |
| One practical step | something the reader can do, from the writer's own practice | two to four lines |
| One resource | a tool, report or page the writer actually uses, with why | one to two lines |
| Reader prompt | a question or a reader spotlight (with the reader's consent) | one to two lines |
| Close | one clear call to action and the writer's sign off | one to two lines |
| Author line | who writes this and why they can, from the person's own facts | one to two lines |

The lead runs longer than the other stories. If the user's house rule says something else (for example three to four sentences for the lead), the house rule wins.

## 2. Each curated item: the three beats

Every item has:
- a headline in the writer's words (not the source's headline copied), never claiming more than the item's body: a claim the body attributes to its source stays attributed in the headline;
- the source name, the date as written on the source, and the link;
- What happened: one or two sentences, from the opened page only, with at most one short exact quote;
- Why it matters to these readers: tied to their jobs and their sector (verticals.md), and to this one item only. One vendor session, one release or one page shows what that company did or says; it is never written up as a market trend or as what "the industry" is doing;
- The take: the writer's own view or the action for the reader. If the writer has not given one, write "[User to add: your take]". When the user asked for something paste ready, add a suggested take under the placeholder, marked "[Suggested take, for the editor to confirm or replace]" and built only from the item's facts and the user's notes. Never present a take as the writer's own when they did not give it.

## 3. Formats to choose from

- Curated roundup: three to six items with the three beats, plus the editor's note. Best when the writer reads widely and has a point of view on each item.
- Deep dive: one topic, the writer's own experience first, sources as support, one practical step. Best when the writer has done the work themselves. It has no "### " curated items, so run scripts/asset_check.py with --deep-dive; without it, an issue with 0 curated items does not pass.
- Mixed: a short personal note, one deep item, three curated items, one resource. Its curated items are "### " items, so the check runs without --deep-dive.

## 4. Series and calendar

- Recurring sections keep the same names and order every issue, so readers know where to look.
- A theme can run across several issues; each issue still stands alone and says where it sits ("part 2 of 4").
- Cadence is the user's choice: what they can sustain. Never promise a growth or open rate result from a cadence.
- Keep a short backlog of evergreen items from the writer's own practice for weeks when news is thin.
- A series across several issues or platforms (for example a newsletter, a blog and a long form article): first ask the questions that shape it, then write a short series plan and get the user's approval before drafting: the role and angle of each part, which data point, source and personal story each part carries (each used in one part only), and how the parts link to each other.

## 5. Share card (separate from the hero image)

The share card is its own image, made for link previews and social posts. Do not reuse the issue's hero image at a different size.
- Content: a large image, the newsletter's masthead, the cover story headline, and one to two lines beside it.
- Size: the platform's current link preview recommendation, checked on its own help page; never stated from memory.
- The skill writes the card's text and an image brief; the user or their design tool makes the image.
- Every number on the card matches the issue (run scripts/asset_check.py).

## 6. Locked content

When the user says the content is final, or gives a design to replicate:
- change only what they asked (for example "only the editorial");
- never change headlines, quotes, links, numbers, images, colours or calls to action they gave;
- list any fact problem you notice as a question, without fixing it.
- When the user returns a numbered list of fixes, do exactly those and nothing else.
