# R8 - Tell us how to announce poidhz (DRAFT, not cast)

The launch round. **$5 seed, OPEN so the pot can grow, contributor vote.** Nothing is cast
and nothing has been sent.

This round is numbered 8 but is intended to cast **first**, ahead of R6 and R7. Round
numbers here are allocation order, not cast order - R6 (NYC recap) and R7 (WaveWarZ clips)
keep their numbers and stay parked on their own blockers.

## The decision this came from

Zaal, 2026-09-20, when asked how poidhz should be positioned for launch: **"lets draft a 5%
bounty on the best way to annouce this"**, clarified in the same grill to a **$5 pot, OPEN so
others stack**. Rather than pick the framing ourselves, the launch is the bounty.

Also his, same grill, and it sets the sequence: **"lets just post poidhz first then asking
people to make content with zaostock from the /brand page thats highest priority."** So R8
announces poidhz; the ZAOstock content round follows it.

## Why $5 and not more, which is counterintuitive

Measured 2026-09-20 across all 99 open bounties on poidh, written up in ZAOOS research doc
`business/2522-poidh-live-bounty-market`:

| Prize band | Share with at least one submission |
|---|---|
| under $5 | **69%** |
| $5-15 | 42% |
| $15-50 | 56% |
| $50+ | **43%** |

**Prize size does not buy entries on this platform.** The cheapest band has the highest entry
rate and the most expensive nearly the lowest. What does predict entries is format - photo
68%, clip 64%, against code 43% - and this round is format-open, so an entrant can pick the
cheap end deliberately.

Caveat carried from the research rather than dropped: `created_at` is empty on all 99 rows,
so that table is not controlled for how long each bounty has been open. It is a real pattern
in the standing set, not proof that a small prize attracts more people.

## The mechanic is the message

OPEN type is not a default here, it is the thing being demonstrated. Zaal named the audience
this round is really for: **"zao members to support with 1$ or 2 here or there for an idea."**
A $5 seed that ten people top up by a dollar each pays the maker fifteen, in one clean
settlement, from people who never had to coordinate. That is the argument for poidhz as an ad
provider, made by running it rather than by claiming it.

Resolution is a **contributor vote**, not Zaal picking. If the community funds it, the
community decides it.

## What a winning entry hands over

Zaal, same grill: **"anything they think is the best way to release it they can review past
videos or ask me for things to update on the website."** So the ask is deliberately
format-open - a publish-ready post, a clip, a poster, a strategy, or something nobody
proposed. Entrants may request changes to poidhz.com as part of their pitch.

## Before this can cast

- [ ] **Fund the issuer wallet.** Short 0.010763 ETH / $26.79 as of 2026-09-08; re-measure.
- [ ] **Confirm the $5 in ETH.** `0.0019 ETH` in the description is ~$5.00 at $2,633.31,
      which is the ETH price the dashboard read on 2026-09-20. Re-price at cast time.
- [ ] **R8 CASTS AFTER KENNY REPLIES, not just after the message is sent.** Zaal,
      2026-09-20, asked directly whether the round waits on him: **"after"**. So a sent
      message is not the gate clearing - his reply is. If he goes quiet for more than a
      few days that is a decision for Zaal to make, not a timeout this repo should assume.
- [ ] **Send the bundle to Kenny first.** Zaal: "yes we usually send our bounties to him
      always gives us good feedback we can send anything to him before we post", and on
      what to send, **"Everything at once, including the poidhz post"**. Draft at
      `docs/outreach/kenny-poidhz-bundle.md`, unsent.
- [ ] **Set the real deadline, and note that waiting on Kenny may already have broken it.**
      The description carries Sunday October 4, 2026, 11:59pm PT with the vote result by
      Tuesday October 6. Both assume a cast on or before 2026-09-22. Now that the round
      waits on Kenny's reply rather than on the message going out, that assumption is no
      longer safe: **re-read both dates at cast time and move them if the cast slips past
      2026-09-22**, or the round ships with a window shorter than the two weeks it was
      designed for. A deadline written before an unknown wait is the classic stale number.
- [ ] `python3 scripts/precast-check.py --round 8 --prize 0.0019`

## Status

`validate-bounty-description.py` PASSES. Not cast, not funded, not sent. No bounty id yet, so
nothing is in `default_bounty_ids` and nothing scores on the leaderboard.
