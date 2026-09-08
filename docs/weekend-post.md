# poidhz launch post - Farcaster + X

**DRAFT, unsent.** Zaal posts. Drafted 2026-09-07 off `data/bounty-dashboard.json`
generated the same day.

## Re-measure before posting

Every number below is live and moves daily. **Re-check by 2026-09-11**, and re-measure
before posting regardless - the figures below already drifted once between drafting and now.

**Measured 2026-09-08, and every one of these is re-runnable:**

- **88 open bounties across all chains** (Base, Arbitrum, mainnet), **43 draw zero
  submissions (49%)**, **74 state no machine-readable deadline (84%)**, median prize **$10.99**
  <!-- measured 2026-09-08T19:19Z - zao-measure --verify "poidhz: open poidh bounties, zero-submission share" -->
- Cross-checked against poidh's own API, **Base only: 83 open, 43 zero-submission (52%)**
  <!-- measured 2026-09-08T19:24Z - zao-measure --verify "poidhz: LIVE poidh open-bounty count and zero-submission share (from poidh API, not a local file)" -->

  **Name the scope whenever you quote these.** 88 and 83 are not in conflict - one is every
  chain, one is Base. The zero-submission count is 43 in both; only the denominator moves,
  which is why the share reads 49% or 52% depending on which you mean. A number separated
  from its scope is the same defect as a number separated from its date.
- Our four completed rounds: **36 claims** - R1 11, R2 8, R3 8, R5 9 - never zero
  <!-- measured 2026-09-08T19:20Z - zao-measure --verify "poidhz: BCZ rounds claim counts" -->

**What drifted in one day, which is the argument for re-measuring rather than trusting a
draft:** open bounties 90 to 88, undated share 86% to 84%, median prize $12.12 to $10.99.
The 49% zero-submission figure held. Nothing here was wrong when written; it stopped being
right, which is a different problem and the one these citations exist for.

**Use `bounty-dashboard.json` for every figure here, not `poidh-deadlines-global.json`.**
The two disagree on the dated count (13 vs 11) because the global scan only walks four
pages while the dashboard covers every open bounty. The dashboard is what the site renders,
so it is the one a reader can check you against.

## What this post does NOT claim, and why

The audit that produced these numbers (research doc 2466) killed three framings that would
have been the obvious things to write. Do not put them back:

- **Not "ZAO brings the energy to poidh."** Log a Dog runs a *daily* bounty series at ~$52 a
  day. We have cast five rounds since April. On volume we are out-shipped roughly 30 to 1,
  and that is the first thing anyone checking would find.
- **Not "our community co-funds our bounties."** 47.3% of all prize money this programme has
  paid came from a second funder, and for R3 and R5 that funder is Kenny, from POIDH's own
  grants, offered in DM. It is a partnership, not organic community money. Our own Telegram
  history disproves the community framing.
- **Not any figure about WaveWarZ.** See the do-not-carry list in
  `rounds/_template/description.md`.

What survives a check is completion and tooling. That is what the post leads with.

---

## Farcaster (long) - /poidh primary, cross-post /zao

```
poidhz.com is live.

Every open poidh bounty with a stated deadline, on a calendar, with countdowns and a subscribable .ics feed. Plus every open bounty that does not state one, which is most of them.

I built it because I kept missing deadlines on my own bounties.

poidh has an on-chain deadline field and almost nobody sets it. So the date lives in the description as free text, or nowhere. Right now 74 of the 88 open bounties state no deadline a tool can read - 84%. poidhz parses the text, puts what it finds on a calendar, and is honest about the rest.

Some numbers from building it, which say something about bounties generally:

43 of the 88 open bounties across all chains have zero submissions. Half the board is asking and getting nothing back. The median prize is $11.

Across the five rounds I have run, 36 claims came in, 8 to 11 per round, and not one round drew zero. I do not think that is because my bounties are better written. I think it is because a bounty that nobody sees is indistinguishable from one nobody wants, and most of the work is in the seeing.

It is all open. MIT, fork it, point org.config.json at your own wallet and it runs for your org instead of mine:
github.com/bettercallzaal/poidhz

The data is CORS-open too, so if you want the deadline feed for something you are building, take it:
poidhz.com/data/bounty-dashboard.json

@kennyistyping gave me the /data endpoint that made the whole thing possible, and has boosted more of my rounds than I have asked him to.

poidhz.com
```

## X (under 280)

```
poidhz.com is live.

Every open poidh bounty with a deadline, on a calendar, with countdowns and an .ics feed.

84% of open bounties state no deadline a tool can read. Half get zero submissions.

MIT, fork it:
github.com/bettercallzaal/poidhz
```

## X, alternate - leads with the finding instead of the launch

Use this one if the launch framing feels thin. It travels further because the number is the hook.

```
Half of all open poidh bounties get zero submissions. 43 of 88 across all chains, measured today.

The median prize is $11 and 84% state no deadline a tool can read.

So I built the calendar the platform does not have. Free, MIT, and the data is open:

poidhz.com
```

## Reply-cast, to drop under the main one

```
The part I did not expect: poidh bounties outlive their own deadlines. Several of the dated ones on the board right now are past the date and still open, still claimable. Re-count before posting - that split moves daily.

So poidhz shows those separately rather than hiding them - "past deadline, still open" is a real state, not an error.
```

## Notes for whoever posts

- **Credit Kenny.** The `/data` endpoint he shared on 2026-07-25 is what this is built on, and
  he has funded rounds unprompted. The Farcaster version does this; keep it.
- **Do not post this before R5's winner announcement.** Same reasoning as the Kenny note:
  a launch post that reaches Kenny before R5's winner is public lands while he still believes
  that round closed cleanly.
- **`/zabal` is not the channel for this.** `/poidh` is the audience, `/zao` is the
  cross-post.
