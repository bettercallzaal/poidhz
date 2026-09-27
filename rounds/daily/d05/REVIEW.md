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

---

# The round five entry ledger, measured 2026-09-26 14:46 EDT

**Every row below was read from the chain and from GitHub in the same sitting, not carried
forward.** The ledger exists because this round has two populations that do not line up: five
claims on bounty 1421, and six candidate pull requests on ZAODEVZ/ZAOstock. **A PR is not an
entry until a claim points at it.**

| Claim | Entrant | PR | What it changes | Checks | Verdict |
|---|---|---|---|---|---|
| 8304 | pn-research | **#316** | defers the 1.82 MB Ellsworth video until visible; never on Save-Data or 2g | 4 pass, Vercel fail | MERGE |
| 8305 | pn-research | **#318** | gates the 4.5 MB hero frame preload on Data Saver and 2g | 4 pass, Vercel fail | MERGE |
| 8306 | testies1234321-afk | **#317** | removes one unused `SITE` import; lint 8 warnings to 7 | 4 pass, Vercel fail | MERGE |
| 8309 | i001962 | **#319** | sunlight contrast mode and stage jump controls on /program | 4 pass, Vercel fail | CHANGES REQUESTED |
| 8310 | assay | **#320** | cannot be read | none | BLOCKED, link 404s |
| none | GhostMintOps (BrandonDucar) | **#322** | second answer to the same 1.82 MB video | **held at the first-time gate** | NOT AN ENTRY YET |
| none | GhostMintOps (BrandonDucar) | **#325** | cross-platform path handling in two check scripts | **held at the first-time gate** | NOT AN ENTRY YET, and undersold |

**The four verdicts in rows one to four are the ZAOstock lane's, from its own review this
morning, with its own measurements.** The CHANGES REQUESTED on #319 is not a claim in a
message: `gh api repos/ZAODEVZ/ZAOstock/pulls/319/reviews` reads
`bettercallzaal CHANGES_REQUESTED 2026-09-26T13:56:53Z`, so it is on the PR and the entrant
can see it.

**Vercel fails on all six and it is nobody's fault.** It is a preview deploy a fork cannot
authenticate. Every other job passes on the four that have been allowed to run.

**Nothing is merged, and that is deliberate.** This round's own text says open PRs count and
**merged wins ties**, so merging an entry mid-round is not housekeeping, it is judging. That is
Zaal's hand, not a lane's.

## The two claim-less PRs, and why that is urgent rather than tidy

`GhostMintOps` declared itself an autonomous agent in both descriptions, unprompted, which is
the third entity in this round to do that without being asked. It opened **#322 at 12:43 EDT
and #325 at 13:08 EDT**, and **filed no claim on bounty 1421**. Measured: the five claims cite
PRs 320, 319, 318, 317 and 316, and nothing cites 322 or 325.

**So the most active contributor of the afternoon is currently in line for nothing.** The pot
pays claims, not pull requests. They may simply not know, exactly as @assay may not know their
link is dead, and the round closes 5pm Monday.

**Their CI has not run at all.** Both runs sit at `action_required`
(`fix/windows-cross-platform-check-scripts` and `perf/defer-ellsworth-video-mobile`), the
same first-time-contributor gate the other entrants hit. Only Vercel has reported, and it
fails for forks. **Somebody has to approve those two runs before either can be judged.**

## #322 against #316: one defect, two answers, and they cannot both land

Both defer the same 1,819,337-byte `ellsworth.mp4`, and both edit the same block of
`src/app/page.tsx`. A merge conflict is certain.

| | #316 | #322 |
|---|---|---|
| Where the decision lives | `src/lib/should-autoplay-bg-video.ts`, a pure function | inline in the component's `useEffect` |
| Test | **yes**, 4 unit tests, no DOM needed | **none** |
| Skips the video on | Save-Data, `slow-2g`, `2g`, reduced motion | Save-Data, reduced motion, **and every viewport under 768px** |
| Poster | left in the reduced-motion media query | moved onto `.ellBg` unconditionally |
| Re-checks on resize | n/a, connection-based | **no**, `innerWidth` is read once on mount |

**The difference that is a product decision, not a technique:** #322 gives **no phone the video
at any time, on any network**, because `window.innerWidth < 768` returns before the observer
is ever created. #316 still plays it on a phone on wifi once the section scrolls in. The video
is Candy's look, so which of those is correct is Zaal's call and not a reviewer's.

**One thing #322 does better:** it moves the poster background out of the
`prefers-reduced-motion` block and onto `.ellBg` for everyone, so there is no unstyled gap
before the video mounts and the rule stops being duplicated. **It also leaves
`.ellBg video { display: none; }` inside that media query, which is now dead** - on reduced
motion no video element is mounted at all for it to hide. Same question already put to #318:
is the CSS branch still doing its part, or has it quietly become dead code.

## #325 is described as a Windows fix. It is bigger than that, and it is provable.

The entrant's own framing is "Windows developer environments and multi-OS CI matrix runners".
**All four ZAOstock CI jobs run on `ubuntu-latest`**, so on that framing the PR fixes nothing
anybody runs. That undersells it badly.

The real defect is in the entrypoint guard of the security review gate:

```js
if (import.meta.url === `file://${process.argv[1]}`)   // before
```

`import.meta.url` is a URL and percent-encodes; `process.argv[1]` is a path and does not.
**Run from any directory whose name contains a space and the comparison is false, `main()`
never runs, and `check-pr-review.mjs` exits 0 having audited zero files.** A green gate that
measured nothing - the exact defect this round's own bounty text complains about.

Measured here, Node v23.3.0, four invocations of the same probe file:

| Invocation | `import.meta.url` vs `argv[1]` | old guard ran | new guard ran |
|---|---|---|---|
| absolute path | identical | **true** | true |
| relative path | Node absolutises `argv[1]` | **true** | true |
| **path containing a space** | `guard%20test` vs `guard test` | **FALSE** | **true** |
| via a symlink | link path vs real path | FALSE | **FALSE** |

So the relative-path worry is unfounded and the space one is real. **The fix is correct and it
is not cosmetic.** It is also not complete: row four shows `resolve()` does not follow
symlinks, so invoking the gate through a symlink still skips `main()` silently in both
versions. `realpath` on both sides would close that too, and it is the better thing to ask
them for than a Windows story.

The `check-fact-dedup.mjs` half is a plain correctness fix: `EXCLUDED_FILES` holds POSIX
paths, so on a backslash platform the exclusion never matches and the deliberate venue mention
in `src/app/error.tsx` gets flagged. Nothing in this repo's CI hits it today.

**What to ask for, in one line each:** a test that runs the gate from a path with a space and
asserts it audited more than zero files, and `realpath` on both sides of the comparison.

---

## A fifth and sixth entrant, and the suggestion I was about to make got taken. 2026-09-26 21:10 EDT

**Claim 8328** on 1421, wallet `0x1bd0c711`, citing **PR #330 by metismuse**: converts 4 raw
`<img>` to `next/image` with explicit dimensions, replaces the setState-in-effect in
`LocalStartTime` with `useSyncExternalStore`, removes dead imports, and sets
`eslint --max-warnings=0`. Its own claim says CI is green at 482/482.

**That is the third decay in `FEEDBACK.md` today, and the most interesting one.** The drafted
reply to @testies1234321-afk named `LocalStartTime.tsx:24` as the obvious next rung up from
their lint fix. **Another entrant has now done it and claimed it.** Posting the draft unchanged
would have sent somebody after work that was already finished and filed. The paragraph is
rewritten to say so plainly - that is the round working, not a reason to be discouraged - and to
point at what is still open: the `max-warnings=0` idea is the durable half, because nothing in
this repo currently stops the next warning landing.

**Round five now has 6 claims.** The claim-to-PR map, re-measured:

| claim | PR | entrant |
|---|---|---|
| 8304 | #316 | pn-research |
| 8305 | #318 | pn-research |
| 8306 | #317 | testies1234321-afk |
| 8309 | #319 | i001962 |
| 8310 | #320, which 404s | assay |
| **8328** | **#330** | **metismuse** |

**GhostMintOps still has no claim** on #322 or #325, so the ledger's earlier row stands: the
pot pays claims and two of the afternoon's pull requests are in line for nothing.

**#325 now has a review.** `bettercallzaal CHANGES_REQUESTED 2026-09-27T00:08:12Z`, asking for
`realpathSync` and a two-path test. The ZAOstock lane measured the same guard independently on
Node v20.14.0 and got the same answers this ledger recorded on v23.3.0 - the spaced-path case is
fixed by #325, the symlink case is not. **The two Node versions agree**, which is worth writing
down because the alternative was a disagreement nobody had checked.

---

# Corrections to this ledger, and where round five actually stands. 2026-09-27 08:34 EDT

**Two entries above are wrong and one of them is wrong in the way that matters most here:
it states an inference as a measurement.** Both were found by re-reading the claims rather
than trusting what this file already said.

## Claim 8328 does NOT cite PR #330

Line 372 says *"Claim 8328 ... citing PR #330 by metismuse"* and the table on line 394 maps
8328 to #330. **The claim names no pull request at all.** Its full text describes the work -
four raw `<img>` converted, `useSyncExternalStore` in `LocalStartTime`, dead imports,
`eslint --max-warnings=0`, CI green at 482/482 - and closes with *"Declared: made by Metis
(autonomous agent)"*. There is no number and no link.

**#330 by metismuse does exactly that work, so the match is almost certainly right. It is
still an inference.** The correct row is *"no PR link in the claim; matched to #330 by content
and author, unconfirmed"*, and if that PR is ever judged or paid against 8328 somebody should
say out loud that the claim never named it.

## Claim 8329 cites PR #334, in words, and the watcher could not see it

`scripts/watch-rounds.py` classified **#334 as "no claim cites it, so not an entry yet"**
while claim 8329 sits there titled **"ZAOstock PR 334: skip autoplay hero video on mobile"**.
The extractor matched only `/pull/<n>` URLs, so a pull request named in words was invisible
to it. Fixed on PR #185; the live sweep now reads **5 cited by a claim, up from 4.**

**Claim 8329 has a second problem that is ours, not theirs.** Its entire description is
`https://poidhz.com/api/claim-meta` with no query string, and until PR #184 that endpoint
answered with a **ZABAL Gamez embed card** - so a ZAOstock entry renders another festival's
artwork on the bounty page under their name. The fallback was inherited when the file was
copied from `zabalgames/api/clip-meta.mjs`. **Their claim uri is immutable on-chain**, so
what changes is only what the URL returns. **They should be told they can pass
`?img=&t=&d=`** and get their own work on the card - that belongs in their reply, not a deploy.

## Where round five stands, measured 2026-09-27 08:34 EDT

**7 claims. 11 open pull requests. The two sets are drifting apart, not together.**

| claim | PR | how the claim names it | entrant |
|---|---|---|---|
| 8304 | #316 | link | pn-research |
| 8305 | #318 | link | pn-research |
| 8306 | #317 | link | testies1234321-afk |
| 8309 | #319 | link | i001962 |
| 8310 | #320 | link, **and it 404s** | assay |
| 8328 | **none** | describes the work only | metismuse, by inference |
| 8329 | #334 | **in words, "PR 334"** | testies1234321-afk |

**Six open PRs are cited by nobody:** #322 and #325 (GhostMintOps), #330 (metismuse), #336
(opdevio), and #323 and #338 are Zaal's own. **Three separate contributors have now written
code for this round and filed either no claim or a claim that does not name it.** The pot pays
claims. That is not a rule anyone is breaking; it is a rule nobody has been told clearly
enough, and it is the single thing most likely to end this round with somebody unpaid who
earned it.

**@assay's #320 has now 404d on every check since 01:21 on 26 September**, which is over a day.

---

## The reminder went out. 2026-09-27 08:40 EDT

**Zaal ruled on the unclaimed-PR problem and the comments are posted**, one on each of the four
pull requests whose authors had written code with no claim naming it. Verified from the API
rather than from the report of it - `bettercallzaal` on ZAODEVZ/ZAOstock:

| PR | author | comment posted |
|---|---|---|
| #322 | GhostMintOps | **2026-09-27T12:39:38Z** |
| #325 | GhostMintOps | **2026-09-27T12:39:39Z** |
| #330 | metismuse | **2026-09-27T12:39:40Z** |
| #336 | opdevio | **2026-09-27T12:39:41Z** |

Each says the round pays claims on bounty 1421 rather than pull requests, that the claim must
cite the PR URL before 5pm Eastern on Monday 5 October, and that a second claim naming the PR
is fine.

**The record now shows they were told, and when.** If any of these four goes unpaid it is
because they chose not to file, not because nobody said so - which is the thing this ledger
existed to prevent, and the reason the timestamp is in it rather than just the fact.

## A correction to my own warning about round four's clock

**I wrote that if the round four winner were not accepted on Sunday, "the ads it bought never
run" and the ad would be "paid after the festival it was advertising". That was overstated and
the arithmetic says so.**

Zaal accepts Monday 28 September. A two-day contributor vote puts `resolveVote(432)` on
**Wednesday 30 September**, and the festival is **Saturday 3 October** - **three days clear.**

| | |
|---|---|
| accepts | Mon 28 Sep |
| vote ends, resolveVote callable | **Wed 30 Sep** |
| festival | Sat 3 Oct |
| margin | **3 days, before** |

**The urgency was real and the consequence I attached to it was not.** Holding to watch the
entries properly costs nothing here, and saying otherwise put pressure on a decision that did
not need it. The genuine deadline is that the ad should be *posted* while it can still bring
somebody to the festival, which is a separate thing from when the winner is paid.
