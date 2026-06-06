#!/usr/bin/env python3
"""
Inject the cinema layer (CSS + 2 JS files) into umbrella pages.
Idempotent — skips files already wired.

Adds:
  <head>:   <link rel="stylesheet" href="/assets/cinema/cinema.css">
  </body>:  <script src="/assets/cinema/atmosphere.js" defer></script>
            <script src="/assets/cinema/cinema.js" defer></script>
"""
from pathlib import Path
import re, sys

ROOT = Path('/Users/empire-builder98/Jarvis/eCon-Growth-Website')

# Twelve umbrella pages (index.html is already wired and skipped)
PAGES = [
  'index.html',
  'about.html', 'blog.html', 'sales.html', 'press.html', 'contact.html',
  'investors.html', 'ai-social-os.html', 'marketing.html', 'financial-planning.html',
  'book.html', 'privacy.html', 'terms.html',
]

BASE_CSS = '<link rel="stylesheet" href="/assets/cinema/cinema.css">'
PRO_CSS  = '<link rel="stylesheet" href="/assets/cinema/cinema-pro.css">'
MAX_CSS  = '<link rel="stylesheet" href="/assets/cinema/cinema-max.css">'
TUNE_CSS = '<link rel="stylesheet" href="/assets/cinema/cinema-tune.css">'
PERF_CSS = '<link rel="stylesheet" href="/assets/cinema/cinema-perf.css">'
MOV_CSS  = '<link rel="stylesheet" href="/assets/cinema/cinema-mov.css">'
LITE_CSS = '<link rel="stylesheet" href="/assets/cinema/cinema-lite.css">'
NUKE_CSS = '<link rel="stylesheet" href="/assets/cinema/cinema-nuclear.css">'
BASE_JS  = '<script src="/assets/cinema/atmosphere.js" defer></script>\n<script src="/assets/cinema/cinema.js" defer></script>'
PRO_JS   = '<script src="/assets/cinema/cinema-pro.js" defer></script>'
MAX_JS   = '<script src="/assets/cinema/cinema-max.js" defer></script>'
TUNE_JS  = '<script src="/assets/cinema/cinema-tune.js" defer></script>'
PERF_JS  = '<script src="/assets/cinema/cinema-perf.js" defer></script>'
MOV_JS   = '<script src="/assets/cinema/cinema-mov.js" defer></script>'
LITE_JS  = '<script src="/assets/cinema/cinema-lite.js" defer></script>'
NUKE_JS  = '<script src="/assets/cinema/cinema-nuclear.js" defer></script>'

CSS_INSERTION_ANCHOR = '</head>'      # insert before this
JS_INSERTION_ANCHOR  = '</body>'      # insert before this

stats = {'wired':0, 'already':0, 'missing':0}

for p in PAGES:
  f = ROOT / p
  if not f.exists():
    print(f'  · {p:30s} MISSING')
    stats['missing'] += 1
    continue
  s = f.read_text()
  before = s

  # BASE CSS
  if '/assets/cinema/cinema.css' not in s:
    s = s.replace(CSS_INSERTION_ANCHOR, f'<!-- ═══ CINEMA LAYER ═══ -->\n{BASE_CSS}\n{CSS_INSERTION_ANCHOR}', 1)
  # PRO CSS
  if '/assets/cinema/cinema-pro.css' not in s:
    s = s.replace(CSS_INSERTION_ANCHOR, f'{PRO_CSS}\n{CSS_INSERTION_ANCHOR}', 1)
  # MAX CSS
  if '/assets/cinema/cinema-max.css' not in s:
    s = s.replace(CSS_INSERTION_ANCHOR, f'{MAX_CSS}\n{CSS_INSERTION_ANCHOR}', 1)
  # TUNE CSS
  if '/assets/cinema/cinema-tune.css' not in s:
    s = s.replace(CSS_INSERTION_ANCHOR, f'{TUNE_CSS}\n{CSS_INSERTION_ANCHOR}', 1)
  # PERF CSS (must load AFTER tune so it overrides)
  if '/assets/cinema/cinema-perf.css' not in s:
    s = s.replace(CSS_INSERTION_ANCHOR, f'{PERF_CSS}\n{CSS_INSERTION_ANCHOR}', 1)
  # MOV CSS
  if '/assets/cinema/cinema-mov.css' not in s:
    s = s.replace(CSS_INSERTION_ANCHOR, f'{MOV_CSS}\n{CSS_INSERTION_ANCHOR}', 1)
  # LITE CSS (perf overrides)
  if '/assets/cinema/cinema-lite.css' not in s:
    s = s.replace(CSS_INSERTION_ANCHOR, f'{LITE_CSS}\n{CSS_INSERTION_ANCHOR}', 1)
  # NUKE CSS (LAST — wins all)
  if '/assets/cinema/cinema-nuclear.css' not in s:
    s = s.replace(CSS_INSERTION_ANCHOR, f'{NUKE_CSS}\n{CSS_INSERTION_ANCHOR}', 1)
  # BASE JS
  if '/assets/cinema/cinema.js' not in s:
    s = s.replace(JS_INSERTION_ANCHOR, f'<!-- ═══ CINEMA LAYER scripts ═══ -->\n{BASE_JS}\n{JS_INSERTION_ANCHOR}', 1)
  # PRO JS
  if '/assets/cinema/cinema-pro.js' not in s:
    s = s.replace(JS_INSERTION_ANCHOR, f'{PRO_JS}\n{JS_INSERTION_ANCHOR}', 1)
  # MAX JS
  if '/assets/cinema/cinema-max.js' not in s:
    s = s.replace(JS_INSERTION_ANCHOR, f'{MAX_JS}\n{JS_INSERTION_ANCHOR}', 1)
  # TUNE JS
  if '/assets/cinema/cinema-tune.js' not in s:
    s = s.replace(JS_INSERTION_ANCHOR, f'{TUNE_JS}\n{JS_INSERTION_ANCHOR}', 1)
  # PERF JS
  if '/assets/cinema/cinema-perf.js' not in s:
    s = s.replace(JS_INSERTION_ANCHOR, f'{PERF_JS}\n{JS_INSERTION_ANCHOR}', 1)
  # MOV JS
  if '/assets/cinema/cinema-mov.js' not in s:
    s = s.replace(JS_INSERTION_ANCHOR, f'{MOV_JS}\n{JS_INSERTION_ANCHOR}', 1)
  # LITE JS (perf rescue runs after other layers mount)
  if '/assets/cinema/cinema-lite.js' not in s:
    s = s.replace(JS_INSERTION_ANCHOR, f'{LITE_JS}\n{JS_INSERTION_ANCHOR}', 1)
  # NUKE JS (LAST — wins all)
  if '/assets/cinema/cinema-nuclear.js' not in s:
    s = s.replace(JS_INSERTION_ANCHOR, f'{NUKE_JS}\n{JS_INSERTION_ANCHOR}', 1)

  if s == before:
    print(f'  · {p:30s} already wired')
    stats['already'] += 1
    continue

  f.write_text(s)
  print(f'  ✓ {p:30s} wired')
  stats['wired'] += 1

print()
print(f'wired:   {stats["wired"]}')
print(f'already: {stats["already"]}')
print(f'missing: {stats["missing"]}')
