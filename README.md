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
