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
  function fromHash() {
    var t = stage.querySelector('[data-feature="' + location.hash.slice(1) + '"]');
    if (t) { select(t); (document.getElementById('features') || stage).scrollIntoView({ block: 'center' }); }
  }
  window.addEventListener('hashchange', fromHash);
  stage.__select = select;
  stage.__tabs = tabs;
  select(tabs[0]);
  fromHash();
})();
(function () {
  var fig = document.querySelector('.hero-shot.sb');
  fig.addEventListener('click', function (e) { if (e.target.closest('[role="tab"]')) fig.classList.add('touched'); });
})();
(function () {
  // Feature tiles open their full section in a dialog, in place.
  document.querySelectorAll('.bento-card[data-dlg]').forEach(function (card) {
    card.addEventListener('click', function () { document.getElementById(card.dataset.dlg).showModal(); });
  });
  document.querySelectorAll('dialog.bento-dlg').forEach(function (d) {
    d.querySelector('.dlg-close').addEventListener('click', function () { d.close(); });
    d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
  });
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
  if (location.hash && fig.querySelector('[data-feature="' + location.hash.slice(1) + '"]')) stop(); else fig.classList.add('autoplay');
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
