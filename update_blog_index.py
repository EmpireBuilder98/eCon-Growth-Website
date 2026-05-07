"""Update blog.html: insert the new AI dispatch article card and add
crawlable 'Read on its own page' permalinks to every article body.
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from extract_blog_posts import slugify

ROOT = Path(__file__).parent

MARKER_CLASS = "ac-permalink"


def main():
    blog_path = ROOT / "blog.html"
    manifest = json.loads((ROOT / "blog_manifest.json").read_text(encoding="utf-8"))
    by_slug = {p["slug"]: p for p in manifest}

    html = blog_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # 1. Append permalink links to each article-content (idempotent).
    for item in soup.select("div.article-item"):
        title_el = item.select_one(".article-title")
        body_el = item.select_one(".article-content")
        if not (title_el and body_el):
            continue
        slug = slugify(title_el.get_text(" ", strip=True))
        if slug not in by_slug:
            continue
        # Skip if permalink already present
        if body_el.select_one(f".{MARKER_CLASS}"):
            continue
        permalink_html = (
            f'<div style="margin-top:18px;font-family:\'JetBrains Mono\',monospace;'
            f'font-size:11px"><a class="{MARKER_CLASS}" href="/blog/{slug}.html" '
            f'onclick="event.stopPropagation()" style="color:rgba(33,230,138,.85);'
            f'letter-spacing:.06em">Read on its own page →</a></div>'
        )
        body_el.append(BeautifulSoup(permalink_html, "html.parser"))

    # 2. Insert new AI dispatch article card at the top of the article-list.
    list_el = soup.select_one("#article-list, .article-list")
    if list_el is None:
        # fall back to first .article-list
        list_el = soup.find(class_="article-list")
    new_slug = "hvac-dispatch-software-with-ai-2026-guide"
    if list_el is not None and not list_el.find(
        "div",
        class_="article-item",
        attrs={"data-new-dispatch": "1"},
    ) and not soup.find("a", href=f"/blog/{new_slug}.html"):
        new_post = by_slug.get(new_slug)
        if new_post:
            new_card_html = f'''
<div class="article-item" data-cat="dispatch" data-new-dispatch="1" onclick="toggleArticle(this)">
  <div class="article-header">
    <div>
      <div class="article-meta"><span class="article-cat">Dispatch</span><span class="article-date">May 2026</span><span class="article-read">9 min read</span></div>
      <div class="article-author" style="display:flex;align-items:center;gap:8px;margin-top:4px">
        <img src="" class="kris-photo" alt="eCon Growth Team" style="width:24px;height:24px;border-radius:50%;object-fit:cover;object-position:center top;border:1px solid rgba(33,230,138,.3)" loading="lazy">
        <span style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:rgba(234,240,255,.45);letter-spacing:.04em">The eCon Growth Team</span>
      </div>
      <div class="article-title">{new_post["title"]}</div>
      <div class="article-excerpt">{new_post["excerpt"]}</div>
    </div>
    <div class="article-toggle">+</div>
  </div>
  <div class="article-body">
    <div class="article-content">
      <div class="ac-h2">Read the full guide</div>
      <p class="ac-p">This post explains exactly what HVAC dispatch software with AI does in 2026, the five capabilities a real solution needs, why dispatch is where AI pays back fastest, and the five questions to ask any vendor before you sign. Plus where eCon Growth\'s Command HVAC fits.</p>
      <div class="ac-cta">
        <div class="ac-cta-text"><strong>See AI dispatch software actually run.</strong>Book a 30-minute Growth Call and watch Roger handle live calls and dispatch decisions.</div>
        <a href="book.html" class="btn-primary">Book Your Growth Call →</a>
      </div>
      <div style="margin-top:18px;font-family:\'JetBrains Mono\',monospace;font-size:11px"><a class="{MARKER_CLASS}" href="/blog/{new_slug}.html" onclick="event.stopPropagation()" style="color:rgba(33,230,138,.85);letter-spacing:.06em">Read on its own page →</a></div>
    </div>
  </div>
</div>
'''
            new_node = BeautifulSoup(new_card_html, "html.parser")
            # Insert as first child of list_el
            first_child = next((c for c in list_el.children if getattr(c, "name", None) == "div"), None)
            if first_child:
                first_child.insert_before(new_node)
            else:
                list_el.append(new_node)

    blog_path.write_text(str(soup), encoding="utf-8")
    print("blog.html updated")


if __name__ == "__main__":
    main()
