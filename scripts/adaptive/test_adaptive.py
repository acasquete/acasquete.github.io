"""Run: python3 -m unittest discover -s scripts/adaptive -v"""
import json
import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LONG = " ".join(["palabra"] * 30)


def page(body):
    return '<html><body><div class="content prose">%s</div><div class="tags"><p>%s</p></div></body></html>' % (body, LONG)


class Extraction(unittest.TestCase):
    def test_collects_paragraphs_and_list_items_only(self):
        html = page(
            "<h2>Título %s</h2><p>%s uno</p><ul><li>%s dos</li><li>corto</li></ul>"
            "<pre><code>%s</code></pre><blockquote><p>%s cita</p></blockquote>"
            "<table><tr><td><p>%s</p></td></tr></table><p><img src=\"/a.png\">%s</p>"
            % (LONG, LONG, LONG, LONG, LONG, LONG, LONG))
        blocks = lib.extract_blocks(html)
        self.assertEqual([b["tag"] for b in blocks], ["p", "li", "li"])  # short items count too
        self.assertEqual(len(lib.extract_blocks(html, min_words=25)), 2)

    def test_skips_image_captions(self):
        html = page("<p><img src=\"/a.png\"></p><p><em>Imagen 1. Una curva.</em></p><p>La realidad es otra.</p>")
        self.assertEqual([b["text"] for b in lib.extract_blocks(html)], ["La realidad es otra."])

    def test_skips_blocks_with_footnotes_and_nested_lists(self):
        html = page('<p>%s<sup id="fnref:1"><a href="#fn:1" class="footnote">1</a></sup></p>'
                    "<ul><li>%s<ul><li>%s hijo</li></ul></li></ul>" % (LONG, LONG, LONG))
        blocks = lib.extract_blocks(html)
        self.assertEqual(len(blocks), 1)  # only the leaf <li>
        self.assertIn("hijo", blocks[0]["text"])

    def test_text_matches_dom_text_and_keeps_inline_markup(self):
        html = page('<p>%s <a href="https://x.dev/?a=1&amp;b=2">enlace</a> y <code>x &lt; y</code> &amp; “fin”.</p>' % LONG)
        b = lib.extract_blocks(html)[0]
        self.assertIn("enlace y x < y & “fin”.", b["text"])
        self.assertIn('href="https://x.dev/?a=1&amp;b=2"', b["html"])
        self.assertIn("<code>x &lt; y</code>", b["html"])

    def test_duplicate_paragraphs_get_distinct_keys(self):
        b = lib.extract_blocks(page("<p>%s</p><p>%s</p>" % (LONG, LONG)))
        self.assertEqual(b[0]["h"], b[1]["h"])
        self.assertNotEqual(b[0]["k"], b[1]["k"])

    def test_excluded_divs(self):
        html = page('<div class="underreview"><p>%s</p></div><p>%s</p>' % (LONG, LONG))
        self.assertEqual(len(lib.extract_blocks(html)), 1)


class StableIds(unittest.TestCase):
    def blocks(self, *texts):
        return lib.extract_blocks(page("".join("<p>%s</p>" % t for t in texts)))

    def test_ids_survive_edits_elsewhere(self):
        a, b, c = [LONG + " " + w for w in ("alfa", "beta", "gamma")]
        old = self.blocks(a, b, c)
        lib.match_ids(old, [])
        for blk in old:
            blk["levels"] = {"1": "x"}
        new = self.blocks(a, "Nuevo párrafo " + LONG + " intercalado", b, c)  # insertion shifts positions
        orphans = lib.match_ids(new, old)
        self.assertEqual(new[0]["id"], old[0]["id"])
        self.assertEqual(new[2]["id"], old[1]["id"])
        self.assertEqual(new[3]["id"], old[2]["id"])
        self.assertEqual(orphans, [])
        self.assertEqual(new[2]["levels"], {"1": "x"})  # unchanged -> variants reused
        self.assertEqual(new[1]["levels"], {})          # new -> to generate

    def test_small_edit_keeps_id_but_invalidates_variants(self):
        a = LONG + " original"
        old = self.blocks(a)
        lib.match_ids(old, [])
        old[0]["levels"] = {"1": "x", "2": "y", "3": "z", "4": "w"}
        new = self.blocks(a + " corregido")
        lib.match_ids(new, old)
        self.assertEqual(new[0]["id"], old[0]["id"])
        self.assertEqual(new[0]["levels"], {})

    def test_removed_block_is_reported(self):
        old = self.blocks(LONG + " a", LONG + " b")
        lib.match_ids(old, [])
        new = self.blocks(LONG + " a")
        orphans = lib.match_ids(new, old)
        self.assertEqual(len(orphans), 1)


class Validation(unittest.TestCase):
    ORIG = ('Según la <a href="https://x.dev/doc">documentación</a>, el sistema procesa 250 mensajes con '
            '<code>Client</code> y, como dijo alguien, “lo difícil es entender por qué falla”.')
    GOOD = ('Según la <a href="https://x.dev/doc">documentación</a>, el sistema procesa 250 mensajes con '
            '<code>Client</code>. Alguien dijo que “lo difícil es entender por qué falla”.')

    def test_valid(self):
        self.assertEqual(lib.validate_variant(self.ORIG, self.GOOD, 2), [])

    def test_rejections(self):
        cases = {
            "links changed": self.GOOD.replace("x.dev/doc", "evil.dev"),
            "figures changed": self.GOOD.replace("250", "300"),
            "inline code changed": self.GOOD.replace("Client", "Other"),
            "quoted text altered": self.GOOD.replace("entender por qué falla", "saber por qué falla"),
            "tag not allowed": self.GOOD + "<script>alert(1)</script>",
            "attribute not allowed": self.GOOD.replace("<code>", '<code class="x">'),
            "markdown leftovers": self.GOOD + " **negrita**",
            "too short": "Según la documentación.",
        }
        for expected, variant in cases.items():
            errs = lib.validate_variant(self.ORIG, variant, 3)
            self.assertTrue(any(expected in e for e in errs), (expected, errs))
        self.assertEqual(lib.validate_variant(self.ORIG, "", 4), ["empty response"])  # Detallado cannot be omitted

    def test_condensing_is_allowed_inventing_is_not(self):
        short = "El sistema procesa 250 mensajes."
        self.assertEqual(lib.validate_variant(self.ORIG, short, 3), [])  # dropped link/code/quote: fine
        self.assertEqual(lib.validate_variant(self.ORIG, "", 1), [])    # omitted at Resumen
        self.assertEqual(lib.validate_variant(self.ORIG, "", 2), [])    # omitted at Sencillo
        self.assertEqual(lib.validate_variant(self.ORIG, "", 3), [])    # omitted at Esencial
        self.assertTrue(any("figures" in e for e in lib.validate_variant(self.ORIG, "El sistema procesa 999 mensajes.", 2)))
        self.assertTrue(any("too long" in e for e in lib.validate_variant(self.ORIG, self.GOOD + " " + self.GOOD, 1)))

    def test_unsafe_href(self):
        orig = '<a href="javascript:alert(1)">x</a> ' + LONG
        errs = lib.validate_variant(orig, orig, 3)
        self.assertIn("unsafe href", errs)


class HashParity(unittest.TestCase):
    def test_python_and_js_hash_agree(self):
        samples = ["hola", "Cuando escribo “x” ñ — 3,5 %", "日本語 テキスト", " a  b "]
        js = ("const a=require('%s');const s=%s;console.log(JSON.stringify(s.map(x=>a.hash(a.normalize(x)))))"
              % (os.path.join(ROOT, "js", "adaptive.js"), json.dumps(samples)))
        try:
            out = subprocess.check_output(["node", "-e", js], text=True)
        except FileNotFoundError:
            self.skipTest("node not installed")
        expected = [lib.fnv1a(lib.normalize_text(s)) for s in samples]
        self.assertEqual(json.loads(out), expected)


class Manifests(unittest.TestCase):
    def test_public_manifest_omits_source_and_empty_blocks(self):
        blocks = [{"id": "b-1", "k": "aa.0", "text": "secreto", "levels": {"1": "u"}},
                  {"id": "b-2", "k": "bb.0", "text": "otro", "levels": {}}]
        pub = lib.public_manifest("s", blocks)
        self.assertEqual(pub["blocks"], [{"id": "b-1", "k": "aa.0", "l": {"1": "u"}}])
        self.assertNotIn("secreto", json.dumps(pub))


class RepoManifests(unittest.TestCase):
    def test_data_list_matches_manifests(self):
        adir = os.path.join(ROOT, "adaptive")
        if not os.path.isdir(adir):
            self.skipTest("no manifests")
        slugs = sorted(f[:-5] for f in os.listdir(adir) if f.endswith(".json"))
        listed = json.load(open(os.path.join(ROOT, "_data", "adaptive.json"), encoding="utf8"))
        self.assertEqual(listed, slugs)

    """Every committed manifest must be in sync with its state and valid."""

    def test_committed_state_is_valid(self):
        state_dir = os.path.join(ROOT, "_adaptive")
        if not os.path.isdir(state_dir):
            self.skipTest("no adaptations committed")
        for name in os.listdir(state_dir):
            state = json.load(open(os.path.join(state_dir, name), encoding="utf8"))
            for b in state["blocks"]:
                for lvl, variant in b["levels"].items():
                    if int(lvl) not in lib.LEVELS:
                        continue
                    self.assertEqual(lib.validate_variant(b["html"], variant, int(lvl)), [], (name, b["id"], lvl))
            pub = json.load(open(os.path.join(ROOT, "adaptive", name), encoding="utf8"))
            self.assertEqual(pub, lib.public_manifest(state["slug"], state["blocks"]), name)


if __name__ == "__main__":
    unittest.main()
