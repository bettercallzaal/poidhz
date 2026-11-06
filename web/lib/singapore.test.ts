import { describe, it, expect } from 'vitest';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { RECEIPTS, TRACKER_OPENED, totals, type Receipt } from '@/app/singapore/tracker';

describe('singapore tracker', () => {
  it('starts empty and reads $0, dated the day it opened', () => {
    expect(RECEIPTS).toEqual([]);
    const t = totals([]);
    expect(t.total).toBe(0);
    expect(t.remaining).toBe(1000);
    expect(t.updated).toBe(TRACKER_OPENED);
  });

  it('sums per channel and overall, dated by the newest receipt', () => {
    const rows: Receipt[] = [
      { date: '2026-11-03', channel: 'stripe', net_usd: 24.1, note: '' },
      { date: '2026-11-05', channel: 'paypal', net_usd: 48.3, note: '' },
      { date: '2026-11-04', channel: 'stripe', net_usd: 0.2, note: '' },
    ];
    const t = totals(rows);
    expect(t.byChannel.stripe).toBe(24.3);
    expect(t.byChannel.paypal).toBe(48.3);
    expect(t.byChannel.poidh).toBe(0);
    expect(t.total).toBe(72.6);
    expect(t.remaining).toBe(927.4);
    expect(t.updated).toBe('2026-11-05');
  });
});

describe('owner seed sits on top of the goal (misc item 260)', () => {
  it('a $100 owner seed is shown apart and leaves the full $1,000 for the community', () => {
    const t = totals([{ date: '2026-11-06', channel: 'poidh', net_usd: 100, note: 'owner seed', ownerSeed: true }]);
    expect(t.seed).toBe(100);
    expect(t.total).toBe(0);
    expect(t.byChannel.poidh).toBe(0);
    expect(t.remaining).toBe(1000);
    expect(t.updated).toBe('2026-11-06');
  });
  it('the START table adds up to the trip: 900 + 200 + 100 + 1,000 = 2,200, with no $900 community row', () => {
    const page = readFileSync(join(__dirname, '../app/singapore/page.tsx'), 'utf8');
    const rows = [...page.matchAll(/\['([^']+)', '\$([\d,]+)', '[^']*'\]/g)].map((m) => [m[1], Number(m[2].replace(',', ''))] as const);
    const trip = rows.find(([k]) => k === 'Estimated travel cost')![1];
    const parts = rows.filter(([k]) => k !== 'Estimated travel cost').reduce((a, [, v]) => a + v, 0);
    expect(trip).toBe(2200);
    expect(parts).toBe(2200);
    expect(page).not.toContain('Community support, part of the goal');
  });
});

describe('singapore page', () => {
  const src = readFileSync(join(__dirname, '..', 'app', 'singapore', 'page.tsx'), 'utf8');
  it('renders a button only for a non-empty link and carries no placeholder text', () => {
    expect(src).toContain('.filter((b) => b.href)');
    expect(src).toContain('QUESTION_URL &&');
    expect(src).toContain('zaal.eth');
    expect(src).toContain('href={STRIPE_REQUEST_URL}');
    expect(src).not.toMatch(/coming soon|TODO|TBD|\[[A-Z ]+\]/i);
  });
});

describe('singapore story', () => {
  it('is plain voice: no dashes', async () => {
    const { STORY, STORY_HEADING } = await import('@/app/singapore/story');
    const all = [STORY_HEADING, ...STORY].join('\n');
    expect(STORY.length).toBeGreaterThan(0);
    expect(all).not.toMatch(/[\u2013\u2014]| - /);
  });
});

describe('singapore story blocks (bounty v12d order and words)', () => {
  const page = readFileSync(join(__dirname, '../app/singapore/page.tsx'), 'utf8');
  it('is plain voice and names no family member', async () => {
    const { PITCH, STORY_BLOCKS, FUN_FACTS, FUN_FACTS_INTRO } = await import('@/app/singapore/intro');
    const all = [PITCH, ...STORY_BLOCKS.map((b) => b.text), FUN_FACTS_INTRO, ...FUN_FACTS].join('\n');
    expect(all).not.toMatch(/[‒-―]| - /);
    expect(FUN_FACTS).toHaveLength(5);
  });
  it('opens with India at 6th grade, then the POIDH proof, and ends on the ask', async () => {
    const { STORY_BLOCKS } = await import('@/app/singapore/intro');
    expect(STORY_BLOCKS[0].text.startsWith('In 6th grade I went to India for a month to become a mobed')).toBe(true);
    expect(STORY_BLOCKS[1].text).toContain('POIDH (pics or it didn\'t happen)');
    expect(STORY_BLOCKS.at(-1)!.text).toContain("I'll keep rocking out");
    const order = ['Catholic school', 'New York', 'London', 'house warming', 'Singapore as a youth delegate', 'full subsidy', 'flights are around $2k'];
    const idx = order.map((k) => STORY_BLOCKS.findIndex((b) => b.text.includes(k)));
    for (let i = 1; i < idx.length; i++) expect(idx[i]).toBeGreaterThan(idx[i - 1]);
  });
  it('carries the money facts, item 259 wording, and his 6 Nov answers', async () => {
    const { STORY_BLOCKS } = await import('@/app/singapore/intro');
    const all = STORY_BLOCKS.map((b) => b.text).join(' ');
    for (const k of ['28 to 30 December 2026', 'covers my hotel, registration and meals, but not the flight', 'already bought, and this fundraiser helps pay them back', 'the extra hotel night the day before', 'death penalty', 'my version of art', 'The ZAO', 'first $100 on POIDH myself']) expect(all).toContain(k);
    expect(all).not.toContain('shuffl');
    expect(page).toContain("'Flights already bought; this pays them back'");
    expect(page).toContain('I&apos;ll focus on the ones I can share about');
  });
  it('photos: two archive images, three house warming photos and the subsidy letter, all present', async () => {
    const { STORY_BLOCKS } = await import('@/app/singapore/intro');
    const imgs = STORY_BLOCKS.flatMap((b) => b.images ?? []);
    expect(imgs.filter((i) => i.src.startsWith('https://web.archive.org/'))).toHaveLength(2);
    const local = imgs.filter((i) => i.src.startsWith('/assets/singapore/'));
    expect(local.map((i) => i.src).sort()).toEqual(['/assets/singapore/housewarming-1.jpg', '/assets/singapore/housewarming-2.jpg', '/assets/singapore/housewarming-3.jpg', '/assets/singapore/zyab-subsidy-letter.jpg']);
    for (const i of local) expect(readFileSync(join(__dirname, '../..', i.src)).length).toBeGreaterThan(100000);
  });
  it('How to back sits under Raised so far, before Where the trip stands, with the POIDH placeholder', () => {
    const raised = page.indexOf('>Raised so far<'), back = page.indexOf('>How to back<'), trip = page.indexOf('>Where the trip stands<');
    expect(raised).toBeGreaterThan(page.indexOf('{STORY_BLOCKS.map'));
    expect(raised).toBeLessThan(back);
    expect(back).toBeLessThan(trip);
    expect(page).toContain('{!POIDH_BOUNTY_URL && <p className="mt-3 max-w-2xl">The POIDH bounty link goes here when it is live.</p>}');
  });
  it('the story section keeps only what the main story does not tell', async () => {
    const { STORY } = await import('@/app/singapore/story');
    expect(STORY).toHaveLength(3);
  });
});

// Family-names guard (misc item 261). The names live only in a gitignored local file, one per line,
// so this public repo never lists them. Without the file the check is skipped, and says so loudly.
const NAMES_FILE = join(__dirname, '..', '.private-names.txt');
const privateNames = existsSync(NAMES_FILE)
  ? readFileSync(NAMES_FILE, 'utf8').split('\n').map((l) => l.trim()).filter(Boolean)
  : [];
if (privateNames.length === 0) console.warn(`SKIPPED family-names guard: ${NAMES_FILE} is absent or empty, so /singapore was NOT checked for family names.`);

describe.skipIf(privateNames.length === 0)('singapore names no family member (private list)', () => {
  it('no name from the private list appears in any /singapore source file', () => {
    const dir = join(__dirname, '..', 'app', 'singapore');
    for (const f of readdirSync(dir)) {
      const text = readFileSync(join(dir, f), 'utf8');
      for (const n of privateNames) expect(text.includes(n), `${f} contains a private name`).toBe(false);
    }
  });
  it('the private list is not tracked by git', () => {
    expect(readFileSync(join(__dirname, '..', '.gitignore'), 'utf8')).toContain('/.private-names.txt');
  });
});
