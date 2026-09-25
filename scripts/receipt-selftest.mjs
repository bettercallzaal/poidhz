// Offline test of api/receipt.mjs. No network, no Vercel: it builds a Request and reads the
// Response, which is the same contract the edge runtime gives the handler.
import handler from '../api/receipt.mjs';

let pass = 0, fail = 0;
const check = (label, cond) => { console.log((cond ? '  ok   ' : '  FAIL ') + label); cond ? pass++ : fail++; };

const get = async (qs) => {
  const res = await handler(new Request('https://poidhz.com/api/receipt?' + qs));
  return { res, body: await res.text() };
};

let { res, body } = await get('round=5&pr=https%3A%2F%2Fgithub.com%2FZAODEVZ%2FZAOstock%2Fpull%2F312&who=assay&agent=1');
check('serves image/svg+xml', res.headers.get('Content-Type').startsWith('image/svg+xml'));
check('CORS is open so an agent can fetch it', res.headers.get('Access-Control-Allow-Origin') === '*');
check('renders the PR as owner/repo#number', body.includes('ZAODEVZ/ZAOstock#312'));
check('renders the handle with one @', body.includes('@assay') && !body.includes('@@'));
check('declares AGENT when asked', body.includes('>AGENT<'));
check('says the card is not an entry', body.includes('not an entry'));

({ body } = await get('round=5&pr=https%3A%2F%2Fgithub.com%2FZAODEVZ%2FZAOstock%2Fpull%2F312&who=%40assay'));
check('a handle typed with @ is not doubled', body.includes('@assay') && !body.includes('@@'));
check('defaults to HUMAN when agent is not set', body.includes('>HUMAN<'));

({ body } = await get('pr=https%3A%2F%2Fgithub.com%2FZAODEVZ%2FZAOstock%2Ftree%2Fmain'));
check('a github URL that is NOT a pull request is called out', body.includes('NOT A GITHUB PULL REQUEST URL'));

({ body } = await get('pr=javascript%3Aalert(1)'));
check('a javascript: URL is refused, not rendered', !body.includes('javascript:'));
({ body } = await get('pr=data%3Atext%2Fhtml%2C%3Cscript%3E'));
check('a data: URL is refused, not rendered', !body.includes('data:text/html'));

({ body } = await get('what=%3Cscript%3Ealert(1)%3C%2Fscript%3E&pr=https%3A%2F%2Fgithub.com%2Fa%2Fb%2Fpull%2F1'));
check('markup in a free-text field is escaped', !body.includes('<script>') && body.includes('&lt;script&gt;'));

({ body } = await get('pr=https%3A%2F%2Fgithub.com%2Fa%2Fb%2Fpull%2F1&what=' + encodeURIComponent('x'.repeat(200))));
check('an over-long line is truncated rather than overflowing', body.includes('…'));

({ body } = await get('pr=https%3A%2F%2Fgithub.com%2Fa%2Fb%2Fpull%2F1&stamp=1999-01-01'));
check('a stamp cannot be set from the query string', !body.includes('1999-01-01'));

({ body } = await get(''));
check('an empty request still renders a card rather than erroring', body.startsWith('<svg'));
check('and it says the PR is missing', body.includes('NOT A GITHUB PULL REQUEST URL'));

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
