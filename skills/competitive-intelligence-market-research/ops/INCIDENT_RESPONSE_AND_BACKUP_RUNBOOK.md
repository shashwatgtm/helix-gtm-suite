# Incident Response + Backup/Restore Runbook

## 1) Severity Levels
- **SEV-1:** service down/data exposure/payment failure at scale
- **SEV-2:** major functionality degraded
- **SEV-3:** minor degradation or isolated issue

## 2) Response SLA
- Acknowledge incidents within 30 minutes for SEV-1/SEV-2
- User-facing update within 60 minutes for SEV-1

## 3) Escalation
- Primary escalation: `shashwat@gtmhelix.com`

## 4) Incident Steps
1. Detect and triage
2. Contain blast radius
3. Preserve logs/evidence
4. Mitigate and recover
5. Post-incident review within 48 hours

## 5) Backup Policy
- Daily automated backups of critical app data/config snapshots
- Retention: 30 days rolling (minimum)

## 6) Restore Procedure (High-Level)
1. Identify last known good backup
2. Restore to staging and verify integrity
3. Promote restore to production with maintenance notice
4. Validate auth, payments, and analytics event ingestion
5. Close incident and log root cause/actions
