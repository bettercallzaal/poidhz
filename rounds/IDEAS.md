# New bounty ideas, and the pattern they come from

Written 2026-09-20, after rating the eight we already have in `RATING.md`.

## What the live market taught us tonight

Read across all 99 open bounties: 54 have submissions, 45 have none. Comparing the wording of
the two groups turns up a pattern, **after** throwing out every word that came from a single
issuer posting duplicates.

That filter matters and it killed half the result. `public`, `kindness`, `random`,
`screenshot` and `verified` all came from ONE issuer each - three copies of "Random Act of
Kindness", three of "Show this code in public". Those are not signals, they are one person's
posting habit. The same duplicate trap produced a false "SOLO beats OPEN" finding earlier
today.

What survives, with 2 to 3 distinct issuers behind each word:

| Gets entries | Gets nothing |
|---|---|
| `irl`, `photo`, `clip`, `video`, `show` | `share`, `find`, `help` |

**The shape: bounties that ask you to DO something and CAPTURE it get entries. Bounties that
ask you to LOCATE, FORWARD or ASSIST do not.** "Film yourself doing X" works. "Find us a good
X", "share our post", "help us with X" does not. `help` is the starkest - three issuers, zero
submissions between them.

**Confidence: suggestive, not established.** Two or three issuers per word is a thin base, and
this is the same uncontrolled-for-age data as everything else in doc 2522. It agrees with the
stronger format finding (photo 68%, clip 64%, code 43%), which is why it is worth acting on at
$5 and not worth betting a big round on.

**The immediate warning: do not run a "share our announcement" bounty.** It is the obvious
next idea after R8 and it is the exact shape that gets nothing.

## Ideas, rated on the same scale

Every one is capture-and-show, carries a date, and sits in the cheap band that measures best.

| # | Idea | Format | Why it should work | Cost |
|---|---|---|---|---|
| 1 | **Show a stranger poidhz and film their reaction** | video + irl | hits both surviving signals at once, and the artifact IS the ad | $5 |
| 2 | **Print a ZAOstock poster and photograph it somewhere real** | photo + irl | photo is the best format we measure; the /brand kit already ships the poster | $5 |
| 3 | **Film 15 seconds explaining poidhz to someone who has never heard of it** | video | forces the clarity the R8 rubric asks for, and is reusable as onboarding | $5 |
| 4 | **Your ZAOstock artist, 30 seconds, why they are worth watching** | clip | puts the spend on the lineup rather than on us | $10 |
| 5 | **Cast a $1 bounty of your own and show us what came back** | irl + show | teaches the mechanic by making people use it; the entry is proof they did | $5 |
| 6 | **Photograph the ZAO in the wild - sticker, shirt, screen, anywhere** | photo + irl | cheapest possible entry, and it builds a library we can reuse forever | $3 |
| 7 | **Re-cut one of our past five rounds' winning clips** | clip | source already exists, so effort is minutes; credits the original winner again | $5 |
| 8 | **Show your first minute on poidhz - screen record it, warts and all** | video | usability research we would otherwise pay for, disguised as a bounty | $5 |

## The two I would run after R8 and R9

**Idea 5, "cast a $1 bounty of your own and show us what came back", is the strongest thing on
this page.** Every other idea produces an ad. This one produces a *user*. It is the only
bounty here whose completion requires the entrant to become an issuer, which is the exact
behaviour poidhz exists to create, and the proof of completion is on chain and unfakeable.
Cheap to run, and the entries are a public demonstration that the mechanic works.

**Idea 1, "film a stranger's reaction", is the best ad we could commission.** It is also the
only one where the artifact and the evidence are the same file - there is no way to fake the
reaction shot, and an honest confused reaction is more useful to us than a polished one.

## What not to build, on the same evidence

- **Anything asking people to share, find, boost or help.** Measured: nothing.
- **Another code bounty.** 43%, the worst format we measure, and `zabal-bugfix` is already
  drafted and already last in `RATING.md`.
- **A big-prize round to "get serious".** Prize size does not buy entries. $50+ runs 43%,
  under $5 runs 69%.
- **A recurring format**, until `postclose-check.py --all` reports zero rounds owing. We have
  four owing right now.

## Next actions

| Action | Owner | Type | By When |
|--------|-------|------|---------|
| Cast R8, then pick one of ideas 1 or 5 as R10 - draft exists at `rounds/r10/description.md` | @Zaal | PR | 2026-10-11 |
| Re-run the wording comparison once 20 more bounties have closed, to see whether the capture-vs-locate split holds on a bigger base - result appended here | @Zaal | PR | 2026-10-25 |
| Do NOT draft a "share the announcement" round - recorded here so it is refused rather than re-proposed | @Zaal | Decision | DONE 2026-09-20 |
