// Round ten sign-up: artists with a song on WaveZStation enter by email first, then the form.
// Pure checks only; the store and the song lookup live in signupstore.ts and the route.
// Dates come from rounds/daily/d10/description.md: sign-up closes 11:59pm Eastern, Sunday
// 18 October 2026, which is 03:59:59 UTC on the 19th (Eastern is UTC-4 until 1 November 2026).

export const ROUND = {
  n: 10,
  signupClosesAt: '2026-10-19T03:59:59.999Z',
  signupClosesText: '11:59pm Eastern, Sunday October 18, 2026',
  emailUse: 'Your email is used to reach you about this round and for nothing else. It is not a mailing list. It is deleted when the round closes out.',
} as const;

export function signupOpen(now: Date): boolean {
  return now.getTime() <= Date.parse(ROUND.signupClosesAt);
}

export type SignupInput = { email?: string; artist?: string; song?: string; handle?: string; where?: string };
export type Signup = { email: string; artist: string; song_id: string; song_link: string; handle: string; where: string; recorded_at: string };

// Deliberately loose: one @, something either side, no spaces. Anything stricter rejects real addresses.
export function checkEmail(s: string | undefined): string | null {
  const e = (s ?? '').trim();
  if (!e) return 'email is required';
  if (e.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)) return 'that does not look like an email address';
  return null;
}

// The song page is https://wavezstation.com/song/<uuid>. Accept www., http, a query string or a
// trailing slash, and the bare uuid; refuse anything else so the lookup never fetches a guess.
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
export function songIdFromLink(s: string | undefined): string | null {
  const t = (s ?? '').trim();
  if (UUID.test(t)) return t.toLowerCase();
  let u: URL;
  try { u = new URL(t); } catch { return null; }
  if (!/^(www\.)?wavezstation\.com$/.test(u.hostname)) return null;
  const m = u.pathname.match(/^\/song\/([^/]+)\/?$/);
  return m && UUID.test(m[1]) ? m[1].toLowerCase() : null;
}

export function songLink(id: string): string {
  return `https://wavezstation.com/song/${id}`;
}

export function checkSignup(i: SignupInput): string[] {
  const errs: string[] = [];
  const e = checkEmail(i.email);
  if (e) errs.push(e);
  const artist = (i.artist ?? '').trim();
  if (!artist) errs.push('artist name is required');
  if (artist.length > 80) errs.push('artist name is too long (80 characters)');
  if (!songIdFromLink(i.song)) errs.push('the song link must be a wavezstation.com/song/... page');
  const handle = (i.handle ?? '').trim();
  if (handle.length > 60) errs.push('handle is too long (60 characters)');
  const where = (i.where ?? '').trim();
  if (!where) errs.push('say where the rollout will be posted');
  if (where.length > 300) errs.push('where is too long (300 characters)');
  return errs;
}

export function toSignup(i: SignupInput, now: Date): Signup {
  const id = songIdFromLink(i.song)!;
  return {
    email: (i.email ?? '').trim().toLowerCase(), artist: (i.artist ?? '').trim(), song_id: id, song_link: songLink(id),
    handle: (i.handle ?? '').trim().replace(/^@/, ''), where: (i.where ?? '').trim(), recorded_at: now.toISOString(),
  };
}

// https://www.wavezstation.com/api/songs/<id> answers {song: {id, title, artist, ...}} for a listed
// song and 404 otherwise (the apex host 308s to www; measured 20:53Z 10 Oct 2026).
export const SONG_API = 'https://www.wavezstation.com/api/songs/';
export type SongRecord = { id: string; title: string; artist: string };
export function songFromRecord(j: unknown, id: string): SongRecord | null {
  const s = (j as { song?: { id?: unknown; title?: unknown; artist?: unknown } } | null)?.song;
  if (!s || typeof s.id !== 'string' || s.id.toLowerCase() !== id) return null;
  return { id, title: typeof s.title === 'string' ? s.title : '', artist: typeof s.artist === 'string' ? s.artist : '' };
}
