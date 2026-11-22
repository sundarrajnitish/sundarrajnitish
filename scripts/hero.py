"""Header: a rainy neon street corner with a running gag, for the GitHub README.

Left: a brick wall with Nitish's name in neon tubes and a door into the portfolio.
Middle: Nitish eating noodles with chopsticks. Right: a ramen stall whose sign reads
BUG-FREE RAMEN and whose cook is a small robot in a chef hat.

The 12 s loop:
  0.0-3.9  Nitish eats. Rain falls. The robot stirs the pot.
  3.9-4.5  The "-FREE" tube flickers out. The sign now reads BUG   RAMEN.
  5.0-7.0  A bug comes up on his chopsticks. The robot's visor flashes BUG?!
  6.3      "that's bug #15."  He flicks it into the jar and the count goes 14 -> 15.
  7.9-8.4  "-FREE" flickers back on. The robot looks pleased.

GitHub shows README images through <img>, so this is one self-contained SVG: CSS
keyframes and SMIL only, no script, no web fonts. PHASE is 0 so the CSS and SMIL
timelines start together.
"""

import math
import random

from svgkit import MONO, SANS, doc, esc, f

W, H = 1200, 440
FLOOR = 372
CYCLE = 12.0

# Palette: the portfolio's obsidian base and amber/cyan accents, pushed toward neon.
SKY_TOP = "#05060A"
SKY_LOW = "#120B22"
WALL = "#0B0D15"
WALL_LINE = "#151A26"
INK = "#F4F6FB"
MUTED = "#9EA7B8"
AMBER = "#FF9442"
GOLD = "#FFB020"
CYAN = "#38BDF8"
PINK = "#FF4F9A"
GREEN = "#34D399"
RED = "#FF5454"
DEAD_TUBE = "#1A1F2C"

SKIN = "#A96F51"
SKIN_DK = "#86533B"
SKIN_LT = "#BF8766"
HAIR = "#15100E"
HAIR_HI = "#362822"
HOODIE = "#1D2333"
SLEEVE = "#1E2536"


# ---------------------------------------------------------------------------- timing helpers

def pct(sec):
    return f"{f(sec / CYCLE * 100)}%"


def kf(name, stops):
    return f"@keyframes {name}{{" + "".join(f"{pct(t)}{{{p}}}" for t, p in stops) + "}"


def run(name, easing="linear"):
    return f"animation:{name} {f(CYCLE)}s {easing} infinite"


def shown(name, spans, ramp=0.08):
    """Opacity keyframes that are 1 inside each (start, end) span and 0 elsewhere."""
    stops = [(0, "opacity:0")]
    for a, b in spans:
        stops += [(a, "opacity:0"), (a + ramp, "opacity:1"), (b, "opacity:1"), (b + ramp, "opacity:0")]
    stops.append((CYCLE, "opacity:0"))
    return kf(name, stops)


def hidden(name, spans, ramp=0.08):
    """The inverse of shown(): visible except inside each span."""
    stops = [(0, "opacity:1")]
    for a, b in spans:
        stops += [(a, "opacity:1"), (a + ramp, "opacity:0"), (b, "opacity:0"), (b + ramp, "opacity:1")]
    stops.append((CYCLE, "opacity:1"))
    return kf(name, stops)


def smil(attr, frames, kind="animate", extra=""):
    """SMIL animation on the shared CYCLE clock with eased segments."""
    times = ";".join(f"{t / CYCLE:.4f}" for t, _ in frames)
    values = ";".join(v for _, v in frames)
    splines = ";".join([".42 0 .58 1"] * (len(frames) - 1))
    tag = "animateTransform" if kind != "animate" else "animate"
    typ = f' type="{kind}"' if kind != "animate" else ""
    return (f'<{tag} attributeName="{attr}"{typ} dur="{f(CYCLE)}s" repeatCount="indefinite" '
            f'calcMode="spline" keyTimes="{times}" keySplines="{splines}" values="{values}"{extra}/>')


# ---------------------------------------------------------------------------- neon

def neon(x, y, s, size, color, length, cls="", weight=800, family=SANS, core=True):
    """Tube lettering: an unlit tube that is always there, plus a lit layer that can flicker."""
    base = (f'x="{f(x)}" y="{f(y)}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'textLength="{f(length)}" lengthAdjust="spacingAndGlyphs"')
    t = esc(s)
    lit = (f'<text {base} fill="{color}" fill-opacity=".14" stroke="{color}" stroke-width="6" '
           f'filter="url(#glow)" opacity=".85">{t}</text>'
           f'<text {base} fill="none" stroke="{color}" stroke-width="2.4" stroke-linejoin="round">{t}</text>')
    if core:
        lit += (f'<text {base} fill="none" stroke="#FFFFFF" stroke-width=".8" stroke-opacity=".7" '
                f'stroke-linejoin="round">{t}</text>')
    return (f'<text {base} fill="none" stroke="{DEAD_TUBE}" stroke-width="3">{t}</text>'
            f'<g class="{cls}">{lit}</g>')


def tube_line(x1, y1, x2, y2, color, cls=""):
    return (f'<g class="{cls}"><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="7" '
            f'stroke-linecap="round" filter="url(#glow)" opacity=".8"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFF" stroke-width=".8" stroke-opacity=".7" '
            f'stroke-linecap="round"/></g>')


# ---------------------------------------------------------------------------- scenery

def defs():
    return f"""
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{SKY_TOP}"/><stop offset="1" stop-color="{SKY_LOW}"/>
  </linearGradient>
  <radialGradient id="haze" cx=".62" cy="1" r=".7">
    <stop offset="0" stop-color="{PINK}" stop-opacity=".22"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="street" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0D1019"/><stop offset="1" stop-color="#05060A"/>
  </linearGradient>
  <linearGradient id="stallGlow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{AMBER}" stop-opacity=".26"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="doorSpill" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GOLD}" stop-opacity=".38"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="brick" width="44" height="22" patternUnits="userSpaceOnUse">
    <path d="M0 21.5H44M22 0V11M0 10.5H44M0 11V22M44 11V22" stroke="{WALL_LINE}" stroke-width="1" fill="none"/>
  </pattern>
  <filter id="glow" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>"""


def skyline():
    rnd = random.Random(11)
    out = ['<rect width="1200" height="440" fill="url(#sky)"/>', '<rect width="1200" height="440" fill="url(#haze)"/>']
    for layer, (shade, lo, hi, win_op) in enumerate([("#0A0C16", 150, 300, .35), ("#0E1120", 90, 220, .55)]):
        x = -10 if layer == 0 else 4
        while x < W:
            w = rnd.randint(44, 96)
            h = rnd.randint(lo, hi)
            top = FLOOR - h
            out.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{shade}"/>')
            for wy in range(top + 12, FLOOR - 10, 14):
                for wx in range(x + 7, x + w - 7, 11):
                    if rnd.random() < 0.18:
                        c = rnd.choice([AMBER, CYAN, CYAN, GOLD, PINK])
                        blink = ' class="blink"' if rnd.random() < 0.12 else ""
                        delay = f' style="animation-delay:-{rnd.uniform(0, 7):.1f}s"' if blink else ""
                        out.append(f'<rect{blink}{delay} x="{wx}" y="{wy}" width="4" height="6" fill="{c}" '
                                   f'opacity="{win_op * rnd.uniform(.4, 1):.2f}"/>')
            x += w + rnd.randint(2, 10)
    # A far billboard between the wall and the stall, plus a blinking aircraft light.
    out.append(f'<rect x="508" y="38" width="64" height="40" rx="3" fill="#0B0E18" stroke="#1C2234"/>'
               f'<text x="540" y="64" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" '
               f'fill="{CYAN}" opacity=".55" class="billboard">24/7</text>'
               f'<circle class="beacon" cx="1150" cy="40" r="2.5" fill="{RED}"/>')
    return "\n".join(out)


def wall():
    return f"""
<g>
  <rect x="0" y="0" width="470" height="{FLOOR}" fill="{WALL}"/>
  <rect x="0" y="0" width="470" height="{FLOOR}" fill="url(#brick)" opacity=".9"/>
  <rect x="462" y="0" width="8" height="{FLOOR}" fill="#070910"/>
  <!-- conduit feeding the sign -->
  <path d="M418 0 V44 Q418 54 408 54 H392" fill="none" stroke="#1B2131" stroke-width="5" stroke-linecap="round"/>
  {''.join(f'<rect x="{cx}" y="{cy}" width="10" height="4" rx="1.5" fill="#262E42"/>' for cx, cy in [(60, 70), (230, 70), (380, 70), (60, 205), (250, 205), (400, 205)])}
  {neon(46, 128, "Nitish", 74, AMBER, 232, cls="name-a")}
  {neon(46, 200, "Sundarraj", 74, CYAN, 382, cls="name-b")}
  {tube_line(52, 226, 268, 226, PINK, cls="underline")}
  <text x="50" y="258" font-family="{MONO}" font-size="14.5" fill="{MUTED}">power · silicon · robots · cloud</text>
  <text x="50" y="280" font-family="{MONO}" font-size="14.5" fill="{MUTED}">systems developer, mostly awake</text>

  <!-- door into the portfolio, left ajar -->
  <rect x="372" y="294" width="80" height="78" fill="#070910"/>
  <rect x="376" y="298" width="72" height="74" fill="{GOLD}" opacity=".5" class="doorlight"/>
  <path d="M384 298 H448 V372 H384 Z" fill="#121726"/>
  <circle cx="392" cy="338" r="2.6" fill="{GOLD}"/>
  <rect x="372" y="294" width="80" height="78" fill="none" stroke="{CYAN}" stroke-width="2" opacity=".75"/>
  <rect x="372" y="294" width="80" height="78" fill="none" stroke="{CYAN}" stroke-width="6" opacity=".35" filter="url(#glow)"/>
  <text x="412" y="286" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{CYAN}">portfolio →</text>
</g>"""


def stall_sign():
    return f"""
<g>
  <line x1="690" y1="140" x2="690" y2="152" stroke="#1E2536" stroke-width="3"/>
  <line x1="1020" y1="140" x2="1020" y2="152" stroke="#1E2536" stroke-width="3"/>
  <rect x="640" y="72" width="430" height="68" rx="6" fill="#090B12" stroke="#222A3B" stroke-width="1.5"/>
  {neon(664, 123, "BUG", 42, PINK, 82, cls="")}
  {neon(752, 123, "-FREE", 42, GREEN, 132, cls="free")}
  {neon(902, 123, "RAMEN", 42, GOLD, 146, cls="ramen")}
</g>"""


def cat():
    """A cat sitting on top of the sign, tail hanging over the edge."""
    return f"""
<g transform="translate(1040 72)">
  <g class="tail"><path d="M10 -4 C22 -2 22 18 16 30 C13 36 16 40 20 40" fill="none" stroke="#04050A" stroke-width="4.5" stroke-linecap="round"/></g>
  <g stroke="{PINK}" stroke-width="1.2" stroke-opacity=".55" stroke-linejoin="round">
  <path d="M-12 0 C-14 -18 -8 -26 0 -27 C8 -26 14 -18 12 0 Z" fill="#04050A"/>
    <circle cx="0" cy="-30" r="9" fill="#04050A"/>
    <path d="M-8 -34 L-7 -44 L-2 -37 Z M8 -34 L7 -44 L2 -37 Z" fill="#04050A"/>
  </g>
  <g class="cateyes"><ellipse cx="-3.4" cy="-31" rx="1.7" ry="2.1" fill="{GOLD}"/><ellipse cx="3.4" cy="-31" rx="1.7" ry="2.1" fill="{GOLD}"/></g>
</g>"""


def stall():
    bulbs = "".join(
        f'<line x1="{x}" y1="196" x2="{x}" y2="206" stroke="#2A3246" stroke-width="1.5"/>'
        f'<circle cx="{x}" cy="211" r="10" fill="{AMBER}" opacity=".35" filter="url(#glow)"/>'
        f'<circle cx="{x}" cy="211" r="4.5" fill="#FFD9A8"/>' for x in (676, 1004))
    stripes = "".join(
        f'<rect x="{606 + i * 42}" y="150" width="42" height="38" fill="{"#2A1033" if i % 2 == 0 else "#10131F"}"/>'
        for i in range(12))
    scallops = "".join(
        f'<path d="M{606 + i * 42} 187 a21 9 0 0 0 42 0 Z" fill="{"#2A1033" if i % 2 == 0 else "#10131F"}"/>'
        for i in range(12))
    menu = [("2N power broth", AMBER), ("UVM udon · 0 bugs", GREEN), ("formal pho · proven", CYAN),
            ("CAN-bus noodles", PINK)]
    menu_rows = "".join(
        f'<circle cx="932" cy="{238 + i * 16 - 4}" r="2" fill="{c}"/>'
        f'<text x="940" y="{238 + i * 16}" font-family="{MONO}" font-size="12" fill="#D4DAE6">{esc(s)}</text>'
        for i, (s, c) in enumerate(menu))
    return f"""
<g>
  <!-- back wall with warm light under the awning -->
  <rect x="618" y="186" width="484" height="112" fill="#0C0F18"/>
  <rect x="618" y="186" width="484" height="112" fill="url(#stallGlow)"/>
  <rect x="920" y="206" width="166" height="88" rx="5" fill="#070910" stroke="#2A3246"/>
  <text x="932" y="221" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{MUTED}" letter-spacing="1.5">TONIGHT</text>
  {menu_rows}
  {robot()}
  <!-- posts -->
  <rect x="612" y="150" width="9" height="{FLOOR - 150}" fill="#171C2A"/>
  <rect x="1099" y="150" width="9" height="{FLOOR - 150}" fill="#171C2A"/>
  <!-- awning -->
  {stripes}{scallops}
  <rect x="606" y="148" width="504" height="4" fill="#3A1846"/>
  {bulbs}
  <!-- counter -->
  <rect x="604" y="294" width="512" height="10" rx="2" fill="#252D40"/>
  <line x1="606" y1="305" x2="1114" y2="305" stroke="{CYAN}" stroke-width="5" opacity=".45" filter="url(#glow)"/>
  <line x1="606" y1="305" x2="1114" y2="305" stroke="{CYAN}" stroke-width="1.6"/>
  <rect x="612" y="306" width="496" height="{FLOOR - 306}" fill="#121725"/>
  {''.join(f'<line x1="{x}" y1="310" x2="{x}" y2="{FLOOR}" stroke="#0C1019" stroke-width="2"/>' for x in range(652, 1108, 40))}
  <text x="860" y="346" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{GOLD}" opacity=".8">open till the tests pass</text>
  {pot()}
  {jar()}
</g>"""


def pot():
    steam = "".join(
        f'<path class="steam" style="animation-delay:-{d}s" d="M{x} 262 c-6 -8 6 -14 0 -22 c-5 -7 5 -12 0 -18" '
        f'fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity="0"/>'
        for x, d in ((728, 0), (744, 0.9), (760, 1.7)))
    return f"""
<g>
  {steam}
  <rect x="712" y="266" width="64" height="30" rx="5" fill="#2B3448"/>
  <rect x="712" y="266" width="64" height="7" fill="#3A4560"/>
  <rect x="706" y="270" width="8" height="5" rx="2" fill="#3A4560"/>
  <rect x="774" y="270" width="8" height="5" rx="2" fill="#3A4560"/>
</g>"""


def jar():
    rnd = random.Random(3)
    dots = "".join(
        f'<circle cx="{644 + rnd.uniform(0, 22):.1f}" cy="{288 + rnd.uniform(-5, 4):.1f}" r="1.9" fill="{GREEN}" opacity=".9"/>'
        for _ in range(14))
    return f"""
<g>
  <rect x="640" y="258" width="32" height="38" rx="6" fill="{CYAN}" fill-opacity=".07" stroke="#5B6B86" stroke-width="1.5"/>
  <rect x="638" y="255" width="36" height="5" rx="2" fill="#3A4458"/>
  {dots}
  <rect x="643" y="266" width="26" height="13" rx="2" fill="#E8EDF7"/>
  <text class="n14" x="656" y="276.5" text-anchor="middle" font-family="{MONO}" font-size="10.5" font-weight="700" fill="#10131F">14</text>
  <text class="n15" x="656" y="276.5" text-anchor="middle" font-family="{MONO}" font-size="10.5" font-weight="700" fill="#10131F" opacity="0">15</text>
  <text x="656" y="250" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="{MUTED}">bugs</text>
</g>"""


def robot():
    return f"""
<g class="robot">
  <!-- stirring arm and ladle -->
  <g class="stir">
    <path d="M808 284 Q790 272 772 268" fill="none" stroke="#2C354A" stroke-width="8" stroke-linecap="round"/>
    <circle cx="772" cy="268" r="5" fill="#3A4560"/>
    <line x1="772" y1="268" x2="748" y2="282" stroke="#8C97AD" stroke-width="3" stroke-linecap="round"/>
  </g>
  <path d="M872 284 Q888 276 892 262" fill="none" stroke="#2C354A" stroke-width="8" stroke-linecap="round"/>
  <circle cx="892" cy="260" r="5" fill="#3A4560"/>
  <!-- body + apron -->
  <rect x="804" y="274" width="72" height="26" rx="9" fill="#1B2234" stroke="#2C354A"/>
  <rect x="822" y="278" width="36" height="22" rx="3" fill="#E8EDF7" opacity=".92"/>
  <rect x="834" y="264" width="12" height="12" fill="#2C354A"/>
  <!-- head -->
  <rect x="800" y="226" width="80" height="42" rx="13" fill="#232C40" stroke="#36425C"/>
  <rect x="808" y="232" width="64" height="30" rx="9" fill="#04060B"/>
  <g class="r-calm"><g class="r-blink">
    <rect x="822" y="240" width="11" height="14" rx="4" fill="{CYAN}"/>
    <rect x="847" y="240" width="11" height="14" rx="4" fill="{CYAN}"/>
  </g></g>
  <g class="r-alarm" opacity="0">
    <text x="840" y="253" text-anchor="middle" font-family="{MONO}" font-size="13.5" font-weight="800" fill="{RED}">BUG?!</text>
  </g>
  <g class="r-happy" opacity="0">
    <path d="M821 251 Q827.5 240 834 251 M846 251 Q852.5 240 859 251" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>
  </g>
  <!-- chef hat -->
  <rect x="814" y="212" width="52" height="15" rx="3" fill="#EEF1F7"/>
  <circle cx="824" cy="206" r="11" fill="#EEF1F7"/>
  <circle cx="840" cy="201" r="13" fill="#EEF1F7"/>
  <circle cx="856" cy="206" r="11" fill="#EEF1F7"/>
  <line x1="826" y1="216" x2="826" y2="226" stroke="#C9CFDB" stroke-width="1.2"/>
  <line x1="854" y1="216" x2="854" y2="226" stroke="#C9CFDB" stroke-width="1.2"/>
</g>"""


# ---------------------------------------------------------------------------- Nitish

# Chopstick-hand poses in his local frame: (hand x, hand y, stick angle, elbow control x, y)
DOWN = (-6, -128, 40, -44, -98)
MOUTH = (-22, -150, -34, -50, -112)
LOOK = (6, -146, -40, -46, -108)
SHOULDER = (-30, -124)
STICK = 40

POSES = [(0, DOWN), (0.8, DOWN), (1.4, MOUTH), (1.9, MOUTH), (2.5, DOWN), (3.2, DOWN), (3.8, MOUTH),
         (4.2, MOUTH), (4.8, DOWN), (5.0, DOWN), (5.6, LOOK), (7.0, LOOK), (7.5, DOWN), (8.6, DOWN),
         (9.2, MOUTH), (9.7, MOUTH), (10.3, DOWN), (CYCLE, DOWN)]

NX, NY = 540, FLOOR


def tip(pose):
    hx, hy, a, _, _ = pose
    return hx + STICK * math.cos(math.radians(a)), hy + STICK * math.sin(math.radians(a))


def arm_d(pose):
    hx, hy, _, cx, cy = pose
    return f"M{SHOULDER[0]} {SHOULDER[1]} Q{cx} {cy} {hx} {hy}"


def bug(cls=""):
    return f"""
<g class="{cls}">
  <circle r="9" fill="{GREEN}" opacity=".45" filter="url(#glow)"/>
  <path d="M-4 -2 L-9 -6 M-4 1 L-10 1 M-4 4 L-9 8 M4 -2 L9 -6 M4 1 L10 1 M4 4 L9 8" stroke="#0A2A1F" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M-2 -6 Q-5 -12 -8 -12 M2 -6 Q5 -12 8 -12" fill="none" stroke="#0A2A1F" stroke-width="1.4" stroke-linecap="round"/>
  <ellipse cx="0" cy="1" rx="6" ry="7" fill="{GREEN}"/>
  <line x1="0" y1="-3" x2="0" y2="8" stroke="#0A2A1F" stroke-width="1.2"/>
  <circle cx="0" cy="-5" r="3.6" fill="#0A2A1F"/>
  <circle cx="-1.3" cy="-5.6" r="1" fill="#FFF"/><circle cx="1.3" cy="-5.6" r="1" fill="#FFF"/>
</g>"""


def nitish():
    hand_xy = [(t, f"{p[0]} {p[1]}") for t, p in POSES]
    hand_rot = [(t, f"{p[2]}") for t, p in POSES]
    arm = [(t, arm_d(p)) for t, p in POSES]
    d0 = POSES[0][1]
    return f"""
<g transform="translate({NX} {NY})">
  <ellipse cx="0" cy="4" rx="48" ry="8" fill="#000" opacity=".55"/>
  <!-- legs -->
  <rect x="-22" y="-58" width="17" height="50" rx="8" fill="#181D2B"/>
  <rect x="6" y="-58" width="17" height="50" rx="8" fill="#181D2B"/>
  <path d="M-26 -10h22c4 0 6 3 6 7v4h-30v-5c0-3 1-6 2-6z" fill="#2A3244"/>
  <path d="M4 -10h24c4 0 6 3 6 7v4h-30v-11z" fill="#2A3244"/>
  <line x1="-26" y1="0" x2="2" y2="0" stroke="{PINK}" stroke-width="2.4" stroke-linecap="round"/>
  <line x1="4" y1="0" x2="32" y2="0" stroke="{PINK}" stroke-width="2.4" stroke-linecap="round"/>
  <g class="bob">
    <!-- hoodie -->
    <path d="M-34 -126 C-34 -138 -20 -144 0 -144 C20 -144 34 -138 34 -126 L30 -54 C30 -48 24 -45 18 -45 L-18 -45 C-24 -45 -30 -48 -30 -54 Z"
          fill="{HOODIE}" stroke="#2C354A" stroke-width="1.2"/>
    <path d="M-13 -143 Q0 -130 13 -143" fill="#ECEBE6"/>
    <path d="M-8 -134 L-9 -112 M8 -134 L9 -114" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" opacity=".7"/>
    <path d="M-20 -78 L20 -78 L24 -54 L-24 -54 Z" fill="#171C29" stroke="#283145" stroke-width="1"/>
    <!-- neck + head -->
    <rect x="-9" y="-156" width="18" height="18" rx="7" fill="{SKIN_DK}"/>
    <g transform="translate(0 -184)">
      <circle cx="-30" cy="4" r="7.5" fill="{SKIN_DK}"/>
      <circle cx="30" cy="4" r="7.5" fill="{SKIN}"/>
      <rect x="-30" y="-30" width="60" height="64" rx="28" fill="{SKIN}"/>
      <ellipse cx="6" cy="-6" rx="18" ry="14" fill="{SKIN_LT}" opacity=".35"/>
      <path d="M-32 -3 C-35 -24 -24 -40 -6 -43 C6 -45 20 -42 28 -30 C35 -20 35 -10 32 -3 C27 -15 16 -21 2 -21 C-14 -21 -25 -15 -32 -3 Z" fill="{HAIR}"/>
      <path d="M-22 -28 C-8 -39 13 -39 24 -25" fill="none" stroke="{HAIR_HI}" stroke-width="4" stroke-linecap="round" opacity=".6"/>
      <path d="M-22 14 C-18 32 18 32 22 14 C16 26 -16 26 -22 14 Z" fill="{HAIR}" opacity=".22"/>
      <!-- headphones round the neck, because of course -->
      <path d="M-27 22 Q0 44 27 22" fill="none" stroke="#2A3244" stroke-width="5" stroke-linecap="round"/>
      <ellipse cx="-9" cy="1" rx="5.2" ry="5.6" fill="#FFF"/>
      <ellipse cx="12" cy="1" rx="5.2" ry="5.6" fill="#FFF"/>
      <!-- eating: eyes on the bowl -->
      <g class="f-calm">
        <circle cx="-8" cy="3" r="2.7" fill="{HAIR}"/><circle cx="13" cy="3" r="2.7" fill="{HAIR}"/>
        <path d="M-16 -9 Q-9 -11 -3 -9 M6 -9 Q13 -11 19 -9" fill="none" stroke="{HAIR}" stroke-width="2.4" stroke-linecap="round"/>
        <path d="M-4 15 Q3 19 10 15" fill="none" stroke="#4A1915" stroke-width="2.4" stroke-linecap="round"/>
      </g>
      <!-- the bug shows up -->
      <g class="f-shock" opacity="0">
        <circle cx="-6.5" cy="0" r="2.2" fill="{HAIR}"/><circle cx="14.5" cy="0" r="2.2" fill="{HAIR}"/>
        <path d="M-16 -14 Q-9 -18 -3 -14 M6 -14 Q13 -18 20 -14" fill="none" stroke="{HAIR}" stroke-width="2.4" stroke-linecap="round"/>
        <ellipse cx="3" cy="16" rx="4" ry="5" fill="#4A1915"/>
      </g>
      <!-- logged it -->
      <g class="f-smug" opacity="0">
        <circle cx="-6.5" cy="1.5" r="2.7" fill="{HAIR}"/><circle cx="14.5" cy="1.5" r="2.7" fill="{HAIR}"/>
        <path d="M-16 -8 L-3 -8" stroke="{HAIR}" stroke-width="2.6" stroke-linecap="round"/>
        <path d="M6 -12 Q13 -17 20 -11" fill="none" stroke="{HAIR}" stroke-width="2.6" stroke-linecap="round"/>
        <path d="M-5 16 Q5 18 13 12" fill="none" stroke="#4A1915" stroke-width="2.4" stroke-linecap="round"/>
      </g>
    </g>
    <!-- bowl arm -->
    <path d="M30 -124 C46 -112 48 -98 36 -92" fill="none" stroke="{SLEEVE}" stroke-width="16" stroke-linecap="round"/>
    <circle cx="34" cy="-90" r="8.5" fill="{SKIN}"/>
    <!-- bowl -->
    <path d="M-2 -102 H46 C46 -88 36 -80 22 -80 C8 -80 -2 -88 -2 -102 Z" fill="#EEF1F7"/>
    <path d="M0 -95 H44" stroke="{PINK}" stroke-width="3"/>
    <ellipse cx="22" cy="-102" rx="24" ry="5" fill="#5A2E16"/>
    <path d="M4 -103 q4 -3 8 0 t8 0 t8 0 t8 0 t6 0" fill="none" stroke="#F5D27A" stroke-width="2.2" stroke-linecap="round"/>
    <circle cx="34" cy="-104" r="4" fill="#FFF7E6"/><circle cx="34" cy="-104" r="2" fill="{GOLD}"/>
    <path class="steam" style="animation-delay:-.6s" d="M14 -110 c-4 -6 4 -10 0 -16" fill="none" stroke="#FFF" stroke-width="1.6" stroke-linecap="round" opacity="0"/>
    <!-- chopstick arm -->
    <path d="{arm_d(d0)}" fill="none" stroke="{SLEEVE}" stroke-width="16" stroke-linecap="round">{smil("d", arm)}</path>
    <g transform="translate({d0[0]} {d0[1]})">
      {smil("transform", hand_xy, kind="translate")}
      <g transform="rotate({d0[2]})">
        {smil("transform", hand_rot, kind="rotate")}
        <line x1="-12" y1="-3" x2="{STICK}" y2="-1" stroke="#C98A4B" stroke-width="2.6" stroke-linecap="round"/>
        <line x1="-12" y1="3" x2="{STICK}" y2="1" stroke="#B37638" stroke-width="2.6" stroke-linecap="round"/>
        <g transform="translate({STICK} 0) rotate(90)">{bug("tipbug")}</g>
        <circle cx="0" cy="0" r="8.5" fill="{SKIN}"/>
      </g>
    </g>
  </g>
</g>"""


def flying_bug():
    sx, sy = tip(LOOK)
    start = f"{f(NX + sx)} {f(NY + sy)}"
    frames = [(0, start), (7.0, start), (7.3, "620 180"), (7.6, "656 252"), (7.9, "656 286"), (CYCLE, "656 286")]
    return f"""
<g transform="translate({start})">{smil("transform", frames, kind="translate")}
  <g transform="scale(.8)">{bug("flybug")}</g>
</g>"""


def bubble(cx, cy, w, s, tail_x, cls):
    return f"""
<g class="{cls}" opacity="0">
  <rect x="{f(cx - w / 2)}" y="{cy - 18}" width="{w}" height="36" rx="18" fill="#11141F" stroke="{GREEN}" stroke-width="1.6"/>
  <path d="M{tail_x - 7} {cy + 17} L{tail_x - 2} {cy + 28} L{tail_x + 7} {cy + 17}" fill="#11141F" stroke="{GREEN}" stroke-width="1.6" stroke-linejoin="round"/>
  <line x1="{tail_x - 6}" y1="{cy + 17}" x2="{tail_x + 6}" y2="{cy + 17}" stroke="#11141F" stroke-width="3"/>
  <text x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="{INK}">{esc(s)}</text>
</g>"""


# ---------------------------------------------------------------------------- weather + street

def street():
    streaks = [(690, PINK, ""), (818, GREEN, "free"), (975, GOLD, "ramen"), (676, AMBER, ""), (1004, AMBER, ""),
               (130, AMBER, "name-a"), (260, CYAN, "name-b"), (412, GOLD, "doorlight"), (860, CYAN, "")]
    refl = "".join(
        f'<g class="{c}"><rect class="shimmer" style="animation-delay:-{i * .37:.2f}s" x="{x - 26}" y="378" width="52" '
        f'height="58" fill="{col}" opacity=".2" filter="url(#soft)"/></g>'
        for i, (x, col, c) in enumerate(streaks))
    ripples = "".join(
        f'<ellipse class="ripple" style="animation-delay:-{d}s" cx="{x}" cy="{y}" rx="14" ry="3" fill="none" '
        f'stroke="#9FB6D9" stroke-width="1" opacity="0"/>'
        for x, y, d in ((96, 412, 0), (300, 398, .5), (520, 424, 1.1), (742, 404, .3), (930, 420, .8),
                        (1140, 400, 1.4), (420, 432, 1.7)))
    return f"""
<rect x="0" y="{FLOOR}" width="1200" height="{H - FLOOR}" fill="url(#street)"/>
<rect x="0" y="{FLOOR}" width="1200" height="2" fill="#1D2334"/>
<path d="M372 {FLOOR} H452 L500 440 H330 Z" fill="url(#doorSpill)"/>
{refl}
{ripples}"""


def rain():
    rnd = random.Random(5)
    out = []
    for name, n, op in (("rainA", 46, .22), ("rainB", 34, .34)):
        lines = []
        for _ in range(n):
            x, y, ln = rnd.uniform(0, W + 60), rnd.uniform(0, H), rnd.uniform(10, 20)
            for dy in (0, -H):
                lines.append(f'<line x1="{x:.0f}" y1="{y + dy:.0f}" x2="{x - ln * .28:.0f}" y2="{y + dy + ln:.0f}"/>')
        out.append(f'<g class="{name}" stroke="#A9C7F0" stroke-width="1.1" stroke-linecap="round" opacity="{op}">'
                   + "".join(lines) + "</g>")
    return "\n".join(out)


# ---------------------------------------------------------------------------- assembly

def build():
    jitter = [(0, "transform:translate(0,0)"), (4.6, "transform:translate(0,0)")]
    t, s = 4.7, 1
    while t < 7.8:
        jitter.append((round(t, 2), f"transform:translate({1.6 * s}px,{-.8 * (s > 0)}px)"))
        t, s = t + 0.1, -s
    jitter += [(7.85, "transform:translate(0,0)"), (CYCLE, "transform:translate(0,0)")]

    free = [(0, "opacity:1"), (3.9, "opacity:1"), (3.95, "opacity:.1"), (4.05, "opacity:1"), (4.15, "opacity:.2"),
            (4.3, "opacity:.9"), (4.36, "opacity:0"), (7.9, "opacity:0"), (7.95, "opacity:.8"), (8.05, "opacity:.1"),
            (8.2, "opacity:1"), (8.26, "opacity:.3"), (8.4, "opacity:1"), (CYCLE, "opacity:1")]

    css = "\n".join([
        kf("free", free), f".free{{{run('free')}}}",
        kf("rjit", jitter), f".robot{{{run('rjit')}}}",
        hidden("rcalm", [(4.6, 7.8), (8.4, 10.4)]), f".r-calm{{{run('rcalm')}}}",
        shown("ralarm", [(4.6, 7.8)]), f".r-alarm{{{run('ralarm')}}}",
        shown("rhappy", [(8.4, 10.4)]), f".r-happy{{{run('rhappy')}}}",
        hidden("fcalm", [(5.5, 8.4)]), f".f-calm{{{run('fcalm')}}}",
        shown("fshock", [(5.5, 6.3)]), f".f-shock{{{run('fshock')}}}",
        shown("fsmug", [(6.3, 8.4)]), f".f-smug{{{run('fsmug')}}}",
        shown("tipbug", [(4.9, 7.0)], ramp=0.05), f".tipbug{{{run('tipbug')}}}",
        shown("flybug", [(7.0, CYCLE - .2)], ramp=0.02), f".flybug{{{run('flybug')}}}",
        hidden("n14", [(7.9, CYCLE - .2)], ramp=0.05), f".n14{{{run('n14')}}}",
        shown("n15", [(7.9, CYCLE - .2)], ramp=0.05), f".n15{{{run('n15')}}}",
        shown("say", [(6.3, 9.4)], ramp=0.15), f".say{{{run('say')}}}",
        # ambient loops
        "@keyframes blinkR{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}",
        ".r-blink{animation:blinkR 3.7s infinite;transform-box:fill-box;transform-origin:center}",
        "@keyframes stir{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(6deg)}}",
        ".stir{animation:stir 1.6s ease-in-out infinite;transform-box:view-box;transform-origin:808px 284px}",
        "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}",
        ".bob{animation:bob 3s ease-in-out infinite}",
        "@keyframes steam{0%{transform:translateY(4px);opacity:0}30%{opacity:.4}100%{transform:translateY(-14px);opacity:0}}",
        ".steam{animation:steam 2.6s ease-out infinite}",
        "@keyframes tail{0%,100%{transform:rotate(0)}50%{transform:rotate(9deg)}}",
        ".tail{animation:tail 3.4s ease-in-out infinite;transform-box:view-box;transform-origin:1050px 68px}",
        "@keyframes cateyes{0%,46%,50%,100%{transform:scaleY(1)}48%{transform:scaleY(.1)}}",
        ".cateyes{animation:cateyes 5.2s infinite;transform-box:fill-box;transform-origin:center}",
        "@keyframes rain{to{transform:translate(-120px,440px)}}",
        ".rainA{animation:rain 1.5s linear infinite}.rainB{animation:rain .95s linear infinite}",
        "@keyframes ripple{0%{transform:scale(.2);opacity:0}15%{opacity:.6}100%{transform:scale(1.4);opacity:0}}",
        ".ripple{animation:ripple 2s ease-out infinite;transform-box:fill-box;transform-origin:center}",
        "@keyframes shimmer{0%,100%{transform:scaleX(1)}50%{transform:scaleX(1.25)}}",
        ".shimmer{animation:shimmer 2.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}",
        "@keyframes blink{0%,60%{fill-opacity:1}61%,78%{fill-opacity:0}}",
        ".blink{animation:blink 6s steps(1) infinite}",
        "@keyframes beacon{0%,100%{opacity:.15}50%{opacity:1}}.beacon{animation:beacon 1.8s infinite}",
        "@keyframes hum{0%,96%,100%{opacity:1}97%{opacity:.35}98%{opacity:1}99%{opacity:.6}}",
        ".underline{animation:hum 5.5s infinite}.name-b{animation:hum 9s -3s infinite}",
        "@keyframes door{0%,100%{opacity:.45}50%{opacity:.62}}.doorlight{animation:door 4s ease-in-out infinite}",
        "@media (prefers-reduced-motion: reduce){*{animation:none!important}}",
    ])

    body = "\n".join([
        defs(),
        skyline(),
        wall(),
        stall_sign(),
        cat(),
        stall(),
        street(),
        nitish(),
        flying_bug(),
        bubble(560, 112, 160, "that's bug #15.", 556, "say"),
        rain(),
    ])
    svg = doc(
        W, H,
        "Nitish Sundarraj: power, silicon, robots, cloud",
        css, body,
        desc=("A rainy neon street at night. Nitish's name glows on a brick wall next to a door marked portfolio. "
              "He eats noodles beside a stall whose sign reads BUG-FREE RAMEN, run by a robot in a chef hat. "
              "The FREE tube flickers out, a bug climbs onto his chopsticks, he drops it into a jar that goes "
              "from 14 to 15 bugs, says that's bug #15, and the sign lights up again."),
    )
    return svg
