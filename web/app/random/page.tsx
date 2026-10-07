import { pickBounty, toRandomBounty, type RandomBounty } from '@/lib/random';

export const dynamic = 'force-dynamic';
export const metadata = { title: 'Random poidh bounty - poidhz', description: 'A random bounty from all of poidh, Base and Arbitrum.' };

const UA = { 'User-Agent': 'poidhz.com (+https://poidhz.com)' };

async function loadRandom(): Promise<RandomBounty | null> {
  // A few tries, because an id can come back empty.
  for (let i = 0; i < 4; i++) {
    const p = pickBounty();
    try {
      const r = await fetch(`https://poidh.xyz/${p.slug}/bounty/${p.id}/data`, { headers: UA, signal: AbortSignal.timeout(6000), cache: 'no-store' });
      if (!r.ok) continue;
      const b = toRandomBounty(p, await r.json());
      if (b) return b;
    } catch { /* try another id */ }
  }
  return null;
}

export default async function RandomPage() {
  const b = await loadRandom();
  return (
    <>
      <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold tracking-tight">Random poidh bounty</h1>
        {/* A plain link with a fresh query, so the browser really loads a new pick. A Next <Link> to the page you are already on does nothing. */}
        <a href={`/random?n=${Math.random().toString(36).slice(2, 8)}`} className="inline-block rounded-full bg-[var(--accent)] px-6 py-3 text-lg font-semibold text-[var(--on-accent)] no-underline shadow-lg">Give me another one</a>
      </div>
      {!b ? (
        <p className="mt-6">poidh did not answer. Hit the button again.</p>
      ) : (
        <section className="mt-6 rounded-lg border border-[var(--line)] p-5">
          <p className="text-sm text-[var(--muted)]">
            {b.chainName} bounty {b.id} - {b.createdAt.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' })}
            {b.canceled && <span className="ml-2 text-[var(--warn)]">canceled</span>}
          </p>
          <h2 className="mt-2 break-words text-3xl font-bold tracking-tight">{b.title}</h2>
          <p className="mt-2 text-sm text-[var(--muted)]">{b.amountEth} ETH - {b.claims} {b.claims === 1 ? 'claim' : 'claims'}</p>
          {b.description && <p className="mt-4 max-h-80 overflow-auto whitespace-pre-wrap break-words text-sm leading-relaxed">{b.description}</p>}
          <p className="mt-4"><a href={b.url} target="_blank" rel="noopener">Open it on poidh</a></p>
        </section>
      )}
      <p className="mt-6 text-xs text-[var(--muted)]">Picked at random from every bounty ever made on poidh on Base (1 to 1478) and Arbitrum (1 to 334).</p>
    </>
  );
}
