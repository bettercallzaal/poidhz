<!-- NOT-ANNOUNCEMENT-COPY: drafted replies to round five entrants, unsent. Names no deadline anyone submits to. -->
# Round five - replies to entrants, DRAFT, UNSENT

**Zaal posts these.** Round five's immutable text promises answers *while the round is still
running*, so these are written now rather than held to the close - that is the promise, and it
is four hours old.

**Shape, per `docs/feedback-that-recruits.md`:** name the capability rather than the artifact,
ask a real question, and close with what is needed next rather than with a rule. Every
technical claim below was verified by running it on a clean clone.

**THE CI PARAGRAPH WAS REWRITTEN AT 00:59 AND THE FIRST VERSION IS NOW FALSE.** When these
were drafted, all three runs sat at `action_required` and both replies said "your CI has not
run yet". The ZAOstock lane read each diff by hand and approved all three at about 00:5x, and
**every job now passes: typecheck/tests/build, lint, fact-dedup and the review gate**, verified
here rather than taken from their message. Only the Vercel preview still fails, which a fork
cannot authenticate.

Posting the earlier wording would have told two entrants their checks had not run while a green
tick sat on their pull request. A drafted claim decays; this one decayed in under an hour.

---

## To @pn-research - PRs #316 and #318

```
Both of these are in, and they are the two I would have picked myself.

On the checks: both of yours are green now. There was a delay because GitHub holds workflow runs from first-time contributors until a maintainer approves them - that is the first-time gate, not anything you did, and somebody read your diffs and approved them. typecheck, tests, build, lint, fact-dedup and the security review gate all pass on both PRs. The one red line left is Vercel, which is a preview deploy a fork cannot authenticate; ignore it, it is not yours to fix. I had also run the four commands locally on a clean clone before the gate lifted, and your four new tests pass in each branch.

What you did that most people do not: you made the policy a pure function in its own file and unit-tested it, instead of burying an if-statement in a component. This repo has no jsdom, and rather than adding one you moved the decision somewhere it could be tested without a DOM. That is the instinct I want on this codebase.

Three specifics I checked and liked. navigator.connection is read through optional chaining, so Safari - which does not implement it - is not broken by it. IntersectionObserver being undefined loads the video immediately rather than leaving a permanently blank section, which is the failure mode a lazy-load usually ships with. And in #318 the default when there is no Network Information API is to keep existing behaviour, so an unknown connection is never quietly degraded. All three are the same habit: the guard fails toward the visitor.

One thing to check before this merges, and it is a question rather than a fault. The comment you replaced said reduced motion was already handled in home.module.css. You now also check prefers-reduced-motion in JavaScript. Two guards for one rule is safe, but I would rather know whether the CSS branch is still doing its part or has quietly become dead code. Have a look at it while you are in there.

Now the question I actually want answered: you found the 1.8 MB video and the 4.5 MB frame preload in about an hour. What else did you see in there that you did not open a PR for, and what stopped you - scope, or not knowing whether we wanted it?

The festival is October 3 and this round runs to the 5th, so there is time. If you want a harder one: the repo runs a review gate in CI that was reporting PASS after reading zero files until somebody actually read it. Checks that cannot fail are worth more to me than features.
```

---

## To @testies1234321-afk - PR #317

```
This is in, and thank you for declaring the agent in the description without being asked. One agent has entered every round of this programme and declared itself every time, including the one rule it could not meet, and it has never cost them anything.

On the checks: yours is green now. There was a delay because GitHub holds workflow runs from first-time contributors until a maintainer approves them - the first-time gate, not anything you did. typecheck, tests, build, lint, fact-dedup and the security review gate all pass. The one red line left is Vercel, a preview deploy a fork cannot authenticate; ignore it. I had also checked the specific thing you claimed, by hand and by control: main lints at 8 warnings, your branch at 7, and the one that disappears is the SITE warning. You said what was wrong, how you knew, and what you ran, and every part of it held up. That is rarer than it should be.

What it is: the smallest correct change, cleanly argued. What it is not, yet, is something a visitor would notice - and this round's first criterion is whether somebody landing on a phone has a better time. A lint fix is real work and it sits low on that particular ladder, which is about the ladder rather than about you.

So the useful next step is one rung up. Two of the eight lint warnings are not cosmetic: LocalStartTime.tsx:24 calls setState synchronously inside an effect, which can cascade renders, and that component's whole job is to render a time correctly. Fixing that one changes behaviour rather than tidying imports. There is also an unused eslint-disable at opengraph-image.tsx:88 which is a two-line clean-up if you want another quick one.

The question: you ran the full suite before pushing, which tells me you can verify your own work end to end. Can you find something wrong that lint does NOT report? That is the thing I am really paying for, and it is what separates an agent that tidies from one I would hand a real task to.

One practical thing about your claim, and it costs you nothing to fix. The media field on claim 8306 has your explanation in it rather than an image URL, so your claim shows on the bounty page with no picture. poidh needs a link to an actual image there. If you want the card the round uses, fetch it and rehost it - no browser needed:

https://poidhz.com/api/receipt?round=5&pr=https://github.com/ZAODEVZ/ZAOstock/pull/317&who=YOUR_HANDLE&agent=1

That returns an SVG; convert it to PNG, put it anywhere public, and use that URL. The other entrant in this round did exactly that within the hour. Your entry counts either way - the PR link in your description is what I read - this is only so your work has a face on the page.

You may open as many PRs as you like this round and each one is a separate entry.
```

---

## What neither reply does

- **Neither ranks them against each other.** Two entrants, three PRs, and no sentence says
  whose is better. The pick is announced once, at the close.
- **Neither promises a merge or a review date.** The round promises the pot and answers during
  the round. Nothing else.
- **Neither ends on a rule.** Both end on a question or an invitation, because a note that
  needs no answer will not get one - the defect that made round one's first six drafts
  unusable.

---

## To @i001962 - PR #319

```
This is the first entry that went at the top of the list rather than the easy end of it, and I noticed.

The round's first criterion is whether somebody landing on a phone has a better time, and you built for a specific person: someone on Franklin Street at midday in October trying to find out when a band plays. You also went and found our own line in DESIGN.md about staying legible at 14px on a phone in sunlight and built to it, rather than guessing at what I meant. That is reading the brief instead of reading the title.

Checks: typecheck, tests, build, lint, fact-dedup and the review gate all pass. The Vercel red is a preview deploy your fork cannot authenticate - ignore it, it is not yours to fix. If your run looks stuck before that, it is the first-time-contributor gate and someone has to approve it; that is on us, not you.

One thing to fix, and it is the one place this entry argues with the round it is entered in. Lint goes from 8 warnings to 10 with your branch. Both new ones are in ProgramControls.tsx: 'mounted' is assigned and never used at line 10, and line 13 calls setState synchronously inside an effect, which can trigger cascading renders. That second one is the same defect as LocalStartTime.tsx:24, which is the one existing warning in this repo with real runtime behaviour behind it - and the bounty text complains that lint exits zero so nothing stops one more landing. Yours lands two. Both are small, and you have until the 5th.

The question I want answered: you fixed contrast by moving colours. Did you check the result against a measurement, or by eye? Someone else in this round is running axe over the home page and counting failures before and after. If you have a number for /program, put it in the PR - a contrast ratio is the kind of claim that settles itself.

If you want more of this: accessibility across the rest of the site is wide open, and almost nobody does it. Focus states, keyboard order, heading structure. It is the sort of work that stays done.
```

---

## To @assay - claim 8310

**URGENT, and the reason this file exists.** The round promises answers while it runs. This
entrant cannot be judged until the link works, and they may not know.

```
Your claim is in and I cannot read the work, because the link in it does not resolve.

github.com/ZAODEVZ/ZAOstock/pull/320 returns 404. There is no #320 on the repo in any state - #319 is the highest that exists, and I see no pull requests from you there at all. My guess is the push or the PR creation failed after you filed the claim. Nothing about the claim looks careless, which is why I am telling you rather than marking it down.

Get the PR open and reply here with the link. The round closes 5pm Eastern Monday October 5 and nothing about this counts against you; claim again if it is easier, since a later claim does not replace an earlier one in this round.

What I can see from your description is the most thorough entry of the five: axe at 390px, 8 failures to 0 in light and 11 to 0 in dark, a test that reads home.module.css and checks all 14 text/fill pairs in both schemes, failing 16 of 28 on main. You also named the case axe cannot see - near-white on light orange over a gradient - which is the sort of thing that only turns up when somebody actually looks rather than runs the tool and reports the exit code. If the code matches the description, this is strong.

Your question: "Rain or shine" moved from brass to sun so it can pass. I will come back to you on the palette rather than guess at Candy's intent in a bounty reply, because it is her mark and the answer should be hers or mine deliberately, not mine in passing.

And you are the first person to use the feedback box on the submission page. That is exactly what it is for - asking a question you cannot answer alone, before you finish the work rather than after.
```
