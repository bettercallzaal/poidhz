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

describe('singapore story blocks (bounty v19b order and words)', () => {
  const page = readFileSync(join(__dirname, '../app/singapore/page.tsx'), 'utf8');
  it('is plain voice and names no family member', async () => {
    const { PITCH, STORY_BLOCKS, FUN_FACTS, FUN_FACTS_INTRO } = await import('@/app/singapore/intro');
    const all = [PITCH, ...STORY_BLOCKS.map((b) => b.text), FUN_FACTS_INTRO, ...FUN_FACTS].join('\n');
    expect(all).not.toMatch(/[‒-―]| - /);
    expect(FUN_FACTS).toHaveLength(6);
  });
  it('opens with the v19b hook up to "here\'s how I got here", then tells the story in time order, and ends on the ask', async () => {
    const { STORY_BLOCKS } = await import('@/app/singapore/intro');
    expect(STORY_BLOCKS[0].text.startsWith("I've been a Zoroastrian priest since I was 12.")).toBe(true);
    expect(STORY_BLOCKS[1].text).toContain('to help cover my travel');
    expect(STORY_BLOCKS[2].text.startsWith('Back this bounty and send me your questions')).toBe(true);
    expect(STORY_BLOCKS[3].text).toBe("And as always, POIDH (pics or it didn't happen), so here's how I got here.");
    expect(STORY_BLOCKS[4].text.startsWith("I'm Zaal.")).toBe(true);
    expect(STORY_BLOCKS.at(-1)!.text).toContain("I'll keep rocking out");
    const order = ['Before I became a priest, I had my Navjote', "Pluralism Project's page", 'Becoming a priest started years before India', "Here's my Navar", 'Zoroastrian kid at Catholic school', 'That 2016 college essay opened with', 'Congress in New York', 'congress in London', 'house warming jashan in my own home', 'Which brings me to Singapore', 'full subsidy from ZYAB', 'flights are around $2k'];
    const idx = order.map((k) => STORY_BLOCKS.findIndex((b) => b.text.includes(k)));
    for (let i = 1; i < idx.length; i++) expect(idx[i]).toBeGreaterThan(idx[i - 1]);
  });
  it('carries the money facts, item 259 wording, and his 6 Nov answers', async () => {
    const { STORY_BLOCKS } = await import('@/app/singapore/intro');
    const all = STORY_BLOCKS.map((b) => b.text).join(' ');
    for (const k of ['28 to 30 December 2026', 'covers my hotel, registration and meals, but not the flight', 'already bought, and this fundraiser helps pay them back', 'the extra hotel night the day before', 'death penalty', 'my version of art', 'The ZAO', 'first $100 on POIDH myself']) expect(all).toContain(k);
    expect(all).not.toContain('shuffl');
    expect(page).toContain("'Flights already bought; this pays them back'");
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

describe('singapore v15c (items 263 to 265)', () => {
  it('makes no fixed content promise anywhere on the page', () => {
    const dir = join(__dirname, '..', 'app', 'singapore');
    for (const f of readdirSync(dir)) expect(readFileSync(join(dir, f), 'utf8'), f).not.toMatch(/dispatch|livestream|one recap/i);
  });
  it('carries his essay paragraphs, the explained terms, the corrections, and the interview links', async () => {
    const m = await import('@/app/singapore/intro');
    const all = m.STORY_BLOCKS.map((b) => b.text).join(' ');
    for (const k of ['one of the first Zoroastrian priests born and brought up in our Boston community', '24 days at a Zoroastrian temple in Mumbai', 'humata, hukhta, hvarshta', 'daena, also means conscience', 'with my fiance and her family there with us', 'my mom was vice president and later president', 'Iranian Zoroastrians are the ones who stayed', 'as much content as I can from the Congress, fueled by the questions', 'including the Vakhshoori Foundation']) expect(all).toContain(k);
    const letter = m.STORY_BLOCKS.findIndex((b) => b.images?.some((i) => i.src.endsWith('zyab-subsidy-letter.jpg')));
    expect(m.STORY_BLOCKS[letter + 1].text).toBe('The hotel dates should read 27 to 31 December 2026, five nights. ZYAB corrected this after sending.');
    expect(m.INTERVIEW_PARTS.map((p) => p.label)).toEqual(['Part 1', 'Part 2', 'Part 3']);
    for (const p of m.INTERVIEW_PARTS) expect(p.href).toMatch(/^https:\/\/projectinterfaith\.blogspot\.com\/2014\//);
    expect(m.WHAT_YOU_GET).toContain("I'll bring your questions with me to Singapore");
    expect(m.WHAT_YOU_GET).not.toContain('poidhz.com');
  });
});

describe('singapore v15d (item 266)', () => {
  it('the scholarships paragraph sits directly before New York 2022', async () => {
    const { STORY_BLOCKS } = await import('@/app/singapore/intro');
    const i = STORY_BLOCKS.findIndex((b) => b.text.startsWith('My Zoroastrian community backed me in college too.'));
    expect(i).toBeGreaterThan(-1);
    expect(STORY_BLOCKS[i + 1].text.startsWith('Then in 2022 I went to the World Zoroastrian Congress in New York.')).toBe(true);
  });
});

describe('singapore v16 (item 267)', () => {
  it('carries his picks and his own past writing, quoted', async () => {
    const { STORY_BLOCKS, FUN_FACTS } = await import('@/app/singapore/intro');
    const all = [...STORY_BLOCKS.map((b) => b.text), ...FUN_FACTS].join(' ');
    for (const k of ['Priesthood runs in families', 'pocket of merit', 'one for each of the 72 chapters of the Yasna', 'In America the two streams come back together', 'That 2016 college essay opened with', 'needs to be known about more in the US']) expect(all).toContain(k);
    expect(FUN_FACTS.join(' ')).toMatch(/sugar/i);
  });
});

describe('singapore v17g (items 268 to 275)', () => {
  it('matches the v17g wording, puts each photo after its line, and drops the old president wording', async () => {
    const { STORY_BLOCKS } = await import('@/app/singapore/intro');
    const all = STORY_BLOCKS.map((b) => b.text).join(' ');
    expect(all).not.toContain("she's the president now");
    expect(all).not.toContain('In 6th grade I went to India for a month to become a mobed');
    const nav = STORY_BLOCKS.find((b) => b.text.startsWith("Here's my Navar"))!;
    expect(nav.images?.[0].src).toContain('zagba.org/Dec20.JPG');
    const plu = STORY_BLOCKS.find((b) => b.text.includes("Pluralism Project's page"))!;
    expect(plu.link?.href).toBe('https://pluralism.org/zoroastrianism');
    expect(plu.images?.[0].alt).toBe('My Navjote');
    for (const b of STORY_BLOCKS) expect(b.text).not.toMatch(/https?:/);
  });
});

describe('singapore v19b, the cast text (items 279 to 297)', () => {
  it('links the live bounty 1536, seeds 0.045 ETH, and carries his episode quotes and the sources', async () => {
    const links = await import('@/app/singapore/links');
    expect(links.POIDH_BOUNTY_URL).toBe('https://poidh.xyz/base/bounty/1536');
    expect(links.POIDH_BOUNTY_ID).toBe(1536);
    expect(links.POIDH_SEED_ETH).toBe(0.045);
    expect(links.POIDH_LAST_KNOWN).toMatchObject({ eth: 0.045, date: '2026-11-06' });
    const m = await import('@/app/singapore/intro');
    const all = m.STORY_BLOCKS.map((b) => b.text).join(' ');
    for (const k of ['one of the first monotheistic religions [1]', 'I could count on two or three hands', 'Very similar to a crypto event, ironically enough', 'onboarded through a religion', 'We just learned more about each other']) expect(all).toContain(k);
    expect(all).not.toContain('100k to 200k');
    expect(m.INTERVIEW_INTRO).toContain("We don't have a pope or any central figure");
    expect(m.SOURCES.map((s) => s.text.match(/^\[(\d+)\]/)?.[1]).filter(Boolean)).toEqual(['1', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']);
    expect(m.SOURCES.find((s) => s.text.startsWith('[11]'))!.text).toContain('Antia, Kersey H.');
    const cited = new Set([...all.matchAll(/\[(\d+)\]/g)].map((x) => x[1]));
    for (const n of cited) expect(m.SOURCES.some((s) => s.text.startsWith(`[${n}]`)), `[${n}] has a source`).toBe(true);
  });
});
