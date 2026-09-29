import { describe, it, expect } from 'vitest';
import { composeEntryPost } from './share';

const base = { title: 'ZAOstock Round 7 - Run A Bounty For ZAOstock', boardUrl: 'https://poidhz.com/b/1453', channel: 'zao' };

describe('composeEntryPost', () => {
  const p = composeEntryPost({ ...base, claim: '8400', link: 'https://poidh.xyz/base/bounty/1460', about: 'Film the stage from the back of Franklin Street.\nEnds Oct 31.' });
  it('names the round, the claim, the link and the details', () => {
    expect(p.text).toContain('My entry for ZAOstock Round 7');
    expect(p.text).toContain('claim 8400');
    expect(p.text).toContain('https://poidh.xyz/base/bounty/1460');
    expect(p.text).toContain('Ends Oct 31.');
  });
  it('the Farcaster link posts in the channel with the board page embedded', () => {
    const u = new URL(p.farcasterUrl);
    expect(u.origin + u.pathname).toBe('https://farcaster.xyz/~/compose');
    expect(u.searchParams.get('channelKey')).toBe('zao');
    expect(u.searchParams.getAll('embeds[]')).toEqual(['https://poidhz.com/b/1453']);
    expect(u.searchParams.get('text')).toBe(p.text);
  });
  it('the X link carries the text and the board page', () => {
    const u = new URL(p.xUrl);
    expect(u.searchParams.get('url')).toBe('https://poidhz.com/b/1453');
    expect(u.searchParams.get('text')).toBe(p.text);
  });
  it('empty fields are left out, not printed as blanks', () => {
    const q = composeEntryPost({ ...base, claim: ' ', link: '', about: '' });
    expect(q.text).not.toContain('claim');
    expect(q.text).not.toMatch(/\n\n\n/);
    expect(q.ready).toBe(false);
  });
  it('a link that is not http(s) is dropped', () => {
    expect(composeEntryPost({ ...base, claim: '', link: 'javascript:alert(1)', about: 'x' }).text).not.toContain('javascript');
  });
});
