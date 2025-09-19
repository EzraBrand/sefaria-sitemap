import requests

API_BASE = "https://www.sefaria.org/api"

TEST_ENDPOINTS = [
    # Bible
    f"{API_BASE}/texts/Genesis.1.1",
    f"{API_BASE}/texts/Exodus.1.1",
    f"{API_BASE}/texts/Psalms.1.1",
    # Mishnah
    f"{API_BASE}/texts/Mishnah_Berakhot.1.1",
    f"{API_BASE}/texts/Mishnah_Peah.1.1",
    # Talmud Bavli
    f"{API_BASE}/texts/Berakhot.2a",
    f"{API_BASE}/texts/Shabbat.2a",
    # Jerusalem Talmud
    f"{API_BASE}/texts/Jerusalem_Talmud_Berakhot.1.1",
    # Midrash
    f"{API_BASE}/texts/Bereishit_Rabbah.1.1",
    f"{API_BASE}/texts/Midrash_Tanchuma.1.1",
    # Index
    f"{API_BASE}/index/Genesis",
    f"{API_BASE}/index/Mishnah_Berakhot",
    # Links
    f"{API_BASE}/links/Genesis.1.1",
    f"{API_BASE}/links/Berakhot.2a",
]

def test_endpoints():
    print("Testing Sefaria API endpoints...")
    for url in TEST_ENDPOINTS:
        try:
            resp = requests.get(url, timeout=10)
            status = resp.status_code
            if status == 200:
                print(f"✅ {url} [OK]")
            else:
                print(f"❌ {url} [Status: {status}]")
        except Exception as e:
            print(f"❌ {url} [Error: {e}]")

if __name__ == "__main__":
    test_endpoints()
