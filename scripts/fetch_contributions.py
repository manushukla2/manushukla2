import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def fetch_contributions(username="manushukla2", output="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    days = []
    for td in soup.find_all(["td", "tool-tip"], attrs={"data-date": True}):
        date = td["data-date"]
        level = int(td.get("data-level", 0))
        label = td.get("aria-label", "") or td.get("title", "")
        count = 0
        for part in label.replace(",", "").split():
            if part.isdigit():
                count = int(part)
                break
        days.append({"date": date, "level": level, "count": count})

    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"]) if days else {"date": "N/A", "count": 0}

    result = {
        "username": username,
        "generated": datetime.utcnow().isoformat(),
        "total": total,
        "best_day": best,
        "days": days
    }

    with open(output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Fetched {len(days)} days | Total: {total} contributions")

if __name__ == "__main__":
    fetch_contributions()
