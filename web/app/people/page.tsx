import Link from 'next/link';
import { loadPeople } from '@/lib/load';
import { shortAddr } from '@/lib/format';

export const revalidate = 300;

export default async function People() {
  const { people, liveCount, total } = await loadPeople();
  const groups = new Map<number, typeof people>();
  for (const p of people) groups.set(p.bounties.length, [...(groups.get(p.bounties.length) ?? []), p]);
  const back = people.filter((p) => p.bounties.length > 1).length;
  return (
    <>
      <h1 className="mt-6 text-3xl font-bold tracking-tight">The people</h1>
      <p className="mt-2 text-[var(--muted)]">{people.length} people have entered a ZAO round. {back} came back for more than one. Grouped by how many rounds they entered, which is a fact, not a ranking.</p>
      {liveCount < total && <p className="mt-1 text-xs text-[var(--warn)]">{total - liveCount} of {total} rounds were read from the snapshot because poidh did not answer.</p>}
      {[...groups.keys()].sort((a, b) => b - a).map((n) => (
        <section key={n} className="mt-6">
          <h2 className="font-semibold">{n} round{n === 1 ? '' : 's'}</h2>
          <ul className="mt-2 flex flex-wrap gap-2">
            {groups.get(n)!.map((p) => <li key={p.wallet}><Link href={`/u/${encodeURIComponent(p.key)}`} className="block rounded border border-[var(--line)] px-3 py-1 no-underline">{p.handle ? `@${p.handle}` : shortAddr(p.wallet)}</Link></li>)}
          </ul>
        </section>
      ))}
    </>
  );
}
