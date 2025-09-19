# Sefaria Text URL Sitemap

This document provides a comprehensive overview of Sefaria's URL structure for accessing classic Jewish texts.

## Base URL
- Main site: `https://www.sefaria.org`
- API base: `https://www.sefaria.org/api`

## Bible (Tanakh) URLs

### Torah
- Genesis: `/Genesis` or `/Bereshit`
- Exodus: `/Exodus` or `/Shemot`
- Leviticus: `/Leviticus` or `/Vayikra`
- Numbers: `/Numbers` or `/Bamidbar`
- Deuteronomy: `/Deuteronomy` or `/Devarim`

### Prophets (Nevi'im)
- Early Prophets:
  - Joshua: `/Joshua`
  - Judges: `/Judges`
  - Samuel I: `/I_Samuel`
  - Samuel II: `/II_Samuel`
  - Kings I: `/I_Kings`
  - Kings II: `/II_Kings`

- Later Prophets:
  - Isaiah: `/Isaiah`
  - Jeremiah: `/Jeremiah`
  - Ezekiel: `/Ezekiel`
  - Minor Prophets: `/Twelve_Prophets`

### Writings (Ketuvim)
- Psalms: `/Psalms`
- Proverbs: `/Proverbs`
- Job: `/Job`
- Song of Songs: `/Song_of_Songs`
- Ruth: `/Ruth`
- Lamentations: `/Lamentations`
- Ecclesiastes: `/Ecclesiastes`
- Esther: `/Esther`
- Daniel: `/Daniel`
- Ezra: `/Ezra`
- Nehemiah: `/Nehemiah`
- Chronicles I: `/I_Chronicles`
- Chronicles II: `/II_Chronicles`

## Mishnah URLs
Format: `/Mishnah_[Tractate]`

### Orders (Sedarim):
1. Zeraim:
   - `/Mishnah_Berakhot`
   - `/Mishnah_Peah`
   - `/Mishnah_Demai`
   - etc.

2. Moed:
   - `/Mishnah_Shabbat`
   - `/Mishnah_Eruvin`
   - `/Mishnah_Pesachim`
   - etc.

3. Nashim:
   - `/Mishnah_Yevamot`
   - `/Mishnah_Ketubot`
   - `/Mishnah_Nedarim`
   - etc.

4. Nezikin:
   - `/Mishnah_Bava_Kamma`
   - `/Mishnah_Bava_Metzia`
   - `/Mishnah_Bava_Batra`
   - etc.

5. Kodashim:
   - `/Mishnah_Zevachim`
   - `/Mishnah_Menachot`
   - `/Mishnah_Chullin`
   - etc.

6. Tahorot:
   - `/Mishnah_Kelim`
   - `/Mishnah_Oholot`
   - `/Mishnah_Negaim`
   - etc.

## Talmud URLs
Format: `/[Tractate]`

### Babylonian Talmud (Bavli)
- Berakhot: `/Berakhot`
- Shabbat: `/Shabbat`
- Eruvin: `/Eruvin`
- Pesachim: `/Pesachim`
- Yoma: `/Yoma`
- etc.

### Jerusalem Talmud (Yerushalmi)
Format: `/Jerusalem_Talmud_[Tractate]`
- `/Jerusalem_Talmud_Berakhot`
- `/Jerusalem_Talmud_Peah`
- etc.

## Midrash URLs

### Midrash Rabbah
- Genesis Rabbah: `/Bereishit_Rabbah`
- Exodus Rabbah: `/Shemot_Rabbah`
- Leviticus Rabbah: `/Vayikra_Rabbah`
- Numbers Rabbah: `/Bemidbar_Rabbah`
- Deuteronomy Rabbah: `/Devarim_Rabbah`

### Other Major Midrashim
- Midrash Tanchuma: `/Midrash_Tanchuma`
- Sifra: `/Sifra`
- Sifrei Bamidbar: `/Sifrei_Bamidbar`
- Sifrei Devarim: `/Sifrei_Devarim`
- Mechilta d'Rabbi Yishmael: `/Mekhilta_d'Rabbi_Yishmael`

## URL Parameters and Specific References

### Chapter and Verse References
- Specific chapter: `[Base URL]/[Book].[Chapter]`
  - Example: `/Genesis.1` (Genesis Chapter 1)
- Specific verse: `[Base URL]/[Book].[Chapter].[Verse]`
  - Example: `/Genesis.1.1` (Genesis 1:1)
- Range of verses: `[Base URL]/[Book].[Chapter].[StartVerse]-[EndVerse]`
  - Example: `/Genesis.1.1-3` (Genesis 1:1-3)

### Other Parameters
- Language options: Add `?lang=he` for Hebrew, `?lang=en` for English
- Layout options: Add `?layout=heLeft` for Hebrew text on left
- With commentary: Add `?with=Rashi` or other commentary name

### API Endpoints
- Text API: `/api/texts/[Reference]`
  - Example: `/api/texts/Genesis.1.1`
- Index API: `/api/index/[Book]`
  - Example: `/api/index/Genesis`
- Links API: `/api/links/[Reference]`
  - Example: `/api/links/Genesis.1.1`

## Note
All URLs are case-sensitive. Replace spaces with underscores in multi-word references.