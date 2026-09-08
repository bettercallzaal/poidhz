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
