"""Render assets/stack.svg: tech logos grouped by category, in the profile's palette.

Icons are monochrome paths from simple-icons (scripts/icons). Each tile briefly lights up
in its brand colour as a wave passes across the grid.
Run: python3 scripts/stack.py
"""
import re

from brand import ROOT, INK, PANEL, LINE, BONE, ASH, GILT, font_css

ICONS = ROOT / "scripts" / "icons"
TILE = PANEL

# (icon file, label, brand colour; None means the brand is black, so light up in gilt)
GROUPS = [
    ("Languages", [
        ("typescript", "TypeScript", "#3178C6"),
        ("javascript", "JavaScript", "#F7DF1E"),
        ("python", "Python", "#3776AB"),
        ("swift", "Swift", "#F05138"),
    ]),
    ("Frameworks", [
        ("react", "React", "#61DAFB"),
        ("nextdotjs", "Next.js", None),
        ("nodedotjs", "Node.js", "#5FA04E"),
        ("fastapi", "FastAPI", "#009688"),
        ("tailwindcss", "Tailwind", "#06B6D4"),
    ]),
    ("Data & Infra", [
        ("supabase", "Supabase", "#3FCF8E"),
        ("postgresql", "Postgres", "#4169E1"),
        ("mongodb", "MongoDB", "#47A248"),
        ("vercel", "Vercel", None),
        ("stripe", "Stripe", "#635BFF"),
        ("githubactions", "Actions", "#2088FF"),
    ]),
    ("AI & Tools", [
        ("claude", "Claude", "#D97757"),
        ("openai", "OpenAI", None),
        ("opencv", "OpenCV", "#5C3EE8"),
        ("git", "Git", "#F05032"),
        ("figma", "Figma", "#F24E1E"),
    ]),
]

W, PAD = 1200, 48
LABEL_W = 210
TILE_W, TILE_H, GAP = 140, 104, 10
ROW_H = TILE_H + 22
TOP = 40
H = TOP + ROW_H * len(GROUPS) + 18

total = sum(len(items) for _, items in GROUPS)
CYCLE = 9.0  # seconds for the wave to cross every tile once
STEP = CYCLE / total


def icon_path(name):
    return re.search(r'<path d="([^"]+)"', (ICONS / f"{name}.svg").read_text()).group(1)


css = font_css(mono="".join(g.upper() + "".join(i[1] for i in items) for g, items in GROUPS) + "&")

out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  {css}
  .mono {{ font-family: 'Martian Mono', ui-monospace, monospace; }}
  .t rect {{ animation: edge {CYCLE}s ease-in-out infinite; }}
  .t path {{ animation: glow {CYCLE}s ease-in-out infinite; }}
  .t text {{ animation: txt {CYCLE}s ease-in-out infinite; }}
  @keyframes edge {{ 0%, 12%, 100% {{ stroke: {LINE}; }} 4% {{ stroke: {GILT}; }} }}
  @keyframes glow {{ 0%, 14%, 100% {{ fill: {BONE}; }} 4%, 6% {{ fill: var(--c); }} }}
  @keyframes txt {{ 0%, 12%, 100% {{ fill-opacity: .5; }} 4% {{ fill-opacity: 1; }} }}
</style>
<defs><clipPath id="f"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="{INK}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{LINE}"/>''']

i = 0
for r, (group, items) in enumerate(GROUPS):
    y = TOP + r * ROW_H
    out.append(f'<text x="{PAD}" y="{y + TILE_H/2 + 5}" class="mono" font-size="12" letter-spacing="2.4" fill="{ASH}">{group.upper().replace("&", "&amp;")}</text>')
    out.append(f'<rect x="{PAD}" y="{y + TILE_H/2 + 16}" width="18" height="1.5" fill="{GILT}"/>')
    for c, (name, label, color) in enumerate(items):
        x = PAD + LABEL_W + c * (TILE_W + GAP)
        delay = f"{i * STEP:.2f}s"
        s = 34 / 24
        out.append(
            f'<g class="t" style="--c:{color or GILT}">'
            f'<rect x="{x}" y="{y}" width="{TILE_W}" height="{TILE_H}" rx="12" fill="{TILE}" stroke="{LINE}" style="animation-delay:{delay}"/>'
            f'<path transform="translate({x + TILE_W/2 - 17} {y + 20}) scale({s:.4f})" d="{icon_path(name)}" fill="{BONE}" style="animation-delay:{delay}"/>'
            f'<text x="{x + TILE_W/2}" y="{y + TILE_H - 18}" text-anchor="middle" class="mono" font-size="11" letter-spacing=".6" fill="{BONE}" fill-opacity=".5" style="animation-delay:{delay}">{label}</text>'
            f'</g>')
        i += 1

out.append("</g></svg>")
(ROOT / "assets" / "stack.svg").write_text("\n".join(out))
print("wrote assets/stack.svg", W, "x", H)
