"""Build assets/hero.svg: the animated profile header.

Run:  python scripts/build_hero.py
Pure SVG + CSS/SMIL animation, no scripts and no external resources, so it
renders inside GitHub's <img> sandbox.
"""

from pathlib import Path

W, H = 1200, 420
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"

PHRASES = [
    "building simulation-ready multi-storey worlds",
    "designing stairs a humanoid can actually climb",
    "acceptance gates that are built to fail",
    "training humanoid policies in physics simulation",
]
TYPE_X, TYPE_Y, TYPE_SIZE = 84, 250, 20
CHAR_W = TYPE_SIZE * 0.6  # monospace advance
SLOT = 5.0  # seconds per phrase
TYPE_T, HOLD_T, DEL_T = 2.2, 2.0, 0.6


def typing_block() -> str:
    """One clipped <text> per phrase; clip width steps through the characters."""
    total = SLOT * len(PHRASES)
    parts = []
    for i, phrase in enumerate(PHRASES):
        n = len(phrase)
        t0 = i * SLOT
        times, widths = [0.0], [0.0]
        for k in range(1, n + 1):  # typing
            times.append(t0 + TYPE_T * k / n)
            widths.append(CHAR_W * k)
        times.append(t0 + TYPE_T + HOLD_T)  # hold
        widths.append(CHAR_W * n)
        steps = 12
        for k in range(1, steps + 1):  # deleting
            times.append(t0 + TYPE_T + HOLD_T + DEL_T * k / steps)
            widths.append(CHAR_W * n * (1 - k / steps))
        times.append(t0 + SLOT - 0.02)  # hide the cursor once the slot ends
        widths.append(0.0)
        if t0 > 0:  # stay empty until this phrase's slot
            times.insert(1, t0)
            widths.insert(1, 0.0)
        times.append(total)
        widths.append(0.0)
        key_times = ";".join(f"{t / total:.4f}" for t in times)
        values = ";".join(f"{w:.1f}" for w in widths)
        cursor_x = ";".join(f"{TYPE_X + w + 2:.1f}" for w in widths)
        cursor_on = ";".join("visible" if t0 <= t < t0 + SLOT - 0.05 else "hidden" for t in times)
        parts.append(f"""
    <clipPath id="tc{i}"><rect x="{TYPE_X}" y="{TYPE_Y - 24}" height="34" width="0">
      <animate attributeName="width" dur="{total}s" repeatCount="indefinite" calcMode="discrete"
               keyTimes="{key_times}" values="{values}"/></rect></clipPath>
    <text x="{TYPE_X}" y="{TYPE_Y}" class="typed" clip-path="url(#tc{i})">{phrase}</text>
    <rect class="cursor" y="{TYPE_Y - 18}" width="10" height="22" x="{TYPE_X}" visibility="hidden">
      <animate attributeName="x" dur="{total}s" repeatCount="indefinite" calcMode="discrete"
               keyTimes="{key_times}" values="{cursor_x}"/>
      <animate attributeName="visibility" dur="{total}s" repeatCount="indefinite" calcMode="discrete"
               keyTimes="{key_times}" values="{cursor_on}"/>
    </rect>""")
    return "".join(parts)


# --- building cross-section (right half) ---------------------------------
GX0, GX1 = 650, 1150          # building extent
G_Y, F2_Y, ROOF_Y = 352, 212, 92
STEPS = 14
S_X0, S_X1 = 770, 994         # stair foot / head
RISE = (G_Y - F2_Y) / STEPS
RUN = (S_X1 - S_X0) / STEPS


def stair() -> str:
    pts = [(S_X0, G_Y)]
    x, y = S_X0, G_Y
    for _ in range(STEPS):
        y -= RISE
        pts.append((x, y))
        x += RUN
        pts.append((x, y))
    outline = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    body = outline + f" {S_X1:.1f},{F2_Y + 14:.1f} {S_X0 + 26:.1f},{G_Y:.1f}"
    return (f'<polygon points="{body}" fill="url(#stairFill)" opacity=".9"/>'
            f'<polyline points="{outline}" class="tread"/>')


def voxels() -> str:
    """Small voxel cells on each tread; they light up when the scan line passes."""
    cells = []
    scan_dur = 6.0
    x, y = S_X0, G_Y
    for _ in range(STEPS):
        y -= RISE
        for j in range(3):
            cx = x + 2 + j * (RUN / 3)
            delay = (cx - GX0) / (GX1 - GX0) * scan_dur
            cells.append(f'<rect class="vox" x="{cx:.1f}" y="{y - 5:.1f}" width="4.2" height="4.2" '
                         f'style="animation-delay:{delay:.2f}s"/>')
        x += RUN
    for fx in range(GX0 + 14, GX1 - 10, 12):  # floor slabs
        for fy in (G_Y - 5, F2_Y - 5):
            if fy == F2_Y - 5 and S_X1 - 120 < fx < S_X1:  # stair opening
                continue
            delay = (fx - GX0) / (GX1 - GX0) * scan_dur
            cells.append(f'<rect class="vox dim" x="{fx}" y="{fy}" width="4.2" height="4.2" '
                         f'style="animation-delay:{delay:.2f}s"/>')
    return "".join(cells)


def humanoid() -> str:
    """Stick humanoid walking up the flight. Origin = feet."""
    cycle = 10.0
    path = [  # (t, x, y)
        (0.0, 690, G_Y), (1.6, S_X0 - 6, G_Y), (6.4, S_X1, F2_Y),
        (8.2, 1092, F2_Y), (10.0, 1092, F2_Y),
    ]
    kt = ";".join(f"{t / cycle:.3f}" for t, _, _ in path)
    vals = ";".join(f"{x} {y}" for _, x, y in path)
    return f"""
  <g>
    <animateTransform attributeName="transform" type="translate" dur="{cycle}s" repeatCount="indefinite"
                      keyTimes="{kt}" values="{vals}"/>
    <animate attributeName="opacity" dur="{cycle}s" repeatCount="indefinite"
             keyTimes="0;0.06;0.8;0.88;1" values="0;1;1;0;0"/>
    <g class="bob"><g transform="scale(.82)" class="figure">
      <ellipse cx="0" cy="0" rx="16" ry="3" fill="#000" opacity=".35"/>
      <g class="leg legA"><line x1="0" y1="-44" x2="0" y2="-2" class="limb"/></g>
      <g class="leg legB"><line x1="0" y1="-44" x2="0" y2="-2" class="limb"/></g>
      <line x1="0" y1="-44" x2="1" y2="-80" class="limb torso"/>
      <g class="arm armA"><line x1="1" y1="-76" x2="1" y2="-50" class="limb thin"/></g>
      <g class="arm armB"><line x1="1" y1="-76" x2="1" y2="-50" class="limb thin"/></g>
      <circle cx="2" cy="-89" r="7.5" class="head"/>
    </g></g>
  </g>"""


def pipeline() -> str:
    labels = ["scan storeys", "connect stairs", "voxel bake", "accept"]
    x, y = 56, 318
    out, centers = [], []
    for i, lab in enumerate(labels):
        w = len(lab) * 7.8 + 26
        out.append(f'<rect x="{x}" y="{y - 17}" width="{w:.0f}" height="28" rx="14" class="pill"/>'
                   f'<text x="{x + w / 2:.0f}" y="{y + 1}" class="pilltxt" text-anchor="middle">{lab}</text>')
        centers.append((x, x + w))
        x += w + 26
    links = []
    for (a0, a1), (b0, b1) in zip(centers, centers[1:]):
        links.append(f'<line x1="{a1 + 3:.0f}" y1="{y - 3}" x2="{b0 - 3:.0f}" y2="{y - 3}" class="link"/>')
    span0, span1 = centers[0][1], centers[-1][0]
    pulse = (f'<circle r="3.6" cy="{y - 3}" cx="0" class="pulse">'
             f'<animate attributeName="cx" dur="3.2s" repeatCount="indefinite" '
             f'values="{span0:.0f};{span1:.0f}"/></circle>')
    return "".join(links) + pulse + "".join(out)


def build() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
     aria-label="Ma Yixing (Jimmy) — Embodied AI, humanoid robotics and simulation-ready 3D scene generation">
  <title>Ma Yixing (Jimmy) — Embodied AI · Humanoid Robotics · 3D Scene Generation</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#060a17"/><stop offset=".55" stop-color="#0a1330"/><stop offset="1" stop-color="#130b26"/>
    </linearGradient>
    <radialGradient id="glow" cx="76%" cy="46%" r="52%">
      <stop offset="0" stop-color="#3fd6ff" stop-opacity=".16"/><stop offset=".6" stop-color="#7b5cff" stop-opacity=".07"/>
      <stop offset="1" stop-color="#060a17" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#bfeaff"/>
    </linearGradient>
    <linearGradient id="stairFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1d3a63"/><stop offset="1" stop-color="#0c1630"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#3fd6ff" stop-opacity="0"/><stop offset=".85" stop-color="#3fd6ff" stop-opacity=".22"/>
      <stop offset="1" stop-color="#8af6ff" stop-opacity=".9"/>
    </linearGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="#5f7bb5" stroke-width=".6"/>
    </pattern>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    <clipPath id="bldg"><rect x="{GX0}" y="{ROOF_Y - 6}" width="{GX1 - GX0}" height="{G_Y - ROOF_Y + 12}"/></clipPath>
  </defs>
  <style>
    .eyebrow {{ font: 600 12.5px {MONO}; letter-spacing: 3px; fill: #6fb7d6; }}
    .name    {{ font: 700 58px {SANS}; fill: url(#name); letter-spacing: .5px; }}
    .sub     {{ font: 400 17px {SANS}; fill: #9aa8c7; }}
    .typed   {{ font: 500 {TYPE_SIZE}px {MONO}; fill: #5fe0ff; }}
    .prompt  {{ font: 700 {TYPE_SIZE}px {MONO}; fill: #ff5fd8; }}
    .cursor  {{ fill: #5fe0ff; animation: blink 1s steps(1) infinite; }}
    .pill    {{ fill: #0d1834; stroke: #2a4a7a; stroke-width: 1; }}
    .pilltxt {{ font: 500 12.5px {MONO}; fill: #b8c7e6; }}
    .link    {{ stroke: #2a4a7a; stroke-width: 1.4; stroke-dasharray: 3 4; }}
    .pulse   {{ fill: #ff5fd8; filter: drop-shadow(0 0 4px #ff5fd8); }}
    .status  {{ font: 400 13px {MONO}; fill: #7f8db0; }}
    .dot     {{ fill: #3ee08f; animation: breathe 2.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
    .wall    {{ fill: none; stroke: #36507f; stroke-width: 2; }}
    .slab    {{ fill: #13213f; stroke: #3b5c94; stroke-width: 1.4; }}
    .tread   {{ fill: none; stroke: #6fd3ff; stroke-width: 2; stroke-linejoin: round; }}
    .vox     {{ fill: #6ff0ff; opacity: .12; animation: vox 6s linear infinite; }}
    .vox.dim {{ fill: #4fa8ff; }}
    .scanbar {{ animation: scan 6s linear infinite; }}
    .lab     {{ font: 500 11.5px {MONO}; fill: #8fb0d8; }}
    .labk    {{ font: 600 11.5px {MONO}; fill: #ff8fe4; }}
    .hud     {{ fill: #0b1530; stroke: #2a4a7a; stroke-width: 1; }}
    .limb    {{ stroke: #3d8bff; stroke-width: 6.5; stroke-linecap: round; }}
    .limb.thin {{ stroke-width: 5; }}
    .torso   {{ stroke-width: 8.5; }}
    .head    {{ fill: #3d8bff; }}
    .figure  {{ filter: drop-shadow(0 0 6px rgba(61,139,255,.55)); }}
    .leg, .arm {{ transform-box: view-box; }}
    .leg     {{ transform-origin: 0 -44px; }}
    .arm     {{ transform-origin: 1px -76px; }}
    .legA    {{ animation: swing .7s ease-in-out infinite alternate; }}
    .legB    {{ animation: swing .7s ease-in-out infinite alternate-reverse; }}
    .armA    {{ animation: swingS .7s ease-in-out infinite alternate-reverse; }}
    .armB    {{ animation: swingS .7s ease-in-out infinite alternate; }}
    .bob     {{ animation: bob .35s ease-in-out infinite alternate; }}
    .gridg   {{ animation: drift 14s linear infinite; }}
    @keyframes blink   {{ 0%,50% {{ opacity: 1; }} 50.01%,100% {{ opacity: 0; }} }}
    @keyframes breathe {{ 0%,100% {{ opacity: .45; transform: scale(.8); }} 50% {{ opacity: 1; transform: scale(1.15); }} }}
    @keyframes vox     {{ 0% {{ opacity: .12; }} 2% {{ opacity: 1; }} 14% {{ opacity: .38; }} 100% {{ opacity: .12; }} }}
    @keyframes scan    {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX({GX1 - GX0 + 40}px); }} }}
    @keyframes swing   {{ from {{ transform: rotate(-24deg); }} to {{ transform: rotate(24deg); }} }}
    @keyframes swingS  {{ from {{ transform: rotate(-18deg); }} to {{ transform: rotate(18deg); }} }}
    @keyframes bob     {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-2.5px); }} }}
    @keyframes drift   {{ from {{ transform: translate(0,0); }} to {{ transform: translate(28px,28px); }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <g opacity=".07"><g class="gridg"><rect x="-28" y="-28" width="{W + 56}" height="{H + 56}" fill="url(#grid)"/></g></g>
    <rect width="{W}" height="{H}" fill="url(#glow)"/>

    <!-- left: identity -->
    <text x="56" y="76" class="eyebrow">EMBODIED AI · HUMANOID ROBOTICS · 3D SCENE GENERATION</text>
    <text x="54" y="146" class="name">Ma Yixing</text>
    <text x="56" y="184" class="sub">Jimmy  ·  Computer Science with AI  ·  University of Nottingham</text>
    <text x="56" y="{TYPE_Y}" class="prompt">&gt;</text>
    {typing_block()}
    <line x1="56" y1="280" x2="600" y2="280" stroke="#1f2d52" stroke-width="1"/>
    {pipeline()}
    <circle cx="62" cy="372" r="5" class="dot"/>
    <text x="76" y="376" class="status">research focus: humanoid locomotion in generated buildings</text>

    <!-- right: two-storey cross-section -->
    <g>
      <rect x="{GX0}" y="{ROOF_Y}" width="{GX1 - GX0}" height="{G_Y - ROOF_Y}" fill="#0a1228" opacity=".55"/>
      <path d="M{GX0} {G_Y} V{ROOF_Y} H{GX1} V{G_Y}" class="wall"/>
      <rect x="{GX0 - 20}" y="{G_Y}" width="{GX1 - GX0 + 40}" height="10" class="slab"/>
      <rect x="{GX0}" y="{F2_Y}" width="{S_X1 - 120 - GX0}" height="9" class="slab"/>
      <rect x="{S_X1}" y="{F2_Y}" width="{GX1 - S_X1}" height="9" class="slab"/>
      <rect x="{GX0}" y="{ROOF_Y - 9}" width="{GX1 - GX0}" height="9" class="slab"/>
      {stair()}
      <g clip-path="url(#bldg)">{voxels()}
        <g class="scanbar"><rect x="{GX0 - 40}" y="{ROOF_Y}" width="40" height="{G_Y - ROOF_Y}" fill="url(#scan)"/></g>
      </g>
      <!-- labels -->
      <text x="{GX0 + 12}" y="{F2_Y - 14}" class="lab">storey 2</text>
      <text x="{GX0 + 12}" y="{G_Y - 14}" class="lab">storey 1</text>
      <line x1="{S_X0 + 70}" y1="{G_Y - 50}" x2="{S_X0 + 30}" y2="{G_Y - 92}" stroke="#4a6aa0" stroke-width="1"/>
      <text x="{S_X0 - 64}" y="{G_Y - 98}" class="lab">riser ≤ 0.20 m</text>
      <text x="{GX1 - 84}" y="{G_Y - 14}" class="lab">voxel 5 cm</text>
      <rect x="{GX0 + 14}" y="{ROOF_Y + 16}" width="252" height="54" rx="8" class="hud"/>
      <text x="{GX0 + 28}" y="{ROOF_Y + 38}" class="labk">STANDABILITY CHECK</text>
      <text x="{GX0 + 28}" y="{ROOF_Y + 58}" class="lab">r 0.25 m · h 1.60 m · step 0.20 m</text>
      {humanoid()}
    </g>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="#1d2a4d"/>
</svg>
"""


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "hero.svg"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
