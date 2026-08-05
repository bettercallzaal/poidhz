# R4 closeout - qualifying builder list + open decisions

Bounty 1249 ("ZABAL Gamez Open Pot"). Deadline was Jul 31, 2026; today is Aug 5. Kenny
pinged twice (funded another $25 into the pot, asked if this closes this week). Zaal's
reply to Kenny: making one submit-then-claim, then splitting to everyone who submitted.

This doc is the draft candidate list + the still-open MECHANIC.md decisions that block
actually running the split. Nothing here has been submitted or paid - Zaal confirms the
list and the open decisions, then this becomes the real claim.

## The gap that matters

Bar rule 5 says "submit your claim on this POIDH bounty page." Only 2 POIDH claims
exist on 1249 (both the same wallet, ghostmint.base.eth). But zabalgamez's own
submission board (`/api/submissions?feed=projects`) has 16 unique builders across the
July window. Almost nobody individually claimed on POIDH - which is exactly why Zaal
told Kenny he's making one claim on their behalf rather than waiting for 16 separate
POIDH claims that were never going to come.

## Candidate list (pulled live from zabalgamez `/api/submissions`, 2026-08-05)

### Tier 1 - approved/complete, real demo or repo link (clear qualify)

| Builder | Project | Track | Link |
|---|---|---|---|
| uniquebeing404 | ColorZAO | builder | https://colorzao.signalify.xyz/ (+ repo) |
| Pascaline | ZAO Artist Value Ledger | builder | https://zao-artist-ledger.vercel.app/ (+ repo) |
| breadcoop | Stacks | builder | https://bread.coop/stacks (+ repo) |
| kayonfire | NeonTetris | builder | Farcaster mini app (+ repo) |
| LadyrynNemesis | SURFBOARD | builder | https://surfboard.diyama.online/ |
| mettodo | El Charro | builder | https://txirrin.lovable.app/ |
| taydexfun (Halit Tayyar) | TayDex - creator prediction markets | creator | https://taydex.fun/ |
| ghostmintops (Brandon) | ZABAL Recording Scout (+ more projects) | builder | https://dreamnet-zabal-scout.pages.dev/ |
| branth (Korrocorp) | WaveWarZ Bridge Portal (+ more projects) | builder | https://wavewarz-bridge-portal.vercel.app/ |
| jdwalka (JohnDaWalka) | Chroma Poker (+ more projects) | builder | repo linked, no live demo |

**10 builders.**

### Tier 2 - needs Zaal's call

| Builder | Project | Issue |
|---|---|---|
| Gesd01 | "Blend Music Genres" video | No demo/repo link at all - bar says "linkable." Video claim only. |
| IMan Afrikah | ZABAL Artwork | This is Iman - ZAO core team, not a community builder. Splitting the pot to a cofounder reads differently than to an outside builder. Your call whether he's in. |
| Presdency.eth (HOOD) | status: draft, no links | Real project title but nothing to verify. |
| dee-13 (Ledger) | status: draft | Has a Google Drive link - draft status but a real artifact. |
| Joshua Grubbs / pyrofirezerox (GundariuM) | status: draft | Has BOTH a live demo and a repo - looks shipped, just never flipped to "approved." Probably should count. |

**Excluded:** "Iman QA Test" - literal test data in the feed, not a real submission.

## What's still genuinely blocking the split (from rounds/r4/MECHANIC.md, still unresolved)

These were flagged as open back in June and never locked:

1. **Distributor wallet** - which non-issuer wallet wins the vote and sends the shares? Can't be the BCZ Treasury EOA (PoidhV3 blocks issuer == claimant). Needs to be named and made public per the MECHANIC.md trust-transparency commitment.
2. **Wallet addresses for the Tier 1/2 builders** - none of them are in the submission data (just handles + project links). Either resolve each Farcaster handle to a verified address, or ask each builder directly. Web3.bio lookups were timing out when I tried just now (worth a retry, or use Neynar instead).
3. **Min-builders floor** - not relevant now, 10-15 is a real number, this was for the "what if only 1-2 ship" case.
4. **"Real build" judge** - MECHANIC.md proposed Zaal + one co-host. The Tier 2 list above is exactly that call being made.
5. **Late contributions** - Kenny's $25 landed after Jul 31. Does it fold into this split or carry to R5? Needs a decision either way before the claim amount is finalized.

## Draft claim text (placeholder - do not submit until the list + decisions above are locked)

```
Title: ZABAL Gamez July Open Build - Qualifying Builders

Description:
This claim documents the builders who cleared the bar for the July open build pot -
[FINAL COUNT] wallets, one equal slice each. Full submission board:
https://zabalgamez.com/submissions

[Builder handle] - [project] - [link]
... (one line per confirmed builder)

Per rounds/r4/MECHANIC.md (locked 2026-06-15, Option B): the distributor wallet
[DISTRIBUTOR ADDRESS] wins this vote, withdraws the pot, and sends each builder above
an equal share. Disperse tx hashes posted publicly after the split for transparency.
```

## Next step

Zaal confirms: (a) the Tier 2 calls, (b) the distributor wallet, (c) late-contribution
handling. Then wallets get resolved for the confirmed list, the real claim goes up,
`submitClaimForVote(1249, <claimId>)`, 48h vote, `resolveVote(1249)`, distributor
disperses, tx hashes get posted in the closeout cast.
