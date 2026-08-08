# POIDH partnership targets - research notes

Research pass on which orgs/communities are realistic candidates for BCZ/The ZAO to
partner with on POIDH-based bounty campaigns (as a P2P ad system, per
[P2P-AD-BOUNTY-KIT.md](P2P-AD-BOUNTY-KIT.md), or as a general community bounty board).
Grounded in verified precedent, not speculation. Live-searched 2026-08-06 - dates and
figures below are current as of that search; re-verify before acting on anything time-sensitive.

## Already-connected leads (highest priority, found 2026-08-07)

These aren't cold-outreach targets - BCZ already has a real, existing connection to both.
Found by researching what other real initiatives have actually used POIDH historically,
rather than only researching new orgs to approach cold.

- **We Them Media - BCZ already carries their name, correction on how connected that
  actually makes us.** BCZ has posted every one of its own bounty submissions (R1, R2, R3)
  into the Farcaster album `wethemmedia` - it's `org.config.json`'s own `farcaster_album`
  value, not a new discovery. Separately, verified live on-chain this pass (`bounties.fetch`
  / `/data`, id 1096, Base, direct tRPC + REST query, not a search snippet): a real,
  currently-running initiative called **"Preach POIDH & We Them Media"** exists - "IYKYK is
  teaming up with POIDH & We Them Media for a series of weekly bounties intended to survey
  thousands of people from around the world. Each week, We Them Media will set a video
  survey bounty featuring a new question. POIDH sponsors the bounty with a $100 prize, and
  IYKYK works to drive engagement." **Correction to an earlier version of this doc:** bounty
  1096 is tagged to a DIFFERENT POIDH album (`iykyk`), not literally the same `wethemmedia`
  album BCZ posts into - so "BCZ already shares the exact same media pipeline" overstated
  it. What's real: the actual Farcaster account is verified live (`@wethemmedia`, fid
  1091675, real bio: "We Them Media is a community of web3 native creatives... let's build
  it, together") - a real, findable, warm-ish target since BCZ's own album already carries
  their name, but it's "reach out to the account behind the name we've been using," not
  "we're already inside their pipeline." Zaal is personally already close with them and
  noted they're less active right now - outreach draft reflects that (a personal check-in,
  not a template pitch): [outreach/wethemmedia-dm.md](outreach/wethemmedia-dm.md).
- **Haberdashery - already on BCZ's own catalytic-DM whale list, and a grants DAO, not
  just a whale.** `docs/how-to-draft-next-bounty.md` already lists Haberdashery as one of
  the whales BCZ DMs for public co-funder drops before casting an OPEN bounty. Verified
  live: the real Farcaster account is `@thehaberdashery` (fid 578265, 791 followers, real
  bio: "A crowdfunded DAO deploying funds to builders scaling the Base ecosystem") -
  `rounds/_template/cast-templates/catalytic-dm.md` already has the correct handle. This
  reframes the collab pitch: not "ask a whale what worked," but "pitch a grants DAO whose
  entire purpose is funding exactly this" - separately confirmed via web research to have
  run POIDH's biggest documented bounty to date, a $30K "kickflip" bounty that broke a
  Guinness World Record and generated 100K+ views, the clearest proof anywhere that POIDH's
  OPEN-bounty viral co-funding mechanic works at real scale. Outreach draft:
  [outreach/haberdashery-dm.md](outreach/haberdashery-dm.md).

## Official POIDH agent tooling - found 2026-08-08, resolves the Degen contract gap

Found by tracing a real lead from Zaal's own Telegram conversation with Kenny (POIDH
founder): Kenny cast on Farcaster that `@thoughtcrimeboss` had read all 20+ pages of new
official POIDH docs and sent detailed notes - and linked `docs.poidh.xyz`. That site is
real, live, and far more substantial than anything cited in this doc's earlier passes:

- **`docs.poidh.xyz`** - official POIDH v3 documentation: protocol overview, using-poidh
  guide, features, developer guide, and a full contracts section (architecture, state
  machines, security, API reference, deployment guide).
- **The Degen Chain contract address gap flagged earlier in this doc is now resolved,
  from an authoritative source - not guessed.** `docs.poidh.xyz/contracts/deployment.html`
  publishes the full deployment table directly:
  - Ethereum Mainnet: `0xE731dFadBFf20542E10D09D26Fc71445C70d4232` (deployed 2026-05-13)
  - Base: `0x5555Fa783936C260f77385b4E153B9725feF1719` (deployed 2026-01-19)
  - Arbitrum: `0x5555Fa783936C260f77385b4E153B9725feF1719` (same address as Base, confirmed)
  - **Degen Chain: `0x18E5585ca7cE31b90Bc8BB7aAf84152857cE243f`** (deployed 2026-01-19)
  - Degen Chain minimums: 1000 DEGEN minimum bounty, 10 DEGEN minimum contribution (very
    different from the 0.001 ETH minimum on the other three chains - anything adding Degen
    support needs to branch on this, not assume the same minimum everywhere)
- **POIDH's own team publishes a production-ready Claude Code agent skill** -
  [`poidh-app/SKILL.md`](https://github.com/picsoritdidnthappen/poidh-app/blob/prod/SKILL.md)
  (`picsoritdidnthappen/poidh-app`, branch `prod`). This is not a vague "AI-agent
  compatible" feature-list claim - it's a complete, working skill covering: posting a solo
  or open bounty, evaluating claim submissions (fetches each claim's proof URI, uses
  vision for images, web-fetch for links/tweets/PRs, resolves IPFS/Arweave URIs), accepting
  a winning claim directly or running the two-step open-bounty vote flow, submitting a
  claim as an agent, and withdrawing funds. It resolves the correct contract per chain via
  the exact same addresses above, and its own "Agent Decision Flow" section already bakes
  in a human-confirm gate before every fund-moving transaction ("Confirm with user before
  sending - this spends real ETH (or DEGEN)") - the identical "AI proposes, human approves"
  pattern already validated for social posting in ZAO OS V1 doc 2213.

**This directly answers "do stuff that's more automatic."** Instead of (or alongside)
zpoidh's own custom scripts, a Claude Code session working in this repo could use POIDH's
own official skill to post a round, and - genuinely new capability zpoidh doesn't have
today - evaluate every claim's submission with vision and recommend a winner, the same
judgment call R2/R3's manual scorecards did by hand. Worth a real evaluation: adopt this
skill directly for round automation (Stage 4/5 of the round pipeline), rather than
maintaining parallel custom tooling that does a subset of what POIDH's own skill already
does.

## Confirmed precedent (POIDH already has cross-community traction)

- **POIDH x SheFi** - POIDH ran a bounty specifically for the SheFi community, judged by
  POIDH's own "Jessebot" AI, timed to a SheFi AMA. This is the clearest existing proof
  that POIDH already partners across community lines, not just within its own Farcaster
  base. SheFi (women-in-crypto education community) is a plausible direct follow-up
  partner for BCZ - similar audience-growth goals, and POIDH has already broken the ice
  with them once.
- **POIDH is now explicitly AI-agent compatible - confirmed with the real skill above,
  not just a feature-list claim.** Agents can propose bounties and select claims while a
  human retains verification control, and the protocol is deployed across Ethereum
  Mainnet, Arbitrum, Base, and Degen Chain. This matters for ZAO specifically: ZOL/ZOE-
  adjacent tooling could eventually *propose* bounties on behalf of BCZ (not just draft
  casts, per ZAO OS V1 doc 2213), with a human still gating the actual on-chain accept -
  see the section above for the actual mechanism, already built by POIDH's own team.
- **Degen Chain is a first-class POIDH deployment, confirmed with a live example, not
  just a claim.** Queried POIDH's own tRPC feed directly (`bounties.fetchAll` with
  `chainId: 666666666`) and found a real, currently-open bounty on Degen Chain: id 1393
  ("Closest to Zero"), 13,014 DEGEN, `onChainId` 196. This is the same live number
  `scripts/build-bounty-dashboard.py`'s own inline comment references as a real example it
  had to handle correctly (its `CHAIN_TOKENS` mapping already prices DEGEN natively, for
  exactly this reason). So the "run a Degen-denominated bounty" idea below is genuinely
  possible on POIDH - it isn't hypothetical.

  **Gap between "POIDH supports it" and "zpoidh's own tooling supports it" - now
  resolved.** As of 2026-08-08, `docs/create-bounty.html` has real Degen Chain support (see
  below) using the officially-documented contract address, resolving the gap this doc
  previously flagged. `docs/create-bounty.html` previously hardcoded Base mainnet only and
  the shared Base/Arbitrum contract address, with no Degen option - deliberately left
  unfixed in an earlier pass of this doc because the only Degen contract address findable
  at the time was an unverified Blockscout listing, not safe to hardcode into
  transaction-signing code. That blocker is gone: `docs.poidh.xyz/contracts/deployment.html`
  (POIDH's own official docs, found 2026-08-08 - see the section above) now publishes the
  verified address directly from POIDH's team, not from block-explorer archaeology.

  The Degen community (a Farcaster-native tipping/rewards culture with its own token) is a
  low-friction partnership target for the reasons below - they already understand token-
  incentivized public tasks - and creating a Degen bounty can now go through either
  `poidh.xyz/degen` directly or zpoidh's own `create-bounty.html`.

  **Contact point - resolved, honestly, not just a dead end.** Checked the `/degen`
  Farcaster channel directly (2026-08-08): it's a broad, 2K-member "risk-takers and
  meme-makers" channel with no listed host/moderator - it's a culture channel, not an
  organized DAO body with a single point of contact. There is no single "Degen community
  lead" to DM the way Purple DAO or Yellow Collective have one. The closest real,
  verified, organized contact BCZ already has for the Degen ecosystem specifically is
  The Haberdashery - already documented above as "Degen DAO grants council" per this
  repo's own existing template, with a real send-ready draft
  ([outreach/haberdashery-dm.md](outreach/haberdashery-dm.md)). Any Degen-specific
  partnership push should go through that contact rather than a generic "Degen community"
  DM that has no real recipient.

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
| Degen community | Run a DEGEN-denominated bounty via either `poidh.xyz/degen` or `docs/create-bounty.html` (both work as of 2026-08-08) - needs a Degen-chain-specific description | Medium (mainly the description/framing work now, not a tooling blocker) | Degen support shipped in create-bounty.html using the officially-documented contract address - see the section above. No single "Degen community" contact exists to DM (the `/degen` channel has no host) - route any Degen-specific ask through The Haberdashery instead |
| We Them Media | Send the personal check-in at [outreach/wethemmedia-dm.md](outreach/wethemmedia-dm.md), a "Spotlight" bounty about them, zero effort on their end | Low - Zaal already has the relationship, this just needs sending | Deliberately not a template pitch - Zaal is personally close with them, drafted to sound like him, not a cold outreach voice |
| The Haberdashery | Send the outreach DM at [outreach/haberdashery-dm.md](outreach/haberdashery-dm.md), pitching a co-funded "big swing" OPEN round | Medium - the DM is drafted and send-ready, but a real co-designed round needs real back-and-forth after | Reframes an existing catalytic-DM contact as a full grants-DAO partner, not just a one-off co-funder ask |

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
- [Degen Chain marketplace app | Blockscout](https://explorer.degen.tips/apps/poidh) and the POIDH V2 NFT contract at `0xDdfb1A53E7b73Dba09f79FCA24765C593D447a80` - checked directly during an earlier pass, contract was unverified (no published source), which is why its address was not used in transaction-signing code at the time (superseded - see docs.poidh.xyz below)
- [docs.poidh.xyz](https://docs.poidh.xyz) - official POIDH v3 documentation, found via a real cast from Kenny (POIDH founder) in Zaal's own Telegram conversation history, cross-checked live in-browser (found 2026-08-08)
- [docs.poidh.xyz/contracts/deployment.html](https://docs.poidh.xyz/contracts/deployment.html) - official deployment addresses for all 4 chains (Ethereum Mainnet, Arbitrum, Base, Degen Chain), fetched in full, not a snippet
- [poidh.xyz/a/publicgoods](https://poidh.xyz/a/publicgoods) - queried directly via POIDH's own tRPC `album` filter (2026-08-08), confirmed a broad multi-issuer community tag, not a single curated program with one contact
- [Degen Channel on Farcaster](https://farcaster.xyz/~/channel/degen) - checked live in-browser (2026-08-08), confirmed no listed host/moderator - a 2K-member culture channel, not an organized body
- [poidh-app/SKILL.md](https://github.com/picsoritdidnthappen/poidh-app/blob/prod/SKILL.md) - POIDH's own official Claude Code agent skill (`picsoritdidnthappen/poidh-app`, branch `prod`), fetched in full
- POIDH's own tRPC feed (`bounties.fetch`, id 1096, Base) - confirmed live the "Preach POIDH & We Them Media" / IYKYK weekly bounty series, direct on-chain query, not a search snippet
- [Preach POIDH & We Them Media](https://poidh.xyz/base/bounty/1096) - the live bounty page itself
- Web research (2026-08-07) - the $30K Degen Haberdashery kickflip Guinness World Record bounty, and the POAP x Degen community-call artwork bounty (50+ submissions) - both cited as real POIDH precedent, not speculation

## Also see

- [P2P-AD-BOUNTY-KIT.md](P2P-AD-BOUNTY-KIT.md) - the bounty structure to use for any of the above
- [PARTNER-GUIDE.md](PARTNER-GUIDE.md) - if a partner org wants their own forked instance of this tooling rather than a joint bounty
- [outreach/purple-dao-dm.md](outreach/purple-dao-dm.md) - send-ready DM draft pitching Purple DAO a joint round
- [outreach/shefi-dm.md](outreach/shefi-dm.md) - send-ready DM draft pitching SheFi, leading with the existing POIDH x SheFi precedent
- [outreach/yellow-collective-dm.md](outreach/yellow-collective-dm.md) - send-ready DM draft pitching Yellow Collective, an artist-track cross-pollination round
- [outreach/wethemmedia-dm.md](outreach/wethemmedia-dm.md) - personal check-in draft for We Them Media, the "Spotlight" collab idea (Zaal is already close with them)
- [outreach/haberdashery-dm.md](outreach/haberdashery-dm.md) - send-ready draft pitching The Haberdashery a co-funded "big swing" round, grants-DAO framing
