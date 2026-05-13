# Presentation Hub + Presenter View Design

## Overview

A zero-dependency HTML hub to browse, launch, and present multiple reThought presentations with a two-window setup: audience view (conference screen) and presenter view (laptop).

## Architecture

Three pieces, all static HTML/CSS/JS:

1. **`index.html`** — Light-mode hub page (reThought design system). Reads `manifest.json`, fetches each presentation's `<meta>` tags, renders series-grouped cards.
2. **`presenter.html`** — Dark-mode control panel. Current slide + next slide + speaker notes + timer + slide counter. Syncs with audience window via `BroadcastChannel`.
3. **Existing presentation HTML files** — Unchanged except: add `<meta>` tags for hub discovery and `data-notes` attributes for speaker notes. Add ~15 lines of BroadcastChannel listener.

## File Structure

```
presentations-hub/
├── index.html
├── presenter.html
├── manifest.json
├── build-manifest.sh
└── presentations/
    ├── marketing-machine-session-3.html
    └── (future files)
```

## Hub Page (`index.html`)

- Paper (#fbfbfb) background, reThought light-mode design system
- reThought wordmark + "Presentation Hub" header
- Series sections with sprout-dash mono labels
- Cards: white bg, shadow, brand top border, title/date/slide count, Present/View/PDF buttons
- PDF button links to pre-generated PDF (disabled if not found)

## Presenter Window (`presenter.html`)

- Dark Ink (#1B252F) background
- Layout: top bar (title, timer, slide count) + left 60% (current slide iframe) + right 40% (next slide preview + notes) + bottom controls
- Reads `data-notes` from slide elements
- Notes render paragraphs, bold, and `---` as EN/ES language divider
- Timer starts on open, MM:SS format, reset button

## Sync via BroadcastChannel

- Channel: `"rethought-slides"`
- Messages: `{ type: "navigate", slide: N }`, `{ type: "sync-request" }`, `{ type: "sync-response", slide: N }`
- Both windows can send/receive — control from either
- Keyboard: arrows, space, PageUp/Down, Home, End

## Presentation Meta Tags

```html
<meta name="presentation-title" content="...">
<meta name="presentation-series" content="...">
<meta name="presentation-session" content="3">
<meta name="presentation-date" content="2026-05-12">
<meta name="presentation-slides" content="23">
<meta name="presentation-pdf" content="filename.pdf">
```

## Speaker Notes

Embedded as `data-notes` on each `.slide` section. `\n\n` for paragraph breaks, `---` for EN/ES divider.

## Manifest

`build-manifest.sh` generates `manifest.json` — array of filenames from `presentations/` folder.
