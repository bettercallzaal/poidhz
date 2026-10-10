import 'server-only';
import type { Signup } from './signup';

// Where a sign-up goes. Zaal ruled (item 111, 10 Oct 2026): "Hurricane gets it on his database",
// so rows are forwarded to an endpoint hurric4n3ike provides on the WaveZStation side, and
// nothing is kept on poidhz.com. Until SIGNUP_ENDPOINT is set on the Vercel project storeReady is
// false and the route answers 503 without sending anything anywhere. This file is the one
// function to change if the endpoint's shape differs from the note in rounds/daily/d10/HURRICANE-NOTE.md.
const endpoint = process.env.SIGNUP_ENDPOINT;
const token = process.env.SIGNUP_TOKEN;
export const storeReady = Boolean(endpoint);

const headers = () => ({ 'content-type': 'application/json', accept: 'application/json', ...(token ? { authorization: `Bearer ${token}` } : {}) });

export type PutResult = { ok: true; count: number | null } | { ok: false; status: number; errors: string[] };

// The endpoint owns the one-entry-per-song rule and answers 409 for a repeat.
export async function putSignup(round: number, s: Signup): Promise<PutResult> {
  if (!endpoint) return { ok: false, status: 503, errors: ['sign-up is not switched on yet; nothing was stored'] };
  try {
    const r = await fetch(endpoint, { method: 'POST', headers: headers(), body: JSON.stringify({ round, ...s }), signal: AbortSignal.timeout(8000) });
    const j = (await r.json().catch(() => ({}))) as { ok?: boolean; count?: number; errors?: string[] };
    if (!r.ok || j.ok === false) return { ok: false, status: r.status === 409 ? 409 : 502, errors: j.errors?.length ? j.errors : [r.status === 409 ? 'that song is already signed up' : `the sign-up database answered ${r.status}; nothing was stored`] };
    return { ok: true, count: typeof j.count === 'number' ? j.count : null };
  } catch {
    return { ok: false, status: 502, errors: ['could not reach the sign-up database; nothing was stored, try again in a minute'] };
  }
}

export async function countSignups(round: number): Promise<number | null> {
  if (!endpoint) return null;
  try {
    const r = await fetch(`${endpoint}?round=${round}`, { headers: headers(), signal: AbortSignal.timeout(5000) });
    const j = (await r.json().catch(() => ({}))) as { count?: number };
    return r.ok && typeof j.count === 'number' ? j.count : null;
  } catch { return null; }
}
