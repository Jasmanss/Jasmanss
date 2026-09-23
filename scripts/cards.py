"""Render the project and experience cards (assets/cards/*.jpg) with headless Chrome.

Needs Google Chrome installed locally. Run: python3 scripts/cards.py
"""
import subprocess
import tempfile
from pathlib import Path

from brand import ROOT, INK, PANEL, LINE, BONE, ASH, GILT, font_files_css

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SHOTS = ROOT / "scripts" / "shots"
OUT = ROOT / "assets" / "cards"

BASE_CSS = f"""
{font_files_css()}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: {INK}; color: {BONE}; overflow: hidden; }}
body {{ font-family: 'Archivo', system-ui, sans-serif; -webkit-font-smoothing: antialiased; }}
.card {{ position: relative; overflow: hidden; border: 1px solid {LINE}; border-radius: 22px;
  background: radial-gradient(120% 90% at 100% 0%, rgba(214,165,74,.10), transparent 55%), {INK}; }}
.d {{ font-family: 'Fraunces Display', Georgia, serif; font-weight: 400; letter-spacing: -.02em; }}
.a {{ font-family: 'Fraunces Accent', Georgia, serif; font-style: italic; color: {GILT}; }}
.m {{ font-family: 'Martian Mono', ui-monospace, monospace; text-transform: uppercase; letter-spacing: .2em; }}
.ash {{ color: {ASH}; }}
.gilt {{ color: {GILT}; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 10px; }}
.chip {{ border: 1px solid {LINE}; border-radius: 999px; padding: 9px 16px; color: {ASH}; background: rgba(26,20,15,.6); }}
.win {{ position: absolute; border: 1px solid #3A3026; border-radius: 16px; overflow: hidden; background: {PANEL};
  box-shadow: 0 40px 80px -20px rgba(0,0,0,.7), 0 0 0 1px rgba(0,0,0,.4); }}
.bar {{ height: 40px; display: flex; align-items: center; gap: 8px; padding: 0 18px; border-bottom: 1px solid #3A3026; background: {PANEL}; }}
.bar i {{ width: 11px; height: 11px; border-radius: 50%; background: #3A3026; display: block; }}
.bar span {{ margin-left: 14px; font-size: 12px; color: {ASH}; }}
.shot {{ display: block; width: 100%; }}
.shot.cover {{ height: calc(100% - 40px); object-fit: cover; object-position: left top; }}
.cta {{ display: inline-flex; gap: 14px; align-items: center; color: {GILT}; }}
.cta::after {{ content: ""; width: 36px; height: 1px; background: {GILT}; }}
"""


def render(name, html, width, height):
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "card.html"
        png = Path(tmp) / "card.png"
        page.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}</style></head>"
                        f"<body style='width:{width}px;height:{height}px'>{html}</body></html>")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--allow-file-access-from-files", "--force-device-scale-factor=2",
                        f"--window-size={width},{height}", f"--screenshot={png}", page.as_uri()],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "84", str(png),
                        "--out", str(OUT / f"{name}.jpg")], stdout=subprocess.DEVNULL, check=True)
    print("wrote", f"assets/cards/{name}.jpg")


def window(url, body, style):
    return (f'<div class="win" style="{style}"><div class="bar"><i></i><i></i><i></i>'
            f'<span class="m">{url}</span></div>{body}</div>')


def shot(file, cover=False):
    return f'<img class="shot{" cover" if cover else ""}" src="{(SHOTS / file).as_uri()}">'


IMPERIUM_UI = f"""
<div style="display:flex;height:560px;font-size:17px">
  <div style="width:300px;border-right:1px solid #3A3026;padding:30px 24px;display:flex;flex-direction:column;gap:14px">
    <div class="m ash" style="font-size:10px">Phone · paired</div>
    <div style="align-self:flex-end;background:{GILT};color:{INK};padding:12px 16px;border-radius:18px 18px 4px 18px;max-width:230px">open spotify and play my focus mix</div>
    <div style="align-self:flex-start;background:#2A2119;padding:12px 16px;border-radius:18px 18px 18px 4px;max-width:230px">Done. Playing “Focus” on Spotify.</div>
    <div style="align-self:flex-end;background:{GILT};color:{INK};padding:12px 16px;border-radius:18px 18px 4px 18px;max-width:230px">git status on imperium</div>
  </div>
  <div style="flex:1;padding:30px 30px;font-family:'Martian Mono',monospace;font-size:13px;line-height:2.3;color:{ASH}">
    <div style="opacity:.6">imperium-agent · mac</div>
    <div><span class="gilt">✓</span> auth&nbsp;&nbsp;&nbsp;&nbsp; bearer token · paired</div>
    <div><span class="gilt">✓</span> intent&nbsp;&nbsp; claude → media.play</div>
    <div><span class="gilt">✓</span> permit&nbsp;&nbsp; low risk · no confirm</div>
    <div><span class="gilt">✓</span> policy&nbsp;&nbsp; script passes gate</div>
    <div><span class="gilt">▶</span> exec&nbsp;&nbsp;&nbsp;&nbsp; tell app "Spotify"…</div>
    <div><span class="gilt">✓</span> audit&nbsp;&nbsp;&nbsp; entry written</div>
    <div style="margin-top:10px;color:{BONE}">❯ <span style="display:inline-block;width:9px;height:17px;background:{GILT};vertical-align:middle"></span></div>
  </div>
</div>"""

HAIRSTYL_UI = f"""
<div style="height:340px;background:#000;display:flex;align-items:center;justify-content:center;padding-right:40px">
  <img src="{(SHOTS / 'hairstyl-logo.jpg').as_uri()}" style="width:440px">
</div>"""

FEATURED = [
    dict(key="imperium", num="01", title="Imperium", tagline="Text your Mac. It does the thing.",
         body="A FastAPI agent on the Mac turns plain English into AppleScript with Claude. "
              "Every command clears token-paired auth, a tiered permission model, a script policy gate, "
              "and lands in an audit log.",
         stack=["Python", "FastAPI", "Claude API", "Next.js"],
         facts=[("4", "security layers per command"), ("v2", "hardened rebuild of the hackathon demo")],
         url="imperium · local agent", visual=IMPERIUM_UI, side="right"),
    dict(key="callback", num="02", title="Callback", tagline="You applied. Then, silence.",
         body="A job application tracker that follows up. Board and table views, email import, "
              "and reminders, and anything that goes quiet for four months moves to Ghosted on its own. "
              "No account; your data stays in your browser.",
         stack=["TypeScript", "React", "Vite"],
         facts=[("0", "servers or accounts"), ("4 mo", "until auto-ghosted")],
         url="jasmanss.github.io/callback", visual=shot("callback.jpg", cover=True), side="left"),
]

COMPACT = [
    dict(key="portlkit", title="Portlkit", tagline="Get paid by the client you already have.",
         stack=["Next.js", "Supabase", "Stripe"], badge="In development", url="portlkit", visual=shot("portl.jpg")),
    dict(key="haven", title="Haven", tagline="A household's money, in one calm place.",
         stack=["Next.js", "Supabase", "Plaid"], badge="Live", url="haven-money.vercel.app", visual=shot("haven.jpg")),
    dict(key="hairstyl", title="Hairstyl", tagline="A selfie in, a grooming routine out.",
         stack=["Swift", "SwiftUI", "OpenAI"], badge="150+ users", url="ios app", visual=HAIRSTYL_UI),
    dict(key="aroma", title="Aroma AI", tagline="A photo in, your next fragrance out.",
         stack=["Python", "OpenCV", "JavaScript"], badge="Best UI/UX · GrizzHacks 7", url="jasmanss.github.io/aromaai",
         visual=shot("aroma.jpg")),
]


def featured(p):
    W, H = 1200, 640
    text_x = 64 if p["side"] == "right" else 640
    win_style = ("left:600px;top:72px;width:720px;height:620px" if p["side"] == "right"
                 else "left:-30px;top:72px;width:620px;height:620px")
    facts = "".join(
        f'<div><div class="d gilt" style="font-size:44px;line-height:1">{v}</div>'
        f'<div class="m ash" style="font-size:10px;margin-top:10px;max-width:180px;line-height:1.6">{k}</div></div>'
        for v, k in p["facts"])
    chips = "".join(f'<span class="chip m" style="font-size:10px">{s}</span>' for s in p["stack"])
    html = f"""
<div class="card" style="width:{W}px;height:{H}px">
  {window(p['url'], p['visual'], win_style)}
  <div style="position:absolute;left:{text_x}px;top:64px;width:500px">
    <div class="m gilt" style="font-size:12px">{p['num']} / Featured</div>
    <div class="d" style="font-size:84px;line-height:1;margin-top:22px">{p['title']}</div>
    <div class="a" style="font-size:30px;margin-top:12px">{p['tagline']}</div>
    <p class="ash" style="font-size:18px;line-height:1.6;margin-top:24px">{p['body']}</p>
    <div style="display:flex;gap:48px;margin-top:30px">{facts}</div>
    <div class="chips" style="margin-top:34px">{chips}</div>
  </div>
</div>"""
    render(p["key"], html, W, H)


def compact(p):
    W, H = 600, 640
    chips = "".join(f'<span class="chip m" style="font-size:10px;padding:8px 14px">{s}</span>' for s in p["stack"])
    html = f"""
<div class="card" style="width:{W}px;height:{H}px">
  {window(p['url'], p['visual'], "left:40px;top:40px;width:640px;height:380px")}
  <div style="position:absolute;left:40px;right:40px;top:452px">
    <div style="display:flex;justify-content:space-between;align-items:baseline">
      <div class="d" style="font-size:52px;line-height:1">{p['title']}</div>
      <div class="m gilt" style="font-size:10px">{p['badge']}</div>
    </div>
    <div class="a" style="font-size:24px;margin-top:10px">{p['tagline']}</div>
    <div class="chips" style="margin-top:22px">{chips}</div>
  </div>
</div>"""
    render(p["key"], html, W, H)


def experience():
    W, H = 1200, 760
    metrics = [("150+", "active users in four months"), ("−30%", "onboarding drop-off"),
               ("~2s", "per AI analysis"), ("80%+", "analysis accuracy")]
    tiles = "".join(
        f'<div style="border:1px solid {LINE};border-radius:16px;padding:26px 24px;background:rgba(26,20,15,.6)">'
        f'<div class="d gilt" style="font-size:54px;line-height:1">{v}</div>'
        f'<div class="m ash" style="font-size:10px;margin-top:14px;line-height:1.7">{k}</div></div>'
        for v, k in metrics)
    entry = lambda when, title, where, note: f"""
      <div style="display:grid;grid-template-columns:220px 1fr;gap:32px;padding:30px 0;border-top:1px solid {LINE}">
        <div class="m ash" style="font-size:11px;padding-top:8px;line-height:1.8">{when}</div>
        <div><div class="d" style="font-size:30px">{title} <span class="a" style="font-size:26px">{where}</span></div>
        <div class="ash" style="font-size:16px;margin-top:8px;line-height:1.6">{note}</div></div>
      </div>"""
    html = f"""
<div class="card" style="width:{W}px;height:{H}px;padding:60px 64px">
  <div style="display:grid;grid-template-columns:220px 1fr;gap:32px">
    <div>
      <div class="m gilt" style="font-size:11px;line-height:1.8">May 2025 —<br>Present</div>
      <div style="display:flex;align-items:center;gap:10px;margin-top:22px">
        <span style="width:8px;height:8px;border-radius:50%;background:{GILT};box-shadow:0 0 0 6px rgba(214,165,74,.15)"></span>
        <span class="m ash" style="font-size:10px">Current</span></div>
    </div>
    <div>
      <div class="d" style="font-size:46px;line-height:1.1">Frontend Developer &amp; Co-Founder</div>
      <div class="a" style="font-size:28px;margin-top:8px">Vengeance Intelligence LLC</div>
      <p class="ash" style="font-size:18px;line-height:1.6;margin-top:18px;max-width:780px">
        Co-founded the company and led frontend and product for Hairstyl, an iOS grooming app.
        I built it in Swift and SwiftUI from photo capture through AI analysis to routines, and
        reworked the onboarding, capture, results, and tracking flows as it grew.</p>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:30px">{tiles}</div>
    </div>
  </div>
  <div style="margin-top:36px">
    {entry("Hackathon", "Best UI/UX,", "GrizzHacks 7", "Won with Aroma AI, a fragrance recommender that matches scents from a photo or a short quiz.")}
    {entry("Education", "Computer Science,", "Oakland University", "Studying CS in Rochester, Michigan, and shipping side projects along the way.")}
  </div>
</div>"""
    render("experience", html, W, H)


if __name__ == "__main__":
    for p in FEATURED:
        featured(p)
    for p in COMPACT:
        compact(p)
    experience()
