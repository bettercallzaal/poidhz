import { describe, it, expect } from 'vitest';
import { ROUND, checkEmail, checkSignup, readStoreConfig, signupOpen, songFromRecord, songIdFromLink, toSignup } from './signup';

const id = 'a6c6d732-8f7a-4621-a478-d7025e3bfc98';
const good = { email: 'Benny@Example.com', artist: 'BennyJ504', song: `https://wavezstation.com/song/${id}`, handle: '@bennyj504', where: 'X and TikTok' };

describe('signup window', () => {
  it('closes at 11:59pm Eastern on Sunday 18 October 2026, which is 03:59:59Z on the 19th', () => {
    expect(ROUND.signupClosesAt).toBe('2026-10-19T03:59:59.999Z');
    expect(new Date(ROUND.signupClosesAt).getUTCDay()).toBe(1); // Monday in UTC, still Sunday night in Eastern
  });
  it('is open before the close and shut after it', () => {
    expect(signupOpen(new Date('2026-10-19T03:59:59Z'))).toBe(true);
    expect(signupOpen(new Date('2026-10-19T04:00:00Z'))).toBe(false);
  });
});

describe('checkEmail', () => {
  it('takes an ordinary address', () => expect(checkEmail('a@b.co')).toBeNull());
  it('refuses nothing, spaces and no domain', () => {
    expect(checkEmail('')).toBe('email is required');
    expect(checkEmail('a b@c.d')).toMatch(/does not look/);
    expect(checkEmail('a@b')).toMatch(/does not look/);
  });
});

describe('songIdFromLink', () => {
  it('reads the song page link in its shapes', () => {
    for (const s of [`https://wavezstation.com/song/${id}`, `https://www.wavezstation.com/song/${id}/`, `http://wavezstation.com/song/${id}?ref=x`, id, ` ${id.toUpperCase()} `]) expect(songIdFromLink(s)).toBe(id);
  });
  it('refuses other hosts, other paths and non-uuids', () => {
    for (const s of ['https://example.com/song/' + id, 'https://wavezstation.com/artist/benny', 'https://wavezstation.com/song/not-a-uuid', 'wavezstation.com/song/' + id, '', undefined]) expect(songIdFromLink(s)).toBeNull();
  });
});

describe('checkSignup', () => {
  it('a full form has no errors', () => expect(checkSignup(good)).toEqual([]));
  it('names every missing field at once', () => {
    const errs = checkSignup({});
    expect(errs).toContain('email is required');
    expect(errs).toContain('artist name is required');
    expect(errs).toContain('the song link must be a wavezstation.com/song/... page');
    expect(errs).toContain('say where the rollout will be posted');
  });
  it('handle is optional', () => expect(checkSignup({ ...good, handle: '' })).toEqual([]));
});

describe('toSignup', () => {
  it('lowercases the email, strips the @, keeps the canonical song link', () => {
    const s = toSignup(good, new Date('2026-10-12T12:00:00Z'));
    expect(s).toEqual({ email: 'benny@example.com', artist: 'BennyJ504', song_id: id, song_link: `https://wavezstation.com/song/${id}`, handle: 'bennyj504', where: 'X and TikTok', recorded_at: '2026-10-12T12:00:00.000Z' });
  });
});

describe('songFromRecord', () => {
  it("reads the site's {song: {...}} shape", () => expect(songFromRecord({ song: { id: id.toUpperCase(), title: 'Saturday in LA', artist: 'BennyJ504', audio_url: 'x' } }, id)).toEqual({ id, title: 'Saturday in LA', artist: 'BennyJ504' }));
  it('refuses a redirect body, a different id and nothing', () => {
    expect(songFromRecord({ redirect: 'https://www.wavezstation.com/api/songs/' + id, status: '308' }, id)).toBeNull();
    expect(songFromRecord({ song: { id: '11111111-1111-1111-1111-111111111111' } }, id)).toBeNull();
    expect(songFromRecord(null, id)).toBeNull();
  });
});

describe('readStoreConfig', () => {
  const ok = { SIGNUP_ENDPOINT: 'https://wavezstation.com/api/poidhz-signup', SIGNUP_TOKEN: 'abc' };
  it('is on only with an https endpoint and a token', () => expect(readStoreConfig(ok)).toEqual({ endpoint: 'https://wavezstation.com/api/poidhz-signup', token: 'abc' }));
  it('refuses an http endpoint', () => expect(readStoreConfig({ ...ok, SIGNUP_ENDPOINT: 'http://wavezstation.com/api/poidhz-signup' })).toBeNull());
  it('refuses a missing token', () => expect(readStoreConfig({ SIGNUP_ENDPOINT: ok.SIGNUP_ENDPOINT })).toBeNull());
  it('refuses an empty or whitespace token', () => {
    expect(readStoreConfig({ ...ok, SIGNUP_TOKEN: '' })).toBeNull();
    expect(readStoreConfig({ ...ok, SIGNUP_TOKEN: '   ' })).toBeNull();
  });
  it('refuses a missing or unparsable endpoint, and credentials in the URL', () => {
    expect(readStoreConfig({ SIGNUP_TOKEN: 'abc' })).toBeNull();
    expect(readStoreConfig({ ...ok, SIGNUP_ENDPOINT: 'not a url' })).toBeNull();
    expect(readStoreConfig({ ...ok, SIGNUP_ENDPOINT: 'https://user:pw@wavezstation.com/x' })).toBeNull();
  });
});
