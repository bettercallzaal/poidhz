import { describe, it, expect } from 'vitest';
import { voteMessage, parseVoteMessage, checkVote, tally } from './vote';

const at = '2026-09-29T21:30:00.000Z';

describe('vote message', () => {
  const m = voteMessage(1418, { 8239: 2, 8240: 1 }, at);
  it('is fixed-format and human-readable', () => expect(m).toBe('poidhz community vote\nbounty: 1418\nvotes: 8239=2, 8240=1\nissued: 2026-09-29T21:30:00.000Z'));
  it('round-trips', () => expect(parseVoteMessage(m)).toEqual({ bounty: 1418, allocation: { 8239: 2, 8240: 1 }, issued: at }));
  it('drops zero allocations from the message', () => expect(voteMessage(1418, { 8239: 1, 8240: 0 }, at)).toContain('votes: 8239=1\n'));
  it('rejects a message that is not ours', () => expect(parseVoteMessage('hello')).toBeNull());
});

describe('checkVote', () => {
  const base = { bounty: 1418, allocation: { 8239: 2 }, credits: 3, ownClaims: [8341], validClaims: [8239, 8240, 8341], issued: at, now: new Date('2026-09-29T21:31:00Z'), previousIssued: null as string | null };
  it('a valid vote has no errors', () => expect(checkVote(base)).toEqual([]));
  it('no votes for your own entry', () => expect(checkVote({ ...base, allocation: { 8341: 1 } })).toContain('you cannot vote for your own entry (claim 8341)'));
  it('no more votes than you have', () => expect(checkVote({ ...base, allocation: { 8239: 2, 8240: 2 } })).toContain('4 votes used but you have 3'));
  it('a wallet with no past entries cannot vote', () => expect(checkVote({ ...base, credits: 0 })).toContain('this wallet has not entered a ZAO bounty, so it has no votes'));
  it('only entries in this round', () => expect(checkVote({ ...base, allocation: { 9999: 1 } })).toContain('claim 9999 is not an entry in this round'));
  it('whole positive numbers only', () => expect(checkVote({ ...base, allocation: { 8239: 1.5 } })).toContain('votes must be whole numbers'));
  it('an old signature is refused', () => expect(checkVote({ ...base, now: new Date('2026-09-29T22:00:00Z') })).toContain('this signature is more than 10 minutes old; sign again'));
  it('cannot replay an older vote over a newer one', () => expect(checkVote({ ...base, previousIssued: '2026-09-29T21:35:00.000Z' })).toContain('a newer vote from this wallet is already recorded'));
  it('must vote for something', () => expect(checkVote({ ...base, allocation: {} })).toContain('no votes in this ballot'));
});

describe('tally', () => {
  it('sums every wallet', () => expect(tally([{ allocation: { 8239: 2, 8240: 1 } }, { allocation: { 8239: 1 } }])).toEqual({ 8239: 3, 8240: 1 }));
});

import { creditsFor } from './vote';
describe('creditsFor', () => {
  const byBounty = { 1409: ['0xaa', '0xbb'], 1410: ['0xaa', '0xaa'], 1418: ['0xaa', '0xcc'] } as Record<number, string[]>;
  it('one vote per bounty entered, not per claim', () => expect(creditsFor('0xAA', byBounty)).toBe(3));
  it('a wallet that never entered has none', () => expect(creditsFor('0xdd', byBounty)).toBe(0));
});
