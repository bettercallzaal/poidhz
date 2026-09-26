<!-- NOT-ANNOUNCEMENT-COPY: drafted replies to round five entrants, unsent. Names no deadline anyone submits to. -->
# Round five - replies to entrants, DRAFT, UNSENT

**Zaal posts these.** Round five's immutable text promises answers *while the round is still
running*, so these are written now rather than held to the close - that is the promise, and it
is four hours old.

**Shape, per `docs/feedback-that-recruits.md`:** name the capability rather than the artifact,
ask a real question, and close with what is needed next rather than with a rule. Every
technical claim below was verified by running it on a clean clone.

**Say the CI thing first, in both.** Every entrant currently sees a red mark on their pull
request and it is not theirs - it is the first-time-contributor gate plus a Vercel preview.
Leaving that unexplained tells a careful person they failed a bar they cannot reach.

---

## To @pn-research - PRs #316 and #318

```
Both of these are in, and they are the two I would have picked myself.

First, the red mark on your PRs is ours, not yours. GitHub holds workflow runs from first-time contributors until a maintainer approves them, so your CI has not run yet - it says action_required, not failed. The Vercel line is a preview deploy that forks cannot authenticate. I ran the real thing locally on a clean clone with no env file: typecheck, lint, test and build all pass on both branches, and your four new tests pass in each.

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

First, the red mark on your PR is ours, not yours. GitHub holds workflow runs from first-time contributors until a maintainer approves them - your CI says action_required, it did not fail. The Vercel line is a preview deploy that a fork cannot authenticate. I ran the checks by hand on a clean clone: typecheck, lint, test and build all pass, and I confirmed the specific thing you claimed. Main lints at 8 warnings, your branch at 7, and the one that disappears is the SITE warning. You said what was wrong, how you knew, and what you ran, and every part of it held up when I checked it. That is rarer than it should be.

What it is: the smallest correct change, cleanly argued. What it is not, yet, is something a visitor would notice - and this round's first criterion is whether somebody landing on a phone has a better time. A lint fix is real work and it sits low on that particular ladder, which is about the ladder rather than about you.

So the useful next step is one rung up. Two of the eight lint warnings are not cosmetic: LocalStartTime.tsx:24 calls setState synchronously inside an effect, which can cascade renders, and that component's whole job is to render a time correctly. Fixing that one changes behaviour rather than tidying imports. There is also an unused eslint-disable at opengraph-image.tsx:88 which is a two-line clean-up if you want another quick one.

The question: you ran the full suite before pushing, which tells me you can verify your own work end to end. Can you find something wrong that lint does NOT report? That is the thing I am really paying for, and it is what separates an agent that tidies from one I would hand a real task to.

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
