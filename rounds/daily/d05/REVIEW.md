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

## The reminder now also went to #341. 2026-09-27 08:55 EDT

Zaal ruled the same note goes on any new unclaimed PR this week. Verified from the API:
**`bettercallzaal` on #341 at 2026-09-27T12:53:17Z**, and its body is **byte-identical** to
the one on #322 - both hash to `5ac5ab8145748b15b4e3565a1aca7962b02467a2`, so it is the same
note rather than a similar one.

#341 was opened at 12:49:40Z, **ten minutes after the first four reminders went out**, by a
contributor who had therefore never been told. Five PRs have now been reminded: #322, #325,
#330, #336, #341.

## The reminder worked, and here is the measurement. 2026-09-27 09:15 EDT

**Claim 8334 landed about 34 minutes after the note went on #330**, from the same wallet as
claim 8328, and it does exactly what the note asked:

> *"Entry for bounty 1421 (ZAOstock Round 5). PR:
> https://github.com/ZAODEVZ/ZAOstock/pull/330 - zero-warning lint ... By Metis (agent)."*

| | |
|---|---|
| reminder posted on #330 | **2026-09-27T12:39:40Z** |
| claim 8334 filed, citing the PR by URL | **about 34 minutes later** |
| wallet | `0x1bd0c711`, the same as claim 8328 |

**This also settles the correction above.** That section said 8328's mapping to #330 was
*"matched by content and author, unconfirmed"* and warned that judging #330 against 8328 would
be acting on an inference. **The entrant has now confirmed it themselves, in a claim that names
the URL** - so #330 is an entry by citation rather than by my guess. The inference happened to
be right, which is not the same as having been safe to rely on, and it is only not relied on
because the round text's "a second claim naming the PR is fine" gave them a way to fix it.

**The live sweep moved with it: 6 open PRs cited by a claim, up from 5.**

```
open PRs on the code repo: 11 - 6 cited by a claim (#316, #317, #318, #319, #330, #334),
                                5 not an entry (#322, #325, #336, #341, #343)
```

**Still uncited: #322 and #325 (GhostMintOps), #336 (opdevio), #341 (0xnuminous), #343
(Ariyachan).** The last two arrived after the first four reminders went out; #343 is new since
and is queued for the same note.

**Round five is now at 8 claims.**

## Sixth reminder, and a blocker on our side that matters more. 2026-09-27 09:25 EDT

**#343 has the note.** `bettercallzaal` at **2026-09-27T13:13:33Z**, comment id 5856177117,
body byte-identical to #322's - both bodies hash to
digest: 5ac5ab8145748b15b4e3565a1aca7962b02467a2. Six PRs reminded: #322, #325, #330, #336,
#341, #343.

**No second note is needed anywhere.** The one on #330 produced a citing claim in 34 minutes,
so the note works when it is read, and repeating it within hours would be nagging a round that
runs to 5 October.

### FOUR WORKFLOW RUNS ARE HELD, AND ONE OF THEM BELONGS TO A CLAIMED ENTRY

The first-time-contributor gate is still holding runs, and the list has moved since this
morning:

| PR | branch | CI | cited by a claim? |
|---|---|---|---|
| #322 | - | **4 jobs pass** | no |
| #325 | - | **4 jobs pass** | no |
| **#334** | `fix/mobile-video-autoplay` | **HELD - only Vercel has reported** | **YES, claim 8329** |
| #336 | `docs/stale-claims-r5-v2` | HELD | no |
| #341 | `feat/home-running-order-cta` | HELD | no |
| #343 | `codex/fix-tablet-nav-overflow` | HELD | no |

**#322 and #325 were approved since this morning and are green.** The four above are not.

**#334 is the one that matters.** It is a real entry - claim 8329 names it, in words, which is
the claim that exposed the extractor gap - and **its CI has never run.** Nothing but Vercel has
reported on it, and Vercel fails for every fork. So an entrant who did everything asked of
them, including filing a claim that names the PR, **cannot be judged on checks, and the reason
is on our side of the fence.**

**Approving those four runs is worth more than any further reminder.** A reminder asks the
entrant to act; this one asks us to.

## The four held runs were approved and all four are green. 2026-09-27 09:44 EDT

Zaal ruled the seat approves them and it is done. **`action_required` on ZAODEVZ/ZAOstock is
now 0.** Conclusions read from the runs API rather than from the report of them, job by job
rather than as an aggregate word:

| PR | run | typecheck/tests/build | lint | fact-dedup | review gate |
|---|---|---|---|---|---|
| **#334** | 36291982968 | **success** | **success** | **success** | **success** |
| #336 | 36312416260 | success | success | success | success |
| #341 | 36320287359 | success | success | success | success |
| #343 | 36321417524 | success | success | success | success |

**Sixteen of sixteen jobs passed. Nothing went red, so nothing is red for a reason on our side
of the fence** - which was the thing worth checking, since the hold itself had been ours.

**#334 is the one that mattered and it is now judgeable.** Claim 8329 names it, its four jobs
pass, and the only red left anywhere is Vercel, which no fork can authenticate. An entrant who
did everything the round asked can now be assessed on the same evidence as everybody else.

**#336, #341 and #343 are green but still uncited.** Passing CI is not an entry; the pot pays
claims. All three carry the reminder.

## Round five, as it stands

**8 claims, 11 open pull requests, 6 of them cited by a claim.**

| cited | uncited |
|---|---|
| #316, #317, #318, #319, #330, #334 | #322, #325, #336, #341, #343 |

`#320` is still claimed by 8310 and still 404s, now for over a day.

## Measured: PR #334 does not save the bytes it claims. 2026-09-27 10:11 EDT

**The change is +5/-0 in `home.module.css`**, adding `display: none` on the video under
768px, with the comment *"Phones on cellular shouldn't have to download the full autoplay
video"*.

**display: none does not stop an autoplaying video downloading.** Run in Chromium at 390x844
against a control, both pages loading the real `ellsworth.mp4` from zaostock.com:

| page | computed display on the video | .mp4 requests |
|---|---|---|
| the #334 rule active | **none** | **1** |
| control, same page, rule inert | block | 1 |

**The control held** - the visible version also made one request, so the counter works and the
difference between them is **zero**. The element stays in the DOM, autoplay fires the fetch,
and the phone pays the full 1.82 MB. **It now pays for a video it is then not shown**, which is
worse than before the change.

**This is the exact trap the round was written about**, and another entry in the same round
spells it out in its own PR description: *"autoplay wins over preload='none' - the browser
fetched the 1.8 MB mp4 on first load"*. To save the bytes the element has to not be rendered,
or its `src` has to be withheld until it is wanted.

**Recorded before it reached the entrant**, because the first version of this finding was
reasoned from the mechanism rather than measured, and a reasoned finding is how somebody gets
told something wrong with confidence. The trace is what makes it sayable.

## Three green PRs nobody had reviewed. 2026-09-27 10:34 EDT

#336, #341 and #343 have had four passing jobs since the held runs were approved and **no
technical review at all**. None is cited by a claim, so none is an entry yet - all three carry
the reminder. Reviewed anyway, because the round promises answers while it runs and because a
green tick is not a review.

### #343 Ariyachan - the overflow is real, and worse than the description says

The change is `sm:flex` to `lg:flex` on the nav and `sm:hidden` to `lg:hidden` on the
hamburger, five lines. **They also rewrote the comment their change invalidated** - the old one
said the hamburger appears under 640px, which their own diff makes false. That is the habit this
repo keeps asking for.

**Measured on the live site rather than taken from the description**, Chromium against
zaostock.com/program:

| viewport | document width | overflow | the RSVP control |
|---|---|---|---|
| 390px | 390 | 0 | inside |
| 640px | **822** | **182px** | **OUTSIDE, right edge at 822** |
| 768px | **828** | **60px** | **OUTSIDE, right edge at 828** |
| 820px | 831 | 11px | OUTSIDE |
| **840px** | 840 | **0** | inside |
| 1024px | 1024 | 0 | inside |

**The site-wide primary action is off-screen between 640 and about 832 pixels.** That is worse
than a cosmetic overflow and it is exactly what they said, so the entry is sound.

**One number in their description does not match.** They report 845px at a 640px viewport; it
measures **822**. The 768px figure of 828 is exact. Either the page changed under them or that
one was noted rather than read - worth saying because everything else they wrote held.

**And the fix is correct but wider than the defect.** The overflow clears at **840px**, and
`lg` is 1024, so the nav is hidden across roughly 184px of viewport where it fits fine.
Tailwind ships nothing between `md` at 768 and `lg` at 1024, so `lg` is the nearest stock
answer and the choice is defensible. An arbitrary variant - `min-[840px]:flex` - would hide
the nav only where it actually breaks.

### #341 0xnuminous - careful, and it reads like someone who has done this before

A second action beside RSVP in the hero, linking to /program. Twelve lines. **Every detail that
usually gets skipped is present:** a 48px minimum height, which is the touch-target floor; a
`focus-visible` outline so it is reachable by keyboard; `flex-wrap` so it wraps rather than
overflowing on narrow screens; the palette taken from the existing CSS variables so it follows
both colour schemes; and `Link` rather than an anchor, so it uses client routing like the rest
of the app.

**Reading it beside #343 turned up something about the repo, not about either entry.** The
header comment says the RSVP button deliberately points at /tickets rather than straight at
`FESTIVAL.rsvpUrl`, because the site-wide primary action used to skip past the ticket page.
**The hero's RSVP still goes direct to `FESTIVAL.rsvpUrl`.** So the decision recorded in the
header was never applied to the larger button on the home page. That is on main, neither
entrant put it there, and it is the kind of thing only visible when two PRs are read together.

### #336 opdevio - documentation correctness, and the numbers check out

Three files. It adds `check:facts` and `check:review` to the list of commands CONTRIBUTING
tells you to run, corrects the public surface count, and deletes the retired `/team` section.

**Verified independently rather than trusted.** The CI job list measured from the workflow this
morning is typecheck/tests/build, lint, fact-dedup and the security and database review gate -
which is exactly the six npm commands they now list, where the old text listed four.

**Their route count is exact.** Counting `page.tsx` entrypoints on a current checkout: **40
total, 5 under the retired `/team`, leaving 35** - the number they wrote. One small thing to
check: they describe the code-gated backstage sheet as one entrypoint and there are **two**
`page.tsx` files under that path, so either one is an index or the sentence undercounts by one.

## PR #352, the fix #334 attempted, and a decision that belongs to Candy. 2026-09-27 12:59 EDT

**`kepler-ops-maker`, opened 2026-09-27T16:57:17Z**, another contributor new to the
programme - "kepler" returns 0 mentions in `data/claims.json` against a control of 7 for
"pascaline". No claim cites it.

**The code half is the fix #334 attempted and missed**, arrived at independently. It extracts
`shouldLoadVideo` as a pure function with its own tests and renders a still `<img>` rather
than a hidden `<video>`, so the mp4 is never fetched. Their comment says it outright:
*"CSS alone hid the video but still downloaded it."*

**The other half re-encodes the hero video, and that is not a reviewer's call.** Measured, with
a control that scored a video against itself at SSIM 1.000000 before anything else was trusted:

| | main | #352 |
|---|---|---|
| bytes | 1,819,337 | **1,136,654** (-37.5%) |
| resolution | 960x540 | 960x540 |
| frame rate, frames, duration | 24fps, 312, 13.000s | **identical** |
| bitrate | 1,119,592 | 699,479 |
| SSIM against the original | - | **0.960** (luma 0.946, chroma 0.988) |
| PSNR | - | **36.6 dB** avg, 32.9 min |

So it is a pure re-encode: nothing dropped, nothing resized. The quality cost is real but mild
and lands almost entirely in luma detail, **which matters less here than almost anywhere else
because `.ellBgFade` lays a gradient plus `rgba(0,0,0,0.32)` over the whole thing.** The
artifacts sit under a 32 percent black wash.

**It looks like a good trade and it is Candy's asset, so the question went to Vault rather than
being answered here.** The PR also bundles both changes, so the component fix cannot be taken
without the re-encode - the review suggested splitting the video into its own PR.

**Posted from Zaal's account, both verified from the API:** the reminder at
**16:59:02Z** (comment id 5857891326), body byte-identical to the first one by shasum, and a
**COMMENTED** review at **16:59:04Z** - not Changes requested, because nothing in it is wrong.

## Seven open PRs now carry the reminder, counted rather than tallied

Checked every open PR on the repo for a first maintainer comment matching the reminder's
digest: **#322, #325, #330, #336, #341, #343, #352**. Seven.

## The review worked in five and a half minutes, and it produced a judging problem. 2026-09-27 13:08 EDT

**The split happened.** The COMMENTED review on #352 at 16:59:04Z suggested separating the
video so the component fix could be judged alone. **By 17:04:34Z the entrant had done it:**

- **#352** is now the component only - `HeroVideo.tsx`, its test, the CSS and page.tsx,
  +109/-3 across four files. **The mp4 is gone from it.**
- **#353** is the re-encoded video alone.
- **#354** arrived two minutes later.

That is three separate times today that a posted note changed what an entrant did, and this
one took five and a half minutes. The review was submitted at 16:59:04Z and #353 was created at
17:04:34Z. This section first said seven; that figure was arithmetic done in my head and it was
wrong. Both timestamps come from the API.

### But #354 re-implements two other entrants' claimed work

**#354 touches the identical eight files as #330**, which was opened 17 hours earlier and is
claimed by a different wallet. Reading the diff rather than the file list, #354 contains:

| what #354 changes | already submitted by |
|---|---|
| remove the unused `SITE` import in `llms.txt/route.ts` | **#317**, claim 8306, wallet `0xb55fe134` |
| `eslint . --max-warnings=0` in package.json | **#330**, claim 8334, wallet `0x1bd0c711` |
| `useSyncExternalStore` replacing setState-in-effect in `LocalStartTime` | **#330**, same claim |
| **four** `eslint-disable` lines with written justifications | **new** |
| remove an unused `Card` import in `meetings/page.tsx` | **#330**, same claim |
| remove a stale disable in `opengraph-image.tsx` | **#330**, same claim |

Both earlier changes were verified against those PRs' own diffs, not inferred from titles.

**#354 is from wallet `0x5a844e78`, which already holds three claims in this round** (8304,
8305, 8338) and entered round four. So if #354 merged, two other wallets' submitted changes
would land inside a third wallet's pull request.

**Nothing here breaks a rule and intent is unknowable from the outside.** Every one of those
warnings is discoverable by running `npm run lint`, so independent convergence is entirely
plausible - three entrants have now independently found `LocalStartTime`. The other PRs are
also public, so reading them is possible. **There is no way to tell from here and no need to
guess.**

**What makes it matter is the round's own rule.** Open PRs count and **merged wins ties**, so
merge order is consequential, and merging #354 would quietly resolve a tie in favour of the
wallet that submitted last. **That is a decision, not housekeeping**, and it is Zaal's.

**The genuinely new part of #354 is FOUR eslint-disable justifications**, which neither
#317 nor #330 wrote - two in `BioEditor.tsx`, one in `TeamRoles.tsx`, one in
`MemberProfileView.tsx`, each explaining why an arbitrary user-supplied photo URL cannot go
through `next/image`. That is real work and it is worth separating from the rest when judging.

**AND THE OVERLAP IS LARGER THAN THIS SECTION FIRST SAID.** Two rows above were marked new and
are not: #330 makes the identical `Card` import change in `meetings/page.tsx` and touches the
same stale disable in `opengraph-image.tsx`. So #354 duplicates #330 on **four** of its changes
rather than two, which **strengthens the merge-order point rather than softening it** - more of
#354 is already sitting in another wallet's claimed pull request than the first table showed.

**All three corrections came from an independent reviewer on PR #201, and all three were
verified here against the API before being accepted.** The errors were mine: a time gap done in
my head, a count taken from reading rather than from `grep -c`, and two rows called new without
checking them against the pull request they overlap.

**Round five now stands at 9 claims, 14 open PRs, 7 cited.**

## PR #353, the re-encode nobody claimed - measured 2026-09-27 15:1x EDT

**#353 is not cited by any of the nine claims.** It was split out of #352 on maintainer
feedback ("the re-encode changes a designer asset and waits on her sign-off"), and the claim
that cites #352, claim 8338, does not mention it. So the work exists, is open, and is
currently outside the judging set. That is the entrant's to fix, not ours to assume.

**Every byte claim in it is exact.** `public/brand/home/ellsworth.mp4` goes 1,819,337 ->
1,136,654 bytes: **-0.683 MB, -37.5%**, against a body claiming "-37.5%" and "~0.68 MB".
Downloaded both blobs at the PR's own base and head SHAs (`922c30b0`, `f70836f3`) rather
than trusting the diff, which reports `0+/0-` for a binary.

**The invariance claim holds and the numbers in it do not.** ffprobe on both files: h264,
**24/1 fps, 13.000000 s, 312 frames counted, zero audio streams, moov before mdat** - all
identical before and after. But the body says "Same 1280x720" and **both files are 960x540**.
And it credits itself with "audio stripped (it is a silent background loop)" when **the
original already carries zero audio streams**, so nothing was stripped. Two wrong facts in a
verification section, in a PR whose whole case is that it measured rather than guessed.

**SSIM is right, including the part that is easy to get wrong.** All: **0.960092** against a
body claiming "SSIM 0.96 overall". The body also says the loss "concentrates in luma detail",
and it does: **Y 0.945944 against U 0.987984 and V 0.988792**. PSNR y 35.0 dB, min 32.9.
A self-comparison control scored **1.000000**, so the filter was reading frames.

**One suspicion recorded because it was wrong.** Claim 8338's title is "hero video payload
-38% (PR #352)", and -38% sits close enough to #353's -37.5% that it read as the re-encode
credited to the wrong PR - especially since #352's file list carries **no mp4 at all**, only
`HeroVideo.tsx`, its test, `home.module.css` and `page.tsx`. The claim's description settles
it: "1.8 MB no longer fetched for constrained mobile/reduced-motion visitors". That is the
deferral, which is what #352 does. **No misattribution. The number was checked before the
accusation was written down, which is the only reason it is not in this file as a finding.**

**Wallet 0x5a844e7871e0cd7dcf080046e3c17d0c637cd58b now holds 3 of the 9 claims on 1421**,
and #353 would be a fourth piece of work from it if claimed. Counted from `issuerAddress` on
`fetchBountyClaims`, not from GitHub handles.

## PR #363 - the zone bug is real and well tested, the refactor riding with it is not

**Measured 2026-09-27 16:0x EDT, nine minutes after it opened.** #363 from
`testies1234321-afk`, head `c44cfaab`, two files, +66/-15. No claim cites it yet, so it is
not an entry - and its body already carries the round's claim reminder, so the entrant has
been told.

**The bug it names is real.** The old check was
`zone.includes('New_York') || zone.includes('Eastern')`. **America/Toronto, America/Detroit,
America/Kentucky/Louisville and America/Indiana/Indianapolis are all Eastern time and match
neither substring**, so viewers there were shown the redundant "That's 12 PM EDT in your time
zone." line the component exists to suppress. The fix compares the festival instant formatted
in the viewer's zone against the same instant formatted in `America/New_York` and returns null
when they are identical. That is semantic rather than name-based and it is the right shape.

**Its test file is the best of any entry this round.** Five zones that must be suppressed,
including all four the old check missed, plus Europe/London and Asia/Kolkata as controls that
must still convert. A test that only asserted the happy path would have proved nothing here.

**AND THE SAME DIFF MOVES THE COMPUTATION INTO A `useState` INITIALIZER, WHICH IS A
HYDRATION MISMATCH.** The old code did the work in `useEffect`, so the first client render
returned null exactly as the server had, and the text appeared after mount. The new code runs
`useState(() => { if (typeof window === 'undefined') return null; ... })`, so:

- **Server:** `typeof window === 'undefined'` is true, returns null, and the component emits
  no `<p>` at all.
- **Client, first render:** the initializer runs, computes the text, and the component emits
  a `<p>`.

`src/app/live/page.tsx` has **no `'use client'`**, so it is a server component and
`<LocalStartTime />` is server-rendered into the HTML. Server HTML has no element where the
client's first render has one, which is the definition of a hydration mismatch. **Nothing in
the test file can see this** - `hydrat`, `useState` and `render` each appear 0 times in it,
because it tests `localStartTimeText`, a pure function, and the defect is in the component.

**The two changes are separable, which is what makes this worth saying rather than just
scoring.** `localStartTimeText` is a good export and the zone fix needs none of the render
change; keeping `useEffect` and calling the new function from inside it fixes the bug with no
hydration risk. Recommendation is to ask for that split rather than to fail the entry.

**Not measured:** I did not run the page and read a console warning. The finding is from the
client/server boundary and the diff, and it should be confirmed against a running build
before it is put to the entrant as fact.
