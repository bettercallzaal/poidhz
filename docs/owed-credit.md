<!-- SEND-GATE: round=5 -->

# The credit this programme owes, and the copy to close it

**DRAFT, unsent. Outbound is Zaal's tap.** Nothing here has been posted.

Seven promises across R2, R3 and R5 are recorded broken or unrecorded in the round ledgers.
**Every one of them is a publication promise** - announce, pin, run the clip, credit the
person. Not one is a payment. Every winner was paid, on time, on chain, and can prove it.

That is the whole shape of the failure: what rots is the part that costs nothing and has no
deadline forcing it. R1 is the only round that kept every promise, and it is also the only
round whose entire commitment was the pot.

**Why this file exists rather than three separate announcements.** R2 closed 22 May and R3
closed 14 June. A cast today that reads like a timely winner announcement is a second false
claim on top of the first. A single post that says "we owe these people credit and here it
is" is true, is shorter, and closes four promises at once.

## Order. This matters more than the copy.

1. **R5's winner announcement goes first** - `rounds/r5/winner-announce.md`, already drafted.
   Kenny endorsed @wimpydwi himself on 2026-09-02 and believes R5 closed cleanly. Anything
   else that goes out before it pitches a new round while the last one he blessed is an
   unkept promise he does not know about.
2. **Then this post**, which closes R2 and R3.
3. **Then the two pins**, which are one click each and are what was actually promised.

`scripts/send-gate.py --all` holds the R6 note, the wimpydwi retainer and the launch post
until R5's promises are recorded kept. This file carries the same gate.

## Verified facts. Do not restate these from memory.

Read from `data/audit.json` and `data/rounds-live.json` on 2026-09-09, both regenerated from
chain on the 6h refresh.

| | R2 (bounty 1166) | R3 (bounty 1180) |
|---|---|---|
| Closed | 22 May 2026 | 14 June 2026 |
| Paid | 0.0105 ETH | 0.025 ETH |
| Claims | 8 | 8 |
| Winner | @joeyofdeus, claim 6645 | @femmie, claim 6749 |
| Wallet | `0x6dce11cc9bba17d3c1ef60c26f0958300bb06953` | `0xc143cf8515b87ea88d8db8a9892639b5046cf81c` |
| Winning entry | "Real-world coordination shouldn't require permission." | "ZABALGAMEZ.COM AD" |
| Link | https://x.com/i/status/2057966595029319888 | https://x.com/femmie/status/2065083051714003291 |
| Also on Farcaster | - | https://farcaster.xyz/femmie/0xd42f8ee9 |

**Never assume femmie's gender.** Handle, or they/them. femmie won in June, was paid, was
never announced, and was missing from Empire Builder until 2026-09-07 - three uncredited
things for one person, which is why `rounds/r3/cast-templates/femmie-dm.md` asks rather than
decides. Send that DM before or with this post, not after.

**The R2 link is the anonymous `/i/status/` form**, which does not name its author. The
handle comes from the leaderboard's wallet mapping, not from the URL. If you want the
handle-form link, open it before posting - do not construct one.

## The post

Short on purpose. It is a correction, not a victory lap.

```
Two BCZ POIDH winners were paid months ago and never got the post that was promised
with the money. Fixing that now rather than quietly leaving it.

R2, May - @joeyofdeus, "Real-world coordination shouldn't require permission."
0.0105 ETH, 8 entries.
https://x.com/i/status/2057966595029319888

R3, June - @femmie, the ZABALGAMEZ.COM ad. 0.025 ETH, 8 entries.
https://x.com/femmie/status/2065083051714003291

Both are getting pinned, which is what the bounties actually said. Late is worse
than on time and better than never.

Every submitter to these rounds is on the leaderboard: poidhz.com/hub
```

Farcaster: same text. It is already short enough and the /poidh channel is the right room.

## The two pins

The bounty text promised a pin for both rounds. A pin is not visible from a terminal, so
nobody but a person at the account can do this or confirm it.

- [ ] R3 winner pinned across @bettercallzaal channels ("becomes ZABAL Gamez's pinned promo")
- [ ] R2 winner reused as the pinned ad ("will be reused as POIDH's pinned ad")

Only one thing can be pinned at a time per account, and the promises predate each other. If
both cannot stand, pin R3's - it is the one promised twice, in two separate sentences of the
same description.

## What to record afterwards, and where

Not in this file. In the ledgers, which are what `postclose-check.py --all` reads on the 6h
cron:

```
rounds/r2/closeout.json   winner announcement -> kept, with the post URL as evidence
rounds/r3/closeout.json   winner cast + both pin promises -> kept, with URLs
```

Set them **by hand with evidence**. A terminal cannot see a post, and a script that guessed
would recreate the exact failure this whole file exists to close: a confident "done" that
nobody checked.

Once R5's ledger is recorded kept, `send-gate.py --all` opens the three drafts it is holding.
