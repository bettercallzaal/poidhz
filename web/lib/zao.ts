import type { Round } from './types';
import { publicRounds } from './rounds';

export type ListRow = { id: number; title: string; issuer: string; amount_eth: number | null; created_at: string | null; status: string; has_claims: boolean; url: string };
export type ZaoList = { ours: ListRow[]; community?: ListRow[] } | null;

const STATUS: Record<string, string> = { open: 'OPEN', voting: 'OPEN', closed: 'CLOSED', canceled: 'CANCELED' };

// Every ZAO bounty once: the rounds we keep records for, plus any bounty the poidh scan found
// that no record covers (a round cast from another wallet, or cast before anyone wrote it down).
export function mergeBounties(rounds: Round[], list: ZaoList, names: Record<string, string>): Round[] {
  const tracked = new Map(publicRounds(rounds).map((r) => [r.bounty_id!, r]));
  const out: Round[] = [];
  for (const row of list?.ours ?? []) {
    const cast_by = names[row.issuer.toLowerCase()] ?? null;
    const known = tracked.get(row.id);
    if (known) {
      out.push({ ...known, created_at: row.created_at, amount_eth: row.amount_eth, cast_by });
      tracked.delete(row.id);
      continue;
    }
    out.push({
      round: `#${row.id}`, bounty_id: row.id, title: row.title, bounty_title: row.title, url: row.url,
      status: STATUS[row.status] ?? 'OPEN', amount_usd: null, amount_eth: row.amount_eth,
      claims: row.has_claims ? null : 0, created_at: row.created_at, cast_by, winner: null,
    });
  }
  out.push(...tracked.values());
  return out.sort((a, b) => (b.created_at ?? '').localeCompare(a.created_at ?? '') || (b.bounty_id! - a.bounty_id!));
}
