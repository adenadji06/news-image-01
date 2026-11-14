"""news-image-01: sum up 13 November 2026's world news in one image.

A pure-stdlib Python program (no network, no installed packages) that
draws a 1024x1024 newspaper front page and writes /output/entry.png.

Layout: masthead, the FAA ground stop as the dominant lead, a WORLD
MAP with all 30 stories pinned on it, and a three-column numbered
index of the day's stories across six regions.

The 30 stories, all reported on Friday 13 November 2026:
  North America
   1 FAA nationwide ground stop: telecom failure halted all US
     departures 4+ hours; 1,000+ flights cancelled, ~10,000 delayed.
   2 Nvidia chief Jensen Huang resigned after 33 years amid a
     personal scandal; Trump called it "a terrible thing".
   3 Stocks slipped on Wall Street after Nvidia's CEO exit.
   4 Trump told VP Vance to shift focus from Iran to domestic
     corruption and crime.
   5 Justice Dept won court approval to seize $1.2B in crypto
     stolen from Binance in the Oct 29 hack blamed on North Korea.
   6 Brooklyn building-collapse toll settled at 8 dead, 18 hurt.
   7 Back-to-back atmospheric rivers brought flood risk to
     Washington and Oregon.
   8 Global Microsoft 365 outage entered its second day.
   9 Federal report detailed failures in the Knowles fire that
     killed four firefighters.
  10 North American measles status awaited a formal PAHO ruling.
  Europe
  11 Ukraine peace talks advanced: US envoys Kushner and Witkoff
     met Zelensky in Dublin; Europe agreed to join the next round.
  12 European leaders agreed a five-country team to represent
     Europe in the talks.
  13 Ukraine fired almost 1,200 drones at Russia overnight, one
     of its biggest aerial attacks of the war.
  14 Moscow car bomb wounded Sergei Zavorotniy, ex-aide to former
     Ukrainian PM Azarov.
  15 IAEA raised concern over Iran's uninspected Isfahan
     enrichment plant.
  16 COP31 in Antalya: UN chief urged drastic emissions cuts.
  17 UN human rights chief: window closing to stop "killer
     robots" - treaty needed.
  26 IEA forecast a Q4 oil surplus: supply 105m barrels/day,
     1.7m above demand.
  Middle East & Asia
  18 Qatar and Turkey signed a mutual defence pact in Istanbul.
  19 China ran a large unannounced Pacific exercise around
     Taiwan, detailed by Taipei officials on Friday.
  20 Houthis attacked Saudi Arabia's East-West oil pipeline.
  21 US military said it downed two Iranian drones headed for
     Bahrain; Iran claimed a radar strike there.
  22 Four oil tankers hit by explosions in the Strait of Hormuz.
  23 Gulf Cooperation Council called for an end to Houthi attacks.
  24 Israeli airstrikes and shelling reported in southern Lebanon.
  25 Three Palestinians killed by Israeli tank fire in Gaza.
  Africa & South America
  27 UN Security Council extended the Abyei (UNISFA) peacekeeping
     mandate to Nov 15, 2027.
  28 Ethiopian forces took Mekelle as the Tigray conflict resumed.
  29 More than 7,400 migrants reached Spain's Canary Islands in
     the first 10 days of November.
  30 Pope Leo met abuse survivors in Peru before record crowds.

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
OCEAN = (186, 218, 236)
LAND = (206, 224, 178)
LANDLINE = (120, 150, 100)
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
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
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

    def polyline(self, pts, c, t=1):
        for i in range(len(pts)):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % len(pts)]
            self.line(x0, y0, x1, y1, c, t)

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


# ---------------------------------------------------------------- map data
# (number, region, headline, longitude, latitude). Pin spots are nudged
# a few degrees where stories cluster, so no two pins sit on each other.
STORIES = [
    (1, "NA", "FAA HALTS ALL FLIGHTS", -98, 39),
    (2, "NA", "NVIDIA CHIEF RESIGNS", -122, 37),
    (3, "NA", "STOCKS SLIP ON WALL ST", -68, 44),
    (4, "NA", "TRUMP: VANCE, FOCUS HOME", -80, 35),
    (5, "NA", "DOJ SEIZES $1.2B CRYPTO", -84, 42),
    (6, "NA", "BROOKLYN COLLAPSE, 8", -74, 38),
    (7, "NA", "STORMS FLOOD WASHINGTON", -125, 46),
    (8, "NA", "MICROSOFT OUTAGE, DAY 2", -118, 48),
    (9, "NA", "KNOWLES FIRE REPORT", -105, 39),
    (10, "NA", "MEASLES RULING AWAITED", -100, 24),
    (11, "EU", "UKRAINE TALKS ADVANCE", -6, 53),
    (12, "EU", "EUROPE JOINS PEACE TALKS", 5, 53),
    (13, "EU", "UKRAINE'S 1,200 DRONES", 30, 50),
    (14, "EU", "MOSCOW CAR BOMB", 37, 56),
    (15, "EU", "IAEA WARNS ON IRAN PLANT", 16, 48),
    (16, "EU", "COP31: UN URGES CUTS", 33, 36),
    (17, "EU", "KILLER-ROBOT TREATY", 9, 44),
    (18, "ME", "QATAR-TURKEY PACT", 27, 42),
    (19, "AS", "CHINA DRILLS NEAR TAIWAN", 122, 24),
    (20, "ME", "HOUTHI HIT SAUDI LINE", 38, 24),
    (21, "ME", "IRAN DRONES DOWNED", 52, 27),
    (22, "ME", "TANKERS HIT IN HORMUZ", 58, 27),
    (23, "ME", "GCC: END HOUTHI ATTACKS", 45, 24),
    (24, "ME", "ISRAEL HITS S. LEBANON", 36, 34),
    (25, "ME", "3 KILLED IN GAZA FIRE", 32, 29),
    (26, "EU", "IEA: Q4 OIL SURPLUS", -1, 48),
    (27, "AF", "ABYEI MANDATE EXTENDED", 28, 9),
    (28, "AF", "MEKELLE FALLS", 39, 13),
    (29, "AF", "CANARY ROUTE: 7,400", -16, 28),
    (30, "SA", "POPE LEO MEETS SURVIVORS", -77, -12),
]

# Rough continent outlines in (lon, lat); stylised, equirectangular.
CONTINENTS = [
    [(-168, 66), (-155, 71), (-140, 70), (-130, 71), (-120, 72), (-110, 73),
     (-100, 73), (-95, 80), (-85, 76), (-82, 73), (-76, 71), (-70, 68),
     (-65, 60), (-60, 55), (-55, 47), (-60, 45), (-65, 44), (-70, 42),
     (-75, 36), (-76, 34), (-80, 32), (-81, 26), (-84, 30), (-87, 30),
     (-90, 29), (-91, 19), (-94, 17), (-97, 16), (-100, 20), (-105, 20),
     (-110, 23), (-114, 28), (-117, 33), (-122, 37), (-124, 42), (-124, 48),
     (-130, 55), (-140, 60), (-150, 61), (-158, 58), (-162, 60)],
    [(-58, 64), (-52, 60), (-45, 60), (-40, 64), (-32, 68), (-30, 70),
     (-35, 74), (-45, 76), (-55, 76), (-58, 72)],  # Greenland
    [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-70, -38), (-68, -45), (-68, -52), (-70, -54),
     (-73, -50), (-73, -42), (-72, -35), (-72, -25), (-70, -18), (-70, -15),
     (-75, -10), (-79, -6), (-80, 2)],
    [(-17, 15), (-16, 21), (-15, 27), (-10, 31), (-6, 34), (-1, 35),
     (5, 37), (10, 37), (15, 32), (20, 32), (25, 32), (30, 31), (32, 31),
     (35, 28), (37, 22), (39, 18), (43, 12), (48, 11), (51, 11), (51, 10),
     (48, 5), (44, 0), (40, -5), (40, -12), (38, -18), (35, -24),
     (32, -28), (28, -33), (20, -35), (17, -32), (15, -27), (13, -20),
     (12, -15), (13, -10), (9, -1), (9, 4), (4, 6), (-2, 5), (-8, 4),
     (-13, 8), (-17, 12)],  # Africa
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 52), (7, 54), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (28, 66),
     (22, 70), (15, 70), (10, 68), (6, 62), (4, 58), (0, 52), (-5, 50),
     (-8, 46), (-10, 42)],  # Europe
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-2, 50)],  # Britain
    [(30, 62), (35, 66), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
     (90, 75), (100, 76), (110, 74), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 70), (170, 67), (178, 65), (170, 62), (162, 60),
     (158, 53), (156, 51), (150, 59), (142, 55), (141, 50), (140, 45),
     (138, 38), (135, 34), (132, 33), (130, 31), (127, 35), (126, 38),
     (124, 40), (122, 38), (120, 32), (121, 28), (118, 25), (112, 22),
     (108, 18), (105, 10), (103, 8), (100, 6), (98, 10), (97, 16),
     (94, 18), (91, 22), (88, 22), (86, 20), (82, 17), (80, 14), (77, 8),
     (76, 10), (74, 14), (72, 20), (70, 21), (66, 25), (62, 25), (58, 26),
     (54, 27), (52, 28), (50, 29), (48, 30), (44, 29), (42, 31), (39, 31),
     (36, 36), (33, 36), (30, 36), (30, 40), (30, 45), (30, 50), (30, 55)],
    [(95, 5), (98, 3), (100, 0), (103, -2), (106, -5), (110, -7),
     (114, -8), (116, -9), (119, -9), (122, -10), (120, -8), (116, -5),
     (112, -4), (108, -2), (104, 1), (100, 4), (96, 5)],  # Indonesia
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
     (141, 38), (141, 41), (143, 42), (145, 44), (143, 44), (141, 42),
     (140, 38), (138, 35), (135, 34), (132, 32)],  # Japan
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (147, -39),
     (150, -37), (150, -34), (153, -32), (153, -27), (150, -22), (147, -19),
     (146, -19), (142, -15), (142, -11), (140, -13), (137, -12), (136, -15),
     (135, -15), (132, -12), (130, -13), (128, -14), (126, -14), (124, -16),
     (122, -17), (120, -19), (117, -20), (114, -22)],  # Australia
    [(167, -45), (168, -44), (170, -42), (172, -41), (174, -39), (176, -38),
     (178, -37), (176, -38), (174, -40), (172, -42), (169, -44), (167, -46)],
    [(44, -16), (47, -15), (50, -16), (50, -20), (48, -24), (45, -25),
     (43, -22), (43, -18)],  # Madagascar
]

MAP_LABELS = [
    (-100, 56, "NORTH AMERICA"),
    (-60, -22, "SOUTH AMERICA"),
    (12, 63, "EUROPE"),
    (20, -2, "AFRICA"),
    (95, 56, "ASIA"),
    (134, -26, "AUSTRALIA"),
    (-30, 18, "ATLANTIC"),
    (-155, -2, "PACIFIC"),
]


def draw_map(cv, mx, my, mw, mh):
    """World map with every story pinned. mx,my,mw,mh = map area box."""
    cv.fill_rect(mx, my, mw, mh, OCEAN)

    def ll(lon, lat):
        return (mx + int((lon + 180) / 360 * mw),
                my + int((90 - lat) / 150 * mh))

    # Graticule every 30 degrees.
    for lon in range(-150, 181, 30):
        x = mx + int((lon + 180) / 360 * mw)
        cv.line(x, my, x, my + mh, (205, 228, 240))
    for lat in range(-60, 91, 30):
        y = my + int((90 - lat) / 150 * mh)
        cv.line(mx, y, mx + mw, y, (205, 228, 240))
    # Equator, slightly stronger.
    ey = my + int(90 / 150 * mh)
    cv.line(mx, ey, mx + mw, ey, (170, 205, 225))

    for poly in CONTINENTS:
        pts = [ll(lon, lat) for lon, lat in poly]
        cv.polygon(pts, LAND)
        cv.polyline(pts, LANDLINE)

    for lon, lat, name in MAP_LABELS:
        x, y = ll(lon, lat)
        cv.text_center(x, y, name, 1, (90, 110, 95))

    # Numbered pins, one per story.
    for num, _reg, _head, lon, lat in STORIES:
        x, y = ll(lon, lat)
        cv.circle(x, y, 8, RED)
        cv.circle(x, y, 8, WHITE, fill=False)
        label = str(num)
        cv.text(x - cv.text_w(label, 1) // 2, y - 3, label, 1, WHITE)


def draw_page():
    cv = Canvas(W, H, PAPER)
    cv.rect(8, 8, W - 16, H - 16, INK, 4)

    # Masthead.
    cv.text_center(W // 2, 26, "THE WORLD IN ONE PICTURE", 5, INK)
    cv.text_center(W // 2, 72, "FRIDAY, 13 NOVEMBER 2026 - 30 STORIES, 6 REGIONS", 3, RED)
    cv.fill_rect(24, 104, W - 48, 3, INK)
    cv.fill_rect(24, 110, W - 48, 2, RED)

    # Lead story: FAA ground stop (dominant, full width).
    x, y, w, h = 24, 122, W - 48, 168
    cv.fill_rect(x, y, w, h, WHITE)
    cv.rect(x, y, w, h, INK, 3)
    cv.fill_rect(x + 3, y + 3, w - 6, 88, SKY)  # sky
    cv.circle(x + 860, y + 42, 22, (255, 236, 160))  # sun
    cv.circle(x + 180, y + 52, 24, WHITE)  # clouds
    cv.circle(x + 230, y + 46, 28, WHITE)
    cv.circle(x + 620, y + 40, 20, WHITE)
    cv.circle(x + 655, y + 46, 24, WHITE)
    cv.fill_rect(x + 3, y + 91, w - 6, 14, DARKGREY)  # tarmac
    draw_plane(cv, x + 220, y + 62, 1, BLUE, RED)
    draw_plane(cv, x + 500, y + 68, 1, (90, 90, 90), RED)
    draw_plane(cv, x + 780, y + 62, 1, BLUE, RED)
    cv.fill_rect(x + 3, y + 105, w - 6, 4, RED)  # stop line
    cv.text_center(W // 2, y + 116, "U.S. FLIGHTS GROUNDED NATIONWIDE", 4, INK)
    cv.wrapped(x + 28, y + 146, w - 56,
               "FAA halts all departures 4 hours after a telecom "
               "failure; 1,000+ cancelled.",
               2, INK)

    # World map panel: the map carries the same visual weight as the lead.
    mx, my, mw, mh = 24, 300, W - 48, 260
    cv.fill_rect(mx, my, mw, mh, WHITE)
    cv.rect(mx, my, mw, mh, INK, 3)
    cv.fill_rect(mx + 3, my + 3, mw - 6, 28, RED)
    cv.text_center(W // 2, my + 10, "PINNED ON THE MAP: 30 STORIES, 6 REGIONS", 2, WHITE)
    draw_map(cv, mx + 3, my + 34, mw - 6, mh - 37)

    # Numbered index: three columns of micro-headlines.
    # Column 3 splits into three region subsections so all six
    # regions read clearly: Middle East & Asia, Africa, S. America.
    iy = 574

    def index_item(cx, cw, yy, num, head):
        cv.fill_rect(cx, yy, 16, 16, RED)
        cv.text(cx + 3, yy + 4, str(num), 1, WHITE)
        return cv.wrapped(cx + 22, yy, cw - 22, head, 2, INK) + 2

    def index_header(cx, cw, yy, title):
        cv.text(cx, yy, title, 2, RED)
        cv.fill_rect(cx, yy + 18, cw, 2, RED)
        return yy + 28

    # Column 1: North America (stories 1-10).
    yy = index_header(24, 310, iy, "NORTH AMERICA (10)")
    for num, _reg, head, _lon, _lat in STORIES:
        if _reg == "NA":
            yy = index_item(24, 310, yy, num, head)

    # Column 2: Europe (stories 11-17, 26).
    yy = index_header(357, 310, iy, "EUROPE (8)")
    for num, _reg, head, _lon, _lat in STORIES:
        if _reg == "EU":
            yy = index_item(357, 310, yy, num, head)

    # Column 3: Middle East & Asia, then Africa, then S. America.
    yy = index_header(690, 310, iy, "MIDDLE EAST & ASIA (8)")
    for num, _reg, head, _lon, _lat in STORIES:
        if _reg in ("ME", "AS"):
            yy = index_item(690, 310, yy, num, head)
    yy = index_header(690, 310, yy + 2, "AFRICA (3)")
    for num, _reg, head, _lon, _lat in STORIES:
        if _reg == "AF":
            yy = index_item(690, 310, yy, num, head)
    yy = index_header(690, 310, yy + 2, "SOUTH AMERICA (1)")
    for num, _reg, head, _lon, _lat in STORIES:
        if _reg == "SA":
            yy = index_item(690, 310, yy, num, head)

    # Footer strip.
    cv.fill_rect(24, 966, W - 48, 3, INK)
    cv.text_center(W // 2, 976,
                   "SOURCES: AP, REUTERS, AFP - ALL EVENTS REPORTED "
                   "13 NOVEMBER 2026", 2, INK)
    return cv


def main():
    out = Path(OUT)
    out.mkdir(parents=True, exist_ok=True)
    data = png_bytes(draw_page())
    (out / "entry.png").write_bytes(data)
    print("wrote %d bytes" % len(data))


if __name__ == "__main__":
    main()
