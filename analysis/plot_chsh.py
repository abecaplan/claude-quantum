"""
plot_chsh.py — render the Phase 1 CHSH theta-sweep from results/chsh.json as compact SVG.

Reads the SAME JSON contract the verifier reads (never the live run) and emits the figure
used by README.md, in a light and a dark variant so GitHub's <picture> element can serve
whichever matches the reader's theme. Pure stdlib — no matplotlib, no numpy.

Usage:
    python analysis/plot_chsh.py [path/to/chsh.json]   # default results/chsh.json
Outputs:
    results/chsh_curve.svg        (light)
    results/chsh_curve_dark.svg   (dark)
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

QUANTUM_BOUND = 2.0 * math.sqrt(2.0)

THEMES = {
    "light": dict(
        suffix="", surface="#fcfcfb", primary="#0b0b0b", secondary="#52514e",
        muted="#898781", grid="#e1e0d9", baseline="#c3c2b7",
        s1="#2a78d6", s2="#1baf7a",
    ),
    "dark": dict(
        suffix="_dark", surface="#1a1a19", primary="#ffffff", secondary="#c3c2b7",
        muted="#898781", grid="#2c2c2a", baseline="#383835",
        s1="#3987e5", s2="#199e70",
    ),
}

# Geometry
W, H = 880, 560
ML, MR, MT, MB = 42, 158, 72, 48
X0, X1, Y0, Y1 = 0.0, 2.0, -3.55, 3.55
FONT = 'system-ui,-apple-system,Segoe UI,sans-serif'


def px(t):  # theta/pi -> x
    return ML + (t - X0) / (X1 - X0) * (W - ML - MR)


def py(v):  # S value -> y
    return MT + (Y1 - v) / (Y1 - Y0) * (H - MT - MB)


def render(d: dict, th: dict, out_path: Path) -> None:
    theta = [p / math.pi for p in d["phases_rad"]]
    S1, S2 = d["S1"], d["S2"]
    pk_i = min(range(len(theta)),
               key=lambda i: abs(theta[i] - d["S_peak_theta_rad"] / math.pi))
    pk_series = S2 if d["S_peak_witness"] == "S2" else S1
    e = []  # svg elements

    def text(x, y, s, fill, size, anchor="start", weight=None, style=None):
        extra = (f' font-weight="{weight}"' if weight else "") + \
                (f' font-style="{style}"' if style else "")
        e.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
                 f'text-anchor="{anchor}"{extra}>{s}</text>')

    # background, title, legend
    e.append(f'<rect width="{W}" height="{H}" fill="{th["surface"]}"/>')
    text(10, 26, f'CHSH witnesses on {d["backend"]}  ·  {d["shots"]} shots/point  ·  '
         f'{d["timestamp_utc"][:10]}', th["primary"], 16, weight="600")
    for lx, color, label in ((14, th["s1"], "S₁ = ⟨ZZ⟩ − ⟨ZX⟩ + ⟨XZ⟩ + ⟨XX⟩"),
                             (320, th["s2"], "S₂ = ⟨ZZ⟩ + ⟨ZX⟩ − ⟨XZ⟩ + ⟨XX⟩")):
        e.append(f'<circle cx="{lx}" cy="48" r="5" fill="{color}"/>')
        text(lx + 12, 52, label, th["secondary"], 12.5)

    # classically-allowed band, gridlines, bounds
    e.append(f'<rect x="{ML}" y="{py(2):.1f}" width="{W - ML - MR}" '
             f'height="{py(-2) - py(2):.1f}" fill="{th["secondary"]}" opacity="0.06"/>')
    for y in range(-3, 4):
        e.append(f'<line x1="{ML}" x2="{W - MR}" y1="{py(y):.1f}" y2="{py(y):.1f}" '
                 f'stroke="{th["grid"]}" stroke-width="1"/>')
        text(ML - 8, py(y) + 4, y, th["muted"], 12, anchor="end")
    for b, dash in ((2, ""), (-2, ""), (QUANTUM_BOUND, ' stroke-dasharray="4 3"'),
                    (-QUANTUM_BOUND, ' stroke-dasharray="4 3"')):
        e.append(f'<line x1="{ML}" x2="{W - MR}" y1="{py(b):.1f}" y2="{py(b):.1f}" '
                 f'stroke="{th["muted"]}" stroke-width="1.1"{dash}/>')
    text(W - MR + 8, py(QUANTUM_BOUND) + 4, "Tsirelson bound ±2√2", th["secondary"], 12.5)
    text(W - MR + 8, py(2) + 4, "classical bound ±2", th["secondary"], 12.5)

    # baseline, x ticks, axis label
    e.append(f'<line x1="{ML}" x2="{W - MR}" y1="{py(Y0):.1f}" y2="{py(Y0):.1f}" '
             f'stroke="{th["baseline"]}" stroke-width="1"/>')
    for t, lab in ((0, "0"), (0.5, "π/2"), (1, "π"), (1.5, "3π/2"), (2, "2π")):
        text(px(t), H - MB + 20, lab, th["muted"], 12.5, anchor="middle")
    text((ML + W - MR) / 2, H - 8, "Alice's measurement-basis angle θ",
         th["secondary"], 13.5, anchor="middle")

    # series (line + markers with a surface ring)
    for ys, color in ((S1, th["s1"]), (S2, th["s2"])):
        pts = " ".join(f'{"M" if i == 0 else "L"}{px(theta[i]):.1f} {py(v):.1f}'
                       for i, v in enumerate(ys))
        e.append(f'<path d="{pts}" fill="none" stroke="{color}" stroke-width="2.4" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')
        for i, v in enumerate(ys):
            e.append(f'<circle cx="{px(theta[i]):.1f}" cy="{py(v):.1f}" r="4.5" '
                     f'fill="{color}" stroke="{th["surface"]}" stroke-width="2"/>')

    # direct labels at the extremum farthest from the peak callout
    for name, ys in (("S₁", S1), ("S₂", S2)):
        i_max = max(range(len(ys)), key=lambda i: ys[i])
        i_min = min(range(len(ys)), key=lambda i: ys[i])
        i = max((i_max, i_min), key=lambda i: abs(theta[i] - theta[pk_i]))
        dy = -14 if ys[i] > 0 else 22
        text(px(theta[i]), py(ys[i]) + dy, name, th["secondary"], 13.5,
             anchor="middle", style="italic")

    # peak callout
    kx, ky = px(theta[pk_i]), py(pk_series[pk_i])
    e.append(f'<line x1="{kx + 6:.1f}" y1="{ky + 6:.1f}" x2="{kx + 22:.1f}" '
             f'y2="{ky + 16:.1f}" stroke="{th["muted"]}" stroke-width="1"/>')
    text(kx + 26, ky + 21, f'|S| = {d["S_peak_abs"]:.3f} ± {d["S_peak_std"]:.3f}',
         th["primary"], 13.5, weight="650")

    body = "\n".join(e)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'font-family="{FONT}" role="img" aria-label="CHSH witnesses versus theta '
           f'measured on {d["backend"]}: both curves exceed the classical bound of 2, '
           f'peak absolute value {d["S_peak_abs"]:.3f}.">\n{body}\n</svg>\n')
    out_path.write_text(svg)
    print(f"wrote {out_path}  ({len(svg)} bytes)")


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "results/chsh.json")
    d = json.loads(src.read_text())
    for th in THEMES.values():
        render(d, th, src.parent / f"chsh_curve{th['suffix']}.svg")


if __name__ == "__main__":
    main()
