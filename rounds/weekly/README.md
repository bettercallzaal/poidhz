# Weekly - "this is for the ZAO" recurring video competition

Spec: ZAOOS `research/community/2308-poidh-weekly-zao-video-competition-spec/`
(merged PR #3151). This folder holds the weekly machinery; each week gets
`rounds/weekly/wNN/` copied from `_template/`.

This format is deliberately DIFFERENT from `rounds/_template/` (the one-off open
campaign bounty). Weekly is:

- **Solo bounty, not open.** Zaal escrows, Zaal accepts, no contributor vote.
  Open bounties above 50% outside funding trigger contributor-weighted voting,
  which would hand winner selection to dust-voters and break the skill-judged
  raffle-safe requirement.
- **One fresh bounty per week.** poidh pays exactly one accepted claim per
  bounty, so a rolling bounty cannot pay weekly winners.
- **The poidh claim IS the entry. One surface, not two.** R4 ran post-then-claim
  as two steps: 16 builders did the work, 2 claims arrived, both one wallet
  (`rounds/r4/CLOSEOUT.md`). The claim carries the public post URL; the
  screenshot is the claim image. Not claimed = not entered.
- **Raffle-safe.** Full numeric rubric published in the bounty description
  before entries open. Ties break on the Substance sub-score, then earliest
  claim timestamp. Never a draw.

## Prerequisites before week 1 casts (all Zaal, all open as of 2026-08-20)

| # | Decision | State |
|---|---|---|
| 1 | Prize option A 0.01 / B 0.03 (recommended) / C 0.1 ETH weekly | OPEN |
| 2 | Album: `org.config.json` currently sets `farcaster_album: "wethemmedia"` - every weekly bounty would build We Them Media's album on-chain | OPEN |
| 3 | "Feeds ZOLs" = contribution credits (manual award by Zaal) or @zolbot echo | OPEN |
| 4 | BCZ bounty or The ZAO bounty (issuer wallet, voice, channels) | OPEN - default BCZ like R1-R7 |
| 5 | Run week-1 description past Kenny (outbound, Zaal sends) | OPEN |
| 6 | Fix Empire Builder POIDH Submitters `api_endpoint` to the live zpoidh feed (`scripts/check-eb-sync.py` must print IN SYNC) before promising $ZABAL participation | OPEN |

## The weekly loop (doc 2308 section 7)

| Day | Action | Tooling |
|---|---|---|
| Mon | Copy `_template/` to `wNN/`, fill placeholders, cast bounty, escrow prize | `docs/create-bounty.html` auto-versions the round number |
| Mon | Cross-post the cast to /zao and /poidh, Firefly to X | `promo-cast.md` |
| Thu | Mid-window reply-cast: entry count, days left, duration meter | `mid-window-cast.md` |
| Sun 11:59pm PT | Window closes (absolute date in description, never "7 days") | - |
| Mon | Pull claims, ffprobe durations, build judging page, score, accept winner on-chain | `scripts/run-judging-round.py` and siblings |
| Mon | Winner cast WITH next week's bounty in the same cast | `winner-cast.md` - the compounding move |

## Files in `_template/`

- `description.md` - paste-ready poidh Description field (rubric embedded, per
  the raffle-safe rule: criteria disclosed before entry)
- `promo-cast.md` - Monday launch cast
- `mid-window-cast.md` - Thursday reply-cast
- `winner-cast.md` - winner announcement + next week's bounty, one cast

NFT naming: `ZAO Weekly #NNN`, numbering continuous across weeks so the
collection compounds.
