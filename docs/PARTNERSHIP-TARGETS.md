# POIDH partnership targets - research notes

Research pass on which orgs/communities are realistic candidates for BCZ/The ZAO to
partner with on POIDH-based bounty campaigns (as a P2P ad system, per
[P2P-AD-BOUNTY-KIT.md](P2P-AD-BOUNTY-KIT.md), or as a general community bounty board).
Grounded in verified precedent, not speculation. Live-searched 2026-08-06 - dates and
figures below are current as of that search; re-verify before acting on anything time-sensitive.

## Confirmed precedent (POIDH already has cross-community traction)

- **POIDH x SheFi** - POIDH ran a bounty specifically for the SheFi community, judged by
  POIDH's own "Jessebot" AI, timed to a SheFi AMA. This is the clearest existing proof
  that POIDH already partners across community lines, not just within its own Farcaster
  base. SheFi (women-in-crypto education community) is a plausible direct follow-up
  partner for BCZ - similar audience-growth goals, and POIDH has already broken the ice
  with them once.
- **POIDH is now explicitly AI-agent compatible** (per POIDH's own 2026 feature set) -
  agents can propose bounties and select claims while a human retains verification
  control, and the protocol is deployed across Arbitrum, Base, and Degen Chain. This
  matters for ZAO specifically: ZOL/ZOE-adjacent tooling could eventually *propose*
  bounties on behalf of BCZ (not just draft casts, per ZAO OS V1 doc 2213), with a human
  still gating the actual on-chain accept - the same "AI proposes, human approves" pattern
  already validated for social posting applies here too.
- **Degen Chain is a first-class POIDH deployment**, not an afterthought - `zpoidh`'s own
  `CHAIN_TOKENS` mapping already prices DEGEN natively (`scripts/build-bounty-dashboard.py`).
  The Degen community (a Farcaster-native tipping/rewards culture with its own token) is
  a low-friction target: they already understand token-incentivized public tasks, and a
  Degen-denominated bounty removes the "convert to ETH" friction BCZ hits with every round
  (see `docs/how-to-draft-next-bounty.md`'s "POIDH does not support USDC" gotcha - Degen
  sidesteps needing ETH conversion entirely for a Degen-native audience).

## New candidate targets found this pass

- **Purple DAO** - a Farcaster-native DAO whose explicit mission is proliferating the
  Farcaster protocol/ecosystem. Funds small grants via Rounds.wtf and larger on-chain
  proposals, built on Nouns Builder, running daily auctions on Base for 500+ days.
  Fit: Purple already pays to grow Farcaster - a POIDH ad-bounty campaign that grows
  Farcaster channel engagement (e.g. "best ad that gets people to follow /zabal" or a
  joint /zabal x /purple cross-promotion bounty) is directly inside their funding thesis,
  not an ask for charity.
- **Yellow Collective** - a Nouns-Builder-based DAO on Base supporting artists. Fit: this
  is the closest existing match to ZABAL Gamez's "artist" track (one of the three ZABAL
  Gamez tracks per `rounds/r3/description.md`) - a natural co-bounty target for an
  artist-specific P2P ad round, or a cross-pollination bounty that pulls Yellow Collective
  artists into a ZABAL Gamez round and vice versa.
- **The broader Nouns Builder DAO ecosystem** (200+ collectives launched on this infra
  across Ethereum/Optimism/Base/Zora) - a long tail worth scanning individually rather
  than pitching en masse. Each runs its own daily/periodic auction and likely has its own
  small treasury that could co-fund an OPEN POIDH bounty the same way BCZ's own catalytic-DM
  pattern works internally (`docs/how-to-draft-next-bounty.md` step 7).
- **Bountycaster** - not a partner-org exactly, but a complementary distribution surface:
  a Farcaster-native bounty board/aggregator (posted via tagging `@bountybot`), reporting
  $1.5M across ~2,967 bounties as of this search, explicitly no-fee peer-to-peer, and using
  Ethereum Attestation Service (EAS) for onchain completion attestations. Worth
  investigating whether a POIDH bounty can be cross-posted/mirrored to Bountycaster for
  free extra discovery surface - this is a tooling question (does Bountycaster support
  POIDH-originated bounties, or only its own bounty type), not a relationship-building one,
  so it's a fast thing to check before the org-outreach items below.

## Suggested next actions (research-informed, not yet committed to)

| Target | Action | Effort | Notes |
|---|---|---|---|
| SheFi | DM asking if they'd co-run or cross-post a ZABAL Gamez artist/creator round | Low (1 DM) | Precedent already exists via POIDH x SheFi/Jessebot - warm intro angle: "saw POIDH already ran a bounty for you all" |
| Purple DAO | Pitch a joint /zabal x /purple cross-promo bounty, framed as Farcaster-growth (their stated funding thesis) | Medium (needs a bounty description, not just a DM) | Use the P2P Ad Bounty Kit template directly - this is exactly the use case it's built for |
| Yellow Collective | Cross-pollination bounty targeting their artist base for the ZABAL Gamez artist track | Medium | Natural fit given the shared "artist track" framing |
| Bountycaster | Check whether POIDH bounties can cross-post/mirror there | Low (research/test, no relationship needed) | Do this first - it's free extra reach if it works, independent of any org outreach |
| Degen community | Run (or convert) a bounty denominated in DEGEN instead of ETH | Medium (needs a Degen-chain-specific description + confirming DEGEN prize UX on POIDH) | Removes the ETH-conversion friction noted in `docs/how-to-draft-next-bounty.md` |

None of these are commitments - they're researched, precedent-grounded leads for Zaal to
decide on. Every "Action" above assumes the P2P Ad Bounty Kit structure
(`docs/P2P-AD-BOUNTY-KIT.md`) as the actual bounty format, since that's the proven
mechanism, not a new pitch to invent per partner.

## Sources

- [pics or it didn't happen | Gitcoin](https://gitcoin.co/apps/poidh) - POIDH protocol overview, AI-agent compatibility, multi-chain deployment
- [pics or it didn't happen (@poidhxyz) / Posts / X](https://x.com/poidhxyz) - POIDH x SheFi/Jessebot bounty
- [Bountycaster](https://www.bountycaster.xyz/) - Bountycaster platform, fee structure, EAS attestations
- [Bountycaster: Project Guide | Bitget](https://web3.bitget.com/dapp/bountycaster-28503) - Bountycaster figures ($1.5M / ~2,967 bounties)
- [Reflections on Purple - Phil Mohun](https://www.philmohun.com/purple-reflections/amp/) - Purple DAO mission, Rounds.wtf grants, Base auction history
- [Web3 Galaxy Brain - Purple, the Farcaster DAO](https://web3galaxybrain.com/episode/Purple-the-Farcaster-DAO) - Purple DAO background
- [Nouns Builder | Purple](https://nouns.build/dao/base/0x8de71d80eE2C4700bC9D4F8031a2504Ca93f7088/507) - Purple's Nouns Builder deployment
- [ournetwork issue 188](https://ournetwork.substack.com/p/ournetwork-issue-188) - Nouns Builder ecosystem scale (200+ collectives), Yellow Collective

## Also see

- [P2P-AD-BOUNTY-KIT.md](P2P-AD-BOUNTY-KIT.md) - the bounty structure to use for any of the above
- [PARTNER-GUIDE.md](PARTNER-GUIDE.md) - if a partner org wants their own forked instance of this tooling rather than a joint bounty
