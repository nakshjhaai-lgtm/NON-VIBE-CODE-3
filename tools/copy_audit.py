#!/usr/bin/env python3
"""Audit the generated pages against Wikipedia:Signs of AI writing.

Checks the patterns from
https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing that can actually
appear in marketing copy, plus the structural signals a site scanner picks up.

Usage:
    python3 tools/copy_audit.py          # report, exit 1 on any finding
    python3 tools/copy_audit.py --quiet  # only print the summary
"""
from __future__ import annotations

import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── "AI vocabulary" from the guide's High density of "AI vocabulary" words ──
AI_VOCAB = [
    "meticulous", "pivotal", "underscore", "tapestry", "testament", "vibrant",
    "crucial", "vital", "foster", "showcase", "showcasing", "highlight",
    "emphasize", "emphasizing", "enhance", "bolster", "enduring", "align with",
    "seamless", "seamlessly", "elevate", "elevates", "elevating", "unleash",
    "unlock", "unlocks", "delve", "delves",
    "landscape", "realm", "embark", "navigate", "harness", "robust",
    "comprehensive", "streamline", "cutting-edge", "state-of-the-art",
    "game-chang", "revolutioniz", "transformative", "innovative",
    "unwavering", "holistic", "curated", "world-class", "premier",
    "testament to", "rich tapestry", "plays a", "stands as", "serves as",
    "marks a", "functions as", "represents a", "boasts", "at the heart of",
    "gold standard", "when it comes to", "in today", "journey",
    "it is worth noting", "it should be noted", "importantly", "moreover",
    "furthermore", "additionally", "in conclusion", "overall",
]

# ── Negative parallelisms: "not just X but also Y", "not X, but Y", "X rather than Y"
NEGATIVE_PARALLELISM = [
    r"\bnot only\b[^.]{0,80}\bbut also\b",
    r"\bnot just\b",
    r"\bmore than (?:just|a)\b",
    r"\brather than\b",   # "X rather than Y"
    r"\binstead of\b.{0,40}\bjust\b",
    r",\s+not\s+(?:a|an|the|to|how|just)\b",
    r"\bisn't\s+just\b",
    r"\bno longer\b.{0,30}\bbut\b",
]

# ── Promotional / puffery wording the guide flags as advertisement-like ──
PROMOTIONAL = [
    r"\bsetting (?:a|the) (?:clear |new |high )?standard\b",
    r"\bleading (?:provider|practice|clinic|studio)\b",
    r"\bboutique\b",
    r"\bexperience (?:focused|the|our|a)\b",
    r"\bunparalleled\b", r"\bunmatched\b", r"\bsecond to none\b",
    r"\bpassionate\b", r"\bdedicated to\b", r"\bcommitted to\b",
    r"\bstate of the art\b", r"\bworld[- ]class\b",
    r"\byour smile is\b", r"\bdream smile\b", r"\bperfect smile\b",
]

# ── Aphoristic / slogan closers ──
APHORISM = [
    r"^[A-Z][^.]{0,60}\bis the product\b",
    r"\bthat(?:'s| is) (?:the|our) (?:difference|promise|standard)\b",
    r"\bbecause you(?:'re| are) worth it\b",
]

MARKETING_CLASSES = ["eyebrow", "lead", "kicker", "tagline", "hero-copy"]


def visible_text(path: str) -> str:
    """Page text with scripts, styles, SVG and all tags stripped."""
    src = open(path, encoding="utf-8").read()
    src = re.sub(r"<script\b.*?</script>", " ", src, flags=re.S | re.I)
    src = re.sub(r"<style\b.*?</style>", " ", src, flags=re.S | re.I)
    src = re.sub(r"<svg\b.*?</svg>", " ", src, flags=re.S | re.I)
    src = re.sub(r"<!--.*?-->", " ", src, flags=re.S)
    src = re.sub(r"<[^>]+>", "\n", src)
    return html.unescape(src)


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [re.sub(r"\s+", " ", p).strip() for p in parts if p and p.strip()]


# A comma-separated enumeration closed by "and"/"or". Two members is normal
# English; three or more in the same slot, repeatedly, is the rule-of-three tic
# the guide describes.
ENUM = re.compile(
    r"""(?P<a>[\w$][\w'’$./-]*(?:\s+[\w'’$./-]+)*?)"""   # first member
    r""",\s*"""                                            # first comma
    r"""(?P<b>[\w$][\w'’$./-]*(?:\s+[\w'’$./-]+)*?)"""   # second member
    r"""(?:\s*,\s*[\w$][\w'’$./-]*(?:\s+[\w'’$./-]+)*?)*"""  # extra members
    r"""\s*(?:,\s*)?(?:and|or)\s+"""                      # conjunction
    r"""(?P<z>[\w$][\w'’$./-]*(?:\s+[\w'’$./-]+)*)""",   # last member
    re.X,
)

# Clause openers that make the pre-comma span a dependent clause, not a list
# member ("If you prefer paper, arrive early and fill the forms in").
CLAUSE_OPENERS = re.compile(
    r"\b(?:if|when|where|because|after|before|unless|although|while|since|"
    r"once|whether|so|then|therefore|however|also)\b",
    re.I,
)


MEMBER = r"[\w$'’./-]+(?:\s+[\w$'’./-]+)*"


JOIN_BEFORE = re.compile(r"(?:,|\b(?:and|or)\b)\s*(" + MEMBER + r")\s*$", re.I)
JOIN_AFTER = re.compile(r"^\s*(?:,|\b(?:and|or)\b)\s*(" + MEMBER + r")", re.I)


def count_members(sent: str, start: int, end: int) -> int:
    """True size of the enumeration containing the match at [start, end).

    ENUM is lazy, so a match is often a sub-span of a longer list. Walk left and
    right over every comma / and / or join to size the whole enumeration.
    A plain list of four or more things is fine; exactly three items in a
    headline or lead, repeated down the page, is the tic the guide describes.
    """
    left = sent[:start]
    while True:
        m = JOIN_BEFORE.search(left)
        if not m:
            break
        left = left[: m.start()]
    tail = sent[end:]
    while True:
        m = JOIN_AFTER.match(tail)
        if not m:
            break
        tail = tail[m.end():]
    span = sent[len(left):sent.index(tail, end)] if tail else sent[len(left):]
    members = 1 + len(re.findall(r",|\b(?:and|or)\b", span, flags=re.I))
    return members


def find_triplets(
    text: str,
    min_members: int = 3,
    max_members: int = 3,
    max_first: int = 4,
    max_last: int = 5,
) -> list[tuple[str, str]]:
    """Enumerations of `min_members`..`max_members` short items.

    Returns (sentence, matched span) pairs so a human can judge whether a hit is
    rhetorical padding or a list the reader genuinely needs. Long members mean
    the comma is joining clauses rather than list items ("Appointments are kept
    long enough, and materials are picked for ..."), so those are skipped.
    """
    hits = []
    for sent in sentences(text):
        for m in ENUM.finditer(sent):
            span = m.group(0)
            head = sent[max(0, m.start() - 40):m.start()]
            if CLAUSE_OPENERS.search(head.split(".")[-1] + " " + span.split(",")[0]):
                continue
            if len(m.group("a").split()) > max_first:
                continue
            if len(m.group("z").split()) > max_last:
                continue
            n = count_members(sent, m.start(), m.end())
            if n < min_members or n > max_members:
                continue
            hits.append((sent, span))
            break
    return hits


def prominent_text(src: str) -> str:
    """Text in the slots a scanner weighs most: title, meta description,
    headings, section labels and lead/intro paragraphs."""
    parts = re.findall(r"<title>(.*?)</title>", src, flags=re.S | re.I)
    parts += re.findall(r'property="og:title" content="([^"]*)"', src)
    for tag in ("h1", "h2", "h3", "h4"):
        parts += [re.sub(r"<[^>]+>", " ", m)
                  for m in re.findall(rf"<{tag}\b[^>]*>(.*?)</{tag}>", src, flags=re.S)]
    for cls in ("section-label", "intro", "lead", "eyebrow", "blurb", "title"):
        parts += [re.sub(r"<[^>]+>", " ", m)
                  for m in re.findall(rf'class="[^"]*\b{cls}\b[^"]*"[^>]*>(.*?)</', src, flags=re.S)]
    return html.unescape("\n".join(parts))


def scan(path: str) -> tuple[dict, dict]:
    """Returns (findings, notes). Findings are patterns to fix; notes are
    three-item enumerations deep in body copy, which may be plain facts."""
    text = visible_text(path)
    low = text.lower()
    src = open(path, encoding="utf-8").read()
    findings: dict[str, list] = {}
    notes: dict[str, list] = {}

    vocab = sorted({w for w in AI_VOCAB if re.search(r"\b" + re.escape(w), low)})
    if vocab:
        findings["AI vocabulary"] = vocab

    neg = []
    for pat in NEGATIVE_PARALLELISM:
        for m in re.finditer(pat, low):
            start = max(0, m.start() - 40)
            neg.append(re.sub(r"\s+", " ", low[start:m.end() + 40]).strip())
    if neg:
        findings["negative parallelism"] = sorted(set(neg))

    loud = find_triplets(prominent_text(src))
    if loud:
        findings["rule-of-three triplet in heading/lead"] = [f"{span!r} in: {sent}" for sent, span in loud]
    quiet = [t for t in find_triplets(text) if t not in loud]
    if quiet:
        notes["three-item list in body copy"] = [f"{span!r} in: {sent}" for sent, span in quiet]

    # meta description is an SEO summary: a list is expected, but keep it to two
    # members or four-plus so the page summary does not read as a cadence.
    for meta in re.findall(r'name="description" content="([^"]*)"', src):
        for sent, span in find_triplets(html.unescape(meta)):
            findings.setdefault("rule-of-three triplet in meta description", []).append(span)

    promo = []
    for pat in PROMOTIONAL + APHORISM:
        for m in re.finditer(pat, low, flags=re.I):
            promo.append(m.group(0))
    if promo:
        findings["promotional wording"] = sorted(set(promo))

    curly = [c for c in ("\u201c", "\u201d", "\u2018", "\u2019") if c in text]
    if curly:
        findings["curly quotation marks"] = [f"U+{ord(c):04X}" for c in curly]

    if "\u2014" in text:
        findings["em dash in copy"] = [text[max(0, m.start() - 40):m.start() + 40]
                                       for m in re.finditer("\u2014", text)]

    bad_alts = re.findall(r'<img\b[^>]*\balt=""', src)
    if bad_alts:
        findings["empty alt text"] = [f"{len(bad_alts)} image(s)"]

    no_alt = [m.group(0)[:80] for m in re.finditer(r"<img\b(?![^>]*\balt=)[^>]*>", src)]
    if no_alt:
        findings["missing alt attribute"] = no_alt

    classes = sorted({c for c in MARKETING_CLASSES
                      if re.search(r'class="[^"]*\b' + c + r'\b', src)})
    if classes:
        findings["marketing template class"] = classes

    # host consistency: canonical / og:url vs the deployed host
    canon = re.search(r'rel="canonical" href="([^"]+)"', src)
    ogurl = re.search(r'property="og:url" content="([^"]+)"', src)
    if canon and ogurl and canon.group(1) != ogurl.group(1):
        findings["canonical != og:url"] = [canon.group(1), ogurl.group(1)]

    return findings, notes


def main() -> int:
    quiet = "--quiet" in sys.argv
    show_notes = "--notes" in sys.argv
    pages = sorted(p for p in glob.glob(os.path.join(ROOT, "*.html")))
    total = 0
    note_total = 0
    for path in pages:
        findings, notes = scan(path)
        total += sum(len(v) for v in findings.values())
        note_total += sum(len(v) for v in notes.values())
        if quiet or not (findings or (notes and show_notes)):
            continue
        print(f"\n{os.path.basename(path)}")
        for label, items in findings.items():
            print(f"  FIX {label}:")
            for item in items[:6]:
                print(f"    - {item}")
            if len(items) > 6:
                print(f"    ... and {len(items) - 6} more")
        for label, items in notes.items():
            if not show_notes:
                continue
            print(f"  note {label}:")
            for item in items[:4]:
                print(f"    - {item[:150]}")
            if len(items) > 4:
                print(f"    ... and {len(items) - 4} more")
    tail = f"{note_total} note(s)" if note_total else "no notes"
    print(f"\n{len(pages)} pages scanned, {total} finding(s) to fix, {tail}.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
