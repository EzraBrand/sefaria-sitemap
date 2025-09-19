import requests
import re

API_BASE = "https://www.sefaria.org/api/texts"

YERUSHALMI_TRACTATES = [
    "Jerusalem_Talmud_Berakhot",
    "Jerusalem_Talmud_Peah",
    "Jerusalem_Talmud_Demai",
    "Jerusalem_Talmud_Kilayim",
    "Jerusalem_Talmud_Sheviit",
    "Jerusalem_Talmud_Terumot",
    "Jerusalem_Talmud_Maaserot",
    "Jerusalem_Talmud_Maaser_Sheni",
    "Jerusalem_Talmud_Challah",
    "Jerusalem_Talmud_Orlah",
    "Jerusalem_Talmud_Bikkurim",
    # Add more tractates as needed
]

def count_hebrew_words(text):
    hebrew_text = re.sub(r"[^\u0590-\u05FF\s]", "", text)
    words = hebrew_text.split()
    return len(words)

def flatten_text(obj):
    if isinstance(obj, list):
        return " ".join(flatten_text(x) for x in obj)
    elif isinstance(obj, str):
        return obj
    return ""

def get_tractate_hebrew_word_count(tractate):
    url = f"{API_BASE}/{tractate}?lang=he"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        hebrew_text = flatten_text(data.get("he", []))
        return count_hebrew_words(hebrew_text)
    except Exception as e:
        print(f"Error fetching {tractate}: {e}")
        return None

def main():
    print("Yerushalmi Hebrew Word Count per Tractate (Full Text):")
    for tractate in YERUSHALMI_TRACTATES:
        count = get_tractate_hebrew_word_count(tractate)
        if count is not None:
            print(f"{tractate}: {count} words")
        else:
            print(f"{tractate}: Error")

if __name__ == "__main__":
    main()
