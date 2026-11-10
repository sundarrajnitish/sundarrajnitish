"""One animated card per lab. Each animation is a small, honest sketch of what the lab lets you do.

Cards show at about 0.65x on GitHub (two to a row), so text inside a card is 15px or more, and
each card carries one accent colour: the discipline it belongs to.
"""

import math
import random

from svgkit import (AI, BG, BG_ALT, BORDER, BORDER_SOFT, CONTROL, DIM, EMBEDDED, MONO, MUTED, PANEL, ROBOTICS,
                    SILICON, SOFTWARE, TEXT, WHITE, doc, f, mono_text, text)

W, H = 600, 380
BX, BY, BW, BH = 28, 120, 544, 192  # animation box
STEEL = "#D4D4D4"  # the solid parts of machines
BASE = "https://sundarrajnitish.github.io"


def kf(name, stops, dur, extra=""):
    """Keyframes block + class that runs it forever."""
    body = "".join(f"{f(p)}%{{{v}}}" for p, v in stops)
    return f"@keyframes {name}{{{body}}}.{name}{{animation:{name} {f(dur)}s linear infinite{extra}}}"


def card(slug, accent, title, hook, stat, anim_css, anim_svg, desc):
    body = f"""
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="#000" stroke="{BORDER}"/>
{text(28, 62, title, 34, TEXT, 600, extra='letter-spacing="-0.6"')}
{text(28, 96, hook, 20, MUTED)}
<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="12" fill="{BG_ALT}" stroke="{BORDER_SOFT}"/>
<clipPath id="box"><rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="12"/></clipPath>
<g clip-path="url(#box)">{anim_svg}</g>
<circle cx="34" cy="{H - 36}" r="5" fill="{accent}"/>
{mono_text(50, H - 30, stat, 17, MUTED, fit=False)}
<path d="M{W - 46} {H - 24}l14 -14m-10 0h10v10" fill="none" stroke="{accent}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
"""
    return slug, doc(W, H, f"{title}: {hook}", "\n".join(anim_css), body, desc)


def flip(n, i, cycle, first_visible=False):
    """Opacity stops that show item i of n for its slot of the cycle."""
    a, b = i / n * 100, (i + 1) / n * 100
    if first_visible and i == 0:
        return [(0, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")]
    return [(0, "opacity:0"), (a, "opacity:0"), (a + 0.01, "opacity:1"), (b, "opacity:1"), (min(b + 0.01, 100), "opacity:0"),
            (100, "opacity:0")]


# ---------------------------------------------------------------------------------------------

def farme():
    x0, x1, r = BX + 46, BX + BW - 46, 21
    ys = [BY + 33 + i * 2 * r for i in range(4)]
    d = f"M{x0} {ys[0]}"
    for i in range(3):
        if i % 2 == 0:
            d += f"H{x1}A{r} {r} 0 0 1 {x1} {ys[i + 1]}"
        else:
            d += f"H{x0}A{r} {r} 0 0 0 {x0} {ys[i + 1]}"
    d += f"H{x1}"
    straight, arc = x1 - x0, math.pi * r
    total = 4 * straight + 3 * arc
    dur, gap = 13.0, 34
    css = [
        f"@keyframes seed{{0%{{opacity:0;transform:scale(.4)}}1%{{opacity:1;fill:{DIM};transform:scale(1)}}"
        f"14%{{fill:{DIM};transform:scale(1)}}22%,95%{{opacity:1;fill:{EMBEDDED};transform:scale(1.7)}}100%{{opacity:0}}}}",
        f".seed{{opacity:0;transform-box:fill-box;transform-origin:center;animation:seed {dur}s linear infinite}}",
    ]
    soil = "".join(
        f'<line x1="{BX + 14}" y1="{y}" x2="{BX + BW - 14}" y2="{y}" stroke="#1A1A1A" stroke-width="26" stroke-linecap="round"/>'
        for y in ys)
    seeds = []
    for i, y in enumerate(ys):
        for k in range(1, int(straight // gap)):
            s = k * gap
            pos = i * (straight + arc) + s
            x = x0 + s if i % 2 == 0 else x1 - s
            seeds.append(f'<circle class="seed" cx="{f(x)}" cy="{y}" r="2.8" style="animation-delay:{f(pos / total * dur)}s"/>')
    robot = f"""
<g><animateMotion dur="{dur}s" repeatCount="indefinite" rotate="auto" path="{d}"/>
  <path d="M14 -7 L54 -26 L54 26 L14 7Z" fill="{ROBOTICS}" opacity=".12"/>
  <rect x="-16" y="-14" width="32" height="6" rx="2" fill="#4A4A4A"/><rect x="-16" y="8" width="32" height="6" rx="2" fill="#4A4A4A"/>
  <rect x="-13" y="-10" width="26" height="20" rx="3" fill="{STEEL}"/>
  <rect x="-7" y="-6" width="11" height="12" rx="2" fill="{BG}"/>
  <circle cx="12" cy="0" r="2.8" fill="{ROBOTICS}"/>
</g>"""
    svg = soil + f'<path d="{d}" fill="none" stroke="{WHITE}" stroke-opacity=".16" stroke-dasharray="3 6"/>' + "".join(seeds) + robot
    return card("farm-e", ROBOTICS, "FARM-E", "A tracked robot that plants, seeds and waters.",
                "UNO + ESP8266 firmware, co-simulated", css, svg,
                "A small tracked robot drives a serpentine path over soil rows, dropping seeds that sprout behind it.")


def hydro():
    random.seed(7)
    x0, x1, yt, yb = BX + 90, BX + BW - 20, BY + 26, BY + BH - 44
    lo, hi = 5.0, 8.2

    def Y(ph):
        return yb - (ph - lo) / (hi - lo) * (yb - yt)

    pts, doses, ph = [], [], 7.9
    n = 220
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        if i < 40:  # tap water: dose and wait, step by step
            if i % 6 == 3 and ph > 6.3:
                ph -= 0.27
                doses.append(x)
            else:
                ph += 0.004
        else:
            ph += 0.0075 + random.uniform(-0.003, 0.003)
            if ph > 6.3:
                ph = 6.02
                doses.append(x)
        pts.append((x, Y(ph)))
    d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)
    L = sum(math.dist(pts[i], pts[i + 1]) for i in range(n))
    draw, cycle = 6.5, 10.0
    css = [
        kf("trace", [(0, f"stroke-dashoffset:{f(L)};opacity:1"), (draw / cycle * 100, "stroke-dashoffset:0;opacity:1"),
                     (92, "stroke-dashoffset:0;opacity:1"), (100, "stroke-dashoffset:0;opacity:0")], cycle),
    ]
    drops = []
    for i, x in enumerate(doses):
        frac = (x - x0) / (x1 - x0) * draw / cycle * 100
        css.append(kf(f"dp{i}", [(0, "opacity:0"), (frac, "opacity:0"), (frac + 0.5, "opacity:1"), (92, "opacity:1"),
                                 (100, "opacity:0")], cycle))
        drops.append(f'<path class="dp{i}" opacity="0" d="M{f(x)} {f(yt - 12)}q-4.5 7 0 10q4.5 -3 0 -10z" fill="{AI}"/>')
    svg = f"""
<rect x="{x0}" y="{f(Y(6.5))}" width="{x1 - x0}" height="{f(Y(5.5) - Y(6.5))}" fill="{EMBEDDED}" opacity=".10"/>
<line x1="{x0}" y1="{f(Y(6.5))}" x2="{x1}" y2="{f(Y(6.5))}" stroke="{EMBEDDED}" stroke-opacity=".5" stroke-dasharray="4 4"/>
<line x1="{x0}" y1="{f(Y(5.5))}" x2="{x1}" y2="{f(Y(5.5))}" stroke="{EMBEDDED}" stroke-opacity=".5" stroke-dasharray="4 4"/>
{mono_text(x0 - 12, Y(6.5) + 6, "6.5", 16, EMBEDDED, fit=False, anchor="end")}
{mono_text(x0 - 12, Y(5.5) + 6, "5.5", 16, EMBEDDED, fit=False, anchor="end")}
{mono_text(x0 - 12, Y(7.9) + 6, "pH 7.9", 16, MUTED, fit=False, anchor="end")}
{mono_text(x0, yb + 30, "day 0", 16, MUTED, fit=False)}
{mono_text(x1, yb + 30, "day 14", 16, MUTED, fit=False, anchor="end")}
<path d="{d}" fill="none" stroke="{CONTROL}" stroke-width="2.6" stroke-linejoin="round" stroke-dasharray="{f(L)}" class="trace"/>
{''.join(drops)}"""
    return card("hydroponinator", CONTROL, "Hydroponinator", "A grow-rack controller that holds pH in band.",
                "pH in band 100% of a 14-day grow", css, svg,
                "Reservoir pH starts at 7.9 from tap water, is dosed down into the 5.5 to 6.5 band, and "
                "stays there for two weeks with small automatic corrections.")


GESTURES = [  # (name, extended thumb..little)
    ("Hand_Open", (1, 1, 1, 1, 1)),
    ("Index", (0, 1, 0, 0, 0)),
    ("Index_Middle", (0, 1, 1, 0, 0)),
    ("Thumb_Index_Little", (1, 1, 0, 0, 1)),
    ("Hand_Closed", (0, 0, 0, 0, 0)),
    ("Thumb", (1, 0, 0, 0, 0)),
    ("Index_Middle_Ring_Little", (0, 1, 1, 1, 1)),
]
CLOSED_DEG = (160, 150, 180, 150, 150)


def rtmc():
    slot = 1.6
    cycle = slot * len(GESTURES)
    oy = BY + 14
    fingers = [  # x, base y, length, width, tilt
        (BX + 70, oy + 112, 46, 16, -38),
        (BX + 104, oy + 84, 64, 15, -6),
        (BX + 126, oy + 82, 70, 15, 0),
        (BX + 148, oy + 84, 64, 15, 5),
        (BX + 168, oy + 90, 50, 14, 12),
    ]
    css, fsvg = [], []
    for j, (x, y, ln, w, tilt) in enumerate(fingers):
        stops = []
        for g, (_, ext) in enumerate(GESTURES):
            t0 = g / len(GESTURES) * 100
            sc = 1 if ext[j] else 0.32
            stops += [(t0, f"transform:scaleY({sc})"), (t0 + 100 / len(GESTURES) * 0.75, f"transform:scaleY({sc})")]
        stops.append((100, f"transform:scaleY({1 if GESTURES[0][1][j] else 0.32})"))
        css.append(kf(f"fg{j}", stops, cycle, ";transform-box:fill-box;transform-origin:bottom"))
        fsvg.append(f'<g transform="rotate({tilt} {x} {y})"><rect class="fg{j}" x="{f(x - w / 2)}" y="{y - ln}" '
                    f'width="{w}" height="{ln}" rx="{w / 2}" fill="{STEEL}"/></g>')
    labels = []
    for g, (name, ext) in enumerate(GESTURES):
        css.append(kf(f"gl{g}", flip(len(GESTURES), g, cycle, True), cycle))
        servos = ", ".join(str(0 if e else CLOSED_DEG[k]) for k, e in enumerate(ext))
        # the longest gesture name drops to a size that still fits the panel
        size = 24 if len(name) <= 18 else 19
        labels.append(f'<g class="gl{g}" opacity="{1 if g == 0 else 0}">'
                      + mono_text(BX + 256, BY + 84, name, size, TEXT, fit=False)
                      + mono_text(BX + 256, BY + 124, f"servos {servos}", 17, ROBOTICS, fit=False)
                      + "</g>")
    svg = f"""
<rect x="{BX + 232}" y="{BY + 34}" width="2" height="{BH - 68}" fill="{BORDER}"/>
{''.join(labels)}
{''.join(fsvg)}
<rect x="{BX + 58}" y="{oy + 84}" width="124" height="66" rx="22" fill="{STEEL}"/>
<rect x="{BX + 98}" y="{oy + 140}" width="48" height="40" fill="{STEEL}"/>"""
    return card("rtmc-hg", ROBOTICS, "RTMC-HG", "Steer a tendon-driven robot hand with gestures.",
                "20 gestures · 83 tests · CRC-8 frames", css, svg,
                "A robot hand cycles through gestures while the classified gesture and the servo angles sent to it are shown.")


def crc8_j1850(data):
    crc = 0xFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1D) & 0xFF if crc & 0x80 else (crc << 1) & 0xFF
    return crc ^ 0xFF


def f1can():
    # stylised Circuit Gilles Villeneuve: long straights, a hairpin, chicanes
    tx, ty = BX + 20, BY + 32
    track = (f"M{tx + 20} {ty + 92}C{tx + 4} {ty + 92} {tx} {ty + 70} {tx + 14} {ty + 58}L{tx + 60} {ty + 30}"
             f"C{tx + 70} {ty + 24} {tx + 82} {ty + 30} {tx + 92} {ty + 24}L{tx + 150} {ty + 6}"
             f"C{tx + 172} {ty} {tx + 186} {ty + 18} {tx + 170} {ty + 30}C{tx + 160} {ty + 38} {tx + 150} {ty + 46} {tx + 152} {ty + 60}"
             f"L{tx + 168} {ty + 104}C{tx + 172} {ty + 118} {tx + 160} {ty + 126} {tx + 146} {ty + 120}L{tx + 112} {ty + 108}"
             f"C{tx + 100} {ty + 104} {tx + 90} {ty + 112} {tx + 78} {ty + 106}Z")
    lap = 7.0
    samples = [(301.2, 11600, 100, 8, 0, 1), (322.4, 11850, 100, 8, 0, 1), (118.6, 8900, 0, 3, 1, 0),
               (64.3, 7600, 22, 2, 0, 0), (187.9, 10800, 100, 5, 0, 0), (254.0, 11400, 100, 7, 0, 0),
               (139.5, 9600, 0, 4, 1, 0), (233.8, 11200, 86, 6, 0, 0)]
    css, frames = [], []
    rx = BX + 226
    for i, (spd, rpm, thr, gear, brk, drs) in enumerate(samples):
        v = round(spd * 10)
        data = [v & 0xFF, v >> 8, rpm & 0xFF, rpm >> 8, thr, gear | (brk << 4) | (drs << 5), i & 0x0F]
        data.append(crc8_j1850(data))
        css.append(kf(f"fr{i}", flip(len(samples), i, lap, True), lap))
        boxes = []
        for k, byte in enumerate(data):
            x = rx + k * 38
            crc = k == 7  # the checksum byte is the one inverted box
            boxes.append(f'<rect x="{x}" y="{BY + 58}" width="34" height="36" rx="6" fill="{EMBEDDED if crc else PANEL}" stroke="{EMBEDDED if crc else BORDER}"/>'
                         + mono_text(x + 17, BY + 82, f"{byte:02X}", 17, BG if crc else (MUTED if k == 6 else TEXT), fit=False,
                                     anchor="middle", extra='font-weight="700"' if crc else ""))
        flag = "DRS" if drs else ("BRAKE" if brk else "")
        frames.append(f'<g class="fr{i}" opacity="{1 if i == 0 else 0}">{"".join(boxes)}'
                      + mono_text(rx, BY + 130, f"{spd:5.1f} km/h  gear {gear}", 18, TEXT, fit=False)
                      + f'<text x="{rx}" y="{BY + 162}" font-family="{MONO}" font-size="17" xml:space="preserve">'
                        f'<tspan fill="{MUTED}">{rpm:,} rpm  </tspan><tspan fill="{EMBEDDED}" font-weight="700">{flag}</tspan></text>'
                      + "</g>")
    svg = f"""
<path d="{track}" fill="none" stroke="#262626" stroke-width="10" stroke-linejoin="round"/>
<path d="{track}" fill="none" stroke="{BORDER}" stroke-width="1" stroke-dasharray="2 6"/>
<g><animateMotion dur="{lap}s" repeatCount="indefinite" path="{track}" begin="-0.45s"/><circle r="4.5" fill="{DIM}"/></g>
<g><animateMotion dur="{lap}s" repeatCount="indefinite" path="{track}"/><circle r="11" fill="{EMBEDDED}" opacity=".2"/><circle r="5.5" fill="{EMBEDDED}"/></g>
{mono_text(rx, BY + 40, "0x101 CarTelemetry", 17, TEXT, fit=False)}
{''.join(frames)}"""
    return card("f1-can", EMBEDDED, "F1 CAN Telemetry", "The 2023 Canadian GP, streamed over a CAN bus.",
                "CRC-8 on every frame · real lap data", css, svg,
                "A car laps a sketch of the Montreal circuit while its telemetry is packed into 8-byte CAN frames with a CRC.")


def mcl():
    random.seed(3)
    oy = BY + 6
    cy, x_start, x_end = oy + 92, BX + 120, BX + 420
    cycle = 9.0
    walls = (f"M{BX + 10} {oy + 52}H{BX + 150}v-14h40v14H{BX + 330}v-14h50v14H{BX + BW - 10}"
             f"M{BX + 10} {oy + 132}H{BX + 230}v14h44v-14H{BX + 450}v14h40v-14H{BX + BW - 10}")
    css = [kf("ride", [(0, "transform:translateX(0)"), (46, "transform:translateX(0)"),
                       (94, f"transform:translateX({x_end - x_start}px)"), (100, f"transform:translateX({x_end - x_start}px)")], cycle),
           kf("beam", [(0, "opacity:0"), (44, "opacity:0"), (48, "opacity:.45"), (94, "opacity:.45"), (100, "opacity:0")], cycle)]
    parts = []
    for i in range(70):
        ox, oy2 = random.gauss(0, 7), random.gauss(0, 4)
        sx, sy = random.uniform(BX + 16, BX + BW - 16), random.uniform(oy + 58, oy + 126)
        dx, dy = sx - (x_start + ox), sy - (cy + oy2)
        # a few particles lock onto the look-alike stretch first, then die off
        mid = (f"transform:translate({f(dx * 0.45 + 140)}px,{f(dy * 0.3)}px)" if i % 5 == 0 else
               f"transform:translate({f(dx * 0.25)}px,{f(dy * 0.25)}px)")
        css.append(kf(f"p{i}", [(0, f"transform:translate({f(dx)}px,{f(dy)}px)"), (8, f"transform:translate({f(dx)}px,{f(dy)}px)"),
                                (26, mid), (42, "transform:translate(0,0)"), (100, "transform:translate(0,0)")], cycle))
        parts.append(f'<circle class="p{i}" cx="{f(x_start + ox)}" cy="{f(cy + oy2)}" r="2.6" fill="{AI}" opacity=".85"/>')
    beams = "".join(
        f'<line x1="{x_start}" y1="{cy}" x2="{f(x_start + math.cos(a) * 200)}" y2="{f(cy + math.sin(a) * 200)}" stroke="{WHITE}" stroke-width=".7"/>'
        for a in [math.radians(d) for d in range(-150, 181, 30)])
    svg = f"""
<path d="{walls}" fill="none" stroke="{MUTED}" stroke-width="2.5"/>
<g class="ride"><g class="beam" opacity="0" clip-path="url(#hall)">{beams}</g>
{''.join(parts)}
<circle cx="{x_start}" cy="{cy}" r="8" fill="{BG}" stroke="{TEXT}" stroke-width="2"/><path d="M{x_start} {cy}h11" stroke="{TEXT}" stroke-width="2"/></g>
<clipPath id="hall"><rect x="{BX - 400}" y="{oy + 53}" width="{BW + 800}" height="78"/></clipPath>
{mono_text(BX + 16, BY + BH - 16, "scattered → converged → tracking", 16, AI, fit=False)}"""
    return card("monte-carlo-localization", AI, "Monte Carlo Localization", "A particle filter that finds a lost robot.",
                "4 cm median error on a real laser log", css, svg,
                "Particles scattered over a hallway converge onto the robot's true position, then follow it as it drives.")


def mips():
    cols, rows = 9, [
        ("lw  $t1,0($a0)", ["IF", "ID", "EX", "MEM", "WB"], 0),
        ("add $t2,$t1,$t0", ["IF", "ID", "--", "EX", "MEM", "WB"], 1),
        ("sub $t3,$t2,$t0", ["IF", "IF", "ID", "EX", "MEM", "WB"], 2),
        ("sw  $t3,4($a0)", ["IF", "ID", "EX", "MEM", "WB"], 4),
    ]
    # the pipeline as a grey ramp, with the accent where the work happens
    colors = {"IF": "#2E2E2E", "ID": "#4D4D4D", "EX": SILICON, "MEM": "#B4B4B4", "WB": "#7A7A7A", "--": None}
    gx, gy, cw, rh = BX + 178, BY + 36, 40, 29
    cycle, per = 9.0, 0.75
    css = [kf("cur", [(0, "transform:translateX(0)")] + [(((c + 1) * per) / cycle * 100, f"transform:translateX({(c + 1) * cw}px)") for c in range(cols)]
              + [(97, f"transform:translateX({cols * cw}px)"), (100, "transform:translateX(0)")], cycle,
              ";animation-timing-function:steps(1,end)")]
    cells = [mono_text(gx + c * cw + cw / 2, gy - 10, str(c + 1), 15, DIM, fit=False, anchor="middle") for c in range(cols)]
    for r, (ins, stages, start) in enumerate(rows):
        y = gy + r * rh
        cells.append(mono_text(BX + 14, y + 21, ins, 16, TEXT if r == 1 else MUTED, fit=False))
        for k, st in enumerate(stages):
            c = start + k
            t = (c * per + 0.05) / cycle * 100
            name = f"c{r}_{k}"
            css.append(kf(name, [(0, "opacity:0"), (t, "opacity:0"), (t + 0.5, "opacity:1"), (96, "opacity:1"), (100, "opacity:0")], cycle))
            fill = colors[st]
            paint = f'fill="{fill}"' if fill else f'fill="none" stroke="{MUTED}" stroke-dasharray="3 3"'
            label = "" if st == "--" else mono_text(gx + c * cw + cw / 2, y + 20.5, st, 13, BG if st in ("EX", "MEM") else TEXT,
                                                    fit=False, anchor="middle", extra='font-weight="600"')
            cells.append(f'<g class="{name}" opacity="0"><rect x="{gx + c * cw + 2}" y="{y + 2}" width="{cw - 4}" height="{rh - 4}" rx="4" {paint}/>'
                         + label + "</g>")
    # forwarding: lw MEM (cycle 4) -> add EX (cycle 5)
    t = (4 * per + 0.3) / cycle * 100
    css.append(kf("fwd", [(0, "opacity:0"), (t, "opacity:0"), (t + 1, "opacity:1"), (96, "opacity:1"), (100, "opacity:0")], cycle))
    ax, ay = gx + 3 * cw + cw / 2, gy + rh - 4
    bx, by = gx + 4 * cw + cw / 2, gy + rh + 5
    cells.append(f'<path class="fwd" opacity="0" d="M{ax} {ay}C{ax} {ay + 9} {bx - 10} {by - 6} {bx - 4} {by}" fill="none" stroke="{SILICON}" stroke-width="2.4"/>')
    svg = f"""
{''.join(cells)}
<g class="cur"><rect x="{gx}" y="{gy - 28}" width="{cw}" height="{len(rows) * rh + 30}" fill="{TEXT}" opacity=".06"/></g>
{mono_text(BX + 14, BY + BH - 14, "load-use: 1 stall, then forwarded", 16, MUTED, fit=False)}
{mono_text(BX + BW - 14, BY + BH - 14, "CPI 1.298", 16, SILICON, fit=False, anchor="end", extra='font-weight="700"')}"""
    return card("mini-mips", SILICON, "mini-MIPS", "A 5-stage pipelined MIPS in VHDL, cycle by cycle.",
                "1,000 random programs vs a golden ISS", css, svg,
                "Four instructions flow through a five-stage pipeline; a load-use hazard inserts one stall and forwarding resolves it.")


def dadda_stages():
    h0 = [min(c + 1, 15 - c) for c in range(15)] + [0]
    stages, H = [h0[:]], h0[:]
    for d in (6, 4, 3, 2):
        new, carry = [0] * 16, 0
        for c in range(16):
            h, out = H[c] + carry, 0
            while h > d:
                if h - d >= 2:
                    h -= 2
                else:
                    h -= 1
                out += 1
            new[c], carry = h, out
        H = new
        stages.append(H[:])
    stages.append([1] * 16)
    return stages


def arith():
    stages = dadda_stages()
    labels = ["partial products, 8×8", "Dadda d=6", "Dadda d=4", "Dadda d=3", "Dadda d=2", "carry-propagate → product"]
    slot = 1.25
    cycle = slot * len(stages) + 1.5
    dx, dy = 21, 16
    x_right, y_base = BX + 506, BY + 172
    starts = [s * slot / cycle * 100 for s in range(len(stages))]

    def steps_for(vis):
        stops = [(0, f"opacity:{int(vis[0])}")]
        for s in range(1, len(vis)):
            stops += [(starts[s], f"opacity:{int(vis[s - 1])}"), (starts[s] + 2.5, f"opacity:{int(vis[s])}")]
        stops += [(97, f"opacity:{int(vis[-1])}"), (100, f"opacity:{int(vis[0])}")]
        return stops

    css, dots, pat = [], [], {}
    for c in range(16):
        for r in range(8):
            vis = tuple(r < st[c] for st in stages[:-1]) + (False,)
            if not any(vis):
                continue
            if vis not in pat:
                pat[vis] = f"v{len(pat)}"
                css.append(kf(pat[vis], steps_for(vis), cycle))
            dots.append(f'<circle class="{pat[vis]}" cx="{x_right - c * dx}" cy="{y_base - r * dy}" r="5" '
                        f'fill="#8C8C8C" opacity="{int(vis[0])}"/>')
    css.append(kf("pfinal", steps_for((False,) * (len(stages) - 1) + (True,)), cycle))
    dots += [f'<circle class="pfinal" cx="{x_right - c * dx}" cy="{y_base}" r="6" fill="{SILICON}" opacity="0"/>' for c in range(16)]
    lab = []
    for s, name in enumerate(labels):
        a, b = s * slot / cycle * 100, (s + 1) * slot / cycle * 100 if s < len(labels) - 1 else 100
        stops = [(0, "opacity:0"), (a, "opacity:0"), (a + 0.01, "opacity:1"), (b, "opacity:1"), (min(b + 0.01, 100), "opacity:0")]
        if s == 0:
            stops = [(0, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")]
        css.append(kf(f"lb{s}", stops, cycle))
        lab.append(f'<g class="lb{s}" opacity="{1 if s == 0 else 0}">'
                   f'{mono_text(BX + 16, BY + 36, name, 19, SILICON if s == len(labels) - 1 else TEXT, fit=False)}</g>')
    svg = f"""
{''.join(lab)}
{''.join(dots)}"""
    return card("arithmetic-unit", SILICON, "Arithmetic Unit", "Multipliers in structural VHDL, from full adders.",
                "83 regression runs · didn't compile in 2023", css, svg,
                "The 8 by 8 partial-product matrix of a multiplier shrinks through the Dadda reduction stages to a single product row.")


def dds():
    cx, cy, R = BX + 88, BY + 84, 54
    T = 2.4
    lam = 170
    x0 = cx + R + 30
    pts = []
    for i in range(0, 361):
        x = x0 - lam + (BW - (x0 - BX) + 2 * lam) * i / 360
        y = cy + R * math.sin(2 * math.pi * (x - x0) / lam)
        pts.append((x, y))
    wave = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)
    css = [
        f".spin{{transform-origin:{cx}px {cy}px;animation:spin {T}s linear infinite}}@keyframes spin{{to{{transform:rotate(-360deg)}}}}",
        f".scroll{{animation:scroll {T}s linear infinite}}@keyframes scroll{{to{{transform:translateX({lam}px)}}}}",
        f".proj{{transform-origin:0 {cy}px;animation:proj {T}s linear infinite}}",
    ]
    # projection line from the phasor tip to the wave start: one keyframe per 10 degrees
    stops = [(k / 36 * 100, f"transform:translateY({f(-R * math.sin(2 * math.pi * k / 36))}px)") for k in range(37)]
    css.append("@keyframes proj{" + "".join(f"{f(p)}%{{{v}}}" for p, v in stops) + "}")
    svg = f"""
<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{BORDER}" stroke-width="2"/>
<line x1="{cx - R - 8}" y1="{cy}" x2="{BX + BW}" y2="{cy}" stroke="{BORDER_SOFT}"/>
<g class="spin"><line x1="{cx}" y1="{cy}" x2="{cx + R}" y2="{cy}" stroke="{WHITE}" stroke-width="2.2"/><circle cx="{cx + R}" cy="{cy}" r="5" fill="{WHITE}"/></g>
<g class="proj"><line x1="{cx}" y1="{cy}" x2="{x0}" y2="{cy}" stroke="{WHITE}" stroke-opacity=".35" stroke-dasharray="3 4"/><circle cx="{x0}" cy="{cy}" r="4" fill="{TEXT}"/></g>
<clipPath id="wv"><rect x="{x0}" y="{BY}" width="{BW}" height="{BH}"/></clipPath>
<g clip-path="url(#wv)"><path class="scroll" d="{wave}" fill="none" stroke="{SILICON}" stroke-width="2.6"/></g>
{mono_text(BX + 16, BY + BH - 16, "32-bit phase accumulator → sine ROM", 16, MUTED, fit=False)}
<g><rect x="{BX + BW - 196}" y="{BY + 12}" width="182" height="34" rx="17" fill="{PANEL}" stroke="{SILICON}" stroke-opacity=".8"/>
{mono_text(BX + BW - 105, BY + 35, "RTL ≡ netlist ✓", 16, SILICON, fit=False, anchor="middle", extra='font-weight="600"')}</g>"""
    return card("dds-synthesizer", SILICON, "DDS Formal", "Prove a buggy netlist wrong, then fix it.",
                "14 bugs found and repaired in ~5 s", css, svg,
                "A rotating phasor traces a sine wave, the output of a direct digital synthesizer whose netlist is proven equivalent to its RTL.")


def calc():
    n, cycle = 14, 10.0
    css, tiles = [], []
    for i in range(n):
        col, row = i % 7, i // 7
        x, y = BX + 15 + col * 74, BY + 64 + row * 50
        t = (0.8 + i * 0.5) / cycle * 100
        css.append(kf(f"b{i}", [(0, f"fill:{PANEL};stroke:{BORDER}"), (t, f"fill:{PANEL};stroke:{BORDER}"),
                                (t + 1, f"fill:{SILICON};stroke:{SILICON}"), (t + 4, f"fill:#10261E;stroke:{SILICON}"),
                                (95, f"fill:#10261E;stroke:{SILICON}"), (100, f"fill:{PANEL};stroke:{BORDER}")], cycle))
        css.append(kf(f"k{i}", [(0, "opacity:0"), (t + 3.5, "opacity:0"), (t + 4, "opacity:1"), (95, "opacity:1"), (100, "opacity:0")], cycle))
        tiles.append(f'<rect class="b{i}" x="{x}" y="{y}" width="70" height="40" rx="7" stroke-width="1.5"/>'
                     + mono_text(x + 8, y + 26, f"c{1 if i < 7 else 3}·b{i % 7 + 1}", 15, TEXT, fit=False)
                     + f'<g class="k{i}" opacity="0">{mono_text(x + 64, y + 26, "✓", 15, SILICON, fit=False, anchor="end")}</g>')
    cnt = []
    for i in range(n + 1):
        a = (0.8 + (i - 1) * 0.5) / cycle * 100 + 4 if i else 0
        b = (0.8 + i * 0.5) / cycle * 100 + 4 if i < n else 95
        stops = [(0, "opacity:0"), (a, "opacity:0"), (a + 0.01, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")]
        if i == 0:
            stops = [(0, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (99.9, "opacity:0"), (100, "opacity:1")]
        css.append(kf(f"n{i}", stops, cycle))
        done = i == n
        count = (f'<text x="{BX + 16}" y="{BY + 42}" font-family="{MONO}" font-size="21" xml:space="preserve">'
                 f'<tspan fill="{MUTED}">bugs caught </tspan><tspan fill="{SILICON if done else TEXT}" font-weight="700">{i:2d}/14</tspan></text>')
        cnt.append(f'<g class="n{i}" opacity="{1 if i == 0 else 0}">{count}</g>')
    svg = f"""
{''.join(tiles)}
{''.join(cnt)}
{mono_text(BX + 16, BY + BH - 16, "0 false failures on the golden designs", 16, MUTED, fit=False)}"""
    return card("calc-verification", SILICON, "Calc Verification", "A self-checking testbench that finds planted bugs.",
                "14/14 caught · 2024 failures root-caused", css, svg,
                "Fourteen injected bugs in two calculator designs light up as the regression catches each one, then stay ticked.")


def auction():
    cycle = 10.0
    bids = [(0.6, "C$120", "maple_kid"), (2.0, "C$125", "you"), (3.4, "C$135", "otter88"), (5.0, "C$145", "you"),
            (6.6, "C$150", "otter88")]
    circ = 226  # 2 * pi * 36
    css = [kf("ring", [(0, "stroke-dashoffset:0"), (58, "stroke-dashoffset:186"), (60, "stroke-dashoffset:120"),
                       (82, f"stroke-dashoffset:{circ}"), (100, f"stroke-dashoffset:{circ}")], cycle)]
    els = []
    for i, (t, price, who) in enumerate(bids):
        a = t / cycle * 100
        b = bids[i + 1][0] / cycle * 100 if i + 1 < len(bids) else 98
        css.append(kf(f"bd{i}", [(0, "opacity:0"), (a, "opacity:0"), (a + 0.01, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")], cycle))
        els.append(f'<g class="bd{i}" opacity="0">'
                   + text(BX + 176, BY + 104, price, 46, TEXT, 700)
                   + mono_text(BX + 178, BY + 138, f"high bid · {who}", 17, SOFTWARE if who == "you" else MUTED, fit=False) + "</g>")
    css.append(kf("soft", [(0, "opacity:0"), (59, "opacity:0"), (60, "opacity:1"), (80, "opacity:1"), (81, "opacity:0"), (100, "opacity:0")], cycle))
    css.append(kf("sold", [(0, "opacity:0;transform:scale(1.6)"), (84, "opacity:0;transform:scale(1.6)"), (86, "opacity:1;transform:scale(1)"),
                           (98, "opacity:1;transform:scale(1)"), (100, "opacity:0")], cycle, ";transform-box:fill-box;transform-origin:center"))
    rx, ry = BX + BW - 92, BY + 76
    ix, iy = BX + 18, BY + 24
    svg = f"""
<rect x="{ix}" y="{iy}" width="140" height="144" rx="10" fill="{PANEL}" stroke="{BORDER}"/>
<rect x="{ix + 28}" y="{iy + 46}" width="84" height="58" rx="8" fill="none" stroke="{MUTED}" stroke-width="2"/><rect x="{ix + 42}" y="{iy + 37}" width="26" height="10" rx="3" fill="{MUTED}"/>
<circle cx="{ix + 70}" cy="{iy + 75}" r="18" fill="none" stroke="{TEXT}" stroke-width="2"/><circle cx="{ix + 70}" cy="{iy + 75}" r="7" fill="{SOFTWARE}"/>
{mono_text(BX + 178, BY + 48, "LOT 12 · CAMERAS", 16, MUTED, fit=False, extra='letter-spacing="1"')}
{''.join(els)}
<circle cx="{rx}" cy="{ry}" r="36" fill="none" stroke="{BORDER}" stroke-width="6"/>
<circle class="ring" cx="{rx}" cy="{ry}" r="36" fill="none" stroke="{SOFTWARE}" stroke-width="6" stroke-dasharray="{circ}" transform="rotate(-90 {rx} {ry})" stroke-linecap="round"/>
{mono_text(rx, ry + 6, "live", 16, TEXT, fit=False, anchor="middle")}
<g class="soft" opacity="0"><rect x="{rx - 80}" y="{ry + 54}" width="160" height="30" rx="15" fill="{PANEL}" stroke="{SOFTWARE}"/>{mono_text(rx, ry + 75, "soft close +30s", 15, SOFTWARE, fit=False, anchor="middle")}</g>
<g class="sold" opacity="0"><rect x="{BX + 300}" y="{BY + 62}" width="128" height="48" rx="8" fill="{BG_ALT}" stroke="{WHITE}" stroke-width="3" transform="rotate(-8 {BX + 364} {BY + 86})"/>
<text x="{BX + 364}" y="{BY + 96}" text-anchor="middle" font-family="{MONO}" font-size="26" font-weight="700" fill="{WHITE}" transform="rotate(-8 {BX + 364} {BY + 86})">SOLD</text></g>"""
    return card("auctionhub", SOFTWARE, "AuctionHub", "Live auctions on serverless AWS, in real time.",
                "bid p95 43 ms · 0 lost bids under load", css, svg,
                "Bids push the price up on a lot with a countdown; a late bid triggers a soft close extension before the hammer falls.")


def softhub():
    cycle = 8.0
    nodes = ["card", "λ shop", "Stripe", "λ hook", "SES", "inbox"]
    gx0, gstep, y = BX + 42, 92, BY + 50
    css, els = [], []
    for i, n in enumerate(nodes):
        x = gx0 + i * gstep
        t = (0.4 + i * 0.6) / cycle * 100
        css.append(kf(f"nd{i}", [(0, f"stroke:{BORDER}"), (t, f"stroke:{BORDER}"), (t + 1, f"stroke:{SOFTWARE}"), (92, f"stroke:{SOFTWARE}"), (100, f"stroke:{BORDER}")], cycle))
        els.append(f'<circle class="nd{i}" cx="{x}" cy="{y}" r="22" fill="{PANEL}" stroke-width="2.4"/>'
                   + mono_text(x, y + 48, n, 16, TEXT, fit=False, anchor="middle"))
        if i < len(nodes) - 1:
            els.append(f'<line x1="{x + 24}" y1="{y}" x2="{x + gstep - 24}" y2="{y}" stroke="{BORDER}" stroke-width="2"/>')
    t0, t1 = 0.4 / cycle * 100, (0.4 + 5 * 0.6) / cycle * 100
    css.append(kf("pkt", [(0, "transform:translateX(0);opacity:0"), (t0, "transform:translateX(0);opacity:1"),
                          (t1, f"transform:translateX({5 * gstep}px);opacity:1"), (t1 + 1, f"transform:translateX({5 * gstep}px);opacity:0"),
                          (100, f"transform:translateX({5 * gstep}px);opacity:0")], cycle))
    key = "SH-7F3K-Q9XW-2MLD-84NA"
    ts = (0.4 + 5 * 0.6 + 0.3)
    size = 21
    cw = 0.6 * size
    css.append(kf("key", [(0, "transform:scaleX(0)")] + [((ts + k * 0.07) / cycle * 100, f"transform:scaleX({(k + 1) / len(key):.3f})") for k in range(len(key))]
                  + [(92, "transform:scaleX(1)"), (100, "transform:scaleX(0)")], cycle, ";transform-box:fill-box;transform-origin:left;animation-timing-function:steps(1,end)"))
    kw = len(key) * cw
    kx, ky = BX + (BW - kw) / 2, BY + 158
    svg = f"""
{''.join(els)}
<circle class="pkt" cx="{gx0}" cy="{y}" r="7" fill="{SOFTWARE}"/>
<rect x="{BX + 16}" y="{BY + 126}" width="{BW - 32}" height="50" rx="10" fill="{PANEL}" stroke="{BORDER}"/>
<clipPath id="kc"><rect class="key" x="{f(kx)}" y="{ky - 20}" width="{f(kw + 4)}" height="30"/></clipPath>
<g clip-path="url(#kc)">{mono_text(kx, ky + 2, key, size, SOFTWARE, extra='font-weight="600"')}</g>"""
    return card("softhub", SOFTWARE, "SoftHub", "Pay with a card, get a licence key by e-mail.",
                "Stripe webhooks · ~US$2/month on AWS", css, svg,
                "A payment travels from the card through Lambda, Stripe and SES to the inbox, where a licence key types out.")


def crimson():
    cycle = 7.0
    chips = [("Tech", 0.6), ("Science", 1.1), ("Montréal", 1.6), ("F1", 2.1)]
    css, els = [], []
    x = BX + 16
    for i, (c, t) in enumerate(chips):
        w = len(c) * 9.6 + 32
        p = t / cycle * 100
        css.append(kf(f"ch{i}", [(0, f"fill:{PANEL};stroke:{BORDER}"), (p, f"fill:{PANEL};stroke:{BORDER}"),
                                 (p + 1, f"fill:#221D33;stroke:{SOFTWARE}"), (94, f"fill:#221D33;stroke:{SOFTWARE}"), (100, f"fill:{PANEL};stroke:{BORDER}")], cycle))
        els.append(f'<rect class="ch{i}" x="{f(x)}" y="{BY + 14}" width="{f(w)}" height="32" rx="16" stroke-width="1.5"/>'
                   + mono_text(x + w / 2, BY + 36, c, 16, TEXT, fit=False, anchor="middle"))
        x += w + 10
    hues = ["#3D3D3D", "#5A5A5A", "#2C2C2C"]
    for k in range(3):
        cx0 = BX + 16 + k * 176
        t = (2.6 + k * 0.35) / cycle * 100
        css.append(kf(f"sk{k}", [(0, "opacity:1"), (t, "opacity:1"), (t + 3, "opacity:0"), (94, "opacity:0"), (100, "opacity:1")], cycle))
        css.append(kf(f"ct{k}", [(0, "opacity:0"), (t, "opacity:0"), (t + 3, "opacity:1"), (94, "opacity:1"), (100, "opacity:0")], cycle))
        els.append(f"""<g class="ct{k}" opacity="0"><rect x="{cx0}" y="{BY + 60}" width="164" height="66" rx="8" fill="{hues[k]}"/>
<rect x="{cx0}" y="{BY + 138}" width="150" height="10" rx="5" fill="{TEXT}" opacity=".85"/><rect x="{cx0}" y="{BY + 155}" width="110" height="10" rx="5" fill="{TEXT}" opacity=".85"/>
<rect x="{cx0}" y="{BY + 173}" width="70" height="8" rx="4" fill="{SOFTWARE}"/></g>
<g class="sk{k}"><rect x="{cx0}" y="{BY + 60}" width="164" height="66" rx="8" fill="{PANEL}"/><rect x="{cx0}" y="{BY + 138}" width="150" height="10" rx="5" fill="{PANEL}"/>
<rect x="{cx0}" y="{BY + 155}" width="110" height="10" rx="5" fill="{PANEL}"/><rect x="{cx0}" y="{BY + 173}" width="70" height="8" rx="4" fill="{PANEL}"/></g>""")
    css.append(".shim{animation:shim 1.4s linear infinite}@keyframes shim{from{transform:translateX(-120px)}to{transform:translateX(640px)}}")
    svg = f"""
<defs><linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
{''.join(els)}
<rect class="shim" x="{BX}" y="{BY + 54}" width="100" height="{BH - 54}" fill="url(#sh)"/>"""
    return card("le-crimson", SOFTWARE, "Le Crimson", "A personalised news reader, rebuilt from scratch.",
                "React 19 · TanStack Query · axe-checked", css, svg,
                "Interest chips switch on and a news feed loads from skeleton placeholders into story cards.")


CARDS = [  # (builder, live url)
    (farme, f"{BASE}/FARM-E-Plantation-Lab/"),
    (hydro, f"{BASE}/Automated-Hydroponics-Lab/"),
    (rtmc, f"{BASE}/RTMC-HG-Lab/"),
    (f1can, f"{BASE}/F1-CAN-Telemetry-Lab/"),
    (mcl, f"{BASE}/Monte-Carlo-Localization/"),
    (mips, f"{BASE}/mini-MIPS/"),
    (arith, f"{BASE}/Arithmetic-Unit-Lab/"),
    (dds, f"{BASE}/DDS-Synthesizer/"),
    (calc, f"{BASE}/Calc-Functional-Verification/"),
    (auction, f"{BASE}/AuctionSystem-Lab/"),
    (softhub, f"{BASE}/SoftHub-Lab/"),
    (crimson, f"{BASE}/le-crimson-frontend/"),
]
