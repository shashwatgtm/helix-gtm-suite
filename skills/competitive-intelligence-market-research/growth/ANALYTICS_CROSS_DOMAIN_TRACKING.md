# Cross-Domain Analytics (ChatGPT -> gtmhelix.com)

Because chatgpt.com and gtmhelix.com are different domains, use a tokenized handoff approach.

## Event Model

### Events captured in ChatGPT-side workflow (app logic layer)
- `free_run_started`
- `free_run_completed`
- `paywall_shown`
- `handoff_link_clicked`

### Events captured on gtmhelix.com
- `handoff_landing_viewed`
- `signup_started`
- `signup_completed`
- `checkout_started`
- `payment_succeeded`

## Identity Stitching Pattern
1. Generate a short-lived handoff token when showing CTA.
2. Include token in gtmhelix URL query (example: `?handoff_token=...`).
3. On landing, exchange token for internal user/session ID.
4. Persist mapping in Firebase analytics table.
5. Attribute downstream conversion to source run/scenario.

## Minimum Attribution Fields
- source: `chatgpt_app`
- scenario_id
- vertical
- run_count
- paywall_reason (`depth_limit` or `run_limit`)
- handoff_token_id
- converted (bool)
- revenue_amount

## Why this works
You do not need shared cookies across domains; tokenized handoff provides deterministic attribution.
