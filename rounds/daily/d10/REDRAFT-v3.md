<!-- NOT-ANNOUNCEMENT-COPY: internal redraft. Names no deadline anyone submits to. -->
# Round ten, redraft v3 - best marketing rollout on WaveZStation, one month, artists sign up

Written 2026-10-10 after the Grill relayed Zaal's answers (vault `decisions/grill-2026-10-09-seat-morning.md`,
items 96 to 99). His words, verbatim and in order:

1. Q1, the buy: picker "Two buys of 500", then *"2 500$ buys if we need to split the top prize save this for this week"*.
2. Q2, the DM: "DM before the buy". He sends it.
3. Q3, what goes public: no option picked; *"Maybe we say best marketing rollout give it a month and people have to sign up"*.
4. Then, item 103 (vault 0bdcb9e6): *"500 in poidh I'll buy 500 and they buy 500 of their favorite"*.

**Nothing in this file is ruled. It is the reading that makes all four answers fit, and three questions.**

## The reading, after item 103

Item 103 says where each $500 goes, and it is three halves, not two:

| Who pays | How much | Where | What it is |
|---|---|---|---|
| Zaal, into the poidh pot | $500 (about 0.20 ETH at $2,497) | the bounty's reward field, paid in ETH to the winning artist's wallet when the claim is accepted | **the prize** |
| Zaal, from his wallet | $500 USDC | a buy of the winning artist's song on WaveZStation | **the buy**: $225 to the song's creators the second it lands, $225 into its fan pool, $50 platform |
| The winner | $500 | a buy of their favourite song on WaveZStation, their own choice | **the pass-along**: the prize goes back into the site, to an artist the winner picks |

So "two buys of 500" are one by Zaal and one by the winner; "split the top prize" is the $1,000 split into
the pot and the buy; "this week" is when the round opens. The winner ends up with $500 in ETH plus $225
(or their share) in USDC, and the site sees $1,000 of buys: Zaal's into the winner, the winner's into
their favourite. **Zaal's total outlay on this reading is $1,000.** If he means the winner's $500 to be
on top of the prize rather than out of it, it is $1,500 and the third row is a second buy from his wallet.
That is question 1.

**The pass-along cannot be enforced by poidh.** The pot pays the moment the claim is accepted; nothing
on poidh can hold it back until the winner buys. Either it is a stated expectation we post about when
it happens, or the order flips: the winner posts the hash of their $500 buy first and the claim is
accepted after, which means the artist fronts $500 of their own money for up to a day. That is
question 3.



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
| Top prize | $500 in the poidh pot, paid in ETH on accept, plus a $500 buy of the winning song from Zaal's wallet, verified by Basescan hash (45% to the creators in the same transaction, 45% to the song's fan pool, 10% to the platform). The winner then buys $500 of their favourite song on the site. |
| Credit | a $500 buy makes the winning song the first past four figures in sales only if it already has about $500 sold (Saturday in LA has $802; AI LUI $587; everything else is under $360 as of 10 Oct). So the four-figure line is conditional and is not promised. |
| Fans | the reaction round from PR #244 can run alongside, pinned to the winning song after the buy lands, or be dropped. Not part of this redraft. |

**The money.** Each $500 buy: $50 platform, $225 creators, $225 fan pool. Zaal's own claimable share
depends on whether he already supports the winning song: about 21% of Saturday in LA, UNVERIFIED on
every other song.

**What the record says about this shape** (`docs/what-draws-entries-2026-10-01.md`, ZAOOS doc 2522
re-measured 10 Oct): the hardest asks draw the least (our "run your own bounty" round drew 2; a month-long
build is the lowest-entry format on poidh). A stated deadline and one named room to post in help. A sign-up
step is a filter, not a draw: expect few entrants, and the right few. Twenty-seven songs are listed on the
site today, so the whole possible field is about twenty artists.

## Where poidh fits, and the rule it brushes against

poidh pays ETH. The $500 pot is a normal poidh prize. Zaal's $500 buy is a promise in the bounty text that
the pot does not cover, and this repo's standing rule is that a bounty promises the pot and
nothing else (`rounds/daily/README.md`, from `docs/PROMISE-AUDIT.md`: every broken promise we ever made
was a promise outside the pot). It is Zaal's rule to set aside, and if he does, the text has to say exactly
who pays, from which wallet, by when, and that it is verified by hash. The pass-along is a second promise,
made by the winner, which the text can ask for but not enforce.

## Three questions for Zaal

**Q1. The total, and the shape.** Item 103 read as three halves: $500 pot in ETH to the winner, $500 buy of
the winner's song from your wallet, and the winner buys $500 of their favourite song.
- A) Yes, that is it, and your total is $1,000: the pot plus your buy. The winner's $500 comes out of the
  prize they just won. **Recommended: it is the reading in which items 96 to 103 all agree.**
- B) Your total is $1,500: the pot, your buy of the winner's song, AND a $500 buy of the winner's favourite
  song, all from your wallet. The winner spends nothing.
- C) Something else; type it.

**Q2. What the sign-up is.**
- A) A poidh claim by Sunday 19 October with the song's WaveZStation link counts as the sign-up; the final
  claim by Friday 14 November 5pm Eastern is the rollout. Public, on chain, feeds the Submitters
  leaderboard, no new tool. **Recommended.**
- B) A form (Tally or Google Form) linked from the bounty, with the entrant list on poidhz.com.
- C) Reply to the announcement post or DM you.

**Q3. The winner's $500 buy, which poidh cannot enforce.**
- A) It is the stated expectation, not a condition: the text says the winner is asked to put $500 into their
  favourite song, and we post their hash when they do. The pot pays on accept as normal. **Recommended:
  it is honest about what poidh can hold back, which is nothing.**
- B) It is a condition: the winning claim is accepted only after the artist posts the hash of their own
  $500 buy, so they front $500 for up to a day. Enforceable, and the one thing most likely to make an
  independent artist walk.
- C) Drop the pass-along. Pot plus your buy, nothing asked of the winner.

Default if unanswered: nothing opens, nothing is bought, nothing is posted.
