# Launch FAQ

## Should this repository be private?
Yes. For your use case, make this repository private now.

Publishing a ChatGPT Store app does **not** require this repository to be public. Store listing and runtime deployment are separate from your Git repository visibility.

## Can the assistant create and publish the ChatGPT Store app autonomously?
The assistant can prepare all artifacts, copy, flows, and technical specs in this repo.

Final account-level actions (Store submission, domain ownership setup, DNS, payment account settings, policy acceptance) must be completed by the account owner.

## Recommended execution split
1. Assistant: create and validate all launch artifacts in-repo.
2. Owner: perform account-bound publication and billing configuration.
3. Assistant: continue with post-launch iteration (copy, events, prompts, policies).


## I am a noob coder. Can I get one step at a time?
Yes. Follow `ops/OWNER_ONE_STEP_AT_A_TIME.md` and execute exactly one step before moving to the next.


## Do we need to publish policy pages before MVP approval?
No for this MVP sequence. Publish them right after ChatGPT app approval and before enabling paid handoff on `gtmhelix.com`.
