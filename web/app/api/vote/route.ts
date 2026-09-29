import { createPublicClient, http, isAddress } from 'viem';
import { base } from 'viem/chains';
import { loadVoteContext } from '@/lib/voters';
import { getVote, getVotes, putVote, storeReady } from '@/lib/votestore';
import { checkVote, creditsFor, parseVoteMessage, tally } from '@/lib/vote';

export const dynamic = 'force-dynamic';
const client = createPublicClient({ chain: base, transport: http() });
const cors = { 'Access-Control-Allow-Origin': '*' };

export async function GET(req: Request) {
  const ctx = await loadVoteContext();
  const address = new URL(req.url).searchParams.get('address');
  const votes = ctx.bountyId ? await getVotes(ctx.bountyId) : [];
  const body: Record<string, unknown> = {
    bounty: ctx.bountyId, open: ctx.open, storeReady, unreadBounties: ctx.unreadBounties,
    entries: ctx.entries, tally: tally(votes),
    votes: votes.map((v) => ({ address: v.address, allocation: v.allocation, issued: v.issued })),
    howTo: 'Sign the exact message "poidhz community vote\\nbounty: <id>\\nvotes: <claim>=<n>, ...\\nissued: <ISO time>" with the wallet you claimed from, then POST {address, message, signature} here.',
  };
  if (address && isAddress(address)) {
    const a = address.toLowerCase();
    body.you = {
      credits: creditsFor(a, ctx.walletsByBounty),
      ownClaims: ctx.entries.filter((e) => e.wallet === a).map((e) => e.claim),
      current: ctx.bountyId ? (await getVote(ctx.bountyId, a))?.allocation ?? null : null,
    };
  }
  return Response.json(body, { headers: cors });
}

export async function POST(req: Request) {
  const fail = (status: number, errors: string[]) => Response.json({ ok: false, errors }, { status, headers: cors });
  if (!storeReady) return fail(503, ['voting is not switched on yet']);
  let input: { address?: string; message?: string; signature?: string };
  try { input = await req.json(); } catch { return fail(400, ['send JSON: {address, message, signature}']); }
  const { address, message, signature } = input;
  if (!address || !isAddress(address) || !message || !signature?.startsWith('0x')) return fail(400, ['address, message and signature are all required']);
  const parsed = parseVoteMessage(message);
  if (!parsed) return fail(400, ['the message is not in the vote format']);
  const ctx = await loadVoteContext();
  if (!ctx.open || parsed.bounty !== ctx.bountyId) return fail(409, ['voting is not open for this bounty']);
  let valid = false;
  try { valid = await client.verifyMessage({ address: address as `0x${string}`, message, signature: signature as `0x${string}` }); } catch { valid = false; }
  if (!valid) return fail(401, ['the signature does not match this wallet']);
  const a = address.toLowerCase();
  const previous = await getVote(parsed.bounty, a);
  const errors = checkVote({
    bounty: parsed.bounty, allocation: parsed.allocation, credits: creditsFor(a, ctx.walletsByBounty),
    ownClaims: ctx.entries.filter((e) => e.wallet === a).map((e) => e.claim), validClaims: ctx.entries.map((e) => e.claim),
    issued: parsed.issued, now: new Date(), previousIssued: previous?.issued ?? null,
  });
  if (errors.length) return fail(422, errors);
  await putVote(parsed.bounty, { address: a, allocation: parsed.allocation, message, signature, issued: parsed.issued, recorded_at: new Date().toISOString() });
  return Response.json({ ok: true, tally: tally(await getVotes(parsed.bounty)) }, { headers: cors });
}
