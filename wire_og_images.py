"""Update og:image and twitter:image meta tags on every page based on
og_manifest.json — replacing the favicon placeholder with each page's
dedicated 1200x630 social card.
"""

import json
import re
from pathlib import Path

ROOT = Path("/Users/empire-builder98/Jarvis/eCon-Growth-Website")
SITE = "https://econ-growth.com"


def update_image_tag(html, prop_name, prop_attr, new_url):
    """Replace the content="..." of an OG/Twitter image meta tag, regardless of
    attribute order (property/name first OR content first). Idempotent.
    """
    # Order A: <meta property|name="og:image" content="...">
    pat_a = rf'(<meta\s+{prop_attr}="{re.escape(prop_name)}"\s+content=")[^"]*(")'
    new = re.sub(pat_a, lambda m: m.group(1) + new_url + m.group(2), html, count=1, flags=re.IGNORECASE)
    if new != html:
        return new, True
    # Order B: <meta content="..." property|name="og:image">
    pat_b = rf'(<meta\s+content=")[^"]*("\s+{prop_attr}="{re.escape(prop_name)}")'
    new = re.sub(pat_b, lambda m: m.group(1) + new_url + m.group(2), html, count=1, flags=re.IGNORECASE)
    return new, new != html


def main():
    manifest = json.loads((ROOT / "og_manifest.json").read_text(encoding="utf-8"))
    changed_files = 0
    for entry in manifest:
        page = entry["page"]
        img_path = entry["image"]
        full_url = f"{SITE}{img_path}"
        fp = ROOT / page
        if not fp.exists():
            print(f"SKIP missing {page}")
            continue
        html = fp.read_text(encoding="utf-8")
        original = html
        html, _ = update_image_tag(html, "og:image", "property", full_url)
        html, _ = update_image_tag(html, "twitter:image", "name", full_url)
        if html != original:
            fp.write_text(html, encoding="utf-8")
            changed_files += 1
            print(f"  updated {page}")
        else:
            print(f"  no change {page}")
    print(f"\nUpdated {changed_files} pages")


if __name__ == "__main__":
    main()
