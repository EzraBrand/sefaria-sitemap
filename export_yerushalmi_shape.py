import requests
import time
import json
import re

API_INDEX = "https://www.sefaria.org/api/index"
API_TEXTS = "https://www.sefaria.org/api/texts"
PARENT = "Jerusalem_Talmud"
OUTPUT = "yerushalmi_schema.json"
SLEEP = 0.01


def flatten_text(obj):
    if isinstance(obj, list):
        return " ".join(flatten_text(x) for x in obj)
    if isinstance(obj, str):
        return obj
    return ""


def fetch_json(url, timeout=30):
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def discover_tractates():
    url = f"{API_INDEX}/{PARENT}"
    data = fetch_json(url)
    tractates = []

    # Try common fields where child indexes may appear
    for key in ("nodes", "children", "contents", "subnodes"):
        items = data.get(key)
        if isinstance(items, list) and items:
            for it in items:
                # child entries sometimes include a 'key' like 'Jerusalem_Talmud_Berakhot'
                candidate = None
                if isinstance(it, dict):
                    candidate = it.get("key") or it.get("ref") or it.get("url") or it.get("title")
                elif isinstance(it, str):
                    candidate = it
                if candidate and "Jerusalem_Talmud" in candidate:
                    tractates.append(candidate)
            if tractates:
                return tractates

    # Fallback: examine 'contents' and 'children' for index keys or titles
    for k in ("contents", "nodes", "children", "subnodes", "indexes"):
        for it in data.get(k, []):
            if isinstance(it, dict):
                # prefer explicit index 'key'
                key = it.get('key') or it.get('indexTitle') or it.get('ref')
                title = it.get('title') or it.get('heTitle') or it.get('name')
                if key and 'Jerusalem_Talmud' in str(key):
                    tractates.append(key)
                elif title and 'Yerushalmi' in title:
                    # try to construct a likely key
                    slug = re.sub(r"[^0-9A-Za-z_]+", "_", title.replace(' ', '_'))
                    slug = slug.strip('_')
                    tractates.append(f"Jerusalem_Talmud_{slug}")
    # As a last resort: try a hardcoded common list of tractate suffixes
    if not tractates:
        common = [
            'Berakhot','Peah','Sanhedrin','Sheviit','Moed_Katan','Horayot','Kiddushin',
            'Bikkurim','Demai','Kilayim','Terumot','Maaser','Maaser_Sheni'
        ]
        for s in common:
            tractates.append(f"Jerusalem_Talmud_{s}")

    return list(dict.fromkeys(tractates))


def get_chapter_halakhot(tractate):
    # get basic structure lengths
    idx = fetch_json(f"{API_INDEX}/{tractate}")
    lengths = idx.get("schema", {}).get("lengths", [])
    chapters = lengths[0] if len(lengths) > 0 else None
    max_halakhot = lengths[1] if len(lengths) > 1 else None

    # If chapters is not present, try to detect by probing
    if not chapters:
        # conservative upper bound
        chapters = 50

    halakhot_per_chapter = []
    for ch in range(1, chapters + 1):
        ha_count = 0
        # if we have a max_halakhot, use it as upper bound; otherwise use 200
        upper = max_halakhot or 200
        for ha in range(1, upper + 1):
            ref = f"{tractate}.{ch}.{ha}"
            try:
                data = fetch_json(f"{API_TEXTS}/{ref}?lang=he", timeout=10)
                text = flatten_text(data.get("he", []))
                if text and text.strip():
                    ha_count += 1
                else:
                    # assume no more halakhot in this chapter once we hit a missing/empty
                    break
            except requests.HTTPError as e:
                # 404 or other -> stop checking further halakhot for this chapter
                break
            except Exception:
                break
            time.sleep(SLEEP)
        # if ha_count == 0 and we used a guessed chapters cap, it might mean chapter doesn't exist
        halakhot_per_chapter.append(ha_count)
    # Trim trailing zero chapters (if we guessed too many)
    while halakhot_per_chapter and halakhot_per_chapter[-1] == 0:
        halakhot_per_chapter.pop()
    return halakhot_per_chapter


def main():
    print("Discovering Yerushalmi tractates from Sefaria index...")
    tractates = discover_tractates()
    if not tractates:
        print("No tractates discovered. Exiting.")
        return
    print(f"Found {len(tractates)} tractates: {tractates}")

    schema = {}
    for t in tractates:
        print(f"Processing {t}...")
        try:
            halakhot = get_chapter_halakhot(t)
            schema[t] = {
                "chapters": len(halakhot),
                "halakhot_per_chapter": halakhot,
            }
            print(f"  chapters: {len(halakhot)}; sample: {halakhot[:3]}")
        except Exception as e:
            print(f"  failed to process {t}: {e}")

    with open(OUTPUT, "w", encoding="utf-8") as fh:
        json.dump(schema, fh, ensure_ascii=False, indent=2)
    print(f"Saved Yerushalmi schema to {OUTPUT}")


if __name__ == '__main__':
    main()
