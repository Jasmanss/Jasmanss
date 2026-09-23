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


def shot(file, cover=False, focus="left top"):
    style = f' style="object-position:{focus}"' if cover else ""
    return f'<img class="shot{" cover" if cover else ""}"{style} src="{(SHOTS / file).as_uri()}">'


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
    dict(key="portlkit", num="01", title="Portlkit", tagline="Get paid by the client you already have.",
         body="White-label client portals for freelancers and small studios. Invoices, milestones, files, "
              "and messages live behind one shareable link, so clients never make an account. Postgres "
              "row-level security and unguessable share tokens keep each client's data private.",
         stack=["Next.js", "Supabase", "Postgres", "Vercel"],
         facts=[("1 link", "per client, no client accounts"), ("Auto", "overdue-invoice reminders")],
         url="portlkit.com", visual=shot("portlkit.jpg", cover=True, focus="center"), side="left"),
    dict(key="imperium", num="02", title="Imperium", tagline="Text your Mac. It does the thing.",
         body="A FastAPI agent on the Mac turns plain English into actions with Claude: open apps, send "
              "email, run Git, all from your phone. Pairing tokens, permission controls, and confirmation "
              "gates block destructive commands.",
         stack=["Python", "FastAPI", "Claude API", "Next.js"],
         facts=[("Evals", "in CI fail the build if safety weakens"), ("4", "gates on every command")],
         url="imperium · local agent", visual=IMPERIUM_UI, side="right"),
]

COMPACT = [
    dict(key="hairstyl", title="HairStyl", tagline="A selfie in, a grooming routine out.",
         stack=["Swift", "SwiftUI", "OpenAI", "Supabase"], badge="150+ users", url="ios · testflight", visual=HAIRSTYL_UI),
    dict(key="callback", title="Callback", tagline="You applied. Then, silence.",
         stack=["React", "TypeScript", "AWS"], badge="Live", url="jasmanss.github.io/callback",
         visual=shot("callback.jpg")),
    dict(key="haven", title="Haven", tagline="A household's money, in one calm place.",
         stack=["Next.js", "Supabase", "Plaid"], badge="Live", url="haven-money.vercel.app", visual=shot("haven.jpg")),
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
    W, H = 1200, 950

    def tiles(items):
        return "".join(
            f'<div style="border:1px solid {LINE};border-radius:14px;padding:20px 22px;background:rgba(26,20,15,.6)">'
            f'<div class="d gilt" style="font-size:44px;line-height:1">{v}</div>'
            f'<div class="m ash" style="font-size:10px;margin-top:12px;line-height:1.7">{k}</div></div>'
            for v, k in items)

    def chips(items):
        return "".join(f'<span class="chip m" style="font-size:10px;padding:7px 13px">{c}</span>' for c in items)

    def role(when, where, current, title, org, body, facts, stack, first=False):
        dot = (f'<div style="display:flex;align-items:center;gap:10px;margin-top:18px">'
               f'<span style="width:8px;height:8px;border-radius:50%;background:{GILT};box-shadow:0 0 0 6px rgba(214,165,74,.15)"></span>'
               f'<span class="m ash" style="font-size:10px">Current</span></div>') if current else ""
        border = "" if first else f"border-top:1px solid {LINE};"
        grid = (f'<div style="display:grid;grid-template-columns:repeat({len(facts)},1fr);gap:12px;margin-top:22px">'
                f'{tiles(facts)}</div>') if facts else ""
        return f"""
  <div style="display:grid;grid-template-columns:200px 1fr;gap:36px;padding:34px 0;{border}">
    <div><div class="m gilt" style="font-size:11px;line-height:1.8">{when}</div>
      <div class="m ash" style="font-size:10px;margin-top:8px;line-height:1.8">{where}</div>{dot}</div>
    <div>
      <div class="d" style="font-size:38px;line-height:1.1">{title}</div>
      <div class="a" style="font-size:24px;margin-top:6px">{org}</div>
      <p class="ash" style="font-size:17px;line-height:1.6;margin-top:14px;max-width:820px">{body}</p>
      {grid}
      <div class="chips" style="margin-top:20px">{chips(stack)}</div>
    </div>
  </div>"""

    html = f"""
<div class="card" style="width:{W}px;height:{H}px;padding:26px 64px">
  {role("May 2026 —<br>Present", "Sterling Heights, MI", True,
        "Software Engineering Intern", "Motherson Group",
        "Replaced paper maintenance checklists with a web app technicians use from their phones via QR codes. "
        "Built MTTR, MTBF, and compliance dashboards for supervisors, automated Teams alerts with Power Automate, "
        "and deployed it on-prem on Ubuntu with Gunicorn, systemd, HTTPS, and automated backups.",
        [("147", "machines off paper checklists"), ("400+", "pytest tests on production flows"), ("QR", "maintenance from a phone")],
        ["Python", "Flask", "SQL", "JavaScript", "Power Automate", "Ubuntu"], first=True)}
  {role("June 2026 —<br>Present", "Remote · Part-time", True,
        "Frontend Developer", "Aurelius Holdings LLC",
        "Building the customer-facing frontend of a live ecommerce site: reusable components and routed pages, "
        "cart state, pricing rules, and form validation, wired to Supabase for products, orders, and auth. "
        "Ship weekly through Vercel and fix customer-reported bugs in production.",
        [], ["React", "TypeScript", "Vite", "Supabase", "Vercel"])}
  <div style="display:grid;grid-template-columns:200px 1fr;gap:36px;padding:30px 0 0;border-top:1px solid {LINE}">
    <div><div class="m gilt" style="font-size:11px;line-height:1.8">Expected<br>May 2027</div>
      <div class="m ash" style="font-size:10px;margin-top:8px;line-height:1.8">Rochester Hills, MI</div></div>
    <div>
      <div class="d" style="font-size:30px;line-height:1.15">B.S. Computer Science, <span class="a" style="font-size:26px">Oakland University</span></div>
      <div class="ash" style="font-size:16px;margin-top:8px;line-height:1.6">Concentration in Artificial Intelligence. Coursework in data structures &amp; algorithms, software engineering, databases, operating systems, and networks.</div>
    </div>
  </div>
</div>"""
    render("experience", html, W, H)


if __name__ == "__main__":
    for p in FEATURED:
        featured(p)
    for p in COMPACT:
        compact(p)
    experience()
