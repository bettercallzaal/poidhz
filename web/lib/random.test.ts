import { describe, expect, it } from 'vitest';
import { ago, CHAINS, pickBounty, toRandomBounty } from './random';

describe('pickBounty', () => {
  it('starts at Base id 1 and ends at the last Arbitrum id', () => {
    expect(pickBounty(() => 0)).toEqual({ slug: 'base', chainName: 'Base', id: 1 });
    expect(pickBounty(() => 0.999999999)).toEqual({ slug: 'arbitrum', chainName: 'Arbitrum', id: CHAINS[1].maxId });
  });
  it('crosses from Base to Arbitrum at the right id', () => {
    const total = CHAINS[0].maxId + CHAINS[1].maxId;
    expect(pickBounty(() => (CHAINS[0].maxId - 1) / total)).toMatchObject({ slug: 'base', id: CHAINS[0].maxId });
    expect(pickBounty(() => CHAINS[0].maxId / total)).toMatchObject({ slug: 'arbitrum', id: 1 });
  });
  it('never leaves the measured range', () => {
    for (let i = 0; i < 2000; i++) {
      const p = pickBounty();
      const max = CHAINS.find((c) => c.slug === p.slug)!.maxId;
      expect(p.id).toBeGreaterThanOrEqual(1);
      expect(p.id).toBeLessThanOrEqual(max);
    }
  });
});

describe('toRandomBounty', () => {
  const p = { slug: 'base' as const, chainName: 'Base', id: 50 };
  const data = {
    id: '50', title: 'THUMBS UP', description: 'd', amount: '100000000000000', createdAt: '1719153363', issuer: '0xabc', priceUsd: 0.26,
    isCanceled: false, isMultiplayer: true, isVoting: true, inProgress: false,
    claims: [
      { claimId: 7, title: 'one', imageUrl: 'https://x/1', issuerAddress: '0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', farcasterHandle: 'ozak' },
      { claimId: 8, title: 'two', imageUrl: null, issuerAddress: '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', farcasterHandle: null },
      { claimId: 9, title: 'three', imageUrl: null, issuerAddress: '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', twitterHandle: 'tw' },
    ],
  };
  it('reads poidh data into a card', () => {
    const b = toRandomBounty(p, data, new Set([9]))!;
    expect(b).toMatchObject({ title: 'THUMBS UP', amountEth: 0.0001, usd: 0.26, open: true, url: 'https://poidh.xyz/base/bounty/50' });
    expect(b.createdAt.toISOString().slice(0, 10)).toBe('2024-06-23');
    expect(b.claims).toHaveLength(3);
  });
  it('counts people, not claims, ignoring wallet case', () => {
    expect(toRandomBounty(p, data)!.people).toBe(2);
  });
  it('names a claimer by handle, else by a short wallet', () => {
    const b = toRandomBounty(p, data)!;
    expect(b.claims.map((c) => c.by)).toEqual(['@ozak', '0xaaaa...aaaa', '@tw']);
  });
  it('says Paid out and names the winner only when a claim is accepted', () => {
    const paid = toRandomBounty(p, data, new Set([9]))!;
    expect(paid.status).toBe('Paid out');
    expect(paid.winner?.by).toBe('@tw');
    const unknown = toRandomBounty(p, data, null)!;
    expect(unknown.status).toBe('In a vote');
    expect(unknown.winner).toBeNull();
  });
  it('puts Canceled ahead of every other status', () => {
    expect(toRandomBounty(p, { ...data, isCanceled: true }, new Set([9]))!.status).toBe('Canceled');
    expect(toRandomBounty(p, { ...data, isVoting: false, inProgress: true })!.status).toBe('Open');
    expect(toRandomBounty(p, { ...data, isVoting: false })!.status).toBe('Closed');
  });
  it('returns null for an error body', () => {
    expect(toRandomBounty(p, { error: 'not found' })).toBeNull();
  });
});

describe('ago', () => {
  const now = new Date('2026-10-07T12:00:00Z');
  it('reads as days, then months, then years', () => {
    expect(ago(new Date('2026-10-07T01:00:00Z'), now)).toBe('today');
    expect(ago(new Date('2026-10-06T01:00:00Z'), now)).toBe('1 day ago');
    expect(ago(new Date('2026-06-07T12:00:00Z'), now)).toBe('4 months ago');
    expect(ago(new Date('2024-05-27T12:00:00Z'), now)).toBe('2 years ago');
  });
});
