import { loadRandom } from '@/lib/random-load';

export const dynamic = 'force-dynamic';

// One random bounty as JSON. The /random page calls this to keep a few picks
// loaded ahead, so the button shows the next one at once.
export async function GET() {
  const b = await loadRandom();
  return Response.json(b, { status: b ? 200 : 503, headers: { 'Cache-Control': 'no-store' } });
}
