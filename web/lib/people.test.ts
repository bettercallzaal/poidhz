import { describe, it, expect } from 'vitest';
import fb from '../test/fixtures/feedback-d03.json';
import lb from '../test/fixtures/leaderboard.json';
import { notesFrom } from './feedback';
import { buildPeople, findPerson } from './people';
import type { Claim } from './types';

const c = (claim_id: number, bounty_id: number, wallet: string, handle: string | null = null): Claim =>
  ({ claim_id, bounty_id, wallet, handle, title: 't', description: 'd', image_url: null, accepted: false });

const claims = [
  c(8153, 1412, '0xbbb0000000000000000000000000000000000002'),
  c(8149, 1412, '0x5dc697f2799bd232cad2d479c379ff305b699f9b'),
  c(8150, 1412, '0x5dc697f2799bd232cad2d479c379ff305b699f9b'),
  c(8093, 1409, '0x5dc697f2799bd232cad2d479c379ff305b699f9b'),
  c(8338, 1421, '0x5a844e7871e0cd7dcf080046e3c17d0c637cd58b'),
];
const winners = [{ claim_id: 8149, handle: 'pascaline', wallet: '0x5dc697f2799bd232cad2d479c379ff305b699f9b' }];
const people = buildPeople(claims, lb, notesFrom([fb]), winners);

describe('people', () => {
  it('notes attach by claim id even when filed under another handle', () => {
    const p = findPerson(people, 'defifa')!;
    expect(p.notes.map((n) => n.claim)).toEqual([8153]);
  });
  it('rounds entered counts bounties, not claims', () => expect(findPerson(people, 'pascaline')!.bounties).toEqual([1409, 1412]));
  it('wins by claim id', () => expect(findPerson(people, 'pascaline')!.wins).toEqual([1412]));
  it('no handle means keyed by lowercase wallet, found case-insensitively', () => {
    const p = findPerson(people, '0x5A844E7871E0CD7DCF080046E3C17D0C637CD58B')!;
    expect(p.key).toBe('0x5a844e7871e0cd7dcf080046e3c17d0c637cd58b');
    expect(p.handle).toBeNull();
  });
  it('unknown key is undefined', () => expect(findPerson(people, 'nobody')).toBeUndefined());
  it('handle from the live claim beats nothing', () => {
    const ps = buildPeople([c(1, 1, '0xddd', 'assay')], [], new Map(), []);
    expect(ps[0].key).toBe('assay');
  });
});
