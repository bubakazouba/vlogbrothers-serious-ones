# Vlogbrothers — The Serious Ones

A curated, searchable archive of the most **substantial video-essays** from [Vlogbrothers](https://www.youtube.com/@vlogbrothers) (John & Hank Green) — the big-ideas videos on politics, health, philosophy, economics, and mortality.

It is built from their most-watched uploads and then **strictly filtered** to keep only serious, thesis-driven content. The jokes, songs, tour vlogs, and giraffe videos are deliberately left out.

## What's inside

- **127 essays** spanning **2008–2026**
- **11 topic categories** (Politics & Society, Media & Culture, Science & Education, Economics & Money, History & Geopolitics, Personal Reflection, Philosophy & Meaning, Health Care, Mortality & Grief, Mental Health, Global Health & TB)
- Live **search** across titles and summaries
- **Filter** by topic and **sort** by newest / oldest / most-viewed / A–Z
- Each card links straight to the video on YouTube

## How it was made

1. Pulled the full channel video list (~2,460 videos) with `yt-dlp`.
2. Took the top ~320 most-viewed as candidates and fetched each video's description + metadata.
3. Applied a strict "big ideas only" classifier to drop comedy/filler and keep substantive essays.
4. Condensed each kept video's own description into a clean 1–2 sentence summary.
5. Rendered a single static `index.html` (no build step, no dependencies).

## Disclaimer

Unofficial fan-made archive. All videos, titles, and thumbnails belong to Vlogbrothers (John & Hank Green). Summaries are condensed from each video's own description. Not affiliated with or endorsed by the Green brothers.
