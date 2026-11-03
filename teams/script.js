// L2Cache for Teams — waitlist form. Posts JSON to /api/waitlist (api/waitlist.js).
(function () {
  "use strict";

  var form = document.getElementById("waitlist-form");
  if (!form) return;
  var msg = form.querySelector(".form-msg");
  var button = form.querySelector('button[type="submit"]');
  var done = document.querySelector(".done");
  var f = form.elements;
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function checked(name) {
    return Array.prototype.map.call(form.querySelectorAll('input[name="' + name + '"]:checked'), function (el) {
      return el.value;
    });
  }

  function fail(text, field) {
    msg.textContent = text;
    msg.className = "form-msg err";
    if (field) field.focus();
  }

  // Where the visitor came from: utm tags if present, else the referrer's host.
  function source() {
    var params = new URLSearchParams(window.location.search);
    var parts = ["utm_source", "utm_medium", "utm_campaign"]
      .map(function (key) { return params.get(key) ? key + "=" + params.get(key) : ""; })
      .filter(Boolean);
    if (!parts.length && document.referrer) {
      try { parts.push("ref=" + new URL(document.referrer).host); } catch (e) { /* ignore a malformed referrer */ }
    }
    return parts.join("&").slice(0, 300);
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var data = {
      email: f.email.value.trim(),
      name: f["name"].value.trim(),
      company: f.company.value.trim(),
      team_size: f.team_size.value,
      os: checked("os"),
      agents: checked("agents"),
      wanted: checked("wanted"),
      pain: f.pain.value.trim(),
      consent: f.consent.checked,
      website: f.website.value,
      source: source()
    };

    if (!EMAIL.test(data.email)) return fail("Please enter a valid work email.", f.email);
    if (!data.team_size) return fail("Please choose how many developers use coding agents.", f.team_size);
    if (!data.consent) return fail("Please tick the box so we can email you about early access.", f.consent);

    msg.textContent = "";
    msg.className = "form-msg";
    button.disabled = true;
    button.textContent = "Joining…";

    fetch("/api/waitlist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (body) {
          if (!res.ok) throw new Error(body.error || "");
        });
      })
      .then(function () {
        form.hidden = true;
        done.hidden = false;
        done.focus();
      })
      .catch(function (error) {
        button.disabled = false;
        button.textContent = "Join the waitlist";
        fail(error.message || "Something went wrong. Please try again, or email support@amvo.store.");
      });
  });
})();
