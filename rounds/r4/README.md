# R4 - The ZABAL Gamez open pot (OPEN-SPLIT) - CLOSED, CANCELED AT CLOSEOUT

**This round did not execute as designed below.** Cast 2026-06-15 as an OPEN-SPLIT POIDH
bounty (the mechanic this file describes). At closeout on 2026-08-05, the bounty was
**accidentally canceled** instead of resolved through the intended vote/disperse path - see
[CLOSEOUT.md](CLOSEOUT.md) for the full story. The escrowed 0.0138 ETH was reclaimed to the
treasury, not distributed, and the reward pivoted to a $100 equal-share $ZABAL credit paid
through Empire Builder instead of a POIDH-native split. **Read CLOSEOUT.md first** - the rest
of this file (Status, Still open, Run-the-window checklist below) describes the ORIGINAL plan,
kept for the design record, not what actually happened.

POIDH bounty [1249](https://poidh.xyz/base/bounty/1249) on Base.

A new bounty type: **OPEN-SPLIT**. One pot, split equally across every builder who ships a
real project during ZABAL Gamez July open build month and posts a POIDH proof photo. Not a
single-winner ad bounty - the participation reward for the whole July cohort.

## At a glance

- **Bounty:** https://poidh.xyz/base/bounty/1249
- **Type:** OPEN-SPLIT (open contributions all month + equal split across all qualifiers)
- **Campaign:** ZABAL Gamez Season 1 - July open build month
- **Claim:** a photo of you at your computer/phone with your build up + a link to the build
- **Prize:** the whole pot, split equally across every qualifying builder (in ETH on Base)
- **Pot:** seeded by Zaal now, topped up weekly, OPEN so anyone can stack contributions
- **Issuer:** BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af`
- **Payout path:** Option B - non-issuer distributor wallet wins the vote + disperses equal shares (see MECHANIC.md)
- **Window:** build + submit July 1-31, 2026
- **Closes:** 11:59pm PT, Friday July 31, 2026
- **Payout:** first week of August, before the Finals
- **Relationship to August:** the curated August prize goes to a picked few; this pot goes
  to everyone who participated, picked or not

## Files in this folder

- `description.md` - the POIDH Description field as posted (copy-paste clean)
- `MECHANIC.md` - **read this first** - how the split actually pays out + the open decisions
- `promo-cast.md` - launch cast (Farcaster + X + Telegram) + reminder casts

## Why this is different from R1-R3

| | R1-R3 (ad bounties) | R4 (open pot) |
|---|---|---|
| Winners | one | everyone who qualifies |
| Judging | scorecard, best wins | pass/fail floor, no ranking |
| Reward | fixed prize to winner | whole pot split equally |
| Pot growth | OPEN (others can stack) | OPEN (others can stack) - core to the idea |
| Claim | the ad asset | proof photo + link to the build |
| Point | best promo for the campaign | reward participation in the build month |

## Status (original plan - superseded, see CLOSEOUT.md for what actually happened)

- [x] Payout path - **LOCKED: Option B, distributor disperses** (2026-06-15) - never executed; see closed decisions in CLOSEOUT.md
- [x] POIDH OPEN bounty cast on Base - [bounty 1249](https://poidh.xyz/base/bounty/1249) (2026-06-15)
- [x] Bounty id 1249 added to `scripts/refresh-poidh-leaderboard.py` defaults
- Live check 2026-07-08: 2 claims so far (0.0138 ETH escrowed) - window still open through Jul 31, so this is a mid-month snapshot, not a final count. Both claims were the same wallet - individual POIDH claims never really came in, which is part of why closeout ended up handled manually (CLOSEOUT.md).

## Originally still-open items - all moot now (CLOSEOUT.md "Closed decisions")

None of these were resolved via the plan below - they became moot when the bounty was
accidentally canceled at closeout and the reward pivoted to a flat $ZABAL credit per builder:

- ~~Name the distributor wallet~~ - moot, no vote/disperse happened
- ~~Set the weekly top-up size~~ - moot
- ~~Decide the min-builders floor~~ - moot, 15 real builders shipped regardless
- ~~Name the pass/fail "real build" checker~~ - moot, resolved case-by-case at closeout instead
- ~~Decide how post-deadline contributions are handled~~ - moot, no ETH pot being split

## Run-the-window checklist (as planned - did NOT run this way, see CLOSEOUT.md)

- [ ] Cast `promo-cast.md` on /zabal + /poidh + /zao with the bounty URL as embed
- [ ] Pin in /zabal for the whole window
- [ ] Firefly cross-post to X
- [ ] Weekly: top up the pot + reply-cast the running "$X in pot, N builders in" count
- [ ] Day 15 + day 25: reminder casts
- [ ] Fri Jul 31: close. First week of Aug: finalize qualifiers -> distributor wallet wins
      the vote + withdraws -> disperse equal shares -> cast the payout + tx hashes

  **Did not happen this way** - see CLOSEOUT.md: the bounty was accidentally canceled
  instead, the escrowed ETH was reclaimed (not distributed), and the reward became a $100
  equal-share $ZABAL credit via Empire Builder for the 15 qualifying builders instead.
- [ ] Run `scripts/refresh-poidh-leaderboard.py` to fold R4 submitters into the leaderboard

## Related rounds

- [R1 - Hannah Ep 17 clip-up](../r1/)
- [R2 - Best 60s POIDH ad from Ep 19](../r2/)
- [R3 - Best ad for ZABAL Gamez](../r3/)
