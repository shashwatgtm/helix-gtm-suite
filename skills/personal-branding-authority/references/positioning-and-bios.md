# Positioning, bios and profile: how each asset is built

Every asset here is built from the fact sheet. Nothing goes into an asset that is not on the fact sheet with a source. A missing fact is written as [User to add: ...]. Where the given facts cover an asset or part of it, that part is written as near-final copy built only from those facts and labelled "Near-final, built only from the facts you gave; please confirm", so the answer is not mostly placeholders. Where the person gave few facts, a gap that their facts and the company's pages opened in this session can support gets a line marked [Draft for you to confirm: ...] with its source, instead of a bare placeholder (for example a draft audience from the meetups the person named and the buyers the company's own page names); a draft line never carries a fact about the person that they did not give. Only the assets the person asked for are written; anything else is offered in one line. When the person asks to change part of an asset, only that part changes; nothing from their earlier, fuller version is dropped without saying what and why.

## 1. The fact sheet (always first)

| Fact | Exact wording | Source | Status |
|---|---|---|---|
| Current title | as the person writes it, letter for letter | their profile text, CV, or what they typed | confirmed / needs check / missing |
| Employer and what it does | the company's own words | the company's own About page, with URL and fetch date, or the person's paste | confirmed / as pasted, not yet checked / held back, an opened page contradicts it (SKILL.md Step 2) |
| Past roles and dates | as written | CV or profile | ... |
| Results and figures | the number and what it measured, with the employer or client, the person's role and the period it belongs to | the person, a file, a public page | ... |
| Recognition | the exact name of the award or list and the year | the person, the awarding body's page | ... |
| Lived moments | see section 2 | the person | ... |
| Focus order and lead identity | the person's ranked focus areas or services, and the identity they lead with, in their exact words | the person | ... |
| Testimonials and recommendations | word for word, with the recommender's name, title and company as given, and the date | the person's paste, or a page they name opened in this session | ... |
| Not to be named | each client, employer, customer or colleague who must not be named, with the description the person uses instead | the person | ... |

Rules:
- Titles, company names, award names and figures are copied exactly. "Co-founder" never becomes "Founder". "Led the launch messaging" never becomes "built the product". "One of the few" never becomes "the leading".
- When two sources disagree (a CV and a profile with different years), list both, ask which is the source of truth, and use a placeholder until the person answers. Never pick the bigger number.
- A figure the person cannot source is marked "needs check" and stays out of public assets until they confirm it.
- Every result on the fact sheet carries the employer or client, the person's role and the period it belongs to, as the person gave them. An asset never shows a figure without them, and the same figure never appears under two employers; if the person's sources place it in two places, ask which is right.
- Credit only what happened while the person was there: an acquisition, exit, funding round, award or result from after they left, or one they have not confirmed as theirs, is left out or written as the company's own news with its date.
- When the person's method builds on someone else's named framework, credit that framework and its owner in the person's own words. Never present an adapted framework as wholly the person's own, and never add a lineage the person did not state; ask instead.
- Company facts come from the company's own page. The person's facts come only from the person and the files they give. Do not search for the person or profile them.
- Describe the company only in the category words its own page uses for itself (for example a software platform, a SaaS product, an IT services firm), and never turn them into another kind of business: a "fully managed" software product is not a managed service, and a platform is not a consultancy. In a bio, headline or profile the person publishes, and on the company's own team page, state those category words plainly as what the company is or does (for example "[Name] leads product marketing for Freshservice at Freshworks, which provides AI-first service software for customer and employee experiences"), with no "describes itself as", no quote marks and no second quote from the same page. Leave out the page's own praise and ranking words (best, leading, world's, exceptional, trusted by) and its figures unless the person asks for them. The page, its exact words and its fetch date stay in the fact sheet.
- Bios, headlines and the About carry the sector's own words for the person's work, taken from verticals.md, the person's facts and the company's opened product pages, so a peer in that sector recognises the work. Words only: never a new claim, figure or result.
- When the person names their own framework, method or model, take its name, its parts and what any acronym stands for from the person's own text or a source they name. Never expand an acronym or describe its parts from memory; if no definition is given, use a placeholder and ask.
- When the person ranks their focus areas or services, or names the identity they lead with, keep that order in every asset, and never move a secondary service into the first position or the headline. Never relabel the person with a narrower role or category than their own words, and keep their own spelling of terms and abbreviations. Shorten a phrase only when a field limit forces it, and say which phrase was shortened.
- When the person corrects a fact (a name, a title, role dates, an email, an award year), change its row at once and use only the corrected value from then on; before delivery, check every asset drafted in the session for the old value.

## 2. Lived moments (the material that makes a brand sound like one person)

Ask for two to five moments. For each, capture:
- when it happened and where (a specific time, place or meeting);
- what was at stake;
- what the person did or got wrong;
- what changed because of it;
- what they learned that a peer could use;
- whether it can be told in public (employer, client and colleague consent).

Never invent a moment, a scene, a dialogue line or a feeling. If the person gives one sentence, ask one follow up question about it; do not fill the gap.

## 3. Positioning statement

Shape (one paragraph, first person, plain words):
"I help [who, in the buyer's own words] [solve or do what] by [how, grounded in what I have actually done]. [One or two proof points from the fact sheet.] I am not the right person for [what they do not do]."

Then a one line version for a headline or an introduction.

Checks before it is shown:
1. True today: every clause is on the fact sheet.
2. A real buyer: the "who" is a role and a sector the person actually serves (see verticals.md).
3. Sector words: a peer in that vertical would recognise the problem in these words.
4. Lived experience leads; credentials appear as proof after it.
5. There is a "not for" line, so the position excludes something.
6. No self applied labels such as "thought leader", "visionary" or "guru", and no coined term the person does not already use.
7. The person's own lead identity and focus order (fact sheet) lead; a secondary service never takes the first position.

Angle types to choose from, only where the person's material supports them:
- Educator: teaches the methods they actually used.
- Challenger: questions a common practice, with evidence they lived through. Use with care in regulated sectors.
- Builder: documents what they are building, as they build it.
- Analyst: reads public data and cites every number.
- Storyteller: draws lessons from specific moments.

## 4. Bios

Lengths are defaults; the person's or the organiser's limit wins. Count with scripts/count_fields.py.

| Format | Default length | Voice | Use |
|---|---|---|---|
| Short | about 50 words | third person unless asked | social profiles, author lines |
| Medium | about 100 words | third person | event pages, guest posts |
| Long | about 200 words | third person | websites, media kits |
| Speaker | about 100 words | third person | conference programmes, podcasts, panels |
| Host introduction (only when asked) | 40 to 60 words | written to be read aloud | the host or moderator reads it on stage |

Order inside every bio:
1. What the person does and for whom (or the problem they work on).
2. The lived experience behind it, in one concrete line.
3. Proof from the fact sheet (results with what they measured, roles, recognition exactly as named).
4. Current focus, or the talk topic for a speaker bio.
5. A personal line only if the person gave one.

Speaker bio extras: the talk title as the organiser has it; a pronunciation note if the person asks for one ([User to add: how your name is said]); nothing about the session that the organiser has not confirmed.

## 5. Profile rewrite

Field limits change. Check them on the platform's own help page in connected mode, or ask the person to read them from the profile editor in manual mode. Never state a limit from memory. Count every field with scripts/count_fields.py and pass the limit with --limit.

- Headline: what they do, for whom, and one focus or proof point, in the person's own lead identity and focus order. Plain words, no emoji, no self applied labels.
- Paired short fields: when two short fields are read together (for example a headline and a short introduction, or a title and a summary), do not repeat a keyword or claim across them. Give each field different information so the pair carries as much as its limits allow, and list the words both fields share before delivery. When the person asks for one field to carry as much as it allows, write up to its limit using only fact sheet items; never pad.
- Links, handles and contact details: profile links, social handles, booking links, email addresses and newsletter names are copied exactly as the person gives them. Never guess, build or search for one; a missing one is [User to add: ...]. Never attribute a profile, handle or page to the person that they have not confirmed as theirs; other people may share the name.
- Text that AI assistants also read: if the person wants profile text that AI assistants can also read correctly, write their name, current title, company and what they do in full plain sentences, spelled the same way in every asset. Promise no effect on AI answers or search results.
- About: first person prose. Open with the problem they work on or a lived moment, then what they do now, how they work, two or three proof points, and what people can contact them about. No wall of bullets. For an employee (any in-house role), the contact line invites conversation about the topic or the employer's public work, never offers the person's own outside services, help or advice unless the person asks for that, and the employer's policy on outside work and speaking is listed as an open item.
- Featured: only items that exist (posts, talks, articles the person names). Never invent a featured item.
- Experience lines: what changed because of their work, with numbers only from the fact sheet, each under the employer and period the fact sheet gives it, and the team's work credited as the team's.
- Skills: chosen from the person's own list, matched to the pillars.

## 6. Award, nomination or application fields

- Capture each field's limit and type (text, number only, date) before writing.
- Paired fields read together (a title and a summary, a headline and an introduction) carry different information, with no keyword repeated across them (section 5).
- Use only facts the person supplies. Label every result with its real stage: a pilot is a pilot, a prospect is a prospect, a partner is a partner.
- A result needs its baseline. "Three times more leads" with no baseline is not used; ask for the baseline or drop the claim.

## 6a. Testimonials and recommendations

Use only testimonials or recommendations the person supplies (pasted text, or a page they name that was opened in this session). Quote them word for word; never shorten them into new wording and never write testimonial text. Write each recommender's name, title and company exactly as the person or the named page gives them, with the date it was given; never look up a recommender's current title elsewhere and never add a descriptor (such as "former") that the source does not give. If it is unclear whether the recommender's words may be reused in public, ask.

## 7. Number and title lock

Before delivery, run scripts/count_fields.py on all assets together. Any label that carries two different numbers (for example "12 years" in one bio and "14 years" in another) is fixed to the fact sheet value or turned into a placeholder. Titles must match letter for letter across every asset.
