"""Shared palette and fonts for every generated asset.

Palette and type come from the portfolio (jasmanss.com): warm ink, bone text, gilt accent,
Fraunces for display, Martian Mono for labels, Archivo for body copy.
"""
import base64
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "scripts" / "fonts"

INK = "#120D09"
PANEL = "#1A140F"
LINE = "#2F261E"
BONE = "#EEE4D2"
ASH = "#A0917C"
GILT = "#D6A54A"
GILT_DEEP = "#9C7428"  # gilt that holds up on a white background
GILT_RAMP = ["#D6A54A", "#B98A36", "#957029", "#6F5320", "#4A3818"]

FAMILIES = {
    "display": "Fraunces Display",
    "accent": "Fraunces Accent",
    "mono": "Martian Mono",
    "body": "Archivo",
    "bodybold": "Archivo Bold",
}


def font_css(**texts):
    """@font-face rules embedding only the glyphs each string needs.

    font_css(display="Jasman Sidhu", mono="CS · 2025") -> CSS text. Images on GitHub
    can't fetch web fonts, so each SVG carries its own subset.
    """
    from fontTools import subset
    from fontTools.ttLib import TTFont

    rules = []
    for key, text in texts.items():
        font = TTFont(FONTS / f"{key}.ttf")
        opts = subset.Options()
        opts.flavor = "woff"
        opts.layout_features = ["*"]
        sub = subset.Subsetter(opts)
        sub.populate(text=text + " ")
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff"
        font.save(buf)
        data = base64.b64encode(buf.getvalue()).decode()
        rules.append(
            f"@font-face {{ font-family: '{FAMILIES[key]}'; "
            f"src: url(data:font/woff;base64,{data}) format('woff'); }}"
        )
    return "\n".join(rules)


def font_files_css():
    """@font-face rules pointing at the local font files, for pages rendered in Chrome."""
    return "\n".join(
        f"@font-face {{ font-family: '{fam}'; src: url('file://{FONTS / (key + '.ttf')}'); }}"
        for key, fam in FAMILIES.items()
    )


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
