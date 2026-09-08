# poidhz launch post - Farcaster + X

**DRAFT, unsent.** Zaal posts. Drafted 2026-09-07 off `data/bounty-dashboard.json`
generated the same day.

## Re-measure before posting

Every number below is live and moves daily. **Re-check by 2026-09-09**; after that treat
every figure here as unverified and re-run before posting:

```bash
python3 scripts/build-bounty-dashboard.py
```

Measured 2026-09-07: **90 open bounties**, **44 draw zero submissions (49%)**, **77 state no
deadline (86%)**, median prize **$12.12**, **$6,412** in open prize money platform-wide.
Of the 13 that do state a date, **6 are already past it and still open.**
Our own four completed rounds: **36 claims**, 8 to 11 each, never zero, at prizes of $26-$63.

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

poidh has an on-chain deadline field and almost nobody sets it. So the date lives in the description as free text, or nowhere. Right now 77 of the 90 open bounties state no deadline a tool can read - 86%. poidhz parses the text, puts what it finds on a calendar, and is honest about the rest.

Some numbers from building it, which say something about bounties generally:

44 of the 90 open bounties have zero submissions. Half the board is asking and getting nothing back. The median prize is $12.

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

86% of open bounties state no deadline a tool can read. Half get zero submissions.

MIT, fork it:
github.com/bettercallzaal/poidhz
```

## X, alternate - leads with the finding instead of the launch

Use this one if the launch framing feels thin. It travels further because the number is the hook.

```
Half of all open poidh bounties get zero submissions. 44 of 90, measured today.

The median prize is $12 and 86% state no deadline a tool can read.

So I built the calendar the platform does not have. Free, MIT, and the data is open:

poidhz.com
```

## Reply-cast, to drop under the main one

```
The part I did not expect: poidh bounties outlive their own deadlines. Six of the thirteen dated ones on the board right now are past the date and still open, still claimable.

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
