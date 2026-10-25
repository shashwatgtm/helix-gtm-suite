# GUARD CS Metrics Glossary

## Revenue Metrics

**ARR (Annual Recurring Revenue):** Total annualized value of active subscription contracts. The primary measure of a CS team's portfolio value.

**NRR (Net Revenue Retention):** Revenue from existing customers at end of period divided by revenue from same cohort at start of period. Includes expansion, contraction, and churn. Target: 100%+ (net expansion). Formula: (Starting ARR + Expansion - Contraction - Churn) / Starting ARR.

**GRR (Gross Revenue Retention):** Revenue retained from existing customers WITHOUT expansion. Measures pure retention. Target: 90%+ for enterprise, 80%+ for SMB. Formula: (Starting ARR - Contraction - Churn) / Starting ARR.

**Expansion ARR:** Additional ARR from existing customers through upsell, cross-sell, or price increases. The CS team's revenue growth contribution.

**Logo Churn Rate:** Percentage of customers lost in a period. Formula: Churned Customers / Starting Customers. Target: under 5% annually for B2B SaaS.

**Revenue Churn Rate:** Percentage of ARR lost in a period. More meaningful than logo churn because losing a $500K customer is different from losing a $5K customer.

## Health Metrics

**Health Score:** Composite metric (0-100) combining multiple signals to assess account wellness. See `health-scoring-model.md` for the GUARD 6-signal model.

**NPS (Net Promoter Score):** Survey metric (-100 to +100). Promoters (9-10) minus Detractors (0-6). Useful as trend indicator, not absolute score. Industry benchmark for B2B SaaS: 30-50.

**CSAT (Customer Satisfaction Score):** Direct satisfaction rating, typically 1-5 or 1-10. Usually measured after specific interactions (support tickets, onboarding, QBR).

**CES (Customer Effort Score):** Measures how easy it is for the customer to accomplish their goal. Lower effort = higher retention. Often used post-support interaction.

## Adoption Metrics

**DAU/WAU/MAU:** Daily/Weekly/Monthly Active Users. Track adoption breadth over time.

**Feature Adoption Rate:** Percentage of available features actively used by the customer. Formula: Features Used / Features Available in their plan.

**Time to Value (TTV):** Days from contract start to first measurable value milestone. Shorter TTV correlates with higher retention. Target varies by product complexity.

**Activation Rate:** Percentage of users who complete key activation actions (defined per product). Leading indicator of retention.

## Engagement Metrics

**QBR Attendance Rate:** Percentage of scheduled QBRs where key stakeholders attend. Declining attendance is a churn risk signal.

**Response Time:** Average time for customer to respond to CSM outreach. Lengthening response times = engagement decline.

**CSM Touch Frequency:** Number of meaningful touchpoints per account per month. "Meaningful" excludes automated emails — only counts conversations, meetings, value-adding interactions.

## Operational Metrics

**Renewal Rate:** Percentage of contracts renewed at end of term. Denominator = contracts up for renewal, numerator = contracts renewed. Target: 90%+ by logo, 95%+ by ARR.

**Save Rate:** Percentage of at-risk accounts successfully saved from churn. Measured against accounts flagged as At Risk or Critical. Industry benchmark: 25-40%.

**Onboarding Completion Rate:** Percentage of new customers who complete all onboarding milestones within the defined timeframe (typically 90 days).

**Time to Renewal Decision:** Days before renewal date when the renewal outcome is confirmed. Earlier is better — indicates proactive management.

## Portfolio Metrics

**Accounts per CSM:** Number of accounts managed per CSM. Varies by segment: Enterprise 10-30, Mid-Market 30-80, SMB 80-200+ (tech-touch).

**ARR per CSM:** Total portfolio value per CSM. More meaningful than account count because it captures the weight of responsibility.

**At-Risk ARR:** Total ARR classified as At Risk or Critical. Track as percentage of total portfolio. Alert threshold: greater than 15% of portfolio ARR at risk.
