#!/usr/bin/env python3
"""Generate (or check) Adaptive Reading variants for a post.

    python3 scripts/adaptive/generate.py <slug> [options]

The slug is the post URL path (``/vibe-coding-deuda-tecnica`` -> ``vibe-coding-deuda-tecnica``).
Run ``bundle exec jekyll build`` first: blocks are read from the built page so they
match exactly what the browser renders. The Markdown is never touched.

Outputs (both versioned):
  _adaptive/<slug>.json   authoritative state (original text, variants, errors)
  adaptive/<slug>.json    trimmed manifest served to the browser

Credentials come from environment variables only (see scripts/adaptive/README.md).
"""
import argparse
import datetime
import glob
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROMPT_VERSION = 1

LEVEL_GUIDE = {
    "1": "Sencillo (~8-10% del texto): casi sentencias. Cada bloque que mantengas es UNA frase corta (máx. ~25 palabras) que expresa el concepto, sin relleno, sin adjetivos ni ejemplos; todo lo demás se omite con \"\". No son frases sueltas: leídas seguidas forman un resumen que explica las ideas del artículo con palabras llanas.",
    "2": "Esencial (~45% del texto): el hilo del argumento sin digresiones ni ejemplos secundarios. Puedes omitir con \"\" los párrafos prescindibles y condensar el resto.",
    "3": "Detallado (~75% del texto): casi todo el contenido, quitando repeticiones y giros innecesarios. Normalmente conserva todos los bloques.",
}

SYSTEM = """Eres un editor que adapta la profundidad de textos de un blog personal sin cambiar su contenido ni inventar nada.
Recibirás UN bloque (un párrafo o elemento de lista) y devolverás tres variantes de lectura: 1 (Sencillo, la más corta: casi una sentencia por idea), 2 (Esencial) y 3 (Detallado, la más cercana al original). El nivel 4 (Original) es el texto del autor y no se genera.

Reglas obligatorias:
- Condensar es válido (omitir ideas secundarias, ejemplos, cifras o enlaces), pero no inventes información ni añadas afirmaciones que no estén en el original.
- Todo lo que aparezca en una variante debe existir en el original: cifras, enlaces (mismo href), texto de <code> y citas entre comillas (idénticas).
- Conserva la voz, la persona gramatical y el estilo del autor siempre que sea posible. Mismo idioma que el original.
- Un nivel puede omitir el bloque entero devolviendo una cadena vacía "" (solo niveles 1 y 2). Los niveles más cortos omiten más.
- Usa SOLO estas etiquetas HTML: a (solo href), em, strong, code, kbd, sup, sub, br. Nada de Markdown, atributos extra ni clases.
- Responde únicamente con un objeto JSON con las claves "1", "2" y "3" cuyos valores son cadenas HTML. Sin texto adicional."""


# ----------------------------------------------------------------- helpers ---

def find_post(slug):
    for path in glob.glob(os.path.join(ROOT, "_posts", "**", "*.md"), recursive=True):
        name = os.path.basename(path)[:-3]
        parts = name.split("-", 3)
        base = parts[3] if len(parts) == 4 and parts[0].isdigit() else name
        if base == slug:
            return path
    draft = os.path.join(ROOT, "_drafts", slug + ".md")
    return draft if os.path.exists(draft) else None


def page_path(slug, override=None):
    if override:
        return override
    for candidate in (os.path.join(ROOT, "_site", slug + ".html"),
                      os.path.join(ROOT, "_site", slug, "index.html")):
        if os.path.exists(candidate):
            return candidate
    return None


def front_matter(path):
    text = open(path, encoding="utf8").read()
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        for line in text[3:end].splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"\'')
    return meta


def load_state(slug):
    path = os.path.join(ROOT, "_adaptive", slug + ".json")
    if os.path.exists(path):
        return json.load(open(path, encoding="utf8"))
    return {"version": 1, "slug": slug, "blocks": []}


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1 if "_adaptive" in path else None,
                  separators=None if "_adaptive" in path else (",", ":"))
        f.write("\n")


# --------------------------------------------------------------- providers ---

def build_user_prompt(meta, blocks, i):
    b = blocks[i]
    prev_t = blocks[i - 1]["text"][:300] if i > 0 else "(inicio)"
    next_t = blocks[i + 1]["text"][:300] if i + 1 < len(blocks) else "(fin)"
    guide = "\n".join("%s = %s" % (k, v) for k, v in LEVEL_GUIDE.items())
    return (
        "Artículo: %s\nDescripción: %s\n\nContexto (no lo reescribas):\n- Bloque anterior: %s\n- Bloque siguiente: %s\n\n"
        "Niveles:\n%s\n\nBLOQUE ORIGINAL (HTML):\n%s\n"
        % (meta.get("title", ""), meta.get("description", ""), prev_t, next_t, guide, b["html"])
    )


def _http_json(url, headers, payload, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %s: %s" % (e.code, e.read().decode("utf8", "replace")[:300]))


def extract_json(text):
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < 0:
        raise ValueError("no JSON object in response")
    return json.loads(text[start:end + 1])


class Anthropic:
    name = "anthropic"

    def __init__(self, model):
        self.key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.key:
            sys.exit("ANTHROPIC_API_KEY is not set")
        self.model = model or os.environ.get("ADAPTIVE_MODEL", "claude-sonnet-5-5")

    def complete(self, system, user):
        data = _http_json(
            os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com") + "/v1/messages",
            {"x-api-key": self.key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            {"model": self.model, "max_tokens": 4000, "system": system,
             "messages": [{"role": "user", "content": user}]},
        )
        return "".join(part.get("text", "") for part in data.get("content", []))


class OpenAICompatible:
    name = "openai"

    def __init__(self, model):
        self.key = os.environ.get("OPENAI_API_KEY")
        if not self.key:
            sys.exit("OPENAI_API_KEY is not set")
        self.base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.environ.get("ADAPTIVE_MODEL")
        if not self.model:
            sys.exit("Set --model or ADAPTIVE_MODEL for the openai provider")

    def complete(self, system, user):
        data = _http_json(
            self.base + "/chat/completions",
            {"Authorization": "Bearer " + self.key, "content-type": "application/json"},
            {"model": self.model, "messages": [{"role": "system", "content": system},
                                                {"role": "user", "content": user}]},
        )
        return data["choices"][0]["message"]["content"]


class FileProvider:
    """Reads variants from a JSON file: {"<block index>": {"1": "...", ..., "4": "..."}}.

    Useful for hand-authored variants and for tests; no network involved.
    """
    name = "file"
    model = "file"

    def __init__(self, path):
        if not path:
            sys.exit("--variants-file is required for the file provider")
        self.data = json.load(open(path, encoding="utf8"))
        self.index = None

    def complete(self, system, user):
        entry = self.data.get(str(self.index))
        if entry is None:
            raise RuntimeError("no entry for block %s in variants file" % self.index)
        return json.dumps(entry, ensure_ascii=False)


def make_provider(args):
    if args.provider == "anthropic":
        return Anthropic(args.model)
    if args.provider == "openai":
        return OpenAICompatible(args.model)
    return FileProvider(args.variants_file)


# -------------------------------------------------------------- generation ---

def generate_block(provider, meta, blocks, i, log):
    b = blocks[i]
    todo = [str(l) for l in lib.LEVELS if str(l) not in b["levels"]]
    prompt = build_user_prompt(meta, blocks, i)
    feedback = ""
    for attempt in (1, 2):
        if isinstance(provider, FileProvider):
            provider.index = i
        try:
            raw = provider.complete(SYSTEM, prompt + feedback)
            data = extract_json(raw)
        except Exception as e:  # network, JSON...
            log("  block %d attempt %d failed: %s" % (i, attempt, e))
            feedback = "\n\nLa respuesta anterior no fue un JSON válido. Devuelve solo el JSON."
            continue
        problems = {}
        for lvl in todo:
            errs = lib.validate_variant(b["html"], data.get(lvl), int(lvl))
            if errs:
                problems[lvl] = "; ".join(errs)
            else:
                b["levels"][lvl] = data[lvl].strip()
                b["errors"].pop(lvl, None)
        todo = [l for l in todo if l not in b["levels"]]
        if not todo:
            return
        log("  block %d attempt %d invalid levels: %s" % (i, attempt, {l: e[:120] for l, e in problems.items()}))
        feedback = "\n\nCorrige solo estos niveles (los demás son válidos):\n" + "\n".join(
            "- nivel %s: %s" % (l, e) for l, e in problems.items())
        for l, e in problems.items():
            b["errors"][l] = e
    for l in todo:
        b["errors"].setdefault(l, "generation failed")


def level_totals(blocks):
    """Words per level as a share of the original (omitted blocks count 0)."""
    total = sum(len(b["text"].split()) for b in blocks) or 1
    out = {}
    for lvl in lib.LEVELS:
        words = 0
        for b in blocks:
            v = b.get("levels", {}).get(str(lvl))
            words += len(b["text"].split()) if v is None else len(lib.normalize_text("".join(lib._parse_inline(v).text)).split())
        out[lvl] = words / total
    return out


def print_totals(blocks):
    names = {1: "Sencillo", 2: "Esencial", 3: "Detallado"}
    print("  words vs original: " + ", ".join("%s %.0f%%" % (names[l], r * 100) for l, r in level_totals(blocks).items()))
    omitted = {l: sum(1 for b in blocks if b.get("levels", {}).get(str(l)) == "") for l in lib.OMITTABLE}
    print("  omitted blocks: " + ", ".join("%s %d" % (names[l], n) for l, n in omitted.items()))


def cmd_check(slug, state, blocks, public_path):
    """Validate stored state against the current page. Returns number of problems."""
    problems = []
    by_text = {s["text"]: s for s in state["blocks"]}
    for b in blocks:
        s = by_text.get(b["text"])
        if s is None:
            problems.append("stale: block %s... changed since the last generation" % b["text"][:40])
            continue
        for lvl in lib.LEVELS:
            v = s.get("levels", {}).get(str(lvl))
            if v is None:
                problems.append("missing level %d for block %s" % (lvl, s["id"]))
            else:
                for e in lib.validate_variant(b["html"], v, lvl):
                    problems.append("%s level %d: %s" % (s["id"], lvl, e))
    live = {s["id"] for s in state["blocks"] if s["text"] in {b["text"] for b in blocks}}
    for s in state["blocks"]:
        if s["id"] not in live:
            problems.append("orphan: %s no longer exists in the post" % s["id"])
    if os.path.exists(public_path):
        pub = json.load(open(public_path, encoding="utf8"))
        expected = lib.public_manifest(slug, state["blocks"])
        if pub != expected:
            problems.append("public manifest is out of sync with the state (re-run without --check)")
    else:
        problems.append("public manifest missing: %s" % public_path)
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--provider", choices=["anthropic", "openai", "file"], default="anthropic")
    ap.add_argument("--model")
    ap.add_argument("--variants-file")
    ap.add_argument("--html", help="built page to read (default: _site/<slug>.html)")
    ap.add_argument("--min-words", type=int, default=lib.MIN_WORDS)
    ap.add_argument("--force", action="store_true", help="regenerate every block")
    ap.add_argument("--only-levels", help="comma-separated levels (e.g. 1 or 1,2) to regenerate for every block, keeping the others")
    ap.add_argument("--dry-run", action="store_true", help="show the plan, call nothing, write nothing")
    ap.add_argument("--check", action="store_true", help="validate stored adaptations, no API calls")
    args = ap.parse_args()
    slug = args.slug.strip("/")

    post = find_post(slug)
    if not post:
        sys.exit("No post found for slug %r under _posts/ or _drafts/" % slug)
    page = page_path(slug, args.html)
    if not page:
        sys.exit("Built page not found. Run `bundle exec jekyll build` (add --drafts for drafts) first.")
    meta = front_matter(post)
    blocks = lib.extract_blocks(open(page, encoding="utf8").read(), args.min_words)
    state = load_state(slug)
    public_path = os.path.join(ROOT, "adaptive", slug + ".json")

    if args.check:
        problems = cmd_check(slug, state, blocks, public_path)
        for p in problems:
            print("  ✗", p)
        print("%d block(s) in the page, %d problem(s)" % (len(blocks), len(problems)))
        print_totals([by_text_state for by_text_state in state["blocks"] if by_text_state["text"] in {b["text"] for b in blocks}])
        sys.exit(1 if problems else 0)

    orphans = lib.match_ids(blocks, state["blocks"])
    if args.force:
        for b in blocks:
            b["levels"], b["errors"], b["stale"] = {}, {}, True
    if args.only_levels:
        for lvl in args.only_levels.split(","):
            if int(lvl) not in lib.LEVELS:
                sys.exit("--only-levels: %r is not a generated level" % lvl)
            for b in blocks:
                b["levels"].pop(lvl.strip(), None)
                b["errors"].pop(lvl.strip(), None)
    pending = [i for i, b in enumerate(blocks) if len(b["levels"]) < len(lib.LEVELS)]
    print("%s: %d adaptable block(s), %d to generate, %d reused, %d orphaned"
          % (slug, len(blocks), len(pending), len(blocks) - len(pending), len(orphans)))
    if args.dry_run:
        for i in pending:
            print("  - block %d (%s): %s..." % (i, blocks[i]["id"], blocks[i]["text"][:60]))
        return

    provider = make_provider(args)
    log = lambda m: print(m, file=sys.stderr)
    for n, i in enumerate(pending, 1):
        print("  [%d/%d] %s" % (n, len(pending), blocks[i]["id"]))
        generate_block(provider, meta, blocks, i, log)
        if provider.name != "file":
            time.sleep(0.3)

    failed = sum(1 for b in blocks if len(b["levels"]) < len(lib.LEVELS))
    for b in blocks:
        if "model" not in b or b.get("stale"):
            b["model"] = getattr(provider, "model", args.provider)
        b.pop("stale", None)
    new_state = {
        "version": 1, "slug": slug,
        "post": os.path.relpath(post, ROOT),
        "generator": {"provider": provider.name, "model": getattr(provider, "model", None),
                      "prompt_version": PROMPT_VERSION,
                      "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
        "blocks": blocks,
    }
    write_json(os.path.join(ROOT, "_adaptive", slug + ".json"), new_state)
    write_json(public_path, lib.public_manifest(slug, blocks))
    slugs = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, "adaptive", "*.json")))
    write_json(os.path.join(ROOT, "_data", "adaptive.json"), slugs)  # layout reads this list
    print("Wrote _adaptive/%s.json and adaptive/%s.json" % (slug, slug))
    print_totals(blocks)
    if failed:
        print("%d block(s) have missing levels; the browser will show the original for them." % failed,
              file=sys.stderr)


if __name__ == "__main__":
    main()
