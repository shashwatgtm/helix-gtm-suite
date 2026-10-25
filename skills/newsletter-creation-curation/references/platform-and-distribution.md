# Platform checks and distribution

## 1. Check the platform before writing a word

Platforms change what they accept. Check before formatting, and format for the platform and nothing else.

| What to check | How |
|---|---|
| Does pasted Markdown render, or does it show as symbols? | connected: the platform's own help page; manual: ask the user to paste one test paragraph |
| Is pasted HTML accepted, and in which parts (body, welcome email, templates)? | help page, and the user's plan level (some features depend on the plan) |
| Images: hosted by the platform or linked; size limits; ALT text field | help page |
| Embeds and scripts: email clients do not run scripts, so nothing interactive goes in an email | help page |
| Character or length limits on subject, preview, title and description fields | the field itself or the help page; count by script |
| Canonical link: can the platform point to the original page? | help page |
| The user's own design file or template | replicate it exactly; never invent a template |

Record what was checked, with the page and date, in the answer. If nothing could be checked, say so and ask the user to test one paragraph before the full paste.

## 2. Derived assets (only those the user asks for)

- Share card text: see issue-structure.md, section 5.
- Subject lines and preview text: three options, each with its count, no clickbait, no fake urgency, no emoji. They carry the same guard as the body: no stronger claim than the issue makes, and a claim the issue attributes ("the company says on its home page") stays attributed.
- A social teaser post: points to the issue without giving all of it away. On LinkedIn: no link in the post body (the link goes in a comment), opens with the writer or the reader's situation, one idea, an open question to close, two or three hashtags. If a LinkedIn post skill is installed in the session, hand the teaser brief to it; otherwise draft it here under the voice check.
- A long form version on another platform: keep the canonical page as the home, set the canonical link where the platform allows it, and keep source links out of the body flow there when the user wants readers to stay; list sources at the end instead.
- Cross posting: each platform's own guidelines apply; never paste the same text to several platforms where the platform treats it as duplicate; adapt the opening and the call to action. A planned series across platforms follows the approved series plan (issue-structure.md, section 4), with each data point and story in one part only.

Every derived asset goes through scripts/asset_check.py with the issue (add --deep-dive only for a deep dive issue).

## 3. Approval gate

Nothing is published, scheduled or sent by this skill. The answer ends with what is ready and what the user must approve. When the user or a teammate publishes, they do it in their own account. Never say an issue was "sent" or "published" unless the user says they did it.

## 4. Owned list or platform newsletter

When the user is choosing where to publish, set out the trade off without numbers:
- A list the user owns (an email platform they control) moves with them if they change jobs or platforms.
- A newsletter inside a social platform reaches people already following them there, but the platform controls the list.
- Many writers keep the list they own as the home and use the platform version for reach.
The choice is the user's.

## 5. Employee and company newsletters

- A personal newsletter by an employee: ask about the employer's social media and disclosure policy; no non public company figures, customers or roadmap; company facts from public company pages; the employer's required disclaimer if they have one.
- A company newsletter: the brand voice guide applies; regulated topics go through the company's own review before sending.
- A newsletter written for a client or an executive: the principal approves every take; mark takes "[Principal to confirm]".

## 6. Things this skill does not do

It does not send email, manage lists, read the user's open or click data unless the user pastes it, submit to news aggregators, or promise subscriber growth, open rates or leads.
