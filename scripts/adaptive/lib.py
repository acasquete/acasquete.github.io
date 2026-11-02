"""Core logic for Adaptive Reading: block extraction, stable ids and validation.

Standard library only. The extraction runs over the *built* page (``_site``) so the
text it stores is exactly the text the browser will see (kramdown typography,
links, inline code...). The post's Markdown is never modified.
"""
import difflib
import html
import re
import secrets
import unicodedata
from html.parser import HTMLParser

LEVELS = (1, 2, 3)  # Sencillo, Esencial, Detallado; Original is always the author's text
OMITTABLE = (1, 2)  # at these levels a block may be dropped entirely (empty string)
MIN_WORDS = 25

VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "col",
        "area", "base", "embed", "param", "track"}
# Descendants that make a block non-adaptable (they must stay untouched).
FORBIDDEN_INSIDE = {"img", "iframe", "video", "audio", "svg", "math", "script",
                    "style", "pre", "table", "blockquote", "ul", "ol", "div",
                    "figure", "h1", "h2", "h3", "h4", "h5", "h6", "input",
                    "button", "form", "object", "embed", "canvas", "p", "li"}
# Ancestors (inside .prose) that exclude everything below them.
EXCLUDED_ANCESTORS = {"blockquote", "pre", "table", "figure", "details",
                      "aside", "nav", "footer", "header", "h1", "h2", "h3",
                      "h4", "h5", "h6"}
EXCLUDED_DIV_CLASSES = {"underreview", "video-embed", "highlight", "tags",
                        "highlighter-rouge", "footnotes"}
# What a generated variant may contain.
ALLOWED_TAGS = {"a", "em", "strong", "b", "i", "code", "kbd", "sup", "sub", "br"}


# ---------------------------------------------------------------- hashing ---

def normalize_text(text):
    """Collapse whitespace and apply NFC. Must match normalize() in adaptive.js."""
    text = unicodedata.normalize("NFC", text)
    return re.sub(r"[\s﻿]+", " ", text).strip()


def fnv1a(text):
    """32-bit FNV-1a over the UTF-8 bytes. Must match hash() in adaptive.js."""
    h = 0x811C9DC5
    for byte in text.encode("utf-8"):
        h ^= byte
        h = (h * 0x01000193) & 0xFFFFFFFF
    return format(h, "08x")


def new_id():
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "b-" + "".join(secrets.choice(alphabet) for _ in range(6))


# ------------------------------------------------------------- extraction ---

def clean_starttag(tag, attrs):
    """Re-serialise an inline start tag keeping only what variants may carry."""
    if tag == "a":
        href = dict(attrs).get("href")
        return '<a href="%s">' % html.escape(href, quote=True) if href is not None else "<a>"
    return "<%s>" % tag


class _Candidate:
    __slots__ = ("tag", "raw", "text", "bad", "depth")

    def __init__(self, tag, depth):
        self.tag = tag
        self.raw = []
        self.text = []
        self.bad = False
        self.depth = depth


class BlockExtractor(HTMLParser):
    """Collects adaptable paragraphs / list items inside ``div.content.prose``."""

    def __init__(self, min_words=MIN_WORDS):
        super().__init__(convert_charrefs=False)
        self.min_words = min_words
        self.stack = []  # (tag, classes)
        self.prose_depth = None
        self.active = []
        self.blocks = []

    # -- helpers
    def _in_prose(self):
        return self.prose_depth is not None

    def _excluded(self):
        if self.prose_depth is None:
            return True
        for tag, classes in self.stack[self.prose_depth:]:
            if tag in EXCLUDED_ANCESTORS:
                return True
            if tag == "div" and classes & EXCLUDED_DIV_CLASSES:
                return True
        return False

    def _mark_bad_if_forbidden(self, tag, attrs):
        if not self.active:
            return
        cls = set((dict(attrs).get("class") or "").split())
        bad = tag in FORBIDDEN_INSIDE or "math" in cls
        a = dict(attrs)
        if tag == "sup" and "id" in a:
            bad = True
        if tag == "a" and cls & {"footnote", "reversefootnote"}:
            bad = True
        if tag == "span" and (a.get("style") or cls):
            bad = True
        if bad:
            for cand in self.active:
                cand.bad = True

    # -- events
    def handle_starttag(self, tag, attrs):
        classes = set((dict(attrs).get("class") or "").split())
        if tag == "div" and {"content", "prose"} <= classes and self.prose_depth is None:
            self.stack.append((tag, classes))
            self.prose_depth = len(self.stack)
            return
        if self._in_prose():
            self._mark_bad_if_forbidden(tag, attrs)
            if tag in ("p", "li") and not self._excluded() and tag not in VOID:
                cand = _Candidate(tag, len(self.stack))
                self.active.append(cand)
            elif self.active:
                self.active[-1].raw.append(clean_starttag(tag, attrs))
        if tag not in VOID:
            self.stack.append((tag, classes))

    def handle_startendtag(self, tag, attrs):
        if self._in_prose():
            self._mark_bad_if_forbidden(tag, attrs)
            if self.active:
                self.active[-1].raw.append(clean_starttag(tag, attrs).replace(">", ">") if tag != "br" else "<br>")

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        # Close the matching element on the stack.
        idx = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                idx = i
                break
        if idx is None:
            return
        closing_depth = idx  # depth of the element being closed (0-based)
        if self.active and self.active[-1].tag == tag and self.active[-1].depth == closing_depth:
            cand = self.active.pop()
            self._finish(cand)
        elif self.active:
            self.active[-1].raw.append("</%s>" % tag)
        del self.stack[idx:]
        if self.prose_depth is not None and len(self.stack) < self.prose_depth:
            self.prose_depth = None
            self.active = []

    def handle_data(self, data):
        if self.active:
            self.active[-1].raw.append(html.escape(data, quote=False))
            self.active[-1].text.append(data)

    def handle_entityref(self, name):
        if self.active:
            self.active[-1].raw.append("&%s;" % name)
            self.active[-1].text.append(html.unescape("&%s;" % name))

    def handle_charref(self, name):
        if self.active:
            self.active[-1].raw.append("&#%s;" % name)
            self.active[-1].text.append(html.unescape("&#%s;" % name))

    def _finish(self, cand):
        if cand.bad:
            return
        text = normalize_text("".join(cand.text))
        if len(text.split()) < self.min_words:
            return
        self.blocks.append({
            "tag": cand.tag,
            "html": normalize_text("".join(cand.raw)),
            "text": text,
        })


def extract_blocks(page_html, min_words=MIN_WORDS):
    """Return the adaptable blocks of a built post, in document order.

    Each block gets ``h`` (text hash) and ``k`` (hash + occurrence), the lookup
    key used by the browser. The persistent identity (``id``) is assigned later.
    """
    parser = BlockExtractor(min_words)
    parser.feed(page_html)
    parser.close()
    seen = {}
    for block in parser.blocks:
        h = fnv1a(block["text"])
        occ = seen.get(h, 0)
        seen[h] = occ + 1
        block["h"] = h
        block["k"] = "%s.%d" % (h, occ)
    return parser.blocks


# --------------------------------------------------------- stable block ids ---

def match_ids(new_blocks, old_blocks, fuzzy=0.55):
    """Assign persistent ids to ``new_blocks`` from the previous state.

    1. Exact text match keeps id *and* variants.
    2. Otherwise a similar, still-unmatched old block keeps the id (its variants
       become stale and are regenerated).
    3. Anything else gets a brand new id.
    Returns the list of old blocks that disappeared.
    """
    old_by_text = {}
    for ob in old_blocks:
        old_by_text.setdefault(ob["text"], []).append(ob)
    used = set()
    pending = []
    for nb in new_blocks:
        candidates = [o for o in old_by_text.get(nb["text"], []) if id(o) not in used]
        if candidates:
            ob = candidates[0]
            used.add(id(ob))
            nb["id"] = ob["id"]
            nb["levels"] = dict(ob.get("levels", {}))
            nb["errors"] = dict(ob.get("errors", {}))
            nb["stale"] = False
        else:
            pending.append(nb)
    leftovers = [o for o in old_blocks if id(o) not in used]
    for nb in pending:
        best, best_ratio = None, fuzzy
        for ob in leftovers:
            if id(ob) in used:
                continue
            ratio = difflib.SequenceMatcher(None, ob["text"], nb["text"]).quick_ratio()
            if ratio >= best_ratio:
                ratio = difflib.SequenceMatcher(None, ob["text"], nb["text"]).ratio()
            if ratio >= best_ratio:
                best, best_ratio = ob, ratio
        if best is not None:
            used.add(id(best))
            nb["id"] = best["id"]
        else:
            nb["id"] = new_id()
        nb["levels"] = {}
        nb["errors"] = {}
        nb["stale"] = True
    return [o for o in old_blocks if id(o) not in used]


# ------------------------------------------------------------- validation ---

class _Inline(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.attrs = []
        self.hrefs = []
        self.codes = []
        self.text = []
        self._code = None

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.attrs.append((tag, attrs))
        if tag == "a":
            self.hrefs.append(dict(attrs).get("href", ""))
        if tag == "code":
            self._code = []

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "code" and self._code is not None:
            self.codes.append("".join(self._code))
            self._code = None

    def handle_data(self, data):
        self.text.append(data)
        if self._code is not None:
            self._code.append(data)


def _parse_inline(fragment):
    p = _Inline()
    p.feed(fragment)
    p.close()
    return p


NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")
QUOTE_RE = re.compile(r"[“«\"]([^”»\"]{12,}?)[”»\"]")


def numbers_of(text):
    return {n.rstrip(".,") for n in NUMBER_RE.findall(text)}


# Length of a variant relative to its original block: (min, max).
RATIO = {1: (0.02, 0.6), 2: (0.2, 1.2), 3: (0.45, 1.3)}


def validate_variant(original_html, variant_html, level):
    """Return a list of problems (empty list = valid).

    Condensing is allowed (dropping links, code, figures or quotes), inventing is
    not: everything that appears in a variant must exist in the original.
    ``""`` means "omit this block at this level" and is only valid for OMITTABLE levels.
    """
    if variant_html == "" and level in OMITTABLE:
        return []
    errors = []
    if not isinstance(variant_html, str) or not variant_html.strip():
        return ["empty response"]
    v = variant_html.strip()
    if any(tok in v for tok in ("**", "```", "`", "\n#")):
        errors.append("markdown leftovers")
    orig = _parse_inline(original_html)
    var = _parse_inline(v)
    for tag, attrs in var.attrs:
        if tag not in ALLOWED_TAGS:
            errors.append("tag not allowed: <%s>" % tag)
            continue
        for name, value in attrs:
            if tag == "a" and name == "href":
                continue
            errors.append("attribute not allowed: %s on <%s>" % (name, tag))
    if not set(var.hrefs) <= set(orig.hrefs):
        errors.append("links changed")
    for href in var.hrefs:
        if re.match(r"\s*(javascript|data|vbscript):", href, re.I):
            errors.append("unsafe href")
    if not set(var.codes) <= set(orig.codes):
        errors.append("inline code changed")
    o_text = normalize_text("".join(orig.text))
    v_text = normalize_text("".join(var.text))
    if not numbers_of(v_text) <= numbers_of(o_text):
        errors.append("figures changed: %s -> %s" % (sorted(numbers_of(o_text)), sorted(numbers_of(v_text))))
    for quote in QUOTE_RE.findall(v_text):
        if quote not in o_text:
            errors.append("quoted text altered: %r" % quote[:40])
    lo, hi = RATIO[level]
    ratio = len(v_text) / max(1, len(o_text))
    if ratio < lo:
        errors.append("too short (%.2fx)" % ratio)
    if ratio > hi:
        errors.append("too long (%.2fx): level %d must not be longer than the original" % (ratio, level))
    return list(dict.fromkeys(errors))


# --------------------------------------------------------------- manifests ---

def public_manifest(slug, blocks):
    """Trimmed manifest served to the browser (no original text)."""
    out = []
    for b in blocks:
        levels = {str(l): b["levels"][str(l)] for l in LEVELS if str(l) in b.get("levels", {})}
        if not levels:
            continue
        out.append({"id": b["id"], "k": b["k"], "l": levels})
    return {"version": 1, "slug": slug, "blocks": out}
