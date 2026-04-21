---
name: pliant-brand-guidelines
description: Applies Pliant's official brand colors and typography to any sort of artifact that may benefit from having Pliant's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply. Make sure to use this skill whenever the user mentions Pliant branding, corporate identity, brand colors, visual identity, or wants outputs styled with the Pliant brand, even if they don't explicitly say "brand guidelines."
license: Complete terms in LICENSE.txt
---

# Pliant Brand Styling

## Overview

This skill contains Pliant's official brand identity — colors, typography, and usage rules. Apply these whenever creating branded outputs (presentations, documents, HTML artifacts, dashboards, etc.).

Source: Pliant LEAP Brand Platform (Frontify)

## Colors

### Primary Colors

These three colors form the foundation of Pliant's visual identity.

| Name | HEX | RGB | Usage |
|------|-----|-----|-------|
| Pliant Yellow | `#e6ff52` | 230, 255, 82 | Lead brand color. Use sparingly — logos, key highlights, focal moments. **Never use for text.** |
| Pliant Black | `#201c1c` | 32, 28, 28 | Primary text color, logos. Background only on swag (tote bags, t-shirts). |
| White | `#ffffff` | 255, 255, 255 | Primary background. Generous white space is an important part of the brand. |

### Secondary Colors

Complementary accents that enhance the visual identity in brand communications and product design.

| Name | HEX | RGB |
|------|-----|-----|
| Pliant Orange | `#ffa070` | 255, 160, 112 |
| Pliant Red | `#ff727e` | 255, 114, 126 |
| Pliant Blue | `#a5c3c3` | 165, 195, 195 |
| Pliant Fawn | `#e4d7cf` | 228, 215, 207 |
| Pliant Gray | `#404c52` | 64, 76, 82 |

### Tints

Support colors for when more variation is needed (e.g., virtual card designs).

| Light | HEX | Dark | HEX |
|-------|-----|------|-----|
| Light Yellow | `#eeff8b` | Dark Yellow | `#717f21` |
| Light Orange | `#ffb38d` | Dark Orange | `#8c583e` |
| Light Red | `#ff8e98` | Dark Red | `#8c3f45` |
| Light Blue | `#b7cfcf` | Dark Blue | `#5b6b6b` |
| Light Fawn | `#e9dfd9` | Dark Fawn | `#7d7672` |
| Light Charcoal | `#6b787e` | Dark Charcoal | `#19242a` |

### Neutrals

Balance brand communications. Good support for brand colors as blocks. Can also serve as backgrounds.

| Name | HEX | RGB |
|------|-----|-----|
| Pliant Gray 1 | `#f5f5f0` | 245, 245, 240 |
| Pliant Gray 2 | `#ddddd5` | 221, 221, 213 |
| Pliant Gray 3 | `#9b9b91` | 155, 155, 145 |

### Color Usage Rules

The reason these rules exist is to keep Pliant's brand feeling clean, bright, and distinctive — yellow is the attention-grabber, and it works best when it's not overused.

- **Prioritize white backgrounds** with primary color accents. This is the signature Pliant look.
- **Maximum two bright colors** in one composition, always balanced with a neutral or white.
- Pliant Yellow should be the most associated with logos and key moments — not general backgrounds or text.
- Don't combine more than two accent colors together.
- Don't create compositions using only neutral shades — include at least one brand color.
- Don't use colors outside the official palette.
- **For CaaS / technical assets**: Use Dark Charcoal (`#19242a`) as the main background to convey technology and professionalism. All other brand colors remain usable and should be complemented with the Charcoal tone.

## Typography

### Typefaces

| Role | Font | Weights | CSS |
|------|------|---------|-----|
| Headlines | **Pangea** | 300 (Light/Regular), 700 (Bold/Semi-bold) | `font-family: "Pangea", sans-serif;` |
| Body copy | **Maison Neue** | 300 (Book), 500 (Medium), 700 (Bold) | `font-family: "Maison Neue", sans-serif;` |

**Fallbacks**: If Pangea is unavailable, use Arial. If Maison Neue is unavailable, use Helvetica.

### Typography Rules

These rules ensure readability and visual consistency across all Pliant materials.

- **Always sentence case** — never all-caps for headlines or body.
- **Alignment**: Left-aligned or centered. Never right-aligned.
- **No letter-spacing (tracking)** on headline typography.
- **Leading**: Minimum 95% of the X-height.
- **Limit sizes**: Use ideally no more than three font sizes in one layout.
- Pangea is used in Regular weight by default; Semi-bold (700) can highlight keywords within headlines.

### Text Color Rules

These exist because Pliant Yellow is eye-catching but low-contrast — it shouldn't be used as a text color.

| Background | Text Color |
|------------|------------|
| White | Pliant Black (`#201c1c`) |
| Black | White (`#ffffff`) |
| Bright colors (Yellow, Orange, Red, Blue, Fawn) | Pliant Black (`#201c1c`) |
| Dark colors (Dark Charcoal, Pliant Gray) | White (`#ffffff`) |
| Light Grays | Pliant Black (`#201c1c`) |

**Never** use white text on bright colors. **Never** use black text on dark colors. **Never** use Pliant Yellow as a text color.

## Applying the Brand

When creating branded outputs, apply the guidelines as follows:

### HTML / Web Artifacts
- Set body background to White, text to Pliant Black
- Use Pangea for headings, Maison Neue for body text (with Arial/Helvetica fallbacks)
- Use Pliant Yellow sparingly for highlights, CTAs, or accent elements — not for large backgrounds
- Use secondary colors for cards, tags, and visual variety
- For dark/tech sections, use Dark Charcoal background with white text

### Presentations (PPTX)
- Apply via python-pptx's RGBColor class
- Headings (24pt+): Pangea font
- Body text: Maison Neue font
- Title slides can use Pliant Yellow as an accent stripe or highlight
- Content slides: white background, black text, accent colors for shapes

### Documents (DOCX)
- Headings: Pangea, Pliant Black
- Body: Maison Neue, Pliant Black on white
- Accent colors for borders, table headers, or callout boxes
- Pliant Yellow only for small highlight elements

### General Principles
- Generous white space — don't crowd layouts
- Balance bright and neutral colors
- Yellow = focal point, not filler
- Keep compositions clean with max two bright colors + neutrals
