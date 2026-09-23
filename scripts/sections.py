"""Render the section headings in assets/sections/, one per GitHub theme.
Run: python3 scripts/sections.py
"""
from brand import ROOT, BONE, INK, GILT, GILT_DEEP, ASH, font_css

# (file key, number, plain words, accent word, note on the right)
SECTIONS = [
    ("work", "01", "Selected", "work", "SIX PROJECTS"),
    ("experience", "02", "Where I've", "worked", "2025 — NOW"),
    ("stack", "03", "The", "stack", "WHAT I REACH FOR"),
    ("activity", "04", "Recent", "activity", "REFRESHED DAILY"),
]
THEMES = {
    "dark": dict(fg=BONE, accent=GILT, muted=ASH, rule="#3A3026"),
    "light": dict(fg=INK, accent=GILT_DEEP, muted="#7A6E5E", rule="#E2D9CB"),
}

css = font_css(
    display="".join(s[2] for s in SECTIONS),
    accent="".join(s[3] for s in SECTIONS),
    mono="".join(s[1] + s[4] for s in SECTIONS) + "/",
)

W, H = 1200, 100
out_dir = ROOT / "assets" / "sections"
out_dir.mkdir(parents=True, exist_ok=True)

for key, num, words, accent, note in SECTIONS:
    for theme, c in THEMES.items():
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
{css}
.d {{ font-family: 'Fraunces Display', Georgia, serif; }}
.a {{ font-family: 'Fraunces Accent', Georgia, serif; font-style: italic; }}
.m {{ font-family: 'Martian Mono', ui-monospace, monospace; }}
.rule {{ transform-origin: 0 0; animation: draw 1.4s cubic-bezier(.2,.7,.2,1) both .15s; }}
@keyframes draw {{ from {{ transform: scaleX(0); }} }}
</style>
<text x="2" y="30" class="m" font-size="13" letter-spacing="2.6" fill="{c['accent']}">{num} /</text>
<text x="0" y="78" font-size="50" letter-spacing="-1" fill="{c['fg']}"><tspan class="d">{words} </tspan><tspan class="a" fill="{c['accent']}">{accent}</tspan></text>
<text x="{W - 4}" y="76" text-anchor="end" class="m" font-size="12" letter-spacing="2.4" fill="{c['muted']}">{note}</text>
<line class="rule" x1="0" y1="{H - 0.5}" x2="{W}" y2="{H - 0.5}" stroke="{c['rule']}"/>
</svg>'''
        (out_dir / f"{key}-{theme}.svg").write_text(svg)
print("wrote", len(SECTIONS) * len(THEMES), "section headings")
