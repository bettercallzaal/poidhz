# R6 - WaveWarZ clip round 2 (DRAFT, not cast)

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
into the Clippers group at [t.me/wavewarzclipshq](https://t.me/wavewarzclipshq), where the
people who clip this stream for points already are. It went out from Zaal's personal
account, Iman's, and @TheZAODAO. So R5 got nine claims while never reaching its own
audience. That is R6's single biggest lever and it costs nothing, which is why it is
gate 1 below and not a step 7 afterthought.

Winner: claim 7795, accepted on-chain, 0.0238 ETH to
`0x3f07d412da0aa3615bd92a496c73823a64370ec9`. The clip is
[@wimpydwi's](https://x.com/wimpydwi/status/2094135544758608181), JOHN 3v16 by
@LadyrynNemesis vs THE SUMO WRESLER by @The7_is_a_T.

## What is different from R5, and why

1. **The ask moved from finding to making.** R5 said cut the best existing moment. R6 says
   take a moment and give it a treatment nobody has tried on this stream. Zaal's call,
   2026-09-05: "be more specific that the goal is to capture a moment and try something
   new so that we can use that." This changes what wins, so the description's ranking is
   explicit: treatment first, moment second, craft third. R5 ranked moment first.
2. **The deliverable spec is binding.** R5 said "vertical is welcome, not required" and
   left captions and logo in the rubric as bonuses. R6 makes vertical 9:16, burned-in
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
  VOD dies - what R6 ships, same as R5, with the warning stated in days rather than implied.

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
- **Window:** 14 days. Recommended cast Monday 2026-09-07, close 11:59 pm PT Sunday
  2026-09-20. Both weekdays verified. Sunday close matches R1-R3 and R5.
- **Winner:** poidh consensus, contributor-weighted vote on the OPEN pot. Same as R5, which
  was a deliberate override of R1-R3's single-judge template.

## Set the on-chain deadline to match the stated one

R5's description said Aug 30 while the on-chain `deadline` field read 2026-09-05 00:21 UTC,
six days later. The field is set at creation and does not track the text - every prior round
shows the same drift (R1 14.1d, R2 20.1d, R3 19.8d between `createdAt` and `deadline`). It
did no harm in R5 because the winner was accepted by hand, but it means any tool reading the
chain gets a different close date than any human reading the bounty. Set them to agree.

## Validator status, and what its PASS does not mean

`python3 scripts/validate-bounty-description.py --description rounds/r6/description.md`
returns PASS. Two things to know before trusting that:

- **R5 fails the same validator** on four sections, and R5 drew nine claims. The validator
  encodes the R3-era template (`THE BAR` / `THE RUBRIC` / `THE ASSET KIT` / `THE REWARD`),
  which R5 deliberately walked away from in favour of a plainer voice. R6 keeps R5's voice
  and restores the canonical headers, so it satisfies both. Do not read R5's FAIL as a defect.
- **The section check is a literal header-name match.** It reads nothing inside the section.
  In particular `THE REWARD` is labelled "prize + winner-cast distribution + EB ZABAL trail"
  and passes on the header alone - R6's reward section has **no Empire Builder $ZABAL trail**,
  because R5 omitted that mechanic and inventing reward terms is Zaal's call, not a drafting
  decision. If the $ZABAL trail should be in this round, it has to be added by hand; the
  green verdict will not tell you it is missing.

The two remaining WARNs are both expected: no poidh URL yet (added after creation) and no
GitHub brand-kit link (there is no WaveWarZ brand kit - see below).

## No WaveWarZ brand kit exists

`assets/brand-kits/` contains only `zabal-games`, and `bettercallzaal.com/assets/wavewarz/`
404s. R5's "DM @bettercallzaal for the logo files" was the only route to the mark.

This mattered more in R6 than in R5, because R6 promotes the visible mark from a rubric bonus
to a floor rule - which would have put a hard requirement behind a DM. Rule 3 is written as
"@wavewarz **or** the logo", and now says outright that typing the handle on screen satisfies
it, so no entrant is blocked on artwork they cannot get. Building a real WaveWarZ kit is worth
doing before a third round, and is the natural companion to the Hurric4n3IKE conversation.

## Every bettercallzaal.com/poidh* link in this repo is dead

Measured 2026-09-05. `bettercallzaal.com/poidh-bounty-best-practices.html`,
`/poidh.html` and `/poidh-round<N>-judging.html` all return 200 only after redirecting to
`https://github.com/bettercallzaal/poidhz`. The pages still exist as `docs/*.html` in this
repo, but nothing serves them: GitHub Pages 404s, `poidhz.vercel.app` 404s at those paths,
and `poidhz.xyz` / `poidhz.com` do not resolve at all - the domain purchase flagged as
outstanding in the 2026-08-21 handoff is still outstanding.

This is entrant-facing, not cosmetic. The `_template` description tells every future round
to cite the canonical bar, which now drops a clipper on a GitHub repo page. The same dead
URL is cited in `README.md`, `docs/how-to-draft-next-bounty.md`, `rounds/r3/`, and both
`_template` cast files. R6 cites the repo directly instead, which works today.

Two notes for whoever fixes this properly: the repo has been **renamed to `poidhz`** (the
push to `zpoidh` redirects, and the remote now answers as `bettercallzaal/poidhz`), and the
`_template` winner-announce copy promises every submitter a $ZABAL airdrop and links a
per-round judging page - neither of which existed for R5. Do not paste that template
without checking both claims against the round it is describing.

## Zaal gates (money, public, outbound)

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
      paid but never posted on @wavewarz with credit, which the R5 bounty text promised. R6
      should not launch before R5's promise is kept, or the next round's text is writing
      cheques the last one did not cash.

## POIDH creation steps

1. Connect the issuer EOA to poidh.xyz. Switch network to Base before Create.
2. Create bounty. Type: **Open**. Token: ETH. Amount: 0.0128.
3. Title: `Best original clip from the WaveWarZ battle stream`
4. Description: paste `description.md` between the sentinel lines. Keep line breaks.
5. Set the deadline to 2026-09-20, matching the description.
6. Submit, confirm the tx, copy the bounty URL. Check it appears under
   [poidh.xyz/a/wethemmedia](https://poidh.xyz/a/wethemmedia). Add to the README round index.
7. Cast `promo-cast.md`: @wavewarz and the Clippers group FIRST (gate 1), then Farcaster
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
  R6 quotes the site's current figure and its exclusion wording rather than picking between
  them. Worth settling with WaveWarZ before a third round quotes a number at all.
- SOL volume and artist-earnings totals from R5's description are NOT carried over. They
  were "as of Aug 20" and could not be re-measured from `wavewarz.info` this session, which
  serves those figures client-side and exposes no JSON endpoint. Refresh them from WaveWarZ
  directly before casting if you want them in the text.
