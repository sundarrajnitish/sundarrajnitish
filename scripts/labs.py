"""One animated card per lab. Each animation is a small, honest sketch of what the lab lets you do."""

import math
import random

from svgkit import (AMBER, BG_ALT, BORDER, BORDER_SOFT, CYAN, DIM, GREEN, MONO, MUTED, PANEL, RED, TEXT, VIOLET,
                    doc, esc, f, mono_text, text)

W, H = 600, 360
BX, BY, BW, BH = 28, 128, 544, 168  # animation box
BASE = "https://sundarrajnitish.github.io"


def kf(name, stops, dur, extra=""):
    """Keyframes block + class that runs it forever."""
    body = "".join(f"{f(p)}%{{{v}}}" for p, v in stops)
    return f"@keyframes {name}{{{body}}}.{name}{{animation:{name} {f(dur)}s linear infinite{extra}}}"


def card(slug, color, tag, title, hook, stat, anim_css, anim_svg, desc):
    css = "\n".join([
        f".play{{animation:nudge 2.4s ease-in-out infinite}}@keyframes nudge{{0%,70%,100%{{transform:none}}80%{{transform:translateX(4px)}}}}",
        *anim_css,
    ])
    body = f"""
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="#0A0E13" stroke="{BORDER}"/>
<rect x="28" y="28" width="4" height="16" rx="2" fill="{color}"/>
{mono_text(42, 42, tag, 14, color, fit=False, extra='letter-spacing="1.5"')}
{text(28, 84, title, 30, TEXT, 700)}
{text(28, 113, hook, 17, MUTED)}
<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="12" fill="{BG_ALT}" stroke="{BORDER_SOFT}"/>
<clipPath id="box"><rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="12"/></clipPath>
<g clip-path="url(#box)">{anim_svg}</g>
{mono_text(28, 330, stat, 15, MUTED, fit=False)}
<g class="play"><rect x="458" y="309" width="114" height="32" rx="16" fill="none" stroke="{color}"/>
{mono_text(515, 330, "▶ play it", 14, color, fit=False, anchor="middle")}</g>
"""
    return slug, doc(W, H, f"{title}: {hook}", css, body, desc)


# ---------------------------------------------------------------------------------------------

def farme():
    x0, x1, r = BX + 46, BX + BW - 46, 19
    ys = [BY + 26 + i * 2 * r for i in range(4)]
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
        f"@keyframes seed{{0%{{opacity:0;transform:scale(.4)}}1%{{opacity:1;fill:{AMBER};transform:scale(1)}}"
        f"14%{{fill:{AMBER};transform:scale(1)}}22%,95%{{opacity:1;fill:{GREEN};transform:scale(1.6)}}100%{{opacity:0}}}}",
        f".seed{{opacity:0;transform-box:fill-box;transform-origin:center;animation:seed {dur}s linear infinite}}",
    ]
    soil = "".join(
        f'<line x1="{BX + 14}" y1="{y}" x2="{BX + BW - 14}" y2="{y}" stroke="#3a2e1c" stroke-width="22" stroke-linecap="round" opacity=".55"/>'
        for y in ys)
    seeds = []
    for i, y in enumerate(ys):
        for k in range(1, int(straight // gap)):
            s = k * gap
            pos = i * (straight + arc) + s
            x = x0 + s if i % 2 == 0 else x1 - s
            seeds.append(f'<circle class="seed" cx="{f(x)}" cy="{y}" r="2.6" style="animation-delay:{f(pos / total * dur)}s"/>')
    robot = f"""
<g><animateMotion dur="{dur}s" repeatCount="indefinite" rotate="auto" path="{d}"/>
  <path d="M14 -7 L52 -24 L52 24 L14 7Z" fill="{AMBER}" opacity=".10"/>
  <rect x="-15" y="-13" width="30" height="5" rx="2" fill="#2a3340"/><rect x="-15" y="8" width="30" height="5" rx="2" fill="#2a3340"/>
  <rect x="-12" y="-9" width="24" height="18" rx="3" fill="#c9ced6"/>
  <rect x="-6" y="-6" width="10" height="12" rx="2" fill="{AMBER}"/>
  <circle cx="11" cy="0" r="2.4" fill="{CYAN}"/>
</g>"""
    svg = soil + f'<path d="{d}" fill="none" stroke="{AMBER}" stroke-opacity=".18" stroke-dasharray="3 6"/>' + "".join(seeds) + robot
    return card("farm-e", AMBER, "MACHINES · 2020 → 2026", "FARM-E", "A tracked robot that plants, seeds and waters a bed.",
                "UNO + ESP8266 firmware, co-simulated", css, svg,
                "A small tracked robot drives a serpentine path over soil rows, dropping seeds that sprout behind it.")


def hydro():
    random.seed(7)
    x0, x1, yt, yb = BX + 54, BX + BW - 20, BY + 18, BY + BH - 22
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
        drops.append(f'<path class="dp{i}" opacity="0" d="M{f(x)} {f(yt + 2)}q-4 6 0 9q4 -3 0 -9z" fill="{CYAN}"/>')
    svg = f"""
<rect x="{x0}" y="{f(Y(6.5))}" width="{x1 - x0}" height="{f(Y(5.5) - Y(6.5))}" fill="{GREEN}" opacity=".10"/>
<line x1="{x0}" y1="{f(Y(6.5))}" x2="{x1}" y2="{f(Y(6.5))}" stroke="{GREEN}" stroke-opacity=".45" stroke-dasharray="4 4"/>
<line x1="{x0}" y1="{f(Y(5.5))}" x2="{x1}" y2="{f(Y(5.5))}" stroke="{GREEN}" stroke-opacity=".45" stroke-dasharray="4 4"/>
{mono_text(x0 - 10, Y(6.5) + 4, "6.5", 12, GREEN, fit=False, anchor="end")}
{mono_text(x0 - 10, Y(5.5) + 4, "5.5", 12, GREEN, fit=False, anchor="end")}
{mono_text(x0 - 10, Y(7.9) + 4, "pH 7.9", 12, DIM, fit=False, anchor="end")}
{mono_text(x0, yb + 16, "day 0", 12, DIM, fit=False)}
{mono_text(x1, yb + 16, "day 14", 12, DIM, fit=False, anchor="end")}
<path d="{d}" fill="none" stroke="{AMBER}" stroke-width="2.2" stroke-linejoin="round" stroke-dasharray="{f(L)}" class="trace"/>
{''.join(drops)}"""
    return card("hydroponinator", AMBER, "MACHINES · 2020 → 2026", "Hydroponinator",
                "Grow-rack controller that keeps the pH in band.", "pH in 5.5–6.5 for 100% of a 14-day grow",
                css, svg, "Reservoir pH starts at 7.9 from tap water, is dosed down into the 5.5 to 6.5 band, and "
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
    fingers = [  # x, base y, length, width, tilt
        (BX + 70, BY + 112, 46, 16, -38),
        (BX + 104, BY + 84, 64, 15, -6),
        (BX + 126, BY + 82, 70, 15, 0),
        (BX + 148, BY + 84, 64, 15, 5),
        (BX + 168, BY + 90, 50, 14, 12),
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
                    f'width="{w}" height="{ln}" rx="{w / 2}" fill="#c9ced6"/></g>')
    labels = []
    for g, (name, ext) in enumerate(GESTURES):
        a, b = g / len(GESTURES) * 100, (g + 1) / len(GESTURES) * 100
        stops = [(0, "opacity:0"), (a, "opacity:0"), (a + 0.01, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")]
        if g == 0:
            stops = [(0, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")]
        css.append(kf(f"gl{g}", stops, cycle))
        servos = ", ".join(str(0 if e else CLOSED_DEG[k]) for k, e in enumerate(ext))
        labels.append(f'<g class="gl{g}" opacity="{1 if g == 0 else 0}">'
                      + mono_text(BX + 262, BY + 64, name, 18, TEXT, fit=False)
                      + mono_text(BX + 262, BY + 96, f"servos ({servos})", 14, AMBER, fit=False)
                      + "</g>")
    svg = f"""
<rect x="{BX + 236}" y="{BY + 20}" width="2" height="{BH - 40}" fill="{BORDER}"/>
{mono_text(BX + 262, BY + 36, "gesture", 13, DIM, fit=False)}
{''.join(labels)}
{mono_text(BX + 262, BY + 130, "camera -> CNN -> UDP -> servos", 13, DIM, fit=False)}
{''.join(fsvg)}
<rect x="{BX + 58}" y="{BY + 84}" width="124" height="66" rx="22" fill="#c9ced6"/>
<rect x="{BX + 98}" y="{BY + 140}" width="48" height="28" fill="#c9ced6"/>
<path d="M{BX + 70} {BY + 112}L{BX + 50} {BY + 96}" stroke="#c9ced6" stroke-width="0"/>"""
    return card("rtmc-hg", AMBER, "MACHINES · 2021 → 2026", "RTMC-HG", "Steer a tendon-driven robot hand with gestures.",
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
    tx, ty = BX + 22, BY + 26
    track = (f"M{tx + 20} {ty + 92}C{tx + 4} {ty + 92} {tx} {ty + 70} {tx + 14} {ty + 58}L{tx + 60} {ty + 30}"
             f"C{tx + 70} {ty + 24} {tx + 82} {ty + 30} {tx + 92} {ty + 24}L{tx + 150} {ty + 6}"
             f"C{tx + 172} {ty} {tx + 186} {ty + 18} {tx + 170} {ty + 30}C{tx + 160} {ty + 38} {tx + 150} {ty + 46} {tx + 152} {ty + 60}"
             f"L{tx + 168} {ty + 104}C{tx + 172} {ty + 118} {tx + 160} {ty + 126} {tx + 146} {ty + 120}L{tx + 112} {ty + 108}"
             f"C{tx + 100} {ty + 104} {tx + 90} {ty + 112} {tx + 78} {ty + 106}Z")
    lap = 7.0
    samples = [(301.2, 11600, 100, 8, 0, 1), (322.4, 11850, 100, 8, 0, 1), (118.6, 8900, 0, 3, 1, 0),
               (64.3, 7600, 22, 2, 0, 0), (187.9, 10800, 100, 5, 0, 0), (254.0, 11400, 100, 7, 0, 0),
               (139.5, 9600, 0, 4, 1, 0), (233.8, 11200, 86, 6, 0, 0)]
    slot = lap / len(samples)
    css, frames = [], []
    for i, (spd, rpm, thr, gear, brk, drs) in enumerate(samples):
        v = round(spd * 10)
        data = [v & 0xFF, v >> 8, rpm & 0xFF, rpm >> 8, thr, gear | (brk << 4) | (drs << 5), i & 0x0F]
        data.append(crc8_j1850(data))
        a, b = i / len(samples) * 100, (i + 1) / len(samples) * 100
        stops = [(0, "opacity:0"), (a, "opacity:0"), (a + 0.01, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")]
        if i == 0:
            stops = [(0, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")]
        css.append(kf(f"fr{i}", stops, lap))
        boxes = []
        for k, byte in enumerate(data):
            x = BX + 236 + k * 37
            col = AMBER if k == 7 else (GREEN if k == 6 else TEXT)
            boxes.append(f'<rect x="{x}" y="{BY + 56}" width="33" height="30" rx="5" fill="{PANEL}" stroke="{BORDER}"/>'
                         + mono_text(x + 16.5, BY + 76, f"{byte:02X}", 15, col, fit=False, anchor="middle"))
        frames.append(f'<g class="fr{i}" opacity="{1 if i == 0 else 0}">{"".join(boxes)}'
                      + mono_text(BX + 236, BY + 116, f"speed {spd:5.1f} km/h  gear {gear}", 14, TEXT, fit=False)
                      + mono_text(BX + 236, BY + 140, f"rpm {rpm:,}  thr {thr:3d}%  " + ("DRS" if drs else ("BRAKE" if brk else "")),
                                  14, GREEN if drs else (RED if brk else MUTED), fit=False)
                      + "</g>")
    svg = f"""
<path d="{track}" fill="none" stroke="#2a3340" stroke-width="9" stroke-linejoin="round"/>
<path d="{track}" fill="none" stroke="{BORDER}" stroke-width="1" stroke-dasharray="2 6"/>
<g><animateMotion dur="{lap}s" repeatCount="indefinite" path="{track}" begin="-0.45s"/><circle r="5" fill="{MUTED}" opacity=".7"/></g>
<g><animateMotion dur="{lap}s" repeatCount="indefinite" path="{track}"/><circle r="9" fill="{GREEN}" opacity=".2"/><circle r="5" fill="{GREEN}"/></g>
{mono_text(BX + 236, BY + 36, "0x101 F1_CarTelemetry", 14, GREEN, fit=False)}
{mono_text(BX + 530, BY + 36, "500 kbit/s", 12, DIM, fit=False, anchor="end")}
{''.join(frames)}"""
    return card("f1-can", GREEN, "SIGNALS · 2025 → 2026", "F1 CAN Telemetry", "The 2023 Canadian GP, streamed over a CAN bus.",
                "CRC-8 on every frame · real lap data", css, svg,
                "A car laps a sketch of the Montreal circuit while its telemetry is packed into 8-byte CAN frames with a CRC.")


def mcl():
    random.seed(3)
    cy, x_start, x_end = BY + 92, BX + 120, BX + 420
    cycle = 9.0
    walls = (f"M{BX + 10} {BY + 52}H{BX + 150}v-14h40v14H{BX + 330}v-14h50v14H{BX + BW - 10}"
             f"M{BX + 10} {BY + 132}H{BX + 230}v14h44v-14H{BX + 450}v14h40v-14H{BX + BW - 10}")
    css = [kf("ride", [(0, "transform:translateX(0)"), (46, "transform:translateX(0)"),
                       (94, f"transform:translateX({x_end - x_start}px)"), (100, f"transform:translateX({x_end - x_start}px)")], cycle),
           kf("beam", [(0, "opacity:0"), (44, "opacity:0"), (48, "opacity:.5"), (94, "opacity:.5"), (100, "opacity:0")], cycle)]
    parts = []
    for i in range(70):
        ox, oy = random.gauss(0, 7), random.gauss(0, 4)
        sx, sy = random.uniform(BX + 16, BX + BW - 16), random.uniform(BY + 58, BY + 126)
        dx, dy = sx - (x_start + ox), sy - (cy + oy)
        # a few particles lock onto the look-alike stretch first, then die off
        mid = (f"transform:translate({f(dx * 0.45 + 140)}px,{f(dy * 0.3)}px)" if i % 5 == 0 else
               f"transform:translate({f(dx * 0.25)}px,{f(dy * 0.25)}px)")
        css.append(kf(f"p{i}", [(0, f"transform:translate({f(dx)}px,{f(dy)}px)"), (8, f"transform:translate({f(dx)}px,{f(dy)}px)"),
                                (26, mid), (42, "transform:translate(0,0)"), (100, "transform:translate(0,0)")], cycle))
        parts.append(f'<circle class="p{i}" cx="{f(x_start + ox)}" cy="{f(cy + oy)}" r="2.3" fill="{GREEN}" opacity=".8"/>')
    beams = "".join(
        f'<line x1="{x_start}" y1="{cy}" x2="{f(x_start + math.cos(a) * 200)}" y2="{f(cy + math.sin(a) * 200)}" stroke="{AMBER}" stroke-width=".8"/>'
        for a in [math.radians(d) for d in range(-150, 181, 30)])
    svg = f"""
<path d="{walls}" fill="none" stroke="#c9ced6" stroke-width="3"/>
<g class="ride"><g class="beam" opacity="0" clip-path="url(#hall)">{beams}</g>
{''.join(parts)}
<circle cx="{x_start}" cy="{cy}" r="7" fill="none" stroke="{TEXT}" stroke-width="2"/><path d="M{x_start} {cy}h10" stroke="{TEXT}" stroke-width="2"/></g>
<clipPath id="hall"><rect x="{BX - 400}" y="{BY + 53}" width="{BW + 800}" height="78"/></clipPath>
{mono_text(BX + 16, BY + 24, "28 m hallway · 180-beam laser · 1000 particles", 13, DIM, fit=False)}
{mono_text(BX + 16, BY + 160, "uniform -> converged -> tracking", 13, GREEN, fit=False)}"""
    return card("monte-carlo-localization", GREEN, "SIGNALS · 2026", "Monte Carlo Localization",
                "A particle filter that works out where the robot is.", "4 cm median error on a real laser log", css, svg,
                "Particles scattered over a hallway converge onto the robot's true position, then follow it as it drives.")


def mips():
    cols, rows = 9, [
        ("lw  $t1,0($a0)", ["IF", "ID", "EX", "MEM", "WB"], 0, None),
        ("add $t2,$t1,$t0", ["IF", "ID", "--", "EX", "MEM", "WB"], 1, 2),
        ("sub $t3,$t2,$t0", ["IF", "IF", "ID", "EX", "MEM", "WB"], 2, None),
        ("sw  $t3,4($a0)", ["IF", "ID", "EX", "MEM", "WB"], 4, None),
    ]
    colors = {"IF": "#2c6f86", "ID": "#2b5f8a", "EX": CYAN, "MEM": "#7a6cd9", "WB": GREEN, "--": RED}
    gx, gy, cw, rh = BX + 186, BY + 34, 38, 26
    cycle = 9.0
    per = 0.75
    css = [kf("cur", [(0, "transform:translateX(0)")] + [(((c + 1) * per) / cycle * 100, f"transform:translateX({(c + 1) * cw}px)") for c in range(cols)]
              + [(97, f"transform:translateX({cols * cw}px)"), (100, "transform:translateX(0)")], cycle,
              ";animation-timing-function:steps(1,end)")]
    cells = [mono_text(gx + c * cw + cw / 2, gy - 12, str(c + 1), 12, DIM, fit=False, anchor="middle") for c in range(cols)]
    for r, (ins, stages, start, _) in enumerate(rows):
        y = gy + r * rh
        cells.append(mono_text(BX + 16, y + 18, ins, 14, TEXT if r != 1 else AMBER, fit=False))
        for k, st in enumerate(stages):
            c = start + k
            t = (c * per + 0.05) / cycle * 100
            name = f"c{r}_{k}"
            css.append(kf(name, [(0, "opacity:0"), (t, "opacity:0"), (t + 0.5, "opacity:1"), (96, "opacity:1"), (100, "opacity:0")], cycle))
            fill = colors[st]
            label = "stall" if st == "--" else st
            cells.append(f'<g class="{name}" opacity="0"><rect x="{gx + c * cw + 2}" y="{y + 2}" width="{cw - 4}" height="{rh - 4}" rx="4" '
                         f'fill="{fill}" fill-opacity="{0.25 if st == "--" else 0.85}"/>'
                         + mono_text(gx + c * cw + cw / 2, y + 17.5, label, 11 if st != "--" else 10, TEXT, fit=False, anchor="middle") + "</g>")
    # forwarding: lw MEM (cycle 4) -> add EX (cycle 5)
    t = (4 * per + 0.3) / cycle * 100
    css.append(kf("fwd", [(0, "opacity:0"), (t, "opacity:0"), (t + 1, "opacity:1"), (96, "opacity:1"), (100, "opacity:0")], cycle))
    ax, ay = gx + 3 * cw + cw / 2, gy + rh - 4
    bx, by = gx + 4 * cw + cw / 2, gy + rh + 4
    cells.append(f'<path class="fwd" opacity="0" d="M{ax} {ay}C{ax} {ay + 8} {bx - 10} {by - 6} {bx - 4} {by}" fill="none" stroke="{AMBER}" stroke-width="2"/>')
    svg = f"""
{''.join(cells)}
<g class="cur"><rect x="{gx}" y="{gy - 26}" width="{cw}" height="{len(rows) * rh + 28}" fill="{TEXT}" opacity=".06"/></g>
{mono_text(BX + 16, BY + 160, "load-use: 1 stall, then forwarded", 13, AMBER, fit=False)}
{mono_text(BX + BW - 16, BY + 160, "CPI 1.298", 13, CYAN, fit=False, anchor="end")}"""
    return card("mini-mips", CYAN, "SILICON · 2023 → 2026", "mini-MIPS", "A 5-stage pipelined MIPS in VHDL, cycle by cycle.",
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
    labels = ["partial products 8x8", "Dadda d=6", "Dadda d=4", "Dadda d=3", "Dadda d=2", "carry-propagate -> P"]
    slot = 1.25
    cycle = slot * len(stages) + 1.5
    dx, dy = 21, 15
    x_right, y_base = BX + 506, BY + 138
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
                        f'fill="{CYAN}" opacity="{int(vis[0])}"/>')
    css.append(kf("pfinal", steps_for((False,) * (len(stages) - 1) + (True,)), cycle))
    dots += [f'<circle class="pfinal" cx="{x_right - c * dx}" cy="{y_base}" r="5" fill="{GREEN}" opacity="0"/>' for c in range(16)]
    lab = []
    for s, name in enumerate(labels):
        a, b = s * slot / cycle * 100, (s + 1) * slot / cycle * 100 if s < len(labels) - 1 else 100
        stops = [(0, "opacity:0"), (a, "opacity:0"), (a + 0.01, "opacity:1"), (b, "opacity:1"), (min(b + 0.01, 100), "opacity:0")]
        if s == 0:
            stops = [(0, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")]
        css.append(kf(f"lb{s}", stops, cycle))
        lab.append(f'<g class="lb{s}" opacity="{1 if s == 0 else 0}">{mono_text(BX + 16, BY + 28, name, 15, TEXT if s < 5 else GREEN, fit=False)}</g>')
    svg = f"""
{''.join(lab)}
{''.join(dots)}
{mono_text(BX + 16, BY + 160, "P = A·B/2^C + D", 13, DIM, fit=False)}"""
    return card("arithmetic-unit", CYAN, "SILICON · 2023 → 2026", "Arithmetic Unit",
                "Multipliers in structural VHDL, from full adders up.", "83 regression runs · didn't compile in 2023",
                css, svg, "The 8 by 8 partial-product matrix of a multiplier shrinks through the Dadda reduction stages to a single product row.")


def dds():
    cx, cy, R = BX + 86, BY + 86, 50
    T = 2.4
    lam = 160
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
<g class="spin"><line x1="{cx}" y1="{cy}" x2="{cx + R}" y2="{cy}" stroke="{CYAN}" stroke-width="2.5"/><circle cx="{cx + R}" cy="{cy}" r="5" fill="{CYAN}"/></g>
<g class="proj"><line x1="{cx}" y1="{cy}" x2="{x0}" y2="{cy}" stroke="{CYAN}" stroke-opacity=".35" stroke-dasharray="3 4"/><circle cx="{x0}" cy="{cy}" r="4" fill="{TEXT}"/></g>
<clipPath id="wv"><rect x="{x0}" y="{BY}" width="{BW}" height="{BH}"/></clipPath>
<g clip-path="url(#wv)"><path class="scroll" d="{wave}" fill="none" stroke="{CYAN}" stroke-width="2.4"/></g>
{mono_text(BX + 16, BY + 160, "32-bit phase accumulator -> quarter-wave sine ROM", 13, DIM, fit=False)}
<g><rect x="{BX + BW - 168}" y="{BY + 12}" width="156" height="28" rx="14" fill="{PANEL}" stroke="{GREEN}" stroke-opacity=".6"/>
{mono_text(BX + BW - 90, BY + 31, "RTL ≡ netlist ✓", 13, GREEN, fit=False, anchor="middle")}</g>"""
    return card("dds-synthesizer", CYAN, "SILICON · 2024 → 2026", "DDS Formal",
                "Prove a buggy netlist wrong, then fix it, automatically.", "14 bugs found and repaired in ~5 s",
                css, svg, "A rotating phasor traces a sine wave, the output of a direct digital synthesizer whose netlist is proven equivalent to its RTL.")


def calc():
    n, cycle = 14, 10.0
    css, tiles = [], []
    for i in range(n):
        col, row = i % 7, i // 7
        x, y = BX + 16 + col * 74, BY + 62 + row * 46
        t = (0.8 + i * 0.5) / cycle * 100
        css.append(kf(f"b{i}", [(0, f"fill:{PANEL};stroke:{BORDER}"), (t, f"fill:{PANEL};stroke:{BORDER}"),
                                (t + 1, f"fill:#3a1714;stroke:{RED}"), (t + 4, f"fill:#0f2a20;stroke:{GREEN}"),
                                (95, f"fill:#0f2a20;stroke:{GREEN}"), (100, f"fill:{PANEL};stroke:{BORDER}")], cycle))
        css.append(kf(f"k{i}", [(0, "opacity:0"), (t + 3.5, "opacity:0"), (t + 4, "opacity:1"), (95, "opacity:1"), (100, "opacity:0")], cycle))
        tiles.append(f'<rect class="b{i}" x="{x}" y="{y}" width="66" height="36" rx="7" stroke-width="1.5"/>'
                     + mono_text(x + 9, y + 23, f"c{1 if i < 7 else 3}·b{i % 7 + 1}", 13, MUTED, fit=False)
                     + f'<g class="k{i}" opacity="0">{mono_text(x + 60, y + 23, "✓", 14, GREEN, fit=False, anchor="end")}</g>')
    cnt = []
    for i in range(n + 1):
        a = (0.8 + (i - 1) * 0.5) / cycle * 100 + 4 if i else 0
        b = (0.8 + i * 0.5) / cycle * 100 + 4 if i < n else 95
        stops = [(0, "opacity:0"), (a, "opacity:0"), (a + 0.01, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")]
        if i == 0:
            stops = [(0, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (99.9, "opacity:0"), (100, "opacity:1")]
        css.append(kf(f"n{i}", stops, cycle))
        cnt.append(f'<g class="n{i}" opacity="{1 if i == 0 else 0}">{mono_text(BX + BW - 16, BY + 34, f"caught {i:2d}/14", 16, GREEN if i == n else TEXT, fit=False, anchor="end")}</g>')
    svg = f"""
{mono_text(BX + 16, BY + 34, "inject a bug -> the testbench must fail", 13, DIM, fit=False)}
{''.join(tiles)}
{''.join(cnt)}
{mono_text(BX + 16, BY + 160, "0 false failures on the golden designs", 13, DIM, fit=False)}"""
    return card("calc-verification", CYAN, "SILICON · 2024 → 2026", "Calc Verification",
                "A self-checking testbench that finds the planted bugs.", "14/14 bugs caught · 2024 failures root-caused",
                css, svg, "Fourteen injected bugs in two calculator designs light up red as the regression catches each one, then turn green.")


def auction():
    cycle = 10.0
    bids = [(0.6, "C$120", "maple_kid"), (2.0, "C$125", "you"), (3.4, "C$135", "otter88"), (5.0, "C$145", "you"),
            (6.6, "C$150", "otter88")]
    css = [kf("ring", [(0, "stroke-dashoffset:0"), (58, "stroke-dashoffset:170"), (60, "stroke-dashoffset:110"),
                       (82, "stroke-dashoffset:207"), (100, "stroke-dashoffset:207")], cycle)]
    els = []
    for i, (t, price, who) in enumerate(bids):
        a = t / cycle * 100
        b = bids[i + 1][0] / cycle * 100 if i + 1 < len(bids) else 98
        css.append(kf(f"bd{i}", [(0, "opacity:0"), (a, "opacity:0"), (a + 0.01, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0"), (100, "opacity:0")], cycle))
        els.append(f'<g class="bd{i}" opacity="0">'
                   + text(BX + 168, BY + 82, price, 38, TEXT, 700)
                   + mono_text(BX + 170, BY + 108, f"high bid · {who}", 14, VIOLET if who == "you" else MUTED, fit=False) + "</g>")
    css.append(kf("soft", [(0, "opacity:0"), (59, "opacity:0"), (60, "opacity:1"), (80, "opacity:1"), (81, "opacity:0"), (100, "opacity:0")], cycle))
    css.append(kf("sold", [(0, "opacity:0;transform:scale(1.6)"), (84, "opacity:0;transform:scale(1.6)"), (86, "opacity:1;transform:scale(1)"),
                           (98, "opacity:1;transform:scale(1)"), (100, "opacity:0")], cycle, ";transform-box:fill-box;transform-origin:center"))
    rx, ry = BX + BW - 70, BY + 80
    svg = f"""
<rect x="{BX + 18}" y="{BY + 18}" width="130" height="130" rx="10" fill="#2b2350"/>
<circle cx="{BX + 83}" cy="{BY + 80}" r="34" fill="{VIOLET}" opacity=".55"/><rect x="{BX + 50}" y="{BY + 104}" width="66" height="22" rx="4" fill="{VIOLET}" opacity=".35"/>
{mono_text(BX + 170, BY + 40, "LOT 12 · ROOM: CAMERAS", 13, DIM, fit=False)}
{''.join(els)}
<circle cx="{rx}" cy="{ry}" r="33" fill="none" stroke="{BORDER}" stroke-width="6"/>
<circle class="ring" cx="{rx}" cy="{ry}" r="33" fill="none" stroke="{VIOLET}" stroke-width="6" stroke-dasharray="207" transform="rotate(-90 {rx} {ry})" stroke-linecap="round"/>
{mono_text(rx, ry + 5, "live", 13, MUTED, fit=False, anchor="middle")}
<g class="soft" opacity="0"><rect x="{rx - 56}" y="{ry + 44}" width="112" height="24" rx="12" fill="{PANEL}" stroke="{AMBER}"/>{mono_text(rx, ry + 61, "soft close +30s", 12, AMBER, fit=False, anchor="middle")}</g>
<g class="sold" opacity="0"><rect x="{BX + 300}" y="{BY + 56}" width="120" height="44" rx="8" fill="none" stroke="{GREEN}" stroke-width="3" transform="rotate(-8 {BX + 360} {BY + 78})"/>
<text x="{BX + 360}" y="{BY + 87}" text-anchor="middle" font-family="{MONO}" font-size="24" font-weight="700" fill="{GREEN}" transform="rotate(-8 {BX + 360} {BY + 78})">SOLD</text></g>"""
    return card("auctionhub", VIOLET, "CLOUD · 2024 → 2026", "AuctionHub", "Live auctions on serverless AWS, in real time.",
                "bid p95 43 ms · 0 lost bids under load", css, svg,
                "Bids push the price up on a lot with a countdown; a late bid triggers a soft close extension before the hammer falls.")


def softhub():
    cycle = 8.0
    nodes = ["card", "λ shop", "Stripe", "λ hook", "SES", "inbox"]
    gx0, gstep, y = BX + 40, 92, BY + 46
    css, els = [], []
    for i, n in enumerate(nodes):
        x = gx0 + i * gstep
        t = (0.4 + i * 0.6) / cycle * 100
        css.append(kf(f"nd{i}", [(0, f"stroke:{BORDER}"), (t, f"stroke:{BORDER}"), (t + 1, f"stroke:{VIOLET}"), (92, f"stroke:{VIOLET}"), (100, f"stroke:{BORDER}")], cycle))
        els.append(f'<circle class="nd{i}" cx="{x}" cy="{y}" r="20" fill="{PANEL}" stroke-width="2"/>'
                   + mono_text(x, y + 40, n, 12, MUTED, fit=False, anchor="middle"))
        if i < len(nodes) - 1:
            els.append(f'<line x1="{x + 22}" y1="{y}" x2="{x + gstep - 22}" y2="{y}" stroke="{BORDER}" stroke-width="2"/>')
    t0, t1 = 0.4 / cycle * 100, (0.4 + 5 * 0.6) / cycle * 100
    css.append(kf("pkt", [(0, "transform:translateX(0);opacity:0"), (t0, "transform:translateX(0);opacity:1"),
                          (t1, f"transform:translateX({5 * gstep}px);opacity:1"), (t1 + 1, f"transform:translateX({5 * gstep}px);opacity:0"),
                          (100, f"transform:translateX({5 * gstep}px);opacity:0")], cycle))
    key = "SH-7F3K-Q9XW-2MLD-84NA"
    ts = (0.4 + 5 * 0.6 + 0.3)
    cw = 0.6 * 17
    css.append(kf("key", [(0, "transform:scaleX(0)")] + [((ts + k * 0.07) / cycle * 100, f"transform:scaleX({(k + 1) / len(key):.3f})") for k in range(len(key))]
                  + [(92, "transform:scaleX(1)"), (100, "transform:scaleX(0)")], cycle, ";transform-box:fill-box;transform-origin:left;animation-timing-function:steps(1,end)"))
    kx, ky = BX + 150, BY + 126
    svg = f"""
{''.join(els)}
<circle class="pkt" cx="{gx0}" cy="{y}" r="6" fill="{VIOLET}"/>
<rect x="{BX + 16}" y="{BY + 104}" width="{BW - 32}" height="44" rx="8" fill="{PANEL}" stroke="{BORDER}"/>
{mono_text(BX + 30, ky + 6, "licence key", 13, DIM, fit=False)}
<clipPath id="kc"><rect class="key" x="{kx}" y="{ky - 16}" width="{f(len(key) * cw + 4)}" height="24"/></clipPath>
<g clip-path="url(#kc)">{mono_text(kx, ky + 6, key, 17, GREEN)}</g>"""
    return card("softhub", VIOLET, "CLOUD · 2025 → 2026", "SoftHub", "Pay with a card, get a licence key by e-mail.",
                "Stripe webhooks · ~US$2/month on AWS", css, svg,
                "A payment travels from the card through Lambda, Stripe and SES to the inbox, where a licence key types out.")


def crimson():
    cycle = 7.0
    chips = [("Tech", 0.6), ("Science", 1.1), ("Montréal", 1.6), ("F1", 2.1)]
    css, els = [], []
    x = BX + 16
    for i, (c, t) in enumerate(chips):
        w = len(c) * 8.4 + 24
        p = t / cycle * 100
        css.append(kf(f"ch{i}", [(0, f"fill:{PANEL};stroke:{BORDER}"), (p, f"fill:{PANEL};stroke:{BORDER}"),
                                 (p + 1, f"fill:#2b2350;stroke:{VIOLET}"), (94, f"fill:#2b2350;stroke:{VIOLET}"), (100, f"fill:{PANEL};stroke:{BORDER}")], cycle))
        els.append(f'<rect class="ch{i}" x="{f(x)}" y="{BY + 14}" width="{f(w)}" height="26" rx="13"/>'
                   + mono_text(x + w / 2, BY + 32, c, 13, TEXT, fit=False, anchor="middle"))
        x += w + 8
    hues = ["#5b3fa8", "#2c6f86", "#8a5a1c"]
    for k in range(3):
        cx0 = BX + 16 + k * 176
        t = (2.6 + k * 0.35) / cycle * 100
        css.append(kf(f"sk{k}", [(0, "opacity:1"), (t, "opacity:1"), (t + 3, "opacity:0"), (94, "opacity:0"), (100, "opacity:1")], cycle))
        css.append(kf(f"ct{k}", [(0, "opacity:0"), (t, "opacity:0"), (t + 3, "opacity:1"), (94, "opacity:1"), (100, "opacity:0")], cycle))
        els.append(f"""<g class="ct{k}" opacity="0"><rect x="{cx0}" y="{BY + 52}" width="164" height="58" rx="8" fill="{hues[k]}"/>
<rect x="{cx0}" y="{BY + 118}" width="150" height="9" rx="4" fill="{TEXT}" opacity=".85"/><rect x="{cx0}" y="{BY + 133}" width="110" height="9" rx="4" fill="{TEXT}" opacity=".85"/>
<rect x="{cx0}" y="{BY + 150}" width="70" height="7" rx="3" fill="{MUTED}"/></g>
<g class="sk{k}"><rect x="{cx0}" y="{BY + 52}" width="164" height="58" rx="8" fill="{PANEL}"/><rect x="{cx0}" y="{BY + 118}" width="150" height="9" rx="4" fill="{PANEL}"/>
<rect x="{cx0}" y="{BY + 133}" width="110" height="9" rx="4" fill="{PANEL}"/><rect x="{cx0}" y="{BY + 150}" width="70" height="7" rx="3" fill="{PANEL}"/></g>""")
    css.append(".shim{animation:shim 1.4s linear infinite}@keyframes shim{from{transform:translateX(-120px)}to{transform:translateX(640px)}}")
    svg = f"""
<defs><linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
{''.join(els)}
<rect class="shim" x="{BX}" y="{BY + 46}" width="100" height="{BH - 46}" fill="url(#sh)"/>"""
    return card("le-crimson", VIOLET, "INTERFACES · 2022 → 2026", "Le Crimson", "A personalised news reader, rebuilt from scratch.",
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
