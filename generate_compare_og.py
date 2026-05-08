"""Generate OG cards for comparison pages using the existing brand template."""

import json
from pathlib import Path
from generate_og_images import render_card, OG_DIR

ROOT = Path("/Users/empire-builder98/Jarvis/eCon-Growth-Website")

if __name__ == "__main__":
    manifest = json.loads((ROOT / "compare_manifest.json").read_text(encoding="utf-8"))
    for entry in manifest:
        out = OG_DIR / f"compare-{entry['slug']}.png"
        title = f"Command HVAC vs {entry['competitor']}."
        subtitle = entry["description"]
        eyebrow = f"COMPARISON · VS {entry['competitor'].upper()}"
        render_card(
            out,
            title,
            subtitle=subtitle,
            eyebrow=eyebrow,
            accent_word=entry["competitor"],
            is_blog=True,
        )
        print(f"  compare-{entry['slug']}.png")
    print(f"\nGenerated {len(manifest)} comparison OG cards")
