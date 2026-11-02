import type { Metadata } from 'next';
import { PAYPAL_LINK, POIDH_BOUNTY_URL, QUESTION_URL, STRIPE_LINK } from './links';
import { CHANNELS, GOAL_USD, totals } from './tracker';

export const metadata: Metadata = {
  title: 'Singapore Congress crowdfund - poidhz',
  description: 'Help Zaal travel to the 13th World Zoroastrian Congress in Singapore as a youth delegate. $1,000 community goal, tracked across every platform.',
};

const usd = (n: number) => `$${n.toLocaleString('en-US', { minimumFractionDigits: Number.isInteger(n) ? 0 : 2, maximumFractionDigits: 2 })}`;
const day = (ymd: string) => new Date(`${ymd}T12:00:00Z`).toLocaleDateString('en-US', { timeZone: 'UTC', dateStyle: 'medium' });

const START: [string, string, string][] = [
  ['Estimated travel cost', '$2,200', 'Flights already purchased'],
  ['Set aside myself', '$900', 'Not part of the goal'],
  ['Support before this fundraiser', '$200', 'Not part of the goal'],
  ['My POIDH bounty seed', '$100', 'Planned, separate from the goal'],
  ['New community support', '$1,000 net', 'The goal, counted after fees and refunds'],
];

function Button({ href, children }: { href: string; children: React.ReactNode }) {
  return <a href={href} target="_blank" rel="noopener" className="inline-block rounded-lg bg-[var(--accent)] px-4 py-2 font-semibold text-[var(--on-accent)] no-underline">{children}</a>;
}

export default function Singapore() {
  const t = totals();
  const pay = [
    { href: STRIPE_LINK, label: 'Back with card (Stripe)' },
    { href: PAYPAL_LINK, label: 'Back with PayPal' },
    { href: POIDH_BOUNTY_URL, label: 'Back the POIDH bounty' },
  ].filter((b) => b.href);
  return (
    <>
      <h1 className="mt-6 text-3xl font-bold tracking-tight">Help bring the World Zoroastrian Congress back to our community</h1>
      <p className="mt-3 max-w-2xl">I&apos;m attending the 13th World Zoroastrian Congress in Singapore as a youth delegate. My youth subsidy covers the hotel, registration and meals, but not the flights. My travel cost is about $2,200, and the flights have already been purchased.</p>
      <p className="mt-3 max-w-2xl">I have $900 set aside and received $200 in support before opening this fundraiser. I&apos;m asking the community for $1,000 in net travel support. I also plan to contribute $100 of my own to start the POIDH bounty; that seed is separate from the community goal.</p>

      <h2 className="mt-8 text-xl font-semibold">Raised so far</h2>
      <p className="mt-2 text-2xl font-bold">{usd(t.total)} of {usd(GOAL_USD)} raised so far</p>
      <p className="text-sm text-[var(--muted)]">Updated {day(t.updated)}. Settled support across every platform, after fees and refunds.</p>
      <ul className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
        {CHANNELS.map((c) => (
          <li key={c.id} className="rounded-lg border border-[var(--line)] p-3"><span className="block text-sm text-[var(--muted)]">{c.label}</span><span className="font-semibold">{usd(t.byChannel[c.id])}</span></li>
        ))}
      </ul>

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
      <p className="mt-2 text-sm text-[var(--muted)]">$900 + $200 + $100 + $1,000 = $2,200.</p>

      <h2 className="mt-8 text-xl font-semibold">What you get</h2>
      <p className="mt-2 max-w-2xl">Back this trip and send me a question about Zoroastrianism, and I&apos;ll make a piece of content answering it. If no questions come in, I&apos;ll make one piece of content about Zoroastrianism and credit it to everyone who crowdfunded this trip.</p>
      {QUESTION_URL && <p className="mt-3"><Button href={QUESTION_URL}>Send a question</Button></p>}

      <h2 className="mt-8 text-xl font-semibold">How to back</h2>
      <p className="mt-2 max-w-2xl">Give $25, $50, $100, or another amount. These are examples, not reward tiers.</p>
      {pay.length > 0 && <div className="mt-3 flex flex-wrap gap-3">{pay.map((b) => <Button key={b.label} href={b.href}>{b.label}</Button>)}</div>}

      <h2 className="mt-8 text-xl font-semibold">Updates</h2>
      <p className="mt-2 max-w-2xl">While the fundraiser is open I&apos;ll update the total on this page each week. During the Congress I&apos;ll share a short dispatch each day, and one recap after the trip.</p>

      <p className="mt-8 text-xs text-[var(--muted)]">This is personal travel support. Contributions are not tax-deductible.</p>
    </>
  );
}
