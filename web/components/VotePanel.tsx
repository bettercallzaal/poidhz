'use client';
import { useEffect, useState } from 'react';
import { toHex } from 'viem';
import { voteMessage, type Allocation } from '@/lib/vote';

type Entry = { claim: number; wallet: string; title: string; image: string | null; name: string | null; link: string | null };
type State = { bounty: number; open: boolean; storeReady: boolean; entries: Entry[]; tally: Allocation; votes: { address: string; allocation: Allocation }[] };
type You = { credits: number; ownClaims: number[]; current: Allocation | null };
type Eth = { request: (a: { method: string; params?: unknown[] }) => Promise<unknown> };

const short = (a: string) => `${a.slice(0, 6)}...${a.slice(-4)}`;

export function VotePanel({ heading, advisory }: { heading: string; advisory: string }) {
  const [s, setS] = useState<State | null>(null);
  const [addr, setAddr] = useState<string | null>(null);
  const [you, setYou] = useState<You | null>(null);
  const [alloc, setAlloc] = useState<Allocation>({});
  const [msg, setMsg] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const load = async (a?: string | null) => {
    const r = await fetch(`/api/vote${a ? `?address=${a}` : ''}`, { cache: 'no-store' });
    const d = await r.json();
    setS(d);
    if (d.you) { setYou(d.you); setAlloc(d.you.current ?? {}); }
  };
  useEffect(() => { load().catch(() => setMsg('Could not load the vote.')); }, []);

  const eth = (): Eth | null => (typeof window !== 'undefined' ? ((window as unknown as { ethereum?: Eth }).ethereum ?? null) : null);
  const connect = async () => {
    const e = eth();
    if (!e) { setMsg('No wallet found in this browser. Open this page in a browser with the wallet you claimed from (MetaMask, Coinbase Wallet, Rabby).'); return; }
    const [a] = (await e.request({ method: 'eth_requestAccounts' })) as string[];
    setAddr(a); setMsg(null); await load(a);
  };
  const used = Object.values(alloc).reduce((x, n) => x + n, 0);
  const bump = (c: number, d: number) => setAlloc((p) => ({ ...p, [c]: Math.max(0, (p[c] ?? 0) + d) }));
  const submit = async () => {
    if (!s || !addr) return;
    setBusy(true); setMsg(null);
    try {
      const message = voteMessage(s.bounty, alloc, new Date().toISOString());
      const signature = (await eth()!.request({ method: 'personal_sign', params: [toHex(message), addr] })) as string;
      const r = await fetch('/api/vote', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ address: addr, message, signature }) });
      const d = await r.json();
      setMsg(d.ok ? 'Vote recorded. You can change it until the pick is made.' : d.errors.join('. '));
      await load(addr);
    } catch (e) { setMsg(e instanceof Error ? e.message : 'Signing was cancelled.'); }
    setBusy(false);
  };

  if (!s) return null;
  const total = Object.values(s.tally).reduce((x, n) => x + n, 0);
  return (
    <section className="mt-6 rounded-lg border-2 border-[var(--accent)] p-4">
      <h2 className="text-2xl font-bold">{heading}</h2>
      <p className="mt-1 text-sm text-[var(--muted)]">{advisory} You get one vote for every ZAO bounty you have entered, and you cannot vote for your own entry. Sign with the wallet you claimed from.</p>
      {!s.storeReady && <p className="mt-2 text-sm text-[var(--warn)]">Voting is not switched on yet. The entries are below; check back shortly.</p>}
      {!s.open && <p className="mt-2 text-sm">Voting has closed. These are the final numbers.</p>}
      <ul className="mt-4 grid gap-3 sm:grid-cols-2">
        {s.entries.map((e) => {
          const t = s.tally[e.claim] ?? 0; const mine = you?.ownClaims.includes(e.claim);
          return (
            <li key={e.claim} className="rounded-lg border border-[var(--line)] p-3">
              {e.image && <img src={e.image} alt="" className="mb-2 max-h-40 w-full rounded object-cover" loading="lazy" />}
              <div className="text-sm font-semibold">{e.name ? `@${e.name}` : short(e.wallet)} <span className="font-normal text-[var(--muted)]">claim {e.claim}</span></div>
              <div className="text-sm">{e.title}</div>
              {e.link && <a href={e.link} target="_blank" rel="noopener ugc" className="text-sm">Watch it</a>}
              <div className="mt-2 h-2 rounded bg-[var(--line)]"><div className="h-2 rounded bg-[var(--accent)]" style={{ width: `${total ? (100 * t) / total : 0}%` }} /></div>
              <div className="mt-1 text-sm">{t} vote{t === 1 ? '' : 's'}</div>
              {addr && s.open && (mine ? <div className="mt-2 text-xs text-[var(--muted)]">Your entry</div> : (
                <div className="mt-2 flex items-center gap-2">
                  <button type="button" className="rounded border border-[var(--line)] px-3" onClick={() => bump(e.claim, -1)} disabled={!alloc[e.claim]}>-</button>
                  <span className="w-6 text-center">{alloc[e.claim] ?? 0}</span>
                  <button type="button" className="rounded border border-[var(--line)] px-3" onClick={() => bump(e.claim, 1)} disabled={!you || used >= you.credits}>+</button>
                </div>
              ))}
            </li>
          );
        })}
      </ul>
      {s.open && s.storeReady && (
        <div className="mt-4 flex flex-wrap items-center gap-3 text-sm">
          {!addr ? <button type="button" onClick={connect} className="rounded bg-[var(--accent)] px-4 py-2 font-semibold text-[var(--on-accent)]">Connect wallet to vote</button> : (
            <>
              <span>{short(addr)}: {you ? `${used} of ${you.credits} vote${you.credits === 1 ? '' : 's'} used` : 'checking...'}</span>
              <button type="button" onClick={submit} disabled={busy || !you || you.credits === 0 || used === 0} className="rounded bg-[var(--accent)] px-4 py-2 font-semibold text-[var(--on-accent)] disabled:opacity-40">{busy ? 'Signing...' : 'Sign and vote'}</button>
            </>
          )}
        </div>
      )}
      {msg && <p className="mt-2 text-sm">{msg}</p>}
      {s.votes.length > 0 && (
        <details className="mt-4 text-sm"><summary className="cursor-pointer">Every vote ({s.votes.length} wallet{s.votes.length === 1 ? '' : 's'})</summary>
          <ul className="mt-2 space-y-1">{s.votes.map((v) => <li key={v.address}><code>{short(v.address)}</code>: {Object.entries(v.allocation).filter(([, n]) => n > 0).map(([c, n]) => `claim ${c} x${n}`).join(', ')}</li>)}</ul>
        </details>
      )}
      <p className="mt-3 text-xs text-[var(--muted)]">Agents: GET /api/vote for the entries and the exact message to sign, then POST {'{address, message, signature}'} to /api/vote.</p>
    </section>
  );
}
