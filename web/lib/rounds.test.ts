import { describe, it, expect } from 'vitest';
import fx from '../test/fixtures/rounds-live.json';
import { roundPhase, publicRounds, personBountyIds } from './rounds';
import { countText, shortAddr, usd } from './format';
import type { Round } from './types';

const rs = fx.rounds as Round[];
const now = new Date('2026-09-28T15:37:00Z');
const by = (id: number) => rs.find((r) => r.bounty_id === id)!;

describe('roundPhase', () => {
  it('open before close', () => expect(roundPhase(by(1421), now)).toBe('open'));
  it('past close with chain still OPEN is awaiting pick, not open', () => expect(roundPhase(by(1418), now)).toBe('awaiting-pick'));
  it('winner set is won', () => expect(roundPhase(by(1412), now)).toBe('won'));
  it('canceled stays canceled', () => expect(roundPhase(by(1249), now)).toBe('canceled'));
  it('OPEN with no closes_at is open', () => expect(roundPhase({ status: 'OPEN', round: 'x', bounty_id: 1 }, now)).toBe('open'));
});

describe('publicRounds', () => {
  it('drops drafts', () => expect(publicRounds(rs).map((r) => r.bounty_id)).toEqual([1249, 1412, 1418, 1421]));
});

describe('format', () => {
  it('unknown count is UNKNOWN, never 0', () => { expect(countText(null)).toBe('UNKNOWN'); expect(countText(undefined)).toBe('UNKNOWN'); expect(countText(0)).toBe('0'); });
  it('shortAddr', () => expect(shortAddr('0x5dc697f2799bd232cad2d479c379ff305b699f9b')).toBe('0x5dc6...9f9b'));
  it('usd', () => { expect(usd(13.2706)).toBe('$13.27'); expect(usd(null)).toBe('UNKNOWN'); });
});

describe('personBountyIds', () => {
  it('includes canceled rounds so their entrants still have pages', () => expect(personBountyIds(rs)).toEqual([1249, 1412, 1418, 1421]));
});
