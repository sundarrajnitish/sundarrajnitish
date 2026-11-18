"""Header: portfolio-themed obsidian convergence stage where the 2019 Handwriting-Machine
plots the signature while six disciplines orbit as glowing convergence nodes."""

import math
import random

from svgkit import (ACCENT, ACCENT_2, ACCENT_MID, AI, BG, BG_ALT, BORDER, BORDER_SOFT, DIM, EASE, EMBEDDED, GREEN,
                    MONO, MUTED, POWER, ROBOTICS, SANS, SERIF, SILICON, SOFTWARE, TEXT, VIOLET, WHITE, discrete, doc,
                    esc, f, length, mono_text, parse_path, polyline, seg_path, text)

W, H = 1200, 620
TOP_H = 64
BOT_Y = 542

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

SCALE, SLANT = 1.55, math.tan(math.radians(12))
OX, OY = 411, 298
HOME = (960, 120)

T_START, T_DRAW = 0.6, 4.2  # main stroke timing (s)

# The system the name sits in: three tilted convergence orbits, two disciplines on each.
# The hollow node marks where I'm headed next.
CX, CY, TILT = 600, 286, -6
ORBITS = [  # (rx, ry, period s, packet colour, [(label, colour, phase 0..1, hollow)])
    (392, 144, 46, GREEN, [("SILICON", SILICON, 0.96, False), ("FIRMWARE", EMBEDDED, 0.55, False)]),
    (462, 174, 62, ACCENT, [("POWER", POWER, 0.27, False), ("ROBOTICS", ROBOTICS, 0.67, False)]),
    (532, 204, 80, ACCENT_2, [("CLOUD", SOFTWARE, 0.43, False), ("PHYSICAL AI", AI, 0.90, True)]),
]

# Four connected threads from the portfolio, anchored along the bottom proof bar.
THREADS = [
    (38, "01", "Power & OT", POWER),
    (248, "02", "Verified Silicon", SILICON),
    (496, "03", "Autonomy", ROBOTICS),
    (696, "04", "Cloud & AI", VIOLET),
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
        lift_svg.append(f'<path class="ink lift{i}" stroke="{TEXT}" stroke-width="{6 if L < 6 else 3.8}" '
                        f'd="M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}"/>')
    dot_x, dot_y = OX + SCALE * 250, OY - 4
    signature = f"""
<path class="ink main" d="{main_d}" stroke="url(#sigBloom)" stroke-width="10" opacity=".42" filter="url(#bloom)"/>
<path class="ink main" d="{main_d}" stroke="{TEXT}" stroke-width="3.8"/>
{''.join(lift_svg)}
<g class="rise" style="animation-delay:{f(t_signed)}s">
  <circle cx="{f(dot_x)}" cy="{f(dot_y)}" r="12" fill="{ACCENT}" opacity=".2"/>
  <circle cx="{f(dot_x)}" cy="{f(dot_y)}" r="4.8" fill="{ACCENT}"/>
</g>"""

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
  <circle r="28" fill="url(#halo)" opacity="0">{discrete("opacity", pen_ev, t_signed + 0.01)}</circle>
  <circle r="3.4" fill="{WHITE}"/>
</g>"""

    # ---- convergence orbits, telemetry packets & glowing glass nodes -----------------------
    t_orbit = 1.1
    orbit_svg, pkt_svg, sat_svg = [], [], []
    # Subtle static dashed architectural ring echoing the portfolio convergence console
    orbit_svg.append(
        f'<path d="{ellipse(427, 159)}" fill="none" stroke="{WHITE}" stroke-opacity=".075" '
        f'stroke-dasharray="3 7"/>'
    )
    for i, (rx, ry, period, pcol, sats) in enumerate(ORBITS):
        d = ellipse(rx, ry)
        delay = t_orbit + i * 0.42
        orbit_svg.append(
            f'<path class="orbit" d="{d}" pathLength="1" style="animation-delay:{f(delay)}s" '
            f'stroke-opacity="{f(0.17 - i * 0.032)}"/>'
        )
        # Telemetry packet streaming silently along the orbit ring
        p_dur = period * 0.42
        pkt_svg.append(f"""
<g class="rise" style="animation-delay:{f(delay + 1.8)}s"><g>
  <animateMotion dur="{f(p_dur)}s" begin="-{f(i * 5.2 + 2.4)}s" repeatCount="indefinite" path="{d}"/>
  <circle r="9" fill="{pcol}" opacity=".24"/>
  <circle r="2.4" fill="{WHITE}"/>
</g></g>""")
        for label, colour, phase, hollow in sats:
            begin = f"-{f(phase * period)}s"
            loop = f'dur="{period}s" begin="{begin}" repeatCount="indefinite"'
            core = ("" if hollow else f'<circle r="2.7" fill="{colour}"/>')
            sat_svg.append(f"""
<g class="rise" style="animation-delay:{f(delay + 2.0)}s"><g>
  <animateMotion {loop} path="{d}"/>
  <g><animate attributeName="opacity" {loop} values=".84;1;.84;.56;.84" keyTimes="0;.25;.5;.75;1"/>
    <circle r="13.5" fill="{colour}" opacity=".18"/>
    <circle r="6.4" fill="#0A0D14" stroke="{colour}" stroke-width="2.1"/>
    {core}
    <text transform="rotate({-TILT})" y="27" text-anchor="middle" font-family="{MONO}" font-size="16.5" font-weight="600" letter-spacing="1.8" fill="{colour}">{esc(label)}</text>
  </g>
</g></g>""")
    css += [
        f".orbit{{fill:none;stroke:{WHITE};stroke-dasharray:1;stroke-dashoffset:1;animation:draw 3.0s {EASE} forwards}}",
        f".rise{{opacity:0;animation:rise 1.2s {EASE} forwards}}",
        "@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}",
        "@keyframes breath{50%{opacity:.55}}",
        ".glow{animation:breath 14s ease-in-out infinite}",
    ]

    # ---- subtle pinpoint ambient coordinates -----------------------------------------------
    random.seed(19)
    dots = []
    for i in range(32):
        x, y = random.uniform(32, W - 32), random.uniform(TOP_H + 18, BOT_Y - 18)
        r, o = random.choice([0.7, 0.9, 1.1]), random.uniform(0.08, 0.28)
        col = random.choice([WHITE, WHITE, WHITE, ACCENT_2, ACCENT])
        tw = f' class="tw loop" style="animation-delay:-{f(random.uniform(0, 6))}s"' if i % 4 == 0 else ""
        dots.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{col}" opacity="{f(o)}"{tw}/>')
    css.append(".tw{animation:tw 6.5s ease-in-out infinite}@keyframes tw{50%{opacity:.04}}")

    # ---- editorial headline & subtitle -----------------------------------------------------
    t_words = t_signed + 0.12
    words = f"""
<g class="rise" style="animation-delay:{f(t_words)}s">
  <text x="{W / 2}" y="384" text-anchor="middle" font-family="{SANS}" font-size="42" font-weight="700" letter-spacing="-0.9" fill="{TEXT}">Connecting ideas. Making <tspan font-family="{SERIF}" font-style="italic" font-weight="400" font-size="47" letter-spacing="-0.2" fill="url(#brandGrad)">things work.</tspan></text>
</g>
<g class="rise" style="animation-delay:{f(t_words + 0.22)}s">
  {text(W / 2, 426, "Bridging power infrastructure, verified silicon, autonomous machines & cloud.", 18.5, MUTED, 400, anchor="middle", extra='letter-spacing="-0.1"')}
</g>"""

    # ---- top console bar (matches portfolio .nav-inner & .hc-bar) --------------------------
    top_bar = f"""
<rect x="0" y="0" width="{W}" height="{TOP_H}" fill="#0A0D16" fill-opacity=".68"/>
<rect x="0" y="0" width="{W}" height="3" fill="url(#accentBar)"/>
<line x1="0" y1="{TOP_H}" x2="{W}" y2="{TOP_H}" stroke="{WHITE}" stroke-opacity=".075"/>
<circle cx="38" cy="33" r="10" fill="{GREEN}" opacity=".2" class="live loop"/>
<circle cx="38" cy="33" r="4.5" fill="{GREEN}" class="live loop"/>
<text x="56" y="39" font-family="{SANS}" font-size="17.5" font-weight="700" letter-spacing="-0.3" fill="{TEXT}">Nitish Sundarraj<tspan fill="{ACCENT}">.</tspan></text>
<line x1="204" y1="22" x2="204" y2="44" stroke="{BORDER}"/>
{mono_text(222, 38, "MULTIDISCIPLINARY DEVELOPER", 14.5, MUTED, fit=False, extra='letter-spacing="2.2" font-weight="500"')}
<rect x="904" y="19" width="76" height="28" rx="14" fill="{GREEN}" fill-opacity=".13" stroke="{GREEN}" stroke-opacity=".34"/>
<circle cx="921" cy="33" r="3.5" fill="{GREEN}" class="live loop"/>
{mono_text(932, 37.5, "LIVE", 12.5, GREEN, fit=False, extra='letter-spacing="1.2" font-weight="700"')}
{mono_text(W - 34, 38, "SYS // 09 LAYERS", 14, DIM, fit=False, anchor="end", extra='letter-spacing="1.4" font-weight="500"')}"""

    # ---- bottom proof & CTA bar (matches portfolio .hero-proof & .pill) --------------------
    thread_svg = []
    for x, num, label, col in THREADS:
        thread_svg.append(
            f'<rect x="{x}" y="{BOT_Y + 35}" width="8" height="8" rx="2" fill="{col}"/>'
            + mono_text(x + 17, BOT_Y + 44, num, 15, TEXT, fit=False, extra='font-weight="600"')
            + text(x + 43, BOT_Y + 44, label, 16, MUTED, 500)
        )
    bx, by, bw, bh = 954, BOT_Y + 17, 212, 44
    bottom_bar = f"""
<rect x="0" y="{BOT_Y}" width="{W}" height="{H - BOT_Y}" fill="#07090F" fill-opacity=".86"/>
<line x1="0" y1="{BOT_Y}" x2="{W}" y2="{BOT_Y}" stroke="{WHITE}" stroke-opacity=".075"/>
{''.join(thread_svg)}
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{bh / 2}" fill="{TEXT}"/>
{text(bx + 26, by + 27.5, "Explore portfolio", 15.5, BG, 700, extra='letter-spacing="-0.1"')}
<g class="arrow loop"><path d="M{bx + bw - 38} {by + bh / 2}h14m-5.5 -5.5l5.5 5.5l-5.5 5.5" fill="none" stroke="{BG}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/></g>"""

    css += [
        ".live{animation:live 2.8s ease-in-out infinite}@keyframes live{50%{opacity:.45}}",
        f".arrow{{animation:arrow 3.2s {EASE} infinite}}@keyframes arrow{{0%,55%,100%{{transform:none}}75%{{transform:translateX(5px)}}}}",
        "@media (prefers-reduced-motion: reduce){.main,[class*=lift],.orbit{animation-duration:.01s!important;"
        "animation-delay:0s!important}.rise{animation:none!important;opacity:1!important}}",
    ]

    body = f"""<defs>
<clipPath id="frame"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="23"/></clipPath>
<linearGradient id="canvasBg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#101521"/>
  <stop offset=".55" stop-color="{BG_ALT}"/>
  <stop offset="1" stop-color="{BG}"/>
</linearGradient>
<linearGradient id="accentBar" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{ACCENT}"/>
  <stop offset=".5" stop-color="#FFD166"/>
  <stop offset="1" stop-color="{ACCENT_2}"/>
</linearGradient>
<linearGradient id="brandGrad" gradientUnits="userSpaceOnUse" x1="715" y1="360" x2="965" y2="390">
  <stop offset="0" stop-color="{ACCENT}"/>
  <stop offset=".55" stop-color="{ACCENT_MID}"/>
  <stop offset="1" stop-color="{ACCENT_2}"/>
</linearGradient>
<linearGradient id="sigBloom" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{ACCENT}"/>
  <stop offset=".5" stop-color="{WHITE}"/>
  <stop offset="1" stop-color="{ACCENT_2}"/>
</linearGradient>
<radialGradient id="glowAmber" cx="76%" cy="32%" r="42%">
  <stop offset="0" stop-color="{ACCENT}" stop-opacity=".18"/>
  <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowCyan" cx="22%" cy="30%" r="40%">
  <stop offset="0" stop-color="{ACCENT_2}" stop-opacity=".14"/>
  <stop offset="1" stop-color="{ACCENT_2}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowGreen" cx="52%" cy="84%" r="36%">
  <stop offset="0" stop-color="{GREEN}" stop-opacity=".09"/>
  <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="wordVeil" cx="50%" cy="50%" r="50%">
  <stop offset="0" stop-color="{BG}" stop-opacity=".86"/>
  <stop offset=".58" stop-color="{BG}" stop-opacity=".62"/>
  <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="halo">
  <stop offset="0" stop-color="{ACCENT}" stop-opacity=".62"/>
  <stop offset=".45" stop-color="{ACCENT_MID}" stop-opacity=".22"/>
  <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
</radialGradient>
<pattern id="archGrid" width="64" height="64" patternUnits="userSpaceOnUse">
  <path d="M64 0H0V64" fill="none" stroke="{WHITE}" stroke-width="1" stroke-opacity=".075"/>
</pattern>
<radialGradient id="gridFade" cx="50%" cy="46%" r="58%">
  <stop offset="0" stop-color="{WHITE}" stop-opacity="1"/>
  <stop offset=".68" stop-color="{WHITE}" stop-opacity=".45"/>
  <stop offset="1" stop-color="{WHITE}" stop-opacity="0"/>
</radialGradient>
<mask id="gridMask"><rect width="{W}" height="{H}" fill="url(#gridFade)"/></mask>
<filter id="bloom" x="-12%" y="-30%" width="124%" height="160%"><feGaussianBlur stdDeviation="8.5"/></filter>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="24" fill="url(#canvasBg)" stroke="{BORDER}"/>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#archGrid)" mask="url(#gridMask)"/>
  <rect class="glow loop" width="{W}" height="{H}" fill="url(#glowAmber)"/>
  <rect class="glow loop" style="animation-delay:-5s" width="{W}" height="{H}" fill="url(#glowCyan)"/>
  <rect class="glow loop" style="animation-delay:-10s" width="{W}" height="{H}" fill="url(#glowGreen)"/>
  {''.join(dots)}
  <g transform="rotate({TILT} {CX} {CY})">{''.join(orbit_svg)}{''.join(pkt_svg)}{''.join(sat_svg)}</g>
  <ellipse cx="{W / 2}" cy="396" rx="450" ry="96" fill="url(#wordVeil)"/>
  {signature}
  {pen}
  {words}
  {top_bar}
  {bottom_bar}
  <line x1="24" y1="3.5" x2="{W - 24}" y2="3.5" stroke="{WHITE}" stroke-opacity=".1"/>
</g>"""
    return doc(W, H, "Nitish Sundarraj: Connecting ideas. Making things work.", "\n".join(css), body,
               "Obsidian architectural glass hero matching Nitish Sundarraj's portfolio theme: a pen plotter signs "
               "'nitish' in white and warm amber while six disciplines orbit as glowing convergence nodes above four "
               "engineering threads.")
