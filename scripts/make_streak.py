import json
from datetime import datetime, timedelta

def make_streak(input_file="data/contributions.json", output="streak.svg"):
    with open(input_file) as f:
        data = json.load(f)

    days = sorted(data["days"], key=lambda d: d["date"])
    
    # Calculate current streak
    current_streak = 0
    today = datetime.today().strftime("%Y-%m-%d")
    check = datetime.today()
    
    for _ in range(365):
        date_str = check.strftime("%Y-%m-%d")
        day = next((d for d in days if d["date"] == date_str), None)
        if day and day["level"] > 0:
            current_streak += 1
            check -= timedelta(days=1)
        else:
            break

    # Calculate longest streak
    longest = 0
    temp = 0
    for day in days:
        if day["level"] > 0:
            temp += 1
            longest = max(longest, temp)
        else:
            temp = 0

    total = data["total"]

    svg_w = 860
    svg_h = 120

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" style="background:#0d1117">

  <!-- Current Streak -->
  <rect x="30" y="15" width="250" height="90" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>
  <text x="155" y="45" text-anchor="middle" font-family="Courier New,monospace" font-size="11" fill="#555">Current Streak</text>
  <text x="155" y="80" text-anchor="middle" font-family="Courier New,monospace" font-size="32" fill="#39d353" opacity="0">
    {current_streak} days
    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.2s" fill="freeze"/>
  </text>

  <!-- Longest Streak -->
  <rect x="305" y="15" width="250" height="90" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>
  <text x="430" y="45" text-anchor="middle" font-family="Courier New,monospace" font-size="11" fill="#555">Longest Streak</text>
  <text x="430" y="80" text-anchor="middle" font-family="Courier New,monospace" font-size="32" fill="#58a6ff" opacity="0">
    {longest} days
    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.5s" fill="freeze"/>
  </text>

  <!-- Total Contributions -->
  <rect x="580" y="15" width="250" height="90" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>
  <text x="705" y="45" text-anchor="middle" font-family="Courier New,monospace" font-size="11" fill="#555">Total Contributions</text>
  <text x="705" y="80" text-anchor="middle" font-family="Courier New,monospace" font-size="32" fill="#f0883e" opacity="0">
    {total}
    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.8s" fill="freeze"/>
  </text>

</svg>"""

    with open(output, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Saved: {output} | Streak: {current_streak} | Longest: {longest} | Total: {total}")

if __name__ == "__main__":
    make_streak()
