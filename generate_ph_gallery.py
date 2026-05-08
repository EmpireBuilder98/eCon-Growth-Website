"""Generate Producthunt-spec 1270x760 gallery images for the launch.

Reuses the brand template from generate_og_images.py but at PH spec.
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

# Reuse helpers from the OG generator
sys.path.insert(0, "/Users/empire-builder98/Jarvis/eCon-Growth-Website")
from generate_og_images import (
    BG, GREEN, WHITE, MUTED, MUTED_2,
    F_BEBAS, F_SYNE, F_MONO, font, measure, wrap_text,
    draw_logo, draw_url_badge, draw_eyebrow,
)

ROOT = Path("/Users/empire-builder98/Jarvis/eCon-Growth-Website")
PH_DIR = ROOT / "assets" / "ph"
PH_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1270, 760


def draw_background_ph(img):
    draw = ImageDraw.Draw(img, "RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-300, -300, 600, 600), fill=(33, 230, 138, 38))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=80))
    img.paste(glow, (0, 0), glow)
    glow2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g2 = ImageDraw.Draw(glow2)
    g2.ellipse((W - 500, H - 500, W + 200, H + 200), fill=(33, 230, 138, 24))
    glow2 = glow2.filter(ImageFilter.GaussianBlur(radius=120))
    img.paste(glow2, (0, 0), glow2)
    for y in range(120, H, 120):
        draw.line([(0, y), (W, y)], fill=(234, 240, 255, 6), width=1)
    for x in range(160, W, 160):
        draw.line([(x, 0), (x, H)], fill=(234, 240, 255, 6), width=1)


def render_ph_card(out_path, title, subtitle="", eyebrow="", accent_word=None):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_background_ph(img)
    draw_logo(img, draw)

    if eyebrow:
        fnt = font(F_MONO, 16)
        draw.text((72, 230), eyebrow.upper(), font=fnt, fill=GREEN)

    max_w = W - 144
    sizes = [88, 78, 68, 60, 52]
    title_fnt = font(F_SYNE, sizes[0], weight=800)
    title_lines = wrap_text(draw, title, title_fnt, max_w)
    for size in sizes:
        title_fnt = font(F_SYNE, size, weight=800)
        title_lines = wrap_text(draw, title, title_fnt, max_w)
        if len(title_lines) <= 3:
            break

    title_line_h = title_fnt.getbbox("Hg")[3] + 6
    y = 280
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

    if subtitle:
        if len(subtitle) > 200:
            subtitle = subtitle[:200].rsplit(" ", 1)[0] + "…"
        sub_fnt = font(F_SYNE, 30, weight=500)
        sub_max_w = 900
        sub_lines = wrap_text(draw, subtitle, sub_fnt, sub_max_w)[:3]
        sline_h = sub_fnt.getbbox("Hg")[3] + 6
        y += 16
        for line in sub_lines:
            draw.text((72, y), line, font=sub_fnt, fill=MUTED)
            y += sline_h

    draw_url_badge(img, draw)
    img.save(out_path, "PNG", optimize=True)
    return out_path


CARDS = [
    {
        "filename": "ph-1-hero.png",
        "title": "The AI Operating System for HVAC.",
        "subtitle": "Built on Anthropic's Claude. Exclusively for HVAC contractors running 2–50+ trucks.",
        "eyebrow": "ECON GROWTH · COMMAND HVAC",
        "accent": "AI",
    },
    {
        "filename": "ph-2-roger.png",
        "title": "Meet Roger. Your AI Voice Agent.",
        "subtitle": "Answers every inbound call in under three seconds. Books directly into dispatch. 24/7. Powered by Claude.",
        "eyebrow": "PRODUCT · ROGER",
        "accent": "Roger",
    },
    {
        "filename": "ph-3-dispatch.png",
        "title": "AI Dispatch Decisions, Not a Calendar.",
        "subtitle": "Smart job assignment based on tech certifications, location, workload, and customer history. The system makes the call — not your dispatcher's bad day.",
        "eyebrow": "PRODUCT · AI DISPATCH",
        "accent": "AI",
    },
    {
        "filename": "ph-4-visibility.png",
        "title": "Real-Time Visibility for the Owner.",
        "subtitle": "Close rates, technician performance, call outcomes, dispatch efficiency, revenue. All in one screen. AI-surfaced, not manually reported.",
        "eyebrow": "PRODUCT · VISIBILITY",
        "accent": "Owner",
    },
    {
        "filename": "ph-5-built-by.png",
        "title": "Built From the Inside Out.",
        "subtitle": "Co-founded by Kristopher Cravens (10 years inside HVAC operations) and Watson Wheeler (operations and exit strategy). Designed for HVAC contractors, by HVAC operators.",
        "eyebrow": "ABOUT THE FOUNDERS",
        "accent": "Inside",
    },
    {
        "filename": "ph-6-vs-servicetitan.png",
        "title": "ServiceTitan, reimagined as AI-native.",
        "subtitle": "Not a calendar with workflows on top. The AI Operating System the business runs on. For HVAC contractors 2–50+ trucks.",
        "eyebrow": "VS SERVICETITAN",
        "accent": "AI-native",
    },
]


if __name__ == "__main__":
    for cfg in CARDS:
        out = PH_DIR / cfg["filename"]
        render_ph_card(
            out,
            cfg["title"],
            subtitle=cfg["subtitle"],
            eyebrow=cfg["eyebrow"],
            accent_word=cfg["accent"],
        )
        print(f"  /assets/ph/{cfg['filename']}")
    print(f"\nGenerated {len(CARDS)} Producthunt gallery images at 1270x760")
