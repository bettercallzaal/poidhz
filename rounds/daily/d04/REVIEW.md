<!-- NOT-ANNOUNCEMENT-COPY: internal review notes on round four entries. Names no deadline anyone submits to. -->
# Round four - entries as they arrive

Bounty 1418, the ad round, closes **Sunday 27 September 5pm ET**. Nothing here is posted.

## 2026-09-26 03:1x - three claims

A third entry landed overnight: **claim 8312, wallet `0x5a844e78`, "ZAOstock Round 4 Ad - 28s
Spot"**, linking a public X post and a 1920x1080 still.

**THAT WALLET IS ALSO IN ROUND FIVE.** It filed claims 8304 and 8305 on bounty 1421 - the two
performance pull requests from @pn-research. **The same agent is now entered in both open
rounds, in media and in code.** That is the first cross-round entrant of this run and it is
worth knowing before either round is judged.

### What I verified, and what I did not

**Verified:** the X post returns 200. The still resolves, 1920x1080 JPEG, 56,729 bytes. The
frame carries the moose mark, **ZAOSTOCK**, **FREE**, and "ALL AGES - RAIN OR SHINE -
zaostock.com".

**NOT verified, and this is the part that matters for judging.** Round four's bar requires, on
the piece itself: *"ZAOstock, Saturday October 3, Ellsworth Maine, and the word FREE."* The
frame I can see carries two of those four - ZAOSTOCK and FREE. **It does not show the date or
the place.**

That is not a finding against the entry. The claim says the piece carries "Saturday Oct 3, noon
to six, Franklin Street Parklet, Ellsworth Maine", and **a single frame of a 28.5-second video
is not the video.** This programme has already made the mistake of rating a still and calling
it the work, in round two, and it is written down precisely so it is not repeated.

**To judge this properly somebody has to watch the X post.** I cannot from this seat. Until
then the honest state is: two of the four required facts confirmed on the frame supplied, the
other two claimed and unconfirmed, and the piece itself unwatched.

### For the close, Sunday 5pm

- 3 claims. Every one needs its media resolved to the actual work before it is scored, not
  judged from the thumbnail poidh renders.
- The feedback promise on this round is the same one that has been kept twice: every entrant
  gets written notes, published.

---

## Claim 8312's X post exists. Measured 2026-09-26 16:30 EDT, with the control that makes it mean something.

The claim's whole case sits in a link: `x.com/inkier35/status/2103721261570707770`, described as
a 28.5-second spot carrying all six required facts, no watermark, built from the brand kit.

**The post is public and it resolves.** `curl -L` returns **200**.

**A 200 from x.com would normally prove nothing** - it is a single-page app, and an SPA
happily serves its shell for a URL with no content behind it. So the 200 was only worth writing
down after the control:

| URL | code |
|---|---|
| the claim's post | **200** |
| `x.com/inkier35/status/1111111111111111111` (same account, impossible id) | **404** |
| a nonexistent account and id | **404** |

x.com really does 404 a status that is not there, so the 200 on the claim's link is evidence
rather than an artefact. **Without those two control rows the first row is unreadable.**

**What this does NOT establish, and no script can:** whether the video contains the six facts,
whether it carries a watermark, and whether it came from the brand kit. **The claim carries no
media on the bounty itself** - all three round four claims have an empty media field - so the
bounty page shows this entry with no picture, and the link is the only way in.

**Somebody still has to watch 28.5 seconds of video before this round is scored.** The round
closes 5pm Sunday. That is the whole remaining cost of judging it, and it cannot be delegated to
a check.

## Both open rounds share two entrants, and nothing anywhere shows it

Reading the issuer wallets across 1418 and 1421 together:

| Wallet | Round four | Round five |
|---|---|---|
| `0x5a844e78` | claim 8312, the ad | claims 8304 and 8305, PRs #316 and #318 |
| `0xd34f10e2` | claim 8239 | claim 8310 |

**Two entrants are competing in an ad round and a code round at the same time, this weekend.**
That is the returning-entrant behaviour `docs/community-plan.md` was written about, happening
inside a single weekend rather than across months, and **no page on the site shows it** - the
gallery is organised by round, so a person who appears in two of them appears twice and is
joined up nowhere. It is the strongest argument yet for the per-person page being first.

Recorded here rather than acted on: this is an observation about the field, and it changes
nothing about how either round is judged.
