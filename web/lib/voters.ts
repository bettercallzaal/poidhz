import 'server-only';
import { loadAll, sources } from './load';
import { fetchLiveBounty } from './poidh';
import { claimsFor } from './claims';
import { publicRounds, roundPhase } from './rounds';
import { buildPeople } from './people';

// Who can vote, and on what. Wallets come from live poidh claims on every ZAO bounty.
export async function loadVoteContext() {
  const all = await loadAll();
  const bountyId = (sources as { vote?: { bounty_id: number } }).vote?.bounty_id;
  const round = publicRounds(all.rounds).find((r) => r.bounty_id === bountyId) ?? null;
  const ids = publicRounds(all.rounds).filter((r) => r.status !== 'CANCELED').map((r) => r.bounty_id!);
  const lives = await Promise.all(ids.map((id) => fetchLiveBounty(id, sources.chain_id)));
  const walletsByBounty: Record<number, string[]> = {};
  let unread = 0;
  ids.forEach((id, i) => {
    const set = claimsFor(id, lives[i], all.snapshot);
    if (set.source !== 'live') unread++;
    walletsByBounty[id] = set.claims.map((c) => c.wallet);
  });
  const entrySet = bountyId ? claimsFor(bountyId, lives[ids.indexOf(bountyId)] ?? null, all.snapshot) : null;
  const people = entrySet ? buildPeople(entrySet.claims, all.leaderboard, all.notes, []) : [];
  const entries = (entrySet?.claims ?? []).map((c) => ({
    claim: c.claim_id, wallet: c.wallet, title: c.title, image: c.image_url,
    name: people.find((p) => p.wallet === c.wallet)?.handle ?? null,
    link: c.description.match(/https?:\/\/[^\s)]+/)?.[0] ?? null,
  }));
  const open = round ? !['won', 'canceled'].includes(roundPhase(round, new Date())) : false;
  return { bountyId: bountyId ?? null, round, open, walletsByBounty, entries, unreadBounties: unread };
}
