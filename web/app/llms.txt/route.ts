import { loadAll, sources, SITE } from '@/lib/load';
import { roundsFeed, llmsTxt } from '@/lib/feeds';
export const revalidate = 300;
export async function GET() {
  const { rounds } = await loadAll();
  return new Response(llmsTxt(roundsFeed(rounds, new Date(), SITE, sources.channel), SITE), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
