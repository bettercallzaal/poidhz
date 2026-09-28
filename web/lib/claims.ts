import type { Claim } from './types';
import type { LiveBounty } from './poidh';
export type ClaimSet = { claims: Claim[]; source: 'live' | 'snapshot' | 'none' };

export function claimsFor(bountyId: number, live: LiveBounty | null, snapshot: { claims: any[] }): ClaimSet {
  if (live) {
    return { source: 'live', claims: live.claims.map((c) => ({
      claim_id: c.claimId, bounty_id: bountyId, wallet: c.issuerAddress.toLowerCase(), title: c.title, description: c.description,
      image_url: c.imageUrl, accepted: live.accepted.has(c.claimId), handle: c.farcasterHandle,
    })) };
  }
  const rows = snapshot.claims.filter((c) => Number(c.bounty_id) === bountyId);
  if (!rows.length) return { source: 'none', claims: [] };
  return { source: 'snapshot', claims: rows.map((c) => ({
    claim_id: Number(c.claim_id), bounty_id: bountyId, wallet: String(c.issuer).toLowerCase(), title: c.title ?? '', description: c.description ?? '',
    image_url: c.image_url ?? null, accepted: c.accepted === true || c.accepted === 'True', handle: null,
  })) };
}
