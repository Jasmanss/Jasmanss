"""Render the section headings in assets/sections/. Run: python3 scripts/sections.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INK, BONE, LIME, LINE = "#0A0B0C", "#EDEFEA", "#C8FF2E", "#2A2D30"

SECTIONS = [
    ("work", "01", "Selected work", "SIX PROJECTS, ALL SHIPPED OR SHIPPING"),
    ("experience", "02", "Experience", "2025 — NOW"),
    ("stack", "03", "Stack", "WHAT I REACH FOR"),
    ("activity", "04", "Activity", "LIVE · REFRESHED DAILY"),
]

W, H = 1200, 84
out_dir = ROOT / "assets" / "sections"
out_dir.mkdir(parents=True, exist_ok=True)

for (key, num, title, note), (theme, fg, muted, rule) in (
    (s, t) for s in SECTIONS for t in (("dark", BONE, "#8B9096", LINE), ("light", "#0A0B0C", "#6A6F75", "#D0D4D8"))
):
    title_w = len(title) * 21.5  # close enough for a bold 36px system sans
    rule_x = 112 + title_w + 28
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .mono {{ font-family: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace; }}
  .sans {{ font-family: system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif; }}
  .rule {{ transform-origin: {rule_x}px 0; animation: draw 1.2s cubic-bezier(.2,.7,.2,1) both .2s; }}
  @keyframes draw {{ from {{ transform: scaleX(0); }} }}
</style>
<rect x="0" y="22" width="84" height="42" fill="{LIME}"/>
<text x="42" y="50" text-anchor="middle" class="mono" font-size="17" letter-spacing="2" fill="{INK}">{num}</text>
<text x="112" y="56" class="sans" font-size="36" font-weight="800" letter-spacing="-.8" fill="{fg}">{title.upper()}</text>
<line class="rule" x1="{rule_x:.0f}" y1="43.5" x2="{W - len(note) * 9.3 - 28:.0f}" y2="43.5" stroke="{rule}" stroke-width="1"/>
<text x="{W}" y="48" text-anchor="end" class="mono" font-size="12" letter-spacing="2" fill="{muted}">{note}</text>
</svg>'''
    (out_dir / f"{key}-{theme}.svg").write_text(svg)
print("wrote", len(SECTIONS) * 2, "section headings")
