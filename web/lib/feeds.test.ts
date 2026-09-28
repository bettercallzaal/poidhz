import { describe, it, expect } from 'vitest';
import fx from '../test/fixtures/rounds-live.json';
import { roundsFeed, llmsTxt } from './feeds';
import type { Round } from './types';

const now = new Date('2026-09-28T15:37:00Z');
const feed = roundsFeed(fx.rounds as Round[], now, 'https://poidhz.com', 'zao');

describe('roundsFeed', () => {
  it('open holds only rounds taking entries', () => expect(feed.open.map((r) => r.bounty_id)).toEqual([1421]));
  it('recent holds the rest, newest first, no drafts', () => expect(feed.recent.map((r) => r.bounty_id)).toEqual([1418, 1412, 1249]));
  it('unknown claim count stays null in JSON', () => expect(feed.open[0].claims).toBeNull());
  it('links point at poidh and the board', () => {
    expect(feed.open[0].url).toBe('https://poidh.xyz/base/bounty/1421');
    expect(feed.open[0].board_url).toBe('https://poidhz.com/b/1421');
  });
});

describe('llmsTxt', () => {
  const t = llmsTxt(feed, 'https://poidhz.com');
  it('names the live domain and never the old one', () => { expect(t).toContain('https://poidhz.com/rounds.json'); expect(t).not.toContain('zpoidh.vercel.app'); });
  it('lists the open round with its close', () => expect(t).toContain('2026-10-05T17:00:00-04:00'));
  it('prints UNKNOWN for an unknown count', () => expect(t).toContain('entries so far: UNKNOWN'));
});

describe('llmsTxt with an unknown pot', () => {
  it('prints UNKNOWN, not $UNKNOWN', () => {
    const f = roundsFeed([{ round: 'x', bounty_id: 5, status: 'OPEN', amount_usd: null }], now, 'https://poidhz.com', 'zao');
    const t = llmsTxt(f, 'https://poidhz.com');
    expect(t).toContain('Pot UNKNOWN');
    expect(t).not.toContain('$UNKNOWN');
  });
});
