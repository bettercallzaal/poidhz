# R8 launch readiness - what is left before the first bounty goes up

Measured 2026-09-20. Every line is a thing someone does, with how to check it is done.

**Where it is:** the Kenny bundle is SENT. The round is drafted, validated and not cast.
`precast-check --round 8 --prize 0.0019` blocks on exactly one item.

## The number, and who to thank

**R8 is the 20th bounty in the `wethemmedia` album on poidh, and only BCZ's 5th.**

Measured from `bounties.fetchByAlbum`, album `wethemmedia`, all three statuses, 2026-09-20:
19 distinct bounties exist in it. Four are ours - 1151, 1166, 1180, 1330. R4 (1249) was
canceled and is not in the album, which is why our count reads 4 rather than 5.

**The other 15 are We Them Media's own**, and they are real media work, not test posts:

```
229  Is the Internet Spreading Truth or Misinformation?
231  "What is Ethereum?" Street Interview
240  "What Is the Most Important Global Issue Today?"
247  "What's Made You Smile Today?" Street Interview
278  "What's Your Take on the USA Today?" Street Interview
279  Open Reporter Audition
281  We Them Media Clipping Bounty
282  Jingle Bounty - One Month
283  On The Ground - We Them Media Cultural Scout Bounty
284  Lights Out Nigeria - We Them Media Testimony Bounty
310  Bigger Red Flag: AI Lover or Crypto Trader?
1131 Find Someone Who Remembers
1169 WTM X Pizza Day
1239 We Them Media x DEGEN Clip Challenge
1269 Ask the World One Question
```

**One caution, recorded because it nearly went into public copy.** `fetchByAlbum` **ignores
`chainId`** - it returns the identical 19 rows for Base, Arbitrum, mainnet and Degen. Keying
by `(chain, id)` gives 76 and a confident wrong answer of "R8 is #77". The tell was Degen
returning 19 when Degen's RPCs could not be reached at all. Dedupe on bounty id alone.

## Blocking, in order

- [ ] **Fund the issuer wallet.** Short **0.001662 ETH, $4.38**. This is the only thing
      `precast-check` still blocks on. Re-run it after funding, do not assume.
- [ ] **Wait for Kenny's reply.** Zaal, asked whether the round waits on him: **"after"**.
      The message is sent; the gate is his answer, not our send.
- [ ] **Re-read the deadline.** The description says 11:59pm PT Sunday October 4 with the
      vote by Tuesday October 6. Those assume a cast on or before **2026-09-22**. If Kenny
      takes a week, move both or the round ships with a window shorter than the two weeks
      it was designed for.
- [ ] **Re-price the $5.** `0.0019 ETH` is $5.00 at $2,633.31, the price read on 2026-09-20.
      Re-check at cast time; the pot is small enough that a 20% ETH move is visible.

## At cast time

- [ ] Paste **only** the text between the sentinels in `description.md`. Title field:
      `Tell us how to announce poidhz`.
- [ ] Type **OPEN**. Not SOLO. The pot growing is the entire argument of this round.
- [ ] File it in the **`wethemmedia`** album, per the locked convention since R1.
- [ ] Add the new bounty id to `default_bounty_ids` in `org.config.json` **the same day**.
      R5 was not, and nine claimants scored zero on the leaderboard for weeks before anyone
      noticed by hand.
- [ ] Move R8 from `planned_rounds` into `rounds` in `org.config.json`.
- [ ] `python3 scripts/refresh-rounds.py` so `/about` and `/hub` show it as OPEN. Both pages
      default to "no round is open" and will keep saying that until the feed says otherwise.

## Right after it is live

- [ ] `python3 scripts/postclose-check.py --scaffold --bounty <id> --round 8` to write the
      promise ledger while the text is fresh. Four of five past rounds were paid and left
      owing something because nobody wrote the promises down at cast time.
- [ ] Seed the pot yourself with a second small contribution from a different wallet if one
      is available. An OPEN bounty at exactly the seed amount does not visibly demonstrate
      that the pot grows; one top-up does.
- [ ] Post it in `/poidh` on Farcaster and tag @bettercallzaal, per the round's own floor
      rules. 5,681 people follow that channel.

## What follows it

**R9, the ZAOstock content round.** Zaal, 2026-09-20: *"asking people to make content with
zaostock from the /brand page thats highest priority"*, format-open - clips, posters,
anything, artist spotlights, and interviews via Paragraph. The asset kit already exists and
is good: https://zaostock.com/brand ships the moose mark by attabotty, posters, a texture,
the palette, the font and a one-click zip. Not drafted yet.
