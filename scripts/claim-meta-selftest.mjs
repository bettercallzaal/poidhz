// Offline test of api/claim-meta.mjs. No network, no Vercel: it builds a Request and reads
// the Response, which is the same contract the edge runtime gives the handler.
//
// WHY THIS EXISTS, and it is not hypothetical. On 2026-09-27 a round five entrant filed
// claim 8329 on bounty 1421 whose entire description was `https://poidhz.com/api/claim-meta`
// with no query string. The endpoint answered 200 with an empty description and, for the
// image, a ZABAL GAMEZ embed card - a different brand entirely - because the fallback came
// along when this file was copied from ZAODEVZ/zabalgames api/clip-meta.mjs and nobody
// changed it. So an entrant's ZAOstock claim rendered another festival's artwork, on the
// poidh bounty page, under their name.
//
// The fallback is a real code path, reached by the least-effort call, so it gets a test.

import handler from '../api/claim-meta.mjs';

let pass = 0, fail = 0;
const check = (label, cond) => { console.log((cond ? '  ok   ' : '  FAIL ') + label); cond ? pass++ : fail++; };

const get = async (qs) => {
  const res = await handler(new Request('https://poidhz.com/api/claim-meta' + (qs ? '?' + qs : '')));
  return { res, body: JSON.parse(await res.text()) };
};

// THE BUG, pinned in both directions.
let { res, body } = await get('');
check('a bare call does NOT serve another brand', !JSON.stringify(body).includes('zabal-games'));
check('a bare call does NOT serve the gamez card', !JSON.stringify(body).includes('embed-card-gamez'));
check('a bare call falls back to poidhz own og image', body.image === 'https://poidhz.com/assets/og/og.png');
check('a bare call still returns the keys poidh reads', 'name' in body && 'description' in body && 'image' in body);
check('serves JSON', res.headers.get('Content-Type') === 'application/json');
check('CORS is open, which is why poidh can read it at all', res.headers.get('Access-Control-Allow-Origin') === '*');

// A supplied image must win over the fallback, or the fix would have broken the feature.
({ body } = await get('img=https%3A%2F%2Fexample.com%2Fmine.png'));
check('a supplied image is used instead of the fallback', body.image === 'https://example.com/mine.png');

// safeUrl is the only thing between a claim uri and whatever someone puts in the query string.
for (const bad of ['javascript:alert(1)', 'data:text/html,<script>', 'file:///etc/passwd', 'not a url']) {
  ({ body } = await get('img=' + encodeURIComponent(bad)));
  check(`a ${bad.split(':')[0]} image is refused and falls back`, body.image === 'https://poidhz.com/assets/og/og.png');
}
({ body } = await get('c=' + encodeURIComponent('javascript:alert(1)')));
check('an unsafe submission url never reaches external_url', body.external_url === 'https://poidhz.com');

// The documented shape.
({ body } = await get('t=My%20entry&d=Some%20notes&c=https%3A%2F%2Fx.com%2Fa%2Fstatus%2F1'));
check('title comes from t', body.name === 'My entry');
check('description keeps what was given', body.description.includes('Some notes'));
check('the submission url is appended to the description', body.description.includes('Submission: https://x.com/a/status/1'));
check('external_url points at the submission', body.external_url === 'https://x.com/a/status/1');

({ body } = await get('c=https%3A%2F%2Fx.com%2Fa%2Fstatus%2F1&d=' + encodeURIComponent('see https://x.com/a/status/1')));
check('the submission url is not appended twice when already present',
      (body.description.match(/https:\/\/x\.com\/a\/status\/1/g) || []).length === 1);

({ body } = await get('t=' + 'x'.repeat(300)));
check('an over-long title is truncated to 140', body.name.length === 140);
({ body } = await get('d=' + 'y'.repeat(2000)));
check('an over-long description is truncated to 1000', body.description.length === 1000);

({ body } = await get(''));
check('a bare call names itself rather than pretending to be an entry', body.name === 'POIDH claim');

console.log(`claim-meta selftest: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
