#!/usr/bin/env python3
"""Build the news-image-20261120 front page, v3 (1024x1024 PNG).

One image summing up Friday 20 November 2026: three scene photos with
PIL-drawn headlines, an ALSO TODAY panel with five more stories, a dotted
world map in the header and a ticker footer. Every word is drawn by PIL;
the photos carry no baked-in text.

v3 fixes v2's faithfulness defects: the ICJ Myanmar ruling (delivered
19 Nov), the Voyager 1 light-day milestone (18 Nov), the Hayabusa2
announcement (17 Nov) and the Pete Rose pardon (announced 19 Nov) are
gone, and the GTA VI panel now uses Sensor Tower's updated estimate as
reported on 20 Nov, labelled (EST.). Every remaining item was verified
against reporting dated 20 November 2026.

Run:  python3 build_entry.py   -> writes entry.png next to this script.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

# ---------------------------------------------------------------- palette
W, H = 1024, 1024
PAPER = (244, 239, 230)      # warm newsprint background
NAVY = (24, 24, 96)          # header, footer, headlines
GOLD = (198, 160, 38)        # header rule + dotted map
INK = (28, 28, 28)
GREY = (105, 105, 105)
RULE = (203, 196, 182)       # card borders + row dividers
RED = (176, 32, 32)
WHITE = (255, 255, 255)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, start, max_width, path=BOLD):
    """Largest size (down from `start`) in font `path` that fits `max_width`."""
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, 10)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines."""
    lines, current = [], ""
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


def cover(photo, tw, th):
    """Centre-crop + resize a photo so it exactly fills (tw, th)."""
    iw, ih = photo.size
    scale = max(tw / iw, th / ih)
    nw, nh = round(iw * scale), round(ih * scale)
    big = photo.resize((nw, nh), Image.LANCZOS)
    x0, y0 = (nw - tw) // 2, (nh - th) // 2
    return big.crop((x0, y0, x0 + tw, y0 + th))


# ------------------------------------------------------- dotted world map
# Hand-drawn land mask ('#' = land), 60 cols x 20 rows. Rendered as gold
# dots in the header; rough continents are fine at this size.
WORLD = [
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


def dotted_map(draw, x0, y0, pitch=4, dot=2):
    for r, line in enumerate(WORLD):
        for c, ch in enumerate(line):
            if ch == "#":
                cx, cy = x0 + c * pitch, y0 + r * pitch
                draw.ellipse(
                    (cx - dot, cy - dot, cx + dot, cy + dot), fill=GOLD
                )


# ------------------------------------------------------------ panel icons
def pictogram(draw, cx, cy, kind, colour):
    """Tiny line icon inside a 42px circle, centred on (cx, cy)."""
    draw.ellipse((cx - 21, cy - 21, cx + 21, cy + 21), outline=colour, width=3)
    w = 2
    if kind == "scales":  # world court
        draw.line((cx, cy - 11, cx, cy + 11), fill=colour, width=w)
        draw.line((cx - 11, cy - 8, cx + 11, cy - 8), fill=colour, width=w)
        draw.ellipse((cx - 14, cy - 8, cx - 8, cy - 2), outline=colour, width=w)
        draw.ellipse((cx + 8, cy - 8, cx + 14, cy - 2), outline=colour, width=w)
        draw.line((cx - 7, cy + 11, cx + 7, cy + 11), fill=colour, width=w)
    elif kind == "planet":  # voyager
        draw.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=colour)
        draw.ellipse((cx - 15, cy - 5, cx + 15, cy + 5), outline=colour, width=w)
    elif kind == "rocket":  # hayabusa2
        draw.polygon(
            [(cx, cy - 13), (cx - 8, cy + 6), (cx + 8, cy + 6)],
            outline=colour, width=w,
        )
        draw.ellipse((cx - 3, cy - 4, cx + 3, cy + 2), outline=colour, width=w)
        draw.polygon([(cx - 4, cy + 8), (cx + 4, cy + 8), (cx, cy + 14)], fill=colour)
    elif kind == "globe":  # europe / russia talks
        draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), outline=colour, width=w)
        draw.ellipse((cx - 5, cy - 12, cx + 5, cy + 12), outline=colour, width=w)
        draw.line((cx - 12, cy, cx + 12, cy), fill=colour, width=w)
    elif kind == "burst":  # houthi strike
        for k in range(8):
            import math
            a = math.pi * k / 4
            draw.line(
                (cx + 5 * math.cos(a), cy + 5 * math.sin(a),
                 cx + 13 * math.cos(a), cy + 13 * math.sin(a)),
                fill=colour, width=w,
            )
        draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=colour)
    elif kind == "chart":  # wall street sell-off
        draw.line((cx - 13, cy + 12, cx + 13, cy + 12), fill=colour, width=w)
        draw.line((cx - 13, cy - 10, cx - 4, cy - 2), fill=colour, width=w)
        draw.line((cx - 4, cy - 2, cx + 4, cy + 3), fill=colour, width=w)
        draw.line((cx + 4, cy + 3, cx + 13, cy + 10), fill=colour, width=w)
        draw.polygon([(cx + 13, cy + 4), (cx + 13, cy + 12), (cx + 6, cy + 11)],
                     fill=colour)
    elif kind == "leaf":  # cop31 climate talks
        draw.polygon(
            [(cx, cy - 13), (cx + 11, cy - 4), (cx + 9, cy + 8),
             (cx, cy + 13), (cx - 9, cy + 8), (cx - 11, cy - 4)],
            outline=colour, width=w,
        )
        draw.line((cx, cy - 10, cx, cy + 11), fill=colour, width=w)
        draw.line((cx, cy - 2, cx + 6, cy - 6), fill=colour, width=w)
        draw.line((cx, cy + 3, cx - 6, cy - 1), fill=colour, width=w)
    elif kind == "swirl":  # cyclone xavier
        import math
        for k in range(3):
            a0 = 120 * k
            draw.arc((cx - 12, cy - 12, cx + 12, cy + 12), a0, a0 + 100,
                     fill=colour, width=w)
            a1 = a0 + 180
            draw.arc((cx - 6, cy - 6, cx + 6, cy + 6), a1, a1 + 100,
                     fill=colour, width=w)
        draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=colour)
    elif kind == "ball":  # pete rose
        draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), outline=colour, width=w)
        draw.arc((cx - 12, cy - 16, cx + 4, cy + 16), 300, 60, fill=colour, width=w)
        draw.arc((cx - 4, cy - 16, cx + 12, cy + 16), 120, 240, fill=colour, width=w)


# ------------------------------------------------------------------- data
TOP_STORIES = [
    {
        "photo": "media-generation-trump-plane-night-0-f12400ba-06c9-4b0d-a00e-100e4edfadc2.webp",
        "headline": "TRUMP DELAYS IRAN DECISION TO 2027",
        "deck": "\u201cWE\u2019LL SEE AFTER JANUARY 1,\u201d HE SAYS ABOARD AIR "
                "FORCE ONE; SENATE REJECTS WAR-POWERS CURB 51\u201348",
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

ALSO_TODAY = [
    ("globe", NAVY, "EUROPE READY FOR RUSSIA TALKS",
     "LEADERS BACK NEGOTIATIONS TO END UKRAINE WAR"),
    ("burst", RED, "HOUTHIS HIT RIYADH\u2019S TALLEST TOWER",
     "PIF HQ DAMAGED; SAUDI SAYS NO INJURIES"),
    ("chart", RED, "WALL STREET TUMBLES AGAIN",
     "S&P 500 FALLS 2.0%: SIXTH STRAIGHT DAY OF LOSSES"),
    ("leaf", NAVY, "COP31: CLOSING DAY, NO DEAL YET",
     "FOSSIL-FREE DRAFT FACES FINAL TEST IN ANTALYA"),
    ("swirl", NAVY, "CYCLONE XAVIER: COOK ISLANDS ALERT",
     "GALE WARNING SUWARROW; STORM ALERT PUKAPUKA"),
]

TICKER = ("AKVAN: 423 RESCUE TEAMS DEPLOYED  \u2022  GTA VI: 75% OF COPIES "
          "ON PLAYSTATION (EST.)  \u2022  TRUMP: \u201cNOT RUSHING\u201d ON IRAN")

# ------------------------------------------------------------------ layout
MARGIN = 24
HEADER_H = 100
FOOTER_H = 56
GAP = 16
COL_W = (W - 3 * MARGIN) // 2          # 476
COL_X = (MARGIN, MARGIN + COL_W + GAP)  # 24, 524
TOP_Y = HEADER_H + 12                  # 112
TOP_H = 430
BOT_Y = TOP_Y + TOP_H + GAP            # 558
BOT_H = (H - FOOTER_H) - BOT_Y         # 410


def story_card(canvas, draw, x, y, w, photo_h, story):
    """Photo on top, headline + deck in a white caption box below."""
    photo = Image.open(os.path.join(ASSETS, story["photo"])).convert("RGB")
    canvas.paste(cover(photo, w, photo_h), (x, y))
    cap_y = y + photo_h
    cap_bottom = y + (TOP_H if y == TOP_Y else BOT_H)
    draw.rectangle((x, cap_y, x + w, cap_bottom), outline=RULE, width=1)
    # red editorial accent bar down the left edge of the caption
    draw.rectangle((x, cap_y, x + 5, cap_bottom), fill=RED)
    pad = 16
    text_x = x + 5 + pad
    head = fit(draw, story["headline"], 31, w - 5 - pad - 12)
    draw.text((text_x, cap_y + 10), story["headline"], font=head, fill=NAVY)
    deck_font = font(REGULAR, 20)
    lines = wrap(draw, story["deck"], deck_font, w - 5 - pad - 12)
    yy = cap_y + 10 + head.size + 8
    for line in lines:
        draw.text((text_x, yy), line, font=deck_font, fill=INK)
        yy += 25


def also_today_panel(draw, x, y, w, h):
    draw.rectangle((x, y, x + w, y + h), outline=RULE, width=1)
    bar_h = 62
    draw.rectangle((x, y, x + w, y + bar_h), fill=NAVY)
    draw.text((x + 18, y + 12), "ALSO TODAY", font=font(BOLD, 34), fill=WHITE)
    rows_y, rows_h = y + bar_h, h - bar_h
    row_h = rows_h // len(ALSO_TODAY)
    for i, (kind, colour, head, sub) in enumerate(ALSO_TODAY):
        ry = rows_y + i * row_h
        if i:
            draw.line((x + 1, ry, x + w - 1, ry), fill=RULE, width=1)
        cy = ry + row_h // 2
        pictogram(draw, x + 38, cy, kind, colour)
        tx = x + 70
        avail = w - 70 - 12
        head_f = fit(draw, head, 20, avail)
        draw.text((tx, ry + 8), head, font=head_f, fill=NAVY)
        sub_f = fit(draw, sub, 17, avail, REGULAR)
        draw.text((tx, ry + 32), sub, font=sub_f, fill=INK)


def build():
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)

    # header: date left, dotted world map right, gold rule underneath
    date = "FRIDAY, 20 NOVEMBER 2026"
    date_font = fit(draw, date, 54, 720)
    draw.rectangle((0, 0, W, HEADER_H), fill=NAVY)
    ascent = date_font.getbbox(date)[3]
    draw.text((MARGIN, (HEADER_H - ascent) // 2), date,
              font=date_font, fill=WHITE)
    map_w = 60 * 4
    dotted_map(draw, W - MARGIN - map_w, 10)
    draw.rectangle((0, HEADER_H, W, HEADER_H + 4), fill=GOLD)

    # three photo stories: two across the top, one bottom-left
    story_card(canvas, draw, COL_X[0], TOP_Y, COL_W, 300, TOP_STORIES[0])
    story_card(canvas, draw, COL_X[1], TOP_Y, COL_W, 300, TOP_STORIES[1])
    story_card(canvas, draw, COL_X[0], BOT_Y, COL_W, 280, TOP_STORIES[2])

    # also-today panel, bottom-right
    also_today_panel(draw, COL_X[1], BOT_Y, COL_W, BOT_H)

    # footer ticker
    draw.rectangle((0, H - FOOTER_H, W, H), fill=NAVY)
    tick = fit(draw, TICKER, 26, W - 2 * MARGIN)
    tw = draw.textlength(TICKER, font=tick)
    draw.text(((W - tw) // 2, H - FOOTER_H + (FOOTER_H - tick.size) // 2 - 2),
              TICKER, font=tick, fill=WHITE)

    canvas.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {W}x{H}, {size} bytes")


if __name__ == "__main__":
    build()
