# Mutual close plan and account plan: the method

Rewritten for this skill from the Helix revenue enablement connector (mutual_action_plan_generator and account_plan_builder), read on 14 October 2026. No figure here is a benchmark.

## The mutual close plan (from today to signature)
A mutual close plan is written WITH the buyer, not for them: every step has an owner on the buyer side or the seller side, a date, and a status, and the buyer can edit it.

1. Confirm the target close date and why it matters to the BUYER (a go live, a budget year, a contract end). A date that matters only to the seller's quarter is a risk: say so.
2. List the buyer's own steps as the user gave them (security review, legal, procurement, budget approval, board). Never add a buyer step the user did not give as if it were known: write it as a question ("Is there a security review? Who runs it?").
3. Agree the pass mark before the evaluation starts: what result, measured how, on whose data, decides that the evaluation succeeded. Without it the evaluation has no end.
4. Run scripts/close_plan.py for the working day calendar: phases from the current stage to the close, phase lengths from example default weights, milestone dates inside each phase, holidays removed, warnings when the plan is short. Never write a date by mental arithmetic.
5. Put each step in a table: phase, step, owner (buyer or seller role), due date with weekday, status, what moves the date. A review the buyer runs on a document (a security questionnaire, a contract, a data processing agreement, a vendor form) gets its own milestones, never one line: returned (the seller's side), reviewed (the buyer's reviewer), approved (the buyer's approver), each with an owner and a date; pass all three to the script as steps of the phase where the review happens.
6. Name what can move the close date (a missing pass mark, a step with no owner, a review that has not started, a signer who has not seen the case) and the action for each.
7. Agree how both sides talk: a weekly check in with the champion, a short written update, who escalates.
8. Stop at signature. The plan after signature (onboarding) belongs to b2b-customer-success / onboarding-plan.

Owners are roles (the buyer's head of IT, our sales engineer), never invented names. A role the user did not mention is written as an open seat ("security reviewer: to be named by the buyer").

## The 30, 60 and 90 day account plan (win or widen one account)
1. Start from what the user knows: the account, the contacts and their roles, what the account uses today, the threats, the expansion idea. Research on the account or its people is done with b2b-research-market-and-account / account-research, not here.
2. Power map: one row per contact the user named, with their seat (champion, economic buyer, technical evaluator, user, blocker or reviewer), what they care about, and the next step with them. Missing seats are listed as gaps to fill.
3. Where the account can grow: each expansion idea tied to a pain the user named and the part of the offer that answers it.
4. Threats: incumbents or alternatives the user named, with the question that tests each (no battle card; that is b2b-sales-enablement / competitive-intelligence).
5. Dates: run `python3 scripts/close_plan.py account` for the 30, 60 and 90 day dates (example default offsets, moved back to a working day); the user's own offsets win.
6. Three phases: by day 30, map and listen (every seat met or named, the problem measured in the account's terms); by day 60, prove (a pilot, a reference, or a measured result agreed); by day 90, decide and widen (the decision or the expansion proposal, with the signer).
7. "This week": three actions, each with an owner and a date.
