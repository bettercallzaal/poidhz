<!-- NOT-ANNOUNCEMENT-COPY: the reasoning behind round two's pick and the transaction that sets it. Internal. Names no deadline anyone submits to. -->
# Round two - the pick, the reasoning, and the exact transaction

Prepared 2026-09-23 14:30 EDT. **Nothing here has been sent.** The transaction is Zaal's tap
and the announcement is his to post.

## State, verified rather than taken on trust

Vault relayed Zaal's figures and asked me to check them before acting. They are exactly right:

| | Measured from `poidh.xyz/base/bounty/1410/data` |
|---|---|
| Claims | **8** |
| Accepted claim | **NONE** |
| `deadline` field | **null**, so `submitClaimForVote` has never been sent |
| onChainId | **424** |

## ROUND THREE CANNOT BE REVIEWED YET, AND THAT IS THE BLOCKER

Bounty 1412 has **0 claims** and closes at **5:00pm Eastern**, which is two and a half hours
from this read. There is nothing in it to review.

The brief asked for both rounds reviewed today and posted together. Round two can be decided
now. Round three cannot be decided before it closes, so **"posted together" means after 5pm**,
not this afternoon. That is the one part of the ask that cannot be met as worded, and it is
reported rather than worked around.

## The field, and why the top two are both from one entrant

Full per-entry detail is in `REVIEW.md`. Condensed against the bar as cast:

| Claim | Who | Plays on poidh | What is wrong with it |
|---|---|---|---|
| **8111** | @assay | **yes**, 31.5s, audio | nothing disqualifying (see the Black Moon note) |
| **8107** | @assay | **yes**, 15.0s, audio | nothing |
| 8105 | @joeyofdeus | still only | missing "free" and the venue; stray export artifact |
| 8115 | @pascaline | no | filed a screenshot; the person on camera is UNVERIFIED |
| 8104 | @taku0x | no | CapCut watermark burned in; filed a screenshot |
| 8103 | @barsam | no | filed a screenshot |
| 8099 | @mfa | no | ZABAL Gamez logo instead of the moose; tool watermark; screenshot |
| 8100 | @assay | no | dead host, superseded by 8107 |

**Only two of eight play on the bounty page and both are @assay's.** That is the honest
result. An autonomous agent made the two best pieces in the round, declared itself in every
claim, declared the one rule it could not meet, and fixed its own dead link mid-round without
being asked.

## THE BLACK MOON OBJECTION IS WITHDRAWN

`REVIEW.md` originally held 8111's "BLACK MOON PUBLIC HOUSE, 6 TO 10" against it as an
invented fact. **That was my error.** `zaostock.com/program` publishes exactly that - "from six
(poster: 6 to 10 PM)" - so @assay read it off our own page. The finding was corrected on
2026-09-22 and the correction stands: the number is ours, hedged three ways, and the fix
belongs on the site.

**So 8111 has no remaining objection against it.**

## The pick: 8111

**Recommended, and the reasoning is that it does the thing the round asked for best.**

Round two's cast text said, in capitals: *"WHAT I WANT MOST TODAY: VIDEO WITH AUDIO"*, and
pointed at the kit's own audio. 8111 is the only entry that used **Zaal's own voice** - the
Star 97 radio interview cut to nine passages and captioned word by word - with the eight acts
named in running order as he says them, a progress rail through 01 to 08, and credits to
attabotty and Star 97 in the footer. 1080x1920, 29.6s of it carrying the full fact bar.

**8107 is the alternative** and is defensible: tighter at 15s, uses the 30-second spot, nothing
on it is wrong. If the preference is the piece most likely to be watched to the end, it is
8107. If the preference is the best advertisement for what the kit can do, it is 8111.

**@joeyofdeus (8105) is the strongest entry from a human** and the only non-assay entrant who
filed the piece rather than a photograph of a post. It is missing "free" and the venue, which
is why it does not win, and that is exactly what his note will say.

## THE ONE JUDGEMENT THAT IS ZAAL'S, NOT MINE - RULED 2026-09-23 16:48 EDT

Both top entries are from the same entrant, and that entrant is an autonomous agent. He has
already ruled agents eligible, and round three's immutable text says so publicly. Nothing in
the bar excludes this outcome.

But a run whose stated purpose is building a roster of people who make things regularly may
want to weigh that an agent taking round two changes what the other ten entrants read. **That
is a call about the programme, not about the work**, and it is his.

### HE RULED. ROUND TWO GOES TO @assay, AND THE REASONING IS NOT MINE

At 16:10 Zaal said he would rather not reward an agent. At 16:48, after showing the piece to
Kenny, he reversed - and the argument that moved him came from Kenny, in the ZAOstock
Telegram:

> **Kenny, 16:47:** *"naw man you know some human put a lot of work into that agent"*
> **Kenny, 16:47:** *"so still you rewarding a human haha"*

Zaal's own words either side of it: *"I can't find a better human video"*, then *"Valid valid
yeah"*. Both messages carry his heart reaction.

**This resolves the tension rather than ignoring it.** 1412's immutable text promises agents
are judged on the same bar as everyone else, and this honours that. The thing he wanted -
humans learning rather than an agent farming the run - becomes the NEXT bounty's job, which
he announced in the same breath: *"Tbh imma make an agent only bounty next, with my other
bounty."*

**The earlier recommendation stands unchanged: 8111.** It was the recommendation before the
ruling and the ruling does not alter which of @assay's two is better.

The human alternative, now superseded rather than wrong: **8105 @joeyofdeus**, on the grounds
that he filed the piece itself when six of eight did not. He is still the strongest human
entry and that belongs in his note.

## The transaction, ready to fire

**Zaal sends this. A lane does not, and a lane does not hand it to another lane that could.**

- **Chain:** Base (8453)
- **Contract:** `0x5555Fa783936C260f77385b4E153B9725feF1719`
  (verified: 39,368 chars of bytecode at that address; a control address returns none)
- **Function:** `submitClaimForVote(uint256 bountyId, uint256 claimId)`
- **Selector:** `0x9e9251c8` (computed from the signature, matches the repo's record)
- **From:** the treasury wallet that issued the bounty, `0x7234c36a71ec237c2ae7698e8916e0735001e9af`

**Arguments - these are ON-CHAIN ids, not poidh ids, and getting that wrong picks a stranger's
entry:**

| For the pick | bountyId | claimId |
|---|---|---|
| **8111 (recommended)** | **424** | **2795** |
| 8107 (alternative) | 424 | 2791 |
| 8105 (if a human is preferred) | 424 | 2789 |

**Why that warning is not theoretical.** Building this, I called `fetchBountyClaims` with
`bountyId: 424` - the on-chain id - and it returned **23 claims from somebody else's alpaca
drawing bounty**, because that endpoint takes the POIDH id. Had I not read the output, the
transaction would have pointed at a stranger's claim. The poidh id is 1410; the on-chain id is
424; they are different numbers for the same bounty and both appear in the same tooling.

After it lands, a **two-day contributor vote** runs, then `resolveVote(uint256)` and the winner
withdraws.

## The easier route

poidh's own UI has an accept/submit-for-vote button on the bounty page for the issuer. If that
works, use it - it builds the same call and there is no id to mistype. The raw transaction
above is the fallback if the button is missing or fails.
