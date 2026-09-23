"""Render assets/stats.svg from live GitHub data, in the profile's palette.

Needs a token in GITHUB_TOKEN (the Actions token works). Run: python3 scripts/stats.py
"""
import json
import os
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USER = os.environ.get("PROFILE_USER", "Jasmanss")

INK, BONE, LIME, LINE, TILE = "#0A0B0C", "#EDEFEA", "#C8FF2E", "#24272A", "#111315"
RAMP = ["#C8FF2E", "#A3D11F", "#7A9E17", "#556F12", "#3A4B10"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    body = json.load(urllib.request.urlopen(req))
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]["user"]


def streaks(days):
    counts = {d["date"]: d["contributionCount"] for d in days}
    ordered = sorted(counts)
    longest = run = 0
    for d in ordered:
        run = run + 1 if counts[d] else 0
        longest = max(longest, run)
    # Current streak: a quiet today doesn't break it yet.
    current = 0
    day = date.fromisoformat(ordered[-1])
    if not counts[day.isoformat()]:
        day -= timedelta(days=1)
    while counts.get(day.isoformat(), 0):
        current += 1
        day -= timedelta(days=1)
    return current, longest


def languages(repos, top=5):
    totals = {}
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            totals[edge["node"]["name"]] = totals.get(edge["node"]["name"], 0) + edge["size"]
    whole = sum(totals.values()) or 1
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    shown = [(name, size / whole) for name, size in ranked[:top]]
    rest = 1 - sum(p for _, p in shown)
    if rest > 0.005:
        shown.append(("Other", rest))
    return shown


def render(user):
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]]
    current, longest = streaks(days)
    repos = user["repositories"]
    stars = sum(r["stargazerCount"] for r in repos["nodes"])
    langs = languages(repos["nodes"])

    W, H = 1200, 420
    o = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .mono {{ font-family: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace; }}
  .sans {{ font-family: system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif; }}
  .bar {{ transform-box: fill-box; transform-origin: bottom; animation: rise .9s cubic-bezier(.2,.7,.2,1) both; }}
  @keyframes rise {{ from {{ transform: scaleY(0); }} }}
  .seg {{ transform-box: fill-box; transform-origin: left; animation: grow 1.1s cubic-bezier(.2,.7,.2,1) both; }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} }}
</style>
<defs><clipPath id="f"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="{INK}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{LINE}"/>''']

    # Metrics, 4 across.
    metrics = [
        (f"{cal['totalContributions']:,}", "Contributions", "last 12 months"),
        (f"{current}", "Current streak", "days"),
        (f"{longest}", "Longest streak", "days"),
        (f"{repos['totalCount']}", "Public repos", f"{stars} stars" if stars else "and counting"),
    ]
    for k, (value, label, sub) in enumerate(metrics):
        x = 48 + k * 180
        o.append(f'<text x="{x}" y="100" class="sans" font-size="54" font-weight="800" letter-spacing="-1.5" fill="{LIME if k == 0 else BONE}">{value}</text>')
        o.append(f'<text x="{x + 2}" y="130" class="mono" font-size="11" letter-spacing="1.6" fill="{BONE}" fill-opacity=".45">{label.upper()}</text>')
        o.append(f'<text x="{x + 2}" y="148" class="mono" font-size="11" letter-spacing="1.6" fill="{BONE}" fill-opacity=".25">{sub.upper()}</text>')

    # Languages, right column.
    lx, lw = 800, 352
    o.append(f'<text x="{lx}" y="56" class="mono" font-size="11" letter-spacing="1.6" fill="{BONE}" fill-opacity=".45">LANGUAGES · PUBLIC REPOS</text>')
    x = lx
    for k, (name, p) in enumerate(langs):
        w = max(lw * p - 3, 2)
        color = LINE if name == "Other" else RAMP[k % len(RAMP)]
        o.append(f'<rect class="seg" style="animation-delay:{.15 * k:.2f}s" x="{x:.1f}" y="70" width="{w:.1f}" height="10" rx="2" fill="{color}"/>')
        x += lw * p
    for k, (name, p) in enumerate(langs):
        col, row = k % 2, k // 2
        tx, ty = lx + col * 180, 108 + row * 22
        color = LINE if name == "Other" else RAMP[k % len(RAMP)]
        o.append(f'<rect x="{tx}" y="{ty - 9}" width="9" height="9" rx="1" fill="{color}"/>')
        o.append(f'<text x="{tx + 18}" y="{ty}" class="mono" font-size="12" fill="{BONE}" fill-opacity=".8">{name}</text>')
        o.append(f'<text x="{tx + 160}" y="{ty}" text-anchor="end" class="mono" font-size="12" fill="{BONE}" fill-opacity=".45">{p * 100:.0f}%</text>')

    # Weekly contributions.
    top, base = 206, 368
    o.append(f'<line x1="48" y1="{top - 26}" x2="{W - 48}" y2="{top - 26}" stroke="{LINE}"/>')
    o.append(f'<text x="48" y="{top - 2}" class="mono" font-size="11" letter-spacing="1.6" fill="{BONE}" fill-opacity=".45">COMMITS, PRS &amp; REVIEWS PER WEEK</text>')
    peak = max(weeks) or 1
    n = len(weeks)
    span = W - 96
    bw = span / n
    chart_h = base - top - 20
    for k, v in enumerate(weeks):
        h = max(chart_h * v / peak, 2 if v else 1)
        fill = LIME if v else LINE
        op = 0.35 + 0.65 * (v / peak) if v else 1
        o.append(f'<rect class="bar" style="animation-delay:{k * 0.012:.3f}s" x="{48 + k * bw + 1:.1f}" y="{base - h:.1f}" width="{bw - 3:.1f}" height="{h:.1f}" rx="1.5" fill="{fill}" fill-opacity="{op:.2f}"/>')
    o.append(f'<text x="{W - 48}" y="{top - 2}" text-anchor="end" class="mono" font-size="11" letter-spacing="1.6" fill="{BONE}" fill-opacity=".45">PEAK {peak}/WK · <tspan fill="{LIME}" fill-opacity="1">UPDATED {date.today().isoformat()}</tspan></text>')

    # Month ticks under the chart.
    seen = set()
    for k, w in enumerate(cal["weeks"]):
        d = date.fromisoformat(w["contributionDays"][0]["date"])
        if d.day <= 7 and d.month not in seen and 0 < k < n - 2:
            seen.add(d.month)
            o.append(f'<text x="{48 + k * bw:.1f}" y="{base + 22}" class="mono" font-size="10" letter-spacing="1" fill="{BONE}" fill-opacity=".35">{d.strftime("%b").upper()}</text>')

    o.append("</g></svg>")
    return "\n".join(o)


if __name__ == "__main__":
    (ROOT / "assets" / "stats.svg").write_text(render(fetch()))
    print("wrote assets/stats.svg")
