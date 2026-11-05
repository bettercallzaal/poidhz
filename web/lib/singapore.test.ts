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
  it('is plain voice: no dashes, no pasted reference text, no one named', async () => {
    const { STORY, STORY_HEADING } = await import('@/app/singapore/story');
    const all = [STORY_HEADING, ...STORY].join('\n');
    expect(STORY.length).toBeGreaterThan(0);
    expect(all).not.toMatch(/[\u2013\u2014]| - /);
    expect(all).not.toMatch(/Zoti|Rathwi|Spenta Mainyu|Amesha/);
  });
});
