# R4 closeout - final resolution (2026-08-05)

Bounty 1249 ("ZABAL Gamez Open Pot"). Deadline was Jul 31, 2026.

## What actually happened

While closing this out, the bounty was accidentally **canceled** (via Farcaster
wallet) instead of withdrawn to submit a split claim - the two actions were
confused because the wallets were linked. This closed off the POIDH claim/vote
path entirely (a canceled bounty can't take new claims).

- **The escrowed 0.0138 ETH has been reclaimed** back to the treasury wallet via
  the cancel-bounty refund path. It is not part of the builder reward - it
  rolls forward, not distributed.
- **Reward mechanism pivoted**: instead of a POIDH-native split, qualifying
  builders get a $ZABAL Empire Builder leaderboard credit - 1 point per wallet,
  uploaded via CSV (`address,score` schema, Empire Builder's CSV Upload
  Leaderboard endpoint). No ETH or USDC changes hands for R4.
- A $100 USDC split was floated and then dropped in favor of the simpler
  1-point-per-wallet leaderboard credit - final call.

## The gap that started this

Bar rule 5 said "submit your claim on this POIDH bounty page." Only 2 POIDH
claims ever existed on 1249 (both the same wallet). zabalgamez's own
submission board had the real activity - this mismatch (individual claims
never came) is why a claim-and-split was attempted manually in the first
place, before the cancel mistake happened.

## Final builder list (15, no tiers)

Resolved live from zabalgamez `/api/submissions` + Farcaster-verified wallets
(via Warpcast's user-by-username API). Full detail with fid/project links in
`rounds/r4/r4-builder-leaderboard.csv`; upload-ready CSV in
`rounds/r4/r4-empire-builder-upload.csv`.

| Handle | Project | Wallet |
|---|---|---|
| uniquebeing404 | ColorZAO | 0xd6B69E58D44e523EB58645F1B78425c96Dfa648C |
| pascaline | ZAO Artist Value Ledger | 0x5Dc697f2799bd232CaD2d479C379fF305b699F9b |
| breadcoop | Stacks | 0x09051AAa3a472A8Bf73B000349fca2073D06fa03 |
| kayonfire | NeonTetris | 0xf109e709B89B820Ac38529bC354aA1f5AFB2f1a1 |
| n3m (LadyrynNemesis) | SURFBOARD | 0xE243c5C876FD259AC41Bf8A15aEF64Cf522fea8f |
| mettodo | El Charro | 0xad7575AEFd4d64520c3269FD24eae1b0E13dbE7B |
| taydexfun (Halit Tayyar) | TayDex | 0x6A5B8AaFEDF836D2883bc5a251b3539F36f35D7B |
| ghostmintops (Brandon) | ZABAL Recording Scout + 5 more | 0x7D79E902482469dA64977d2B0977120C77029593 |
| branth (Korrocorp) | WaveWarZ Bridge Portal + 4 more | 0x258772bbc43845a43df7187f53624605366e0138 |
| jdwalka (JohnDaWalka) | Chroma Poker + 2 more | 0x59223379E56f18Ead2AbDecE93BcfB5c6d6Cf5ae |
| gesd1 | "Blend Music Genres" video | 0x97FdcF12e299031958f9Dd1e9Cc01E1eD73d4180 |
| imanafrikah (IMan Afrikah) | ZABAL Artwork | 0xA0434a9A5403b9E2a197BA1cAe9963406c4f31ac |
| presdency.eth | HOOD | 0x2805E9dBCe2839C5FeAe858723F9499f15fd88CF |
| dee-13 | Ledger | 0x96E9025466a3e15DC2c3B28C1c6C71523a93f703 |
| pyrofirezerox (Joshua Grubbs) | GundariuM | 0x682ebE895E62e046D86cBc1652E61196Dff1f256 |

**Excluded:** the 2 "Iman QA Test" entries on the submission board - literal
test data, not real submissions.

**Note on wallets:** several builders have multiple Farcaster-verified
addresses; the first one returned by Warpcast's API was used as primary.
Not re-verified individually - acceptable for a leaderboard-point credit,
would need double-checking before any real-money send.

## Closed decisions (previously open in MECHANIC.md)

- ~~Distributor wallet~~ - moot. No vote/disperse happens; ZABAL credit goes
  directly to each builder's own wallet.
- ~~Wallet resolution~~ - done, see table above.
- ~~Min-builders floor~~ - moot, 15 real builders shipped.
- ~~"Real build" judge~~ - all Tier-2 judgment calls resolved to include
  (Gesd01, Presdency.eth, dee-13, Joshua Grubbs, Iman all in).
- ~~Late contributions~~ - moot, no ETH pot being split.

## Closeout cast

Draft at `rounds/r4/closeout-cast-draft.md` - tags all 15, explains the
cancel mistake transparently, points to the ZABAL leaderboard credit. Not yet
posted - post after the Empire Builder leaderboard CSV is actually live so
the claim is true when made.
