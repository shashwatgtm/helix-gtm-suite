# Standard Taxonomy (ST / HR / FT / OT)

This file removes ambiguity in scenario routing by mapping each vertical to standard market categories commonly used by analyst ecosystems (Gartner/Forrester-style category language) and review platforms (G2-style software categories).

## Audience and Company Type Coverage

This app supports:
- B2B SaaS companies
- AI-led software companies (B2B)
- Services marketing teams for B2B companies

Global market coverage includes:
- India
- APAC
- MEA
- US
- UK
- EU

---

## ST = Sales Tech & Revenue Growth Tech

### Definition
Software used by revenue teams to create demand, progress pipeline, and close deals.

### In-Scope Product Categories
- CRM platforms
- Sales Engagement Platforms
- Revenue Intelligence / Conversation Intelligence
- Sales Performance Management
- CPQ (Configure, Price, Quote)
- Lead/Data Enrichment for Sales
- Sales Enablement Platforms
- Marketing Automation (B2B)
- B2B marketing software used for pipeline generation

### Out of Scope (route elsewhere)
- Hardware product marketing

### Typical Buyers
CRO, VP Sales, RevOps, VP Marketing, Demand Gen Leaders

---

## HR = HR Tech (Narrow Scope)

### Definition
Software for core HR workflows except excluded domains listed below.

### In-Scope Product Categories
- Core HRIS/HCM workflows (non-payroll deep processing)
- Talent acquisition workflows excluding LMS/performance/talent intelligence modules

### Explicit Exclusions
- Payroll processing
- Learning Management (LMS)
- Performance Management
- Workforce Planning
- Talent Intelligence

### Typical Buyers
CHRO, VP People, Talent Acquisition, HR Ops

---

## FT = Fintech (B2B, Controlled Scope)

### Definition
Software and infrastructure enabling regulated or finance-adjacent transaction workflows.

### In-Scope Product Categories
- Payment Processing / Payment Orchestration
- Spend Management / Expense Platforms
- Digital Banking Infrastructure

### Explicit Exclusions
- Underwriting Platforms
- Treasury / Cashflow Intelligence
- Wealth / Investment Operations Platforms

### Typical Buyers
CFO, Head of Finance, Head of Payments, Risk/Compliance

---

## OT = Ops Tech (Operations + Product Operations)

### Definition
Software used to run internal operations, delivery, product operations, and process reliability.

### In-Scope Product Categories
- Workflow Automation
- Project/Program Management
- IT Service Management (ITSM)
- Observability / Infrastructure Monitoring
- DevOps / Release Tooling
- Field Operations / Logistics Operations Platforms
- B2B Cybersecurity software
- Vertical SaaS products
- Services marketing operations tooling

### Out of Scope (route elsewhere)
- Pure CRM/sales execution products (route to ST)
- Financial transaction rails (route to FT)
- Hardware product marketing

### Typical Buyers
COO, VP Operations, CIO/CTO, CISO, IT Ops, Delivery Leaders

---

## Category Routing Clarifications (Requested)

- **B2B Cybersecurity products** -> OT
- **Vertical SaaS products** -> OT by default; ST if primary JTBD is revenue execution
- **CRMs** -> ST
- **Marketing Automation** -> ST
- **B2B Marketing software** -> ST by default; OT if use case is internal delivery operations

---

## Routing Rules (Tie-Breakers)

1. Route by **primary business outcome** (revenue, people, money movement, operations reliability).
2. If multi-category product, route by **economic buyer** and immediate JTBD.
3. If still ambiguous, ask one clarification:
   - “Is your primary decision about revenue execution, people operations, financial rails, or operational reliability?”
4. Record final route in output header:
   - `Vertical Route: ST|HR|FT|OT (confidence: High|Medium|Low)`
