function norm(text) {
	return text.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
}

// Header: shrinks past the hero and shows the reading progress
(function () {
	var header = document.querySelector('.site-header--hero');
	if (header === null) return;

	function update() {
		var y = window.scrollY || 0;
		var max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
		header.classList.toggle('is-scrolled', y > 80);
		header.style.setProperty('--prog', Math.min(1, y / max).toFixed(3));
	}

	window.addEventListener('scroll', update, { passive: true });
	window.addEventListener('resize', update);
	update();
})();

// Mobile menu
(function () {
	var toggle = document.getElementById('menu-toggle');
	var sheet = document.getElementById('mobile-menu');
	var scrim = document.getElementById('menu-scrim');
	var root = document.documentElement;

	function setOpen(open) {
		root.classList.toggle('menu-open', open);
		toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
		toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
	}

	toggle.addEventListener('click', function () {
		setOpen(!root.classList.contains('menu-open'));
	});

	scrim.addEventListener('click', function () {
		setOpen(false);
	});

	document.addEventListener('keydown', function (event) {
		if (event.key === 'Escape' && root.classList.contains('menu-open')) {
			setOpen(false);
			toggle.focus();
		}
	});

	window.matchMedia('(min-width: 521px)').addEventListener('change', function () {
		setOpen(false);
	});

	sheet.querySelectorAll('a').forEach(function (link) {
		link.addEventListener('click', function () {
			setOpen(false);
		});
	});
})();

// Theme: auto, light or dark, cycled from the theme buttons
(function () {
	var names = { auto: 'automático (según el sistema)', light: 'claro', dark: 'oscuro' };
	var next = { auto: 'light', light: 'dark', dark: 'auto' };
	var root = document.documentElement;
	var system = window.matchMedia('(prefers-color-scheme: dark)');
	var buttons = document.querySelectorAll('[data-theme-toggle]');
	var pref = root.getAttribute('data-theme-pref') || 'auto';

	function apply() {
		var label = 'Tema: ' + names[pref] + '. Pulsa para cambiar a ' + names[next[pref]];
		root.setAttribute('data-theme-pref', pref);
		root.classList.toggle('dark', pref === 'dark' || (pref === 'auto' && system.matches));
		buttons.forEach(function (button) {
			button.setAttribute('aria-label', label);
			button.title = label;
		});
	}

	buttons.forEach(function (button) {
		button.addEventListener('click', function () {
			pref = next[pref];
			try {
				localStorage.setItem('acn-theme', pref);
			} catch (e) {}
			apply();
		});
	});

	system.addEventListener('change', apply);
	apply();
})();

// Home carousel
(function () {
	var slides = document.querySelectorAll('.hero .slide');
	var segs = document.querySelectorAll('.hero .seg-btn');
	var items = document.querySelectorAll('.hero .hero-item');
	var search = document.getElementById('search');
	var interval = 7000;
	var idx = 0;
	var timer = null;
	if (slides.length < 2) return;

	function show(next) {
		idx = next;
		slides.forEach(function (slide, i) {
			slide.classList.toggle('is-active', i === idx);
			slide.setAttribute('aria-hidden', i === idx ? 'false' : 'true');
		});
		segs.forEach(function (seg, i) {
			seg.classList.toggle('is-active', i === idx);
			seg.classList.toggle('is-done', i < idx);
			seg.setAttribute('aria-selected', i === idx ? 'true' : 'false');
		});
		items.forEach(function (item, i) {
			item.hidden = i !== idx;
		});
	}

	function start() {
		clearInterval(timer);
		if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
		timer = setInterval(function () {
			if (search !== null && search.open) return;
			show((idx + 1) % slides.length);
		}, interval);
	}

	segs.forEach(function (seg, i) {
		seg.addEventListener('click', function () {
			show(i);
			start();
		});
	});

	start();
})();

// Search dialog
(function () {
	var dialog = document.getElementById('search');
	if (dialog === null) return;

	var input = document.getElementById('search-q');
	var count = document.getElementById('search-count');
	var results = document.getElementById('search-results');
	var posts = null;

	function render() {
		var q = norm(input.value.trim());
		var found = q === '' ? posts.slice(0, 6) : posts.filter(function (post) {
			return norm(post.t + ' ' + post.k).includes(q);
		});
		count.textContent = q === '' ? 'Lo más reciente' : found.length + ' resultados';
		results.textContent = '';
		found.slice(0, 40).forEach(function (post) {
			var link = document.createElement('a');
			link.className = 'res';
			link.href = post.u;
			[['mono', post.d], ['res-title', post.t], ['res-kick', post.k]].forEach(function (part) {
				var span = document.createElement('span');
				span.className = part[0];
				span.textContent = part[1];
				link.appendChild(span);
			});
			results.appendChild(link);
		});
	}

	function open(event) {
		event.preventDefault();
		dialog.showModal();
		document.documentElement.classList.add('search-open');
		input.focus();
		if (posts !== null) return;
		fetch('/search.json').then(function (response) {
			return response.json();
		}).then(function (data) {
			posts = data;
			render();
		}).catch(function () {
			count.textContent = 'No se ha podido cargar el buscador';
		});
	}

	document.querySelectorAll('[data-search-open]').forEach(function (trigger) {
		trigger.addEventListener('click', open);
	});
	document.querySelector('[data-search-close]').addEventListener('click', function () {
		dialog.close();
	});
	dialog.addEventListener('close', function () {
		document.documentElement.classList.remove('search-open');
	});
	input.addEventListener('input', function () {
		if (posts !== null) render();
	});
	document.querySelectorAll('[data-search-chip]').forEach(function (chip) {
		chip.addEventListener('click', function () {
			input.value = chip.dataset.searchChip;
			if (posts !== null) render();
			input.focus();
		});
	});
})();

// Archive: search, topic filters and older notes
(function () {
	var archive = document.getElementById('archive');
	if (archive === null) return;

	var input = document.getElementById('archive-q');
	var count = document.getElementById('archive-count');
	var empty = document.getElementById('archive-empty');
	var more = document.getElementById('archive-more');
	var filters = document.querySelectorAll('[data-topic-filter]');
	var years = archive.querySelectorAll('.year');
	var since = Number(archive.dataset.recentSince);
	var topic = new URLSearchParams(window.location.search).get('tema') || 'todo';
	var expanded = false;

	years.forEach(function (year) {
		year.querySelectorAll('.row').forEach(function (row) {
			row.searchText = norm(row.dataset.search);
		});
	});

	function update() {
		var q = norm(input.value.trim());
		var filtering = q !== '' || topic !== 'todo';
		var shown = 0;

		years.forEach(function (year) {
			var inYear = 0;
			year.querySelectorAll('.row').forEach(function (row) {
				var match = (topic === 'todo' || row.dataset.topic === topic) && row.searchText.includes(q);
				row.hidden = !match;
				if (match) inYear += 1;
			});
			shown += inYear;
			var recent = Number(year.dataset.year) >= since;
			year.hidden = inYear === 0 || !(filtering || expanded || recent);
		});

		count.textContent = filtering ? shown + ' resultados' : archive.dataset.total;
		empty.hidden = shown > 0;
		more.hidden = filtering || expanded;
		filters.forEach(function (filter) {
			filter.setAttribute('aria-pressed', filter.dataset.topicFilter === topic ? 'true' : 'false');
		});
	}

	input.addEventListener('input', update);
	filters.forEach(function (filter) {
		filter.addEventListener('click', function () {
			topic = filter.dataset.topicFilter;
			update();
		});
	});
	more.addEventListener('click', function () {
		expanded = true;
		update();
	});

	update();
})();

// Post: short blockquotes become pull quotes
document.querySelectorAll('.post-column .content > blockquote').forEach(function (quote) {
	if (quote.children.length === 1 && quote.textContent.trim().length < 130) {
		quote.classList.add('is-pull');
	}
});
