"""Extract each article from blog.html into its own SEO-optimized standalone page.

Generates /blog/{slug}.html for every <div class="article-item"> on blog.html,
each with full Article JSON-LD, canonical, OG/Twitter, and the same visual
look as the rest of the site. Idempotent: overwrites existing standalone files.
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
BLOG_DIR = ROOT / "blog"
BLOG_DIR.mkdir(exist_ok=True)
SITE = "https://econ-growth.com"
DEFAULT_IMAGE = f"{SITE}/assets/images/favicon.png"

CAT_MAP = {
    "operations": "Operations",
    "dispatch": "Dispatch",
    "revenue": "Revenue",
    "ai": "AI & Technology",
    "coaching": "Team & Coaching",
    "exit": "Exit & Valuation",
}


def slugify(title):
    s = title.lower()
    s = re.sub(r"[''`]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s[:80]


def date_iso(date_label):
    months = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
    }
    parts = date_label.strip().split()
    if len(parts) == 2 and parts[0] in months:
        return f"{parts[1]}-{months[parts[0]]}-01"
    return "2026-01-01"


POST_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | eCon Growth</title>
<meta name="description" content="{excerpt}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="eCon Growth">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:image" content="{image}">
<meta property="article:published_time" content="{date_iso}">
<meta property="article:author" content="The eCon Growth Team">
<meta property="article:section" content="{category}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{excerpt}">
<meta name="twitter:image" content="{image}">
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
a{{color:var(--green);text-decoration:none}}
a:hover{{text-decoration:underline}}
.nav{{position:fixed;top:0;left:0;right:0;z-index:1000;padding:0 28px;height:64px;display:flex;align-items:center;background:rgba(7,10,15,.97);backdrop-filter:blur(28px);border-bottom:1px solid var(--bd)}}
.logo{{font-family:'Bebas Neue',sans-serif;font-size:20px;display:flex;align-items:center;gap:8px;color:var(--text)}}
.logo-dot{{width:7px;height:7px;background:var(--green);border-radius:50%;box-shadow:0 0 10px rgba(33,230,138,.5)}}
.logo-text .c{{color:var(--green)}}
.nav-spacer{{margin-left:auto}}
.nav-spacer a{{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--mu);padding:6px 12px;border-radius:5px;letter-spacing:.08em;text-transform:uppercase;margin-left:8px}}
.nav-spacer a.cta{{background:var(--green);color:var(--bg);font-family:'Syne',sans-serif;font-weight:700;font-size:12px;padding:9px 20px;border-radius:7px;text-transform:none}}
main{{max-width:760px;margin:0 auto;padding:120px 24px 80px}}
.crumbs{{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--mu2);margin-bottom:24px;letter-spacing:.06em}}
.crumbs a{{color:var(--mu)}}
.cat{{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--green);letter-spacing:.14em;text-transform:uppercase;margin-bottom:14px;background:var(--gd);border:1px solid var(--gb);padding:5px 12px;border-radius:6px}}
h1{{font-family:'Syne',sans-serif;font-size:clamp(28px,4.4vw,46px);font-weight:800;line-height:1.18;margin-bottom:18px;letter-spacing:-.01em}}
.lede{{font-family:'JetBrains Mono',monospace;font-size:15px;color:var(--mu);margin-bottom:28px;line-height:1.7}}
.byline{{display:flex;align-items:center;gap:10px;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--mu2);margin-bottom:48px;padding-bottom:24px;border-bottom:1px solid var(--bd)}}
.byline .dot{{width:3px;height:3px;background:var(--mu2);border-radius:50%}}
.body{{font-size:15px;color:var(--text)}}
.body .ac-h2{{font-family:'Syne',sans-serif;font-size:clamp(20px,2.6vw,26px);font-weight:700;margin:36px 0 14px;letter-spacing:-.005em}}
.body .ac-p{{font-family:'JetBrains Mono',monospace;font-size:14.5px;color:var(--mu);font-weight:300;line-height:1.85;margin-bottom:18px}}
.body .ac-p strong{{color:var(--text);font-weight:500}}
.body .ac-ul{{list-style:none;padding-left:0;margin:6px 0 24px}}
.body .ac-ul li{{font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--mu);font-weight:300;line-height:1.8;padding-left:22px;position:relative;margin-bottom:12px}}
.body .ac-ul li:before{{content:"";position:absolute;left:0;top:11px;width:8px;height:1px;background:var(--green)}}
.body .ac-ul li strong{{color:var(--text);font-weight:500}}
.body .ac-cta{{margin-top:42px;background:var(--gd);border:1px solid var(--gb);border-radius:14px;padding:24px;display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap}}
.body .ac-cta-text{{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--mu);font-weight:300;line-height:1.7;flex:1;min-width:240px}}
.body .ac-cta-text strong{{color:var(--text);display:block;margin-bottom:6px;font-family:'Syne',sans-serif;font-size:15px;font-weight:700}}
.btn-primary{{background:var(--green);color:var(--bg);font-family:'Syne',sans-serif;font-weight:700;font-size:13px;padding:12px 22px;border-radius:8px;text-decoration:none;white-space:nowrap}}
.back{{margin-top:60px;padding-top:30px;border-top:1px solid var(--bd);font-family:'JetBrains Mono',monospace;font-size:12px}}
.back a{{color:var(--green)}}
footer{{margin-top:80px;padding:40px 24px;text-align:center;border-top:1px solid var(--bd);font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--mu2)}}
@media (max-width:600px){{main{{padding:96px 18px 60px}}}}
</style>
</head>
<body>
<nav class="nav">
  <a href="/" class="logo"><div class="logo-dot"></div><span class="logo-text">e<span class="c">C</span>on Growth</span></a>
  <div class="nav-spacer">
    <a href="/blog.html">All Posts</a>
    <a href="/book.html" class="cta">Book Your Growth Call</a>
  </div>
</nav>
<main>
  <div class="crumbs"><a href="/">Home</a> &nbsp;/&nbsp; <a href="/blog.html">Blog</a> &nbsp;/&nbsp; {category}</div>
  <span class="cat">{category}</span>
  <h1>{title}</h1>
  <p class="lede">{excerpt}</p>
  <div class="byline">
    <span>The eCon Growth Team</span><span class="dot"></span>
    <span>{date_label}</span><span class="dot"></span>
    <span>{read_time}</span>
  </div>
  <article class="body">
    {body_html}
  </article>
  <div class="back"><a href="/blog.html">← Back to all posts</a></div>
</main>
<footer>© eCon Growth · The AI Operating System for HVAC · <a href="/">econ-growth.com</a></footer>
</body>
</html>
"""


def extract_articles(blog_html):
    soup = BeautifulSoup(blog_html, "html.parser")
    items = soup.select("div.article-item")
    out = []
    for item in items:
        cat_key = item.get("data-cat", "operations")
        cat = CAT_MAP.get(cat_key, cat_key.title())
        title_el = item.select_one(".article-title")
        excerpt_el = item.select_one(".article-excerpt")
        date_el = item.select_one(".article-date")
        read_el = item.select_one(".article-read")
        body_el = item.select_one(".article-content")
        if not (title_el and body_el):
            continue
        title = title_el.get_text(" ", strip=True)
        excerpt = excerpt_el.get_text(" ", strip=True) if excerpt_el else ""
        date_label = date_el.get_text(strip=True) if date_el else "2026"
        read_time = read_el.get_text(strip=True) if read_el else ""
        body_html = body_el.decode_contents()
        out.append({
            "slug": slugify(title),
            "title": title,
            "excerpt": excerpt,
            "category": cat,
            "date_label": date_label,
            "date_iso": date_iso(date_label),
            "read_time": read_time,
            "body_html": body_html.strip(),
        })
    return out


def render_post(post):
    canonical = f"{SITE}/blog/{post['slug']}.html"
    article_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["excerpt"],
        "url": canonical,
        "mainEntityOfPage": canonical,
        "image": DEFAULT_IMAGE,
        "datePublished": post["date_iso"],
        "dateModified": post["date_iso"],
        "author": {
            "@type": "Organization",
            "name": "The eCon Growth Team",
            "url": SITE,
        },
        "publisher": {
            "@type": "Organization",
            "name": "eCon Growth",
            "url": SITE,
            "logo": {"@type": "ImageObject", "url": DEFAULT_IMAGE},
        },
        "articleSection": post["category"],
    }, indent=2)
    breadcrumb_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog.html"},
            {"@type": "ListItem", "position": 3, "name": post["title"], "item": canonical},
        ],
    }, indent=2)
    safe_excerpt = post["excerpt"].replace('"', "&quot;")
    safe_title = post["title"].replace('"', "&quot;")
    return POST_TEMPLATE.format(
        title=safe_title,
        excerpt=safe_excerpt,
        canonical=canonical,
        image=DEFAULT_IMAGE,
        date_iso=post["date_iso"],
        category=post["category"],
        date_label=post["date_label"],
        read_time=post["read_time"],
        body_html=post["body_html"],
        article_jsonld=article_jsonld,
        breadcrumb_jsonld=breadcrumb_jsonld,
    )


if __name__ == "__main__":
    blog_html = (ROOT / "blog.html").read_text(encoding="utf-8")
    posts = extract_articles(blog_html)
    print(f"Found {len(posts)} articles\n")
    manifest = []
    for post in posts:
        out_path = BLOG_DIR / f"{post['slug']}.html"
        out_path.write_text(render_post(post), encoding="utf-8")
        manifest.append({
            "slug": post["slug"],
            "title": post["title"],
            "url": f"/blog/{post['slug']}.html",
            "category": post["category"],
            "date_iso": post["date_iso"],
            "excerpt": post["excerpt"],
        })
        print(f"  /blog/{post['slug']}.html  —  {post['title'][:60]}…")
    (ROOT / "blog_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(f"\nWrote {len(manifest)} posts and blog_manifest.json")
