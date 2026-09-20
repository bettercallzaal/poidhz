# To Kenny - poidhz launch bundle

**DRAFT, unsent. Outbound is Zaal's tap.** Nothing here has been sent.

Zaal, 2026-09-20, on whether Kenny sees this first: *"yes we usually send our bounties to him
always gives us good feedback we can send anything to him before we post"*, and on what goes
in it: **"Everything at once, including the poidhz post."** So this is one message, not three.

**No SEND-GATE marker on this file, deliberately.** Every other outbound draft here carries
`<!-- SEND-GATE: round=5 -->`, which holds it until R5's promises are recorded kept. Zaal
lifted that for this thread on 2026-09-20: **"lets not worry about the inner annoucment."**
The gate still holds `owed-credit.md`, the R6 note and the retainer; this one is out from
under it by his decision, recorded here rather than quietly omitted.

**Send this BEFORE casting R8.** He is the single largest issuer on poidh - 21 open bounties,
fid 2210, 20,695 followers, verified two ways in ZAOOS research doc
`business/2522-poidh-live-bounty-market`. His feedback has changed our rounds before.

**Lead with the chain verification, not the ask.** His repo has an open issue about stranded
funds that nobody has replied to in 23 days. We independently confirmed half of it. That is
worth more to him than anything we want.

---

## The message

```
Kenny - three things, and the first one is yours not ours.

1. Someone filed issue #1459 on poidh-app on Aug 28 about open, funded bounties on the
pre-v3 contracts that the app no longer reads. It has had no replies for 23 days. We
re-read the contracts ourselves and it checks out exactly.

Base 0xb502c585, all 990 ids: 201 still open and still funded, 0.581754831471201010 ETH.
Arbitrum 0x0Aa50ce0, all 180 ids: 24 open and funded, 0.024858010 ETH.

That is 0.606612841471201010 ETH, matching the issue to the wei. At today's price about
$1,597, against roughly $3,181 across every bounty poidh can currently show. So there is
half as much value again sitting in bounties nobody can reach as in the whole visible
market.

We could not read the four Degen contracts at all - rpc.degen.tips is returning Cloudflare
1016 and five other public endpoints either fail or refuse eth_call. So the other 225 are
unverified rather than disproven.

The scanner is about 40 lines and reads bounties(uint256) over every id on any contract you
point it at. It is yours if you want it, and we will run it on Degen the moment there is a
working RPC.

2. We built poidhz - poidhz.com. It started as our own bounty ops and turned into a public
client: every open bounty with a stated deadline on one calendar, countdowns, a
subscribable .ics, and the submitter leaderboard. The thing that started it was noticing
the native deadline field is set on zero of the open bounties, so we parse the date out of
the description instead.

3. We want to announce it, and we would rather not guess how. So the launch is a bounty:
$5 seeded, OPEN so anyone can stack a dollar on it, contributor vote, asking people to
pitch the best way to announce poidhz in any format they like. Draft is below. If the
community tops it up and someone outside The ZAO makes the thing that launches it, that is
the whole argument for what we are building, demonstrated instead of claimed.

Anything you would change before we cast it? You have made every one of these rounds better
and we would rather hear it now than after.
```

## Attached to the same message

- The R8 description, exactly as it will be pasted: `rounds/r8/description.md`
- poidhz.com, and the repo at github.com/bettercallzaal/zpoidh

## Do not include

- Anything about R5's winner announcement. Zaal, 2026-09-20: **"lets not worry about the
  inner annoucment."** It is a separate thread and it is his.
- Any claim about the Degen contracts beyond "we could not read them". Six endpoints failed;
  that is unreadable, not refuted.

## Numbers in this message, and where each came from

Re-verify before sending. All measured 2026-09-20.

| Claim | Source |
|---|---|
| 201 open+funded, 0.581754831471201010 ETH on Base | batched `eth_call` over all 990 ids |
| 24 open+funded, 0.024858010 ETH on Arbitrum | batched `eth_call` over all 180 ids |
| $1,597 stranded vs $3,181 visible | at ETH $2,633.31, the price `data/bounty-dashboard.json` used the same day |
| 21 open bounties, fid 2210, 20,695 followers | `api.web3.bio` and Farcaster `fc/primary-address`, two independent sources |
| native deadline field set on zero open bounties | `scripts/scan-poidh-deadlines.py`, `bounties_with_native_deadline: 0` of 83 scanned |
| issue #1459 open, 0 comments, 23 days | `gh api`, 2026-09-20 |
