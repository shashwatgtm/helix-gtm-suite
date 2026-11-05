# Helix GTM Suite: 85 free B2B GTM tools and skills (shashwatgtm/helix-gtm-suite)
Built by Shashwat Ghosh, Co-Founder and Fractional CMO, Helix GTM Consulting (https://gtmhelix.com | https://tools.gtmhelix.com).

For founders, CMOs and CROs of growth stage B2B firms and their marketing, sales and customer success teams. Use it when a lean team has to make a go to market call (which motion leads, which customers to target, positioning, product market fit, a stalled deal, churn risk, a case study, an ROI case) and wants a proven method it can run today. 85 tools and skills: 48 tools in 6 hosted MCP connectors and 37 skills in 9 Claude plugins, plus companion skills.

## 1. Non-Negotiable Operating Rules (Parity with Claude & ChatGPT)
1. **3-Layer Operating Architecture**: Before running any skill in this package, read `references/operating-principles.md` (Layer 1) and `references/plugin-specific-rules.md` (Layer 2) first, then follow `SKILL.md` (Layer 3).
2. **Deterministic MCP Tool Sanctity**: When calling any connected Helix GTM MCP server over Streamable HTTP, never alter, recompute, or override its deterministic scores or arithmetic.
3. **Truthful Output & Placeholders**: Never fabricate customer metrics, competitor pricing, SLAs, or unverified claims. Mark missing user facts with `[User to add: ...]` and keep preset figures labelled as `Example figures: replace with your own`.
4. **House Style**: Use plain, direct, operator-grade prose. Never use em dashes or en dashes anywhere; use commas, colons, parentheses, or the word "to" for ranges.

## 2. Included Skills
The 37 skills of the 9 Helix GTM Claude plugins (the plugin repos hold the newest version of each):
* Customer success (5): `account-health-check`, `onboarding-plan`, `qbr-prep`, `renewal-save-plan`, `upsell-and-expansion`
* Events, PR and launches (4): `event-planner`, `event-speaker-kit`, `pr-launch-pack`, `event-follow-up-engine`
* ICP and customer insight (5): `icp-review`, `customer-interviews`, `lead-scoring-model`, `buying-role-hypotheses`, `pmf-check`
* Personal branding (3): `personal-branding-authority`, `handcrafted-voice-audit`, `newsletter-creation-curation`
* Research, market and account (4): `account-research`, `evidence-research-asset`, `claims-fact-check`, `second-opinion-review`
* Sales enablement (3): `competitive-intelligence`, `meeting-prep-debrief`, `sales-proposal-builder`
* Positioning and GTM strategy (3): `gtm-motion-picker`, `positioning-and-messaging`, `prompt-improver`
* AEO, built with Optise (6): `optise-helix-prompt-pack-builder`, `optise-helix-fitq-audit`, `optise-helix-race-audit`, `optise-helix-bluf-writer`, `optise-helix-eu-trust-centre`, `optise-helix-aeo-tracker`
* Deal execution (4): `deal-review-and-close-plan`, `discovery-and-buying-group`, `negotiation-and-champion`, `sales-sequences`

Companion skills in this package (earlier versions and connector guides): `epic-motion-diagnostic`, `impact-quick-positioning`, `craft-context-engineering`, `guard-gauge-diagnostic`, `guard-uplift-expansion`, `guard-activate-onboarding`, `guard-review-qbr`, `guard-defend-renewal`, `content-writing-thought-leadership`, `social-media-management`, `competitive-intelligence-market-research`, `executive-morning-briefing`, `helix-mcp-gtm-alpha`, `helix-mcp-craft-gtm`, `helix-mcp-craft-content`, `helix-mcp-impact-positioning`, `helix-mcp-icp-intelligence`, `helix-mcp-revenue-enablement`

## 3. Connected Streamable HTTP MCP Servers (6)
* `gtm-alpha`: `https://gtmalpha.gtmhelix.com/mcp` (GTM Alpha: 3 deterministic EPIC framework motion scoring and 180-day roadmap tools)
* `craft-gtm`: `https://craft-gtm.gtmhelix.com/mcp` (CRAFT GTM: 8 strategic GTM execution tools (PMF Scorecard, Launch Commander, Customer Interview Kit, Retention Playbook, Partner Architect, Crisis Planner, Competitive Intel, CRAFT GTM Analyzer))
* `craft-content`: `https://craft-content.gtmhelix.com/mcp` (CRAFT Content: 8 B2B content creation tools (Case Study Generator, Newsletter Builder, Webinar Script, Content Repurposer, Thought Leadership Series, Testimonial Capture, Sales Enablement Content, CRAFT Content Improver))
* `impact`: `https://impact.gtmhelix.com/mcp` (IMPACT: 8 hypothesis-driven B2B positioning and messaging tools)
* `icp-intelligence`: `https://icp-intelligence.gtmhelix.com/mcp` (ICP Intelligence: 9 ideal customer profile, TAM/SAM/SOM, buying group, and account prioritization tools)
* `revenue-enablement`: `https://revenue-enablement.gtmhelix.com/mcp` (Revenue Enablement: 12 deal strategy, MEDDPICC discovery, ROI business case, mutual action plan, and sales execution tools)
