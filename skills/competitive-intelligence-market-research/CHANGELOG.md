# Changelog

## v1.5.1
- Rewrote MCP deployment guide into strict one-command-at-a-time Windows PowerShell steps for first-time users.
- Added recursive RCA section explaining why prior instructions were hard to follow and what changed.
- Added explicit failure branch (`railway status/logs/domain` + `curl.exe`) for "Deploy failed" and Railway "Not Found" outcomes.
- Updated owner one-step guide to enforce one-command execution and mandatory diagnostics on failure.

## v1.5.0
- Switched MCP runbook to Railway-first 24x7 deployment (no local tunnel dependency for final URL).
- Added one-block PowerShell flow for Railway deploy and domain retrieval.
- Updated owner step to require Railway MCP deployment before connector submission.

## v1.4.9
- Hardened MCP PowerShell script by removing JavaScript template literals to prevent copy/paste quote corruption.
- Added troubleshooting note to paste JS block exactly without manual edits.

## v1.4.8
- Removed outdated duplicate MCP script section to avoid conflicting instructions.
- Kept only corrected McpServer + zod PowerShell block.

## v1.4.7
- Fixed PowerShell MCP block to use `McpServer` + `zod` tool registration (avoids schema-literal runtime error).
- Fixed package.json script update logic for PowerShell JSON object edge case.
- Added explicit note to not paste markdown fence lines in terminal.

## v1.4.6
- Added a single copy-paste PowerShell block for end-to-end MCP setup in `C:\Users\shash`.
- Included session-aware `/sse` + `/messages` minimal MCP server example and connector URL instruction.

## v1.4.5
- Replaced MCP guidance with PowerShell-first copy-paste setup commands for creating and exposing an MCP server.
- Clarified MCP URL must be public MCP endpoint (`/sse`) and not normal website URL.
- Updated owner Step 2 wording to explicitly use the PowerShell MCP setup flow.

## v1.4.4
- Added MCP server URL guide with noob-friendly setup steps and error fixes.
- Updated owner playbook to make MCP connector setup the current first task before Store submission.
- Added README link to MCP setup guide.

## v1.4.3
- Added noob-friendly ChatGPT Store submission playbook with copy-paste listing text, validation prompts, and submission checklist.
- Linked playbook from owner one-step guide and README operations section.

## v1.4.2
- Switched to Store-first rollout: complete ChatGPT app approval before enabling paywall.
- Updated monetization threshold to 30% depth (post-approval) with 2 free runs.
- Deferred `gtmhelix.com` policy page publication to post-approval phase.
- Reordered owner step-by-step guide for MVP-first execution.

## v1.4.1
- Recorded owner-confirmed private repository step as completed in the one-step guide.
- Advanced next single owner action to policy page publication (Step 2).
- Updated gate status notes in MVP plan with privacy completion.

## v1.4.0
- Simplified security guidance to a lean solo-operator baseline.
- Added one-person compliance implementation plan with 24h/48h/1-week SLA bands.
- Added owner one-step-at-a-time execution guide and gate progression (G2 -> G3).
- Updated launch FAQ and README links for private repo + noob-friendly execution.

## v1.3.0
- Added Privacy Policy, Terms of Service, Enterprise DPA, and GDPR/UK GDPR checklist docs.
- Added security add-ons guidance, access control matrix, and incident backup/restore runbook.
- Added billing/refund/tax policy (no refund/cancel, advance payment, Dodo handling).
- Added paywall/CTA copy, SLA/escalation policy, and cross-domain analytics attribution design.
- Added launch FAQ on repo privacy and Store publication responsibilities.

## v1.2.0
- Expanded region coverage to India, APAC, MEA, US, UK, EU, Global.
- Clarified supported company types (B2B SaaS, AI-led software, B2B services marketing).
- Added explicit exclusions and category routing clarifications for ST/HR/FT/OT.
- Updated monetization default to 40% free threshold and 2 free runs before paid CTA.
- Added app readiness approvals checklist and status notification templates.

## v1.1.0
- Added App-first execution assets for all 24 scenarios.
- Added contracts, scenario cards, templates, examples, and eval framework.
- Added safety boundaries and role-based user flow.
