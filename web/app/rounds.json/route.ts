import { loadAll, sources, SITE } from '@/lib/load';
import { roundsFeed } from '@/lib/feeds';
export const revalidate = 300;
export async function GET() {
  const { rounds } = await loadAll();
  return Response.json(roundsFeed(rounds, new Date(), SITE, sources.channel), { headers: { 'Access-Control-Allow-Origin': '*' } });
}
