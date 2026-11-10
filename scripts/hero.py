"""Header: my 2019 Handwriting-Machine plots the signature, and the disciplines fall into orbit around it."""

import math
import random

from svgkit import (AI, BG, BORDER, EASE, EMBEDDED, MONO, MUTED, POWER, ROBOTICS, SILICON, SOFTWARE, TEXT, WHITE,
                    discrete, doc, esc, f, length, mono_text, parse_path, polyline, seg_path, text)

W, H = 1200, 560

# "nitish" in one continuous cursive stroke. Units: baseline y=0, x-height 50, up is negative.
STROKE = """
M0,0 C10,-6 16,-30 20,-50 C20,-35 19,-15 18,0
C22,-28 32,-52 46,-50 C56,-48 56,-36 55,-24 C54,-12 54,-2 60,0
C66,1 72,-18 76,-46 C75,-28 74,-6 80,0
C88,2 96,-40 100,-88 C99,-55 97,-15 104,-1
C110,2 120,-20 124,-46 C122,-28 121,-6 127,0
C133,2 140,-30 146,-52 C154,-40 165,-24 158,-9 C152,1 137,1 133,-6
C139,-2 152,-1 162,-10
C170,-30 186,-90 180,-118 C176,-132 162,-124 164,-100 C165,-70 166,-30 166,0
C170,-30 180,-52 192,-50 C202,-48 202,-34 201,-22 C200,-10 200,-2 208,0
C216,2 226,-8 238,-22
"""
# Pen-lift strokes, drawn after the word like real handwriting: two i dots and the t bar.
LIFTS = [
    ("i", [(77, -70), (79.5, -72)]),
    ("i", [(126, -70), (128.5, -72)]),
    ("t", [(86, -60), (116, -64)]),
]

SCALE, SLANT = 1.7, math.tan(math.radians(12))
OX, OY = 384, 290
HOME = (960, 96)

T_START, T_DRAW = 0.6, 4.2  # main stroke timing (s)

# The system the name sits in: three orbits, two disciplines on each. The hollow one is where I'm headed.
CX, CY, TILT = 600, 272, -7
ORBITS = [  # (rx, ry, period s, [(label, colour, phase 0..1, hollow)])
    (404, 172, 46, [("SILICON", SILICON, 0.06, False), ("FIRMWARE", EMBEDDED, 0.56, False)]),
    (474, 204, 62, [("POWER", POWER, 0.30, False), ("ROBOTICS", ROBOTICS, 0.80, False)]),
    (544, 236, 80, [("CLOUD", SOFTWARE, 0.47, False), ("PHYSICAL AI", AI, 0.93, True)]),
]


def place(p):
    x, y = p
    return (OX + SCALE * (x - y * SLANT), OY + SCALE * y)


def ellipse(rx, ry):
    """Closed ellipse that starts on the right and comes round the front (bottom) first."""
    return (f"M{CX + rx} {CY}A{rx} {ry} 0 1 1 {CX - rx} {CY}"
            f"A{rx} {ry} 0 1 1 {CX + rx} {CY}Z")


def build():
    segs = [tuple(place(p) for p in s) for s in parse_path(STROKE)]
    main_pts = polyline(segs)
    main_len = length(main_pts)
    lifts = [(k, [place(p) for p in pts]) for k, pts in LIFTS]
    start, end = main_pts[0], main_pts[-1]

    # ---- pen timeline: (time, distance along the motion path) ------------------------------
    main_d = seg_path(segs)
    motion = [f"M{f(HOME[0])} {f(HOME[1])}L{f(start[0])} {f(start[1])}", main_d[main_d.index("C"):]]
    dist, times = [0.0, math.dist(HOME, start)], [0.0, T_START]
    dist.append(dist[-1] + main_len)
    t = T_START + T_DRAW
    times.append(t)
    pen_down, lift_draws = [(T_START, t)], []
    cur = end
    for kind, (a, b) in lifts:
        travel = math.dist(cur, a)
        t_travel = 0.16 + travel / 1500
        motion.append(f"L{f(a[0])} {f(a[1])}")
        dist.append(dist[-1] + travel)
        t += t_travel
        times.append(t)
        t_draw = 0.12 if kind == "i" else 0.28
        motion.append(f"L{f(b[0])} {f(b[1])}")
        dist.append(dist[-1] + math.dist(a, b))
        lift_draws.append((a, b, t, t_draw))
        pen_down.append((t, t + t_draw))
        t += t_draw
        times.append(t)
        t += 0.06
        cur = b
    t_signed = t
    total = dist[-1]
    key_times = [tt / t_signed for tt in times]
    key_points = [dd / total for dd in dist]

    # ---- the signature ---------------------------------------------------------------------
    css = [
        ".ink{fill:none;stroke-linecap:round;stroke-linejoin:round}",
        f".main{{stroke-dasharray:{f(main_len + 2)};stroke-dashoffset:{f(main_len + 2)};"
        f"animation:draw {T_DRAW}s cubic-bezier(.45,.05,.55,.95) {T_START}s forwards}}",
        "@keyframes draw{to{stroke-dashoffset:0}}",
    ]
    lift_svg = []
    for i, (a, b, t0, td) in enumerate(lift_draws):
        L = math.dist(a, b) + 1
        css.append(f".lift{i}{{stroke-dasharray:{f(L)};stroke-dashoffset:{f(L)};"
                   f"animation:draw {td}s linear {f(t0)}s forwards}}")
        lift_svg.append(f'<path class="ink lift{i}" stroke="{WHITE}" stroke-width="{6 if L < 6 else 3.8}" '
                        f'd="M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}"/>')
    signature = f"""
<path class="ink main" d="{main_d}" stroke="{WHITE}" stroke-width="9" opacity=".34" filter="url(#bloom)"/>
<path class="ink main" d="{main_d}" stroke="{WHITE}" stroke-width="3.8"/>
{''.join(lift_svg)}"""

    # The main stroke eases in and out, so the pen has to follow the same curve: sample it.
    def ease(u, a=0.45, b=0.05, c=0.55, d=0.95):
        lo, hi = 0.0, 1.0
        for _ in range(40):  # solve bezier x(s) = u
            s = (lo + hi) / 2
            x = 3 * (1 - s) ** 2 * s * a + 3 * (1 - s) * s * s * c + s ** 3
            lo, hi = (s, hi) if x < u else (lo, s)
        return 3 * (1 - s) ** 2 * s * b + 3 * (1 - s) * s * s * d + s ** 3

    kt, kp = [key_times[0]], [key_points[0]]
    for k in range(25):
        u = k / 24
        kt.append((T_START + T_DRAW * u) / t_signed)
        kp.append((dist[1] + main_len * ease(u)) / total)
    kt += key_times[3:]
    kp += key_points[3:]

    pen_ev = [(0, "0")]
    for a, b in pen_down:
        pen_ev += [(a, "1"), (b, "0")]
    pen = f"""
<g opacity="0">
  <animate attributeName="opacity" dur="{f(t_signed + 0.5)}s" fill="freeze" values="0;1;1;0"
    keyTimes="0;{0.2 / (t_signed + 0.5):.4f};{t_signed / (t_signed + 0.5):.4f};1"/>
  <animateMotion dur="{f(t_signed)}s" fill="freeze" calcMode="linear" path="{''.join(motion)}"
    keyPoints="{';'.join(f'{k:.5f}' for k in kp)}" keyTimes="{';'.join(f'{k:.5f}' for k in kt)}"/>
  <circle r="26" fill="url(#halo)" opacity="0">{discrete("opacity", pen_ev, t_signed + 0.01)}</circle>
  <circle r="3.2" fill="{WHITE}"/>
</g>"""

    # ---- orbits ----------------------------------------------------------------------------
    t_orbit = 1.2
    orbit_svg, sat_svg = [], []
    for i, (rx, ry, period, sats) in enumerate(ORBITS):
        d = ellipse(rx, ry)
        delay = t_orbit + i * 0.45
        orbit_svg.append(f'<path class="orbit" d="{d}" pathLength="1" style="animation-delay:{f(delay)}s" '
                         f'stroke-opacity="{f(0.2 - i * 0.04)}"/>')
        for label, colour, phase, hollow in sats:
            begin = f"-{f(phase * period)}s"
            loop = f'dur="{period}s" begin="{begin}" repeatCount="indefinite"'
            dot = (f'<circle r="5" fill="{BG}" stroke="{colour}" stroke-width="2"/>' if hollow
                   else f'<circle r="4.5" fill="{colour}"/>')
            sat_svg.append(f"""
<g class="rise" style="animation-delay:{f(delay + 2.2)}s"><g>
  <animateMotion {loop} path="{d}"/>
  <g><animate attributeName="opacity" {loop} values=".75;1;.75;.45;.75" keyTimes="0;.25;.5;.75;1"/>
    {dot}
    <text transform="rotate({-TILT})" y="28" text-anchor="middle" font-family="{MONO}" font-size="17" font-weight="600" letter-spacing="2" fill="{colour}">{esc(label)}</text>
  </g>
</g></g>""")
    css += [
        f".orbit{{fill:none;stroke:{WHITE};stroke-dasharray:1;stroke-dashoffset:1;animation:draw 3.2s {EASE} forwards}}",
        f".rise{{opacity:0;animation:rise 1.4s {EASE} forwards}}",
        "@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}",
    ]

    # ---- a quiet field of stars behind everything -------------------------------------------
    random.seed(11)
    stars = []
    for i in range(64):
        x, y = random.uniform(24, W - 24), random.uniform(24, H - 24)
        r, o = random.choice([0.6, 0.8, 0.8, 1.1, 1.4]), random.uniform(0.12, 0.5)
        tw = f' class="tw loop" style="animation-delay:-{f(random.uniform(0, 6))}s"' if i % 5 == 0 else ""
        stars.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{WHITE}" opacity="{f(o)}"{tw}/>')
    css.append(".tw{animation:tw 6s ease-in-out infinite}@keyframes tw{50%{opacity:.05}}")

    # ---- words -----------------------------------------------------------------------------
    t_words = t_signed + 0.15
    words = f"""
<g class="rise" style="animation-delay:{f(t_words)}s">
  {text(W / 2, OY + 94, "Connecting ideas. Making things work.", 42, TEXT, 600, anchor="middle", extra='letter-spacing="-0.8"')}
</g>
<g class="rise" style="animation-delay:{f(t_words + 0.25)}s">
  {mono_text(W / 2 + 2, OY + 138, "MULTIDISCIPLINARY ENGINEER  ·  MONTRÉAL", 18, MUTED, fit=False, anchor="middle", extra='letter-spacing="3"')}
</g>"""

    chrome = f"""
{mono_text(40, 54, "NITISH SUNDARRAJ", 18, TEXT, fit=False, extra='letter-spacing="4" font-weight="600"')}
<circle cx="{W - 216}" cy="48" r="5" fill="{SILICON}" class="live loop"/>
{mono_text(W - 40, 54, "12 LABS LIVE", 17, MUTED, fit=False, anchor="end", extra='letter-spacing="3"')}"""
    css += [
        ".live{animation:live 2.4s ease-in-out infinite}@keyframes live{50%{opacity:.2}}",
        "@media (prefers-reduced-motion: reduce){.main,[class*=lift],.orbit{animation-duration:.01s!important;"
        "animation-delay:0s!important}.rise{animation:none!important;opacity:1!important}}",
    ]

    body = f"""<defs>
<clipPath id="frame"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17"/></clipPath>
<radialGradient id="stage" cx="50%" cy="48%" r="60%"><stop offset="0" stop-color="{WHITE}" stop-opacity=".075"/><stop offset=".55" stop-color="{WHITE}" stop-opacity=".02"/><stop offset="1" stop-color="{WHITE}" stop-opacity="0"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="{WHITE}" stop-opacity=".55"/><stop offset="1" stop-color="{WHITE}" stop-opacity="0"/></radialGradient>
<filter id="bloom" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="soft" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="#000" stroke="{BORDER}"/>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#stage)"/>
  {''.join(stars)}
  <g transform="rotate({TILT} {CX} {CY})">{''.join(orbit_svg)}{''.join(sat_svg)}</g>
</g>
<rect x="236" y="{OY + 46}" width="{W - 472}" height="116" rx="58" fill="#000" opacity=".92" filter="url(#soft)"/>
{signature}
{pen}
{words}
{chrome}"""
    return doc(W, H, "Nitish Sundarraj: Connecting ideas. Making things work.", "\n".join(css), body,
               "A pen plotter signs 'nitish' in white on black while six disciplines, from silicon and firmware to "
               "robotics, cloud and physical AI, settle into orbit around the name.")
