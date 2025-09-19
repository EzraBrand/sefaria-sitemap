import requests
import re

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

# Example: Jerusalem Talmud Berakhot, Chapter 1, Halakhah 1
ref = "Jerusalem_Talmud_Berakhot.1.1"
url = f"https://www.sefaria.org/api/texts/{ref}?lang=he"
resp = requests.get(url, timeout=20)
data = resp.json()
hebrew_text = flatten_text(data.get("he", []))
word_count = count_hebrew_words(hebrew_text)

print(f"Reference: {ref}")
print(f"Word count: {word_count}")
print("Sample Hebrew text:")
print(hebrew_text[:500])  # Print first 500 characters for sample
