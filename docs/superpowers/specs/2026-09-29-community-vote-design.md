<!-- NOT-ANNOUNCEMENT-COPY: internal design spec. Names no deadline anyone submits to. -->
# Community vote on bounty winners - design (awaiting Zaal's approval)

**Zaal's proposal, 2026-09-28:** entrants get votes from their past entries, cast them
quadratically, and comment on each other's submissions.

**Ruled, grill 2026-09-29 item 27** (`zao-vault decisions/grill-2026-09-29-grill-morning.md`,
commit c2f3f975): *"Hybrid: you shortlist, vote decides"*. Zaal shortlists; the community
quadratic vote picks the winner from the shortlist.

**Nothing is built, and no live round's text changes, before Zaal approves this spec.** Poidh
is parked until 6 October.

## Why these numbers, measured 2026-09-28 across all 9 ZAO bounties on poidh

37 people, 73 claims. With one credit per claim:

- **30 of 37** could never put more than one vote on a single entry, so the quadratic part
  would do nothing.
- **9 of 37** have more claims than rounds, so a credit per claim rewards claiming twice.

Hence credits per round entered, and more of them.

## The rules

1. **Credits: 10 per closed round entered.** One round gives 10 credits: 3 votes on one
   entry (9 credits), or 10 single votes. Five rounds give 50. Loyalty counts, but only by its
   square root.
2. **Cost is quadratic:** n votes on one entry cost n squared credits.
3. **Only rounds closed before this vote opened earn credits.** Nobody can farm the round being
   voted on.
4. **No voting on your own entry.**
5. **Identity is the claiming wallet.** A voter signs a message with the wallet their past
   claims came from. Agents vote the same way, as the entrants they are.
6. **Credits do not carry over.** Each vote starts from the voter's full balance.

## The flow for a round that uses it

1. **The round's text says so before it is cast.** It names the shortlist and the vote, and
   when each happens. No round already cast changes.
2. **The round closes.** Zaal publishes a shortlist of 2 to 4 entries with one line each on why
   they made it.
3. **The vote opens for 48 hours** on the entry's bounty page on poidhz.com. Each voter sees
   their balance, spends it across the shortlist, and signs.
4. **The vote closes.** The entry with the most votes wins. A tie goes to the entry Zaal ranked
   first on the shortlist, and the round text says so.
5. **Zaal accepts that claim on poidh.** poidh's own two-day contributor vote still follows,
   because the contract does it.

## Comments

Comments are Farcaster replies on each entry's cast in /zao, shown on the bounty page, which is
the same design as the site spec's threads. Commenting needs no credits.

## Things to watch, and what the design does about them

| risk | what it does |
|---|---|
| agents run by one operator voting as a bloc | the page shows every signed vote publicly, wallet by wallet; Zaal can void a bloc that coordinated, and the round text says so |
| regulars deciding everything | the square-root cost; the shortlist is Zaal's |
| very few voters | a round with fewer than 5 voters falls back to Zaal's first shortlisted entry, and the round text says so |
| a shortlisted entrant votes for themselves | refused by rule 4, enforced at signing |

## Data and build (after approval)

Supabase tables: `votes` (round, voter wallet, entry claim id, votes, credits spent, signature,
signed_at) and `shortlists` (round, claim ids in Zaal's order, published_at). Credits are
computed from poidh claims, never stored.

It needs the site's sign-in step, plus the Neynar and Supabase keys through `/secret`.

**Tests pin:**
- credit arithmetic
- the quadratic cost
- no self-vote
- no credit from the open round
- the tie-break
- the under-5-voters fallback

## Open for Zaal, each with a default

- **Shortlist size:** default 2 to 4.
- **Vote window:** default 48 hours after the shortlist is published.
- **Minimum turnout:** default 5 voters, otherwise his first pick.
