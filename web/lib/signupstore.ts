import 'server-only';
import { Redis } from '@upstash/redis';
import type { Signup } from './signup';

// The same store the vote endpoint uses (votestore.ts). Vercel's Upstash integration injects
// KV_REST_API_*; a direct Upstash setup uses UPSTASH_*. Until one of them is set on the project
// storeReady is false and the route answers 503 instead of writing anywhere. The storage choice
// is round ten's open question Q4 (rounds/daily/d10/PLAN.md); this adapter is the one function
// to swap if the answer is not Upstash.
const url = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const token = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
export const storeReady = Boolean(url && token);
const redis = storeReady ? new Redis({ url: url!, token: token! }) : null;

// One hash per round, one field per song, so one song is one entry whoever submits it.
const key = (round: number) => `signup:d${round}`;

export async function countSignups(round: number): Promise<number | null> {
  if (!redis) return null;
  return redis.hlen(key(round));
}

export async function hasSignup(round: number, songId: string): Promise<boolean> {
  if (!redis) return false;
  return (await redis.hexists(key(round), songId)) === 1;
}

export async function putSignup(round: number, s: Signup): Promise<void> {
  if (!redis) throw new Error('sign-up storage is not connected');
  await redis.hset(key(round), { [s.song_id]: JSON.stringify(s) });
}
