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

## THE BLOCKER - CLEARED AT 00:5x, kept here because the judging rule it created still holds

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

## 00:59 - the gate is lifted and every entry is genuinely green

The ZAOstock lane read all three diffs by hand, confirmed none of them touch a workflow file or
reach a secret, and approved the runs. **Verified here rather than taken from their message:**

| PR | typecheck/tests/build | lint | fact-dedup | review gate | Vercel |
|---|---|---|---|---|---|
| #316 | SUCCESS | SUCCESS | SUCCESS | SUCCESS | FAILURE |
| #317 | SUCCESS | SUCCESS | SUCCESS | SUCCESS | FAILURE |
| #318 | SUCCESS | SUCCESS | SUCCESS | SUCCESS | FAILURE |

**Vercel is the only red and it stays red.** It is a preview deploy a fork cannot authenticate.
That is a permanent condition of every outside entry in this round, so "it passes CI" means the
four workflow jobs, and an entrant must not be marked down for the preview.

**They are keeping the first-time-contributor gate on**, deliberately: it is the reason each
diff got read before it ran. Every future entry needs the same check-then-approve pass, from
them or from Dotfiles. That is a cost worth paying and it is worth knowing about in advance -
if entries arrive while nobody is awake, they will sit.

**AND IT MADE MY OWN DRAFT WRONG WITHIN THE HOUR.** The replies in `FEEDBACK.md` said "your CI
has not run yet". Posting that after the gate lifted would have told two entrants their checks
were stuck while a green tick sat on their pull request. Rewritten at 00:59. This is the same
lesson as the resolveVote timing four hours earlier: a drafted claim about a live system decays,
and the fix is to re-read it in the same breath as sending it.

## 01:2x - five claims, a third and fourth entrant, and one entry pointing at nothing

**PR #319 - i001962 - sunlight contrast mode on /program.** The first entry aimed squarely at
criterion 1, and it reads the brief closely: it quotes `DESIGN.md`'s own line about staying
legible "at 14px on a phone in sunlight" and builds for somebody standing on Franklin Street
at midday. +258/-25 across `globals.css`, a new `ProgramControls.tsx`, the program page and a
test file.

All four jobs pass. **But lint goes from 8 warnings to 10**, and the round's own text says
"Running lint prints warnings and still exits zero, so nothing stops one more landing." This
lands two:

- `ProgramControls.tsx:10` - `'mounted' is assigned a value but never used`
- `ProgramControls.tsx:13` - `Calling setState synchronously within an effect can trigger
  cascading renders`

The second is the **same warning class as `LocalStartTime.tsx:24`**, which is the one existing
warning with real runtime behaviour behind it. An entry that adds an instance of the defect the
bounty complains about should be told before the close, not after it. Both are small fixes and
there are nine days left.

**Claim 8309 points its media straight at `poidhz.com/api/receipt`** rather than rehosting -
the live endpoint as the image. It answers 200 as `image/svg+xml`, 1,953 bytes. **UNKNOWN
whether poidh's claim view renders an SVG**; the two entries that rehosted used PNG. Worth
telling them a PNG is the safer bet, and worth finding out, because if SVG renders then the
whole rehosting step disappears for every future agent.

### CLAIM 8310 REFERENCES A PULL REQUEST THAT DOES NOT EXIST

@assay's wallet (`0xd34f10e2`, the agent that has entered every round of this run) filed a
claim whose description is `https://github.com/ZAODEVZ/ZAOstock/pull/320`. **That URL returns
404.** `gh pr list --state all` shows no #320 in any state, and that account has zero pull
requests on the repo. The highest PR on the repo is #319.

The claim body itself is the most detailed of the five - axe counts before and after in both
colour schemes, a new test that reads `home.module.css` and checks 14 text/fill pairs, and a
note that it fails 16 of 28 on main. **None of that can be verified while the link 404s.**

**This is a "tell them now" case, not a disqualification.** The round runs nine more days, the
claim is plainly made in good faith, and the likeliest explanation is that the push or the PR
creation failed after the claim went out. Answering during the round is exactly the promise
round five makes.

### THE FEEDBACK MECHANIC GOT ITS FIRST USE, AND IT IS A REAL QUESTION

Same claim ends: *"I would like feedback on: 'Rain or shine' moved from brass to sun so it can
pass. Does that sit right with Candy's palette, or would you rather have a darker brass?"*

That is an entrant asking a brand question they cannot answer alone, which is precisely what
the mechanic was for. **It needs Zaal, and it needs him before they finish the work.**

## 02:0x - #319's headline feature does not work, confirmed in a browser

The Zaostock lane spotted this at parse level and said plainly they had not run it in a
browser. **I have now, and they are right.**

`src/app/globals.css` in PR #319:

```css
.site #program-schedule-container.sunlight-active,
@media (prefers-contrast: more) {
  .site #program-schedule-container { ... }
}
```

The comma puts an at-rule where the second member of a selector list should be. **postcss parses
it as ONE rule with a two-member selector list**, the second member being the literal string
`@media (prefers-contrast: more)`. Per the Selectors spec an invalid member invalidates the
entire list, and this is not one of the forgiving `:is()` / `:where()` forms.

**Measured in Chromium, with a control, rather than argued from the spec:**

| | rules the browser kept | computed colour | custom property |
|---|---|---|---|
| #319 as written | **0** | default | empty, rule never applied |
| the same CSS split correctly | **2** | applied | applied |

So the entry's headline feature - the sunlight mode the whole PR is named for - **is dropped
entirely by the browser**, both the manual `.sunlight-active` toggle and the automatic
`prefers-contrast` path. The React toggle flips a class onto an element that has no matching
rule.

**Their own test cannot see it**, and this is the part worth keeping:

```js
expect(cssSrc).toContain("@media (prefers-contrast: more)");
```

It string-matches the CSS **source text**. The broken text contains that string, so the test
passes *because* of the defect it should have caught. That is the same shape as the review gate
that returned PASS after reading zero files, and the same shape as a hostname allowlist with no
test - a green check measuring something other than the thing.

**The fix is two lines**: close the `.sunlight-active` rule, then open the `@media` block
separately. Nine days left, and the entrant should hear it now rather than at the close. A test
that would actually catch it has to assert a computed style, not the presence of a string.

**Not a disqualification and not CI-blocking.** It passed four jobs honestly; no job in this
repo evaluates CSS. It is the single most useful piece of feedback this round has produced.
