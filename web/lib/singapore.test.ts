import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
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

describe('owner seed counts toward the goal (grill item 124)', () => {
  it('a $100 owner seed row leaves $900 for the community', () => {
    const t = totals([{ date: '2026-11-03', channel: 'poidh', net_usd: 100, note: 'owner seed' }]);
    expect(t.total).toBe(100);
    expect(t.remaining).toBe(900);
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

describe('singapore intro and POIDH moment', () => {
  it('is plain voice, names no one, and uses https archive images', async () => {
    const { INTRO, MOMENT, PITCH } = await import('@/app/singapore/intro');
    const all = [PITCH, ...INTRO, ...MOMENT.map((m) => m.text)].join('\n');
    expect(all).not.toMatch(/[\u2013\u2014]| - /);
    expect(all).not.toMatch(/Farhad|Firoza|Sanaya|Keki|Norwood/);
    const images = MOMENT.flatMap((m) => (m.image ? [m.image.src] : []));
    expect(images).toHaveLength(2);
    for (const src of images) expect(src).toMatch(/^https:\/\/web\.archive\.org\//);
    expect(all).toContain('$200 is for hotel and public transport');
  });
});

describe('singapore culture-first order', () => {
  it('opens with his culture, then the trip', async () => {
    const { INTRO, MOMENT } = await import('@/app/singapore/intro');
    expect(MOMENT[0].text.startsWith("I'm gonna tell you a bit about my culture.")).toBe(true);
    expect(MOMENT[0].text).toContain('a mobed, a Zoroastrian priest, since 6th grade');
    expect(INTRO[0].startsWith("So now I'm going to the 13th World Zoroastrian Congress")).toBe(true);
    expect(INTRO.join(' ')).not.toContain('since 6th grade');
    const page = (await import('node:fs')).readFileSync('app/singapore/page.tsx', 'utf8');
    expect(page.indexOf('{MOMENT.map')).toBeLessThan(page.indexOf('{INTRO.map'));
  });
});

describe('singapore Catholic school section', () => {
  it('renders only once filled from his words', async () => {
    const m = await import('@/app/singapore/school');
    expect(m.SCHOOL_PENDING).toBe(false);
    expect(m.SCHOOL_HEADING).toBe('My time in Catholic school');
    expect(m.SCHOOL.join(' ')).toContain('K to 12');
    expect((await import('@/app/singapore/intro')).MOMENT.map((b) => b.text).join(' ')).toContain('a house warming for my own home');
    expect(m.schoolReady()).toBe(true);
    expect(m.schoolReady('h', ['p'], true)).toBe(false);
    expect(m.schoolReady('h', ['p'], false)).toBe(true);
  });
  it('once filled, has no dashes and names no family member', async () => {
    const m = await import('@/app/singapore/school');
    const text = [m.SCHOOL_HEADING ?? '', ...m.SCHOOL].join(' ');
    expect(text).not.toMatch(/[‒-―]| - /);
    expect(text).not.toMatch(/Farhad|Firoza|Sanaya|Keki|Norwood/);
  });
});

describe('singapore Iman review fixes (item 259)', () => {
  const page = readFileSync(join(__dirname, '../app/singapore/page.tsx'), 'utf8');
  it('intro has the dates and the flights-already-bought wording', async () => {
    const { INTRO } = await import('@/app/singapore/intro');
    expect(INTRO[0]).toContain('as a youth delegate, 28 to 30 December 2026.');
    expect(INTRO[0]).toContain('covers my hotel, registration and meals, but not the flight');
    expect(INTRO[0]).toContain('The flights are around $2k and are already bought, and this fundraiser helps pay them back.');
    expect(page).toContain("'Flights already bought; this pays them back'");
  });
  it('How to back sits directly under Raised so far, before Where the trip stands', () => {
    const raised = page.indexOf('>Raised so far<'), back = page.indexOf('>How to back<'), trip = page.indexOf('>Where the trip stands<');
    expect(raised).toBeGreaterThan(-1);
    expect(raised).toBeLessThan(back);
    expect(back).toBeLessThan(trip);
  });
  it('shows a placeholder line only while the POIDH link is empty', () => {
    expect(page).toContain('{!POIDH_BOUNTY_URL && <p className="mt-3 max-w-2xl">The POIDH bounty link goes here when it is live.</p>}');
  });
});

describe('singapore story-gap answers (6 Nov)', () => {
  it('carries his answers 2, 3, 4, 5, 6 and 8, with no dashes', async () => {
    const { INTRO } = await import('@/app/singapore/intro');
    const { STORY } = await import('@/app/singapore/story');
    const page = readFileSync(join(__dirname, '../app/singapore/page.tsx'), 'utf8');
    const all = [...INTRO, ...STORY].join(' ');
    for (const k of ['the next World Congress from the last one I went to', 'language, snacks, customs and more', 'a community based on learning more about my culture and faith', 'support in my business from these communities']) expect(all).toContain(k);
    expect(page).toContain('It&apos;s not a something for something.');
    expect(all).not.toMatch(/[\u2012-\u2015]| - /);
  });
});

describe('singapore house warming photos (his pick, all 3)', () => {
  it('ships three local photos with alt text and no names', async () => {
    const { HOUSEWARMING_PHOTOS, MOMENT } = await import('@/app/singapore/intro');
    expect(HOUSEWARMING_PHOTOS).toHaveLength(3);
    for (const p of HOUSEWARMING_PHOTOS) {
      expect(p.src).toMatch(/^\/assets\/singapore\/housewarming-[123]\.jpg$/);
      expect(readFileSync(join(__dirname, '../..', p.src)).length).toBeGreaterThan(100000);
      expect(p.alt).not.toMatch(/Farhad|Firoza|Sanaya|Keki|Norwood|Lauren|Peggy|Denis/);
    }
    expect(MOMENT.some((b) => b.images === HOUSEWARMING_PHOTOS)).toBe(true);
  });
});
