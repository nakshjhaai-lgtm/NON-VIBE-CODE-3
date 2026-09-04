# Copy guide: writing this site so it does not read as machine-generated

Every string a visitor sees lives in `build_pages.py` (plus `SEARCH_INDEX` in
`js/main.js`). The HTML files are generated, so edit the generator and re-run:

```bash
python3 build_pages.py     # regenerate all pages
python3 tools/copy_audit.py --notes   # must exit 0
```

The rules below apply
[Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
to marketing copy. That page is descriptive rather than prescriptive, and it
warns that the patterns are signs of a problem, not the problem itself, so
these are house rules for this site, not a claim that any sentence containing
them was written by a machine.

## 1. Rule of three

Do not build a headline, a hero lead or a card blurb out of a three-item list.
"A, B and C" is the single loudest rhythm in generated copy, and this site had
it four times on the home page alone.

| No | Yes |
| --- | --- |
| Care shaped around diagnosis, materials and longevity | Each plan lists the materials, how many visits the work needs and what it will cost |
| Artistry, technology and empathy | Dr. Vance examines every patient and writes every treatment plan himself |

Two items read as a pair. Four or more read as a list of things the reader
actually needs, which is usually what a dental page is for. If a genuine
three-item list is unavoidable ("Photo ID, your insurance card and a list of
medications"), keep it in body copy where it is informational, and do not put
another one in the same section.

`tools/copy_audit.py` reports three-item lists in headings, leads and meta
descriptions as findings, and three-item lists deep in body copy as notes.
Notes need a human decision; findings need a rewrite.

## 2. Negative antithesis

"No longer X, but Y", "not just X", "X rather than Y" and the clipped
comma form "planned for harmony, not a shade guide" are all the same move:
define the subject by what it is not, then supply the flattering opposite.

Cut them. State the thing.

| No | Yes |
| --- | --- |
| Your smile is planned, not improvised | Every treatment plan is written out before anything is scheduled |
| Materials chosen for how they age, not how they photograph | Materials are picked for how they hold up five years out |
| Outcomes you can read, not just admire | Three recent treatments, written up |
| Match translucency at the incisal edge rather than a flat shade | Match translucency at the incisal edge instead of one flat shade across the tooth |

Plain negation that carries information is fine and should stay: "We do not
sell personal information", "Clinical photographs are not published here".
The tell is the rhetorical contrast, not the word "not".

## 3. Promotional and puffery wording

Banned outright: *setting a standard*, *gold standard*, *boutique*, *premier*,
*world-class*, *seamless*, *elevate*, *unlock*, *experience focused*,
*your dream smile*, *passionate about*, *dedicated to*, *committed to*,
*unwavering*, *holistic*, *cutting-edge*, *state of the art*.

Replace every one of them with a fact that can be checked: a number, a
material, a time, a street, a name. "Setting a clear standard for dental
health" became "One dentist, one address. Dr. Vance examines every patient
and writes every treatment plan himself."

## 4. AI vocabulary

The words the guide lists as high-density in model output are banned here:
*meticulous, pivotal, underscore, tapestry, testament, vibrant, crucial,
vital, foster, showcase, highlight, emphasize, enhance, bolster, enduring,
seamless, delve, landscape, realm, embark, navigate, harness, robust,
comprehensive, streamline, transformative, innovative, unwavering, curated,
plays a role, stands as, serves as, boasts, at the heart of, it is worth
noting, moreover, furthermore, additionally*.

This is literal, per the guide: a listed word is the problem, its synonym is
not. "Care shaped around diagnosis" was cut because *shaped around* is the
copula-dodging construction; "planned from" would have been fine.

## 5. Copula dodging

Prefer *is*, *are* and *has* over *serves as*, *stands as*, *features*,
*offers*, *boasts*, *maintains* and *represents*. "The studio has two
operatories" beats "the studio features two operatories".

## 6. Aphoristic closers

A paragraph that ends on a polished slogan reads as generated. Delete the
slogan; the preceding sentence is usually the better ending.

| No | Yes |
| --- | --- |
| That continuity is the product. | ...so the person charting your pockets has read last year's notes. |
| Prevention is quieter than repair, and far less expensive over a lifetime. | Decay caught while it is still in enamel is a small filling; the same lesion two years later is usually a crown. |
| You set the pace. | We describe each step before we start, and you can ask for a break at any point. |
| It keeps the clinical hour clinical. | Filling in the paperwork before you arrive leaves the appointment itself for the examination. |

## 7. Headings

Sentence case, no terminal full stop, and do not stack parallel labels down a
page. Vary length: one long concrete heading next to two short ones reads
human; six headings of the same shape and length do not.

"Listen & map / Design the plan / Treat & maintain" became "The first hour /
A written plan you keep / Treatment and follow-up".

Titles of services and cases follow the same rule. "Enamel-led veneer harmony"
became "Four upper veneers after grinding wear". `Invisalign®` keeps its
capital because it is a registered brand name.

## 8. Unverifiable claims

No number goes on this site unless somebody at the studio can source it.
Removed on that basis: *5,000+ documented smiles*, *4.9/5 from 800+ reviews*
(and the `aggregateRating` block in the JSON-LD that repeated it), *2× faster
healing*, and the three stock headshots in the hero that implied a patient
roster. Patient quotes now carry the month of the visit and a line saying
where they came from.

If a claim cannot be sourced, cut it rather than softening it.

## 9. Typography

Straight quotes and apostrophes in body copy. Em dashes are not used here at
all. En dashes only for ranges that are genuinely ranges (`Mon–Fri`), and
spelled-out ranges elsewhere ("7 to 10 days"). Curly quotation marks are a
listed tell, so the generated pages avoid them even inside patient quotes.

## 10. Class names and markup

Scanners read the source, not just the rendered text. Structural names only:
`section-label` and `intro`, not `eyebrow`, `lead`, `kicker`, `tagline` or
`hero-copy`. No inline-header lists built from `<strong>Label.</strong> body`
more than once per page. Alt text on every image, describing what is in the
picture ("A treatment room at the studio: chair, overhead light and a window
facing Avenue of the Americas"), never "" on a meaningful image and never a
restatement of the caption.

## 11. Host consistency

`SITE_URL` at the top of `build_pages.py` is the only place an absolute URL is
assembled. Canonical, `og:url`, `twitter:image`, JSON-LD, `sitemap.xml`,
`robots.txt` and `llms.txt` all read from it, so the markup never advertises a
domain the visitor did not arrive on. If the studio attaches a custom domain,
change `SITE_URL` and regenerate. Do not hand-edit the HTML.
