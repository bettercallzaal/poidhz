<!-- NOT-ANNOUNCEMENT-COPY: internal ledger of open work across the poidhz programme. Names no deadline anyone submits to. -->
# Open ledger - every unfinished thing in the poidhz programme

Built 2026-09-23 16:2x to 16:4x EDT. **Every number below was measured in this pass with the
command named beside it.** Nothing is restated from an earlier handoff, because round three
was still receiving claims while this was written.

## The clock, which is what orders everything

| Time tonight | What happens | Whose hand |
|---|---|---|
| **17:00:00 EDT** | Round three (1412) closes as cast. Stated deadline only - poidh has no on-chain submission cut-off. | nobody - it just passes |
| **22:00:17 EDT** | Round one's (1409) contributor vote deadline. Measured from its `deadline` field, `1790215217`. | Zaal fires `resolveVote` |

Everything else in this file has no deadline attached to it, which is the exact shape
`docs/PROMISE-AUDIT.md` says rots quietly.

## Live state of the three bounties

Read at **2026-09-23 16:20:25 EDT** with `python3 scripts/claim-report.py --bounty N --json`
and `curl -s https://poidh.xyz/base/bounty/N/data`.

| poidh | on-chain | claims | accepted | `deadline` | pot now | state |
|---|---|---|---|---|---|---|
| **1409** | 423 | 6 | none | `1790215217` | 0.0061 ETH | vote running to 22:00:17 tonight |
| **1410** | 424 | 8 | none | **null** | 0.005 ETH | closed, unjudged, `submitClaimForVote` never sent |
| **1412** | 426 | 4 | none | **null** | **0.005 ETH** | open until 17:00 today |

**1412's pot has grown.** `rounds/daily/d03/description.md:68` records 0.004 ETH at cast; the
live amount reads `5000000000000000` wei. Either 0.001 ETH was contributed after casting or the
cast figure was mis-recorded. Not resolved here - it wants a look at the on-chain deposits.
This is the number bounty two's round lost forever, so it is worth settling while it is cheap.

## FIVE THINGS THIS REVIEW FOUND THAT WERE NOT KNOWN BEFORE

### 1. All four round-three claims uploaded a still. Again.

Every `media_url` resolves to metadata JSON whose `image` is a **JPEG**:

| claim | on-chain | who | uploaded | what it actually is |
|---|---|---|---|---|
| 8145 | 2829 | @taku0x | 574x1280 JPEG | screenshot of his X post, 20:49 23 Sept from Bulawayo, 13 views |
| 8147 | 2831 | @joeyofdeus | 719x804 JPEG | screenshot of a Farcaster cast carrying a 0:16 video |
| 8149 | 2833 | @pascaline | 606x1280 JPEG | screenshot of an X post carrying drone footage of the real parklet |
| 8150 | 2834 | @pascaline | 606x1280 JPEG | screenshot of an X post **timestamped 8:39 PM 22 Sep** |

That is **54 claims across four bounties and not one uploaded video.** Rule 1 asked for the
file itself AND a link; everyone linked. Zaal already settled the judging side of this - "claim
having a link to video is ok" - so the rule is fine and the platform question is still open.
**Resolve every one of these to the linked post before rating it.** Rating the JPEG is exactly
the error that scored @taku0x 4/10 for an 8/10 video.

### 2. @pascaline filed twice, and the rule as cast judges the weaker one

1412's immutable text, line 121: *"If you already claimed, claim again; the later one is the
one judged."*

- **8149** (on-chain 2833) is new work: "ONE SATURDAY, CARS GIVE WAY TO MUSIC" over drone
  footage captioned "THE ACTUAL PARKLET", with the full fact bar - Saturday October 3 2026,
  Franklin Street Parklet, Ellsworth Maine, Noon to 6, Free.
- **8150** (on-chain 2834) is **later**, and its post is dated **8:39 PM on 22 September** - it
  is the piece she made for round two, the same X post she linked in round-two claim 8115.

So the rule as written discards her new piece in favour of a re-post from the night before.
The metadata differs (different IPFS objects, different wording) so this is not a duplicate
claim in the mechanical sense - it is the same underlying post being re-entered. **This is a
judgement call and it is Zaal's**, because the rule is immutable and honouring it literally
costs her the round.

### 3. `check-copy-counts.py` now fires a FALSE POSITIVE on round three's cast text

```
FAIL: description.md:126 says "Fourteen entries from eleven" but no bounty has 14 claims
      and the two-round total is 18. Live: [4, 6, 8, 18].
```

The sentence is **correct**: 1409's six plus 1410's eight is fourteen, which is what it says.
The checker adds **1412's own four claims** into the total it validates against, so a round
describing the rounds before it fails the moment it starts receiving entries of its own.

**The fix:** exclude the round's own `bounty_id` from `valid` before checking its copy. It is
the same failure mode the script's own header warns about - a checker that flags correct copy
trains its reader to ignore it, which is why `BARE` was narrowed once already.

### 4. The repo's own header contradicts the text we cast

`rounds/daily/d03/description.md:12` reads *"Pick: named live on Twitch around 5pm Eastern"*.
The cast body at line 141 says the opposite, deliberately: *"I said I would name the round two
pick on stream and I did not, so I am not promising a stream again - I post it on Firefly."*

Line 12 is local notes, not cast text, so nothing public is wrong. But it is the line a future
session reads first, and repeating a retracted stream promise is how the original one happened.

### 5. There is still no pre-party anywhere we can point at - and the site calls it an AFTER-party

Fetched 16:3x EDT: `zaostock.com/`, `/program`, `/artists`, all HTTP 200. Controls pass - each
page returns a hit for "Black Moon", "Franklin", "Parklet", "Ellsworth", "6 to 10".

- **"pre-party", "preparty", "pre party", "September 26", "Sept 26", "9/26": zero hits on all
  three pages.**
- What the site does publish, in JSON-LD: the festival runs **2026-10-03 12:00 to 18:00 -04:00**,
  and a second event, *"ZAOstock 2026 - the evening at Black Moon Public House"*, starts
  **18:00** with **no end time in the structured data**. The prose calls it *"The ZAOstock
  after-party at Black Moon Public House, with a DJ, run by Steve, from six (poster: 6 to 10
  PM)"*.

**I did not search Farcaster, Telegram, Discord or the ZAO Twitter.** `luma.com/zao` returned
200 but its event list is not in the served HTML - the string "ZAOstock" does not appear in the
bytes at all - so that page proves nothing either way and is recorded as UNKNOWN rather than
as an absence.

Standing consequence, unchanged: writing "4pm Eastern at the ZAOstock pre-party" into an
immutable bounty commits to an event nobody outside the room can look up. That is the Black
Moon shape, where two entrants repeated a time off our page and I then blamed them for it.

## The ledger

### Tonight, in order

| # | Item | Owner | Blocked on |
|---|---|---|---|
| 1 | **1412 closes 17:00.** Re-read claims at the close - it went 0 at 12:13, 1 at 15:27, 4 at 16:20. | lane | the clock |
| 2 | **Resolve every round-three claim to its linked post** and rate the media, not the screenshot. | lane | item 1 |
| 3 | **Round two's pick.** `submitClaimForVote(424, <claim>)`, selector `0x9e9251c8`. 8111 -> 2795, 8107 -> 2791, 8105 -> 2789. Reasoning in `rounds/daily/d02/PICK.md`. | **Zaal** | his call on agent vs human |
| 4 | **Round three's pick.** Same call against bounty **426**: 8145 -> 2829, 8147 -> 2831, 8149 -> 2833, 8150 -> 2834. | **Zaal** | items 1 and 2 |
| 5 | **The joint announcement**, both rounds at once, on Firefly. Promised in 1412's immutable text. | **Zaal** | items 3 and 4 |
| 6 | **`resolveVote(423)` at 22:00:17**, then round one's winner withdraws. | **Zaal** | the clock |

Round one's vote tally is **not readable** from the bounty's `/data` endpoint - no vote fields
are present in the 7,724 bytes it returns. Whether the vote has enough participation to resolve
the way we expect is UNKNOWN from this surface, and wants the contract read before 22:00.

### Owed to entrants, and overdue

| Item | Promised where | State |
|---|---|---|
| **Round two's feedback pages** - 8 entrants | 1412's cast text: *"Everyone who enters gets written notes... They all go up at poidhz.com/feedback"* | **nothing exists.** `data/feedback/` holds only `d01.json` |
| **Round three's feedback pages** - 4 and counting | same sentence | **nothing exists** |
| Round one's pages | same | **live**, 5 pages at `/feedback/1409/` |
| @leoxcrane has no round-one page | he won 1409 | 6 claims, 5 pages - deliberate or dropped, unrecorded either way |
| **@assay's note**, asked for at 00:05 | direct request | drafted, unsent |
| **"On Farcaster tag @zaal, not @bettercallzaal"** | the cast text tags a handle the fname registry has no record of | drafted, unsent |
| **R3's winner announcement** (femmie) | R3's cast text, "by end of day Monday June 15" | unsent since June. `docs/PROMISE-AUDIT.md:57` |
| **R5's winner announcement** | R5's cast text | unsent, 17 days. `rounds/r5/winner-announce.md` |

The build path exists and is proven: edit `data/feedback/dNN.json`, run
`python3 scripts/build-feedback-pages.py --round dNN`, then `python3 scripts/sync-site-nav.py`.
The builder refuses ranking words, promises, and any page naming another entrant. Its staleness
check passes today on all five live pages.

### The two new bounties Zaal asked for, and what each is blocked on

**Human round - "make an ad for ZAOstock", closes Saturday 26 September, winner named 4pm
Eastern.** Blocked on one fact: the pre-party is not published anywhere we can cite. Two ways
out, both fine - publish it on zaostock.com first, or write *"4pm Eastern Saturday"* into the
bounty and put the pre-party in the post, where it can be corrected.

**Agent round - agents only, runs to Saturday 3 October, unlimited resubmissions, entrants must
take feedback and resubmit.** No blocker. One constraint that is not negotiable: **this split
cannot be applied backwards to 1412**, whose immutable text says *"ANYONE CAN ENTER, INCLUDING
AGENTS... You are judged on the same bar as everyone else."* Round two never mentioned agents,
so preferring a human there is a live option rather than a broken promise.

### Repo and tooling

| Item | Effort | Why it matters |
|---|---|---|
| Fix `check-copy-counts.py` to exclude the round's own bounty | small | it fails a correct sentence today |
| Fix `rounds/daily/d03/description.md:12` - it says Twitch, the cast says Firefly | one line | it is the line a future session reads first |
| Settle 1412's 0.004 vs 0.005 ETH | small | round two's pot growth is unknowable because nobody did this |
| `check-round-copy-agrees` fails 3 of 16 rounds | small | all three are templates and drafts with `{{DEADLINE_DATE}}` placeholders. Noise that teaches people to skip the output |
| Ask Kenny whether poidh's uploader accepts video | a message | 54 claims, zero video uploaded. Still UNPROVEN that the uploader rejects it |
| Research: the voice agent, roughly $1/min | research | Zaal's own ask, held by the Dotfiles seat |
| Research: Farcaster mini app with wallet auto-login for comments | research | same |

### Site, measured rather than assumed

`poidhz.com/`, `/feedback/1409/` and `/about` all return 200. `check-external-links.py` reports
**45 of 45 external links across 16 pages answering**, with its live and dead controls behaving.
`check-tracked-bounties.py` passes: every cast bounty is tracked and every cast round sits in
`rounds` rather than `planned_rounds`. `build-feedback-pages.py --check` passes.

## What is still unknown, named on purpose

- Round one's vote tally and whether it resolves cleanly at 22:00:17.
- Whether poidh's uploader rejects video or entrants simply never try.
- Whether a ZAOstock pre-party exists on a surface I did not read - Farcaster, Telegram,
  Discord, or luma, whose page I could not read at all.
- Whether 1412's extra 0.001 ETH is a contribution or a mis-recorded cast amount.
- Whether @leoxcrane's missing feedback page was a decision or an omission.
