import { notFound } from 'next/navigation';
import Link from 'next/link';
import { loadPeople } from '@/lib/load';
import { findPerson } from '@/lib/people';
import { shortAddr } from '@/lib/format';
import { ClaimCard } from '@/components/ClaimCard';

export const revalidate = 300;

export default async function PersonPage({ params }: { params: Promise<{ key: string }> }) {
  const { people, notes, rounds } = await loadPeople();
  const p = findPerson(people, (await params).key);
  if (!p) notFound();
  const name = p.handle ? `@${p.handle}` : shortAddr(p.wallet);
  const byBounty = [...p.bounties].reverse();
  return (
    <>
      <div className="mt-6 flex items-center gap-4">
        {p.avatar && <img src={p.avatar} alt="" className="h-16 w-16 rounded-full" />}
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{p.displayName || name}</h1>
          <p className="text-sm text-[var(--muted)]">{name} - entered {p.bounties.length} round{p.bounties.length === 1 ? '' : 's'}{p.wins.length ? ` - won ${p.wins.length}` : ''}{p.handle && <> - <a href={`https://farcaster.xyz/${p.handle}`}>Farcaster</a></>}</p>
        </div>
      </div>
      {byBounty.map((bid) => {
        const r = rounds.find((x) => x.bounty_id === bid);
        return (
          <section key={bid} className="mt-8">
            <h2 className="text-lg font-semibold"><Link href={`/b/${bid}`}>{r?.bounty_title || r?.title || `Bounty ${bid}`}</Link></h2>
            <div className="mt-3 grid gap-3 sm:grid-cols-2">
              {p.claims.filter((c) => c.bounty_id === bid).map((c) => <ClaimCard key={c.claim_id} c={c} note={notes.get(c.claim_id)} won={r?.winner?.claim_id === c.claim_id} personKey={p.key} />)}
            </div>
          </section>
        );
      })}
    </>
  );
}
