# Paywall Copy and Upgrade CTA

## Monetization Position

The ChatGPT app should deliver a strong free diagnostic layer and then hand off to GTMHelix.com for the execution layer.

The free layer proves value.
The paid layer operationalizes value.

## Gating Precondition

Handoff is allowed only when all of the following are true:
- all blocking fields required by `chatgpt/INPUT_CONTRACT.md` are resolved
- routing is explicit
- scenario selection is explicit
- confidence is High or Medium
- the free diagnostic layer has actually been completed

Do not trigger handoff:
- to avoid asking a needed clarification
- when confidence would otherwise be Low
- when competitor resolution is incomplete
- when geography, ICP, company stage, role, JTBD, objective, or deadline are still unresolved
- as a substitute for weak or incomplete analysis

## Preferred Trigger Point

Use handoff at approximately 40% of total workflow depth once:
- the diagnostic layer is complete, and
- the user's next need is implementation-heavy, export-heavy, or recurring-workflow-heavy

This is the preferred operating trigger.

## Secondary Metering Trigger

After app approval, the product may also enforce handoff after either:
1. 2 free scenario runs, or
2. the user requests a premium export, implementation workflow, recurring monitoring, or team-ready execution pack

These metering rules do not override routing, evidence, confidence, or fallback rules.

## Fallback Rule

If GTMHelix.com handoff is unavailable, broken, disallowed by policy, or not appropriate for the current run, the app should continue inside ChatGPT and complete the best allowable end-to-end output instead of creating a dead end.

## What Stays Free Inside ChatGPT

Free diagnostic layer may include:
- JTBD capture and normalization
- deterministic scenario routing
- competitor prioritization
- initial key signals
- decision recommendation
- action plan through 24h / 7d / 30d / 60d / 90d / medium term / long term
- risk and validation framing

## What Moves to GTMHelix.com

Premium layer includes:
- detailed competitor teardown
- team-ready battle cards and decks
- full implementation workflows
- recurring tracking workspace and weekly updates
- premium templates and execution packs
- support-backed execution

## Primary Headline
**Unlock the Full Competitive Execution Pack**

## Supporting Copy
You have completed the free diagnostic layer. Continue on GTMHelix.com to unlock the execution layer:
- Detailed competitor teardown
- Team-ready battle cards and decks
- Execution workflows and premium templates
- Recurring tracking workspace and weekly updates
- Priority support with 24-hour response SLA

## CTA Buttons
- **Primary:** Continue on GTMHelix.com
- **Secondary:** See Plan Details

## Soft Handoff Text
"You have completed the diagnostic layer. Continue on GTMHelix.com to turn this into execution-ready artifacts, workflows, and recurring tracking."

## Hard Handoff Text
"You have reached the free analysis boundary. Continue on GTMHelix.com to unlock the full competitive execution pack."

## Handoff Failure Message
"GTMHelix.com handoff is not available right now. Continuing inside ChatGPT with the best available end-to-end workflow."

## Operational Rule

Inside ChatGPT:
- quality gates come first
- routing gates come second
- monetization comes third
- fallback continuity comes fourth when handoff is not available

## Implementation Note

For MVP review phase (pre-approval), keep hard enforcement disabled if store review requires it.

For post-approval production:
- enable the preferred 40% handoff logic
- optionally enable the 2 free runs policy
- never allow paywall logic to fire before answer-readiness gates are satisfied
- always preserve the in-ChatGPT fallback path
