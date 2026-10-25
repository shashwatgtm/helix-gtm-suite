# Input Contract (Internal Normalized Fields for Every Run)

This contract exists for internal normalization, not as a rigid user-facing form.

The app must accept natural conversational input and map it into the fields below.

## Operating Principle

- Do not require the user to paste JSON.
- Do not force the user through a form unless the builder UI explicitly requires it.
- Infer only what can be inferred with High confidence.
- Ask exactly one targeted clarification only when a blocking field is missing or ambiguous.
- Do not publish substantive analysis until all blocking fields are resolved.
- Do not guess real competitor names.
- Seller role and company identity are mandatory first-gate fields.

## Internal Normalized Fields

1. **Seller Role**
   - founder | pmm | sales-leader | strategy | inferred-other

2. **Company**
   - company name or product/company identifier

3. **Primary JTBD**
   - market-sizing
   - feature-gap-analysis
   - pricing-intelligence
   - customer-sentiment
   - launch-readiness
   - strategic-positioning
   - battle-card
   - mixed-other

4. **Company Type**
   - b2b-saas
   - ai-led-software
   - b2b-services-marketing

5. **Vertical**
   - ST | HR | FT | OT

6. **Scenario ID**
   - ST-01..ST-06
   - HR-01..HR-06
   - FT-01..FT-06
   - OT-01..OT-06

7. **Company Stage**
   - series-a
   - series-b-c
   - series-d-plus

8. **ARR Range**
   - numeric band or not-provided

9. **ACV Range**
   - numeric band or not-provided

10. **Primary Geography**
   - india | apac | mea | us | uk | eu | global

11. **ICP Segment**
   - smb | mid-market | enterprise | mixed

12. **Top Competitors**
   - 1 to 5 real company names only
   - user-provided or explicitly resolved through approved category intelligence sources
   - never placeholders

13. **Objective**
   - one-sentence decision goal

14. **Deadline**
   - date, timeframe, or urgency window

15. **Known Constraints**
   - budget
   - legal/compliance
   - data availability
   - team bandwidth
   - messaging constraints
   - no known constraints

16. **Available Evidence**
   - links
   - notes
   - market observations
   - customer quotes
   - internal assumptions only
   - no evidence provided

17. **Taxonomy Confirmation**
   - final route using `chatgpt/TAXONOMY_STANDARD.md`

18. **Free vs Premium Stage**
   - clarification
   - free-diagnostic
   - handoff-eligible
   - premium-requested

## Blocking Fields Required Before Publishing Any Substantive Analysis

The app must not publish substantive analysis unless all of the following are resolved:

- Seller Role
- Company
- Primary JTBD
- Vertical
- Scenario ID
- Company Stage
- Primary Geography
- ICP Segment
- Top Competitors
- Objective
- Deadline or clear planning horizon

If any blocking field is missing or ambiguous, ask exactly one targeted clarification question and stop.

## Deterministic Routing Order

Resolve fields in this order:

1. Seller Role
2. Company
3. Primary JTBD
4. Vertical
5. Scenario ID
6. Top Competitors
7. Primary Geography
8. ICP Segment
9. Company Stage
10. Objective
11. Deadline

Do not let monetization logic override routing or quality gates.

## Clarification Priority Order

When multiple blocking fields are missing, ask for the one with the highest decision value in this order:

1. Seller Role
2. Company
3. Primary JTBD
4. Vertical route
5. Top Competitors
6. Primary Geography
7. ICP Segment
8. Company Stage
9. Objective
10. Deadline

Ask only one question at a time.

## Validation Rules

- If seller role is missing, ask for seller role first and stop.
- If company is missing, ask for company next and stop.
- If JTBD is ambiguous, ask one route-setting question.
- If vertical fit is ambiguous, use `chatgpt/TAXONOMY_STANDARD.md` tie-breakers.
- If scenario fit is ambiguous, choose no scenario yet and ask one clarification.
- If competitor names are missing, ask for them or resolve them through approved category intelligence sources before publishing.
- Never invent competitor names.
- If company stage, geography, or ICP are unclear, ask and resolve them before publishing.
- If evidence is thin, outputs may still proceed only if blocking fields are resolved and confidence remains High or Medium.
- Never fabricate customer evidence, pricing precision, market numbers, or deployment claims.
- Do not force the user to re-enter information already implied in the conversation.

## Confidence Gate

- **High**: publish
- **Medium**: publish with explicit validation needs
- **Low**: do not publish substantive analysis; ask one short clarification explaining what is missing and why it blocks a reliable answer

## Variance Control Standard

For materially identical normalized inputs:
- routing must remain consistent
- scenario selection must remain consistent
- output structure must remain consistent
- recommendation direction must remain materially stable across repeated runs

Do not substitute colorful assumptions for missing facts.
