# Plugin-Specific Rules — optise-helix-aeo-toolkit

**Scope:** This file applies ONLY to the six skills in the `optise-helix-aeo-toolkit` plugin (optise-helix-prompt-pack-builder, optise-helix-fitq-audit, optise-helix-race-audit, optise-helix-bluf-writer, optise-helix-eu-trust-centre, optise-helix-aeo-tracker). It is read in addition to the shared `operating-principles.md` file in this same `references/` folder, NOT instead of it.

**Read order:** Skills MUST read `operating-principles.md` (shared core) FIRST, then this file. The shared core's rules (Rule 0 to Rule 10 and the mandatory disclaimer) apply to every skill in this plugin.

---

## Plugin Rule 1: No harmful output about named companies

**The rule.** Never produce content that makes unverified negative, comparative, or compliance claims about a named real company, and stop before building competitor-targeted content when the user's company and the named competitor are related.

**Why this matters.** These skills write public web copy (BLUFs, Trust Centre pages, comparison pages) that names real companies. An invented weakness, price, certification, or compliance status about a real company can mislead buyers, expose the user to legal risk, and damage a third party. Content aimed at a company the user owns or recently acquired is also self-defeating.

**What this means in practice.** Before writing about any named company, run the competitor verification in operating-principles Rule 9, step 2, including the ownership searches listed in each skill's Section 0. Every claim about a named company is tagged under Rule 8 and must be `[VERIFIED · source]` to appear as a fact; otherwise it becomes a `[User to confirm: ...]` placeholder or is left out. Worked examples inside these skills that use real company names are illustrations of structure only; never reuse their figures.

**Never do this.**
- Invent prices, certifications, data residency, subprocessor counts, or compliance statements for any company, including the user's own.
- Present a named competitor's weakness without a Tier 1 to 3 source.
- Build comparison or "alternative to" content targeting a company that the ownership searches show is related to the user.
- Name third-party vendors, resellers, or individuals as biased or unreliable unless a Tier 1 to 3 source supports it.

**Fail-closed behavior.** If an ownership search returns a positive hit, stop and ask the user one HARD STOP question before writing anything. If a claim about a named company cannot be verified, omit it or replace it with a placeholder, and list it under "Verification gaps" in the Verification Log.

**When to add plugin-specific rules to this file:**

Add a new `## Plugin Rule N` section here when:

1. A failure mode emerges that is specific to the AEO methodology (FITq scoring, RACE framework, BLUF copy generation, EU trust-centre compliance, or AEO tracker measurement) and is not adequately covered by the universal shared core
2. A skill in this plugin develops its own domain rule that should apply across multiple skills in the toolkit (e.g., a methodology-wide constraint)
3. The Optise-Helix v2 release introduces new operational requirements that go beyond the shared core

**When to add rules to the SHARED CORE instead of this file:**

Add to `operating-principles.md` (and propagate to all three plugins) when:

1. The rule applies to ANY plugin's skills, not just the AEO toolkit's
2. The rule is a universal rigor / verification / fact-check / output-quality requirement
3. The rule reflects a lesson learned that should be taught to every Claude plugin developer

**When NOT to add rules at all:**

Do NOT add rules here for:

1. Personal preferences (those belong in your global `~/.claude/CLAUDE.md`)
2. Project-specific context (those belong in the project's local `CLAUDE.md`)
3. Cargo-culted rules from other projects that don't apply to this plugin's actual content

---

## Rule format reference

When adding a new rule, follow the long-format pattern used by Plugin Rule 1 above:

```
## Plugin Rule N — [Short title]

**The rule.** [One-sentence imperative statement.]

**Why this matters.** [2-4 sentences explaining the failure mode this prevents.]

**What this means in practice.** [3-5 sentences describing the operational behavior.]

**Never do this.**
- [Specific anti-pattern 1]
- [Specific anti-pattern 2]
- [...]

**Fail-closed behavior.** [What the skill does when it cannot satisfy the rule.]
```

---

**File version:** 1.1 (September 2026): adds Plugin Rule 1
**Authorship:** optise-helix-aeo-toolkit plugin
**Status:** 1 plugin-specific rule defined
**Read order:** AFTER `operating-principles.md` (shared core), BEFORE skill-specific SKILL.md body
