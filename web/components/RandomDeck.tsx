'use client';

import { useEffect, useRef, useState } from 'react';
import { ago, shortWallet, type RandomBounty } from '@/lib/random';

// How many picks to keep loaded behind the one on screen.
const AHEAD = 5;

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

// Warm the browser cache for a pick's pictures before it is shown.
function preload(b: RandomBounty) {
  for (const c of b.claims.slice(0, 12)) if (c.image) new Image().src = c.image;
}

export function RandomDeck({ first }: { first: RandomBounty | null }) {
  const [shown, setShown] = useState<RandomBounty | null>(first);
  const [ready, setReady] = useState(0);
  const queue = useRef<RandomBounty[]>([]);
  const inFlight = useRef(0);
  const seen = useRef(new Set<string>(first ? [`${first.slug}-${first.id}`] : []));

  const fill = () => {
    while (queue.current.length + inFlight.current < AHEAD) {
      inFlight.current++;
      fetch('/api/random', { cache: 'no-store' })
        .then((r) => (r.ok ? (r.json() as Promise<RandomBounty>) : null))
        .then((b) => {
          if (!b) return;
          const key = `${b.slug}-${b.id}`;
          if (seen.current.has(key)) return; // skip a repeat, the next fill asks again
          seen.current.add(key);
          preload(b);
          queue.current.push(b);
        })
        .catch(() => {})
        .finally(() => {
          inFlight.current--;
          setReady(queue.current.length);
          if (queue.current.length < AHEAD) setTimeout(fill, 300);
        });
    }
  };

  // Start loading ahead once the page is up. fill only reads refs and sets
  // state after a network answer, so it is safe to start from here.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { fill(); }, []);

  const next = () => {
    const b = queue.current.shift();
    if (b) {
      setShown(b);
      setReady(queue.current.length);
      window.scrollTo({ top: 0 });
    }
    fill();
  };

  const b = shown;
  const now = new Date();
  return (
    <>
      <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold tracking-tight">Random poidh bounty</h1>
        <div className="flex items-center gap-3">
          <span className="text-xs text-[var(--muted)]">{ready} ready</span>
          <button type="button" onClick={next} disabled={ready === 0} className="rounded-full bg-[var(--accent)] px-6 py-3 text-lg font-semibold text-[var(--on-accent)] shadow-lg disabled:opacity-60">
            {ready === 0 ? 'Loading...' : 'Give me another one'}
          </button>
        </div>
      </div>
      {!b ? (
        <p className="mt-6">poidh did not answer. The next one is loading.</p>
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
            <Stat label="Posted" value={ago(new Date(b.createdAt), now)} sub={new Date(b.createdAt).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' })} />
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
                    {c.image ? <img src={c.image} alt={c.title} className="aspect-square w-full object-cover" /> : <div className="flex aspect-square w-full items-center justify-center text-xs text-[var(--muted)]">no image</div>}
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
      <p className="mt-6 text-xs text-[var(--muted)]">Picked at random from every bounty ever made on poidh on Base (1 to 1478) and Arbitrum (1 to 334). Five more are loaded behind this one, so the button is instant.</p>
    </>
  );
}
