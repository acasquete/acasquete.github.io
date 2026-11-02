# Adaptive Reading

Lets a reader change how deep an article reads: for the whole article (header card, which collapses into a floating pill on scroll) and per paragraph (layers icon in the left margin). Design reference: the "Demo - Prototipo" mock-up.

| Reader level | Manifest variant | Target size | What it does |
|---|---|---|---|
| Sencillo | `1` | ≈8-10% of the words | near-one-liners: each kept block is one short sentence stating the concept; everything else is **omitted**; no images, code or tables |
| Esencial (default) | `2` | ≈45% | the thread of the argument; blocks may be omitted; only the first image |
| Detallado | `3` | ≈75% | almost everything, without repetition; never omits a block |
| Original | (none) | 100% | the author's exact text |

An empty string (`""`) as a variant means "omit this block at this level" (levels 1 and 2 only). Headings whose section ends up empty are hidden too. Condensing is allowed, inventing is not: everything in a variant (figures, links, inline code, quotes) must exist in the original. Reading time per level is computed in the browser from the visible text (same formula as `_includes/read-time.html`), so Sencillo shows far fewer minutes than Original. `generate.py` prints each level's share of the original words and the omitted-block counts after every run.

State: `globalLevel` (saved in `localStorage` as `acn-reading-depth`; default Esencial) and `overrides` (blockId → level, session only). Choosing the article's level in a paragraph removes its override; changing the global level clears all overrides.

## How it works

```
Markdown ──jekyll build──▶ _site/<slug>.html ──generate.py──▶ _adaptive/<slug>.json   (state, versioned, not published)
                                                          └─▶ adaptive/<slug>.json    (trimmed manifest, published)
```

* The generator reads the **built** page, so the text it stores is exactly what the browser sees. The Markdown is never modified.
* Adaptable blocks: paragraphs and list items of 25+ words inside `.content.prose`. Headings, images, tables, code, quotes (`<blockquote>`), footnotes and blocks containing them are left untouched.
* Every block has a **persistent id** (`b-xxxxxx`) kept in `_adaptive/<slug>.json`. On regeneration ids are matched by exact text, then by similarity, so editing or inserting other paragraphs does not change them. The text hash is only a *lookup key* for the browser (`k`), not the identity.
* The browser fetches `/adaptive/<slug>.json` lazily (idle time, or immediately if the saved level is not 5), finds each paragraph by hashing its text and swaps in the variant. If a paragraph was edited after generation its hash no longer matches, so it simply shows the original: a stale variant is never shown.
* Global and per-paragraph controls share the same blocks.

## Generate adaptations for a post

```bash
bundle exec jekyll build              # add --drafts for a draft
python3 scripts/adaptive/generate.py <slug> --dry-run     # plan only, no API calls, writes nothing
export ANTHROPIC_API_KEY=...          # see "Credentials"
python3 scripts/adaptive/generate.py <slug>
bundle exec jekyll build              # a full build is needed once so the page gets data-adaptive
```

`<slug>` is the post URL without the slash (`/vibe-coding-deuda-tecnica` → `vibe-coding-deuda-tecnica`). Commit `_adaptive/<slug>.json` and `adaptive/<slug>.json` together.

## Regenerate when the original changes

Run the same command. Only blocks whose text changed (or that failed before) are sent to the model; unchanged blocks keep their id and variants. `--force` regenerates everything; `--only-levels 1` (or `1,2`) regenerates just those levels and keeps the rest. The summary line reports blocks to generate / reused / orphaned.

`python3 scripts/adaptive/generate.py <slug> --check` validates the stored adaptations against the current page (stale, missing, invalid, orphaned, manifest out of sync) with no API calls; exit code 1 if anything is wrong.

## Credentials and providers

Credentials are read from environment variables only; never put keys in the repo or the frontend.

| Provider | Flag | Variables |
|---|---|---|
| Anthropic (default) | `--provider anthropic` | `ANTHROPIC_API_KEY`, optional `ADAPTIVE_MODEL` (default `claude-sonnet-5-5`), `ANTHROPIC_BASE_URL` |
| OpenAI-compatible | `--provider openai` | `OPENAI_API_KEY`, `ADAPTIVE_MODEL` or `--model`, optional `OPENAI_BASE_URL` |
| Hand-written / tests | `--provider file --variants-file f.json` | none; `f.json` is `{"<block index>": {"1": "<html>", "2": "<html>", "3": "<html>"}}` |

Generation is a manual step; it never runs during a normal Jekyll build.

## Validation (a variant that fails is not published)

Each variant is checked against its original: only `a[href] em strong b i code kbd sup sub br`; no Markdown leftovers; links, inline code, numeric figures and quoted text must be a subset of the original's (nothing new, quotes verbatim); length between 0.04×/0.2×/0.45× (levels 1/2/3) and 1.2×–1.3× the original. On failure the model is asked once more for just the failing levels; if it still fails the level is omitted and the browser shows the original for that block. Errors are kept in `_adaptive/<slug>.json` (`errors`) and printed to stderr.

## Turn it on / off

* Whole site: `adaptive_reading: false` in `_config.yml`.
* One post: `adaptive: false` in its front matter.
* A post is adaptive only if its slug is listed in `_data/adaptive.json` (kept in sync by `generate.py`) and `adaptive/<slug>.json` exists. Remove both to turn that post off.
* Without JavaScript the article is the plain original; the controls are created by `js/adaptive.js`.

## Tests

```bash
python3 -m unittest discover -s scripts/adaptive -v   # extraction, stable ids, validation, JS/Python hash parity, committed manifests
```

## Demo

`_drafts/adaptive-demo.md` (only built with `--drafts`) has hand-written variants (generated with the `file` provider) covering a link, inline code, figures, a quote, a list item and an image. Open `/adaptive-demo` with `bundle exec jekyll serve --drafts`.

## Known limitations / ideas

* **Pinch gesture: not implemented on purpose.** Intercepting a two-finger pinch on a block needs `touch-action` restrictions or `preventDefault` on touch events, which disable native pinch-zoom (an accessibility regression), and Safari/Chrome handle the gesture differently. The contextual slider (popover or bottom sheet when there is no 184px margin) covers the use case. It could be revisited as progressive enhancement using Safari's `gesturechange` only.
* Paragraph overrides are not persisted between visits.
* Block triggers are individually tabbable; on very long articles a "skip" shortcut or roving tabindex would help keyboard users.
* Block quotes, headings, tables and code are never adapted.
* Variants are single-pass model output validated mechanically; a human read-through of generated adaptations before committing is recommended.
