# R7 - WaveWarZ clip round 2 (DRAFT, not cast)

> **Renumbered from R6 on 2026-09-06, and queued behind the NYC recap round.** Zaal moved
> the next cast to a different ask (see [rounds/r6/](../r6/), the NYC trip recap), and this
> round waits its turn rather than being discarded - it is fully written and passes the
> validator.
>
> **Two things to redo before casting it, both consequences of the delay:**
>
> 1. **The deadline is now a `<DAY>, <MONTH DAY, YEAR>` placeholder** in `description.md`.
>    It used to say Sunday, September 20, 2026, which was written for a Sep 7 cast and is
>    meaningless now. Set it when you know the cast date, and keep 14 days.
> 2. **Re-measure the Twitch archive - RE-CHECK BY 2026-09-13 and before any cast.**
>    Everything below about VOD counts and the 7-day window was measured on 2026-09-06. The
>    archive self-deletes after 7 days, so those specific VODs are already gone. The
>    constraint holds; the numbers do not.
>
> Run `python3 scripts/precast-check.py --round 7 --prize 0.0128` before casting.

Not live. No bounty ID yet. Second WaveWarZ clip round, running the shape R5 (bounty
[1330](https://poidh.xyz/base/bounty/1330)) proved, with the ask deliberately changed and
two R5 defects fixed in the text.

**Why a second clip round at all:** R5 worked. The premise that it did not is the main
thing this doc exists to correct, so read the next section before re-deriving anything.

## R5's real result, measured 2026-09-05

The handoff brief that opened this round said R5 had low turnout and that the format was
the thing to fix. Both are wrong. Measured off `poidh.xyz/base/bounty/1330/data` and
`claims.fetchBountyClaims`, reproducible with `python3 scripts/query-bounty.py --bounty 1330`:

| | R1 (1151) | R2 (1166) | R3 (1180) | R5 (1330) |
|---|---|---|---|---|
| Claims | 11 | 8 | 8 | **9** |
| Prize | 0.0105 | 0.0105 | 0.025 | **0.0125 seed, 0.0238 final** |

Nine claims from seven distinct entrants (coolhat and one unlinked wallet each filed
twice). That is mid-pack for the series, not a failure. The pot also grew from the 0.0128
funded to 0.0238 ETH without any catalytic DM campaign being run, which is the OPEN type
doing its job.

**What actually underperformed was propagation, and R5's own README already says so:**
the bounty was never announced from [@wavewarz](https://x.com/wavewarz) and never dropped
into the clippers Telegram at [t.me/wavewarzclipshq](https://t.me/wavewarzclipshq), where the
people who already clip this stream are. It went out from Zaal's personal
account, Iman's, and @TheZAODAO. So R5 got nine claims while never reaching its own
audience. That is R7's single biggest lever and it costs nothing, which is why it is
gate 1 below and not a step 7 afterthought.

Winner: claim 7795, accepted on-chain, 0.0238 ETH to
`0x3f07d412da0aa3615bd92a496c73823a64370ec9`. The clip is
[@wimpydwi's](https://x.com/wimpydwi/status/2094135544758608181), JOHN 3v16 by
@LadyrynNemesis vs THE SUMO WRESLER by @The7_is_a_T.

## What is different from R5, and why

1. **The ask moved from finding to making.** R5 said cut the best existing moment. R7 says
   take a moment and give it a treatment nobody has tried on this stream. Zaal's call,
   2026-09-05: "be more specific that the goal is to capture a moment and try something
   new so that we can use that." This changes what wins, so the description's ranking is
   explicit: treatment first, moment second, craft third. R5 ranked moment first.
2. **The deliverable spec is binding.** R5 said "vertical is welcome, not required" and
   left captions and logo in the rubric as bonuses. R7 makes vertical 9:16, burned-in
   captions, visible @wavewarz mark, kept battle audio and the 20-90s length into five
   floor rules, and says plainly that missing one means we cannot run it so it cannot win.
   The reason is the same reason the ask changed: we publish the winner, so an unpublishable
   file is worth nothing to us no matter how good the moment is.
3. **Handle required in the claim text.** R5's winning claim came from a wallet that
   resolves to no Farcaster, X or ENS identity on web3.bio. The clip carried @wimpydwi's X
   link, but nothing on-chain tied the payee address to that handle - the pot was released
   on a judgment call. Asking for the @ in the claim body costs an entrant one line and
   removes the guess.
4. **Retainer holders excluded.** Zaal's call, 2026-09-05, alongside opening a paid
   monthly clipping conversation with @wimpydwi (see `retainer-outreach.md`). A contractor
   on a retainer taking the community pot reads badly, and it reads worse if it surfaces
   after the fact. Stated in the description rather than held as an unwritten rule.
5. **Two weeks, not ten days.** Zaal's call: "lets just do one for two week we can run for
   a little longer than last time." A month was considered and rejected as too long against
   a 7-day archive.

## The 7-day archive constraint, which gets worse at two weeks

`twitch.tv/wavewarzofficial` is not a Twitch Affiliate or Partner channel, so VODs
auto-delete after 7 days. Verified again 2026-09-05 via Twitch GQL: 7 archive VODs, oldest
2026-08-29, newest 2026-09-05, 26 to 202 minutes each, 0 to 11 views apiece.

At R5's 10 days this was a warning. At 14 days roughly half the window's source expires
before the deadline, and someone who hears about the bounty in week two cannot see week
one at all. Three fixes were considered:

- Four weekly capture windows naming live VODs each week - rejected with the month.
- Archiving VODs off Twitch so the full window stays reachable - this is the real fix, and
  it is still an open gate from R5 (Hurric4n3Ike was going to capture VODs himself,
  unchecked since 2026-08-21). Worth chasing independently of this round.
- Clip-early warning plus pointing at Twitch's native Clip button, which persists after the
  VOD dies - what R7 ships, same as R5, with the warning stated in days rather than implied.

The near-zero view counts are also worth reading straight: almost nobody watches this
stream live. The clip is the distribution, not a highlight of it. The description says so.

## At a glance

- **Type / chain:** OPEN, Base. Album `wethemmedia`, continuity with R1-R3 and R5 per the
  locked playbook in the root README. Not `thezao`.
- **Issuer:** BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af`. Must be an EOA,
  not a smart wallet.
- **Prize:** 0.0125 ETH seed, fund **0.0128** (0.0125 x 1.025) so the 2.5% protocol fee does
  not eat the headline. Same as R5, Zaal's call 2026-09-05 - the R5 pot grew on its own, so
  the seed is a floor rather than the number that has to do the work.
- **Window:** 14 days. **Cast date TBD - this round is queued behind R6 (NYC recap).**
  The old Sep 7 / Sep 20 pair is dead; `description.md` now carries a placeholder. Pick the
  close date when you pick the cast date, keep 14 days, and verify the weekday.
- **Winner:** poidh consensus, contributor-weighted vote on the OPEN pot. Same as R5, which
  was a deliberate override of R1-R3's single-judge template.

## Set the on-chain deadline to match the stated one

R5's description said Aug 30 while the on-chain `deadline` field read 2026-09-05 00:21 UTC,
six days later. The field is set at creation and does not track the text - every prior round
shows the same drift (R1 14.1d, R2 20.1d, R3 19.8d between `createdAt` and `deadline`). It
did no harm in R5 because the winner was accepted by hand, but it means any tool reading the
chain gets a different close date than any human reading the bounty. Set them to agree.

## Validator status, and what its PASS does not mean

`python3 scripts/validate-bounty-description.py --description rounds/r7/description.md`
returns PASS. Two things to know before trusting that:

- **R5 fails the same validator** on four sections, and R5 drew nine claims. The validator
  encodes the R3-era template (`THE BAR` / `THE RUBRIC` / `THE ASSET KIT` / `THE REWARD`),
  which R5 deliberately walked away from in favour of a plainer voice. R7 keeps R5's voice
  and restores the canonical headers, so it satisfies both. Do not read R5's FAIL as a defect.
- **The section check reads section bodies as of 2026-09-08, not just header names.**
  THE REWARD must name a prize amount with its token, THE BAR must carry at least one
  numbered or bulleted rule, THE ASSET KIT must carry a link, DEADLINE must carry a date or
  time. A header over an empty section now fails. This paragraph previously said the check
  was a bare header match, which was true until that change and is the kind of note that
  stays loud after it stops being true.
- **It still cannot check a promise against reality.** It can see that THE REWARD names an
  amount; it cannot see whether a $ZABAL trail the text promises actually exists. R7's
  reward section has **no Empire Builder $ZABAL trail**, because R5 omitted that mechanic
  and inventing reward terms is Zaal's call, not a drafting decision. The green verdict will
  not tell you it is missing.

The two remaining WARNs are both expected: no poidh URL yet (added after creation) and no
GitHub brand-kit link (there is no WaveWarZ brand kit - see below).

## No WaveWarZ brand kit exists

`assets/brand-kits/` contains only `zabal-games`, and `bettercallzaal.com/assets/wavewarz/`
404s. R5's "DM @bettercallzaal for the logo files" was the only route to the mark.

This mattered more in R7 than in R5, because R7 promotes the visible mark from a rubric bonus
to a floor rule - which would have put a hard requirement behind a DM. Rule 3 is written as
"@wavewarz **or** the logo", and now says outright that typing the handle on screen satisfies
it, so no entrant is blocked on artwork they cannot get. Building a real WaveWarZ kit is worth
doing before a third round, and is the natural companion to the Hurric4n3IKE conversation.

## Every bettercallzaal.com/poidh* link in this repo is dead

Measured 2026-09-05. `bettercallzaal.com/poidh-bounty-best-practices.html`,
`/poidh.html` and `/poidh-round<N>-judging.html` all return 200 only after redirecting to
`https://github.com/bettercallzaal/poidhz`. The pages still exist as `docs/*.html` in this
repo, but nothing serves them: GitHub Pages 404s, `poidhz.vercel.app` 404s at those paths,
and no `poidhz.*` domain resolved. **That last part is fixed: poidhz.com was registered and
connected on 2026-09-06 and is now the production domain**, so the URLs below point at it.

This is entrant-facing, not cosmetic. The `_template` description tells every future round
to cite the canonical bar, which now drops a clipper on a GitHub repo page. The same dead
URL is cited in `README.md`, `docs/how-to-draft-next-bounty.md`, `rounds/r3/`, and both
`_template` cast files. R7 cites the repo directly instead, which works today.

Two notes for whoever fixes this properly: the repo has been **renamed to `poidhz`** (the
push to `zpoidh` redirects, and the remote now answers as `bettercallzaal/poidhz`), and the
`_template` winner-announce copy promises every submitter a $ZABAL airdrop and links a
per-round judging page - neither of which existed for R5. Do not paste that template
without checking both claims against the round it is describing.

## Pre-cast audit, measured 2026-09-06

Run these four checks again on the morning you cast. Three of the four were green when
this was written; one was not, and it stops the round dead.

### BLOCKER: the issuer wallet cannot fund this bounty

`0x7234c36a71ec237c2ae7698e8916e0735001e9af` holds **0.002154 ETH** on Base, measured
against `mainnet.base.org` and `base-rpc.publicnode.com` (same answer from both).
R7 needs **0.0128** plus gas.

| | ETH | USD at $2,499.78 |
|---|---|---|
| Have | 0.002154 | $5.38 |
| Need | 0.0128 | $32.00 |
| **Short** | **0.0106** | **$26.61** |

This is expected, not alarming: R5 funded 0.0128 out of this wallet and the pot paid out
to the winner. Nobody had checked it since. **Fund the wallet before anything else** -
every other gate below is wasted effort if this one is not cleared first.

Re-check with:

```bash
curl -s -X POST https://mainnet.base.org -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_getBalance","params":["0x7234c36a71ec237c2ae7698e8916e0735001e9af","latest"]}'
```

poidh's on-chain `MIN_BOUNTY_AMOUNT` is 0.001 ETH (doc 2202), so a smaller round is
technically castable - but 0.0125 is Zaal's locked number and dropping it to fit the
wallet would be a silent downgrade, not a decision.

### Green: the description passes

`python3 scripts/validate-bounty-description.py --description rounds/r7/description.md`
returns PASS. The one WARN (no poidh URL) is expected before creation. Read the caveat in
"Validator status" below before trusting the PASS further than it goes.

### Green, with a caveat: the source still exists

Twitch archive on 2026-09-06: **5 archive VODs**, window **2026-09-01 to 2026-09-05**,
124-157 minutes each, 0-3 views apiece. Down from 7 VODs the day before, which is the
7-day expiry doing exactly what this round's text warns about.

The caveat is that the newest VOD is from 2026-09-05 and there was no stream on the 6th.
The round assumes battle nights keep happening across its 14 days. If the stream goes
quiet mid-window, entrants who join late have nothing to clip. Worth a word with
Hurric4n3IKE, who is already on the gate list below.

### The deadline is hardcoded, so a slipped cast silently shortens the round

`description.md` states **Sunday, September 20, 2026** in plain text. That was written for a
cast on Monday 2026-09-07, giving 14 days. The date does not move on its own.

If funding pushes the cast later, either edit the date in `description.md` to keep 14 days,
or accept a shorter round on purpose. What must not happen is casting on the 12th against a
Sep 20 deadline and calling it a two-week window, which is how R5 ended up with a stated
deadline and an on-chain deadline six days apart.

| Cast date | Sep 20 close gives |
|---|---|
| Mon Sep 7 | 14 days, as designed |
| Wed Sep 9 | 12 days |
| Fri Sep 11 | 10 days, R5's length |
| Mon Sep 14 | 7 days, and half the archive expires inside it |

### Green: the data pipeline is healthy

`data/bounty-dashboard.json` regenerating on cron. The leaderboard refresh failed twice on
2026-09-05/06 with poidh 504s; the retry added in #114 landed 2026-09-06T07:38 and the
first run after it (10:43) succeeded. One green run is not proof the fix works, but it is
not contradicted either.

## Zaal gates (money, public, outbound)

- [ ] **FUND THE WALLET - 0.0106 ETH short, see the blocker above.** Nothing else on this
      list can complete until this does.
- [ ] **Gate 1, and the one that matters: announce from @wavewarz and drop it in
      [t.me/wavewarzclipshq](https://t.me/wavewarzclipshq).** R5 never did either. Owner-account
      posting is Zaal's, which is exactly why it is first here instead of buried in a
      propagation checklist.
- [ ] **Confirm with Hurric4n3IKE** - still open from R5, never sent. Also the natural place
      to ask about archiving VODs off Twitch.
- [ ] **Set prize** 0.0125 ETH, fund 0.0128 to the issuer EOA.
- [ ] **Create the bounty** on poidh with the deadline matching the text.
- [ ] **Post** `promo-cast.md` with the live URL.
- [ ] **Send** `retainer-outreach.md` to @wimpydwi, if the retainer conversation is still on.
- [ ] **Announce R5's winner** - carried over and still not done. @wimpydwi's clip has been
      paid but never posted on @wavewarz with credit, which the R5 bounty text promised. R7
      should not launch before R5's promise is kept, or the next round's text is writing
      cheques the last one did not cash.

## POIDH creation steps

1. Connect the issuer EOA to poidh.xyz. Switch network to Base before Create.
2. Create bounty. Type: **Open**. Token: ETH. Amount: 0.0128.
3. Title: `Best original clip from the WaveWarZ battle stream`
4. Description: paste `description.md` between the sentinel lines. Keep line breaks.
5. Set the on-chain deadline to whatever date you put in `description.md`, so the two agree.
6. Submit, confirm the tx, copy the bounty URL. Check it appears under
   [poidh.xyz/a/wethemmedia](https://poidh.xyz/a/wethemmedia). Add to the README round index.
7. Cast `promo-cast.md`: @wavewarz and the clippers Telegram FIRST (gate 1), then Farcaster
   /wavewarz and /poidh, X via Firefly, ZAO GCs and Discord.
8. Day 5: reply-cast with submission count and days left, per the playbook's mid-window step.
   Note that by day 7 the launch-week VODs are gone, so the reply-cast should point at the
   current week's.
9. Close, run the consensus vote, accept the claim, post the winner on @wavewarz with credit.

## Files in this folder

- `description.md` - poidh Title + Description, paste-ready between sentinels
- `promo-cast.md` - Farcaster / X / Telegram / Discord launch copy plus a reply-cast
- `retainer-outreach.md` - draft message to @wimpydwi about a paid monthly clipping deal
- `cast-templates/` - catalytic co-funder DM and winner-announce, inherited from the template

## Sources

- R5 (`rounds/r5/README.md`) for the template, the propagation post-mortem, and the locked
  levers. `docs/how-to-draft-next-bounty.md` for the playbook.
- Bounty 1330 state measured 2026-09-05 via `scripts/query-bounty.py`, which merges
  `poidh.xyz/base/bounty/<id>/data` with `claims.fetchBountyClaims` for the real
  `isAccepted` flag. Claim counts for R1/R2/R3 from the same endpoint.
- Twitch GQL 2026-09-05, public web client id, for the VOD list and view counts.
- `wavewarz.info` 2026-09-05 for the battle count (1,371, test battles excluded).
  **Unreconciled:** R5's description said 1,419 battles as of Aug 20, a higher number than
  today's. Different counting, most likely test battles included then and excluded now.
  R7 quotes the site's current figure and its exclusion wording rather than picking between
  them. Worth settling with WaveWarZ before a third round quotes a number at all.
- SOL volume and artist-earnings totals from R5's description are NOT carried over. They
  were "as of Aug 20" and could not be re-measured from `wavewarz.info` this session, which
  serves those figures client-side and exposes no JSON endpoint. **That call turned out to
  be the right one** - see below.

### The artist-earnings figure R5 shipped was right, and dated two weeks early

Measured from per-battle chain data by the wwtracker lane, 2026-09-07. R5's description
said **"13.9 SOL paid straight to artists, as of Aug 20."** On 20 August the artist total
was **13.47**. 13.9 is where it gets to around **5 September**.

The number is defensible under the all-legs reading; the date is not. Anyone checking it
against an August snapshot fails to reproduce it and concludes we invented it. Bounty 1330
is immutable so it cannot be fixed there - the only job is not to inherit it, and R7 does
not, because these figures were dropped rather than carried.

**If R7 quotes an artist figure, use this exact form, legs named:**

> 13.94 SOL to artists, all legs, as of 7 September 2026 - 9.33 from the artist share of
> the trade fee, 4.61 from settlement bonuses.

A bare "13.9 to artists" is what produced three irreconcilable copies of this number across
three documents. **Generate that line, do not copy it** - the string above is right today,
`wavewarz-protocol/tools/artist-earnings.py` is right always, and it labels which legs are
measured versus inherited.

Four more do-not-carry figures from the same pass. **"458 SOL volume as of 2026-05-25" is a
superseded May figure, and its own source already says so** -
`wavewarz/743-wavewarz-whitepaper-v2-deep-dive` carries a numbers warning added 2026-08-09
naming the replacement and recording that a public brand page had already copied it once and
had to be corrected. Use `wavewarz/974-wavewarz-financials-snapshot-2026-07`: 878.316 SOL
volume, 13.3918 SOL artist payouts, validated 2026-07-23. **"2.28% effective fee rate"**
is platform revenue over volume, so it falls as volume rises - it is not a fee rate.
**"1.53% artist payout rate on every trade"** folds in settlement bonuses, which are not
per-trade. And the fee itself, stated correctly because a compressed version of it briefly
got written into our own template as a fourth wrong variant: **the trade fee is 1.500%, it
splits 67/33 artist to platform, so the artist share is 1.005% of volume** - not the 1.00%
the PRD states. Do not say "the trade fee is 1.005%"; that is the artist's share of the fee,
not the fee.

Re-measure before casting regardless. R7 is queued behind R6, so every figure here will be
weeks stale by the time it goes out. The rule now also lives in
`rounds/_template/description.md` so future rounds inherit the caution instead of the number.
