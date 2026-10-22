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

  // Screenshot Carousel Modal
  var modal = document.getElementById("screenshot-modal");
  var modalImg = document.getElementById("modal-image");
  var modalTitle = document.getElementById("modal-title");
  var modalCaption = document.getElementById("modal-caption");
  var modalCounter = document.getElementById("modal-counter");
  var modalDots = document.getElementById("modal-dots");
  var prevBtn = document.getElementById("modal-prev");
  var nextBtn = document.getElementById("modal-next");

  var galleryImages = Array.prototype.slice.call(
    document.querySelectorAll("img[data-gallery='true']")
  );

  if (modal && modalImg && galleryImages.length > 0) {
    var currentIndex = 0;

    // Build navigation dots
    modalDots.innerHTML = "";
    galleryImages.forEach(function (img, i) {
      var dot = document.createElement("button");
      dot.type = "button";
      dot.className = "modal-dot" + (i === 0 ? " is-active" : "");
      dot.setAttribute("role", "tab");
      dot.setAttribute("aria-label", "Screenshot " + (i + 1) + ": " + (img.dataset.title || ""));
      dot.addEventListener("click", function () {
        showIndex(i);
      });
      modalDots.appendChild(dot);
    });

    function getFullSrc(img) {
      return img.dataset.full || img.getAttribute("src");
    }

    function showIndex(i) {
      if (i < 0) i = galleryImages.length - 1;
      if (i >= galleryImages.length) i = 0;
      currentIndex = i;

      var currentImg = galleryImages[currentIndex];
      var title = currentImg.dataset.title || currentImg.alt || "L2Cache Screenshot";
      var caption = currentImg.dataset.caption || currentImg.alt || "";

      modalImg.style.opacity = "0";
      modalImg.style.transform = "scale(0.97)";

      setTimeout(function () {
        modalImg.src = getFullSrc(currentImg);
        modalImg.alt = title;
        modalTitle.textContent = title;
        modalCaption.textContent = caption;
        modalCounter.textContent = (currentIndex + 1) + " / " + galleryImages.length;

        var dots = modalDots.querySelectorAll(".modal-dot");
        dots.forEach(function (d, idx) {
          d.classList.toggle("is-active", idx === currentIndex);
        });

        modalImg.style.opacity = "1";
        modalImg.style.transform = "scale(1)";
      }, 80);
    }

    function openModal(index) {
      showIndex(index);
      if (typeof modal.showModal === "function") {
        modal.showModal();
      } else {
        modal.setAttribute("open", "");
      }
      document.body.style.overflow = "hidden";
    }

    function closeModal() {
      if (typeof modal.close === "function") {
        modal.close();
      } else {
        modal.removeAttribute("open");
      }
      document.body.style.overflow = "";
    }

    // Attach click listeners to all screenshots
    galleryImages.forEach(function (img, index) {
      img.addEventListener("click", function (e) {
        e.preventDefault();
        openModal(index);
      });

      // Keyboard accessibility (Enter / Space to zoom)
      img.setAttribute("role", "button");
      img.setAttribute("tabindex", "0");
      img.setAttribute("aria-haspopup", "dialog");
      img.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          openModal(index);
        }
      });
    });

    // Also allow clicking stage zoom-hint or stage area to open corresponding image
    document.querySelectorAll(".stage").forEach(function (stage) {
      var img = stage.querySelector("img[data-gallery='true']");
      if (!img) return;
      var index = galleryImages.indexOf(img);
      if (index === -1) return;
      var hint = stage.querySelector(".zoom-hint");
      if (hint) {
        hint.style.pointerEvents = "auto";
        hint.style.cursor = "pointer";
        hint.addEventListener("click", function (e) {
          e.stopPropagation();
          openModal(index);
        });
      }
    });

    if (prevBtn) {
      prevBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        showIndex(currentIndex - 1);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        showIndex(currentIndex + 1);
      });
    }

    // Close on backdrop or close button
    modal.querySelectorAll("[data-close-modal]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.stopPropagation();
        closeModal();
      });
    });

    modal.addEventListener("click", function (e) {
      if (e.target === modal || e.target.classList.contains("modal-backdrop") || e.target.classList.contains("modal-viewport")) {
        closeModal();
      }
    });

    modal.addEventListener("close", function () {
      document.body.style.overflow = "";
    });

    // Keyboard shortcuts (ArrowLeft / ArrowRight / Escape)
    window.addEventListener("keydown", function (e) {
      if (!modal.open) return;
      if (e.key === "ArrowRight" || e.key === "l") {
        e.preventDefault();
        showIndex(currentIndex + 1);
      } else if (e.key === "ArrowLeft" || e.key === "h") {
        e.preventDefault();
        showIndex(currentIndex - 1);
      } else if (e.key === "Escape") {
        closeModal();
      }
    });

    // Touch swipe gestures
    var touchStartX = 0;
    var touchStartY = 0;
    modal.addEventListener("touchstart", function (e) {
      if (e.changedTouches && e.changedTouches[0]) {
        touchStartX = e.changedTouches[0].screenX;
        touchStartY = e.changedTouches[0].screenY;
      }
    }, { passive: true });

    modal.addEventListener("touchend", function (e) {
      if (e.changedTouches && e.changedTouches[0]) {
        var diffX = e.changedTouches[0].screenX - touchStartX;
        var diffY = e.changedTouches[0].screenY - touchStartY;
        if (Math.abs(diffX) > 50 && Math.abs(diffX) > Math.abs(diffY)) {
          if (diffX < 0) {
            showIndex(currentIndex + 1);
          } else {
            showIndex(currentIndex - 1);
          }
        }
      }
    }, { passive: true });
  }
})();
