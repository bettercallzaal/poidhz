export type LiveClaim = { claimId: number; imageUrl: string | null; issuerAddress: string; farcasterHandle: string | null; title: string; description: string };
export type LiveBounty = { id: number; title: string; description: string; claims: LiveClaim[]; accepted: Set<number> };

const UA = { 'User-Agent': 'poidhz.com (+https://poidhz.com)' };

export async function fetchLiveBounty(id: number, chainId: number, fetchImpl: typeof fetch = fetch): Promise<LiveBounty | null> {
  const chain = chainId === 8453 ? 'base' : chainId === 42161 ? 'arbitrum' : 'degen';
  try {
    const r = await fetchImpl(`https://poidh.xyz/${chain}/bounty/${id}/data`, { headers: UA, signal: AbortSignal.timeout(8000), next: { revalidate: 300 } } as RequestInit);
    if (!r.ok) return null;
    const d = await r.json();
    const accepted = new Set<number>();
    try {
      const input = encodeURIComponent(JSON.stringify({ 0: { json: { bountyId: id, chainId } } }));
      const t = await fetchImpl(`https://poidh.xyz/api/trpc/claims.fetchBountyClaims?batch=1&input=${input}`, { headers: UA, signal: AbortSignal.timeout(8000), next: { revalidate: 300 } } as RequestInit);
      const items = (await t.json())[0].result.data.json.items as { id: number; isAccepted: boolean }[];
      for (const c of items) if (c.isAccepted) accepted.add(c.id);
    } catch { /* acceptance unknown; winner comes from rounds-live instead */ }
    return { id: d.id, title: d.title, description: d.description, claims: d.claims ?? [], accepted };
  } catch {
    return null;
  }
}
