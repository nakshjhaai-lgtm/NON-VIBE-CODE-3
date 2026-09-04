# Vance Dental Studio: design system

Personality: quiet Midtown suite. Warm limestone paper, charcoal ink, single brass accent.
References: Refero (ElevenLabs warmth, Apple restraint, Notion paper), premium dental editorial sites.

## Tokens
- Canvas: `#F3F0EA` paper / `#FFFEFB` porcelain / `#E7E1D7` limestone
- Ink: `#1C1915` / `#5A554C` / `#8A847A`
- Accent: `#A67C52` brass only (no purple, neon, multi-gradient)
- Radius: 6 / 12 / pill only
- Spacing: 8px base
- Type: Newsreader (display) + Figtree (UI) + IBM Plex Mono (labels)
- Motion: 160–320ms, max 2px hover lift, respects prefers-reduced-motion

## Copy and markup rules enforced
Structural class names only: `section-label`, `intro`. Never `eyebrow`, `lead`, `kicker`,
`tagline` or `hero-copy`, because scanners read the source, and those names are a landing-page
template fingerprint. All page text follows `COPY_GUIDE.md`, which applies
[Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
to marketing copy. `python3 tools/copy_audit.py` must exit 0 before a deploy.

Every absolute URL is assembled from `SITE_URL` in `build_pages.py`, so canonical, `og:url`,
JSON-LD, `sitemap.xml`, `robots.txt` and `llms.txt` always name the host the site is served
from. No number appears in copy unless it can be sourced. That is why the hero carries no
review count, no "documented smiles" total and no `aggregateRating` in the structured data.

## Anti-vibe rules enforced
No Inter/Geist/Poppins defaults, no purple gradients, no sparkles/emoji UI, no nested card stacks,
no aggressive hover, no invented testimonials (patient quotes carry a month and a stated source),
no stock headshots standing in for patients, no team photos, no broken socials,
full meta/OG/favicon, robots/sitemap/llms.txt, 404, legal pages, loading states, keyboard access.
