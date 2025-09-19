import requests
import json

def inspect_structure(tractate):
    url = f"https://www.sefaria.org/api/texts/{tractate}?lang=he"
    resp = requests.get(url, timeout=30)
    data = resp.json()
    he = data.get("he", [])
    print(f"Tractate: {tractate}")
    print(f"Type of 'he': {type(he)}")
    if isinstance(he, list):
        print(f"Top level: {len(he)} chapters")
        total_halakhot = 0
        total_segments = 0
        for i, chapter in enumerate(he):
            if isinstance(chapter, list):
                print(f"  Chapter {i+1}: {len(chapter)} halakhot")
                total_halakhot += len(chapter)
                for j, halakhah in enumerate(chapter):
                    if isinstance(halakhah, list):
                        seg_count = len([seg for seg in halakhah if seg.strip()])
                        total_segments += seg_count
                        print(f"    Halakhah {j+1}: {seg_count} non-empty segments")
                        if seg_count > 0:
                            print(f"      Sample segment: {halakhah[0][:100]}")
        print(f"Total chapters: {len(he)}")
        print(f"Total halakhot: {total_halakhot}")
        print(f"Total non-empty segments: {total_segments}")
    else:
        print("Unexpected structure for 'he' field.")

if __name__ == "__main__":
    inspect_structure("Jerusalem_Talmud_Berakhot")
