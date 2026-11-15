# Stage 4 — The Meta Ads Funnel

> Read **"The Meta Ads Concept"** in `SKILL.md` first — this file is the build detail for it. The
> deliverable is a filled `assets/meta-campaign-setup-sheet.md`.

## Three separate campaigns (recap)

| # | Stage | Framework | Objective | Audience | Excludes |
|---|-------|-----------|-----------|----------|----------|
| 01 | **Cold** | AIDA | **Engagement** | Location only (e.g. 25-mi radius) | your warm engagers |
| 02 | **Warm** | PAS / FAB | **Leads** | `Warm-Engagers-90d` (IG+FB engagement + video viewers, 90d) | anyone who converted |
| 03 | **Retarget** | IDCA | **Conversions** | 50–75% video viewers + Calendly visitors who didn't book | booked · in pipeline · unfollowed |

Cold's engagement spend builds the warm audience **for free**. Retarget is the tightest audience you
have — aim for ~**500–2,000 people max**.

## Naming convention

`[Number] [Stage] [Avatar] [Framework]` — so you can read the dashboard in one glance:

- `01 Cold Pedro AIDA`
- `02 Warm Pedro PAS+FAB`
- `03 Retarget Pedro IDCA`

## Two declarations before you configure anything

1. **Special Ad Category** — you MUST declare it. Housing for buyer/seller ads; **Employment** for
   recruiting agents. Meta then locks age / gender / detailed targeting and tight zip radius. Don't
   fight it — *the creative does the targeting* (see `03-ad-copy.md`). You CAN still **exclude**
   audiences, which is what powers the cascade. Forget to declare it and Meta blocks you mid-launch
   and you rebuild.
2. **Objective per campaign** — Engagement (cold) → Leads (warm) → Conversions (retarget). Engagement
   on cold matters because the AIDA reel ends with "comment SYSTEMS" and ManyChat fires the DM —
   Engagement trains Meta to find people who comment.

## Audience build order (do this before the ad sets)

1. Build **`Warm-Engagers-90d`** = Instagram engagement + Facebook engagement + video viewers, last
   90 days. Save it. The warm campaign retargets this.
2. Build the **retarget custom audience** = 50–75% video viewers of the warm video + Calendly
   visitors who didn't book.
3. Wire the **exclusions**: cold excludes warm engagers; warm excludes converters; retarget excludes
   booked + pipeline + unfollowed.

## Budget

- **$20–$50/day** on cold and retarget — *"small enough to learn, big enough to give Meta data."*
- **Warm:** run two ad sets (e.g. PAS vs FAB), ~$100/day split 50/50 for 7 days. Then check which ad
  set has the lower CPL (cost per Calendly book), move **80% of budget to the winner, kill the
  loser.**
- Heuristic: plan to spend ~**10% of what you want to earn annually**.

## Build checklist

- [ ] Special Ad Category declared (Housing or Employment)
- [ ] 3 separate campaigns created and named per convention
- [ ] Objectives set: Engagement / Leads / Conversions
- [ ] `Warm-Engagers-90d` + retarget custom audiences built
- [ ] Exclusions cascade correctly (cold→warm→retarget)
- [ ] Each campaign's creative uses the right framework (AIDA / PAS·FAB / IDCA)
- [ ] Cold caption ends on the comment keyword
- [ ] **ManyChat wired and tested BEFORE publish** (Stage 6)
- [ ] Budgets set per the rules above

→ Fill `assets/meta-campaign-setup-sheet.md` and continue to **Stage 5 — Offer** (`05-offer-lead-magnet.md`).
