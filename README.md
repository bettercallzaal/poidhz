# zpoidh - BCZ POIDH bounty ops

Source of truth for every BCZ-issued POIDH bounty. Rounds, judging pages, brand kits, leaderboard refresh, the canonical bar, the lessons learned. Everything you need to draft + cast + judge the next round lives here.

**Latest closed:** [Round 4 - The ZABAL Gamez open pot](https://poidh.xyz/base/bounty/1249) - CLOSED 2026-08-05. Bounty was accidentally canceled instead of withdrawn mid-closeout (ETH refund reclaimed to treasury); the 15 qualifying builders were rewarded via a $ZABAL Empire Builder leaderboard credit instead, cast posted. See [rounds/r4/CLOSEOUT.md](rounds/r4/CLOSEOUT.md) for the full story - worth reading before running another OPEN-SPLIT round.
**Also closed:** [Round 3 - Best ad for ZABAL Gamez](https://poidh.xyz/base/bounty/1180) - fully resolved + paid out on-chain, winner @femmie claim 6749 (verified via direct `bounties()`/`getClaimsByBountyId()` eth_call against the deployed contract, not just the API). Winner + honorable-mention casts are drafted and ready in [rounds/r3/cast-templates/](rounds/r3/cast-templates/).
**Designed, awaiting Zaal's go:** the WEEKLY format - "this is for the ZAO" recurring solo video bounty, one fresh bounty per week, claim-is-the-entry, skill-judged with a published 100-point rubric (raffle-safe). Spec: ZAOOS doc 2308. Templates: [rounds/weekly/](rounds/weekly/). Blocked on prize pick + album config + EB sync fix.

**Drafting, not cast:** Round 5 (POIDH x Unlock Protocol, DAO co-funded pitch, DM never sent), Round 6 (same idea, solo-cast version, tooling built via `docs/create-bounty.html`, recommended over R5), Round 7 (first CODE bounty - bug fixes for zabalgamez.com, also ZOL's first money-action trust-ladder rung). See [rounds/r5/](rounds/r5/), [rounds/r6/](rounds/r6/), [rounds/r7/](rounds/r7/).

**Live surfaces (all verified 200 on 2026-05-31, BCZ canonical during R3 window):**
- Hub: https://bettercallzaal.com/poidh.html
- Best practices: https://bettercallzaal.com/poidh-bounty-best-practices.html
- R2 judging: https://bettercallzaal.com/poidh-round2-judging.html
- R3 judging (scaffold ready, populates as submissions land): https://bettercallzaal.com/poidh-round3-judging.html
- Brand kit landing: https://bettercallzaal.com/assets/zabal-games-brand/
- Brand kit promo MP3 (50s): https://bettercallzaal.com/assets/zabal-games-brand/zabal-gamez-promo.mp3
- EB leaderboard feed: https://bettercallzaal.com/poidh-leaderboard.json

After R3 closes + winner cast, those URLs cut over to redirect into this repo's Vercel deploy. Until then BCZ stays canonical so the live bounty 1180 description never breaks.

## Session closeout 2026-05-31 (everything that landed)

All PRs from the R3 prep + zpoidh launch session merged. Live state:

| Repo | PR | What |
|---|---|---|
| BCZ | #16 | R3 prep folder + best-practices page + binaural beat MP3 (merged earlier) |
| BCZ | #17 | Replace binaural with synth promo (merged, superseded by #18) |
| BCZ | #18 | Real production promo MP3 + full brand kit rebuild (12 files) |
| BCZ | #19 | index.html for `/assets/zabal-games-brand/` folder URL (fixes Vercel directory 404) |
| BCZ | **#20** | R3 judging scaffold + zpoidh cross-links from nexus, poidh hub, best-practices, brand kit README |
| ZAOOS | #718 | Doc 768 - POIDH bounty best practices + R3 draft seed |
| ZAOOS | #724 | Doc 769 - ZAODEVZ/zabalgames repo audit |
| ZAOOS | #761 | Doc 786 - ZABAL Gamez brand kit rebuild audit |
| ZAODEVZ/zabalgames | #33 | llms.txt R3 bounty section (so any LLM reading zabalgamez.com gets bounty context) |
| zpoidh | initial | This repo's first 47 files + landing + vercel.json |

R3 bounty 1180 LIVE on POIDH through Sun Jun 14. Brand kit fully shipped. zpoidh repo is the canonical home for everything POIDH going forward.

---

## What this repo holds

```
zpoidh/
├── README.md                        # this file
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
│   ├── r5/                          # POIDH x Unlock (DAO co-fund pitch) - draft only, not cast
│   ├── r6/                          # POIDH x Unlock (solo-cast, recurring) - built, not cast
│   └── r7/                          # ZABAL Gamez bug-fix bounty (first CODE round) - draft, not cast
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

## How to draft + cast the next BCZ POIDH bounty (the playbook)

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
- **For CODE bounties especially**: same-day cross-post to Bountycaster (bountycaster.xyz, indexed by @bountybot via the `/bounties` channel) - reaches 200-400 Farcaster-native builders who won't see poidh.xyz or a GitHub issue on their own. POIDH handles escrow, Bountycaster handles discovery. See [rounds/r7/bountycaster-cast.md](rounds/r7/bountycaster-cast.md) for the format (ZAOOS doc 1584 has the full mechanics). This was flagged for R7 back in July and never actually posted because R7 itself was never cast - don't repeat that gap.

### 5. Set reminders
- Day 5 of window: reply-cast with "N submissions so far, deadline in X days, gallery: bettercallzaal.com/poidh.html"
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

Update via `scripts/refresh-poidh-leaderboard.py` - reads POIDH tRPC, aggregates per-wallet counts, writes the strict EB feed at `data/leaderboard.json`. EB pulls from `https://bettercallzaal.com/poidh-leaderboard.json` during the R3 window; after cut-over it pulls from this repo's Vercel deploy.

---

## Round index

| Round | Bounty | Episode / Source | Prize | Winner | State | Doc |
|---|---|---|---|---|---|---|
| R1 | [1151](https://poidh.xyz/base/bounty/1151) | BCZ YapZ Ep 17 (Hannah / Farm Drop clip-up) | 0.0105 ETH | @cryptfi-mariano (claim 6368) | closed, paid | [rounds/r1/](rounds/r1/) |
| R2 | [1166](https://poidh.xyz/base/bounty/1166) | BCZ YapZ Ep 19 (Best 60s POIDH ad w/ Kenny) | 0.0105 ETH | @joeyofdeus / Monksage (claim 6645) | closed, paid | [rounds/r2/](rounds/r2/) |
| R3 | [1180](https://poidh.xyz/base/bounty/1180) | ZABAL Gamez ad (any format) | 0.025 ETH | @femmie (claim 6749) | closed, paid, confirmed on-chain via direct `bounties()`/`getClaimsByBountyId()` eth_call - cast templates drafted, not yet posted | [rounds/r3/](rounds/r3/) |
| R4 | [1249](https://poidh.xyz/base/bounty/1249) | ZABAL Gamez July open build pot | $ZABAL leaderboard credit (originally an ETH split, bounty was accidentally canceled mid-close) | 15 qualifying builders | CLOSED 2026-08-05 - see [CLOSEOUT.md](rounds/r4/CLOSEOUT.md) | [rounds/r4/](rounds/r4/) |
| R5 | not cast | POIDH x Unlock Protocol clip bounty, DAO co-funded pitch | TBD (Unlock to set) | - | DRAFT - pitch DM never sent | [rounds/r5/](rounds/r5/) |
| R6 | not cast | Same Unlock idea, solo-cast, auto-versioning via `docs/create-bounty.html` | TBD | - | built + tested, ready to cast, recommended over R5 | [rounds/r6/](rounds/r6/) |
| R7 | not cast | ZABAL Gamez bug fixes (first CODE bounty) | seeded at cast time, multiple winners possible | - | DRAFT - also ZOL's first trust-ladder money-action rung | [rounds/r7/](rounds/r7/) |
| R8 | not cast | WaveWarZ Twitch clip bounty (twitch.tv/wavewarzofficial, clip for WaveWarZ's own socials) | 0.02 ETH recommended, Zaal sets | - | DRAFT 2026-08-20 - paste-ready, gated on Zaal (scope confirm, prize, fund, create, post); card 769a4a6b | [rounds/r8/](rounds/r8/) |

Leaderboard refresh last run 2026-08-05 - `data/leaderboard.json` / `claims.json` /
`audit.json` include R1-R4 (22 submitters via on-chain POIDH claims, plus R4's separate
15-wallet $ZABAL leaderboard credit tracked in `rounds/r4/r4-builder-leaderboard.csv`).

---

## Brand kits

Each campaign gets a CC-BY brand kit under `assets/brand-kits/<campaign>/`. The kit holds the canonical logo, palette, typography spec, voice rules, approved/banned phrases, glossary, and an official 50-second promo audio file editors can use freely.

Current campaigns:
- [`assets/brand-kits/zabal-games/`](assets/brand-kits/zabal-games/) - for R3 (active) and any future ZABAL Gamez bounties

Future campaigns get their own subfolder when launched.

Each kit mirrors a canonical source repo (e.g. `github.com/ZAODEVZ/zabalgames` for ZABAL Gamez). Sync target: weekly during the active campaign. If a kit and its canonical source disagree, the source wins.

---

## Where to go for more

- **Doc 768** (ZAO OS V1) - canonical bounty best practices distillation
- **Doc 769** (ZAO OS V1) - the ZAODEVZ/zabalgames repo audit
- **Doc 786** (ZAO OS V1) - the ZABAL Gamez brand kit rebuild audit
- **Doc 759** (ZAO OS V1) - POIDH history (Kenny + lifetime stats + cohort patterns)
- **Doc 631** (ZAO OS V1) - POIDH x $ZABAL x Sentinel convergence map
- **Doc 625** (ZAO OS V1) - POIDH x ZAO bounty playbook (18 templates)
- **Doc 992** (ZAO OS V1) - clipper -> POIDH pipeline concept, R5 is the manual v1 test of it
- **Doc 2202** (ZAO OS V1) - POIDH x ZAO current-state + brand-alignment synthesis (Aug 2026)
- **Doc 2203** (ZAO OS V1) - full POIDH x ZAO lore, Kenny's 2023 founding through today
- **[docs/unlock-fireside-collectible.md](docs/unlock-fireside-collectible.md)** - the Unlock Protocol proof-of-attendance NFT minted at the fireside R5 draws on
- **[docs/RECAP.md](docs/RECAP.md)** - resume artifact + ongoing state
- **[docs/PARTNER-GUIDE.md](docs/PARTNER-GUIDE.md)** - fork this repo's tooling for your own org, via `org.config.json`
- **[docs/P2P-AD-BOUNTY-KIT.md](docs/P2P-AD-BOUNTY-KIT.md)** - the proven ad/promo bounty structure (BAR/RUBRIC/ASSET KIT/REWARD), extracted from R2/R3 into an org-agnostic template
- **[docs/GENERAL-BOUNTY-BOARD.md](docs/GENERAL-BOUNTY-BOARD.md)** - using POIDH beyond ads, as a general task bounty board (bug fixes, research, docs), grounded in R7's precedent
- **[docs/PARTNERSHIP-TARGETS.md](docs/PARTNERSHIP-TARGETS.md)** - researched partnership candidates for spreading POIDH adoption, plus send-ready outreach drafts in `docs/outreach/`

---

## License

This repo: MIT.

Brand kits inside `assets/brand-kits/`: CC-BY 4.0 (per each kit's own README). Remix freely - keep the campaign name + canonical URL visible in your final piece.

---

Maintained by Zaal / BetterCallZaal. POIDH bounties are BCZ-issued + Zaal-funded. Issuer wallet: BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af` on Base.
