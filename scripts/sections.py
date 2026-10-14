"""Page sections: the abstraction stack, the rebuild log and the footer."""

from svgkit import (AMBER, BG_ALT, BORDER, BORDER_SOFT, CYAN, DIM, GREEN, MONO, MONO_ADV, MUTED, PANEL, RED,
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
    ("2023", "COEN 6501 arithmetic unit", "Arithmetic Unit Lab", "didn't compile -> 83 runs green", SILICON),
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
