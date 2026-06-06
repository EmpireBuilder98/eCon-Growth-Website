/* ============================================================
   CINEMA V3 — "Movie Grade" additive controller
   Layers on cinema-v2 without touching it. Safe to remove.
   Kill switch: window.CINE3_OFF = true  (before this loads)
   ============================================================ */
(function () {
  "use strict";
  if (window.CINE3_OFF) return;
  if (window.__cine3) return;            // guard double-load
  window.__cine3 = true;

  var reduce = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function el(cls, html) {
    var n = document.createElement("div");
    n.className = cls;
    if (html) n.innerHTML = html;
    return n;
  }

  function boot() {
    var body = document.body;

    /* ---- 1. grain + vignette + flare overlays ---- */
    var grain = el("cine3-grain");
    var vign = el("cine3-vignette");
    var flare = el("cine3-flare");
    body.appendChild(vign);
    body.appendChild(grain);
    body.appendChild(flare);

    /* ---- 2. chapter title cards ---- */
    var card = el("cine3-titlecard",
      '<div class="cine3-tc-num"></div>' +
      '<div class="cine3-tc-name"></div>' +
      '<div class="cine3-tc-wipe"></div>');
    body.appendChild(card);
    var numEl = card.querySelector(".cine3-tc-num");
    var nameEl = card.querySelector(".cine3-tc-name");

    var sections = [].slice.call(
      document.querySelectorAll("section[data-chapter]"));
    // skip the hero ("Open") so we don't curtain the landing
    var chapters = sections.filter(function (s) {
      return (s.getAttribute("data-chapter") || "").toLowerCase() !== "open";
    });

    var shownFor = null, hideT = null, lastY = window.scrollY;
    function showCard(name, idx) {
      if (shownFor === name) return;
      shownFor = name;
      numEl.textContent = "Ch. " + ("0" + idx).slice(-2);
      nameEl.textContent = name;
      // restart wipe
      card.classList.remove("show");
      void card.offsetWidth;
      card.classList.add("show");
      clearTimeout(hideT);
      hideT = setTimeout(function () { card.classList.remove("show"); },
        reduce ? 1000 : 1400);
    }

    var io = new IntersectionObserver(function (entries) {
      var goingDown = window.scrollY >= lastY;
      lastY = window.scrollY;
      if (!goingDown) return;            // only announce on the way down
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var name = e.target.getAttribute("data-chapter");
        var idx = chapters.indexOf(e.target) + 1;
        if (idx > 0) showCard(name.toUpperCase(), idx);
        // fire anamorphic flare on key moments
        if (e.target.hasAttribute("data-keymoment") && !reduce) {
          flare.classList.remove("fire");
          void flare.offsetWidth;
          flare.classList.add("fire");
        }
      });
    }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
    chapters.forEach(function (s) { io.observe(s); });

    /* ---- 3. end-title credit roll (built into footer) ---- */
    var credits = el("cine3-credits",
      '<div class="cr-fin">FIN.</div>' +
      row("The Operating System", "ECON GROWTH") +
      row("Founders", "Kristopher Cravens · Watson Wheeler") +
      row("Operations Layer", "Run themselves") +
      row("Marketing Layer", "Compounds") +
      row("Financial Layer", "Holds under pressure") +
      row("Flagship Product", "Command HVAC") +
      '<div class="cr-rule"></div>' +
      '<div class="cr-tag">AI Operating Systems for Serious Operators</div>');
    function row(role, name) {
      return '<div class="cr-row"><div class="cr-role">' + role +
        '</div><div class="cr-name">' + name + "</div></div>";
    }
    var footer = document.querySelector("footer") ||
      document.querySelector(".final-cta");
    if (footer && footer.parentNode) {
      footer.parentNode.insertBefore(credits, footer);
      var cio = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) { credits.classList.add("show"); cio.disconnect(); }
        });
      }, { threshold: 0.25 });
      cio.observe(credits);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
