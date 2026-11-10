"""Page sections: the abstraction stack, the coursework map and the footer.

GitHub shows these about two-thirds of their drawn size, so nothing here is set below 15px.
"""

from svgkit import (AI, BG, BG_ALT, BORDER, BORDER_SOFT, CONTROL, DIM, EASE, EMBEDDED, MATH, MECH, MONO_ADV, MUTED,
                    PANEL, PEOPLE, POWER, ROBOTICS, SILICON, SOFTWARE, TEXT, WHITE, doc, f, headline, mono_text, panel,
                    text)

# ---------------------------------------------------------------------------------------------
# The stack: every layer from gates to UI has a project of mine on it.

LAYERS = [  # top to bottom: (layer, colour, projects, tech)
    ("INTERFACES", SOFTWARE, ["Le Crimson", "12 lab sites"], "React · TypeScript · three.js"),
    ("CLOUD", SOFTWARE, ["AuctionHub", "SoftHub"], "Lambda · DynamoDB · WebSockets"),
    ("ALGORITHMS", AI, ["Monte Carlo Localization", "RTMC-HG"], "particle filters · CNNs"),
    ("BUSES", EMBEDDED, ["F1 CAN Telemetry", "FARM-E link"], "CAN · CRC-8 · UDP"),
    ("MACHINES", ROBOTICS, ["FARM-E", "Hydroponinator", "Handwriting-Machine"], "steppers · servos · pumps"),
    ("FIRMWARE", EMBEDDED, ["ATmega2560", "UNO + ESP8266"], "watchdogs · EEPROM"),
    ("VERIFICATION", SILICON, ["Calc1/Calc3", "DDS formal"], "SystemVerilog · k-induction"),
    ("RTL", SILICON, ["mini-MIPS", "Arithmetic Unit"], "VHDL-2008 · Yosys"),
    ("GATES", SILICON, ["full adders", "Dadda trees"], "carry-save · ripple carry"),
]


def stack():
    W, top, rh, gap = 1200, 150, 52, 8
    n = len(LAYERS)
    H = top + n * (rh + gap) + 24
    climb, cycle = 5.2, 9.0
    rise = (n - 1) * (rh + gap)
    p_end = climb / cycle * 100
    css = [
        f".sig{{animation:climb {cycle}s linear infinite}}",
        f"@keyframes climb{{0%{{transform:translateY(0);opacity:0}}3%{{opacity:1}}{f(p_end)}%{{transform:translateY(-{rise}px);opacity:1}}"
        f"{f(p_end + 5)}%,100%{{transform:translateY(-{rise}px);opacity:0}}}}",
    ]
    rows = []
    for i, (name, colour, chips, tech) in enumerate(LAYERS):
        y = top + i * (rh + gap)
        k = n - 1 - i  # 0 at the bottom
        on = 1.5 + p_end * k / (n - 1)
        # each row wakes as the signal passes, then settles: a wave, not a wall
        css.append(f"@keyframes on{i}{{0%,{f(on)}%{{opacity:0}}{f(on + 2.5)}%{{opacity:1}}{f(on + 20)}%,100%{{opacity:0}}}}"
                   f".on{i}{{animation:on{i} {cycle}s ease-out infinite}}")
        chip_svg, cx = [], 300
        for label in chips:
            w = len(label) * MONO_ADV * 17 + 32
            chip_svg.append(f'<rect x="{f(cx)}" y="{y + 9}" width="{f(w)}" height="34" rx="17" fill="{PANEL}" stroke="{BORDER}"/>'
                            + mono_text(cx + 16, y + 32, label, 17, TEXT))
            cx += w + 10
        rows.append(f"""
<g>
  <rect x="96" y="{y}" width="1064" height="{rh}" rx="12" fill="{BG_ALT}" stroke="{BORDER_SOFT}"/>
  <g class="on{i} loop" opacity="0">
    <rect x="96" y="{y}" width="1064" height="{rh}" rx="12" fill="url(#wake{i})" stroke="{colour}" stroke-opacity=".8"/>
    <circle cx="60" cy="{y + rh / 2}" r="6" fill="{colour}"/>
  </g>
  <circle cx="60" cy="{y + rh / 2}" r="6" fill="{BG}" stroke="{colour}" stroke-opacity=".6" stroke-width="1.5"/>
  {mono_text(116, y + 32, name, 17, colour, extra='letter-spacing="1.5" font-weight="600"', fit=False)}
  {''.join(chip_svg)}
  {text(1140, y + 32, tech, 17, MUTED, anchor="end")}
</g>""")
    wakes = "".join(
        f'<linearGradient id="wake{i}" x1="0" x2="1"><stop offset="0" stop-color="{c}" stop-opacity=".16"/>'
        f'<stop offset=".6" stop-color="{c}" stop-opacity=".03"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>'
        for i, (_, c, _, _) in enumerate(LAYERS))
    bus_top, bus_bot = top + rh / 2, top + (n - 1) * (rh + gap) + rh / 2
    body = f"""
<defs>{wakes}
<radialGradient id="glow"><stop offset="0" stop-color="{WHITE}" stop-opacity=".8"/><stop offset="1" stop-color="{WHITE}" stop-opacity="0"/></radialGradient>
</defs>
{panel(W, H, fill="#000")}
{headline(40, 76, "From a full adder to a WebSocket.")}
{text(40, 116, "Something of mine runs on every layer, from logic gates to the browser.", 21, MUTED)}
<line x1="60" y1="{bus_top}" x2="60" y2="{bus_bot}" stroke="{BORDER}" stroke-width="1.5"/>
{''.join(rows)}
<g class="sig loop"><circle cx="60" cy="{bus_bot}" r="20" fill="url(#glow)"/><circle cx="60" cy="{bus_bot}" r="4" fill="{WHITE}"/></g>
"""
    return doc(W, H, "From a full adder to a WebSocket", "\n".join(css), body,
               "Nine layers of abstraction, from gates and RTL up through firmware, machines, buses, algorithms, "
               "cloud and interfaces, each with projects built on it. A signal climbs through all nine.")


# ---------------------------------------------------------------------------------------------
# The coursework: every course as an element-style tile, stacked year by year and coloured by
# layer, people at the base up to software on top. Each layer takes the light in turn.

LAYER_KEY = [  # bottom to top: (id, legend label, colour)
    ("people", "People", PEOPLE),
    ("math", "Math", MATH),
    ("mech", "Mechanics", MECH),
    ("power", "Power", POWER),
    ("control", "Control", CONTROL),
    ("embedded", "Embedded", EMBEDDED),
    ("silicon", "Digital HW", SILICON),
    ("robotics", "Robotics", ROBOTICS),
    ("data", "Vision & ML", AI),
    ("cloud", "Software", SOFTWARE),
]

TERMS = [  # (label, school, [(symbol, short name, layer)]); names fit a tile at 15px
    ("Year 1", "bachelors", [
        ("Fr", "French", "people"),
        ("Ps", "Professional Skills", "people"), ("En", "English", "people"),
        ("Cl", "Calculus & Lin. Algebra", "math"), ("Cx", "Complex Analysis", "math"),
        ("Ph", "Physics: EM, QM", "math"), ("Ch", "Chemistry", "math"),
        ("Ws", "Mech & Civil Workshop", "mech"), ("Eg", "Engineering Graphics", "mech"),
        ("Ee", "Electrical & Electronics", "power"), ("Pf", "Programming Basics", "cloud"),
    ]),
    ("Year 2", "bachelors", [
        ("Mp", "Management Principles", "people"),
        ("Ct", "Creative Thinking", "people"),
        ("Tb", "Transforms & BVPs", "math"), ("Nm", "Numerical Methods", "math"), ("Bi", "Biology", "math"),
        ("Th", "Thermodynamics", "mech"), ("Sf", "Solids & Fluids", "mech"),
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
        ("Mc", "MCUs & Embedded", "embedded"), ("Mt", "Intro to Mechatronics", "embedded"),
        ("Ro", "Robotics Basics", "robotics"), ("Au", "Intelligent Automation", "robotics"),
        ("Da", "Data Analysis (OSS)", "data"),
    ]),
    ("Year 4", "bachelors", [
        ("Mf", "Manufacturing", "mech"), ("Sn", "Sustainable Energy", "power"),
        ("Am", "Applied Mechatronics", "embedded"), ("Dm", "Mechatronics Design", "embedded"),
        ("Mv", "Machine Vision", "data"),
    ]),
    ("Master's", "masters", [
        ("Ca", "Computer Architecture", "silicon"), ("Ds", "Digital Synthesis", "silicon"),
        ("Fv", "Functional Verification", "silicon"), ("Fo", "Formal Verification", "silicon"),
        ("Rm", "Robotic Manipulators", "robotics"), ("Ar", "Mobile Robotics", "robotics"),
        ("Nn", "Neural Networks", "data"),
        ("Sw", "Software Engineering", "cloud"), ("Pc", "Cloud Programming", "cloud"),
        ("Cn", "Cloud Networking", "cloud"),
    ]),
]


def coursework():
    order = {k: i for i, (k, _, _) in enumerate(LAYER_KEY)}
    colour = {k: c for k, _, c in LAYER_KEY}
    n_layers = len(LAYER_KEY)
    symbols = [sym for _, _, cs in TERMS for sym, _, _ in cs]
    assert len(symbols) == len(set(symbols)), "course symbols must be unique"

    W, cw, gap, school_gap = 1200, 212, 14, 30
    th, step, badge = 32, 36, 34
    tallest = max(len(cs) for _, _, cs in TERMS)
    top = 226
    base = top + tallest * step
    H = base + 112
    x0 = (W - (len(TERMS) * cw + (len(TERMS) - 2) * gap + school_gap)) / 2
    n_total = len(symbols)

    # one loop: everything lit and still for a long beat, then each layer takes the light in turn,
    # base to top. Unlit layers only dim to half, so every name stays readable.
    cycle, rest, low = 24.0, 36.0, 0.5
    slot = (100 - rest) / n_layers
    css = []
    for i in range(n_layers):
        a, b = rest + i * slot, rest + (i + 1) * slot
        stops = [("0%", 1)]
        if i > 0:
            stops += [(f"{f(rest - 1.5)}%", 1), (f"{f(rest)}%", low), (f"{f(a - 1.5)}%", low)]
        stops.append((f"{f(a)}%", 1))
        if i < n_layers - 1:
            stops += [(f"{f(b - 1.5)}%", 1), (f"{f(b)}%", low), ("98.5%", low)]
        stops.append(("100%", 1))
        css.append(f"@keyframes l{i}{{" + "".join(f"{p}{{opacity:{o}}}" for p, o in stops) + f"}}"
                   f".l{i}{{animation:l{i} {cycle}s ease-in-out infinite}}")

    tiles, axis, xs = [], [], []
    for c, (label, school, courses) in enumerate(TERMS):
        x = x0 + c * (cw + gap) + (school_gap - gap if school == "masters" else 0)
        xs.append(x)
        for j, (sym, name, layer) in enumerate(sorted(courses, key=lambda t: order[t[2]])):  # bottom-up
            y = base - (j + 1) * step + (step - th)
            tiles.append(
                f'<g class="l{order[layer]} loop">'
                f'<rect x="{f(x)}" y="{y}" width="{cw}" height="{th}" rx="7" fill="{PANEL}" stroke="{BORDER}"/>'
                f'<rect x="{f(x)}" y="{y}" width="{badge}" height="{th}" rx="7" fill="{colour[layer]}"/>'
                + mono_text(x + badge / 2, y + 21, sym, 15, BG, extra='font-weight="700"', fit=False, anchor="middle")
                + text(x + badge + 9, y + 21.5, name, 15, TEXT)
                + "</g>")
        y_top = base - len(courses) * step
        axis.append(mono_text(x + cw / 2, y_top - 9, f"{len(courses)}", 17, MUTED, fit=False, anchor="middle"))
        axis.append(mono_text(x + cw / 2, base + 32, label.upper(), 16, TEXT, fit=False, anchor="middle",
                              extra='letter-spacing="2.4" font-weight="600"'))

    def bracket(xa, xb, label):
        yb = base + 54
        return (f'<path d="M{f(xa)} {yb}v8H{f(xb)}v-8" fill="none" stroke="{DIM}"/>'
                + mono_text((xa + xb) / 2, yb + 34, label, 15, MUTED, fit=False, anchor="middle",
                            extra='letter-spacing="2"'))
    axis.append(bracket(xs[0], xs[3] + cw, "BACHELOR'S · MECHATRONICS ENGINEERING"))
    axis.append(bracket(xs[4], xs[4] + cw, "MASTER'S · ECE"))
    divider = (f'<line x1="{f(xs[4] - school_gap / 2)}" y1="{top - 30}" x2="{f(xs[4] - school_gap / 2)}" '
               f'y2="{base + 4}" stroke="{BORDER}" stroke-dasharray="2 6"/>')

    # legend: one swatch per layer, in the same base-to-top order as the stacks
    chips, lx = [], 40
    for i, (key, label, col) in enumerate(LAYER_KEY):
        chips.append(f'<g class="l{i} loop"><rect x="{f(lx)}" y="148" width="16" height="16" rx="4" fill="{col}"/>'
                     + text(lx + 24, 162, label, 17, TEXT) + "</g>")
        lx += 24 + len(label) * 8.6 + 26
    body = f"""
{panel(W, H, fill="#000")}
{headline(40, 76, f"{n_total} courses, stacked year by year.")}
{text(40, 116, "People and math at the base, software on top.", 21, MUTED)}
{''.join(chips)}
<line x1="40" y1="{base + 4}" x2="{W - 40}" y2="{base + 4}" stroke="{BORDER}"/>
{divider}
{''.join(tiles)}
{''.join(axis)}
"""
    return doc(W, H, f"{n_total} courses, stacked year by year", "\n".join(css), body,
               "Selected coursework from a Bachelor's in Mechatronics Engineering and a Master's in Electrical and "
               "Computer Engineering, drawn as periodic-table tiles stacked by year and coloured by layer, from people "
               "and math at the base up to digital hardware, robotics and software. Each layer lights up in turn.")


# ---------------------------------------------------------------------------------------------

def footer():
    W, H = 1200, 200
    bx, by, bw, bh = 904, 72, 256, 60
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
{headline(40, 92, "Next build: yours?", 48)}
{text(40, 140, "If it can be built, I'd like to try. If it can't, I'd like to find out why.", 21, MUTED)}
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{bh / 2}" fill="{TEXT}"/>
{text(bx + 36, by + 38, "Let's connect", 22, BG, 600)}
<g class="arrow loop"><path d="M{bx + bw - 64} {by + bh / 2}h24m-9 -9l9 9l-9 9" fill="none" stroke="{BG}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g>
"""
    return doc(W, H, "Next build: yours? Let's connect.", "\n".join(css), body)
