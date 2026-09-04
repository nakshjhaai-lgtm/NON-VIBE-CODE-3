# Vance Dental Studio

Static multi-page website for Dr. Alistair Vance / Vance Dental Studio.

## Deploy on Netlify

1. Connect this repository to Netlify, **or** drag-and-drop the project folder onto [Netlify Drop](https://app.netlify.com/drop).
2. Publish directory: project root (`.`).
3. No build command required (optional: `python3 build_pages.py` if you edit the generator).

Forms use Netlify Forms (`netlify` attribute on the contact form). Enable forms in the Netlify UI after first deploy.

## Local preview

```bash
python3 -m http.server 8080
```

Open http://localhost:8080

## Structure

- `index.html` and sibling pages, static HTML
- `css/styles.css`, design system
- `js/main.js`, interactions
- `netlify.toml`, `_headers`, `_redirects`, Netlify config
- `sitemap.xml`, `robots.txt`, `llms.txt`, SEO / AI discovery

## Canonical host

`SITE_URL` at the top of `build_pages.py` is the single source for every
absolute URL the site emits (canonical, `og:url`, `twitter:image`, JSON-LD,
`sitemap.xml`, `robots.txt`, `llms.txt`). It currently points at the Netlify
host the site is served from, so the markup never advertises a domain the
visitor did not arrive on. When a custom domain is attached, change that one
line and re-run the generator.

## Copy rules

Page text follows `COPY_GUIDE.md`, which applies
[Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
to marketing copy. Read it before editing any string in `build_pages.py`.
