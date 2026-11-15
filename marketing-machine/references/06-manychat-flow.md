# Stage 6 — ManyChat Automation

> *"Automate the DM."* Three automations cover every engagement gap on Instagram. Deliverable: a
> filled `assets/manychat-build-spec.md` the agent can replicate click-for-click in ManyChat.

## The non-negotiable rules (read before building)

1. **First message MUST have a button.** No button = no 24-hour window = dead automation. The user
   has to *tap* a button to open your **24-hour messaging window**; only then can you send
   follow-ups.
2. **First private reply = 1 block max.** After the button is tapped, the full conversation flow
   opens.
3. **The comment keyword MUST exactly match the ad caption.** Caption says "comment SYSTEMS" →
   trigger keyword is `SYSTEMS`.
4. **Wire and TEST ManyChat BEFORE the ad publishes.** If it's not live, your first commenters get
   nothing back. You can't trigger on your own comments — test with a teammate's account.

## Universal setup path (every automation starts here)

`Automation → + New Automation → Start From Scratch → + New Trigger → Instagram → [pick trigger]`

---

## Automation 1 — Welcome Message  👋  *(trigger: New Followers)*

Auto-DM every new follower with a greeting + opt-in button.

1. Trigger: **New Followers**.
2. Timing: short delay (instant–5 min) → opening DM.
3. Opening DM: greeting personalized with `{{first_name}}` **+ a button** (this opens the 24h
   window). Offer 2–3 button paths, e.g. **Buying · Selling · Just curious**.
4. Build a follow-up branch per button → toggle **Active**.

---

## Automation 2 — Comment-to-DM  💬  *(trigger: Keyword in Comments)* — the money automation

Highest-ROI: comments boost the algorithm **and** capture the lead in DMs. This is the one wired to
your cold ad.

1. Trigger: **Comments** on the post (or all posts).
2. **Keyword:** set it to match the caption exactly. Common keywords by stage:
   - Cold (AIDA): `SYSTEMS`, `GUIDE`, `INFO`, `LIST`, `HOMES`
   - Warm (FAB): `COMPARE`, `LINK`
   - Retarget (IDCA): `NOW`
3. **Public reply variations:** write 3+ so ManyChat rotates them and it never looks robotic.
4. **Private DM (1 block):** the first DM must contain a **button** that opens the offer/link. Keep
   it to one block.
5. After the tap: deliver the lead magnet + ask the qualifying question / push to Calendly.
6. **Test the keyword, then Activate** — before the ad goes live.

---

## Automation 3 — Story Reply  📱  *(trigger: User replies to your Story)*

Catch every story reply before the story disappears in 24h.

1. Trigger: **User replies to your Story** → scope: **All Stories** (recommended — no gaps).
2. Conditions + response flow: auto-respond with value, open the 24h window with a button, chain
   follow-ups.
3. Respond fast — story replies are time-sensitive.

---

## Build order with the user

1. Confirm the offer (Stage 5) and the ad caption keyword (Stage 3) — they must match.
2. Fill `assets/manychat-build-spec.md`: trigger, keyword, public-reply variations, the 1-block
   first DM with its button, and the follow-up blocks.
3. Remind the user to **build + test in ManyChat before publishing the ad**, with a teammate.

This closes the loop from `SKILL.md`: **Cold AIDA reel → "comment SYSTEMS" → ManyChat DM → offer →
pipeline.** All six stages are now wired together.
