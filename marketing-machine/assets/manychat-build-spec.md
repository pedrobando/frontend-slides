# ManyChat Build Spec — [[AVATAR NAME]] / [[CAMPAIGN]]

Replicate this in ManyChat click-for-click. See `references/06-manychat-flow.md` for the rules.
**Universal path:** `Automation → + New → Start From Scratch → + New Trigger → Instagram → [trigger]`

> 🔴 Before you publish the ad: build + **test these with a teammate's account** (you can't trigger
> on your own comments). First message must have a button. Keyword must match the caption exactly.

---

## Automation 1 — Welcome Message  👋

- **Trigger:** New Followers
- **Delay:** `[[instant – 5 min]]`
- **Opening DM (must include a button):**
  > [[Greeting w/ {{first_name}} — e.g. "¡Hola {{first_name}}! Gracias por seguirme 🙌 ¿Qué te trae por aquí?"]]
- **Buttons → branch:**
  | Button | Leads to |
  |---|---|
  | `[[Comprando / Buying]]` | `[[response + next step]]` |
  | `[[Vendiendo / Selling]]` | `[[response + next step]]` |
  | `[[Solo mirando / Curious]]` | `[[response + nurture]]` |
- **Status:** `[ ] Active`

---

## Automation 2 — Comment-to-DM  💬  (wired to the COLD ad)

- **Trigger:** Comments on `[[post / all posts]]`
- **Keyword:** `[[SYSTEMS]]`  ← **must match the ad caption exactly**
- **Public reply variations (3+, ManyChat rotates them):**
  1. `[[e.g. "¡Te lo mando ahora mismo! 📩"]]`
  2. `[[variation 2]]`
  3. `[[variation 3]]`
- **First private DM — 1 block, must contain a button:**
  > [[Short intro + the offer. Button opens the link.]]
  >
  > Button: `[[e.g. "Descargar la guía"]]` → `[[offer/lead-magnet link]]`
- **After button tap (24h window open):**
  - Block 2: `[[deliver/confirm the lead magnet]]`
  - Block 3: `[[qualifying question — e.g. "¿Para cuándo te gustaría mudarte?"]]`
- **Status:** `[ ] Tested with teammate  [ ] Active BEFORE ad publish`

---

## Automation 3 — Story Reply  📱

- **Trigger:** User replies to your Story → scope: **All Stories**
- **Auto-response (with button to open 24h window):**
  > [[value-first reply — e.g. "¡Gracias por contestar! Te mando algo que te va a servir 👇"]]
- **Follow-up flow:** `[[chain blocks / route to offer or DM]]`
- **Status:** `[ ] Active`

---

## Match-up check (the loop must connect)

- [ ] Ad caption says "comment **[[keyword]]**" — and Automation 2 keyword is the same word
- [ ] First DM offer = the **exact** offer the ad hook promised (`assets/offer-template.html`)
- [ ] Every first message has a button (opens the 24-hour window)
- [ ] All three automations tested before the ad goes live
