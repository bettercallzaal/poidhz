import Link from 'next/link';
import { loadAll, sources } from '@/lib/load';
import { publicRounds, roundPhase } from '@/lib/rounds';
import { countText, roundName, usd } from '@/lib/format';
import { PhaseBadge } from '@/components/PhaseBadge';
import type { Phase, Round } from '@/lib/types';

export const revalidate = 300;

type Item = { r: Round; phase: Phase };

function Row({ x }: { x: Item }) {
  return (
    <li className="rounded-lg border border-[var(--line)] p-4">
      <div className="flex flex-wrap items-center gap-2"><PhaseBadge phase={x.phase} /><span className="text-sm text-[var(--muted)]">{roundName(x.r)}</span></div>
      <Link href={`/b/${x.r.bounty_id}`} className="mt-1 block text-lg font-semibold">{x.r.bounty_title || x.r.title}</Link>
      <p className="text-sm text-[var(--muted)]">Pot {usd(x.r.amount_usd)} - {countText(x.r.claims)} entries{x.r.closes_at ? ` - closes ${new Date(x.r.closes_at).toLocaleString('en-US', { timeZone: 'America/New_York', dateStyle: 'medium', timeStyle: 'short' })} ET` : ''}{x.r.winner?.handle ? ` - won by @${x.r.winner.handle}` : ''}</p>
    </li>
  );
}

export default async function Board() {
  const { rounds, roundsAsOf } = await loadAll();
  const now = new Date();
  const rs: Item[] = publicRounds(rounds).map((r) => ({ r, phase: roundPhase(r, now) }));
  const open = rs.filter((x) => x.phase === 'open');
  const waiting = rs.filter((x) => x.phase === 'awaiting-pick');
  const done = rs.filter((x) => x.phase === 'won' || x.phase === 'canceled').reverse();
  return (
    <>
      <h1 className="mt-6 text-3xl font-bold tracking-tight">The ZAO bounty board</h1>
      <p className="mt-2 max-w-2xl text-[var(--muted)]">Paid bounties on poidh. Judged in public. Everyone who enters gets written notes. Agents welcome. Talk about any of it in <a href={`https://farcaster.xyz/~/channel/${sources.channel}`}>/{sources.channel}</a>.</p>
      <h2 className="mt-8 text-xl font-semibold">Open now</h2>
      {open.length ? <ul className="mt-3 grid gap-3">{open.map((x) => <Row key={x.r.bounty_id} x={x} />)}</ul> : <p className="mt-2">Nothing open right now.</p>}
      {waiting.length > 0 && <><h2 className="mt-8 text-xl font-semibold">Closed, being judged</h2><ul className="mt-3 grid gap-3">{waiting.map((x) => <Row key={x.r.bounty_id} x={x} />)}</ul></>}
      <h2 className="mt-8 text-xl font-semibold">Past rounds</h2>
      <ul className="mt-3 grid gap-3">{done.map((x) => <Row key={x.r.bounty_id} x={x} />)}</ul>
      <p className="mt-8 text-xs text-[var(--muted)]">Round data as of {roundsAsOf}. Machine-readable: <a href="/rounds.json">/rounds.json</a>, <a href="/llms.txt">/llms.txt</a>.</p>
    </>
  );
}
