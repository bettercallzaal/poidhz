import { notFound } from 'next/navigation';
import { loadBounty } from '@/lib/load';
import { roundPhase } from '@/lib/rounds';
import { countText, roundName, usd } from '@/lib/format';
import { buildPeople } from '@/lib/people';
import { PhaseBadge } from '@/components/PhaseBadge';
import { ClaimCard } from '@/components/ClaimCard';

export const revalidate = 300;

export default async function BountyPage({ params }: { params: Promise<{ id: string }> }) {
  const id = Number((await params).id);
  if (!Number.isInteger(id)) notFound();
  const b = await loadBounty(id);
  if (!b) notFound();
  const { round, live, set, leaderboard, notes } = b;
  const phase = roundPhase(round, new Date());
  const people = buildPeople(set.claims, leaderboard, notes, round.winner ? [round.winner] : []);
  const keyOf = (w: string) => people.find((p) => p.wallet === w)!.key;
  const count = set.source === 'none' ? null : set.claims.length;
  return (
    <>
      <div className="mt-6 flex items-center gap-2"><PhaseBadge phase={phase} /><span className="text-sm text-[var(--muted)]">{roundName(round)} - bounty {id}</span></div>
      <h1 className="mt-2 text-3xl font-bold tracking-tight">{round.bounty_title || round.title}</h1>
      <p className="mt-2 text-sm text-[var(--muted)]">Pot {usd(round.amount_usd)} - {countText(count)} entries</p>
      {phase === 'open' && <p className="mt-4 flex gap-3"><a href={round.url || `https://poidh.xyz/base/bounty/${id}`} className="rounded bg-[var(--accent)] px-4 py-2 font-semibold text-[var(--bg)] no-underline">Enter on poidh</a><a href="/submit" className="px-2 py-2">Make a submission card</a></p>}
      {live?.description && <section className="mt-6 whitespace-pre-wrap rounded-lg border border-[var(--line)] p-4 text-sm leading-relaxed">{live.description}</section>}
      <h2 className="mt-8 text-xl font-semibold">Entries</h2>
      {set.source === 'snapshot' && <p className="mt-1 text-xs text-[var(--warn)]">poidh did not answer, so this list is from the last snapshot and may be missing recent entries.</p>}
      {set.source === 'none' && <p className="mt-1 text-sm">Entries could not be read right now.</p>}
      <div className="mt-3 grid gap-3 sm:grid-cols-2">
        {set.claims.map((c) => <ClaimCard key={c.claim_id} c={c} note={notes.get(c.claim_id)} won={round.winner?.claim_id === c.claim_id} personKey={keyOf(c.wallet)} />)}
      </div>
    </>
  );
}
