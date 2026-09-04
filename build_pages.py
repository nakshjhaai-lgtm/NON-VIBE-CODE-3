#!/usr/bin/env python3
"""Generate all Vance Dental Studio static pages for Netlify."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ─── Shared data (from original Index.html, same clinic data) ───
DATA = {
    "name": "Vance Dental Studio",
    "short": "Vance Dental",
    "doctor": "Dr. Alistair Vance",
    "tagline": "Precision dentistry in Midtown Manhattan",
    "phone": "+1 (212) 555-0198",
    "phone_tel": "+12125550198",
    "email": "hello@vancedental.com",
    "address_line1": "1200 Avenue of the Americas, Suite 400",
    "address_line2": "New York, NY 10036",
    "lat": "40.758896",
    "lng": "-73.985130",
    "hours": [
        ("Monday – Friday", "08:00 AM – 07:00 PM"),
        ("Saturday", "09:00 AM – 04:00 PM"),
        ("Sunday", "Closed"),
    ],
    "instagram": "https://www.instagram.com/",
    "facebook": "https://www.facebook.com/",
    "linkedin": "https://www.linkedin.com/",
    "reviews_count": "800+",
    "rating": "4.9",
    "smiles": "5,000+",
    "response": "within 24 hours",
}

NAV = [
    ("index.html", "Home", "home"),
    ("services.html", "Services", "services"),
    ("gallery.html", "Gallery", "gallery"),
    ("cases.html", "Cases", "cases"),
    ("about.html", "About", "about"),
    ("visit.html", "Visit", "visit"),
    ("patients.html", "Patients", "patients"),
    ("contact.html", "Contact", "contact"),
]

SERVICES = [
    {
        "id": "cosmetic",
        "title": "Cosmetic Dentistry",
        "icon": "heart",
        "blurb": "Veneers, whitening, and bonding planned for facial harmony, not a one-size shade guide.",
        "body": "Every cosmetic plan starts with photography, shade mapping, and a trial smile when needed. We use conservative preparation and laboratory partners who match enamel translucency, so restorations read as natural teeth under daylight and evening light.",
        "points": ["Porcelain veneers & bonding", "Guided whitening protocols", "Smile trial & mock-ups"],
    },
    {
        "id": "implants",
        "title": "Dental Implants",
        "icon": "layers",
        "blurb": "3D-guided implant placement for permanent, natural-looking tooth replacement.",
        "body": "Implant care is planned on CBCT imaging with surgical guides when anatomy demands precision. From single-tooth replacement to full-arch reconstruction, the goal is stable bone, clean emergence profiles, and a bite you can trust for decades.",
        "points": ["CBCT & guided surgery", "Single tooth to full arch", "Immediate provisional options"],
        "dark": True,
    },
    {
        "id": "invisalign",
        "title": "Invisalign®",
        "icon": "scan",
        "blurb": "Custom clear aligners with computerized staging and refinements built into the plan.",
        "body": "Digital scans replace messy impressions. We review tooth movement stage by stage, including attachments and elastics when indicated, and schedule progress checks so treatment stays on time without surprise mid-course corrections.",
        "points": ["Digital scan workflow", "Discreet full-time wear", "Refinement included in plan"],
    },
    {
        "id": "checkup",
        "title": "General Checkup",
        "icon": "shield",
        "blurb": "Preventive exams and cleanings that protect the work we place and the enamel you still have.",
        "body": "Routine visits combine periodontal charting, low-dose imaging when indicated, and a hygiene protocol matched to your risk level. Prevention is quieter than repair, and far less expensive over a lifetime.",
        "points": ["Risk-based hygiene", "Early decay detection", "Home-care coaching"],
    },
]

# Patient reviews, specific, named, no AI face claims; initials + borough only
REVIEWS = [
    {
        "name": "Marisa K.",
        "meta": "Upper West Side · Veneers",
        "quote": "I came in for two chipped front teeth after a bike fall. Dr. Vance matched the translucency so well that my hygienist asked which ones were new.",
        "stars": 5,
    },
    {
        "name": "James O.",
        "meta": "Financial District · Implant",
        "quote": "The implant consult included a clear fee range before any surgery date. Placement day was shorter than I expected, and the temporary looked finished, not temporary.",
        "stars": 5,
    },
    {
        "name": "Priya S.",
        "meta": "Brooklyn · Invisalign",
        "quote": "Aligner check-ins took twenty minutes and always showed the next three stages on screen. I finished two weeks ahead of the original estimate.",
        "stars": 5,
    },
]

CASES = [
    {
        "id": "veneer-harmony",
        "title": "Enamel-led veneer harmony",
        "tag": "Cosmetic",
        "summary": "Four upper veneers to correct wear and uneven length after years of night grinding.",
        "result": "Even central length, restored canine guidance, and a shade that holds under office LEDs and restaurant light.",
        "duration": "3 visits · 5 weeks",
    },
    {
        "id": "single-implant",
        "title": "Single molar implant, guided",
        "tag": "Implants",
        "summary": "Failed root canal on a lower first molar replaced with a guided implant and screw-retained crown.",
        "result": "Stable bone levels at 12-month review; patient returned to normal chewing on that side within six weeks of final crown.",
        "duration": "Surgery + crown · 4 months",
    },
    {
        "id": "align-crowding",
        "title": "Adult crowding, clear aligners",
        "tag": "Invisalign",
        "summary": "Moderate lower crowding and a deep bite addressed with aligners and limited IPR.",
        "result": "Arch form improved without extractions; retention plan set with fixed lower wire and night aligner.",
        "duration": "11 months · 28 trays",
    },
]

FAQS = [
    ("How soon can I be seen?",
     "Urgent pain is triaged the same day when the schedule allows. Routine new-patient exams are typically offered within 7–10 days. We confirm every booking request within 24 hours."),
    ("Do you accept my insurance?",
     "We work with most major PPO plans as an out-of-network provider and submit claims on your behalf. Before treatment, you receive a written estimate showing expected insurance portion and your share."),
    ("Is the studio accessible?",
     "Suite 400 is elevator-served from the Avenue of the Americas lobby. Tell us about mobility needs when you book so we can allocate the right operatory and schedule buffer."),
    ("What should I bring to my first visit?",
     "Photo ID, insurance card if applicable, a medication list, and any recent X-rays on disc or portal. New-patient forms can be completed ahead of time from the Patients page."),
    ("How do you handle comfort and anxiety?",
     "We explain each step before instruments are in the mouth, offer breaks on request, and discuss nitrous or oral sedation when clinically appropriate. You set the pace."),
    ("Where do I park?",
     "Validated parking is available at the 43rd Street garage for scheduled patients. Subway access is via Bryant Park / 42 St and 47–50 St Rockefeller Center stations."),
]

GALLERY = [
    ("https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&q=80&w=1200",
     "Treatment suite with natural light and calibrated operatory lighting"),
    ("https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&q=80&w=1000",
     "Clinical equipment arranged for a planned restorative visit"),
    ("https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&q=80&w=800",
     "Reception lounge with quiet seating and material samples"),
    ("https://images.unsplash.com/photo-1597764690523-15bea4c581c9?auto=format&fit=crop&q=80&w=800",
     "Consultation desk with digital scan display"),
    ("https://images.unsplash.com/photo-1606811971618-4486d14f3f99?auto=format&fit=crop&q=80&w=1000",
     "Corridor view toward private operatories"),
    ("https://images.unsplash.com/photo-1629909615184-74f495363b67?auto=format&fit=crop&q=80&w=800",
     "Sterilization and prep area maintained to clinic protocol"),
]

# Patient avatars in hero, real Unsplash people photos (not claimed as team)
AVATARS = [
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=100",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=100",
    "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=100",
]


def icon(name, size=20):
    return f'<span data-icon="{name}" data-size="{size}" aria-hidden="true"></span>'


def stars(n=5):
    return '<span class="stars" role="img" aria-label="{} out of 5 stars">{}</span>'.format(
        n, "".join(icon("star", 14) for _ in range(n))
    )


def head(title, description, path, canonical=None, og_type="website", extra=""):
    can = canonical or path
    abs_og = "https://vancedental.com/og-image.svg"
    return f"""<!DOCTYPE html>
<html lang="en" class="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#F3F0EA">
  <meta name="color-scheme" content="light dark">
  <link rel="canonical" href="https://vancedental.com/{can}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Vance Dental Studio">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="https://vancedental.com/{can}">
  <meta property="og:image" content="{abs_og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{abs_og}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="icon" href="favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://images.unsplash.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap">
  <link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/styles.css">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">
  {extra}
</head>
<body>
<!-- Netlify forms detection (contact form also posts here when hosted) -->
<form name="contact" netlify netlify-honeypot="bot-field" hidden aria-hidden="true">
  <input type="text" name="name">
  <input type="email" name="email">
  <input type="tel" name="phone">
  <input type="text" name="topic">
  <textarea name="message"></textarea>
  <input name="bot-field">
</form>
<script>window.VD_GA_ID = "G-XXXXXXXX";</script>
<a class="skip-link" href="#main-content">Skip to content</a>
<div class="scroll-progress" data-scroll-progress aria-hidden="true"><span></span></div>
"""


def header(active):
    links = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ""
        links.append(f'<a class="nav-link" href="{href}"{cur}>{label}</a>')
    drawer_links = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ""
        drawer_links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f"""
<header class="site-header" data-header>
  <div class="inner">
    <a class="brand" href="index.html" translate="no" aria-label="Vance Dental Studio home">
      <span class="brand-mark" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7 20L12 4l5 16" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M9.2 14h5.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/></svg>
      </span>
      <span>VANCE<em>DENTAL</em></span>
    </a>
    <nav class="nav-desktop" aria-label="Primary">{''.join(links)}</nav>
    <div class="header-actions">
      <button type="button" class="theme-toggle" data-theme-toggle role="switch" aria-checked="false" aria-label="Toggle dark mode"></button>
      <button type="button" class="btn btn-primary btn-sm header-book" data-book-open>Book appointment</button>
      <button type="button" class="btn btn-icon btn-ghost menu-btn" data-menu-open aria-label="Open menu" aria-expanded="false" aria-controls="mobile-drawer">{icon("menu", 22)}</button>
    </div>
  </div>
</header>
<div class="drawer-overlay" data-drawer-overlay></div>
<aside class="drawer" id="mobile-drawer" data-drawer role="dialog" aria-label="Mobile menu" aria-hidden="true">
  <div class="row between">
    <strong class="small">Menu</strong>
    <button type="button" class="btn btn-icon btn-ghost btn-sm" data-menu-close aria-label="Close menu">{icon("x", 20)}</button>
  </div>
  <nav aria-label="Mobile">{''.join(drawer_links)}
    <a href="search.html">Search</a>
  </nav>
  <hr class="divider" style="margin:16px 0">
  <button type="button" class="btn btn-primary" style="width:100%" data-book-open>Book appointment</button>
</aside>
"""


def booking_modal():
    opts = "".join(f'<option value="{s["title"]}">{s["title"]}</option>' for s in SERVICES)
    return f"""
<div class="modal-overlay" id="booking-modal" data-booking-modal role="dialog" aria-modal="true" aria-labelledby="book-title" aria-hidden="true">
  <div class="modal">
    <div class="row between start mb-5">
      <div>
        <h2 id="book-title" class="title" style="font-size:1.75rem">Book a visit</h2>
        <p class="small text-2 mt-2">We confirm every request {DATA["response"]}.</p>
      </div>
      <button type="button" class="btn btn-icon btn-ghost btn-sm" data-book-close aria-label="Close dialog">{icon("x", 20)}</button>
    </div>
    <form class="stack stack-4" data-booking-form novalidate>
      <div class="field">
        <label class="field-label" for="book-name">Full name</label>
        <input class="input" id="book-name" name="name" autocomplete="name" required placeholder="Jordan Lee">
        <p class="field-error" role="alert">Enter your full name.</p>
      </div>
      <div class="field">
        <label class="field-label" for="book-email">Email</label>
        <input class="input" id="book-email" name="email" type="email" autocomplete="email" required placeholder="you@email.com" spellcheck="false">
        <p class="field-error" role="alert">Enter a valid email.</p>
      </div>
      <div class="field">
        <label class="field-label" for="book-phone">Phone</label>
        <input class="input" id="book-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+1 (212) 555-0198">
      </div>
      <div class="field">
        <label class="field-label" for="book-service">Service</label>
        <select class="select" id="book-service" name="service" required>
          <option value="" disabled selected>Select a service…</option>
          {opts}
        </select>
        <p class="field-error" role="alert">Choose a service.</p>
      </div>
      <div class="field">
        <label class="field-label" for="book-note">Anything we should know?</label>
        <textarea class="textarea" id="book-note" name="note" placeholder="Preferred days, sensitivity, recent X-rays…"></textarea>
      </div>
      <button type="submit" class="btn btn-primary btn-lg">Confirm booking {icon("check", 16)}</button>
      <p class="micro text-3">By submitting, you agree to be contacted about this appointment. See our <a href="privacy.html" style="color:var(--brass)">Privacy Policy</a>.</p>
    </form>
  </div>
</div>
"""


def footer():
    return f"""
<footer class="site-footer" role="contentinfo">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html" translate="no" style="color:#fff">
          <span class="brand-mark" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7 20L12 4l5 16" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M9.2 14h5.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/></svg>
          </span>
          <span>VANCE<em>DENTAL</em></span>
        </a>
        <p class="small mt-5" style="color:var(--footer-muted);max-width:32ch;line-height:1.7">
          Setting a clear standard for dental health with artistry, technology, and empathy. Your smile is planned, not improvised.
        </p>
        <div class="social-row">
          <a class="social-btn" href="{DATA['instagram']}" target="_blank" rel="noopener noreferrer" aria-label="Instagram">{icon("instagram", 16)}</a>
          <a class="social-btn" href="{DATA['facebook']}" target="_blank" rel="noopener noreferrer" aria-label="Facebook">{icon("facebook", 16)}</a>
          <a class="social-btn" href="{DATA['linkedin']}" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">{icon("linkedin", 16)}</a>
        </div>
      </div>
      <div>
        <h2 class="footer-title">Explore</h2>
        <nav class="footer-links" aria-label="Footer">
          <a href="services.html">Services</a>
          <a href="cases.html">Case studies</a>
          <a href="gallery.html">Gallery</a>
          <a href="about.html">About {DATA["doctor"]}</a>
          <a href="visit.html">Visit the studio</a>
          <a href="search.html">Search</a>
        </nav>
      </div>
      <div>
        <h2 class="footer-title">Patients</h2>
        <nav class="footer-links" aria-label="Patient links">
          <a href="patients.html">Patient forms</a>
          <a href="patients.html#insurance">Insurance</a>
          <a href="contact.html">Contact</a>
          <a href="privacy.html">Privacy Policy</a>
          <a href="terms.html">Terms of Service</a>
          <a href="thank-you.html">After you write</a>
        </nav>
      </div>
      <div>
        <h2 class="footer-title">Newsletter</h2>
        <p class="small" style="color:var(--footer-muted);margin-bottom:12px">Oral health notes and studio updates. Monthly, no clutter.</p>
        <form data-newsletter class="row gap-2" style="align-items:stretch">
          <label for="footer-email" class="sr-only">Email address</label>
          <input id="footer-email" class="input" type="email" name="email" required placeholder="Email address" autocomplete="email" spellcheck="false" style="background:#1F1C18;border-color:rgba(255,255,255,.12);color:#F3F0EA;min-height:40px;font-size:14px">
          <button type="submit" class="btn btn-primary btn-sm" aria-label="Subscribe">{icon("arrowRight", 16)}</button>
        </form>
        <p class="small mt-5" style="color:var(--footer-muted)">
          <a href="tel:{DATA['phone_tel']}">{DATA["phone"]}</a><br>
          <a href="mailto:{DATA['email']}">{DATA["email"]}</a>
        </p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span data-year>2026</span> Vance Dental Studio. All rights reserved.</p>
      <p><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a> · <a href="sitemap.xml">Sitemap</a></p>
    </div>
  </div>
</footer>

<button type="button" class="back-top" data-back-top aria-label="Back to top">{icon("arrowUp", 18)}</button>
<a class="float-contact" href="contact.html" aria-label="Contact the studio">{icon("message", 22)}</a>
<div class="mobile-cta" data-mobile-cta>
  <a class="btn btn-secondary" href="tel:{DATA['phone_tel']}">{icon("phone", 16)} Call</a>
  <button type="button" class="btn btn-primary" data-book-open>{icon("calendar", 16)} Book</button>
</div>
<div class="cookie-bar" data-cookie role="dialog" aria-label="Cookie preference">
  <p>We use essential cookies to run the site and optional analytics if you accept. <a href="privacy.html" style="color:var(--brass)">Privacy Policy</a></p>
  <div class="row gap-2">
    <button type="button" class="btn btn-secondary btn-sm" data-cookie-reject>Reject</button>
    <button type="button" class="btn btn-primary btn-sm" data-cookie-accept>Accept</button>
  </div>
</div>
<div class="toast-region" data-toast-region aria-live="polite" aria-relevant="additions"></div>
{booking_modal()}
<script src="js/icons.js" defer></script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin="" defer></script>
<script src="js/main.js" defer></script>
"""


def breadcrumbs(items):
    """items: list of (href|None, label)"""
    parts = []
    for i, (href, label) in enumerate(items):
        if i:
            parts.append('<span class="sep" aria-hidden="true">/</span>')
        if href and i < len(items) - 1:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
    return f'<nav class="breadcrumbs container" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def page_hero(eyebrow, title, lead):
    return f"""
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <p class="lead mt-4">{lead}</p>
  </div>
</section>
"""


def schema_org():
    return f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "name": "Vance Dental Studio",
  "image": "https://vancedental.com/og-image.svg",
  "url": "https://vancedental.com/",
  "telephone": "{DATA['phone_tel']}",
  "email": "{DATA['email']}",
  "priceRange": "$$",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "1200 Avenue of the Americas, Suite 400",
    "addressLocality": "New York",
    "addressRegion": "NY",
    "postalCode": "10036",
    "addressCountry": "US"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": {DATA['lat']},
    "longitude": {DATA['lng']}
  }},
  "openingHoursSpecification": [
    {{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "08:00",
      "closes": "19:00"
    }},
    {{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "09:00",
      "closes": "16:00"
    }}
  ],
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "800"
  }},
  "founder": {{
    "@type": "Person",
    "name": "Dr. Alistair Vance",
    "jobTitle": "Dentist"
  }}
}}
</script>
"""


def faq_schema():
    entities = []
    for q, a in FAQS:
        entities.append(
            f'{{"@type":"Question","name":{q!r},"acceptedAnswer":{{"@type":"Answer","text":{a!r}}}}}'
        )
    return f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(entities)}]}}</script>'


def close_body():
    return """
</body>
</html>
"""


def build_index():
    service_cards = []
    for s in SERVICES[:3]:
        dark = " card-dark" if s.get("dark") else ""
        service_cards.append(f"""
        <article class="card card-interactive{dark}">
          <div class="icon-wrap mb-5">{icon(s["icon"], 20)}</div>
          <h3 class="heading mb-3">{s["title"]}</h3>
          <p class="small text-2 mb-5">{s["blurb"]}</p>
          <a class="btn btn-link" href="services.html#{s["id"]}">View service {icon("chevronRight", 16)}</a>
        </article>""")

    review_cards = []
    for r in REVIEWS:
        review_cards.append(f"""
        <figure class="card card-flat stack stack-4">
          {stars(r["stars"])}
          <blockquote class="quote">“{r["quote"]}”</blockquote>
          <figcaption class="small"><strong>{r["name"]}</strong><span class="text-3"> · {r["meta"]}</span></figcaption>
        </figure>""")

    faq_html = []
    for i, (q, a) in enumerate(FAQS[:5]):
        faq_html.append(f"""
        <details class="faq-item">
          <summary class="faq-trigger">{q}<span class="faq-icon">{icon("plus", 16)}</span></summary>
          <div class="faq-panel">{a}</div>
        </details>""")

    avatars = "".join(
        f'<img src="{src}" width="40" height="40" alt="" loading="lazy">' for src in AVATARS
    )

    content = f"""
<main id="main-content">
  <section class="hero" id="home">
    <div class="container hero-panel">
      <div>
        <p class="eyebrow">Precision dental care in New York</p>
        <h1>Modern <span class="accent">precision</span> dentistry.</h1>
        <p class="lead mt-5">
          Experience focused dental care with {DATA["doctor"]}. Measured diagnostics, calm operatories, and treatment plans you can read before you commit.
        </p>
        <div class="hero-actions">
          <button type="button" class="btn btn-primary btn-lg" data-book-open>{icon("calendar", 18)} Schedule visit</button>
          <a class="btn btn-secondary btn-lg" href="gallery.html">View gallery {icon("arrowRight", 18)}</a>
        </div>
        <div class="hero-proof">
          <div class="avatar-stack" aria-hidden="true">{avatars}</div>
          <div>
            <p class="small" style="font-weight:600">{DATA["smiles"]} documented smiles</p>
            <div class="row gap-2 mt-2">
              {stars(5)}
              <span class="micro text-3">{DATA["rating"]}/5 · {DATA["reviews_count"]} reviews</span>
            </div>
          </div>
        </div>
      </div>
      <div style="position:relative">
        <div class="media media-wide">
          <img src="https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&q=80&w=1000"
               width="800" height="600"
               alt="Interior of Vance Dental Studio showing a modern treatment room"
               fetchpriority="high">
        </div>
        <div class="float-card">
          <div class="icon-wrap" style="width:40px;height:40px">{icon("zap", 16)}</div>
          <div>
            <p class="small" style="font-weight:600">2× faster healing</p>
            <p class="micro text-3">Laser-assisted protocols</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section-tight">
    <div class="container">
      <div class="stat-strip" aria-label="Studio highlights">
        <div class="stat-item"><strong class="tabular">18</strong><span>Years in practice</span></div>
        <div class="stat-item"><strong class="tabular">{DATA["rating"]}</strong><span>Average patient rating</span></div>
        <div class="stat-item"><strong class="tabular">24h</strong><span>Booking response promise</span></div>
        <div class="stat-item"><strong class="tabular">1</strong><span>Midtown studio address</span></div>
      </div>
    </div>
  </section>

  <section class="section" id="services" aria-labelledby="services-heading">
    <div class="container">
      <p class="eyebrow">What we do</p>
      <div class="md-grid-2 mb-8">
        <h2 id="services-heading" class="title">Care shaped around diagnosis, not packages.</h2>
        <p class="lead">From preventive visits to complex restoration, each plan is written with materials, timeline, and fees you can review in advance.</p>
      </div>
      <div class="grid-3">{''.join(service_cards)}</div>
      <div class="mt-6"><a class="btn btn-secondary" href="services.html">All services {icon("arrowRight", 16)}</a></div>
    </div>
  </section>

  <section class="section section-band" id="approach" aria-labelledby="approach-heading">
    <div class="container">
      <p class="eyebrow">How visits work</p>
      <h2 id="approach-heading" class="title mb-8">Three steps. No mystery fees mid-appointment.</h2>
      <div class="steps">
        <div class="step">
          <h3 class="heading mb-3">Listen & map</h3>
          <p class="small text-2">We start with history, photos, and only the imaging that changes the plan. You leave with findings in plain language.</p>
        </div>
        <div class="step">
          <h3 class="heading mb-3">Design the plan</h3>
          <p class="small text-2">Options are ranked by longevity and invasiveness. You approve sequence and budget before chairs recline for treatment.</p>
        </div>
        <div class="step">
          <h3 class="heading mb-3">Treat & maintain</h3>
          <p class="small text-2">Procedures are paced for comfort. Maintenance intervals are set to protect the work, not to fill the book.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="cases-preview" aria-labelledby="cases-heading">
    <div class="container">
      <div class="row between row-wrap gap-4 mb-8">
        <div>
          <p class="eyebrow">Case studies</p>
          <h2 id="cases-heading" class="title">Outcomes you can read, not just admire.</h2>
        </div>
        <a class="btn btn-secondary" href="cases.html">All cases</a>
      </div>
      <div class="grid-3">
        {''.join(f'''
        <article class="card card-interactive">
          <span class="badge badge-brass mb-4">{c["tag"]}</span>
          <h3 class="heading mb-3">{c["title"]}</h3>
          <p class="small text-2 mb-4">{c["summary"]}</p>
          <p class="micro text-3">{c["duration"]}</p>
          <a class="btn btn-link mt-4" href="cases.html#{c["id"]}">Read case {icon("chevronRight", 16)}</a>
        </article>''' for c in CASES)}
      </div>
    </div>
  </section>

  <section class="section section-band" id="reviews" aria-labelledby="reviews-heading">
    <div class="container">
      <p class="eyebrow">Patient notes</p>
      <h2 id="reviews-heading" class="title mb-4">Specific feedback from real visits.</h2>
      <p class="lead mb-8">Quotes reference named treatments and neighborhoods. We do not publish stock headshots as proof.</p>
      <div class="grid-3">{''.join(review_cards)}</div>
    </div>
  </section>

  <section class="section" id="faq" aria-labelledby="faq-heading" data-faq>
    <div class="container" style="max-width:800px">
      <p class="eyebrow">FAQs</p>
      <h2 id="faq-heading" class="title mb-6">Questions patients ask before the first visit.</h2>
      {''.join(faq_html)}
      <p class="small text-2 mt-6">Still unsure? <a href="contact.html" style="color:var(--brass);font-weight:600">Write the studio</a>, response {DATA["response"]}.</p>
    </div>
  </section>

  <section class="section section-dark" aria-labelledby="cta-heading">
    <div class="container" style="text-align:center;max-width:640px">
      <p class="eyebrow" style="justify-content:center">Next step</p>
      <h2 id="cta-heading" class="title mb-4">Reserve a chair on Avenue of the Americas.</h2>
      <p class="lead mb-6" style="margin-inline:auto">Tell us what hurts, what you want to change, or simply that it is time for a checkup. We reply {DATA["response"]}.</p>
      <div class="row-wrap gap-3 center">
        <button type="button" class="btn btn-primary btn-lg" data-book-open>{icon("calendar", 18)} Book appointment</button>
        <a class="btn btn-secondary btn-lg" href="visit.html" style="background:transparent;color:#F3F0EA;border-color:rgba(255,255,255,.2)">Get directions</a>
      </div>
    </div>
  </section>
</main>
"""
    html = (
        head(
            "Vance Dental Studio | Precision Dentistry in Midtown Manhattan",
            "Dr. Alistair Vance provides precision dentistry at 1200 Avenue of the Americas, implants, Invisalign, cosmetic care, and preventive visits.",
            "index.html",
            canonical="",
            extra=schema_org() + faq_schema(),
        )
        + header("home")
        + content
        + footer()
        + close_body()
    )
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def build_services():
    blocks = []
    for s in SERVICES:
        points = "".join(f"<li>{p}</li>" for p in s["points"])
        blocks.append(f"""
        <article class="card mb-5" id="{s["id"]}">
          <div class="row gap-4 start mb-5">
            <div class="icon-wrap">{icon(s["icon"], 20)}</div>
            <div>
              <h2 class="heading">{s["title"]}</h2>
              <p class="small text-2 mt-2">{s["blurb"]}</p>
            </div>
          </div>
          <p class="text-2" style="max-width:48rem">{s["body"]}</p>
          <ul class="mt-5 stack stack-2 small" style="padding-left:1.1rem;list-style:disc;color:var(--text-2)">{points}</ul>
          <button type="button" class="btn btn-primary mt-6" data-book-open>Request this service</button>
        </article>""")
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Services")])
        + page_hero(
            "Services",
            "Treatment built from diagnosis outward.",
            "Four core service lines. Each plan lists materials, visits, and fees before work begins.",
        )
        + f'<main id="main-content" class="section"><div class="container">{"".join(blocks)}</div></main>'
    )
    html = head(
        "Services | Vance Dental Studio",
        "Cosmetic dentistry, dental implants, Invisalign, and general checkups with Dr. Alistair Vance in Midtown Manhattan.",
        "services.html",
    ) + header("services") + content + footer() + close_body()
    (ROOT / "services.html").write_text(html, encoding="utf-8")


def build_gallery():
    items = []
    for i, (src, alt) in enumerate(GALLERY):
        cls = "span-2" if i == 0 else ("span-2-w" if i == 5 else "")
        items.append(f"""
        <figure class="media {cls}">
          <img src="{src}" alt="{alt}" width="800" height="600" loading="{'eager' if i==0 else 'lazy'}">
        </figure>""")
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Gallery")])
        + page_hero(
            "Inside the studio",
            "The Vance experience, room by room.",
            "A boutique clinic designed for calm focus, not a waiting-room television and fluorescent hum.",
        )
        + f"""
<main id="main-content" class="section section-band">
  <div class="container">
    <div class="mosaic">{''.join(items)}</div>
    <p class="small text-2 mt-6">Photography shows the Midtown studio environment. We do not publish staff portraits on this site.</p>
  </div>
</main>"""
    )
    html = head(
        "Gallery | Vance Dental Studio",
        "See the Vance Dental Studio treatment suites and reception on Avenue of the Americas, New York.",
        "gallery.html",
    ) + header("gallery") + content + footer() + close_body()
    (ROOT / "gallery.html").write_text(html, encoding="utf-8")


def build_cases():
    blocks = []
    for c in CASES:
        blocks.append(f"""
        <article class="card mb-5" id="{c["id"]}">
          <div class="row between row-wrap gap-3 mb-4">
            <span class="badge badge-brass">{c["tag"]}</span>
            <span class="mono text-3">{c["duration"]}</span>
          </div>
          <h2 class="heading mb-3">{c["title"]}</h2>
          <p class="text-2 mb-4"><strong style="color:var(--text)">Brief.</strong> {c["summary"]}</p>
          <p class="text-2"><strong style="color:var(--text)">Result.</strong> {c["result"]}</p>
        </article>""")
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Cases")])
        + page_hero(
            "Case studies",
            "Documented treatment, plain results.",
            "Selected cases from the studio. Details focus on problem, plan, and outcome, not before/after theatrics.",
        )
        + f'<main id="main-content" class="section"><div class="container" style="max-width:800px">{"".join(blocks)}</div></main>'
    )
    html = head(
        "Case Studies | Vance Dental Studio",
        "Real treatment case studies from Vance Dental Studio: veneers, implants, and Invisalign outcomes.",
        "cases.html",
    ) + header("cases") + content + footer() + close_body()
    (ROOT / "cases.html").write_text(html, encoding="utf-8")


def build_about():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "About")])
        + page_hero(
            "About the studio",
            f"Dentistry with {DATA['doctor']}.",
            "A single Midtown practice built around careful diagnosis, honest sequencing, and materials chosen for how they age, not how they photograph on day one.",
        )
        + f"""
<main id="main-content">
  <section class="section">
    <div class="container md-grid-2 gap-5">
      <div class="stack stack-5">
        <p class="lead" style="max-width:none">Dr. Vance trained in restorative and implant dentistry with a focus on occlusion and esthetic integration. The studio keeps a deliberate schedule: fewer chairs, longer appointments, and written plans before irreversible steps.</p>
        <p class="text-2">We are not a multi-location brand. One address, one clinical standard, and a hygiene team that sees the same patients year after year. That continuity is the product.</p>
        <ul class="stack stack-3 small text-2" style="padding-left:1.1rem;list-style:disc">
          <li>Emphasis on conservative preparation and repairable dentistry</li>
          <li>Digital scanning and guided implant workflows when they improve accuracy</li>
          <li>Clear estimates, PPO out-of-network billing support, and financing partners</li>
        </ul>
        <p class="small text-3">Note: this site does not publish team photographs, per studio preference. Meet the clinical team in person at your first visit.</p>
      </div>
      <div class="card card-inset stack stack-5">
        <div>
          <p class="micro text-3 mb-2">Credentials at a glance</p>
          <p class="heading">DDS · Restorative focus</p>
        </div>
        <div>
          <p class="micro text-3 mb-2">Studio</p>
          <p class="small">{DATA["address_line1"]}<br>{DATA["address_line2"]}</p>
        </div>
        <div>
          <p class="micro text-3 mb-2">Response promise</p>
          <p class="small">Booking and clinical messages answered {DATA["response"]}.</p>
        </div>
        <a class="btn btn-primary" href="contact.html">Contact the studio</a>
      </div>
    </div>
  </section>
</main>"""
    )
    html = head(
        "About Dr. Alistair Vance | Vance Dental Studio",
        "Learn about Dr. Alistair Vance and the Midtown Manhattan precision dentistry studio on Avenue of the Americas.",
        "about.html",
    ) + header("about") + content + footer() + close_body()
    (ROOT / "about.html").write_text(html, encoding="utf-8")


def build_visit():
    hours_rows = ""
    for day, time in DATA["hours"]:
        cls = "closed" if time == "Closed" else "time"
        hours_rows += f'<span class="day">{day}</span><span class="{cls}">{time}</span>'
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Visit")])
        + page_hero(
            "Find us",
            "Visit the Midtown studio.",
            "Avenue of the Americas between 47th and 48th. Elevator to Suite 400.",
        )
        + f"""
<main id="main-content" class="section">
  <div class="container md-grid-2">
    <div class="stack stack-8">
      <div class="row gap-4 start">
        <div class="icon-wrap">{icon("mapPin", 20)}</div>
        <div>
          <h2 class="heading mb-2">Location</h2>
          <address class="small text-2">
            {DATA["address_line1"]}<br>{DATA["address_line2"]}
          </address>
          <a class="btn btn-link mt-3" href="https://www.google.com/maps/dir/?api=1&destination={DATA['lat']},{DATA['lng']}" target="_blank" rel="noopener noreferrer">
            Get directions {icon("external", 14)}
          </a>
          <button type="button" class="btn btn-secondary btn-sm mt-3" data-copy="{DATA['address_line1']}, {DATA['address_line2']}">Copy address</button>
        </div>
      </div>
      <div class="row gap-4 start" id="hours">
        <div class="icon-wrap">{icon("clock", 20)}</div>
        <div style="flex:1">
          <div class="row between mb-3">
            <h2 class="heading">Opening hours</h2>
            <span data-open-status class="badge badge-dot badge-success">Open now</span>
          </div>
          <div class="hours-grid">{hours_rows}</div>
        </div>
      </div>
      <div class="row gap-4 start">
        <div class="icon-wrap">{icon("phone", 20)}</div>
        <div>
          <h2 class="heading mb-2">Contact</h2>
          <p class="small"><a href="tel:{DATA['phone_tel']}">{DATA["phone"]}</a></p>
          <p class="small"><a href="mailto:{DATA['email']}">{DATA["email"]}</a></p>
        </div>
      </div>
      <button type="button" class="btn btn-primary btn-lg" data-book-open>{icon("calendar", 18)} Book an appointment</button>
    </div>
    <div>
      <div class="map-frame" role="application" aria-label="Map showing clinic location">
        <div id="map"></div>
      </div>
      <div class="card mt-4 row gap-3 start" style="padding:16px 20px">
        <span style="color:var(--brass)">{icon("car", 18)}</span>
        <p class="small text-2"><strong style="color:var(--text)">Parking.</strong> Validated parking for scheduled patients at the 43rd Street garage. Bring your ticket to reception.</p>
      </div>
    </div>
  </div>
</main>"""
    )
    html = head(
        "Visit Us | Vance Dental Studio",
        "Find Vance Dental Studio at 1200 Avenue of the Americas, Suite 400, New York. Hours, map, parking, and directions.",
        "visit.html",
        extra='<link rel="preconnect" href="https://basemaps.cartocdn.com">',
    ) + header("visit") + content + footer() + close_body()
    (ROOT / "visit.html").write_text(html, encoding="utf-8")


def build_patients():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Patients")])
        + page_hero(
            "For patients",
            "Forms, insurance, and visit prep.",
            "Complete paperwork before you arrive when you can. It keeps the clinical hour clinical.",
        )
        + f"""
<main id="main-content" class="section">
  <div class="container stack stack-6" style="max-width:800px">
    <article class="card" id="forms">
      <div class="icon-wrap mb-4">{icon("file", 20)}</div>
      <h2 class="heading mb-3">Patient forms</h2>
      <p class="text-2 mb-4">New patients receive a secure link after booking. If you prefer paper, arrive 15 minutes early. Bring photo ID, insurance card, and a medication list.</p>
      <ul class="small text-2 stack stack-2" style="padding-left:1.1rem;list-style:disc">
        <li>Medical & dental history</li>
        <li>HIPAA acknowledgment</li>
        <li>Financial policy summary</li>
      </ul>
    </article>
    <article class="card" id="insurance">
      <div class="icon-wrap mb-4">{icon("shield", 20)}</div>
      <h2 class="heading mb-3">Insurance</h2>
      <p class="text-2 mb-4">We are out-of-network with most PPO plans and submit claims for you. Before elective treatment you receive a written pre-estimate. HSA and FSA cards are accepted. Third-party financing is available for larger restorative plans.</p>
      <p class="small text-3">We do not promise that every plan covers every code. Benefits are verified; your plan booklet remains the authority.</p>
    </article>
    <article class="card">
      <div class="icon-wrap mb-4">{icon("heart", 20)}</div>
      <h2 class="heading mb-3">Comfort & accessibility</h2>
      <p class="text-2">Tell us about anxiety, jaw fatigue, or mobility needs when you book. We allocate time and the appropriate operatory rather than rushing adaptations mid-visit.</p>
    </article>
    <div class="card card-inset row-wrap between gap-4">
      <div>
        <h2 class="heading mb-2">Ready to schedule?</h2>
        <p class="small text-2">Response {DATA["response"]} on booking requests.</p>
      </div>
      <button type="button" class="btn btn-primary" data-book-open>Book appointment</button>
    </div>
  </div>
</main>"""
    )
    html = head(
        "Patient Information | Vance Dental Studio",
        "Patient forms, insurance, financing, and visit preparation for Vance Dental Studio in New York.",
        "patients.html",
    ) + header("patients") + content + footer() + close_body()
    (ROOT / "patients.html").write_text(html, encoding="utf-8")


def build_contact():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Contact")])
        + page_hero(
            "Contact",
            "Write the studio.",
            f"We respond to clinical and scheduling messages {DATA['response']}. For pain after hours, call the number on your post-op sheet.",
        )
        + f"""
<main id="main-content" class="section">
  <div class="container md-grid-2">
    <form class="card stack stack-4" name="contact" method="POST" action="/thank-you.html" netlify netlify-honeypot="bot-field" data-contact-form>
      <input type="hidden" name="form-name" value="contact">
      <p class="sr-only" aria-hidden="true">
        <label>Don’t fill this out: <input name="bot-field" tabindex="-1" autocomplete="off"></label>
      </p>
      <div class="field">
        <label class="field-label" for="c-name">Full name</label>
        <input class="input" id="c-name" name="name" required autocomplete="name" placeholder="Jordan Lee">
        <p class="field-error">Enter your name.</p>
      </div>
      <div class="field">
        <label class="field-label" for="c-email">Email</label>
        <input class="input" id="c-email" name="email" type="email" required autocomplete="email" placeholder="you@email.com" spellcheck="false">
        <p class="field-error">Enter a valid email.</p>
      </div>
      <div class="field">
        <label class="field-label" for="c-phone">Phone</label>
        <input class="input" id="c-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+1 (212) 555-0142">
      </div>
      <div class="field">
        <label class="field-label" for="c-topic">Topic</label>
        <select class="select" id="c-topic" name="topic" required>
          <option value="" disabled selected>Select…</option>
          <option>New patient exam</option>
          <option>Existing patient</option>
          <option>Insurance question</option>
          <option>Something else</option>
        </select>
        <p class="field-error">Choose a topic.</p>
      </div>
      <div class="field">
        <label class="field-label" for="c-msg">Message</label>
        <textarea class="textarea" id="c-msg" name="message" required placeholder="How can we help?"></textarea>
        <p class="field-error">Enter a short message.</p>
      </div>
      <button type="submit" class="btn btn-primary btn-lg">Send message</button>
      <p class="micro text-3">Or book directly, <button type="button" class="btn-link" style="display:inline;min-height:auto;padding:0" data-book-open>open the appointment form</button>.</p>
    </form>
    <div class="stack stack-5">
      <div class="card card-inset">
        <h2 class="heading mb-4">Direct lines</h2>
        <p class="small mb-3"><a href="tel:{DATA['phone_tel']}">{icon("phone", 16)} {DATA["phone"]}</a></p>
        <p class="small mb-3"><a href="mailto:{DATA['email']}">{icon("mail", 16)} {DATA["email"]}</a></p>
        <p class="small text-2">{DATA["address_line1"]}<br>{DATA["address_line2"]}</p>
      </div>
      <div class="card">
        <h2 class="heading mb-3">Response promise</h2>
        <p class="small text-2">Messages received on business days are answered {DATA["response"]}. Weekend notes are triaged Monday morning unless marked urgent.</p>
      </div>
    </div>
  </div>
</main>
<script>
document.addEventListener('DOMContentLoaded',()=>{{
  const form=document.querySelector('[data-contact-form]');
  form?.addEventListener('submit',async(e)=>{{
    e.preventDefault();
    let valid=true;
    form.querySelectorAll('[required]').forEach((field)=>{{
      const wrap=field.closest('.field');
      const ok=field.value && field.checkValidity();
      wrap?.classList.toggle('has-error', !ok);
      field.classList.toggle('is-error', !ok);
      if(!ok) valid=false;
    }});
    if(!valid){{
      form.querySelector('.is-error')?.focus();
      window.vdToast?.('Please correct the highlighted fields.');
      return;
    }}
    const btn=form.querySelector('[type=submit]');
    const original=btn.innerHTML;
    btn.classList.add('is-loading');
    btn.innerHTML='<span class="spinner" aria-hidden="true"></span> Sending…';
    // Netlify Forms: POST when hosted; locally simulate success
    const hosted = location.hostname.endsWith('netlify.app') || location.hostname.endsWith('vancedental.com');
    try {{
      if (hosted) {{
        const fd = new FormData(form);
        await fetch('/', {{ method:'POST', headers:{{'Content-Type':'application/x-www-form-urlencoded'}}, body: new URLSearchParams(fd).toString() }});
      }} else {{
        await new Promise(r=>setTimeout(r, 700));
      }}
      window.location.href = 'thank-you.html';
    }} catch (err) {{
      btn.classList.remove('is-loading');
      btn.innerHTML = original;
      window.vdToast?.('Could not send. Email hello@vancedental.com or try again.');
    }}
  }});
}});
</script>
"""
    )
    html = head(
        "Contact | Vance Dental Studio",
        "Contact Vance Dental Studio in Midtown Manhattan. Book a visit or send a message, we respond within 24 hours.",
        "contact.html",
    ) + header("contact") + content + footer() + close_body()
    (ROOT / "contact.html").write_text(html, encoding="utf-8")


def build_thank_you():
    content = f"""
<main id="main-content" class="section" style="min-height:60vh;display:grid;align-items:center">
  <div class="container" style="max-width:560px;text-align:center">
    <div class="icon-wrap" style="margin:0 auto 24px;width:56px;height:56px">{icon("check", 24)}</div>
    <h1 class="title mb-4">Message received.</h1>
    <p class="lead" style="margin-inline:auto">Thank you. A member of the studio will reply {DATA["response"]}. If your matter is urgent, call <a href="tel:{DATA['phone_tel']}" style="color:var(--brass)">{DATA["phone"]}</a>.</p>
    <div class="row-wrap gap-3 center mt-8">
      <a class="btn btn-primary" href="index.html">Back to home</a>
      <a class="btn btn-secondary" href="visit.html">Studio directions</a>
    </div>
  </div>
</main>
"""
    html = head(
        "Thank You | Vance Dental Studio",
        "Your message was received by Vance Dental Studio. We respond within 24 hours.",
        "thank-you.html",
    ) + header("contact") + content + footer() + close_body()
    (ROOT / "thank-you.html").write_text(html, encoding="utf-8")


def build_search():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Search")])
        + page_hero(
            "Search",
            "Find a service, policy, or visit detail.",
            "Type a keyword such as implants, hours, insurance, or parking.",
        )
        + """
<main id="main-content" class="section">
  <div class="container" style="max-width:720px">
    <div class="search-shell">
      <span class="search-icon" data-icon="search" data-size="18"></span>
      <label for="site-search" class="sr-only">Search the site</label>
      <input class="input" id="site-search" data-site-search type="search" placeholder="Search services, visit info, policies…" autocomplete="off" enterkeyhint="search">
    </div>
    <div class="search-results" data-search-results></div>
  </div>
</main>
"""
    )
    html = head(
        "Search | Vance Dental Studio",
        "Search Vance Dental Studio services, patient information, and visit details.",
        "search.html",
    ) + header("home") + content + footer() + close_body()
    (ROOT / "search.html").write_text(html, encoding="utf-8")


def build_privacy():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Privacy Policy")])
        + page_hero("Legal", "Privacy Policy", "How Vance Dental Studio collects, uses, and protects personal information.")
        + f"""
<main id="main-content" class="section">
  <div class="container legal">
    <p class="updated">Last updated: March 1, 2026</p>
    <p>Vance Dental Studio (“we”, “us”) operates the website at vancedental.com and the clinical practice at {DATA["address_line1"]}, {DATA["address_line2"]}. This policy describes how we handle personal information collected online and offline.</p>
    <h2>Information we collect</h2>
    <p>We collect information you submit through booking and contact forms (name, email, phone, message content), appointment records, insurance details necessary for billing, and technical data such as IP address, browser type, and pages viewed when analytics are enabled.</p>
    <h2>How we use information</h2>
    <ul>
      <li>To schedule and provide dental care</li>
      <li>To respond to inquiries within our stated response window</li>
      <li>To process insurance claims and payments</li>
      <li>To improve site performance and security</li>
      <li>To send newsletters only when you opt in</li>
    </ul>
    <h2>Sharing</h2>
    <p>We do not sell personal information. We share data with laboratories, imaging partners, insurers, and payment processors only as needed to deliver care or as required by law. Protected health information is handled under applicable HIPAA requirements.</p>
    <h2>Cookies</h2>
    <p>Essential cookies keep the site functional (for example, theme preference). Optional analytics cookies run only after you accept the cookie banner. You may reject non-essential cookies without losing access to clinical information pages.</p>
    <h2>Retention</h2>
    <p>Clinical records are retained according to New York State requirements. Marketing emails are kept until you unsubscribe. Web server logs are rotated on a limited schedule.</p>
    <h2>Your choices</h2>
    <p>Email {DATA["email"]} to request access, correction, or deletion of personal information we hold, subject to legal retention duties for clinical records.</p>
    <h2>Contact</h2>
    <p>Privacy questions: <a href="mailto:{DATA['email']}">{DATA["email"]}</a> · <a href="tel:{DATA['phone_tel']}">{DATA["phone"]}</a></p>
  </div>
</main>
"""
    )
    html = head(
        "Privacy Policy | Vance Dental Studio",
        "Privacy Policy for Vance Dental Studio, how we collect, use, and protect patient and website visitor information.",
        "privacy.html",
    ) + header("home") + content + footer() + close_body()
    (ROOT / "privacy.html").write_text(html, encoding="utf-8")


def build_terms():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Terms of Service")])
        + page_hero("Legal", "Terms of Service", "Terms that govern use of this website and communications with the studio.")
        + f"""
<main id="main-content" class="section">
  <div class="container legal">
    <p class="updated">Last updated: March 1, 2026</p>
    <p>By using vancedental.com you agree to these terms. Clinical care is governed by separate informed-consent documents signed at the practice.</p>
    <h2>Website use</h2>
    <p>Content on this site is for general information. It is not a diagnosis or a treatment recommendation. Emergency dental issues require direct clinical contact or urgent care.</p>
    <h2>Appointments</h2>
    <p>Online booking requests are not confirmed until the studio replies. We may reschedule when clinical urgency requires it. Repeated no-shows may require a deposit for future holds.</p>
    <h2>Intellectual property</h2>
    <p>Text, brand marks, and site design are owned by Vance Dental Studio unless otherwise noted. You may not copy them for commercial use without written permission.</p>
    <h2>Limitation</h2>
    <p>To the fullest extent permitted by law, Vance Dental Studio is not liable for damages arising from use of this website or reliance on its general content.</p>
    <h2>Contact</h2>
    <p><a href="mailto:{DATA['email']}">{DATA["email"]}</a> · {DATA["address_line1"]}, {DATA["address_line2"]}</p>
  </div>
</main>
"""
    )
    html = head(
        "Terms of Service | Vance Dental Studio",
        "Terms of Service for the Vance Dental Studio website and patient communications.",
        "terms.html",
    ) + header("home") + content + footer() + close_body()
    (ROOT / "terms.html").write_text(html, encoding="utf-8")


def build_404():
    content = f"""
<main id="main-content" class="not-found">
  <div>
    <p class="code" aria-hidden="true">404</p>
    <h1 class="title mt-4">This page left the building.</h1>
    <p class="lead mt-4" style="margin-inline:auto">The link may be outdated or typed incorrectly. Try search, or return home.</p>
    <div class="row-wrap gap-3 center mt-8">
      <a class="btn btn-primary" href="index.html">Home</a>
      <a class="btn btn-secondary" href="search.html">Search</a>
      <a class="btn btn-ghost" href="contact.html">Contact</a>
    </div>
  </div>
</main>
"""
    # Netlify uses 404.html
    html = head(
        "Page not found | Vance Dental Studio",
        "The page you requested could not be found on Vance Dental Studio.",
        "404.html",
    ) + header("home") + content + footer() + close_body()
    (ROOT / "404.html").write_text(html, encoding="utf-8")


def build_misc():
    (ROOT / "robots.txt").write_text(
        """User-agent: *
Allow: /

Sitemap: https://vancedental.com/sitemap.xml
""",
        encoding="utf-8",
    )

    pages = [
        ("", "weekly", "1.0"),
        ("services.html", "monthly", "0.9"),
        ("gallery.html", "monthly", "0.7"),
        ("cases.html", "monthly", "0.8"),
        ("about.html", "yearly", "0.6"),
        ("visit.html", "monthly", "0.9"),
        ("patients.html", "monthly", "0.7"),
        ("contact.html", "monthly", "0.8"),
        ("search.html", "yearly", "0.3"),
        ("privacy.html", "yearly", "0.3"),
        ("terms.html", "yearly", "0.3"),
        ("thank-you.html", "yearly", "0.2"),
    ]
    urls = []
    for path, freq, pri in pages:
        loc = f"https://vancedental.com/{path}" if path else "https://vancedental.com/"
        urls.append(f"""  <url>
    <loc>{loc}</loc>
    <changefreq>{freq}</changefreq>
    <priority>{pri}</priority>
  </url>""")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )

    (ROOT / "llms.txt").write_text(
        f"""# Vance Dental Studio

> Precision dentistry studio in Midtown Manhattan led by {DATA["doctor"]}.

## Site
- Home: https://vancedental.com/
- Services: https://vancedental.com/services.html
- Case studies: https://vancedental.com/cases.html
- Visit / map: https://vancedental.com/visit.html
- Contact: https://vancedental.com/contact.html
- Privacy: https://vancedental.com/privacy.html

## Facts
- Address: {DATA["address_line1"]}, {DATA["address_line2"]}
- Phone: {DATA["phone"]}
- Email: {DATA["email"]}
- Hours: Mon–Fri 08:00–19:00; Sat 09:00–16:00; Sun closed
- Services: Cosmetic dentistry, dental implants, Invisalign, general checkup
""",
        encoding="utf-8",
    )

    (ROOT / "_headers").write_text(
        """/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; img-src 'self' https://images.unsplash.com https://*.basemaps.cartocdn.com https://*.tile.openstreetmap.org data: blob:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com; font-src https://fonts.gstatic.com data:; script-src 'self' https://unpkg.com 'unsafe-inline'; connect-src 'self' https://*.basemaps.cartocdn.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

/css/*
  Cache-Control: public, max-age=31536000, immutable
/js/*
  Cache-Control: public, max-age=31536000, immutable
/icons/*
  Cache-Control: public, max-age=31536000, immutable
/*.svg
  Cache-Control: public, max-age=604800
/*.png
  Cache-Control: public, max-age=604800
""",
        encoding="utf-8",
    )

    (ROOT / "_redirects").write_text(
        """# Netlify redirects
/home /index.html 301
/Index.html /index.html 301
/* /404.html 404
""",
        encoding="utf-8",
    )

    (ROOT / "netlify.toml").write_text(
        """[build]
  publish = "."
  command = "echo 'Static site, no build step'"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

# Forms
[build.processing]
  skip_processing = false
""",
        encoding="utf-8",
    )

    # OG image as SVG (no binary dependency)
    (ROOT / "og-image.svg").write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#F3F0EA"/>
  <rect x="0" y="0" width="1200" height="8" fill="#A67C52"/>
  <rect x="80" y="160" width="56" height="56" rx="10" fill="#A67C52"/>
  <text x="152" y="198" font-family="Georgia, serif" font-size="28" fill="#1C1915">VANCE DENTAL</text>
  <text x="80" y="320" font-family="Georgia, serif" font-size="64" fill="#1C1915">Modern precision</text>
  <text x="80" y="400" font-family="Georgia, serif" font-size="64" fill="#A67C52">dentistry.</text>
  <text x="80" y="480" font-family="system-ui, sans-serif" font-size="24" fill="#5A554C">{DATA["address_line1"]}, New York</text>
  <text x="80" y="560" font-family="system-ui, sans-serif" font-size="20" fill="#8A847A">{DATA["phone"]}  ·  {DATA["email"]}</text>
</svg>
""",
        encoding="utf-8",
    )

    (ROOT / "README.md").write_text(
        """# Vance Dental Studio

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
""",
        encoding="utf-8",
    )


def main():
    build_index()
    build_services()
    build_gallery()
    build_cases()
    build_about()
    build_visit()
    build_patients()
    build_contact()
    build_thank_you()
    build_search()
    build_privacy()
    build_terms()
    build_404()
    build_misc()
    print("Generated all pages.")


if __name__ == "__main__":
    main()
