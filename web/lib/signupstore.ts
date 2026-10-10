import 'server-only';
import { readStoreConfig, type Signup } from './signup';

// Where a sign-up goes. Zaal ruled (item 111, 10 Oct 2026): "Hurricane gets it on his database",
// so rows are forwarded to an endpoint hurric4n3ike provides on the WaveZStation side, and
// nothing is kept on poidhz.com. storeReady is true only when SIGNUP_ENDPOINT is https AND
// SIGNUP_TOKEN is set (readStoreConfig); otherwise every function here refuses without a fetch.
// Remote answers are mapped to fixed messages; nothing the endpoint says reaches the entrant.
// This file is the one function to change if the endpoint's shape differs from
// rounds/daily/d10/HURRICANE-NOTE.md.
const config = () => readStoreConfig(process.env);
export const storeReady = config() !== null;

const NOT_ON = 'sign-up is not switched on yet; nothing was stored';
const DUP = 'that song is already signed up';
const DOWN = 'the sign-up database did not accept it; nothing was stored, try again in a minute';

export type PutResult = { ok: true; count: number | null } | { ok: false; status: number; errors: string[] };

// The endpoint owns the one-entry-per-song rule and answers 409 for a repeat.
export async function putSignup(round: number, s: Signup): Promise<PutResult> {
  const c = config();
  if (!c) return { ok: false, status: 503, errors: [NOT_ON] };
  try {
    const r = await fetch(c.endpoint, {
      method: 'POST', body: JSON.stringify({ round, ...s }), signal: AbortSignal.timeout(8000),
      headers: { 'content-type': 'application/json', accept: 'application/json', authorization: `Bearer ${c.token}` },
    });
    if (r.status === 409) return { ok: false, status: 409, errors: [DUP] };
    const j = (await r.json().catch(() => ({}))) as { ok?: boolean; count?: number };
    if (!r.ok || j.ok === false) return { ok: false, status: 502, errors: [DOWN] };
    return { ok: true, count: typeof j.count === 'number' ? j.count : null };
  } catch {
    return { ok: false, status: 502, errors: [DOWN] };
  }
}

export async function countSignups(round: number): Promise<number | null> {
  const c = config();
  if (!c) return null;
  try {
    const u = new URL(c.endpoint); u.searchParams.set('round', String(round));
    const r = await fetch(u, { headers: { accept: 'application/json', authorization: `Bearer ${c.token}` }, signal: AbortSignal.timeout(5000) });
    const j = (await r.json().catch(() => ({}))) as { count?: number };
    return r.ok && typeof j.count === 'number' ? j.count : null;
  } catch { return null; }
}
