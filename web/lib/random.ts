// A random bounty from poidh's whole history, for talking through old
// bounties live (Kenny, 7 Oct: "need a 'give me a random bounty' button").
//
// The id ranges are poidh's own, not ours. Measured 7 Oct 2026 against
// poidh.xyz/<chain>/bounty/<id>/data: Base answers up to 1478, Arbitrum up
// to 334. Newer bounties are left out until these numbers are raised, which
// is fine for lore. Degen did not answer on that endpoint, so it is not here.
export const CHAINS = [
  { slug: 'base', chainId: 8453, name: 'Base', maxId: 1478 },
  { slug: 'arbitrum', chainId: 42161, name: 'Arbitrum', maxId: 334 },
] as const;

export type Pick = { slug: (typeof CHAINS)[number]['slug']; chainName: string; id: number };

// Every id on every chain is equally likely, so a chain is weighted by how
// many bounties it has.
export function pickBounty(rand: () => number = Math.random): Pick {
  const total = CHAINS.reduce((n, c) => n + c.maxId, 0);
  let k = Math.floor(rand() * total);
  for (const c of CHAINS) {
    if (k < c.maxId) return { slug: c.slug, chainName: c.name, id: k + 1 };
    k -= c.maxId;
  }
  const last = CHAINS[CHAINS.length - 1];
  return { slug: last.slug, chainName: last.name, id: last.maxId };
}

export type RandomBounty = Pick & {
  title: string;
  description: string;
  amountEth: number;
  createdAt: Date;
  canceled: boolean;
  claims: number;
  url: string;
};

export function toRandomBounty(p: Pick, d: Record<string, unknown>): RandomBounty | null {
  if (d == null || d.id == null || typeof d.title !== 'string') return null;
  return {
    ...p,
    title: d.title,
    description: typeof d.description === 'string' ? d.description : '',
    amountEth: Number(d.amount ?? 0) / 1e18,
    createdAt: new Date(Number(d.createdAt ?? 0) * 1000),
    canceled: d.isCanceled === true,
    claims: Array.isArray(d.claims) ? d.claims.length : 0,
    url: `https://poidh.xyz/${p.slug}/bounty/${p.id}`,
  };
}
