// Fetches every route against a running server. Usage: BASE=http://localhost:3000 node test/smoke.mjs
const BASE = process.env.BASE || 'http://localhost:3000';
const routes = ['/', '/people', '/b/1421', '/b/1418', '/b/1412', '/u/pascaline', '/u/assay', '/rounds.json', '/llms.txt',
  '/submit', '/gallery', '/calendar', '/dashboard', '/create-bounty', '/about', '/best-practices', '/feedback', '/feedback/1418', '/feedback/1418/assay', '/round/5', '/round/2/judging', '/docs/about', '/docs/poidh-hub', '/rounds/r2/judging', '/b/1249',
  '/data/claims.json', '/data/rounds-live.json', '/leaderboard', '/api/receipt?round=5&pr=https%3A%2F%2Fgithub.com%2FZAODEVZ%2FZAOstock%2Fpull%2F352'];
let bad = 0;
for (const r of routes) {
  const res = await fetch(BASE + r, { redirect: 'manual' });
  const body = await res.text();
  const ok = res.status === 200 && body.length > 0 && !body.includes('Application error');
  if (!ok) bad++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${res.status} ${r} (${body.length} bytes)`);
}
const nf = await fetch(BASE + '/b/999999');
console.log(`${nf.status === 404 ? 'ok  ' : 'FAIL'} ${nf.status} /b/999999 must 404`); if (nf.status !== 404) bad++;

// Old .html paths redirect to their clean URL.
for (const [from, to] of [['/index.html', '/'], ['/people.html', '/people']]) {
  const res = await fetch(BASE + from, { redirect: 'manual' });
  const loc = res.headers.get('location') || '';
  const ok = res.status >= 300 && res.status < 400 && new URL(loc, BASE).pathname === to;
  if (!ok) bad++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${res.status} ${from} -> ${loc || 'nothing'}`);
}
// A malformed person key is a 404, not a 500.
const mk = await fetch(BASE + '/u/%E0%A4%A');
console.log(`${mk.status === 404 ? 'ok  ' : 'FAIL'} ${mk.status} /u/%E0%A4%A must 404`); if (mk.status !== 404) bad++;
// Phase-bearing pages must not be served from a 5-minute cache: a round that closed would still read open.
for (const r of ['/', '/rounds.json', '/llms.txt']) {
  const cc = (await fetch(BASE + r)).headers.get('cache-control') || '';
  const ok = !/s-maxage=\d+/.test(cc);
  if (!ok) bad++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${r} cache-control: ${cc}`);
}
// Every person link on every bounty page resolves.
const feed = await (await fetch(BASE + '/rounds.json')).json();
const ids = [...feed.open, ...feed.recent].map((r) => r.bounty_id);
if (ids.length === 0) { console.log('UNKNOWN: rounds.json listed no bounties to crawl'); process.exit(2); }
const links = new Set();
for (const id of ids) for (const m of (await (await fetch(`${BASE}/b/${id}`)).text()).matchAll(/href="(\/u\/[^"]+)"/g)) links.add(m[1]);
if (links.size === 0) { console.log('UNKNOWN: no person links found to check'); process.exit(2); }
let dead = 0;
for (const l of links) { const st = (await fetch(BASE + l)).status; if (st !== 200) { dead++; console.log(`FAIL ${st} ${l}`); } }
console.log(`${dead ? 'FAIL' : 'ok  '} ${links.size - dead} of ${links.size} person links from ${ids.length} bounty pages resolve`); bad += dead;
if (routes.length === 0) { console.log('UNKNOWN: no routes'); process.exit(2); }
console.log(bad ? `${bad} check(s) failed` : 'all checks passed');
process.exit(bad ? 1 : 0);
