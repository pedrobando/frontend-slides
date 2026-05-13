# Marketing Machine Series Build — Sessions 1 & 2 + Presenter EN/ES Toggle

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build Marketing Machine Sessions 1 and 2 as HTML presentations with full bilingual presenter scripts, add EN/ES language toggle to presenter view, and update the hub manifest.

**Architecture:** Each session is a self-contained HTML file following the reThought design system (#1B252F dark, paper light, Poppins/Instrument Sans/Geist Mono). Slides use viewport-base.css patterns, BroadcastChannel sync, and data-notes with word-for-word EN + PR Spanish scripts. Presenter view gets a toggle button to show only EN or ES sections of notes.

**Tech Stack:** HTML/CSS/JS (zero dependencies), reThought design system, BroadcastChannel API

**Source Content:**
- Session 1: `6 Frameworks That Stop the Scroll 1.pdf` + screenshot images from conversation
- Session 2: `Build-Your-Offer-The-Missing-Middle.pdf` + `reThought_Training_BuildYourOffer_2026-04-13 1.pdf` + screenshot images
- Session 3: Already built at `presentations/marketing-machine-session-3.html` (reference for style/structure)

---

### Task 1: Add EN/ES Toggle to Presenter View

**Files:**
- Modify: `presenter.html` (CSS + JS + HTML)

**What to build:**
Add a toggle button in the presenter top bar that switches notes display between:
- "ALL" (default) — shows both EN and ES sections
- "EN" — hides everything after the `---` divider (ES section)
- "ES" — hides everything before the `---` divider (EN section)

**Step 1: Add toggle HTML to top bar**

In the `.top-bar__meta` div, before the timer, add:
```html
<div class="lang-toggle" id="langToggle">
  <button class="lang-btn active" data-lang="all">ALL</button>
  <button class="lang-btn" data-lang="en">EN</button>
  <button class="lang-btn" data-lang="es">ES</button>
</div>
```

**Step 2: Add toggle CSS**

```css
.lang-toggle {
    display: flex;
    gap: 2px;
    background: var(--ink-deep);
    border: 1px solid var(--border-d);
    border-radius: 6px;
    overflow: hidden;
}
.lang-btn {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 1px;
    padding: 4px 10px;
    background: transparent;
    color: var(--muted-2);
    border: none;
    cursor: pointer;
    transition: all 0.15s;
}
.lang-btn.active {
    background: var(--sprout);
    color: var(--ink);
    font-weight: 600;
}
.lang-btn:hover:not(.active) {
    color: var(--paper);
}
```

**Step 3: Update renderNotes() to support language filtering**

Modify the `renderNotes` function to accept a language parameter. Store current language in state. When "EN" is selected, only render content before `---`. When "ES", only after. When "ALL", render everything (current behavior).

```javascript
let currentLang = 'all'; // state

// Toggle handler
document.getElementById('langToggle').addEventListener('click', function(e) {
    if (!e.target.classList.contains('lang-btn')) return;
    currentLang = e.target.dataset.lang;
    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    renderNotes(slideNotes[currentSlide]);
});

// Updated renderNotes
function renderNotes(rawNotes) {
    if (!rawNotes || rawNotes.trim() === '') {
        elNotes.innerHTML = '<span class="notes-empty">No notes for this slide.</span>';
        return;
    }
    const sections = rawNotes.split('---');
    let html = '';

    if (sections.length > 1) {
        // Has EN/ES sections
        if (currentLang === 'all' || currentLang === 'en') {
            if (currentLang === 'all') html += '<span class="lang-label">EN</span>';
            html += renderParagraphs(sections[0]);
        }
        if (currentLang === 'all') html += '<hr>';
        if (currentLang === 'all' || currentLang === 'es') {
            if (currentLang === 'all') html += '<span class="lang-label lang-label--below">ES</span>';
            html += renderParagraphs(sections.slice(1).join('---'));
        }
    } else {
        html += renderParagraphs(sections[0]);
    }

    elNotes.innerHTML = html;
    elNotes.scrollTop = 0;
}

function renderParagraphs(text) {
    return text.split(/\n\n+/).map(p => {
        const trimmed = p.trim();
        if (!trimmed) return '';
        return '<p>' + trimmed.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>') + '</p>';
    }).join('');
}
```

**Step 4: Test**
- Open presenter view with Session 3
- Verify ALL shows both languages
- Click EN — only English visible
- Click ES — only Spanish visible
- Navigate slides — toggle persists

**Step 5: Commit**
```bash
git add presenter.html
git commit -m "feat: add EN/ES language toggle to presenter view"
```

---

### Task 2: Build Session 1 — 6 Frameworks That Stop the Scroll

**Files:**
- Create: `presentations/marketing-machine-session-1.html`

**Content structure (from PDF + images):**

**Mandatory opening:**
1. Cover — "6 Frameworks That Stop the Scroll" / Avatar → Hook → Story → Offer
2. Year Statement — "2026 Is THE Year of SYSTEMS..."
3. Mission & Vision (English)
4. Misión y Visión (Spanish)

**Session content:**
5. Session Arc — Marketing Machine 4-session overview (Session 1 highlighted)
6. Feel It Before You Write It — 3 avatar empathy questions (What at 11pm? / What didn't work? / Afraid to admit?)
7. AIDA Framework — Attention · Interest · Desire · Action + Pedro's avatar example
8. PAS Framework — Problem · Agitate · Solution + Pedro's example
9. FAB Framework — Feature · Advantage · Benefit + Pedro's example
10. SPIN Framework — Situation · Problem · Implication · Need + Pedro's example
11. SCIPAB Framework — The Complete Framework (6 steps) + Pedro's example
12. IDCA Framework — Interest · Desire · Conviction · Action + Pedro's example
13. Quick Reference Table — All 6 frameworks: Best For, Tone, Funnel Stage
14. Live Exercise — Pick your framework, write your hook
15. Before You Leave — Say it out loud (4 commitments)
16. Closing Quote

**Key design elements from the original PDFs:**
- Mix of dark and light slides
- Framework slides: framework name + description on left, Pedro's avatar example in dark card on right
- Cards with colored top borders (sprout/brand/clay) per framework element
- Animated stagger reveals
- Stats/comparison tables
- SVG diagrams for each framework (AIDA circles, PAS arrows, FAB venn, SPIN pinwheel, SCIPAB steps, IDCA diamonds)

**Presenter scripts:** Full word-for-word scripts in EN + PR Spanish for every slide. Scripts explain the framework, give context, walk through Pedro's example, and tell agents exactly what to do.

**Meta tags:**
```html
<meta name="presentation-title" content="6 Frameworks That Stop the Scroll">
<meta name="presentation-series" content="Marketing Machine">
<meta name="presentation-session" content="1">
<meta name="presentation-date" content="2026-03-17">
<meta name="presentation-slides" content="16">
```

**Step 1:** Create the full HTML file following the Session 3 pattern:
- Same CSS base (reThought tokens, viewport fitting, animations, IG-style components where applicable)
- BroadcastChannel sync
- data-notes with full EN + PR Spanish scripts on every slide
- Conference-room readable text sizes
- Mix of dark (#1B252F) and light (#fbfbfb) slides
- Animated HTML components: SVG framework diagrams, staggered card reveals, animated comparison table

**Step 2:** Test by opening in browser
```bash
open presentations/marketing-machine-session-1.html
```

**Step 3:** Commit
```bash
git add presentations/marketing-machine-session-1.html
git commit -m "feat: add Marketing Machine Session 1 — 6 Frameworks That Stop the Scroll"
```

---

### Task 3: Build Session 2 — Build Your Offer: The Missing Middle

**Files:**
- Create: `presentations/marketing-machine-session-2.html`

**Content structure (from PDF + images):**

**Mandatory opening:**
1. Cover — "Build Your Offer: The Missing Middle"
2. Year Statement
3. Mission & Vision (English)
4. Misión y Visión (Spanish)

**Session content:**
5. Session Arc — Marketing Machine overview (Session 2 highlighted)
6. The Honest Truth — What You Have vs What You're Missing (split card: green checks / red X's)
7. 6-Step Duplicable Ad Workflow — Steps 1-6 visual pipeline (Steps 1,3 done, Step 2 = TODAY)
8. What Is a Lead Magnet? — Definition + THE RULE + 4 options (Guide / List / Checklist / Report)
9. Pedro's Case Study — Lead Magnet (Avatar + Hook + Lead Magnet setup + 5-page contents)
10. Live Exercise — Build Your Lead Magnet Decision (4 questions, 10 minutes)
11. The Bridge Sequence — 3 messages overview (MSG 1: Instant / MSG 2: 24hrs / MSG 3: 48-72hrs)
12. Bridge Message 1 — Instant Delivery (Email + Text, EN + ES)
13. Bridge Message 2 — Value Reinforcement (Email, EN + ES)
14. Bridge Message 3 — Qualifying Question + Lofty Handoff (Text + response routing table)
15. The Lofty Handoff — Right Tag → Right Plan → Right Nurture (routing tables for recruiting + buyer/seller)
16. Where Are You Right Now? — Full workflow checklist
17. Before You Leave — Say It Out Loud (4 commitments)
18. Closing Quote

**Key design elements:**
- "Honest Truth" slide: split layout with green (you have) and red (you're missing) sections
- Lead Magnet options as 4 colored cards (green/brand/yellow/grey)
- Bridge sequence as 3-step timeline with colored cards (green/brand/yellow)
- Bridge message slides: dark card with email template on left, text message on right
- Lofty handoff: routing table with color-coded response cards
- Checklist: two-column layout with check boxes

**Presenter scripts:** Full word-for-word EN + PR Spanish for every slide.

**Meta tags:**
```html
<meta name="presentation-title" content="Build Your Offer: The Missing Middle">
<meta name="presentation-series" content="Marketing Machine">
<meta name="presentation-session" content="2">
<meta name="presentation-date" content="2026-04-13">
<meta name="presentation-slides" content="18">
```

**Step 1:** Create the full HTML file.

**Step 2:** Test
```bash
open presentations/marketing-machine-session-2.html
```

**Step 3:** Commit
```bash
git add presentations/marketing-machine-session-2.html
git commit -m "feat: add Marketing Machine Session 2 — Build Your Offer: The Missing Middle"
```

---

### Task 4: Update Manifest and Final Push

**Files:**
- Run: `build-manifest.sh`
- Verify: `manifest.json`

**Step 1:** Rebuild manifest
```bash
bash build-manifest.sh
```
Expected: "Manifest updated: 3 presentation(s) found"

**Step 2:** Verify manifest
```bash
cat manifest.json
```
Expected: `["marketing-machine-session-1.html", "marketing-machine-session-2.html", "marketing-machine-session-3.html"]`

**Step 3:** Test hub
```bash
open http://localhost:8847
```
Expected: Marketing Machine series shows 3 cards (Sessions 1, 2, 3) with progress dots 3/4

**Step 4:** Test presenter view for each new session

**Step 5:** Final commit and push
```bash
git add manifest.json
git commit -m "chore: update manifest for sessions 1-3"
git push
```
