import { describe, expect, it } from 'vitest';
import { CHAINS, pickBounty, toRandomBounty } from './random';

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
  it('reads poidh data into a card', () => {
    const b = toRandomBounty(p, { id: '50', title: 'THUMBS UP', description: 'd', amount: '100000000000000', createdAt: '1719153363', isCanceled: false, claims: [{}, {}] });
    expect(b).toMatchObject({ title: 'THUMBS UP', amountEth: 0.0001, canceled: false, claims: 2, url: 'https://poidh.xyz/base/bounty/50' });
    expect(b!.createdAt.toISOString().slice(0, 10)).toBe('2024-06-23');
  });
  it('returns null for an error body', () => {
    expect(toRandomBounty(p, { error: 'not found' })).toBeNull();
  });
});
