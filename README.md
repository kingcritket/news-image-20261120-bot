# news-image-20261120-bot

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/kingcritket/news-image-20261120-bot/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/kingcritket/news-image-20261120-bot/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world news of Friday 20 November 2026: Trump pushes any decision on renewed strikes against Iran to 2027 — "we'll see what happens after January 1" — on his flight home from China, as the Senate rejects a war-powers curb 51–48; Cyclone Akvan makes landfall on India's east coast by noon, with about 300,000 people evacuated; and GTA VI's day-one sales pass $1.8 billion, overtaking The Odyssey's global run. Also today: the ICJ rules Myanmar committed genocide against the Rohingya (9–6, the first state ever held liable for genocide), NASA confirms Voyager 1 has passed a light-day from Earth, Japan's Hayabusa2 scraps its asteroid landing after engine trouble, European leaders say they are ready for talks with Russia on ending the Ukraine war, Houthis damage a Riyadh tower, and Trump posthumously pardons Pete Rose.

All stories verified against reporting from 20 November 2026 (Reuters, BBC, AP, IMD, The Hindu, Space). The Shenzhen trilateral itself happened on 19 November and is deliberately not repeated as today's news — only its follow-up, the Iran-decision delay, is today's story. Three AI-generated scene photos with no text baked in, composited with PIL; every word on the image is drawn by PIL in Liberation Sans Bold, plus a dotted world map. The image is built by `build_entry.py` and shipped as `entry.png`; `main.py` copies it to the output directory.

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
