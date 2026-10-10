import { ROUND, SONG_API, checkSignup, signupOpen, songFromRecord, songIdFromLink, toSignup } from '@/lib/signup';
import { countSignups, hasSignup, putSignup, storeReady } from '@/lib/signupstore';

export const dynamic = 'force-dynamic';
const cors = { 'Access-Control-Allow-Origin': '*' };

// GET says whether sign-up is open and how many songs are in. Never the names or the addresses.
export async function GET() {
  return Response.json({
    round: ROUND.n, open: signupOpen(new Date()), closesAt: ROUND.signupClosesAt, storeReady,
    count: await countSignups(ROUND.n), emailUse: ROUND.emailUse,
  }, { headers: cors });
}

// Is this song listed on WaveZStation? Read its own record; a 404 or a timeout is a no.
async function songListed(id: string): Promise<{ listed: boolean; title?: string; artist?: string; reason?: string }> {
  try {
    const r = await fetch(SONG_API + id, { signal: AbortSignal.timeout(6000), headers: { accept: 'application/json' } });
    if (!r.ok) return { listed: false, reason: `wavezstation.com answered ${r.status} for that song; is it listed?` };
    const song = songFromRecord(await r.json(), id);
    if (!song) return { listed: false, reason: 'wavezstation.com has no song with that id' };
    return { listed: true, title: song.title, artist: song.artist };
  } catch {
    return { listed: false, reason: 'could not reach wavezstation.com to check the song; try again in a minute' };
  }
}

export async function POST(req: Request) {
  const fail = (status: number, errors: string[]) => Response.json({ ok: false, errors }, { status, headers: cors });
  let input: Record<string, unknown>;
  try { input = await req.json(); } catch { return fail(400, ['send JSON: {email, artist, song, handle, where}']); }
  const pick = (k: string) => (typeof input[k] === 'string' ? (input[k] as string) : undefined);
  const i = { email: pick('email'), artist: pick('artist'), song: pick('song'), handle: pick('handle'), where: pick('where') };
  const errors = checkSignup(i);
  if (errors.length) return fail(422, errors);
  const now = new Date();
  if (!signupOpen(now)) return fail(409, [`sign-up closed at ${ROUND.signupClosesText}`]);
  const id = songIdFromLink(i.song)!;
  const song = await songListed(id);
  if (!song.listed) return fail(422, [song.reason!]);
  // Checks first, store last, so the form can be tried end to end before the store is switched on.
  if (!storeReady) return fail(503, ['sign-up is not switched on yet; nothing was stored']);
  if (await hasSignup(ROUND.n, id)) return fail(409, ['that song is already signed up']);
  await putSignup(ROUND.n, toSignup(i, now));
  return Response.json({ ok: true, song: { id, title: song.title, artist: song.artist }, count: await countSignups(ROUND.n) }, { headers: cors });
}
