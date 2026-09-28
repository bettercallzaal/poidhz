import { loadAll, sources, SITE } from '@/lib/load';
import { roundsFeed } from '@/lib/feeds';
// Phase is computed from the clock; a cached render would show a closed round as open.
export const dynamic = 'force-dynamic';
export async function GET() {
  const { rounds } = await loadAll();
  return Response.json(roundsFeed(rounds, new Date(), SITE, sources.channel), { headers: { 'Access-Control-Allow-Origin': '*' } });
}
