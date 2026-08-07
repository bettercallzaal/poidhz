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
- **Degen Chain is a first-class POIDH deployment, confirmed with a live example, not
  just a claim.** Queried POIDH's own tRPC feed directly (`bounties.fetchAll` with
  `chainId: 666666666`) and found a real, currently-open bounty on Degen Chain: id 1393
  ("Closest to Zero"), 13,014 DEGEN, `onChainId` 196. This is the same live number
  `scripts/build-bounty-dashboard.py`'s own inline comment references as a real example it
  had to handle correctly (its `CHAIN_TOKENS` mapping already prices DEGEN natively, for
  exactly this reason). So the "run a Degen-denominated bounty" idea below is genuinely
  possible on POIDH - it isn't hypothetical.

  **But a real gap exists between "POIDH supports it" and "zpoidh's own tooling supports
  it."** `docs/create-bounty.html` (this repo's standalone bounty-creation page) hardcodes
  Base mainnet only (`BASE_HEX = '0x2105'`) and the single POIDH contract address used on
  Base/Arbitrum (`0x5555fa78...`) - it has no Degen Chain option and no Degen contract
  address wired in. Creating a Degen bounty today means going directly to
  `poidh.xyz/degen` (POIDH's own frontend), not zpoidh's tool.

  Deliberately did NOT add Degen support to `create-bounty.html` to close this gap -
  `create-bounty.html` signs real transactions with the connected wallet, and the Degen
  Chain contract's exact address could not be confirmed from a source reliable enough to
  hardcode into transaction-signing code. It's an unverified contract on Degen Chain's
  block explorer (Blockscout) - no published source, no confirmed constructor args
  distinguishing the NFT contract from the bounty-logic contract. Guessing a contract
  address for a page that locks real funds is exactly the kind of shortcut this repo has
  avoided all session. If someone wants to add real Degen support to `create-bounty.html`
  later, get the verified address from POIDH's own team/docs first, not from block-explorer
  archaeology.

  The Degen community (a Farcaster-native tipping/rewards culture with its own token) is
  still a low-friction partnership target for the reasons below - they already understand
  token-incentivized public tasks - but today that means pointing them at `poidh.xyz/degen`
  directly, not zpoidh's own bounty-creation tool.

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
  Ethereum Attestation Service (EAS) for onchain completion attestations.

  **Cross-posting feasibility - answered.** Checked Bountycaster's own FAQ directly. There
  is no native mirroring/import mechanism for bounties created on another protocol - it
  isn't mentioned anywhere in their docs, and Bountycaster is architecturally its own
  standalone system. But the mechanism it actually uses turns out to make a manual
  workaround realistic: Bountycaster **does not escrow funds at all**. A bounty there is
  just a cast tagging `@bountybot` with a description + amount; the bot indexes it into a
  page, and the actual payment happens peer-to-peer, off-platform, however the two parties
  agree (wallet transfer or a Farcaster tip) - Bountycaster is a listing/discovery layer,
  not a funds-holding one. That means a POIDH bounty's real content (the description, THE
  BAR, the POIDH URL where the actual ETH is escrowed and claims are submitted) can simply
  be pasted into a `@bountybot`-tagged cast as its own listing, with the POIDH link doing
  double duty as both the funding mechanism and the "where to submit" instruction. This is
  a **manual, one-time cross-post per bounty**, not an automatic sync - there's no API/webhook
  to keep the two in sync if a POIDH bounty's status changes, so whoever posts it needs to
  remember to update or note completion on the Bountycaster side too. Still free extra
  discovery surface for the cost of one extra cast per round - worth doing on the next
  bounty cast as a real test rather than a hypothetical.

## Suggested next actions (research-informed, not yet committed to)

| Target | Action | Effort | Notes |
|---|---|---|---|
| SheFi | Send the outreach DM at [outreach/shefi-dm.md](outreach/shefi-dm.md), a warm intro leading with the POIDH x SheFi/Jessebot precedent | Low - the DM is drafted and send-ready, just needs a recipient confirmed and Zaal's go-ahead | Deliberately does not assume ZABAL Gamez is the right subject - the draft's next-steps note flags asking SheFi what they'd want promoted first |
| Purple DAO | Send the outreach DM at [outreach/purple-dao-dm.md](outreach/purple-dao-dm.md), pitching a joint /zabal x /purple cross-promo bounty | Low - the DM is drafted and send-ready, just needs a recipient confirmed and Zaal's go-ahead | Framed against Purple's own stated Farcaster-growth funding thesis, not a generic ask |
| Yellow Collective | Send the outreach DM at [outreach/yellow-collective-dm.md](outreach/yellow-collective-dm.md), pitching a cross-pollination round for artist-made work | Low - the DM is drafted and send-ready, just needs a recipient confirmed and Zaal's go-ahead | Natural fit given the shared "artist track" framing - narrower and more specific than the Purple DAO pitch |
| Bountycaster | Manually cross-post the next round's bounty as a `@bountybot`-tagged cast, with the POIDH URL as the funding/submission link | Low (1 extra cast per round, no relationship needed) | Feasibility confirmed via their FAQ - no native mirroring, but their no-escrow architecture makes a manual cross-post trivial. No sync mechanism, so note completion manually too |
| Degen community | Run a DEGEN-denominated bounty directly via `poidh.xyz/degen` (confirmed working - real live example: bounty 1393, 13,014 DEGEN) - NOT via `docs/create-bounty.html`, which only supports Base today | Medium (needs a Degen-chain-specific description; the bounty itself must be created on POIDH's own site, not this repo's tool) | Confirmed genuinely possible on POIDH, but adding Degen support to this repo's own create-bounty.html needs a verified contract address from POIDH's team first - see the note above on why that wasn't guessed |

None of these are commitments - they're researched, precedent-grounded leads for Zaal to
decide on. Every "Action" above assumes the P2P Ad Bounty Kit structure
(`docs/P2P-AD-BOUNTY-KIT.md`) as the actual bounty format, since that's the proven
mechanism, not a new pitch to invent per partner.

## Sources

- [pics or it didn't happen | Gitcoin](https://gitcoin.co/apps/poidh) - POIDH protocol overview, AI-agent compatibility, multi-chain deployment
- [pics or it didn't happen (@poidhxyz) / Posts / X](https://x.com/poidhxyz) - POIDH x SheFi/Jessebot bounty
- [Bountycaster](https://www.bountycaster.xyz/) - Bountycaster platform, fee structure, EAS attestations
- [Bountycaster FAQ](https://www.bountycaster.xyz/faq) - confirmed no native cross-protocol mirroring, no-escrow p2p payment architecture, @bountybot cast-based creation flow
- [Bountycaster: Project Guide | Bitget](https://web3.bitget.com/dapp/bountycaster-28503) - Bountycaster figures ($1.5M / ~2,967 bounties)
- [Reflections on Purple - Phil Mohun](https://www.philmohun.com/purple-reflections/amp/) - Purple DAO mission, Rounds.wtf grants, Base auction history
- [Web3 Galaxy Brain - Purple, the Farcaster DAO](https://web3galaxybrain.com/episode/Purple-the-Farcaster-DAO) - Purple DAO background
- [Nouns Builder | Purple](https://nouns.build/dao/base/0x8de71d80eE2C4700bC9D4F8031a2504Ca93f7088/507) - Purple's Nouns Builder deployment
- [ournetwork issue 188](https://ournetwork.substack.com/p/ournetwork-issue-188) - Nouns Builder ecosystem scale (200+ collectives), Yellow Collective
- POIDH's own tRPC feed (`bounties.fetch`, id 1393, `chainId: 666666666`, queried directly) - confirmed a real live Degen Chain bounty (13,014 DEGEN, onChainId 196)
- [Degen Chain marketplace app | Blockscout](https://explorer.degen.tips/apps/poidh) and the POIDH V2 NFT contract at `0xDdfb1A53E7b73Dba09f79FCA24765C593D447a80` - checked directly, contract is unverified (no published source), which is why its address was not used in any transaction-signing code

## Also see

- [P2P-AD-BOUNTY-KIT.md](P2P-AD-BOUNTY-KIT.md) - the bounty structure to use for any of the above
- [PARTNER-GUIDE.md](PARTNER-GUIDE.md) - if a partner org wants their own forked instance of this tooling rather than a joint bounty
- [outreach/purple-dao-dm.md](outreach/purple-dao-dm.md) - send-ready DM draft pitching Purple DAO a joint round
- [outreach/shefi-dm.md](outreach/shefi-dm.md) - send-ready DM draft pitching SheFi, leading with the existing POIDH x SheFi precedent
- [outreach/yellow-collective-dm.md](outreach/yellow-collective-dm.md) - send-ready DM draft pitching Yellow Collective, an artist-track cross-pollination round
