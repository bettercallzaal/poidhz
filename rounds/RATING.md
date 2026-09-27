# Every bounty we could cast, rated

Written 2026-09-20. Eight candidates exist in this repo: three numbered and drafted, one
named but unwritten, three unnumbered drafts, and one recurring format that has never run.

**Rated against what we measured, not against how good the idea sounds.** The numbers come
from ZAOOS research doc `business/2522-poidh-live-bounty-market`, taken across all 99 open
bounties on poidh on 2026-09-20:

| Lever | Effect |
|---|---|
| **A stated deadline** | entries roughly **double** - 74% vs 48%, and it survives controlling for format and prize band |
| **Format** | photo **68%**, clip **64%**, build 52%, code **43%**, social 33% |
| **Prize size** | **no effect**. Under $5 runs 69%, $50+ runs 43% |
| **Our own record** | 8-11 claims per round at $27-66, so our entry rate comes from format and promotion |

One caveat carried from that doc: `created_at` is empty on all 99 rows, so the format and
prize tables are uncontrolled for how long each bounty has been open. The deadline finding
survived controls; the others are patterns in the standing set.

## The ranking

| # | Bounty | Format | Ready? | Cost | Verdict |
|---|---|---|---|---|---|
| 1 | **R8 - promo post for poidhz** | any, clip/photo likely | **$4.46 short, nothing else** | $5 | **CAST IT** |
| 2 | **R9 - ZAOstock content** | clip + photo | not drafted | ~$5-25 | **DRAFT NEXT** |
| 3 | **R7 - WaveWarZ clip round 2** | clip 64% | placeholder + overdue re-check | $33 | Fix the source problem first |
| 4 | **R6 - NYC trip recap** | clip 64% | needs Drive link + one sentence | $33 + $35 | Parked by choice, and complex |
| 5 | **weekly - "this is for the ZAO"** | video 64% | machinery only, never run | recurring | **Do not start yet** |
| 6 | **unlock-solo** | clip 64% | needs Unlock | ? | Blocked on someone else |
| 7 | **unlock-cofund** | clip 64% | needs Kenny AND trigs | $10 | Blocked on two someone-elses |
| 8 | **zabal-bugfix** | code **43%** | never cast | ? | **Worst format we measure** |

## Why each

**1. R8, promo post for poidhz.** The only one that is one payment from live. Format-open so
entrants self-select into the cheap formats that actually get entries, real deadline, $5 seed
in the highest-entry prize band, and OPEN so the pot can grow - which is the mechanic the
round is demonstrating. Kenny reviewed the concept and pushed it from a meta idea-competition
to promo posts, which also moved it from an abstraction to an artifact. **Blocked on $4.46.**

**2. R9, ZAOstock content.** Zaal called it highest priority on 2026-09-20 and the asset kit
at zaostock.com/brand is genuinely ready - moose mark by attabotty, posters, texture, palette,
font, one-click zip. Clips and posters are the two best-performing formats we measure, 64% and
68%. The only reason it is not first is that it does not exist yet. **Write it next.**

**3. R7, WaveWarZ clip round 2.** Good format, and R5 proved the audience. Two problems, and
the second is structural: a `<DAY>` placeholder still in the description, and **Twitch keeps
non-affiliate VODs for 7 days** while the round runs two weeks - so half the source material
expires mid-round. Its own re-check date passed on 2026-09-13 and has not been actioned. Fix
the source window before casting, not after.

**4. R6, NYC trip recap.** Parked by Zaal, not blocked by us. It needs a Drive link and one
sentence about the trip, both his. It also carries the most untested mechanic we have - one
pot plus seven channel slots paying $5 in $ZABAL each, bounded at $35 - which pays up to eight
people instead of one. Worth running eventually because it is the best demonstration of the
spend-rail idea, but it is a new payout shape and a new round at the same time.

**5. weekly, the recurring video competition.** `rounds/weekly/` contains a template and a
README and **has never run a single week.** Rated low on our own record rather than on the
idea: four of five rounds we have cast were paid and still left a promise unkept, and a
recurring format multiplies that exposure every week. Start it when the promise ledger for a
one-off round closes clean. It is a good idea we have not yet earned.

**6 and 7. The two Unlock rounds.** Both are clip bounties, which is the right format.
unlock-solo needs Unlock Protocol; unlock-cofund needs Kenny **and** trigs at Unlock DAO to
both agree, for a $10 pot. The coordination cost exceeds the prize by an order of magnitude.
Keep them drafted; do not chase them.

**8. zabal-bugfix.** Code bounties are the **worst-performing format we measure, 43%**, and
the effect showed up at issuer level too: one issuer's 7 code bounties totalling $108 drew
14%, while another's 3 photo bounties totalling $7.89 drew 100%. The doc's first decision is
not to repeat the code-bounty shape. This is that shape.

## What the ranking is really saying

The top two are the two that ask for an **artifact somebody can make in an afternoon**, have
a **date**, and **cost almost nothing**. Everything below them is blocked on a person, a
platform, or a promise we have not proven we keep.

The cheapest round we have ever considered is the one most likely to get entries, and that is
not intuition - it is the measured shape of this platform.

## Next actions

| Action | Owner | Type | By When |
|--------|-------|------|---------|
| Fund the issuer wallet $4.46 and cast R8 while Kenny is engaged - bounty live, id in `default_bounty_ids` same day | @Zaal | Onchain | 2026-09-22 |
| Draft R9 ZAOstock off the /brand kit, clip and poster led, real deadline - `rounds/r9/description.md` passes `validate-bounty-description.py` | @Zaal | PR | 2026-09-27 |
| Re-measure the Twitch archive window and fix R7's `<DAY>` placeholder, or change the source - `precast-check --round 7` clean | @Zaal | PR | 2026-10-04 |
| Close R2, R3 and R5's promise ledgers before starting anything recurring - `postclose-check.py --all` reports 0 rounds owing | @Zaal | Outbound | 2026-10-11 |

---

## The code round recruits strangers. Measured 2026-09-27 08:55 EDT, and it cuts against the 43% above.

**The format table rates code the worst thing we can cast: 43% entry rate, against 68% for
photo and 64% for clip.** Round five is a code round and the entry count agrees - 7 claims,
where the media rounds ran 8 to 11. **But the table counts claims, and claims are not the only
thing a code round produces.**

**Six of the nine people who have worked on round five had never entered this programme
before.** Measured against `data/claims.json`, with controls that prove the filter works:

| round five contributor | prior mentions in claims.json |
|---|---|
| assay | 6 |
| coolhat *(control, media rounds)* | 6 |
| pascaline *(control)* | 7 |
| leoxcrane *(control)* | 5 |
| pn-research | 1 |
| ghostmintops | 1 |
| **testies1234321-afk, i001962, brandonducar, metismuse, opdevio, 0xnuminous** | **0 each** |

**Five media rounds drew largely from one returning pool. One code round pulled in six people
who had never touched it.** Two of those six arrived on the same day, 27 September, with no
prompting from any post.

**So the 43% is measuring the wrong thing for our purposes.** A photo round gets more claims
from people we already have. A code round gets fewer claims and more *new* people, and the
artifact it leaves behind is merged into a repo rather than posted once. If the goal is entries
per round, the table is right. If the goal is the thing `docs/community-plan.md` measured -
**10 of 35 entrants ever return** - then the format that brings strangers is worth more than
its entry rate suggests.

**The cost is a step every one of them missed.** All six new contributors filed code with either
no claim or a claim that did not name the pull request, because a code contributor's instinct
is that opening the PR *is* the submission. **The pot pays claims.** Five reminder comments had
to be posted by hand on 27 September to close that gap, and a PR-template line is going in so
the next stranger reads it before opening the PR rather than after.

**For round six:** if it is a code round, the claim instruction belongs in the repo the
contributor is already looking at, not only in the bounty text they may never read.

### Correction: that table counted handles, and the pot pays wallets. 2026-09-27 13:05 EDT

**The claim above that "six of the nine people who have worked on round five had never entered
this programme before" counted GITHUB HANDLES.** A handle is not an entrant. The pot pays the
wallet that files the claim, and the two do not map one to one.

**What surfaced it:** claim 8338 arrived citing PR #352, whose GitHub author is
`kepler-ops-maker` - a handle with zero prior mentions anywhere in `data/claims.json`, which
by the old method is a seventh stranger. **The wallet behind it is `0x5a844e78`, which also
filed claims 8304 and 8305 in this round and claim 8312 in round four.** One wallet, three
public identities: `pn-research` and `kepler-ops-maker` on GitHub, `inkier35` on X.

**Round five by wallet, which is the unit that gets paid:**

| wallet | claims | PRs cited | GitHub handles behind them |
|---|---|---|---|
| `0x5a844e78` | 3 | #316, #318, #352 | **kepler-ops-maker, pn-research** |
| `0x1bd0c711` | 2 | #330 | metismuse |
| `0xb55fe134` | 2 | #317, #334 | testies1234321-afk |
| `0xd34f10e2` | 1 | #320, which 404s | (assay) |
| `0xa21e6116` | 1 | #319 | i001962 |

**Five wallets. Nine claims. Three of the five had never entered before** - `0x1bd0c711`,
`0xb55fe134` and `0xa21e6116`. The other two entered round four, and one of those entered
rounds two and four.

**So the corrected figure is three of five, not six of nine, and the argument survives it.**
A code round still brought in more first-time entrants than a media round did, and it is still
the format that reaches people the returning pool does not. The number was inflated by counting
every GitHub account that opened a pull request, including four that have never filed a claim
at all and therefore are not entrants in any sense the pot recognises.

**Nothing here is against the rules and nobody is accused of anything.** The round says you may
enter as many times as you like, one operator running several accounts is ordinary for agents,
and that wallet's PRs are among the strongest work in the round. It is recorded because **one
entrant holding three of nine claims and two of the best pull requests is a judging fact**, and
because a table that counts the wrong unit will keep being wrong in the same direction.

**The lesson is the same one this repo keeps relearning:** a proxy that is cheaper to reach -
a handle in a PR - was used for the thing that actually matters, which is who the money goes
to. **Count wallets.**
