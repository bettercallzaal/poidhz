import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { parseIgnore, isIgnored } from './ignore.mjs';

const pats = parseIgnore(readFileSync(join(__dirname, '..', '..', '.vercelignore'), 'utf8'));

describe('the repo .vercelignore is honoured by the sync', () => {
  it('has patterns to honour', () => expect(pats.length).toBeGreaterThan(10));
  for (const p of ['rounds/r5/winner-announce.md', 'rounds/daily/d01/winner-announce.md', 'rounds/daily/d04/ANNOUNCE.md',
    'rounds/daily/d05/FEEDBACK.md', 'rounds/r3/cast-templates/femmie-dm.md', 'rounds/r6/kenny-note.md', 'docs/owed-credit.md',
    'docs/outreach/anything.md', 'rounds/r6/promo-cast.md']) {
    it(`excludes ${p}`, () => expect(isIgnored(p, pats)).toBe(true));
  }
  for (const p of ['rounds/r5/README.md', 'rounds/r2/judging.html', 'docs/about.html', 'data/claims.json', 'rounds/daily/d04/PICK.md']) {
    it(`keeps ${p}`, () => expect(isIgnored(p, pats)).toBe(false));
  }
});
