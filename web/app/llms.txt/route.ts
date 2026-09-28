import { loadAll, sources, SITE } from '@/lib/load';
import { roundsFeed, llmsTxt } from '@/lib/feeds';
// Phase is computed from the clock; a cached render would show a closed round as open.
export const dynamic = 'force-dynamic';
export async function GET() {
  const { rounds } = await loadAll();
  return new Response(llmsTxt(roundsFeed(rounds, new Date(), SITE, sources.channel), SITE), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
