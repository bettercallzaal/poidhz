<!-- COPY: text to post when this round is live, not a statement that it is.
     scripts/check-site-claims.py skips files that declare this, because copy
     saying "the bounty is live" is correct in copy and wrong in a status page. -->

# R6 promo copy - NYC trip recap

Replace `<BOUNTY-ID>` and `<DRIVE-LINK>` everywhere once the bounty is live.

The seven-slot mechanic is the reason to enter this one, and it is the part people will not
expect. Lead with it everywhere except the shortest surface. "You can get paid even if you
lose" is a different pitch from every round this repo has run, so do not bury it under the
prize.

**Post R5's winner announcement before any of this goes out.** That round promised a winner
post and has not delivered one; launching R6 on the same channels first is how a series
teaches people its promises are soft.

---

## Farcaster (long) - /zao primary, cross-post /poidh

```
New bounty: cut the best 60 second recap of my NYC trip.

https://poidh.xyz/base/bounty/<BOUNTY-ID>

All the footage is in one folder, link is in the bounty. Sixty seconds is the cap, not the target - the whole ask is density. The most of what happened, in the least time, so someone who was not there gets it.

0.0125 ETH on Base to the best cut. OPEN bounty, so the pot grows if people stack on it.

Here is the part that is different. One person wins the ETH, but I am running the best of these across seven channels - Instagram, YouTube, TikTok, Facebook, Farcaster, X, Lens - and every channel gets ONE clip. If I post yours, you get $5 in $ZABAL for it. Seven slots, and they close as they fill.

Which means submitting early is worth actual money, even though the prize itself is judged at the end on merit.

Every clip I post gets its maker credited by handle, and I say where it came from. You keep your edit.

Closes 11:59pm PT Wednesday September 30.

cc @poidhxyz @kennyistyping
```

## X (short, under 280)

```
Cut the best 60 second recap of my NYC trip. Footage is all in the folder.

0.0125 ETH to the winner. But I am running the best across 7 channels, one clip each, and if I post yours you get $5 in $ZABAL. Slots close as they fill, so early is worth money.

Closes Wed Sep 30.

https://poidh.xyz/base/bounty/<BOUNTY-ID>
```

## Telegram / GC / Discord (mid-length)

```
NYC trip recap bounty: https://poidh.xyz/base/bounty/<BOUNTY-ID>

60 seconds max, cut from my own footage - the folder link is in the bounty. Density is the brief: the most of what happened in the least time.

0.0125 ETH on Base to the best one, OPEN so the pot can grow.

The new part: I am posting the best of these across 7 channels (Instagram, YouTube, TikTok, Facebook, Farcaster, X, Lens). Each channel gets one clip. If I post yours, that is $5 in $ZABAL to you, credited by handle every time. Seven slots total and they close as they fill, so getting in early is worth something even if you do not win the pot.

Claim on the poidh page with your video link and put your @ in the claim, or you are not entered.

Closes 11:59pm PT Wed Sep 30.
```

## For the ZAO channels, where people know what $ZABAL is

```
Bounty is up: 60 second recap of my NYC trip, footage provided.

https://poidh.xyz/base/bounty/<BOUNTY-ID>

0.0125 ETH to the winner, and up to seven more people get $5 in $ZABAL each - one clip per channel across Instagram, YouTube, TikTok, Facebook, Farcaster, X and Lens. Post yours early and more slots are still open.

This is the first round where not winning still pays. Curious whether that changes who enters.

Closes Wed Sep 30, 11:59pm PT.
```

---

## Reply-cast, right after launch

```
To be clear about the seven slots, since it is the unusual bit:

The ETH is judged at the end, on merit, no matter when you submit. The slots are different - each of the seven channels gets one clip, first good one in takes it, and that is $5 in $ZABAL to whoever made it.

So there is no penalty for submitting late, but there is a reason not to.
```

## Reply-cast, mid-window

Fill in the real numbers before posting. `python3 scripts/query-bounty.py --bounty <BOUNTY-ID>`
prints the claim count; the slot table in `README.md` has what has actually been posted.

```
<N> cuts in on the NYC recap bounty, <N> days left.

<N> of the 7 channel slots are still open, so there is still $ZABAL on the table beyond the pot.

https://poidh.xyz/base/bounty/<BOUNTY-ID>
```

## When posting a used clip on one of the seven channels

Not a bounty announcement - this is the credit line that runs with each posted clip. The
description promises this explicitly, so it is not optional.

```
Cut by @<MAKER>, from an open bounty I ran on poidh - anyone could enter, the footage was public, and I am paying for the ones I use.

<BOUNTY-URL>
```
