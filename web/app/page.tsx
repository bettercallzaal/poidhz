import Link from 'next/link';
import { loadAll, sources } from '@/lib/load';
import { publicRounds, roundPhase } from '@/lib/rounds';
import { countText, potText, roundName } from '@/lib/format';
import { PhaseBadge } from '@/components/PhaseBadge';
import { VotePanel } from '@/components/VotePanel';
import type { Phase, Round } from '@/lib/types';

// Phase is computed from the clock; a cached render would show a closed round as open.
export const dynamic = 'force-dynamic';

type Item = { r: Round; phase: Phase };
const et = (iso: string, opts: Intl.DateTimeFormatOptions) => new Date(iso).toLocaleString('en-US', { timeZone: 'America/New_York', ...opts });

function Row({ x }: { x: Item }) {
  return (
    <li className="rounded-lg border border-[var(--line)] p-4">
      <div className="flex flex-wrap items-center gap-2"><PhaseBadge phase={x.phase} /><span className="text-sm text-[var(--muted)]">{roundName(x.r)}{x.r.cast_by && x.r.cast_by !== 'bettercallzaal' ? ` - cast by @${x.r.cast_by}` : ''}</span></div>
      <Link href={`/b/${x.r.bounty_id}`} className="mt-1 block text-lg font-semibold">{x.r.bounty_title || x.r.title}</Link>
      <p className="text-sm text-[var(--muted)]">Pot {potText(x.r)} - {countText(x.r.claims)} entries{x.r.closes_at ? ` - closes ${et(x.r.closes_at, { dateStyle: 'medium', timeStyle: 'short' })} ET` : ''}{x.r.winner?.handle ? ` - won by @${x.r.winner.handle}` : ''}</p>
    </li>
  );
}

export default async function Board() {
  const { rounds, roundsAsOf, listAsOf } = await loadAll();
  const now = new Date();
  const rs: Item[] = publicRounds(rounds).map((r) => ({ r, phase: roundPhase(r, now) }));
  const open = rs.filter((x) => x.phase === 'open');
  const waiting = rs.filter((x) => x.phase === 'awaiting-pick');
  const paid = rs.filter((x) => x.phase === 'won').length;
  return (
    <>
      <h1 className="mt-6 text-3xl font-bold tracking-tight">The ZAO bounty board</h1>
      <p className="mt-2 max-w-2xl text-[var(--muted)]">Paid bounties on poidh. Judged in public. Everyone who enters gets written notes. Agents welcome. Talk about any of it in <a href={`https://farcaster.xyz/~/channel/${sources.channel}`}>/{sources.channel}</a>.</p>
      {(sources as { vote?: { heading: string; advisory: string } }).vote && <VotePanel heading={(sources as { vote: { heading: string } }).vote.heading} advisory={(sources as { vote: { advisory: string } }).vote.advisory} />}
      <h2 className="mt-8 text-xl font-semibold">Open now</h2>
      {open.length ? <ul className="mt-3 grid gap-3">{open.map((x) => <Row key={x.r.bounty_id} x={x} />)}</ul> : <p className="mt-2">Nothing open right now.</p>}
      {waiting.length > 0 && <><h2 className="mt-8 text-xl font-semibold">Closed, being judged</h2><ul className="mt-3 grid gap-3">{waiting.map((x) => <Row key={x.r.bounty_id} x={x} />)}</ul></>}
      <h2 className="mt-10 text-xl font-semibold">Every ZAO bounty</h2>
      <p className="mt-1 text-sm text-[var(--muted)]">{rs.length} bounties on poidh so far, {paid} with a winner picked. Newest first.</p>
      <div className="mt-3 overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="text-[var(--muted)]"><tr><th className="py-2 pr-3 font-medium">Cast</th><th className="py-2 pr-3 font-medium">Bounty</th><th className="py-2 pr-3 font-medium">Pot</th><th className="py-2 pr-3 font-medium">Entries</th><th className="py-2 font-medium">Status</th></tr></thead>
          <tbody>
            {rs.map((x) => (
              <tr key={x.r.bounty_id} className="border-t border-[var(--line)] align-top">
                <td className="py-2 pr-3 whitespace-nowrap text-[var(--muted)]">{x.r.created_at ? et(x.r.created_at, { dateStyle: 'medium' }) : 'UNKNOWN'}</td>
                <td className="py-2 pr-3"><Link href={`/b/${x.r.bounty_id}`}>{x.r.bounty_title || x.r.title}</Link>{x.r.cast_by && x.r.cast_by !== 'bettercallzaal' ? <span className="text-[var(--muted)]"> - @{x.r.cast_by}</span> : null}{x.r.winner?.handle ? <span className="text-[var(--muted)]"> - won by @{x.r.winner.handle}</span> : null}</td>
                <td className="py-2 pr-3 whitespace-nowrap">{potText(x.r)}</td>
                <td className="py-2 pr-3">{countText(x.r.claims)}</td>
                <td className="py-2"><PhaseBadge phase={x.phase} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-8 text-xs text-[var(--muted)]">Round records as of {roundsAsOf}{listAsOf ? `; full poidh scan as of ${listAsOf}` : '; the full poidh scan has not run, so only tracked rounds are listed'}. Machine-readable: <a href="/rounds.json">/rounds.json</a>, <a href="/llms.txt">/llms.txt</a>.</p>
    </>
  );
}
