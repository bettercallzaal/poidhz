import { describe, it, expect } from 'vitest';
import { RateLimiter, clientKey, readBodyCapped, sameOrigin } from './guard';

describe('sameOrigin', () => {
  it('allows no Origin and the same host, in any case', () => {
    expect(sameOrigin(null, 'poidhz.com')).toBe(true);
    expect(sameOrigin('https://poidhz.com', 'poidhz.com')).toBe(true);
    expect(sameOrigin('https://POIDHZ.com', 'poidhz.com')).toBe(true);
  });
  it('refuses another host, a subdomain, a port change, garbage and a missing host', () => {
    expect(sameOrigin('https://evil.example', 'poidhz.com')).toBe(false);
    expect(sameOrigin('https://www.poidhz.com', 'poidhz.com')).toBe(false);
    expect(sameOrigin('https://poidhz.com:8443', 'poidhz.com')).toBe(false);
    expect(sameOrigin('null', 'poidhz.com')).toBe(false);
    expect(sameOrigin('https://poidhz.com', null)).toBe(false);
  });
});

describe('clientKey', () => {
  const h = (m: Record<string, string>) => ({ get: (k: string) => m[k.toLowerCase()] ?? null });
  it('takes the first forwarded address', () => expect(clientKey(h({ 'x-forwarded-for': '203.0.113.9, 10.0.0.1' }))).toBe('203.0.113.9'));
  it('falls back to x-real-ip, then unknown', () => {
    expect(clientKey(h({ 'x-real-ip': '203.0.113.7' }))).toBe('203.0.113.7');
    expect(clientKey(h({}))).toBe('unknown');
  });
});

describe('RateLimiter', () => {
  it('allows max hits in the window, refuses the next, and lets it through once the window slides', () => {
    let t = 0;
    const l = new RateLimiter(3, 1000, () => t);
    expect([l.allow('a'), l.allow('a'), l.allow('a')]).toEqual([true, true, true]);
    expect(l.allow('a')).toBe(false);
    expect(l.allow('b')).toBe(true);
    t = 1001;
    expect(l.allow('a')).toBe(true);
  });
});

describe('readBodyCapped', () => {
  it('reads a small body and refuses a big one by header or by size', async () => {
    expect(await readBodyCapped(new Request('https://x', { method: 'POST', body: '{"a":1}' }), 100)).toBe('{"a":1}');
    expect(await readBodyCapped(new Request('https://x', { method: 'POST', body: 'x'.repeat(101) }), 100)).toBeNull();
    expect(await readBodyCapped(new Request('https://x', { method: 'POST', body: 'x', headers: { 'content-length': '5000' } }), 100)).toBeNull();
  });
});
