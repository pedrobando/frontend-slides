---
name: marketing-machine
description: >-
  Run the "Marketing Machine" — a complete real-estate lead-generation system that takes an
  agent from a client avatar, to video scripts (AIDA/PAS/FAB/SPIN/SCIPAB/IDCA), to ad copy, to a
  3-campaign Meta Ads funnel, to a lead-magnet offer, to a live ManyChat DM automation. Use when a
  real-estate agent (or marketer) wants help building any part of this system — developing an
  avatar, writing scripts or ad copy, planning Meta campaigns, building an offer/lead magnet, or
  wiring ManyChat. Outputs are bilingual English/Spanish.
license: Proprietary — internal Marketing Machine training material.
---

# Marketing Machine

A turnkey system that turns a real-estate agent's expertise into a predictable stream of qualified
conversations. It runs on six stages. Each stage feeds the next — the avatar tells you *what to
say*, the framework tells you *how to say it*, the ad puts it in front of people, the offer delivers
on the promise, and ManyChat captures the lead automatically.

**Core philosophy:** *"Systems > Effort. Discipline > Motivation. Consistency pays."* The agent's
real face, real voice, and real specificity build trust — not production value. Complexity equals
value: the goal of every touch is to become a **guide**, not just a door-opener.

> Outputs are **bilingual (English + Spanish)** by default — the training serves the PR/US-Latino
> real-estate market. At the start of a guided run, confirm the market and language; otherwise
> produce both EN and ES side by side.

---

## How to use this skill (router)

First, figure out what the user wants, then route:

**A) "Run the whole machine" / "help me build my marketing" / unsure where to start**
→ Run the **Guided Build** below: walk the six stages in order, one at a time. Don't dump all six
on the user. Finish a stage, show the artifact, get a thumbs-up, carry the avatar + niche forward,
then move to the next stage.

**B) "I just need X" (a script, ad copy, the campaign setup, an offer, the ManyChat flow)**
→ Jump straight to the matching stage. Read that stage's reference file, produce the artifact, done.
You don't need to run the earlier stages — but if you're missing the avatar, ask the 3 avatar
questions first (Stage 1), because every other stage depends on it.

**C) "Explain the Meta ads thing / how does this work"**
→ Teach from **The Meta Ads Concept** section below, then offer to build it.

### The six stages

| # | Stage | Reference file | Deliverable |
|---|-------|----------------|-------------|
| 1 | **Client Avatar** | `references/01-client-avatar.md` | Filled avatar profile + 5-Pillar Frame |
| 2 | **Video Scripts** | `references/02-script-frameworks.md` | Script(s) in the right framework |
| 3 | **Ad Copy** | `references/03-ad-copy.md` | Cold / warm / retarget ad copy |
| 4 | **Meta Funnel** | `references/04-meta-funnel.md` | Filled `assets/meta-campaign-setup-sheet.md` |
| 5 | **Offer / Lead Magnet** | `references/05-offer-lead-magnet.md` | Offer doc from `assets/offer-template.html` |
| 6 | **ManyChat Flow** | `references/06-manychat-flow.md` | Filled `assets/manychat-build-spec.md` |

**Always read the stage's reference file before producing that stage's artifact** — the frameworks,
exact scripts, naming conventions, and gotchas live there, not in this file.

---

## The Meta Ads Concept (read this first — everything hangs off it)

This is the mental model the whole system is built on. Internalize it before building anything.

### Three SEPARATE campaigns, not three ad sets

The single most common mistake is one campaign with three ad sets. **Don't.** You build **three
separate campaigns** — Cold, Warm, Retarget — because each one owns its own **objective, audience,
and exclusions**, and the exclusions need to *cascade*:

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ 01  COLD    │ ───► │ 02  WARM    │ ───► │ 03 RETARGET │
│ AIDA        │      │ PAS / FAB   │      │ IDCA        │
│ Engagement  │      │ Leads       │      │ Conversions │
└─────────────┘      └─────────────┘      └─────────────┘
   location only      engagers 90d         50–75% viewers +
   (cold)             (built free from      Calendly no-books
                       cold's spend)         (tightest audience)
```

- **Cold** runs to a location only and builds your warm audience *for free* out of everyone who
  engages.
- **Warm** retargets those engagers and excludes anyone who already converted.
- **Retarget** is the tightest, highest-converting audience you have (~500–2,000 people) and
  excludes everyone who already booked, is in your pipeline, or unfollowed.

If you cram this into one campaign with three ad sets: the same person sees all three ads
(exclusions don't cascade) and one shared budget pool can starve your warm. That's why it's three
campaigns.

### Each stage gets its own framework

Match the framework to where the audience is in the journey — *not where you want them to be*:

- **Cold → AIDA** (they don't know you; stop the scroll)
- **Warm → PAS or FAB** (they know the problem / are comparing options)
- **Retarget → IDCA** (they already know you; convince, don't re-introduce)

### Special Ad Category: the copy does the targeting

Real-estate ads must be declared **Housing** (recruiting agents = **Employment**) under Meta's
Special Ad Category. Meta then **locks demographic targeting** — no age, gender, detailed interests,
or tight zip radius. Don't fight it. **The creative does the targeting through specificity.**
*Generic fails. Specific filters.* "Milwaukee agents producing $1M–$3M" filters itself; "real estate
professionals" does not. (You *can* still exclude audiences — that's what powers the cascade.)

### The full loop

> Cold AIDA reel → caption says "comment SYSTEMS" → **ManyChat** fires a DM with the **offer** →
> the offer delivers on the hook's promise → lead enters the pipeline → warm + retarget campaigns
> close them.

Every piece exists to serve this loop. A great ad with no ManyChat wired, or an offer that doesn't
deliver the hook's promise, breaks the whole machine.

> **Budget rule of thumb:** $20–$50/day per campaign — *"small enough to learn, big enough to give
> Meta data."* Heuristic: plan to spend ~10% of what you want to earn annually.

---

## Guided Build — the six stages in order

Run these one at a time. After each, show the artifact and confirm before continuing.

1. **Avatar** — Read `references/01-client-avatar.md`. Ask the three "Feel It Before You Write It"
   questions. Produce a tight avatar profile and the 5-Pillar Frame. *This is the foundation —
   never skip it.* Garbage avatar = garbage everything.
2. **Scripts** — Read `references/02-script-frameworks.md`. Ask which audience temperature / video
   you're writing for, pick the matching framework, write the script (EN + ES).
3. **Ad Copy** — Read `references/03-ad-copy.md`. Turn the script's angle into ad copy that does its
   own targeting under Special Ad Category. Produce cold/warm/retarget variants as needed.
4. **Meta Funnel** — Read `references/04-meta-funnel.md`. Fill `assets/meta-campaign-setup-sheet.md`
   with the three campaigns: names, objectives, budgets, audiences, exclusions.
5. **Offer** — Read `references/05-offer-lead-magnet.md`. Build the lead magnet from
   `assets/offer-template.html` so it delivers *exactly* what the hook promised.
6. **ManyChat** — Read `references/06-manychat-flow.md`. Fill `assets/manychat-build-spec.md` with
   the trigger keyword (must match the ad caption), buttons, and message blocks.

---

## The Operating System (supporting discipline)

The ads are the engine; these are what keep it running. Surface them when relevant, don't force them.

- **Lofty 3-Step SOP (within 24h of a new lead):** ① rename the search, ② expand it if too narrow,
  ③ schedule a recurring market report.
- **5-Pillar Frame** for every outbound contact (in Stage 1 reference): who I am · why I'm calling ·
  what you're looking for · I can help you get it · the specific thing only I provide.
- **Callback architecture:** voicemail under 45 sec (5 pillars) + email within 5 minutes.
- **Hidden decision-maker capture:** 80%+ of buyers/sellers have a co-decision-maker — capture the
  spouse in the CRM (target 60% within 90 days).
- **Weekly scoreboard:** Steps 1-2-3 on every lead · 100 calls/week · hidden-DM captures · showings
  · dinners · testimonials.
- **Post-close exponential loop:** dinner → testimonial → multi-channel posting → direct mail to the
  geo farm.

---

## Guardrails

- **Never fabricate the avatar's pain.** Pull it from the user's real answers to the three
  questions. Specificity is the whole game.
- **Never promise what the offer won't deliver.** *"An ad that promises something and delivers
  nothing is worse than no ad at all — it builds distrust before the relationship starts."*
- **Respect Special Ad Category.** Don't write copy or targeting that assumes age/gender/zip
  targeting you can't use for Housing/Employment.
- **Keep the agent's real voice.** Don't sand scripts into generic marketing-speak. Banned words in
  hooks: *revolutionary, game-changing, disruptive.*
- **Wire ManyChat before the ad goes live**, and make the caption keyword match the trigger exactly.
