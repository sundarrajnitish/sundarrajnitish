"""Header: ground to orbit in one 14 s loop, for the GitHub README.

Left: a lights-out factory where a robot arm builds rocket upper stages.
Middle: a driverless truck hauls the stage along the service road while Nitish rides
past in a self-driving convertible (empty driver seat, steering wheel turning itself).
Right: a reusable booster on its pad, launch tower and countdown board.

The loop:
  0.0-2.0   The arm picks an upper stage off the conveyor and sets it on the truck.
  3.0-6.4   The truck drives itself to the pad.
  6.6-7.4   The stage is stacked on top of the booster that landed last loop.
  8.0-9.0   T-3, T-2, T-1. Liftoff at 9.0.
 11.0-13.2  The booster comes back down, legs out, and sticks the landing.
 13.2-1.6   Nitish raises his coffee: "stuck it."

GitHub shows README images through <img>, so this is one self-contained SVG: CSS
keyframes and SMIL only, no script, no web fonts. CSS and SMIL share one clock.
"""

import math
import random

from svgkit import MONO, SANS, doc, esc, f

W, H = 1200, 440
GROUND = 330
CYCLE = 14.0

INK = "#F4F6FB"
MUTED = "#9EA7B8"
AMBER = "#FF9442"
GOLD = "#FFB020"
CYAN = "#38BDF8"
PINK = "#FF4F9A"
GREEN = "#34D399"
VIOLET = "#A78BFA"
RED = "#FF5454"
STEEL = "#232C40"
STEEL_HI = "#36425C"

SKIN = "#A96F51"
SKIN_DK = "#86533B"
SKIN_LT = "#BF8766"
HAIR = "#15100E"
HAIR_HI = "#362822"
HOODIE = "#1D2333"

EASE = ".42 0 .58 1"
EASE_IN = ".55 0 1 .6"
EASE_OUT = "0 .4 .3 1"


# ---------------------------------------------------------------------------- timing helpers

def pct(sec):
    return f"{f(sec / CYCLE * 100)}%"


def kf(name, stops):
    return f"@keyframes {name}{{" + "".join(f"{pct(t)}{{{p}}}" for t, p in stops) + "}"


def run(name, easing="linear"):
    return f"animation:{name} {f(CYCLE)}s {easing} infinite"


def toggle(name, spans, ramp=0.08, invert=False):
    """Opacity keyframes: on inside each (start, end) span. Spans may touch 0 or CYCLE."""
    def on(t):
        return any((a + ramp <= t <= b) or (a == 0 and t <= b) for a, b in spans)

    pts = {0.0, CYCLE}
    for a, b in spans:
        pts |= {x for x in (a, a + ramp, b, b + ramp) if 0 <= x <= CYCLE}
    stops = [(t, f"opacity:{int(on(t) != invert)}") for t in sorted(pts)]
    return kf(name, stops) + f".{name}{{{run(name)}}}"


def smil(attr, frames, kind="animate", splines=None):
    """SMIL animation on the shared clock. frames: [(t, value[, spline into this frame])]."""
    times = ";".join(f"{fr[0] / CYCLE:.4f}" for fr in frames)
    values = ";".join(fr[1] for fr in frames)
    sp = ";".join((fr[2] if len(fr) > 2 else EASE) for fr in frames[1:])
    tag = "animate" if kind == "animate" else "animateTransform"
    typ = "" if kind == "animate" else f' type="{kind}"'
    return (f'<{tag} attributeName="{attr}"{typ} dur="{f(CYCLE)}s" repeatCount="indefinite" '
            f'calcMode="spline" keyTimes="{times}" keySplines="{sp}" values="{values}"/>')


# ---------------------------------------------------------------------------- sky

def defs():
    return f"""
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#020308"/><stop offset=".6" stop-color="#090A1A"/><stop offset="1" stop-color="#1A0E2A"/>
  </linearGradient>
  <radialGradient id="haze" cx=".5" cy="1" r=".6">
    <stop offset="0" stop-color="{PINK}" stop-opacity=".18"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="road" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0C0F18"/><stop offset="1" stop-color="#05060A"/>
  </linearGradient>
  <linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFF1C9" stop-opacity=".35"/><stop offset="1" stop-color="#FFF1C9" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="flame" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset=".3" stop-color="{GOLD}"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
  </linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>"""


def sky():
    rnd = random.Random(21)
    stars = []
    for _ in range(110):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 250)
        r = rnd.choice([.6, .8, .8, 1.1, 1.4])
        tw = f' class="tw" style="animation-delay:-{rnd.uniform(0, 4):.1f}s"' if rnd.random() < .3 else ""
        stars.append(f'<circle{tw} cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#DDE6FF" opacity="{rnd.uniform(.3, .9):.2f}"/>')
    orbit = "M60 150 A560 70 -6 0 1 1140 60"
    return f"""
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<rect width="{W}" height="{H}" fill="url(#haze)"/>
{''.join(stars)}
<!-- moon -->
<circle cx="560" cy="64" r="30" fill="{VIOLET}" opacity=".12" filter="url(#soft)"/>
<circle cx="560" cy="64" r="22" fill="#D9DDF0"/>
<circle cx="552" cy="58" r="4" fill="#B8BED6"/><circle cx="566" cy="72" r="3" fill="#B8BED6"/><circle cx="568" cy="55" r="2" fill="#B8BED6"/>
<!-- orbit with a satellite riding it -->
<path id="orbit" d="{orbit}" fill="none" stroke="{CYAN}" stroke-opacity=".22" stroke-width="1" stroke-dasharray="3 7"/>
<g>
  <animateMotion dur="{f(CYCLE)}s" repeatCount="indefinite" rotate="auto"><mpath href="#orbit"/></animateMotion>
  <rect x="-3" y="-3" width="6" height="6" fill="#C9D2E6"/>
  <rect x="-15" y="-2" width="10" height="4" fill="{CYAN}" opacity=".8"/><rect x="5" y="-2" width="10" height="4" fill="{CYAN}" opacity=".8"/>
  <circle class="beacon" r="1.5" cy="-5" fill="{RED}"/>
</g>"""


def skyline():
    rnd = random.Random(8)
    out = []
    x = 330
    while x < 900:
        w, h = rnd.randint(30, 64), rnd.randint(30, 110)
        top = GROUND - h
        out.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="#0E1120"/>')
        for wy in range(top + 8, GROUND - 6, 10):
            for wx in range(x + 5, x + w - 5, 8):
                if rnd.random() < .2:
                    c = rnd.choice([AMBER, CYAN, CYAN, PINK])
                    out.append(f'<rect x="{wx}" y="{wy}" width="3" height="4" fill="{c}" opacity="{rnd.uniform(.25, .6):.2f}"/>')
        x += w + rnd.randint(2, 8)
    return "\n".join(out)


# ---------------------------------------------------------------------------- factory + arm

SHOULDER = (210, 214)
L1, L2 = 62, 62
PICK = (112, 242)
PLACE = (300, 248)
REST = (180, 200)
ARM_KEYS = [(0, REST), (0.4, (112, 218)), (0.8, PICK), (1.15, (140, 214)), (1.7, (300, 224)), (2.0, PLACE),
            (2.35, (290, 222)), (2.9, REST), (CYCLE, REST)]


def ik(target):
    sx, sy = SHOULDER
    dx, dy = target[0] - sx, target[1] - sy
    d = min(math.hypot(dx, dy), L1 + L2 - 1e-3)
    phi = math.degrees(math.atan2(dx, -dy))
    alpha = math.degrees(math.acos((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)))

    def elbow(t1):
        return sx + L1 * math.sin(math.radians(t1)), sy - L1 * math.cos(math.radians(t1))

    t1 = min((phi + alpha, phi - alpha), key=lambda a: elbow(a)[1])  # elbow up
    ex, ey = elbow(t1)
    psi = math.degrees(math.atan2(target[0] - ex, -(target[1] - ey)))
    return t1, psi - t1, -psi


def stage(cls="", x=0, y=0):
    """A rocket upper stage, drawn hanging from its nose tip at (x, y)."""
    return f"""
<g class="{cls}" transform="translate({f(x)} {f(y)})">
  <path d="M0 0 C7 4 9 10 9 16 H-9 C-9 10 -7 4 0 0 Z" fill="#E8EDF7"/>
  <rect x="-9" y="16" width="18" height="30" fill="#D6DCE8"/>
  <rect x="-9" y="24" width="18" height="3" fill="{PINK}"/>
  <circle cx="0" cy="36" r="2.6" fill="{CYAN}"/>
  <path d="M-9 46 L-12 52 H12 L9 46 Z" fill="#3A4560"/>
</g>"""


def arm():
    sx, sy = SHOULDER
    poses = [(t, ik(p)) for t, p in ARM_KEYS]
    up = smil("transform", [(t, f"{a[0]:.1f} {sx} {sy}") for t, a in poses], kind="rotate")
    fore = smil("transform", [(t, f"{a[1]:.1f} {sx} {sy - L1}") for t, a in poses], kind="rotate")
    wrist = smil("transform", [(t, f"{a[2]:.1f} {sx} {sy - L1 - L2}") for t, a in poses], kind="rotate")
    a0 = poses[0][1]
    gx, gy = sx, sy - L1 - L2
    return f"""
<g>
  <rect x="198" y="{sy}" width="24" height="{GROUND - sy}" fill="#2A3246"/>
  <rect x="188" y="{GROUND - 10}" width="44" height="10" rx="2" fill="#323B52"/>
  <g transform="rotate({a0[0]:.1f} {sx} {sy})">{up}
    <rect x="{sx - 8}" y="{sy - L1}" width="16" height="{L1}" rx="8" fill="{AMBER}"/>
    <g transform="rotate({a0[1]:.1f} {sx} {sy - L1})">{fore}
      <rect x="{sx - 6}" y="{sy - L1 - L2}" width="12" height="{L2}" rx="6" fill="{GOLD}"/>
      <g transform="rotate({a0[2]:.1f} {gx} {gy})">{wrist}
        {stage("u2", gx, gy + 4)}
        <rect x="{gx - 9}" y="{gy - 3}" width="18" height="6" rx="2" fill="#3A4560"/>
        <path d="M{gx - 8} {gy + 3} v7 M{gx + 8} {gy + 3} v7" stroke="#8C97AD" stroke-width="2.4" stroke-linecap="round"/>
        <circle cx="{gx}" cy="{gy}" r="2" fill="{CYAN}"/>
      </g>
      <circle cx="{sx}" cy="{sy - L1}" r="8" fill="#1B2234" stroke="{STEEL_HI}"/>
    </g>
    <circle cx="{sx}" cy="{sy}" r="10" fill="#1B2234" stroke="{STEEL_HI}"/>
    <circle cx="{sx}" cy="{sy}" r="3" fill="{CYAN}" class="beacon"/>
  </g>
</g>"""


def factory():
    teeth = "".join(f"L{x} 150 L{x + 68} 178 " for x in range(20, 360, 68))
    glass = "".join(f'<path d="M{x} 150 L{x} 178 L{x + 6} 178 L{x + 6} 153 Z" fill="{CYAN}" opacity=".35"/>'
                    for x in range(88, 360, 68))
    belt = "".join(f'<line x1="{x}" y1="300" x2="{x + 5}" y2="300"/>' for x in range(0, 180, 12))
    rollers = "".join(f'<circle cx="{x}" cy="306" r="4" fill="#1B2234" stroke="{STEEL_HI}"/>' for x in range(40, 166, 18))
    return f"""
<g>
  <path d="M20 178 {teeth} L360 178 V{GROUND} H20 Z" fill="#0C0F18"/>
  <path d="M20 178 {teeth}" fill="none" stroke="#1E2536" stroke-width="2"/>
  {glass}
  <rect x="26" y="184" width="328" height="{GROUND - 184}" fill="#080A11"/>
  <!-- floor arrows for the AGVs nobody is here to read -->
  <path d="M60 326 h20 l-5 -3 m5 3 l-5 3 M250 326 h20 l-5 -3 m5 3 l-5 3" stroke="{GOLD}" stroke-opacity=".5" fill="none"/>
  <!-- conveyor -->
  <rect x="32" y="298" width="140" height="10" rx="5" fill="#1B2234"/>
  <g class="belt" stroke="{STEEL_HI}" stroke-width="2">{belt}</g>
  {rollers}
  <rect x="44" y="308" width="6" height="22" fill="#1B2234"/><rect x="154" y="308" width="6" height="22" fill="#1B2234"/>
  <g class="u1slide">{stage("u1", PICK[0], 246)}</g>
</g>"""


def factory_front():
    return f"""
<g>
  <rect x="20" y="176" width="10" height="{GROUND - 176}" fill="#121725"/>
  <rect x="350" y="176" width="10" height="{GROUND - 176}" fill="#121725"/>
  <rect x="20" y="176" width="340" height="8" fill="#121725"/>
  <line x1="40" y1="138" x2="40" y2="150" stroke="#1E2536" stroke-width="3"/>
  <line x1="340" y1="138" x2="340" y2="150" stroke="#1E2536" stroke-width="3"/>
  <rect x="34" y="114" width="312" height="26" rx="4" fill="#07080E" stroke="#1E2536"/>
  <text x="190" y="132" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="{CYAN}"
        letter-spacing="2" filter="url(#glow)" opacity=".7">LIGHTS-OUT FACTORY</text>
  <text x="190" y="132" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="#BFE9FF"
        letter-spacing="2">LIGHTS-OUT FACTORY</text>
</g>"""


# ---------------------------------------------------------------------------- truck

TRUCK = [(0, "300 0"), (3.0, "300 0"), (6.4, "930 0"), (7.6, "930 0"), (9.0, "1320 0", EASE_IN),
         (10.5, "1320 0"), (10.51, "-140 0"), (13.6, "300 0", EASE_OUT), (CYCLE, "300 0")]


def truck():
    return f"""
<g transform="translate(300 0)">{smil("transform", TRUCK, kind="translate")}
  <ellipse cx="10" cy="{GROUND}" rx="60" ry="4" fill="#000" opacity=".6"/>
  <rect x="-38" y="304" width="76" height="10" rx="2" fill="#2A3246"/>
  <path d="M38 314 V294 Q38 286 46 286 H60 Q68 286 70 296 L72 314 Z" fill="#1B2234" stroke="{STEEL_HI}"/>
  <path d="M46 290 H59 Q64 290 66 298 H46 Z" fill="#0B1424" stroke="{CYAN}" stroke-opacity=".5"/>
  <rect x="52" y="280" width="8" height="6" rx="2" fill="#3A4560"/><circle class="beacon" cx="56" cy="279" r="2" fill="{CYAN}"/>
  <circle cx="71" cy="306" r="2.4" fill="#FFF1C9"/>
  <line x1="-38" y1="320" x2="72" y2="320" stroke="{CYAN}" stroke-width="3" opacity=".6" filter="url(#glow)"/>
  <circle cx="-22" cy="321" r="8" fill="#0B0D14" stroke="#3A4560" stroke-width="2"/>
  <circle cx="20" cy="321" r="8" fill="#0B0D14" stroke="#3A4560" stroke-width="2"/>
  <circle cx="56" cy="321" r="8" fill="#0B0D14" stroke="#3A4560" stroke-width="2"/>
  {stage("u3", 0, 252)}
</g>"""


# ---------------------------------------------------------------------------- pad + booster

PAD_X = 980
BTOP = 198
UP = -420
BOOST = [(0, "0 0"), (9.0, "0 0"), (10.4, f"0 {UP}", EASE_IN), (11.0, f"0 {UP}"), (13.2, "0 0", EASE_OUT),
         (CYCLE, "0 0")]


def booster():
    left = smil("transform", [(0, f"0 {PAD_X - 8} 292"), (9.3, f"0 {PAD_X - 8} 292"), (9.6, f"-30 {PAD_X - 8} 292"),
                              (12.4, f"-30 {PAD_X - 8} 292"), (12.8, f"0 {PAD_X - 8} 292"), (CYCLE, f"0 {PAD_X - 8} 292")],
                kind="rotate")
    right = smil("transform", [(0, f"0 {PAD_X + 8} 292"), (9.3, f"0 {PAD_X + 8} 292"), (9.6, f"30 {PAD_X + 8} 292"),
                               (12.4, f"30 {PAD_X + 8} 292"), (12.8, f"0 {PAD_X + 8} 292"), (CYCLE, f"0 {PAD_X + 8} 292")],
                 kind="rotate")
    x0 = PAD_X - 11
    return f"""
<g>{smil("transform", BOOST, kind="translate")}
  <g class="burn">
    <path d="M{PAD_X - 14} 318 Q{PAD_X} 520 {PAD_X + 14} 318 Z" fill="{AMBER}" opacity=".35" filter="url(#glow)"/>
    <path class="flick" d="M{PAD_X - 9} 318 Q{PAD_X} 450 {PAD_X + 9} 318 Z" fill="url(#flame)"/>
    <circle cx="{PAD_X}" cy="326" r="16" fill="{GOLD}" opacity=".5" filter="url(#soft)"/>
  </g>
  <g transform="rotate(0 {PAD_X - 8} 292)">{left}<path d="M{PAD_X - 8} 292 L{PAD_X - 30} 318 H{PAD_X - 24}" fill="none" stroke="#9AA4BA" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></g>
  <g transform="rotate(0 {PAD_X + 8} 292)">{right}<path d="M{PAD_X + 8} 292 L{PAD_X + 30} 318 H{PAD_X + 24}" fill="none" stroke="#9AA4BA" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></g>
  <rect x="{x0}" y="{BTOP}" width="22" height="114" rx="2" fill="#E2E7F1"/>
  <rect x="{x0}" y="{BTOP}" width="7" height="114" fill="#FFFFFF" opacity=".35"/>
  <rect x="{x0}" y="{BTOP + 70}" width="22" height="44" fill="#C3C9D6"/>
  <rect x="{x0}" y="{BTOP + 70}" width="22" height="44" fill="#2B2018" opacity=".35"/>
  <rect x="{x0 - 4}" y="{BTOP + 4}" width="5" height="7" fill="#5B667C"/><rect x="{x0 + 21}" y="{BTOP + 4}" width="5" height="7" fill="#5B667C"/>
  <text x="{PAD_X}" y="{BTOP + 50}" text-anchor="middle" font-family="{MONO}" font-size="8" font-weight="700" fill="#3A4560"
        transform="rotate(-90 {PAD_X} {BTOP + 50})">REUSE</text>
  <path d="M{PAD_X - 8} 312 H{PAD_X + 8} L{PAD_X + 10} 319 H{PAD_X - 10} Z" fill="#2A3246"/>
</g>"""


def stacked_stage():
    frames = [(0, "930 252"), (6.6, "930 252"), (7.0, f"948 {BTOP - 96}"), (7.4, f"{PAD_X} {BTOP - 52}"),
              (9.0, f"{PAD_X} {BTOP - 52}"), (10.4, f"{PAD_X} {BTOP - 52 + UP}", EASE_IN), (CYCLE, f"{PAD_X} {BTOP - 52 + UP}")]
    return f'<g>{smil("transform", frames, kind="translate")}{stage("u4")}</g>'


def pad():
    lattice = "".join(f'<path d="M1064 {y} L1080 {y + 14} M1080 {y} L1064 {y + 14}" stroke="#2A3246" stroke-width="1.4"/>'
                      for y in range(126, 316, 14))
    return f"""
<g>
  <rect x="1062" y="122" width="20" height="{GROUND - 122}" fill="none" stroke="#2A3246" stroke-width="2.4"/>
  {lattice}
  <circle class="beacon" cx="1072" cy="118" r="3" fill="{RED}"/>
  <rect x="1022" y="190" width="40" height="5" fill="#2A3246"/>
  <rect x="1090" y="140" width="94" height="26" rx="4" fill="#07080E" stroke="#2A3246"/>
  {''.join(f'<text class="{c}" x="1137" y="158" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{col}">{esc(s)}</text>'
           for c, s, col in (("cd-ok", "landed ✓", GREEN), ("cd3", "T-3", GOLD), ("cd2", "T-2", GOLD), ("cd1", "T-1", GOLD),
                             ("cd-go", "liftoff", AMBER), ("cd-back", "coming home", CYAN)))}
  <path d="M916 {GROUND} L928 318 H1032 L1044 {GROUND} Z" fill="#1B2234"/>
  <ellipse cx="{PAD_X}" cy="318" rx="30" ry="3" fill="none" stroke="{GOLD}" stroke-opacity=".6"/>
  <text x="{PAD_X}" y="327" text-anchor="middle" font-family="{MONO}" font-size="7" fill="{GOLD}" opacity=".7">LAND HERE</text>
</g>"""


def smoke():
    puffs = "".join(f'<circle class="puff" style="animation-delay:-{i * .07:.2f}s" cx="{PAD_X + dx}" cy="{GROUND - 6}" r="{r}" fill="#A7B0C4" opacity=".8"/>'
                    for i, (dx, r) in enumerate(((-46, 14), (-26, 18), (0, 20), (26, 18), (48, 14), (-64, 10), (66, 10))))
    return f'<g class="smoke">{puffs}</g>'


# ---------------------------------------------------------------------------- highway + Nitish

CAR_X, CAR_Y = 640, 424  # car centre, wheel-axle line


def head():
    """Nitish's head, local origin at the face centre."""
    return f"""
<circle cx="-30" cy="4" r="7.5" fill="{SKIN_DK}"/><circle cx="30" cy="4" r="7.5" fill="{SKIN}"/>
<rect x="-30" y="-30" width="60" height="64" rx="28" fill="{SKIN}"/>
<ellipse cx="6" cy="-6" rx="18" ry="14" fill="{SKIN_LT}" opacity=".35"/>
<path d="M-32 -3 C-35 -24 -24 -40 -6 -43 C6 -45 20 -42 28 -30 C35 -20 35 -10 32 -3 C27 -15 16 -21 2 -21 C-14 -21 -25 -15 -32 -3 Z" fill="{HAIR}"/>
<path d="M-22 -28 C-8 -39 13 -39 24 -25" fill="none" stroke="{HAIR_HI}" stroke-width="4" stroke-linecap="round" opacity=".6"/>
<path d="M-22 14 C-18 32 18 32 22 14 C16 26 -16 26 -22 14 Z" fill="{HAIR}" opacity=".22"/>
<ellipse cx="-9" cy="1" rx="5.2" ry="5.6" fill="#FFF"/><ellipse cx="12" cy="1" rx="5.2" ry="5.6" fill="#FFF"/>
<g class="f-calm">
  <circle cx="-7" cy="2" r="2.7" fill="{HAIR}"/><circle cx="14" cy="2" r="2.7" fill="{HAIR}"/>
  <path d="M-16 -9 Q-9 -11 -3 -9 M6 -9 Q13 -11 19 -9" fill="none" stroke="{HAIR}" stroke-width="2.4" stroke-linecap="round"/>
  <path d="M-4 15 Q3 19 10 15" fill="none" stroke="#4A1915" stroke-width="2.4" stroke-linecap="round"/>
</g>
<g class="f-look" opacity="0">
  <circle cx="-6.5" cy="-1.5" r="2.7" fill="{HAIR}"/><circle cx="14.5" cy="-1.5" r="2.7" fill="{HAIR}"/>
  <path d="M-16 -13 Q-9 -16 -3 -13 M6 -13 Q13 -16 20 -13" fill="none" stroke="{HAIR}" stroke-width="2.4" stroke-linecap="round"/>
  <ellipse cx="3" cy="16" rx="3.4" ry="4.4" fill="#4A1915"/>
</g>
<g class="f-smug" opacity="0">
  <circle cx="-7" cy="1.5" r="2.7" fill="{HAIR}"/><circle cx="14" cy="1.5" r="2.7" fill="{HAIR}"/>
  <path d="M-16 -8 L-3 -8" stroke="{HAIR}" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M6 -12 Q13 -17 20 -11" fill="none" stroke="{HAIR}" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M-6 13 Q4 22 14 12" fill="none" stroke="#4A1915" stroke-width="2.4" stroke-linecap="round"/>
</g>"""


def wheel(cx, cy):
    spokes = "".join(f'<line x1="{cx}" y1="{cy}" x2="{f(cx + 9 * math.cos(math.radians(a)))}" '
                     f'y2="{f(cy + 9 * math.sin(math.radians(a)))}"/>' for a in range(0, 360, 60))
    return (f'<circle cx="{cx}" cy="{cy}" r="17" fill="#07080C" stroke="#2A3246" stroke-width="3"/>'
            f'<g class="spin" stroke="{CYAN}" stroke-width="2" stroke-linecap="round">{spokes}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="3" fill="{CYAN}"/>')


def car():
    cup_up = [(0, "-26 -26"), (1.4, "-26 -26"), (1.9, "0 0"), (13.2, "0 0"), (13.5, "-26 -26"), (CYCLE, "-26 -26")]
    arm_d = [(0, "M585 352 Q566 350 564 342"), (1.4, "M585 352 Q566 350 564 342"), (1.9, "M585 352 Q584 362 590 368"),
             (13.2, "M585 352 Q584 362 590 368"), (13.5, "M585 352 Q566 350 564 342"), (CYCLE, "M585 352 Q566 350 564 342")]
    return f"""
<g class="drive">
  <ellipse cx="{CAR_X}" cy="{CAR_Y + 16}" rx="140" ry="6" fill="#000" opacity=".6"/>
  <path d="M800 392 L1000 370 V430 L800 410 Z" fill="url(#beam)"/>
  <!-- Nitish in the back seat -->
  <path d="M574 380 V362 Q574 344 600 342 H616 Q640 344 640 362 V380 Z" fill="{HOODIE}" stroke="#2C354A"/>
  <path d="M598 342 Q608 352 618 342" fill="#ECEBE6"/>
  <g transform="translate(608 312) scale(.78)">{head()}</g>
  <!-- empty driver seat; the wheel steers itself -->
  <rect x="676" y="336" width="20" height="30" rx="7" fill="#151B29" stroke="#2C354A"/>
  <g class="steer"><ellipse cx="716" cy="352" rx="4" ry="12" fill="none" stroke="#8C97AD" stroke-width="3"/></g>
  <!-- body -->
  <path d="M512 426 V398 Q512 372 546 370 H712 L744 340 Q750 334 756 340 L770 376 Q798 380 800 402 V426 Z" fill="#1A2236"/>
  <path d="M712 370 L744 340" stroke="{CYAN}" stroke-opacity=".45" stroke-width="2"/>
  <path d="M520 384 H790" stroke="#2C354A"/>
  <path d="M600 372 V420" stroke="#11182A" stroke-width="2"/>
  <line x1="516" y1="428" x2="798" y2="428" stroke="{PINK}" stroke-width="6" opacity=".7" filter="url(#glow)"/>
  <rect x="512" y="392" width="6" height="10" rx="2" fill="{RED}"/>
  <rect x="794" y="392" width="7" height="8" rx="2" fill="#FFF1C9"/>
  <!-- lidar puck -->
  <rect x="744" y="328" width="14" height="8" rx="3" fill="#2A3246"/>
  <g class="scan"><path d="M751 330 L800 316 A50 50 0 0 1 800 346 Z" fill="{CYAN}" opacity=".18"/></g>
  <!-- rear display -->
  <rect x="514" y="352" width="56" height="18" rx="3" fill="#07080E" stroke="#2C354A"/>
  <text x="542" y="365" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="{GOLD}">ETA:orbit</text>
  <!-- coffee arm -->
  <path d="M585 352 Q566 350 564 342" fill="none" stroke="#1E2536" stroke-width="13" stroke-linecap="round">{smil("d", arm_d)}</path>
  <g>{smil("transform", cup_up, kind="translate")}
    <circle cx="590" cy="368" r="6.5" fill="{SKIN}"/>
    <rect x="579" y="352" width="13" height="16" rx="3" fill="#EFF3FA"/>
    <rect x="579" y="358" width="13" height="4" fill="{AMBER}"/>
  </g>
  {wheel(566, CAR_Y)}{wheel(748, CAR_Y)}
</g>"""


def traffic():
    cars = []
    for i, (dur, delay, col) in enumerate(((3.4, 0, CYAN), (5.1, 2.2, VIOLET), (4.3, 3.6, GOLD))):
        cars.append(f"""
<g class="oncoming" style="animation-duration:{dur}s;animation-delay:-{delay}s">
  <path d="M0 376 V366 Q2 356 16 355 L26 347 H52 L62 355 Q76 356 78 366 V376 Z" fill="#141A28"/>
  <path d="M29 349 H50 L57 356 H22 Z" fill="#0B1424"/>
  <rect x="36" y="342" width="7" height="5" rx="2" fill="#3A4560"/>
  <rect x="1" y="364" width="5" height="4" rx="1.5" fill="#FFF1C9"/>
  <line x1="2" y1="378" x2="76" y2="378" stroke="{col}" stroke-width="4" opacity=".7" filter="url(#glow)"/>
  <circle cx="18" cy="377" r="6" fill="#07080C"/><circle cx="60" cy="377" r="6" fill="#07080C"/>
</g>""")
    return "".join(cars)


def highway():
    dashes = "".join(f'<rect x="{x}" y="389" width="34" height="3" fill="#3A4560"/>' for x in range(-80, 1320, 80))
    posts = "".join(f'<rect x="{x}" y="336" width="3" height="14" fill="#1E2536"/>' for x in range(-60, 1300, 60))
    return f"""
<rect x="0" y="{GROUND}" width="{W}" height="{H - GROUND}" fill="url(#road)"/>
<rect x="0" y="{GROUND}" width="{W}" height="2" fill="#1D2334"/>
<g class="rail">{posts}</g>
<rect x="0" y="338" width="{W}" height="3" fill="#2A3246"/>
<rect x="0" y="352" width="{W}" height="2" fill="#2A3246"/>
{traffic()}
<g class="dash">{dashes}</g>
<rect x="0" y="436" width="{W}" height="2" fill="#2A3246"/>"""


def exit_sign():
    return f"""
<g>
  <rect x="1186" y="270" width="4" height="{GROUND - 270}" fill="#2A3246"/>
  <rect x="1100" y="244" width="94" height="40" rx="4" fill="#0E5A3A" stroke="#E8EDF7" stroke-width="1.5"/>
  <text x="1147" y="261" text-anchor="middle" font-family="{SANS}" font-size="12.5" font-weight="700" fill="#FFFFFF">portfolio</text>
  <text x="1147" y="277" text-anchor="middle" font-family="{SANS}" font-size="11" font-weight="600" fill="#D7F5E6">exit here ↗</text>
</g>"""


def bubble(cx, cy, w, s, tail_x, cls):
    return f"""
<g class="{cls}" opacity="0">
  <rect x="{f(cx - w / 2)}" y="{cy - 17}" width="{w}" height="34" rx="17" fill="#11141F" stroke="{GREEN}" stroke-width="1.6"/>
  <path d="M{tail_x - 7} {cy + 16} L{tail_x + 2} {cy + 27} L{tail_x + 7} {cy + 16}" fill="#11141F" stroke="{GREEN}" stroke-width="1.6" stroke-linejoin="round"/>
  <line x1="{tail_x - 6}" y1="{cy + 16}" x2="{tail_x + 6}" y2="{cy + 16}" stroke="#11141F" stroke-width="3"/>
  <text x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="{INK}">{esc(s)}</text>
</g>"""


# ---------------------------------------------------------------------------- assembly

def build():
    css = "\n".join([
        toggle("u1", [(0, 0.8), (12.4, CYCLE)], ramp=0.02),
        kf("u1slide", [(0, "transform:translateX(0)"), (12.4, "transform:translateX(-76px)"),
                       (13.4, "transform:translateX(0)"), (CYCLE, "transform:translateX(0)")]),
        f".u1slide{{{run('u1slide', 'ease-out')}}}",
        toggle("u2", [(0.8, 2.0)], ramp=0.02),
        toggle("u3", [(2.0, 6.6)], ramp=0.02),
        toggle("u4", [(6.6, 10.4)], ramp=0.02),
        toggle("burn", [(9.0, 10.4), (12.0, 13.2)], ramp=0.1),
        toggle("smoke", [(8.9, 10.6), (12.8, 13.9)], ramp=0.15),
        toggle("cd-ok", [(0, 7.9), (13.3, CYCLE)], ramp=0.04),
        toggle("cd3", [(8.0, 8.33)], ramp=0.02),
        toggle("cd2", [(8.35, 8.66)], ramp=0.02),
        toggle("cd1", [(8.68, 8.98)], ramp=0.02),
        toggle("cd-go", [(9.0, 11.0)], ramp=0.02),
        toggle("cd-back", [(11.02, 13.25)], ramp=0.02),
        toggle("f-calm", [(8.9, 13.2), (13.2, CYCLE), (0, 1.6)], ramp=0.08, invert=True),
        toggle("f-look", [(8.9, 13.2)]),
        toggle("f-smug", [(13.2, CYCLE), (0, 1.6)]),
        toggle("say", [(13.3, CYCLE), (0, 1.6)], ramp=0.12),
        # ambient
        "@keyframes spin{to{transform:rotate(360deg)}}",
        ".spin{animation:spin .5s linear infinite;transform-box:fill-box;transform-origin:center}",
        "@keyframes steer{0%,100%{transform:rotate(-14deg)}50%{transform:rotate(14deg)}}",
        ".steer{animation:steer 2.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}",
        "@keyframes scan{0%,100%{transform:scaleY(.4)}50%{transform:scaleY(1.2)}}",
        ".scan{animation:scan 1.2s ease-in-out infinite;transform-box:fill-box;transform-origin:0 50%}",
        "@keyframes drive{0%,100%{transform:translateY(0)}50%{transform:translateY(-1.5px)}}",
        ".drive{animation:drive .45s ease-in-out infinite}",
        "@keyframes dash{to{transform:translateX(-80px)}}.dash{animation:dash .32s linear infinite}",
        "@keyframes rail{to{transform:translateX(-60px)}}.rail{animation:rail .5s linear infinite}",
        "@keyframes oncoming{from{transform:translateX(1260px)}to{transform:translateX(-120px)}}",
        ".oncoming{animation-name:oncoming;animation-timing-function:linear;animation-iteration-count:infinite}",
        "@keyframes belt{to{transform:translateX(12px)}}.belt{animation:belt .6s linear infinite}",
        "@keyframes flick{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.8)}}",
        ".flick{animation:flick .12s linear infinite;transform-box:fill-box;transform-origin:50% 0}",
        "@keyframes puff{0%{transform:scale(.3);opacity:.7}100%{transform:scale(1.6);opacity:0}}",
        ".puff{animation:puff .9s ease-out infinite;transform-box:fill-box;transform-origin:center}",
        "@keyframes tw{0%,100%{opacity:.9}50%{opacity:.15}}.tw{animation:tw 3s ease-in-out infinite}",
        "@keyframes beacon{0%,100%{opacity:.2}50%{opacity:1}}.beacon{animation:beacon 1.6s infinite}",
        "@media (prefers-reduced-motion: reduce){*{animation:none!important}}",
    ])

    body = "\n".join([
        defs(),
        sky(),
        skyline(),
        factory(),
        arm(),
        factory_front(),
        pad(),
        stacked_stage(),
        booster(),
        smoke(),
        truck(),
        exit_sign(),
        highway(),
        car(),
        bubble(610, 252, 112, "stuck it.", 606, "say"),
    ])
    return doc(
        W, H,
        "Ground to orbit: a lights-out factory, a driverless truck, a reusable booster",
        css, body,
        desc=("A neon night scene. In a lights-out factory a robot arm loads a rocket upper stage onto a driverless "
              "truck, which drives itself to the launch pad. The stage is stacked on a reusable booster, the countdown "
              "runs, the rocket lifts off, and the booster comes back down and lands on the pad. In the foreground "
              "Nitish rides past in a self-driving car with an empty driver's seat, raises his coffee and says "
              "stuck it."),
    )
