import 'server-only';
import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import sources from '@/sources.json';
import type { LeaderRow, Round, Winner } from './types';
import { notesFrom } from './feedback';
import { fetchLiveBounty } from './poidh';
import { claimsFor } from './claims';
import { buildPeople } from './people';
import { personBountyIds, publicRounds } from './rounds';
import { mergeBounties, type ZaoList } from './zao';

export const SITE = process.env.NEXT_PUBLIC_SITE_URL || 'https://poidhz.com';
export { sources };
const DATA = join(process.cwd(), 'public', 'data');
const json = async (f: string) => JSON.parse(await readFile(join(DATA, f), 'utf8'));

export async function loadAll() {
  const live = await json('rounds-live.json');
  const issuers = new Set(sources.issuers.map((a: string) => a.toLowerCase()));
  const snapshot = await json('claims.json');
  const issuerOf = new Map<number, string>(snapshot.bounties.map((b: any) => [Number(b.id), String(b.issuer).toLowerCase()]));
  const tracked = (live.rounds as Round[]).filter((r) => r.bounty_id === undefined || !issuerOf.has(r.bounty_id) || issuers.has(issuerOf.get(r.bounty_id)!));
  // The full scan is optional: without it the board still shows every tracked round.
  const list = (await json('zao-bounties.json').catch(() => null)) as ZaoList;
  const rounds = mergeBounties(tracked, list, (sources as { issuer_names?: Record<string, string> }).issuer_names ?? {});
  const files = (await readdir(join(DATA, 'feedback'))).filter((f) => f.endsWith('.json'));
  const notes = notesFrom(await Promise.all(files.map((f) => json(join('feedback', f)))));
  const leaderboard = (await json('leaderboard.json')) as LeaderRow[];
  return { rounds, roundsAsOf: live.generated_at as string, listAsOf: (list as { generated_at?: string } | null)?.generated_at ?? null, snapshot, leaderboard, notes };
}

export async function loadBounty(id: number) {
  const all = await loadAll();
  const round = publicRounds(all.rounds).find((r) => r.bounty_id === id);
  if (!round) return null;
  const live = await fetchLiveBounty(id, sources.chain_id);
  return { ...all, round, live, set: claimsFor(id, live, all.snapshot) };
}

export async function loadPeople() {
  const all = await loadAll();
  const ids = personBountyIds(all.rounds);
  const lives = await Promise.all(ids.map((id) => fetchLiveBounty(id, sources.chain_id)));
  const claims = ids.flatMap((id, i) => claimsFor(id, lives[i], all.snapshot).claims);
  const winners = all.rounds.map((r) => r.winner).filter(Boolean) as Winner[];
  return { ...all, people: buildPeople(claims, all.leaderboard, all.notes, winners), liveCount: lives.filter(Boolean).length, total: ids.length };
}
