# news-image-20261121 — The World in One Picture

Entry for make.fun `news-image-20261121`: sum up Saturday 21 November 2026's
world news in one image.

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
