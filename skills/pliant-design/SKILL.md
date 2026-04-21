---
name: pliant-design
description: Applies Pliant's official brand colors, typography, and shape language (rounded corners, never sharp) to any sort of artifact that may benefit from having Pliant's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply. Make sure to use this skill whenever the user mentions Pliant branding, corporate identity, brand colors, visual identity, or wants outputs styled with the Pliant brand, even if they don't explicitly say "brand guidelines."
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

## Shape & Corners

Pliant's shape language is **soft and rounded** — never sharp. Rounded corners reinforce the friendly, approachable feel of the brand and pair with the generous white space and bright accent colors.

### Corner Radius Scale

Use these radii consistently so the softness feels intentional rather than random.

| Element | Radius | CSS |
|---------|--------|-----|
| Small controls (chips, tags, inline badges) | 6px | `border-radius: 6px;` |
| Buttons, inputs, form fields | 10px | `border-radius: 10px;` |
| Cards, callouts, tables, panels | 16px | `border-radius: 16px;` |
| Large containers, hero blocks, modals | 24px | `border-radius: 24px;` |
| Pills, avatars, fully-rounded CTAs | 9999px | `border-radius: 9999px;` |
| Images, illustrations, media | 12–16px | `border-radius: 12px;` |

### Shape Rules

- **Never use sharp (0px) corners** on branded surfaces — cards, buttons, inputs, tables, images, charts, and callouts must all be rounded.
- Apply radii consistently within a layout — don't mix, e.g., 4px buttons with 16px cards.
- Children should be more rounded than their parent is unrounded — avoid square elements sitting inside rounded containers.
- On nested elements, keep child radius ≤ parent radius so curves stay concentric.
- Charts, code blocks, and image thumbnails must also be rounded — they're not exceptions.
- Fully-rounded pills (`9999px`) are reserved for status tags and avatar-style elements, not standard buttons.

## Applying the Brand

When creating branded outputs, apply the guidelines as follows:

### HTML / Web Artifacts
- Set body background to White, text to Pliant Black
- Use Pangea for headings, Maison Neue for body text (with Arial/Helvetica fallbacks)
- Use Pliant Yellow sparingly for highlights, CTAs, or accent elements — not for large backgrounds
- Use secondary colors for cards, tags, and visual variety
- For dark/tech sections, use Dark Charcoal background with white text
- **Rounded corners everywhere**: buttons `border-radius: 10px`, cards/tables/panels `16px`, hero blocks/modals `24px`, chips/tags `6px`, status pills `9999px`. Images and chart containers `12–16px`. Never ship sharp 0px corners on branded surfaces.

### Presentations (PPTX)
- Apply via python-pptx's RGBColor class
- Headings (24pt+): Pangea font
- Body text: Maison Neue font
- Title slides can use Pliant Yellow as an accent stripe or highlight
- Content slides: white background, black text, accent colors for shapes
- **Use rounded shapes**: prefer `MSO_SHAPE.ROUNDED_RECTANGLE` over `RECTANGLE` for every shape, callout, and image frame. After inserting, set `shape.adjustments[0]` to ~0.1 for standard content shapes and ~0.15 for hero/title shapes so the radius matches the web scale.

### Documents (DOCX)
- Headings: Pangea, Pliant Black
- Body: Maison Neue, Pliant Black on white
- Accent colors for borders, table headers, or callout boxes
- Pliant Yellow only for small highlight elements
- **Round callout boxes and image frames** wherever the renderer supports it (e.g., shape `prstGeom` set to `roundRect`). Table corners and inserted images should not read as hard rectangles.

### General Principles
- Generous white space — don't crowd layouts
- Balance bright and neutral colors
- Yellow = focal point, not filler
- Keep compositions clean with max two bright colors + neutrals
- Soft, rounded corners on every surface — sharp rectangles break the brand feel
