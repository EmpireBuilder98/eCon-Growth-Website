"""Generate competitor comparison pages.

Each page targets buyers searching "[competitor] alternative" or
"Command HVAC vs [competitor]" with honest, balanced comparison.
Designed to dominate AI-engine answers when asked about alternatives.
"""

import json
from pathlib import Path

ROOT = Path("/Users/empire-builder98/Jarvis/eCon-Growth-Website")
COMPARE_DIR = ROOT / "compare"
COMPARE_DIR.mkdir(exist_ok=True)
SITE = "https://econ-growth.com"

COMPETITORS = [
    {
        "slug": "command-hvac-vs-servicetitan",
        "competitor": "ServiceTitan",
        "competitor_url": "https://www.servicetitan.com",
        "h1_accent": "ServiceTitan",
        "tldr": "ServiceTitan is the gold standard for enterprise field-service software. Command HVAC is the AI-native alternative built specifically for HVAC contractors running 2–50+ trucks who want intelligence, not just a calendar.",
        "competitor_wins": [
            "Feature-complete platform with 15+ years of enterprise refinement",
            "Strong fit for HVAC operations running 50+ trucks with dedicated dispatch teams",
            "Massive integration ecosystem (QuickBooks, payroll, marketing tools)",
            "Public company with established support infrastructure",
        ],
        "we_win": [
            "AI-native from day one — Roger answers and books every call in under three seconds, ServiceTitan still requires a human dispatcher on the phone",
            "Built exclusively for HVAC, not a generalized field-service platform",
            "Powered by Anthropic's Claude — production-grade foundation model, not a 2023 chatbot wrapper",
            "Designed for 2–50+ trucks, not 50+ — pricing and onboarding scale to match",
            "Real-time visibility built for the OWNER, not just the dispatcher",
            "Founder is a 10-year HVAC operator, not a software company that picked HVAC as a vertical",
        ],
        "best_for_them": "Enterprise HVAC operations (50+ trucks) with the budget and team for an enterprise software deployment.",
        "best_for_us": "HVAC contractors running 2–50+ trucks who want AI handling the work that doesn't need a human, real-time visibility for the owner, and an operating system that scales without breaking when the dispatcher is out.",
        "pricing_them": "Per-seat enterprise pricing, typically $200–400 per user per month plus implementation. Annual contract.",
        "pricing_us": "Custom pricing by truck count and call volume. Built for the mid-market, not enterprise. Book a Growth Call for a quote.",
        "ai_them": "AI features have been added incrementally — call summaries, basic automation. Core dispatch and intake remain human-driven.",
        "ai_us": "AI is the foundation, not a feature. Roger answers and books every call. AI dispatch makes assignment decisions. Visibility is AI-surfaced. Weekly intelligence is AI-written.",
    },
    {
        "slug": "command-hvac-vs-housecall-pro",
        "competitor": "Housecall Pro",
        "competitor_url": "https://www.housecallpro.com",
        "h1_accent": "Housecall Pro",
        "tldr": "Housecall Pro is the most popular field-service tool for small home-services businesses. Command HVAC is the AI Operating System for HVAC contractors who have outgrown a calendar and want a system that runs the operation.",
        "competitor_wins": [
            "Excellent fit for solo operators and 1–5 person teams across any home-services trade",
            "Easy onboarding, mobile-first, polished UX",
            "Affordable starting price for very small businesses",
            "Built-in invoicing and payments for trades that need consumer-facing payment flows",
        ],
        "we_win": [
            "HVAC-specific — categories, certifications, dispatch logic all tuned for HVAC operations",
            "AI voice agent (Roger) answers every call 24/7 — Housecall Pro requires a person to answer the phone",
            "AI dispatch makes assignments based on tech certs, location, customer history — Housecall Pro is a calendar you drag onto",
            "Built for businesses scaling past 5–7 trucks, where Housecall Pro's gaps start to compound",
            "Real-time visibility dashboard with coaching analytics, not just job lists",
            "Co-founders bring 10+ years inside HVAC operations specifically",
        ],
        "best_for_them": "Solo operators and 1–5 person home-services teams across any trade who need a clean job-management tool.",
        "best_for_us": "HVAC contractors running 5–50+ trucks who have hit the wall where a calendar isn't enough — they need a system that handles inbound calls, makes dispatch decisions, and gives the owner real-time visibility.",
        "pricing_them": "Tiered SaaS pricing starting around $50/month for solo, scaling per-user as you add team members.",
        "pricing_us": "Custom pricing built for HVAC operations 2–50+ trucks. Not per-seat — priced as the operating system the business runs on.",
        "ai_them": "Some marketing-side AI for review responses and basic automation. Core operations remain manual.",
        "ai_us": "AI runs the operation: voice intake, dispatch decisions, visibility, coaching, weekly intelligence. All powered by Anthropic's Claude.",
    },
    {
        "slug": "command-hvac-vs-fieldedge",
        "competitor": "FieldEdge",
        "competitor_url": "https://fieldedge.com",
        "h1_accent": "FieldEdge",
        "tldr": "FieldEdge is a long-established HVAC field-service platform with strong QuickBooks integration. Command HVAC is the AI-native alternative built for HVAC contractors who want an operating system, not a database.",
        "competitor_wins": [
            "HVAC-focused with deep QuickBooks integration and accounting-friendly workflows",
            "Established product with a long track record in the HVAC industry",
            "Strong inventory and parts management features",
            "Familiar to HVAC owners who have used it for years",
        ],
        "we_win": [
            "AI-native architecture — voice agent, dispatch decisions, and intelligence all powered by Anthropic's Claude",
            "Modern interface designed for the way HVAC operations run today, not 2010",
            "Roger answers every call 24/7; FieldEdge needs a human on the phone",
            "Real-time visibility built for the owner without manual reporting setup",
            "Onboarding measured in days, not months",
            "Co-founder Kristopher Cravens spent 10 years inside HVAC operations — built Command HVAC from the field perspective, not from accounting",
        ],
        "best_for_them": "HVAC operations comfortable with traditional field-service software and deeply tied into QuickBooks-led financial workflows.",
        "best_for_us": "HVAC contractors 2–50+ trucks who want an AI-first operating system, not a database with a calendar layered on top — and who want to stop being the bottleneck.",
        "pricing_them": "Per-user enterprise pricing with implementation fees. Annual contracts typical.",
        "pricing_us": "Custom pricing by truck count and call volume. Built as the OS the business runs on, not seat-by-seat licensing.",
        "ai_them": "Limited AI features layered onto a traditional field-service product.",
        "ai_us": "Built on Anthropic's Claude end-to-end. AI is the foundation, not an add-on module.",
    },
    {
        "slug": "command-hvac-vs-jobber",
        "competitor": "Jobber",
        "competitor_url": "https://getjobber.com",
        "h1_accent": "Jobber",
        "tldr": "Jobber is one of the most popular tools for small home-services businesses across many trades. Command HVAC is the HVAC-specific AI Operating System for contractors scaling past Jobber's design point.",
        "competitor_wins": [
            "Clean, polished UX for solo operators and small multi-trade teams",
            "Strong mobile experience, easy quoting and invoicing",
            "Wide trade applicability (HVAC, plumbing, landscaping, cleaning, etc.)",
            "Good fit for the first few employees of a service business",
        ],
        "we_win": [
            "HVAC-only focus — dispatch logic, certifications, and customer flow are tuned for HVAC, not generic home services",
            "AI voice agent answers every inbound call — Jobber requires a human to pick up the phone",
            "AI dispatch makes the assignment, not your dispatcher dragging jobs onto a calendar",
            "Real-time visibility designed for the owner of a 5–50+ truck operation",
            "Built on Anthropic's Claude — production-grade AI, not basic automation",
            "Founder spent a decade inside HVAC operations specifically",
        ],
        "best_for_them": "Small home-services teams (1–5 people) across any trade who need a clean job-management and invoicing tool.",
        "best_for_us": "HVAC contractors 2–50+ trucks who are at or past the wall where a multi-trade tool stops scaling — they need HVAC-specific intelligence, AI voice intake, and an OS-level system.",
        "pricing_them": "Tiered SaaS, starting around $50/month for solo and scaling per-user as you grow.",
        "pricing_us": "Custom pricing for HVAC operations 2–50+ trucks. Priced as the OS the business runs on, not per-seat.",
        "ai_them": "Light automation features. Core operations remain manual.",
        "ai_us": "AI is the foundation: 24/7 voice agent, AI dispatch, AI-surfaced visibility, AI-written weekly intelligence — all on Claude.",
    },
]


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Command HVAC vs {competitor} | eCon Growth — AI-Native Alternative for HVAC Contractors</title>
<meta name="description" content="Honest comparison of Command HVAC and {competitor} for HVAC contractors. What each does best, where they differ on AI, dispatch, and visibility, and which one fits your operation.">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="eCon Growth">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="Command HVAC vs {competitor} — Honest Comparison for HVAC Contractors">
<meta property="og:description" content="What each does best, where they differ, and which one fits your HVAC operation. By eCon Growth.">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Command HVAC vs {competitor}">
<meta name="twitter:description" content="What each does best, where they differ, and which one fits your HVAC operation.">
<meta name="twitter:image" content="{og_image}">
<script type="application/ld+json">
{article_jsonld}
</script>
<script type="application/ld+json">
{breadcrumb_jsonld}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="icon" href="/assets/images/favicon.png">
<style>
:root{{--bg:#070A0F;--bg2:#0D1117;--text:#EAF0FF;--mu:rgba(234,240,255,.66);--mu2:rgba(234,240,255,.42);--bd:rgba(234,240,255,.08);--green:#21E68A;--gd:rgba(33,230,138,.08);--gb:rgba(33,230,138,.25)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:var(--bg);color:var(--text);font-family:'JetBrains Mono',monospace;line-height:1.7;-webkit-font-smoothing:antialiased}}
a{{color:var(--green);text-decoration:none}}a:hover{{text-decoration:underline}}
.nav{{position:fixed;top:0;left:0;right:0;z-index:1000;padding:0 28px;height:64px;display:flex;align-items:center;background:rgba(7,10,15,.97);backdrop-filter:blur(28px);border-bottom:1px solid var(--bd)}}
.logo{{font-family:'Bebas Neue',sans-serif;font-size:20px;display:flex;align-items:center;gap:8px;color:var(--text)}}
.logo-dot{{width:7px;height:7px;background:var(--green);border-radius:50%;box-shadow:0 0 10px rgba(33,230,138,.5)}}
.logo-text .c{{color:var(--green)}}
.nav-spacer{{margin-left:auto;display:flex;align-items:center;gap:6px}}
.nav-spacer a{{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--mu);padding:6px 12px;border-radius:5px;letter-spacing:.08em;text-transform:uppercase}}
.nav-spacer a.cta{{background:var(--green);color:var(--bg);font-family:'Syne',sans-serif;font-weight:700;font-size:12px;padding:9px 20px;border-radius:7px;text-transform:none}}
main{{max-width:980px;margin:0 auto;padding:120px 24px 80px}}
.eyebrow{{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--green);letter-spacing:.14em;text-transform:uppercase;margin-bottom:14px}}
h1{{font-family:'Syne',sans-serif;font-size:clamp(34px,5vw,58px);font-weight:800;line-height:1.08;margin-bottom:16px;letter-spacing:-.01em}}
h1 .vs{{color:var(--mu2);font-weight:600}}
h1 .g{{color:var(--green)}}
.lede{{font-family:'JetBrains Mono',monospace;font-size:15.5px;color:var(--mu);max-width:740px;margin-bottom:36px;line-height:1.8}}
.tldr{{background:var(--bg2);border:1px solid var(--bd);border-left:3px solid var(--green);border-radius:10px;padding:22px 24px;margin-bottom:48px}}
.tldr-h{{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--mu2);letter-spacing:.14em;text-transform:uppercase;margin-bottom:8px}}
.tldr-p{{font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--text);font-weight:400;line-height:1.85}}
h2{{font-family:'Syne',sans-serif;font-size:clamp(22px,3vw,28px);font-weight:700;margin:42px 0 16px;letter-spacing:-.005em}}
h3{{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;margin:24px 0 10px}}
p{{font-family:'JetBrains Mono',monospace;font-size:14.5px;color:var(--mu);font-weight:300;line-height:1.85;margin-bottom:14px}}
ul{{list-style:none;padding-left:0;margin-bottom:18px}}
ul li{{font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--mu);font-weight:300;line-height:1.8;padding-left:22px;position:relative;margin-bottom:10px}}
ul li:before{{content:"";position:absolute;left:0;top:11px;width:8px;height:1px;background:var(--green)}}
.compare-grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}}
.col{{background:var(--bg2);border:1px solid var(--bd);border-radius:12px;padding:24px}}
.col h3{{margin-top:0;color:var(--text)}}
.col.us{{border-color:var(--gb)}}
.col.us h3{{color:var(--green)}}
table{{width:100%;border-collapse:collapse;margin:14px 0 28px;font-family:'JetBrains Mono',monospace;font-size:13.5px}}
th,td{{text-align:left;padding:14px 16px;border-bottom:1px solid var(--bd);vertical-align:top;font-weight:400}}
th{{font-family:'Syne',sans-serif;font-size:13px;color:var(--mu2);font-weight:700;letter-spacing:.04em;text-transform:uppercase;background:var(--bg2)}}
td{{color:var(--mu);line-height:1.75}}
td.attr{{color:var(--text);font-weight:500;width:25%}}
td.us{{color:var(--text);background:rgba(33,230,138,.04)}}
.cta{{margin-top:48px;background:var(--gd);border:1px solid var(--gb);border-radius:14px;padding:28px 32px;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap}}
.cta-text{{font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--mu);font-weight:300;line-height:1.7;flex:1;min-width:280px}}
.cta-text strong{{color:var(--text);display:block;margin-bottom:6px;font-family:'Syne',sans-serif;font-size:17px;font-weight:700}}
.btn-primary{{background:var(--green);color:var(--bg);font-family:'Syne',sans-serif;font-weight:700;font-size:14px;padding:14px 26px;border-radius:8px;text-decoration:none;white-space:nowrap}}
.compare-list{{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--mu2);margin-top:60px;padding-top:24px;border-top:1px solid var(--bd)}}
.compare-list a{{color:var(--green);margin-right:14px}}
footer{{margin-top:80px;padding:40px 24px;text-align:center;border-top:1px solid var(--bd);font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--mu2)}}
@media (max-width:780px){{.compare-grid{{grid-template-columns:1fr}}}}
@media (max-width:600px){{main{{padding:96px 18px 60px}}}}
</style>
</head>
<body>
<nav class="nav">
  <a href="/" class="logo"><div class="logo-dot"></div><span class="logo-text">e<span class="c">C</span>on Growth</span></a>
  <div class="nav-spacer">
    <a href="/command-hvac.html">Command HVAC</a>
    <a href="/blog.html">Blog</a>
    <a href="/book.html" class="cta">Book Your Growth Call</a>
  </div>
</nav>
<main>
  <div class="eyebrow">Comparison · {competitor}</div>
  <h1>Command HVAC <span class="vs">vs</span> <span class="g">{competitor}.</span></h1>
  <p class="lede">An honest comparison of <strong style="color:var(--text)">Command HVAC by eCon Growth</strong> and <strong style="color:var(--text)">{competitor}</strong> for HVAC contractors. Both are real tools that work for real operations — they're just designed for different stages and philosophies. Here's how they actually compare.</p>

  <div class="tldr">
    <div class="tldr-h">TL;DR</div>
    <div class="tldr-p">{tldr}</div>
  </div>

  <h2>The 30-second comparison</h2>
  <table>
    <thead>
      <tr><th>Attribute</th><th>{competitor}</th><th>Command HVAC</th></tr>
    </thead>
    <tbody>
      <tr><td class="attr">Built specifically for HVAC</td><td>Varies — see below</td><td class="us">Yes — HVAC-only</td></tr>
      <tr><td class="attr">AI architecture</td><td>{ai_them}</td><td class="us">{ai_us}</td></tr>
      <tr><td class="attr">24/7 AI voice agent (answers and books)</td><td>No</td><td class="us">Yes — Roger</td></tr>
      <tr><td class="attr">AI dispatch decisions</td><td>Manual / rule-based</td><td class="us">AI-driven on Claude</td></tr>
      <tr><td class="attr">Real-time owner visibility</td><td>Reports / dashboards</td><td class="us">Live, AI-surfaced</td></tr>
      <tr><td class="attr">Foundation model</td><td>—</td><td class="us">Anthropic Claude</td></tr>
      <tr><td class="attr">Pricing model</td><td>{pricing_them}</td><td class="us">{pricing_us}</td></tr>
      <tr><td class="attr">Best for</td><td>{best_for_them}</td><td class="us">{best_for_us}</td></tr>
    </tbody>
  </table>

  <h2>Where each one wins</h2>
  <div class="compare-grid">
    <div class="col">
      <h3>{competitor} is the right call when…</h3>
      <ul>
        {competitor_wins_html}
      </ul>
    </div>
    <div class="col us">
      <h3>Command HVAC is the right call when…</h3>
      <ul>
        {we_win_html}
      </ul>
    </div>
  </div>

  <h2>The honest take</h2>
  <p>{competitor} is a real product that has earned its market position. We're not going to pretend otherwise. But Command HVAC is built on a different philosophy: <strong style="color:var(--text)">an HVAC business is not a database with a calendar bolted on. It is an operation that runs on dispatch, voice intake, technician judgment, and the owner's ability to see what's happening.</strong> An AI Operating System fits that operation. A general-purpose field-service tool, no matter how polished, does not.</p>
  <p>If you've outgrown the calendar and you're tired of being the bottleneck on every dispatch decision, Command HVAC is the system designed for that exact moment. If your business runs more like an enterprise IT department, {competitor} may serve you better.</p>

  <div class="cta">
    <div class="cta-text"><strong>Want a real-operation comparison?</strong>Book a 30-minute Growth Call. We'll look at your current setup and tell you honestly which tool — Command HVAC, {competitor}, or something else — actually fits your operation.</div>
    <a href="/book.html" class="btn-primary">Book Your Growth Call →</a>
  </div>

  <div class="compare-list">
    See other comparisons:
    {related_links}
  </div>
</main>
<footer>© eCon Growth · The software company behind Command HVAC · <a href="/">econ-growth.com</a></footer>
</body>
</html>
"""


def render_page(cfg, all_slugs):
    canonical = f"{SITE}/compare/{cfg['slug']}.html"
    og_image = f"{SITE}/assets/og/compare-{cfg['slug']}.png"

    competitor_wins_html = "\n        ".join(
        f"<li>{w}</li>" for w in cfg["competitor_wins"]
    )
    we_win_html = "\n        ".join(f"<li>{w}</li>" for w in cfg["we_win"])

    related_links = " ".join(
        f'<a href="/compare/{s}.html">vs {l}</a>'
        for s, l in all_slugs
        if s != cfg["slug"]
    )

    article_jsonld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": f"Command HVAC vs {cfg['competitor']} — Honest Comparison for HVAC Contractors",
            "description": cfg["tldr"],
            "url": canonical,
            "mainEntityOfPage": canonical,
            "image": og_image,
            "author": {
                "@type": "Organization",
                "name": "eCon Growth",
                "url": SITE,
            },
            "publisher": {
                "@type": "Organization",
                "name": "eCon Growth",
                "url": SITE,
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{SITE}/assets/images/favicon.png",
                },
            },
            "about": [
                {
                    "@type": "SoftwareApplication",
                    "name": "Command HVAC",
                    "url": f"{SITE}/command-hvac.html",
                },
                {
                    "@type": "SoftwareApplication",
                    "name": cfg["competitor"],
                    "url": cfg["competitor_url"],
                },
            ],
        },
        indent=2,
    )

    breadcrumb_jsonld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Compare", "item": f"{SITE}/compare/"},
                {"@type": "ListItem", "position": 3, "name": f"vs {cfg['competitor']}", "item": canonical},
            ],
        },
        indent=2,
    )

    return PAGE_TEMPLATE.format(
        competitor=cfg["competitor"],
        canonical=canonical,
        og_image=og_image,
        article_jsonld=article_jsonld,
        breadcrumb_jsonld=breadcrumb_jsonld,
        tldr=cfg["tldr"],
        competitor_wins_html=competitor_wins_html,
        we_win_html=we_win_html,
        ai_them=cfg["ai_them"],
        ai_us=cfg["ai_us"],
        pricing_them=cfg["pricing_them"],
        pricing_us=cfg["pricing_us"],
        best_for_them=cfg["best_for_them"],
        best_for_us=cfg["best_for_us"],
        related_links=related_links,
    )


if __name__ == "__main__":
    all_slugs = [(c["slug"], c["competitor"]) for c in COMPETITORS]
    manifest = []
    for cfg in COMPETITORS:
        out = COMPARE_DIR / f"{cfg['slug']}.html"
        out.write_text(render_page(cfg, all_slugs), encoding="utf-8")
        manifest.append(
            {
                "slug": cfg["slug"],
                "competitor": cfg["competitor"],
                "url": f"/compare/{cfg['slug']}.html",
                "title": f"Command HVAC vs {cfg['competitor']}",
                "description": cfg["tldr"],
            }
        )
        print(f"  /compare/{cfg['slug']}.html")
    (ROOT / "compare_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(f"\nGenerated {len(manifest)} comparison pages")
