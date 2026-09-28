import { describe, it, expect, vi } from 'vitest';
import snap from '../test/fixtures/claims.json';
import liveRaw from '../test/fixtures/live-1421.json';
import { claimsFor } from './claims';
import { fetchLiveBounty, type LiveBounty } from './poidh';

const live: LiveBounty = { ...liveRaw, accepted: new Set(liveRaw.accepted) } as LiveBounty;

describe('claimsFor', () => {
  it('prefers live and lowercases wallets', () => {
    const r = claimsFor(1421, live, snap);
    expect(r.source).toBe('live');
    expect(r.claims.map((c) => c.claim_id)).toEqual([8338, 8310]);
    expect(r.claims[1]).toMatchObject({ handle: 'assay', accepted: true, wallet: '0xccc0000000000000000000000000000000000003' });
  });
  it('falls back to snapshot when live is null', () => {
    const r = claimsFor(1412, null, snap);
    expect(r.source).toBe('snapshot');
    expect(r.claims[0].wallet).toBe('0xbbb0000000000000000000000000000000000002');
  });
  it('none when neither has the bounty', () => expect(claimsFor(9999, null, snap).source).toBe('none'));
});

describe('fetchLiveBounty', () => {
  it('returns null on network failure instead of throwing', async () => {
    const f = vi.fn().mockRejectedValue(new Error('down'));
    expect(await fetchLiveBounty(1421, 8453, f as any)).toBeNull();
  });
  it('merges accepted flags from trpc', async () => {
    const f = vi.fn()
      .mockResolvedValueOnce({ ok: true, json: async () => ({ ...liveRaw, accepted: undefined }) })
      .mockResolvedValueOnce({ ok: true, json: async () => [{ result: { data: { json: { items: [{ id: 8310, isAccepted: true }, { id: 8338, isAccepted: false }] } } } }] });
    const b = await fetchLiveBounty(1421, 8453, f as any);
    expect(b && [...b.accepted]).toEqual([8310]);
  });
});
