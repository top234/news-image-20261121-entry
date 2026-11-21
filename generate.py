#!/usr/bin/env python3
"""Generate entry.png for news-image-20261121: one front page summing up
Saturday 21 November 2026's world news. Deterministic (seeded), PIL only,
renders to 1024x1024 PNG. Run: python3 generate.py [out.png]

Stories (as reported 21 Nov 2026):
  HERO   Russian missiles land in Poland; NATO calls it a grave violation;
         Warsaw seeks NATO reinforcements (Nov 21 follow-up).
  PANEL1 Trump dials into a European allies meeting on Ukraine, after the
         Xi / Putin trilateral summit in Shenzhen.
  PANEL2 S&P 500 slides into correction as AI shares plunge.
  PANEL3 Russian strike hits Kryvyi Rih: 2 killed, 42 hurt.
"""
import math
import random
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
RNG = random.Random(20261121)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_OB = FD + "DejaVuSans-Oblique.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(x0, y), (x1, y)], fill=c)


def star4(d, cx, cy, r_out, r_in, fill):
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy - r * math.sin(ang)))
    d.polygon(pts, fill=fill)


def main(out_path):
    img = Image.new("RGB", (W, H), (246, 241, 231))  # cream paper
    d = ImageDraw.Draw(img, "RGBA")

    # ---- masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 8], fill=(178, 34, 34))  # red top rule
    draw_centered(d, W // 2, 14, "THE WORLD", font(SERIF_B, 92), (12, 12, 12))
    d.line([(48, 118), (W - 48, 118)], fill=(12, 12, 12), width=4)
    draw_centered(
        d, W // 2, 128,
        "SATURDAY, 21 NOVEMBER 2026  \u2022  THE DAY IN ONE PICTURE",
        font(SANS_B, 25), (12, 12, 12),
    )

    # ---- hero: night sky over Poland ------------------------------------
    hx0, hy0, hx1, hy1 = 28, 168, W - 28, 606
    vgrad(d, (hx0, hy0, hx1, hy1), (8, 16, 46), (30, 48, 96))
    # stars
    for _ in range(90):
        x = RNG.randint(hx0 + 6, hx1 - 6)
        y = RNG.randint(hy0 + 6, hy1 - 180)
        r = RNG.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, RNG.randint(120, 220)))
    # moon glow
    for r, a in ((46, 26), (34, 46), (24, 90)):
        d.ellipse([hx0 + 66 - r, hy0 + 40 - r, hx0 + 66 + r, hy0 + 40 + r], fill=(235, 240, 255, a))
    d.ellipse([hx0 + 48, hy0 + 22, hx0 + 84, hy0 + 58], fill=(245, 247, 255, 255))
    # missile trail: bright arc from upper right to impact lower left-centre
    ix, iy = 330, 465  # impact point, just above the headline band
    sx, sy = 940, 210  # trail start (top right)
    # glow layers, wide to narrow
    for width, col in ((26, (255, 90, 20, 60)), (14, (255, 120, 30, 130)), (7, (255, 170, 60, 220))):
        pts = []
        for t in [i / 40 for i in range(41)]:
            x = sx + (ix - sx) * t
            y = sy + (iy - sy) * t - 150 * math.sin(math.pi * t)
            pts.append((x, y))
        d.line(pts, fill=col, width=width, joint="curve")
    # missile body at the head of the trail
    mx, my = sx - 46, sy + 26
    d.line([(sx, sy), (mx, my)], fill=(255, 220, 160, 255), width=6)
    d.polygon([(mx, my - 5), (mx - 16, my), (mx, my + 5)], fill=(255, 220, 160, 255))
    # explosion glow at impact
    for r, a in ((120, 40), (84, 80), (52, 140), (28, 220)):
        d.ellipse([ix - r, iy - r, ix + r, iy + r], fill=(255, 150, 40, a))
    d.ellipse([ix - 16, iy - 16, ix + 16, iy + 16], fill=(255, 230, 150, 255))
    # skyline silhouette
    base = hy1
    x = hx0
    while x < hx1:
        bw = min(RNG.randint(46, 96), hx1 - x)
        bh = RNG.randint(46, 150)
        d.rectangle([x, base - bh, min(x + bw, hx1), base], fill=(5, 8, 20))
        for _ in range(max(1, bw // 16)):
            wx = RNG.randint(x + 5, max(x + 6, min(x + bw - 9, hx1 - 9)))
            wy = RNG.randint(base - bh + 8, base - 14)
            if RNG.random() < 0.55:
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 205, 90, 235))
        x += bw + RNG.randint(2, 10)
    # NATO emblem: blue disc + white compass star, top-left of hero
    ex, ey, er = hx0 + 62, hy0 + 96, 44
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(0, 49, 130, 255))
    d.ellipse([ex - er, ey - er, ex + er, ey + er], outline=(255, 255, 255, 255), width=3)
    star4(d, ex, ey, 34, 9, (255, 255, 255, 255))
    d.text((ex + er + 12, ey - 14), "NATO", font=font(SANS_B, 26), fill=(255, 255, 255, 255))
    # BREAKING tag
    tag = "BREAKING"
    tf = font(SANS_B, 24)
    tw = d.textlength(tag, font=tf)
    d.rectangle([hx1 - tw - 36, hy0 + 14, hx1 - 14, hy0 + 48], fill=(178, 34, 34))
    d.text((hx1 - tw - 25, hy0 + 19), tag, font=tf, fill=(255, 255, 255))
    # headline band at hero bottom
    d.rectangle([hx0, hy1 - 132, hx1, hy1], fill=(5, 8, 20, 215))
    d.text((hx0 + 26, hy1 - 122), "RUSSIAN MISSILES", font=font(SANS_B, 56), fill=(255, 255, 255))
    d.text((hx0 + 26, hy1 - 64), "LAND IN POLAND", font=font(SANS_B, 56), fill=(255, 255, 255))
    # subline sits just under the hero
    draw_centered(
        d, W // 2, 616,
        "NATO calls it a grave violation \u2014 Warsaw seeks reinforcements",
        font(SANS_B, 24), (140, 20, 20),
    )

    # ---- three story panels ---------------------------------------------
    d.line([(28, 652), (W - 28, 652)], fill=(12, 12, 12), width=3)
    panels = [
        ("TRUMP CALLS", "EUROPE ON UKRAINE", "After the summit with Xi and Putin, talks turn to Kyiv.", "flags"),
        ("MARKETS", "TUMBLE", "S&P 500 slides into correction as AI shares plunge.", "chart"),
        ("STRIKE HITS", "KRYVYI RIH", "2 killed, 42 hurt as Russia hits a Ukrainian city.", "city"),
    ]
    pw, gap, py0 = 308, 14, 668
    for i, (h1, h2, sub, kind) in enumerate(panels):
        px0 = 28 + i * (pw + gap)
        px1 = px0 + pw
        # illustration strip
        iy0, iy1 = py0, py0 + 128
        if kind == "flags":
            d.rectangle([px0, iy0, px1, iy1], fill=(233, 228, 216))
            # US flag
            fx, fy, fw, fh = px0 + 12, iy0 + 24, 88, 56
            for s in range(7):
                d.rectangle([fx, fy + s * 8, fx + fw, fy + s * 8 + 8],
                            fill=(178, 34, 34) if s % 2 == 0 else (255, 255, 255))
            d.rectangle([fx, fy, fx + 36, fy + 32], fill=(30, 50, 110))
            for r_ in range(3):
                for c_ in range(4):
                    d.ellipse([fx + 4 + c_ * 9, fy + 4 + r_ * 10, fx + 7 + c_ * 9, fy + 7 + r_ * 10],
                              fill=(255, 255, 255))
            # EU flag
            ex0, ey0 = px0 + 112, iy0 + 24
            d.rectangle([ex0, ey0, ex0 + 88, ey0 + 56], fill=(0, 49, 130))
            for k in range(12):
                a = 2 * math.pi * k / 12 - math.pi / 2
                d.ellipse([ex0 + 44 + 18 * math.cos(a) - 2, ey0 + 28 + 18 * math.sin(a) - 2,
                           ex0 + 44 + 18 * math.cos(a) + 2, ey0 + 28 + 18 * math.sin(a) + 2],
                          fill=(255, 210, 0))
            # Ukraine flag
            ux0, uy0 = px0 + 212, iy0 + 24
            d.rectangle([ux0, uy0, ux0 + 84, uy0 + 28], fill=(0, 91, 187))
            d.rectangle([ux0, uy0 + 28, ux0 + 84, uy0 + 56], fill=(255, 213, 0))
        elif kind == "chart":
            d.rectangle([px0, iy0, px1, iy1], fill=(16, 24, 44))
            pts = [(px0 + 14 + t * (pw - 40) / 6, iy0 + 26 + v) for t, v in
                   enumerate([0, 8, 4, 26, 22, 52, 88])]
            d.line(pts, fill=(220, 50, 40), width=5, joint="curve")
            for (qx, qy) in pts:
                d.ellipse([qx - 4, qy - 4, qx + 4, qy + 4], fill=(255, 120, 100))
            d.polygon([(px1 - 34, iy0 + 104), (px1 - 14, iy0 + 104), (px1 - 24, iy0 + 122)],
                      fill=(220, 50, 40))
            d.text((px0 + 14, iy0 + 96), "-3.7%", font=font(SANS_B, 26), fill=(255, 90, 70))
        else:  # city: damaged building + smoke
            vgrad(d, (px0, iy0, px1, iy1), (120, 120, 125), (70, 70, 78))
            d.rectangle([px0 + 60, iy0 + 52, px0 + 150, iy1], fill=(30, 30, 36))
            d.polygon([(px0 + 60, iy0 + 52), (px0 + 105, iy0 + 22), (px0 + 150, iy0 + 52)],
                      fill=(30, 30, 36))
            d.rectangle([px0 + 170, iy0 + 78, px0 + 250, iy1], fill=(44, 44, 50))
            for (wx, wy) in [(px0 + 74, iy0 + 70), (px0 + 100, iy0 + 70), (px0 + 126, iy0 + 70),
                             (px0 + 74, iy0 + 96), (px0 + 100, iy0 + 96), (px0 + 186, iy0 + 96),
                             (px0 + 214, iy0 + 96)]:
                d.rectangle([wx, wy, wx + 10, wy + 12], fill=(255, 205, 90, 220))
            for (cx, cy, r) in [(px0 + 120, iy0 + 16, 14), (px0 + 142, iy0 + 6, 18),
                                (px0 + 168, iy0 + 14, 12)]:
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 200, 205, 170))
        # headlines: auto-fit so no line ever overflows its column
        hsize = 27
        while hsize > 18:
            hf = font(SANS_B, hsize)
            if (d.textlength(h1, font=hf) <= pw and d.textlength(h2, font=hf) <= pw):
                break
            hsize -= 1
        hf = font(SANS_B, hsize)
        d.text((px0, py0 + 142), h1, font=hf, fill=(12, 12, 12))
        d.text((px0, py0 + 142 + hsize + 4), h2, font=hf, fill=(12, 12, 12))
        sf = font(SANS, 19)
        y = py0 + 142 + 2 * (hsize + 4) + 10
        for line in wrap(d, sub, sf, pw):
            d.text((px0, y), line, font=sf, fill=(40, 40, 40))
            y += 24

    # ---- footer ----------------------------------------------------------
    d.line([(28, 962), (W - 28, 962)], fill=(12, 12, 12), width=3)
    draw_centered(
        d, W // 2, 976,
        "WORLD NEWS  \u2022  21 NOVEMBER 2026  \u2022  AS REPORTED TODAY",
        font(SANS_B, 22), (12, 12, 12),
    )

    img.save(out_path, "PNG", optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
