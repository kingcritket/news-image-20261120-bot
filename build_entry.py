#!/usr/bin/env python3
"""news-image-20261120 — front page builder ("Friday, In Full").

Renders a single 1024x1024 PNG that sums up the world news of Friday
20 November 2026, in the style of a broadsheet front page:

  * a navy masthead carrying the date and a dotted world map in gold,
  * three photo stories with PIL-drawn headlines and decks,
  * an "ALSO TODAY" panel with five further stories and line icons,
  * a navy ticker strip along the bottom.

The three scene photos in ``assets/`` are AI-generated and contain no
text; every word on the page is typeset here with PIL (Liberation Sans),
so nothing can come out garbled. All stories were verified against
reporting dated 20 November 2026 (Reuters, AP, BBC, IMD, The Hindu,
Deadline, Samsung newsroom); the one outside estimate on the page —
Sensor Tower's GTA VI sales figure — is labelled (EST.) and the deck
states that Take-Two has not confirmed it.

Usage:  python3 build_entry.py     # writes entry.png beside this file
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_PNG = os.path.join(BASE_DIR, "entry.png")

# --------------------------------------------------------------------------
# Page geometry and ink colours
# --------------------------------------------------------------------------
PAGE_W = 1024
PAGE_H = 1024

PAPER = (244, 239, 230)   # warm newsprint
NAVY = (24, 24, 96)       # masthead, ticker, headlines
GOLD = (198, 160, 38)     # masthead rule and map dots
INK = (28, 28, 28)        # body text
RULE = (203, 196, 182)    # hairline borders
RED = (176, 32, 32)       # editorial accent
WHITE = (255, 255, 255)

SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

MARGIN = 24
MASTHEAD_H = 100
TICKER_H = 56
GUTTER = 16
COL_W = (PAGE_W - 3 * MARGIN) // 2           # 476
COL_XS = (MARGIN, MARGIN + COL_W + GUTTER)   # 24 and 524
ROW1_Y = MASTHEAD_H + 12                     # 112
ROW1_H = 430
ROW2_Y = ROW1_Y + ROW1_H + GUTTER            # 558
ROW2_H = (PAGE_H - TICKER_H) - ROW2_Y        # 410


def load_font(path, size):
    return ImageFont.truetype(path, size)


def shrink_to_fit(draw, text, start_size, max_width, path=SANS_BOLD):
    """Biggest font size, counting down from ``start_size``, whose
    rendering of ``text`` is no wider than ``max_width`` pixels."""
    size = start_size
    while size > 10:
        candidate = load_font(path, size)
        if draw.textlength(text, font=candidate) <= max_width:
            return candidate
        size -= 1
    return load_font(path, 10)


def wrap_lines(draw, text, fnt, max_width):
    """Split ``text`` into lines that each fit ``max_width`` (greedy)."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if not current or draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fill_frame(photo, target_w, target_h):
    """Resize ``photo`` so it covers the frame, then centre-crop it to
    exactly (target_w, target_h)."""
    src_w, src_h = photo.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = round(src_w * scale), round(src_h * scale)
    resized = photo.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


# --------------------------------------------------------------------------
# Dotted world map for the masthead.
# A coarse hand-drawn land mask: '#' marks land, anything else is sea.
# It is stamped as gold dots, so continental accuracy hardly matters.
# --------------------------------------------------------------------------
LAND_MASK = [
    "                                                            ",
    "   ###########     ####      #####    #################    ",
    "  #############   ######     ######   ##################   ",
    "  ##############   #####    #######   ###################  ",
    "   ############    #####    ######    ##################   ",
    "    ##########      ###     #####     ################     ",
    "     ########        ##     ######     #############      ",
    "      ######               #######      ##########        ",
    "       ####                ######        #######          ",
    "        ##        ##        #####         #####           ",
    "                #####       ####          ###             ",
    "               #######       ###                           ",
    "               ########       ##                           ",
    "                #######                                     ",
    "                 #####                                      ",
    "                  ####                    #######           ",
    "                   ##                    #########          ",
    "                                        #########           ",
    "                                         #######            ",
    "                                          #####             ",
]


def stamp_map(draw, origin_x, origin_y, pitch=4, radius=2):
    for row_idx, row in enumerate(LAND_MASK):
        for col_idx, cell in enumerate(row):
            if cell != "#":
                continue
            cx = origin_x + col_idx * pitch
            cy = origin_y + row_idx * pitch
            draw.ellipse(
                (cx - radius, cy - radius, cx + radius, cy + radius),
                fill=GOLD,
            )


# --------------------------------------------------------------------------
# Line icons for the ALSO TODAY rows: a small pictogram inside a circle
# of 42 px diameter centred on (cx, cy), stroked 2 px wide.
# --------------------------------------------------------------------------
def draw_icon(draw, cx, cy, kind, colour):
    draw.ellipse((cx - 21, cy - 21, cx + 21, cy + 21), outline=colour, width=3)
    w = 2
    if kind == "globe":
        # Meridians and the equator of a wireframe globe.
        draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), outline=colour, width=w)
        draw.ellipse((cx - 5, cy - 12, cx + 5, cy + 12), outline=colour, width=w)
        draw.line((cx - 12, cy, cx + 12, cy), fill=colour, width=w)
    elif kind == "rocket":
        # Triangular body, a porthole and a filled exhaust flame.
        draw.polygon(
            [(cx, cy - 13), (cx - 8, cy + 6), (cx + 8, cy + 6)],
            outline=colour, width=w,
        )
        draw.ellipse((cx - 3, cy - 4, cx + 3, cy + 2), outline=colour, width=w)
        draw.polygon(
            [(cx - 4, cy + 8), (cx + 4, cy + 8), (cx, cy + 14)], fill=colour
        )
    elif kind == "chart":
        # A line that climbs, wobbles and dives, with an arrowhead down.
        draw.line((cx - 13, cy + 12, cx + 13, cy + 12), fill=colour, width=w)
        draw.line((cx - 13, cy - 10, cx - 4, cy - 2), fill=colour, width=w)
        draw.line((cx - 4, cy - 2, cx + 4, cy + 3), fill=colour, width=w)
        draw.line((cx + 4, cy + 3, cx + 13, cy + 10), fill=colour, width=w)
        draw.polygon(
            [(cx + 13, cy + 4), (cx + 13, cy + 12), (cx + 6, cy + 11)],
            fill=colour,
        )
    elif kind == "leaf":
        # Leaf outline with a stem and two side veins.
        draw.polygon(
            [(cx, cy - 13), (cx + 11, cy - 4), (cx + 9, cy + 8),
             (cx, cy + 13), (cx - 9, cy + 8), (cx - 11, cy - 4)],
            outline=colour, width=w,
        )
        draw.line((cx, cy - 10, cx, cy + 11), fill=colour, width=w)
        draw.line((cx, cy - 2, cx + 6, cy - 6), fill=colour, width=w)
        draw.line((cx, cy + 3, cx - 6, cy - 1), fill=colour, width=w)
    elif kind == "swirl":
        # Cyclone: two rings of opposing arcs around a calm eye.
        for k in range(3):
            start = 120 * k
            draw.arc((cx - 12, cy - 12, cx + 12, cy + 12), start, start + 100,
                     fill=colour, width=w)
            inner = start + 180
            draw.arc((cx - 6, cy - 6, cx + 6, cy + 6), inner, inner + 100,
                     fill=colour, width=w)
        draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=colour)


# --------------------------------------------------------------------------
# The day's news. Photo files live in assets/; headlines and decks are
# set in capitals, newspaper style.
# --------------------------------------------------------------------------
LEAD_STORIES = [
    {
        "photo": "media-generation-trump-plane-night-0-f12400ba-06c9-4b0d-a00e-100e4edfadc2.webp",
        "headline": "TRUMP DELAYS IRAN DECISION TO 2027",
        "deck": "“WE’LL SEE AFTER JANUARY 1,” HE SAYS ABOARD AIR "
                "FORCE ONE; SENATE REJECTS WAR-POWERS CURB 51–48",
    },
    {
        "photo": "media-generation-cyclone-akvan-0-a7665993-77a3-4ceb-9152-15f1595f5e73.webp",
        "headline": "CYCLONE AKVAN MAKES LANDFALL",
        "deck": "STORM CROSSES COAST NEAR GOPALPUR BY NOON; 300,000 "
                "EVACUATED, RED ALERTS, 69 TRAINS CANCELLED",
    },
    {
        "photo": "media-generation-vice-city-neon-0-c7e53773-cc3a-4fcd-beb5-e269edc67f9f.webp",
        "headline": "GTA VI SALES TOP $2.36 BILLION (EST.)",
        "deck": "SENSOR TOWER ESTIMATE: 24.6M COPIES ON DAY ONE; "
                "TAKE-TWO HAS NOT CONFIRMED THE FIGURES",
    },
]

BRIEF_ITEMS = [
    ("globe", NAVY, "UK–EU RESET SUMMIT IN BRUSSELS",
     "FOOD TRADE, YOUTH MOBILITY DEALS ON THE TABLE"),
    ("rocket", NAVY, "SAMSUNG NAMES NEW MEMORY CHIEF",
     "HWANG LEADS MEMORY AMID RECORD AI-CHIP PROFITS"),
    ("chart", RED, "WALL STREET TUMBLES AGAIN",
     "S&P 500 FALLS 2.0%: SIXTH STRAIGHT DAY OF LOSSES"),
    ("leaf", NAVY, "COP31: CLOSING DAY, NO DEAL YET",
     "FOSSIL-FREE DRAFT FACES FINAL TEST IN ANTALYA"),
    ("swirl", NAVY, "CYCLONE XAVIER: COOK ISLANDS ALERT",
     "GALE WARNING SUWARROW; STORM ALERT PUKAPUKA"),
]

TICKER_TEXT = (
    "AKVAN: 423 RESCUE TEAMS DEPLOYED  •  GTA VI: 75% OF COPIES "
    "ON PLAYSTATION (EST.)  •  TRUMP: “NOT RUSHING” ON IRAN"
)

EDITION_DATE = "FRIDAY, 20 NOVEMBER 2026"


# --------------------------------------------------------------------------
# Page furniture
# --------------------------------------------------------------------------
def photo_story(canvas, draw, x, y, w, block_h, photo_h, story):
    """One photo story: the picture on top of a bordered caption box
    with a red accent bar, headline and deck."""
    photo_path = os.path.join(ASSET_DIR, story["photo"])
    photo = Image.open(photo_path).convert("RGB")
    canvas.paste(fill_frame(photo, w, photo_h), (x, y))

    caption_top = y + photo_h
    caption_bottom = y + block_h
    draw.rectangle((x, caption_top, x + w, caption_bottom),
                   outline=RULE, width=1)
    draw.rectangle((x, caption_top, x + 5, caption_bottom), fill=RED)

    pad = 16
    text_x = x + 5 + pad
    text_w = w - 5 - pad - 12
    head_font = shrink_to_fit(draw, story["headline"], 31, text_w)
    draw.text((text_x, caption_top + 10), story["headline"],
              font=head_font, fill=NAVY)

    deck_font = load_font(SANS_REG, 20)
    line_y = caption_top + 10 + head_font.size + 8
    for line in wrap_lines(draw, story["deck"], deck_font, text_w):
        draw.text((text_x, line_y), line, font=deck_font, fill=INK)
        line_y += 25


def briefs_panel(draw, x, y, w, h):
    """The ALSO TODAY panel: navy title bar over five icon rows."""
    draw.rectangle((x, y, x + w, y + h), outline=RULE, width=1)
    bar_h = 62
    draw.rectangle((x, y, x + w, y + bar_h), fill=NAVY)
    draw.text((x + 18, y + 12), "ALSO TODAY",
              font=load_font(SANS_BOLD, 34), fill=WHITE)

    rows_top = y + bar_h
    row_h = (h - bar_h) // len(BRIEF_ITEMS)
    text_x = x + 70
    text_w = w - 70 - 12
    for idx, (kind, colour, head, sub) in enumerate(BRIEF_ITEMS):
        row_y = rows_top + idx * row_h
        if idx:
            draw.line((x + 1, row_y, x + w - 1, row_y), fill=RULE, width=1)
        centre_y = row_y + row_h // 2
        draw_icon(draw, x + 38, centre_y, kind, colour)
        head_font = shrink_to_fit(draw, head, 20, text_w)
        draw.text((text_x, row_y + 8), head, font=head_font, fill=NAVY)
        sub_font = shrink_to_fit(draw, sub, 17, text_w, SANS_REG)
        draw.text((text_x, row_y + 32), sub, font=sub_font, fill=INK)


def render():
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(canvas)

    # Masthead: navy band, date on the left, dotted map on the right,
    # and a gold rule closing the band.
    date_font = shrink_to_fit(draw, EDITION_DATE, 54, 720)
    draw.rectangle((0, 0, PAGE_W, MASTHEAD_H), fill=NAVY)
    text_depth = date_font.getbbox(EDITION_DATE)[3]
    draw.text((MARGIN, (MASTHEAD_H - text_depth) // 2), EDITION_DATE,
              font=date_font, fill=WHITE)
    map_width = 60 * 4
    stamp_map(draw, PAGE_W - MARGIN - map_width, 10)
    draw.rectangle((0, MASTHEAD_H, PAGE_W, MASTHEAD_H + 4), fill=GOLD)

    # Two lead stories across the top row, the third at bottom-left,
    # and the briefs panel filling the bottom-right cell.
    photo_story(canvas, draw, COL_XS[0], ROW1_Y, COL_W, ROW1_H, 300,
                LEAD_STORIES[0])
    photo_story(canvas, draw, COL_XS[1], ROW1_Y, COL_W, ROW1_H, 300,
                LEAD_STORIES[1])
    photo_story(canvas, draw, COL_XS[0], ROW2_Y, COL_W, ROW2_H, 280,
                LEAD_STORIES[2])
    briefs_panel(draw, COL_XS[1], ROW2_Y, COL_W, ROW2_H)

    # Ticker: navy strip with the wire line centred in white.
    draw.rectangle((0, PAGE_H - TICKER_H, PAGE_W, PAGE_H), fill=NAVY)
    tick_font = shrink_to_fit(draw, TICKER_TEXT, 26, PAGE_W - 2 * MARGIN)
    tick_w = draw.textlength(TICKER_TEXT, font=tick_font)
    tick_y = PAGE_H - TICKER_H + (TICKER_H - tick_font.size) // 2 - 2
    draw.text(((PAGE_W - tick_w) // 2, tick_y), TICKER_TEXT,
              font=tick_font, fill=WHITE)

    canvas.save(OUTPUT_PNG, optimize=True)
    print("wrote {}: {}x{}, {} bytes".format(
        OUTPUT_PNG, PAGE_W, PAGE_H, os.path.getsize(OUTPUT_PNG)))


if __name__ == "__main__":
    render()
