import requests
import re
import time
import csv
import argparse
import subprocess
from datetime import datetime
import os

TRACTATES = [
    "Jerusalem_Talmud_Berakhot",
    "Jerusalem_Talmud_Peah",
    "Jerusalem_Talmud_Sanhedrin",
]
SCHEMA_FILE = "yerushalmi_schema.json"
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

def get_structure(tractate):
    url = f"https://www.sefaria.org/api/index/{tractate}"
    resp = requests.get(url, timeout=30)
    data = resp.json()
    # Get lengths per depth: [chapters, halakhot, segments]
    lengths = data.get("schema", {}).get("lengths", [0, 0, 0])
    return lengths

def get_ref_word_count(tractate, chapter, halakhah):
    ref = f"{tractate}.{chapter}.{halakhah}"
    url = f"{API_TEXTS}/{ref}?lang=he"
    try:
        resp = requests.get(url, timeout=20)
        data = resp.json()
        hebrew_text = flatten_text(data.get("he", []))
        return ref, count_hebrew_words(hebrew_text)
    except Exception as e:
        return ref, 0

SLEEP_SECONDS = 0.01


def main():
    parser = argparse.ArgumentParser(description="Count Hebrew words in Yerushalmi by reference and write CSV")
    parser.add_argument("--sleep", type=float, default=SLEEP_SECONDS, help="Seconds to sleep between requests")
    parser.add_argument("--output", type=str, default="yerushalmi_word_counts.csv", help="CSV output path")
    parser.add_argument("--auto-commit", action="store_true", help="If set, git add/commit/push the output CSV after a successful run")
    args = parser.parse_args()

    sleep_seconds = args.sleep
    csv_file = args.output

    # Ensure output dir exists
    try:
        out_dir = os.path.dirname(csv_file)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
    except Exception:
        pass

    # Overwrite any existing file
    try:
        if os.path.exists(csv_file):
            os.remove(csv_file)
    except Exception:
        pass

    with open(csv_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["tractate", "chapter", "halakhah", "words"])

        # Try loading schema file so we can iterate exactly
        try:
            import json
            with open(SCHEMA_FILE, 'r', encoding='utf-8') as fh:
                schema = json.load(fh)
            tractates = list(schema.keys())
            print(f"Loaded {len(tractates)} tractates from {SCHEMA_FILE}")
        except Exception:
            schema = {}
            tractates = TRACTATES

        for tractate in tractates:
            print(f"\nCounting Hebrew words for {tractate} by reference (sequential)...")
            tractate_schema = schema.get(tractate)
            total = 0

            if tractate_schema:
                halakhot_list = tractate_schema.get('halakhot_per_chapter', [])
                chapters = len(halakhot_list)
                for ch_index, ha_count in enumerate(halakhot_list, start=1):
                    chapter_rows = []
                    chapter_total = 0
                    for ha in range(1, ha_count+1):
                        ref, count = get_ref_word_count(tractate, ch_index, ha)
                        parts = ref.split('.')
                        if len(parts) >= 3:
                            tname = '.'.join(parts[:-2])
                            chn = parts[-2]
                            han = parts[-1]
                        else:
                            tname = parts[0]
                            chn = ''
                            han = ''
                        if count > 0:
                            print(f"{ref}: {count} words")
                            chapter_rows.append([tname, chn, han, count])
                            chapter_total += count
                        total += count
                        time.sleep(sleep_seconds)
                    if chapter_total > 0:
                        for row in chapter_rows:
                            writer.writerow(row)
                    else:
                        print(f"Skipping chapter {ch_index} for {tractate} (0 words)")
            else:
                # fallback to old behavior (index-based probing with cap)
                chapters, halakhot, _ = get_structure(tractate)
                chapters = min(chapters, 30)
                for ch in range(1, chapters+1):
                    chapter_rows = []
                    chapter_total = 0
                    for ha in range(1, halakhot+1):
                        ref, count = get_ref_word_count(tractate, ch, ha)
                        parts = ref.split('.')
                        if len(parts) >= 3:
                            tname = '.'.join(parts[:-2])
                            chn = parts[-2]
                            han = parts[-1]
                        else:
                            tname = parts[0]
                            chn = ''
                            han = ''
                        if count > 0:
                            print(f"{ref}: {count} words")
                            chapter_rows.append([tname, chn, han, count])
                            chapter_total += count
                        total += count
                        time.sleep(sleep_seconds)
                    if chapter_total > 0:
                        for row in chapter_rows:
                            writer.writerow(row)
                    else:
                        print(f"Skipping chapter {ch} for {tractate} (0 words)")

            print(f"Total Hebrew words in {tractate}: {total}")
            # write a per-tractate summary row (tractate, total_words)
            writer.writerow([tractate, "", "", total])
    print(f"CSV written to {csv_file}")

if __name__ == "__main__":
    main()
