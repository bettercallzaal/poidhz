# R6 - NYC trip recap, 60 seconds (DRAFT, not cast)

Not live. No bounty ID yet. Zaal's call 2026-09-06, replacing the WaveWarZ clip round that
had held the R6 slot - that round is written, passes the validator, and now waits as
[R7](../r7/).

> "recap my trip to nyc in a video max 60 seconds with the most info from it, i can provide
> a drive link with all the files it can go til the end of the month but the submissions
> that come in sooner have more likelihood to be posted, but i want to post multiple to
> multiple socials so if you dont win the contest, if i use your content ill send $5 in
> zabal tokens"

## Two blockers before this can cast

Both are Zaal's and neither is optional.

1. **The Drive link.** `description.md` carries `<DRIVE-LINK>` in three places. Without the
   footage there is no bounty at all.
2. **What the trip actually was.** `<WHAT-THE-TRIP-WAS>` is the only paragraph that tells an
   editor what story they are cutting. Everything else in the description is structure. Two
   or three sentences: what the trip was for, who was there, what happened that mattered.
   A round that ships without this asks strangers to find a story in someone else's holiday
   footage, which is how you get seven montages and no recap.

`python3 scripts/precast-check.py --round 6 --prize 0.0128` blocks on the placeholders as
well as the wallet, so it will not let this cast half-finished.

## What is new about this round, and why it is worth watching

Every round R1 through R5 paid exactly one person. This one pays up to eight, and the
second mechanism is the interesting part.

**One pot, seven channel slots.** The 0.0125 ETH goes to the best cut, decided by poidh contributor vote at close.
Separately, seven channels - Instagram, YouTube, TikTok, Facebook, Farcaster, X, Lens -
each carry ONE used clip, and whoever made it gets **$5 in $ZABAL** per channel their clip
runs on. When a channel's slot is filled it is gone.

Three things follow from that, and the description states all three plainly:

- **Early submission is worth real money**, without making the prize first-come-first-served.
  Slots fill as clips arrive; the pot is still judged at the end on merit. This is the first
  round in the series with a reason to enter on day two rather than day twenty-three.
- **The liability is bounded and knowable**: at most 7 x $5 = **$35 in $ZABAL** beyond the
  0.0125 ETH pot. That number should stay in this doc so nobody later has to reconstruct
  what was promised. R5's `_template` incident - a winner-announce that promised every
  submitter an airdrop the round never offered - is exactly what an unbounded, unwritten
  promise turns into.
- **Losing is not the same as getting nothing**, which is the actual fix for the thing that
  makes bounties feel bad. 46% of open poidh bounties draw zero entries
  (`docs/PLATFORM-AUDIT.md`); of the ones that do draw entries, everyone but one person
  walks away empty. This round is a test of whether paying the runners-up a little changes
  who bothers to enter.

**The ask back is amplification.** When we post a clip, the maker helps push it. That is the
reason to run seven people's cuts instead of hiring one editor, and it is stated in the
description rather than assumed.

## At a glance

- **Ask:** 60 second maximum recap of the NYC trip, cut from Zaal's own footage. Density is
  the brief: the most of what happened, in the least time.
- **Source:** a Drive folder Zaal provides. Unlike R5/R7, this source does not expire - no
  7-day Twitch window, no clip-early warning needed. It is the first round in the series
  whose material is fully under our control, which is why a 24-day window is safe here and
  would not have been for a WaveWarZ round.
- **Type / chain:** OPEN, Base. Album `wethemmedia`, continuity with R1-R3 and R5.
- **Issuer:** BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af`, EOA not smart wallet.
- **Prize:** 0.0125 ETH seed, fund **0.0128** (0.0125 x 1.025) so the 2.5% protocol fee does
  not eat the headline. Zaal's call 2026-09-06. Plus up to $35 in $ZABAL as above.
- **Window:** cast on or after Mon 2026-09-07, close **11:59 pm PT Wednesday, September 30,
  2026**. Weekday verified: Sep 30 2026 is a Wednesday. From a Sep 7 cast that is 23 days,
  the longest round this repo has run.
- **Winner: poidh contributor vote.** Zaal's call, 2026-09-07, asked directly because the
  round was ambiguous: he had said "at the end of the month ill pick the best" while the
  bounty type is OPEN, which resolves by contributor vote. He confirmed the vote - "it is a
  contributor vote we can say that" - so the description says so plainly rather than leaving
  entrants to infer it.

  This is a real change from R5, not a restatement. R5 was OPEN but resolved by the issuer
  accepting the winning claim directly; no vote was ever run. R6 runs the vote. Whoever
  funds the pot gets a say in who takes it, which matters more here than in any prior round
  because 47.3% of all prize money this programme has paid came from a second funder.

## Deliberately different from R5 and R7

- **No Twitch expiry problem.** The whole "clip early, the VODs die in 7 days" apparatus is
  gone, because the source is a static folder. Do not copy that language in from R7.
- **Vertical or square, not vertical only.** R7 requires 9:16 because it feeds a specific
  channel. This one runs on seven, so square is allowed and 16:9 is not.
- **No retainer-holder exclusion.** That clause exists in R7 because of the @wimpydwi
  conversation. It has no bearing here and is not in this text.
- **The $ZABAL trail is real this time.** R5 had none, which is why the template's airdrop
  promise was false for it. Here it is an actual, bounded, stated mechanic - so the
  `[OPTIONAL - verify first]` $ZABAL lines in `cast-templates/winner-announce.md` ARE usable
  for this round, once the numbers match what actually got posted.

## A measurement is planned on this round - do not change the round to make it come out

The finance-hq lane read the POIDH contract on Base and found that every round so far
(R1, R2, R3, R5) has a second funder leg beyond the BCZ treasury - **0.0330 ETH, 47.3% of
all prize money the programme has ever paid.** For R3 and R5 that money is Kenny's, from
POIDH's own Clanker Eco Fund and Activation Grant, offered in DM each time. R1 and R2
predate that programme and remain unattributed.

So the honest read is: this programme distributes to members well, and the money it
distributes comes from Zaal and from POIDH. **A mechanism that turns members into funders
exists** - Zaal used it himself, calling `joinOpenBounty` for 0.003 ETH on someone else's
bounty 331 on 2026-08-13 - **but the ask has never been made on one of ours.**

R6 is the first round where a non-winner has a reason to care about the pot at all, because
the seven channel slots pay for clips that actually run. That makes it a clean test. The
measurement is one contract call after close: **does any address other than the treasury and
the poidh relayer appear in `getParticipants` for this bounty.**

**Two things follow, and the second matters more.**

1. A yes is the first measured instance of internal capital formation in this estate. A no
   closes the question honestly instead of leaving it hopeful. Both outcomes are useful.
2. **Do not add a "chip in to the pot" ask to this round in order to make the test come
   out.** Running the ask to produce the result is how a measurement becomes theatre. If an
   ask belongs in R6 it is because it is right for the round on its own merits - and that is
   Zaal's call, made for that reason, not a finance-side experiment design. Recorded here so
   nobody later reads the planned measurement as an instruction.

## Zaal gates (money, public, outbound)

- [ ] **Provide the Drive link** and paste it over `<DRIVE-LINK>` in `description.md`.
- [ ] **Write `<WHAT-THE-TRIP-WAS>`** - two or three sentences, see above.
- [ ] **Fund the wallet.** Measured 2026-09-06 it held 0.002154 ETH against 0.0128 + gas
      needed. Re-check with `precast-check.py`.
- [ ] **Decide the seven channels are right.** The description names Instagram, YouTube,
      TikTok, Facebook, Farcaster, X and Lens. If any of those is not a channel we actually
      post to, it should not be a slot - a slot nobody can win is a promise that quietly
      does not pay.
- [ ] **Create the bounty** with the on-chain deadline set to Sep 30, matching the text.
- [ ] **Post** `promo-cast.md` with the live URL.
- [ ] **Announce R5's winner first.** Still owed, still unposted. R6 makes new promises on
      the same channels where the last one has not been kept.

## POIDH creation steps

1. Connect the issuer EOA to poidh.xyz. Switch network to Base before Create.
2. Create bounty. Type: **Open**. Token: ETH. Amount: 0.0128.
3. Title: `Recap my NYC trip in 60 seconds`
4. Description: paste `description.md` between the sentinel lines. Keep line breaks.
5. Set the on-chain deadline to 2026-09-30 so it agrees with the description.
6. Submit, confirm the tx, copy the bounty URL. Check it appears under
   [poidh.xyz/a/wethemmedia](https://poidh.xyz/a/wethemmedia).
7. **Add the new bounty id to `default_bounty_ids` in `org.config.json` and move R6 from
   `planned_rounds` to `rounds`.** R5 was never added, so its nine claimants scored nothing
   on the leaderboard until 2026-09-06.
8. Cast `promo-cast.md`.
9. Track which clip went to which channel as you post them - see the slot table below.

## Channel slot tracker

Fill this in as clips get posted. It is the record of who is owed $5 in $ZABAL, and it is
the only place that record will exist.

| Channel | Clip / maker | Posted | $ZABAL sent |
|---|---|---|---|
| Instagram | | | |
| YouTube | | | |
| TikTok | | | |
| Facebook | | | |
| Farcaster | | | |
| X | | | |
| Lens | | | |

## Files in this folder

- `description.md` - poidh Title + Description, paste-ready between sentinels, two placeholders
- `promo-cast.md` - launch copy per surface
- `cast-templates/` - catalytic co-funder DM and winner-announce, inherited from `_template`

## Sources

- Zaal, 2026-09-06, quoted in full at the top of this doc. The seven-channel slot mechanic
  is his: "per clip cap total per social media ... so once one is posted to one of these the
  next one cant win that and at the end of the month ill pick the best".
- `docs/PLATFORM-AUDIT.md` for the 46%-draw-zero figure and the platform context.
- `docs/how-to-draft-next-bounty.md` for the playbook and the creation steps.
