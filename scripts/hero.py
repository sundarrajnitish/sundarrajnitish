"""Header: the 2020 Handwriting-Machine plots my signature from its own G-code dialect."""

import math

from svgkit import (AMBER, BG_ALT, BORDER, BORDER_SOFT, CYAN, DIM, GREEN, MONO, MONO_ADV, MUTED, RED, TEXT,
                    VIOLET, bez, discrete, doc, esc, f, grid_pattern, length, mono_text, panel, parse_path,
                    polyline, resample, seg_path, typed)

W, H = 1200, 500

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

SCALE, SLANT = 1.82, math.tan(math.radians(12))
OX, OY = 452, 300

# Bed and its mapping to plotter millimetres (the real machine had a 155 x 155 mm bed).
BED = (392, 60, 1180, 480)
PX_PER_MM = (BED[2] - BED[0]) / 155
HOME = (1128, 112)

T_START, T_DRAW = 0.7, 6.2  # main stroke timing (s)


def place(p):
    x, y = p
    return (OX + SCALE * (x - y * SLANT), OY + SCALE * y)


def mm(p):
    return ((p[0] - BED[0]) / PX_PER_MM, (BED[3] - p[1]) / PX_PER_MM)


def g01(p):
    x, y = mm(p)
    return f"G01 X{x:.2f} Y{y:.2f}"


def g00(p):
    x, y = mm(p)
    return f"G00 X{x:.2f} Y{y:.2f}"


def build():
    segs = [tuple(place(p) for p in s) for s in parse_path(STROKE)]
    main_pts = polyline(segs)
    main_len = length(main_pts)
    lifts = [(k, [place(p) for p in pts]) for k, pts in LIFTS]
    start, end = main_pts[0], main_pts[-1]

    # ---- timeline -------------------------------------------------------------------------
    # waypoints for the pen: (time, cumulative distance along the motion path)
    motion = [f"M{f(HOME[0])} {f(HOME[1])}L{f(start[0])} {f(start[1])}", seg_path(segs)[seg_path(segs).index("C"):]]
    dist = [0.0, math.dist(HOME, start)]
    times = [0.0, T_START]
    dist.append(dist[-1] + main_len)
    t = T_START + T_DRAW
    times.append(t)
    pen_down = [(T_START, T_START + T_DRAW)]
    lift_draws = []
    gcode = [(T_START - 0.02, "M03", "; pen down")]
    gcode_main = resample(main_pts, 58)
    for k, p in enumerate(gcode_main[1:], 1):
        gcode.append((T_START + T_DRAW * k / 58, g01(p), ""))
    gcode.append((t + 0.02, "M05", "; pen up"))
    cur = end
    for kind, (a, b) in lifts:
        travel = math.dist(cur, a)
        t_travel = 0.18 + travel / 1400
        motion.append(f"L{f(a[0])} {f(a[1])}")
        dist.append(dist[-1] + travel)
        t += t_travel
        times.append(t)
        gcode.append((t - t_travel / 2, g00(a), "; i dot" if kind == "i" else "; cross the t"))
        gcode.append((t, "M03", ""))
        t_draw = 0.14 if kind == "i" else 0.32
        motion.append(f"L{f(b[0])} {f(b[1])}")
        dist.append(dist[-1] + math.dist(a, b))
        lift_draws.append((a, b, t, t_draw))
        pen_down.append((t, t + t_draw))
        t += t_draw
        times.append(t)
        gcode.append((t, g01(b), ""))
        gcode.append((t + 0.02, "M05", ""))
        t += 0.08
        cur = b
    travel = math.dist(cur, HOME)
    motion.append(f"L{f(HOME[0])} {f(HOME[1])}")
    dist.append(dist[-1] + travel)
    t += 0.55
    times.append(t)
    gcode.append((t - 0.3, g00(HOME), "; park"))
    gcode.append((t + 0.1, "M02", "; done"))
    t_plot_end = t
    # pad the pen's still segments (lift pauses) into the motion keys
    total = dist[-1]
    key_points, key_times = [], []
    # dist/times are paired except for pauses; rebuild pairs in order
    pairs = list(zip(times, dist))
    for tt, dd in pairs:
        key_times.append(tt / t_plot_end)
        key_points.append(dd / total)

    # ---- G-code panel --------------------------------------------------------------------
    preamble = [
        (0.00, "; nitish.gcode", ""),
        (0.08, "; Handwriting-Machine, 2020", ""),
        (0.16, "; ATmega16 + 2x A4988 + servo pen", ""),
        (0.24, "; 54.35 steps/mm, 155x155 mm bed", ""),
        (0.36, "G21", "; mm"),
        (0.44, "M05", "; pen up (servo 90)"),
        (0.56, g00(start), ""),
    ]
    lines = preamble + gcode
    lines.append((t_plot_end + 0.6, "; next: anything.", ""))
    gx0, gy0, lh, rows = 40, 104, 20, 18
    g_total = lines[-1][0] + 0.2
    row_events, clip_events, scroll_events = [], [], []
    for i, (tt, _, _) in enumerate(lines):
        row = min(i, rows - 1)
        row_events.append((tt, f(gy0 + row * lh)))
        clip_events.append((tt, f((row + 1) * lh)))
        scroll_events.append((tt, f"0,{f(-max(0, i - rows + 1) * lh)}"))
    gl = []
    for i, (_, code, cmt) in enumerate(lines):
        y = gy0 + 14 + i * lh
        if code.startswith(";"):
            gl.append(mono_text(gx0, y, code, 12.5, DIM, fit=False))
            continue
        color = AMBER if code.startswith("M0") else (CYAN if code.startswith("G01") else MUTED)
        gl.append(
            f'<text x="{gx0}" y="{y}" font-family="{MONO}" font-size="12.5" xml:space="preserve">'
            f'<tspan fill="{color}">{esc(code)}</tspan><tspan fill="{DIM}">{esc("  " + cmt) if cmt else ""}</tspan></text>'
        )
    gcode_svg = f"""
<g>
  <rect x="20" y="60" width="356" height="420" rx="12" fill="{BG_ALT}" stroke="{BORDER_SOFT}"/>
  {mono_text(40, 86, "nitish.gcode", 12, CYAN, fit=False)}
  {mono_text(356, 86, "G01 / M03 / M05", 11, DIM, fit=False, anchor="end")}
  <line x1="20" y1="96" x2="376" y2="96" stroke="{BORDER_SOFT}"/>
  <clipPath id="gwin"><rect x="24" y="{gy0}" width="348" height="0">{discrete("height", clip_events, g_total)}</rect></clipPath>
  <rect x="24" y="{gy0}" width="348" height="{lh}" fill="{CYAN}" opacity="0.10">{discrete("y", row_events, g_total)}</rect>
  <rect x="24" y="{gy0}" width="3" height="{lh}" fill="{CYAN}">{discrete("y", row_events, g_total)}</rect>
  <g clip-path="url(#gwin)"><g>
    <animateTransform attributeName="transform" type="translate" calcMode="discrete" dur="{f(g_total)}s" fill="freeze"
      keyTimes="{';'.join(f'{min(e[0], g_total) / g_total:.5f}' for e in [(0, '0,0')] + scroll_events[1:])}"
      values="{';'.join(e[1] for e in [(0, '0,0')] + scroll_events[1:])}"/>
    {''.join(gl)}
  </g></g>
</g>"""

    # ---- bed, drawn strokes, pen -------------------------------------------------------
    main_d = seg_path(segs)
    draw_css = [
        f".ink{{fill:none;stroke:{TEXT};stroke-width:4.2;stroke-linecap:round;stroke-linejoin:round}}",
        f"#main{{stroke-dasharray:{f(main_len + 2)};stroke-dashoffset:{f(main_len + 2)};"
        f"animation:draw {T_DRAW}s linear {T_START}s forwards}}",
        "@keyframes draw{to{stroke-dashoffset:0}}",
        ".dot{stroke-width:6.5}",
    ]
    lift_svg = []
    for i, (a, b, t0, td) in enumerate(lift_draws):
        L = math.dist(a, b) + 1
        draw_css.append(
            f"#lift{i}{{stroke-dasharray:{f(L)};stroke-dashoffset:{f(L)};animation:draw {td}s linear {f(t0)}s forwards}}"
        )
        lift_svg.append(f'<path id="lift{i}" class="ink{" dot" if L < 6 else ""}" d="M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}"/>')

    pen_ev = [(0, "0")]
    for a, b in pen_down:
        pen_ev += [(a, "1"), (b, "0")]
    pen_svg = f"""
<g clip-path="url(#bedclip)">
  <g>
    <animateMotion dur="{f(t_plot_end)}s" fill="freeze" calcMode="linear"
      path="{''.join(motion)}" keyPoints="{';'.join(f'{k:.5f}' for k in key_points)}" keyTimes="{';'.join(f'{k:.5f}' for k in key_times)}"/>
    <line x1="0" y1="-800" x2="0" y2="800" stroke="{CYAN}" stroke-opacity="0.16"/>
    <line x1="-1200" y1="0" x2="1200" y2="0" stroke="{CYAN}" stroke-opacity="0.16"/>
    <circle r="13" fill="none" stroke="{CYAN}" stroke-width="1.6" opacity="0.9"/>
    <path d="M-20 0h-6M20 0h6M0 -20v-6M0 20v6" stroke="{CYAN}" stroke-width="1.6"/>
    <circle r="4.5" fill="{AMBER}" opacity="0">{discrete("opacity", pen_ev, t_plot_end + 0.01)}</circle>
  </g>
</g>"""

    bx0, by0, bx1, by1 = BED
    bed_svg = f"""
<clipPath id="bedclip"><rect x="{bx0}" y="{by0}" width="{bx1 - bx0}" height="{by1 - by0}" rx="12"/></clipPath>
<rect x="{bx0}" y="{by0}" width="{bx1 - bx0}" height="{by1 - by0}" rx="12" fill="{BG_ALT}" stroke="{BORDER_SOFT}"/>
<rect x="{bx0}" y="{by0}" width="{bx1 - bx0}" height="{by1 - by0}" rx="12" fill="url(#grid)"/>
{mono_text(bx1 - 16, by1 - 14, "155 x 155 mm", 11, DIM, fit=False, anchor="end")}
<path id="main" class="ink" d="{main_d}"/>
{''.join(lift_svg)}"""

    # ---- words ----------------------------------------------------------------------------
    t_words = t_plot_end + 0.2
    name_s = "NITISH SUNDARRAJ  ·  MONTRÉAL"
    tag = "I can build anything I put my mind to."
    c1, tag_el = typed(OX, 398, tag, 28, TEXT, t_words + 0.5, 0.045, cid="ctag", caret=None,
                       extra='font-weight="600"')
    t_rot = t_words + 0.5 + len(tag) * 0.045 + 0.6

    phrases = [
        ("a robot that plants its own seed rows", AMBER),
        ("a 5-stage MIPS pipeline, cycle-exact", CYAN),
        ("multipliers out of nothing but full adders", CYAN),
        ("F1 telemetry streamed over a CAN bus", GREEN),
        ("a particle filter that finds a lost robot", GREEN),
        ("live auctions on serverless AWS", VIOLET),
        ("a pH controller that keeps roots alive", AMBER),
        ("proofs that a broken netlist is fixed", CYAN),
        ("a robot hand you steer with gestures", AMBER),
        ("a licence store wired to Stripe", VIOLET),
    ]
    slot, ty, bk = 3.4, 0.032, 0.012
    cycle = slot * len(phrases)
    rx, ry, rs = OX + len("↳ built: ") * MONO_ADV * 19, 442, 19
    rot_defs, rot_els, caret_ev = [], [], []
    for j, (p, color) in enumerate(phrases):
        s0 = j * slot
        hold = slot - len(p) * (ty + bk) - 0.35
        d, e = typed(rx, ry, p, rs, color, s0 + 0.05, ty, dur=cycle, hold=hold, back=bk, cid=f"rot{j}",
                     begin=f"{f(t_rot)}s", repeat="indefinite")
        rot_defs.append(d)
        rot_els.append(e)
        cw = MONO_ADV * rs
        caret_ev += [(s0 + 0.05 + i * ty, f(rx + i * cw + 1)) for i in range(1, len(p) + 1)]
        t_back = s0 + 0.05 + len(p) * ty + hold
        caret_ev += [(t_back + i * bk, f(rx + (len(p) - i) * cw + 1)) for i in range(1, len(p) + 1)]
    caret = (
        f'<rect x="{f(rx)}" y="{ry - 16}" width="10" height="20" fill="{MUTED}" class="blink" opacity="0">'
        f'<set attributeName="opacity" to="1" begin="{f(t_rot)}s" fill="freeze"/>'
        + discrete("x", caret_ev, cycle, f"{f(t_rot)}s", "indefinite", initial=f(rx + 1))
        + "</rect>"
    )

    words_svg = f"""
<g class="fadein" style="animation-delay:{f(t_words)}s">
  {mono_text(OX, 352, name_s, 14, CYAN, fit=False, extra='letter-spacing="2.4"')}
</g>
{tag_el}
<g class="fadein" style="animation-delay:{f(t_rot)}s">{mono_text(OX, ry, "↳ built:", rs, DIM)}</g>
{''.join(rot_els)}
{caret}"""

    # ---- chrome ---------------------------------------------------------------------------
    chrome = f"""
<circle cx="28" cy="30" r="6" fill="{RED}" opacity="0.85"/>
<circle cx="48" cy="30" r="6" fill="{AMBER}" opacity="0.85"/>
<circle cx="68" cy="30" r="6" fill="{GREEN}" opacity="0.85"/>
{mono_text(92, 34, "handwriting-machine  ~  plotting nitish.gcode", 12.5, DIM, fit=False)}
<circle cx="1036" cy="30" r="4.5" fill="{GREEN}" class="pulse"/>
{mono_text(1048, 34, "12 labs live", 12.5, GREEN, fit=False)}
<line x1="0" y1="48" x2="{W}" y2="48" stroke="{BORDER_SOFT}"/>"""

    css = "\n".join(draw_css + [
        ".fadein{opacity:0;animation:fade .6s ease forwards}",
        "@keyframes fade{to{opacity:1}}",
        ".blink{animation:blink 1s steps(1) infinite}",
        "@keyframes blink{50%{opacity:0}}",
        ".pulse{animation:pulse 1.6s ease-in-out infinite}",
        "@keyframes pulse{50%{opacity:.25}}",
        "@media (prefers-reduced-motion: reduce){#main,[id^=lift]{animation-duration:.01s!important;animation-delay:0s!important}}",
    ])
    body = f"""<defs>{grid_pattern("grid")}{c1}{''.join(rot_defs)}</defs>
{panel(W, H)}
{chrome}
{gcode_svg}
{bed_svg}
{pen_svg}
{words_svg}"""
    return doc(W, H, "Nitish Sundarraj: I can build anything I put my mind to.", css, body,
               "A pen plotter writes 'nitish' in cursive from streaming G-code, then types: "
               "I can build anything I put my mind to.")
