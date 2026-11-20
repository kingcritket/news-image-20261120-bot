# news-image-20261120-bot

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/kingcritket/news-image-20261120-bot/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/kingcritket/news-image-20261120-bot/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world news of Friday 20 November 2026: Trump pushes any decision on renewed strikes against Iran into next year — "we'll see what happens after January 1" — telling reporters aboard Air Force One on his flight home from China, as the Senate rejects a war-powers curb 51–48; Cyclone Akvan makes landfall near Gopalpur on India's east coast, with about 300,000 people evacuated, red alerts issued and 69 trains cancelled; and Sensor Tower's updated estimate puts GTA VI's day-one sales at $2.36 billion on 24.6 million copies — an outside estimate that Take-Two has not confirmed. Also today: European leaders say they are ready for talks with Russia on ending the Ukraine war, a Houthi strike damages Riyadh's tallest tower (the PIF headquarters), Wall Street falls 2.0% for a sixth straight day, COP31 reaches its closing day in Antalya with no final deal yet, and Cyclone Xavier keeps the Cook Islands under gale and storm alerts.

All stories verified against reporting dated 20 November 2026 (Reuters, AP, BBC, IMD, The Hindu, Deadline). This v3 corrects the previous version's faithfulness defects: it removes four items that belonged to earlier days — the ICJ's Myanmar genocide ruling (delivered 19 Nov), Voyager 1's light-day milestone (18 Nov), JAXA's Hayabusa2 announcement (17 Nov) and the Pete Rose pardon (announced 19 Nov) — along with a ticker that repeated 18–19 Nov items, and it replaces the GTA panel's "$1.8 billion" stated as fact with Sensor Tower's 20 Nov updated estimate, labelled (EST.). Three AI-generated scene photos with no text baked in, composited with PIL; every word on the image is drawn by PIL in Liberation Sans, plus a dotted world map. The image is built by `build_entry.py` and shipped as `entry.png`; `main.py` copies it to the output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To rebuild the image from the scene photos:

```sh
python3 build_entry.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=97vd661v&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
