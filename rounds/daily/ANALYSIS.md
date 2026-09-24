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

> **That last row is a bad metric and it is kept only so the correction has something to point
> at.** It counts entrants who uploaded a still as having missed, and for a video that is the
> only thing poidh's uploader allows. Read the corrected section below before using it.
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

## THE FAILURE THAT DOMINATED EVERYTHING WAS MOSTLY OURS

**Corrected 2026-09-23, on Kenny's answer.** This section used to read: *"Filing a screenshot of
a post instead of the work. Round 1: 2 of 6. Round 2: 4 of 7 judgeable claims. It is the most
common miss."* It then made that the round-three bar's first requirement.

**Most of those were not misses.** Asked directly whether poidh's uploader takes video, Kenny
answered: *"yee man all media is uploaded to ipfs it would suck if we took videos lol"*. The
uploader is **images-only by design**, because every upload goes to IPFS. So for anyone
entering with a video, uploading a still and linking the piece is **the only thing the platform
allows** - and rounds two and three both asked for video.

Re-derived against what each entrant actually made, rather than against what they uploaded:

| Round | Entered with a still and photographed a screen instead of uploading it | Entered with video and uploaded a still |
|---|---|---|
| One - posters were the ask | **2 of 6.** A real miss, and the advice stands | n/a |
| Two - video was the ask | **1** (@mfa, a photo of a phone gallery) | **3** (@taku0x, @barsam, @pascaline) - not a miss |
| Three - anything but a poster | 0 | **4 of 4** competing entries - not a miss |

**What survives the correction, and it is much smaller.** A screenshot of your POST is still
worse than a FRAME of your piece. The ones filed in rounds two and three carry app chrome,
battery icons, view counts and reply boxes, and that is what the bounty page shows a visitor.
That is a presentation note worth one line in someone's feedback. It is not a floor rule, it is
not "the failure that dominates everything", and it never was.

**One entrant got video onto a bounty page anyway.** @assay's claims point their media field at
a direct external mp4 rather than uploading - `files.catbox.moe/2ypwkq.mp4`, verified live at
13,398,991 bytes, h264 1080x1920 with audio. Two of fifty-four claims are watchable in place
and both are its. **UNVERIFIED** whether a person using poidh's web form can do the same or
whether it needs a direct contract call; that is the next question for Kenny, and until it is
answered it must not go into bounty text.

**What this cost.** Round three's cast text carries the impossible version of the rule and
cannot be edited. Twenty-four generated drafts carried it too and have been fixed
(`rounds/daily/_template/description.md`). Round two's review marked entries down for it. The
notes owed to those entrants must not repeat it.

Every other defect is genuinely a one-off: one wrong logo, two editor watermarks, one set of
invented people, two entrants repeating a closing time that **our own site publishes**.

**The lesson under the lesson:** we measured what entrants did, found a near-universal pattern,
and concluded it was a discipline problem in them. A near-universal result is almost always the
instrument. One question to the person who built the platform would have settled it before it
became a requirement, and nobody asked for three rounds.

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
**Two corrections applied to this table on 2026-09-23, both of which had marked people down
for something that was not their fault.** "Filed a screenshot" is removed wherever the entrant
made video, because poidh's uploader cannot take video (see the corrected section above).
"States an unpublished closing time" is removed entirely, because `zaostock.com/program`
**does** publish it - *"from six (poster: 6 to 10 PM)"*, re-verified on the live page today.
Two entrants were marked down for reading our own site.

| Who | Claims | What they proved they can do | What stopped it |
|---|---|---|---|
| **@assay** (poidh shows `@!3351620`) | 3 (8100, 8107, 8111) | The only entrant who has got a playable video onto a poidh page, twice, both 1080x1920 with audio - by pointing the claim at an external mp4 instead of uploading. Used the kit's radio interview cut to nine captioned passages. | Nothing disqualifying. Declared itself an agent in every claim, unprompted. (Handle SOLVED, see below.) |
| **@pascaline** | 4 (8093, 8115, 8149, 8150) | **The only entrant in all three rounds.** Round one to round three she went from invented band photos to drone footage of the real parklet with every fact correct. Switched to video unprompted before anyone asked. | Round one used invented band photos and carried no date or place. In round three she claimed twice and the later claim pointed at round two's video. |
| **@leoxcrane** | 1 (8086) | Won round one. | Did not return. |
| **@predaking** | 1 (8091) | Went and got the running order and genres, credited attabotty and Candy unprompted, filed the actual file. Production discipline. | Did not return. |
| **@dee-13** | 1 (8092) | Artwork carried every fact on its own; worked in multiple versions. | Photographed a phone screen rather than uploading the artwork - a real miss, because a still CAN be uploaded. Did not return. |
| **@uniquebeing404** | 1 (8094) | The only physical-world piece anyone has made: shot on a real street with real flyers. | Facts only in the caption, photographed a screen rather than uploading the still, landed 59 minutes late. Did not return. |
| **@coolhat** | 1 (8098) | Heavy typesetting held together at square with all eight names. | Redrawn moose, filed after the close. Did not return. |
| **@joeyofdeus** | 2 (8105, 8147) | Returned for round three and **fixed one of his two notes before being given it** - the venue is now in the piece, twice. Credits attabotty unprompted, every time. | Missing "free" in round two and **still missing "free" in round three**, across twelve frames sampled. Stray export artifact in round two. |
| **@taku0x** | 2 (8104, 8145) | Most complete post copy anyone has written, tagged correctly, and **removed a watermark and re-posted clean without being asked** once he heard it was a problem. | Round two carried a CapCut watermark. Round three is AI-generated throughout and carries no venue, time or URL. |
| **@barsam** | 1 (8103) | Cross-posted to both platforms unprompted. | Facts sit in the post rather than on the piece. |
| **@mfa** | 1 (8099) | Strongest fact set on any still - readable across a room. | Used the ZABAL Gamez logo instead of the ZAOstock moose. Tool watermark. Photographed a phone gallery rather than uploading the still. |
| **@kmacb.eth** | 1 (8153) | Runs poidh. Entered round three at the buzzer with deliberately unsupervised agent output to make a point. | A still with type on it, in the round that banned exactly that. Says so himself: *"It's shite."* Not competing. |

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
