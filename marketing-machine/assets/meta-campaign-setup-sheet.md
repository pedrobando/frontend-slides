# Meta Campaign Setup Sheet — [[AVATAR NAME]]

Fill this in, then build the three campaigns in Ads Manager exactly as written. See
`references/04-meta-funnel.md` for the why behind each field.

## 0. Account-level declarations

- **Special Ad Category:** `[[Housing | Employment]]`  *(Housing = buyer/seller ads · Employment = recruiting agents)*
- **Page / IG account:** `[[@handle]]`
- **ManyChat connected & tested before publish?** `[ ] yes`  *(must be yes — see Stage 6)*
- **Target annual earnings → ~10% ad budget:** `$[[annual]]` → `~$[[monthly ad budget]]/mo`

---

## Campaign 01 — COLD

| Field | Value |
|---|---|
| Campaign name | `01 Cold [[Avatar]] AIDA` |
| Objective | **Engagement** |
| Framework | **AIDA** (`references/02`) |
| Audience | Location only — `[[city/region, radius e.g. 25 mi]]` |
| Exclusions | `Warm-Engagers-90d` |
| Budget | `$[[20–50]]/day` |
| Creative | `[[link/desc of the AIDA reel]]` |
| Caption keyword (→ ManyChat) | `[[SYSTEMS / GUIDE / INFO]]` |
| Primary CTA | "Comment `[[keyword]]`" |

## Campaign 02 — WARM

| Field | Value |
|---|---|
| Campaign name | `02 Warm [[Avatar]] PAS+FAB` |
| Objective | **Leads** |
| Framework | **PAS** and/or **FAB** |
| Audience | `Warm-Engagers-90d` (IG+FB engagement + video viewers, 90d) |
| Exclusions | anyone who already converted / booked |
| Ad set A | `[[PAS variant]]` — `$50/day` |
| Ad set B | `[[FAB variant]]` — `$50/day` |
| Test rule | after 7 days, move **80% budget to lower-CPL (cost per Calendly book) ad set, kill the loser** |
| CTA | form / Calendly · keyword `[[COMPARE / LINK]]` |

## Campaign 03 — RETARGET

| Field | Value |
|---|---|
| Campaign name | `03 Retarget [[Avatar]] IDCA` |
| Objective | **Conversions** |
| Framework | **IDCA** |
| Audience | 50–75% video viewers of warm video + Calendly visitors who didn't book |
| Audience size target | **500–2,000 people max** |
| Exclusions | booked · in pipeline · unfollowed |
| Budget | `$[[20–50]]/day` |
| CTA | dual path: book in bio **or** comment `[[NOW]]` |

---

## Audiences to build first (before the ad sets)

- [ ] `Warm-Engagers-90d` = IG engagement + FB engagement + video viewers (90 days)
- [ ] Retarget custom audience = 50–75% video viewers + Calendly no-books
- [ ] Exclusion cascade verified: cold ⟶ excludes warm · warm ⟶ excludes converters · retarget ⟶ excludes booked/pipeline/unfollowed

## Pre-publish checklist

- [ ] Special Ad Category declared
- [ ] 3 separate campaigns (not 3 ad sets), named per convention
- [ ] Objectives: Engagement / Leads / Conversions
- [ ] Each creative uses the matching framework
- [ ] Cold caption keyword = ManyChat trigger (exact match)
- [ ] ManyChat wired + tested with a teammate
- [ ] Budgets set
