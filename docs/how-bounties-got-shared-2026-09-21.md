# How other poidh bounties got shared out

**Measured 2026-09-21, 08:4x EDT.** Asked by Zaal the morning bounty one was live: "lets just
research other ways poidh bounties were shared out".

**The short answer is that the question could not be answered as asked, and something more
useful came out instead.** How an issuer *promoted* a bounty lives in Farcaster and X, and
reading either needs API keys this lane was denied (see Limits). What the poidh platform itself
records is how each bounty was *set up* - its ask, its type, who funded it - and how many
entries it drew. So this is about set-up, not promotion.

## Method, first

- **Population:** `bounties.fetchAll` with `status: past`, `chainId: 8453`, 12 pages of 50.
  The **most recent 600 completed bounties on Base**, created 2025-07-15 to 2026-09-18, from
  **179 distinct issuers**.
- **Entry counts:** `claims.fetchBountyClaims` per bounty, because `fetchAll` returns only a
  `hasClaims` boolean.
- **Positive controls, run before any other number was trusted:** the counter returned
  **R1 (bounty 1151) = 11** and **R5 (bounty 1330) = 9**, both known independently. A counter
  that has never been seen returning a known answer is not a counter; this repo once read
  `fetchByAlbum`'s empty claims arrays as "zero claims across 15 bounties".
- **Reproduce:** `python3 scripts/pull-past-bounty-claims.py`. It refuses to run past a failed
  control. The slim data is committed at `data/past-bounties-2026-09-21.json`.

## Limits - read these before the findings

These are written here word for word as the lane lead asked, because each one changes what a
finding is allowed to claim.

- **Survivors only.** `status: past` means completed bounties, so every one of them had
  entries - 600 of 600. That is the sample's definition, not a result. Nothing here says
  anything about bounties that drew no one.
- **No promotion data.** How issuers shared their bounties - casts, channels, reposts - is not
  in this data. Reading Farcaster or X needs API keys, and reading `~/.zao/zao.env` was denied
  in this session. Every finding below is about how a bounty was *set up*.
- **n=10 for finding b.** Too few to call it proven.
- **n=1 for finding d.** An idea, not evidence.
- **The page cap binds.** 12 pages stopped at 600 with more available. This is the most recent
  slice, not the whole history.

Across the sample: median **3** entries, mean **7.7**, max **100**. The top of the list is
dominated by trivially easy photo asks ("take a pic of something green", "upload a pic, any
pic") - which is why the easy-photo confound is controlled for below.

## Findings

### a. Bounties someone else added money to drew about three times the entries

Among the 552 OPEN bounties:

| | n | Median entries | Share reaching 10+ |
|---|---|---|---|
| Boosted by someone other than the issuer | 270 | **5.5** | **35%** |
| Not boosted | 282 | 1.5 | 17% |

The largest sample in this doc and the strongest signal. **But the direction is not known.**
People may boost bounties they can already see doing well, rather than the boost causing the
entries. This data has no timestamps for contributions against claims, so it cannot separate
the two.

**Bounty one is already boosted** - Kenny, confirmed in his DM to Zaal ("boosting and will
promo on X in the morning!", 2026-09-20 11:21 PM) and on chain as the second contributor.

### b. Naming ONE room for the entry to be posted in

Bounties whose ask said, in effect, "post your entry in this one place":

| | n | Median entries | Share reaching 10+ |
|---|---|---|---|
| Names a room | **10** | **11.5** | 50% |
| Does not | 590 | 3 | 25% |
| *Non-photo asks only:* names a room | 8 | 11.5 | 50% |
| *Non-photo asks only:* does not | 394 | 2 | 22% |

It survives removing the easy-photo asks. The mechanism is plausible: each entry becomes a
public post in one place, the place fills up, and the people in it see the bounty working.
Examples read by hand:

- #1243, 61 entries: "post a photo of your viewing setup in the /football channel on farcaster"
- #569, 61: "Post anything about Inflynce on the /inflynce channel"
- #1170, 43: "post your sunrise / sunset photo on Fotocaster - share the link to it on Farcaster"

**n=10, so this is suggestive, not proven.** A looser test - any `/channel` mention at all -
finds 14 of 600, median 9 against 3. **Almost nobody on the platform does this**, which is
either why it works or why there are too few cases to know.

### c. Asking for a link back to your post does nothing

| | n | Share reaching 10+ |
|---|---|---|
| Asks for a link to your cast or post | 76 | 24% |
| Does not | 524 | 26% |

A useful null. If finding b is real, it is the *room* that matters, not the link.

### d. Inverting the ask

"Create the worst ad for Hivemind ever" (#996) drew **66 entries**, 6th in the whole sample - a
brand paying for ads, which is the closest thing on the platform to what we are doing. Asking
for the *worst* version removes the fear of not being good enough. **n=1**: the only other
"worst" match (#328) is a false positive, a technical measurement. An idea, not evidence.

## What was done with it

- **Today (bounty one):** the description is immutable, so finding b can only reach it through
  the copy. The 2pm reminder adds "drop yours in /zao so everyone can see them" - a free test.
  Approved by the zaoonparagraph lane, which leads today; Zaal posts it.
- **Day 2:** a one-named-room variant is drafted and marked as **Zaal's call** - see
  `rounds/daily/d02-room-variant/`. It carries a real trade-off: a Farcaster room excludes the
  Maine audience that is not on Farcaster, which is the audience the festival needs most.
- **Kenny** was asked how the Hivemind bounty was pushed, since he sees more bounties than
  anyone and that is the promotion data this doc could not reach.
