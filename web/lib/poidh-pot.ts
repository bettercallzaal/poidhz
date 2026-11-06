// Live pot of one poidh bounty, read from poidh's own public tRPC API (bounties.fetch), plus an
// approximate ETH to USD rate. Read-only, no keys, cached by Next for 5 minutes (misc item 256).
// If either read fails, the caller falls back to the last known numbers, never to zero.

const UA = { 'User-Agent': 'poidhz.com (+https://poidhz.com)' };
const CACHE = { revalidate: 300 };

export type LastKnownPot = { eth: number; usdPerEth: number; date: string };

export type PotView = {
  eth: number;
  usd: number | null; // approximate: eth times the rate used; null when no rate is known
  approxUsd: true;
  source: 'live' | 'last-known';
  rateSource: 'live' | 'last-known' | null;
  asOf: string | null; // date of the last known numbers when source is last-known
};

/** The bounty's current pot in ETH, or null if poidh cannot be read. Zero is a real answer. */
export async function fetchPotEth(id: number, chainId = 8453, fetchImpl: typeof fetch = fetch): Promise<number | null> {
  try {
    const input = encodeURIComponent(JSON.stringify({ 0: { json: { id, chainId } } }));
    const r = await fetchImpl(`https://poidh.xyz/api/trpc/bounties.fetch?batch=1&input=${input}`, { headers: UA, signal: AbortSignal.timeout(8000), next: CACHE } as RequestInit);
    if (!r.ok) return null;
    const b = (await r.json())?.[0]?.result?.data?.json;
    if (!b || b.id !== id || b.isCanceled) return null;
    const wei = typeof b.amount === 'string' ? b.amount : String(b.amount ?? '');
    if (!/^\d+$/.test(wei)) return null;
    return Number(BigInt(wei) / BigInt(1e12)) / 1e6; // wei to ETH, 6 decimals
  } catch {
    return null;
  }
}

/** Approximate USD per ETH from CoinGecko's keyless simple price, or null. */
export async function fetchEthUsd(fetchImpl: typeof fetch = fetch): Promise<number | null> {
  try {
    const r = await fetchImpl('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd', { headers: UA, signal: AbortSignal.timeout(8000), next: CACHE } as RequestInit);
    if (!r.ok) return null;
    const p = (await r.json())?.ethereum?.usd;
    return typeof p === 'number' && p > 0 ? p : null;
  } catch {
    return null;
  }
}

/**
 * Pick what the page shows. A live pot wins, including a live zero. When the pot cannot be read,
 * the last known pot is shown with its date. With no live pot and no last known pot, null: the
 * page then falls back to the hand-entered tracker.
 */
export function potView(liveEth: number | null, liveRate: number | null, last: LastKnownPot | null): PotView | null {
  const eth = liveEth ?? last?.eth ?? null;
  if (eth == null) return null;
  const rate = liveRate ?? last?.usdPerEth ?? null;
  return {
    eth,
    usd: rate == null ? null : round2(eth * rate),
    approxUsd: true,
    source: liveEth != null ? 'live' : 'last-known',
    rateSource: liveRate != null ? 'live' : rate != null ? 'last-known' : null,
    asOf: liveEth != null ? null : last!.date,
  };
}

const round2 = (n: number) => Math.round(n * 100) / 100;

export async function loadPot(id: number | null, last: LastKnownPot | null, fetchImpl: typeof fetch = fetch): Promise<PotView | null> {
  if (id == null) return null;
  const [eth, rate] = await Promise.all([fetchPotEth(id, 8453, fetchImpl), fetchEthUsd(fetchImpl)]);
  return potView(eth, rate, last);
}
