# GUARD Health Scoring Model — Gauge Mode Reference

## 6-Signal Weighted Diagnostic

Total score: 0-100. Each signal has a defined weight and scoring rubric.

### Signal 1: Product Adoption (0-20 points, weight 20%)

| Score | Criteria |
|-------|----------|
| 17-20 | 80%+ feature adoption vs entitlement, daily active usage, power users identified, new features adopted within 30 days |
| 13-16 | 60-79% adoption, weekly active usage, core workflows embedded, some features untouched |
| 9-12 | 40-59% adoption, bi-weekly usage, basic functionality only, multiple unused modules |
| 5-8 | 20-39% adoption, monthly or sporadic usage, limited workflows, declining login trend |
| 0-4 | Under 20% adoption, rare logins, no workflow integration, data export signals |

**Key inputs:** Login frequency, feature breadth (% of entitled features used), feature depth (advanced vs basic usage), usage trend (growing/stable/declining), time-in-product per session.

**When data is missing:** If no product usage data is available, score based on qualitative signals from CSM observations and customer conversations. Flag as "estimated — no telemetry" in the output.

### Signal 2: Engagement Quality (0-20 points, weight 20%)

| Score | Criteria |
|-------|----------|
| 17-20 | Multi-stakeholder engagement, exec sponsor active, customer initiates meetings, responsive within 24h, attends all QBRs |
| 13-16 | Primary contact engaged, exec sponsor accessible but passive, responds within 48h, attends most QBRs |
| 9-12 | Single contact only, exec sponsor unknown or disengaged, responds within a week, skips some meetings |
| 5-8 | Contact hard to reach, no exec sponsor, delayed responses, skipped last QBR, ghosting signals |
| 0-4 | No response to outreach, all meetings cancelled/skipped, contact may have left, no engagement for 30+ days |

**Key inputs:** Number of active stakeholders, executive sponsor engagement level, response time to CSM outreach, QBR/meeting attendance, customer-initiated touchpoints.

**Champion departure adjustment:** If the primary champion left in the last 90 days and no replacement is engaged, subtract 4 points from this signal regardless of other factors.

### Signal 3: Value Realization (0-20 points, weight 20%)

| Score | Criteria |
|-------|----------|
| 17-20 | Documented ROI exceeding original business case, customer references/case study willingness, value communicated to their leadership |
| 13-16 | Measurable outcomes achieved, customer acknowledges value verbally, some goals met |
| 9-12 | Partial value realized, some goals met but gaps remain, customer unsure of full ROI |
| 5-8 | Limited value visible, original goals not being tracked, customer questioning investment |
| 0-4 | No measurable value, customer unable to articulate what they get from the product, "shelf-ware" risk |

**Key inputs:** Business outcomes vs original success criteria, ROI documentation, customer's own assessment of value, NPS/CSAT trend, willingness to be a reference.

### Signal 4: Sentiment Trajectory (0-15 points, weight 15%)

| Score | Criteria |
|-------|----------|
| 13-15 | NPS 9-10, CSAT improving, positive unsolicited feedback, advocacy behavior (referrals, reviews, speaking at events) |
| 10-12 | NPS 7-8, CSAT stable, generally positive, no complaints |
| 7-9 | NPS 5-6, CSAT flat or slightly declining, mixed feedback, some frustration signals |
| 4-6 | NPS 3-4, CSAT declining, escalations in last 90 days, negative sentiment in conversations |
| 0-3 | NPS 0-2, CSAT poor, multiple unresolved escalations, vendor review language, competitor mentions |

**Key inputs:** NPS score and trend, CSAT score and trend, support ticket sentiment, qualitative signals from calls/emails, social media mentions.

**Trajectory matters more than absolute score.** An NPS of 6 that was 8 last quarter is more alarming than an NPS of 6 that was 5 last quarter.

### Signal 5: Commercial Health (0-15 points, weight 15%)

| Score | Criteria |
|-------|----------|
| 13-15 | Pays on time, full contract utilization, no billing disputes, multi-year contract, expanding usage within entitlement |
| 10-12 | Pays on time, reasonable utilization, minor billing questions resolved quickly |
| 7-9 | Occasional late payments, underutilizing contract (paying for more than they use), some billing friction |
| 4-6 | Payment delays, significant underutilization, requesting contract restructuring, cost-cutting language |
| 0-3 | Overdue payments, requesting early termination terms, procurement involved in "vendor review", budget freeze language |

**Key inputs:** Payment timeliness, contract utilization rate (usage vs entitlement), billing dispute history, contract terms awareness, budget signals.

### Signal 6: Expansion Readiness (0-10 points, weight 10%)

| Score | Criteria |
|-------|----------|
| 9-10 | Customer actively asking about additional products/features, new departments exploring, growing headcount, requesting pricing for expansion |
| 7-8 | Positive signals (new use cases mentioned, org growing), but no active expansion conversation |
| 5-6 | Neutral — no expansion signals but no contraction signals either |
| 3-4 | Contraction signals — reducing seats, consolidating tools, cost-cutting initiatives |
| 0-2 | Active downsizing, budget cuts announced, RFP for replacement, competitor POC running |

**Key inputs:** Expansion conversations, new department interest, headcount changes, usage approaching plan limits, feature requests for advanced capabilities.

---

## Health Classification

| Total Score | Classification | Color | Action Cadence |
|-------------|---------------|-------|----------------|
| 80-100 | Healthy | Green | Monthly check-in, expansion focus |
| 60-79 | Needs attention | Yellow | Bi-weekly check-in, proactive value reinforcement |
| 40-59 | At risk | Orange | Weekly check-in, intervention plan required |
| 0-39 | Critical | Red | Immediate action, escalate to CS leadership |

## Batch Mode

When scoring multiple accounts, output a ranked table sorted by risk (lowest score first). Include:
- Account name, ARR, health score, classification, primary risk signal, recommended action this week.

## Incomplete Data Handling

CSMs rarely have complete data. Score what you have, flag what you do not:
- If 4+ signals scorable: Produce full assessment with caveats on missing signals.
- If 2-3 signals scorable: Produce partial assessment, recommend data collection as first action.
- If 0-1 signals scorable: Do not produce a score. Recommend a structured discovery call to gather baseline data.
