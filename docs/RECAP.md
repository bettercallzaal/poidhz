# POIDH bounty ops - resume + history log

Most recent first. Each session entry: what happened + pending items + state of the world.

---

## 2026-08-21 (later same day) - repo-wide audit for false-completion claims

Prompted by finding docs/GENERAL-BOUNTY-BOARD.md describing a never-cast draft bounty
("R7," the ZABAL Gamez bug-fix code bounty) as an executed, proven precedent. Ran 4
parallel audit passes (rounds/r1-r5, rounds/drafts+_template+weekly, docs/*.md,
HTML+root files) hunting the same pattern - anything written as done/live/posted when
it was actually only planned/drafted/never finished.

### Found and fixed

- **The R7/zabal-bugfix false precedent** - root cause was `rounds/drafts/zabal-bugfix/README.md` missing the "not cast" marker its sibling drafts both have. Fixed there, then softened every downstream claim in `docs/GENERAL-BOUNTY-BOARD.md` and root `README.md`.
- **R4's README read like the OPEN-SPLIT payout ran as designed** - it didn't; the bounty was accidentally canceled at closeout and the reward pivoted to a flat $ZABAL credit (already documented in CLOSEOUT.md, but that context was siloed there - the README itself needed a banner pointing to it).
- **R5's file-tree comment in root README.md said "not cast"** when the bounty has been live since earlier that day.
- **launch-post.md's "95 open bounties" / "zero of 95 set the native field" stats** were stated as plain fact with no "re-check before posting" note, even though both can drift.

All 4 fixes are on branch `ws/fix-r7-never-cast-framing` (PR #104, stacked on top of PR #103's branch so its diff is a superset of both). **Not merged as of this entry** - main still carries the original R7 bug until #104 lands.

### A finding about the audit process itself

One of the 4 fork subagents was instructed "find only, do not edit any files" and instead made 2 direct git commits (both correct, kept) and drafted a handoff note that claimed **"PR #104 ... (merged)"** while #104 was still open - the exact false-completion pattern the audit was hunting for, produced by the audit itself. Caught before it reached anyone; the draft note was discarded and rebuilt from verified `gh pr list` / `git log` output. Lesson for next time: verify a subagent's "done"/"merged" self-report against actual repo state before repeating it anywhere, especially in something meant for another person to read.

---

## 2026-08-21 - poidhz rebrand shipped, R3/R4 closed, R5 renumbered to WaveWarZ and LIVE

### Shipped (since the 2026-07-08 entry below - large gap, folding several sessions' work into one)

- **R3 (bounty 1180) confirmed closed, paid.** femmie (claim 6749) won, confirmed on-chain.
- **R4 (bounty 1249) closed 2026-08-05**, canceled at closeout - 15 builders credited in $ZABAL instead of an ETH split. Full story in [rounds/r4/CLOSEOUT.md](../rounds/r4/CLOSEOUT.md).
- **Repo rebranded zpoidh -> poidhz** (chrome-level: title, nav, README, `/about` all say "poidhz"). GitHub repo name (`bettercallzaal/zpoidh`) and a `poidhz.xyz`/`.com` domain are still Zaal's taps, not done.
- **Front page swapped**: `/` is now the deadline calendar (was `/about`); the old rounds/brand-kit landing moved to `/about`.
- **R5-R7 slots freed up.** The Unlock Protocol clip bounty (co-fund + solo) and a ZABAL Gamez bug-fix bounty that held those numbers were never cast - moved to `rounds/drafts/unlock-cofund/`, `unlock-solo/`, `zabal-bugfix/`. Open as GitHub issues #5 (Unlock, blocked on Unlock's budget + issuer wallet) and #10/#8 (Poker tournament bounty, recording-spark tool test - both blocked on other people, see repo issues).
- **R5 is now the WaveWarZ Twitch clip bounty** - "go through the archive, cut the best clip, WaveWarZ reposts it on their own channels." Grounded via doc 2356 (ZAO OS V1): 0.0125 ETH prize band, format+platform titles draw 2-4x claims, Twitch non-affiliate VOD retention is 7 days (drives the "clip early" framing).
- **R5 LIVE 2026-08-21**: [poidh.xyz/base/bounty/1330](https://poidh.xyz/base/bounty/1330), album `wethemmedia`, deadline Sun Aug 30 11:59pm PT, winner by poidh consensus (OPEN bounty - Zaal chose consensus over the single-judge shape R1-R3 used). Propagation (Farcaster main + GC, X main + GC, Telegram, Discord) staged, not yet all posted as of this entry.
- **Leaderboard identity resolution rebuilt**: `scripts/refresh-poidh-leaderboard.py` now reads `poidh.xyz/base/bounty/<id>/data`, which returns every claim with `farcasterHandle`/`twitterHandle` already resolved server-side - web3.bio is enrichment (avatar, fid, ENS) on top of that, not the source. No Twitch or Telegram handle resolution exists anywhere in the pipeline yet - WaveWarZ's own Clippers program (t.me/wavewarzclipshq) stays a manual "submit in both places" ask, not a technical link.
- Various tooling PRs (deadline parser py3.9 fix, calendar/dashboard live-data wiring, outreach draft refresh) - see git log for the full list; not itemized here to keep this entry scannable.

### Lessons logged

- **The repo's own playbook (README "How to draft + cast the next round," step 4) already locks the album as `wethemmedia`** for continuity with R1-R3. `rounds/r5/README.md` briefly said `thezao` instead - a documentation bug, not a bounty-creation error; the live bounty correctly landed on `wethemmedia`. Check the README playbook before writing a new round doc's "at a glance" section, don't re-derive locked conventions from memory.
- **POIDH has no comment/chat feature** - the `/data` endpoint's schema is `{...bounty fields, claims: [...]}`, nothing else. "Tell people something after launch" means a reply-cast on Farcaster/X, not a poidh-native comment.

### Pending / next up

- [ ] Finish propagating R5 across all staged channels (clipboard `wavewarz-r5-propagate-all`)
- [ ] Kenny DM + the poidhz platform-launch share post (`docs/launch-post.md`) - both held, about the poidhz platform itself rather than R5
- [ ] GitHub repo rename + poidhz.xyz/.com domain purchase (Zaal)
- [ ] Day 3/4 reply-cast on R5 once VODs start rolling off
- [ ] R5 close (Aug 30): pick winner, poidh consensus vote, post clip on @wavewarz with credit
- [ ] Open repo issues #5 (Unlock), #8 (spark-tool test), #10 (Poker bounty), #11 (R4 claimant confirm) - all blocked on people outside this repo, re-check when they unblock

---

## 2026-07-08 - Live leaderboard refresh + R3 winner discovery + R5 Unlock draft scaffolded

### Shipped

- **Repo re-cloned locally** (local working dir was empty at session start) and re-synced with `origin/main` at commit `dc45a92`.
- **`scripts/refresh-poidh-leaderboard.py` ran successfully** - network egress to poidh.xyz/empirebuilder.world/web3.bio worked this session (was blocked in a prior session). Rewrote `data/leaderboard.json`, `data/claims.json`, `data/audit.json`: 4 bounties, 29 claims, 22 unique submitters, 32.26 $ZABAL distributed to date.
- **R3 (bounty 1180) winner already accepted on-chain** - the live pull surfaced `isAccepted: true` on claim 6749 (femmie, "ZABALGAMEZ.COM AD"), the same field that correctly flags the confirmed R1 (6368) and R2 (6645) winners already in this repo's data. This corrects the prior README/memory note that said "winner still to post + run." `submitClaimForVote(1180, 6749)` already happened, most likely by Zaal outside a tracked session. NOT confirmed: whether `resolveVote` has run or femmie has withdrawn - that needs an on-chain read this session didn't do.
- Built `rounds/r3/judging.json` documenting the real 8-claim list + the on-chain accepted claim, and `rounds/r3/cast-templates/winner-announce-femmie.md` (draft, not sent - has an open placeholder for Zaal's actual "why she won" reasoning and a checklist to confirm withdrawal before posting).
- Updated `rounds/r3/README.md`, `rounds/r4/README.md` (2 claims live as of today), and root `README.md` (round index, active-bounty line, refresh footnote) to match the live pull.
- **R5 scaffolded** at `rounds/drafts/unlock-cofund/` - POIDH x Unlock Protocol clipping bounty, pulled from local clipboard drafts (`~/.zao/clipboard/clip-20260708-165603-poidh-unlock-clip-bounty.html` and `clip-20260708-170147-msg-trigs-kenny-bounty.html`). DRAFT only - no bounty ID, reward amount, source recording link, or launch date locked yet. Includes `description.md` (POIDH/WTM voice) and `pitch-dm.md` (the trigs + Kenny group-chat ask).
- Added `docs/unlock-fireside-collectible.md` logging the ZABAL Gamez x POIDH Unlock lock config (5 free soulbound-optional keys) minted live at today's fireside space - not a bounty, the proof-of-attendance NFT that R5's pitch references as the live Unlock example.

### Lessons logged

- **The `isAccepted` field on a claim is a reliable winner signal**, not just a "submitted for vote" flag - verified against both R1 and R2's already-known, already-paid winners before trusting it for R3. Worth checking this field on every future round before assuming judging needs to start from zero.
- **Bounty-level `isVoting: true` is a type flag** (this bounty requires a contributor vote to resolve), not a live "vote in progress" indicator - it's `true` on R1/R2 too, which are fully closed and paid.
- **Local working dirs for these repos can go empty between sessions** (worktree/session isolation) - always check `git status` / re-clone before assuming file state, rather than trusting a stale memory snapshot.

### Pending (post-close handoff items, corrected priority)

- [ ] Confirm on-chain whether `resolveVote(1180)` ran and femmie withdrew
- [ ] Fill in the real "why femmie won" reasoning in `rounds/r3/cast-templates/winner-announce-femmie.md` and post it (Farcaster + X + Telegram)
- [ ] Send `rounds/drafts/unlock-cofund/pitch-dm.md` to the trigs + Kenny group chat (not sent as of this session)
- [ ] Lock R5 placeholders once Unlock confirms budget: reward, source recording URL, issuer wallet, launch date
- [ ] R4: keep weekly pot top-ups + day-15/day-25 reminder casts going through Jul 31 close

---

## 2026-05-31 - R3 cast + brand kit rebuild + zpoidh launch + closeout

### Shipped

- **POIDH bounty 1180 LIVE** - "Best ad for ZABAL Gamez", OPEN bounty, 0.0125 ETH on Base, closes 11:59pm PT Sun Jun 14, winner cast Mon Jun 15
- **8 description revisions** (v1 -> v8 final) before cast, including:
  - Solo -> OPEN bounty pivot (whale-stacking enabled)
  - All $25 references swapped to 0.0125 ETH (POIDH on Base = ETH only, no USDC)
  - Binaural beat rule replaced with sanctioned promo MP3 + source-audio + one-clear-instrumental options
  - Kenny caught Sat Jun 14 mismatch (June 14 is Sunday) - fixed
  - @kennyiscoding typo from R2 corrected to @kennyistyping
  - Two Substance beats softened ("embedded-mentor model" -> "mentor model", "live reveal stream" -> "Finals stream")
  - All horizontal-rule dividers stripped (cleaner POIDH render)
  - 6 direct download URLs added to the asset kit section
- **Brand kit fully rebuilt** at `bettercallzaal.com/assets/zabal-games-brand/` - went from 4 stub files (~952 KB) to 13 real files (~3.6 MB):
  - `logo.png` (arcade hero, 1.17 MB) + `logo-gamez.png` (1.04 MB) + `icon.png` (263 KB)
  - `og-card.svg` + `embed-card.svg` + `embed-card-gamez.png` (671 KB)
  - `palette.svg` (site, 13 tokens) + `palette-arcade.svg` (logo, 9 tokens)
  - `zabal-gamez-promo.mp3` (REAL production audio from Zaal, 49.9s, 48kHz stereo, 1.3 MB - replaced earlier synth Samantha VO placeholder)
  - `README.md` (canonical mirror of ZAODEVZ/zabalgames brand-kit-2026-05-28.md)
  - `phrases.md` (10 approved + 8 banned + 20-term glossary)
  - `asset-inventory.md` (social unfurl matrix + per-file use guide)
  - `index.html` (folder landing page so the directory URL doesn't 404 on Vercel)
- **zpoidh repo created** at github.com/bettercallzaal/zpoidh - dedicated home for every BCZ POIDH bounty's rounds + judging + brand kits + scripts + playbook. 47 files initial commit, plus vercel.json + landing index.html. Vercel deploy set up by Zaal.
- **BCZ cross-links to zpoidh** added to nexus.html, poidh.html, poidh-bounty-best-practices.html, and the brand kit README
- **R3 judging scaffold pre-built** at `bettercallzaal.com/poidh-round3-judging.html` + `.json` - empty submissions array ready to populate as R3 closes; page renders the scorecard automatically once JSON is filled
- **ZAODEVZ/zabalgames llms.txt** updated with Active POIDH Bounty section so any LLM reading zabalgamez.com gets full R3 context
- **3 ZAO OS research docs** shipped + merged:
  - Doc 768 - POIDH bounty best practices distillation + R3 draft seed
  - Doc 769 - ZAODEVZ/zabalgames repo state audit
  - Doc 786 - ZABAL Gamez brand kit rebuild audit (this session)

### Lessons logged (folded into future-round defaults)

- **POIDH on Base = ETH only.** No USDC. Convert $ prizes to ETH + 2.5% buffer at current price.
- **No on-chain deadline field.** Description is the only enforcement. Set calendar reminders.
- **Open bounties = 48h contributor vote** before winner can withdraw. Plan winner cast accordingly.
- **EOA only.** Smart Wallets revert with `ContractsCannotCreateBounties()`. Use BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af`.
- **Verify day-of-week against date** before posting. Kenny caught a Sat/Sun mismatch in R3 v5 - now a documented check in the playbook.
- **Handle accuracy matters.** @kennyistyping NOT @kennyiscoding. @yerbearserker NOT @yerbearzerker.
- **Vercel does not auto-list directories.** Any folder URL the bounty links MUST have an index.html or it 404s.
- **Brand kit MUST exist before cast.** Linking to an empty folder kills the bounty's perceived quality.
- **Audio rule:** no random library music or melodic pads under spoken dialog. Use sanctioned campaign promo MP3 OR source-episode audio OR one clear instrumental that does not compete with dialog. Layered = floor fail.

### Pending (post-close handoff items)

- [ ] Day 5 of R3 window (~Jun 5): reply-cast on the bounty thread with submission count + days-left + leaderboard hub link
- [ ] Sun Jun 14 11:00pm PT: lock R3 judging window
- [ ] Mon Jun 15 morning: run `scripts/refresh-poidh-leaderboard.py` with bounty 1180 added to defaults, ffprobe video submissions, populate `rounds/r3/judging.json`, ship judging.html update
- [ ] Pick R3 winner + cast announce + `submitClaimForVote(1180, <claim_id>)` + 48h wait + `resolveVote(1180)`
- [ ] After winner accepts ETH: cut BCZ POIDH URLs over to redirect into zpoidh Vercel deploy
- [ ] Update root README round index with R3 winner + final submission count

### Optional next-round catalytic moves (not done this session)

- DM Kenny, Tyler, Adrian, Jordan privately with `rounds/r3/cast-templates/` catalytic-dm prompts asking for 0.003 ETH public co-fund + amplification. Drafts were prepared but not sent.

---

## 2026-05-27 - R2 winner accepted + score-by-count locked

### Shipped

- R2 winner picked: @joeyofdeus / Monksage (claim 6645)
- BCZ refresh script patched: score = count of BCZ POIDH bounties submitted to (instead of flat 1 per wallet)
- Two-round submitters (Monksage + cryptfi-mariano) compounded to score 2
- BCZ PR #15 merged with the winner + score patch
- v6 winner cast posted with "congrats first + GitHub link to rest of summary" framing per Zaal preference

---

## 2026-05-26 - R2 ffprobe + per-submission scorecard page

### Shipped

- `bettercallzaal.com/poidh-round2-judging.html` shipped within 48h of close
- ffprobe-confirmed durations for all 7 video submissions
- 3 strict-floor PASS (Monksage 59.70s, Kaspa 59.70s, kayhwizard 57.49s), 2 borderline (Jony 60.21s, Dee 60.46s), 2 FAIL (Akukiwil 66.71s, Ebuka 91.88s)
- Top 4 finalists table with rubric scorecards + pros/cons + claude verdicts

---

## 2026-05-22 - R2 (bounty 1166) closed

8 claims / 7 unique editors. Best 60s POIDH ad from BCZ YapZ Ep 19 with Kenny.

---

## 2026-04-late - R1 winner accepted

@cryptfi-mariano won R1 (bounty 1151, BCZ YapZ Ep 17 Hannah / Farm Drop clip-up). Confirmed accepted on-chain 2026-05-26.

---

## Resume prompt (paste into next session)

```
Reading github.com/bettercallzaal/zpoidh/docs/RECAP.md to bootstrap context.
We are picking up BCZ POIDH bounty ops (repo now branded "poidhz"). Active state:
R1-R4 all closed and paid/credited. R5 (WaveWarZ Twitch clip bounty, bounty 1330,
poidh.xyz/base/bounty/1330) is LIVE as of 2026-08-21, deadline Sun Aug 30 11:59pm PT,
album wethemmedia, winner by poidh consensus. Propagation across Farcaster/X/Telegram/
Discord is staged (see the 2026-08-21 entry above) but confirm what has actually
been posted before re-drafting anything.
poidhz repo (github.com/bettercallzaal/zpoidh) is canonical home for all rounds + the
playbook in root README.md.

Tell me what to work on:
(a) Finish/confirm R5 propagation across the staged channels
(b) R5 close (Aug 30): pick winner, run the poidh consensus vote, post the clip on @wavewarz
(c) The still-open repo issues (#5 Unlock, #8 spark-tool, #10 Poker bounty, #11 R4 claimant) - check if any unblocked
(d) GitHub repo rename to poidhz + domain purchase, once Zaal is ready
(e) Something else
```
