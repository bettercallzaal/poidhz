// Guards for the public sign-up route. Pure, so they are tested without a server.

// A browser sends Origin on every cross-site POST. No Origin at all (curl, same-site form posts in
// some browsers) is allowed; an Origin from another host is not. Host is the request's own host.
export function sameOrigin(origin: string | null, host: string | null): boolean {
  if (!origin) return true;
  if (!host) return false;
  try { return new URL(origin).host.toLowerCase() === host.toLowerCase(); } catch { return false; }
}

// The first address in x-forwarded-for is the client as Vercel saw it; anything else is unknown.
export function clientKey(headers: { get(name: string): string | null }): string {
  const xff = headers.get('x-forwarded-for') ?? '';
  const first = xff.split(',')[0].trim();
  return first || headers.get('x-real-ip') || 'unknown';
}

// Sliding window per key, in memory. One serverless instance sees only its own traffic, so this
// is a brake on a loop from one client, not a wall; the endpoint behind it has the real quota.
export class RateLimiter {
  private hits = new Map<string, number[]>();
  constructor(private readonly max: number, private readonly windowMs: number, private readonly now: () => number = Date.now) {}
  allow(key: string): boolean {
    const t = this.now();
    const recent = (this.hits.get(key) ?? []).filter((h) => t - h < this.windowMs);
    if (recent.length >= this.max) { this.hits.set(key, recent); return false; }
    recent.push(t);
    this.hits.set(key, recent);
    if (this.hits.size > 10000) this.hits.clear();
    return true;
  }
}

// Read a request body up to a byte cap; null when it is over or unreadable.
export async function readBodyCapped(req: Request, maxBytes: number): Promise<string | null> {
  const declared = Number(req.headers.get('content-length') ?? '0');
  if (declared > maxBytes) return null;
  try {
    const text = await req.text();
    return new TextEncoder().encode(text).length > maxBytes ? null : text;
  } catch { return null; }
}
