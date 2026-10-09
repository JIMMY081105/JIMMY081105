"""Refresh the live parts of the profile from the GitHub API.

Writes  <out_dir>/stats-dark.svg and <out_dir>/stats-light.svg
Updates the block between the LIVE:RECENT markers in README.md.

Run:  python scripts/update_profile.py dist
Env:  GITHUB_TOKEN (optional, raises the API rate limit), PROFILE_USER.
Public data only. Jupyter Notebook bytes are left out of the language bar:
notebook outputs inflate byte counts and would hide everything else.
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "JIMMY081105")
ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_LANGS = {"Jupyter Notebook"}
LANG_COLORS = {
    "Python": "#3572A5", "C++": "#f34b7d", "C": "#555555", "Java": "#b07219",
    "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Julia": "#a270ba",
    "Shell": "#89e051", "PowerShell": "#012456", "HTML": "#e34c26",
    "CSS": "#663399", "CMake": "#DA3434", "Batchfile": "#C1F12E",
}
THEMES = {
    "dark": {"bg": "#0d1117", "border": "#30363d", "title": "#e6edf3", "text": "#9aa7b8",
             "value": "#5fe0ff", "accent": "#ff5fd8", "track": "#21262d"},
    "light": {"bg": "#ffffff", "border": "#d0d7de", "title": "#1f2328", "text": "#59636e",
              "value": "#0969da", "accent": "#bf3989", "track": "#eaeef2"},
}


def api(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": f"{USER}-profile"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def collect() -> dict:
    user = api(f"https://api.github.com/users/{USER}")
    repos = api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
    own = [r for r in repos if not r["fork"] and not r["private"]]
    langs: dict[str, int] = {}
    for r in own:
        for name, size in api(r["languages_url"]).items():
            if name not in EXCLUDED_LANGS:
                langs[name] = langs.get(name, 0) + size
    recent = sorted((r for r in own if r["name"] != USER), key=lambda r: r["pushed_at"], reverse=True)
    return {
        "public_repos": user["public_repos"],
        "followers": user["followers"],
        "stars": sum(r["stargazers_count"] for r in own),
        "langs": sorted(langs.items(), key=lambda kv: -kv[1]),
        "recent": recent[:5],
    }


def stats_svg(d: dict, theme: str) -> str:
    c = THEMES[theme]
    font = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
    mono = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    w, h = 860, 210
    total = sum(v for _, v in d["langs"]) or 1
    top = d["langs"][:6]
    other = total - sum(v for _, v in top)
    if other > 0:
        top.append(("Other", other))

    metrics = [("Public repos", d["public_repos"]), ("Stars", d["stars"]), ("Followers", d["followers"])]
    m_svg = []
    for i, (label, value) in enumerate(metrics):
        x = 32 + i * 118
        m_svg.append(
            f'<g class="fade" style="animation-delay:{0.15 * i:.2f}s">'
            f'<text x="{x}" y="104" class="num">{value}</text>'
            f'<text x="{x}" y="128" class="lab">{label}</text></g>')

    bar_x, bar_y, bar_w = 400, 74, 428
    segs, legend, x = [], [], bar_x
    for i, (name, size) in enumerate(top):
        frac = size / total
        seg_w = max(bar_w * frac, 2)
        color = LANG_COLORS.get(name, "#8b949e")
        segs.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{seg_w:.1f}" height="10" fill="{color}" '
                    f'class="grow" style="animation-delay:{0.08 * i:.2f}s"/>')
        x += seg_w
        lx = bar_x + (i % 3) * 145
        ly = bar_y + 36 + (i // 3) * 24
        legend.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{color}"/>'
                      f'<text x="{lx + 16}" y="{ly}" class="leg">{escape(name)} '
                      f'<tspan class="pct">{100 * frac:.1f}%</tspan></text>')

    latest = d["recent"][0] if d["recent"] else None
    latest_txt = (f'latest push: {escape(latest["name"])} · {latest["pushed_at"][:10]}'
                  if latest else "")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"
     aria-label="GitHub stats for {USER}: {d['public_repos']} public repos, {d['stars']} stars, {d['followers']} followers">
  <title>GitHub stats — {USER}</title>
  <style>
    .title {{ font: 600 17px {font}; fill: {c['title']}; }}
    .num   {{ font: 700 34px {font}; fill: {c['value']}; }}
    .lab   {{ font: 400 13px {font}; fill: {c['text']}; }}
    .leg   {{ font: 500 13px {font}; fill: {c['title']}; }}
    .pct   {{ fill: {c['text']}; font-weight: 400; }}
    .foot  {{ font: 400 12px {mono}; fill: {c['text']}; }}
    .live  {{ fill: {c['accent']}; animation: pulse 2s ease-in-out infinite; }}
    .fade  {{ opacity: 0; animation: fade .6s ease-out forwards; }}
    .grow  {{ transform-box: fill-box; transform-origin: left; transform: scaleX(0);
              animation: grow .9s cubic-bezier(.2,.7,.2,1) forwards; }}
    @keyframes fade  {{ to {{ opacity: 1; }} }}
    @keyframes grow  {{ to {{ transform: scaleX(1); }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{ .fade, .grow {{ animation: none; opacity: 1; transform: none; }} .live {{ animation: none; }} }}
  </style>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{c['bg']}" stroke="{c['border']}"/>
  <text x="32" y="42" class="title">GitHub at a glance</text>
  <text x="{bar_x}" y="42" class="title">Languages <tspan class="lab">· own public repos, by bytes, excl. notebooks</tspan></text>
  {''.join(m_svg)}
  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="10" rx="5" fill="{c['track']}"/>
  <g>{''.join(segs)}</g>
  {''.join(legend)}
  <line x1="32" y1="{h - 44}" x2="{w - 32}" y2="{h - 44}" stroke="{c['border']}"/>
  <circle cx="38" cy="{h - 23}" r="4" class="live"/>
  <text x="50" y="{h - 19}" class="foot">{latest_txt}</text>
  <text x="{w - 32}" y="{h - 19}" class="foot" text-anchor="end">refreshed {stamp}</text>
</svg>
"""


def recent_block(d: dict) -> str:
    rows = []
    for r in d["recent"]:
        desc = (r["description"] or "").strip()
        if len(desc) > 110:
            desc = desc[:108].rsplit(" ", 1)[0].rstrip(" ,;:—-") + "…"
        desc = f" — {desc}" if desc else ""
        rows.append(f"- [**{r['name']}**]({r['html_url']}){desc} <sub>· pushed {r['pushed_at'][:10]}</sub>")
    return "\n".join(rows)


def update_readme(d: dict) -> bool:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"(<!-- LIVE:RECENT:START -->).*?(<!-- LIVE:RECENT:END -->)", re.S)
    if not pattern.search(text):
        raise SystemExit("README.md is missing the LIVE:RECENT markers")
    new = pattern.sub(lambda m: f"{m.group(1)}\n{recent_block(d)}\n{m.group(2)}", text)
    if new != text:
        path.write_text(new, encoding="utf-8")
    return new != text


def main() -> None:
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    out_dir.mkdir(parents=True, exist_ok=True)
    d = collect()
    if not d["langs"] or d["public_repos"] == 0:
        raise SystemExit("GitHub API returned no repositories; refusing to publish an empty card")
    for theme in THEMES:
        (out_dir / f"stats-{theme}.svg").write_text(stats_svg(d, theme), encoding="utf-8")
    changed = update_readme(d)
    print(f"repos={d['public_repos']} stars={d['stars']} followers={d['followers']} "
          f"langs={len(d['langs'])} readme_changed={changed}")


if __name__ == "__main__":
    main()
