# Owner Actions (One Instruction at a Time)

## Current Gate Status
- G0: Approved
- G1: Approved
- **Current: Move to G2 (Scenario Coverage Sign-off)**
- G3: Pending (quality calibration)

## Step 1 (Completed)
Repository visibility set to private (owner-confirmed).

## Step 2 (Do this now)
Deploy MCP on Railway (24x7) and set connector URL using `ops/MCP_SERVER_URL_AND_NEXT_STEPS.md`.

Important for Step 2:
- Run commands in **Windows PowerShell**.
- Execute **one command at a time**.
- If deploy fails, run the diagnostics in Section 3 of `ops/MCP_SERVER_URL_AND_NEXT_STEPS.md` before doing anything else.

## Step 3
Complete ChatGPT Store submission activities for MVP using `ops/CHATGPT_STORE_SUBMISSION_PLAYBOOK.md`:
- Finalize app listing copy and category
- Validate prompt/schema behavior with eval prompts
- Submit app for review/approval

## Step 4
Run G2 checklist:
- Confirm all 24 scenarios map cleanly and are usable.
- Confirm taxonomy routing for ambiguous categories.

## Step 5
Run G3 checklist:
- Execute eval prompts
- Confirm scoring methodology threshold
- Fix low-scoring scenarios

## Step 6 (After app approval)
Enable paywall in app logic:
- Trigger after 2 free runs OR 30% depth.
- Use CTA text from `growth/PAYWALL_AND_CTA.md`.

## Step 7 (After app approval)
Implement cross-domain handoff token tracking per `growth/ANALYTICS_CROSS_DOMAIN_TRACKING.md`.

## Step 8 (After app approval)
Publish policy pages on `gtmhelix.com`:
- Privacy Policy
- Terms of Service
- Enterprise DPA
- GDPR/UK GDPR checklist

## Step 9
Enable support channel SLA:
- Response within 24 hours
- Escalation to `shashwat@gtmhelix.com`

