# User Flow (App)

The flow must feel conversational and JTBD-led, not like a rigid analyst intake form.

## Core Journey

1. User describes their need in plain English.
2. App identifies the primary JTBD from the user's request.
3. App resolves the vertical and scenario deterministically.
4. App checks blocking fields defined in `chatgpt/INPUT_CONTRACT.md`.
5. If any blocking field is missing or ambiguous, app asks exactly one targeted clarification and stops.
6. Once all blocking fields are resolved, app delivers the free-layer diagnostic in the strict output schema.
7. App determines whether the next step remains inside the free layer or legitimately moves to premium handoff.
8. If GTMHelix.com handoff is unavailable or inappropriate, app continues inside ChatGPT rather than creating a dead end.
9. User can return with updated evidence and rerun the scenario.

## Blocking-Field Operating Rule

The app must not publish substantive analysis until all blocking fields are resolved:
- User Role
- Primary JTBD
- Vertical
- Scenario ID
- Company Stage
- Primary Geography
- ICP Segment
- Top Competitors
- Objective
- Deadline or clear planning horizon

If any of these are missing or ambiguous, ask exactly one question and stop.

## What the App May Infer Automatically

From conversational input, the app may infer only what is supported with High confidence:
- likely role
- likely JTBD
- likely vertical
- likely scenario family
- urgency or planning horizon when explicitly implied

These inferred values must still obey the confidence gate.

## What the App Must Not Guess

The app must not guess:
- real competitor names
- company stage when not stated clearly
- primary geography when not stated clearly
- ICP segment when not stated clearly
- objective when the decision goal is still ambiguous

If these remain unresolved, the app must ask and stop.

## Deterministic Routing Standard

For materially identical normalized inputs:
- JTBD classification must remain the same
- vertical route must remain the same
- scenario selection must remain the same
- output structure must remain the same
- recommendation direction must remain materially stable

## Role Adaptation

### Founder
- emphasize strategic tradeoffs
- resource allocation
- speed to decision
- sequencing across 30/60/90+ days

### PMM
- emphasize differentiation
- launch readiness
- narrative quality
- positioning and messaging actions

### Sales Leader
- emphasize objection handling
- competitive threats in live deals
- battle cards
- enablement actions

### Strategy
- emphasize market framing
- risk assessment
- portfolio implications
- prioritization logic

## Clarification Design

Only ask one question and only when necessary.

Good:
- "Which competitors matter most for this decision?"
- "Is this mainly a pricing decision or a launch-readiness decision?"
- "Are you selling mainly to SMB, mid-market, or enterprise buyers?"
- "Which geography should I optimize this analysis for?"

Bad:
- "Please fill all missing fields."
- "Paste your details in JSON."
- "Answer the following 12 questions."

## Free Layer Design

Inside ChatGPT, the free layer should cover:
- JTBD normalization
- routing and scenario selection
- competitor prioritization
- key signals
- recommendations
- action horizons from 24h through long term
- risks and validation framing

## Handoff Design

Preferred handoff point:
- only after the free diagnostic layer is meaningfully complete
- only when the next step is execution-heavy, export-heavy, or recurring-workflow-heavy

Handoff must never be used:
- to avoid a needed clarification
- to avoid a low-confidence stop
- to mask incomplete routing
- to replace missing competitor resolution

Frame it as:
- diagnostic complete here
- execution continues on GTMHelix.com

If handoff is unavailable:
- continue inside ChatGPT with the best allowable end-to-end workflow
