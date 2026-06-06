"""Refresh sitemap.xml lastmod from git, preserving curated priority/changefreq.

For every <url> already in sitemap.xml, map its <loc> to the local file and
replace <lastmod> with that file's last git commit date. URLs whose file no
longer exists are left untouched (and reported). Idempotent: re-running only
changes dates that actually moved.

Run after committing site changes, before deploy:
    python3 generate_sitemap.py
"""

import re
import subprocess
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent
SITEMAP = ROOT / "sitemap.xml"
SITE = "https://econ-growth.com/"


def loc_to_file(loc: str) -> Path:
    path = loc[len(SITE):] if loc.startswith(SITE) else loc
    return ROOT / ("index.html" if path in ("", "/") else path)


def git_date(f: Path) -> Optional[str]:
    if not f.exists():
        return None
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cd", "--date=short", "--", f.name if f.parent == ROOT else str(f.relative_to(ROOT))],
        cwd=ROOT, capture_output=True, text=True,
    )
    return out.stdout.strip() or None


def main() -> None:
    xml = SITEMAP.read_text()
    missing, updated = [], 0

    def repl(m: re.Match) -> str:
        block, loc = m.group(0), m.group(1)
        d = git_date(loc_to_file(loc))
        if d is None:
            missing.append(loc)
            return block
        new = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{d}</lastmod>", block)
        return new

    new_xml, _ = re.subn(
        r"<url><loc>(https://econ-growth\.com/[^<]*)</loc>.*?</url>",
        repl, xml,
    )
    # count real changes
    updated = sum(1 for a, b in zip(xml.splitlines(), new_xml.splitlines()) if a != b)
    SITEMAP.write_text(new_xml)
    print(f"sitemap.xml refreshed — {updated} URL line(s) changed")
    for loc in missing:
        print(f"  WARN file missing for {loc} (lastmod left as-is)")


if __name__ == "__main__":
    main()
