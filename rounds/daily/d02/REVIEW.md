<!-- NOT-ANNOUNCEMENT-COPY: internal review of what was claimed on 1410. Never posted, tells nobody when to submit. It passed the deadline check by coincidence before this marker existed, purely because bounty two also closes at 5pm. -->
# Bounty two - what came in

Bounty 1410, onchain #424. **Five claims, read 2026-09-22 13:42 EDT**
(`scripts/claim-report.py --bounty 1410`). Closes 5:00pm Eastern today, so this is the state
about three and a quarter hours out, not the final field.

**Every media file was downloaded from its IPFS CID and opened.** Nothing below is inferred
from a claim title.

## The one thing to fix before the stream

**Four of the five claims uploaded a SCREENSHOT instead of the file.** Not four of the
entrants made a screenshot - four of them made something and then photographed their own phone
to submit it. barsam, taku0x and mfa all claimed a picture of a post, with the status bar,
the battery percentage and in two cases the player controls in frame. So what poidh holds for
three of five entries is unusable as media even though the underlying work may be fine.

Day one's own text called this out ("submitted as the actual file rather than a screenshot of a
post") and it got worse, not better, in round two. **It is a claim-flow problem, not a taste
problem**, and it needs one line in round three's description rather than five pieces of
private feedback.

## The broken one

**Claim 8100 cannot be judged as filed.** Both URLs it carries are dead and the account behind
them does not resolve:

- `https://raw.githubusercontent.com/goldrush-gr01/assay-claims/.../claim.json` returns **404**
- `https://goldrush-gr01.github.io/assay-claims/poidh-1410-zaostock/` returns **404**
- `api.github.com/users/goldrush-gr01` returns **404**, so that name does not resolve today.

**Say "does not resolve", not "does not exist".** That endpoint returns 404 for a name that
was never taken, for a deleted account and for a **renamed** one, and the three are
indistinguishable from outside. A renamed account is still reachable, so this is not evidence
of bad faith or of a fake entry. Caught by the Dotfiles seat, 2026-09-22.

Instrument checked both ways before that was written: a known-good raw.githubusercontent URL
returns **200** from here, so 404 is a real answer and not a blanket block; and a nonsense path
under the same repo also returns 404, so the endpoint does discriminate.

Its handle does not resolve either - poidh reports the wallet as `@!3351620`, which is an fid
with no username attached. **Title and description promise exactly what the round asked for**
(vertical 1080x1920, 15 seconds, the kit's own 30-second spot cut to its fact-carrying lines,
captioned word by word). There is just nothing at the end of the link.

Do not score it and do not assume bad faith. If they are reachable before 5pm, the fix is one
re-claim with a live URL.

## The four that resolve

### @joeyofdeus - claim 8105

The only entry whose claimed file is **the piece itself** rather than a photograph of a post.
Vertical, the real moose mark, kit type and colours, ZAOSTOCK / returns to Ellsworth / maine /
Saturday / October 3, 2026. Credits attabotty in the description unprompted.

What it is missing: **free**, and the venue. A reader knows the day and the town and still does
not know it costs nothing or where on the street to stand. There is also a stray text cursor
left visible after "2026", which reads as a frame exported mid-edit.

### @taku0x - claim 8104

Video, and the post text is the most complete of the round: free music festival, Saturday
October 3, Ellsworth Maine, Franklin St Parklet, noon to six, all ages, rain or shine, 8 acts
one stage, and it tags @bettercallzaal and @poidhxyz. The frame uses the real moose mark.

Two problems. The claim is a screenshot of the X post rather than the video. And there is a
**CapCut Ai watermark** burned into the top left of the piece, which puts someone else's brand
on ours in every repost.

### @barsam - claim 8103

Cross-posted to both Farcaster and X, and the embedded media is a video with the real kit
artwork on its cover.

Two problems. The claim is a screenshot of the Farcaster post, so the video is two clicks away
from the bounty page. And the copy says the party moves to Black Moon Public House **till
10 PM**. Black Moon is real and is on zaostock.com as "the evening, and the official
after-party" - **the 10 PM is not on the site**. Nobody should be promoted with a closing time
we have not published.

### @mfa - claim 8099

Carries the strongest fact set on the artwork itself: ZAOstock, Saturday October 3, Ellsworth
Maine, Free Music Festival, Noon to 6 PM, all in type big enough to read from across a room.

Then it uses the **ZABAL Gamez logo**, not the ZAOstock moose. That is our own mark from
another brand, which is a harder miss than a stock graphic would be. There is also a
"Music Festival Event" watermark from whatever tool made it sitting across the middle of the
word Festival, and the claim is a phone screenshot with Share, Favorite, Edit, Delete and
More visible along the bottom.

## What this round actually told us

1. **Asking for video with audio worked.** At least three of the five are video, against one in
   round one. The audio in the kit is being used.
2. **The claim flow is the bottleneck now, not the craft.** Fixing "upload the file" is worth
   more than any note about composition.
3. **Two entries carry another tool's watermark** and one carries the wrong ZAO mark. Round
   three should say that a watermark from an editor is a floor fail, in the same breath as the
   mark rule.
4. **Nobody has photographed a physical placement yet**, across eleven entries over two rounds.
   That is the thing the rubric rewards most and the thing zero people have done. It is worth
   saying out loud rather than leaving in a list.

## Not measured

- **Whether any of the five went anywhere in Maine.** No entry claims a Maine placement and I
  did not check reach on any post. UNMEASURED, not zero.
- **Claim timestamps.** Neither poidh endpoint carries one, so lateness cannot be established
  from this data. Day one's two late entries were established by reading chain logs, and that
  has not been run for 1410.
