# Universal Output Schema (All 24 Scenarios)

Use this exact section order for every substantive analysis response.

## Non-Negotiable Publishing Rule

Publish a substantive analysis only if:
- all blocking fields defined in `chatgpt/INPUT_CONTRACT.md` are resolved
- routing is explicit
- scenario selection is explicit
- confidence is High or Medium

If confidence is Low, do not use this schema.
Ask exactly one short clarification instead.

## 0) Output Header
- **Vertical Route:** ST | HR | FT | OT (confidence: High | Medium)
- **Scenario Route:** scenario ID + scenario name
- **Primary JTBD:** one line
- **Seller Role Lens:** Founder | PMM | Sales Leader | Strategy | inferred-other
- **Company:** company name
- **Free/Premium Stage:** clarification | free-diagnostic | handoff-eligible | premium-requested

## 1) Action Panel
- **Do in 24h** (3 bullets)
- **Do in 7d** (3 bullets)
- **Do in 30d** (3 bullets)
- **Do in 60d** (3 bullets)
- **Do in 90d** (3 bullets)
- **Medium term** (2-3 bullets)
- **Long term** (2-3 bullets)

## 2) Executive Summary
- Context recap (2-4 lines)
- Decision recommendation (1-2 lines)
- Why this matters now (1-2 lines)

## 3) JTBD and Context Normalization
- inferred or confirmed company context
- confirmed objective
- explicit constraints
- explicit evidence provided
- explicit assumptions made
- explicit missing-but-non-blocking items, if any

## 4) Competitor Snapshot
- Table: competitor | relevance | threat level | why now | confidence

## 5) Key Signals
- Pricing signals
- Product / feature signals
- GTM signals
- Buyer / category signals

Rules:
- separate evidence from interpretation where useful
- do not present unsupported specifics as fact
- do not fabricate pricing precision or market numbers

## 6) Recommendations
- 3-5 prioritized actions
- each action must include:
  - owner
  - expected outcome
  - confidence
  - what must be validated next

Rules:
- recommendations must be materially stable for materially identical normalized inputs
- recommendations must follow the selected scenario and role lens
- recommendations must not depend on invented competitors or speculative facts

## 7) Risks and Validation Needs
- Table: risk | impact | mitigation | confidence

Must include:
- evidence gaps
- missing-information warnings that are non-blocking
- validation steps required to move Medium confidence toward High

## 8) Deliverable Artifact
- scenario-specific artifact block users can copy into docs/slides
- artifact must match the selected scenario
- artifact must stay inside the free diagnostic boundary unless premium stage is already triggered legitimately

## 9) Handoff Decision

### If still in free layer
State:
- what has been completed
- what remains inside the free diagnostic layer
- what would trigger premium handoff next

### If handoff-eligible or premium-requested
Use approved language from `growth/PAYWALL_AND_CTA.md` and state:
- what diagnostic work has been completed
- why the next step belongs in GTMHelix.com
- exactly what unlocks on GTMHelix.com

Rules:
- do not trigger handoff before blocking fields are resolved
- do not trigger handoff to avoid asking a needed clarification
- do not use handoff language as a substitute for a weak answer

## 10) Sources and Assumptions
- explicit source list
- explicit assumptions list
- explicit confidence summary

Confidence summary rule:
- **High** = evidence and routing are strong enough to act now
- **Medium** = usable now, but named validations are still required
- **Low** must never appear in a published substantive analysis

## Clarification-Only Mode

If a blocking field is missing or confidence would otherwise be Low:
- ask exactly one short targeted clarification
- explain briefly why it is required
- do not output any other section from this schema
- the response must contain exactly one question and no bullets, lists, examples, tool narration, connector explanation, or partial analysis
