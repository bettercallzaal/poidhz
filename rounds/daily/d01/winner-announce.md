# Round one - winner announcement, UNSENT

**NOTHING HERE HAS BEEN POSTED.** Zaal posts. Written 2026-09-25.

**This is overdue and the copy says so.** Bounty 1409 closed 2026-09-21 at 4pm Eastern. The
contributor vote resolved and **@leoxcrane was paid 0.0061 ETH on 2026-09-23**, verified on
chain (`postclose-check.py --bounty 1409` reports the payout against claim 8086). Nothing has
been said publicly in the four days since. `postclose-check` has been BLOCKING on the absence
of this file the whole time.

**It also has to answer a broken promise.** Round one's cast text says, twice and immutably:
*"Live on stream at 5pm Eastern, the same day it closes. Zaal picks it out loud with the
entries on screen."* There was no stream. Round three's text already apologised for the round
two version of this; round one's has never been addressed at all.

## Verified before writing

| Claim | Source |
|---|---|
| Winner @leoxcrane, claim 8086 | `claims.fetchBountyClaims`, `isAccepted` true |
| 0.0061 ETH paid | on-chain, via `postclose-check.py` |
| Cast at 0.004 ETH | `rounds/daily/d01/README.md` - recorded at cast on purpose |
| Pot grew 53% while open | 0.004 to 0.0061 |
| Six entries | `claim-report.py --bounty 1409` |
| Feedback live for all five other entrants | 19 of 19 URLs returned 200 on 2026-09-25 |

The winning piece: a poster built entirely from the kit. Downeast Maine, free, all ages, the
real moose mark, Saturday October 3 2026, Franklin Street Parklet, Ellsworth Maine, music noon
to six, rain or shine, outdoors, **all eight acts named**, and zaostock.com. It is the most
fact-complete thing anyone has made across three rounds.

## Block 1 - the announcement

```
ZAOstock bounty one is settled. @leoxcrane won it and has been paid.

The piece is a poster built entirely out of the free brand kit, and it carries every fact a stranger needs without being asked to: Downeast Maine, free, all ages, Saturday October 3, Franklin Street Parklet in Ellsworth, music noon to six, rain or shine, outdoors, all eight acts by name, and the URL. Three rounds in, nothing else has been that complete.

The pot was 0.004 ETH when it was cast and 0.0061 ETH when it paid out. It grew 53% while the round was open, because anyone can add to an open bounty and people did.

I owe everyone an apology on this one. The bounty text said the winner would be named live on stream at 5pm the day it closed. There was no stream, and instead of saying so I said nothing for four days while the winner was already paid. That is the second time this programme has promised a stream and not run one, so I am going to stop writing it into bounties until I have actually done it once.

All six entries got written notes and they are public: https://poidhz.com/feedback/1409

https://poidh.xyz/base/bounty/1409
```

## Block 2 - reply under @leoxcrane's own post

His entry: https://farcaster.xyz/leoxcrane/0xccd03ab2

```
This won round one and the 0.0061 ETH is already in your wallet.

It is still the most complete piece anyone has made for ZAOstock - every fact on the poster, all eight acts named, nothing a reader has to go and look up.

Your notes are at https://poidhz.com/feedback/1409/leoxcrane if you want them. There is another round coming and I would like you in it.
```

## Block 3 - the short one

Measured: **232 characters of text**, 267 of 280 with a 34-character URL. Fits with 13 to spare.

```
ZAOstock bounty one is settled. @leoxcrane won with a poster carrying every fact - all eight acts, free, noon to six, the street, the date.

Pot grew 53% while it was open, 0.004 to 0.0061 ETH.

Notes for all six entries are public.
```

## What this deliberately does not do

- **It promises nothing.** No pin, no repost, no "we will run this on the channels". Five
  rounds of that are in `docs/PROMISE-AUDIT.md` and every one is still unkept.
- **It does not name a date for anything.**
- **It does not say the stream is coming.** It says the opposite: no more stream promises until
  one has actually happened. That is the only version of this that is not a sixth promise.
- **It does not say round four is open**, because it is not cast. An earlier draft of block 2
  did. A winner announcement that points at a bounty nobody can enter is the same class of
  error as the rest of this file - saying a thing before it is true.
- **It does not use the winner's reply to point at other entrants' mistakes.** The first draft
  noted that people are still leaving the word FREE off, which is true, and putting it in a
  congratulation makes the message about somebody else. That belongs in their own notes, where
  it already is.
