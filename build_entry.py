#!/usr/bin/env python3
"""Build the complete-edition entry image for make.fun news-image-20261120.

Composites one 1024x1024 PNG summing up the world news of Friday
20 November 2026. Three AI-generated scene photos (no text baked in)
are combined with text drawn entirely by PIL in Liberation Sans.

Deterministic: no randomness, no clock, no network. Running this
script twice produces a byte-identical entry.png.

Usage:  python3 build_entry.py
Output: entry.png  (1024x1024, under 1 MiB)
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024

# Palette
PAPER = (247, 243, 234)      # warm newsprint
INK = (16, 22, 30)           # near-black
NAVY = (14, 30, 51)          # masthead
RED = (178, 34, 34)          # accent / kicker
RED_DARK = (140, 24, 24)
GREY = (90, 96, 104)
LIGHT_GREY = (220, 216, 206)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, fill, leading=None):
    """Draw wrapped text; return the y just below the last line."""
    if leading is None:
        leading = fnt.size + 4
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_photo(path, size):
    """Centre-crop a photo to exactly `size` (deterministic)."""
    img = Image.open(path).convert("RGB")
    return ImageOps.fit(img, size, method=Image.LANCZOS, centering=(0.5, 0.5))


def build():
    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)

    # ------------------------------------------------------------------
    # Masthead
    # ------------------------------------------------------------------
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((28, 14), "FRIDAY, IN FULL", font=font("LiberationSans-Bold.ttf", 62), fill=WHITE)
    d.text((28, 82), "THE WORLD IN ONE IMAGE", font=font("LiberationSans-Bold.ttf", 17),
           fill=(196, 205, 216))
    d.text((742, 22), "FRIDAY", font=font("LiberationSans-Bold.ttf", 30), fill=WHITE)
    d.text((742, 56), "20 NOVEMBER 2026", font=font("LiberationSans-Bold.ttf", 21),
           fill=(255, 214, 120))
    d.rectangle([0, 108, W, 114], fill=RED)

    # ------------------------------------------------------------------
    # Ticker strip
    # ------------------------------------------------------------------
    ticker = ("KYIV BRIDGES HIT  •  S&P 500 -3.7%  •  NATO JETS UP  •  "
              "TRUMP ON AIR FORCE ONE: NO IRAN DECISION UNTIL JANUARY")
    d.rectangle([0, 118, W, 146], fill=INK)
    d.text((14, 124), ticker, font=font("LiberationSans-Bold.ttf", 16), fill=(255, 214, 120))

    # ------------------------------------------------------------------
    # Lead story: Russia's biggest strike on Ukraine (Kyiv photo)
    # ------------------------------------------------------------------
    lead_y = 156
    photo = fit_photo(
        os.path.join(ASSETS, "media-generation-kyiv-bridge-dawn-0-c077d439-3f75-4356-ac2a-eb8f73d3e64d.jpg"),
        (600, 250))
    canvas.paste(photo, (24, lead_y))
    d.rectangle([24, lead_y, 624, lead_y + 250], outline=INK, width=2)
    d.text((24, lead_y + 256),
           "A damaged Dnipro bridge in Kyiv at dawn.  Illustration: AI-generated scene.",
           font=font("LiberationSans-Italic.ttf", 13), fill=GREY)

    # Lead text panel, right of the photo
    px, pw = 648, 352
    d.text((px, lead_y), "WAR IN EUROPE", font=font("LiberationSans-Bold.ttf", 18), fill=RED)
    d.line([(px, lead_y + 26), (px + pw, lead_y + 26)], fill=RED, width=2)
    y = draw_wrapped(d, px, lead_y + 36,
                     "RUSSIA'S BIGGEST\nSTRIKE YET",
                     font("LiberationSans-Bold.ttf", 36), pw, INK, leading=38)
    y = draw_wrapped(d, px, y + 8,
                     "400+ drones and 110+ missiles hit Ukraine overnight. "
                     "Three Kyiv bridges over the Dnipro are damaged; "
                     "8 people are killed.",
                     font("LiberationSans-Regular.ttf", 17), pw, INK, leading=22)
    y = draw_wrapped(d, px, y + 8,
                     "Two missiles and a drone fall in Poland; NATO jets "
                     "scrambled, no casualties.",
                     font("LiberationSans-Regular.ttf", 17), pw, INK, leading=22)

    # ------------------------------------------------------------------
    # Second row: two photo cards
    # ------------------------------------------------------------------
    row_y = 448
    card_w, card_h = 488, 196

    # --- Wall Street card (left)
    ws = fit_photo(
        os.path.join(ASSETS, "media-generation-wall-street-selloff-0-244bb497-0b57-4803-ae5e-b6f2c819afd8.jpg"),
        (card_w, card_h))
    canvas.paste(ws, (24, row_y))
    d.rectangle([24, row_y, 24 + card_w, row_y + card_h], outline=INK, width=2)
    y = row_y + card_h + 10
    d.text((24, y), "MARKETS  —  WALL STREET SELLS OFF",
           font=font("LiberationSans-Bold.ttf", 17), fill=RED)
    y = draw_wrapped(d, 24, y + 24,
                     "S&P 500 -3.70% to 6,910.39 — a seventh straight fall, "
                     "into correction. Nasdaq -5.28% wipes out 2026 gains.",
                     font("LiberationSans-Bold.ttf", 18), 472, INK, leading=22)
    y = draw_wrapped(d, 24, y + 4,
                     "Nvidia -14% to $125.53 after Reuters reports the SEC "
                     "is examining its accounting.",
                     font("LiberationSans-Regular.ttf", 15), 472, INK, leading=19)

    # --- Cyclone card (right)
    cy = fit_photo(
        os.path.join(ASSETS, "media-generation-cyclone-odisha-coast-0-a4d38340-b9c0-463e-b834-9ede466c3ca1.jpg"),
        (card_w, card_h))
    canvas.paste(cy, (512, row_y))
    d.rectangle([512, row_y, 512 + card_w, row_y + card_h], outline=INK, width=2)
    y = row_y + card_h + 10
    d.text((512, y), "WEATHER  —  CYCLONE AKVAN LANDFALLS",
           font=font("LiberationSans-Bold.ttf", 17), fill=RED)
    y = draw_wrapped(d, 512, y + 24,
                     "Akvan comes ashore near Gopalpur, Odisha. About "
                     "300,000 evacuated; 69 trains cancelled.",
                     font("LiberationSans-Bold.ttf", 18), 472, INK, leading=22)
    y = draw_wrapped(d, 512, y + 4,
                     "Red alerts stand along India's east coast as the "
                     "storm pushes inland.",
                     font("LiberationSans-Regular.ttf", 15), 472, INK, leading=19)

    # ------------------------------------------------------------------
    # "Also today" grid: nine short items, three columns x three rows
    # ------------------------------------------------------------------
    grid_y = 772
    d.rectangle([0, grid_y - 8, W, grid_y + 22], fill=NAVY)
    d.text((24, grid_y - 4), "ALSO TODAY  —  FRIDAY 20 NOVEMBER 2026",
           font=font("LiberationSans-Bold.ttf", 17), fill=WHITE)

    items = [
        ("IRAN", "Trump: no decision until after 1 January. Senate rejects "
         "a war-powers curb 51–48."),
        ("GTA VI (EST.)", "Sensor Tower estimates $2.36bn day one, 24.6m "
         "copies. Take-Two unconfirmed."),
        ("UK–EU SUMMIT", "Deal reached in Brussels, including a youth "
         "mobility scheme."),
        ("SAMSUNG", "New heads named for the memory-chip and mobile "
         "businesses."),
        ("COP31", "Closing day in Antalya ends with no final deal; talks "
         "run over."),
        ("HORMUZ", "Tanker burns in the Strait of Hormuz after hitting "
         "a sea mine."),
        ("HAITI", "Police kill 34 gang members and retake the Martissant "
         "corridor."),
        ("ANTHROPIC", "Shares fall 8.5% to $88.91 on day two of trading, "
         "after a +17% debut."),
        ("AI DATA CENTRES", "Trump threatens to bar US firms from building "
         "AI data centres abroad."),
    ]

    col_w = 304
    col_x = [24, 360, 696]
    row_h = 58
    for i, (kicker, body) in enumerate(items):
        cx = col_x[i % 3]
        cy = grid_y + 32 + (i // 3) * row_h
        d.text((cx, cy), kicker, font=font("LiberationSans-Bold.ttf", 15), fill=RED_DARK)
        draw_wrapped(d, cx, cy + 19, body, font("LiberationSans-Regular.ttf", 14),
                     col_w, INK, leading=17)

    # ------------------------------------------------------------------
    # Optional strip + footer
    # ------------------------------------------------------------------
    strip_y = 984
    d.line([(24, strip_y), (W - 24, strip_y)], fill=LIGHT_GREY, width=1)
    d.text((24, strip_y + 6),
           "ALSO: Mamdani plans to close Rikers by 2032  •  Denmark accuses Russia "
           "over a rapper murder plot  •  Nigeria ends jail for attempted suicide",
           font=font("LiberationSans-Regular.ttf", 14), fill=GREY)
    d.text((24, 1006),
           "All events 20 November 2026. Sources: Reuters, BBC, AP, IMD, The Hindu, "
           "Samsung newsroom, Sensor Tower (estimate). Photos: AI-generated scenes.",
           font=font("LiberationSans-Regular.ttf", 12), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    canvas.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    img = Image.open(path)
    print(f"{path}: {img.size[0]}x{img.size[1]}, {os.path.getsize(path)} bytes")
