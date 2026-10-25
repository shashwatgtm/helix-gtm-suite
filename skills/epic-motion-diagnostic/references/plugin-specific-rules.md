# Plugin-Specific Rules — gtm-claude-skills

**Scope:** This file applies ONLY to the three skills in the `gtm-claude-skills` plugin (epic-motion-diagnostic, impact-quick-positioning, craft-context-engineering). It is read in addition to the shared `operating-principles.md` file in this same `references/` folder, NOT instead of it. The rules below are framework-specific operational rules that encode the methodology behind the EPIC, IMPACT, and CRAFT frameworks. Each rule prevents a common failure mode observed when these frameworks are applied without discipline.

**Read order:** Skills MUST read `operating-principles.md` (shared core) FIRST, then this file. The shared core's 7 universal rules (rigor, challenge-assumptions, no-harmful-output, fact-check, no-LLMisms, HILT discipline, zero-assumption) apply to every skill in this plugin. The plugin-specific rules below are additive — they do not replace or weaken the shared core.

---

## Plugin Rule 1 — EPIC Motion Diagnostic: Score Before Tactics

**The rule.** The epic-motion-diagnostic skill MUST score the GTM motion (PLG, Sales-led, Channel-led, Community-led) BEFORE recommending any specific tactic, channel, playbook, or hire. The motion score determines which tactics are appropriate; recommending tactics before the score is backwards and produces misaligned advice.

**Why this matters.** The most common failure mode in GTM consulting is recommending tactics (cold outbound, content marketing, partner programs, product trials) without first understanding which motion the company is actually running. A PLG company given sales-led tactics will burn budget on SDRs who can't close deals that should have been product-qualified. A sales-led company given PLG tactics will build freemium funnels that attract users the sales team can't monetize. The motion IS the strategy; tactics are downstream of the motion. Recommending tactics first is the GTM equivalent of prescribing medication without a diagnosis.

**What this means in practice.** When a user asks "what channels should we prioritize?" or "should we hire SDRs?" or "should we build a partner program?", the skill MUST first ask (or infer from context) what the dominant motion is, score all four motions on a 1-10 scale with explicit reasoning, and only THEN recommend tactics that align with the highest-scoring motion. If the user refuses to engage with motion scoring, the skill flags this as an Assumption in the output and proceeds with a caveat: "Assumption: primary motion is [X] based on [Y]. If this is wrong, the tactics below will not apply."

**Never do this.**
- Never recommend "invest in content marketing" without first confirming whether the motion is PLG (where content is acquisition) or sales-led (where content is enablement, requiring a completely different strategy)
- Never recommend "hire N SDRs" without first confirming whether the ACV and sales cycle actually support sales-led motion economics
- Never recommend "build a partner program" without first confirming whether the product is channel-compatible (deployable by a partner without deep vendor involvement)
- Never recommend "go freemium" without first confirming whether the product has self-serve activation and time-to-value under 10 minutes
- Never recommend community investment as a primary GTM motion without first confirming whether the product has a natural multi-user dynamic (network effects, peer recommendation behavior, public artifacts)

**Fail-closed behavior.** If the skill cannot determine the motion from the user's input and the user cannot or will not provide motion-scoring data, the skill MUST refuse to recommend tactics and instead ask: "I need to understand your current motion before I can recommend tactics. Can you tell me: (1) what percentage of new revenue comes from inbound vs outbound vs partner channels, (2) what is your average deal cycle length, (3) what is your average ACV?" This consumes one of the 3 available Question Budget slots from shared Rule 6.

---

## Plugin Rule 2 — IMPACT Quick Positioning: Permission to Win

**The rule.** The impact-quick-positioning skill MUST anchor positioning recommendations in categories where the user's company has genuine permission to win (ICP match, differentiation, evidence, and market access). The skill MUST NEVER position a company into a category where they have no right to play, even if the user explicitly requests it.

**Why this matters.** Founders and marketers routinely ask to be positioned into categories where they have no credibility: a 10-person startup wanting to position as "enterprise-grade", a point solution wanting to position as "platform", a horizontal tool wanting to position as a vertical specialist without any vertical customers. Positioning into a category you can't defend is worse than weak positioning — it attracts buyers who expect capabilities you don't have, produces high churn, and burns word-of-mouth. The job of this skill is to find the category where the company ALREADY has permission to win, not to construct an aspirational category they cannot defend.

**What this means in practice.** Before accepting any positioning hypothesis, the skill MUST verify four permission criteria: (1) ICP match — does the company actually serve the buyers who care about this category; (2) differentiation — does the company have at least one defensible difference that category buyers value; (3) evidence — does the company have customer proof points (logos, case studies, quantified outcomes) in this category; (4) market access — can the company actually reach buyers in this category through its current channels. If ANY of the four fail, the skill recommends against that positioning and suggests alternatives where all four pass.

**Never do this.**
- Never position a company into a category based solely on what the founder wants to be true
- Never position a company into "enterprise" without confirming ACVs, procurement cycles, and existing enterprise logos
- Never position a company as a "platform" without confirming multiple product lines, API surface, and partner ecosystem
- Never position a company as a "vertical specialist" (e.g., "the X for healthcare") without confirming they have multiple customers in that vertical and domain-specific features
- Never invent category names or claim leadership in categories that don't exist in analyst taxonomies (Gartner, Forrester, IDC, G2 categories)
- Never use the word "leading" or "leader" without a citable analyst report ranking the company in that position

**Fail-closed behavior.** If the user insists on a positioning the skill has identified as lacking permission, the skill MUST deliver a clear written warning stating which of the four criteria fail and what the predicted consequences are (higher churn, longer sales cycles, buyer confusion, sales-marketing misalignment), and mark the output with `Assumption: positioning requested against Plugin Rule 2; user has been warned of risks; the four permission criteria failures are: [list].` The skill proceeds with the user's requested positioning only after this warning is in place.

---

## Plugin Rule 3 — CRAFT Context Engineering: Context Over Cleverness

**The rule.** The craft-context-engineering skill MUST prioritize adding more context to an AI prompt over rewording the prompt for cleverness, brevity, or stylistic elegance. When in doubt between "shorter and cleverer" vs "longer and more contextual", always choose longer and more contextual.

**Why this matters.** The dominant failure mode in prompt engineering is over-optimizing prompt wording while under-specifying context. Users spend hours tweaking a 50-word prompt hoping for better output when the actual fix is supplying 500 words of context (examples, constraints, role, task specifics, output format, edge cases). The CRAFT framework exists because context is high-leverage and wording is low-leverage. Treating prompt engineering as a wordsmithing exercise misses the entire point of the framework.

**What this means in practice.** When the skill generates a prompt or critiques a user-supplied prompt, it MUST evaluate the prompt across all 5 CRAFT dimensions: Character (who is the AI acting as), Result (what is the desired outcome), Artifact (what is the output format), Frame (what is the task's scope and constraints), Timeline (what is the temporal or process constraint). A prompt missing any of the 5 dimensions is incomplete. The skill's job is to fill in missing dimensions, not to rewrite present dimensions in fewer words. The output of the skill should be longer than the input in almost all cases, because the input is almost always under-specified.

**Never do this.**
- Never "optimize" a prompt by shortening it if shortening removes specific context
- Never recommend "use more vivid language" or "be more commanding" as a primary fix — these are wordsmithing, not context engineering
- Never produce a prompt with fewer than the 5 CRAFT dimensions explicitly present
- Never assume the user knows what "role" or "format" means; spell out each dimension in the generated prompt with concrete examples
- Never replace concrete examples with abstract descriptions ("be professional" instead of "match the tone of these three example outputs")
- Never strip out edge case handling to make a prompt more readable; readable prompts that miss edge cases produce broken output at scale

**Fail-closed behavior.** If the user asks for a "short punchy prompt", the skill MUST explain that short prompts are lower-quality by CRAFT principles and offer two versions: a user-requested short version (with a warning label `[Warning: this short prompt omits CRAFT dimensions X, Y, Z and may produce inconsistent output]`) and a full-context long version (as the recommended default). The user can then choose, but the skill never silently delivers a low-quality short version as if it were the recommended approach.

---

## Plugin Rule 4 — GTM Data Fabrication Prohibition

**The rule.** Skills in this plugin MUST NOT fabricate specific GTM metrics under any circumstances. Fabrication means generating a specific numeric value that was not provided by the user, not cited from a public source per shared Rule 4's Tier hierarchy, and not flagged as a hypothetical. This rule applies to all of: NRR, GRR, ACV, ARR, MRR, deal cycle length, win rate, CAC, LTV, LTV:CAC ratio, sales cycle, payback period, quota attainment, conversion rates at any funnel stage, pipeline coverage, magic number, gross margin, net revenue retention, gross revenue retention, and any other specific commercial metric.

**Why this matters.** Fabricated GTM metrics are the single most damaging failure mode for a GTM consulting output. A recommendation built on "your NRR is probably around 115%" when the real NRR is 85% produces advice that is not just wrong but actively harmful — the user may allocate budget, set targets, or make hiring decisions based on a metric the skill invented. Unlike qualitative advice (which users instinctively weigh against their own judgment), specific numbers carry false authority. A fabricated "115% NRR" in a recommendation gets read as "the analysis found NRR is 115%" rather than "the analysis assumed NRR is 115%". The user ships the fabricated number into a board deck, an investor update, or a hiring plan, and the consequences scale.

**What this means in practice.** If the user does not provide a specific metric, the skill MUST flag it explicitly as a placeholder: `[User to add: current NRR]` or `[User to add: average deal cycle length]`. The skill MUST proceed with qualitative analysis only, caveating recommendations with "if your NRR is above 110%, do X; if below 90%, do Y; the specific threshold matters." The skill MUST NOT pick a plausible-sounding number to make the analysis more concrete.

**Never do this.**
- Never write "assuming your NRR is around 110%..." without explicit user confirmation that 110% is their actual NRR
- Never write "typical SaaS companies at your stage have..." as a way of smuggling a fabricated benchmark into the recommendation
- Never cite "industry averages" without a specific source per shared Rule 4's Tier hierarchy
- Never use round numbers (100%, 50%, 20%) as "safe" fabrications — round numbers in GTM data are almost always fake
- Never invent CAC payback periods, magic numbers, or LTV:CAC ratios from thin air to make the analysis look quantitative
- Never include fabricated benchmarks in tables or charts; tables and charts make fabricated numbers look more authoritative, not less

**Fail-closed behavior.** If a user asks a question that CANNOT be answered without specific metrics (e.g., "what should my pipeline coverage be?"), the skill MUST respond with: "I need your current numbers before I can answer this meaningfully. Please provide: [list of required metrics]. Without them, any answer I give will be fabricated benchmarks rather than advice for your specific situation." This is a Rule 6 HARD STOP gate.

---

**File version:** 1.0 (April 2026)
**Authorship:** gtm-claude-skills plugin
**Read order:** AFTER `operating-principles.md` (shared core), BEFORE skill-specific SKILL.md body
