"""Rebuild assets/*.png from the Kenney Tiny Farm tilemap (CC0, kenney.nl).

Needs Pillow (not needed to play the game):  pip install pillow
Run from the project root:                   python tools/build_assets.py
"""

from __future__ import annotations

import random
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(__file__).with_name("kenney_tiny_farm_tilemap_packed.png")
OUT = ROOT / "assets"
T = 16

sheet = Image.open(SRC).convert("RGBA")


def tile(row, col):
    return sheet.crop((col * T, row * T, col * T + T, row * T + T))


# Kenney palette values read from the tilemap itself
OUTLINE = (63, 38, 49, 255)
SOIL_DARK = (184, 101, 66, 255)
SOIL_MID = (207, 130, 84, 255)
SOIL_LIGHT = (234, 165, 108, 255)
SOIL_PALE = (254, 201, 156, 255)
SAND = (225, 154, 101, 255)
GRASS_BASE = (132, 198, 105, 255)
GRASS_DARK = (78, 151, 76, 255)
GRASS_LIGHT = (198, 229, 141, 255)


def speckle(base, marks, seed, n):
    rng = random.Random(seed)
    img = Image.new("RGBA", (T, T), base)
    for _ in range(n):
        x, y = rng.randrange(T), rng.randrange(T)
        img.putpixel((x, y), rng.choice(marks))
    return img


# ---- soil + grass (generated so they tile without outlines) ----
soil_ok = speckle(SOIL_DARK, [SOIL_MID, (150, 80, 55, 255)], 1, 26)
soil_dry = speckle(SOIL_LIGHT, [SOIL_PALE, SOIL_MID], 2, 22)
soil_cracked = speckle(SAND, [SOIL_LIGHT, SOIL_MID], 3, 14)
for x, y in [(2, 3), (3, 4), (4, 5), (5, 6), (6, 6), (7, 7), (8, 8), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12),
             (7, 8), (6, 9), (5, 10), (5, 11), (4, 12), (9, 5), (10, 4), (11, 3), (12, 2)]:
    soil_cracked.putpixel((x, y), OUTLINE)
grass = speckle(GRASS_BASE, [GRASS_DARK, GRASS_LIGHT], 4, 22)

tiles = Image.new("RGBA", (T * 4, T), (0, 0, 0, 0))
for i, img in enumerate((soil_ok, soil_dry, soil_cracked, grass)):
    tiles.paste(img, (i * T, 0))
tiles.save(OUT / "tiles.png")

# ---- crops: 3 columns (good, mid, bad) x 3 rows (maize, soy, sorghum) ----
# Kenney has no soybean art; soy uses the closest leafy-green plants.
crop_map = [
    [(2, 6), (2, 5), (2, 7)],   # maize
    [(5, 5), (4, 5), (4, 7)],   # soy (approximation)
    [(5, 6), (5, 4), (5, 7)],   # sorghum (wheat-like grain)
]
crops = Image.new("RGBA", (T * 3, T * 3), (0, 0, 0, 0))
for r, row in enumerate(crop_map):
    for c, (tr, tc) in enumerate(row):
        crops.paste(tile(tr, tc), (c * T, r * T))
crops.save(OUT / "crops.png")

# ---- farmer: Kenney farmer with hat, plus small face edits for the moods ----
farmer = tile(9, 1)
FACE_DARK = (38, 43, 68, 255)


def mood(name):
    img = farmer.copy()
    if name == "happy":
        # open grin with teeth, rosy cheeks
        img.putpixel((7, 9), FACE_DARK)
        img.putpixel((9, 9), FACE_DARK)
        img.putpixel((8, 9), (255, 255, 255, 255))
        for x, y in [(5, 9), (11, 9)]:
            img.putpixel((x, y), (242, 132, 98, 255))
    elif name == "worried":
        # raised inner eyebrows, small open mouth, blue sweat drop
        for x, y in [(5, 6), (6, 6), (10, 6), (11, 6)]:
            img.putpixel((x, y), (118, 59, 54, 255))
        img.putpixel((8, 9), FACE_DARK)
        for x, y in [(12, 8), (12, 9)]:
            img.putpixel((x, y), (140, 200, 255, 255))
    return img


for m in ("happy", "neutral", "worried"):
    mood(m).save(OUT / ("farmer_%s.png" % m))

# ---- background 320x180 (scaled x4 to the 1280x720 screen) ----
BW, BH = 320, 180
bg = Image.new("RGBA", (BW, BH), (126, 192, 238, 255))
px = bg.load()
for y in range(BH):
    for x in range(BW):
        if y > 112:
            px[x, y] = (140, 200, 241, 255)
        elif y > 92:
            px[x, y] = (133, 196, 240, 255)

CLOUD = (150, 208, 244, 255)
CLOUD_HI = (166, 217, 247, 255)


def cloud(cx, cy, w):
    for dx in range(-w, w + 1):
        for dy in range(-3, 4):
            if (dx / w) ** 2 + (dy / 3.2) ** 2 <= 1:
                bg.putpixel((cx + dx, cy + dy), CLOUD)
    for dx in range(-w + 3, w - 2):
        bg.putpixel((cx + dx, cy - 3), CLOUD_HI)


cloud(268, 22, 16)
cloud(300, 44, 11)
cloud(232, 60, 9)
cloud(120, 14, 10)


def hills(base_y, amp, color, seed, hi=None):
    rng = random.Random(seed)
    ph1, ph2 = rng.random() * 6, rng.random() * 6
    import math

    for x in range(BW):
        top = base_y - int(amp * (0.6 * math.sin(x / 38 + ph1) + 0.4 * math.sin(x / 15 + ph2)))
        for y in range(top, BH):
            bg.putpixel((x, y), color)
        if hi:
            bg.putpixel((x, top), hi)


hills(128, 6, (110, 183, 130, 255), 11, (150, 208, 160, 255))
hills(144, 5, GRASS_BASE, 7, GRASS_LIGHT)

rng = random.Random(5)
for y in range(150, BH):
    for _ in range(3):
        x = rng.randrange(BW)
        bg.putpixel((x, y), rng.choice([GRASS_DARK, GRASS_LIGHT]))


def stamp(row, col, x, y):
    bg.alpha_composite(tile(row, col), (x, y))


# keep the bottom ~60 screen px free of art: the key-help text is drawn there
for x in (14, 44, 96, 150, 205, 262, 300):
    stamp(0, 3, x, 114 + (x % 6))
for x, kind in ((70, (2, 3)), (178, (1, 3)), (232, (2, 3)), (28, (1, 3))):
    stamp(kind[0], kind[1], x, 112 + (x % 5))
for x in (120, 188, 250, 306, 224):
    stamp(3, 3, x, 136 + (x % 8))
for x in (34, 160, 280):
    stamp(6, 11, x, 140 + (x % 5))
stamp(6, 5, 226, 146)
stamp(6, 5, 84, 147)
bg.save(OUT / "background.png")
print("assets rebuilt in", OUT)
