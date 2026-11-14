"""
generate_svg.py
Fetches manushukla2's GitHub contribution data and generates
an animated SVG contribution grid — ready to embed in README.md.

Usage:
    GITHUB_TOKEN=ghp_xxx python generate_svg.py
"""

import os, json, math, requests, sys
from datetime import datetime

USERNAME  = "manushukla2"
OUT_FILE  = "contribution-graph.svg"
TOKEN     = os.environ.get("GITHUB_TOKEN", "")

# GitHub greens (same as the HTML page)
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
LEVEL_MAP = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}

QUERY = """
{
  user(login: "%s") {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
""" % USERNAME


# ── Fetch ──────────────────────────────────────────────────────────────────────
def fetch_data():
    if not TOKEN:
        print("❌  Set GITHUB_TOKEN env variable.")
        sys.exit(1)

    r = requests.post(
        "https://api.github.com/graphql",
        headers={"Authorization": f"bearer {TOKEN}"},
        json={"query": QUERY},
        timeout=15,
    )
    r.raise_for_status()
    j = r.json()
    if "errors" in j:
        print("GitHub API error:", j["errors"])
        sys.exit(1)

    cal   = j["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days  = [d for w in cal["weeks"] for d in w["contributionDays"]]
    total = cal["totalContributions"]

    counts = [d["contributionCount"] for d in days]
    levels = [LEVEL_MAP.get(d["contributionLevel"], 0) for d in days]
    dates  = [d["date"] for d in days]
    return counts, levels, dates, total


# ── SVG builder ────────────────────────────────────────────────────────────────
def build_svg(counts, levels, dates, total):
    COLS  = math.ceil(len(counts) / 7)
    CELL  = 11          # px per cell
    GAP   = 3           # gap between cells
    PAD_X = 4
    PAD_Y = 32          # space for top label

    W = PAD_X * 2 + COLS  * (CELL + GAP) - GAP
    H = PAD_Y     + 7     * (CELL + GAP) - GAP + 20

    # --- build <rect> elements with CSS animation delays ---
    rects = []
    for c in range(COLS):
        for r in range(7):
            i = c * 7 + r
            if i >= len(counts):
                continue
            lv    = levels[i]
            color = COLORS[lv]
            x     = PAD_X + c * (CELL + GAP)
            y     = PAD_Y + r * (CELL + GAP)
            delay = (c + r * 1.6) * 18          # diagonal wave (ms)
            date  = dates[i]
            cnt   = counts[i]

            rects.append(
                f'  <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" ry="2"'
                f' fill="{color}"'
                f' style="animation-delay:{delay:.0f}ms"'
                f' class="cell lv{lv}">'
                f'<title>{date}: {cnt} contribution{"s" if cnt!=1 else ""}</title>'
                f'</rect>'
            )

    rects_svg = "\n".join(rects)

    # best day label
    best_i     = counts.index(max(counts)) if counts else 0
    best_col   = best_i // 7
    best_row   = best_i  % 7
    best_x     = PAD_X + best_col * (CELL + GAP) + CELL // 2
    best_y     = PAD_Y + best_row * (CELL + GAP)
    best_label = f"{counts[best_i]} · {dates[best_i]}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="{W}" height="{H}"
     viewBox="0 0 {W} {H}"
     role="img"
     aria-label="{total} GitHub contributions by {USERNAME}">

  <title>{USERNAME} · {total} contributions</title>

  <style>
    /* ── base ── */
    svg {{ background: #0d1117; border-radius: 8px; }}
    text {{ font-family: -apple-system, 'Segoe UI', sans-serif; fill: #e6edf3; }}
    .label {{ font-size: 12px; font-weight: 600; }}
    .sub   {{ font-size: 10px; fill: #7d8590; }}
    .best  {{ font-size: 9px;  fill: #39d353; font-family: monospace; }}

    /* ── cell entrance animation ── */
    @keyframes drop-in {{
      0%   {{ transform: scaleY(0.1); opacity: 0; transform-origin: bottom; }}
      70%  {{ transform: scaleY(1.1); opacity: 1; }}
      100% {{ transform: scaleY(1);   opacity: 1; }}
    }}
    .cell {{
      opacity: 0;
      animation: drop-in 0.4s ease forwards;
    }}

    /* ── level glow on hover ── */
    .lv1:hover, .lv2:hover, .lv3:hover, .lv4:hover {{
      filter: brightness(1.5);
      cursor: pointer;
    }}
  </style>

  <!-- total label -->
  <text x="{PAD_X}" y="20" class="label">{total:,}</text>
  <text x="{PAD_X + len(str(total)) * 7 + 6}" y="20" class="sub">contributions in the last year</text>

  <!-- contribution cells -->
{rects_svg}

  <!-- best-day leader -->
  <line x1="{best_x}" y1="{best_y - 4}" x2="{best_x}" y2="{best_y - 14}"
        stroke="#39d353" stroke-width="1" stroke-dasharray="2,2"
        style="animation:drop-in 0.3s ease {((best_col + best_row*1.6)*18 + 500):.0f}ms forwards; opacity:0"/>
  <text x="{best_x}" y="{best_y - 16}" text-anchor="middle" class="best"
        style="animation:drop-in 0.3s ease {((best_col + best_row*1.6)*18 + 500):.0f}ms forwards; opacity:0">
    {best_label}
  </text>

</svg>"""

    return svg


# ── main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Fetching contributions for {USERNAME}…")
    counts, levels, dates, total = fetch_data()
    print(f"✓  {total} contributions across {len(counts)} days")

    svg = build_svg(counts, levels, dates, total)
    with open(OUT_FILE, "w") as f:
        f.write(svg)
    print(f"✓  SVG written → {OUT_FILE}  ({len(svg):,} bytes)")
