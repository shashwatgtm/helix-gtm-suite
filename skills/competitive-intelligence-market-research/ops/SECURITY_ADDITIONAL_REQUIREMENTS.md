# Security Baseline (Lean Setup for Solo Operator)

This app can run safely with a minimal baseline. Advanced enterprise controls are optional.

## Required (Keep)
1. Use Clerk/Firebase/Railway managed secrets and platform defaults.
2. Keep separate dev and production environments.
3. Enable basic audit visibility (who changed pricing/prompt/policies).
4. Keep dependency updates monthly.
5. Keep backups enabled and test restore once per quarter.

## Not Required Right Now
- Complex SOC2-style control programs
- Dedicated security team processes
- Real-time SOC monitoring

## Practical Rule
If a control adds operational burden without clear current risk reduction, defer it.
