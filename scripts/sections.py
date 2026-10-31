"""Page sections: the abstraction stack, the rebuild log and the footer."""

from svgkit import (AMBER, BG, BG_ALT, BORDER, BORDER_SOFT, CYAN, DIM, GREEN, MONO, MONO_ADV, MUTED, PANEL, RED,
                    SANS, TEXT, VIOLET, doc, esc, f, grid_pattern, mono_text, panel, text, typed)

MACHINE, SILICON, SIGNAL, CLOUD = AMBER, CYAN, GREEN, VIOLET

# ---------------------------------------------------------------------------------------------
# The stack: every layer from gates to UI has a project of mine on it.

LAYERS = [  # top to bottom
    ("INTERFACES", [("Le Crimson", CLOUD), ("12 lab sites", CLOUD)], "React 19 · TypeScript · three.js · SVG"),
    ("CLOUD", [("AuctionHub", CLOUD), ("SoftHub", CLOUD)], "Lambda · DynamoDB streams · WebSockets · Stripe"),
    ("ALGORITHMS", [("Monte Carlo Localization", SIGNAL), ("RTMC-HG", MACHINE)], "particle filters · gesture classifiers"),
    ("BUSES", [("F1 CAN Telemetry", SIGNAL), ("FARM-E link", MACHINE)], "CAN 500 kbit/s · CRC-8 frames · UDP"),
    ("MACHINES", [("FARM-E", MACHINE), ("Hydroponinator", MACHINE), ("Handwriting-Machine", MACHINE)], "tracks · steppers · servos · pumps"),
    ("FIRMWARE", [("ATmega2560", MACHINE), ("UNO + ESP8266", MACHINE)], "non-blocking loops · watchdogs · EEPROM"),
    ("VERIFICATION", [("Calc1/Calc3", SILICON), ("DDS formal", SILICON)], "SystemVerilog · equivalence · k-induction"),
    ("RTL", [("mini-MIPS", SILICON), ("Arithmetic Unit", SILICON)], "VHDL-2008 · 5-stage pipeline · Yosys"),
    ("GATES", [("full adders", SILICON), ("Dadda trees", SILICON)], "carry-save arrays · ripple carries"),
]


def stack():
    W, top, rh, gap = 1200, 132, 50, 8
    n = len(LAYERS)
    H = top + n * (rh + gap) + 26
    climb, cycle = 5.4, 9.0
    rows, css = [], [
        ".pulse{animation:climb %ss linear infinite}" % cycle,
        "@keyframes climb{0%%{transform:translateY(0);opacity:0}4%%{opacity:1}%s%%{transform:translateY(-%spx);opacity:1}"
        "%s%%{opacity:0}100%%{transform:translateY(-%spx);opacity:0}}" % (
            f(climb / cycle * 100), (n - 1) * (rh + gap), f(climb / cycle * 100 + 6), (n - 1) * (rh + gap)),
    ]
    for i, (name, chips, tech) in enumerate(LAYERS):
        y = top + i * (rh + gap)
        k = n - 1 - i  # 0 at the bottom
        on = 2 + (climb / (n - 1)) * k / cycle * 100
        css.append(
            f"@keyframes on{i}{{0%,{f(on - 0.1)}%{{opacity:0}}{f(on + 2)}%,88%{{opacity:1}}96%,100%{{opacity:0}}}}"
            f".on{i}{{animation:on{i} {cycle}s linear infinite}}"
        )
        chip_svg, cx = [], 330
        for label, color in chips:
            w = len(label) * MONO_ADV * 15 + 36
            chip_svg.append(
                f'<rect x="{f(cx)}" y="{y + 10}" width="{f(w)}" height="30" rx="15" fill="{PANEL}" stroke="{BORDER}"/>'
                f'<circle cx="{f(cx + 14)}" cy="{y + 25}" r="4" fill="{color}"/>'
                + mono_text(cx + 25, y + 30, label, 15, TEXT)
            )
            cx += w + 10
        rows.append(f"""
<g>
  <rect x="96" y="{y}" width="1078" height="{rh}" rx="10" fill="{BG_ALT}" stroke="{BORDER_SOFT}"/>
  <rect x="96" y="{y}" width="1078" height="{rh}" rx="10" fill="{CYAN}" fill-opacity="0.05" stroke="{CYAN}" stroke-opacity="0.55" class="on{i}" opacity="0"/>
  <circle cx="60" cy="{y + rh / 2}" r="5" fill="{BG_ALT}" stroke="{BORDER}" stroke-width="2"/>
  <circle cx="60" cy="{y + rh / 2}" r="5" fill="{CYAN}" class="on{i}" opacity="0"/>
  {mono_text(114, y + 31, f"{k + 1:02d}", 14, DIM)}
  {mono_text(146, y + 31, name, 15, MUTED, extra='letter-spacing="1"', fit=False)}
  {''.join(chip_svg)}
  {text(1154, y + 31, tech, 15, DIM, anchor="end")}
</g>""")
    bus_top, bus_bot = top + rh / 2, top + (n - 1) * (rh + gap) + rh / 2
    body = f"""
<defs>{grid_pattern("g2", 24)}
<radialGradient id="glow"><stop offset="0" stop-color="{CYAN}" stop-opacity=".9"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient></defs>
{panel(W, H)}
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#g2)" opacity=".5"/>
{mono_text(40, 54, "// range", 15, CYAN, fit=False)}
{text(40, 98, "From a full adder to a WebSocket.", 38, TEXT, 700)}
{text(1160, 98, "every layer has something of mine running on it", 18, MUTED, anchor="end")}
<line x1="60" y1="{bus_top}" x2="60" y2="{bus_bot}" stroke="{BORDER}" stroke-width="2"/>
{''.join(rows)}
<g class="pulse loop"><circle cx="60" cy="{bus_bot}" r="16" fill="url(#glow)"/><circle cx="60" cy="{bus_bot}" r="4" fill="{TEXT}"/></g>
"""
    return doc(W, H, "From a full adder to a WebSocket", "\n".join(css), body,
               "Nine layers of abstraction, from gates and RTL up through firmware, machines, buses, algorithms, "
               "cloud and interfaces, each with projects built on it.")


# ---------------------------------------------------------------------------------------------
# The rebuild log: old projects in, playable labs out.

LOG = [  # oldest first, dated from the original projects
    ("2019", "FARM-E-Plantation-Robot", "FARM-E Lab", "both boards' firmware, co-simulated", MACHINE),
    ("2020", "Automated-Hydroponics-System", "Hydroponinator Lab", "pH in band 100% of a 14-day grow", MACHINE),
    ("2021", "RTMC-HG", "RTMC-HG Lab", "20 gestures, 83 tests", MACHINE),
    ("2022", "le-crimson-frontend", "Le Crimson v2", "React 19, WCAG 2.1 AA in CI", CLOUD),
    ("2023", "mini-MIPS", "Pipeline Lab", "1,000 random programs, cycle-exact", SILICON),
    ("2023", "VHDL arithmetic unit", "Arithmetic Unit Lab", "didn't compile -> 83 runs green", SILICON),
    ("2023", "MATLAB particle filter", "Monte Carlo Localization", "4 cm from the wall on a real log", SIGNAL),
    ("2024", "Calc1/Calc3 verification", "Calc Lab", "14/14 bugs caught, 2024 fails root-caused", SILICON),
    ("2024", "DDS-Synthesizer", "DDS Formal", "14 netlist bugs repaired in ~5 s", SILICON),
    ("2024", "SoftHubGlobal", "SoftHub", "Stripe -> licence key, ~US$2/month", CLOUD),
    ("2024", "AuctionSystem", "AuctionHub", "bid p95 43 ms, 0 lost bids", CLOUD),
    ("2025", "F1-CAN-Telemetry", "F1 CAN Telemetry Lab", "2023 Canadian GP over CAN", SIGNAL),
]


def rebuild_log():
    W, x0, lh, size = 1200, 40, 34, 16
    y0 = 146
    H = y0 + len(LOG) * lh + 132
    cmd = './rebuild --since 2019 --until "you can play with it"'
    t0, step = 0.4, 0.028
    t_cmd_end = t0 + len(cmd) * step
    cycle = 16.0
    defs, els, css = [], [], [f".blink{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}"]

    d, e = typed(x0 + 28 * MONO_ADV * size, 104, cmd, size, TEXT, t0, step, dur=cycle, hold=cycle - t_cmd_end - 0.6,
                 back=0.0, cid="cmd", repeat="indefinite")
    defs.append(d)
    els.append(e)

    cols = [x0, 100, 430, 680]  # year, old, new, proof (16px mono = 9.6px per glyph)
    head_y = y0 - 8
    for i, (yr, old, new, note, color) in enumerate(LOG):
        y = y0 + 46 + i * lh
        t_on = t_cmd_end + 0.5 + i * 0.32
        on = t_on / cycle * 100
        css.append(f"@keyframes r{i}{{0%,{f(on)}%{{opacity:0;transform:translateX(-8px)}}"
                   f"{f(on + 2)}%,95%{{opacity:1;transform:none}}100%{{opacity:0}}}}"
                   f".r{i}{{animation:r{i} {cycle}s ease-out infinite}}")
        els.append(f"""
<g class="r{i} loop" opacity="0">
  {mono_text(cols[0], y, yr, size, DIM)}
  {mono_text(cols[1], y, old, size, MUTED)}
  {mono_text(cols[2] - 48, y, "->", size, DIM)}
  <circle cx="{cols[2] - 12}" cy="{y - 5.5}" r="4.5" fill="{color}"/>
  {mono_text(cols[2], y, new, size, TEXT)}
  {mono_text(cols[3], y, "OK", size, GREEN, extra='font-weight="700"')}
  {mono_text(cols[3] + 34, y, note, size, MUTED)}
</g>""")
    t_sum = t_cmd_end + 0.5 + len(LOG) * 0.32 + 0.4
    on = t_sum / cycle * 100
    css.append(f"@keyframes sum{{0%,{f(on)}%{{opacity:0}}{f(on + 3)}%,95%{{opacity:1}}100%{{opacity:0}}}}"
               f".sum{{animation:sum {cycle}s linear infinite}}")
    ys = y0 + 46 + len(LOG) * lh + 26
    els.append(f"""
<g class="sum loop" opacity="0">
  <line x1="{x0}" y1="{ys - 26}" x2="{W - 40}" y2="{ys - 26}" stroke="{BORDER}" stroke-dasharray="4 6"/>
  <text x="{x0}" y="{ys + 4}" font-family="{MONO}" font-size="17" xml:space="preserve"><tspan fill="{GREEN}" font-weight="700">12 rebuilt</tspan><tspan fill="{MUTED}">  ·  </tspan><tspan fill="{TEXT}">12 running in a browser</tspan><tspan fill="{MUTED}">  ·  </tspan><tspan fill="{AMBER}">0 "works on my machine"</tspan></text>
  <rect x="{x0}" y="{ys + 22}" width="9" height="18" fill="{MUTED}" class="blink"/>
</g>""")
    body = f"""
<defs>{''.join(defs)}</defs>
{panel(W, H, fill="#080B0F")}
<circle cx="28" cy="30" r="6" fill="{RED}" opacity=".85"/><circle cx="48" cy="30" r="6" fill="{AMBER}" opacity=".85"/><circle cx="68" cy="30" r="6" fill="{GREEN}" opacity=".85"/>
{mono_text(92, 35, "~/projects  ·  rebuild season, sep-oct 2026", 14, DIM, fit=False)}
<line x1="0" y1="48" x2="{W}" y2="48" stroke="{BORDER_SOFT}"/>
{mono_text(x0, 104, "nitish@montreal:~/projects$", size, GREEN, fit=True)}
<line x1="{x0}" y1="{head_y - 4}" x2="{W - 40}" y2="{head_y - 4}" stroke="{BORDER_SOFT}"/>
{mono_text(cols[0], head_y + 16, "YEAR", 13, DIM, fit=False, extra='letter-spacing="1.5"')}
{mono_text(cols[1], head_y + 16, "WHAT I HAD", 13, DIM, fit=False, extra='letter-spacing="1.5"')}
{mono_text(cols[2], head_y + 16, "WHAT IT IS NOW", 13, DIM, fit=False, extra='letter-spacing="1.5"')}
{mono_text(cols[3], head_y + 16, "PROOF", 13, DIM, fit=False, extra='letter-spacing="1.5"')}
{''.join(els)}"""
    return doc(W, H, "The rebuild log", "\n".join(css), body,
               "A terminal lists twelve past projects, from 2019 to 2025, each rebuilt in 2026 as an interactive lab, "
               "with one line of evidence each.")


# ---------------------------------------------------------------------------------------------
# The coursework: all 68 courses as element-style tiles, stacked year by year and coloured by
# layer (people at the base, software on top). Mirrors js/data/courses.js on the portfolio.

LAYER_KEY = [  # bottom to top: (id, legend label, colour)
    ("people", "PEOPLE", "#C9D3DE"),
    ("math", "MATH", "#ff6b6b"),
    ("mech", "MECHANICS", "#ff8a3d"),
    ("power", "POWER", "#ffb020"),
    ("control", "CONTROL", "#e3d633"),
    ("embedded", "EMBEDDED", "#a3e635"),
    ("silicon", "DIGITAL HW", "#34d399"),
    ("robotics", "ROBOTICS", "#22d3ee"),
    ("data", "VISION · ML", "#60a5fa"),
    ("cloud", "SOFTWARE", "#a78bfa"),
]

TERMS = [  # (label, school, [(symbol, short name, layer)])
    ("Year 1", "bachelors", [
        ("Ve", "Value Education", "people"), ("Fr", "French", "people"), ("Ns", "NSO", "people"),
        ("Ps", "Professional Skills", "people"), ("En", "English", "people"), ("Ga", "General Aptitude", "people"),
        ("Ci", "Constitution of India", "people"), ("Yo", "Yoga: Mind & Body", "people"),
        ("Cl", "Calculus & Lin. Algebra", "math"), ("Cx", "Complex Analysis", "math"),
        ("Ph", "Physics: EM, QM, Optics", "math"), ("Ch", "Chemistry", "math"),
        ("Ws", "Mech & Civil Workshop", "mech"), ("Eg", "Engineering Graphics", "mech"),
        ("Ee", "Electrical & Electronics", "power"), ("Pf", "Programming Basics", "cloud"),
    ]),
    ("Year 2", "bachelors", [
        ("Se", "Social Engineering", "people"), ("Ss", "Social Skills", "people"),
        ("Es", "Environmental Science", "people"), ("Mp", "Management Principles", "people"),
        ("Ct", "Creative Thinking", "people"),
        ("Tb", "Transforms & BVPs", "math"), ("Nm", "Numerical Methods", "math"), ("Bi", "Biology", "math"),
        ("Th", "Thermo & Heat Transfer", "mech"), ("Sf", "Solids & Fluids", "mech"),
        ("Kd", "Kinematics & Dynamics", "mech"), ("Fp", "Fluid Power Systems", "mech"),
        ("Em", "Electrical Machines", "power"), ("Sd", "Solid-State Devices", "power"), ("Lb", "E&E Laboratory", "power"),
        ("Sy", "System Dynamics", "control"), ("Dp", "Digital Systems & µP", "silicon"),
    ]),
    ("Year 3", "bachelors", [
        ("Mo", "MOOC I", "people"), ("At", "Analytical Thinking", "people"), ("Ia", "Indian Art Form", "people"),
        ("Ek", "Employability Skills", "people"), ("Co", "Comprehension", "people"),
        ("Tk", "Traditional Knowledge", "people"), ("S2", "Seminar II", "people"),
        ("Cp", "Competitive Prof. Skills", "people"),
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


def coursework():
    order = {k: i for i, (k, _, _) in enumerate(LAYER_KEY)}
    colour = {k: c for k, _, c in LAYER_KEY}
    symbols = [sym for _, _, cs in TERMS for sym, _, _ in cs]
    assert len(symbols) == len(set(symbols)) == 68, "symbols must be unique, 68 courses"

    W, cw, gap, school_gap = 1200, 200, 20, 40
    th, step = 28, 32
    tallest = max(len(cs) for _, _, cs in TERMS)
    top, base = 196, 196 + tallest * step
    H = base + 104
    x0 = (W - (len(TERMS) * cw + (len(TERMS) - 2) * gap + school_gap)) / 2
    cycle, fade, drop0, drop1 = 16.0, 56.0, 62.0, 90.0  # % of the cycle: hold, clear, then restack

    css, tiles, axis = [], [], []
    xs, n_total, k = [], len(symbols), 0
    for c, (label, school, courses) in enumerate(TERMS):
        x = x0 + c * (cw + gap) + (school_gap - gap if school == "masters" else 0)
        xs.append(x)
        stack = sorted(courses, key=lambda t: order[t[2]])  # bottom-up
        for j, (sym, name, layer) in enumerate(stack):
            y = base - (j + 1) * step + (step - th)
            t = drop0 + (drop1 - drop0) * k / (n_total - 1)
            out = fade + 3 * (1 - j / tallest)  # the top of each stack clears first
            css.append(f".c{k}{{animation:c{k} {cycle}s ease-out infinite}}"
                       f"@keyframes c{k}{{0%,{f(out)}%{{opacity:1;transform:none}}{f(out + 2)}%,{f(t)}%{{opacity:0;"
                       f"transform:translateY(-36px)}}{f(t + 2.2)}%,100%{{opacity:1;transform:none}}}}")
            col = colour[layer]
            tiles.append(
                f'<g class="c{k} loop">'
                f'<rect x="{f(x)}" y="{y}" width="{cw}" height="{th}" rx="6" fill="{PANEL}" stroke="{BORDER}"/>'
                f'<rect x="{f(x)}" y="{y}" width="{th + 6}" height="{th}" rx="6" fill="{col}"/>'
                + mono_text(x + (th + 6) / 2, y + 19, sym, 13, BG, extra='font-weight="700"', fit=False, anchor="middle")
                + text(x + th + 14, y + 19, name, 12.5, TEXT)
                + "</g>")
            k += 1
        y_top = base - len(courses) * step
        axis.append(mono_text(x + cw / 2, y_top - 6, f"{len(courses)}", 15, MUTED, fit=False, anchor="middle"))
        axis.append(mono_text(x + cw / 2, base + 26, label, 14, TEXT, fit=False, anchor="middle"))

    # school brackets under the axis
    def bracket(xa, xb, label, col):
        yb = base + 62
        return (f'<path d="M{f(xa)} {yb}v8H{f(xb)}v-8" fill="none" stroke="{col}" stroke-opacity=".6"/>'
                + mono_text((xa + xb) / 2, yb + 26, label, 12, col, fit=False, anchor="middle",
                            extra='letter-spacing="1.5"'))
    axis.append(bracket(xs[0], xs[3] + cw, "BACHELOR'S · MECHATRONICS ENG.", AMBER))
    axis.append(bracket(xs[4], xs[4] + cw, "MASTER'S · ECE", CYAN))
    divider = (f'<line x1="{f(xs[4] - school_gap / 2)}" y1="{top - 10}" x2="{f(xs[4] - school_gap / 2)}" '
               f'y2="{base + 4}" stroke="{BORDER}" stroke-dasharray="3 6"/>')

    # legend: one chip per layer, with its course count
    counts = {key: 0 for key, _, _ in LAYER_KEY}
    for _, _, cs in TERMS:
        for _, _, layer in cs:
            counts[layer] += 1
    chips, lx = [], 40
    for key, label, col in reversed(LAYER_KEY):  # software first, reading left to right
        s = f"{label} {counts[key]}"
        w = len(s) * MONO_ADV * 12 + 26
        chips.append(f'<rect x="{f(lx)}" y="128" width="12" height="12" rx="3" fill="{col}"/>'
                     + mono_text(lx + 18, 139, s, 12, MUTED, fit=False))
        lx += w
    body = f"""
<defs>{grid_pattern("g3", 24)}</defs>
{panel(W, H)}
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#g3)" opacity=".5"/>
{mono_text(40, 54, "// coursework", 15, CYAN, fit=False)}
{text(40, 98, "68 courses, stacked year by year.", 38, TEXT, 700)}
{text(1160, 98, "people at the base, software on top", 18, MUTED, anchor="end")}
{''.join(chips)}
<line x1="40" y1="{base + 4}" x2="{W - 40}" y2="{base + 4}" stroke="{BORDER}"/>
{divider}
{''.join(tiles)}
{''.join(axis)}
"""
    return doc(W, H, "68 courses, stacked year by year", "\n".join(css), body,
               "Every course from a Bachelor's in Mechatronics Engineering and a Master's in Electrical and "
               "Computer Engineering, drawn as periodic-table tiles stacked by year and "
               "coloured by layer, from people and math at the base up to digital hardware, robotics and software.")


# ---------------------------------------------------------------------------------------------

def footer():
    W, H = 1200, 196
    css = [
        ".blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}",
        ".bar{animation:bar 4.5s cubic-bezier(.6,0,.3,1) infinite;transform-box:fill-box;transform-origin:left}",
        "@keyframes bar{0%{transform:scaleX(0)}70%,100%{transform:scaleX(1)}}",
        ".shine{animation:shine 4.5s linear infinite}@keyframes shine{0%,70%{opacity:0}78%{opacity:1}100%{opacity:0}}",
    ]
    body = f"""
{panel(W, H)}
{mono_text(40, 56, "// queue", 15, CYAN, fit=False)}
{text(40, 104, "Next build: yours?", 38, TEXT, 700)}
{text(40, 146, "If it can be built, I'd like to try. If it can't, I'd like to find out why.", 20, MUTED)}
<rect x="860" y="84" width="300" height="14" rx="7" fill="{BG_ALT}" stroke="{BORDER}"/>
<rect x="862" y="86" width="296" height="10" rx="5" fill="{CYAN}" class="bar loop"/>
<rect x="862" y="86" width="296" height="10" rx="5" fill="{TEXT}" class="shine" opacity="0"/>
{mono_text(860, 128, "loading next project", 15, DIM, fit=False)}
<rect x="1046" y="114" width="9" height="17" fill="{DIM}" class="blink"/>
"""
    return doc(W, H, "Next build: yours?", "\n".join(css), body)
