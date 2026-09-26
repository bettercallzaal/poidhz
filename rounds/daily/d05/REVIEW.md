<!-- NOT-ANNOUNCEMENT-COPY: internal review notes on round five entries. Names no deadline anyone submits to. -->
# Round five - entries as they arrive

Bounty 1421, closes Monday 5 October 5pm ET. **Nothing here is posted.** Zaal answers entrants;
this is the measured basis for it.

**Every check below was run locally on a clean clone**, because the repo's own CI has not run on
any entry - see the blocker at the bottom, which is the most important thing on this page.

## The state at 2026-09-26 00:1x, four hours after cast

**Three pull requests, two entrants, zero claims on the bounty yet.** All three landed within
about 100 minutes of the cast, and all three are working targets named in the bounty text or in
`docs/zaostock-pr-targets.md`. That is the brief being read, not guessed at.

| PR | Entrant | What it does | typecheck | lint | test | build |
|---|---|---|---|---|---|---|
| [#317](https://github.com/ZAODEVZ/ZAOstock/pull/317) | testies1234321-afk | removes an unused import | PASS | PASS | PASS | PASS |
| [#316](https://github.com/ZAODEVZ/ZAOstock/pull/316) | pn-research | defers the 1.8 MB background video | PASS | PASS | PASS | PASS |
| [#318](https://github.com/ZAODEVZ/ZAOstock/pull/318) | pn-research | skips a 4.5 MB hero preload on Data Saver | PASS | PASS | PASS | PASS |

## THE BLOCKER, and it is ours rather than theirs

**GitHub reports `action_required` on the CI run for all three pull requests.** That is the
first-time-contributor gate: a maintainer has to press "Approve and run" before any workflow
executes on a fork's PR. Until someone does:

- no entry will ever show a green check, however good it is
- the only status visible on each PR is `Vercel: FAILURE`, which is the preview deploy, not the
  test suite

**Round five's immutable text says "IT PASSES CI. typecheck, lint, test, build."** If the round
were judged on the checks GitHub displays, every entrant would fail a bar they are not permitted
to clear. **A missing check is not a failed check**, and the judging must not treat it as one.

**The action is a maintainer's**, in ZAODEVZ/ZAOstock, on each PR. It is not this seat's to
take and nothing here works around it.

Meanwhile the checks were run by hand, on a clean `--depth=1` clone with `npm ci` and no
`.env.local`, and **all three pass all four**. The numbers above are that run, not a prediction.

## #317 - testies1234321-afk, removes an unused import

One line. `src/app/llms.txt/route.ts` imported `SITE` and never used it.

**Verified rather than taken on trust.** `SITE` occurs exactly once in that file, on the import
line. And the claim is controlled both ways: **main lints at 8 warnings, this branch at 7**, and
the `SITE` warning is the one that disappears.

It is the smallest possible entry and it is completely honest: the description says what was
wrong, how they knew, and that they ran the four commands. It declares itself as the work of an
autonomous agent, unprompted, which is exactly the standard the bounty asked for.

**What it does not do** is change anything a visitor sees. Against the round's own order -
criterion 1 is "makes the site better to use" - a lint fix sits low. That is not a criticism of
the work; it is where the work sits on this particular ladder.

## #316 - pn-research, defers the background video

**This is the target the bounty names in its own body**, and the diagnosis is exact: `autoPlay`
beats `preload="none"`, so the 1.8 MB mp4 was fetched on first load for every visitor including
those who never scrolled to that section.

The shape of the fix is the part worth praising:

- the policy is a **pure, DOM-free function** in its own file, with four unit tests, because
  this repo has no jsdom and they noticed rather than adding one
- `navigator.connection` is read through optional chaining, so Safari, which does not implement
  it, is not broken
- there is a real fallback: `typeof IntersectionObserver === 'undefined'` loads immediately
  rather than leaving a permanently blank section
- the observer is disconnected on unmount and after first intersection
- the poster still covers every path, including refusal of autoplay in low-power mode

**One thing to check before merging**, and it is a question rather than a defect: the comment
they replaced said reduced motion was already handled in `home.module.css`. The new component
checks `prefers-reduced-motion` in JavaScript as well. Two guards for one rule is safe, but
somebody should confirm the CSS branch still does its part rather than silently becoming dead.

## #318 - pn-research, skips the hero preload on constrained connections

Same author, same discipline, a different asset: 68 hero frames, about 4.5 MB, preloaded on
`window.load` for everybody.

The guard's default is the right way round - **no Network Information API means keep current
behaviour**, so a browser that cannot report its connection is never degraded. The scrub still
works when the preload is skipped; frames fetch on demand.

## What I am not doing

Not posting any of this. Not approving the workflow runs. Not merging anything. The bounty
promises that Zaal answers questions while the round runs, and that promise is his to keep.

**Judging note for the close:** the round says an OPEN pull request is a complete entry and
merged only breaks ties. All three are open and mergeable. None has been claimed on the bounty
yet, and the entry is the claim, not the pull request.

## 00:33 - three claims, and the receipt flow got its first real test

All three pull requests are now claimed on 1421. **The claim is the entry, so the round has
three entries from two entrants**, four hours after cast.

**THE BROWSERLESS AGENT PATH WORKS, AND IT WAS USED WITHIN THE HOUR.** Claims 8304 and 8305
(@pn-research) carry a 1200x630 PNG that is **our own receipt card** - "POIDHZ SUBMISSION
RECEIPT", the AGENT badge, round 5, `ZAODEVZ/ZAOstock#316`, `@pn-research`, and the footer line
saying the card is a picture rather than an entry. They fetched `/api/receipt`, rasterised the
SVG themselves and rehosted the PNG on nostr.build, because poidh needs an uploaded image.
That is exactly the route the endpoint was built for, taken by an agent with no browser, with
no instructions beyond the bounty text.

**Claim 8306 has no image at all.** Its media field contains prose - "Autonomous agent claim.
This claim was submitted by an autonomous AI agent, as the bounty brief requests. PR: ..." -
where poidh expects a URL. The PR link is in the description and readable, so the entry stands
on its merits, but the claim will render without a picture on the bounty page.

**That is worth fixing for them rather than marking them down for.** The round requires the
receipt, they are the entrant who did not use it, and the honest reading is that a required
step got missed by one of the two people who tried - which is a discoverability result about
our page, not a character result about them. Tell them where the receipt is; do not dock them.

| claim | entrant | PR | media |
|---|---|---|---|
| 8304 | @pn-research | #316 | our receipt card, rehosted |
| 8305 | @pn-research | #318 | our receipt card, rehosted |
| 8306 | (unresolved wallet) | #317 | prose in the media field, no image |

Both wallets are UNRESOLVED on the leaderboard feed, which is normal for a first entry and
means their feedback pages cannot be filed by handle yet.
