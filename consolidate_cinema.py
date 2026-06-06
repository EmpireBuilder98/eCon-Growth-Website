#!/usr/bin/env python3
"""
Strip the 8 old cinema CSS + 9 old cinema JS includes from each page
and insert ONE link + ONE script (cinema-v2.css + cinema-v2.js).
Idempotent.
"""
from pathlib import Path
import re

ROOT = Path('/Users/empire-builder98/Jarvis/eCon-Growth-Website')

PAGES = [
  'index.html', 'about.html', 'blog.html', 'sales.html', 'press.html',
  'contact.html', 'investors.html', 'ai-social-os.html', 'marketing.html',
  'financial-planning.html', 'book.html', 'privacy.html', 'terms.html',
]

# Patterns matching the OLD cinema lines (with optional comments above)
OLD_PATTERNS = [
    # CSS links
    r'<!--\s*═══[^\n]*CINEMA[^\n]*-->\s*\n',
    r'<link rel="stylesheet" href="/assets/cinema/cinema\.css">\s*\n',
    r'<link rel="stylesheet" href="/assets/cinema/cinema-pro\.css">\s*\n',
    r'<link rel="stylesheet" href="/assets/cinema/cinema-max\.css">\s*\n',
    r'<link rel="stylesheet" href="/assets/cinema/cinema-tune\.css">\s*\n',
    r'<link rel="stylesheet" href="/assets/cinema/cinema-perf\.css">\s*\n',
    r'<link rel="stylesheet" href="/assets/cinema/cinema-mov\.css">\s*\n',
    r'<link rel="stylesheet" href="/assets/cinema/cinema-lite\.css">\s*\n',
    r'<link rel="stylesheet" href="/assets/cinema/cinema-nuclear\.css">\s*\n',
    # JS scripts
    r'<script src="/assets/cinema/atmosphere\.js" defer></script>\s*\n',
    r'<script src="/assets/cinema/cinema\.js" defer></script>\s*\n',
    r'<script src="/assets/cinema/cinema-pro\.js" defer></script>\s*\n',
    r'<script src="/assets/cinema/cinema-max\.js" defer></script>\s*\n',
    r'<script src="/assets/cinema/cinema-tune\.js" defer></script>\s*\n',
    r'<script src="/assets/cinema/cinema-perf\.js" defer></script>\s*\n',
    r'<script src="/assets/cinema/cinema-mov\.js" defer></script>\s*\n',
    r'<script src="/assets/cinema/cinema-lite\.js" defer></script>\s*\n',
    r'<script src="/assets/cinema/cinema-nuclear\.js" defer></script>\s*\n',
]

NEW_CSS = '<!-- CINEMA v2 (consolidated) -->\n<link rel="stylesheet" href="/assets/cinema/cinema-v2.css">'
NEW_JS  = '<!-- CINEMA v2 (consolidated) -->\n<script src="/assets/cinema/cinema-v2.js" defer></script>'

stats = {'cleaned':0, 'inserted':0, 'missing':0}

for p in PAGES:
    f = ROOT / p
    if not f.exists():
        print(f'  · {p:30s} MISSING')
        stats['missing'] += 1
        continue
    s = f.read_text()
    before = s

    # Strip old patterns
    for pat in OLD_PATTERNS:
        s = re.sub(pat, '', s)

    # Strip leftover empty comment lines that were just headers
    s = re.sub(r'\n{3,}', '\n\n', s)

    # Insert NEW_CSS before </head> if not already there
    if '/assets/cinema/cinema-v2.css' not in s:
        s = s.replace('</head>', f'{NEW_CSS}\n</head>', 1)

    # Insert NEW_JS before </body> if not already there
    if '/assets/cinema/cinema-v2.js' not in s:
        s = s.replace('</body>', f'{NEW_JS}\n</body>', 1)

    if s != before:
        f.write_text(s)
        print(f'  ✓ {p:30s} consolidated')
        stats['cleaned'] += 1
    else:
        print(f'  · {p:30s} already consolidated')

print()
print(f'cleaned:  {stats["cleaned"]}')
print(f'missing:  {stats["missing"]}')
