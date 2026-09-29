// Community vote on a round's entries. Advisory: the round's own text says Zaal picks.
// One vote per ZAO bounty a wallet has claimed on; nobody votes for their own entry.
export type Allocation = Record<number, number>;

const HEAD = 'poidhz community vote';
const MAX_AGE_MS = 10 * 60 * 1000;

export function voteMessage(bounty: number, allocation: Allocation, issued: string): string {
  const votes = Object.entries(allocation)
    .filter(([, n]) => n > 0)
    .sort(([a], [b]) => Number(a) - Number(b))
    .map(([c, n]) => `${c}=${n}`)
    .join(', ');
  return `${HEAD}\nbounty: ${bounty}\nvotes: ${votes}\nissued: ${issued}`;
}

export function parseVoteMessage(m: string): { bounty: number; allocation: Allocation; issued: string } | null {
  const x = m.match(/^poidhz community vote\nbounty: (\d+)\nvotes: ([0-9=, ]*)\nissued: (\S+)$/);
  if (!x) return null;
  const allocation: Allocation = {};
  for (const part of x[2].split(',').map((s) => s.trim()).filter(Boolean)) {
    const [c, n] = part.split('=').map(Number);
    if (!Number.isFinite(c) || !Number.isFinite(n)) return null;
    allocation[c] = n;
  }
  return { bounty: Number(x[1]), allocation, issued: x[3] };
}

export type VoteCheck = {
  bounty: number; allocation: Allocation; credits: number; ownClaims: number[]; validClaims: number[];
  issued: string; now: Date; previousIssued: string | null;
};

export function checkVote(v: VoteCheck): string[] {
  const errs: string[] = [];
  const entries = Object.entries(v.allocation).map(([c, n]) => [Number(c), n] as const);
  const used = entries.reduce((s, [, n]) => s + (Number.isFinite(n) ? n : 0), 0);
  if (v.credits <= 0) errs.push('this wallet has not entered a ZAO bounty, so it has no votes');
  if (entries.length === 0 || used === 0) errs.push('no votes in this ballot');
  for (const [c, n] of entries) {
    if (!Number.isInteger(n) || n < 0) errs.push('votes must be whole numbers');
    if (v.ownClaims.includes(c) && n > 0) errs.push(`you cannot vote for your own entry (claim ${c})`);
    if (!v.validClaims.includes(c)) errs.push(`claim ${c} is not an entry in this round`);
  }
  if (v.credits > 0 && used > v.credits) errs.push(`${used} votes used but you have ${v.credits}`);
  const t = Date.parse(v.issued);
  if (!Number.isFinite(t) || v.now.getTime() - t > MAX_AGE_MS || t - v.now.getTime() > 60_000) errs.push('this signature is more than 10 minutes old; sign again');
  if (v.previousIssued && Date.parse(v.previousIssued) >= t) errs.push('a newer vote from this wallet is already recorded');
  return [...new Set(errs)];
}

export function tally(votes: { allocation: Allocation }[]): Allocation {
  const out: Allocation = {};
  for (const v of votes) for (const [c, n] of Object.entries(v.allocation)) out[Number(c)] = (out[Number(c)] ?? 0) + n;
  return out;
}

// Votes = the number of distinct ZAO bounties this wallet has claimed on.
export function creditsFor(wallet: string, walletsByBounty: Record<number, string[]>): number {
  const w = wallet.toLowerCase();
  return Object.values(walletsByBounty).filter((ws) => ws.some((x) => x.toLowerCase() === w)).length;
}
