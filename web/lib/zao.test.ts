import { describe, it, expect } from 'vitest';
import { mergeBounties } from './zao';
import type { Round } from './types';

const rounds: Round[] = [
  { round: 'daily-04', label: 'Daily 4', bounty_id: 1418, closes_at: '2026-09-27T17:00:00-04:00', status: 'OPEN', claims: 6, amount_usd: 13.3 },
  { round: '7', status: 'DRAFT' },
];
const list = { ours: [
  { id: 1446, title: 'Zaostock event', issuer: '0x2805e9dbce2839c5feae858723f9499f15fd88cf', amount_eth: 0.0115, created_at: '2026-09-27T20:11:51+00:00', status: 'open', has_claims: false, url: 'https://poidh.xyz/base/bounty/1446' },
  { id: 1418, title: 'ZAOstock Round 4', issuer: '0x7234', amount_eth: 0.005, created_at: '2026-09-26T00:00:00+00:00', status: 'open', has_claims: true, url: 'https://poidh.xyz/base/bounty/1418' },
  { id: 1151, title: 'Old round', issuer: '0x7234', amount_eth: 0.0105, created_at: '2026-04-01T00:00:00+00:00', status: 'closed', has_claims: true, url: 'https://poidh.xyz/base/bounty/1151' },
] };
const names = { '0x2805e9dbce2839c5feae858723f9499f15fd88cf': 'presdency.eth' };
const m = mergeBounties(rounds, list, names);
const by = (id: number) => m.find((r) => r.bounty_id === id)!;

describe('mergeBounties', () => {
  it('lists every ZAO bounty once, newest first, and no drafts', () => expect(m.map((r) => r.bounty_id)).toEqual([1446, 1418, 1151]));
  it('a round we track keeps its record', () => expect(by(1418)).toMatchObject({ label: 'Daily 4', claims: 6, closes_at: '2026-09-27T17:00:00-04:00' }));
  it('a bounty only on the list is still a full entry', () => expect(by(1446)).toMatchObject({ title: 'Zaostock event', status: 'OPEN', claims: 0, cast_by: 'presdency.eth' }));
  it('a closed list-only bounty is closed, not open', () => expect(by(1151).status).toBe('CLOSED'));
  it('a list-only bounty with entries has an unknown count, not zero', () => expect(by(1151).claims).toBeNull());
  it('with no list file the tracked rounds still show', () => expect(mergeBounties(rounds, null, {}).map((r) => r.bounty_id)).toEqual([1418]));
});
