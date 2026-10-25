# ChatGPT Store Submission Playbook (Final Testing and Submission)

This version assumes the app is a conversational JTBD-led competitive intelligence copilot with deterministic routing, blocking-field enforcement, stable output behavior, and fallback continuity when GTMHelix.com handoff is unavailable.

## 0) Final Files to Use

Use these files as the runtime basis:
- `chatgpt/SYSTEM_PROMPT.md`
- `chatgpt/INPUT_CONTRACT.md`
- `chatgpt/OUTPUT_SCHEMA.md`
- `chatgpt/TAXONOMY_STANDARD.md`
- `chatgpt/SCENARIO_INDEX.md`
- `chatgpt/USER_FLOW.md`
- `chatgpt/STATUS_NOTIFICATION_TEMPLATES.md`
- `growth/PAYWALL_AND_CTA.md`

Scenario behavior comes from:
- `scenarios/*.md`

## 1) Store Listing Copy

### App Name
`GTM Helix Competitive Intelligence Copilot`

### One-line Tagline
`Understand the JTBD, route the right scenario, and get decision-ready competitive intelligence with structured action plans.`

## 2) Positive Smoke Test Prompts

1. We are a Series B sales tech company in India selling to mid-market. Need pricing intelligence against Apollo, Outreach, and Salesloft before next Friday.
2. We are launching an HR tech product in the UK against Rippling, Deel, and Darwinbox in 3 weeks. Are we ready?
3. We are a fintech company in MEA and need a strategic positioning narrative versus Stripe, Adyen, and Checkout.com.
4. We sell cybersecurity software into US enterprise buyers. Give me a feature-gap analysis versus CrowdStrike, SentinelOne, and Microsoft.
5. Need a battle card for tomorrow. We compete with HubSpot, Salesforce, and Zoho.

## 3) Blocking-Field Clarification Tests

The app must ask exactly one question and stop for each case below.

1. We are a Series B company in India. Help us.
   - Expected: asks for seller role only.

2. We are a PMM at Acme. Help us.
   - Expected: asks for JTBD only.

3. We compete with Salesforce and HubSpot. Help us position.
   - Expected: asks only for the highest-priority unresolved blocking field after seller role and company are resolved.

4. Need pricing intelligence for our category before next month.
   - Expected: asks only for seller role if missing; otherwise asks only for company; otherwise asks only for the next highest-priority unresolved field.

5. We need a competitor analysis.
   - Expected: one targeted question only, no lists and no connector/tool explanation.

## 4) Hard Failure Tests

The app must fail these cases safely:
- asks more than one question in a single clarification response
- asks for a field already supplied by the user
- includes bullets in clarification-only mode
- includes tool chatter or connector narration before readiness
- provides partial guidance before blocking fields are resolved
- publishes substantive analysis with missing seller role
- publishes substantive analysis with missing company

## 5) Deterministic Routing Tests

For materially identical inputs across repeated runs, confirm:
- same JTBD classification
- same vertical route
- same scenario route
- same output section order
- materially same recommendation direction

## 6) Final Submission Checklist

- [ ] Runtime prompt updated
- [ ] Input contract aligned with seller role and company first-gate rules
- [ ] Output schema aligned with clarification-only enforcement
- [ ] Store playbook updated with one-question and no-tool-chatter failure tests
- [ ] Clarification-only behavior verified
- [ ] No substantive output before seller role and company are resolved
- [ ] Deterministic routing verified across repeated runs
- [ ] Ready to submit for review
