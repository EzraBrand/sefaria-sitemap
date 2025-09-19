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

## New: CLI flags and schema workflow

- `--sleep SLEEP` : seconds to sleep between requests (default small polite delay). Use a small value for faster runs, but avoid hitting API rate limits.
- `--output OUTPUT` : path to write the CSV output (default `yerushalmi_word_counts.csv`).
- `--auto-commit` : if present, the script will `git add`/`commit`/`push` the CSV after a successful run (use with care).

The project includes an exporter `export_yerushalmi_shape.py` which probes Sefaria to discover tractates, chapter counts and per-chapter halakhah counts and writes `yerushalmi_schema.json`.

Workflow summary:

1. Generate or update the schema (recommended before a full run):

```bash
python3 export_yerushalmi_shape.py
```

This script uses a conservative cap (MAX_CHAPTERS=25, MAX_HALAKHOT=20) and will probe each tractate, trimming trailing empty chapters.

2. Run the word-count using the schema (default file `yerushalmi_schema.json` is used):

```bash
python3 yerushalmi_word_count_by_ref.py --sleep 0.01 --output yerushalmi_word_counts.csv
```

Optional: To avoid noisy commits, prefer running without `--auto-commit` and inspect the CSV before committing.

If you'd like a custom schema file or to analyze a subset of tractates, ask and I can add `--schema` / `--tractates` flags to the word-count script.