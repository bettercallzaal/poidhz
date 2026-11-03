import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { BOUNTY_URL, IRL, ONLINE, SONG_MAP, SONG_MP3 } from '../app/music-video/data';

describe('music video footage guide', () => {
  it('lists only https sources, with no duplicates', () => {
    const all = [...IRL, ...ONLINE].map((s) => s.href);
    expect(all.length).toBeGreaterThan(0);
    for (const href of all) expect(href).toMatch(/^https:\/\//);
    expect(new Set(all).size).toBe(all.length);
  });

  it('maps the whole song, 0:00 to 2:22, in order', () => {
    expect(SONG_MAP[0][0].startsWith('0:00')).toBe(true);
    expect(SONG_MAP[SONG_MAP.length - 1][0].endsWith('2:22')).toBe(true);
    const sec = (t: string) => { const [m, s] = t.split(':').map(Number); return m * 60 + s; };
    for (let i = 1; i < SONG_MAP.length; i++) {
      const prevEnd = SONG_MAP[i - 1][0].split(' to ')[1];
      const start = SONG_MAP[i][0].split(' to ')[0];
      expect(sec(start)).toBe(sec(prevEnd));
    }
  });

  it('points at the public mp3 and renders the bounty button only once the URL is set', () => {
    expect(SONG_MP3).toContain('/releases/download/bettercallzaal-song-mp3/');
    expect(typeof BOUNTY_URL).toBe('string');
    const src = readFileSync(join(__dirname, '..', 'app', 'music-video', 'page.tsx'), 'utf8');
    expect(src).toContain('{BOUNTY_URL &&');
    expect(src).toContain('update this page as much as I can');
    expect(src).not.toMatch(/coming soon|TODO|TBD|\[[A-Z ]+\]/i);
  });
});
