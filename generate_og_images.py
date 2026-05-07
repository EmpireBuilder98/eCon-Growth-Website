"""Generate brand-matching 1200x630 OG/social images for every key page
and blog post. Writes PNGs to assets/og/ and prints a manifest mapping
each page → its OG image path.
"""

import json
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path("/Users/empire-builder98/Jarvis/eCon-Growth-Website")
OG_DIR = ROOT / "assets" / "og"
OG_DIR.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path("/tmp/og-fonts")

W, H = 1200, 630
BG = "#070A0F"
GREEN = "#21E68A"
WHITE = "#EAF0FF"
MUTED = (234, 240, 255, 165)  # ~65% opacity
MUTED_2 = (234, 240, 255, 105)

# Fonts
F_BEBAS = FONT_DIR / "BebasNeue-Regular.ttf"
F_SYNE = FONT_DIR / "Syne-VariableFont.ttf"
F_MONO = FONT_DIR / "JetBrainsMono-Regular.ttf"


def font(path, size, weight=None):
    f = ImageFont.truetype(str(path), size=size)
    # For variable fonts (Syne), set weight via font_variation
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def draw_background(img):
    """Solid background + subtle radial green glow + grid lines for texture."""
    draw = ImageDraw.Draw(img, "RGBA")
    # Soft green glow in top-left corner
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-300, -300, 600, 600), fill=(33, 230, 138, 38))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=80))
    img.paste(glow, (0, 0), glow)
    # Subtle bottom-right glow
    glow2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g2 = ImageDraw.Draw(glow2)
    g2.ellipse((W - 500, H - 500, W + 200, H + 200), fill=(33, 230, 138, 24))
    glow2 = glow2.filter(ImageFilter.GaussianBlur(radius=120))
    img.paste(glow2, (0, 0), glow2)
    # Faint horizontal grid lines for techy texture
    for y in range(120, H, 120):
        draw.line([(0, y), (W, y)], fill=(234, 240, 255, 6), width=1)
    for x in range(160, W, 160):
        draw.line([(x, 0), (x, H)], fill=(234, 240, 255, 6), width=1)


def measure(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(draw, text, fnt, max_width):
    words = text.split()
    lines = []
    cur = []
    for w in words:
        trial = " ".join(cur + [w])
        tw, _ = measure(draw, trial, fnt)
        if tw <= max_width or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def draw_logo(img, draw):
    """Top-left brand: green dot + 'eCon Growth' wordmark."""
    # Green dot
    dot_x, dot_y, dot_r = 72, 84, 9
    draw.ellipse(
        (dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r),
        fill=GREEN,
    )
    # Wordmark
    fnt = font(F_BEBAS, 38)
    # Slightly extra letter spacing by drawing chars
    text = "eCon Growth"
    x = dot_x + dot_r + 14
    base_y = dot_y - 22
    # Draw whole string but color the C green
    # Bebas Neue is uppercase-only display, so draw char-by-char with the C in green.
    px = x
    for ch in text:
        color = GREEN if ch == "C" else WHITE
        draw.text((px, base_y), ch, font=fnt, fill=color)
        cw, _ = measure(draw, ch, fnt)
        px += cw + 1


def draw_url_badge(img, draw):
    fnt = font(F_MONO, 18)
    text = "ECON-GROWTH.COM"
    tw, th = measure(draw, text, fnt)
    pad_x, pad_y = 16, 9
    x = W - tw - 72 - pad_x * 2
    y = H - 72 - th - pad_y * 2
    # Pill background
    draw.rounded_rectangle(
        (x, y, x + tw + pad_x * 2, y + th + pad_y * 2),
        radius=8,
        fill=(33, 230, 138, 36),
        outline=(33, 230, 138, 110),
        width=1,
    )
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=GREEN)


def draw_eyebrow(img, draw, eyebrow):
    if not eyebrow:
        return 0
    fnt = font(F_MONO, 16)
    tw, th = measure(draw, eyebrow.upper(), fnt)
    x = 72
    y = 200
    draw.text((x, y), eyebrow.upper(), font=fnt, fill=GREEN)
    return th + 18


def draw_title_and_subtitle(img, draw, title, subtitle, accent_word=None, is_blog=False):
    max_w = W - 144

    # Auto-fit title: try font sizes from large to small until it fits in <=3 lines.
    sizes = [80, 72, 64, 56, 50, 44, 40] if not is_blog else [64, 56, 50, 46, 42, 38]
    title_fnt = None
    title_lines = []
    for size in sizes:
        title_fnt = font(F_SYNE, size, weight=800)
        title_lines = wrap_text(draw, title, title_fnt, max_w)
        if len(title_lines) <= 3:
            break
    # Last-resort truncate
    if len(title_lines) > 3:
        title_lines = title_lines[:3]
        last = title_lines[-1]
        while measure(draw, last + "…", title_fnt)[0] > max_w and len(last) > 2:
            last = last[:-1]
        title_lines[-1] = last + "…"

    subtitle_fnt = font(F_SYNE, 26 if is_blog else 28, weight=500)
    # Subtitle width capped so it doesn't run under the URL badge in the bottom-right.
    sub_max_w = 800

    # Truncate raw subtitle to ~180 chars before wrapping
    if subtitle and len(subtitle) > 180:
        subtitle = subtitle[:180].rsplit(" ", 1)[0] + "…"

    # Compute total title height + subtitle height to vertically center the block
    title_line_h = title_fnt.getbbox("Hg")[3] + 6
    title_block_h = title_line_h * len(title_lines)

    sub_lines = wrap_text(draw, subtitle, subtitle_fnt, sub_max_w)[:2] if subtitle else []
    sub_line_h = subtitle_fnt.getbbox("Hg")[3] + 6
    sub_block_h = (sub_line_h * len(sub_lines)) + (14 if sub_lines else 0)

    # Available content area: y=210 (after eyebrow) → y=520 (before URL badge)
    content_top = 210
    content_bot = 520
    total_h = title_block_h + sub_block_h
    y = content_top + max(0, ((content_bot - content_top) - total_h) // 2)

    # Draw title with optional green accent for one word
    for line in title_lines:
        if accent_word and accent_word.lower() in line.lower():
            idx = line.lower().find(accent_word.lower())
            before = line[:idx]
            match = line[idx : idx + len(accent_word)]
            after = line[idx + len(accent_word):]
            x = 72
            for chunk, color in [(before, WHITE), (match, GREEN), (after, WHITE)]:
                if not chunk:
                    continue
                draw.text((x, y), chunk, font=title_fnt, fill=color)
                cw, _ = measure(draw, chunk, title_fnt)
                x += cw
        else:
            draw.text((72, y), line, font=title_fnt, fill=WHITE)
        y += title_line_h

    if sub_lines:
        y += 14
        for line in sub_lines:
            draw.text((72, y), line, font=subtitle_fnt, fill=MUTED)
            y += sub_line_h


def render_card(out_path, title, subtitle="", eyebrow="", accent_word=None, is_blog=False):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_background(img)
    draw_logo(img, draw)
    draw_eyebrow(img, draw, eyebrow)
    draw_title_and_subtitle(
        img, draw, title, subtitle, accent_word=accent_word, is_blog=is_blog
    )
    draw_url_badge(img, draw)
    img.save(out_path, "PNG", optimize=True)
    return out_path


# ── Page definitions ──
PAGES = [
    {
        "filename": "home.png",
        "page_path": "index.html",
        "title": "The AI Operating System for HVAC.",
        "subtitle": "Built on Anthropic's Claude. Exclusively for HVAC contractors running 2–50+ trucks.",
        "eyebrow": "ECON GROWTH",
        "accent": "AI",
    },
    {
        "filename": "command-os.png",
        "page_path": "command-os.html",
        "title": "Command HVAC.",
        "subtitle": "The full operating system. Roger, dispatch, visibility, coaching, and weekly intelligence — in one OS.",
        "eyebrow": "PRODUCT · COMMAND OS",
        "accent": "Command",
    },
    {
        "filename": "roger.png",
        "page_path": "roger.html",
        "title": "Meet Roger. Your AI Voice Agent.",
        "subtitle": "Answers every call in under three seconds. Books directly into dispatch. 24/7. Powered by Claude.",
        "eyebrow": "PRODUCT · ROGER",
        "accent": "Roger",
    },
    {
        "filename": "meet-roger.png",
        "page_path": "meet-roger.html",
        "title": "Watch Roger Handle Live HVAC Calls.",
        "subtitle": "Real conversations. Real bookings. In real time. Powered by Anthropic's Claude.",
        "eyebrow": "DEMO · MEET ROGER",
        "accent": "Live",
    },
    {
        "filename": "visibility.png",
        "page_path": "visibility.html",
        "title": "Know Everything Without Being Everywhere.",
        "subtitle": "Real-time visibility across every part of your HVAC operation. For the owner, not just the dispatcher.",
        "eyebrow": "PRODUCT · VISIBILITY",
        "accent": "Everything",
    },
    {
        "filename": "about.png",
        "page_path": "about.html",
        "title": "Built From the Inside Out.",
        "subtitle": "Ten years inside HVAC operations. Every role, every truck, every shift. Then we built the OS.",
        "eyebrow": "ABOUT · KRISTOPHER CRAVENS",
        "accent": "Inside",
    },
    {
        "filename": "press.png",
        "page_path": "press.html",
        "title": "Press Kit.",
        "subtitle": "Official entity facts, founder bio, product summaries, and verified claims for media and AI engines.",
        "eyebrow": "PRESS",
        "accent": "Press",
    },
    {
        "filename": "glossary.png",
        "page_path": "glossary.html",
        "title": "HVAC AI Glossary.",
        "subtitle": "Plain-English definitions of every AI and operations term that matters for HVAC business owners.",
        "eyebrow": "RESOURCE · GLOSSARY",
        "accent": "AI",
    },
    {
        "filename": "blog.png",
        "page_path": "blog.html",
        "title": "The HVAC Business Growth Blog.",
        "subtitle": "Real insights for HVAC owners running 2–50+ trucks. Dispatch, revenue, AI, and operations.",
        "eyebrow": "BLOG",
        "accent": "Growth",
    },
    {
        "filename": "book.png",
        "page_path": "book.html",
        "title": "Book Your Growth Call.",
        "subtitle": "30 minutes. See Command HVAC and Roger handle live operations. Walk away with a real plan.",
        "eyebrow": "BOOK A CALL",
        "accent": "Growth",
    },
    {
        "filename": "roi-calculator.png",
        "page_path": "roi-calculator.html",
        "title": "What Is Chaos Costing You?",
        "subtitle": "Calculate your missed revenue, owner-time drain, and operating cost of running without an OS.",
        "eyebrow": "TOOL · ROI CALCULATOR",
        "accent": "Chaos",
    },
]


def post_to_card(post):
    """Map a blog manifest entry to OG card config."""
    # Pull a 1-2 word accent from the title (longest word likely a keyword)
    title = post["title"]
    return {
        "filename": f"blog-{post['slug']}.png",
        "page_path": f"blog/{post['slug']}.html",
        "title": title,
        "subtitle": post["excerpt"],
        "eyebrow": f"BLOG · {post['category'].upper()}",
        "accent": None,
    }


if __name__ == "__main__":
    manifest = []
    for cfg in PAGES:
        out = OG_DIR / cfg["filename"]
        render_card(out, cfg["title"], cfg["subtitle"], cfg["eyebrow"], accent_word=cfg["accent"], is_blog=False)
        manifest.append({"page": cfg["page_path"], "image": f"/assets/og/{cfg['filename']}"})
        print(f"  {cfg['filename']}")

    blog_manifest = json.loads((ROOT / "blog_manifest.json").read_text(encoding="utf-8"))
    for post in blog_manifest:
        cfg = post_to_card(post)
        out = OG_DIR / cfg["filename"]
        render_card(out, cfg["title"], cfg["subtitle"], cfg["eyebrow"], accent_word=cfg["accent"], is_blog=True)
        manifest.append({"page": cfg["page_path"], "image": f"/assets/og/{cfg['filename']}"})
        print(f"  {cfg['filename']}")

    (ROOT / "og_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nGenerated {len(manifest)} OG images")
