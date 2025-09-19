import requests
import re

API_BASE = "https://www.sefaria.org/api"

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

def get_all_refs(tractate):
    url = f"{API_BASE}/index/{tractate}"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        # Get all section references (e.g., chapters)
        refs = []
        for node in data.get("contents", []):
            if "sectionNames" in data:
                # For tractates with chapters
                for i in range(1, node.get("length", 0) + 1):
                    refs.append(f"{tractate}.{i}")
            else:
                # For tractates without chapters
                refs.append(tractate)
        return refs
    except Exception as e:
        print(f"Error fetching index for {tractate}: {e}")
        return []

def get_section_hebrew_word_count(ref):
    url = f"{API_BASE}/texts/{ref}?lang=he"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        def flatten_text(obj):
            if isinstance(obj, list):
                return " ".join(flatten_text(x) for x in obj)
            elif isinstance(obj, str):
                return obj
            return ""
        hebrew_text = flatten_text(data.get("he", []))
        return count_hebrew_words(hebrew_text)
    except Exception as e:
        print(f"Error fetching {ref}: {e}")
        return 0

def main():
    print("Yerushalmi Hebrew Word Count per Tractate (Full Text):")
    for tractate in YERUSHALMI_TRACTATES:
        refs = get_all_refs(tractate)
        total = 0
        for ref in refs:
            total += get_section_hebrew_word_count(ref)
        print(f"{tractate}: {total} words")

if __name__ == "__main__":
    main()
