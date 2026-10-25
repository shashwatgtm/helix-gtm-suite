# Banned words, banned patterns and what stays allowed

This list is the union of several working lists kept by a B2B marketer over two years of editing machine drafts by hand. scripts/voice_scan.py carries the same list. When the user has their own list, theirs is added to this one; nothing here is removed unless the user says so.

## 1. Banned words and phrases (flag every time in text for publication)

high-impact shift, game changer, game-changing, use (and using, used), dive in, dive into, dive deep, examine, mix, elevate, elevated, open, smooth, smoothly, landed hard, resonated, struck a chord, genuine open, genuinely, honestly, straightforward, revolutionize, supercharge, harness, empower, in today's world, in the ever-evolving landscape, ever-evolving, take your X to the next level, next-level, it's important to note, proof to, the rise of, keep coming back to, sat with me, scoring methodology (say "scoring method"), move the needle, here's the thing, groundbreaking, revolutionary, transformative, comprehensive, robust, complete, synergy, paradigm shift.

Stock openers: "Humbled to share", "Humbled and honored", "Thrilled to announce", "Thrilled to share", "Excited to announce", "Excited to share".

Self labels: "thought leader" or "thought leadership" applied to the writer by themselves.

## 2. Review words (flag for a human decision; fine when literal)

| Word | Allowed when | Flag when |
|---|---|---|
| landscape | a domain modifier: "competitive landscape", "threat landscape" | used as filler: "the AI landscape is changing" |
| navigate | a literal route | abstract: "navigate change" |
| dynamic | a technical term: "dynamic pricing" | praise: "a dynamic leader" |
| mechanics | literal | a vague label for "how it works" |
| just | it carries meaning ("just in time") | filler ("just wanted to say"), or inside a contrast ("not just X", "no longer just X" followed by a second claim): that is the banned contrast pattern, never a meaningful keep |
| incredible, unprecedented, massive, mind-blowing | almost never | hyperbole |

"Landed hard" and similar phrases are banned in published copy only. A user saying "that lands" in a chat message is not a flag.

## 3. Banned patterns (with a fix for each)

| Pattern | Example | Fix |
|---|---|---|
| Long, short or spaced dashes | "We shipped it [long dash] and waited." (the long dash is Unicode U+2014; the short dash is U+2013) | Split into two sentences, or use a comma or a colon. Hyphens inside words stay. |
| "That's not X. That's Y" and its variants ("It wasn't X. It was Y.", "They are not just X. They are Y.", "no longer just X; now Y", "We don't just X; we Y") | "That's not a feature. That's a movement." | Say the one true thing plainly: "The feature changed how our agents close calls." When both halves are the writer's claims, keep both as plain statements ("The engines are outdated. They are also a liability.") and never join them with a cause, effect or link the writer did not give ("and that makes them", "because", "so"). |
| Lazy "start on Monday" lines | "Start on Monday and see the difference." | Give the concrete first step, or cut the line. |
| Uncommon coined labels | "the Insight Flywheel Stack" when nobody uses that name | Describe what it is in common words. |
| Unusual or showy words where a plain word works | "a many of", "a many of", "critical" | Use the word the reader would say ("many", "key"). A review item: the scan does not catch it, so read for it. |
| Staccato fragments of one to three words | "Big news. Huge win." | Join into a full sentence with a subject and a verb. |
| "First... Second... Third..." inside prose | "First, we listened. Second, we shipped." | Write it as a story in time order, or a single sentence. |
| Neat punchlines and aphorisms | "Ship fast. Learn faster." | Replace with what happened. |
| Hyperbole, sudden excitement or despair | "This changes everything." | State the specific change and its size, if sourced. |
| Exclamation marks | "We did it!" | Full stop. |
| Essay openers | "In an era of rapid change," | Start with the person, the reader's situation, or the moment. |
| Rhetorical questions in the body | "Why would anyone wait?" | Turn into a statement; keep one genuine open question only at the close. |
| "Old thinking / New thinking" framing | "Old way: guess. New way: data." | Tell what the writer did before and after, in sentences. |
| Focus on semantics over narrative | sentences that rearrange abstract nouns | Put a person, an action and an object in each sentence. |
| Unnecessary curiosity hooks | "You won't believe what happened next." | Say what happened. |
| Fabricated scenes or speculated feelings | "The room went silent." when the writer never said so | Remove, or ask the writer whether it happened. |
| Emoji, Unicode bold letters, arrows, checkmarks | a rocket emoji, words typed in mathematical bold letters, a right arrow character, a green check mark | Plain words. The user's own choice wins when they give a reason. |
| Broken encoding | a run of odd symbols (for example a letter a with a circumflex followed by a euro sign) in place of an apostrophe | Ask for a clean copy if meaning is unclear. |

Writing style that also counts as a pattern, from a voice template's avoid list: generic thought leadership, overly academic tone, buzzword stuffing, purely promotional copy, no structure, description with no point of view, ignoring what the buyer worries about, a voice that changes from paragraph to paragraph.

## 4. What stays, always

- Text inside quotation marks taken from a source (a press release, a report, a person's words). It is quoted as the source wrote it, even when it uses a banned word. Only the writer's own sentences are audited. Run the script with --skip-quotes for this.
- The writer's raw human take: emotion, a small mistake, a frustration, humour, spoken phrasing. Emotion can matter more than a neat narrative.
- Regional English such as Indian English, unless it blocks understanding.
- Facts, names, numbers and dates. The audit never changes them. If one looks wrong, it is listed as a question, not fixed.
- A single genuine open question at the close of a post.
- The user's own edit when they say why they made it.

