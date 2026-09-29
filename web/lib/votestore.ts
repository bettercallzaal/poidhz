import 'server-only';
import { Redis } from '@upstash/redis';
import type { Allocation } from './vote';

// Vercel's Upstash integration injects KV_REST_API_*; a direct Upstash setup uses UPSTASH_*.
const url = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const token = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
export const storeReady = Boolean(url && token);
const redis = storeReady ? new Redis({ url: url!, token: token! }) : null;

export type StoredVote = { address: string; allocation: Allocation; message: string; signature: string; issued: string; recorded_at: string };
const key = (bounty: number) => `vote:${bounty}`;

export async function getVotes(bounty: number): Promise<StoredVote[]> {
  if (!redis) return [];
  const h = (await redis.hgetall<Record<string, StoredVote | string>>(key(bounty))) ?? {};
  return Object.values(h).map((v) => (typeof v === 'string' ? (JSON.parse(v) as StoredVote) : v));
}

export async function getVote(bounty: number, address: string): Promise<StoredVote | null> {
  if (!redis) return null;
  const v = await redis.hget<StoredVote | string>(key(bounty), address.toLowerCase());
  return v == null ? null : typeof v === 'string' ? (JSON.parse(v) as StoredVote) : v;
}

export async function putVote(bounty: number, v: StoredVote): Promise<void> {
  if (!redis) throw new Error('vote storage is not connected');
  await redis.hset(key(bounty), { [v.address.toLowerCase()]: JSON.stringify(v) });
}
