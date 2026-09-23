<!-- NOT-ANNOUNCEMENT-COPY: cross-round analysis of who entered and what they made. Internal, never posted, names no deadline anyone submits to. -->
# The daily run, rounds one and two together

Measured 2026-09-22 18:40 EDT from poidh (`scripts/claim-report.py`, both bounties) and
`data/leaderboard.json`. Every media file was downloaded and identified by its bytes.

| | Round 1 (1409) | Round 2 (1410) |
|---|---|---|
| Claims | 6 | 8 |
| Distinct wallets | 6 | 6 |
| Playable video on poidh | 1 | 2 |
| Filed the work rather than a screenshot | 4 | 3 |
| Pot at cast | 0.004 ETH (~$9.84) | **UNRECORDED** |
| Pot at 19:29 on 09-22 | **0.0061 ETH (~$16.79)** | 0.005 ETH (~$13.76) |

## The number that should decide round three

**Retention is 1 of 6.** Exactly one round-one entrant came back for round two:
**@pascaline**. The other five did not, **including the winner, @leoxcrane**.

Round two's field was 5 new wallets and 1 returner. The two rounds share almost nobody, so
"fourteen entries over two days" is really **eleven different people entering once each**.

**The obvious explanation is the one that has not been tested yet.** Nobody received any
feedback until the afternoon of 2026-09-22, which is *after* round two had already closed. So
round two was asked for with no feedback having been given to anyone, and the thesis in ZAOOS
research doc `community/2536-bounty-entrant-feedback` - that same-day directed feedback is what
makes an entrant enter again - has not yet had a round in which to work.

**Round three is the first honest test of it.** The five round-one notes went out today, they
point at round three, and each person has a page. If retention does not move, the thesis is
wrong here and the programme needs a different lever. That is a real prediction with a real
way to be wrong, and it should be written down before the result rather than after.

A winner not returning is the sharper half of this. Somebody was paid and did not come back the
next day.

## Format moved hard, and the honest caveat

| | Posters / stills | Video |
|---|---|---|
| Round 1 | 5 | 1 |
| Round 2 | 2 | 5 |

Round two's description asked for **VIDEO WITH AUDIO** in capitals and linked the kit's
30-second spot and radio interview. The format flipped.

**But the field also turned over almost completely**, so this cannot be read as "the ask
persuaded people". Five of round two's six wallets had never entered before and were never
asked for a poster. The change may be composition rather than persuasion, and there is no way
to separate them from this data. **UNRESOLVED.** Round three bans posters outright, which will
at least make the next reading unambiguous.

## The one failure that dominates everything

**Filing a screenshot of a post instead of the work.**

- Round 1: 2 of 6
- Round 2: **4 of 7** judgeable claims

It is the most common miss, it got **worse** after round one's description mentioned it in
passing, and it is the only miss that makes a good piece unusable rather than merely weaker.
taku0x, barsam and pascaline all made video in round two, and none of it can be watched from
the bounty page.

Every other defect is a one-off by comparison: one wrong logo, two editor watermarks, one set
of invented people, two entrants inventing the same closing time.

**This is why it is floor rule one in round three rather than a line of advice**, and it is the
single change most likely to raise the usable-entry count without asking anyone to work harder.

## Two entrants repeated a number we hedge, and they were right to find it

Both claim 8111 and @barsam state Black Moon runs "to 10".

**They did not invent it.** `zaostock.com/program` says "The ZAOstock after-party at Black Moon
Public House next door, with a DJ, run by Steve, from six **(poster: 6 to 10 PM)**", and adds
"Close. Approximate. Black Moon keeps its own hours."

**An earlier version of this document called it invented, on the grounds that "the site
publishes no end time". That was wrong: I read the HOMEPAGE, which says only "from six", and
wrote "the site".** Caught by the ZAO-on-Paragraph seat and re-verified here. Naming the
surface you actually read, in the sentence carrying the claim, is the rule this broke.

The finding is better than the wrong version of it. We print the number hedged three ways - a
parenthetical, attributed to "poster:", and under "approximate" - and two independent entrants
have now repeated it in public as a flat fact. **That is our own copy leaking a number we will
not stand behind.** The fix is on zaostock.com: stand behind the 10 unhedged, or do not print
it. Nothing about it belongs in feedback to either entrant, who did the right thing by reading
our pages.

## What is working

- **Everyone is getting paid.** All 11 daily-run wallets appear in `data/leaderboard.json`, so
  every entrant scores $ZABAL. That is the failure this repo hit twice before and the
  `check-tracked-bounties` guard now prevents.
- **Both pots grew unasked, and 1409's grew most.** Bounty one cast at 0.004 ETH
  (`rounds/daily/d01/README.md`) and read **0.0061 ETH, about $16.79** at 19:29 on 2026-09-22 -
  **up 52% while in its contributor vote**, so @leoxcrane wins more than was on the table when
  anyone entered. This is the mechanic the whole programme exists to demonstrate and it is now
  measured rather than hoped for.

  **Bounty two's growth is NOT established.** It reads 0.005 ETH now, and **no file in this
  repo records what it cast at** - an earlier draft of this document said "0.004 to 0.005"
  and that baseline was assumed, not measured. Record the reward figure at cast time from
  round three onward, or this number stays unknowable after the fact.

  **Who contributed is not measured either.** The /data endpoint was not read for
  contributions, so no claim is made about who topped either pot up.
- **An entrant self-corrected mid-round.** Claim 8100's host went offline; they noticed and
  re-filed twice on a host that plays. That is the revise behaviour round three's checkpoint is
  designed to produce, happening before the rule existed.

## Per-entrant, across everything they have filed

Eleven people, fourteen claims. Only two have filed in more than one round or more than once,
so this is mostly a list of first impressions - which is itself the finding.

| Who | Claims | What they proved they can do | What stopped it |
|---|---|---|---|
| **@assay** (poidh shows `@!3351620`) | 3 (8100, 8107, 8111) | The only person who has filed a real playable video on poidh, twice, both 1080x1920 with audio. Used the kit's radio interview cut to nine captioned passages. | One entry states a closing time we have not published. (Handle SOLVED, see below.) |
| **@pascaline** | 2 (8093, 8115) | Turned round one around fast, then switched format to video unprompted for round two. The only returner. | Round one used invented band photos and carried no date or place. Round two filed as a screenshot; whether the person on camera is real is UNVERIFIED. |
| **@leoxcrane** | 1 (8086) | Won round one. | Did not return. |
| **@predaking** | 1 (8091) | Went and got the running order and genres, credited attabotty and Candy unprompted, filed the actual file. Production discipline. | Did not return. |
| **@dee-13** | 1 (8092) | Artwork carried every fact on its own; worked in multiple versions. | Filed a screenshot. Did not return. |
| **@uniquebeing404** | 1 (8094) | The only physical-world piece anyone has made: shot on a real street with real flyers. | Facts only in the caption, filed a screenshot, landed 59 minutes late. Did not return. |
| **@coolhat** | 1 (8098) | Heavy typesetting held together at square with all eight names. | Redrawn moose, filed after the close. Did not return. |
| **@joeyofdeus** | 1 (8105) | Filed the piece itself rather than a photo of a post - one of only three people who have. Credited attabotty unprompted. | Missing "free" and the venue. Stray export artifact. |
| **@taku0x** | 1 (8104) | The most complete post copy anyone has written, and tagged correctly. | CapCut watermark burned in. Filed a screenshot. |
| **@barsam** | 1 (8103) | Cross-posted to both platforms unprompted. | Filed a screenshot. States an unpublished closing time. |
| **@mfa** | 1 (8099) | Strongest fact set on any still - readable across a room. | Used the ZABAL Gamez logo instead of the ZAOstock moose. Tool watermark. Filed a screenshot. |

### The two trajectories we actually have

**@assay improved inside a single round, twice.** 8100 pointed at a host that went offline.
They noticed without being told, re-filed as 8107 explaining exactly what had happened, then
filed 8111 as a second, different piece. Three claims, each better than the last, all in one
day. **Nobody gave them feedback to cause this.**

**@pascaline changed format between rounds, unprompted.** Round one was a poster with invented
band photos. Round two was a video with a real-looking person on a real street, with the facts
in the caption and the right tag. She moved toward exactly what round two asked for - and
**her feedback did not reach her until after round two closed**, so nothing we did caused it
either.

**Both improvements happened with zero feedback.** That is worth sitting with before concluding
round three's retention result means anything about feedback: the two most improved entrants
here improved on their own, which means improvement and return are different things and this
programme has so far only demonstrated the first.

### What this says about a standing brief

On evidence rather than impression, three people have shown something that is hard to teach:

1. **@assay** - produces finished, spec-correct video repeatedly and fixes their own errors
   without being asked.
2. **@predaking** - research and production discipline, credits sources unprompted, files
   correctly. Did not return, so the question is whether he would.
3. **@uniquebeing404** - the only person who has made anything physical, which is the rarest
   and most valuable thing in the pool and the thing the rubric rewards most.

@pascaline is the only proven returner, which is its own kind of valuable, and the invented
people in round one is a brief-following question rather than a craft one.

## Which platform the entries came from

Measured from each claim's title, description and post URL - what the entrant actually linked,
not what they said.

| | X only | Farcaster only | Both | Neither |
|---|---|---|---|---|
| Round 1 (6) | 3 | 3 | 0 | 0 |
| Round 2 (8) | 1 | 1 | 3 | 3 |

**Both channels produce.** The socials are not being written on nothing.

**On round one, every late entry came from Farcaster and every X entry was on time.**
@coolhat and @uniquebeing404 were the two that missed the 4pm close and both posted on
Farcaster; @predaking, @dee-13 and @pascaline were on X and all made it. Two cases is a
pattern to watch, not a finding.

The round-two "neither" three are two catbox.moe video files and one claim carrying no post
link at all - an entrant can file a video here without posting it anywhere, which the rubric
rewards nothing for.

### The handle that would not resolve is @assay

poidh reports that wallet as `@!3351620`, an fid with no username, and it owns the only two
playable videos in the run. **Claim 8107's description carries Farcaster post links**, which
name the account.

Confirmed properly rather than by eye: `farcaster.xyz` returns **200 for a username that
cannot exist**, so an HTTP check proves nothing about a Farcaster handle. The fname registry
can answer - `fnames.farcaster.xyz/transfers?name=assay` returns one record mapping **assay to
fid 3351620**, and a nonsense name returns zero records.

So they can be credited, announced and paid by name.

## The bar excludes five of eight, and only one entrant noticed

This bears directly on the @assay ruling, and it makes that ruling bigger than one entrant.

**Round one, rule text:** *"Tagging @bettercallzaal and cross-posting in /poidh helps. Neither
is required today, and skipping both costs you nothing."* Optional, in writing.

**Round two, rule text:** floor rule 6, *"Tag @bettercallzaal on X and cross-post in the /poidh
channel on Farcaster"*, under a heading that reads **"THE BAR. Requirements, not preferences.
Miss one and it is not entered."** Mandatory, and it requires **both** platforms, not either.

Measured from what each claim links:

| | Linked both platforms | Did not |
|---|---|---|
| Round 1, when it was optional | **0 of 6** | 6 |
| Round 2, when it became a floor rule | **3 of 8** | **5** |

**So the rule moved behaviour - 0% to 38% - and still excludes five of eight entries.**

The five are @pascaline (X only), @mfa (no post link at all), and all three @assay claims
(Farcaster only, or a bare file). **@assay is the only one of the five who noticed and said
so**, in every claim: *"I have no X account, so the X tag is the one line of the bar I could
not meet, said plainly."*

### The caveat that matters, and it does not rescue the rule

This measures **what the claim links**, not what the entrant did. Somebody could have
cross-posted and linked only one. So the honest statement is *"cannot be shown from the claim
to meet rule 6"*, not *"violated rule 6"*.

**That distinction is itself the problem.** If compliance cannot be established from the claim,
the rule cannot be enforced consistently - and it has already been enforced inconsistently,
because nobody applied it to anyone until @assay volunteered that it had missed.

### What this means for the ruling

The question is not "is @assay a special case". Five of eight are in the same position and one
of them is the round's most likely pick on craft. The real options:

1. **Enforce it.** Five of eight entries are out, including the only two playable videos, and
   the round is decided among @joeyofdeus, @taku0x and @barsam. Defensible, and it makes the
   bar mean something for the eleven days left.
2. **Waive it for this round and say so.** Cheapest, and it costs the three entrants who did
   the cross-post specifically to comply - so they should be told it was waived and why.
3. **Change the rule for round three.** Require *one* public post plus the claim, and make
   cross-posting a rubric item that earns weight rather than a floor rule that voids an entry.
   This is what the round-one text effectively did, and round one lost nobody to it.

**Option 3 is the one the data supports**, because the rule's purpose is reach, and an entrant
with no account on a platform cannot buy reach there at any effort level. A floor rule should
be something every honest entrant can clear.

Whatever is chosen, it should be said out loud in round three's text rather than applied
silently, because the same five people will read it.

## What is not measured, and must not be written as zero

- **Whether any entry reached a single person in Maine.** Fourteen entries, and **not one is a
  photograph of something physically placed in a real location** - the thing the rubric rewards
  most. No post reach was checked on any platform.
- **Claim timestamps.** Neither poidh endpoint carries one. Round one's two late entries were
  established by reading chain logs; that has not been run for round two, so no round-two entry
  is described as late.
- **Whether the two round-two videos were watched by anyone.**
- **Why five of six did not return.** The feedback timing above is a hypothesis, not a finding.
  Nobody has been asked.

## The next thing worth doing

Ask the five who did not come back. Eleven people have now made something for this festival and
ten of them made exactly one thing. That is a one-question DM, and it is worth more than another
round of guessing from claim data.
