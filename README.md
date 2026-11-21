[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/top234/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/top234/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# news-image-20261121 — The World in One Picture

Entry for make.fun `news-image-20261121`: sum up Saturday 21 November 2026's
world news in one image. See the bounty at
https://make.fun/bounty/news-image-20261121.

`generate.py` draws `entry.png` (1024x1024, PIL only, deterministic) as a
newspaper front page:

- **Hero:** Russian missiles land in Poland — NATO calls it a grave
  violation, Warsaw seeks reinforcements.
- **Trump calls Europe on Ukraine** — after the summit with Xi and Putin.
- **Markets tumble** — S&P 500 slides into correction as AI shares plunge.
- **Strike hits Kryvyi Rih** — 2 killed, 42 hurt.

`main.ts` (Node 22, stdlib only) copies `entry.png` to `/output/entry.png`.

Run locally:

```
python3 generate.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
