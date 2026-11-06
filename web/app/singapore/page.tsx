import type { Metadata } from 'next';
import { PAYPAL_LINK, POIDH_BOUNTY_ID, POIDH_BOUNTY_URL, POIDH_LAST_KNOWN, POIDH_SEED_ETH, QUESTION_URL, STRIPE_LINK, STRIPE_REQUEST_URL } from './links';
import { communityShare, loadPot } from '@/lib/poidh-pot';
import { CURIOUS, FUN_FACTS, FUN_FACTS_INTRO, INTERVIEW_INTRO, INTERVIEW_PARTS, PITCH, SOURCES, SOURCES_NOTE, STORY_BLOCKS, WHAT_YOU_GET } from './intro';
import { STORY, STORY_HEADING } from './story';
import { CHANNELS, GOAL_USD, totals } from './tracker';

export const metadata: Metadata = {
  title: 'Singapore Congress crowdfund - poidhz',
  description: 'Help Zaal travel to the 13th World Zoroastrian Congress in Singapore as a youth delegate. $1,000 goal, tracked across every platform.',
};

export const revalidate = 300;

const usd = (n: number) => `$${n.toLocaleString('en-US', { minimumFractionDigits: Number.isInteger(n) ? 0 : 2, maximumFractionDigits: 2 })}`;
const day = (ymd: string) => new Date(`${ymd}T12:00:00Z`).toLocaleDateString('en-US', { timeZone: 'UTC', dateStyle: 'medium' });

const START: [string, string, string][] = [
  ['Estimated travel cost', '$2,200', 'Flights already bought; this pays them back'],
  ['Set aside by me and my family', '$900', 'Not part of the goal'],
  ['Support before this fundraiser', '$200', 'Not part of the goal'],
  ['My POIDH seed', '$100', 'Not part of the goal; I fund it when I cast the bounty'],
  ['Goal, from the community', '$1,000', 'Counted after fees and refunds'],
];

function Button({ href, children }: { href: string; children: React.ReactNode }) {
  return <a href={href} target="_blank" rel="noopener" className="inline-block rounded-lg bg-[var(--accent)] px-4 py-2 font-semibold text-[var(--on-accent)] no-underline">{children}</a>;
}

export default async function Singapore() {
  const t = totals();
  const pot = await loadPot(POIDH_BOUNTY_ID, POIDH_LAST_KNOWN);
  // The live pot includes Zaal's own seed, which sits on top of the goal (misc item 260): subtract it.
  const seedEth = POIDH_SEED_ETH ?? 0;
  const share = pot ? communityShare(pot, seedEth) : null;
  const communityEth = share?.eth ?? 0;
  const poidhUsd = share?.usd ?? null;
  const total = poidhUsd != null ? Math.round((t.total - t.byChannel.poidh + poidhUsd) * 100) / 100 : t.total;
  const tile = (id: string) =>
    id === 'poidh' && pot ? `${communityEth.toFixed(4)} ETH${poidhUsd != null ? ` (about ${usd(poidhUsd)})` : ''}` : usd(t.byChannel[id as keyof typeof t.byChannel]);
  const pay = [
    { href: STRIPE_LINK, label: 'Back with card (Stripe)' },
    { href: PAYPAL_LINK, label: 'Back with PayPal' },
    { href: POIDH_BOUNTY_URL, label: 'Back the POIDH bounty' },
  ].filter((b) => b.href);
  return (
    <>
      <h1 className="mt-6 text-3xl font-bold tracking-tight">Help bring the World Zoroastrian Congress back to our community</h1>
      <p className="mt-3 max-w-2xl text-lg font-semibold">{PITCH}</p>
      {STORY_BLOCKS.map((m) => (
        <div key={m.text.slice(0, 40)} className="mt-4 max-w-2xl">
          <p>{m.text}{m.link && <> <a className="underline" href={m.link.href} target="_blank" rel="noopener">{m.link.label}</a></>}</p>
          {m.images && (
            <div className={`mt-2 grid gap-2 ${m.images.length > 1 ? 'grid-cols-1 sm:grid-cols-3' : 'max-w-sm grid-cols-1'}`}>
              {m.images.map((im) => (
                // eslint-disable-next-line @next/next/no-img-element
                <img key={im.src} src={im.src} alt={im.alt} loading="lazy" className="w-full rounded-lg border border-[var(--line)]" />
              ))}
            </div>
          )}
        </div>
      ))}

      <h2 className="mt-8 text-xl font-semibold">Raised so far</h2>
      <p className="mt-2 text-2xl font-bold">{poidhUsd != null ? 'About ' : ''}{usd(total)} of {usd(GOAL_USD)} raised so far</p>
      {pot && seedEth > 0 && <p className="text-sm text-[var(--muted)]">Plus my own {seedEth} ETH POIDH seed, on top of the goal and not counted in it.</p>}
      {!pot && t.seed > 0 && <p className="text-sm text-[var(--muted)]">Plus my own {usd(t.seed)} POIDH seed, on top of the goal.</p>}
      <p className="text-sm text-[var(--muted)]">Updated {day(t.updated)}. Settled support across every platform, after fees and refunds.</p>
      <ul className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
        {CHANNELS.map((c) => (
          <li key={c.id} className="rounded-lg border border-[var(--line)] p-3"><span className="block text-sm text-[var(--muted)]">{c.label}</span><span className="font-semibold">{tile(c.id)}</span></li>
        ))}
      </ul>
      {pot && (
        <p className="mt-2 text-sm text-[var(--muted)]">
          {pot.source === 'live' ? 'POIDH updates on its own from the live bounty.' : `POIDH as last seen on ${day(pot.asOf!)}; the live bounty could not be read.`}
          {pot.usd != null && ' Its dollar figure is approximate, at the current ETH price.'}
        </p>
      )}

      <h2 className="mt-8 text-xl font-semibold">How to back</h2>
      <p className="mt-2 max-w-2xl">Give $25, $50, $100, or another amount. These are examples, not reward tiers.</p>
      {pay.length > 0 && <div className="mt-3 flex flex-wrap gap-3">{pay.map((b) => <Button key={b.label} href={b.href}>{b.label}</Button>)}</div>}
      {!POIDH_BOUNTY_URL && <p className="mt-3 max-w-2xl">The POIDH bounty link goes here when it is live.</p>}
      <p className="mt-3 max-w-2xl">You can also send crypto directly to <span className="font-mono">zaal.eth</span>.</p>
      <p className="mt-3 max-w-2xl">If you need a Stripe link, I can provide one. <a className="underline" href={STRIPE_REQUEST_URL}>Email me</a> and I&apos;ll send it.</p>

      <h2 className="mt-8 text-xl font-semibold">Where the trip stands</h2>
      <div className="mt-3 overflow-x-auto">
        <table className="w-full text-left text-sm">
          <tbody>
            {START.map(([item, amount, note]) => (
              <tr key={item} className="border-t border-[var(--line)] align-top">
                <td className="py-2 pr-3">{item}</td>
                <td className="py-2 pr-3 whitespace-nowrap font-semibold">{amount}</td>
                <td className="py-2 text-[var(--muted)]">{note}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2 className="mt-8 text-xl font-semibold">{STORY_HEADING}</h2>
      {STORY.map((p) => <p key={p.slice(0, 40)} className="mt-3 max-w-2xl">{p}</p>)}

      <h2 className="mt-8 text-xl font-semibold">Fun facts to get you asking</h2>
      <p className="mt-2 max-w-2xl">{FUN_FACTS_INTRO}</p>
      <ul className="mt-2 max-w-2xl list-disc pl-6">{FUN_FACTS.map((f) => <li key={f.slice(0, 40)} className="mt-1">{f}</li>)}</ul>
      <p className="mt-3 max-w-2xl">{INTERVIEW_INTRO}</p>
      <ul className="mt-1 max-w-2xl list-disc pl-6">{INTERVIEW_PARTS.map((x) => <li key={x.href}><a className="underline" href={x.href} target="_blank" rel="noopener">{x.label}</a></li>)}</ul>
      <p className="mt-3 max-w-2xl">{CURIOUS}</p>

      <h2 className="mt-8 text-xl font-semibold">What you get</h2>
      <p className="mt-2 max-w-2xl">{WHAT_YOU_GET}</p>
      {QUESTION_URL && <p className="mt-3"><Button href={QUESTION_URL}>Send a question</Button></p>}
      {POIDH_BOUNTY_URL && <p className="mt-3 max-w-2xl">If you have a suggestion, you can also comment it on the <a href={POIDH_BOUNTY_URL} target="_blank" rel="noopener">POIDH bounty</a>, and as long as it&apos;s reasonable I&apos;ll make sure to try and make it happen.</p>}

      <h2 className="mt-8 text-xl font-semibold">Updates</h2>
      <p className="mt-2 max-w-2xl">While the fundraiser is open I&apos;ll update the total on this page each week. During the Congress I&apos;ll share as much content as I can, fueled by the questions people send me. I&apos;ll probably keep this open until even after the Congress, because I need the support to be able to take a trip like this.</p>

      <h2 className="mt-8 text-xl font-semibold">Sources</h2>
      <p className="mt-2 max-w-2xl text-sm">{SOURCES_NOTE}</p>
      <ul className="mt-2 max-w-2xl text-sm">{SOURCES.map((s) => <li key={s.text.slice(0, 24)} className="mt-1">{s.text}{s.href && <> <a className="underline break-all" href={s.href} target="_blank" rel="noopener">{s.href}</a></>}</li>)}</ul>

      <p className="mt-8 text-xs text-[var(--muted)]">This is personal travel support. Contributions are not tax-deductible.</p>
    </>
  );
}
