# Access Control Matrix (Admin / Operator / Support)

| Capability | Admin | Operator | Support |
|---|---|---|---|
| Manage plans/pricing/paywall | Yes | No | No |
| Modify system prompt/contracts/taxonomy | Yes | Yes | No |
| Publish scenario/template updates | Yes | Yes | No |
| View user workspace content | Yes (limited need basis) | Yes (limited need basis) | Read-only (ticket-bound) |
| Access billing dashboard (Dodo) | Yes | No | Read-only |
| Trigger refunds/cancellations | No (policy: none) | No | No |
| Manage auth roles (Clerk) | Yes | No | No |
| Access analytics dashboard | Yes | Yes | Read-only |
| Incident commander role | Yes | Backup only | No |
| Execute backup/restore runbook | Yes | Yes (with approval log) | No |

## Principles
- Least privilege by default
- Time-bound elevated access
- Ticket ID required for customer-data access
- Quarterly access review
