# R5 - WaveWarZ Twitch clip bounty

> **CLOSED AND PAID 2026-09-05. THE WINNER HAS STILL NOT BEEN ANNOUNCED.**
>
> Claim 7795, 0.0238 ETH, paid to `0x3f07d412da0aa3615bd92a496c73823a64370ec9`. The clip is
> [@wimpydwi's](https://x.com/wimpydwi/status/2094135544758608181). 9 claims from 7 entrants.
>
> **The bounty text promised the clip would go up on @wavewarz with the entrant's name on
> it. It has not.** Copy is written and unsent at [`winner-announce.md`](winner-announce.md);
> Zaal is posting it himself. Everything below describing this round as running is history.
>
> This banner exists because the status lines further down read "LIVE" before they read
> "CLOSED", and a record that stays loud after it stops being true is as dangerous as an
> alarm that goes quiet when things break. Corrections belong where the file is read.

Fifth cast round (the Unlock and bug-fix drafts that held R5-R7 numbers were never cast and now live in rounds/drafts/). Entrants go through the WaveWarZ Twitch archive and cut the best
20 to 90 second moment. The winning clip is for WaveWarZ's OWN social channels, not the entrant's.

Card `769a4a6b` ("Launch WaveWarZ clip bounty - set prize + deadline, create/fund on POIDH, clipboard
wavewarz-clip-bounty"). Template: R1 / doc 533 (bounty 1151), the proven single-judge clip-up shape.

## At a glance

- **Source:** [twitch.tv/wavewarzofficial/videos](https://www.twitch.tv/wavewarzofficial/videos). Verified 2026-08-20 via Twitch GQL: channel id 1329490346, "WaveWarZOfficial", 39 followers, 6 archive VODs titled "WaveWarZ Song vs. Song BattleZ" (Aug 13 to Aug 20, 1.9h to 3h each), 0 highlights, a handful of viewer clips.
- **Format:** 20 to 90 second clip, battle audio kept, posted to either X / Instagram / TikTok / YouTube, then claimed on poidh with the post link. Poidh claim is the entry (doc 2308 one-surface rule).
- **Deadline:** 11:59 pm PT Sunday, August 30, 2026 (10-day window, locked by Zaal).
- **Winner:** poidh consensus (contributor-weighted vote on the OPEN pot). Zaal chose OPEN over single-judge on 2026-08-20.
- **Chain / type:** Base, OPEN bounty (anyone can top up). Album `wethemmedia` (continuity with R1-R3, per the locked playbook in the repo README) - live at [poidh.xyz/a/wethemmedia](https://poidh.xyz/a/wethemmedia). This doc originally said `thezao`, which was wrong; the bounty was created against the correct album.
- **Issuer:** the EOA Zaal connects (BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af` per docs/how-to-draft-next-bounty.md). Must be an EOA, not a smart wallet.
- **Reward:** recommendation below. One winner takes the pot.

## Prize: 0.0125 ETH seed, locked by Zaal 2026-08-20 (recommendation had been 0.02)

| Round | Ask | Prize | Outcome |
|---|---|---|---|
| R1 (1151) | clip-up, one 30-min episode, post to own channel | 0.0105 ETH (~$24) | 1 strong claim, paid |
| R2 (1166) | 60s ad from one episode | 0.0105 ETH (~$24) | paid, duration-cap dispute |
| R3 (1180) | full ad, any format | 0.025 ETH (~$58) | paid, best craft of the series |

This ask sits between R1 and R3: harder than R1 (hours of VOD to scan, not one link, and we keep the
output), lighter than R3 (no asset production). Doc 625's tier table puts creative clip output at
0.01 to 0.03 ETH. 0.02 ETH is the midpoint and is about 2x what R1 paid for a clip we did not even
get to reuse. Fund 0.0205 ETH so the 2.5% protocol fee does not eat the headline number.

Cheaper option: 0.0125 ETH (repo default, ~$29). Richer option if Zaal wants to signal this is the
first of a series: 0.03 ETH (~$70). Prize is Zaal's call.

## What is different from R1 (and why the text reads the way it does)

1. **Source is a rolling Twitch archive, not one link.** The channel is not Twitch Affiliate or
   Partner, so VODs auto-delete after 7 days. Oldest VOD today is Aug 13, which matches. A 7-day
   bounty therefore points at a window that keeps moving: nights 1 to 3 roll off before the
   deadline while new nights land. The text says so plainly, tells people to clip early, and
   points at Twitch's native Clip button (clips persist after the VOD is gone, 60s max).
2. **Narrow prompt.** Brief flagged that "go through the archive" produces unfocused entries. The
   "what wins" paragraph borrows WaveWarZ's own Clippers Tier A list (doc 1293): battle climax +
   flip, payout reaction, one-breath explainer line.
3. **Rights.** R1 asked people to post to their own channels. This asks for a clip WE repost, so the
   text carries a plain grant ("by entering you are saying WaveWarZ and The ZAO can repost your
   clip ... we credit your handle every time") and keeps ownership with the entrant. Battle music
   belongs to the artists, so entrants must name the artists in the post. This is
   `credit-attribution.md` applied: visible credit on every published surface.
4. **Meshes with the existing Clippers program.** WaveWarZ already runs a points-based clippers
   group at t.me/wavewarzclipshq (docs 1223, 1293). The bounty tells clippers to submit both
   places rather than competing with that program.
5. **Tags.** @wavewarz (confirmed X + YouTube handle, doc 1223) and @bettercallzaal. Not @thezao.

## Zaal gates (money, public, outbound)

- [x] **Confirm scope:** source channel is `twitch.tv/wavewarzofficial` (the only channel with WaveWarZ battle VODs; `twitch.tv/bettercallzaal` carries ZM / Artizen streams, not battles). All VODs in the 7-day window are in scope, plus live.
- [ ] **Confirm with Hurric4n3IKE** - held by Zaal 2026-08-21 (not sent yet; will capture VODs himself soon). Clip-upload toggle (Settings > Stream > Clips > "Let viewers upload clips to their socials") confirmed ON via screenshot 2026-08-21.
- [x] **Standing hold check:** confirmed does not extend to this one-off.
- [x] **Set prize** 0.0125 ETH, funded 0.0128 ETH (fee-adjusted) to the issuer EOA.
- [x] **Create the bounty** - LIVE: [poidh.xyz/base/bounty/1330](https://poidh.xyz/base/bounty/1330), 2026-08-21.
- [x] **Post** promo-cast.md with the live URL. **PARTIAL, and this is the R5 problem.** It went out 2026-08-21 12:36 PT from Zaal's personal X ([@bettercallzaal](https://x.com/bettercallzaal/status/2090749876950691917)) and from Iman's personal account. Verified by eye 2026-08-22. It has **never** gone out from [@wavewarz](https://x.com/wavewarz) (verified, and the audience that actually watches the stream; handle confirmed in doc 1223), or into the WaveWarZ clippers group at [t.me/wavewarzclipshq](https://t.me/wavewarzclipshq) where the clippers named in docs 1223 / 1293 already are. Result after 27 hours: **147 views, 0 claims.** The pot moved 0.0128 to 0.0238 ETH, so someone in Zaal's own network topped it up, which is reach among peers and not among clippers. The bounty text promises "the clip runs on WaveWarZ official channels" while never having been announced on one. Owner-account propagation is Zaal's call, so this is flagged, not actioned.
- [x] **ZAO amplification** - posted from @TheZAODAO on X 2026-08-22 by Iman, under the standing rule that ZAO account posting continues unless Zaal says otherwise. This is the first owner-account reach R5 has had. @wavewarz and t.me/wavewarzclipshq remain unreached and remain Zaal's to run.
- [ ] Kenny DM (kenny-poidhz-combined) - held for tomorrow per Zaal.

## POIDH creation steps

1. Wallet: connect the issuer EOA to poidh.xyz. Switch network to Base before Create.
2. Create bounty. Type: **Open**. Token: ETH. Amount: 0.0128 (0.0125 seed x 1.025).
3. Title: `Best 60s clip from the WaveWarZ Twitch stream`
4. Description: paste `description.md` between the sentinel lines. Poidh renders plain text; keep line breaks.
5. Submit, confirm the tx, copy the bounty URL.
6. Check it shows under poidh.xyz/a/wethemmedia. Add to the README round index.
7. Cast: Farcaster long version in /wavewarz and /poidh, X short version via Firefly, Telegram version in the Clippers group and ZAO GCs, plus X/Farcaster DM group chats and Discord.
8. Day 3 or 4: reply-cast (VODs rolling off). Day 7: close. Pick winner within 48h, accept claim on poidh, post the clip on @wavewarz with the entrant credited.

**Status 2026-08-21 - SUPERSEDED, kept as the record of what was true that day:** LIVE at [poidh.xyz/base/bounty/1330](https://poidh.xyz/base/bounty/1330). Steps 1-6 done. Step 7 (propagation) staged in clipboard `wavewarz-r5-propagate-all` - Farcaster main, X main, X GC, Farcaster /zao GC, Telegram, Discord, all six ready to post.

**Status 2026-09-05: CLOSED AND PAID, WINNER NEVER ANNOUNCED.**

Claim **7795** accepted on-chain, **0.0238 ETH** paid to
`0x3f07d412da0aa3615bd92a496c73823a64370ec9`. Winning clip is
[@wimpydwi's](https://x.com/wimpydwi/status/2094135544758608181): JOHN 3v16 by
@LadyrynNemesis vs THE SUMO WRESLER by @The7_is_a_T. Final field **9 claims from 7 distinct
entrants** (coolhat and one unlinked wallet filed twice each). Accepted outside a tracked
session between 09-03 and 09-05. Verify with `python3 scripts/query-bounty.py --bounty 1330`.

Two things this closes out, and one it does not:

- The "low turnout" reading of this round was wrong. Nine claims sits between R2/R3's eight
  and R1's eleven. The round was under-distributed, not under-subscribed - see the 2026-08-22
  entry in `docs/RECAP.md`.
- The pot grew 0.0128 to 0.0238 with no catalytic DM campaign run at all.
- **Still open: the winner has been paid but never announced.** Nothing has gone out on
  @wavewarz crediting @wimpydwi, which this bounty's own text promised ("the clip goes up on
  @wavewarz with your name on it"). Copy is drafted and unsent in
  [`winner-announce.md`](winner-announce.md). Do not paste the `_template` version - it
  promises a $ZABAL airdrop this round never offered and links a judging page that does not
  exist.

The payee wallet resolves to no Farcaster, X or ENS identity on web3.bio. The claim carried
@wimpydwi's X link, so the pot was released on a reasonable judgment call, but nothing
on-chain ties the address to the handle. R6 fixes the general case by requiring the handle
in the claim text.

## Files in this folder

- `description.md` - poidh Title + Description, paste-ready
- `promo-cast.md` - Farcaster / X / Telegram launch copy + a reply-cast

## Sources

- `community/533-poidh-clipup-bounty-bcz-yapz-hannah` and rounds/r1 - bounty 1151 wording and lessons
- `community/625-poidh-zao-bounty-playbook` - playbook, tiers, solo vs open
- `business/768-poidh-bounty-best-practices-zabalgames-r3` - R3 best practices, audio rule, title pattern
- `community/415-poidh-bounties-zao-wavewarz` - WaveWarZ bounty templates. **Note 415 is ambiguous** - it also names `dev-workflows/415-composio-agent-orchestrator` and `infrastructure/415-composable-os-architecture`.
- `community/2308-poidh-weekly-zao-video-competition-spec` - weekly spec, claim-is-entry rule
- `wavewarz/1223-wavewarz-live-programming-community-jul2026` and `wavewarz/1293-wavewarz-clippers-program-guide-jul2026` - WaveWarZ channels and the clippers Telegram. Note there is no formal points programme; see the correction in rounds/r7.
- `wavewarz/743-wavewarz-whitepaper-v2-deep-dive` - "979 battles, 458 SOL volume, 7.76 SOL to artists, as of 2026-05-25". **Do not carry those forward.** They are superseded May figures, and that doc has said so at the top since 2026-08-09: it holds two conflicting sets of headline numbers, names `wavewarz/974-wavewarz-financials-snapshot-2026-07` as the one to use, and records that a public brand page copied the old ones once already and had to be corrected. Current, validated 2026-07-23: **878.316 SOL volume, 13.3918 SOL artist payouts.** Note `743` is also ambiguous, naming `business/743-agentic-cold-outreach-workflow`.
- Twitch GQL lookups 2026-08-20 (public web client id) for channel status, VOD list, affiliate flag.
- ETH spot: Coinbase API, 2026-08-20, $2,328.
