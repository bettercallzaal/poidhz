import type { Claim, LeaderRow, Note, Person, Winner } from './types';

export function buildPeople(claims: Claim[], leaderboard: LeaderRow[], notes: Map<number, Note>, winners: Winner[]): Person[] {
  const lb = new Map(leaderboard.map((r) => [r.address.toLowerCase(), r]));
  const winClaims = new Set(winners.map((w) => w.claim_id));
  const byWallet = new Map<string, Person>();
  for (const c of claims) {
    const w = c.wallet.toLowerCase();
    let p = byWallet.get(w);
    if (!p) {
      const row = lb.get(w);
      const handle = c.handle ?? row?.farcaster_username ?? null;
      p = { key: handle ?? w, wallet: w, handle, displayName: row?.displayName ?? null, avatar: row?.avatar ?? null, fid: row?.fid ?? null, claims: [], bounties: [], wins: [], notes: [] };
      byWallet.set(w, p);
    } else if (!p.handle && c.handle) { p.handle = c.handle; p.key = c.handle; }
    p.claims.push(c);
    if (!p.bounties.includes(c.bounty_id)) p.bounties.push(c.bounty_id);
    if (winClaims.has(c.claim_id) && !p.wins.includes(c.bounty_id)) p.wins.push(c.bounty_id);
    const n = notes.get(c.claim_id);
    if (n) p.notes.push(n);
  }
  const out = [...byWallet.values()];
  for (const p of out) { p.bounties.sort((a, b) => a - b); p.wins.sort((a, b) => a - b); }
  return out.sort((a, b) => b.bounties.length - a.bounties.length || Math.min(...a.claims.map((c) => c.claim_id)) - Math.min(...b.claims.map((c) => c.claim_id)));
}

export function findPerson(people: Person[], key: string): Person | undefined {
  let raw = key;
  try { raw = decodeURIComponent(key); } catch { return undefined; }
  const k = raw.toLowerCase().replace(/^@/, '');
  return people.find((p) => p.wallet === k || (p.handle ?? '').toLowerCase() === k);
}
