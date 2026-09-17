# FAIRWORK Design System

Baseline style guide for the FAIRWORK research portal. Share with anyone building database visualization pages or new site sections so visuals stay aligned with the homepage.

## Typography (2 fonts)

| Role | Font | CSS variable | Usage |
|------|------|--------------|-------|
| Display | Cormorant Garamond | `--ff-d` | Headlines, quotes, large intro text |
| UI & body | Syne | `--ff-u` / `--ff-m` | Body copy, nav, labels, buttons, forms |

**Do not add additional font families.** Material Symbols Outlined is used for icons only.

### Type scale

| Token | Size | Use |
|-------|------|-----|
| `--text-base` | 1rem (16px) | Body paragraphs, dialogue text |
| `--text-sm` | 0.9375rem (15px) | Card descriptions, form inputs |
| `--text-xs` | 0.8125rem (13px) | Status labels, meta text |
| `--text-label` | 0.75rem (12px) | Eyebrows, section labels (uppercase) |

Display headlines use `clamp()` for responsive sizing. Minimum body size on public pages: **15px** for descriptions, **16px** for primary copy.

## Color palette

| Token | Hex | Use |
|-------|-----|-----|
| `--ink` | `#0C1623` | Primary dark background, text on light |
| `--ink2` | `#0D2231` | Secondary dark surfaces |
| `--cream` | `#F4EFE6` | Light section backgrounds |
| `--warm` | `#ECE7DD` | Alternate light (dialogue band, soon tiles) |
| `--white` | `#FDFAF5` | Cards, search bar |
| `--rust` / `--rust2` | `#BA4B2D` / `#CC5538` | Accent, links, CTAs |
| `--gold` / `--gold2` | `#1A80AE` / `#3DAACE` | Secondary accent, stats |
| `--fog` | `#6E8595` | Muted text on dark |
| `--teal` | `#1A80AE` | Methodology highlights |

**Contrast rule:** Never place `--fog` body text on `--ink` without sufficient size/weight. Light sections use `#444`–`#555` for body, not fog.

## Buttons

```html
<a class="btn-primary" href="#">Primary action</a>
<a class="btn-outline" href="#">Secondary action</a>
<button type="button" class="btn-outline" onclick="...">Secondary</button>
```

- **Primary:** rust background, cream text, uppercase Syne 700
- **Outline:** transparent, cream/ink border depending on section
- Min touch target: 44px height
- Padding: `.9rem 2.5rem` (primary)

## Cards & tiles

### Initiative tile (primary CTA)

```html
<article class="initiative-tile">
  <span class="initiative-tag">Tag</span>
  <h3 class="initiative-title">Title</h3>
  <p class="initiative-desc">Description</p>
  <div class="initiative-status status-active"><span class="initiative-status-dot"></span>Status</div>
  <span class="initiative-link">Action →</span>
</article>
```

- Padding: `2rem 1.75rem`
- Background: `--white` on cream sections
- Coming soon: add `initiative-tile--soon`, use `status-soon`

### Theme / audience cards

- 2px gap grid on shared background strip
- Hover: warm tint + top/side accent bar (`--rust`)

## Section patterns

```html
<div class="section-header">
  <span class="eyebrow-fog">Section Label</span>
  <div class="section-rule-dark"></div>
</div>
```

- **Dark sections:** `--ink` bg, `--eyebrow` (rust) + `--section-rule`
- **Light sections:** `--cream` bg, `--eyebrow-fog` + `--section-rule-dark`

## Spacing

- Section padding: `5rem 3rem` (desktop), `3rem 1.5rem` (mobile)
- Max content width: `1100px` for grids, `680px` for centered dialogue
- Grid gap: `1.25rem` (tiles), `2px` (flush card grids)

## Forms

- Inputs: white bg, `1px solid rgba(10,10,10,.12)`, focus `--rust` border
- Modal (Get Involved): cream panel, 440px max-width, name + email required

## Files

| File | Purpose |
|------|---------|
| `css/styles.css` | Global tokens, homepage, shared components |
| `css/about.css` | About page layout |
| `css/pages.css` | Shared subpage layout (About, Team) |
| `index.html` | Reference implementation |

## Phase 2 placeholders

Mark unfinished features explicitly: `(Ask FAIRWORK)`, search note, `Coming soon` on forecasting/experiment tiles, Learning Hub nav item removed until ready.
