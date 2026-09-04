#!/usr/bin/env python3
"""Generate all Vance Dental Studio static pages for Netlify."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ─── Canonical host ───
# Every absolute URL this generator emits (canonical, og:url, twitter:image,
# JSON-LD, sitemap.xml, robots.txt, llms.txt) is built from SITE_URL, so the
# host in the markup always matches the host the site is actually served from.
# When the studio moves to its own domain, change this one line and re-run
# `python3 build_pages.py`.
SITE_URL = "https://vance-dental.netlify.app"


def abs_url(path=""):
    """Absolute URL on the canonical host. Empty path returns the site root."""
    return f"{SITE_URL}/{path}" if path else f"{SITE_URL}/"


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
        "title": "Cosmetic dentistry",
        "icon": "heart",
        "blurb": "Veneers, bonding and whitening, planned against the shade of your own enamel.",
        "body": "Cosmetic work starts with photographs and a shade map of the teeth next to the one being restored. Where the change is large enough to be worth previewing, we make a mock-up you can look at in the chair first. Preparation stays inside enamel wherever the case allows it, and the laboratory we use is asked to match translucency at the incisal edge instead of one flat shade across the tooth.",
        "points": ["Porcelain veneers and bonding", "In-office and take-home whitening", "Mock-up before any tooth is prepared"],
    },
    {
        "id": "implants",
        "title": "Dental implants",
        "icon": "layers",
        "blurb": "Implants planned on a CBCT scan and placed through a printed surgical guide.",
        "body": "Implant cases are planned on a CBCT scan. Where bone sits close to a nerve or a sinus, the plan is transferred to the mouth through a printed guide. We place single teeth and full arches. Crowns are screw-retained when the bite allows it, so the restoration can be taken off for cleaning instead of being cut apart.",
        "points": ["CBCT scan and printed surgical guide", "Single tooth to full arch", "Screw-retained crowns where the bite allows"],
        "dark": True,
    },
    {
        "id": "invisalign",
        "title": "Invisalign®",
        "icon": "scan",
        "blurb": "Clear aligners with the movement staged on a scan and one refinement phase included.",
        "body": "We take an intraoral scan instead of a putty impression, then go through the staged movement with you before you order trays. Attachments and elastics are added where the plan needs them. Check-ups run every six to eight weeks, and the fee includes one refinement phase after the first set of trays.",
        "points": ["Intraoral scan instead of putty impressions", "Full-time wear, 20 to 22 hours a day", "One refinement phase included in the fee"],
    },
    {
        "id": "checkup",
        "title": "General checkup",
        "icon": "shield",
        "blurb": "Exams and cleanings, with X-rays only when a finding calls for them.",
        "body": "A hygiene visit here includes periodontal charting at every appointment. X-rays are taken when there is a finding to follow, so there is no fixed radiography schedule. The cleaning interval is set from what we see at that visit. Decay caught while it is still in enamel is a small filling; the same lesion two years later is usually a crown.",
        "points": ["Periodontal charting at every visit", "Cleaning interval set from findings"],
    },
]

# Patient feedback, reproduced with first name + last initial and borough.
# Source and date are stated on the page so the quotes are checkable.
REVIEWS = [
    {
        "name": "Marisa K.",
        "meta": "Upper West Side · Veneers",
        "when": "March 2026",
        "quote": "I came in with two chipped front teeth after a bike fall. Six months on, my hygienist had to check the chart to see which two had been bonded.",
        "stars": 5,
    },
    {
        "name": "James O.",
        "meta": "Financial District · Implant",
        "when": "January 2026",
        "quote": "The implant consult came with a written fee range before any surgery date was set. Placement day was shorter than I expected and I was back at work the next morning.",
        "stars": 5,
    },
    {
        "name": "Priya S.",
        "meta": "Brooklyn · Invisalign",
        "when": "November 2025",
        "quote": "Aligner check-ins took twenty minutes and always showed the next three stages on screen. I finished two weeks ahead of the original estimate.",
        "stars": 5,
    },
]

CASES = [
    {
        "id": "veneer-harmony",
        "title": "Four upper veneers after grinding wear",
        "tag": "Cosmetic",
        "summary": "Years of night grinding had worn the upper front teeth to uneven lengths. Four veneers were placed after a mock-up was approved in the chair.",
        "result": "Central incisors back to equal length and canine guidance restored. The shade was matched to the neighboring teeth under the operatory light and checked again at the six-week review.",
        "duration": "3 visits · 5 weeks",
    },
    {
        "id": "single-implant",
        "title": "Guided implant for a lower first molar",
        "tag": "Implants",
        "summary": "A lower first molar with a failed root canal was extracted and grafted, then replaced with an implant placed through a printed guide.",
        "result": "Stable bone levels at 12-month review; patient returned to normal chewing on that side within six weeks of final crown.",
        "duration": "Surgery + crown · 4 months",
    },
    {
        "id": "align-crowding",
        "title": "Clear aligners for adult crowding",
        "tag": "Invisalign",
        "summary": "Moderate lower crowding with a deep bite, treated with aligners and interproximal reduction between the lower front teeth.",
        "result": "The lower arch aligned without extractions. Retention is a bonded wire behind the lower front teeth plus a night aligner.",
        "duration": "11 months · 28 trays",
    },
]

FAQS = [
    ("How soon can I be seen?",
     "If you are in pain we will usually see you the same day, as long as the schedule has room. New-patient exams are generally booked 7 to 10 days out. Every booking request gets a reply within 24 hours."),
    ("Do you accept my insurance?",
     "We are out-of-network with most PPO plans and file the claim for you. Before treatment starts you get a written estimate that separates what the plan is expected to pay from what you owe."),
    ("Is the studio accessible?",
     "Suite 400 is reached by elevator from the Avenue of the Americas lobby, and the operatory door is 36 inches clear. Tell us about mobility needs when you book so we can put you in the right room and leave extra time."),
    ("What should I bring to my first visit?",
     "Photo ID, your insurance card if you have one, a list of medications. Bring any recent X-rays too, on disc or through a portal link. New-patient forms can be filled in ahead of time from the Patients page."),
    ("How do you handle comfort and anxiety?",
     "We describe each step before we start, and you can ask for a break at any point. Nitrous or oral sedation can be arranged when it is clinically appropriate."),
    ("Where do I park?",
     "Scheduled patients can have their ticket validated at the 43rd Street garage. The nearest subway stops are Bryant Park / 42 St and 47-50 St Rockefeller Center."),
]

GALLERY = [
    ("https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&q=80&w=1200",
     "Treatment suite with natural light and calibrated operatory lighting"),
    ("https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&q=80&w=1000",
     "Operatory set up for a restorative appointment"),
    ("https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&q=80&w=800",
     "Reception lounge with quiet seating and material samples"),
    ("https://images.unsplash.com/photo-1597764690523-15bea4c581c9?auto=format&fit=crop&q=80&w=800",
     "Consultation desk with digital scan display"),
    ("https://images.unsplash.com/photo-1606811971618-4486d14f3f99?auto=format&fit=crop&q=80&w=1000",
     "Corridor view toward private operatories"),
    ("https://images.unsplash.com/photo-1629909615184-74f495363b67?auto=format&fit=crop&q=80&w=800",
     "Sterilization room"),
]

# No stock headshots in the hero. The studio does not publish patient or team
# photographs, so the home page carries practice facts instead of avatars.


def icon(name, size=20):
    return f'<span data-icon="{name}" data-size="{size}" aria-hidden="true"></span>'


def stars(n=5):
    return '<span class="stars" role="img" aria-label="{} out of 5 stars">{}</span>'.format(
        n, "".join(icon("star", 14) for _ in range(n))
    )


def head(title, description, path, canonical=None, og_type="website", extra=""):
    can = canonical if canonical is not None else path
    if can == "index.html":
        can = ""  # home page canonicalises to the bare origin, no filename
    canonical_url = abs_url(can)
    og_image = abs_url("og-image.svg")
    return f"""<!DOCTYPE html>
<html lang="en" class="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#F3F0EA">
  <meta name="color-scheme" content="light dark">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Vance Dental Studio">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{og_image}">
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
        <p class="small text-2 mt-2">We reply to every request {DATA["response"]}.</p>
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
        <p class="small mt-5" style="color:var(--footer-muted);max-width:34ch;line-height:1.7">
          One dentist, one address. {DATA["doctor"]} examines every patient and writes every treatment plan himself.
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
        <p class="small" style="color:var(--footer-muted);margin-bottom:12px">About one email a month: opening changes and the occasional note on oral health.</p>
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
      <p>&copy; <span data-year>2026</span> Vance Dental Studio</p>
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
  <p>This site stores your theme choice in a cookie. Analytics only load if you accept them. <a href="privacy.html" style="color:var(--brass)">Privacy Policy</a></p>
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


def page_hero(label, title, intro):
    """Page header. `label` is a short section marker, `intro` one or two plain
    sentences. Class names are structural, not marketing vocabulary."""
    return f"""
<section class="page-hero">
  <div class="container">
    <p class="section-label">{label}</p>
    <h1>{title}</h1>
    <p class="intro mt-4">{intro}</p>
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
  "image": "{abs_url("og-image.svg")}",
  "url": "{abs_url()}",
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
  "founder": {{
    "@type": "Person",
    "name": "Dr. Alistair Vance",
    "jobTitle": "Dentist"
  }}
}}
</script>
"""


def faq_schema():
    """FAQPage structured data. Serialised with json.dumps so the block is
    valid JSON; Python repr() emits single quotes, which JSON rejects."""
    entities = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in FAQS
    ]
    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(payload, ensure_ascii=False)
        + "</script>"
    )


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
          <blockquote class="quote">"{r["quote"]}"</blockquote>
          <figcaption class="small"><strong>{r["name"]}</strong><span class="text-3"> · {r["meta"]} · {r["when"]}</span></figcaption>
        </figure>""")

    faq_html = []
    for i, (q, a) in enumerate(FAQS[:5]):
        faq_html.append(f"""
        <details class="faq-item">
          <summary class="faq-trigger">{q}<span class="faq-icon">{icon("plus", 16)}</span></summary>
          <div class="faq-panel">{a}</div>
        </details>""")

    content = f"""
<main id="main-content">
  <section class="hero" id="home">
    <div class="container hero-panel">
      <div>
        <p class="section-label">Suite 400, 1200 Avenue of the Americas</p>
        <h1>A <span class="accent">dentist</span> who books longer appointments</h1>
        <p class="intro mt-5">
          {DATA["doctor"]} runs a single practice in Midtown Manhattan. New patients get a 60-minute first appointment. Every treatment plan is written out before anything is scheduled, down to the materials, how many visits it takes and what it costs.
        </p>
        <div class="hero-actions">
          <button type="button" class="btn btn-primary btn-lg" data-book-open>{icon("calendar", 18)} Schedule visit</button>
          <a class="btn btn-secondary btn-lg" href="gallery.html">View gallery {icon("arrowRight", 18)}</a>
        </div>
        <div class="hero-proof">
          <div>
            <p class="small" style="font-weight:600">Taking new patients</p>
            <p class="micro text-3 mt-2">New-patient exams are usually booked 7 to 10 days out · replies {DATA["response"]}</p>
          </div>
        </div>
      </div>
      <div style="position:relative">
        <div class="media media-wide">
          <img src="https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&q=80&w=1000"
               width="800" height="600"
               alt="A treatment room at the studio: chair, overhead light and a window facing Avenue of the Americas"
               fetchpriority="high">
        </div>
        <div class="float-card">
          <div class="icon-wrap" style="width:40px;height:40px">{icon("clock", 16)}</div>
          <div>
            <p class="small" style="font-weight:600">60-minute first visit</p>
            <p class="micro text-3">One dentist, one address</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section-tight">
    <div class="container">
      <div class="stat-strip" aria-label="Practice facts">
        <div class="stat-item"><strong class="tabular">18</strong><span>Years Dr. Vance has practiced</span></div>
        <div class="stat-item"><strong class="tabular">60</strong><span>Minutes booked for your first appointment</span></div>
        <div class="stat-item"><strong class="tabular">24h</strong><span>To reply to a booking request</span></div>
        <div class="stat-item"><strong class="tabular">4</strong><span>Services offered</span></div>
      </div>
    </div>
  </section>

  <section class="section" id="services" aria-labelledby="services-heading">
    <div class="container">
      <p class="section-label">Services</p>
      <div class="md-grid-2 mb-8">
        <h2 id="services-heading" class="title">Four services, each with the fee written down before treatment</h2>
        <p class="intro">Each plan lists the materials, how many visits the work needs and what it will cost. You take it home and read it before anything is booked.</p>
      </div>
      <div class="grid-3">{''.join(service_cards)}</div>
      <div class="mt-6"><a class="btn btn-secondary" href="services.html">All services {icon("arrowRight", 16)}</a></div>
    </div>
  </section>

  <section class="section section-band" id="approach" aria-labelledby="approach-heading">
    <div class="container">
      <p class="section-label">Treatment sequence</p>
      <h2 id="approach-heading" class="title mb-8">How an appointment runs</h2>
      <div class="steps">
        <div class="step">
          <h3 class="heading mb-3">The first hour</h3>
          <p class="small text-2">Medical and dental history, photographs of every surface, X-rays where a finding needs following up, and time at the end to ask questions. Dr. Vance describes what he sees while you are still in the chair.</p>
        </div>
        <div class="step">
          <h3 class="heading mb-3">A written plan you keep</h3>
          <p class="small text-2">Options are listed in order of how long each one lasts and how much tooth structure it costs you. Nothing is booked until you have chosen a sequence and agreed the fee.</p>
        </div>
        <div class="step">
          <h3 class="heading mb-3">Treatment and follow-up</h3>
          <p class="small text-2">Appointments are booked long enough to finish the work in one sitting where that is safe. Review intervals depend on what was done: six months for a filling, twelve for a crown.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="cases-preview" aria-labelledby="cases-heading">
    <div class="container">
      <div class="row between row-wrap gap-4 mb-8">
        <div>
          <p class="section-label">Cases</p>
          <h2 id="cases-heading" class="title">Three recent treatments, written up</h2>
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
      <p class="section-label">Patient feedback</p>
      <h2 id="reviews-heading" class="title mb-4">What three patients said afterwards</h2>
      <p class="intro mb-8">Collected from written reviews left after treatment. Names appear as the reviewer wrote them, with the month of the visit.</p>
      <div class="grid-3">{''.join(review_cards)}</div>
    </div>
  </section>

  <section class="section" id="faq" aria-labelledby="faq-heading" data-faq>
    <div class="container" style="max-width:800px">
      <p class="section-label">Before you book</p>
      <h2 id="faq-heading" class="title mb-6">Questions asked most often before a first appointment</h2>
      {''.join(faq_html)}
      <p class="small text-2 mt-6">If your question is not here, <a href="contact.html" style="color:var(--brass);font-weight:600">send it to the studio</a>. We answer {DATA["response"]}.</p>
    </div>
  </section>

  <section class="section section-dark" aria-labelledby="cta-heading">
    <div class="container" style="text-align:center;max-width:640px">
      <p class="section-label" style="justify-content:center">Booking</p>
      <h2 id="cta-heading" class="title mb-4">Book an appointment</h2>
      <p class="intro mb-6" style="margin-inline:auto">Tell us what is bothering you and we will find a slot. Requests get a reply {DATA["response"]}. You can also call <a href="tel:{DATA["phone_tel"]}" style="color:var(--brass)">{DATA["phone"]}</a>.</p>
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
            "Vance Dental Studio: Dr. Alistair Vance, dentist in Midtown Manhattan",
            "Dental practice at 1200 Avenue of the Americas, Suite 400, New York. The studio places implants, fits Invisalign and does veneer and hygiene work. Open Monday to Friday 08:00-19:00, Saturday 09:00-16:00.",
            "index.html",
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
          <button type="button" class="btn btn-primary mt-6" data-book-open>Ask about this service</button>
        </article>""")
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Services")])
        + page_hero(
            "Services",
            "What we treat",
            "Four services. Every written plan names the materials, how many visits the work takes and what it costs, before any of it is booked.",
        )
        + f'<main id="main-content" class="section"><div class="container">{"".join(blocks)}</div></main>'
    )
    html = head(
        "Services | Vance Dental Studio",
        "Veneers, implants, Invisalign and hygiene visits at Vance Dental Studio, 1200 Avenue of the Americas, New York.",
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
            "Photographs of the studio",
            "The rooms at 1200 Avenue of the Americas, fourth floor. There is no television in the waiting room and the operatory lights are on dimmers.",
        )
        + f"""
<main id="main-content" class="section section-band">
  <div class="container">
    <div class="mosaic">{''.join(items)}</div>
    <p class="small text-2 mt-6">These photographs show the rooms. The studio does not publish portraits of staff or patients.</p>
  </div>
</main>"""
    )
    html = head(
        "Gallery | Vance Dental Studio",
        "Photographs of the treatment rooms, waiting room and sterilization area at Vance Dental Studio on Avenue of the Americas, New York.",
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
          <p class="text-2 mb-4"><strong style="color:var(--text)">Problem.</strong> {c["summary"]}</p>
          <p class="text-2"><strong style="color:var(--text)">Outcome.</strong> {c["result"]}</p>
        </article>""")
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Cases")])
        + page_hero(
            "Cases",
            "Three treatments, written up",
            "Each record below sets out the problem and the treatment, then what the review appointment found and how long it all took. Clinical photographs are not published here; ask to see them at a consultation.",
        )
        + f'<main id="main-content" class="section"><div class="container" style="max-width:800px">{"".join(blocks)}</div></main>'
    )
    html = head(
        "Case Studies | Vance Dental Studio",
        "Three write-ups from Vance Dental Studio: upper veneers after grinding wear, a guided lower molar implant, and clear aligners for adult crowding.",
        "cases.html",
    ) + header("cases") + content + footer() + close_body()
    (ROOT / "cases.html").write_text(html, encoding="utf-8")


def build_about():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "About")])
        + page_hero(
            "About",
            f"{DATA['doctor']}, DDS",
            "A one-address practice in Midtown Manhattan. Appointments are kept long enough to finish the work properly, and materials are picked for how they hold up five years out.",
        )
        + f"""
<main id="main-content">
  <section class="section">
    <div class="container md-grid-2 gap-5">
      <div class="stack stack-5">
        <p class="intro" style="max-width:none">Dr. Vance trained in restorative dentistry and implant placement, with a focus on occlusion. He has been practicing for 18 years. The diary is deliberately thin: an hour for a first appointment, and a written plan before anything irreversible happens.</p>
        <p class="text-2">There is one address and no second location. The hygiene team sees the same patients year after year, so the person charting your pockets has read last year's notes.</p>
        <ul class="stack stack-3 small text-2" style="padding-left:1.1rem;list-style:disc">
          <li>Preparation kept inside enamel wherever the case allows, and existing restorations repaired where they can be</li>
          <li>Digital scanning and printed guides for implant cases where they improve accuracy</li>
          <li>Written estimates, out-of-network PPO claims filed by the office</li>
          <li>Third-party financing available for larger restorative plans</li>
        </ul>
        <p class="small text-3">This site carries no team photographs. That is the studio's preference, so you will meet everyone at your first visit.</p>
      </div>
      <div class="card card-inset stack stack-5">
        <div>
          <p class="micro text-3 mb-2">Qualification</p>
          <p class="heading">DDS, restorative and implant dentistry</p>
        </div>
        <div>
          <p class="micro text-3 mb-2">Studio</p>
          <p class="small">{DATA["address_line1"]}<br>{DATA["address_line2"]}</p>
        </div>
        <div>
          <p class="micro text-3 mb-2">Replies</p>
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
        "Dr. Alistair Vance, DDS, has practiced restorative and implant dentistry for 18 years at Vance Dental Studio, Suite 400, 1200 Avenue of the Americas, New York.",
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
            "Location and hours",
            "Getting to the studio",
            "1200 Avenue of the Americas, on the block between 47th and 48th Street. Elevator from the lobby to Suite 400.",
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
        <p class="small text-2"><strong style="color:var(--text)">Parking.</strong> The 43rd Street garage validates tickets for patients with a booked appointment. Bring the ticket to reception before you leave.</p>
      </div>
    </div>
  </div>
</main>"""
    )
    html = head(
        "Visit Us | Vance Dental Studio",
        "Vance Dental Studio is at 1200 Avenue of the Americas, Suite 400, New York, NY 10036. Opening hours, map, parking and the nearest subway stops.",
        "visit.html",
        extra='<link rel="preconnect" href="https://basemaps.cartocdn.com">',
    ) + header("visit") + content + footer() + close_body()
    (ROOT / "visit.html").write_text(html, encoding="utf-8")


def build_patients():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Patients")])
        + page_hero(
            "For patients",
            "Paperwork and insurance",
            "Filling in the paperwork before you arrive leaves the appointment itself for the examination.",
        )
        + f"""
<main id="main-content" class="section">
  <div class="container stack stack-6" style="max-width:800px">
    <article class="card" id="forms">
      <div class="icon-wrap mb-4">{icon("file", 20)}</div>
      <h2 class="heading mb-3">Patient forms</h2>
      <p class="text-2 mb-4">New patients get a secure link by email after booking. If you prefer paper, arrive 15 minutes early and fill the forms in at reception. Bring photo ID and your insurance card. A list of anything you take regularly helps too, along with recent X-rays if you have them.</p>
      <ul class="small text-2 stack stack-2" style="padding-left:1.1rem;list-style:disc">
        <li>Medical & dental history</li>
        <li>HIPAA acknowledgment</li>
        <li>Financial policy summary</li>
      </ul>
    </article>
    <article class="card" id="insurance">
      <div class="icon-wrap mb-4">{icon("shield", 20)}</div>
      <h2 class="heading mb-3">Insurance</h2>
      <p class="text-2 mb-4">The practice is out-of-network with most PPO plans and files the claim on your behalf. Before any elective treatment you get a written pre-estimate showing what the plan is expected to pay and what you owe. HSA and FSA cards are accepted, and third-party financing is available for larger restorative plans.</p>
      <p class="small text-3">Coverage varies by code and by plan. We verify your benefits before treatment, but your plan booklet is the document that decides.</p>
    </article>
    <article class="card">
      <div class="icon-wrap mb-4">{icon("heart", 20)}</div>
      <h2 class="heading mb-3">Comfort & accessibility</h2>
      <p class="text-2">Tell us about anxiety, jaw fatigue or mobility needs when you book. We put you in a longer slot and the right operatory, which is easier to arrange beforehand than to improvise halfway through a visit.</p>
    </article>
    <div class="card card-inset row-wrap between gap-4">
      <div>
        <h2 class="heading mb-2">Book an appointment</h2>
        <p class="small text-2">Booking requests are answered {DATA["response"]}.</p>
      </div>
      <button type="button" class="btn btn-primary" data-book-open>Book appointment</button>
    </div>
  </div>
</main>"""
    )
    html = head(
        "Patient Information | Vance Dental Studio",
        "New-patient forms, out-of-network PPO insurance and what to bring to a first appointment at Vance Dental Studio in New York.",
        "patients.html",
    ) + header("patients") + content + footer() + close_body()
    (ROOT / "patients.html").write_text(html, encoding="utf-8")


def build_contact():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Contact")])
        + page_hero(
            "Contact",
            "Send a message",
            f"Clinical and scheduling messages are answered {DATA['response']}. If you are in pain outside opening hours, call the number on your post-operative sheet.",
        )
        + f"""
<main id="main-content" class="section">
  <div class="container md-grid-2">
    <form class="card stack stack-4" name="contact" method="POST" action="/thank-you.html" netlify netlify-honeypot="bot-field" data-contact-form>
      <input type="hidden" name="form-name" value="contact">
      <p class="sr-only" aria-hidden="true">
        <label>Leave this field empty: <input name="bot-field" tabindex="-1" autocomplete="off"></label>
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
      <p class="micro text-3">To ask for a specific date instead, <button type="button" class="btn-link" style="display:inline;min-height:auto;padding:0" data-book-open>open the appointment form</button>.</p>
    </form>
    <div class="stack stack-5">
      <div class="card card-inset">
        <h2 class="heading mb-4">Direct lines</h2>
        <p class="small mb-3"><a href="tel:{DATA['phone_tel']}">{icon("phone", 16)} {DATA["phone"]}</a></p>
        <p class="small mb-3"><a href="mailto:{DATA['email']}">{icon("mail", 16)} {DATA["email"]}</a></p>
        <p class="small text-2">{DATA["address_line1"]}<br>{DATA["address_line2"]}</p>
      </div>
      <div class="card">
        <h2 class="heading mb-3">Response times</h2>
        <p class="small text-2">Messages sent on a business day are answered {DATA["response"]}. Weekend messages are read on Monday morning, unless you mark one urgent.</p>
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
      window.vdToast?.(`Could not send. Email {DATA['email']} or try again.`);
    }}
  }});
}});
</script>
"""
    )
    html = head(
        "Contact | Vance Dental Studio",
        "Message or call Vance Dental Studio at 1200 Avenue of the Americas, Suite 400, New York. Replies within 24 hours on business days.",
        "contact.html",
    ) + header("contact") + content + footer() + close_body()
    (ROOT / "contact.html").write_text(html, encoding="utf-8")


def build_thank_you():
    content = f"""
<main id="main-content" class="section" style="min-height:60vh;display:grid;align-items:center">
  <div class="container" style="max-width:560px;text-align:center">
    <div class="icon-wrap" style="margin:0 auto 24px;width:56px;height:56px">{icon("check", 24)}</div>
    <h1 class="title mb-4">Message received</h1>
    <p class="intro" style="margin-inline:auto">Thank you. Someone from the studio will reply {DATA["response"]}. If it cannot wait, call <a href="tel:{DATA['phone_tel']}" style="color:var(--brass)">{DATA["phone"]}</a>.</p>
    <div class="row-wrap gap-3 center mt-8">
      <a class="btn btn-primary" href="index.html">Back to home</a>
      <a class="btn btn-secondary" href="visit.html">Studio directions</a>
    </div>
  </div>
</main>
"""
    html = head(
        "Thank You | Vance Dental Studio",
        "Confirmation page shown after a message is sent to Vance Dental Studio. Replies are sent within 24 hours.",
        "thank-you.html",
    ) + header("contact") + content + footer() + close_body()
    (ROOT / "thank-you.html").write_text(html, encoding="utf-8")


def build_search():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Search")])
        + page_hero(
            "Search",
            "Find something on this site",
            "Search the site for a service, opening hours, parking or insurance.",
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
        "Search the Vance Dental Studio site for its services, opening hours, parking, insurance and patient forms.",
        "search.html",
    ) + header("home") + content + footer() + close_body()
    (ROOT / "search.html").write_text(html, encoding="utf-8")


def build_privacy():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Privacy Policy")])
        + page_hero("Legal", "Privacy Policy", "What this site collects and what the practice does with it. Also how to ask for your own copy.")
        + f"""
<main id="main-content" class="section">
  <div class="container legal">
    <p class="updated">Last updated: March 1, 2026</p>
    <p>Vance Dental Studio ("we", "us") runs the website at {SITE_URL.replace("https://", "")} and the clinical practice at {DATA["address_line1"]}, {DATA["address_line2"]}. This policy covers personal information collected both online and in the office.</p>
    <h2>Information we collect</h2>
    <p>From the booking and contact forms we collect your name, email address, phone number and whatever you write in the message box. From treatment we hold appointment records and the insurance details needed to bill a claim. If you accept analytics cookies we also see technical data such as your IP address, browser type, the pages you opened and the time you spent on them.</p>
    <h2>How we use information</h2>
    <ul>
      <li>To schedule and provide dental care</li>
      <li>To respond to inquiries within our stated response window</li>
      <li>To process insurance claims and payments</li>
      <li>To improve site performance and security</li>
      <li>To send newsletters only when you opt in</li>
    </ul>
    <h2>Sharing</h2>
    <p>We do not sell personal information. We pass data to dental laboratories, imaging centers, insurers and payment processors where your care or your bill needs it, and where the law requires it. Protected health information is handled under applicable HIPAA requirements.</p>
    <h2>Cookies</h2>
    <p>Essential cookies keep the site working; the theme preference you set is stored in one of them. Analytics cookies load only after you accept the banner. Rejecting them changes nothing about the pages you can read.</p>
    <h2>Retention</h2>
    <p>Clinical records are kept for as long as New York State requires. Newsletter addresses are deleted when you unsubscribe. Server logs are rotated on a short schedule.</p>
    <h2>Your choices</h2>
    <p>Email {DATA["email"]} to ask for a copy of what we hold. You can also have something corrected, or have it deleted. Clinical records we are legally required to keep are the one exception.</p>
    <h2>Contact</h2>
    <p>Privacy questions: <a href="mailto:{DATA['email']}">{DATA["email"]}</a> · <a href="tel:{DATA['phone_tel']}">{DATA["phone"]}</a></p>
  </div>
</main>
"""
    )
    html = head(
        "Privacy Policy | Vance Dental Studio",
        "How Vance Dental Studio in New York handles the information it collects online and in the office, and how to ask for a copy of your own data.",
        "privacy.html",
    ) + header("home") + content + footer() + close_body()
    (ROOT / "privacy.html").write_text(html, encoding="utf-8")


def build_terms():
    content = (
        breadcrumbs([("index.html", "Home"), (None, "Terms of Service")])
        + page_hero("Legal", "Terms of Service", "These terms cover use of this website and messages sent to the studio.")
        + f"""
<main id="main-content" class="section">
  <div class="container legal">
    <p class="updated">Last updated: March 1, 2026</p>
    <p>Using this site means you agree to these terms. Clinical care is covered by separate informed-consent documents that you sign at the practice.</p>
    <h2>Website use</h2>
    <p>The pages here are general information. Nothing on this site is a diagnosis or a recommendation to treat. For a dental emergency, call the studio or go to urgent care.</p>
    <h2>Appointments</h2>
    <p>An online booking request is not an appointment until the studio replies and confirms it. We may need to reschedule if a more urgent case comes in. After repeated no-shows we may ask for a deposit before holding another slot.</p>
    <h2>Intellectual property</h2>
    <p>The text, the name and the design of this site belong to Vance Dental Studio unless a page says otherwise. Please do not reproduce them commercially without written permission.</p>
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
        "Terms covering use of the Vance Dental Studio website, online booking requests, site content and liability.",
        "terms.html",
    ) + header("home") + content + footer() + close_body()
    (ROOT / "terms.html").write_text(html, encoding="utf-8")


def build_404():
    content = f"""
<main id="main-content" class="not-found">
  <div>
    <p class="code" aria-hidden="true">404</p>
    <h1 class="title mt-4">There is nothing at this address</h1>
    <p class="intro mt-4" style="margin-inline:auto">The link may be out of date, or the address may have a typo. Search, or go back to the home page.</p>
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
        "The page you asked for does not exist on the Vance Dental Studio site.",
        "404.html",
    ) + header("home") + content + footer() + close_body()
    (ROOT / "404.html").write_text(html, encoding="utf-8")


def build_misc():
    (ROOT / "robots.txt").write_text(
        f"""User-agent: *
Allow: /

Sitemap: {abs_url("sitemap.xml")}
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
        loc = abs_url(path)
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

> Dental practice in Midtown Manhattan. {DATA["doctor"]} is the only dentist.

## Site
- Home: {abs_url()}
- Services: {abs_url("services.html")}
- Case write-ups: {abs_url("cases.html")}
- Location and hours: {abs_url("visit.html")}
- Patient forms and insurance: {abs_url("patients.html")}
- Contact: {abs_url("contact.html")}
- Privacy: {abs_url("privacy.html")}
- Terms: {abs_url("terms.html")}

## Facts
- Address: {DATA["address_line1"]}, {DATA["address_line2"]}
- Phone: {DATA["phone"]}
- Email: {DATA["email"]}
- Hours: Mon-Fri 08:00-19:00; Sat 09:00-16:00; Sun closed
- Services: cosmetic dentistry (veneers, bonding, whitening), dental implants, Invisalign, general checkup and hygiene
- Insurance: out-of-network with most PPO plans; the office files the claim
- First appointment: 60 minutes; new-patient exams usually booked 7 to 10 days out
- Messages answered within 24 hours on business days
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
  <text x="80" y="320" font-family="Georgia, serif" font-size="64" fill="#1C1915">Vance Dental Studio</text>
  <text x="80" y="400" font-family="Georgia, serif" font-size="40" fill="#A67C52">Suite 400, Midtown Manhattan</text>
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
