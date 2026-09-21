# To Kenny - the twelve-day ZAOstock ladder

**DRAFT, unsent. Outbound is Zaal's tap.** No SEND-GATE marker, same as the launch bundle -
Zaal lifted that for this thread on 2026-09-20.

**Send after R8 is cast, or alongside it.** He has already shaped R8 twice, and this is the
natural follow-up: here is what we are doing with your advice, and here is what we found in
our own album.

**Why he is worth asking:** both of his interventions so far were right and cheap. "Too meta,
low participation" killed a bad round before it cast. "Completely drained" corrected a figure
we had published. He answers in one line and he is usually correct.

---

## The message

```
Kenny - took your note and ran with it. Two things, one ask.

1. R8 is now the summary bounty you described: best explanation of what poidhz does and what
is actually different about it. Any format. That is live shortly.

2. The bigger thing. ZAOstock is our free festival in Ellsworth, Maine on Oct 3, twelve days
out. Rather than one big promo bounty we are running twelve daily ones off the brand kit, two
a day at $3 each, 24 hours apiece, escalating from "make a poster" to "print it and put it in
a window, photograph the placement" to "invite one person by name". Everything is at
zaostock.com/brand.

The reason it is daily and cheap rather than weekly and fat: across the 99 open bounties on
poidh right now, a stated deadline is the strongest thing we can find. 74% of bounties with a
real date get submissions against 48% without, and it holds inside every prize band. 81% of
the market states no date at all. A 24-hour window is the most legible deadline that exists.

Prize size does the opposite of what we expected. $2-6 draws entries 70% of the time, $6-15
draws 33%. Bounties within $2 of a $10 prize: 2 of 10 got anything.

3. The ask. We pulled the claim counts for the whole wethemmedia album, ours and We Them
Media's, and the gap is bigger than we can explain by the copy alone:

  We Them Media, 13 bounties: 30 claims total, median 1 per bounty
  Ours, 4 bounties:           36 claims total, median 8.5

Same album, same platform, similar or smaller prizes on our side. The only difference we can
point at is that we push every round into channels and they mostly post and move on. If that
is right, distribution is doing nearly all the work and the pot is close to irrelevant, which
would change how anyone should advise a new issuer.

The one that argues against us: WTM X Pizza Day, 0.251 ETH, 14 claims - the biggest prize in
the album AND the most entries. It is also the easiest and most universal ask in it, so we
cannot separate "big prize" from "anyone can do this in five minutes".

You see more bounties than anyone. Does that gap match what you see, or are we reading our
own numbers too kindly? And is there a reason not to run twelve small ones in a row that we
have not thought of - does it look like spam in the feed?
```

## Do not include

- Any figure about the pre-v3 contracts. He already corrected us on that, it is settled, and
  raising it again spends his attention on something finished.
- R5's winner announcement. Zaal, 2026-09-20: "lets not worry about the inner annoucment."

## Numbers in this message and where each came from

Re-verify before sending. All measured 2026-09-20.

| Claim | Source |
|---|---|
| 74% vs 48% deadline effect, holds within every band | `data/bounty-dashboard.json`, 99 open bounties, controls in ZAOOS doc `business/2522-poidh-live-bounty-market` |
| 81% of the market states no deadline | same, 19 of 99 have a parseable date |
| $2-6 = 70%, $6-15 = 33%, 2 of 10 near $10 | same file, finer bands |
| WTM 13 bounties / 30 claims / median 1 | `claims.fetchBountyClaims` per bounty, positive-controlled against R5=9 and R1=11 first |
| Ours 4 bounties / 36 claims / median 8.5 | same endpoint, R1 11, R2 8, R3 8, R5 9 |
| Pizza Day 0.251 ETH, 14 claims | same endpoint, bounty 1169 |
| ZAOstock Oct 3, Ellsworth, 8 acts, noon-six, free | zaostock.com and /artists, read 2026-09-20 |

**One caution on the comparison before it goes out.** WTM's bounties are older, and the
platform itself has grown - 89 open bounties on 2026-09-09 against 99 on 09-20. Some of the
gap could be that the audience was smaller when they ran. We cannot control for it because
`created_at` comes back empty on every row the API returns. The message says "the only
difference we can point at", which is honest, but if he pushes back on it he is probably
right to.
