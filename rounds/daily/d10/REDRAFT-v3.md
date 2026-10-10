<!-- NOT-ANNOUNCEMENT-COPY: internal redraft. Names no deadline anyone submits to. -->
# Round ten, redraft v3 - best marketing rollout on WaveZStation, one month, artists sign up

Written 2026-10-10 after the Grill relayed Zaal's answers (vault `decisions/grill-2026-10-09-seat-morning.md`,
items 96 to 99). His words, verbatim and in order:

1. Q1, the buy: picker "Two buys of 500", then *"2 500$ buys if we need to split the top prize save this for this week"*.
2. Q2, the DM: "DM before the buy". He sends it.
3. Q3, what goes public: no option picked; *"Maybe we say best marketing rollout give it a month and people have to sign up"*.

**Nothing in this file is ruled. It is the reading that makes all three answers fit, and three questions.**

## The reading

Read together, the three answers describe one round, not a buy plus a round:

- **The $1,000 is the prize, not a purchase we make first.** "Split the top prize" only makes sense if the
  $1,000 is a prize. Two buys of $500 is how the prize splits if two artists finish level.
- **The prize is paid as a WaveZStation buy of the winner's song.** That is the original idea (10 Oct, relayed:
  a $1,000 buy "with the best artist", 45% straight to them, first four figures on the site), and it is what
  makes the prize worth more than $1,000 to the artist: $450 in their wallet the second it lands, $450 into
  their song's fan pool for their supporters, and the title.
- **"Best artist" is decided by a contest: best marketing rollout of a song on WaveZStation, over one month.**
- **Artists sign up to enter.** "People have to sign up" is the entry condition. The natural reading is the
  artists, since only an artist with a song listed on WaveZStation can receive a buy.
- **"This week"** then means the round opens this week, not that the buy lands this week.

This replaces the plan where Zaal buys the current most-funded song first. Saturday in LA's artist is
not pre-selected; he enters like everyone else, and the pitch to him becomes an invitation.

## The round, as it would run

| | |
|---|---|
| Who can enter | any artist with a song listed on wavezstation.com, or who lists one by the sign-up close |
| Sign-up | by Sunday 19 October, 11:59pm Eastern: name, the song's WaveZStation link, where the rollout will be posted |
| The ask | run a marketing rollout for that song over the month: posts, clips, reaction videos, shows, collabs, whatever moves people to buy in. Post it publicly as it happens. |
| Close | Friday 14 November 2026, 5:00pm Eastern (four weeks from the Friday after sign-up; the date is this lane's reading of "give it a month") |
| What is judged | the rollout itself (clarity, consistency, craft) AND what it moved on the site, which this lane can measure at a stamp from the site's own `/api/discover` and `/api/songs`: supporters gained and fan pool growth from sign-up close to round close |
| Top prize | a $1,000 buy of the winning song from Zaal's wallet, or two $500 buys if he splits it between two artists. Verified by Basescan hash. 45% to the creators in the same transaction, 45% to the song's fan pool, 10% to the platform. |
| Credit | the winner is the first song on WaveZStation past four figures in sales (bound: the most-sold song had about $802 on 10 Oct). If the winner is already the most-sold song, the line still holds; if not, it needs re-checking at the close. |
| Fans | the reaction round from PR #244 can run alongside, pinned to the winning song after the buy lands, or be dropped. Not part of this redraft. |

**The money.** Each $500 buy: $50 platform, $225 creators, $225 fan pool. A $1,000 buy on one song: $100,
$450, $450. Zaal's own claimable share depends on whether he already supports the winning song: about 21%
of Saturday in LA, UNVERIFIED on every other song.

**What the record says about this shape** (`docs/what-draws-entries-2026-10-01.md`, ZAOOS doc 2522
re-measured 10 Oct): the hardest asks draw the least (our "run your own bounty" round drew 2; a month-long
build is the lowest-entry format on poidh). A stated deadline and one named room to post in help. A sign-up
step is a filter, not a draw: expect few entrants, and the right few. Twenty-seven songs are listed on the
site today, so the whole possible field is about twenty artists.

## Where poidh fits, and the rule it brushes against

poidh pays ETH. A WaveZStation buy is not a poidh payout. So the $1,000 prize is a promise in the bounty
text that the pot does not cover, and this repo's standing rule is that a bounty promises the pot and
nothing else (`rounds/daily/README.md`, from `docs/PROMISE-AUDIT.md`: every broken promise we ever made
was a promise outside the pot). It is Zaal's rule to set aside, and if he does, the text has to say exactly
who pays, from which wallet, by when, and that it is verified by hash. Question 3 below is this.

## Three questions for Zaal

**Q1. Is this the round?** The $1,000 (or two $500) is the prize for the best marketing rollout, paid as a
buy of the winning artist's song, after a month.
- A) Yes. Open sign-ups this week, close 14 November, buy the winner's song then. **Recommended: it is the
  reading in which all three of his answers agree.**
- B) No. Buy the current most-funded song this week as planned (two $500), and run the rollout contest as a
  separate round eleven with its own prize.
- C) Both halves: $500 into today's most-funded song this week, $500 into the rollout winner in a month.

**Q2. What is the sign-up?**
- A) A poidh claim by 19 October with the song link counts as the sign-up; the final claim by 14 November
  is the rollout. Public, on chain, feeds the Submitters leaderboard, no new tool. **Recommended.**
- B) A form (Tally or Google Form) linked from the bounty, with the entrant list on poidhz.com.
- C) Reply to the announcement post or DM Zaal.

**Q3. How the prize is written, given the pot-only rule.**
- A) poidh pot of $100 in the reward field (what the contributor vote confirms) AND the $1,000 buy stated in
  the text as Zaal's own pledge, wallet named, verified by hash, with the rule set aside for this round by
  his decision. **Recommended, and this lane records that it is the first promise outside the pot since
  the audit.**
- B) The whole prize in the poidh pot as ETH, no WaveZStation buy: about 0.40 ETH at today's price. Clean on
  the rule, but the artist gets ETH instead of a four-figure song.
- C) No poidh bounty for the artists at all: sign-up and judging on poidhz.com, the buy is the prize, and
  poidh carries only the fan reaction round.

Default if unanswered: nothing opens, nothing is bought, nothing is posted.
