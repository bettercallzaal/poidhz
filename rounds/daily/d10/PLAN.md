<!-- NOT-ANNOUNCEMENT-COPY: internal plan. Names no deadline anyone submits to. -->
# Round ten plan - the $1,000 buy on WaveZStation, and the reaction bounty around it

Status 2026-10-10: PLAN, nothing fired. **Zaal ruled Q1 in the Grill at 18:27Z (vault `decisions/grill-2026-10-09-seat-morning.md`, items 96 and 97): two buys of $500, not one of $1,000, "if we need to split the top prize", and "save this for this week". Everything below is rewritten to that ruling. Q2 ruled at the same sitting (items 98 and 99): DM before the buy, he sends it. Q3 was not picked; he typed "Maybe we say best marketing rollout give it a month and people have to sign up", which reshapes the round. The redraft is `REDRAFT-v3.md` beside this file, with three questions; nothing fires until he rules on it.** Every figure here comes from `RESEARCH.md` in this
folder, which names the surface and the clock time for each one. The four gates are Zaal's:
the $1,000 and the wallet that sends it; the message to the artist; every post; the cast.

## The idea in one paragraph

Zaal makes two buys of $500 on wavezstation.com this week. Default: both into the most-funded song.
His ruling keeps the second $500 free to go to the second artist instead, "if we need to split the
top prize". On the site's fixed split each $500 buy sends $225 to the song's creator wallets in the
same transaction, $50 to the platform, and $225 into the song's fan pool for earlier supporters to
claim. The first $500 alone makes Saturday in LA the first song on the site past $1,000 in sales
(about $802 sold before it). If the second $500 goes to AI LUI instead, that song passes $1,000 too
(about $587 sold before it), and the site gets its first two four-figure songs on the same day.
The "first four-figure single buy" line is dropped: no one transaction is four figures any more. Then the
poidh round that Zaal asked for on 6 Oct runs on that song: buy in for a dollar, film yourself
hearing it, best reaction wins the pot. The buy is the news; the round is how people find it.

## Who, measured

At 16:02:43Z on 10 Oct the most-funded song was **Saturday in LA by BennyJ504** (fan pool
360.80 USDC, 14 supporters; `@bennyj504` on X per the song's own record). Second was AI LUI at
264.00. The artist is fixed at the moment of the buy, not now: whoever leads `/api/discover?
sort=funded` when Zaal opens the page is the one. If it is still Saturday in LA, the pitch and
the copy are already written for it. If it has changed, the pitch is re-addressed and this lane
re-reads the song's creator wallets before anything goes out.

## Mechanics, in order

| Step | What | Whose hand | Public? |
|---|---|---|---|
| 1 | Send the artist the pitch (`ARTIST-PITCH.md`). It says what is coming, asks who owns the second creator wallet, and asks for three things in return. | Zaal | no, a DM |
| 2 | Buy 500 USDC of the most-funded song from the issuer wallet `0x7234c36a71ec237c2ae7698e8916e0735001e9af`, through wavezstation.com. Then the second 500 USDC: same song by default, or the second artist if he wants the prize split. Both this week. | Zaal | yes, the instant each lands |
| 3 | Paste both transaction hashes into `description.md` where it says `BUY_TX_HASH_1` and `BUY_TX_HASH_2`, and the amount that landed on the round's song where it says `BUY_AMOUNT` (five hundred, or a thousand), then cast the OPEN bounty with $100 in the reward field. | Zaal | yes |
| 4 | Post block 1 of `ANNOUNCE.md` from Firefly (Farcaster /zao and X) with the Basescan link and the poidh link. Tag the artist. | Zaal | yes |
| 5 | Round runs to 11:59pm Eastern, Saturday 31 October 2026. Zaal picks the following week; contributors vote two days; pot pays out. | Zaal picks; this lane drafts the notes | yes |

Steps 1 and 2 can swap if Zaal wants the artist to find the money before he hears from us. This
lane's default is pitch first, because $225 arriving unexplained in two wallets is a strange
first contact. If the second $500 goes to a second artist, that artist gets the same DM with the
numbers halved, and the announcement names both.

## What each $500 buys

| | USDC | Where it goes |
|---|---|---|
| Platform fee | 50 | WaveZStation wallet, same transaction |
| Creators | 225 | the song's creator wallets, same transaction. Saturday in LA has two at 50/50, so 112.50 each. Who owns the second one is an open question in the pitch. AI LUI has one creator wallet, so 225 to it. |
| Fan pool | 225 | retained by the contract for the earlier supporters, pro rata. On Saturday in LA Zaal is one of them with 170 in, about 21% of what the song has sold, so roughly 48 of this 225 is his to claim back on the first buy and a larger share on a second buy into the same song. |

Two buys on the same song: $450 to the creators, $100 platform, $450 fan pool, of which about $120 is Zaal's own claimable share (21% of the first $225, then about 37% of the second), net cost about $880. Split across the top two songs: $225 to each song's creators, $100 platform, about $48 back to Zaal from Saturday in LA and nothing from AI LUI unless he already holds some of it (UNVERIFIED), net cost about $950. These are the site's stated split
and the chain's observed behaviour; the fan-pool formula sits in unverified bytecode and is an
estimate (RESEARCH.md section 2).

## The bounty

- **Type:** OPEN, reward field $100 (0.0399 ETH at 2,506.72 USD per ETH, Coinbase 16:06Z). The
  text names no amount, per the repo rule.
- **Ask:** buy at least one dollar of the song, film yourself hearing it start to finish, post
  it, claim with one frame plus the links. The shape is PR #236's, which Zaal asked for on 6
  Oct, now pinned to one song.
- **Close:** 11:59pm Eastern, Saturday 31 October 2026 (Zaal, 7 Oct: "keep this as a til the
  end of the month of october as a test one first").
- **Judging:** Zaal picks with the entries in front of him; contributor vote confirms; every
  entrant gets one note back.
- **Promise:** the pot and nothing else. No publication promise.
- **Disclosure, in the text and in numbers:** Zaal held about 21% of this song's fan pool before
  these buys. After them he holds about 65% if both $500 land on it ($1,170 of about $1,802 sold) or
  about 51% if one does ($670 of about $1,302), so between 23 and 29 cents of each dollar an entrant
  spends on it is claimable by him. The text says so under THE REWARD. Hiding it is the one thing
  that could turn the round into a story about us instead of the artist.

## How the artist is credited

- Named in the bounty title and text, with the X handle the site lists for him.
- Named and tagged in the announcement, which links the Basescan hash so the $450 is checkable
  by anyone.
- The pitch offers him the "first song past four figures on WaveZStation" line to use himself,
  with the hashes, and asks him to post the song and the bounty to his own people.
- Every reaction video in the round names the song and the artist out loud and on screen
  (rule 4 of the text).

## Verification by hash

Two Basescan links do the whole job: `https://basescan.org/tx/<hash>` for each buy. The token
transfers on each page show 500 USDC from the issuer wallet into `0x6eee...b255`, then 50 out to
`0xd974...8E72` and 112.50 and 112.50 out to the two creator wallets (or 225 to AI LUI's one).
Anyone can check it in thirty seconds. The announcement links it; the bounty text links it; the pitch promises it. The
issuer wallet's two earlier buys on the same song (100 and 70 USDC, Sep) are on the same
explorer page, so the "already the biggest supporter" line is also checkable.

## What is public, and when

| Moment | Public surface |
|---|---|
| The buy lands | basescan.org, immediately, whether or not anyone posts |
| The cast | poidh.xyz bounty page, and poidhz.com/b/<id> after the record PR merges |
| The announcement | Farcaster /zao and X from Zaal's account, then the artist's own post if he makes one |
| The round | every entry is a public video by its own rule |
| The pick | poidh accept, two-day contributor vote, payout on chain |

The pitch, this plan and the research memo stay in the repo (public repo, so "private" means
"not promoted", not secret). Nothing in them is a secret: wallets, hashes and splits are all
on chain already.

## What could go wrong

- **The top song flips before the buy.** AI LUI trails by about 215 USDC of sales. Re-read
  the discover endpoint at the moment of the buy; the copy is re-addressed if it moved.
- **The second creator wallet is not the artist.** Then the honest line is "$450 to the
  song's creators", and the pitch already asks.
- **A buy cap.** No ceiling is visible in the site data, and 500 is five times the largest buy
  on record (Zaal's own 100). If the UI refuses 500, four buys of 250 land the same money.
- **Entrants balk at paying a dollar.** No prior round cost the entrant money. If the first
  week draws nothing, the fallback is a sibling bounty with the buy optional, which the text
  does not promise.
- **The disclosure line gets cut.** This lane recommends it stays. The number is small and the
  trust is not.

## Auto-proceeded choices in this PR (one line each)

1. Pinned the round to one song instead of "the top song that day" (PR #236's rule 7), because
   the buys fix which song the round is about. If the second $500 goes to a second song, the
   round still pins to the most-funded one.
6. Read "split the top prize" as "the second $500 may go to the second artist", decided at the
   buy, with same-song as the default. The ruling does not say which; this is the reading.
7. Read "this week" as the week starting Monday 12 October, since he ruled it on Saturday the 10th.
2. Kept the 31 October close and the $100 reward from #236; nothing new was ruled.
3. Default order: pitch, buy, cast, announce.
4. Default sending wallet: the issuer wallet, because its prior buys are already public.
5. Wrote the fan-pool numbers as estimates and said why.
