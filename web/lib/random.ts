// A random bounty from poidh's whole history, for talking through old
// bounties live (Kenny, 7 Oct: "need a 'give me a random bounty' button").
//
// The id ranges are poidh's own, not ours. Measured 7 Oct 2026 against
// poidh.xyz/<chain>/bounty/<id>/data: Base answers up to 1478, Arbitrum up
// to 334. Newer bounties are left out until these numbers are raised, which
// is fine for lore. Degen did not answer on that endpoint, so it is not here.
import { claimImage } from './poidh';
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

export type RandomClaim = { id: number; title: string; image: string | null; by: string; wallet: string; won: boolean };

export type RandomBounty = Pick & {
  title: string;
  description: string;
  amountEth: number;
  usd: number | null;
  createdAt: string; // ISO, so a bounty can travel as JSON to the browser
  issuer: string;
  open: boolean; // an open bounty takes contributions and a vote; a solo one has a single issuer
  status: 'Canceled' | 'Paid out' | 'In a vote' | 'Open' | 'Closed';
  claims: RandomClaim[];
  people: number;
  winner: RandomClaim | null;
  url: string;
};

export const shortWallet = (w: string) => (w.length > 10 ? `${w.slice(0, 6)}...${w.slice(-4)}` : w);

// `accepted` is the set of claim ids poidh marks isAccepted, read from a second
// endpoint. Pass null when that read failed: the status then cannot say "Paid out".
export function toRandomBounty(p: Pick, d: Record<string, unknown>, accepted: Set<number> | null = null): RandomBounty | null {
  if (d == null || d.id == null || typeof d.title !== 'string') return null;
  const raw = Array.isArray(d.claims) ? (d.claims as Record<string, unknown>[]) : [];
  const claims: RandomClaim[] = raw.map((c) => {
    const wallet = String(c.issuerAddress ?? '');
    const handle = (c.farcasterHandle ?? c.twitterHandle ?? c.issuerName) as string | null | undefined;
    const id = Number(c.claimId);
    return { id, title: String(c.title ?? ''), image: claimImage(c), by: handle ? `@${handle}` : shortWallet(wallet), wallet, won: accepted?.has(id) ?? false };
  });
  const winner = claims.find((c) => c.won) ?? null;
  const status = d.isCanceled === true ? 'Canceled' : winner ? 'Paid out' : d.isVoting === true ? 'In a vote' : d.inProgress === true ? 'Open' : 'Closed';
  return {
    ...p,
    title: d.title,
    description: typeof d.description === 'string' ? d.description : '',
    amountEth: Number(d.amount ?? 0) / 1e18,
    usd: typeof d.priceUsd === 'number' ? d.priceUsd : null,
    createdAt: new Date(Number(d.createdAt ?? 0) * 1000).toISOString(),
    issuer: String(d.issuer ?? ''),
    open: d.isMultiplayer === true,
    status,
    claims,
    people: new Set(claims.map((c) => c.wallet.toLowerCase())).size,
    winner,
    url: `https://poidh.xyz/${p.slug}/bounty/${p.id}`,
  };
}

export function ago(from: Date, now: Date): string {
  const days = Math.floor((now.getTime() - from.getTime()) / 86400000);
  if (days < 1) return 'today';
  if (days < 60) return `${days} day${days === 1 ? '' : 's'} ago`;
  if (days < 730) return `${Math.floor(days / 30)} months ago`;
  return `${Math.floor(days / 365)} years ago`;
}
