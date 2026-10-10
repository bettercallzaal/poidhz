<!-- NOT-ANNOUNCEMENT-COPY: internal research memo. Names no deadline anyone submits to. -->
# The $1,000 WaveZStation buy - what the site, the chain and the contract actually say

Written 2026-10-10 by the poidhz lane for the round-ten reopen (orchestrator2, vault decisions
item 64). Zaal's words, relayed: *"i have an idea for a 1000 buy on wavezstation with the best
artist, tradoff you would be the firs artist with 4 figures on wavestation which 45% would
immedatly go to you"*. Every number below names the surface it was read from and the clock
time it was read. Nothing here was bought, cast, posted or sent.

## 1. Which site, which chain

- **WaveZStation is wavezstation.com, USDC on Base (chain 8453).** The site's own JS bundle
  references chain id 8453 and USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
  (`/_next/static/chunks/app/discover/page-*.js`, read 15:12Z). Every song record from
  `/api/songs/<id>` says `chain_id: 8453`. This matches the 20 Sep call clip
  (`zao-vault/inbox/clips/clip-20260920-172314-wave-station-daily-quest.md`): Wave Station is
  USDC on Base, WaveWarZ is Solana. Different products, different chains.
- **The song contract is `0x6eee0a8ebd1446a3a77a8f720bf37232fd88b255` on Base.** Every one of
  Zaal's fifteen posted share links (`wavezstation.com/share/buy/<tx>`, from
  `zao-vault/projects/x-account/posted-log.tsv`) is a transaction to that address with function
  selector `0x45feb00d`, and the song's own create transaction
  (`wavestation_create_tx_hash` in the song API) went to the same address. Receipts read from
  `https://mainnet.base.org` at 15:3xZ.
- **The contract is NOT verified on Basescan.** Read at 16:05Z: the Contract tab says "Are you
  the contract creator? Verify and Publish", no ABI, no source. Creator
  `0xF3aFf958fbA167bAb80e515AbC8d7077DEED886a`, deployed 76 days before the read. The 20 Sep
  clip says "the contract is verified on Basescan"; that was wrong, or it has changed. So the
  split below is confirmed from transfers, not from source.

## 2. What share the artist gets, and when - CONFIRMED, with one catch

**Zaal's 45 percent is right, and "immediately" is literally true.** Three surfaces agree:

| Surface | What it says | Read |
|---|---|---|
| `wavezstation.com/docs` section 2 | every sale: 45% fan pool, 45% artist + collaborators, 10% platform | 15:12Z |
| `/api/songs/<id>` for all 27 listed songs | `wavestation_creator_pct_bps: 4500`, `wavestation_fan_pct_bps: 4500`, `wavestation_min_amount: 1000000` (1 USDC) on every song | 16:02Z |
| Base receipts of 15 real buys | buyer sends USDC to the contract; **in the same transaction** the contract sends 10% to the platform wallet `0xd97409D949d032A12bD4B7af1f94F7D3222C8E72` and 45% to the creator wallets, split by the song's `wavestation_creator_splits_bps`. The other 45% stays in the contract. | 15:3xZ |

Worked example from the chain, Zaal's issuer wallet `0x7234c36a71ec237c2ae7698e8916e0735001e9af`
buying 100 USDC of Saturday in LA at block 51,091,069: 10.0 to the platform, 22.5 and 22.5 to the
two creator wallets, 45.0 retained. His 70 USDC buy at block 51,607,926: 7.0, 15.75, 15.75, 31.5
retained.

**The catch: "the artist" is the song's creator wallet list, and Saturday in LA has two of
them, split 50/50.** `wavestation_creator_wallets` = `0x7e1e8eD40A57E4defd80d60228Cc3E3F1E81a811`
and `0x73A8C85CcAD4cfc7C37e12Ad37d64Aa5427C0c5b`, `splits_bps` = `[5000, 5000]`. Neither
resolves to an ENS, Farcaster or X identity on web3.bio (16:0xZ). So of a $1,000 buy, **$225
reaches each wallet**, and whether both are BennyJ504's is unknown until he says. Of the 27
listed songs, 17 have one creator wallet, 9 have two, and one (What It Douie?) has six.

**The fan pool's 45% is retained, not pushed.** Basescan labels one decoded method on the
contract "Claim Rewards"; the docs say fans earn "proportionally to how much each fan contributed"
and that payout timing "can depend on smart contract behavior". So earlier buyers claim; nothing
arrives in their wallet unasked. The exact formula is in unverified bytecode and is UNVERIFIED
here.

## 3. Who the top artist is - MEASURED at a stamp

`https://www.wavezstation.com/api/discover?limit=100&sort=funded` is the endpoint behind the
site's "Most funded" tab (found in the discover page's JS). Read twice today; both reads are
saved beside this file (`wavezstation-discover-2026-10-10T160243Z.json`).

| Rank at 16:02:43Z | Song | Artist | Fan pool (USDC) | Supporters |
|---|---|---|---|---|
| 1 | Saturday in LA | BennyJ504 (`@bennyj504` on X, per the song API) | 360.80 | 14 |
| 2 | AI LUI - The Album (The Wavewarz Chronicles) | AI LUI | 264.00 | 18 |
| 3 | Killing Floor | GodclouD | 159.00 | 8 |
| 4 | WYAU - No Sleep Gang Anthem (ft. DaDutchess) | PKMN CTO | 157.00 | 10 |
| 5 | WAGBG | Nessy the Rilla | 128.00 | 7 |

Summed per artist across all their songs it is the same order at the top: BennyJ504 360.80 (one
song), GodclouD 271.00 (two), AI LUI 264.00 (one), r3plic4nt 183.00 (two). 27 songs listed,
1,775.30 USDC in all pools together. The 15:21:17Z read gave identical numbers. Zaal's 7 Oct
note ("the top song right now is saturday in LA") holds.

**The gap is small.** AI LUI's pool trails by 96.80 USDC, which is about 215 USDC of sales. One
mid-sized buyer flips it. The plan below fixes the artist at the moment of the buy, not at the
moment of this memo.

## 4. Has anyone bought four figures already - NO, by a bound

The full buy list could not be pulled today: Dune is read-only on this account, and every free
Base RPC refused the history (publicnode: archive needs a token; drpc: 10,000-block cap and then
refused 2,000; blastapi: 10-block cap; mainnet.base.org: "request limit reached" from the second
call). That is UNMEASURED and says so.

What the site data proves without it: `pool_total_usdc_wei` is the fan pool, which is 45% of
every sale on that song (section 2). Saturday in LA's 360.80 pool means **about 801.78 USDC of
cumulative sales on the most-sold song on the site.** No single buy can exceed a song's
cumulative sales, so **no four-figure buy has ever happened on WaveZStation, and no song has
reached four figures in sales.** Assumption carried: the pool counts sales only. The docs also
speak of fans "contributing" to a pool; if a direct contribution path exists and was used, the
bound loosens, but the site exposes no such action (home page: "Buy Into Songs", "Pay What You
Want"; song records have `pool_address: null`).

So both of Zaal's framings are true at the stamp: a $1,000 buy would be the first four-figure
buy, and it would make Saturday in LA the first song past $1,000 in sales (about $1,802).

## 5. Where the $1,000 goes, line by line

On today's config, buying 1,000 USDC of Saturday in LA in one transaction:

| Bucket | USDC | Who | When |
|---|---|---|---|
| Platform | 100.00 | `0xd974...8E72` | same transaction |
| Creator wallet 1 | 225.00 | `0x7e1e...a811` | same transaction |
| Creator wallet 2 | 225.00 | `0x73A8...0c5b` | same transaction |
| Fan pool | 450.00 | retained in the contract, claimable by the 14 earlier supporters pro rata | on claim |

**Zaal is already the song's biggest supporter, and that changes the fan-pool line.** His
issuer wallet put 170 USDC into Saturday in LA (100 on 9 Sep, 70 on about 21 Sep, both on
chain). That is about 21% of the 801.78 USDC sold so far. If the pool pays earlier supporters
pro rata by what they put in, roughly **$95 of the $450 fan share is claimable by Zaal himself**,
and after the buy he holds about 65% of the pool, so about 29 cents of every later dollar
spent on that song is his to claim. Both figures rest on the formula in section 2 being the
simple pro-rata one the docs describe; the contract is unverified, so they are estimates.

Net of his own claimable share, the $1,000 costs about $905 and puts $450 in the creators'
hands, $355 in thirteen other fans' hands, $100 with the platform.

## 6. How a $1,000 buy is actually made

- The site's buy is "pay what you want" with a 1 USDC floor (`wavestation_min_amount`). No
  ceiling is visible in the site data; whether the UI or contract caps a single buy is
  UNVERIFIED. Zaal's 100 USDC buy went through the site, so the path works at that size.
- It needs 1,000 USDC on Base in the sending wallet plus Base gas. The issuer wallet held
  0.000107 ETH on 1 Oct (status file); its USDC balance was not read today.
- The transaction is public the moment it lands. Anyone can open the hash on basescan.org and
  see the three outbound transfers. That is the whole verification story: one hash.

## 7. What poidh can and cannot do here

poidh on Base pays native ETH only (`docs/erc20-bounty-fork.md`, root README). The $1,000 is a
WaveZStation buy from Zaal's wallet, not a poidh pot. So round ten is two separate acts:

1. **The buy.** On-chain, Zaal's wallet, Zaal's tap. Not a bounty.
2. **The bounty.** A reaction round on that song, the shape Zaal asked for on 6 Oct (PR #236),
   now pinned to the song the $1,000 went into. The pot is the reward field, $100 at his ask
   (0.0399 ETH at 2,506.72 USD per ETH, Coinbase spot 16:06:44Z).

What the record says about the bounty shape (`docs/what-draws-entries-2026-10-01.md`): rounds
built on our own source media draw best (7 to 10 wallets); a stated deadline roughly doubles
entries; naming one room to post in helps; a mandatory tag rule disqualified most of a field
once, so tags stay optional. The reaction shape is new for us; the one-dollar buy in the rules
is a cost on the entrant that no prior round had, and it pays Zaal a slice (section 5), which
the text now discloses in numbers.

## 8. Open before anything fires (each with the default the plan takes)

1. **Who owns the second creator wallet.** Default: ask BennyJ504 in the pitch; if it is a
   producer or feature, say "$450 to the song's creators" not "$450 to you".
2. **Buy as one transaction or several.** Default: one, so there is one hash and the
   "first four-figure buy" claim is literal.
3. **Which wallet sends.** Default: the issuer wallet `0x7234...e9af`, because its prior buys
   are already public and the announcement can link all three.
4. **Order of operations.** Default: pitch first (so the artist is not surprised by $450 landing),
   buy second, cast third, announce fourth. Zaal can collapse 1 and 2 if he wants the surprise.
5. **The disclosure.** Default: the bounty text states that Zaal holds most of the song's fan
   pool and that part of each entrant's dollar is claimable by him. Removing it is his call and
   this lane recommends against it.
