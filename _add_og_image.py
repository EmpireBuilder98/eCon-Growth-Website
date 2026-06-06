#!/usr/bin/env python3
"""Insert og:image + twitter:image meta tags on the 4 pages missing them.
Uses /assets/og/home.png as a brand-consistent placeholder."""
from pathlib import Path

ROOT = Path('/Users/empire-builder98/Jarvis/eCon-Growth-Website')
IMG_URL = 'https://econ-growth.com/assets/og/home.png'

PAGES = ['investors.html', 'ai-social-os.html', 'marketing.html', 'financial-planning.html']

for p in PAGES:
    f = ROOT / p
    s = f.read_text()

    if 'og:image' in s:
        print(f'  · {p}: already has og:image (skipping)')
        continue

    # Find og:title and insert og:image + twitter:image right after the og: block,
    # before the next <link> or <script>
    og_tag = f'<meta property="og:image" content="{IMG_URL}">'
    tw_tag = f'<meta name="twitter:image" content="{IMG_URL}">'
    card_tag = '<meta name="twitter:card" content="summary_large_image">'

    inject = ''
    if 'twitter:card' not in s:
        inject = f'{og_tag}\n{card_tag}\n{tw_tag}\n'
    else:
        inject = f'{og_tag}\n{tw_tag}\n'

    # Insert before </head>
    if '</head>' in s:
        s = s.replace('</head>', f'{inject}</head>', 1)
        f.write_text(s)
        print(f'  ✓ {p}: og:image + twitter:image inserted')
    else:
        print(f'  ! {p}: no </head> found')
