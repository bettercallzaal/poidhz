<!-- NOT-ANNOUNCEMENT-COPY: internal review of what was claimed on 1410. Never posted, tells nobody when to submit. It passed the deadline check by coincidence before this marker existed, purely because bounty two also closes at 5pm. -->
# Bounty two - the full field

Bounty 1410, onchain #424. **8 claims from 6 wallets**, read 2026-09-22 18:35 EDT
(`scripts/claim-report.py --bounty 1410`). Past its 5:00pm Eastern close. Pot **0.005 ETH,
about $13.73** at read time, up from the 0.004 it cast at - **somebody topped it up unasked**,
which is the mechanic this whole programme exists to demonstrate and the first time it has
happened in the daily run.

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
| 8111 | @!3351620 | **MP4, 1080x1920, 31.5s, with audio** | **yes** |
| 8107 | @!3351620 | **MP4, 1080x1920, 15.0s, with audio** | **yes** |
| 8105 | @joeyofdeus | JPEG, 46 KB - the piece itself | still only |
| 8104 | @taku0x | JPEG, 67 KB - screenshot of an X post | no |
| 8103 | @barsam | JPEG, 135 KB - screenshot of a Farcaster post | no |
| 8100 | @!3351620 | dead link, superseded by 8107 | no |
| 8099 | @mfa | JPEG, 90 KB - screenshot of a phone gallery | no |

## The entrant who fixed their own entry mid-round

Claim 8100 pointed at a host that went offline, and both its URLs 404'd. Rather than write it
off, it was flagged as unjudgeable-as-filed. **They saw it and re-filed twice**, on a host that
plays: *"My first claim here (8100) linked to a host that went offline today, so its links are
dead. Same piece, nothing changed."*

That is exactly the tag-a-draft-and-revise behaviour round three is being built around, and it
happened before the rule existed. It is also the reason not to score a broken link as bad
faith.

Note their handle still does not resolve - poidh reports the wallet as `@!3351620`, an fid with
no username. **There is no way to credit or pay this person by handle**, which needs solving
before they can win anything.

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

**But it says "THEN BLACK MOON PUBLIC HOUSE, 6 TO 10".** Black Moon is real and is on
zaostock.com as "the evening, and the official after-party" - **the site publishes no end
time**. barsam's entry carries the same invented 10 PM. Two entrants inventing the same
detail suggests it is being guessed from the shape of the sentence on the site, which is worth
fixing on the site rather than only in feedback.

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

## Recommendation

**8107 as the pick.** It is the only entry with nothing wrong on it, it is exactly the format
the round asked for, and it plays on the page.

**8111 is better work carrying one error.** If the 6-to-10 can be corrected before anything is
run publicly, it is the stronger piece and the better advertisement for what the kit can do.

Whichever wins, **the handle problem has to be solved first**: `@!3351620` resolves to no
username on any platform, so there is currently no way to announce or credit them.

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
