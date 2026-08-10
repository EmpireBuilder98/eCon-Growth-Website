/* CINEMA v5 — TRAILER MODE
   Additive, safe. Injects grain/vignette/scanline overlays and arms
   scroll reveals for content blocks (headings are handled by cinema-v4). */
(function () {
  function mount() {
    // ── overlays ─────────────────────────────────────────────
    if (!document.getElementById('tr-grain')) {
      ['tr-vignette', 'tr-scan', 'tr-grain'].forEach(function (id) {
        var d = document.createElement('div'); d.id = id;
        document.body.appendChild(d);
      });
    }

    // ── scroll reveals ───────────────────────────────────────
    var reduce = window.matchMedia &&
                 window.matchMedia('(prefers-reduced-motion:reduce)').matches;
    if (reduce || !('IntersectionObserver' in window)) return;

    document.documentElement.classList.add('tr-js');

    var sel = [
      '.section p',
      '.section .svc-card', '.section .svc-name', '.section [class*="svc"]',
      '.section [class*="card"]',
      '.section .faq-item',
      '.section a.btn-primary', '.section a.btn-ghost',
      '.section img',
      '.section li',
      '.section .stat'
    ].join(',');

    var els = [].slice.call(document.querySelectorAll(sel)).filter(function (e) {
      // never touch the hero (already animated) or the section headings (v4 owns them)
      return !e.closest('#scroll-hero-sticky') &&
             !e.classList.contains('section-h2') &&
             !e.closest('.section-h2');
    });

    // stagger reveals within each parent section for a cascading "slam-in"
    els.forEach(function (e) {
      e.classList.add('tr-up');
      var sec = e.closest('.section');
      if (sec) {
        if (sec.__tr == null) sec.__tr = 0;
        var i = sec.__tr++;
        e.style.transitionDelay = Math.min(i * 55, 420) + 'ms';
      }
    });

    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('tr-in');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    els.forEach(function (e) { io.observe(e); });

    // safety net: never leave anything hidden
    setTimeout(function () {
      els.forEach(function (e) { e.classList.add('tr-in'); });
    }, 6000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
