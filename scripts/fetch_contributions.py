import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def fetch_contributions(username="manushukla2", output="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    days = []
    for cell in soup.find_all(attrs={"data-date": True}):
        date = cell["data-date"]
        level = int(cell.get("data-level", 0))
        days.append({"date": date, "level": level, "count": level})

    total = sum(d["level"] for d in days)
    best = max(days, key=lambda d: d["level"]) if days else {"date": "N/A", "count": 0}

    result = {
        "username": username,
        "generated": datetime.utcnow().isoformat(),
        "total": total,
        "best_day": best,
        "days": days
    }

    with open(output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Fetched {len(days)} days | Total levels: {total}")

if __name__ == "__main__":
    fetch_contributions()
