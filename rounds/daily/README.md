# Daily poidhz - the spec

Zaal, 2026-09-20: **"let's do daily poidhz."** This is the format. Nothing is cast yet.

## The one rule that makes daily safe

**A daily bounty promises the pot and nothing else.**

That is not caution, it is arithmetic from our own record. `docs/PROMISE-AUDIT.md`, across the
five rounds we have cast:

- **R1 is the only round that kept every promise, and the only round whose entire commitment
  was the pot.**
- Four of five were paid and still left something owed. Every single unkept promise was a
  *publication* promise - announce the winner, pin the clip, run it on our channels, credit
  the entrant. Nobody was ever short-changed on money.
- `postclose-check.py --all` says four rounds owe something **right now**.

A publication promise costs nothing to make, has no deadline forcing it, and we have kept
roughly one in five. At a weekly cadence that is 52 chances a year to break our word. **At a
daily cadence it is 365.** The format that fails is not "daily" - it is "daily plus a promise
we have already proven we do not keep."

So the daily template carries no announcement, no pin, no repost, no credit commitment. Winner
takes the pot, resolved by contributor vote, done. If we later want to publish a winner, we
do it because we chose to that day, not because a bounty said we would.

## Why daily is structurally advantaged

A daily bounty **has a deadline by construction**, and a stated deadline is the strongest
lever we measured: entries roughly double, 74% against 48%, and the effect survives
controlling for format and prize band. 81% of the poidh market carries no deadline at all.
Daily is the only cadence where the strongest lever is free.

It also sits in the best prize band by default. Under $5 runs **69%** with-submission against
43% for $50-plus. Prize size does not buy entries on this platform, so a dollar a day is not a
cheap version of a real bounty - it is the version that measures best.

## The shape

| | |
|---|---|
| **Prize** | $1 to $3, OPEN so anyone can stack on it |
| **Window** | 24 hours, stated with a timezone |
| **Resolution** | contributor vote |
| **Promise** | the pot. Nothing else |
| **Album** | `wethemmedia`, same as every round we cast |
| **Format** | capture-and-show only - see below |

## What to ask for, and what never to ask for

From the wording comparison in `IDEAS.md`, across the 54 open bounties with submissions and
the 45 without, after discarding every word traceable to one issuer posting duplicates:

**Ask for these:** `irl`, `photo`, `clip`, `video`, `show`. Do something and capture it.

**Never ask for these:** `share`, `find`, `help`. Locate, forward or assist. `help` is the
starkest - three issuers, zero submissions between them.

A daily prompt is one line and it is always "do this small thing and show us". Rotate so it
never becomes the same bounty every day:

| Day | Prompt shape | Example |
|---|---|---|
| Mon | ZAO in the wild | photograph a sticker, shirt, screen, poster |
| Tue | 15 seconds | explain one thing about poidh to camera |
| Wed | Your own bounty | cast a $1 bounty and show what came back |
| Thu | Remix | re-cut a past winner, credit them |
| Fri | Artist | 30 seconds on a ZAOstock artist worth watching |
| Sat | Reaction | show a stranger poidhz, film the reaction |
| Sun | Open | entrant picks, any capture-and-show |

## What this costs, stated before anyone commits

$1/day is **$365 a year**. $3/day is **$1,095**. The issuer wallet was **$4.46 short of a
single $5 bounty** on 2026-09-20, so the funding question is not a detail to sort out later -
it is the gate. Decide the daily number and fund a month of it up front, or run it weekly
until that is true.

**A daily bounty that stops appearing is worse than one that never started.** It reads as
abandonment to everyone who entered, and this repo already has four rounds owing.

## Before day one

- [ ] **Cast R8 first.** The daily format should launch into an audience that knows what
      poidhz is. R8 is one payment from live.
- [ ] **Decide the number** - $1, $2 or $3 - and fund 30 days of it.
- [ ] **Close the four owing rounds.** Starting a daily commitment while four rounds owe
      promises is how a cadence becomes a liability. `postclose-check.py --all` must report
      zero.
- [ ] **Write the template** at `rounds/daily/_template/description.md`, pot-only, and run it
      through `validate-bounty-description.py`.
- [ ] **Decide who casts it at the same time every day**, and what happens on the day nobody
      does. That answer is the format's real dependency, not the money.

## Next actions

| Action | Owner | Type | By When |
|--------|-------|------|---------|
| Fund the wallet and cast R8, the summary bounty Kenny asked for - bounty live with an id | @Zaal | Onchain | 2026-09-22 |
| Decide the daily prize and fund 30 days - amount recorded here | @Zaal | Decision | 2026-09-27 |
| Write `rounds/daily/_template/description.md`, pot-only, validator clean | @Zaal | PR | 2026-09-27 |
| Close R2, R3 and R5's ledgers before day one - `postclose-check.py --all` reports 0 owing | @Zaal | Outbound | 2026-10-11 |
