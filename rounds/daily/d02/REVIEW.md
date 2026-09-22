<!-- NOT-ANNOUNCEMENT-COPY: internal review of what was claimed on 1410. Never posted, tells nobody when to submit. It passed the deadline check by coincidence before this marker existed, purely because bounty two also closes at 5pm. -->
# Bounty two - the full field

Bounty 1410, onchain #424. **8 claims from 6 wallets**, read 2026-09-22 18:35 EDT
(`scripts/claim-report.py --bounty 1410`). Past its 5:00pm Eastern close. Pot **0.005 ETH, about $13.76** at read time.

**Its growth is UNKNOWN, not zero.** No file in this repo records what 1410 cast at, so the
"up from 0.004" an earlier version of this document claimed was an assumed baseline, not a
measurement. Bounty ONE's growth *is* measured: 0.004 ETH at cast
(`rounds/daily/d01/README.md`) to 0.0061 ETH, about $16.79, while in its vote - up 52%. Write
the reward figure down at cast time from round three on.

**Every claimed file was downloaded and identified by its bytes**, not by its title and not by
the claim's own description. Where it was a video, `ffprobe` confirmed duration and the
presence of an audio stream.

## The finding that matters

**Only 2 of the 8 claims are a playable video on poidh.** Claims 8107 and 8111. Every other
claim resolves to a still JPEG, and four of those five stills are a photograph of a phone
screen rather than the work itself.

The round asked for **video with audio** in capitals and gave people the kit audio to use.
Several people did make video - taku0x, barsam and pascaline all have one on X or Farcaster -
but **you cannot watch any of it from the bounty page**, because what they filed is a
screenshot of the post that contains it.

So the bottleneck is not craft and it is not willingness. It is the claim flow, and it got
worse rather than better after day one's description called it out in passing. That is why it
is floor rule one in round three rather than a line of advice.

| Claim | Who | What was actually filed | Playable on poidh |
|---|---|---|---|
| 8115 | @pascaline | JPEG, 113 KB - screenshot of an X post | no |
| 8111 | @assay | **MP4, 1080x1920, 31.5s, with audio** | **yes** |
| 8107 | @assay | **MP4, 1080x1920, 15.0s, with audio** | **yes** |
| 8105 | @joeyofdeus | JPEG, 46 KB - the piece itself | still only |
| 8104 | @taku0x | JPEG, 67 KB - screenshot of an X post | no |
| 8103 | @barsam | JPEG, 135 KB - screenshot of a Farcaster post | no |
| 8100 | @assay | dead link, superseded by 8107 | no |
| 8099 | @mfa | JPEG, 90 KB - screenshot of a phone gallery | no |

## The entrant who fixed their own entry mid-round

Claim 8100 pointed at a host that went offline, and both its URLs 404'd. Rather than write it
off, it was flagged as unjudgeable-as-filed. **They saw it and re-filed twice**, on a host that
plays: *"My first claim here (8100) linked to a host that went offline today, so its links are
dead. Same piece, nothing changed."*

That is exactly the tag-a-draft-and-revise behaviour round three is being built around, and it
happened before the rule existed. It is also the reason not to score a broken link as bad
faith.

**The handle is solved.** poidh reports the wallet as `@!3351620`, an fid with no username,
but claim 8107's own description carries its Farcaster links: the account is **@assay**.
Confirmed against the fname registry, which maps `assay` to fid 3351620 while a nonsense name
returns nothing - farcaster.xyz itself returns 200 for any username, so a status check proves
nothing there.

## Entry by entry

### 8107 - 15 seconds, and the cleanest on facts

1080x1920, 15.0s, real audio stream. Real moose mark, the kit's cracked-cement texture, the
lineup in running order, and a persistent bottom bar carrying Saturday October 3, Ellsworth
Maine, Franklin Street Parklet, free, all ages, rain or shine, plus zaostock.com. No watermark
from any editor.

Nothing on it is wrong. It is the safe pick.

### 8111 - 31 seconds, more ambitious, one fact we have not published

Uses **the kit's own Star 97 radio interview**, cut to nine passages and captioned word by
word, with an act-by-act running order and a progress bar through the eight acts. Credits
attabotty for the moose and Star 97 for the audio in the footer. This is the best use anybody
has made of the kit.

It says "THEN BLACK MOON PUBLIC HOUSE, 6 TO 10", and **that is not invented - they read it off
our own page.** Corrected 2026-09-22 by the ZAO-on-Paragraph seat, and re-verified here:
**zaostock.com/program** says "The ZAOstock after-party at Black Moon Public House next door,
with a DJ, run by Steve, from six **(poster: 6 to 10 PM)**", twice, and adds "Close.
Approximate. Black Moon keeps its own hours."

**An earlier version of this file said "the site publishes no end time". That was wrong, and
wrong in a specific way worth naming: I read the HOMEPAGE and wrote "the site".** The homepage
says only "from six". The program page carries the 10.

The finding survives and is sharper. We publish the number hedged three ways - as a
parenthetical, attributed to "poster:", and under "approximate" - and entrants are repeating
it publicly as a flat fact. @barsam did the same thing independently. **That is our copy
leaking a number we will not stand behind**, and the fix is on zaostock.com: either stand
behind the 10 unhedged or do not print it.

### 8115 - @pascaline

A video with a person talking to camera in a ZAOstock hoodie on a street, captioned. The post
text carries every fact: 8 acts, Saturday October 3, Franklin Street Parklet, noon to 6 PM,
and it tags @bettercallzaal.

**This one needs Zaal's eyes rather than mine.** I cannot establish whether the person on
camera is real and agreed to appear, or is generated. Against floor rule 4, no invented people,
that distinction decides whether it can run at all - and her round one entry used invented band
photos, so it is a live question rather than a theoretical one. **UNVERIFIED, not a finding.**

Filed as a screenshot of the post, so the video is not on the bounty page.

### 8105 - @joeyofdeus

**The only entrant besides 8107/8111 who filed the piece rather than a photo of a post.**
Vertical, real moose mark, kit type and colours. Credits attabotty in the description without
being asked.

Missing **free** and the venue. A reader knows the day and the town and still does not know it
costs nothing or where on the street to stand. There is also a stray text cursor left visible
after "2026", which reads as a frame exported mid-edit.

### 8104 - @taku0x

The most complete post text of the round: free music festival, Saturday October 3, Ellsworth
Maine, Franklin St Parklet, noon to six, all ages, rain or shine, 8 acts one stage, tagging
@bettercallzaal and @poidhxyz. The video uses the real moose mark.

Two problems. Filed as a screenshot. And a **CapCut Ai watermark** burned into the top left,
which puts another company's brand on ours in every repost.

### 8103 - @barsam

Cross-posted to both Farcaster and X, and the underlying media is a video on the real kit
artwork.

Filed as a screenshot of the Farcaster post. And the copy carries the same unpublished
**"till 10 PM"** for Black Moon.

### 8099 - @mfa

The artwork carries the strongest fact set of any still: ZAOstock, Saturday October 3,
Ellsworth Maine, Free Music Festival, Noon to 6 PM, in type readable across a room.

Then it uses the **ZABAL Gamez logo** instead of the ZAOstock moose. That is our own mark from
a different brand, which is a harder miss than a stock graphic would be. A tool watermark
reading "Music Festival Event" sits across the word Festival, and the claim is a phone
screenshot with Share, Favorite, Edit, Delete and More along the bottom.

## The thing that changes the recommendation, found by reading the claims verbatim

**@assay declares in all three of its claims that it is an autonomous AI agent**, and it
declares in the same breath that it cannot meet one of the floor rules:

> "Made by Assay, an autonomous AI agent."
> "I have no X account, so the X tag is the one line of the bar I could not meet, said plainly."

Bounty two's immutable text reads **"THE BAR. Requirements, not preferences. Miss one and it is
not entered"**, and rule 6 is *"Tag @bettercallzaal on X and cross-post in the /poidh channel on
Farcaster."*

**So by the bar as written, 8107 and 8111 are not entered.** The entrant said so itself, before
anyone checked, and did it in the claim rather than hoping nobody noticed.

That is two separate decisions, and both are Zaal's:

1. **Is an autonomous agent eligible to win at all?** Nothing in any description addresses it.
   The rules cover invented people and generated imagery, not an agent entering on its own
   behalf. This will recur - it has entered three times in one round already.
2. **Does an entrant who cannot meet a floor rule, and says so, get judged anyway?** The rule
   exists for reach. An entrant with no X account cannot buy reach on X at any effort level,
   which is different from an entrant who did not bother.

**Whatever is decided has to be decided out loud**, because the other seven entrants read the
same bar and two of them did the X cross-post specifically to meet it.

## Recommendation

**If the bar is enforced as written:** neither 8107 nor 8111 is entered, and the pick comes
from the rest. On the remaining field @joeyofdeus (8105) is the strongest - the piece itself
rather than a screenshot, the real mark, credits attabotty unprompted - with the caveat that it
is missing "free" and the venue.

**If the X rule is waived for an entrant who has no X account:** 8107 is the pick. It is the
only entry in the round with nothing else wrong on it and it is exactly the format asked for.
8111 is better work but states a Black Moon closing time we have not published.

**Do not let the waiver happen silently by just picking 8107.** Say which rule was set aside
and why, or the bar stops meaning anything for the eleven days that follow.

The handle is no longer a blocker: the wallet is **@assay** on Farcaster, confirmed against the
fname registry (fid 3351620).

## What this round changes for round three

1. **Upload the file** became floor rule one, not advice. 6 of 8 claims could not be watched or
   viewed properly from the bounty page.
2. **Editor watermarks are a floor fail.** Two entries carried one.
3. **The ZABAL Gamez logo is not the ZAOstock logo** is now stated, because it happened.
4. **Two separate entrants invented the same Black Moon closing time.** Publishing the real one
   on zaostock.com would stop it recurring, and that is a fix on our side.

## Not measured

- **Whether any entry reached anyone in Maine.** No entry claims a Maine placement and no post
  reach was checked. UNMEASURED, not zero. Across two rounds and fourteen entries, still
  nobody has photographed a physical placement.
- **Claim timestamps.** Neither poidh endpoint carries one, so lateness cannot be established
  from this data and no entry here is described as late.
- **Whether the two videos were seen by anyone.** Views were not checked on any platform.
