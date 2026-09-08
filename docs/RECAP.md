# POIDH bounty ops - resume + history log

Most recent first. Each session entry: what happened + pending items + state of the world.

---

## 2026-09-06 to 09-08 - the money got credited, the promises got counted, and the tooling started checking itself

Three days in one entry. If you read nothing else: **R5's entrants were uncredited in two
places at once and only one was visible**, four of five rounds were paid and left owing
something, and the two checkers built to catch that were themselves broken in ways only
running them exposed.

### The credit gap, closed in both places

R5's nine claimants were scoring **zero** on the leaderboard. Bounty 1330 was never added to
`default_bounty_ids`, so `refresh-poidh-leaderboard.py` never counted it and
`refresh-rounds.py` never tracked it - 1330 appeared nowhere in `data/claims.json`. Fixed;
the leaderboard went 34 -> 38 submitters and the two R5-only wallets, including the winner,
now appear.

Separately, **Empire Builder had been serving a stale feed since at least 2026-08-08**,
missing six submitters including **femmie, R3's winner**. Zaal repointed its `api_endpoint`
at `poidhz.com/leaderboard`; re-adding the leaderboard changed its uuid, so every tool here
was calling a dead one and 404ing. `org.config.json` updated, and `check-eb-sync.py` now
passes end to end for the first time since it was written - **38 local vs 38 on EB, in sync**.

**Both halves were needed.** Either fix alone still leaves R5's entrants uncredited.

### Four of five rounds were paid and left owing something

[`docs/PROMISE-AUDIT.md`](PROMISE-AUDIT.md), read from the live on-chain descriptions rather
than this repo's copies. **R1 is the only round that kept every promise it made - and it is
the round that promised the least.** Every round since promised distribution on top of money
and delivered the money only. R2 promised an announcement by a named date and never even
drafted the copy; R3's has been READY TO SEND since June; R5's is unsent today.

This is not carelessness about money. Every winner was paid, and R3's got more than
promised. What rots is the promises that cost nothing and have no deadline forcing them.

### The tooling now checks the parts humans forget

- `scripts/precast-check.py` - can this round cast. Caught R6 unfundable.
- `scripts/postclose-check.py` - did we do what the bounty text said. Runs `--all` on the 6h
  cron, which would have caught R5's zero-scoring entrants the same day.
- `check-eb-sync.py` finally **runs**, on that same cron. It had existed since 2026-08-08
  invoked by nothing, while the bug it detects stayed open the whole time.

Three bugs were found by *running* these, not by their selftests passing: postclose-check
reported a paid round as unpaid (`/data` does not carry `isAccepted`), its tRPC accessor
assumed a list where the payload is `{"items": [...]}`, and a cron exit code I "verified"
through a pipe was reading grep's status, not the script's.

### poidhz.com, and the rounds

Domain live 2026-09-06, all 18 files migrated, `zpoidh.vercel.app` 307s to it. `/calendar`
had been 404ing while `/` served the same file - fixed and verified in production.

**R6 is now the NYC trip recap** (Zaal, 09-06), with a seven-channel-slot mechanic paying $5
in $ZABAL per used clip - the first round that pays more than one person. **It is PARKED as
of 09-08**: the Drive link and the one-sentence trip summary are deferred, ZAOstock's 13th is
the priority. Drafted, uncast, gated on `precast-check --round 6`.
**R7** is the WaveWarZ clip round, renumbered and queued.

### Two defect families worth carrying forward

**Numbers separated from what makes them true.** A figure ahead of its date (R5 shipped
"13.9 SOL as of Aug 20" when the total hit 13.9 in September), separated from its leg
(1.005% is the artist's *share*, not the trade fee - which is 1.500%), or separated from its
source's own warning (`wavewarz/743` has said since 2026-08-09 not to use its 458 SOL figure,
and nobody had opened it). `rounds/_template/description.md` now carries the rule, the
do-not-carry list, and the generator path - **generate the line, do not copy it.**

**Records that stay loud after they stop being true.** The mirror of an inverted alarm. R5's
README said LIVE above CLOSED; three dropped outreach DMs still read as send-ready. Fixed at
the top of each file, because that is where they are read. Anything time-bound now carries a
re-check date next to the claim.

### Pending

- [ ] **R5's winner announcement.** Paid 09-05, still unannounced. Zaal posts it himself.
      Gates the Kenny R6 note, the wimpydwi retainer, and the launch post - all written.
- [ ] **femmie's DM** - `rounds/r3/cast-templates/femmie-dm.md`, asks before announcing
- [ ] R6: Drive link + trip sentence, both **parked** by Zaal, not pending
- [ ] Verify the 6h cron goes green after the 404-retry fix (#130); it failed 09-08T04:11
- [ ] Empire Builder: nothing owed, in sync. Left here so nobody re-opens it.

---

## 2026-09-05 - R5 closed and paid, R6 drafted, and the "low turnout" story was wrong

### R5 final state, measured not assumed

Bounty 1330 is **closed and paid**. Claim **7795** carries `isAccepted: true`, `inProgress`
is `false`, pot **0.0238 ETH** (~$59) to `0x3f07d412da0aa3615bd92a496c73823a64370ec9`. The
winning clip is [@wimpydwi's](https://x.com/wimpydwi/status/2094135544758608181), JOHN 3v16
by @LadyrynNemesis vs THE SUMO WRESLER by @The7_is_a_T. Accepted on-chain outside a tracked
session, some time between 2026-09-03 and 2026-09-05.

Reproduce any of this with `python3 scripts/query-bounty.py --bounty 1330`.

### Three things this repo believed about R5 that were false

1. **"Claims cannot be read without a connected wallet."** They can. The anonymous
   `poidh.xyz/base/bounty/1330/data` endpoint returns the full claims array to nobody in
   particular. Only the *rendered page* hangs on "loading claims" - the data behind it was
   always public. A whole handoff was built around going and connecting a wallet, and the
   answer was one curl.
2. **"Low turnout, the format is the problem."** R5 drew **9 claims from 7 distinct
   entrants** (coolhat and one unlinked wallet filed twice each). Against R1's 11, R2's 8
   and R3's 8, that is mid-pack. There was never a format problem to fix.
3. **"The dashboard is nine days stale."** It refreshes on cron now - `data/bounty-dashboard.json`
   was 20 minutes old when checked, correctly showing `has_submissions: true`. The
   auto-refresh from #106 works. The stale-dashboard warning was itself stale.

The lesson is the one already in this log, pointing the other way: a claim about what
*cannot* be known deserves the same verification as a claim about what was done. "The live
page hangs, so this needs a wallet" was a guess that hardened into a blocker across two
handoffs.

### What is actually still owed on R5

**The winner has been paid but never announced.** Nothing has gone out on @wavewarz with
@wimpydwi credited, which the bounty text explicitly promised ("the clip goes up on
@wavewarz with your name on it"). R5's under-distribution problem, logged on 2026-08-22,
now extends past the close: the round was never announced to the clippers, and its winner
has not been announced to anyone. This is the oldest open item in the repo and it is one post.

Also unresolved: the payee wallet resolves to no Farcaster, X or ENS identity on web3.bio.
The claim carried @wimpydwi's X link, so the pot was released on a reasonable judgment call,
but nothing on-chain ties the address to the handle. R6 fixes the general case by requiring
the handle in the claim text.

### R6 drafted

`rounds/r6/` - WaveWarZ clip round 2, not cast, no bounty ID. Zaal's levers, set 2026-09-05:
0.0125 ETH seed (fund 0.0128), **14-day window** (a month was considered and rejected against
a 7-day archive), and the ask reframed from finding to making - "capture a moment and try
something new so that we can use that."

Five changes from R5, each with its reasoning inline in `rounds/r6/README.md`: treatment
ranked above moment, the deliverable spec made binding rather than a rubric bonus (vertical
9:16, burned-in captions, visible mark, kept audio, 20-90s), handle required in the claim,
retainer holders excluded from the pot, and the on-chain deadline set to match the stated one
(R5's disagreed by six days; every prior round shows the same drift, since the field is set
at creation and never tracks the text).

Gate 1 on R6 is not the money. It is announcing from @wavewarz and dropping it in
t.me/wavewarzclipshq - the two surfaces R5 never reached. R5 got nine claims without ever
being shown to the people who clip this stream for points.

Also drafted: `rounds/r6/retainer-outreach.md`, a message to @wimpydwi asking what a month
of clips would cost. Zaal's call, price to come from them. It states the eligibility
exclusion up front rather than letting it surface after a deal.

### Source freshness note

`wavewarz.info` reports **1,371 battles** (test battles excluded) as of 2026-09-05. R5's
description said 1,419 as of Aug 20 - a *higher* number a fortnight earlier, so the two are
counting different things. R6 quotes the site's current figure with its exclusion wording
rather than picking a side. The SOL volume and artist-earnings figures from R5 are dropped
rather than carried, because `wavewarz.info` serves them client-side with no JSON endpoint
and they could not be re-measured. Settle the battle count with WaveWarZ before a third
round quotes one.

### Pending

- [ ] **Announce R5's winner on @wavewarz with @wimpydwi credited.** Oldest open promise.
- [ ] Confirm with @wimpydwi that `0x3f07d412...70ec9` is their wallet
- [ ] Send `rounds/r6/retainer-outreach.md`, if the retainer conversation is on
- [ ] R6 gate 1: @wavewarz + t.me/wavewarzclipshq, before anything else
- [ ] R6: fund 0.0128, cast with the deadline matching the text
- [ ] Hurric4n3IKE conversation, open since 2026-08-21 - includes archiving VODs off Twitch,
      which is the real fix for the 7-day expiry that a 14-day window makes worse

---

## 2026-08-22 - R5 was posted after all, but only from personal accounts

The unchecked "Post promo-cast.md" gate was **stale in the opposite direction**: the promo had
in fact gone out, from Zaal's personal X on 2026-08-21 12:36 PT
([status 2090749876950691917](https://x.com/bettercallzaal/status/2090749876950691917)) and from
Iman's personal account. Same false-completion pattern this log already warns about, just
inverted: a box left unticked on work that happened.

What it has **not** done is reach an owner account. Nothing from @wavewarz (verified, and the
audience that watches the stream it is asking people to clip), nothing from @TheZAODAO, and
nothing in the WaveWarZ clippers Telegram at t.me/wavewarzclipshq, which docs 1223 and 1293
name as an existing points-based clippers group.

That reconciles the numbers exactly. 147 views in 27 hours. `has_participants: true` because
someone in Zaal's network topped the pot 0.0128 to 0.0238 ETH. `has_submissions: false` because
no clipper saw it. The bounty copy promises "the clip runs on WaveWarZ official channels" while
never having been announced on one.

So R5 is not under-priced and not badly written. It is **under-distributed**, and the fix is one
post from an account that already has the right audience. Owner-account posting is Zaal's call,
so this is flagged and queued, not actioned.

### Update, same day: ZAO posted, handle corrected

Iman posted the R5 promo from @TheZAODAO on X on 2026-08-22, the first owner-account reach the
round has had, under the standing rule that ZAO posting continues unless Zaal says otherwise.
Zaal was told in the same breath, with the post treated as reversible.

@wavewarz and t.me/wavewarzclipshq are still unreached and still Zaal's to run. Those two are
the ones that matter: ZAO's audience is builders, while the clippers group is people already
clipping that exact stream for points.

Also corrected an error introduced earlier in this entry: the handle is **@wavewarz**, confirmed
in doc 1223 and in the R5 README, not "@WaveWaZ" which was misread off a truncated screenshot
sidebar. Fixed here and in rounds/r5/README.md.

---

## 2026-08-21 (evening) - handoff to Iman, R5 verified live but unpromoted

Ownership of this repo passed to Iman. First act was verifying the handoff against live repo
state rather than acting on it, per the lesson recorded in the entry below.

### Handoff items that were already done or do not exist

- **"Merge PR #104 first, then close #103"** - both already done by Zaal before the handoff
  landed. #104 merged 13:00:39Z (`eb9e9a2`), #103 closed unmerged 15:31:56Z, branch deleted.
  Superset claim independently confirmed: #103's 3 files are all inside #104's 11. No action.
- **`.handoffs/session-2026-08-21-wavewarz-r5-iman-handoff/README.md`** - does not exist. Not
  on main, not on any of the 23 branches, not in either PR. Zero of main's 157 files match
  "handoff". Probably an uncommitted scratchpad, or lived on the deleted `ws/r5-docs-recap-update`.
  Root README.md stands as the reference playbook. Flagged to Zaal, not blocking.

### R5 state, verified from data/bounty-dashboard.json (generated 13:24:54Z)

Bounty 1330 is `open`, multiplayer, 0.0128 ETH / $30.49, deadline 2026-08-30, issuer matches
the BCZ Treasury EOA on file. **`has_submissions: false`, `has_participants: false`.**

Zero claims, because the promo was never posted. The "Post promo-cast.md with the live URL"
gate in `rounds/r5/README.md` is unchecked, and `promo-cast.md` still carries an unfilled
`<BOUNTY_URL>` placeholder, so the casts are not merely unposted, they are not yet postable.
Repo state is not proof of social state, so the accounts still get checked by eye before
anything goes out.

Urgency is structural: the bounty asks entrants to clip a Twitch archive that self-deletes
after 7 days on a 10-day round, so source VODs roll off faster than the deadline arrives.
Every silent day burns material. Nine days left as of this entry.

### Timing

R5 closes Sun 30 Aug 11:59pm PT = **Mon 31 Aug 08:59 CAT / 02:59 ET**. That falls inside
Iman's working morning while Zaal is asleep, so the close and the consensus vote need no one
else awake.

### Pending

1. Fill `<BOUNTY_URL>` across promo-cast.md surfaces, verify copy against repo rules (no
   emojis, no em dashes, artists credited), hand Zaal a one-tap queue.
2. Eyeball the socials before posting. Assume nothing.
3. Track R5 to close, consensus vote, winner posted on @wavewarz with the entrant credited.
4. Zaal's calls, unchanged: GitHub repo rename to `poidhz`, buying `poidhz.xyz`/`.com`, and
   posting from ZAO-owned accounts.
5. Logged not fixed: dashboard classifies 1330 as `task_type: "code"`. It is a clip bounty.
   Auto-classifier artifact, harmless unless it affects discovery.

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

All 4 fixes are on branch `ws/fix-r7-never-cast-framing` (PR #104, stacked on top of PR #103's branch so its diff is a superset of both). **Merged 2026-08-21 13:00:39Z as `eb9e9a2`** - main no longer carries the R7 bug. PR #103 was closed unmerged at 15:31:56Z the same day, correctly: its 3 changed files are all contained in #104's 11. Superset claim verified against both PRs' file lists rather than taken on trust.

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
- Built `rounds/r3/judging.json` documenting the real 8-claim list + the on-chain accepted claim, and `rounds/r3/cast-templates/winner-announce-femmie.md` (draft, not sent - has an open placeholder for Zaal's actual "why they won" reasoning and a checklist to confirm withdrawal before posting).
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
  - Doc 769 (`business/769-zaodevz-zabalgames-repo-state`) - ZAODEVZ/zabalgames repo state audit
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
