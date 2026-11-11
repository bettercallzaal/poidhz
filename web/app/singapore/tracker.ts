// Money tracker for the Singapore Congress crowdfund, across every platform.
// One row per SETTLED receipt, net of fees and refunds. Aggregates only: never a name, email,
// payment id, transaction hash or wallet. Add rows by PR; the page totals them.

export type Channel = 'poidh' | 'stripe' | 'paypal' | 'other';

export type Receipt = {
  date: string; // YYYY-MM-DD, the day the receipt settled
  channel: Channel;
  net_usd: number;
  note: string;
  ownerSeed?: true; // Zaal's own POIDH seed: shown, but never counted toward the goal (item 260)
};

// Zaal's own $100 POIDH seed sits ON TOP of the goal (misc item 260, supersedes item 124): once
// funded it is a row { date, channel: 'poidh', net_usd: 100, note: 'owner seed', ownerSeed: true },
// shown apart and left out of the total. The community raises the full $1,000.
export const GOAL_USD = 1000;

// The day the tracker opened; shown as the "updated" date until the first receipt lands.
export const TRACKER_OPENED = '2026-11-02';

export const RECEIPTS: Receipt[] = [
  // Zaal's word 2026-11-11: $100 on PayPal from one family. Settle date and fee not given; logged on the day he reported it.
  { date: '2026-11-11', channel: 'paypal', net_usd: 100, note: 'family backer' },
];

export const CHANNELS: { id: Channel; label: string }[] = [
  { id: 'poidh', label: 'POIDH' },
  { id: 'stripe', label: 'Stripe' },
  { id: 'paypal', label: 'PayPal' },
  { id: 'other', label: 'Other' },
];

const cents = (n: number) => Math.round(n * 100);

export function totals(receipts: Receipt[] = RECEIPTS) {
  const byChannel: Record<Channel, number> = { poidh: 0, stripe: 0, paypal: 0, other: 0 };
  let seed = 0;
  for (const r of receipts) {
    if (r.ownerSeed) seed += cents(r.net_usd);
    else byChannel[r.channel] += cents(r.net_usd);
  }
  const total = Object.values(byChannel).reduce((a, b) => a + b, 0);
  const updated = receipts.reduce((d, r) => (r.date > d ? r.date : d), TRACKER_OPENED);
  return {
    byChannel: Object.fromEntries(Object.entries(byChannel).map(([k, v]) => [k, v / 100])) as Record<Channel, number>,
    total: total / 100,
    seed: seed / 100,
    remaining: Math.max(0, GOAL_USD - total / 100),
    updated,
  };
}
