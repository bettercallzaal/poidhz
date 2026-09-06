# Winner announce cast template

Use after the winner is settled on poidh. For an OPEN bounty that runs the vote path, that
means after `submitClaimForVote` + `resolveVote` + the winner withdraws; for a round the
issuer accepted directly, it means after the claim shows `isAccepted: true`. Confirm which
happened with `python3 scripts/query-bounty.py --bounty <id>` rather than assuming.

## Check these two before you paste anything

This template used to state both as facts. Neither is true of every round, and R5 shipped
with neither - a paste-as-is would have promised seven people an airdrop nobody offered.

1. **The $ZABAL trail.** The blocks below carry an optional line saying every submitter
   earned $ZABAL via Empire Builder slot 8. **Only use it if the round's own
   `description.md` actually promised it.** Check with
   `grep -ci zabal rounds/r<N>/description.md` - R5 returns 0. Announcing an airdrop that
   was never offered creates a debt to every entrant on the spot.
   Also note: Empire Builder's leaderboard is currently pointed at a stale endpoint and is
   missing 6 submitters including R3's winner (see the root README). Do not claim a
   submitter "already got" anything without checking EB shows them.
2. **The judging page.** `poidhz.com/round/<N>/judging` only resolves if a judging
   page was actually built for that round. R1-R3 have one; R5 does not. Check that the URL
   returns 200 before putting it in a public post, and drop the line if it does not.

Lines marked `[OPTIONAL - verify first]` are the ones this applies to. Delete them rather
than shipping them unverified.

## Farcaster (long)

```
@<WINNER-HANDLE> won Round <N> of the BCZ x POIDH bounty.

The <ARTIFACT>: <X-URL or POIDH-CLAIM-URL>

<ONE SENTENCE on WHY THEY WON - the specific thing that beat the cohort>. Felt like a real <ARTIFACT-TYPE>, not a clip dump.

Real congrats. Earned it.

<PRIZE> ETH, paid.

[OPTIONAL - verify first] And here is the part that actually scales - every submitter to Round <N> also earned $ZABAL via slot 8 of $ZABAL Empire on Empire Builder. Winning the ETH is the spike. Showing up earns the baseline. That's the whole model.

Full breakdown of all <N-SUBMISSIONS> submissions + rubric scoring + the judging logic:
[OPTIONAL - verify first] - Page: https://poidhz.com/round/<N>/judging
- GitHub: https://github.com/bettercallzaal/poidhz/tree/main/rounds/r<N>

cc @poidhxyz
```

Note on the prize line: say "paid" only once the payout has actually settled. If the
contributor vote is still running, say "<PRIZE> ETH released once the contributor vote
resolves, about 48h on POIDH's open bounty flow" instead.

## X (under 280)

```
@<WINNER-X-HANDLE> / <NAME> won Round <N> of the BCZ x POIDH bounty - real congrats

<ONE-LINE WHY THEY WON>

winner takes <PRIZE> ETH

clip: <X-URL>
[OPTIONAL - verify first] breakdown: https://poidhz.com/round/<N>/judging
```

## Short - Telegram / GC / Discord

```
Round <N> BCZ x POIDH winner: @<WINNER-HANDLE> / <NAME>. Real congrats - earned it.

Winner takes <PRIZE> ETH.

[OPTIONAL - verify first] Every submitter to Round <N> also earned $ZABAL via the $ZABAL Empire leaderboard - submitting is the reward, winning is the bonus.

Clip: <X-URL>
[OPTIONAL - verify first] Breakdown: https://poidhz.com/round/<N>/judging
Source: https://github.com/bettercallzaal/poidhz/tree/main/rounds/r<N>
```

## Reply-cast to winner on the thread

```
brought heat with that <SPECIFIC THING> @<WINNER-HANDLE> - shipping you the next bounty brief direct when Round <N+1> drops, would love to see you defend it
```
