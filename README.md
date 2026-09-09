# poidhz - a public client for poidh bounties

**Live: [poidhz.com](https://poidhz.com)** - every open [poidh](https://poidh.xyz) bounty with a stated deadline, on a calendar, with countdowns, filters, and a subscribable `.ics`. Refreshes every 6 hours. poidh has an on-chain deadline field that almost nobody sets, so this reads the date out of each bounty's description instead; of the bounties scanned on 2026-09-07, exactly one had the native field populated.

poidhz started as BetterCallZaal / The ZAO's own bounty-ops repo (rounds, judging pages, the canonical bounty bar) and grew the tooling any issuer or hunter can use. Both halves live here. MIT, fork it.

## Start here

Nothing below needs permission, an account, or a fork. Pick the row that is you.

| You are | Start with | You do not need |
|---|---|---|
| **Hunting bounties** - looking for work worth doing | [poidhz.com](https://poidhz.com) for what closes when, and [/dashboard](https://poidhz.com/dashboard) for prize size and whether anyone has claimed yet | anything in this repo |
| **Issuing a bounty** and want people to actually enter | [/best-practices](https://poidhz.com/best-practices), then [docs/how-to-draft-next-bounty.md](docs/how-to-draft-next-bounty.md). [`docs/PROMISE-AUDIT.md`](docs/PROMISE-AUDIT.md) is the honest version - five of our own rounds, and what we promised and failed to deliver | to run our rounds or use our brand |
| **Building something on poidh** | [The open data](#the-open-data-cors-open-no-key) below. Every file the site renders is a public endpoint | to scrape the site |
| **Running your own bounty programme** | [docs/PARTNER-GUIDE.md](docs/PARTNER-GUIDE.md) - point `org.config.json` at your wallet and every script here runs for your org | to change any code |

**The rounds, playbook and brand kits further down are BetterCallZaal's own use of this
tooling.** They are here as a worked example, not as the product. Skip them unless a real
example of a bounty that actually paid out is useful to you.

## The open data (CORS-open, no key)

poidh has no public deadline index and no submitter leaderboard. These are those, rebuilt
from poidh's own API every 6 hours and served with `Access-Control-Allow-Origin: *` so you
can fetch them straight from a browser. Verified live 2026-09-07.

| Endpoint | What is in it |
|---|---|
| [`/data/bounty-dashboard.json`](https://poidhz.com/data/bounty-dashboard.json) | Every open bounty platform-wide: prize in native token and USD, parsed deadline, claim status, chain, and a guessed task type. This is what both pages render. |
| [`/data/poidh-deadlines.ics`](https://poidhz.com/data/poidh-deadlines.ics) | The same deadlines as a calendar feed. Subscribe in any calendar app. |
| [`/leaderboard`](https://poidhz.com/leaderboard) | Submitters by count of bounties entered, in Empire Builder's `[{address, score}]` shape. |
| [`/data/poidh-deadlines-global.json`](https://poidhz.com/data/poidh-deadlines-global.json) | The raw deadline scan, with the free text each date was parsed out of so you can check the parse. |
| [`/data/health.json`](https://poidhz.com/data/health.json) | What this programme currently owes: promises made in bounty text and not yet delivered, time-bound claims that have gone unverified, and drafts held back because a round is not closed out. Written by the 6h cron. |

**The one thing worth knowing before you build on it:** poidh has an on-chain `deadline`
field and almost nobody sets it. Of the 90 open bounties on 2026-09-07, **77 stated no
machine-readable deadline at all** and only one had the native field populated. Every date
in these files was parsed out of free text in the description, and
`deadline_raw_text` carries the exact string it came from so you can judge the parse
yourself rather than trusting it.

Bounties also outlive their own deadlines - a passed date does not close a poidh bounty, so
`deadline_status` is `past` or `upcoming` and is **not** the same question as whether the
bounty is still open. `status` in the dashboard answers that one.

> **Domain note.** `poidhz.com` is the production domain as of 2026-09-06.
> `zpoidh.vercel.app` still resolves and 307s to it, so older links keep working.
> `www.poidhz.com` does not resolve yet - use the apex.

## Surfaces

| URL | What |
|---|---|
| [/](https://poidhz.com/) | Deadline calendar + agenda + every open bounty without a date |
| [/dashboard](https://poidhz.com/dashboard) | Platform-wide live dashboard: timers, claim status, ease / difficulty / money per bounty |
| [/data/poidh-deadlines.ics](https://poidhz.com/data/poidh-deadlines.ics) | Subscribe in any calendar app |
| [/data/bounty-dashboard.json](https://poidhz.com/data/bounty-dashboard.json) | The data behind both pages, CORS open |
| [/best-practices](https://poidhz.com/best-practices) | The canonical bounty bar: how to write a bounty people can actually win |
| [/about](https://poidhz.com/about) | Our own rounds, winners, brand kits |
| [/leaderboard](https://poidhz.com/leaderboard) | Submitter leaderboard feed (Empire Builder format) |

## Our rounds (cast order)

*BetterCallZaal's own five rounds. Kept public because a bounty that actually paid out is
more useful than a template - including [R4](rounds/r4/CLOSEOUT.md), which we broke, and
[the audit](docs/PROMISE-AUDIT.md) of what every round promised and did not deliver.*


| Round | Bounty | Ask | Prize | Result |
|---|---|---|---|---|
| R1 | [1151](https://poidh.xyz/base/bounty/1151) | BCZ YapZ Ep 17 clip-up | 0.0105 ETH | paid, @cryptfi-mariano |
| R2 | [1166](https://poidh.xyz/base/bounty/1166) | Best 60s POIDH ad from Ep 19 | 0.0105 ETH | paid, @joeyofdeus |
| R3 | [1180](https://poidh.xyz/base/bounty/1180) | ZABAL Gamez ad, any format | 0.025 ETH | paid, @femmie (8 claims) |
| R4 | [1249](https://poidh.xyz/base/bounty/1249) | ZABAL Gamez July open pot | canceled at closeout | 15 builders credited in $ZABAL, see [CLOSEOUT.md](rounds/r4/CLOSEOUT.md) |
| R5 | [1330](https://poidh.xyz/base/bounty/1330) | Best 60s clip from the WaveWarZ Twitch stream | 0.0125 ETH seed, 0.0238 final | paid, claim 7795 (9 claims). Winner announcement still owed |
| R6 | not cast | Recap my NYC trip in 60 seconds - one pot plus seven paid channel slots | 0.0125 ETH (open pot) + up to $35 $ZABAL | DRAFT, closes Wed Sep 30. See [rounds/r6/](rounds/r6/) |
| R7 | not cast | WaveWarZ clip round 2 - the edit, not the moment | 0.0125 ETH (open pot) | DRAFT, queued behind R6. See [rounds/r7/](rounds/r7/) |

Never-cast drafts (Unlock Protocol clip bounty, solo variant, ZABAL Gamez bug-fix bounty) live in [rounds/drafts/](rounds/drafts/).

## Run it yourself

```bash
python3 scripts/build-bounty-dashboard.py     # all open bounties + USD + type guess -> data/bounty-dashboard.json
python3 scripts/scan-poidh-deadlines.py       # free-text deadline parse -> data/poidh-deadlines-global.json
python3 scripts/build-bounty-calendar.py      # our rounds -> data/bounty-calendar.json
python3 scripts/deadlines-to-ics.py           # -> data/poidh-deadlines.ics
python3 scripts/query-bounty.py --bounty 1180 --chain 8453   # any bounty, any chain, resolves the winner
python3 scripts/precast-check.py --round 6 --prize 0.0128     # can this round cast? wallet, deadline, config, placeholders
python3 scripts/postclose-check.py --bounty 1330 --round 5    # did we do what the bounty text promised after it closed?
```

Every script takes `--selftest` and runs it offline, so you can check the logic without
hitting the network or having our data.

Python 3.9+ standard library only, no dependencies. `org.config.json` holds the issuer wallets and bounty ids; point it at your own to run this for a different org.

## What this repo holds

```
poidhz/
├── README.md
├── index.html                       # the deadline calendar (front page)                        # this file
├── docs/
│   ├── bounty-best-practices.html   # canonical bar (use for every bounty)
│   ├── bounty-calendar.html         # rendered deadline calendar
│   ├── create-bounty.html           # standalone bounty-creation tool - any EIP-6963
│   │                                 # browser wallet, no Farcaster app required (used for R6)
│   ├── poidh-hub.html               # the live hub UI source
│   ├── how-to-draft-next-bounty.md
│   ├── erc20-bounty-fork.md         # notes on an ERC20-reward PoidhV2 fork explored, not shipped
│   ├── qr-bid-reward-design.md      # design-only, gated on-chain spend
│   ├── unlock-fireside-collectible.md
│   └── RECAP.md                     # resume artifact + history log
├── rounds/
│   ├── _template/                   # starter files for the NEXT round
│   ├── r1/                          # Hannah Ep 17 clip-up (bounty 1151, Apr 2026) - closed, paid
│   ├── r2/                          # Best 60s POIDH ad from Ep 19 (bounty 1166, May 2026) - closed, paid
│   ├── r3/                          # Best ad for ZABAL Gamez (bounty 1180) - closed, paid, cast drafted
│   ├── r4/                          # ZABAL Gamez open pot (bounty 1249) - closed, see CLOSEOUT.md
│   ├── r5/                          # WaveWarZ Twitch clip bounty (bounty 1330) - closed, paid,
│   │                                 # winner announcement still owed (see r5/winner-announce.md)
│   ├── r6/                          # NYC trip recap, 60s - DRAFT. Blocked on the Drive link,
│   │                                 # the trip write-up, and funding the issuer wallet
│   ├── r7/                          # WaveWarZ clip round 2 - DRAFT, queued behind R6
│   └── drafts/                      # never-cast drafts: unlock-cofund, unlock-solo, zabal-bugfix
├── assets/
│   └── brand-kits/
│       └── zabal-games/             # full CC-BY kit (used by R3+)
├── api/
│   └── claim-meta.mjs               # claim metadata endpoint
├── pipeline/                        # Fable eval-runner - AI-assisted submission scoring
│   ├── eval-runner.mjs              # per-submission scoring (distribution/craft/substance/spec), Claude-called
│   ├── run-eval.md                  # manual-first runbook
│   └── *-template.md                # rubric / scorecard / cohort-synthesis templates
├── data/
│   ├── leaderboard.json             # the EB-pulled feed (`[{address, score}]`)
│   ├── claims.json                  # rich page data
│   ├── audit.json                   # audit trail
│   ├── bounty-calendar.json         # parsed deadlines, output of build-bounty-calendar.py
│   ├── poidh-deadlines-global.json  # platform-wide deadline scan (not just BCZ's own bounties)
│   └── zabal-preview.json           # EB snapshot per submitter
└── scripts/
    ├── refresh-poidh-leaderboard.py # canonical leaderboard refresh (tRPC + web3.bio)
    ├── scan-poidh-deadlines.py      # parses deadlines from bounty description free text
    ├── build-bounty-calendar.py     # turns scanned deadlines into a calendar view
    ├── deadlines-to-ics.py          # subscribable .ics calendar export
    ├── build-bounty-dashboard.py    # platform-wide live dashboard: timers, submission status,
    │                                 # estimated ease/difficulty/money per bounty (docs/bounty-dashboard.html)
    ├── process-judging-videos.py    # Stage 1: download + duration-check + scaffold judging.json
    ├── render-judging-html.py       # Stage 2: judging.json -> shareable HTML scorecard
    ├── precast-check.py             # is this round castable? wallet balance, deadline window,
    │                                 # config wiring, placeholders, validator, data freshness
    ├── validate-bounty-description.py # Stage 3: check a draft description against the canonical bar
    ├── prepare-winner-announcement.py # Stage 4: scaffold the winner-announce cast templates
    └── run-judging-round.py         # Stage 5: orchestrates stages 1-4, pauses at two human gates
```

## Round automation pipeline (stages 1-5)

Chains together everything from "submissions closed" to "winner cast drafted," with two
hard human gates that are never automated: **rubric scoring / winner selection**, and
**posting the actual announcement + any on-chain call**. Run the whole thing with:

```bash
python3 scripts/run-judging-round.py --bounty <id> --round <N> [--skip-stage 1] [--skip-stage 3]
```

Or run each stage standalone:
- `process-judging-videos.py --bounty <id> --round <N>` - downloads submitted videos, checks duration against spec, scaffolds `judging.json`
- `render-judging-html.py --round <N>` - turns `judging.json` into a shareable HTML scorecard
- `validate-bounty-description.py --description <path>` - checks a draft bounty description against the canonical bar before casting
- `prepare-winner-announcement.py --round <N>` - scaffolds the winner-announce cast templates (Farcaster/X/short) into `rounds/rN/cast-templates/`, leaving the "why it won" reasoning for a human to fill

All idempotent, safe to re-run. No script in this pipeline posts anything, signs anything, or touches chain state.

---

## How to draft + cast the next round (the playbook)

### 1. Pick the subject + the win
- What is the bounty FOR? (an ad, a clip, a recap, a proof-of-attendance, etc.)
- What is the prize? Default = 0.0125 ETH on Base (covers ~$25 worth + 2.5% protocol fee).
- What gets the WINNER beyond ETH? (pinned promo, feature in newsletter, etc.)
- What gets EVERY submitter? Slot 8 of $ZABAL Empire (`0xbB48f19B0494Ff7C1fE5Dc2032aeEE14312f0b07`) - score = count of BCZ POIDH bounties they have entered.

### 2. Decide bounty type
- **OPEN** = others can stack contributions on top + contributor-weighted vote at the end. Use this when you want catalytic momentum (Jesse Pollak / Haberdashery whale pattern). R1-R3 were all OPEN.
- **SOLO** = you fund + you accept directly, no vote. Use when judging is yours alone and you want fast resolution. Trade-off: no whale-stacking mechanic.
- **OPEN-SPLIT** = open contributions all window, then the whole pot splits equally across *every* submitter who clears the floor (no single winner). Use for participation rewards - "everyone who showed up gets a slice." POIDH pays one winner natively, so the split needs a chosen payout path (split contract / distributor / proof-gallery-only). First used in R4 - see [rounds/r4/MECHANIC.md](rounds/r4/MECHANIC.md).

### 3. Write the description
Use [docs/bounty-best-practices.html](docs/bounty-best-practices.html) as the canonical bar. Required sections in order:
1. One-paragraph WHY (link to source episode / event / page)
2. **THE BAR** - 3-5 numbered floor rules ("do these or you are not in the running")
3. **THE RUBRIC** - grouped by Distribution / Craft / Substance / Bonus with `+` checkboxes
4. **THE ASSET KIT** - link to GitHub brand folder + direct download URLs for editors
5. **THE REWARD** - prize + winner-cast distribution + EB ZABAL trail for all submitters
6. **DEADLINE** - exact PT date/time + winner cast date

Floor rules MUST include:
- Tag `@bettercallzaal` on X
- Cross-post in the relevant Farcaster channel (`/zabal`, `/zao`, etc.)
- Submit X URL on POIDH bounty page
- AUDIO rule: official promo MP3 from brand kit OR source-episode audio OR one clear instrumental that does not compete with dialog. Layered melodic music over spoken dialog = floor fail.

Use the existing rounds as reference:
- [rounds/r3/description.md](rounds/r3/description.md) (newest, ZABAL Gamez ad)
- [rounds/r2/judging.json](rounds/r2/judging.json) → has full R2 description + rubric

### 4. Cast it
- POIDH UI → Create → OPEN, Base, title, paste description
- Reward seed: 0.0125 ETH (or your chosen amount + 2.5% buffer)
- Wallet: BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af` (must be EOA, not Smart Wallet - POIDH reverts on contract callers)
- Album: `wethemmedia` (continuity with R1+R2+R3)
- Cast on `/zabal` (or relevant channel) + `/poidh` + `/zao` with the bounty URL as embed
- Pin in the home channel for the bounty window
- Firefly cross-post to X
- **For CODE bounties especially**: same-day cross-post to Bountycaster (bountycaster.xyz, indexed by @bountybot via the `/bounties` channel) - reaches 200-400 Farcaster-native builders who won't see poidh.xyz or a GitHub issue on their own. POIDH handles escrow, Bountycaster handles discovery. See [rounds/drafts/zabal-bugfix/bountycaster-cast.md](rounds/drafts/zabal-bugfix/bountycaster-cast.md) for the format (ZAOOS doc 1584 has the full mechanics). This was flagged for R7 back in July and never actually posted because R7 itself was never cast - don't repeat that gap.

### 5. Set reminders
- Day 5 of window: reply-cast with "N submissions so far, deadline in X days, gallery: poidhz.com/hub"
- Close date + 1: lock judging
- Close date + 2: cast winner

### 6. Judge
- Use [rounds/_template/judging.json.template](rounds/_template/judging.json.template) as the starter
- Run `ffprobe` on every video to confirm duration vs spec
- Floor-fail per spec; do not inflate to clear the bounty
- Ship per-submission scorecard at `/poidh-round{N}-judging.html` within 48h
- Use the canonical scorecard structure from [rounds/r2/judging.html](rounds/r2/judging.html)

### 7. Post-bounty
- For OPEN bounty: call `submitClaimForVote(bountyId, claimId)` → 48h contributor vote → `resolveVote(bountyId)` → winner withdraws
- Run [scripts/refresh-poidh-leaderboard.py](scripts/refresh-poidh-leaderboard.py) to update the EB feed
- Add winner clip to the hub gallery
- Push final state to GitHub before drafting the next round

---

## The hard audio rule (locked 2026-05-28, evolved from R2 post-mortem)

> No random background music or ambient audio under dialog in any BCZ POIDH bounty submission. If you want non-silence, use the official campaign promo MP3 (e.g. `assets/brand-kits/zabal-games/zabal-gamez-promo.mp3`), original source-episode audio, or one clear instrumental that does not compete with spoken dialog. Layered melodic music over spoken dialog = automatic floor fail.

Why: R2 had submissions where Kenny's voice was buried under cinematic ambient pads - the editor's craft was real but the message disappeared. POIDH ads are watched at 50% volume on Farcaster + X with subtitles on.

This rule lives in every round's description starting from R3.

---

## Score-by-count mechanic (locked 2026-05-27)

Every BCZ POIDH submitter lands on slot 8 of $ZABAL Empire (`POIDH Submitters` leaderboard). Each wallet's `score` = the count of BCZ POIDH bounties they have submitted to. Empire Builder distributes $ZABAL proportional to score every refresh cycle.

- Submitter who entered R1 only = score 1
- Submitter who entered R1 + R2 = score 2
- Submitter who entered R1 + R2 + R3 = score 3 (compounds linearly)

Token Boosters + Reputation Boosters intentionally OFF (cleanest mechanic, no Talent Protocol or token-holder confounders).

Update via `scripts/refresh-poidh-leaderboard.py` - reads POIDH tRPC, aggregates per-wallet counts, writes the strict EB feed at `data/leaderboard.json`, served at [poidhz.com/leaderboard](https://poidhz.com/leaderboard).

**The cut-over has not happened.** Empire Builder's "POIDH Submitters" leaderboard still has its `api_endpoint` pointed at `bettercallzaal.com/poidh-leaderboard.json`, a pre-poidhz URL that now redirects away. Measured 2026-08-08 and unchanged since: EB shows 16 entries where this repo generates 22, so 6 real submitters are missing from EB entirely - including **femmie, the R3 winner**, whose wallet is absent from EB's feed. Three more wallets have understated scores. No code change here can fix it; EB's own admin dashboard needs the `api_endpoint` corrected by someone with access. `scripts/check-eb-sync.py` exists to detect exactly this drift.

---

## Round index

| Round | Bounty | Episode / Source | Prize | Winner | State | Doc |
|---|---|---|---|---|---|---|
| R1 | [1151](https://poidh.xyz/base/bounty/1151) | BCZ YapZ Ep 17 (Hannah / Farm Drop clip-up) | 0.0105 ETH | @cryptfi-mariano (claim 6368) | closed, paid | [rounds/r1/](rounds/r1/) |
| R2 | [1166](https://poidh.xyz/base/bounty/1166) | BCZ YapZ Ep 19 (Best 60s POIDH ad w/ Kenny) | 0.0105 ETH | @joeyofdeus / Monksage (claim 6645) | closed, paid | [rounds/r2/](rounds/r2/) |
| R3 | [1180](https://poidh.xyz/base/bounty/1180) | ZABAL Gamez ad (any format) | 0.025 ETH | @femmie (claim 6749) | closed, paid, confirmed on-chain via direct `bounties()`/`getClaimsByBountyId()` eth_call - cast templates drafted, not yet posted | [rounds/r3/](rounds/r3/) |
| R4 | [1249](https://poidh.xyz/base/bounty/1249) | ZABAL Gamez July open build pot | $ZABAL leaderboard credit (originally an ETH split, bounty was accidentally canceled mid-close) | 15 qualifying builders | CLOSED 2026-08-05 - see [CLOSEOUT.md](rounds/r4/CLOSEOUT.md) | [rounds/r4/](rounds/r4/) |
| R5 | [1330](https://poidh.xyz/base/bounty/1330) | WaveWarZ Twitch clip bounty (twitch.tv/wavewarzofficial, clip for WaveWarZ's own socials) | 0.0125 ETH seed, pot grew to 0.0238 | claim 7795, [@wimpydwi's clip](https://x.com/wimpydwi/status/2094135544758608181), paid to `0x3f07d412...70ec9` (wallet resolves to no linked handle) | closed, paid, `isAccepted` confirmed on-chain 2026-09-05. 9 claims from 7 entrants. **Winner never announced on @wavewarz**, which the bounty text promised | [rounds/r5/](rounds/r5/) |
| R6 | not cast | Recap my NYC trip in 60 seconds. One 0.0125 ETH pot, plus seven channel slots paying $5 in $ZABAL each to clips we actually post | 0.0125 ETH seed, fund 0.0128, plus up to $35 $ZABAL | - | DRAFT. Closes Wed 2026-09-30. Blocked on the Drive link, the trip write-up, and funding | [rounds/r6/](rounds/r6/) |
| R7 | not cast | WaveWarZ clip round 2 - the edit, not the moment. Binding deliverable spec, handle required in claim, retainer holders excluded | 0.0125 ETH seed, fund 0.0128 | - | DRAFT, queued behind R6. Deadline placeholdered, re-measure the Twitch archive before casting | [rounds/r7/](rounds/r7/) |
| drafts | not cast | Unlock Protocol clip bounty (co-fund + solo variants), ZABAL Gamez bug-fix bounty | TBD | - | parked, see folder READMEs | [rounds/drafts/](rounds/drafts/) |

Leaderboard refresh last run 2026-08-05 - `data/leaderboard.json` / `claims.json` /
`audit.json` include R1-R4 (22 submitters via on-chain POIDH claims, plus R4's separate
15-wallet $ZABAL leaderboard credit tracked in `rounds/r4/r4-builder-leaderboard.csv`).

---

## Brand kits

Each campaign gets a CC-BY brand kit under `assets/brand-kits/<campaign>/`. The kit holds the canonical logo, palette, typography spec, voice rules, approved/banned phrases, glossary, and an official 50-second promo audio file editors can use freely.

Current campaigns:
- [`assets/brand-kits/zabal-games/`](assets/brand-kits/zabal-games/) - used by R3, which closed 2026-06-14, and by any future ZABAL Gamez bounties. Said "R3 (active)" until 2026-09-09, nearly three months after it closed.

Future campaigns get their own subfolder when launched.

Each kit mirrors a canonical source repo (e.g. `github.com/ZAODEVZ/zabalgames` for ZABAL Gamez). Sync target: weekly during the active campaign. If a kit and its canonical source disagree, the source wins.

---

## Where to go for more

These live in the ZAO OS V1 research library, which is internal. Paths are given in full
because **a doc number alone is not an address** - 218 numbers in that library resolve to
more than one document. Four of the nine below are among them: 759, 769, 992 and 743 each
name two different docs in two different topic folders. Resolve with
`zao-research-health --resolve <n>` if you ever have only a number; never rebuild a path
with `find | head -1`, which is how a lane read a POIDH bounty doc under an Empire Builder
title tonight.

| Path | What |
|---|---|
| `business/768-poidh-bounty-best-practices-zabalgames-r3` | canonical bounty best practices distillation |
| `business/769-zaodevz-zabalgames-repo-state` | the ZAODEVZ/zabalgames repo audit |
| `business/786-zabal-gamez-brand-kit-rebuild` | the ZABAL Gamez brand kit rebuild audit |
| `business/759-poidh-history-origin-to-2026` | POIDH history: Kenny, lifetime stats, cohort patterns |
| `business/631-poidh-zabal-sentinel-convergence` | POIDH x $ZABAL x Sentinel convergence map |
| `community/625-poidh-zao-bounty-playbook` | POIDH x ZAO bounty playbook, 18 templates |
| `agents/992-live-clipper-agent-creator-ops` | clipper to POIDH pipeline concept; R5 was the manual v1 test |
| `business/2202-poidh-zao-collab-current-state-brand-alignment` | current-state + brand-alignment synthesis, Aug 2026 |
| `business/2203-poidh-zao-full-lore-history` | full POIDH x ZAO lore, Kenny's 2023 founding onward |
| `business/2466-poidhz-platform-honest-audit` | this platform measured against the live poidh board, Sep 2026 |
- **[docs/unlock-fireside-collectible.md](docs/unlock-fireside-collectible.md)** - the Unlock Protocol proof-of-attendance NFT minted at the fireside R5 draws on
- **[docs/RECAP.md](docs/RECAP.md)** - resume artifact + ongoing state
- **[docs/PARTNER-GUIDE.md](docs/PARTNER-GUIDE.md)** - fork this repo's tooling for your own org, via `org.config.json`
- **[docs/P2P-AD-BOUNTY-KIT.md](docs/P2P-AD-BOUNTY-KIT.md)** - the proven ad/promo bounty structure (BAR/RUBRIC/ASSET KIT/REWARD), extracted from R2/R3 into an org-agnostic template
- **[docs/GENERAL-BOUNTY-BOARD.md](docs/GENERAL-BOUNTY-BOARD.md)** - using POIDH beyond ads, as a general task bounty board (bug fixes, research, docs), designed around the never-cast zabal-bugfix draft (see [rounds/drafts/zabal-bugfix/](rounds/drafts/zabal-bugfix/))
- **[docs/PARTNERSHIP-TARGETS.md](docs/PARTNERSHIP-TARGETS.md)** - researched partnership candidates for spreading POIDH adoption, plus send-ready outreach drafts in `docs/outreach/`

---

## License

This repo: MIT.

Brand kits inside `assets/brand-kits/`: CC-BY 4.0 (per each kit's own README). Remix freely - keep the campaign name + canonical URL visible in your final piece.

---

Maintained by Zaal / BetterCallZaal. POIDH bounties are BCZ-issued + Zaal-funded. Issuer wallet: BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af` on Base.
