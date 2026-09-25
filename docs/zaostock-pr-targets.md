<!-- NOT-ANNOUNCEMENT-COPY: internal target list for another repository. Names no deadline anyone submits to. -->
# ZAOstock - what is actually worth a pull request

Measured 2026-09-25 against a fresh `--depth=1` clone of `ZAODEVZ/ZAOstock` at **`b017c87`**,
with every command run rather than read about. Companion to `docs/repo-readiness-zaostock.md`,
which asked whether a stranger *can* contribute; this asks **what they should contribute**.

**A bounty that asks for pull requests owes entrants real targets.** Round five's cast text says
"if you find something better, do that instead", and that still holds - this is a floor, not a
list to work through.

## First, the claim round five makes about credentials is TRUE, verified end to end

Round five's immutable text says: *"Clone it, npm ci, and then npm run typecheck, npm run lint,
npm run test and npm run build all work with no secrets at all."* Run on a clean clone with no
`.env.local` at all:

| Command | Result | Wall time |
|---|---|---|
| `npm ci` | exit 0, 601 packages | 16s |
| `npm run typecheck` | exit 0 | 8.4s |
| `npm run lint` | exit 0, **8 warnings** | 15.9s |
| `npm run test` | exit 0, **56 files, 462 tests, all passing** | 4.8s |
| `npm run build` | exit 0, 40 routes | 13.8s |

**Under a minute from clone to a verified build, with nothing to ask anyone for.** That is the
strongest thing this repo has to offer an agent, and it is now measured rather than asserted.

## 1. `check:review` reports PASS after reviewing ZERO files

**The highest-value target in the repo, because it is a check that cannot fail on the thing it
exists to catch.** On a clean clone:

```
$ npm run check:review
[check-pr-review] target @ HEAD b017c87...
  no changed files to review
  OVERALL VERDICT: PASS
exit 0
```

`scripts/check-pr-review.mjs` asks `git diff --name-only HEAD` (empty on a clean tree), then
`git diff --name-only HEAD~1...HEAD`, then **returns `[]` and prints PASS**. Two further
consequences of that range:

- On a `--depth=1` clone `HEAD~1` does not exist at all, so the fallback cannot work either.
  Agents clone shallow.
- Even with full history it reviews **only the last commit**. A three-commit pull request gets
  one commit audited, and the two before it are never read.

**What a good PR does:** scope the audit to `origin/main...HEAD` so it sees the whole branch,
and make an undeterminable range exit non-zero with UNKNOWN instead of printing PASS. A gate
that green-lights an empty set is worse than no gate, because it is quoted as evidence.

**Test it honestly.** The fix is only proven by a control: plant a string the pattern must catch,
confirm the gate fails, remove it, confirm it passes.

**One thing to know before you touch this file.** `findZaoReviewGate()` hands off to a
`zao-review-gate` binary if one exists in `~/bin` or on `PATH`. On a maintainer's machine that
binary runs instead and full-scans 684 files - where it currently reports a HIGH finding on
`public/ops/index.html:739`, which is a **false positive on a `data:image/png;base64,` URI**, not
a credential. Keep the handoff; fix the fallback.

## 2. The homepage ships 3.07 MB, and one autoplaying video is 58% of it

Measured live against `zaostock.com/`, every same-origin asset in the HTML fetched:

| | |
|---|---|
| Same-origin assets referenced | **28** |
| Total transferred | **3.07 MB** |
| `/brand/home/ellsworth.mp4` alone | **1.78 MB** |
| The HTML itself | 69 KB, TTFB ~0.13s |

The server is fast. The payload is not, and this is a festival site people open on a phone, on
Downeast cell service, possibly standing on Franklin Street.

`src/app/page.tsx:174` is also self-contradictory:

```jsx
<video src="/brand/home/ellsworth.mp4" poster="..." autoPlay loop muted playsInline preload="none" />
```

`preload="none"` asks the browser not to fetch it; `autoPlay` makes it fetch it anyway. The
poster is already a 100 KB webp that carries the same picture.

**What a good PR does:** any of - respect `prefers-reduced-motion`, hold the poster and load the
video only on interaction or when it scrolls into view, re-encode it smaller, or drop it. **Bring
the before and after numbers**, measured the same way, not "improved performance".

## 3. Eight lint warnings on `main`, and nothing stops a ninth

`npm run lint` exits 0 because warnings do not fail, so they accumulate. All eight, exact:

| File | Line | Warning |
|---|---|---|
| `src/app/llms.txt/route.ts` | 2 | `'SITE' is defined but never used` |
| `src/app/meetings/page.tsx` | 5 | `'Card' is defined but never used` |
| `src/app/opengraph-image.tsx` | 88 | unused `eslint-disable` directive |
| `src/app/team/BioEditor.tsx` | 170, 227 | `<img>` instead of `next/image` |
| `src/app/team/TeamRoles.tsx` | 158 | same |
| `src/app/team/m/[slug]/MemberProfileView.tsx` | 29 | same |
| `src/components/poster/LocalStartTime.tsx` | 24 | `setState` called synchronously in an effect |

The last one is the only one with runtime behaviour behind it - it can cascade renders, and the
component's whole job is to render a time. The four `<img>` warnings are a judgement call, not
an automatic fix: `PartnerTile.tsx` already carries a reasoned `eslint-disable` explaining why a
partner mark should not go through the optimiser. **Copy that standard: either convert, or
disable with a reason.**

**A stronger version of this PR** turns the warning count into a ratchet so the ninth cannot land
quietly.

## 4. One end-to-end spec for forty pages

`e2e/` contains exactly **one** file, `checkout.spec.ts`, against **40 `page.tsx` routes**.
Playwright is already configured (`playwright.config.ts`) and `npm run test:e2e` exists, so the
cost of a second spec is writing it, not wiring it.

The obvious first ones are the pages a stranger actually lands on: `/`, `/artists`, `/program`,
`/tickets`. All four return 200 live and are static, so they are cheap to assert against.

## 5. The test runner spends more time starting workers than testing

`npm run test` says so itself, unprompted:

```
Isolate  56 workers spawned - ~353ms startup each (spawn + environment, per file)
         at least ~1.84s faster with isolate: false - reuses workers across files instead of one per file
```

4.82s total, of which 4% is worker spawn per the same report. **This is a config PR with a number
attached**, and the honest version of it checks that the suite still passes with isolation off
rather than assuming shared workers are safe - some tests are not.

## 6. Every clone pays for 60 MB of media

`public/` is **60 MB**; the shallow `.git` is **59 MB**. The heaviest committed files:

| Size | File | Referenced |
|---|---|---|
| 18 MB | `public/brand/audio/zaostock-radio-interview-2026-09-10.mp3` | once |
| 12 MB | `public/brand/zaostock-brand-kit.zip` | once |
| 3.3 MB | `public/brand/posters/2026-lineup-poster-1600x2000.png` | twice |
| 3.2 MB | `public/ops/assets/zaostock.mp3` | once |

**Every one is referenced, so none is dead** - this is not a delete-unused-files PR, and treating
it as one would break the brand kit page. It is a "should a 30 MB download live in git" question,
and the answer is a maintainer's to give. **Ask in an issue before writing that PR.**

## 7. CONTRIBUTING.md leads with the one thing you do not need

The Setup section opens with `cp .env.example .env.local` and *"You'll need real values for
`NEXT_PUBLIC_SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`"*. True for `npm run dev` against live
data. **Not true for typecheck, lint, test or build**, which is what a contributor is going to do
first and what CI runs on their PR.

It also lists four commands under "Before you push" while `.github/workflows/ci.yml` runs **six
jobs**: typecheck/test/build, lint, `check:facts`, and `check:review`. An entrant who runs the
four documented ones can still be surprised by two.

And `npm run check:exposure` **cannot be run by an outside contributor at all** - it exits 2 with
"No project URL. Set NEXT_PUBLIC_SUPABASE_URL". That is correct behaviour, and nothing says so.

**A documentation PR that fixes this is worth as much as a code one** for a repo that is about to
ask strangers for pull requests.

## 8. 164 markdown files under `docs/`

Round five's cast text already says it: *"A PR that deletes something no longer true is worth as
much as one that adds something."* Nothing in this pass audited which of the 164 are stale, so
**this target carries no measurement and is listed as unmeasured on purpose.** Anyone taking it
should bring the evidence that a specific file is wrong, not a count.

## What this pass did NOT measure, named so nobody reads silence as clean

- **Accessibility beyond alt text.** Contrast, focus order, keyboard traps: not tested. Alt text
  itself is fine - 27 of 27 `<img>` elements carry `alt`, and the two apparent misses were the
  string `<img>` inside code comments, which is the same line-based-grep trap this estate has hit
  before.
- **Bundle sizes per route.** The build log for this Next version prints no size column, so no
  number is quoted. Not zero - unknown.
- **Runtime behaviour of the API routes**, which need Supabase credentials this seat does not and
  should not have.
- **Lighthouse, Core Web Vitals, or anything needing a real browser profile.**
- **Whether the two open issues are good first issues.** Only `#230 Uptime: /api/events is down`
  was open at the last read, and an uptime alert is not an outside contributor's task.
