// Links for the Singapore Congress crowdfund page (/singapore).
// Creating each link is Zaal's tap. The page renders a button only for a non-empty value,
// so an empty string here means that button does not exist on the page.

export const STRIPE_LINK = '';
// No Stripe link for now (misc item 167). A backer who needs one asks by email.
export const STRIPE_REQUEST_URL = 'mailto:zaal@thezao.com?subject=Stripe%20link%20for%20the%20Singapore%20trip';
export const PAYPAL_LINK = 'https://www.paypal.com/biz/profile/zaalpanthaki';
export const POIDH_BOUNTY_URL = 'https://poidh.xyz/base/bounty/1536';
// The bounty's numeric id on Base, from POIDH_BOUNTY_URL (misc item 256). While null, the page
// shows the hand-entered POIDH row from tracker.ts. Set both in the same held PR after the cast.
export const POIDH_BOUNTY_ID: number | null = 1536;
// The last pot this repo saw, shown with its date if poidh cannot be read. Never zero by accident:
// null until the first real reading after the cast.
// The ETH Zaal funds the bounty with at the cast: his own seed, on top of the goal (misc item 260).
// The page subtracts it from the live pot. Null until he casts.
export const POIDH_SEED_ETH: number | null = 0.045;

// First reading 2026-11-06 via scripts/query-bounty.py: 0.045 ETH, about $101.29 (0 claims), all of it his seed.
export const POIDH_LAST_KNOWN: { eth: number; usdPerEth: number; date: string } | null = { eth: 0.045, usdPerEth: 2250.89, date: '2026-11-06' };
// Where a backer sends a question about Zoroastrianism.
// Interim until the ZAO learns about Zoroastrianism site has a URL (seat, from misc item 148).
export const QUESTION_URL = 'mailto:zaal@thezao.com?subject=Question%20for%20Zaal%20about%20Zoroastrianism';
