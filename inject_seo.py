"""One-shot SEO injector for econ-growth.com static HTML pages.

For each HTML file mapped below: ensure a canonical link, Open Graph tags,
Twitter card tags, and (homepage only) Organization + WebSite JSON-LD are
present. Skips tags that already exist so the script is idempotent.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://econ-growth.com"
SITE_NAME = "eCon Growth"
DEFAULT_IMAGE = f"{SITE}/assets/images/favicon.png"
LINKEDIN = "https://www.linkedin.com/company/econ-growthoffical/"

PAGES = {
    "index.html": "/",
    "command-os.html": "/command-os.html",
    "roger.html": "/roger.html",
    "sales.html": "/sales.html",
    "about.html": "/about.html",
    "visibility.html": "/visibility.html",
    "book.html": "/book.html",
    "contact.html": "/contact.html",
    "blog.html": "/blog.html",
    "investors.html": "/investors.html",
    "roi-calculator.html": "/roi-calculator.html",
    "meet-roger.html": "/meet-roger.html",
    "aeo.html": "/aeo.html",
    "privacy.html": "/privacy.html",
    "terms.html": "/terms.html",
}

ORG_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "eCon Growth",
  "alternateName": "Command HVAC",
  "url": "{SITE}/",
  "logo": "{DEFAULT_IMAGE}",
  "description": "The AI Operating System built exclusively for HVAC business owners. Powered by Anthropic's Claude.",
  "founder": {{
    "@type": "Person",
    "name": "Kristopher Cravens"
  }},
  "sameAs": [
    "{LINKEDIN}"
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "eCon Growth",
  "url": "{SITE}/",
  "potentialAction": {{
    "@type": "SearchAction",
    "target": "{SITE}/?q={{search_term_string}}",
    "query-input": "required name=search_term_string"
  }}
}}
</script>"""


def extract(pattern, html):
    m = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else None


def build_block(title, desc, page_url, is_home):
    # Escape any double-quotes in description for safety inside content="...".
    safe_desc = desc.replace('"', "&quot;")
    safe_title = title.replace('"', "&quot;")
    og_type = "website"
    lines = [
        f'<link rel="canonical" href="{page_url}">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:url" content="{page_url}">',
        f'<meta property="og:title" content="{safe_title}">',
        f'<meta property="og:description" content="{safe_desc}">',
        f'<meta property="og:image" content="{DEFAULT_IMAGE}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{safe_title}">',
        f'<meta name="twitter:description" content="{safe_desc}">',
        f'<meta name="twitter:image" content="{DEFAULT_IMAGE}">',
    ]
    block = "\n".join(lines)
    if is_home:
        block += "\n" + ORG_JSONLD
    return block


def inject(filename, path):
    fp = ROOT / filename
    html = fp.read_text(encoding="utf-8")
    page_url = f"{SITE}{path}"
    is_home = path == "/"

    title = extract(r"<title>([^<]+)</title>", html) or SITE_NAME
    desc = extract(
        r'<meta\s+name="description"\s+content="([^"]+)"', html
    ) or ""

    has_canonical = re.search(r'rel="canonical"', html, re.IGNORECASE)
    has_og = re.search(r'property="og:title"', html, re.IGNORECASE)
    has_twitter = re.search(r'name="twitter:card"', html, re.IGNORECASE)
    has_jsonld_org = (
        '"@type": "Organization"' in html or '"@type":"Organization"' in html
    )

    parts = []
    if not has_canonical:
        parts.append(f'<link rel="canonical" href="{page_url}">')
    if not has_og:
        parts.extend([
            f'<meta property="og:site_name" content="{SITE_NAME}">',
            f'<meta property="og:type" content="website">',
            f'<meta property="og:url" content="{page_url}">',
            f'<meta property="og:title" content="{title.replace(chr(34), "&quot;")}">',
            f'<meta property="og:description" content="{desc.replace(chr(34), "&quot;")}">',
            f'<meta property="og:image" content="{DEFAULT_IMAGE}">',
        ])
    if not has_twitter:
        parts.extend([
            f'<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{title.replace(chr(34), "&quot;")}">',
            f'<meta name="twitter:description" content="{desc.replace(chr(34), "&quot;")}">',
            f'<meta name="twitter:image" content="{DEFAULT_IMAGE}">',
        ])
    if is_home and not has_jsonld_org:
        parts.append(ORG_JSONLD)

    if not parts:
        return f"{filename}: already complete, skipped"

    block = "\n".join(parts) + "\n"

    # Insert right after the existing <meta name="description" ...> line if present;
    # otherwise after <title>; otherwise after <head>.
    desc_match = re.search(
        r'(<meta\s+name="description"[^>]*>\s*)', html, re.IGNORECASE
    )
    if desc_match:
        idx = desc_match.end()
        new_html = html[:idx] + block + html[idx:]
    else:
        title_match = re.search(r"</title>\s*", html, re.IGNORECASE)
        if title_match:
            idx = title_match.end()
            new_html = html[:idx] + block + html[idx:]
        else:
            head_match = re.search(r"<head[^>]*>\s*", html, re.IGNORECASE)
            idx = head_match.end()
            new_html = html[:idx] + block + html[idx:]

    fp.write_text(new_html, encoding="utf-8")
    added = []
    if not has_canonical:
        added.append("canonical")
    if not has_og:
        added.append("og")
    if not has_twitter:
        added.append("twitter")
    if is_home and not has_jsonld_org:
        added.append("jsonld")
    return f"{filename}: added {', '.join(added)}"


if __name__ == "__main__":
    for filename, path in PAGES.items():
        print(inject(filename, path))
