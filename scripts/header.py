"""Render assets/header.svg. Run: python3 scripts/header.py"""
from brand import ROOT, INK, LINE, BONE, ASH, GILT, font_css

EYEBROW = "CS + AI · OAKLAND UNIVERSITY · CLASS OF 2027"
FIRST, LAST = "Jasman", "Sidhu"
TAGLINE = "I build practical AI products: agents that take real actions,"
TAGLINE2 = "and apps people actually use."
META = ["SOFTWARE ENGINEERING INTERN · MOTHERSON", "STERLING HEIGHTS, MI"]

css = font_css(
    display=FIRST,
    accent=LAST,
    body=TAGLINE + TAGLINE2,
    mono=EYEBROW + "".join(META) + "01",
)

W, H = 1200, 420
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <radialGradient id="glow" cx="0.82" cy="0.1" r="0.7">
    <stop offset="0" stop-color="{GILT}" stop-opacity="0.16"/>
    <stop offset="1" stop-color="{GILT}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="rules" width="1200" height="42" patternUnits="userSpaceOnUse">
    <line x1="0" y1="41.5" x2="1200" y2="41.5" stroke="{BONE}" stroke-opacity="0.025"/>
  </pattern>
  <clipPath id="f"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
{css}
.d {{ font-family: 'Fraunces Display', Georgia, serif; }}
.a {{ font-family: 'Fraunces Accent', Georgia, serif; font-style: italic; }}
.b {{ font-family: 'Archivo', system-ui, sans-serif; }}
.m {{ font-family: 'Martian Mono', ui-monospace, monospace; }}
.up {{ opacity: 0; animation: up 1s cubic-bezier(.2,.7,.2,1) forwards; }}
@keyframes up {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
.rule {{ transform-origin: 64px 0; transform: scaleX(0); animation: draw 1.6s cubic-bezier(.2,.7,.2,1) .9s forwards; }}
@keyframes draw {{ to {{ transform: scaleX(1); }} }}
.pulse {{ animation: pulse 2.6s ease-in-out infinite; }}
@keyframes pulse {{ 50% {{ opacity: .3; }} }}
</style>
<g clip-path="url(#f)">
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#rules)"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{LINE}"/>

  <g class="up" style="animation-delay:.1s">
    <rect x="64" y="66" width="8" height="8" fill="{GILT}" class="pulse"/>
    <text x="86" y="75" class="m" font-size="12" letter-spacing="2.6" fill="{ASH}">{EYEBROW}</text>
  </g>

  <text x="58" y="210" class="up" style="animation-delay:.25s" font-size="128" letter-spacing="-3" fill="{BONE}">
    <tspan class="d">{FIRST} </tspan><tspan class="a" fill="{GILT}">{LAST}</tspan>
  </text>

  <g class="up b" style="animation-delay:.45s" font-size="22" fill="{ASH}">
    <text x="64" y="272">{TAGLINE}</text>
    <text x="64" y="302">{TAGLINE2}</text>
  </g>

  <line class="rule" x1="64" y1="352.5" x2="{W - 64}" y2="352.5" stroke="{GILT}" stroke-opacity=".55"/>
  <g class="up m" style="animation-delay:1.1s" font-size="11" letter-spacing="2.4" fill="{ASH}">
    <text x="64" y="380">{META[0]}</text>
    <text x="{W - 64}" y="380" text-anchor="end">{META[1]}</text>
  </g>
</g>
</svg>'''

(ROOT / "assets" / "header.svg").write_text(svg)
print("wrote assets/header.svg", round(len(svg) / 1024), "KB")
