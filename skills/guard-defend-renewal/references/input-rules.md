# GUARD Input Rules

## Rule 1: One Dump, One Output
The CSM pastes or uploads everything they have in ONE message. The skill normalizes. Accept: conversational dump, messy notes, Slack pastes, CRM tables (any headers), PDFs (surgical extraction of 4-8 key slides), screenshots, voice-to-text, or any combination.

## Rule 2: Question Budget — Maximum 2
Only ask if you cannot produce ANY output. Valid questions: "Which account?" / "Health check, QBR prep, renewal, expansion, or onboarding?" / "What do these columns represent?" Everything else → assume and flag with [Missing: X] or [Assumption: Y].

## Rule 3: Column Mapping (for CRM/spreadsheet tables)
Map headers by meaning, case-insensitive, fuzzy:
- Account: account, company, customer, client, name, org
- Revenue: arr, mrr, revenue, contract value, deal size, acv
- Satisfaction: nps, net promoter, csat, satisfaction
- Support: tickets, cases, support cases, open tickets, issues
- Usage: logins, login frequency, dau, wau, mau, usage, activity, adoption
- Cadence: last qbr, last review, last meeting, last check-in
- Renewal: renewal, renewal date, contract end, expiry, renews in
- Stakeholder: champion, champion left, sponsor, key contact
Unrecognized columns: skip silently, note in output.

## Rule 4: Risk Signal Detection from Natural Language
Detect these signals in ANY input — CSM does not need to label them:
- Champion departure: "left", "departed", "new VP", "contact changed"
- Engagement decline: "went quiet", "not responding", "ghosting", "skipped QBR"
- Competitor threat: "evaluating", "looking at alternatives", "competitor", "RFP"
- Usage decline: "usage dropped", "not logging in", "stopped using"
- Sentiment decline: "frustrated", "disappointed", "NPS dropped", "escalation"
- Budget pressure: "budget cut", "cost reduction", "vendor review", "procurement"
- Product gaps: "missing feature", "can't do X", "workaround", "blocked"
- Stakeholder risk: "reorg", "new CTO", "leadership change", "layoffs"
- Data export: "exporting data", "data dump", "migration", "backup"

## Rule 5: Document Handling
- PDF QBR decks (50-60 slides): read ONLY slides matching "executive summary", "action items", "risks", "forward plan", "key metrics". Skip screenshots, appendix, org charts.
- Meeting transcripts: extract action items + risk signals + sentiment. Ignore small talk.
- NPS: accept as single score, score+trajectory, verbatim list, CSV, screenshot, or nothing.
- Feature usage: accept as %, feature table, descriptive text, login frequency, or nothing.

## Rule 6: Batch Size
- Health checks: 5-15 accounts per run. Over 15 → suggest segmented batches.
- QBR prep: 1 account deep. Batch makes no sense.
- Renewal assessment: 1-5 accounts per run.
- Expansion scan: 3-8 accounts per run.
- Onboarding: 1-3 accounts per run.

## Rule 7: Use the evidence available
For renewal work, follow renewal evidence review 20261103 in `renewal-playbook.md`. Four or more evidenced factors permit a fuller evidence review; two or three permit a partial review; zero or one calls for structured discovery. None authorizes a probability, numerical risk score or GRR forecast. Do not use an inferred or assumed signal to fill a gap. A supplied health score remains an attributed input, not a renewal probability.

## Rule 8: No LLMisms
Never use: "high-impact shift", "dive in", "use", "examine", "landscape", "mix", "elevate", "open", "smoothly." Write like a seasoned CSM.

