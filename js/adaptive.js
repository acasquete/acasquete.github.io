/*
 * Adaptive Reading: lets the reader change how deep an article reads
 * (Sencillo / Esencial / Detallado / Original), for the whole article and per
 * paragraph. "Original" is always the author's exact text. Variants are
 * pre-generated static JSON; nothing is generated in the browser.
 * See scripts/adaptive/README.md.
 */
(function () {
	'use strict';

	var LEVELS = ['sencillo', 'esencial', 'detallado', 'original'];
	var LABELS = ['Sencillo', 'Esencial', 'Detallado', 'Original'];
	// Manifest variants are keyed "1".."3" (generation pipeline, see generate.py).
	// "original" is never stored. An empty string means "omit this block at this level".
	var VARIANT_KEY = ['1', '2', '3', null];
	var DEFAULT_LEVEL = 1; // Esencial
	var STORAGE_KEY = 'acn-reading-depth';
	var ALLOWED = { A: 1, EM: 1, STRONG: 1, B: 1, I: 1, CODE: 1, KBD: 1, SUP: 1, SUB: 1, BR: 1 };
	// Must mirror scripts/adaptive/lib.py
	var FORBIDDEN_INSIDE = 'img,iframe,video,audio,svg,math,script,style,pre,table,blockquote,ul,ol,div,figure,h1,h2,h3,h4,h5,h6,input,button,form,object,embed,canvas,p,li,sup[id],a.footnote,a.reversefootnote,span[class],span[style],.math';
	var EXCLUDED_ANCESTORS = 'blockquote,pre,table,figure,details,aside,nav,footer,header,h1,h2,h3,h4,h5,h6,.underreview,.video-embed,.highlight,.highlighter-rouge,.tags,.footnotes';

	// --- Pure helpers (also exported for tests) ------------------------------

	function normalize(text) {
		return text.normalize('NFC').replace(/[\s﻿]+/g, ' ').trim();
	}

	// 32-bit FNV-1a over UTF-8 bytes. Must match fnv1a() in lib.py.
	function hash(text) {
		var bytes = new TextEncoder().encode(text);
		var h = 0x811c9dc5;
		for (var i = 0; i < bytes.length; i++) {
			h ^= bytes[i];
			h = Math.imul(h, 0x01000193) >>> 0;
		}
		return ('00000000' + h.toString(16)).slice(-8);
	}

	function clampIndex(value) {
		var n = parseInt(value, 10);
		return n >= 0 && n <= 3 ? n : DEFAULT_LEVEL;
	}

	function countWords(text) {
		var t = normalize(text);
		return t ? t.split(' ').length : 0;
	}

	// Same rule as _includes/read-time.html
	function readingMinutes(words) {
		return words < 360 ? 1 : Math.floor(words / 180);
	}

	if (typeof module !== 'undefined' && module.exports) {
		module.exports = {
			normalize: normalize, hash: hash, clampIndex: clampIndex, countWords: countWords,
			readingMinutes: readingMinutes, LEVELS: LEVELS, LABELS: LABELS, VARIANT_KEY: VARIANT_KEY
		};
	}
	if (typeof document === 'undefined') return;

	// --- Boot ------------------------------------------------------------------

	var article = document.getElementById('post-page');
	var src = article && article.getAttribute('data-adaptive');
	var prose = article && article.querySelector('.content.prose');
	if (!src || !prose || !window.fetch) return;

	var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
	var memoryLevel = null;

	function readStoredLevel() {
		try {
			var v = window.localStorage.getItem(STORAGE_KEY);
			var i = LEVELS.indexOf(v);
			if (i >= 0) return i;
		} catch (e) { /* storage unavailable */ }
		return memoryLevel === null ? DEFAULT_LEVEL : memoryLevel;
	}

	function storeLevel(index) {
		memoryLevel = index;
		try { window.localStorage.setItem(STORAGE_KEY, LEVELS[index]); } catch (e) { /* ignore */ }
	}

	var state = {
		globalLevel: readStoredLevel(),
		overrides: new Map(), // block id -> level index (session only)
		blocks: new Map()     // block id -> block record
	};
	var ui = {};
	var openId = null;
	var totalWords = 0;
	var levelMinutes = [1, 1, 1, 1];
	var hiddenExtraWords = 0; // code/tables dropped at Sencillo
	var mediaEls = [];        // images and other figures
	var extraEls = [];        // code blocks, tables, rules, embeds

	if (state.globalLevel < 3) {
		prose.classList.add('ar-loading');
		window.setTimeout(function () { prose.classList.remove('ar-loading'); }, 1500);
	}

	function start() {
		fetch(src, { credentials: 'same-origin' })
			.then(function (r) {
				if (!r.ok) throw new Error('HTTP ' + r.status);
				return r.json();
			})
			.then(init)
			.catch(function () { prose.classList.remove('ar-loading'); });
	}

	if (state.globalLevel < 3 || !('requestIdleCallback' in window)) {
		start();
	} else {
		window.requestIdleCallback(start, { timeout: 1500 });
	}

	// --- Matching blocks -------------------------------------------------------

	function collectBlocks(manifest) {
		var byKey = new Map();
		manifest.blocks.forEach(function (b) { byKey.set(b.k, b); });
		var seen = {};
		var found = [];
		prose.querySelectorAll('p, li').forEach(function (el) {
			var anc = el.closest(EXCLUDED_ANCESTORS);
			if (anc && anc !== prose && prose.contains(anc)) return;
			if (el.querySelector(FORBIDDEN_INSIDE)) return;
			var text = normalize(el.textContent);
			if (!text) return;
			var h = hash(text);
			var occ = seen[h] || 0;
			seen[h] = occ + 1;
			var entry = byKey.get(h + '.' + occ);
			if (entry) found.push({ el: el, entry: entry, words: countWords(text) });
		});
		return found;
	}

	// --- Variants --------------------------------------------------------------

	function sanitize(html) {
		var tpl = document.createElement('template');
		tpl.innerHTML = html;
		(function walk(node) {
			Array.prototype.slice.call(node.childNodes).forEach(function (child) {
				if (child.nodeType === 3) return;
				if (child.nodeType !== 1) { node.removeChild(child); return; }
				walk(child);
				if (!ALLOWED[child.tagName]) {
					while (child.firstChild) node.insertBefore(child.firstChild, child);
					node.removeChild(child);
					return;
				}
				Array.prototype.slice.call(child.attributes).forEach(function (attr) {
					var ok = child.tagName === 'A' && attr.name === 'href' &&
						/^(https?:|mailto:|\/|#|\.\.?\/)/i.test(attr.value.trim());
					if (!ok) child.removeAttribute(attr.name);
				});
				if (child.tagName === 'A' && !child.hasAttribute('href')) {
					while (child.firstChild) node.insertBefore(child.firstChild, child);
					node.removeChild(child);
				} else if (child.tagName === 'CODE') {
					child.className = 'language-plaintext highlighter-rouge';
				}
			});
		})(tpl.content);
		return tpl.content;
	}

	// undefined: show the original; '': omit the block; otherwise the variant HTML.
	function variantFor(b, index) {
		var key = VARIANT_KEY[index];
		if (!key || !Object.prototype.hasOwnProperty.call(b.entry.l, key)) return undefined;
		return b.entry.l[key];
	}

	function effectiveLevel(id) {
		return state.overrides.has(id) ? state.overrides.get(id) : state.globalLevel;
	}

	// --- Reading time ----------------------------------------------------------

	function computeReadingTimes(blocks) {
		var base = totalWords;
		blocks.forEach(function (b) { base -= b.words; });
		for (var i = 0; i < 4; i++) {
			var words = base;
			blocks.forEach(function (b) {
				var v = variantFor(b, i);
				words += v === undefined ? b.words : (v ? countWords(sanitize(v).textContent) : 0);
			});
			if (i === 0) words -= hiddenExtraWords;
			levelMinutes[i] = readingMinutes(Math.max(words, 0));
		}
	}

	function timeLabel(index) { return levelMinutes[index] + ' min'; }

	// --- Rendering -------------------------------------------------------------

	var swapCount = 0;

	function renderBlock(id, animate) {
		var b = state.blocks.get(id);
		var level = effectiveLevel(id);
		var variant = variantFor(b, level);
		var omit = variant === '';
		var custom = state.overrides.has(id);
		var shown = variant === undefined ? 3 : level; // missing variant: show the original
		var key = shown + (omit ? 'omit' : '');
		if (b.shown !== key) {
			b.shown = key;
			b.content.textContent = '';
			if (shown === 3) {
				b.nodes.forEach(function (n) { b.content.appendChild(n); });
			} else if (omit) {
				b.content.textContent = 'Omitido en este nivel';
			} else {
				b.content.appendChild(sanitize(variant));
			}
			b.el.setAttribute('data-ar-level', LEVELS[shown]);
			if (animate && !reduceMotion) {
				swapCount++;
				b.content.style.animation = 'ar-txt-' + (swapCount % 2 ? 'a' : 'b') + ' 380ms ease both';
			}
		}
		b.omitted = omit;
		// An omitted block disappears, unless the reader picked that level for it (or is adjusting it).
		b.el.classList.toggle('ar-gone', omit && !custom && openId !== id);
		b.el.classList.toggle('ar-omitted', omit);
		b.el.classList.toggle('ar-custom', custom);
		b.badge.textContent = custom ? LABELS[level] : '';
		syncBlockSlider(b);
	}

	function renderAll(animate) {
		state.blocks.forEach(function (b, id) { renderBlock(id, animate); });
		syncExtras();
	}

	// Sencillo: no images, code or tables. Esencial: only the first image.
	// Headings whose section ends up empty are hidden too.
	function isGone(node) {
		if (node.classList.contains('ar-gone') || node.classList.contains('ar-hide')) return true;
		if (node.matches('ul, ol')) {
			var items = node.querySelectorAll('li');
			return items.length > 0 && Array.prototype.every.call(items, function (li) { return li.classList.contains('ar-gone'); });
		}
		return false;
	}

	function syncExtras() {
		var g = state.globalLevel;
		mediaEls.forEach(function (m, i) { m.classList.toggle('ar-hide', g === 0 || (g === 1 && i > 0)); });
		extraEls.forEach(function (x) { x.classList.toggle('ar-hide', g === 0); });
		var heads = Array.prototype.slice.call(prose.querySelectorAll(':scope > h1, :scope > h2, :scope > h3, :scope > h4, :scope > h5, :scope > h6')).reverse();
		heads.forEach(function (h) {
			var n = parseInt(h.tagName.charAt(1), 10);
			var visible = false;
			for (var sib = h.nextElementSibling; sib; sib = sib.nextElementSibling) {
				var m = /^H([1-6])$/.exec(sib.tagName);
				if (m && parseInt(m[1], 10) <= n) break;
				if (!isGone(sib)) { visible = true; break; }
			}
			h.classList.toggle('ar-gone', !visible);
		});
	}

	// Height animation: the wrapper animates between the measured heights.
	function fitHeight(b) {
		var h = b.content.offsetHeight;
		if (h && b.text.style.height !== h + 'px') b.text.style.height = h + 'px';
	}

	// --- Scroll anchoring ------------------------------------------------------

	var anchorLoop = null;
	function stopAnchor() {
		if (anchorLoop) { cancelAnimationFrame(anchorLoop.raf); anchorLoop = null; }
	}
	['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (evt) {
		window.addEventListener(evt, stopAnchor, { passive: true });
	});

	// Keeps `anchor` at the same viewport position while heights animate.
	function holdAnchor(anchor) {
		stopAnchor();
		if (!anchor) return;
		var top0 = anchor.getBoundingClientRect().top;
		var until = performance.now() + (reduceMotion ? 80 : 480);
		var loop = { raf: 0 };
		anchorLoop = loop;
		(function tick(now) {
			var delta = anchor.getBoundingClientRect().top - top0;
			if (Math.abs(delta) > 0.5) window.scrollBy(0, delta);
			if (now < until && anchorLoop === loop) loop.raf = requestAnimationFrame(tick);
			else if (anchorLoop === loop) anchorLoop = null;
		})(performance.now());
	}

	function firstVisibleBlock() {
		var top = ui.topOffset || 0;
		var list = Array.from(state.blocks.values());
		for (var i = 0; i < list.length; i++) {
			if (list[i].el.getBoundingClientRect().bottom > top + 8) return list[i].el;
		}
		return null;
	}

	// --- Slider component (header, pill and per-paragraph) ---------------------

	function el(tag, cls, attrs) {
		var node = document.createElement(tag);
		if (cls) node.className = cls;
		if (attrs) Object.keys(attrs).forEach(function (k) { node.setAttribute(k, attrs[k]); });
		return node;
	}

	function createSlider(opts) {
		var root = el('div', 'ar-slider ar-slider--' + (opts.vertical ? 'v' : 'h') + (opts.cls ? ' ' + opts.cls : ''));
		var box = el('div', 'ar-sl-box');
		var track = el('span', 'ar-sl-track', { 'aria-hidden': 'true' });
		var fill = el('span', 'ar-sl-fill', { 'aria-hidden': 'true' });
		box.appendChild(track);
		box.appendChild(fill);
		var dots = [];
		for (var i = 0; i < 4; i++) {
			var d = el('span', 'ar-sl-dot', { 'aria-hidden': 'true' });
			d.style.setProperty('--p', (i / 3 * 100) + '%');
			box.appendChild(d);
			dots.push(d);
		}
		var thumb = el('span', 'ar-sl-thumb', { 'aria-hidden': 'true' });
		box.appendChild(thumb);
		var input = el('input', 'ar-sl-input', { type: 'range', min: '0', max: '3', step: '1' });
		if (opts.id) input.id = opts.id;
		if (opts.ariaLabel) input.setAttribute('aria-label', opts.ariaLabel);
		box.appendChild(input);
		root.appendChild(box);
		input.addEventListener('input', function () { opts.onInput(parseInt(input.value, 10)); });
		input.addEventListener('focus', function () { root.classList.add('is-focus'); });
		input.addEventListener('blur', function () { root.classList.remove('is-focus'); });
		input.addEventListener('pointerdown', function () { root.classList.add('is-drag'); });
		['pointerup', 'pointercancel', 'blur'].forEach(function (evt) {
			input.addEventListener(evt, function () { root.classList.remove('is-drag'); });
		});
		return {
			root: root, input: input,
			// o: {value, valueText, accent (bool), globalMark (index|null), filled (bool)}
			set: function (o) {
				input.value = String(o.value);
				input.setAttribute('aria-valuetext', o.valueText);
				root.style.setProperty('--p', (o.value / 3 * 100) + '%');
				root.classList.toggle('is-accent', !!o.accent);
				dots.forEach(function (d, j) {
					d.classList.toggle('is-reached', o.filled === false ? false : j <= o.value);
					d.classList.toggle('is-global', o.globalMark === j);
				});
				fill.style.setProperty('--fill', o.filled === false ? '0%' : (o.value / 3 * 100) + '%');
			}
		};
	}

	// --- Header card + floating pill -------------------------------------------

	function setGlobalUi() {
		var g = state.globalLevel;
		var o = { value: g, valueText: LABELS[g], accent: false, globalMark: null, filled: true };
		ui.headSlider.set(o);
		ui.pillSlider.set(o);
		ui.headLabels.forEach(function (l, i) { l.classList.toggle('is-active', i === g); });
		ui.pillName.textContent = LABELS[g];
		ui.pillTime.textContent = timeLabel(g);
		if (ui.metaTime) ui.metaTime.nodeValue = ' · ' + levelMinutes[g] + ' min de lectura';
	}

	function announce(message) {
		ui.live.textContent = '';
		window.setTimeout(function () { ui.live.textContent = message; }, 30);
	}

	function setGlobal(index, persist) {
		index = clampIndex(index);
		if (index === state.globalLevel && !state.overrides.size) return;
		closePanel(false);
		var anchor = firstVisibleBlock();
		state.globalLevel = index;
		state.overrides.clear();
		if (persist !== false) storeLevel(index);
		renderAll(true);
		setGlobalUi();
		holdAnchor(anchor);
		announce('Nivel del artículo: ' + LABELS[index] + ', ' + timeLabel(index) + ' de lectura');
	}

	function buildHeader() {
		var anchorNode = article.querySelector('.post-meta') || article.querySelector('.post-head > *:last-child');
		var timeNode = anchorNode.querySelector('time');
		ui.metaTime = null;
		if (timeNode) {
			var n = timeNode.nextSibling;
			while (n && !(n.nodeType === 3 && /de lectura/.test(n.nodeValue))) n = n.nextSibling;
			ui.metaTime = n || null;
		}

		var card = el('div', 'ar-card');
		card.setAttribute('role', 'group');
		var label = el('label', 'ar-card__label');
		label.setAttribute('for', 'ar-level-article');
		label.textContent = 'Nivel de lectura';
		ui.headSlider = createSlider({ id: 'ar-level-article', onInput: onArticleInput, cls: 'ar-slider--head' });
		var labels = el('div', 'ar-card__labels', { 'aria-hidden': 'true' });
		ui.headLabels = LABELS.map(function (name) {
			var s = el('span'); s.textContent = name; labels.appendChild(s); return s;
		});
		card.appendChild(label);
		card.appendChild(ui.headSlider.root);
		card.appendChild(labels);
		anchorNode.parentNode.insertBefore(card, anchorNode.nextSibling);
		ui.card = card;

		var pill = el('div', 'ar-pill', { 'aria-hidden': 'true' });
		pill.setAttribute('role', 'group');
		pill.setAttribute('aria-label', 'Nivel de lectura del artículo');
		ui.pillName = el('span', 'ar-pill__name');
		ui.pillSlider = createSlider({ ariaLabel: 'Nivel de lectura del artículo', onInput: onArticleInput, cls: 'ar-slider--pill' });
		ui.pillTime = el('span', 'ar-pill__time');
		pill.appendChild(ui.pillName);
		pill.appendChild(ui.pillSlider.root);
		pill.appendChild(el('span', 'ar-pill__sep', { 'aria-hidden': 'true' }));
		pill.appendChild(ui.pillTime);
		document.body.appendChild(pill);
		ui.pill = pill;

		ui.live = el('div', 'ar-sr', { role: 'status', 'aria-live': 'polite' });
		document.body.appendChild(ui.live);

		var hdr = document.getElementById('header');
		function measure() {
			ui.topOffset = hdr ? hdr.getBoundingClientRect().height : 0;
			pill.style.setProperty('--ar-top', ui.topOffset + 'px');
		}
		measure();
		window.addEventListener('resize', measure);

		if ('IntersectionObserver' in window) {
			var io = new IntersectionObserver(function (entries) {
				var e = entries[entries.length - 1];
				var past = !e.isIntersecting && e.boundingClientRect.bottom < (ui.topOffset || 0) + 8;
				pill.classList.toggle('is-shown', past);
				pill.setAttribute('aria-hidden', past ? 'false' : 'true');
				card.classList.toggle('is-collapsed', past);
			}, { rootMargin: '-' + Math.round(ui.topOffset || 0) + 'px 0px 0px 0px', threshold: 0 });
			io.observe(card);
		}
	}

	function onArticleInput(index) { setGlobal(index); }

	// --- Per-paragraph control -------------------------------------------------

	function syncBlockSlider(b) {
		var id = b.id;
		var level = effectiveLevel(id);
		var custom = state.overrides.has(id);
		b.slider.set({
			value: level,
			valueText: custom ? LABELS[level] : 'Nivel del artículo (' + LABELS[state.globalLevel] + ')',
			accent: custom,
			globalMark: state.globalLevel,
			filled: custom
		});
		b.labels.forEach(function (s, j) { s.classList.toggle('is-active', j === level); });
		b.el.classList.toggle('ar-custom', custom);
		b.icon.classList.toggle('is-custom', custom);
		b.badge.classList.toggle('is-on', custom && openId !== id);
	}

	function onBlockInput(id, index) {
		if (index === state.globalLevel) state.overrides.delete(id); else state.overrides.set(id, index);
		renderBlock(id, true);
		announce('Párrafo: ' + LABELS[index]);
	}

	function openPanel(id, focusSlider) {
		if (openId === id) return;
		closePanel(false);
		openId = id;
		var b = state.blocks.get(id);
		b.el.classList.add('ar-open');
		b.icon.setAttribute('aria-expanded', 'true');
		b.panel.setAttribute('aria-hidden', 'false');
		syncBlockSlider(b);
		if (focusSlider) b.slider.input.focus({ preventScroll: true });
	}

	function closePanel(restoreFocus) {
		if (openId === null) return;
		var b = state.blocks.get(openId);
		openId = null;
		b.el.classList.remove('ar-open');
		b.icon.setAttribute('aria-expanded', 'false');
		b.panel.setAttribute('aria-hidden', 'true');
		renderBlock(b.id, false);
		syncExtras();
		if (restoreFocus) b.icon.focus({ preventScroll: true });
		else if (b.panel.contains(document.activeElement)) document.activeElement.blur();
	}

	var marginQuery = window.matchMedia('(min-width: 1200px)');
	var hoverQuery = window.matchMedia('(hover: hover)');

	function wireBlock(found) {
		var elBlock = found.el;
		var id = found.entry.id;
		var b = { id: id, el: elBlock, entry: found.entry, words: found.words, shown: 3 };

		var nodes = Array.prototype.slice.call(elBlock.childNodes);
		var text = el('span', 'ar-text');
		var content = el('span', 'ar-content');
		nodes.forEach(function (n) { content.appendChild(n); });
		text.appendChild(content);
		elBlock.appendChild(text);

		var margin = el('span', 'ar-margin');
		var icon = el('button', 'ar-icon', {
			type: 'button', 'aria-label': 'Ajustar la profundidad de este párrafo',
			'aria-expanded': 'false', 'aria-haspopup': 'true'
		});
		icon.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l9 4.5-9 4.5-9-4.5z"/><path d="M3 12l9 4.5 9-4.5"/><path d="M3 16.5l9 4.5 9-4.5"/></svg>';
		var badge = el('span', 'ar-badge', { 'aria-hidden': 'true' });
		var panel = el('span', 'ar-panel', { role: 'group', 'aria-label': 'Nivel de este párrafo', 'aria-hidden': 'true' });
		var row = el('span', 'ar-panel__row');
		var labelsCol = el('span', 'ar-panel__labels', { 'aria-hidden': 'true' });
		b.labels = LABELS.map(function (name, j) {
			var s = el('span'); s.textContent = name; s.style.setProperty('--p', (j / 3 * 100) + '%'); labelsCol.appendChild(s); return s;
		});
		b.slider = createSlider({ vertical: true, ariaLabel: 'Nivel de este párrafo', onInput: function (i) { onBlockInput(id, i); } });
		row.appendChild(labelsCol);
		row.appendChild(b.slider.root);
		panel.appendChild(row);
		margin.appendChild(icon);
		margin.appendChild(badge);
		margin.appendChild(panel);
		elBlock.appendChild(margin);

		b.text = text; b.content = content; b.nodes = nodes; b.icon = icon; b.badge = badge; b.panel = panel;
		elBlock.classList.add('ar-block');
		elBlock.setAttribute('data-ar-id', id);
		state.blocks.set(id, b);

		// Hover: the icon shows on the row; the panel opens only from the margin.
		elBlock.addEventListener('mouseenter', function () {
			if (hoverQuery.matches) elBlock.classList.add('ar-hover');
		});
		elBlock.addEventListener('mouseleave', function () {
			elBlock.classList.remove('ar-hover');
			if (openId === id && !panel.contains(document.activeElement)) closePanel(false);
		});
		margin.addEventListener('mouseenter', function () {
			if (hoverQuery.matches && marginQuery.matches) openPanel(id, false);
		});
		margin.addEventListener('mouseleave', function () {
			if (openId === id && !panel.contains(document.activeElement)) closePanel(false);
		});
		icon.addEventListener('click', function (e) {
			e.stopPropagation();
			if (openId === id) closePanel(false); else openPanel(id, e.detail === 0);
		});
		elBlock.addEventListener('keydown', function (e) {
			if (e.key === 'Escape' && openId === id) { e.stopPropagation(); closePanel(true); }
		});
		margin.addEventListener('focusout', function (e) {
			if (openId === id && !margin.contains(e.relatedTarget) && e.relatedTarget !== null) closePanel(false);
		});

		if (window.ResizeObserver) {
			b.ro = new ResizeObserver(function () { fitHeight(b); });
			b.ro.observe(content);
		}
	}

	// --- Init ------------------------------------------------------------------

	function collectExtras() {
		var seen = new Set();
		prose.querySelectorAll('img').forEach(function (img) {
			if (img.closest('.ar-block')) return;
			var c = img.closest('figure') || img.closest('p') || img;
			if (!seen.has(c)) { seen.add(c); mediaEls.push(c); }
		});
		var sel = '.highlighter-rouge, pre, table, hr, iframe, video, .video-embed';
		prose.querySelectorAll(sel).forEach(function (x) {
			var parent = x.parentElement && x.parentElement.closest(sel);
			if (parent && prose.contains(parent)) return;
			extraEls.push(x);
			if (x.matches('pre, table, .highlighter-rouge')) hiddenExtraWords += countWords(x.textContent);
		});
	}

	var touchActive = null;

	function init(manifest) {
		var found = collectBlocks(manifest);
		if (!found.length) { prose.classList.remove('ar-loading'); return; }
		totalWords = countWords(prose.textContent);
		collectExtras();
		found.forEach(wireBlock);
		computeReadingTimes(Array.from(state.blocks.values()));

		buildHeader();
		article.classList.add('ar-ready');

		// First paint without transitions, then enable them.
		prose.classList.add('ar-instant');
		var first = firstVisibleBlock();
		renderAll(false);
		state.blocks.forEach(function (b) { b.text.style.height = b.content.offsetHeight + 'px'; });
		setGlobalUi();
		holdAnchor(first);
		prose.classList.remove('ar-loading');
		requestAnimationFrame(function () {
			requestAnimationFrame(function () { prose.classList.remove('ar-instant'); });
		});
		if (document.fonts && document.fonts.ready) {
			document.fonts.ready.then(function () { state.blocks.forEach(fitHeight); });
		}

		document.addEventListener('click', function (e) {
			if (openId && !e.target.closest('.ar-panel') && !e.target.closest('.ar-icon')) closePanel(false);
			if (hoverQuery.matches) return;
			var block = e.target.closest('.ar-block');
			var interactive = e.target.closest('a, button, .ar-panel');
			var hasSelection = window.getSelection && String(window.getSelection()).length > 0;
			if (touchActive && touchActive !== block) { touchActive.classList.remove('ar-touch'); touchActive = null; }
			if (block && !interactive && !hasSelection) {
				block.classList.toggle('ar-touch');
				touchActive = block.classList.contains('ar-touch') ? block : null;
			}
		});
		document.addEventListener('keydown', function (e) {
			if (e.key === 'Escape' && openId) closePanel(true);
		});
	}
})();
