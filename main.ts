// A news-image-20261121 entry (Node 22, standard library only): the image
// is entry.png beside this file, drawn by generate.py from the day's news,
// and this program copies it to /output/entry.png for the gate and judge.
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
if (!existsSync(src)) {
  throw new Error('entry.png is missing from the repository');
}
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);
const bytes = statSync(dest).size;
if (bytes === 0) {
  throw new Error('entry.png copied as an empty file');
}
console.log(`wrote entry.png (${bytes} bytes) to`, outDir);
