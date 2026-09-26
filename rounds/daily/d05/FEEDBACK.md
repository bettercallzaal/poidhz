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
