import requests
import re
import time

TRACTATE = "Jerusalem_Talmud_Berakhot"
API_INDEX = f"https://www.sefaria.org/api/index/{TRACTATE}"
API_TEXTS = "https://www.sefaria.org/api/texts"

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

def get_structure():
    resp = requests.get(API_INDEX, timeout=30)
    data = resp.json()
    # Get lengths per depth: [chapters, halakhot, segments]
    lengths = data.get("schema", {}).get("lengths", [0, 0, 0])
    return lengths

def get_ref_word_count(chapter, halakhah):
    ref = f"{TRACTATE}.{chapter}.{halakhah}"
    url = f"{API_TEXTS}/{ref}?lang=he"
    try:
        resp = requests.get(url, timeout=20)
        data = resp.json()
        hebrew_text = flatten_text(data.get("he", []))
        return count_hebrew_words(hebrew_text)
    except Exception as e:
        print(f"Error fetching {ref}: {e}")
        return 0

def main():
    print(f"Counting Hebrew words for {TRACTATE} by reference...")
    chapters, halakhot, _ = get_structure()
    total = 0
    for ch in range(1, chapters+1):
        for ha in range(1, halakhot+1):
            count = get_ref_word_count(ch, ha)
            if count > 0:
                print(f"{TRACTATE}.{ch}.{ha}: {count} words")
            total += count
            time.sleep(0.2)  # Be gentle to API
    print(f"Total Hebrew words in {TRACTATE}: {total}")

if __name__ == "__main__":
    main()
