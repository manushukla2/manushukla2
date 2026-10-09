import requests
from bs4 import BeautifulSoup

url = "https://github.com/users/manushukla2/contributions"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

# Print first cell with data-date
cell = soup.find(attrs={"data-date": True})
print("Tag:", cell.name)
print("Attrs:", cell.attrs)
print("Parent tag:", cell.parent.name)
print("Parent attrs:", cell.parent.attrs)
