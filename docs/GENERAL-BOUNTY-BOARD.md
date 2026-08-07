# POIDH as The ZAO's general bounty board

Everything documented in this repo so far - [P2P-AD-BOUNTY-KIT.md](P2P-AD-BOUNTY-KIT.md),
`docs/how-to-draft-next-bounty.md` - covers one bounty type: ads/clips, judged on a
Distribution/Craft/Substance rubric. That's proven and it's real. But POIDH's actual
protocol doesn't care what the task is - it's a generic "post a bounty, submit proof,
get paid" primitive. This doc covers the other half: using POIDH as a general-purpose
task board for whatever The ZAO needs done, not just promotional content.

## The one real precedent that already exists: R7

[rounds/r7/](../rounds/r7/) is BCZ's first non-ad bounty: a code bounty for fixing real
bugs on zabalgamez.com. Submissions are pull requests, not clips. This is the pattern to
generalize from, not a hypothetical - it's live, its description is already written
(`rounds/r7/description.md`), and it already established the key structural differences
from an ad bounty:

- **No BAR/RUBRIC ad-specific requirements** (no "tag @account", no "cross-post to
  another platform", no distribution scoring) - because the value here isn't
  distribution, it's the work product itself.
- **A different rubric shape**: R7 scores on `impact` (does it fix something that
  actually blocks a user) and `craft` (clean minimal diff, doesn't break anything else),
  not Distribution/Craft/Substance/Bonus.
- **Not winner-take-all by default**: R7's description states explicitly - "this is not
  winner-take-all - multiple strong fixes can each get paid, because the whole point is
  making zabal gamez better." A task bounty can pay every submission that clears the bar,
  since the goal is the work getting done, not picking one best entry.
- **Proof requirement matches the task type**: R7 asks for "a short screen recording or
  before/after screenshots showing the bug and the fix working" - proof-of-completion
  needs to be tailored to what verification actually looks like for that task, the same
  way an ad bounty's proof is a public post URL.
- **A longer window**: R7 runs cast-date + 14 days instead of the usual 7, because
  `rounds/r7/README.md` notes explicitly - "code takes longer than clips."
- **Named as a trust-ladder step**: R7's README frames this bounty as "the trust-ladder
  first step for ZOL toward money actions - a controlled, human-funded bounty ZOL can
  help scope + judge without ever holding funds." Worth remembering if ZAO OS V1's
  agent tooling (ZOL/ZOE) becomes more involved in bounty scoping over time - R7 already
  establishes the pattern of an agent assisting a human-gated bounty rather than the
  agent controlling funds directly.

## What task types fit POIDH's model well

POIDH's actual constraint isn't the task category - it's how it verifies completion:
whoever created the bounty (or, for OPEN bounties, contributor vote) decides whether a
submitted claim satisfies the bounty, based on a public claim submission. That mechanism
favors:

- **Verifiable by looking at the output** - a PR, a published post, a document, a design
  file, a recording. If a stranger can look at the claim and roughly judge whether it did
  the thing, it fits. R7 (bug fix -> PR + before/after proof) is the clearest example.
- **One-off, bounded scope** - "fix this bug," "make this asset," "write this doc,"
  "research this question" all have a clear finish line. POIDH has no concept of a
  recurring role or partial credit for ongoing work.
- **Fine to be public** - the bounty description, the claim, and (for OPEN bounties) the
  contributor vote are all on-chain and public. Anything sensitive can't go through POIDH
  in the clear.
- **Fine to pay per-submission, not per-hour** - POIDH pays for a result, not time spent.
  A task that's naturally "done or not done" (fix the bug, ship the doc) fits; a task
  that's naturally hourly (ongoing moderation, a support rotation) doesn't map cleanly.

Realistic ZAO task-bounty candidates beyond R7's bug-fix format, following the same
pattern:

- **Research bounties** - "answer this open question, cite your sources" (the same shape
  as this repo's own `zao-research` skill, just crowdsourced instead of agent-run)
- **Documentation bounties** - "write the missing docs for X" with a clear list of what
  "done" looks like
- **Design/asset bounties** - a specific graphic, a specific template, judged the same
  impact/craft way R7 judges code
- **Event-support bounties** - a specific deliverable tied to an event (a recap, a
  highlight reel, a resource page), one-off and bounded like R7, not an ongoing role

## What fits poorly

- **Private or sensitive work** - anything involving access to non-public systems,
  member PII, or content that can't be posted publicly as proof
- **Ongoing roles, not tasks** - a recurring moderator, a standing "check in on X weekly"
  responsibility. POIDH pays once per accepted claim; it has no subscription/salary
  primitive
- **Work that's hard to verify from the outside** - "improve morale," "build
  relationships," anything where the deliverable isn't a concrete artifact a judge can
  actually inspect
- **Anything requiring real-time coordination** rather than an asynchronous
  submit-and-judge flow - POIDH bounties are fundamentally async

## The tooling already supports this - it's just not framed this way yet

`scripts/build-bounty-dashboard.py` and `docs/bounty-dashboard.html` already scan the
**entire live POID platform feed** (`bounties.fetchAll`, unfiltered by issuer or bounty
id), not just BCZ's own bounties - confirmed by running the script directly: a real run
scanned 91 live bounties platform-wide, unrelated to BCZ's own 4 rounds. That means a
general "what's open on POIDH right now" bounty-board view already exists in this repo;
it's just been described as a POID *deadline scanner*, not framed as a ZAO-facing
"here's what's open to work on" board.

If The ZAO wants to run task bounties through POIDH regularly (bug fixes, research,
docs, design), the dashboard is the natural place to also surface The ZAO's *own* task
bounties specifically - the same way `org.config.json`'s `default_bounty_ids` already
lets any org's known bounty ids get pulled into the calendar/leaderboard tooling (see
[PARTNER-GUIDE.md](PARTNER-GUIDE.md)). No new tooling is required to start; R7 is the
proof this already works end to end with the existing scripts.

## Practical next step

The fastest way to validate this beyond R7 is running a second, different task-bounty
type (research or docs, since code is already proven) using the same structural pattern
R7 established: no ad-style BAR/RUBRIC, an impact/craft-style rubric suited to the task,
proof tailored to what verification actually needs, and non-winner-take-all payout if
multiple submissions genuinely clear the bar. This doc doesn't propose drafting that
bounty yet - that's a real decision for Zaal, not something to pre-write speculatively.

## Also see

- [rounds/r7/](../rounds/r7/) - the one real non-ad bounty this doc generalizes from
- [P2P-AD-BOUNTY-KIT.md](P2P-AD-BOUNTY-KIT.md) - the ad/promo bounty pattern (the other half of "ad system + bounty board")
- [PARTNER-GUIDE.md](PARTNER-GUIDE.md) - org.config.json and the tooling this doc references
- `docs/bounty-dashboard.html` / `scripts/build-bounty-dashboard.py` - the already-platform-wide bounty scanner referenced above
