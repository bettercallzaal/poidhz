# Promise audit - R1 through R5

What each round's bounty text promised, against what was actually delivered. Run
2026-09-07 after R3 and R5 both turned out to have unkept public promises that nobody
noticed for months.

**Method.** Promises were read from the live on-chain description at
`poidh.xyz/base/bounty/<id>/data`, not from this repo's copies - the on-chain text is what
entrants actually agreed to and is immutable. Delivery was checked against the repo, the
722-message Zaal/Kenny Telegram history, and the Empire Builder leaderboard.

**A promise here means a sentence in the bounty text that commits us to do something after
the round closes.** Prize payment is one. So is a winner announcement, a pinned promo, a
leaderboard drop, a split.

## The result

| Round | Promises made | Kept | Broken or unmeasured |
|---|---|---|---|
| R1 (1151) | 1 | **1** | 0 |
| R2 (1166) | 4 | 2 | **2** |
| R3 (1180) | 4 | 2 | **2** |
| R4 (1249) | 3 | 1 | **2** |
| R5 (1330) | 3 | 1 | **2** |

**R1 is the only round that kept every promise it made** - and it is the round that promised
the least. Its entire commitment was "one winner takes the full pot", and the pot was paid
to @cryptfi-mariano. It made no promise about announcing, reposting, or crediting, so it
could not fail one.

Every round since has promised distribution on top of money, and **every single one has
delivered the money and not the distribution.**

## Round by round

### R1 (1151) - CLEAN

> "One winner takes the full pot - and the pot grows in real time as others contribute."

Paid, claim 6368, @cryptfi-mariano. Nothing else promised. Nothing else owed.

### R2 (1166) - two unkept

| Promise | Status |
|---|---|
| "One winner takes the full pot" | **KEPT** - claim 6645, @joeyofdeus, paid |
| "every submitter... lands on the leaderboard and gets boosted ZABAL drops" | **KEPT, late** - true today, but Empire Builder served a stale feed from at least 2026-08-08 until 2026-09-07 |
| "Winner announced via cast + X post by end of day Sunday May 24, 2026" | **NOT KEPT.** No announcement copy was ever drafted - `rounds/r2/` has no `cast-templates/` directory at all. The Telegram history shows Zaal still deciding the winner on 2026-05-27, three days after the promised announcement date, and telling Kenny privately rather than posting. No public announcement found. |
| "The winning clip will be reused as POIDH's pinned ad on @bettercallzaal channels" | **NO EVIDENCE.** Nothing in the repo records this happening. UNMEASURED rather than confirmed-broken - a pin is not visible from a terminal - but nobody wrote down that it was done. |

### R3 (1180) - two unkept

| Promise | Status |
|---|---|
| "Best one wins 0.0125 ETH on Base" | **KEPT** - claim 6749, femmie, 0.025 ETH paid (more than promised) |
| "Every submitter earns $ZABAL automatically via the slot 8 leaderboard" | **KEPT, late** - same Empire Builder gap as R2, and femmie in particular was absent from EB's feed entirely until 2026-09-07 |
| "Winner cast by end of day Monday June 15, 2026" | **NOT KEPT.** Copy exists at `cast-templates/winner-announce-femmie.md`, is filled in and marked READY TO SEND, and has never been posted. Nearly three months late. |
| "Winner clip becomes ZABAL Gamez's pinned promo across @bettercallzaal channels" | **NOT KEPT.** No record of it ever being pinned anywhere. |

### R4 (1249) - the honest failure, already documented

| Promise | Status |
|---|---|
| "the whole pot is split equally across every wallet that cleared the bar" | **NOT KEPT.** The bounty was accidentally **canceled** rather than withdrawn during closeout, which closed the on-chain claim path entirely. |
| "Every qualifying builder splits the pot equally in ETH on Base" | **NOT KEPT as stated** - 15 builders were credited a flat $ZABAL amount instead of an ETH split |
| "every submitter earns $ZABAL... this is BCZ POIDH round 4" | **KEPT** - the 15 offchain credits are in `org.config.json` and `rounds/r4/r4-empire-builder-upload.csv` |

R4 is the one failure that was written down honestly at the time, in
[`rounds/r4/CLOSEOUT.md`](../rounds/r4/CLOSEOUT.md). That is why it is the least bad of the
four - the people affected were told, and the substitute was actually delivered.

### R5 (1330) - two unkept

| Promise | Status |
|---|---|
| "Winner paid here within 48 hours" | **KEPT** - claim 7795 accepted, 0.0238 ETH |
| "the clip goes up on @wavewarz with your name on it" | **NOT KEPT.** Copy ready at `rounds/r5/winner-announce.md`, unsent. Zaal is posting it himself. |
| "WaveWarZ runs your clip on its official channels with your name on it" | **NOT KEPT** - same promise, stated twice in the text |

## What this means for R6 and R7

The failure is not carelessness about money. **Every winner got paid, every time, and R3's
winner got more than promised.** The failure is specifically in the promises that cost
nothing and have no deadline enforcing them - a post, a pin, a credit.

Three consequences, all already in the round docs:

1. **R6 and R7 both carry send gates** tying their outreach to R5's announcement going out
   first, because the same pattern would otherwise repeat a fourth time.
2. **Do not promise a pin.** Three rounds promised a pinned promo and no round has ever
   delivered one. Either stop writing it into bounty text, or make pinning part of closeout
   with someone's name on it. R6's text does not promise a pin.
3. **A promise with a date is checkable; a promise without one rots quietly.** R2 and R3
   both named a specific announcement date and missed it, which is at least visible. R2's
   pin promise had no date and simply evaporated.

## What would stop this recurring

`scripts/precast-check.py` checks whether a round is castable. Nothing checked whether a
round was **closed out** - so `scripts/postclose-check.py` now does, built the same day as
this audit.

```bash
python3 scripts/postclose-check.py --bounty 1330 --round 5
```

It reads the live on-chain description, confirms the payout, confirms the round is in
`default_bounty_ids` so its entrants actually score, checks that announcement copy exists at
all - R2's did not - and then lists every promise-shaped sentence as a checklist.

**Step four is deliberately not automated.** Whether a clip was posted on @wavewarz is not
knowable from a terminal, and a script that guessed would recreate the exact failure this
exists to catch: a confident "done" nobody checked. It tells you what you said you would do
and makes a human tick it off.

Run against the real rounds it reproduces this audit: R2 blocks on having no announcement
copy, R4 blocks as canceled, R5 flags that its winning wallet has no linked handle so it
cannot be credited by name from chain data alone.

## 2026-09-23 - THE $ZABAL PROMISE WAS KEPT, FOR THE FIRST TIME

Every round from R2 onward promised $ZABAL through the Empire Builder leaderboard and
delivered the ETH but not that. R3's winner announcement is still unsent. R5's winner was
paid 0.0238 ETH in early September and held **zero** $ZABAL seventeen days later.

On 2026-09-23 Zaal ran a distribution to **all 43 addresses on the leaderboard feed**.

**Transaction:** `0x4b795c5ea5b34da9f44613b81603a3893edc2d7fe9d48f503480be29699ede76`
(Base, block 51686953, status SUCCESS)

Decoded from the receipt rather than taken on trust:

- **43 ERC-20 Transfer events, 43 distinct recipients**, all of them $ZABAL
  (`0xbb48f19b...`)
- **111,012,370.81 $ZABAL** total
- **Four distinct amounts**, so the leaderboard score scaling applied rather than a flat split
- Reconciled against `data/leaderboard.json`: **43 on the feed, 43 paid, zero missed, zero
  extra**
- The five who were absent from Empire Builder's own list entirely - @leoxcrane, @predaking,
  @barsam, @assay, @mfa - **were all paid.** That set includes round one's winner and both of
  the only playable videos in round two.

**What this changes.** R1 is no longer the only round that kept every promise it made. It
also makes the line now cast into bounty 1412's immutable text true and checkable: "Every
submitter is added to the POIDH Submitters leaderboard on Empire Builder, which is how $ZABAL
has been distributed to this programme's entrants."

**Still owed, and not fixed by this:** R3's winner announcement (femmie, unsent since June)
and R5's (unsent 17 days). Money is not the same as credit, and those were promised
separately.

## 2026-09-25 - THE FEEDBACK PROMISE WAS KEPT, AND IT IS THE SECOND ONE EVER

Bounty 1412's immutable text promises, in the round that is still in its contributor vote as
this is written:

> *"Everyone who enters gets written notes on their own piece, win or lose. One thing it did
> and one thing to do better. They all go up at https://poidhz.com/feedback - every entrant
> gets their own page, and they are public so you can read what was asked of everybody else
> and not only of you."*

**That is now true.** Measured by HTTP at 06:5x on 2026-09-25, every page fetched individually:
**19 of 19 feedback URLs return 200**, covering all fifteen entrant pages across three rounds
plus the per-round indexes.

| Round | Bounty | Entrant pages live |
|---|---|---|
| One | 1409 | 5 |
| Two | 1410 | 6 |
| Three | 1412 | 4 |

**It was not true for most of a day, and the gap is the point.** Round two's and round three's
eleven pages were written, committed and pushed on 2026-09-24 - and returned a clean **404**
until PR #172 merged at 20:51 EDT that evening, because poidhz.com deploys from `main` and the
work sat on a branch. Written is not published. The check that caught it was fetching the URL,
not looking in the repo, and nothing in this repo had been doing that.

**What this makes two.** The $ZABAL distribution on 2026-09-23 was the first promise this
programme kept after five rounds of not keeping them. This is the second, and unlike the first
it is a promise about **attention** rather than money - the exact class the audit above says
rots quietest, because nothing enforces it and nobody is out of pocket when it lapses.

**Still owed, unchanged by this:** R3's winner announcement (femmie, unsent since June), R5's
(unsent), and **round one of the daily run has no winner announcement copy in any form** while
its winner has been paid since 2026-09-23. `postclose-check.py --bounty 1409` blocks on it.
Round one's cast text also promised, twice, *"Live on stream at 5pm Eastern, the same day it
closes."* That stream did not happen and is not yet answered publicly.

**Correction, later the same day:** round one's copy now exists, at
`rounds/daily/d01/winner-announce.md`, and it answers the missed stream head on rather than
omitting it. **It is written and unsent, which is exactly the state R3's copy has been in since
June.** Written is not posted, and this audit's whole point is that the two get confused.

## 2026-09-25 - ROUND FOUR IS CAST (1418), AND WHAT IT COMMITS US TO

Cast by Zaal at 14:46 EDT. **Bounty <https://poidh.xyz/base/bounty/1418>**, on-chain 432, OPEN,
**0.005 ETH at cast**. Verified against the chain with
`verify-cast-text.py --round rounds/daily/d04 --bounty 1418`: PASS at 6,720 characters, so the
promises below are quoted from text that is now immutable.

| Promise in the cast text | How it can be checked | Status |
|---|---|---|
| "Winner takes the whole pot" | the payout transaction | OPEN - closes Sun 27 Sep 5pm ET |
| "EVERYONE WHO ENTERS GETS WRITTEN NOTES... They go up at https://poidhz.com/feedback" | fetch each entrant URL and read the status code, per the 404 lesson above | OPEN |
| "I review every entry after the close and post the pick next week, during the week, on Firefly, everywhere at once, with the link" | a public post | OPEN, and deliberately undated - see below |
| "Every submitter is added to the POIDH Submitters leaderboard on Empire Builder" | the leaderboard feed against the claim list | OPEN, and the mechanism exists as of 2026-09-23 |
| "If your piece needs thirty to sixty seconds of me saying something... If there is time before the close I will record it" | conditional on being asked | OPEN, nobody has asked in two rounds |

**The announcement promise is soft on purpose and that is a trade, not a win.** Zaal, 2026-09-24:
*"dont say an annoucmenet date just say next week during the week"*. This audit's own finding is
that a dated promise is checkable and an undated one rots quietly. R2 and R3 broke dated
announcement promises; this one cannot be broken the same way, and it also cannot be held to.
His call, made knowing that.

**One number in the immutable text is already wrong, and it understates us.** The body says
*"Fifteen pages are up there now, covering all three rounds so far."* It was drafted on 09-24
when fifteen were live; by the time it cast on the 25th there were **19**, measured by HTTP.
Nothing can edit it. It is recorded here rather than quietly forgotten, because the rule this
repo keeps relearning is that a hand-carried count goes stale between drafting and casting -
three hand-counted lengths were wrong in the session that wrote this round.

## 2026-09-25 17:1x - THE $ZABAL FORK IS MOOT. IT WENT OUT AGAIN ON THE 24th.

This lane spent the session holding a decision for Zaal: top up 7,400,824.72 $ZABAL to 4
addresses, or send the full 118,413,195.53 to all 44. **Neither is needed. A second distribution
already happened**, and nobody in this repo knew until the chain was read.

Zaal's own words, relayed by the Dotfiles lane: *"we did one this morning i think"*. **The chain
says 2026-09-24 at 14:02 EDT**, which is the afternoon of the day before. His recollection was
right about the event and about 27 hours out on the timing, which is exactly why this was
measured instead of believed.

**Transaction:** `0x4467274beeb910643d2a2e767a84860a77521979e36acfaf94b4096337b714c2`
(Base, block 51741806)

Found by scanning **48 hours of $ZABAL Transfer logs from the distributing address**
`0xe0faa499d6711870211505bd9ae2105206af1462`, in 1,000-block chunks, blocks 51704413 to
51790813. The scan completed; a failed chunk would have made this UNKNOWN rather than "one
transaction".

| | 2026-09-23 | 2026-09-24 |
|---|---|---|
| Recipients | 43 | **44** |
| Total $ZABAL | 111,012,370.81 | **112,185,930.16** |
| Points on the feed | 60 | **64** |
| Per point | 1,850,206.18 | **1,752,905.16** |

**Is it the same mechanism as this repo's?** Yes, and the evidence is exact rather than
circumstantial:

- **44 of 44 addresses on `data/leaderboard.json` were paid. Zero missed, zero extra.**
- **Strictly proportional to score**: the per-point rate is identical across all 44 addresses -
  minimum, median and maximum are all 1,752,905.16, so max/min is 1.000000. Five distinct
  amounts for five distinct scores (1, 2, 3, 5, 6). That is `build-distribution.py --full`'s
  method, `total / sum(scores)`, arrived at independently.

**The four who earned since the 23rd were all paid in full.** Derived from the two transactions
rather than from the feed: three addresses went up a point (`0x5dc697f2` 5 to 6, `0x6dce11cc`
4 to 5, `0xb464fc1d` 2 to 3) and one address is new (`0x59733c7c`, @defifa, who claimed on
bounty 1412). 60 points plus 4 is 64. **That set of four is exactly the top-up this lane was
holding**, and it settled a day before anybody chose.

**The pot was smaller, not the method different.** The proposed full used the 09-23 rate carried
forward, 1,850,206.18 per point; the real one used 1,752,905.16. A pot chosen per distribution,
scaled pro-rata - which is his call to make and needs no reconciliation.

**What is still UNKNOWN and is not needed for this conclusion:** the dollar figures in the
ZABAL app's history (weighted $10.06 one day ago, $10.22 two days ago). The only DEX pair for
this token returns zero price and zero liquidity, so no USD conversion is quoted here. The rows
line up with these two transactions by count and by day; that is a match on shape, not a proof,
and nothing above rests on it.

**What this changes in the ledger:** the $ZABAL fork closes as ANSWERED BY ACTION, not by
decision. It is the third promise this programme has kept, and the first one it kept twice.
