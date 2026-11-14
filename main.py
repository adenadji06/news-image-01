"""news-image-01: sum up 13 November 2026's world news in one image.

A pure-stdlib Python program (no network, no installed packages) that
draws a 1024x1024 newspaper front page and writes /output/entry.png.

The stories, all reported on Friday 13 November 2026:
  1. FAA nationwide ground stop: a telecom failure halted all US
     departures for 4+ hours (from ~3:36pm ET, lifted ~8:15pm ET);
     1,000+ flights cancelled, ~10,000 delayed. Officials blamed
     the ageing analog air-traffic system; no evidence of a cyber
     or AI attack; Trump called it a national emergency.
  2. Nvidia chief Jensen Huang resigned after 33 years amid a
     personal scandal; Trump called it "a terrible thing".
  3. Ukraine peace talks advanced: US envoys Kushner and Witkoff
     met Zelensky in Dublin; Europe agreed to join the next round.
  4. China ran a large unannounced Pacific exercise around Taiwan,
     detailed by Taipei officials on Friday.
  5. Houthi forces attacked Saudi Arabia's East-West oil pipeline
     and a facility at Yanbu.
  Also: the Microsoft 365 outage eased; Qatar and Turkey signed a
  mutual defence pact; the IEA forecast a Q4 oil surplus.

Text is rendered with an embedded 5x7 bitmap font, so every label
is crisp and legible at small sizes -- no AI-generated garbled text.
"""
import os
import struct
import zlib
from pathlib import Path

W, H = 1024, 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (176, 42, 32)
BLUE = (29, 78, 137)
SKY = (178, 214, 235)
GREEN = (34, 120, 60)
GOLD = (212, 175, 55)
ORANGE = (224, 110, 30)
WHITE = (255, 255, 255)
GREY = (120, 120, 120)
DARKGREY = (70, 70, 70)
YELLOW = (245, 205, 60)

# 5x7 bitmap font: each glyph is 7 rows of 5 bits ("#" = on).
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill_rect(self, x, y, w, h, c):
        for yy in range(max(0, y), min(self.h, y + h)):
            base = (yy * self.w + max(0, x)) * 3
            for xx in range(max(0, x), min(self.w, x + w)):
                i = (yy * self.w + xx) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c, t=1):
        self.fill_rect(x, y, w, t, c)
        self.fill_rect(x, y + h - t, w, t, c)
        self.fill_rect(x, y, t, h, c)
        self.fill_rect(x + w - t, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x0 + a, y0 + b, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) ** 2) ** 0.5) if abs(yy - cy) <= r else 0
            if fill:
                self.fill_rect(cx - dx, yy, 2 * dx + 1, 1, c)
            else:
                self.set(cx - dx, yy, c)
                self.set(cx + dx, yy, c)

    def polygon(self, pts, c):
        # Scanline fill of a simple polygon.
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.fill_rect(int(xs[i]), y, int(xs[i + 1]) - int(xs[i]) + 1, 1, c)

    def text(self, x, y, s, scale, c):
        s = s.upper()
        for ch in s:
            g = FONT.get(ch, FONT[" "])
            for r, row in enumerate(g):
                for col, bit in enumerate(row):
                    if bit == "1":
                        self.fill_rect(x + col * scale, y + r * scale, scale, scale, c)
            x += 6 * scale

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_center(self, cx, y, s, scale, c):
        self.text(cx - self.text_w(s, scale) // 2, y, s, scale, c)

    def wrapped(self, x, y, max_w, s, scale, c, lh=None):
        lh = lh or (7 * scale + 4 * scale)
        words, line = s.upper().split(" "), ""
        for word in words:
            trial = (line + " " + word).strip()
            if self.text_w(trial, scale) <= max_w or not line:
                line = trial
            else:
                self.text(x, y, line, scale, c)
                y += lh
                line = word
        if line:
            self.text(x, y, line, scale, c)
            y += lh
        return y


def png_bytes(cv):
    raw = b"".join(b"\x00" + bytes(cv.px[y * cv.w * 3:(y + 1) * cv.w * 3])
                   for y in range(cv.h))
    comp = zlib.compress(raw, 9)

    def chunk(typ, data):
        return struct.pack(">I", len(data)) + typ + data + struct.pack(
            ">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


def draw_plane(cv, cx, cy, s, body, wing):
    # Side-view airliner, nose to the right, parked on the tarmac.
    cv.polygon([(cx - 52 * s, cy - 4 * s), (cx + 30 * s, cy - 8 * s),
                (cx + 52 * s, cy), (cx + 30 * s, cy + 8 * s),
                (cx - 52 * s, cy + 8 * s)], body)
    cv.polygon([(cx - 48 * s, cy - 4 * s), (cx - 38 * s, cy - 26 * s),
                (cx - 28 * s, cy - 4 * s)], body)  # tail fin
    cv.polygon([(cx - 12 * s, cy + 4 * s), (cx + 14 * s, cy + 4 * s),
                (cx + 32 * s, cy + 28 * s), (cx + 10 * s, cy + 28 * s)], body)  # wing
    for wx in (-34, -6, 22):
        cv.fill_rect(cx + wx * s, cy + 8 * s, 3 * s, 6 * s, INK)  # wheels
    for wx in (-24, 0, 24):
        cv.fill_rect(cx + wx * s, cy - 3 * s, 6 * s, 4 * s, SKY)  # windows


def draw_page():
    cv = Canvas(W, H, PAPER)
    cv.rect(8, 8, W - 16, H - 16, INK, 4)

    # Masthead.
    cv.text_center(W // 2, 26, "THE WORLD IN ONE PICTURE", 5, INK)
    cv.text_center(W // 2, 72, "FRIDAY, 13 NOVEMBER 2026", 3, RED)
    cv.fill_rect(24, 104, W - 48, 3, INK)
    cv.fill_rect(24, 110, W - 48, 2, RED)

    # Lead story: FAA ground stop.
    x, y, w, h = 24, 122, W - 48, 320
    cv.fill_rect(x, y, w, h, WHITE)
    cv.rect(x, y, w, h, INK, 3)
    cv.fill_rect(x + 3, y + 3, w - 6, 180, SKY)  # sky
    cv.circle(x + 860, y + 55, 26, (255, 236, 160))  # sun
    cv.circle(x + 180, y + 70, 30, WHITE)  # clouds
    cv.circle(x + 240, y + 62, 36, WHITE)
    cv.circle(x + 620, y + 52, 26, WHITE)
    cv.circle(x + 665, y + 58, 32, WHITE)
    cv.fill_rect(x + 3, y + 183, w - 6, 20, DARKGREY)  # tarmac
    draw_plane(cv, x + 220, y + 150, 1, BLUE, RED)
    draw_plane(cv, x + 500, y + 160, 1, (90, 90, 90), RED)
    draw_plane(cv, x + 780, y + 150, 1, BLUE, RED)
    cv.fill_rect(x + 3, y + 203, w - 6, 4, RED)  # stop line
    cv.text_center(W // 2, y + 216, "U.S. FLIGHTS GROUNDED NATIONWIDE", 4, INK)
    cv.wrapped(x + 28, y + 256, w - 56,
               "FAA halts all departures for 4 hours after a telecom "
               "failure; 1,000+ flights cancelled, 10,000 delayed.",
               2, INK)

    # Two story rows.
    def panel(px, py, pw, ph, tag, tag_c):
        cv.fill_rect(px, py, pw, ph, WHITE)
        cv.rect(px, py, pw, ph, INK, 3)
        cv.fill_rect(px + 3, py + 3, pw - 6, 26, tag_c)
        cv.text_center(px + pw // 2, py + 9, tag, 2, WHITE)
        return px + 16, py + 44

    # Nvidia.
    px, py = panel(24, 456, 476, 246, "TECHNOLOGY", GREEN)
    cv.fill_rect(px + 130, py + 8, 180, 96, GREEN)
    cv.fill_rect(px + 146, py + 24, 148, 64, (20, 90, 45))
    for i in range(5):
        cv.fill_rect(px + 118, py + 22 + i * 16, 12, 8, GOLD)
        cv.fill_rect(px + 310, py + 22 + i * 16, 12, 8, GOLD)
    cv.text_center(px + 220, py + 38, "NV", 4, WHITE)
    cv.wrapped(px, py + 118, 444, "NVIDIA CHIEF RESIGNS", 3, INK)
    cv.wrapped(px, py + 156, 444,
               "CEO Huang quits after 33 years; Trump calls the "
               "scandal \"a terrible thing\".", 2, INK)

    # Ukraine.
    px, py = panel(524, 456, 476, 246, "DIPLOMACY", BLUE)
    cv.fill_rect(px + 150, py + 8, 140, 44, BLUE)
    cv.fill_rect(px + 150, py + 52, 140, 44, YELLOW)
    cv.circle(px + 220, py + 52, 34, WHITE)
    cv.circle(px + 220, py + 52, 28, BLUE)
    cv.line(px + 220, py + 24, px + 220, py + 80, WHITE, 4)
    cv.line(px + 220, py + 52, px + 196, py + 74, WHITE, 4)
    cv.line(px + 220, py + 52, px + 244, py + 74, WHITE, 4)
    cv.wrapped(px, py + 118, 444, "UKRAINE TALKS ADVANCE", 3, INK)
    cv.wrapped(px, py + 156, 444,
               "U.S. envoys meet Zelensky in Dublin; Europe to join "
               "the next round.", 2, INK)

    # Taiwan drills.
    px, py = panel(24, 714, 476, 250, "ASIA", RED)
    cv.fill_rect(px, py + 60, 440, 34, (200, 225, 240))
    cv.polygon([(px + 120, py + 60), (px + 320, py + 60),
                (px + 300, py + 94), (px + 140, py + 94)], DARKGREY)
    cv.fill_rect(px + 210, py + 8, 6, 52, INK)
    cv.polygon([(px + 216, py + 8), (px + 252, py + 20), (px + 216, py + 32)], RED)
    for wy in (py + 100, py + 108):
        for wx in range(0, 440, 44):
            cv.line(px + wx, wy, px + wx + 22, wy - 8, BLUE, 3)
    cv.wrapped(px, py + 122, 444, "CHINA DRILLS NEAR TAIWAN", 3, INK)
    cv.wrapped(px, py + 156, 444,
               "Taipei details a large unannounced Pacific exercise "
               "around the island.", 2, INK)

    # Houthi pipeline attack.
    px, py = panel(524, 714, 476, 250, "MIDDLE EAST", (140, 60, 20))
    cv.fill_rect(px + 60, py + 40, 320, 22, DARKGREY)
    cv.fill_rect(px + 60, py + 30, 18, 42, GREY)
    cv.fill_rect(px + 362, py + 30, 18, 42, GREY)
    cv.polygon([(px + 210, py + 8), (px + 236, py + 44), (px + 224, py + 62),
                (px + 244, py + 62), (px + 210, py + 96), (px + 176, py + 62),
                (px + 196, py + 62), (px + 184, py + 44)], ORANGE)
    cv.polygon([(px + 210, py + 34), (px + 224, py + 56), (px + 214, py + 70),
                (px + 196, py + 56)], (255, 220, 80))
    cv.wrapped(px, py + 122, 444, "SAUDI PIPELINE ATTACKED", 3, INK)
    cv.wrapped(px, py + 156, 444,
               "Houthis hit the East-West line and an oil facility "
               "at Yanbu.", 2, INK)

    # Footer strip.
    cv.fill_rect(24, 972, W - 48, 3, INK)
    cv.text_center(W // 2, 982,
                   "ALSO: MICROSOFT OUTAGE EASES - QATAR-TURKEY "
                   "DEFENCE PACT - IEA: OIL SURPLUS", 2, INK)
    return cv


def main():
    out = Path(OUT)
    out.mkdir(parents=True, exist_ok=True)
    data = png_bytes(draw_page())
    (out / "entry.png").write_bytes(data)
    print("wrote %d bytes" % len(data))


if __name__ == "__main__":
    main()
