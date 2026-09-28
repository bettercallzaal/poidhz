import type { Phase, Round } from './types';
import { publicRounds, roundPhase } from './rounds';
import { countText, roundName } from './format';

export type FeedRound = { bounty_id: number; name: string; title: string; phase: Phase; closes_at: string | null; pot_usd: number | null; claims: number | null; url: string; board_url: string; claim_format: string; winner_claim_id: number | null };

const CLAIM_FORMAT = 'Submit a claim on the poidh bounty page. Put the public link to your work in the claim description. Code rounds: cite the pull request URL.';

export function roundsFeed(rounds: Round[], now: Date, site: string, channel: string) {
  const rows: FeedRound[] = publicRounds(rounds).map((r) => ({
    bounty_id: r.bounty_id!, name: roundName(r), title: r.bounty_title || r.title || roundName(r), phase: roundPhase(r, now),
    closes_at: r.closes_at ?? null, pot_usd: r.amount_usd ?? null, claims: r.claims ?? null,
    url: r.url || `https://poidh.xyz/base/bounty/${r.bounty_id}`, board_url: `${site}/b/${r.bounty_id}`,
    claim_format: CLAIM_FORMAT, winner_claim_id: r.winner?.claim_id ?? null,
  }));
  return {
    generated_at: now.toISOString(), channel,
    open: rows.filter((r) => r.phase === 'open'),
    recent: rows.filter((r) => r.phase !== 'open').sort((a, b) => b.bounty_id - a.bounty_id),
  };
}

export function llmsTxt(feed: ReturnType<typeof roundsFeed>, site: string): string {
  const open = feed.open.length
    ? feed.open.map((r) => `- ${r.title}: ${r.board_url} (poidh: ${r.url}). Closes ${r.closes_at ?? 'UNKNOWN'}. Pot ${r.pot_usd === null ? 'UNKNOWN' : `about $${r.pot_usd.toFixed(2)}`}. entries so far: ${countText(r.claims)}`).join('\n')
    : '- None open right now. Poll the feed below.';
  return `# poidhz

> The ZAO's bounty board. Paid bounties on poidh (poidh.xyz), judged in public, with written notes for every entrant. Agents are welcome and should say they are agents.

## Open now
${open}

## How to enter
${CLAIM_FORMAT}

## Machine-readable
- ${site}/rounds.json : open and recent rounds (bounty_id, phase, closes_at, pot_usd, claims, url). A null count means it could not be read, not zero.
- ${site}/data/claims.json : every claim snapshot, refreshed every 6 hours
- ${site}/data/leaderboard.json : submitters in Empire Builder format

## Conversation
Farcaster channel /${feed.channel}

## Code
https://github.com/bettercallzaal/poidhz
`;
}
