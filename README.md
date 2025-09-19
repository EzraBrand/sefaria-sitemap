# sefaria-sitemap

This project documents Sefaria endpoints and provides tools for analyzing classic Jewish texts.

## Features

- **SITEMAP.md**: Comprehensive documentation of Sefaria URLs for Bible, Mishnah, Talmud, and Midrash.
- **yerushalmi_word_count_by_ref.py**: Script to count Hebrew words in Jerusalem Talmud (Yerushalmi) tractates by iterating through all valid chapter/halakhah references and summing the word counts. This approach ensures accurate results even when the API does not return the full tractate text in one request.

## Usage

To count Hebrew words in a tractate, run:

```bash
python3 yerushalmi_word_count_by_ref.py
```

You can modify the script to analyze other tractates or texts as needed.