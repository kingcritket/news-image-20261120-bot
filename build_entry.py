"""Build entry.png for news-image-20261120 from three AI-generated scene
photos (assets/, no text baked in) plus PIL-drawn text and a dotted
world map.

Layout (1024x1024): navy date header with a gold dot world map, 2x2 grid
of three photo stories + an "ALSO TODAY" strip, navy footer ticker.
Every word on the image is drawn here in Liberation Sans; the photos
carry no text.

Stories, all verified against reporting of 20 November 2026 (events of
the day, or first reported that day in some time zone):
  1. Trump delays Iran decision to 2027 - "We'll see what happens after
     January 1", on his plane home from China; Senate rejects the
     Iran war-powers resolution 51-48 (Reuters, 20 Nov).
  2. Cyclone Akvan hits India today - landfall by noon between Narsapur
     and Puri; ~300,000 evacuated, 69 trains cancelled, red alerts
     (IMD; The Hindu, 20 Nov).
  3. GTA VI sales top $1.8bn - day-one sales pass The Odyssey's global
     run (reported 20 Nov).
Strip (all first reported 20 Nov, all verified): ICJ rules Myanmar
committed genocide against the Rohingya, 9-6, the first state ever
held liable for genocide (Reuters/BBC); NASA confirms Voyager 1 has
passed a light-day from Earth (20 Nov); Japan's Hayabusa2 scraps its
asteroid landing after engine trouble (Space, 20 Nov); European
leaders say they are ready for talks with Russia on ending the
Ukraine war (BBC, 20 Nov); Houthis damage a Riyadh tower, Saudi
authorities confirm (20 Nov); Trump posthumously pardons Pete Rose,
clearing his 1990 tax conviction (AP/Reuters, 19 Nov evening US,
20 Nov in Asia).
Footer ticker: Fiji declares a national disaster over drought;
South Korea's exports top $1 trillion for the first time; Taiwan
moves to steady its stocks (all 20 Nov).
Deliberately NOT repeated as today's news: the Shenzhen trilateral
itself (19 Nov) - only its follow-up, the Iran-decision delay, is
today's story.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

NAVY = (26, 38, 92)
GOLD = (212, 175, 55)
BG = (245, 243, 238)
PANEL_BORDER = (205, 200, 190)
INK = (26, 38, 92)
SUB_INK = (90, 90, 90)
WHITE = (255, 255, 255)

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# Coarse world map as (row, col) cell rectangles, equirectangular:
# 48 columns of longitude, 20 rows of latitude. Each cell is one dot.
WORLD_MAP_RECTS = [
    # North America
    (0, 2, 9), (1, 1, 11), (2, 2, 12), (3, 3, 12),
    (4, 4, 11), (5, 5, 10), (6, 6, 9), (7, 6, 8),
    (8, 5, 8), (9, 4, 7), (10, 3, 6), (11, 3, 5),
    # South America
    (10, 13, 17), (11, 13, 18), (12, 13, 18),
    (13, 14, 18), (14, 14, 17), (15, 15, 17),
    (16, 15, 16), (17, 15, 16), (18, 16, 16),
    # Europe
    (1, 24, 28), (2, 23, 29), (3, 23, 28),
    (4, 24, 28), (5, 25, 27),
    # Africa
    (6, 23, 29), (7, 22, 30), (8, 22, 30),
    (9, 23, 30), (10, 23, 29), (11, 24, 29),
    (12, 24, 28), (13, 25, 27), (14, 26, 27),
    # Asia
    (0, 30, 45), (1, 29, 46), (2, 29, 46),
    (3, 30, 45), (4, 30, 44), (5, 31, 43),
    (6, 31, 42), (7, 32, 41), (8, 32, 40),
    (9, 33, 39), (10, 34, 38),
    # Australia
    (13, 39, 43), (14, 39, 44), (15, 40, 43),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_width):
    """Largest bold size at or below `start` that fits `max_width`."""
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, size)


def wrap(draw, text, f, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_world_map(draw, x0, y0, step=4, colour=GOLD):
    """Gold dotted world map, 48x20 cells."""
    r = 1.6
    for row, c0, c1 in WORLD_MAP_RECTS:
        for col in range(c0, c1 + 1):
            cx = x0 + col * step
            cy = y0 + row * step
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)


def photo_panel(canvas, draw, img, box, headline, sub, img_h=300):
    """One photo story panel: image on top, headline + sub below."""
    x, y, w, h = box
    photo = img.resize((w, img_h), Image.LANCZOS)
    canvas.paste(photo, (x, y))
    draw.rectangle([x, y + img_h, x + w, y + h], fill=WHITE)
    draw.rectangle([x, y, x + w, y + h], outline=PANEL_BORDER, width=2)
    pad = 16
    max_w = w - 2 * pad
    hf = fit_font(draw, headline, FONT_BOLD, 30, max_w)
    draw.text((x + pad, y + img_h + 12), headline, font=hf, fill=INK)
    sf = font(FONT_REG, 18)
    lines = wrap(draw, sub, sf, max_w)
    ty = y + img_h + 12 + hf.size + 8
    for line in lines:
        draw.text((x + pad, ty), line, font=sf, fill=SUB_INK)
        ty += 23


def ring_icon(draw, cx, cy, r, colour, kind):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
    if kind == "capitol":
        draw.arc([cx - r + 8, cy - r + 10, cx + r - 8, cy + r - 4],
                 start=180, end=360, fill=colour, width=4)
        draw.line([cx - r + 10, cy + 6, cx + r - 10, cy + 6],
                  fill=colour, width=4)
        draw.line([cx, cy - r + 12, cx, cy - r + 2], fill=colour, width=4)
    elif kind == "cyclone":
        draw.arc([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
                 start=0, end=270, fill=colour, width=4)
        draw.arc([cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16],
                 start=90, end=360, fill=colour, width=4)
    elif kind == "planet":
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=colour)
        draw.line([cx - r + 4, cy + 8, cx + r - 4, cy - 8],
                  fill=colour, width=4)
    elif kind == "globe":
        draw.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
                     outline=colour, width=4)
        draw.line([cx, cy - r + 8, cx, cy + r - 8], fill=colour, width=3)
    elif kind == "chart":
        draw.line([cx - 12, cy + 12, cx + 12, cy + 12],
                  fill=colour, width=3)
        for bx, bh in ((-11, 10), (-2, 18), (7, 26)):
            draw.rectangle([cx + bx, cy + 12 - bh, cx + bx + 6, cy + 12],
                           fill=colour)
    elif kind == "rocket":
        # nose cone + fins
        draw.polygon([(cx, cy - r + 4), (cx - 8, cy + 8),
                      (cx + 8, cy + 8)], fill=colour)
        draw.rectangle([cx - 6, cy + 6, cx + 6, cy + 14], fill=colour)
        draw.line([cx, cy + 14, cx, cy + r - 4], fill=colour, width=3)
    elif kind == "burst":
        # radiating starburst lines
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (1, -1), (-1, 1), (1, 1)):
            draw.line([cx, cy, cx + dx * (r - 6), cy + dy * (r - 6)],
                      fill=colour, width=3)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=colour)


def strip_item(draw, x, y, w, colour, kind, head, sub):
    ring_icon(draw, x + 26, y + 24, 21, colour, kind)
    tx = x + 60
    max_w = w - 60 - 8
    hf = fit_font(draw, head, FONT_BOLD, 21, max_w)
    draw.text((tx, y + 1), head, font=hf, fill=INK)
    sf = fit_font(draw, sub, FONT_REG, 15, max_w)
    draw.text((tx, y + 1 + hf.size + 4), sub, font=sf, fill=SUB_INK)
    return y + 1 + hf.size + 4 + 20


def main():
    canvas = Image.new("RGB", (1024, 1024), BG)
    draw = ImageDraw.Draw(canvas)

    # Header: date band + gold rule + dotted world map at right.
    draw.rectangle([0, 0, 1024, 96], fill=NAVY)
    date_font = fit_font(draw, "FRIDAY, 20 NOVEMBER 2026",
                         FONT_BOLD, 56, 760)
    draw.text((24, 96 // 2 - date_font.size // 2 - 4),
              "FRIDAY, 20 NOVEMBER 2026", font=date_font, fill=WHITE)
    draw_world_map(draw, 812, 10)
    draw.rectangle([0, 96, 1024, 100], fill=GOLD)

    plane = Image.open(os.path.join(
        ASSETS,
        "media-generation-trump-plane-night-0-f12400ba-06c9-4b0d-a00e-100e4edfadc2.webp"
    )).convert("RGB")
    cyclone = Image.open(os.path.join(
        ASSETS,
        "media-generation-cyclone-akvan-0-a7665993-77a3-4ceb-9152-15f1595f5e73.webp"
    )).convert("RGB")
    vice = Image.open(os.path.join(
        ASSETS,
        "media-generation-vice-city-neon-0-c7e53773-cc3a-4fcd-beb5-e269edc67f9f.webp"
    )).convert("RGB")

    # Top row: Trump delays Iran decision | Cyclone Akvan hits India.
    photo_panel(canvas, draw, plane, (24, 116, 480, 420),
                "TRUMP DELAYS IRAN DECISION TO 2027",
                "\u201cWE\u2019LL SEE AFTER JANUARY 1,\u201d HE SAYS ON RETURN FROM CHINA; SENATE REJECTS WAR-POWERS CURB 51\u201348")
    photo_panel(canvas, draw, cyclone, (520, 116, 480, 420),
                "CYCLONE AKVAN HITS INDIA TODAY",
                "300,000 EVACUATED AS STORM MAKES LANDFALL BY NOON; RED ALERTS, 69 TRAINS CANCELLED")

    # Bottom-left: GTA VI sales.
    photo_panel(canvas, draw, vice, (24, 552, 480, 420),
                "GTA VI SALES TOP $1.8 BILLION",
                "DAY-ONE SALES PASS THE ODYSSEY\u2019S GLOBAL RUN; LAUNCH WEEK CONTINUES")

    # Bottom-right: also today.
    x, y, w, h = 520, 552, 480, 420
    draw.rectangle([x, y, x + w, y + h], fill=WHITE)
    draw.rectangle([x, y, x + w, y + h], outline=PANEL_BORDER, width=2)
    draw.rectangle([x, y, x + w, y + 56], fill=NAVY)
    hf = font(FONT_BOLD, 28)
    draw.text((x + 16, y + 12), "ALSO TODAY", font=hf, fill=WHITE)

    items = [
        ("globe", NAVY, "WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
         "ICJ 9\u20136: FIRST STATE EVER HELD LIABLE"),
        ("planet", NAVY, "VOYAGER 1 PASSES A LIGHT-DAY",
         "NASA CONFIRMS PROBE\u2019S DISTANCE MILESTONE"),
        ("rocket", (150, 40, 40), "HAYABUSA2 ENGINE TROUBLE",
         "JAPAN SCRAPS ASTEROID LANDING PLAN"),
        ("globe", NAVY, "EUROPE READY FOR RUSSIA TALKS",
         "LEADERS BACK NEGOTIATIONS TO END UKRAINE WAR"),
        ("burst", (150, 40, 40), "HOUTHIS DAMAGE RIYADH TOWER",
         "SAUDI CONFIRMS STRIKE ON LANDMARK BUILDING"),
        ("capitol", NAVY, "PETE ROSE PARDONED POSTHUMOUSLY",
         "TRUMP CLEARS LATE STAR\u2019S 1990 TAX CONVICTION"),
    ]
    iy = y + 70
    for i, (kind, colour, head, sub) in enumerate(items):
        end = strip_item(draw, x + 12, iy, w - 24, colour, kind, head, sub)
        iy = end + 8
        if i < len(items) - 1:
            draw.line([x + 16, iy - 4, x + w - 16, iy - 4],
                      fill=(220, 218, 210), width=2)

    # Footer ticker.
    draw.rectangle([0, 988, 1024, 1024], fill=NAVY)
    ff = fit_font(draw,
                  "FIJI DECLARES DROUGHT DISASTER  \u2022  S. KOREA EXPORTS TOP $1TN  \u2022  TAIWAN STEADIES STOCKS",
                  FONT_BOLD, 17, 1024 - 32)
    ft = "FIJI DECLARES DROUGHT DISASTER  \u2022  S. KOREA EXPORTS TOP $1TN  \u2022  TAIWAN STEADIES STOCKS"
    fw = draw.textlength(ft, font=ff)
    draw.text(((1024 - fw) / 2, 997), ft, font=ff, fill=WHITE)

    canvas.save(os.path.join(HERE, "entry.png"), "PNG", optimize=True)


if __name__ == "__main__":
    main()
