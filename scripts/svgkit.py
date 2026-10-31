"""Shared helpers for the profile SVGs.

GitHub shows README images through <img>, so every SVG here has to be
self-contained: no scripts, no web fonts, no external references. Motion is
plain CSS keyframes plus SMIL, which both run inside <img>.
"""

import math
import re
from xml.sax.saxutils import escape

# Palette from the portfolio site (sundarrajnitish.github.io/portfolio).
BG = "#0A0E13"
BG_ALT = "#0D131A"
PANEL = "#121922"
PANEL_HI = "#161F2A"
BORDER = "#223040"
BORDER_SOFT = "#1A2430"
TEXT = "#E8EDF2"
MUTED = "#8A97A6"
DIM = "#57687A"
CYAN = "#35C4E8"
AMBER = "#F2A93B"
GREEN = "#3ED598"
RED = "#E4574C"
VIOLET = "#8B7CF6"

MONO = "ui-monospace,'SFMono-Regular','JetBrains Mono','Cascadia Mono',Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Inter',system-ui,'Helvetica Neue',Arial,sans-serif"

# Advance of one monospace glyph as a fraction of the font size. Typed text is
# pinned to n * MONO_ADV * size with textLength, so the reveal clips line up
# whichever monospace font the viewer's system picks.
MONO_ADV = 0.6


def esc(s):
    return escape(str(s), {'"': "&quot;"})


def f(x):
    """Compact number formatting for attributes."""
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def doc(w, h, title, css, body, desc=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-labelledby="t d">\n'
        f"<title id=\"t\">{esc(title)}</title><desc id=\"d\">{esc(desc or title)}</desc>\n"
        f"<style>\n{css}\n"
        "@media (prefers-reduced-motion: reduce){.loop{animation:none!important;opacity:1!important}}\n"
        f"</style>\n{body}\n</svg>\n"
    )


def panel(w, h, r=18, fill=BG, stroke=BORDER):
    return f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'


def grid_pattern(pid, step=20, color=BORDER_SOFT, opacity=0.55):
    return (
        f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
        f'<path d="M{step} 0H0V{step}" fill="none" stroke="{color}" stroke-width="1" opacity="{opacity}"/></pattern>'
    )


def mono_text(x, y, s, size, fill, extra="", fit=True, anchor=None):
    """Monospace text whose width is pinned to len(s) * MONO_ADV * size."""
    tl = f' textLength="{f(len(s) * MONO_ADV * size)}" lengthAdjust="spacingAndGlyphs"' if fit and s else ""
    a = f' text-anchor="{anchor}"' if anchor else ""
    return (
        f'<text x="{f(x)}" y="{f(y)}" font-family="{MONO}" font-size="{size}" fill="{fill}"{tl}{a} '
        f'xml:space="preserve" {extra}>{esc(s)}</text>'
    )


def text(x, y, s, size, fill, weight=400, family=SANS, extra="", anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ""
    return (
        f'<text x="{f(x)}" y="{f(y)}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}"{a} {extra}>{esc(s)}</text>'
    )


def discrete(attr, events, dur, begin="0s", repeat=None, initial=None):
    """SMIL step animation. events: [(time_s, value)], sorted, times within [0, dur]."""
    times, values = [0.0], [initial if initial is not None else events[0][1]]
    for t, v in events:
        t = min(max(t, 0.0), dur)
        if t <= times[-1] + 1e-6:
            values[-1] = v
            continue
        times.append(t)
        values.append(v)
    kt = ";".join(f"{t / dur:.5f}" for t in times)
    vs = ";".join(str(v) for v in values)
    rep = f' repeatCount="{repeat}"' if repeat else ' fill="freeze"'
    return (
        f'<animate attributeName="{attr}" calcMode="discrete" dur="{f(dur)}s" begin="{begin}" '
        f'keyTimes="{kt}" values="{vs}"{rep}/>'
    )


def typed(x, y, s, size, fill, start, step, dur=None, hold=None, back=0.0, cid=None, begin="0s",
          repeat=None, caret=None, extra=""):
    """Typewriter reveal of a monospace string through a clip rect.

    Returns (defs, element). With dur/hold/back the string types, holds, then
    backspaces, inside a cycle of length dur (for looping).
    """
    cw = MONO_ADV * size
    n = len(s)
    ev = [(start + i * step, f(i * cw)) for i in range(1, n + 1)]
    if hold is not None:
        t_end = start + n * step + hold
        ev += [(t_end + i * back, f((n - i) * cw)) for i in range(1, n + 1)]
    total = dur if dur else ev[-1][0] + 0.01
    clip = (
        f'<clipPath id="{cid}"><rect x="{f(x - 2)}" y="{f(y - size * 1.05)}" width="0" height="{f(size * 1.45)}">'
        + discrete("width", ev, total, begin, repeat, initial="0")
        + "</rect></clipPath>"
    )
    el = f'<g clip-path="url(#{cid})">{mono_text(x, y, s, size, fill, extra)}</g>'
    if caret:
        cx_ev = [(t, f(x + float(v) + 1)) for t, v in ev]
        el += (
            f'<rect x="{f(x)}" y="{f(y - size * 0.85)}" width="{f(size * 0.55)}" height="{f(size * 1.0)}" '
            f'fill="{caret}" class="blink">'
            + discrete("x", cx_ev, total, begin, repeat, initial=f(x))
            + "</rect>"
        )
    return clip, el


# --- Bezier helpers (for the plotted signature) --------------------------------------------

def parse_path(d):
    """Parse an absolute path of M and C commands into cubic segments."""
    toks = re.sub(r"([MC])", r" \1 ", d).replace(",", " ").split()
    segs, i, cur = [], 0, None
    while i < len(toks):
        cmd = toks[i]
        if cmd == "M":
            cur = (float(toks[i + 1]), float(toks[i + 2]))
            i += 3
        elif cmd == "C":
            i += 1
            while i < len(toks) and toks[i] not in ("M", "C"):
                p1 = (float(toks[i]), float(toks[i + 1]))
                p2 = (float(toks[i + 2]), float(toks[i + 3]))
                p3 = (float(toks[i + 4]), float(toks[i + 5]))
                segs.append((cur, p1, p2, p3))
                cur = p3
                i += 6
        else:
            raise ValueError(cmd)
    return segs


def bez(seg, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = seg
    u = 1 - t
    a, b, c, d = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
    return (a * x0 + b * x1 + c * x2 + d * x3, a * y0 + b * y1 + c * y2 + d * y3)


def polyline(segs, per_seg=120):
    pts = [segs[0][0]]
    for s in segs:
        for k in range(1, per_seg + 1):
            pts.append(bez(s, k / per_seg))
    return pts


def length(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def resample(pts, n):
    """n+1 points evenly spaced by arc length."""
    cum = [0.0]
    for i in range(len(pts) - 1):
        cum.append(cum[-1] + math.dist(pts[i], pts[i + 1]))
    total, out, j = cum[-1], [], 0
    for k in range(n + 1):
        target = total * k / n
        while j < len(cum) - 2 and cum[j + 1] < target:
            j += 1
        seg = cum[j + 1] - cum[j] or 1
        t = (target - cum[j]) / seg
        out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * t, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * t))
    return out


def seg_path(segs):
    d = f"M{f(segs[0][0][0])} {f(segs[0][0][1])}"
    for _, p1, p2, p3 in segs:
        d += f"C{f(p1[0])} {f(p1[1])} {f(p2[0])} {f(p2[1])} {f(p3[0])} {f(p3[1])}"
    return d
