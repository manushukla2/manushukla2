import json
from datetime import datetime, timedelta

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap(input_file="data/contributions.json", output="contrib-heatmap.svg"):
    with open(input_file) as f:
        data = json.load(f)

    days = {d["date"]: d for d in data["days"]}
    total = data["total"]
    best = data["best_day"]

    today = datetime.today()
    start = today - timedelta(weeks=52, days=today.weekday()+1)

    box = 12
    gap = 3
    step = box + gap
    pad_left = 30
    pad_top = 30
    svg_w = pad_left + 53 * step + 20
    svg_h = pad_top + 7 * step + 60

    cells = []
    col = 0
    d = start
    while d <= today:
        row = d.weekday()
        if row == 0 and d != start:
            col += 1
        date_str = d.strftime("%Y-%m-%d")
        day_data = days.get(date_str, {"level": 0, "count": 0})
        level = min(day_data["level"], 5)
        color = PALETTE[level]
        x = pad_left + col * step
        y = pad_top + row * step
        delay = (col * 0.02 + row * 0.01)
        cells.append(
            f'<rect x="{x}" y="{y}" width="{box}" height="{box}" rx="2" fill="{color}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{delay:.3f}s" fill="freeze"/>'
            f'</rect>'
        )
        d += timedelta(days=1)

    legend_x = pad_left
    legend_y = pad_top + 7 * step + 15
    legend = f'<text x="{legend_x}" y="{legend_y + box}" font-family="Courier New,monospace" font-size="10" fill="#555">Less</text>'
    for i, c in enumerate(PALETTE):
        lx = legend_x + 35 + i * (box + 2)
        legend += f'<rect x="{lx}" y="{legend_y}" width="{box}" height="{box}" rx="2" fill="{c}"/>'
    legend += f'<text x="{legend_x + 35 + len(PALETTE)*(box+2) + 4}" y="{legend_y + box}" font-family="Courier New,monospace" font-size="10" fill="#555">More</text>'

    stats_y = legend_y + 22
    stats_text = f"{total} contributions in the last year | best day: {best['date']} ({best['count']})"
    stats = f'<text x="{pad_left}" y="{stats_y}" font-family="Courier New,monospace" font-size="10" fill="#555">{stats_text}</text>'

    svg_parts = ''.join(cells) + legend + stats
    svg = f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" style="background:#0d1117">\n{svg_parts}\n</svg>'

    with open(output, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Saved: {output}")

if __name__ == "__main__":
    render_heatmap()
