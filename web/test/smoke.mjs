// Fetches every route against a running server. Usage: BASE=http://localhost:3000 node test/smoke.mjs
const BASE = process.env.BASE || 'http://localhost:3000';
const routes = ['/', '/people', '/b/1421', '/b/1418', '/b/1412', '/u/pascaline', '/u/assay', '/rounds.json', '/llms.txt',
  '/submit', '/gallery', '/calendar', '/dashboard', '/create-bounty', '/about', '/best-practices', '/feedback', '/feedback/1418', '/feedback/1418/assay', '/round/5',
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
if (routes.length === 0) { console.log('UNKNOWN: no routes'); process.exit(2); }
console.log(`${routes.length + 1 - bad} of ${routes.length + 1} passed`);
process.exit(bad ? 1 : 0);
