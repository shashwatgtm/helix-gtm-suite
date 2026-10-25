# MCP Connector Setup & Input Handling

This reference governs how the skill discovers what the user has connected, asks for what is missing, and accepts data via a 4-tier fallback architecture. Loaded on the first invocation in a new conversation, then again only if the user signals their stack has changed.

The existing per-tool integration references (`calendar-integration.md`, `email-integration.md`, `slack-integration.md`, `notion-integration.md`, `dashboard-parsing.md`) cover universal-stack tools at the API and logic level. This file covers the broader CS software landscape, the discovery workflow, and the indirect-access patterns for tools without native MCP connectors.

## Section 1 — Software Landscape by Function (17 Categories)

Professionals across GTM, CS, and operational roles work across a wide tool landscape. **The skill routes by CATEGORY, not by tool name.** A category captures the kind of data the skill needs to extract; the specific tool name only matters for MCP connector detection.

The 17 categories below are the starting taxonomy. Each list of named tools is illustrative — append "and similar tools in this category" mentally to every line.

1. **CS Platforms** — Gainsight, Totango, Planhat, ChurnZero, Custify, Vitally, and similar tools in this category
2. **CRM** — Salesforce, HubSpot CRM, Zoho CRM, Copper, Freshsales, and similar tools in this category
3. **Helpdesk / Service Desk** — Zendesk Support, Zoho Desk, Freshservice, Freshdesk, Jira Service Management, ServiceNow, and similar tools in this category
4. **Customer Communication & Engagement** — Intercom, Pylon, Zendesk Messaging, Braze, Customer.io, and similar tools in this category
5. **Voice-of-Customer / NPS / CX** — Qualtrics, Delighted, SurveyMonkey, Typeform, Tally, InMoment, Medallia, and similar tools in this category
6. **Conversation Intelligence & Call Reports** — Gong, Chorus, Fathom, Observe.AI, Cresta, Otter.ai, Zoom IQ; plus call center platforms (Five9, Genesys, Talkdesk, Aircall) producing transcripts, CSAT surveys, disposition reports — and similar tools in this category
7. **Product Adoption & Usage Analytics** — Amplitude, Mixpanel, Pendo, Heap, OpenReplay, FullStory, and similar tools in this category
8. **Onboarding & Digital Adoption** — UserGuiding, Pendo, Appcues, WalkMe, Intercom, and similar tools in this category
9. **Knowledge Base & Self-Service** — Zendesk Guide, Helpjuice, HelpDocs, Document360, Guru, and similar tools in this category
10. **Project / Work Management** — Asana, Notion, Confluence, Jira, Monday.com, Linear, Coda, Slab, and similar tools in this category
11. **Product Feedback & Roadmap** — Canny, Productboard, Aha!, UserVoice, Jira Product Discovery, and similar tools in this category
12. **Customer Data & Identity** — Segment, mParticle, RudderStack, Clay, Clearbit, ZoomInfo, and similar tools in this category
13. **BI & Reporting** — Tableau, Looker, Power BI, Amplitude, and similar tools in this category
14. **Billing & Subscription** — Stripe, Chargebee, Recurly, Zuora, ProfitWell, and similar tools in this category
15. **Community & Advocacy** — Discourse, Khoros, Higher Logic, Influitive, Mighty Networks, and similar tools in this category
16. **Productivity (universal)** — Google Calendar, Gmail, Google Drive, Notion, Outlook, and similar tools in this category
17. **Document & Contract Management** — DocuSign, PandaDoc, Ironclad, and similar tools in this category

**Routing rule:** the skill cares about CATEGORY for data-extraction logic, and TOOL NAME only for MCP connector detection. If the user names a tool not in the lists above but matches a category capability ("we use a custom internal CRM"), route by category and apply the 4-tier fallback (Section 3).

### Section 1.1 — Persona-Specific Tools Not Covered Above

The 17 categories above cover tools shared across personas. Some roles use specialized tools:

- **Sales:** Outreach, SalesLoft, LinkedIn Sales Navigator, Clari, Apollo
- **Marketing / ABM:** HubSpot Marketing, Marketo, 6sense, Demandbase, Terminus
- **DemandGen / Performance:** Google Ads, LinkedIn Ads, Meta Ads, SEMrush
- **Content:** WordPress, Contentful, Ahrefs, SEMrush
- **Product Marketing:** Showpad, Highspot, Seismic, MindTickle

Route these by the same 4-tier fallback. Most will land on Tier 2 (Drive export) or Tier 4 (paste). The discovery workflow in Section 2 already handles unlisted tools — the user names their tool, the skill matches it to the nearest category or creates an ad-hoc entry.

## Section 2 — First-Run Discovery Workflow

On the first invocation in a new conversation, before generating any briefing, run this workflow.

**Step 1: Ask which CATEGORIES the user uses**

Present the 17 categories from Section 1. Phrasing:

> "Quick one-time setup. Which of these CS tool categories do you use? Just check the categories — I'll ask for specific tool names only when I need them.
>
> [list the 17 categories with short examples]
>
> Anything else? Add categories I didn't list."

Accept any response format — checkmarks, numbered list, freeform paste, or "all of them."

**Step 2: For each marked category, capture the specific tool name**

For each category the user marked, ask: "Which tool do you use for [category]?" — one short question per category. Skip if the user already named the tool in Step 1.

**Step 3: Apply the 4-tier fallback per tool**

For each named tool, run through the 4-tier architecture (Section 3) to determine the access path. Surface the result once: "I'll pull [tool] data via [Tier X]."

**Step 4: Persist for the rest of the conversation**

Store category selections, named tools, and access tier per tool as in-conversation context. Reference it on every subsequent invocation in this conversation. Do not re-ask discovery questions unless the user signals a stack change (Section 5).

## Section 3 — 4-Tier Input Fallback Architecture

For every named tool, attempt access in this order. Stop at the first tier that works.

### Tier 1 — Native MCP connector (preferred)

The tool has a vendor-published or Anthropic-published MCP server. The skill calls the connector directly. Highest fidelity, lowest friction.

**Detection:** attempt the tool's known MCP namespace (e.g., a server prefix like `salesforce_` or `gainsight_`). If a server responds, mark as Tier 1.

If detected, proceed without further user input. If not, drop to Tier 2.

### Tier 2 — Drive folder hub (automation deposits files)

The user has automation (n8n, Zapier, Scheduled Reports, custom scripts) that deposits the tool's data as files in a Drive folder. The skill reads the folder via the Drive MCP connector.

Common patterns:
- Daily CSV export of at-risk accounts dropped into `/CS Daily Snapshots/`
- Weekly Tableau PDF dropped into `/CS Reports/`
- Scheduled report from a CS platform auto-saved to a Drive folder

**Detection:** ask once: "Do you have a Drive folder where [tool] data lands automatically? If yes, share the folder link or name."

If the folder exists and is accessible, proceed. If not, drop to Tier 3.

### Tier 3 — Email alert extraction (tool sends digests)

The tool sends daily or weekly digest emails. The skill reads Gmail / Outlook via the email MCP connector and extracts data from the body or attachment.

Common patterns:
- Daily "Customer Health Digest" email from a CS platform
- Weekly NPS roundup
- Daily ticket-volume summary from a helpdesk
- Scheduled BI email report with PDF attachment

**Detection:** ask once: "Does [tool] email you a daily or weekly summary? If yes, what's the typical sender or subject so I can find it?"

If detected, extract data from the email body or its attachments (apply Tier 4 file-handling rules to any attached PDF / CSV / XLSX). If not, drop to Tier 4.

### Tier 4 — Manual paste / upload / screenshot (always works)

Last-resort fallback. The user provides data in-conversation:

- **Paste:** Free-form text. The skill ingests, normalizes column names internally, and asks one question only if a critical field is missing.
- **Upload:** CSV / XLSX / PDF. The skill parses the file. For XLSX with macros, see Section 6.A.
- **Screenshot:** Image of a dashboard. The skill uses vision to extract metrics, color-coding, and trend signals (apply `dashboard-parsing.md` "Screenshot (Vision)" logic).

Default to CSV upload if the user offers a choice; otherwise honor the user's preference. Never ask for more than one format at once.

### Tier selection log

When discovery completes, surface the access path per tool once so the user knows what to expect:

> "Here's how I'll pull data this conversation:
> - [CRM tool] → Tier 1 (native MCP)
> - [CS Platform] → Tier 2 (Drive folder /CS Snapshots/)
> - [Helpdesk] → Tier 3 (daily digest email)
> - [VoC tool] → Tier 4 (paste when needed)"

## Section 4 — MCP Connector Availability Snapshot (per category)

**Critical: this table is a STARTING POINT, not authoritative state.** The MCP registry changes frequently. The skill MUST verify at runtime by attempting tool discovery; do not trust this table.

| Category | Tools likely with native MCP (Apr 2026) | Default tier if MCP absent |
|---|---|---|
| 1. CS Platforms | None widely known | Tier 2 / 3 / 4 |
| 2. CRM | Salesforce (vendor), HubSpot (vendor) likely; verify others | Tier 2 / 3 / 4 |
| 3. Helpdesk | Zendesk (vendor) likely; verify others | Tier 2 / 3 / 4 |
| 4. Customer Comm | Intercom (vendor) likely; verify others | Tier 2 / 3 / 4 |
| 5. VoC / NPS | None widely known | Tier 3 (digest emails common) |
| 6. Conv Intelligence | Otter.ai, Fathom possibly; verify | Tier 4 (transcript paste) |
| 7. Product Analytics | Amplitude, Mixpanel possibly; verify | Tier 2 (export to Drive) |
| 8. Onboarding | None widely known | Tier 2 / 3 |
| 9. Knowledge Base | Atlassian Confluence (vendor) likely | Tier 4 |
| 10. Project / Work Mgmt | Notion (vendor), Asana (vendor), Atlassian Jira (vendor), Linear (vendor) likely | Tier 4 |
| 11. Product Feedback | None widely known | Tier 2 / 3 |
| 12. Customer Data | None widely known for the listed tools | Tier 2 (CSV export) |
| 13. BI / Reporting | None widely known for Tableau / Looker | Tier 2 / 3 (PDF / CSV export) |
| 14. Billing | Stripe (vendor) likely | Tier 2 / 3 |
| 15. Community | None widely known | Tier 3 / 4 |
| 16. Productivity (universal) | Google Calendar, Gmail, Drive (Anthropic); Notion (vendor); Outlook (verify) | Always Tier 1 if connected |
| 17. Document & Contract | DocuSign possibly; verify | Tier 3 / 4 |

**Rule:** Treat every row as "verify at runtime." Do not embed assumptions about specific tools' MCP availability in any briefing response. The runtime check always wins over this table.

**Zapier bridge:** For tools without a native MCP connector, the user may have a Zapier MCP that exposes the tool's actions. Try this between Tier 1 and Tier 2 — but never assume Zapier is connected without verifying.

## Section 5 — Persistence

**In-conversation only for v1.** The skill stores category selections, named tools, and access tiers as conversation context. Future invocations in the same conversation skip discovery. New conversations re-run it.

**No file persistence.** The skill MUST NOT write the user's stack to any file (no `~/.claude/cs-stack.json`, no project-level config). Reasons:
- The user's stack changes (tools added, removed, swapped)
- File-based persistence creates a stale-data risk
- The discovery flow takes ~60 seconds; the cost of re-running per conversation is low
- Avoiding file writes simplifies privacy posture

**Signals to re-trigger discovery within a conversation:**
- User mentions a tool not in the original stack
- User says "we switched from X to Y"
- User says "I just connected [tool]"
- A connector that worked earlier now returns auth errors
- The user names a category not asked about in Step 1

When re-triggered, ask only about the changed item — don't re-run the full Step 1 checklist.

## Section 6 — Power User Input Handling (Level 4)

CS professionals span four automation maturity levels:

- **Level 1 — Manual:** paste / upload only. Handled by Tier 4.
- **Level 2 — Basic tools with MCP.** Handled by Tier 1.
- **Level 3 — Drive / Gmail workarounds.** Handled by Tiers 2 and 3.
- **Level 4 — Power users:** Tableau dashboards exported as PDF / CSV / XLSX with macros, n8n workflows pushing data to webhooks or Drive, Gemini Scheduled Actions generating daily summaries, Clay tables with enriched account data, custom spreadsheets with pivots and macros.

Level 4 needs explicit handling rules. Apply these whenever the input pattern matches.

### 6.A — Tableau / Excel with macros

Accept the OUTPUT file (PDF, CSV, XLSX). Never try to execute macros.

- **PDF dashboards (Tableau export):** Treat as screenshot. Use vision to extract metrics, color-coding, and chart trends. Apply `dashboard-parsing.md` "PDF Dashboards" logic.
- **CSV exports:** Parse as plain CSV. Normalize column names internally. Ignore any embedded formulas — the export already has resolved values.
- **XLSX exports with macros:** Read the SAVED VALUES only. Strip all formulas. Do not execute macro VBA, do not interpret macro code, do not render embedded macros' last output as live data. If the workbook has multiple sheets, ask once: "Which sheet has the data you want me to use?" before parsing.

If a Tableau / Excel file produces zero readable values (corrupted, password-protected, or all data is locked behind macros), invoke Section 6.E.

### 6.B — n8n and other automation outputs

n8n, Zapier, Make, and similar automation tools typically deposit their outputs in:
- Files in Drive — handled via Tier 2
- Messages in Slack — handled via existing `slack-integration.md`
- Emails in Gmail — handled via Tier 3
- Webhooks — out of scope; the skill does not subscribe to webhooks directly

**Rule: do NOT attempt to connect to n8n / Zapier / Make directly.** Consume whatever they deposit in accessible locations. If a user describes "my n8n workflow generates a daily account-health summary in Drive," ask the user to point at the Drive file (or share it via the Drive connector) — the skill reads the output, not the workflow.

If the n8n output is a custom format the skill does not recognize (proprietary JSON, custom CSV column names), apply Section 6.E.

### 6.C — Gemini Scheduled Actions and other AI-generated summaries

Accept as text paste or email content. Apply this flag in the briefing output:

> "Note: this input appears to be an AI-generated summary, not raw data. I'll use it but the signals here are pre-processed — accuracy depends on the upstream AI. If something looks off, double-check against the source dashboard."

**Detection signals for AI-generated input:**
- Phrases like "Today's summary," "Generated on," "Based on data from"
- Highly structured prose with little numerical detail
- Bullet lists with consistent formatting that looks templated
- Author signature mentions Gemini, ChatGPT, Claude, or another LLM

Surface the flag once at the start of the relevant section of the briefing, not on every line.

### 6.D — Clay tables and customer data platforms

Accept Clay (and Segment, Clearbit, ZoomInfo, Bombora, etc.) output as CSV export or pasted table. Normalize columns internally.

Enrichment fields that supplement health scoring and expansion analysis:
- Company size (employees, ARR band, revenue band)
- Industry / vertical
- Tech stack signals (HG Insights, BuiltWith)
- Role / title detail for contacts
- Intent signals (Bombora, G2 intent)

Treat enriched fields as supplementary signals — they enrich analysis but do not override account-health data the user provided directly.

### 6.E — Graceful degradation (unrecognizable input)

If the input format is unrecognizable (corrupted file, binary blob, unsupported encoding, password-protected, empty after parsing), the skill MUST respond:

> "I couldn't parse this file format. Can you export it as CSV, paste the key data as text, or share a screenshot? I work best with any of those."

**Hard rules:**
- Never error silently. The user gets an explicit message about what failed and what alternatives work.
- Never hallucinate data from a file the skill couldn't read. If the parser returned nothing, the skill returns nothing — not a "best guess."
- Never claim the file was processed successfully when it wasn't. If 3 of 5 sheets parsed and 2 failed, say so explicitly.
- Never blame the user. Phrasing is "I couldn't parse this," not "your file is broken."

## Cross-References

- `calendar-integration.md` — Google Calendar / Outlook API and OOO detection
- `email-integration.md` — Gmail / Outlook filtering and response detection
- `slack-integration.md` — Slack mentions, threads, urgency signals
- `notion-integration.md` — Notion task fetching and entity extraction
- `dashboard-parsing.md` — Dashboard parsing across formats (HTML, CSV, XLSX, PDF, screenshot)
- `role-jtbd-matrix.md` — Role-specific prioritization (including Customer Success tier)
- `worked-examples.md` — CSM, CS Manager, VP CS morning briefing examples
