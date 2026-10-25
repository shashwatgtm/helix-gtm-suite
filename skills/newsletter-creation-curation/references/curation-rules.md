# Curation rules

## 1. Where items come from (in this order)
1. Sources the user names (their links, their files, their notes). These beat anything the skill finds.
2. The primary source: the company's own press release or blog, the regulator's own page, the publisher's own report or topline.
3. Reputable business and trade press that names its sources.
4. Never: anonymous posts, content farms, pages that copy other pages, sites that rank tools without a method, and AI generated summaries of news.

## 2. Opening every item
- Connected mode: open each page before writing about it. Record: URL, the date on the page, whether the quote used appears on the page, and the time it was opened.
- Manual mode: use only what the user pasted; label the item "as pasted, not yet checked; link not opened in this session" and ask the user to confirm the date.
- A paywall or a blocked page: say so. In connected mode, run a web search for its headline before dropping it; text from the results is labelled "from a search result; the page itself was not opened" and is never written into the issue as fact. Use only the visible headline and date, or drop the item. Never fill in the article from memory or from other coverage without saying so.
- A link that fails: report it by URL and drop the item unless the user supplies the text.
- Anything recalled from memory rather than read on a page opened or text pasted in this session (a report's exact title, a figure, a date, a publisher's or company's usual practice) is marked "not yet checked in this session" wherever it appears, offered as a lead for the user to open, and never written into the issue as fact.
- Never write "all links verified" or "links checked". Give the per link list instead.
- For each source the user hands over, say whether it was used and, if it was left out, why.

| Item | URL | Opened | Date on page | Quote found | Used, or left out and why |
|---|---|---|---|---|---|

## 3. Dates
- Write the date as the source writes it, with the month as a word.
- A relative date ("last Tuesday", "yesterday") becomes an exact date taken from the source page.
- Any weekday written next to a date is checked by scripts/asset_check.py.
- The issue date and year are checked too: a draft that prints last year's date is a known failure.
- The user sets a recency window for the issue (for example items from the last two weeks). Items outside it are flagged as stale, with their date shown, and kept only if the user says so.

## 4. Numbers and statistics
- Use a number only if the opened source states it. Copy it exactly with what it measured.
- For a survey or report: state what it measured (region, sample, the kind of buyer or person asked, the date of fieldwork if given). A consumer survey is not evidence about B2B buyers; a survey from one region is not evidence about another.
- Never add two figures together to make a new one unless the source does.
- Never round a figure in a way that changes it ("29.5%" is "about 3 in 10", not "1 in 3").
- A number "everyone knows" with no source is not used. Ask for the source, search for the primary source in connected mode, or rewrite the line without a number.
- Analyst firm figures: name the firm, the report and the date; label region and sample.
- A page that cites several sources: say which figure comes from which source, as the page itself attributes it (for example one figure from a consultancy report, another from the company's own platform data). Never describe all of a page's figures as coming from one source when the page names more than one, and for a figure whose source you did not find on the page, write "source of this figure not found on the page I opened: [the page]", never that the page gives no source (one fetch is not proof of absence).

## 5. Quotes
- Quotes are short, exact, inside quotation marks, and from the opened page.
- A quote from a person is used only as the source printed it; never edit it, never extend it.
- Never invent a quote, and never paraphrase a person and present it as a quote.

## 6. Fit to the readers
- Each item answers "why should these readers care this fortnight?" in their sector's words (verticals.md), for that item only: one vendor's session or release is not evidence of a trend. A trend line needs several independent sources, each opened and cited.
- Regulated topics (financial rules, data protection, security incidents): link the regulator's or the company's own statement, add a line that the item is information and not legal or financial advice, and never predict enforcement or name an affected company without a public source.
- Competitors of the user's employer: report facts from primary sources only; no mockery.

## 7. Number lock across assets
Every number in the subject line, preview text, share card, teaser post and any derived asset must match the issue. Run scripts/asset_check.py with the issue and every derived file (add --deep-dive only for a deep dive issue with no "### " curated items). Fix drift to the sourced figure in the issue, then run it again. Spelled out numbers ("three launches") are not caught by the script; check them by reading.
