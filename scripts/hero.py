"""Header: ground to orbit as a pixel-art indie game screen, for the GitHub README.

The scene is drawn on a 300 x 110 pixel grid and scaled 4x with crisp edges. Every
moving thing snaps to that grid: positions are sampled at 12 fps and played back with
discrete SMIL, so motion has the stepped feel of a sprite game.

The 14 s loop:
  0.0-2.5   A gantry crane in the lights-out factory loads an upper stage onto a truck.
  3.0-6.4   The driverless truck hauls it to the pad.
  6.6-7.4   The stage is stacked on the reusable booster.
  8.0-9.0   T-3, T-2, T-1. Liftoff at 9.0.
 11.0-13.2  The booster comes back, legs out, and lands. "+1".
 13.2-1.6   Nitish, riding in a self-driving car, raises his coffee: "STUCK IT!"

GitHub shows README images through <img>, so this is one self-contained SVG: CSS
keyframes and SMIL only, no script, no fonts (text is drawn from a 3x5 pixel font).
"""

import random

from svgkit import doc, f

PX = 4
LW, LH = 300, 110
W, H = LW * PX, LH * PX
GROUND = 82
CYCLE = 14.0
FPS = 12

# Palette
SKY = ["#05040C", "#0A0818", "#110D26", "#1A1233", "#251640", "#331A4A"]
INK = "#F4F6FB"
GREY1, GREY2, GREY3, GREY4 = "#1B2234", "#2A3246", "#3A4560", "#5B667C"
LIGHT = "#9AA4BA"
WHITE = "#E8EDF7"
AMBER = "#FF9442"
GOLD = "#FFB020"
CYAN = "#38BDF8"
PINK = "#FF4F9A"
GREEN = "#34D399"
RED = "#FF5454"
VIOLET = "#A78BFA"
SKIN = "#A96F51"
SKIN_DK = "#86533B"
HAIR = "#15100E"
HOODIE = "#232B40"
MOUTH = "#4A1915"


# ---------------------------------------------------------------------------- pixel primitives

def r(x, y, w, h, c, extra=""):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{c}"{extra}/>'


def sprite(rows, pal, x=0, y=0):
    """ASCII rows -> horizontal runs of rects. '.' and ' ' are transparent."""
    out = []
    for j, row in enumerate(rows):
        i = 0
        while i < len(row):
            ch = row[i]
            if ch in ". ":
                i += 1
                continue
            k = i
            while k < len(row) and row[k] == ch:
                k += 1
            out.append(r(x + i, y + j, k - i, 1, pal[ch]))
            i = k
    return "".join(out)


FONT = {
    "A": ".#. #.# ### #.# #.#", "B": "##. #.# ##. #.# ##.", "C": ".## #.. #.. #.. .##", "D": "##. #.# #.# #.# ##.",
    "E": "### #.. ##. #.. ###", "F": "### #.. ##. #.. #..", "G": ".## #.. #.# #.# .##", "H": "#.# #.# ### #.# #.#",
    "I": "### .#. .#. .#. ###", "K": "#.# #.# ##. #.# #.#", "L": "#.. #.. #.. #.. ###", "M": "#.# ### ### #.# #.#",
    "N": "##. #.# #.# #.# #.#", "O": ".#. #.# #.# #.# .#.", "P": "##. #.# ##. #.. #..", "R": "##. #.# ##. #.# #.#",
    "S": ".## #.. .#. ..# ##.", "T": "### .#. .#. .#. .#.", "U": "#.# #.# #.# #.# ###", "W": "#.# #.# ### ### #.#",
    "Y": "#.# #.# .#. .#. .#.", "0": "### #.# #.# #.# ###", "1": ".#. ##. .#. .#. ###", "2": "##. ..# .#. #.. ###",
    "3": "##. ..# .#. ..# ##.", "-": "... ... ### ... ...", ":": "... .#. ... .#. ...", "!": ".#. .#. .#. ... .#.",
    "+": "... .#. ### .#. ...", ">": "#.. ##. ### ##. #..", " ": "... ... ... ... ...",
}


def glyph_rows(ch):
    return FONT[ch].split()


def text(s, x, y, c):
    out = []
    for n, ch in enumerate(s.upper()):
        out.append(sprite([row.replace("#", "c") for row in glyph_rows(ch)], {"c": c}, x + n * 4, y))
    return "".join(out)


def text_w(s):
    return len(s) * 4 - 1


# ---------------------------------------------------------------------------- timing

def pct(sec):
    return f"{f(sec / CYCLE * 100)}%"


def kf(name, stops):
    return f"@keyframes {name}{{" + "".join(f"{pct(t)}{{{p}}}" for t, p in stops) + "}"


def toggle(name, spans, invert=False):
    """Hard on/off opacity: on inside each (start, end) span."""
    def on(t):
        return any(a <= t < b or (b == CYCLE and t == CYCLE) for a, b in spans)

    pts = sorted({0.0, CYCLE} | {x for a, b in spans for x in (a, b)})
    stops = [(t, f"opacity:{int(on(t) != invert)}") for t in pts]
    return kf(name, stops) + f".{name}{{animation:{name} {f(CYCLE)}s steps(1,end) infinite}}"


def ease_in(u):
    return u * u


def ease_out(u):
    return 1 - (1 - u) * (1 - u)


def lin(u):
    return u


def track(keys):
    """keys: [(t, (x, y), easing-into-this-key)] -> function t -> (x, y)."""
    def at(t):
        for (t0, p0, _), (t1, p1, e) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                u = 0 if t1 == t0 else e((t - t0) / (t1 - t0))
                return p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u
        return keys[-1][1]
    return at


def stepped(attr, fn, kind="translate", fmt=None):
    """Sample fn at FPS, snap to the pixel grid, emit discrete SMIL with only the changes."""
    frames, last = [], None
    for i in range(int(CYCLE * FPS) + 1):
        t = i / FPS
        v = fn(t)
        val = fmt(v) if fmt else f"{round(v[0])} {round(v[1])}"
        if val != last:
            frames.append((t, val))
            last = val
    times = ";".join(f"{t / CYCLE:.4f}" for t, _ in frames)
    values = ";".join(v for _, v in frames)
    if kind == "animate":
        return (f'<animate attributeName="{attr}" dur="{f(CYCLE)}s" repeatCount="indefinite" calcMode="discrete" '
                f'keyTimes="{times}" values="{values}"/>')
    return (f'<animateTransform attributeName="{attr}" type="{kind}" dur="{f(CYCLE)}s" repeatCount="indefinite" '
            f'calcMode="discrete" keyTimes="{times}" values="{values}"/>')


def moving(fn, inner):
    x, y = fn(0)
    return f'<g transform="translate({round(x)} {round(y)})">{stepped("transform", fn)}{inner}</g>'


# ---------------------------------------------------------------------------- sprites

STAGE = ["..ww..", ".wwww.", ".wwww.", "wwwwww", "pppppp", "wwwwww", "wwccww", "wwwwww", "wwwwww", ".gggg."]
STAGE_PAL = {"w": WHITE, "p": PINK, "c": CYAN, "g": GREY3}


def stage(cls="", x=0, y=0):
    return f'<g class="{cls}">{sprite(STAGE, STAGE_PAL, x, y)}</g>'


def booster_body():
    rows = []
    for j in range(26):
        if j < 18:
            rows.append("hwwwws")
        else:
            rows.append("kddddk" if j % 3 else "kdkddk")
    rows += [".nnnn.", "..nn.."]
    pal = {"h": "#FFFFFF", "w": WHITE, "s": "#B8BFCC", "d": "#8E95A3", "k": "#6E7484", "n": GREY3}
    fins = r(-1, 2, 1, 2, LIGHT) + r(6, 2, 1, 2, LIGHT)
    return sprite(rows, pal) + fins


LEGS_OUT = (r(-1, 21, 1, 1, LIGHT) + r(-2, 22, 1, 1, LIGHT) + r(-3, 23, 1, 1, LIGHT) + r(-4, 24, 1, 1, LIGHT)
            + r(-5, 25, 1, 1, LIGHT) + r(-6, 26, 1, 1, LIGHT) + r(-8, 27, 3, 1, LIGHT)
            + r(6, 21, 1, 1, LIGHT) + r(7, 22, 1, 1, LIGHT) + r(8, 23, 1, 1, LIGHT) + r(9, 24, 1, 1, LIGHT)
            + r(10, 25, 1, 1, LIGHT) + r(11, 26, 1, 1, LIGHT) + r(11, 27, 3, 1, LIGHT))
LEGS_IN = r(-1, 18, 1, 8, LIGHT) + r(6, 18, 1, 8, LIGHT)

FLAME_A = ["hhhh", "hhhh", "yhhy", "yyyy", "yyyy", "oyyo", ".oo.", ".oo.", ".oo.", "..o.", ".o..", "..o."]
FLAME_B = ["hhhh", "hhhh", "yhhy", "yhhy", "yyyy", "yyyy", "oyyo", "oyyo", ".oo.", ".oo.", ".oo.", ".o..", "..o.", ".o..", "..o."]
FLAME_PAL = {"h": "#FFFFFF", "y": GOLD, "o": AMBER}

HEAD = [
    "....kkkkk...",
    "..kkkkkkkkk.",
    ".kkkkkkkkkkk",
    ".kkssssssskk",
    ".kssssssssk.",
    "esswwsswwsse",
    ".sswwsswwss.",
    ".ssssssssss.",
    ".ssssssssss.",
    "..ssssssss..",
    "...dssssd...",
    "....ssss....",
]
HEAD_PAL = {"k": HAIR, "s": SKIN, "e": SKIN_DK, "w": "#FFFFFF", "d": SKIN_DK}


# ---------------------------------------------------------------------------- scenery

def sky():
    out = []
    band_h = 15
    for i, c in enumerate(SKY):
        out.append(r(0, i * band_h, LW, band_h + 1, c))
        if i + 1 < len(SKY):  # dither row into the next band
            out.append(r(0, (i + 1) * band_h - 1, LW, 2, f"url(#d{i})"))
    out.append(r(0, len(SKY) * band_h, LW, GROUND, SKY[-1]))
    rnd = random.Random(21)
    for _ in range(70):
        x, y = rnd.randint(0, LW - 1), rnd.randint(10, 70)
        c = rnd.choice(["#DDE6FF", "#DDE6FF", "#9FB2E8", "#FFD9A8"])
        tw = f' class="tw" style="animation-delay:-{rnd.uniform(0, 3):.1f}s"' if rnd.random() < .3 else ""
        out.append(f'<rect{tw} x="{x}" y="{y}" width="1" height="1" fill="{c}"/>')
    # moon
    moon = ["..mmm..", ".mmmmm.", "mmcmmmm", "mmmmcmm", "mmmmmmm", ".mmcmm.", "..mmm.."]
    out.append(sprite(moon, {"m": "#D9DDF0", "c": "#AEB5CF"}, 184, 16))
    return "\n".join(out)


def patterns():
    pats = []
    for i in range(len(SKY) - 1):
        pats.append(f'<pattern id="d{i}" width="2" height="2" patternUnits="userSpaceOnUse">'
                    f'<rect width="2" height="2" fill="{SKY[i]}"/><rect width="1" height="1" fill="{SKY[i + 1]}"/>'
                    f'<rect x="1" y="1" width="1" height="1" fill="{SKY[i + 1]}"/></pattern>')
    pats.append('<pattern id="beam" width="2" height="2" patternUnits="userSpaceOnUse">'
                '<rect width="1" height="1" fill="#FFF1C9" fill-opacity=".45"/></pattern>')
    return "<defs>" + "".join(pats) + "</defs>"


def satellite():
    body = r(-1, -1, 3, 3, LIGHT) + r(-5, 0, 4, 1, CYAN) + r(2, 0, 4, 1, CYAN) + f'<rect class="beacon" x="0" y="-2" width="1" height="1" fill="{RED}"/>'
    fn = track([(0, (-10, 30), lin), (CYCLE, (310, 8), lin)])

    def arc(t):
        x, _ = fn(t)
        u = (x + 10) / 320
        return x, 28 - 22 * (1 - (2 * u - 1) ** 2) + 6 * u

    return moving(arc, body)


def skyline():
    rnd = random.Random(8)
    out = []
    x = 92
    while x < 232:
        w, h = rnd.randint(8, 16), rnd.randint(8, 28)
        out.append(r(x, GROUND - h, w, h, "#120F24"))
        for wy in range(GROUND - h + 2, GROUND - 2, 3):
            for wx in range(x + 1, x + w - 1, 2):
                if rnd.random() < .22:
                    out.append(r(wx, wy, 1, 1, rnd.choice([AMBER, CYAN, CYAN, PINK])))
        x += w + rnd.randint(0, 2)
    return "\n".join(out)


def hud():
    hearts = "".join(sprite([".h.h.", "hhhhh", "hhhhh", ".hhh.", "..h.."], {"h": RED}, 268 + i * 6, 3) for i in range(3))
    start = text("> CLICK TO START", 0, 0, GOLD)
    return (text("WORLD 1-1", 4, 3, INK) + text("GROUND TO ORBIT", 4, 10, LIGHT)
            + f'<g class="press" transform="translate({(LW - text_w("> CLICK TO START")) // 2} 3)">{start}</g>'
            + hearts)


# ---------------------------------------------------------------------------- factory + gantry

F_X0, F_X1 = 4, 90
RAIL_Y = 47
PICK_L, PLACE_L = 26, 66            # stage left edge on the belt and on the parked truck
PICK_TOP, PLACE_TOP = 62, 67


def factory_back():
    teeth = []
    for x0 in range(F_X0, F_X1, 17):
        for k in range(17):
            hgt = 7 - (k * 7) // 17
            teeth.append(r(x0 + k, 45 - hgt, 1, hgt + 1, "#141826"))
        teeth.append(r(x0, 38, 1, 8, CYAN, ' opacity=".5"'))
    belt = "".join(r(x, 73, 2, 1, GREY4) for x in range(8, 48, 4))
    return f"""
<g>
  {''.join(teeth)}
  {r(F_X0, 45, F_X1 - F_X0, GROUND - 45, "#0C0E18")}
  {r(F_X0 + 2, 49, F_X1 - F_X0 - 4, GROUND - 49, "#07080F")}
  {r(8, RAIL_Y, 80, 2, GREY3)}
  {r(8, 72, 40, 3, GREY2)}
  <g class="belt">{belt}</g>
  {r(10, 75, 2, 7, GREY1)}{r(44, 75, 2, 7, GREY1)}
  {text(">", 12, 77, GOLD)}{text(">", 56, 77, GOLD)}
  <g class="u1slide"><g class="u1">{sprite(STAGE, STAGE_PAL, PICK_L, PICK_TOP)}</g></g>
  {sprite(STAGE, STAGE_PAL, 12, PICK_TOP)}
</g>"""


HOOK = track([(0, (PICK_L + 2, 52), lin), (0.3, (PICK_L + 2, 52), lin), (0.8, (PICK_L + 2, PICK_TOP - 2), lin),
              (1.2, (PICK_L + 2, 51), lin), (1.8, (PLACE_L + 2, 51), lin), (2.1, (PLACE_L + 2, PLACE_TOP - 2), lin),
              (2.5, (PLACE_L + 2, 52), lin), (3.0, (PICK_L + 2, 52), lin), (CYCLE, (PICK_L + 2, 52), lin)])


def gantry():
    trolley = moving(lambda t: (round(HOOK(t)[0]) - 2, RAIL_Y - 1),
                     r(0, 0, 6, 3, AMBER) + r(1, 3, 4, 1, GOLD) + f'<rect class="beacon" x="2" y="-1" width="2" height="1" fill="{CYAN}"/>')
    cable = (f'<rect x="{PICK_L + 2}" y="{RAIL_Y + 3}" width="1" height="1" fill="{LIGHT}">'
             + stepped("x", lambda t: round(HOOK(t)[0]) + .5, kind="animate", fmt=lambda v: f"{v}")
             + stepped("height", lambda t: max(1, round(HOOK(t)[1]) - (RAIL_Y + 3)), kind="animate", fmt=lambda v: f"{v}")
             + "</rect>")
    hook = moving(lambda t: (round(HOOK(t)[0]), round(HOOK(t)[1])),
                  r(-1, 0, 4, 1, GREY4) + r(-1, 1, 1, 1, GREY4) + r(2, 1, 1, 1, GREY4)
                  + f'<g class="u2">{sprite(STAGE, STAGE_PAL, -2, 2)}</g>')
    return trolley + cable + hook


def factory_front():
    sign = "LIGHTS-OUT FACTORY"
    sx = F_X0 + (F_X1 - F_X0 - text_w(sign)) // 2
    return f"""
<g>
  {r(F_X0, 45, 2, GROUND - 45, "#151A2A")}{r(F_X1 - 2, 45, 2, GROUND - 45, "#151A2A")}
  {r(sx - 3, 28, text_w(sign) + 6, 9, "#07080E")}{r(sx - 3, 28, text_w(sign) + 6, 1, CYAN)}{r(sx - 3, 36, text_w(sign) + 6, 1, CYAN)}
  {r(sx, 37, 1, 2, GREY2)}{r(sx + text_w(sign) - 1, 37, 1, 2, GREY2)}
  <g class="hum">{text(sign, sx, 30, "#BFE9FF")}</g>
</g>"""


# ---------------------------------------------------------------------------- truck

TRUCK = track([(0, (69, 0), lin), (3.0, (69, 0), lin), (6.4, (232, 0), ease_out), (7.6, (232, 0), lin),
               (9.0, (330, 0), ease_in), (10.5, (330, 0), lin), (10.51, (-40, 0), lin), (13.6, (69, 0), ease_out),
               (CYCLE, (69, 0), lin)])


def truck():
    wheel = lambda x: r(x, 79, 3, 3, "#07080C") + r(x + 1, 80, 1, 1, GREY4)
    body = (r(-11, 77, 21, 2, GREY3) + r(-11, 77, 21, 1, GREY4)
            + r(10, 70, 10, 9, GREY1) + r(10, 70, 10, 1, GREY3) + r(12, 72, 6, 3, "#0B1424") + r(12, 72, 6, 1, CYAN)
            + r(14, 68, 3, 2, GREY4) + f'<rect class="beacon" x="15" y="67" width="1" height="1" fill="{CYAN}"/>'
            + r(19, 76, 1, 1, "#FFF1C9") + r(-11, 79, 31, 1, GREY2) + r(-10, 81, 29, 1, CYAN, ' opacity=".5"')
            + wheel(-8) + wheel(3) + wheel(14)
            + f'<g class="u3">{sprite(STAGE, STAGE_PAL, -3, PLACE_TOP)}</g>')
    return moving(TRUCK, body)


# ---------------------------------------------------------------------------- pad + booster

B_L, B_TOP = 242, 51
UP = -110
BOOST = track([(0, (B_L, B_TOP), lin), (9.0, (B_L, B_TOP), lin), (10.4, (B_L, B_TOP + UP), ease_in),
               (11.0, (B_L, B_TOP + UP), lin), (13.2, (B_L, B_TOP), ease_out), (CYCLE, (B_L, B_TOP), lin)])
STACK = track([(0, (229, PLACE_TOP), lin), (6.6, (229, PLACE_TOP), lin), (6.9, (229, 34), lin), (7.1, (B_L, 34), lin),
               (7.4, (B_L, B_TOP - 10), lin), (9.0, (B_L, B_TOP - 10), lin), (10.4, (B_L, B_TOP - 10 + UP), ease_in),
               (CYCLE, (B_L, B_TOP - 10 + UP), lin)])


def pad():
    lattice = "".join(r(266, y, 1, 1, GREY3) + r(269, y + 2, 1, 1, GREY3) for y in range(32, GROUND, 4))
    board = []
    for cls, s, c in (("cd-ok", "LANDED", GREEN), ("cd3", "T-3", GOLD), ("cd2", "T-2", GOLD), ("cd1", "T-1", GOLD),
                      ("cd-go", "LIFTOFF", AMBER), ("cd-back", "INBOUND", CYAN)):
        board.append(f'<g class="{cls}">{text(s, 216 - text_w(s) // 2, 42, c)}</g>')
    return f"""
<g>
  {r(265, 30, 1, GROUND - 30, GREY2)}{r(270, 30, 1, GROUND - 30, GREY2)}{lattice}
  {r(265, 30, 6, 1, GREY3)}<rect class="beacon" x="267" y="28" width="2" height="2" fill="{RED}"/>
  {r(252, 44, 13, 1, GREY2)}
  {r(215, 49, 2, GROUND - 49, GREY2)}
  {r(200, 39, 32, 10, "#07080E")}{r(200, 39, 32, 1, GREY3)}{r(200, 48, 32, 1, GREY3)}
  {''.join(board)}
  {r(228, 79, 34, 3, GREY2)}{r(228, 79, 34, 1, GREY3)}
  {r(236, 79, 2, 1, GOLD)}{r(246, 79, 2, 1, GOLD)}{r(256, 79, 2, 1, GOLD)}
</g>"""


def booster():
    flame = (f'<g class="burn"><g class="fa">{sprite(FLAME_A, FLAME_PAL, 1, 28)}</g>'
             f'<g class="fb">{sprite(FLAME_B, FLAME_PAL, 1, 28)}</g></g>')
    legs = f'<g class="legs-out">{LEGS_OUT}</g><g class="legs-in">{LEGS_IN}</g>'
    return moving(BOOST, flame + legs + booster_body())


def stacked():
    return moving(STACK, f'<g class="u4">{sprite(STAGE, STAGE_PAL)}</g>')


def smoke():
    rnd = random.Random(4)
    pix = []
    for _ in range(70):
        x = rnd.randint(222, 268)
        y = rnd.randint(70, 81)
        d = abs(x - 245) / 23 + (81 - y) / 14
        if d < 1.2:
            pix.append(r(x, y, 2, 2, rnd.choice(["#C9D0DE", "#A7B0C4", "#8790A6"])))
    return f'<g class="smoke"><g class="jit">{"".join(pix)}</g></g>'


def plus_one():
    fn = track([(0, (243, 34), lin), (13.2, (243, 34), lin), (14.0, (243, 26), lin)])
    return moving(fn, f'<g class="plus">{text("+1", 0, 0, GOLD)}</g>')


# ---------------------------------------------------------------------------- highway + car

def oncoming():
    out = []
    for dur, delay, col in ((3.4, 0, CYAN), (5.1, 2.2, VIOLET), (4.3, 3.6, GOLD)):
        car = (r(0, 90, 20, 4, "#161B2B") + r(5, 87, 9, 3, "#161B2B") + r(6, 88, 7, 2, "#0B1424")
               + r(9, 86, 2, 1, GREY4) + r(0, 91, 1, 1, "#FFF1C9") + r(1, 94, 18, 1, col)
               + r(3, 93, 3, 2, "#07080C") + r(14, 93, 3, 2, "#07080C"))
        out.append(f'<g class="oncoming" style="animation-duration:{dur}s;animation-delay:-{delay}s">{car}</g>')
    return "".join(out)


def highway():
    dashes = "".join(r(x, 97, 8, 1, GREY3) for x in range(-20, LW + 40, 20))
    posts = "".join(r(x, 84, 1, 3, GREY2) for x in range(-15, LW + 30, 15))
    return f"""
{r(0, GROUND, LW, LH - GROUND, "#0B0E17")}
{r(0, GROUND, LW, 1, "#1D2334")}
<g class="rail">{posts}</g>
{r(0, 85, LW, 1, GREY2)}
{r(0, 95, LW, 1, GREY1)}
{oncoming()}
<g class="dash">{dashes}</g>
{r(0, 108, LW, 2, "#070910")}"""


X0 = 124  # player car left edge


def car():
    x0 = X0
    head = sprite(HEAD, HEAD_PAL, x0 + 30, 78)
    eyes_calm = r(x0 + 34, 84, 1, 1, HAIR) + r(x0 + 38, 84, 1, 1, HAIR) + r(x0 + 35, 87, 3, 1, MOUTH)
    eyes_look = (r(x0 + 34, 83, 1, 1, HAIR) + r(x0 + 38, 83, 1, 1, HAIR) + r(x0 + 33, 81, 2, 1, HAIR)
                 + r(x0 + 37, 81, 2, 1, HAIR) + r(x0 + 36, 86, 2, 2, MOUTH))
    eyes_smug = (r(x0 + 34, 84, 1, 1, HAIR) + r(x0 + 38, 84, 1, 1, HAIR) + r(x0 + 33, 82, 2, 1, HAIR)
                 + r(x0 + 37, 81, 2, 1, HAIR) + r(x0 + 34, 87, 4, 1, MOUTH) + r(x0 + 38, 86, 1, 1, MOUTH))
    wheel = lambda x: (sprite(["..rrrr..", ".rrrrrr.", "rrr..rrr", "rr....rr", "rr....rr", "rrr..rrr", ".rrrrrr.", "..rrrr.."],
                              {"r": "#07080C"}, x, 100)
                       + f'<g class="wa">{r(x + 3, 102, 2, 4, CYAN)}</g><g class="wb">{r(x + 2, 103, 4, 2, CYAN)}</g>')
    windshield = "".join(r(x0 + 52 + k, 92 - k, 1, 1, CYAN) for k in range(7))
    steer_a = r(x0 + 50, 86, 1, 5, LIGHT)
    steer_b = r(x0 + 49, 86, 1, 2, LIGHT) + r(x0 + 50, 88, 1, 1, LIGHT) + r(x0 + 51, 89, 1, 2, LIGHT)
    cup_rest = r(x0 + 25, 87, 3, 4, WHITE) + r(x0 + 25, 88, 3, 1, AMBER) + r(x0 + 26, 91, 2, 1, SKIN)
    cup_up = r(x0 + 26, 79, 3, 4, WHITE) + r(x0 + 26, 80, 3, 1, AMBER) + r(x0 + 27, 83, 2, 2, SKIN) + r(x0 + 27, 85, 2, 6, HOODIE)
    return f"""
<g class="drive">
  {r(x0 + 2, 108, 68, 1, "#000")}
  <path d="M{x0 + 73} 95 L{x0 + 120} 89 V107 L{x0 + 73} 99 Z" fill="url(#beam)"/>
  {r(x0 + 27, 88, 18, 5, HOODIE)}{r(x0 + 34, 89, 4, 1, "#ECEBE6")}
  {head}
  <g class="f-calm">{eyes_calm}</g><g class="f-look">{eyes_look}</g><g class="f-smug">{eyes_smug}</g>
  {r(x0 + 46, 85, 4, 7, "#151B29")}
  <g class="sa">{steer_a}</g><g class="sb">{steer_b}</g>
  {windshield}
  {r(x0, 92, 72, 11, "#1A2236")}{r(x0, 92, 52, 1, "#2C354A")}{r(x0 + 28, 93, 1, 10, "#11182A")}
  {r(x0 + 72, 95, 1, 7, "#1A2236")}
  {r(x0, 95, 1, 2, RED)}{r(x0 + 72, 95, 1, 1, "#FFF1C9")}
  {r(x0 + 2, 103, 68, 1, PINK)}{r(x0 + 4, 104, 64, 1, PINK, ' opacity=".4"')}
  {r(x0 + 57, 83, 4, 2, GREY3)}<rect class="beacon" x="{x0 + 58}" y="82" width="2" height="1" fill="{CYAN}"/>
  {r(x0 + 1, 85, 25, 7, "#07080E")}{r(x0 + 1, 85, 25, 1, GREY2)}
  {text(">ORBIT", x0 + 3, 86, GOLD)}
  <g class="cup-rest">{cup_rest}</g><g class="cup-up">{cup_up}</g>
  {wheel(x0 + 9)}{wheel(x0 + 54)}
</g>"""


def bubble():
    s = "STUCK IT!"
    w = text_w(s) + 6
    x = X0 + 36 - w // 2
    return f"""
<g class="say">
  {r(x, 64, w, 10, GREEN)}{r(x + 1, 65, w - 2, 8, "#11141F")}
  {r(X0 + 35, 74, 3, 1, GREEN)}{r(X0 + 36, 74, 1, 1, "#11141F")}{r(X0 + 36, 75, 1, 2, GREEN)}
  {text(s, x + 3, 67, INK)}
</g>"""


# ---------------------------------------------------------------------------- assembly

def build():
    css = "\n".join([
        toggle("u1", [(0, 0.8), (12.4, CYCLE)]),
        kf("u1slide", [(0, "transform:translateX(0)"), (12.4, "transform:translateX(-14px)"),
                       (13.4, "transform:translateX(0)"), (CYCLE, "transform:translateX(0)")]),
        ".u1slide{animation:u1slide 14s steps(168,end) infinite}",
        toggle("u2", [(0.8, 2.1)]),
        toggle("u3", [(2.1, 6.6)]),
        toggle("u4", [(6.6, 10.4)]),
        toggle("burn", [(9.0, 10.4), (12.0, 13.2)]),
        toggle("legs-in", [(9.3, 12.6)]),
        toggle("legs-out", [(9.3, 12.6)], invert=True),
        toggle("smoke", [(8.9, 10.6), (12.8, 13.9)]),
        toggle("plus", [(13.2, CYCLE)]),
        toggle("cd-ok", [(0, 8.0), (13.2, CYCLE)]),
        toggle("cd3", [(8.0, 8.33)]),
        toggle("cd2", [(8.33, 8.66)]),
        toggle("cd1", [(8.66, 9.0)]),
        toggle("cd-go", [(9.0, 11.0)]),
        toggle("cd-back", [(11.0, 13.2)]),
        toggle("f-calm", [(0, 1.6), (8.9, CYCLE)], invert=True),
        toggle("f-look", [(8.9, 13.2)]),
        toggle("f-smug", [(0, 1.6), (13.2, CYCLE)]),
        toggle("cup-up", [(0, 1.6), (13.2, CYCLE)]),
        toggle("cup-rest", [(0, 1.6), (13.2, CYCLE)], invert=True),
        toggle("say", [(0, 1.6), (13.3, CYCLE)]),
        # two-frame sprite flips
        "@keyframes fa{0%{opacity:1}50%{opacity:0}}.fa{animation:fa .2s steps(1,end) infinite}",
        "@keyframes fb{0%{opacity:0}50%{opacity:1}}.fb{animation:fb .2s steps(1,end) infinite}",
        ".wa{animation:fa .16s steps(1,end) infinite}.wb{animation:fb .16s steps(1,end) infinite}",
        ".sa{animation:fa 1.4s steps(1,end) infinite}.sb{animation:fb 1.4s steps(1,end) infinite}",
        "@keyframes jit{0%{transform:translate(0,0)}33%{transform:translate(1px,-1px)}66%{transform:translate(-1px,0)}}",
        ".jit{animation:jit .3s steps(1,end) infinite}",
        # scrolling world
        "@keyframes dash{to{transform:translateX(-20px)}}.dash{animation:dash .4s steps(20,end) infinite}",
        "@keyframes rail{to{transform:translateX(-15px)}}.rail{animation:rail .5s steps(15,end) infinite}",
        "@keyframes belt{to{transform:translateX(4px)}}.belt{animation:belt .5s steps(4,end) infinite}",
        "@keyframes oncoming{from{transform:translateX(320px)}to{transform:translateX(-30px)}}",
        ".oncoming{animation-name:oncoming;animation-timing-function:steps(350,end);animation-iteration-count:infinite}",
        "@keyframes drive{0%,100%{transform:translateY(0)}50%{transform:translateY(-1px)}}",
        ".drive{animation:drive .5s steps(1,end) infinite}",
        # blinkers
        "@keyframes press{0%{opacity:1}50%{opacity:0}}.press{animation:press 1s steps(1,end) infinite}",
        "@keyframes tw{0%{opacity:1}50%{opacity:.2}}.tw{animation:tw 1.6s steps(1,end) infinite}",
        "@keyframes beacon{0%{opacity:1}50%{opacity:.15}}.beacon{animation:beacon 1s steps(1,end) infinite}",
        "@keyframes hum{0%,94%{opacity:1}95%{opacity:.3}97%{opacity:1}98%{opacity:.5}}.hum{animation:hum 6s steps(1,end) infinite}",
        "@media (prefers-reduced-motion: reduce){*{animation:none!important}}",
    ])

    scene = "\n".join([
        patterns(),
        sky(),
        satellite(),
        skyline(),
        factory_back(),
        gantry(),
        pad(),
        stacked(),
        booster(),
        smoke(),
        plus_one(),
        truck(),
        factory_front(),
        highway(),
        car(),
        bubble(),
        hud(),
    ])
    body = f'<g transform="scale({PX})" shape-rendering="crispEdges">\n{scene}\n</g>'
    return doc(
        W, H,
        "Ground to orbit, as a pixel-art game screen",
        css, body,
        desc=("A pixel-art game screen titled World 1-1, Ground to Orbit, with a blinking Click to Start prompt. "
              "A gantry crane in a lights-out factory loads a rocket upper stage onto a driverless truck, which "
              "drives itself to the launch pad. The stage is stacked on a reusable booster, the countdown runs, the "
              "rocket lifts off, and the booster comes back and lands for a +1. In the foreground Nitish rides in a "
              "self-driving car with an empty driver's seat, raises his coffee and says Stuck it!"),
    )
