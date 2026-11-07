<!-- NOT-ANNOUNCEMENT-COPY: internal plan for poidhz. Names no deadline anyone submits to. -->
# Higher on the poidh leaderboard, by doing more for the poidh community

Zaal, 6 Nov 2026, seat pane (recorded in the seat's status file at 10:41 EST): *"lowkey wanna get
higher on poidh leaderboard, lets make poidhz about doing more for the poidh community"*.

**The rule for every step below: each bounty funded, joined, claimed, accepted or resolved is
Zaal's own tap.** This plan builds pages and scripts. It never sends ETH, signs, casts or posts.

## 1. Where he stands - measured 6 Nov 2026, 17:03 EST

Source: poidh's own API, `https://poidh.xyz/api/trpc/leaderboard.fetch`, the call behind
poidh.xyz/leaderboard. Input: `userAddress` = `0x7234c36a71ec237c2ae7698e8916e0735001e9af`, the
issuer of his Singapore bounty 1536 (read from `bounties.fetch` for id 1536, chain 8453).

| | |
|---|---|
| Rank | **47** (the API's `userData.rank`) |
| Score | **223** = Base 179 + mainnet 44 (Degen 0, Arbitrum 0) |
| Board size | 100 rows (10 pages of 10; `totalUsers: 100`) |

This matches his own paste that morning (rank 47, 223 points), so the score did not move during
the day.

**The gaps above him** (same call, all 10 pages read, 100 rows):

| Target | Score there | Points needed |
|---|---|---|
| Rank 46 | 227 | +4 |
| Rank 40 | 256 | +33 |
| Rank 30 | 321 | +98 |
| Rank 25 | 439 | +216 |
| Rank 10 | 1,000 | +777 |

Ranks 40 to 47 sit inside 33 points of each other. A small amount of real activity moves him
several places.

## 2. What the score counts - read from poidh's source, 6 Nov 2026

Source: `picsoritdidnthappen/poidh-app`, branch `prod`, `src/trpc/routers/accounts.ts`
(last changed in commit d170649f, 8 Oct 2026), lines 14 to 35, used by
`src/trpc/routers/leaderboard.ts`:

```
per ETH chain (Base, Arbitrum, mainnet):  1000 x (ETH earned + ETH paid) + 10 x claim NFTs held
Degen:                                    (DEGEN earned + DEGEN paid) / 500 + 10 x claim NFTs held
total = the chain scores + manual extraPoints (the usersExtra table)
```

What that means for him:
- **1 point is 0.001 ETH earned or paid out, or one tenth of a claim NFT.** Rank 40 (+33) is
  about 0.033 ETH paid or earned, or 4 claim NFTs.
- **Money sitting in an open bounty scores nothing.** accounts.ts counts in-progress
  participations separately, as "amount in contract", not in the score. That is why casting and
  funding 1536 left him at 223 (measured: 223 at his morning paste and at 17:03 EST).
- **The manual extraPoints explain the odd rows.** Rank 28 totals 354 with chain values summing
  to 54, and ranks 59 and 60 show 200 with every chain at 0. Who assigns extraPoints, and for
  what, is not in these two files.

Not read: the indexer that fills the leaderboard table, so which wallet is credited with "paid"
when a multiplayer bounty pays out by vote is UNKNOWN. The rank log (step 1) shows it the first
time one of his completes.

## 3. The moves, in order

### Step 1 - a daily rank log (code, no money)
A script, `scripts/poidh-rank-snapshot.py`, that calls `leaderboard.fetch` for his address and
appends `{date, rank, total, per-chain}` to `data/poidh-rank.json`, run from the existing
`refresh-leaderboard.yml` job. It refuses to write a rank when the call fails or returns no
`userData` (prints UNKNOWN, keeps the last good row) - never a zero.

**Why first:** the formula is known, but which wallet gets credited for what is not. One
snapshot before and after each of his taps shows it.

### Step 2 - close what is already his (his taps)
List every open bounty he issued, on every chain, with its claims and its vote state, as one
table in `docs/`. Completions look like what the board counts, and an open bounty with an
unjudged claim is points and a paid community member both waiting on him.

### Step 3 - resolve the stuck votes, community-wide (his taps, no money)
poidh votes do not auto-resolve: after the deadline anyone can call `resolveVote`, and until
someone does, nobody is paid. A page on poidhz listing **every** poidh bounty whose vote has
ended but not been resolved, any issuer, is a direct service to the community: each row is
people waiting for money. He calls them from his wallet; poidhz only lists them. Calling
`resolveVote` is not in the formula, so it earns him no points directly; it is service.

### Step 4 - the community pieces already planned
`docs/community-plan.md` (26 Sep) already holds the build list. Two of its items now serve the
leaderboard goal as well:
- **`/rounds.json` and `/llms.txt`**: most entrants are agents, and agents poll. More entrants on
  his bounties means more completions.
- **A page per person** (`/people/<handle>`): it credits the returning entrants, who are the
  people who complete his bounties.

### Step 5 - fund and claim other people's bounties (his hand, money)
Joining other issuers' bounties counts as "paid" once they pay out, and claiming bounties he can
honestly complete counts as "earned" plus the claim NFT, by the formula in section 2. They are money and on-chain, so this plan only
proposes them: a short weekly list of open poidh bounties that fit him, with the pot and the
deadline, for him to pick from. No auto-funding, no auto-claims.

## 4. The Congress bounty, 1536 - how it can be claimed

Bounty 1536 is poidh's on-chain bounty 550 on the Base contract
`0x5555fa783936c260f77385b4e153b9725fef1719` (the `mainContract` for Base in poidh-app
`src/utils/config.ts`). Read with `cast call bounties(550)` on 6 Nov: issuer
`0x7234c36a...e9af`, 0.05 ETH, claimer `0x0` (still active).

**His casting wallet cannot claim it.** `picsoritdidnthappen/poidh-v3`, `src/PoidhV3.sol` line
569 (main, commit a0a6a104): `if (msg.sender == bountyIssuer) revert IssuerCannotClaim();`.
Checked against the live contract on 6 Nov with a read-only `eth_call` of `createClaim(550, ...)`:
from his wallet it reverts with `0x8f60bb0a`, which is `IssuerCannotClaim()`; from another
address the same call does not revert. No transaction was sent.

**So the claim path is a second wallet of his**, with a comment on the bounty saying the
claiming wallet is his, so backers can see the money goes where the page says. Per the formula,
the "earned" points and the claim NFT then sit on that second wallet, not on 0x7234. Which
wallet, when, and the comment text are all his.

## 5. What this PR is

This document only. Each step above lands as its own held PR, in order, after he says which to
start. The default if he says nothing: step 1, the rank log, because it needs no money and
everything else is measured by it.
