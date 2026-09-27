<!-- NOT-ANNOUNCEMENT-COPY: the field, the pick and the transaction for round four. Internal. Names no deadline anyone submits to. -->
# Round four - the field, the pick, and the transaction

Bounty **1418**, on-chain **432**. **Closes 5:00pm Eastern today, Sunday 27 September**, as cast.
Field read **2026-09-27 07:51 EDT**: **four claims**. **Nothing here has been sent.**

> **The close is a promise, not a chain deadline.** `/data` returns `deadline: null` for 1418 -
> poidh only sets that field when a vote starts. The 5pm close exists in the cast text
> (`description.md` lines 27, 68 and 152) and nowhere else, so it is kept by Zaal acting, not
> by the contract refusing late claims.

**EVERY ENTRY HAS NOW BEEN WATCHED.** This is the gate that blocked this round since yesterday,
and it is cleared. `ffmpeg` is on this Mac and `zao-fetch-x.sh` returns direct mp4 URLs through
fxtwitter, so all four pieces were downloaded, probed and read frame by frame rather than
described.

## The field, measured

| claim | who | length | frame | audio | the four required facts | public post |
|---|---|---|---|---|---|---|
| **8239** | **@assay** | **25.6s** | 1080x1920 | yes, aac | **on EVERY frame** | X 48 views, also Farcaster |
| 8240 | @coolhat | 19.0s | 1080x1920 | **none** | on the final card only | **X 178 views, 4 favs, 1 reply** |
| 8312 | pn-research | 28.58s | **1280x720** | yes | across the piece | X 9 views, 0 favs |
| 8326 | @joeyofdeus | 16.2s (round three record) | 1280x720 | yes | round three record | X 84 views, 5 favs, 1 reply |

**All four are inside the thirty-second limit.** That was the round's only hard constraint on
form and nobody broke it.

### A correction to the record, before anyone judges from it

The note carried since yesterday said claim 8312 *"shows 2 of the 4 required facts and a frame
is not the work"*. **It was right about the frame and wrong about the work.** The still on the
claim carries ZAOSTOCK and FREE only. The video carries all four: SATURDAY OCTOBER 3 with NOON
TO SIX, and **ELLSWORTH MAINE over real aerial footage of the Franklin Street Parklet**, plus
ONE STREET / ONE STAGE / EIGHT ACTS and zaostock.com. **Nothing about 8312 fails the brief.**

## THE PICK: 8239, @assay

**It wins on the brief's own sentence, not on taste.** Rule 4 says the facts go on the piece and
not only in the caption, *"A repost strips your caption"*, and the brief adds that it *"has to
work in the three seconds someone looks at it before scrolling"*.

**8239 is the only entry where every required fact is on screen for the entire runtime.** A
locked banner reading **ZAOSTOCK - SATURDAY, OCTOBER 3 / ELLSWORTH, MAINE - FREE - NOON TO SIX**
is present in every frame sampled across the 25.6 seconds. Any three-second glance carries the
whole thing; a caption-stripped repost loses nothing. That is the rule's purpose, met exactly.

**And it is an advert rather than a list.** It picks one idea - a local TV weather forecast
where the forecast is music, *100% CHANCE OF LIVE MUSIC* - and builds the hourly strip, the
radar and the advisory card out of it. The brief asked for a piece that picks one thing and
lands it; this is the only entry with an idea rather than a treatment.

**Its description held up on every checkable point**, which is rarer than it should be:

| it claimed | measured |
|---|---|
| 25-second vertical, 1080x1920 | **25.6s, 1080x1920** |
| with sound | **aac audio track present** |
| every frame carries the facts | **confirmed across sampled frames** |
| moose mark by attabotty, Star 97.7 from the kit, OpenStreetMap | **all three credited in the footer of the piece itself** |

It also declares itself an autonomous agent, unprompted, for the fourth round running.

## The honest case against, and for @coolhat

**@coolhat's 8240 has the most reach of the four by a distance: 178 views against 48, 84 and 9.**
For an advert that is not a detail. It is clean kinetic type, it is the shortest at 19 seconds,
and **it is the only entry that spells the festival the way the festival spells it - ZAOstock,**
where @assay and pn-research both render ZAOSTOCK in caps.

**Two things count against it and they are both from the brief.** Its facts arrive only on the
final card at the end of 19 seconds, so the three-second glance sees *"ONE STREET."* and no
festival, no date, no FREE. And it has **no audio track at all** - fine in a muted feed, but it
forgoes a channel the brief did not forbid.

**If the pick were reach, it would be @coolhat.** The brief did not say reach; it said the facts
travel with the piece.

## What this round should say out loud

- **Claim 8326 is a piece already entered in round three** - same wallet, same X post as claim
  8147, posted 23 September. Measured across 1410, 1412, 1418 and 1421: 21 links, 19 distinct,
  exactly 2 reused across rounds. **The programme ruled on this shape once already** with
  @pascaline's 8150, by judging the piece and saying the rule and the pick disagreed rather
  than marking anyone down quietly. **Round three asked for anything but a poster and round
  four asks for an ad, so a piece can honestly serve both** - and this one is closer to an ad
  than round three's brief ever wanted.
- **Every entrant put the facts on the piece.** Three rounds ago that was the complaint; the
  brief says three separate entrants had left FREE off. **Four of four carried FREE this time.**

## The transaction

Accept on **bounty 1418, on-chain 432**.

| for the pick | bountyId | claimId |
|---|---|---|
| **8239 @assay (recommended)** | **432** | on-chain id from `claim-report.py` at accept time |
| 8240 @coolhat (if reach decides it) | 432 | as above |
| 8312 pn-research | 432 | as above |
| 8326 @joeyofdeus | 432 | as above |

**Read the on-chain claim id at the moment of the transaction**, never from this table - the
poidh claim id and the on-chain id differ, and this file will be hours old by 5pm.

A two-day contributor vote follows, then `resolveVote(432)`.
