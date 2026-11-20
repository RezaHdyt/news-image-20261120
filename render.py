#!/usr/bin/env python3
"""Render the news-image-20261120 front page: a 1024x1024 PNG newspaper
front page summing up Friday 20 November 2026 in 36 real stories, with
12 flat hand-drawn illustration panels.

Run:  python3 render.py   -> writes entry.png next to this script.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 18
CW = W - 2 * MARGIN  # 988 px of content width

PAPER = (250, 246, 238)
INK = (26, 26, 26)
GRAY = (102, 102, 102)
GRID_RULE = (198, 196, 186)
RED = (158, 27, 27)
RULE = (40, 40, 40)

FD = "/usr/share/fonts/truetype"
SERIF_B = os.path.join(FD, "dejavu/DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FD, "dejavu/DejaVuSans-Bold.ttf")
SANS = os.path.join(FD, "dejavu/DejaVuSans.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- text utils

def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, font, max_w, max_lines):
    """Wrap and truncate to max_lines, adding an ellipsis if text is cut."""
    lines = wrap(d, text, font, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + "\u2026", font=font) > max_w:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] = lines[-1] + "\u2026"
    return lines


def draw_lines(d, x, y, lines, font, fill, leading):
    for i, line in enumerate(lines):
        d.text((x, y + i * leading), line, font=font, fill=fill)
    return y + len(lines) * leading


def poly_points(cx, cy, r, n, rot=-90):
    return [
        (cx + r * math.cos(math.radians(rot + i * 360 / n)),
         cy + r * math.sin(math.radians(rot + i * 360 / n)))
        for i in range(n)
    ]


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def panel_border(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=1)


# ------------------------------------------------------------------- panels
# Each panel draws a flat illustration inside the box (x, y, w, h).

def panel_summit(d, x, y, w, h):
    """Trilateral summit: US, China and Russia flags over a table."""
    d.rectangle([x, y, x + w, y + h], fill=(216, 231, 245))
    gy = y + h - 26
    d.rectangle([x, gy, x + w, y + h], fill=(214, 200, 178))
    # red carpet
    d.rectangle([x + w * 0.12, gy + 8, x + w * 0.88, gy + 20], fill=RED)

    def flag_usa(px, py, fw, fh):
        for i in range(7):
            col = (178, 34, 52) if i % 2 == 0 else (245, 245, 240)
            d.rectangle([px, py + i * fh / 7, px + fw, py + (i + 1) * fh / 7],
                        fill=col)
        d.rectangle([px, py, px + fw * 0.42, py + fh * 4 / 7], fill=(40, 60, 120))
        for r in range(3):
            for c in range(4):
                sx = px + 4 + c * (fw * 0.42 - 8) / 3
                sy = py + 4 + r * (fh * 4 / 7 - 8) / 2
                d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))

    def flag_china(px, py, fw, fh):
        d.rectangle([px, py, px + fw, py + fh], fill=(222, 41, 16))
        d.polygon(star_points(px + fw * 0.25, py + fh * 0.3, 8, 3.2),
                  fill=(255, 222, 0))
        for sx, sy in [(0.55, 0.18), (0.68, 0.32), (0.68, 0.52), (0.55, 0.62)]:
            d.polygon(star_points(px + fw * sx, py + fh * sy, 3.5, 1.4),
                      fill=(255, 222, 0))

    def flag_russia(px, py, fw, fh):
        for i, col in enumerate([(245, 245, 240), (0, 90, 170), (210, 30, 30)]):
            d.rectangle([px, py + i * fh / 3, px + fw, py + (i + 1) * fh / 3],
                        fill=col)

    fw, fh = 62, 38
    for frac, flag_fn in [(0.16, flag_usa), (0.5, flag_china), (0.84, flag_russia)]:
        px = x + w * frac - fw / 2
        py = y + 10
        d.line([(px - 2, py - 2), (px - 2, gy)], fill=(70, 70, 70), width=2)
        d.ellipse([px - 4, py - 5, px, py - 1], fill=(200, 170, 60))
        flag_fn(px, py, fw, fh)
        d.rectangle([px, py, px + fw, py + fh], outline=(90, 90, 90), width=1)

    # table with three chairs and three signed papers
    tx0, tx1 = x + w * 0.30, x + w * 0.70
    for cfrac in (0.36, 0.5, 0.64):
        cx = x + w * cfrac
        d.rectangle([cx - 11, gy - 27, cx + 11, gy - 14], fill=(96, 64, 32))
        d.rectangle([cx - 11, gy - 14, cx + 11, gy - 12], fill=(96, 64, 32))
    d.rectangle([tx0, gy - 14, tx1, gy - 2], fill=(122, 82, 46))
    d.rectangle([tx0 + 4, gy - 2, tx0 + 10, gy + 1], fill=(96, 64, 32))
    d.rectangle([tx1 - 10, gy - 2, tx1 - 4, gy + 1], fill=(96, 64, 32))
    for pfrac in (0.36, 0.5, 0.64):
        px = x + w * pfrac
        d.rectangle([px - 8, gy - 19, px + 8, gy - 14], fill=(255, 255, 255))
        d.line([(px - 5, gy - 17), (px + 5, gy - 17)], fill=(150, 150, 150), width=1)


def panel_kyiv(d, x, y, w, h):
    """Night attack on Kyiv: skyline, missile trails, explosions."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 38, 62))
    for sx, sy in [(0.08, 0.12), (0.2, 0.06), (0.35, 0.15), (0.55, 0.08),
                   (0.7, 0.14), (0.88, 0.07), (0.95, 0.2), (0.45, 0.05)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(220, 225, 235))
    base = y + h - 12
    buildings = [(0.02, 0.09, 0.42), (0.12, 0.07, 0.58), (0.20, 0.10, 0.34),
                 (0.31, 0.08, 0.62), (0.40, 0.09, 0.45), (0.50, 0.07, 0.55),
                 (0.58, 0.11, 0.36), (0.70, 0.08, 0.60), (0.79, 0.09, 0.42),
                 (0.89, 0.09, 0.52)]
    for bx, bw, bh in buildings:
        d.rectangle([x + w * bx, base - h * bh, x + w * (bx + bw), base],
                    fill=(14, 20, 34))
    # lit windows
    for wx, wy in [(0.05, 0.68), (0.14, 0.5), (0.24, 0.72), (0.34, 0.48),
                   (0.44, 0.62), (0.53, 0.52), (0.63, 0.7), (0.73, 0.5),
                   (0.83, 0.66), (0.92, 0.56), (0.36, 0.62), (0.75, 0.66)]:
        d.rectangle([x + w * wx, y + h * wy, x + w * wx + 4, y + h * wy + 5],
                    fill=(255, 200, 100))
    # bridge silhouette along the bottom
    d.rectangle([x + w * 0.05, base - 4, x + w * 0.95, base - 1], fill=(10, 14, 24))
    for tx in (0.25, 0.75):
        d.rectangle([x + w * tx - 2, base - 18, x + w * tx + 2, base - 1],
                    fill=(10, 14, 24))
    d.arc([x + w * 0.05, base - 30, x + w * 0.45, base + 6], 180, 360,
          fill=(10, 14, 24), width=2)
    d.arc([x + w * 0.55, base - 30, x + w * 0.95, base + 6], 180, 360,
          fill=(10, 14, 24), width=2)
    # missile trails
    for (x0, y0, x1, y1) in [(0.06, 0.10, 0.30, 0.42), (0.55, 0.06, 0.72, 0.38),
                            (0.88, 0.12, 0.78, 0.45)]:
        d.line([(x + w * x0, y + h * y0), (x + w * x1, y + h * y1)],
               fill=(255, 220, 120), width=2)
        d.ellipse([x + w * x1 - 3, y + h * y1 - 3, x + w * x1 + 3, y + h * y1 + 3],
                  fill=(255, 240, 180))
    # explosions
    for ex, ey, r in [(0.30, 0.44, 13), (0.72, 0.40, 10)]:
        d.polygon(star_points(x + w * ex, y + h * ey, r, r * 0.4, 8),
                  fill=(255, 140, 0))
        d.polygon(star_points(x + w * ex, y + h * ey, r * 0.5, r * 0.2, 8),
                  fill=(255, 220, 60))
        d.ellipse([x + w * ex - 16, y + h * ey - 22, x + w * ex - 4, y + h * ey - 10],
                  fill=(120, 120, 130))
        d.ellipse([x + w * ex + 2, y + h * ey - 26, x + w * ex + 14, y + h * ey - 14],
                  fill=(110, 110, 120))


def panel_nasdaq(d, x, y, w, h):
    """Anthropic's Nasdaq debut: rising chart, +17%."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 248, 240))
    for gy in (0.3, 0.55, 0.8):
        d.line([(x + 4, y + h * gy), (x + w - 4, y + h * gy)],
               fill=(215, 228, 215), width=1)
    vals = [0.25, 0.4, 0.35, 0.6, 0.8]
    for i, v in enumerate(vals):
        bx = x + 6 + i * (w - 12) / len(vals)
        bw = (w - 12) / len(vals) * 0.55
        bh = v * h * 0.55
        d.rectangle([bx, y + h - 8 - bh, bx + bw, y + h - 8],
                    fill=(120, 190, 120))
    pts = [(x + 6, y + h - 14), (x + w * 0.35, y + h * 0.55),
           (x + w * 0.65, y + h * 0.42), (x + w - 10, y + 9)]
    d.line(pts, fill=(20, 140, 60), width=3, joint="curve")
    d.polygon([(x + w - 9, y + 6), (x + w - 17, y + 12), (x + w - 8, y + 15)],
              fill=(20, 140, 60))
    d.text((x + 6, y + 2), "+17%", font=F(SANS_B, 11), fill=(20, 140, 60))


def panel_icj(d, x, y, w, h):
    """ICJ ruling: scales of justice."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 236, 240))
    cx, base = x + w / 2, y + h - 6
    d.polygon([(cx - 8, y + 9), (cx + 8, y + 9), (cx, y + 2)], fill=(60, 60, 60))
    d.line([(cx, y + 9), (cx, base)], fill=(60, 60, 60), width=2)
    d.line([(cx - 26, y + 13), (cx + 26, y + 13)], fill=(60, 60, 60), width=2)
    for px in (cx - 26, cx + 26):
        d.line([(px, y + 13), (px - 8, y + 27)], fill=(60, 60, 60), width=1)
        d.line([(px, y + 13), (px + 8, y + 27)], fill=(60, 60, 60), width=1)
        d.pieslice([px - 9, y + 25, px + 9, y + 37], 0, 180, fill=(180, 150, 60))
    d.rectangle([cx - 13, base - 2, cx + 13, base + 1], fill=(60, 60, 60))
    d.rectangle([cx - 8, base - 5, cx + 8, base - 2], fill=(60, 60, 60))


def panel_drones(d, x, y, w, h):
    """UK drone pledge: drones flying over green ground."""
    d.rectangle([x, y, x + w, y + h], fill=(212, 232, 248))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(140, 180, 120))
    for i in range(9):
        px = x + 6 + i * 9
        py = y + 32 - i * 1.5
        d.line([(px, py), (px + 5, py - 1)], fill=(130, 150, 170), width=1)

    def drone(cx, cy, s):
        d.rectangle([cx - 5 * s, cy - 2 * s, cx + 5 * s, cy + 2 * s],
                    fill=(50, 55, 65))
        for dx in (-7 * s, 7 * s):
            d.line([(cx + dx - 4 * s, cy - 3 * s), (cx + dx + 4 * s, cy - 3 * s)],
                   fill=(50, 55, 65), width=2)
            d.line([(cx + dx, cy - 2 * s), (cx + dx, cy + 2 * s)],
                   fill=(50, 55, 65), width=1)

    drone(x + w * 0.25, y + h * 0.35, 1.1)
    drone(x + w * 0.55, y + h * 0.58, 0.9)
    drone(x + w * 0.8, y + h * 0.30, 1.2)


def panel_markets(d, x, y, w, h):
    """Market plunge: falling red candles and a diving line."""
    d.rectangle([x, y, x + w, y + h], fill=(248, 240, 240))
    for fx, fy in [(0.15, 0.30), (0.32, 0.45), (0.50, 0.55), (0.68, 0.68),
                   (0.85, 0.80)]:
        cx = x + w * fx
        top = y + h * fy - 8
        d.line([(cx, top - 4), (cx, top + 12)], fill=(180, 30, 30), width=1)
        d.rectangle([cx - 3, top, cx + 3, top + 8], fill=(200, 40, 40))
    pts = [(x + 6, y + 8), (x + w * 0.3, y + h * 0.35),
           (x + w * 0.6, y + h * 0.55), (x + w - 9, y + h - 10)]
    d.line(pts, fill=(180, 30, 30), width=3, joint="curve")
    d.polygon([(x + w - 8, y + h - 8), (x + w - 17, y + h - 12),
               (x + w - 10, y + h - 19)], fill=(180, 30, 30))
    d.text((x + 6, y + h - 17), "-2,200", font=F(SANS_B, 10), fill=(180, 30, 30))


def panel_bridge(d, x, y, w, h):
    """Crimean Bridge hit: arch bridge, explosion, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(205, 225, 240))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(70, 120, 170))
    for fx in (0.2, 0.5, 0.8):
        d.rectangle([x + w * fx - 2, y + h * 0.45, x + w * fx + 2, y + h * 0.62],
                    fill=(90, 100, 110))
    d.rectangle([x + 4, y + h * 0.42, x + w - 4, y + h * 0.48], fill=(70, 80, 90))
    d.arc([x + w * 0.3, y + h * 0.18, x + w * 0.7, y + h * 0.55], 180, 360,
          fill=(70, 80, 90), width=3)
    ex, ey = x + w * 0.62, y + h * 0.36
    d.polygon(star_points(ex, ey, 12, 5, 8), fill=(255, 140, 0))
    d.polygon(star_points(ex, ey, 6, 2.5, 8), fill=(255, 220, 60))
    for sx, sy, r in [(0.55, 0.20, 5), (0.62, 0.14, 6), (0.70, 0.20, 4)]:
        d.ellipse([x + w * sx - r, y + h * sy - r, x + w * sx + r, y + h * sy + r],
                  fill=(150, 150, 150))


def panel_tower(d, x, y, w, h):
    """Riyadh PIF tower damaged: tall tower, smoke, drone."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 240))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(180, 175, 165))
    cx = x + w * 0.5
    d.polygon([(cx - 10, y + h - 8), (cx - 7, y + 10), (cx + 9, y + 10),
               (cx + 12, y + h - 8)], fill=(140, 165, 195))
    for i in range(5):
        yy = y + 14 + i * 6
        d.line([(cx - 8, yy), (cx + 9, yy)], fill=(110, 140, 175), width=1)
    d.line([(cx - 7, y + 10), (cx + 12, y + h - 8)], fill=(110, 140, 175), width=1)
    for sx, sy, r in [(0.42, 0.12, 4), (0.50, 0.06, 5), (0.58, 0.12, 4)]:
        d.ellipse([x + w * sx - r, y + h * sy - r, x + w * sx + r, y + h * sy + r],
                  fill=(140, 140, 140))
    dx, dy = x + w * 0.82, y + h * 0.30
    d.rectangle([dx - 4, dy - 1, dx + 4, dy + 1], fill=(50, 55, 65))
    d.line([(dx - 7, dy - 3), (dx + 7, dy - 3)], fill=(50, 55, 65), width=1)


def panel_tanker(d, x, y, w, h):
    """Tanker hits a mine: ship, flames, spiked mine."""
    d.rectangle([x, y, x + w, y + h], fill=(208, 226, 240))
    d.rectangle([x, y + h * 0.6, x + w, y + h], fill=(60, 110, 160))
    for wy in (0.72, 0.86):
        for i in range(5):
            wx = x + 6 + i * 18
            d.arc([wx, y + h * wy, wx + 12, y + h * wy + 6], 180, 360,
                  fill=(140, 190, 230), width=1)
    d.polygon([(x + 6, y + h * 0.52), (x + w - 14, y + h * 0.52),
               (x + w - 6, y + h * 0.62), (x + 6, y + h * 0.62)],
              fill=(40, 45, 55))
    d.rectangle([x + w * 0.62, y + h * 0.36, x + w * 0.78, y + h * 0.52],
                fill=(240, 240, 235))
    d.rectangle([x + w * 0.68, y + h * 0.30, x + w * 0.74, y + h * 0.36],
                fill=(200, 60, 40))
    mx, my = x + w * 0.30, y + h * 0.66
    d.ellipse([mx - 6, my - 6, mx + 6, my + 6], fill=(20, 20, 20))
    for a in range(0, 360, 45):
        r1 = math.radians(a)
        d.line([(mx + 5 * math.cos(r1), my + 5 * math.sin(r1)),
                (mx + 9 * math.cos(r1), my + 9 * math.sin(r1))],
               fill=(20, 20, 20), width=2)
    for fx, fh in [(0.40, 10), (0.48, 14), (0.56, 9)]:
        d.polygon([(x + w * fx - 4, y + h * 0.52),
                   (x + w * fx, y + h * 0.52 - fh),
                   (x + w * fx + 4, y + h * 0.52)], fill=(255, 140, 0))
    for sx, sy, r in [(0.44, 0.30, 4), (0.50, 0.24, 5), (0.56, 0.30, 4)]:
        d.ellipse([x + w * sx - r, y + h * sy - r, x + w * sx + r, y + h * sy + r],
                  fill=(150, 150, 150))


def panel_cop(d, x, y, w, h):
    """COP31: globe and leaf."""
    d.rectangle([x, y, x + w, y + h], fill=(236, 244, 234))
    cx, cy = x + w * 0.38, y + h * 0.5
    for a in range(0, 360, 30):
        r1 = math.radians(a)
        d.line([(cx + 20 * math.cos(r1), cy + 20 * math.sin(r1)),
                (cx + 25 * math.cos(r1), cy + 25 * math.sin(r1))],
               fill=(230, 200, 60), width=2)
    d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=(90, 160, 220),
              outline=(60, 130, 190))
    d.ellipse([cx - 10, cy - 8, cx + 2, cy + 2], fill=(90, 180, 90))
    d.ellipse([cx + 2, cy + 4, cx + 12, cy + 12], fill=(90, 180, 90))
    d.ellipse([cx - 4, cy - 14, cx + 6, cy - 8], fill=(90, 180, 90))
    lx, ly = x + w * 0.80, y + h * 0.55
    d.polygon([(lx, ly - 14), (lx + 9, ly - 2), (lx, ly + 10), (lx - 9, ly - 2)],
              fill=(60, 160, 60))
    d.line([(lx, ly - 12), (lx, ly + 8)], fill=(40, 120, 40), width=1)
    d.line([(lx, ly + 10), (lx + 3, ly + 15)], fill=(120, 80, 40), width=2)


def panel_baseball(d, x, y, w, h):
    """Pete Rose: baseball diamond, ball and bat."""
    d.rectangle([x, y, x + w, y + h], fill=(96, 165, 96))
    d.polygon([(x + w / 2, y + 6), (x + w - 8, y + h / 2),
               (x + w / 2, y + h - 6), (x + 8, y + h / 2)],
              fill=(214, 186, 140))
    d.polygon([(x + w / 2, y + 12), (x + w - 14, y + h / 2),
               (x + w / 2, y + h - 12), (x + 14, y + h / 2)],
              fill=(96, 165, 96))
    bx, by = x + w * 0.62, y + h * 0.38
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 255, 255),
              outline=(200, 60, 50))
    d.arc([bx - 5, by - 5, bx + 5, by + 5], 300, 60, fill=(200, 60, 50), width=1)
    d.arc([bx - 5, by - 5, bx + 5, by + 5], 120, 240, fill=(200, 60, 50), width=1)
    d.line([(x + 10, y + h - 8), (x + 26, y + 10)], fill=(150, 100, 50), width=4)
    d.ellipse([x + 24, y + 6, x + 30, y + 12], fill=(150, 100, 50))


def panel_sport(d, x, y, w, h):
    """Sport: soccer ball and basketball."""
    d.rectangle([x, y, x + w, y + h], fill=(32, 48, 68))
    sx, sy = x + w * 0.27, y + h * 0.5
    d.ellipse([sx - 11, sy - 11, sx + 11, sy + 11], fill=(245, 245, 240))
    d.polygon(poly_points(sx, sy, 5, 5), fill=(30, 30, 30))
    for px, py in [(sx - 8, sy - 6), (sx + 8, sy - 6), (sx, sy + 8)]:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(30, 30, 30))
    bx, by = x + w * 0.73, y + h * 0.5
    d.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=(230, 120, 40),
              outline=(180, 80, 20))
    d.line([(bx - 11, by), (bx + 11, by)], fill=(120, 60, 20), width=1)
    d.line([(bx, by - 11), (bx, by + 11)], fill=(120, 60, 20), width=1)
    d.arc([bx - 11, by - 11, bx + 3, by + 11], 300, 60, fill=(120, 60, 20), width=1)
    d.arc([bx - 3, by - 11, bx + 11, by + 11], 120, 240, fill=(120, 60, 20), width=1)


# -------------------------------------------------------------------- stories
# All 36 stories are real events from Friday 20 November 2026.

LEADS = [
    {
        "label": "WORLD \u00b7 SHENZHEN SUMMIT",
        "headline": "Trump, Xi & Putin hold first-ever trilateral summit in Shenzhen",
        "summary": "Leaders sign a four-point \u2018Declaration toward Peace\u2019 \u2014 UN reform, "
                   "energy cooperation, official immunity and a nuclear-risk dialogue.",
        "panel": panel_summit,
    },
    {
        "label": "WAR IN UKRAINE",
        "headline": "Russia launches massive missile and drone attack on Ukraine",
        "summary": "At least five killed in Kyiv and Lviv; three Dnipro bridges damaged; "
                   "power grid \u2018extremely critical\u2019 \u2014 hours after the summit.",
        "panel": panel_kyiv,
    },
]

# (headline, summary or None, panel or None)
MEDIUMS = [
    ("Anthropic debuts on Nasdaq as first frontier AI firm to go public",
     "Shares rise 17% on day one.", panel_nasdaq),
    ("ICJ rules Myanmar committed genocide against the Rohingya",
     "Seven-year case ends in a 9\u20136 vote.", panel_icj),
    ("UK pledges 1,000+ drones for Ukraine in \u00a3260m package",
     None, panel_drones),
    ("Asian markets plunge on AI-bubble fears; Dow falls below 50,000",
     "Taiwan stocks down 2,200+ points.", panel_markets),
    ("Ukraine hits Crimean Bridge a third time with Neptune missiles",
     "Putin vows a \u2018far more painful\u2019 response.", panel_bridge),
    ("Europe ready for Ukraine peace talks as ~40 partners pledge aid",
     "Germany, France, UK pledge air defence and energy aid.", None),
    ("Houthi attack damages Riyadh\u2019s 80-storey PIF tower",
     "Saudi air defences down two Houthi drones.", panel_tower),
    ("Tanker catches fire after hitting a mine east of the Strait of Hormuz",
     None, panel_tanker),
    ("US war with Iran has cost over $48bn, CSIS says",
     "Operations consumed over 30% of key munitions.", None),
    ("COP31 draft drops fossil-fuel phase-out",
     "Africa seeks tripled climate finance.", panel_cop),
]

# (headline, deck or None, panel or None)
SMALLS = [
    ("EU to summon Russian envoy over embassy damage in Kyiv",
     "Kallas announces the summons", None),
    ("Poland probes unknown objects near Ukraine border",
     "Air-threat warning lifts", None),
    ("Trump posthumously pardons baseball legend Pete Rose",
     None, panel_baseball),
    ("US Senate rejects Iran war-powers resolution 51\u201348",
     None, None),
    ("US sanctions Comancheros & \u2018Ndrangheta",
     "Two crime groups targeted", None),
    ("UK\u2013EU to agree youth mobility scheme",
     "Young people to live and work more easily", None),
    ("Estonia to close border with Russia from December",
     None, None),
    ("Israeli airstrike hits Hezbollah missile facility in eastern Lebanon",
     None, None),
    ("Israel one-day operation in central Gaza demolishes Hamas tunnel",
     None, None),
    ("Iraqi forces to deploy in Kataib Hezbollah stronghold",
     "Jurf al-Sakhar", None),
    ("Prabowo meets Xi, discusses South China Sea cooperation",
     None, None),
    ("Six dead in gas explosion in Ponichala, Georgia",
     None, None),
    ("5.6-magnitude quake near New Caledonia",
     None, None),
    ("Genoa airport halts flights after unidentified drones",
     None, None),
    ("One dead, 15 hurt in fire at 18-storey block in France",
     None, None),
    ("General strike in Spain disrupts ports & factories",
     None, None),
    ("Prague protesters demand media independence",
     None, None),
    ("Bukele to register for third presidential term in El Salvador",
     None, None),
    ("Senegal boat capsizing kills four",
     None, None),
    ("Malawi fuel crisis triggers violence",
     None, None),
    ("Argentina Senate approves permanent disability framework 71\u20130",
     None, None),
    ("US House panel: ~880,000 advanced AI chips approved for China sales",
     None, None),
    ("California targets Nvidia in China AI-chip probe",
     None, None),
    ("Chelsea beat PSG 1\u20130 in Women\u2019s Champions League",
     "Buurman 87\u2032 \u00b7 Knicks 102\u201399 Timberwolves \u00b7 Wembanyama 32, "
     "Spurs 124\u2013112 Clippers", panel_sport),
]


# --------------------------------------------------------------------- layout

def section_label(d, rule_y, text):
    """A small red label straddling a horizontal rule."""
    font = F(SANS_B, 11)
    tw = d.textlength(text, font=font)
    d.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=RULE, width=1)
    d.rectangle([MARGIN, rule_y - 7, MARGIN + tw + 12, rule_y + 7], fill=PAPER)
    d.text((MARGIN + 6, rule_y - 7), text, font=font, fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- masthead
    d.line([(MARGIN, 12), (W - MARGIN, 12)], fill=RULE, width=1)
    mast_font = F(SERIF_B, 46)
    mast = "THE DAY IN WORLD NEWS"
    mw = d.textlength(mast, font=mast_font)
    d.text(((W - mw) / 2, 16), mast, font=mast_font, fill=INK)
    side_font = F(SANS_B, 10)
    d.text((MARGIN, 32), "WORLD EDITION", font=side_font, fill=GRAY)
    rs = "36 STORIES"
    d.text((W - MARGIN - d.textlength(rs, font=side_font), 32), rs,
           font=side_font, fill=GRAY)

    date_font = F(SANS_B, 17)
    date_text = "FRIDAY 20 NOVEMBER 2026"
    dw = d.textlength(date_text, font=date_font)
    dx = (W - dw) / 2
    d.text((dx, 70), date_text, font=date_font, fill=INK)
    d.line([(MARGIN, 79), (dx - 16, 79)], fill=RULE, width=1)
    d.line([(dx + dw + 16, 79), (W - MARGIN, 79)], fill=RULE, width=1)
    d.line([(MARGIN, 94), (W - MARGIN, 94)], fill=RULE, width=3)
    d.line([(MARGIN, 99), (W - MARGIN, 99)], fill=RULE, width=1)

    # ------------------------------------------------------------- leads
    LEAD_Y, LEAD_END = 106, 334
    col_w = (CW - 12) // 2  # 488
    lead_x = [MARGIN, MARGIN + col_w + 12]
    d.line([(W // 2, LEAD_Y), (W // 2, LEAD_END)], fill=GRID_RULE, width=1)
    label_font = F(SANS_B, 11)
    lead_head_font = F(SERIF_B, 20)
    lead_sum_font = F(SANS, 12)
    for i, lead in enumerate(LEADS):
        x = lead_x[i]
        d.text((x, LEAD_Y), lead["label"], font=label_font, fill=RED)
        px, py, pw, ph = x, LEAD_Y + 16, col_w, 108
        lead["panel"](d, px, py, pw, ph)
        panel_border(d, px, py, pw, ph)
        hy = py + ph + 4
        hlines = fit_lines(d, lead["headline"], lead_head_font, col_w, 3)
        end = draw_lines(d, x, hy, hlines, lead_head_font, INK, 25)
        slines = fit_lines(d, lead["summary"], lead_sum_font, col_w, 2)
        end = draw_lines(d, x, end + 3, slines, lead_sum_font, INK, 15)
        assert end <= LEAD_END, f"lead {i + 1} overflows: ends at {end}"
        assert not any(l.endswith("\u2026") for l in hlines + slines), \
            f"lead {i + 1} text was truncated"

    # ----------------------------------------------------------- mediums
    section_label(d, 336, "TOP STORIES")
    MED_Y, MED_ROW, MED_ROWS = 340, 58, 5
    d.line([(W // 2, MED_Y), (W // 2, MED_Y + MED_ROW * MED_ROWS - 4)],
           fill=GRID_RULE, width=1)
    for r in range(1, MED_ROWS):
        ry = MED_Y + r * MED_ROW
        d.line([(MARGIN, ry - 1), (W - MARGIN, ry - 1)], fill=GRID_RULE, width=1)
    med_head_font = F(SERIF_B, 15)
    med_sum_font = F(SANS, 11)
    for i, (headline, summary, panel_fn) in enumerate(MEDIUMS):
        row, col = divmod(i, 2)
        cx = lead_x[col]
        cy = MED_Y + row * MED_ROW
        if panel_fn is not None:
            px, py, pw, ph = cx, cy + 4, 92, 50
            panel_fn(d, px, py, pw, ph)
            panel_border(d, px, py, pw, ph)
            tx, tw = cx + 100, col_w - 100
        else:
            tx, tw = cx, col_w
        hlines = fit_lines(d, headline, med_head_font, tw, 2)
        slines = fit_lines(d, summary, med_sum_font, tw, 1) if summary else []
        assert not any(l.endswith("\u2026") for l in hlines + slines), \
            f"medium {i + 1} text was truncated"
        block_h = len(hlines) * 18 + (len(slines) * 14 if slines else 0)
        ty = cy + max(0, (MED_ROW - block_h) // 2)
        end = draw_lines(d, tx, ty, hlines, med_head_font, INK, 18)
        if slines:
            draw_lines(d, tx, end + 1, slines, med_sum_font, GRAY, 14)

    # ------------------------------------------------------------ smalls
    section_label(d, 634, "IN BRIEF")
    SMALL_Y = 638
    SMALL_ROWS = [44] * 7 + [58]
    col_xs = [MARGIN, MARGIN + 321 + 12, MARGIN + 2 * (321 + 12)]
    col_w_small = 321
    for vx in (MARGIN + 321 + 6, MARGIN + 2 * 321 + 12 + 6):
        d.line([(vx, SMALL_Y), (vx, SMALL_Y + sum(SMALL_ROWS))],
               fill=GRID_RULE, width=1)
    row_y = SMALL_Y
    small_head_font = F(SANS_B, 12)
    small_deck_font = F(SANS, 10)
    for i, (headline, deck, panel_fn) in enumerate(SMALLS):
        row, col = divmod(i, 3)
        if col == 0 and row > 0:
            d.line([(MARGIN, row_y - 1), (W - MARGIN, row_y - 1)],
                   fill=GRID_RULE, width=1)
        cy = SMALL_Y + sum(SMALL_ROWS[:row])
        rh = SMALL_ROWS[row]
        cx = col_xs[col]
        if panel_fn is not None:
            pw, ph = 62, min(50, rh - 6)
            panel_fn(d, cx, cy + (rh - ph) // 2, pw, ph)
            panel_border(d, cx, cy + (rh - ph) // 2, pw, ph)
            tx, tw = cx + 70, col_w_small - 70
        else:
            tx, tw = cx, col_w_small
        hlines = fit_lines(d, headline, small_head_font, tw, 2)
        deck_lines = fit_lines(d, deck, small_deck_font, tw, 2) if deck else []
        assert not any(l.endswith("\u2026") for l in hlines + deck_lines), \
            f"small {i + 1} text was truncated"
        block_h = len(hlines) * 15 + (len(deck_lines) * 13 if deck_lines else 0)
        assert block_h <= rh, f"small {i + 1} overflows: {block_h} > {rh}"
        ty = cy + (rh - block_h) // 2
        end = draw_lines(d, tx, ty, hlines, small_head_font, INK, 15)
        if deck_lines:
            draw_lines(d, tx, end + 1, deck_lines, small_deck_font, GRAY, 13)
        if col == 2:
            row_y = cy + rh

    # ------------------------------------------------------------ footer
    d.line([(MARGIN, 1008), (W - MARGIN, 1008)], fill=RULE, width=1)
    foot_font = F(SANS, 9)
    foot = ("All 36 stories are real events from Friday 20 November 2026 \u00b7 "
            "Illustrations drawn for this page \u00b7 Compiled from multiple news sources")
    fw = d.textlength(foot, font=foot_font)
    d.text(((W - fw) / 2, 1011), foot, font=foot_font, fill=GRAY)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {size} bytes")
    assert img.size[0] <= 1024 and img.size[1] <= 1024
    assert size <= 1048576, f"entry.png too big: {size} bytes"
    print(f"stories: {len(LEADS) + len(MEDIUMS) + len(SMALLS)}, "
          f"panels: 12")


if __name__ == "__main__":
    main()
