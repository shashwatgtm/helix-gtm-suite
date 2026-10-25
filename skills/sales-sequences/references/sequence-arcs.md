# Sales email sequences: what each email does

Rewritten for this skill from the method of the Helix revenue enablement connector (email_sequence_generator), read on 14 October 2026. Send days come from scripts/sequence_days.py (example defaults or the user's own); no email count or day is a benchmark. Event follow up and nurture sequences are b2b-events-pr-and-launches / event-follow-up-engine; the one follow up email after a meeting is b2b-sales-enablement / meeting-prep-debrief.

## Rules for every email
1. One reason to write, one ask. The ask fits the reader's seat (a short call for a manager, a yes or no question for a busy executive, a document for a technical evaluator).
2. Every claim once, with its source: the user's own proof as they gave it ("from your pilot with [User to add: customer]"), a page opened and cited in this session, or no claim. A claim the user did not source is written as their claim or left out.
3. The pain in the reader's words, one pain per email when the user gave several; never the same sentence twice across the sequence.
4. Subject lines short and plain (the script counts words and characters); no tricks ("Re:" on a first email), no false urgency.
5. The last email closes the loop politely and leaves the door open; no guilt.
6. Personalisation placeholders only where the user must add a real detail: "[User to add: ...]". Never a made up detail about the recipient.
7. Tone set by the user (professional by default; consultative, casual, direct); the founder writing to a CEO is short and peer to peer.

## The arcs (adapt to the user's facts; the count follows the user's days)
- cold_outreach: 1 the opening (the reason this reader, this pain, one question); 2 the value (what changes for teams like theirs, from the user's proof); 3 the proof (one result with its source, or a question if there is none); 4 the right person (ask if someone else owns this); 5 close the loop.
- warm_follow_up (after a referral or an inbound reply): 1 thanks and the reason; 2 value tied to what they said; 3 the ask for a time.
- post_demo: 1 same day recap of what they saw and the next step as the seller named it ("our next step is ..."); 2 answer an open question or objection the seller reported from the demo, in the reader's words (never one the reader did not raise; if none, "[User to add: the question to answer]"); 3 something the champion can forward inside (a short summary, not a deck); 4 a date the reader or the seller named, as they said it, and the decision (otherwise "[User to add: the date]").
- proposal_follow_up: 1 the proposal summary and the one decision; 2 the open question the seller reported (otherwise "[User to add: the question to answer]"); 3 an offer to walk the economic buyer through it; 4 close the loop with a date to revisit.
- re_engagement (a deal that went dark; the user sets the days): 1 a new reason to talk from the user's facts (a change on their side or ours); 2 a direct yes or no question about the decision; 3 close the loop.
- referral_request (after a won deal or a good result): 1 thanks and the result in the customer's words as the user gave it; 2 the specific ask (one or two named roles or company types); 3 a gentle reminder with an easy way to say no.

## Before you send (in every answer)
- The recipient's name and any personal detail: from the user's CRM, never invented.
- Claims checklist: each claim and its source.
- Pains given but not used in any email.
- The send days and dates from the script, with weekdays.
