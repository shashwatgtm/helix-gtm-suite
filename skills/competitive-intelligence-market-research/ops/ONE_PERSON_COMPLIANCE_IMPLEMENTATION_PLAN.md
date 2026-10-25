# One-Person Compliance Implementation Plan

Designed for a solo founder/operator. Response windows are intentionally non-aggressive.

## SLA Bands
- **24 hours**: acknowledge inbound issue/request.
- **48 hours**: initial assessment + action plan.
- **1 week**: closure target for standard issues.

---

## Eventuality A: Privacy/Data Subject Request
Examples: access, correction, deletion, export.

### Identification
- Source: support email (`shashwat@gtmhelix.com`) or contact form.
- Record in a simple tracker with timestamp and requester email.

### Response Plan
1. **Within 24h**: acknowledge receipt and request identity verification.
2. **Within 48h**: confirm scope (what data/processors are involved).
3. **Within 1 week**: complete request or provide status + expected completion date.

### Artifacts to Update
- `legal/PRIVACY_POLICY.md`
- request log (internal)

---

## Eventuality B: Compliance Question (GDPR/UK GDPR)
Examples: lawful basis, transfer question, processor clarification.

### Identification
- Customer/prospect asks legal-compliance question.

### Response Plan
1. **Within 24h**: acknowledge and share policy links.
2. **Within 48h**: provide documented answer from checklists/DPA.
3. **Within 1 week**: if unresolved, escalate to external legal advisor.

### Artifacts to Update
- `legal/REGIONAL_COMPLIANCE_GDPR_UK.md`
- `legal/DPA_ENTERPRISE.md`

---

## Eventuality C: Suspected Security Incident
Examples: account misuse, accidental exposure, service compromise.

### Identification
- User report, unusual auth activity, service disruption.

### Response Plan
1. **Within 24h**: acknowledge + begin containment.
2. **Within 48h**: complete triage and communicate impact scope.
3. **Within 1 week**: publish post-incident summary + corrective actions.

### Artifacts to Update
- `ops/INCIDENT_RESPONSE_AND_BACKUP_RUNBOOK.md`
- incident log

---

## Eventuality D: Billing or Policy Dispute
Examples: refund request, cancellation request, charge dispute.

### Identification
- Support email or payment provider notice.

### Response Plan
1. **Within 24h**: acknowledge and cite billing policy.
2. **Within 48h**: provide case-specific decision and rationale.
3. **Within 1 week**: close ticket, document if policy wording needs refinement.

### Artifacts to Update
- `billing/BILLING_POLICY.md`
- `legal/TERMS_OF_SERVICE.md`

---

## Eventuality E: Backup/Restore Need
Examples: data corruption, accidental deletion, failed deployment.

### Identification
- User-reported data issue or internal detection.

### Response Plan
1. **Within 24h**: acknowledge and freeze impacted writes if needed.
2. **Within 48h**: execute restore validation in staging.
3. **Within 1 week**: production restore completed and verified.

### Artifacts to Update
- `ops/INCIDENT_RESPONSE_AND_BACKUP_RUNBOOK.md`

---

## Operating Cadence (Solo-Friendly)
- Weekly: review open compliance/security/billing tickets.
- Monthly: update dependency + policy wording if needed.
- Quarterly: test backup restore and verify policy links are live.
