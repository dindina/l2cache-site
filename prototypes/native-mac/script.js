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
