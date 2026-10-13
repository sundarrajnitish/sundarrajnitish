"""Regenerate every SVG in assets/:  python3 scripts/build.py"""

import pathlib

import hero
import labs
import sections

ROOT = pathlib.Path(__file__).resolve().parent.parent


def write(rel, svg):
    path = ROOT / "assets" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    print(f"{rel:28s} {len(svg) / 1024:6.1f} KB")


if __name__ == "__main__":
    write("hero.svg", hero.build())
    write("stack.svg", sections.stack())
    write("rebuild-log.svg", sections.rebuild_log())
    write("footer.svg", sections.footer())
    for builder, _ in labs.CARDS:
        slug, svg = builder()
        write(f"labs/{slug}.svg", svg)
