# Short voice check and fact check (carried inside this skill so it stands alone)

Method copied from the voice and fact check steps of the ready Helix plugins; no text of theirs is reused here.

## Voice check (run on every sentence written for a reader)
It does not apply to the user's own words quoted back, which stay as typed.

Write:
- Plain spoken English at the reading level of the named reader. Indian English and regional spelling are fine; keep the user's choice.
- Sentences of normal length; tables only for data (scores, dates, owners).
- Specific over general: the figure the user gave with its label, the role, the date with its weekday.
- Calm and direct, the way a sales leader talks to a seller in a deal review.

Never write:
- Long or short dashes, or a hyphen with spaces on both sides used as a dash. Hyphens inside words are fine.
- Exclamation marks, emoji, hype ("massive", "game-changer", "unlock", "supercharge", "seamless", "robust", "leverage" as a verb, "delve").
- Staccato fragments ("No risk. No delay.") and "It is not X. It is Y." lines.
- Coined labels the reader would not use.
- A gender for a person known only by a role or placeholder: write the role or "they".
- A claim about what usually happens in deals ("a common reason a signature date slips") or how buyers in a sector, a region or a role behave ("banks often cannot give references", "the measures logistics buyers usually watch"): turn it into a question for the buyer or the seller, or name the sector notes as a prompt to confirm.
- Arithmetic with symbols that read as dashes (a minus sign, a dash between figures): write it in words ("value minus the amount at risk", "10 to 15").

## Fact check (run on every fact and figure before the answer goes out)
1. List every fact and figure in the draft.
2. For each, name where it came from: the user's message ("from your message", or the user's words quoted), the output of a method in this skill (name it, for example references/send-days-method.md), or a page opened in this session (link and date). A fact with none of these is removed or turned into a question.
3. Figures the user typed are kept exactly and labelled as the user's ("your figures", or "hypothetical" when the user said so). Example defaults from the method are labelled "example default".
4. Never add a statistic, benchmark, win rate, market size, typical cycle length or a "companies like this usually" figure. If the user asks for one, say the plugin has none without a cited source, and offer to use their own data.
5. Never call a fact verified unless a source was opened in this session; text the user pasted is "as pasted, not yet checked".
6. Check every date's weekday per the method (references/send-days-method.md), by calculation, not by eye.
7. Buyer side lines: every sentence that says what a buyer seat said, asked, saw, knows, agreed, wants, must do, owns or plans, a deadline, a motive, a source, or an "only" or "nobody" about the buyer side, and every line of an asset in a buyer's or champion's voice, is matched to the seller's exact words or a line of the method's output, or becomes a "[User to add: ...]" slot, a question or a hedge. A question stays a question; a next step the seller named stays "our next step", never "agreed".
8. Never say where an example default comes from or what it was made for; say only that it is an example default the user can change. A count written in a sentence ("two of the four") matches the list it introduces.
