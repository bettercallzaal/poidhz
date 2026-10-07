import { ago, pickBounty, shortWallet, toRandomBounty, type RandomBounty } from '@/lib/random';

export const dynamic = 'force-dynamic';
export const metadata = { title: 'Random poidh bounty - poidhz', description: 'A random bounty from all of poidh, Base and Arbitrum.' };

const UA = { 'User-Agent': 'poidhz.com (+https://poidhz.com)' };
const CHAIN_ID = { base: 8453, arbitrum: 42161 } as const;

// Which claims poidh marks accepted. null means the read failed, so the page
// cannot say who won.
async function acceptedClaims(id: number, chainId: number): Promise<Set<number> | null> {
  try {
    const input = encodeURIComponent(JSON.stringify({ 0: { json: { bountyId: id, chainId } } }));
    const r = await fetch(`https://poidh.xyz/api/trpc/claims.fetchBountyClaims?batch=1&input=${input}`, { headers: UA, signal: AbortSignal.timeout(6000), cache: 'no-store' });
    if (!r.ok) return null;
    const items = (await r.json())[0].result.data.json.items as { id: number; isAccepted: boolean }[];
    return new Set(items.filter((c) => c.isAccepted).map((c) => c.id));
  } catch {
    return null;
  }
}

async function loadRandom(): Promise<RandomBounty | null> {
  // A few tries, because an id can come back empty.
  for (let i = 0; i < 4; i++) {
    const p = pickBounty();
    try {
      const [r, accepted] = await Promise.all([
        fetch(`https://poidh.xyz/${p.slug}/bounty/${p.id}/data`, { headers: UA, signal: AbortSignal.timeout(6000), cache: 'no-store' }),
        acceptedClaims(p.id, CHAIN_ID[p.slug]),
      ]);
      if (!r.ok) continue;
      const b = toRandomBounty(p, await r.json(), accepted);
      if (b) return b;
    } catch { /* try another id */ }
  }
  return null;
}

function Stat({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="rounded-lg border border-[var(--line)] p-3">
      <div className="text-xs uppercase tracking-wide text-[var(--muted)]">{label}</div>
      <div className="mt-1 break-words text-lg font-bold">{value}</div>
      {sub && <div className="text-xs text-[var(--muted)]">{sub}</div>}
    </div>
  );
}

const eth = (n: number) => (n === 0 ? '0' : n < 0.0001 ? n.toExponential(1) : String(Number(n.toFixed(5))));

export default async function RandomPage() {
  const b = await loadRandom();
  const now = new Date();
  return (
    <>
      <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold tracking-tight">Random poidh bounty</h1>
        {/* A plain link, so the browser really loads a new pick: a Next <Link> to the page you are already on does nothing. The query names the bounty on screen, which keeps the address changing from one pick to the next. */}
        <a href={`/random?after=${b ? `${b.slug}-${b.id}` : 'retry'}`} className="inline-block rounded-full bg-[var(--accent)] px-6 py-3 text-lg font-semibold text-[var(--on-accent)] no-underline shadow-lg">Give me another one</a>
      </div>
      {!b ? (
        <p className="mt-6">poidh did not answer. Hit the button again.</p>
      ) : (
        <>
          <section className="mt-6 rounded-lg border border-[var(--line)] p-5">
            <p className="text-sm text-[var(--muted)]">{b.chainName} bounty {b.id}</p>
            <h2 className="mt-2 break-words text-3xl font-bold tracking-tight">{b.title}</h2>
            {b.description && <p className="mt-4 max-h-64 overflow-auto whitespace-pre-wrap break-words text-sm leading-relaxed">{b.description}</p>}
            <p className="mt-4 text-sm"><a href={b.url} target="_blank" rel="noopener">Open it on poidh</a></p>
          </section>

          <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4">
            <Stat label="Pot" value={`${eth(b.amountEth)} ETH`} sub={b.usd != null ? `about $${b.usd.toFixed(2)} at poidh's price today` : undefined} />
            <Stat label="Status" value={b.status} sub={b.open ? 'open bounty, others could add to the pot' : 'solo bounty, one issuer picks'} />
            <Stat label="Claims" value={String(b.claims.length)} sub={b.claims.length ? `from ${b.people} ${b.people === 1 ? 'person' : 'people'}` : 'nobody entered'} />
            <Stat label="Posted" value={ago(b.createdAt, now)} sub={b.createdAt.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' })} />
            <Stat label="Posted by" value={shortWallet(b.issuer)} />
            <Stat label="Winner" value={b.winner ? b.winner.by : b.status === 'Canceled' ? 'none, canceled' : 'none recorded'} sub={b.winner ? b.winner.title.slice(0, 60) : undefined} />
          </div>

          {b.claims.length > 0 && (
            <>
              <h3 className="mt-8 text-xl font-semibold">The pics ({b.claims.length})</h3>
              <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4">
                {b.claims.slice(0, 12).map((c) => (
                  <div key={c.id} className={`overflow-hidden rounded-lg border ${c.won ? 'border-2 border-[var(--warn)]' : 'border-[var(--line)]'}`}>
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    {c.image ? <img src={c.image} alt={c.title} loading="lazy" className="aspect-square w-full object-cover" /> : <div className="flex aspect-square w-full items-center justify-center text-xs text-[var(--muted)]">no image</div>}
                    <div className="p-2 text-xs">
                      {c.won && <div className="font-semibold text-[var(--warn)]">Winner</div>}
                      <div className="line-clamp-2 break-words">{c.title}</div>
                      <div className="text-[var(--muted)]">{c.by}</div>
                    </div>
                  </div>
                ))}
              </div>
              {b.claims.length > 12 && <p className="mt-2 text-xs text-[var(--muted)]">Showing 12 of {b.claims.length}. The rest are on poidh.</p>}
            </>
          )}
        </>
      )}
      <p className="mt-6 text-xs text-[var(--muted)]">Picked at random from every bounty ever made on poidh on Base (1 to 1478) and Arbitrum (1 to 334). Numbers are read from poidh as the page loads.</p>
    </>
  );
}
