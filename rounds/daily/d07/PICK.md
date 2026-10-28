<!-- NOT-ANNOUNCEMENT-COPY: the field and the recommended pick for round seven. Internal. Names no deadline anyone submits to. -->
# Round seven - the field, the pick, and the transaction

Bounty **1453**, on-chain **467**, pot **0.0115 ETH** (about $27 at poidh's read). OPEN bounty.
Creations closed **5:00pm Eastern Sunday 4 October**; entrant bounties had to end by **Saturday
31 October**; the text promises the pick **the week of 2 November, on Firefly, with the link**.
Field read **2026-10-28 17:0x EDT** with `query-bounty.py --bounty 1453` plus poidh's
`/base/bounty/<id>/data` for each entrant bounty. **Nothing here has been sent or tapped.**

## The field, measured

| claim | who | their bounty | created (UTC) | its own deadline | resolved | paid to |
|---|---|---|---|---|---|---|
| **8418** | **@assay** (agent, said so) | [1459](https://poidh.xyz/base/bounty/1459) "Show us where you watched ZAOstock from", 0.001 ETH solo | 2026-10-01 05:21 | pay by Fri 9 Oct 11:59pm ET, written in it | by 2026-10-06 04:41 UTC (payout cast) | 8466 @taku0x |
| 8397 | @presdency.eth | [1446](https://poidh.xyz/base/bounty/1446) "Zaostock event", 0.0115 ETH open | **2026-09-27 22:51** | 5 Oct 11:59pm UTC, written in it | vote resolved **2026-10-13 14:50 UTC** | 8515 @leoxcrane |
| 9099 | 0x02c1f87f (no handle) | none: links a GitHub project, "autonomous-micro-entrepreneur" | - | - | - | - |

Round seven was cast 2026-09-29 about 21:17 UTC (`description.md`).

## Against the bar (the round's seven requirements)

**8418 @assay / 1459 - meets every requirement that can be measured.**
- Created after round seven went up, about ZAOstock, links https://zaostock.com, self-funded.
- Ask a stranger can do and prove with a public link: one real photo of the stream, posted with a town.
- Deadline written in the text and kept: paid about three days early.
- A line back to every entrant: the winner reply (cast `0xf8a3f8e2`, 2026-10-06 04:17 UTC, to @taku0x)
  and the payout cast (`0xd8656cb6`, 04:41 UTC) names claim 8465 (@barsam) with its own line.
- Angle is not round six: "everyone who couldn't be there". Two entrants; the winner watched from
  Bulawayo, Zimbabwe.
- Its "map of every watch spot in /zao" promise: the payout cast reads as that post. Not checked
  frame by frame.

**8397 @presdency.eth / 1446 - fails requirement 1 and requirement 6.**
- **Requirement 1, "create your bounty after this one goes up":** 1446 was created
  2026-09-27 22:51 UTC, about two days BEFORE round seven was cast. It was an existing bounty
  claimed into this round, not one made for it.
- **Requirement 6, "pick a winner and pay by your own deadline":** its own deadline was
  5 Oct 23:59 UTC; the vote resolved 13 Oct 14:50 UTC, about eight days late.
- "Every entrant gets one line": no reply found. Searched: @presdency.eth's Farcaster casts
  2026-09-26 to 2026-10-20 (34 casts, Haatz hub) filtered for bounty words. Not searched: X, and
  replies that use none of those words.
- In its favour: it drew three entries, the most of any entrant bounty, and paid the full pot.

**9099 - not an entry.** It links no bounty, so requirement 1 cannot be met.

## Recommendation

**Pick 8418 @assay.** It is the only entry that meets the bar as written, and it is the
"plain bounty run properly" the text says beats a clever one left hanging.

Worth saying out loud before you tap: @assay also won rounds two and eight. That is a pattern
in who shows up, not a reason to mark down this entry. If you would rather spread it, the text
gives you no rule-based way to pick 8397.

## The transaction (Zaal's tap, the week of 2 November)

1. Open https://poidh.xyz/base/bounty/1453 connected as zaal.eth (0x7234...e9af).
2. On claim **8418**, choose submit for vote. Proof: the page shows VOTING with a two-day end time.
3. After the vote ends, anyone can call resolve; until someone does, nobody is paid.
   Proof: `python3 scripts/query-bounty.py --bounty 1453` shows `isAccepted: true` on 8418.
4. Post the pick on Firefly with the link (draft below). Every entrant gets one line.

## Drafts, unsent

Post (under 280):

```
ZAOstock round seven was: run your own bounty for ZAOstock. It goes to @assay.

Clear ask, a deadline written in, a line back to every entrant, and paid three days early. Someone watched from a bed in Zimbabwe.

https://poidh.xyz/base/bounty/1453
```

Line for @presdency.eth (reply under claim 8397):

```
Thanks for running 1446, three people entered and you paid the whole pot. It could not win this round: it was made before round seven went up, and it paid out about eight days past its own deadline.
```
