# R5 - WaveWarZ Twitch clip bounty

Fifth cast round (the Unlock and bug-fix drafts that held R5-R7 numbers were never cast and now live in rounds/drafts/). Entrants go through the WaveWarZ Twitch archive and cut the best
20 to 90 second moment. The winning clip is for WaveWarZ's OWN social channels, not the entrant's.

Card `769a4a6b` ("Launch WaveWarZ clip bounty - set prize + deadline, create/fund on POIDH, clipboard
wavewarz-clip-bounty"). Template: R1 / doc 533 (bounty 1151), the proven single-judge clip-up shape.

## At a glance

- **Source:** [twitch.tv/wavewarzofficial/videos](https://www.twitch.tv/wavewarzofficial/videos). Verified 2026-08-20 via Twitch GQL: channel id 1329490346, "WaveWarZOfficial", 39 followers, 6 archive VODs titled "WaveWarZ Song vs. Song BattleZ" (Aug 13 to Aug 20, 1.9h to 3h each), 0 highlights, a handful of viewer clips.
- **Format:** 20 to 90 second clip, battle audio kept, posted to either X / Instagram / TikTok / YouTube, then claimed on poidh with the post link. Poidh claim is the entry (doc 2308 one-surface rule).
- **Deadline:** 11:59 pm PT Sunday, August 30, 2026 (10-day window, locked by Zaal).
- **Winner:** poidh consensus (contributor-weighted vote on the OPEN pot). Zaal chose OPEN over single-judge on 2026-08-20.
- **Chain / type:** Base, OPEN bounty (anyone can top up). Album poidh.xyz/a/thezao.
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
- [ ] **Post** promo-cast.md with the live URL.
- [ ] Kenny DM (kenny-poidhz-combined) - held for tomorrow per Zaal.

## POIDH creation steps

1. Wallet: connect the issuer EOA to poidh.xyz. Switch network to Base before Create.
2. Create bounty. Type: **Open**. Token: ETH. Amount: 0.0128 (0.0125 seed x 1.025).
3. Title: `Best 60s clip from the WaveWarZ Twitch stream`
4. Description: paste `description.md` between the sentinel lines. Poidh renders plain text; keep line breaks.
5. Submit, confirm the tx, copy the bounty URL.
6. Check it shows under poidh.xyz/a/thezao. Add to the README round index.
7. Cast: Farcaster long version in /wavewarz and /poidh, X short version via Firefly, Telegram version in the Clippers group and ZAO GCs.
8. Day 3 or 4: reply-cast (VODs rolling off). Day 7: close. Pick winner within 48h, accept claim on poidh, post the clip on @wavewarz with the entrant credited.

## Files in this folder

- `description.md` - poidh Title + Description, paste-ready
- `promo-cast.md` - Farcaster / X / Telegram launch copy + a reply-cast

## Sources

- Doc 533 / rounds/r1 (bounty 1151 wording and lessons), doc 625 (playbook, tiers, solo vs open), doc 768 (R3 best practices, audio rule, title pattern), doc 415 (WaveWarZ bounty templates), doc 2308 (weekly spec, claim-is-entry rule), doc 1223 + 1293 (WaveWarZ channels + Clippers program), doc 743 (locked WaveWarZ facts: 979 battles, 458 SOL volume, 7.76 SOL to artists, as of 2026-05-25).
- Twitch GQL lookups 2026-08-20 (public web client id) for channel status, VOD list, affiliate flag.
- ETH spot: Coinbase API, 2026-08-20, $2,328.
