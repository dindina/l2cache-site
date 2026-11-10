// Progressive enhancement only: the page is complete without this script.
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    links.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  var items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("is-visible"); });
    return;
  }
  var list = Array.prototype.slice.call(items);
  // Reveal everything up to the visible item too, so anchor jumps never leave hidden sections above.
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var index = list.indexOf(entry.target);
      list.slice(0, index + 1).forEach(function (el) {
        el.classList.add("is-visible");
        observer.unobserve(el);
      });
    });
  }, { rootMargin: "0px 0px -10% 0px" });
  items.forEach(function (el) { observer.observe(el); });
})();

// Hero live demo (sidebar screens, autoplay), feature tile dialogs, phone swipe dots.
(function () {
  var stage = document.querySelector('.sb');
  var title = stage.querySelector('.sb-title');
  var tabs = Array.prototype.slice.call(stage.querySelectorAll('[role="tab"]'));
  function select(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab, f = t.dataset.feature;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      var pane = document.getElementById('pane-' + f);
      pane.hidden = !on; pane.classList.toggle('is-in', on);
      document.getElementById('cap-' + f).hidden = !on;
      if (on) {
        title.textContent = pane.dataset.title;
        stage.style.setProperty('--sc', getComputedStyle(pane).getPropertyValue('--sc'));
        document.querySelector('.sb-caption-wrap').style.setProperty('--sc', getComputedStyle(pane).getPropertyValue('--sc'));
      }
    });
    if (focus) tab.focus();
  }
  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () { select(tab); });
    tab.addEventListener('keydown', function (e) {
      var d = (e.key === 'ArrowDown' || e.key === 'ArrowRight') ? 1 : (e.key === 'ArrowUp' || e.key === 'ArrowLeft') ? -1 : 0;
      if (d) { e.preventDefault(); select(tabs[(i + d + tabs.length) % tabs.length], true); }
    });
  });
  // Menu links that name a feature without its own sidebar item open the item it lives in.
  var ALIAS = { home: 'today', context: 'agents', 'agent-tools': 'mcp' };
  function fromHash() {
    var h = location.hash.slice(1);
    var t = stage.querySelector('[data-feature="' + (ALIAS[h] || h) + '"]');
    if (t) { select(t); (document.getElementById('features') || stage).scrollIntoView({ block: 'center' }); }
  }
  window.addEventListener('hashchange', fromHash);
  stage.__select = select;
  stage.__alias = ALIAS;
  stage.__tabs = tabs;
  select(tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[0]);
  fromHash();
})();
(function () {
  var fig = document.querySelector('.hero-shot.sb');
  fig.addEventListener('click', function (e) { if (e.target.closest('[role="tab"]')) fig.classList.add('touched'); });
})();
(function () {
  // Feature tiles open the feature carousel at their slide; neighbours peek in and are one click, key or swipe away.
  var dlg = document.querySelector('dialog.feat-dlg');
  if (!dlg) return;
  var track = dlg.querySelector('.feat-track'), slides = Array.prototype.slice.call(track.children);
  var prev = dlg.querySelector('.feat-nav.prev'), next = dlg.querySelector('.feat-nav.next');
  var count = dlg.querySelector('.feat-count'), dots = dlg.querySelector('.feat-dots'), active = -1;
  slides.forEach(function (s, i) {
    var d = document.createElement('i');
    d.addEventListener('click', function () { go(i, true); });
    dots.appendChild(d);
    s.addEventListener('click', function () { if (i !== active) go(i, true); });
  });
  function go(i, smooth) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    var s = slides[i];
    track.scrollTo({ left: s.offsetLeft - (track.clientWidth - s.clientWidth) / 2, behavior: smooth ? 'smooth' : 'auto' });
    mark(i);
  }
  function nearest() {
    var mid = track.scrollLeft + track.clientWidth / 2, best = 0, dist = Infinity;
    slides.forEach(function (s, i) { var d = Math.abs(s.offsetLeft + s.clientWidth / 2 - mid); if (d < dist) { dist = d; best = i; } });
    return best;
  }
  function mark(i) {
    if (i === active) return;
    active = i;
    slides.forEach(function (s, j) { s.classList.toggle('is-active', j === i); s.setAttribute('aria-hidden', String(j !== i)); });
    Array.prototype.forEach.call(dots.children, function (d, j) { d.classList.toggle('on', j === i); });
    count.textContent = (i + 1) + ' / ' + slides.length;
    prev.disabled = i === 0; next.disabled = i === slides.length - 1;
  }
  var settle;
  track.addEventListener('scroll', function () { clearTimeout(settle); settle = setTimeout(function () { mark(nearest()); }, 60); }, { passive: true });
  prev.addEventListener('click', function () { go(active - 1, true); });
  next.addEventListener('click', function () { go(active + 1, true); });
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(active + 1, true); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(active - 1, true); }
  });
  dlg.querySelector('.dlg-close').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target === track || e.target.classList.contains('feat-stage')) dlg.close(); });
  document.querySelectorAll('.bento-card[data-dlg]').forEach(function (card) {
    card.addEventListener('click', function () {
      var i = slides.indexOf(document.getElementById(card.dataset.dlg));
      active = -1;
      dlg.showModal();
      fit();
      requestAnimationFrame(function () { go(i, false); });
    });
  });
  // Shrink each slide's mockup just enough that the whole image is visible without scrolling the slide.
  // Phones stack the text above the mockup, so there the slide scrolls instead of shrinking it unreadably.
  var phone = window.matchMedia('(max-width: 600px)');
  function fit() {
    slides.forEach(function (s) {
      var fig = s.querySelector('figure.stage');
      if (!fig) return;
      fig.style.zoom = '';
      if (phone.matches) return;
      var top = fig.getBoundingClientRect().top - s.getBoundingClientRect().top + s.scrollTop;
      var room = s.clientHeight - top - 24, h = fig.offsetHeight;
      if (h > room) fig.style.zoom = Math.max(0.55, room / h).toFixed(3);
    });
  }
  window.addEventListener('resize', function () { if (dlg.open) { fit(); go(active, false); } });
})();
(function () {
  var fig = document.querySelector('.hero-shot.sb');
  if (!fig || !fig.__select) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var MS = 4500, tabs = fig.__tabs, timer = null, visible = false, hovering = false, stopped = false;
  fig.style.setProperty('--ap-ms', MS + 'ms');
  function current() { return tabs.findIndex(function (t) { return t.getAttribute('aria-selected') === 'true'; }); }
  function schedule() {
    clearTimeout(timer);
    var run = !stopped && visible && !hovering && !document.hidden;
    fig.classList.toggle('paused', !run);
    if (run) timer = setTimeout(function () { fig.__select(tabs[(current() + 1) % tabs.length]); restartBar(); schedule(); }, MS);
  }
  function restartBar() { fig.classList.remove('autoplay'); void fig.offsetWidth; if (!stopped) fig.classList.add('autoplay'); }
  function stop() { stopped = true; clearTimeout(timer); fig.classList.remove('autoplay', 'paused'); }
  // Any real interaction with the demo or its captions hands control to the visitor.
  ['pointerdown', 'keydown'].forEach(function (ev) { fig.addEventListener(ev, stop); });
  document.querySelectorAll('.sbm-more summary').forEach(function (s) { s.addEventListener('click', stop); });
  window.addEventListener('hashchange', stop);
  fig.addEventListener('mouseenter', function () { hovering = true; schedule(); });
  fig.addEventListener('mouseleave', function () { hovering = false; restartBar(); schedule(); });
  document.addEventListener('visibilitychange', schedule);
  new IntersectionObserver(function (es) { visible = es[0].isIntersecting; schedule(); }, { threshold: 0.4 }).observe(fig);
  var h = location.hash.slice(1);
  if (h && fig.querySelector('[data-feature="' + (fig.__alias[h] || h) + '"]')) stop(); else fig.classList.add('autoplay');
})();
(function () {
  var row = document.querySelector('.icon-grid'), dots = document.querySelector('.grid-dots');
  var tiles = Array.prototype.slice.call(row.children);
  tiles.forEach(function () { dots.appendChild(document.createElement('i')); });
  function update() {
    var max = row.scrollWidth - row.clientWidth;
    var i = max <= 2 ? 0 : Math.round((row.scrollLeft / max) * (tiles.length - 1));
    Array.prototype.forEach.call(dots.children, function (d, j) { d.classList.toggle('on', j === i); });
  }
  row.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();

// The token spotlight's "How it works" opens the feature carousel at the Context slide.
(function () {
  var more = document.querySelector('.tk-more');
  if (more) more.addEventListener('click', function () { document.querySelector('.icon-grid [data-feature="context"]').click(); });
})();

// Rotating headline in hero
(function () {
  function initRotator() {
    var headline = document.querySelector('.rotating-headline');
    if (!headline) return;
    var items = headline.querySelectorAll('.rotate-item');
    if (items.length <= 1) return;

    var current = 0;
    var interval = 3000;
    var hovering = false;

    headline.addEventListener('mouseenter', function () { hovering = true; });
    headline.addEventListener('mouseleave', function () { hovering = false; });

    setInterval(function () {
      if (hovering || document.hidden) return;
      items[current].classList.remove('is-active');
      current = (current + 1) % items.length;
      items[current].classList.add('is-active');
    }, interval);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRotator);
  } else {
    initRotator();
  }
})();
