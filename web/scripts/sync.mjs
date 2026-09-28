// Copies the static pipeline's output into the app. The Python crons stay the writers.
import { cpSync, existsSync, mkdirSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const web = join(dirname(fileURLToPath(import.meta.url)), '..');
const root = join(web, '..');
const pub = join(web, 'public');

const dirs = ['data', 'feedback', 'docs', 'assets', 'rounds'];
const files = ['submit.html', 'gallery.html', 'calendar.html'];

for (const d of dirs) {
  const src = join(root, d);
  if (!existsSync(src)) throw new Error(`sync: missing ${src}`);
  rmSync(join(pub, d), { recursive: true, force: true });
  cpSync(src, join(pub, d), { recursive: true, filter: (p) => !p.includes('__pycache__') && !p.endsWith('.py') });
}
for (const f of files) cpSync(join(root, f), join(pub, f));
mkdirSync(join(web, 'legacy-api'), { recursive: true });
for (const f of ['receipt.mjs', 'claim-meta.mjs']) cpSync(join(root, 'api', f), join(web, 'legacy-api', f));
console.log('sync: ok');
