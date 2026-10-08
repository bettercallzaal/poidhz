import { pickBounty, toRandomBounty, type RandomBounty } from './random';

const UA = { 'User-Agent': 'poidhz.com (+https://poidhz.com)' };
const CHAIN_ID = { base: 8453, arbitrum: 42161 } as const;
// Old bounties barely change, so each id's answer from poidh is kept for an hour.
// A repeat pick is then served from the cache instead of a slow round trip.
const KEEP = { next: { revalidate: 3600 } } as RequestInit;

// Which claims poidh marks accepted. null means the read failed, so the page
// cannot say who won.
async function acceptedClaims(id: number, chainId: number): Promise<Set<number> | null> {
  try {
    const input = encodeURIComponent(JSON.stringify({ 0: { json: { bountyId: id, chainId } } }));
    const r = await fetch(`https://poidh.xyz/api/trpc/claims.fetchBountyClaims?batch=1&input=${input}`, { headers: UA, signal: AbortSignal.timeout(6000), ...KEEP });
    if (!r.ok) return null;
    const items = (await r.json())[0].result.data.json.items as { id: number; isAccepted: boolean }[];
    return new Set(items.filter((c) => c.isAccepted).map((c) => c.id));
  } catch {
    return null;
  }
}

export async function loadRandom(): Promise<RandomBounty | null> {
  // A few tries, because an id can come back empty.
  for (let i = 0; i < 4; i++) {
    const p = pickBounty();
    try {
      const [r, accepted] = await Promise.all([
        fetch(`https://poidh.xyz/${p.slug}/bounty/${p.id}/data`, { headers: UA, signal: AbortSignal.timeout(6000), ...KEEP }),
        acceptedClaims(p.id, CHAIN_ID[p.slug]),
      ]);
      if (!r.ok) continue;
      const b = toRandomBounty(p, await r.json(), accepted);
      if (b) return b;
    } catch { /* try another id */ }
  }
  return null;
}
