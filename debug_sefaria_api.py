import requests

tractate = "Jerusalem_Talmud_Berakhot"
API_BASE = "https://www.sefaria.org/api"

# Fetch index to inspect structure
index_url = f"{API_BASE}/index/{tractate}"
resp = requests.get(index_url)
print(f"Index for {tractate}:")
print(resp.json())

# Fetch main text object
text_url = f"{API_BASE}/texts/{tractate}?lang=he"
resp2 = requests.get(text_url)
print(f"Text for {tractate}:")
print(resp2.json())
