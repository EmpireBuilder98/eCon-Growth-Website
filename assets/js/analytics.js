/* ═══════════════════════════════════════════════════════════════════════════
   eCon Growth — site analytics
   ---------------------------------------------------------------------------
   ONE file, loaded by every page. All IDs live in CONFIG below — change them
   here and the whole site follows. Loads Microsoft Clarity (heatmaps, scroll
   depth, session recordings, dead clicks) and GA4 (traffic + conversions),
   then layers on the events that actually matter to this business:

     • card_scan          — a visit to /nampa/, which is only reachable from
                            the printed business-card QR (the page is noindex
                            and linked from nowhere), so a hit ≈ a scan
     • cta_click          — any button press, labelled, with the page it fired on
     • booking_click      — someone left for the booking calendar (the money step)
     • scroll_depth       — 25 / 50 / 75 / 100%, the Nina drop-off signal
     • page_exit          — how long they actually stayed

   Attribution survives the hop: the source that brought someone in is stored
   for the session, so a booking can be traced back to a scanned card.
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var CONFIG = {
    // Microsoft Clarity project id — clarity.microsoft.com → Settings → Setup
    clarityId: "y5len7oie5",
    // GA4 measurement id, looks like G-XXXXXXXXXX
    ga4Id: "GA4_ID_PENDING",
    // Google Ads conversion id, looks like AW-000000000 (optional)
    googleAdsId: "",
    // eCon OS — the CRM keeps its own copy, so the data lives next to the
    // bookings and prospects it should be compared against.
    crmEndpoint: "https://os.econ-growth.com/api/track"
  };

  var isPlaceholder = function (v) { return !v || /_PENDING$/.test(v); };

  // ── Microsoft Clarity ────────────────────────────────────────────────────
  if (!isPlaceholder(CONFIG.clarityId)) {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", CONFIG.clarityId);
  }

  // ── Google Analytics 4 (+ Ads, if set) ───────────────────────────────────
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  if (!isPlaceholder(CONFIG.ga4Id)) {
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + CONFIG.ga4Id;
    document.head.appendChild(s);
    gtag("js", new Date());
    gtag("config", CONFIG.ga4Id);
    if (CONFIG.googleAdsId) gtag("config", CONFIG.googleAdsId);
  }

  // ── a stable id for this visit, so events can be stitched into a session ─
  function sessionId() {
    try {
      var id = sessionStorage.getItem("econ_sid");
      if (!id) {
        id = (Date.now().toString(36) + Math.random().toString(36).slice(2, 10));
        sessionStorage.setItem("econ_sid", id);
      }
      return id;
    } catch (e) { return ""; }
  }

  // ── unified event sink ───────────────────────────────────────────────────
  // Everything goes to all three destinations so no dashboard has a blind
  // spot, and eCon OS holds the durable copy Kris actually owns.
  function track(name, props) {
    props = props || {};
    try { if (window.gtag) window.gtag("event", name, props); } catch (e) {}
    try {
      if (window.clarity) {
        window.clarity("event", name);
        Object.keys(props).forEach(function (k) {
          window.clarity("set", k, String(props[k]));
        });
      }
    } catch (e) {}

    // → the CRM. sendBeacon survives the page being closed, which is the only
    // way page_exit ever arrives; fetch with keepalive is the fallback.
    try {
      if (!CONFIG.crmEndpoint) return;
      var payload = JSON.stringify({
        event: name,
        page: props.page || location.pathname,
        source: props.source || "",
        label: props.label || "",
        href: props.href || "",
        depth: typeof props.depth === "number" ? props.depth : null,
        seconds: typeof props.seconds === "number" ? props.seconds : null,
        session_id: sessionId(),
        referrer: document.referrer || "",
        props: props
      });
      if (navigator.sendBeacon) {
        navigator.sendBeacon(CONFIG.crmEndpoint, new Blob([payload], { type: "text/plain" }));
      } else {
        fetch(CONFIG.crmEndpoint, {
          method: "POST", body: payload, keepalive: true,
          headers: { "Content-Type": "text/plain" }
        }).catch(function () {});
      }
    } catch (e) {}
  }
  window.econTrack = track;

  // ── source attribution, held for the whole session ───────────────────────
  var path = location.pathname.replace(/\/index\.html$/, "/");
  var params = new URLSearchParams(location.search);

  function remember(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  function recall(k) { try { return sessionStorage.getItem(k) || ""; } catch (e) { return ""; } }

  var source = params.get("src") || params.get("utm_source") || "";
  // /nampa/ is noindex and linked from nowhere — arriving there means the QR
  // on a printed business card was scanned.
  var isCardLanding = /^\/nampa\/?$/.test(path);
  if (isCardLanding && !source) source = "business_card_qr";
  if (source && !recall("econ_src")) {
    remember("econ_src", source);
    remember("econ_landing", path);
  }

  var attribution = {
    source: recall("econ_src") || "direct",
    landing_page: recall("econ_landing") || path,
    page: path
  };

  // ── page view + the card-scan event ──────────────────────────────────────
  // Clarity and GA count pageviews on their own; the CRM needs to be told.
  track("page_view", attribution);

  if (isCardLanding) {
    track("card_scan", attribution);
    try { if (window.clarity) window.clarity("set", "campaign", "nampa_business_card"); } catch (e) {}
  }

  // ── clicks: label every CTA, flag the ones that leave for booking ────────
  document.addEventListener("click", function (ev) {
    var el = ev.target && ev.target.closest ? ev.target.closest("a,button") : null;
    if (!el) return;

    var href = (el.getAttribute("href") || "").trim();
    var label = (el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 60);
    var base = { label: label, href: href, page: path, source: attribution.source };

    if (/book\/growth-call|\/book\.html|os\.econ-growth\.com/.test(href)) {
      track("booking_click", base);
    } else if (href.indexOf("tel:") === 0) {
      track("call_click", base);
    } else if (href.indexOf("sms:") === 0) {
      track("text_click", base);
    } else if (href.indexOf("mailto:") === 0) {
      track("email_click", base);
    } else if (el.tagName === "BUTTON" || /btn|cta/i.test(el.className || "")) {
      track("cta_click", base);
    }
  }, true);

  // ── scroll depth: where people quit reading ──────────────────────────────
  var marks = [25, 50, 75, 100], fired = {};
  function onScroll() {
    var doc = document.documentElement;
    var scrollable = doc.scrollHeight - window.innerHeight;
    if (scrollable <= 0) return;
    var pct = Math.round((window.scrollY / scrollable) * 100);
    marks.forEach(function (m) {
      if (pct >= m && !fired[m]) {
        fired[m] = true;
        track("scroll_depth", { depth: m, page: path, source: attribution.source });
      }
    });
  }
  var ticking = false;
  window.addEventListener("scroll", function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () { onScroll(); ticking = false; });
  }, { passive: true });

  // ── time on page, sent on the way out ────────────────────────────────────
  var t0 = Date.now();
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState !== "hidden") return;
    var secs = Math.round((Date.now() - t0) / 1000);
    var depth = marks.filter(function (m) { return fired[m]; }).pop() || 0;
    track("page_exit", { seconds: secs, max_scroll: depth, page: path, source: attribution.source });
  });
})();
