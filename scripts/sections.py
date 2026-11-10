"""Page sections: the abstraction stack, the coursework map and the footer."""

from svgkit import (BG, BG_ALT, BORDER, BORDER_SOFT, DIM, EASE, MONO_ADV, MUTED, PANEL, TEXT, WHITE, doc, eyebrow, f,
                    headline, mono_text, panel, text)

# ---------------------------------------------------------------------------------------------
# The stack: every layer from gates to UI has a project of mine on it.

LAYERS = [  # top to bottom
    ("INTERFACES", ["Le Crimson", "12 lab sites"], "React 19 · TypeScript · three.js · SVG"),
    ("CLOUD", ["AuctionHub", "SoftHub"], "Lambda · DynamoDB streams · WebSockets · Stripe"),
    ("ALGORITHMS", ["Monte Carlo Localization", "RTMC-HG"], "particle filters · gesture classifiers"),
    ("BUSES", ["F1 CAN Telemetry", "FARM-E link"], "CAN 500 kbit/s · CRC-8 frames · UDP"),
    ("MACHINES", ["FARM-E", "Hydroponinator", "Handwriting-Machine"], "tracks · steppers · servos · pumps"),
    ("FIRMWARE", ["ATmega2560", "UNO + ESP8266"], "non-blocking loops · watchdogs · EEPROM"),
    ("VERIFICATION", ["Calc1/Calc3", "DDS formal"], "SystemVerilog · equivalence · k-induction"),
    ("RTL", ["mini-MIPS", "Arithmetic Unit"], "VHDL-2008 · 5-stage pipeline · Yosys"),
    ("GATES", ["full adders", "Dadda trees"], "carry-save arrays · ripple carries"),
]



def stack():
    W, top, rh, gap = 1200, 128, 46, 6
    n = len(LAYERS)
    H = top + n * (rh + gap) + 28
    climb, cycle = 5.2, 9.0
    rise = (n - 1) * (rh + gap)
    p_end = climb / cycle * 100
    css = [
        f".sig{{animation:climb {cycle}s linear infinite}}",
        f"@keyframes climb{{0%{{transform:translateY(0);opacity:0}}3%{{opacity:1}}{f(p_end)}%{{transform:translateY(-{rise}px);opacity:1}}"
        f"{f(p_end + 5)}%,100%{{transform:translateY(-{rise}px);opacity:0}}}}",
    ]
    rows = []
    for i, (name, chips, tech) in enumerate(LAYERS):
        y = top + i * (rh + gap)
        k = n - 1 - i  # 0 at the bottom
        on = 1.5 + p_end * k / (n - 1)
        # each row wakes as the signal passes, then settles: a wave, not a wall
        css.append(f"@keyframes on{i}{{0%,{f(on)}%{{opacity:0}}{f(on + 2.5)}%{{opacity:1}}{f(on + 20)}%,100%{{opacity:0}}}}"
                   f".on{i}{{animation:on{i} {cycle}s ease-out infinite}}")
        chip_svg, cx = [], 340
        for label in chips:
            w = len(label) * MONO_ADV * 14 + 28
            chip_svg.append(f'<rect x="{f(cx)}" y="{y + 9}" width="{f(w)}" height="28" rx="14" fill="{PANEL}" stroke="{BORDER}"/>'
                            + mono_text(cx + 14, y + 28, label, 14, TEXT))
            cx += w + 8
        rows.append(f"""
<g>
  <rect x="96" y="{y}" width="1064" height="{rh}" rx="10" fill="{BG_ALT}" stroke="{BORDER_SOFT}"/>
  <g class="on{i} loop" opacity="0">
    <rect x="96" y="{y}" width="1064" height="{rh}" rx="10" fill="url(#wake)" stroke="{WHITE}" stroke-opacity=".7"/>
    <circle cx="60" cy="{y + rh / 2}" r="5" fill="{WHITE}"/>
    {mono_text(146, y + 29, name, 14, WHITE, extra='letter-spacing="1.6"', fit=False)}
  </g>
  <circle cx="60" cy="{y + rh / 2}" r="5" fill="none" stroke="{BORDER}" stroke-width="1.5"/>
  {mono_text(114, y + 29, f"{k + 1:02d}", 13, DIM)}
  {mono_text(146, y + 29, name, 14, MUTED, extra='letter-spacing="1.6"', fit=False)}
  {''.join(chip_svg)}
  {text(1142, y + 29, tech, 14, DIM, anchor="end")}
</g>""")
    bus_top, bus_bot = top + rh / 2, top + (n - 1) * (rh + gap) + rh / 2
    body = f"""
<defs>
<linearGradient id="wake" x1="0" x2="1"><stop offset="0" stop-color="{WHITE}" stop-opacity=".13"/><stop offset=".55" stop-color="{WHITE}" stop-opacity=".02"/><stop offset="1" stop-color="{WHITE}" stop-opacity="0"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{WHITE}" stop-opacity=".8"/><stop offset="1" stop-color="{WHITE}" stop-opacity="0"/></radialGradient>
</defs>
{panel(W, H, fill="#000")}
{eyebrow(40, 50, "RANGE")}
{headline(40, 94, "From a full adder to a WebSocket.")}
{text(1160, 94, "something of mine runs on every layer", 16, MUTED, anchor="end")}
<line x1="60" y1="{bus_top}" x2="60" y2="{bus_bot}" stroke="{BORDER}" stroke-width="1.5"/>
{''.join(rows)}
<g class="sig loop"><circle cx="60" cy="{bus_bot}" r="18" fill="url(#glow)"/><circle cx="60" cy="{bus_bot}" r="3.5" fill="{WHITE}"/></g>
"""
    return doc(W, H, "From a full adder to a WebSocket", "\n".join(css), body,
               "Nine layers of abstraction, from gates and RTL up through firmware, machines, buses, algorithms, "
               "cloud and interfaces, each with projects built on it. A signal climbs through all nine.")


# ---------------------------------------------------------------------------------------------
# The coursework: every course as an element-style tile, stacked year by year. Tiles are shaded by
# layer, people at the base (darkest) up to software (white), and each layer lights up in turn
# across all five columns.

LAYER_KEY = [  # bottom to top: (id, legend label)
    ("people", "PEOPLE"),
    ("math", "MATH"),
    ("mech", "MECHANICS"),
    ("power", "POWER"),
    ("control", "CONTROL"),
    ("embedded", "EMBEDDED"),
    ("silicon", "DIGITAL HW"),
    ("robotics", "ROBOTICS"),
    ("data", "VISION · ML"),
    ("cloud", "SOFTWARE"),
]

TERMS = [  # (label, school, [(symbol, short name, layer)])
    ("Year 1", "bachelors", [
        ("Fr", "French", "people"),
        ("Ps", "Professional Skills", "people"), ("En", "English", "people"),
        ("Cl", "Calculus & Lin. Algebra", "math"), ("Cx", "Complex Analysis", "math"),
        ("Ph", "Physics: EM, QM, Optics", "math"), ("Ch", "Chemistry", "math"),
        ("Ws", "Mech & Civil Workshop", "mech"), ("Eg", "Engineering Graphics", "mech"),
        ("Ee", "Electrical & Electronics", "power"), ("Pf", "Programming Basics", "cloud"),
    ]),
    ("Year 2", "bachelors", [
        ("Mp", "Management Principles", "people"),
        ("Ct", "Creative Thinking", "people"),
        ("Tb", "Transforms & BVPs", "math"), ("Nm", "Numerical Methods", "math"), ("Bi", "Biology", "math"),
        ("Th", "Thermo & Heat Transfer", "mech"), ("Sf", "Solids & Fluids", "mech"),
        ("Kd", "Kinematics & Dynamics", "mech"), ("Fp", "Fluid Power Systems", "mech"),
        ("Em", "Electrical Machines", "power"), ("Sd", "Solid-State Devices", "power"), ("Lb", "E&E Laboratory", "power"),
        ("Sy", "System Dynamics", "control"), ("Dp", "Digital Systems & µP", "silicon"),
    ]),
    ("Year 3", "bachelors", [
        ("At", "Analytical Thinking", "people"),

        ("Pb", "Probability & Statistics", "math"), ("Md", "Machine Design", "mech"),
        ("Pe", "Power Electronics", "power"),
        ("Lc", "Linear & Digital Control", "control"), ("Sc", "Sensors & Signal Cond.", "control"),
        ("Sm", "Smart Sensor Systems", "control"), ("Mm", "MEMS", "control"),
        ("Mc", "MCUs & Embedded", "embedded"), ("Mt", "Elements of Mechatronics", "embedded"),
        ("Ro", "Fundamentals of Robotics", "robotics"), ("Au", "Intelligent Automation", "robotics"),
        ("Da", "Data Analysis (OSS)", "data"),
    ]),
    ("Year 4", "bachelors", [
        ("Mf", "Manufacturing Processes", "mech"), ("Sn", "Sustainable Energy", "power"),
        ("Am", "Applied Mechatronics", "embedded"), ("Dm", "Mechatronics Design", "embedded"),
        ("Mv", "Machine Vision", "data"),
    ]),
    ("Master's", "masters", [
        ("Ca", "Computer Architecture", "silicon"), ("Ds", "Digital System Synthesis", "silicon"),
        ("Fv", "Functional Verification", "silicon"), ("Fo", "Formal Verification", "silicon"),
        ("Rm", "Robotic Manipulators", "robotics"), ("Ar", "Mobile-Robot Autonomy", "robotics"),
        ("Nn", "Neural Networks", "data"),
        ("Sw", "Software Engineering", "cloud"), ("Pc", "Cloud Programming", "cloud"),
        ("Cn", "Cloud Networking", "cloud"),
    ]),
]



def shade(i, n):
    """Grey for layer i of n, dark at the base to white on top, plus a readable ink colour for it."""
    v = round(0x3C + (0xFF - 0x3C) * i / (n - 1))
    return f"#{v:02X}{v:02X}{v:02X}", (BG if v > 0x90 else TEXT)


def coursework():
    order = {k: i for i, (k, _) in enumerate(LAYER_KEY)}
    n_layers = len(LAYER_KEY)
    symbols = [sym for _, _, cs in TERMS for sym, _, _ in cs]
    assert len(symbols) == len(set(symbols)), "course symbols must be unique"

    W, cw, gap, school_gap = 1200, 200, 20, 40
    th, step = 28, 32
    tallest = max(len(cs) for _, _, cs in TERMS)
    top, base = 190, 190 + tallest * step
    H = base + 104
    x0 = (W - (len(TERMS) * cw + (len(TERMS) - 2) * gap + school_gap)) / 2
    n_total = len(symbols)

    # one loop: everything lit, then each layer takes the light in turn, base to top
    cycle, rest = 22.0, 18.0
    slot = (100 - rest) / n_layers
    css = []
    for i in range(n_layers):
        a, b = rest + i * slot, rest + (i + 1) * slot
        stops = [("0%", 1)]
        if i > 0:
            stops += [(f"{f(rest - 1.5)}%", 1), (f"{f(rest)}%", 0.22), (f"{f(a - 1.5)}%", 0.22)]
        stops.append((f"{f(a)}%", 1))
        if i < n_layers - 1:
            stops += [(f"{f(b - 1.5)}%", 1), (f"{f(b)}%", 0.22), ("98.5%", 0.22)]
        stops.append(("100%", 1))
        css.append(f"@keyframes l{i}{{" + "".join(f"{p}{{opacity:{o}}}" for p, o in stops) + f"}}"
                   f".l{i}{{animation:l{i} {cycle}s ease-in-out infinite}}")

    tiles, axis, xs = [], [], []
    for c, (label, school, courses) in enumerate(TERMS):
        x = x0 + c * (cw + gap) + (school_gap - gap if school == "masters" else 0)
        xs.append(x)
        for j, (sym, name, layer) in enumerate(sorted(courses, key=lambda t: order[t[2]])):  # bottom-up
            y = base - (j + 1) * step + (step - th)
            fill, ink = shade(order[layer], n_layers)
            tiles.append(
                f'<g class="l{order[layer]} loop">'
                f'<rect x="{f(x)}" y="{y}" width="{cw}" height="{th}" rx="6" fill="{PANEL}" stroke="{BORDER}"/>'
                f'<rect x="{f(x)}" y="{y}" width="{th + 6}" height="{th}" rx="6" fill="{fill}"/>'
                + mono_text(x + (th + 6) / 2, y + 19, sym, 13, ink, extra='font-weight="700"', fit=False, anchor="middle")
                + text(x + th + 14, y + 19, name, 12.5, TEXT)
                + "</g>")
        y_top = base - len(courses) * step
        axis.append(mono_text(x + cw / 2, y_top - 6, f"{len(courses)}", 14, MUTED, fit=False, anchor="middle"))
        axis.append(mono_text(x + cw / 2, base + 26, label.upper(), 12, TEXT, fit=False, anchor="middle",
                              extra='letter-spacing="2.4"'))

    def bracket(xa, xb, label):
        yb = base + 58
        return (f'<path d="M{f(xa)} {yb}v8H{f(xb)}v-8" fill="none" stroke="{DIM}"/>'
                + mono_text((xa + xb) / 2, yb + 28, label, 11, MUTED, fit=False, anchor="middle",
                            extra='letter-spacing="2.4"'))
    axis.append(bracket(xs[0], xs[3] + cw, "BACHELOR'S · MECHATRONICS ENGINEERING"))
    axis.append(bracket(xs[4], xs[4] + cw, "MASTER'S · ECE"))
    divider = (f'<line x1="{f(xs[4] - school_gap / 2)}" y1="{top - 10}" x2="{f(xs[4] - school_gap / 2)}" '
               f'y2="{base + 4}" stroke="{BORDER}" stroke-dasharray="2 6"/>')

    # legend: one chip per layer with its course count, in the same base-to-top order as the stacks
    counts = {key: 0 for key, _ in LAYER_KEY}
    for _, _, cs in TERMS:
        for _, _, layer in cs:
            counts[layer] += 1
    chips, lx = [], 40
    for i, (key, label) in enumerate(LAYER_KEY):
        s = f"{label} {counts[key]}"
        fill, _ = shade(i, n_layers)
        chips.append(f'<g class="l{i} loop"><rect x="{f(lx)}" y="128" width="12" height="12" rx="3" fill="{fill}"/>'
                     + mono_text(lx + 18, 139, s, 11.5, MUTED, fit=False) + "</g>")
        lx += len(s) * MONO_ADV * 11.5 + 34
    body = f"""
{panel(W, H, fill="#000")}
{eyebrow(40, 50, "COURSEWORK")}
{headline(40, 94, f"{n_total} courses, stacked year by year.")}
{text(1160, 94, "people at the base, software on top", 16, MUTED, anchor="end")}
{''.join(chips)}
<line x1="40" y1="{base + 4}" x2="{W - 40}" y2="{base + 4}" stroke="{BORDER}"/>
{divider}
{''.join(tiles)}
{''.join(axis)}
"""
    return doc(W, H, f"{n_total} courses, stacked year by year", "\n".join(css), body,
               "Selected coursework from a Bachelor's in Mechatronics Engineering and a Master's in Electrical and "
               "Computer Engineering, drawn as periodic-table tiles stacked by year and shaded by layer, from people "
               "and math at the base up to digital hardware, robotics and software. Each layer lights up in turn.")


# ---------------------------------------------------------------------------------------------

def footer():
    W, H = 1200, 200
    bx, by, bw, bh = 936, 76, 224, 52
    css = [
        f".arrow{{animation:arrow 3.2s {EASE} infinite}}@keyframes arrow{{0%,55%,100%{{transform:none}}75%{{transform:translateX(7px)}}}}",
        ".sweep{animation:sweep 6s linear infinite}@keyframes sweep{0%{transform:translateX(-260px)}60%,100%{transform:translateX(1240px)}}",
    ]
    body = f"""
<defs>
<linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="{WHITE}" stop-opacity="0"/><stop offset=".5" stop-color="{WHITE}" stop-opacity=".9"/><stop offset="1" stop-color="{WHITE}" stop-opacity="0"/></linearGradient>
<clipPath id="edge"><rect x="18" y="0" width="{W - 36}" height="2"/></clipPath>
</defs>
{panel(W, H, fill="#000")}
<g clip-path="url(#edge)"><rect class="sweep loop" x="0" y="0" width="240" height="1.5" fill="url(#beam)"/></g>
{eyebrow(40, 50, "NEXT")}
{headline(40, 100, "Next build: yours?", 40)}
{text(40, 144, "If it can be built, I'd like to try. If it can't, I'd like to find out why.", 18, MUTED)}
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{bh / 2}" fill="{TEXT}"/>
{text(bx + 34, by + 33, "Let's connect", 18, BG, 600)}
<g class="arrow loop"><path d="M{bx + bw - 58} {by + bh / 2}h22m-8 -8l8 8l-8 8" fill="none" stroke="{BG}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>
"""
    return doc(W, H, "Next build: yours? Let's connect.", "\n".join(css), body)
