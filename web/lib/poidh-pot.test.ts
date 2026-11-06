import { describe, it, expect } from 'vitest';
import { fetchEthUsd, fetchPotEth, loadPot, potView, type LastKnownPot } from '@/lib/poidh-pot';

const json = (body: unknown, ok = true) => ({ ok, json: async () => body }) as Response;
const trpc = (b: unknown) => [{ result: { data: { json: b } } }];

// One fake fetch that answers poidh and CoinGecko, or fails, per test.
function fakeFetch(opts: { amount?: string | null; poidhDown?: boolean; rate?: number | null; rateDown?: boolean; id?: number }) {
  return (async (url: string) => {
    if (url.includes('poidh.xyz')) {
      if (opts.poidhDown) throw new Error('poidh down');
      return json(trpc({ id: opts.id ?? 42, amount: opts.amount ?? '0', isCanceled: false }));
    }
    if (opts.rateDown) throw new Error('rate down');
    return json({ ethereum: { usd: opts.rate } });
  }) as unknown as typeof fetch;
}

const LAST: LastKnownPot = { eth: 0.0447, usdPerEth: 2237.49, date: '2026-11-06' };

describe('poidh live pot', () => {
  it('success: reads the live pot and an approximate USD', async () => {
    const f = fakeFetch({ amount: '255936000000000000', rate: 2237.49 });
    expect(await fetchPotEth(42, 8453, f)).toBeCloseTo(0.255936, 6);
    const v = await loadPot(42, LAST, f);
    expect(v).toMatchObject({ source: 'live', rateSource: 'live', approxUsd: true, asOf: null });
    expect(v!.eth).toBeCloseTo(0.255936, 6);
    expect(v!.usd).toBeCloseTo(572.65, 2);
  });

  it('API down: falls back to the last known pot with its date, never zero', async () => {
    const v = await loadPot(42, LAST, fakeFetch({ poidhDown: true, rateDown: true }));
    expect(v).toMatchObject({ eth: 0.0447, source: 'last-known', rateSource: 'last-known', asOf: '2026-11-06' });
    expect(v!.usd).toBeCloseTo(100.02, 2);
    expect(v!.eth).not.toBe(0);
  });

  it('zero contributions: a live zero is shown as zero, not replaced by the last known pot', async () => {
    const v = await loadPot(42, LAST, fakeFetch({ amount: '0', rate: 2237.49 }));
    expect(v).toMatchObject({ eth: 0, usd: 0, source: 'live' });
  });

  it('no id yet: nothing is fetched and the page keeps the hand-entered row', async () => {
    let called = false;
    const f = (async () => { called = true; throw new Error('should not fetch'); }) as unknown as typeof fetch;
    expect(await loadPot(null, LAST, f)).toBeNull();
    expect(called).toBe(false);
  });

  it('poidh down and nothing known yet: null, so the page keeps the hand-entered row', async () => {
    expect(await loadPot(42, null, fakeFetch({ poidhDown: true, rate: 2237.49 }))).toBeNull();
  });

  it('live pot but no price anywhere: ETH only, no made-up dollars', () => {
    expect(potView(0.05, null, null)).toMatchObject({ eth: 0.05, usd: null, rateSource: null, source: 'live' });
  });

  it('rejects a wrong id, a cancelled bounty and a non-numeric amount', async () => {
    expect(await fetchPotEth(42, 8453, fakeFetch({ id: 7, amount: '1' }))).toBeNull();
    const cancelled = (async () => json(trpc({ id: 42, amount: '1', isCanceled: true }))) as unknown as typeof fetch;
    expect(await fetchPotEth(42, 8453, cancelled)).toBeNull();
    expect(await fetchPotEth(42, 8453, fakeFetch({ amount: 'abc' }))).toBeNull();
    expect(await fetchEthUsd(fakeFetch({ rate: -1 }))).toBeNull();
  });
});
