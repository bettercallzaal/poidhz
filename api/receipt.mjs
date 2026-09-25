// zpoidh - submission receipt image (GET /api/receipt).
//
// WHY THIS EXISTS. poidh requires an image on every claim, and a code round has nothing to
// photograph: a CI fix, a deleted stale doc and a renamed variable all look like nothing. The
// image requirement was a tax on exactly the entrants this round is written for.
//
// This turns the tax into a receipt. An entrant fills in /submit, and the card it produces is
// the image they upload - so the picture carries the pull request link, the round, the handle
// and whether they declared themselves an agent, in a form a human reading the bounty page can
// see at a glance.
//
// AND IT IS FETCHABLE WITHOUT A BROWSER, which is the whole point for an agent:
//
//   GET /api/receipt?round=5&pr=https://github.com/ZAODEVZ/ZAOstock/pull/312&who=assay&agent=1
//   -> image/svg+xml
//
// No browser, no canvas, no headless anything. curl it, convert it if you like, upload it.
// An agent claiming through the contract directly can skip the upload entirely and point its
// claim uri at /api/claim-meta with this URL as the image.
//
// STATELESS BY DESIGN. Nothing is stored and nothing is submitted by calling this. It renders
// what you pass it. The real submission is the poidh claim; this is the picture that goes on
// it, and saying so plainly matters more than it sounds - an entrant must not believe that
// loading this URL entered them into anything.

export const config = { runtime: 'edge' };

const W = 1200;
const H = 630;

// Brand tokens, kept in step with index.html's :root by hand. A palette drifting is cosmetic;
// a wrong pull request link is not, which is why the text below is escaped and the colours are
// not parameterised at all.
const BG = '#070709';
const SURFACE = '#111115';
const BORDER = '#1f1e26';
const TEXT = '#e4e2dd';
const MUTED = '#8a8895';
const CYAN = '#00e5ff';
const GOLD = '#f5c842';
const VIOLET = '#a78bfa';

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

// Never echo anything but an http(s) URL back into the card - same rule as claim-meta.mjs.
// A data: or javascript: URL rendered into an SVG that then gets uploaded somewhere is not a
// theoretical problem, and the fix is to refuse rather than to sanitise cleverly.
function safeUrl(s) {
  try {
    const u = new URL(String(s || ''));
    return (u.protocol === 'http:' || u.protocol === 'https:') ? u.href : '';
  } catch (e) {
    return '';
  }
}

function clamp(s, n) {
  const t = String(s == null ? '' : s).trim();
  return t.length > n ? t.slice(0, n - 1) + '…' : t;
}

// A pull request URL is the one field worth reading closely, because it is what the round is
// judged on. Returns a short display form (owner/repo#number) when it really is a PR URL, and
// the empty string when it is not - the caller then says so on the card instead of pretending.
function prShort(href) {
  try {
    const u = new URL(href);
    if (u.hostname !== 'github.com') return '';
    const m = u.pathname.match(/^\/([^/]+)\/([^/]+)\/pull\/(\d+)/);
    return m ? `${m[1]}/${m[2]}#${m[3]}` : '';
  } catch (e) {
    return '';
  }
}

function svg(fields) {
  const { round, prUrl, pr, who, agent, what, asked, stamp } = fields;
  const line = (y, label, value, colour) => `
  <text x="72" y="${y}" font-family="JetBrains Mono, ui-monospace, monospace" font-size="19"
        fill="${MUTED}" letter-spacing="1.5">${esc(label)}</text>
  <text x="72" y="${y + 36}" font-family="Outfit, system-ui, sans-serif" font-size="30"
        fill="${colour || TEXT}">${esc(value)}</text>`;

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img"
     aria-label="poidhz submission receipt for ${esc(pr || 'a pull request')}">
  <rect width="${W}" height="${H}" fill="${BG}"/>
  <rect x="40" y="40" width="${W - 80}" height="${H - 80}" rx="14" fill="${SURFACE}" stroke="${BORDER}"/>
  <text x="72" y="112" font-family="JetBrains Mono, ui-monospace, monospace" font-size="20"
        fill="${CYAN}" letter-spacing="3">POIDHZ SUBMISSION RECEIPT</text>
  <text x="${W - 72}" y="112" text-anchor="end" font-family="JetBrains Mono, ui-monospace, monospace"
        font-size="20" fill="${agent ? VIOLET : MUTED}" letter-spacing="2">${agent ? 'AGENT' : 'HUMAN'}</text>
  <line x1="72" y1="136" x2="${W - 72}" y2="136" stroke="${BORDER}"/>
  ${line(190, 'ROUND', round ? `ZAOstock round ${round}` : 'not stated', GOLD)}
  ${line(288,
         pr ? 'PULL REQUEST'
            : (prUrl ? 'NOT A GITHUB PULL REQUEST URL - THE LINK GIVEN WAS'
                     : 'PULL REQUEST'),
         pr || (prUrl ? clamp(prUrl, 52) : 'NOT A GITHUB PULL REQUEST URL'),
         pr ? TEXT : '#ff3d6e')}
  ${line(386, 'SUBMITTED BY', who || 'not stated')}
  ${what ? line(484, 'WHAT IT CHANGES', clamp(what, 64)) : ''}
  ${asked ? `
  <text x="72" y="558" font-family="JetBrains Mono, ui-monospace, monospace" font-size="17"
        fill="${CYAN}">ASKED FOR FEEDBACK ON: ${esc(clamp(asked, 58))}</text>` : ''}
  <text x="${W - 72}" y="558" text-anchor="end" font-family="JetBrains Mono, ui-monospace, monospace"
        font-size="16" fill="#4e4c57">${esc(stamp)}</text>
  <text x="72" y="${H - 28}" font-family="JetBrains Mono, ui-monospace, monospace" font-size="15"
        fill="#4e4c57">poidhz.com/submit - this card is a picture, not an entry. Your claim on poidh is the entry.</text>
</svg>`;
}

export default async function handler(req) {
  const q = new URL(req.url).searchParams;
  const prUrl = safeUrl(q.get('pr'));
  const fields = {
    round: clamp(q.get('round') || '', 12),
    prUrl,
    pr: prShort(prUrl),
    who: clamp((q.get('who') || '').replace(/^@/, '') ? '@' + (q.get('who') || '').replace(/^@/, '') : '', 40),
    agent: q.get('agent') === '1' || q.get('agent') === 'true',
    what: q.get('what') || '',
    asked: q.get('asked') || '',
    // The date comes from the edge's clock at render time, never from the query string: a
    // stamp a submitter can set is not a stamp.
    stamp: new Date().toISOString().slice(0, 16).replace('T', ' ') + ' UTC',
  };

  return new Response(svg(fields), {
    headers: {
      'Content-Type': 'image/svg+xml; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      // Short cache only: the stamp is part of the image, so a long cache would hand a later
      // fetcher an earlier submitter's minute.
      'Cache-Control': 'public, max-age=60',
    },
  });
}
