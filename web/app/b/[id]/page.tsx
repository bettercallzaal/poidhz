import { notFound } from 'next/navigation';
import { roundPhase } from '@/lib/rounds';
import { countText, potText, roundName } from '@/lib/format';
import { buildPeople } from '@/lib/people';
import { PhaseBadge } from '@/components/PhaseBadge';
import { ClaimCard } from '@/components/ClaimCard';
import { EntryShare } from '@/components/EntryShare';
import { loadBounty, SITE, sources } from '@/lib/load';

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
      <p className="mt-2 text-sm text-[var(--muted)]">Pot {potText(round)} - {countText(count)} entries</p>
      {phase === 'open' && (
        <section className="mt-6 rounded-lg border border-[var(--line)] p-4">
          <h2 className="text-xl font-semibold">How to enter</h2>
          <ol className="mt-2 list-decimal space-y-1 pl-5 text-sm">
            <li>Read the bounty below. The deadline is in the text.</li>
            <li>Make your entry, then claim it on poidh with a public link in the claim.</li>
            <li>Tell everyone about it with the box further down, so people can see it and reply.</li>
          </ol>
          <p className="mt-3"><a href={round.url || `https://poidh.xyz/base/bounty/${id}`} target="_blank" rel="noopener" className="inline-block rounded bg-[var(--accent)] px-4 py-2 font-semibold text-[var(--bg)] no-underline">Enter on poidh</a></p>
        </section>
      )}
      {live?.description && <section className="mt-6 whitespace-pre-wrap rounded-lg border border-[var(--line)] p-4 text-sm leading-relaxed">{live.description}</section>}
      {phase === 'open' && <EntryShare title={round.bounty_title || round.title || `Bounty ${id}`} boardUrl={`${SITE}/b/${id}`} channel={sources.channel} hints={(sources as { entry_hints?: Record<string, { link?: string; about?: string }> }).entry_hints?.[String(id)]} />}
      <h2 className="mt-8 text-xl font-semibold">Entries</h2>
      {set.source === 'snapshot' && <p className="mt-1 text-xs text-[var(--warn)]">poidh did not answer, so this list is from the last snapshot and may be missing recent entries.</p>}
      {set.source === 'none' && <p className="mt-1 text-sm">Entries could not be read right now.</p>}
      <div className="mt-3 grid gap-3 sm:grid-cols-2">
        {set.claims.map((c) => <ClaimCard key={c.claim_id} c={c} note={notes.get(c.claim_id)} won={round.winner?.claim_id === c.claim_id} personKey={keyOf(c.wallet)} />)}
      </div>
    </>
  );
}
