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

## 2. What the score counts - partly UNKNOWN

What is known:
- The page describes itself as *"who's leading in bounty completions and earnings across all
  chains"* (its meta description).
- The score is split per chain (Base, Degen, Arbitrum, mainnet) plus a total.
- **Casting and funding an open bounty did not move his score.** Bounty 1536 was cast about 10:41
  EST with the 0.045 ETH seed; at 17:03 the score was still 223. (poidh's `amount` for 1536 read
  0.05 ETH at 17:03, so about 0.005 ETH has joined since the seed.)

What is not known:
- **The formula.** For some rows the chain columns do not add up to the total: rank 28 shows a
  total of 354 with chain values summing to 54, and ranks 59 and 60 show 200 with every chain at
  0. So there is a component that is not shown per chain. Not read: poidh's server code or docs.
- Whether the points come from completions as issuer, as claimant, or both; and whether the unit
  is USD, ETH or a count.

**Prediction, not a finding:** points arrive when a bounty completes (a claim accepted or a vote
resolved), not when it is funded. It rests on one observation: funding 1536 left the score at 223.
Step 3 is what tests it.

## 3. The moves, in order

### Step 1 - a daily rank log (code, no money)
A script, `scripts/poidh-rank-snapshot.py`, that calls `leaderboard.fetch` for his address and
appends `{date, rank, total, per-chain}` to `data/poidh-rank.json`, run from the existing
`refresh-leaderboard.yml` job. It refuses to write a rank when the call fails or returns no
`userData` (prints UNKNOWN, keeps the last good row) - never a zero.

**Why first:** every later move is a guess until a log shows which of his actions moved the
number. One snapshot before and after each of his taps answers section 2.

### Step 2 - close what is already his (his taps)
List every open bounty he issued, on every chain, with its claims and its vote state, as one
table in `docs/`. Completions look like what the board counts, and an open bounty with an
unjudged claim is points and a paid community member both waiting on him.

### Step 3 - resolve the stuck votes, community-wide (his taps, no money)
poidh votes do not auto-resolve: after the deadline anyone can call `resolveVote`, and until
someone does, nobody is paid. A page on poidhz listing **every** poidh bounty whose vote has
ended but not been resolved, any issuer, is a direct service to the community: each row is
people waiting for money. He calls them from his wallet; poidhz only lists them. Whether a
resolve earns him any points is UNKNOWN until the rank log shows it.

### Step 4 - the community pieces already planned
`docs/community-plan.md` (26 Sep) already holds the build list. Two of its items now serve the
leaderboard goal as well:
- **`/rounds.json` and `/llms.txt`**: most entrants are agents, and agents poll. More entrants on
  his bounties means more completions.
- **A page per person** (`/people/<handle>`): it credits the returning entrants, who are the
  people who complete his bounties.

### Step 5 - fund and claim other people's bounties (his hand, money)
Joining other issuers' open bounties and claiming bounties he can honestly complete are the moves
most likely to count, by the meta description. They are money and on-chain, so this plan only
proposes them: a short weekly list of open poidh bounties that fit him, with the pot and the
deadline, for him to pick from. No auto-funding, no auto-claims.

## 4. What this PR is

This document only. Each step above lands as its own held PR, in order, after he says which to
start. The default if he says nothing: step 1, the rank log, because it needs no money and
everything else is measured by it.
