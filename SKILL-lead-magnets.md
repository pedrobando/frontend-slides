---
name: lead-magnets
description: Create PDF-ready, consumer-facing lead magnet presentations for reThought Real Estate agents. No animations, no presenter notes. 9:16 portrait format, full-color, designed for Google Drive public link sharing.
---

# Lead Magnets — Consumer-Facing Content

Create zero-dependency, PDF-ready HTML lead magnets for reThought Real Estate agents and campaigns.

## How This Differs from Presenter Slides

| Feature | Presenter Slides (SKILL.md) | Lead Magnets (this file) |
|---------|---------------------------|--------------------------|
| Audience | Trainer in a room | Consumer downloading a PDF |
| Animations | Required on every slide | **NONE — forbidden** |
| Presenter notes | Required, self-contained | **NONE — forbidden** |
| Format | Landscape, deck-stage.js | Portrait 9:16 (1080×1920), deck-stage.js |
| Navigation | Slide deck with keyboard nav | Deck nav (←/→) + Cmd+P for PDF download |
| Distribution | Live presentation | Google Drive public link as PDF |

## Core Principles

1. **PDF-First** — Every page must render perfectly when printed to PDF via browser (Cmd+P → Save as PDF). Full color, no cut-off elements, no scroll within pages.
2. **No Animations** — Zero CSS animations or transitions. Content is static.
3. **No Presenter Notes** — Content speaks for itself. The consumer reads it directly.
4. **Deck Navigation + PDF** — Uses `deck-stage.js` for keyboard nav (←/→) and thumbnail rail. `@media print` in deck-stage handles clean PDF export via Cmd+P. Slides use `class="slide"` wrapped in `<deck-stage width="1080" height="1920">`.
5. **Locked Design System** — All lead magnets use `tokens.css` from the Frances source. This is the canonical reThought design system for consumer content. Do not modify or create alternative token files.
6. **9:16 Portrait (1080×1920)** — Default format unless user explicitly requests otherwise.
7. **Agent-Personalized** — Each agent gets their own subfolder. Only photo, name, and byline change between agents. Content structure and design system are shared.

## Folder Structure

```
lead-magnets/
  {agent-name}/
    assets/
      {agent-name}.jpeg     — Agent headshot
      logo-icon-dark.png    — reThought logo variants
      logo-icon-white.png
      logo-wordmark-dark.png
      logo-wordmark-white.png
    tokens.css              — Locked design system (DO NOT MODIFY)
    {keyword}-{slug}.html   — One file per lead magnet
```

**Naming convention:** `{keyword}-{descriptive-slug}.html`
- Examples: `plan-profesionales-salud.html`, `orientame-primera-casa.html`, `inversion-sin-adivinar.html`

## Creating a New Lead Magnet

### 1. Use the page template

Every page uses `class="page"` with these variants:
- `.page` — White background
- `.page.dark` — Navy background (`--re-navy`)
- `.page.green` — Green background (`--re-green`)
- `.page.subtle` — Light gray background (`--re-gray-50`)

### 2. Required HTML structure

```html
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<title>{Lead Magnet Name} · {Agent} · reThought Real Estate</title>
<link rel="stylesheet" href="tokens.css" />
<style>
  @page { size: 1080px 1920px; margin: 0; }
  @media print {
    html, body { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    .page { break-after: page; break-inside: avoid; }
  }
  html, body { margin: 0; padding: 0; background: #faf9f5; }
  body { display: flex; flex-direction: column; align-items: center; gap: 0; }

  /* ... all component styles inline ... */
</style>
</head>
<body>
  <section class="page cover">...</section>
  <section class="page subtle">...</section>
  <!-- ... content pages ... -->
  <section class="page dark"><!-- closing quote --></section>
  <section class="cta-slide page"><!-- CTA --></section>
  <section class="page dark"><!-- final logo --></section>
</body>
</html>
```

### 3. Every lead magnet MUST have

1. **Personalized cover** — Agent photo, lead magnet title, subtitle, byline
2. **Content pages** — The actual guide content, using the component library below
3. **Closing quote** — Motivational quote attributed to the agent
4. **CTA page** — "Una llamada. 20 minutos. Sin pitch." with agent contact info
5. **Final logo page** — reThought branding closer

### 4. Page numbering

Use standalone numbering: `01 / {total}` through `{total} / {total}`. Each lead magnet is independent — no reference to the Master Playbook numbering.

## Component Library

All components are defined in the inline `<style>` block. Reference the existing lead magnets for exact CSS. Key components:

| Component | CSS Class | Use For |
|-----------|-----------|---------|
| Chrome header | `.chrome-top` | Eyebrow + page number on every content page |
| Chrome footer | `.chrome-bottom` | Brand lockup + section label on every content page |
| Title block | `.title-block` | Kicker + heading at top of content pages |
| Check list | `.check-list` | Yes/no item lists with colored marks |
| Numbered list | `.num-list` | Numbered items with big green numbers |
| Row list | `.row-list` | Label + value table rows |
| Card grid | `.card-grid` | 2-column card layout (`.full` for single column) |
| Stat grid | `.stat-grid` | 2×2 big-number stat cards |
| Timeline | `.timeline` | Step-by-step process with dates |
| Callout | `.callout` | Highlighted box with label + text |
| Big quote | `.big-quote` | Large display quote |
| VS split | `.vs-split` | Two-option comparison layout |
| Action block | `.action-block` | Checklist with timeframe header |
| CTA slide | `.cta-slide` | Photo + pitch + contact footer |

## Card Variants

- `.c` — Default (gray-50 background)
- `.c.green` — Green background, navy text
- `.c.navy` — Navy background, white text
- Custom: use inline `style="background: var(--re-blue); color: white;"`

## Adding a New Agent

1. Create `lead-magnets/{agent-name}/` folder
2. Copy `tokens.css` from an existing agent folder (identical file)
3. Add agent assets to `assets/` (headshot + logo variants)
4. Copy an existing lead magnet HTML as template
5. Replace: photo src, agent name in byline, cover-byline, closing-quote author, CTA contact info
6. Content stays the same — only personalization changes

## Quality Checklist

Before delivering any lead magnet:

- [ ] Opens in browser and all pages render at 1080×1920
- [ ] Cmd+P → Save as PDF produces clean output with full colors
- [ ] No animations or transitions in the CSS
- [ ] No JavaScript (no deck-stage.js, no interactivity)
- [ ] Every page has chrome-top and chrome-bottom
- [ ] Page numbers are sequential and correct for this standalone piece
- [ ] Cover is personalized to the specific lead magnet topic
- [ ] CTA has correct agent contact information
- [ ] All asset paths are relative (`assets/filename.ext`)
- [ ] `tokens.css` is linked, not inlined
