# R3 winner announce - femmie (READY TO SEND)

On-chain confirmed 2026-08-05: `bounties(194)` shows amount=0, claimer=femmie's
wallet; `getClaimsByBountyId(194,0)` shows claim 1433 (femmie) `accepted: true`.
Re-verified 2026-08-20 with `scripts/query-bounty.py --bounty 1180 --chain 8453`:
WINNER SET, claim 6749, 8 claims total. Fully paid out, not just voted-through.
Never assume femmie's gender - use the handle or they/them, never she/he.

Reasoning below is grounded in the actual claim (X post 2065083051714003291,
cast 0xd42f8ee9) checked against the R3 rubric in `../description.md`. Video
probed 2026-08-20: 20s, 1920x1080, audio track present.

## Farcaster (long)

```
@femmie won Round 3 of the BCZ x POIDH bounty: the ZABAL Gamez ad.

The ad: https://x.com/femmie/status/2065083051714003291

Why this one, against the rubric we posted before the round opened:

One line that sells the whole thing. "Most hackathons end Sunday. This one pays you in September." That is the takeaway the rubric asked for - free, three months, real builds that keep earning - said in eight words of kinetic type, no voiceover needed.

Names the real beats. June workshops, July build anything, August finals, on screen in order. The post text picks up the three tracks (artist, builder, creator) and the 100+ member community. Nothing generic, nothing invented.

Every distribution box ticked. Posted on X with @bettercallzaal, @kennyistyping and @poidhxyz tagged, cross-posted on Farcaster, zabalgamez.com in the post body AND on the end card next to the wordmark.

Twenty seconds. Reads in three. The kind of asset you forward without being asked.

0.025 ETH already released to you - confirmed on-chain.

And the part that scales: every submitter to Round 3 already got $ZABAL airdropped via slot 8 of $ZABAL Empire on Empire Builder. Winning the ETH is the spike. Showing up earns the baseline.

All 8 submissions: https://github.com/bettercallzaal/zpoidh/tree/main/rounds/r3

cc @poidh
```

## X (under 280)

```
@femmie won Round 3 of the BCZ x @poidhxyz bounty - the ZABAL Gamez ad.

"Most hackathons end Sunday. This one pays you in September." 20 seconds, every rubric box ticked, real beats on screen.

0.025 ETH released on-chain. Every submitter already earned $ZABAL via @empirebuilder.

https://x.com/femmie/status/2065083051714003291
```

## Short - Telegram / GC / Discord

```
Round 3 BCZ x POIDH winner: @femmie, for the ZABAL Gamez ad.

Why: one line that sells it ("most hackathons end Sunday, this one pays you in September"), the real June / July / August beats on screen, all three tracks and the 100+ community in the post, every tag and link the rubric asked for, 20 seconds flat.

0.025 ETH released on-chain. Every Round 3 submitter already got $ZABAL via the $ZABAL Empire leaderboard.

Ad: https://x.com/femmie/status/2065083051714003291
All 8: https://github.com/bettercallzaal/zpoidh/tree/main/rounds/r3
```

## Rubric check (for the record, not for posting)

| Rubric line | Evidence |
|---|---|
| Bar 1: ad in any format | 20s kinetic-type video, 1920x1080 |
| Bar 2: tag @bettercallzaal on X | tagged |
| Bar 3: cross-post on Farcaster | cast 0xd42f8ee9 ("made an ad for the zao homies", video + zabalgamez.com embed). Channel not verified. |
| Bar 4: submit URL on poidh | claim 6749 |
| Bar 5: audio rule | audio track present; which track was not verified by ear |
| Distribution: @kennyistyping, @poidhxyz, zabalgamez.com visible | all three in the X post; URL also on the end card |
| Craft: clarity in 3s, wordmark visible, shareable | yes / end card logo + URL / yes. 16:9, not vertical (one craft box missed) |
| Substance: one takeaway, real beats, right viewer | "pays you in September" / June-July-August on screen / artist-builder-creator + 100+ in post |
| Bonus | none of the four bonus angles (mentor invite, testimonial, B-roll, any-orientation) |

## Before sending, confirm

- [x] `resolveVote(1180)` has run and femmie's claim is accepted+paid - confirmed on-chain 2026-08-05, re-verified 2026-08-20
- [x] Reasoning grounded in the claim + rubric - above
- [x] Other 7 submitters get an honorable-mention reply-cast - see `honorable-mentions.md` in this folder, post as a reply under the winner cast
