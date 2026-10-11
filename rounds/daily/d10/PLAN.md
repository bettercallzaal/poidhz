<!-- NOT-ANNOUNCEMENT-COPY: internal plan. Names no deadline anyone submits to. -->
# Round ten plan - best marketing rollout on WaveZStation, $500 pot, $500 buy of the winner, $500 back from the winner

Status 2026-10-10: PLAN, nothing fired. **All three redraft questions are ruled** (`REDRAFT-v3.md` carries the
verbatim rulings: items 103, 106, 108 and 109, relayed by the Grill). The shape is: a month-long marketing
rollout contest for artists with a song on wavezstation.com; sign-up through an email-gated form on the website;
$500 in the poidh pot; Zaal buys $500 of the winning song; the winner must put $500 of the prize back into
WaveZStation, expected on the site, their own song allowed. **His total is $1,000.** He sees the final text
before anything fires. The gates are his: the cast and the $500 pot; the $500 buy and the wallet that sends it;
the invitation DM; every post; switching on the store behind the form.

Every site and chain figure here comes from `RESEARCH.md` beside this file, which names the surface and the clock
time for each one. The one new measurement in this file is the store check (below), made at 20:46Z 10 Oct.

## The round in one paragraph

Artists with a song on WaveZStation sign up by Sunday 18 October (email first, then the form), then run a public
marketing rollout for that one song until Friday 13 November 5:00pm Eastern. They claim on poidh with the record:
the song link, at least five dated public posts, and the song's supporter count and fan pool on sign-up day and
claim day. Zaal picks on the rollout's craft and on what it moved on the site, which this lane measures from the
site's own `/api/discover` and `/api/songs` at a stamp on close day. The winner takes the pot. Within a week Zaal
buys $500 of the winning song from the issuer wallet, which pays the song's creators $225 in the same transaction.
The winner then puts $500 of the prize into a WaveZStation buy of their own choosing, their own song included.

## Money, all three halves

| Who pays | How much | Where it goes | Enforced by |
|---|---|---|---|
| Zaal, into the pot | $500, 0.1995 ETH at 2,506.72 USD per ETH (Coinbase spot 16:06Z 10 Oct; re-read at cast) | the winning artist's wallet, in ETH, when the claim is accepted | poidh, on chain |
| Zaal, from the issuer wallet `0x7234c36a71ec237c2ae7698e8916e0735001e9af` | 500 USDC | the winning song: 50 platform, 225 creators in the same transaction, 225 retained as the song's fan pool | nothing. A promise in the bounty text, outside the pot, verified by Basescan hash after the fact |
| The winner, from the prize | $500 | a buy on WaveZStation, any song including their own: same 50 / 225 / 225 split | nothing. A rule of the round the text says we are trusting them to keep, and will say publicly whether they kept |

If the winner buys their own song, $225 of their $500 comes straight back to their creator wallet in the same
transaction, and part of the $225 fan-pool half is theirs too if they already support their own song. The text
allows this because Zaal ruled it ("can use it on their own"); the plan notes it because the net cost to a
self-buying winner is about $275, not $500, and someone will point that out.

**Zaal's own claimable share.** His buy makes him a supporter of the winning song. On Saturday in LA he already
holds about 21% (170 of about 802 USDC sold); one $500 buy there takes him to about 51% ($670 of about $1,302).
On any other song his existing stake is UNVERIFIED, so the text's disclosure is written for the Saturday in LA
case by name and in general terms otherwise.

**Net cost to Zaal:** $1,000 out, less whatever he later claims from the fan pool of the song he buys. The
fan-pool formula sits in unverified bytecode (`RESEARCH.md` section 2), so that claim-back is an estimate.

## Mechanics, in order

| Step | What | Whose hand | Public? |
|---|---|---|---|
| 1 | Send the invitation (`ARTIST-PITCH.md`) to BennyJ504, and to any other artist he wants in. | Zaal | no, a DM |
| 2 | Decide Q6 (where the form stores on day one). Ask Hurricane, teammate to teammate, to add Zaal to the WaveZStation repo (`HURRICANE-NOTE.md`). The page (PR #247) is built and merged. | Zaal | the form page is public, unlinked until the cast |
| 3 | Paste the form URL into `description.md` and block 2 of `ANNOUNCE.md`; cast the OPEN bounty with $500 in the reward field. | Zaal | yes |
| 4 | Post block 1 from Firefly (Farcaster /zao and X). Block 2 on Friday 16 October. | Zaal | yes |
| 5 | Sign-up closes Sunday 18 October 11:59pm Eastern. This lane stamps each entrant's song from `/api/songs` that night: supporters, pool total, cumulative sales. | this lane | the stamp is published in this folder |
| 6 | Rollout month. Entrants post; nothing for us to do except answer questions. | entrants | yes |
| 7 | Close Friday 13 November 5:00pm Eastern. This lane re-stamps every entrant's song and writes the deltas beside the claims. | this lane | yes, in this folder |
| 8 | Zaal picks with the entries and the deltas in front of him; posts the pick the following week; two-day contributor vote; payout. | Zaal | yes |
| 9 | Within a week of the pick: 500 USDC into the winning song from the issuer wallet. Hash into block 3, post it. | Zaal | yes, the instant it lands |
| 10 | The winner's $500 buy, within a week of payout. Share their hash when they post it; if they do not, say so once. | the winner; Zaal posts | yes |

## The sign-up form, and where the emails go

Three rulings shape this. Item 108: *"Sign up form on website after they put in email"*. Item 111:
*"Hurricane gets it on his database"*. Item 125, 11 Oct, stopping the first note to Hurricane: *"wait not we
are on a team togetehr im on wavewarz / wavezstation aswell"*. So the sign-up store is **a team build, not
a request to a partner**: Zaal is on the WaveZStation team, and the sign-ups belong to that team.

**What exists.** The page is built and merged (PR #247): `poidhz.com/round/10/signup`, email first, then
the form, noindex, unlinked. It checks the song against `https://www.wavezstation.com/api/songs/<id>` and
forwards the row to `SIGNUP_ENDPOINT` over https with a bearer `SIGNUP_TOKEN`. Neither is set, so the page
answers "not switched on yet; nothing was stored".

**What our side can reach, measured 2026-10-11 at 12:40Z.** No WaveZStation repo and no WaveZStation
hosting project is reachable from this lane, and the WaveZStation database is UNKNOWN. The surfaces read,
the counts and what was not searched are in the vault, not in this public repo.

So from this machine nobody on our side can write to the WaveZStation repo or database today. Either
Hurricane adds Zaal to the repo and this lane sends the table and route as a PR for him to merge, or he
says where he would rather the rows go. `HURRICANE-NOTE.md` is now that question, in three sentences,
teammate to teammate.

**The row, for whoever writes the route:** `{round, email, artist, song_id, song_link, handle, where,
recorded_at}`, one per `song_id`, 409 on a repeat, `{ok: true, count}` on success, and a GET with
`?round=10` returning `{count}`. `web/lib/signupstore.ts` is the one function on our side.

**Monday's cast does not have to wait for it.** The open question to Zaal (below) is how the form stores
on day one. The honest constraint: the bounty text is immutable once cast, and rule 1 says where the email
goes, so the wording has to be true on Monday and still true when the rows move.

**The repo rule.** `docs/community-plan.md`: "No email list. Same reason, plus nobody has consented to one."
Held by making this round contact only, said in the bounty text and on both steps of the form, with deletion
at close-out. That deletion is our promise to entrants and ours to keep, wherever the table sits.

## The bounty

- **Type:** OPEN, reward field $500 (0.1995 ETH at 2,506.72 USD per ETH, Coinbase 16:06Z 10 Oct). The paste
  body names no pot amount; every buy figure is in words.
- **Ask:** sign up, run a public rollout for one song for a month, claim with the record and the numbers.
- **Dates:** sign-up closes Sunday 18 October 2026 11:59pm Eastern; submissions close Friday 13 November 2026
  5:00pm Eastern, four weeks after Friday 16 October, the first weekday after sign-up closes. Weekdays checked
  with `date -j` on 10 Oct. "This week" (item 97) is read as the round opening the week starting Monday 12 October.
- **Judging:** half the weight on the measured change in supporters and fan pool from sign-up close to close,
  read off the site at both stamps; half on the rollout itself. Zaal picks; contributors vote; every entrant gets
  one note back.
- **Promises:** the pot; Zaal's $500 buy of the winner, named with the wallet, the week and the hash; nothing
  else. The winner's buy is a rule on the entrant, not a promise by us.
- **Disclosure:** his buy makes him a supporter of the winning song; on Saturday in LA about half. In the text
  under THE REWARD.

## What the record says about this shape

`docs/what-draws-entries-2026-10-01.md` and ZAOOS doc 2522 (re-measured 10 Oct, poidhz #245): the hardest asks
draw the least, and a month-long build is the lowest-entry format on poidh. A sign-up step is a filter, not a
draw. Twenty-seven songs were listed on the site at 16:02Z 10 Oct, so the whole possible field is about twenty
artists, and the plan should expect single digits. The invitation DM is the thing most likely to produce the
first entrant.

## Verification

- **Zaal's buy:** `https://basescan.org/tx/<hash>` shows 500 USDC from the issuer wallet into `0x6eee...b255`,
  then 50 to `0xd974...8E72` and 225 to the song's creator wallet or wallets. Thirty seconds for anyone.
- **The winner's buy:** their own hash, which the text asks them to post. If they buy their own song the same
  page shows 225 going straight back to them, which is fine and is said in advance.
- **The numbers judged on:** this lane's stamps of `/api/songs/<id>` on sign-up night and close day, committed
  in this folder as JSON with the clock time, beside the entrants' own self-reported numbers.

## What could go wrong

- **Nobody signs up.** Twenty artists in the field, a form gate, a month of work. If sign-up closes with fewer
  than three entrants, the default is to run anyway (the text promises nothing about field size) and say so.
- **The winner does not buy.** poidh cannot hold the pot back. The text says it is a rule we are trusting them
  to keep and that we will say whether they kept it. That is the whole enforcement, and the text says so.
- **The winner games the numbers.** Supporters can be bought: a $1 buy from twenty wallets is twenty supporters.
  Half the weight is on the rollout itself, and the deltas are read with the sales total, not just the count.
- **The WaveZStation route is not live by Monday.** That is Q6. Option A starts the rows on our side under
  the same team and moves them later; it needs his yes, because item 111 named Hurricane's database.
- **The email rule.** Someone reads `community-plan.md` and the form as a contradiction. The answer is in the
  text and above: round contact only, deleted at close-out, no list.
- **ETH moves between cast and payout.** The pot is in ETH; "five hundred dollars of the prize" is written in
  dollars. The text does not pin a conversion; the plan reads it as five hundred dollars at the time of the buy.

## Auto-proceeded choices in this PR (one line each)

1. Read "website" as poidhz.com, and the form as a page in the Next app, because that is the site this repo
   deploys and the one with a store already wired.
2. Storage was this lane's default (the site's own store) until item 111 ruled it: Hurricane's database.
3. The form checks the song against `/api/songs/<id>` so only listed songs get through.
4. Five dated posts as the minimum record, because "rollout" has to mean more than one post and five is checkable.
5. Half the judging weight on measured deltas, half on craft, because item 99 said "best marketing rollout" and
   the site gives us the number for free.
6. One week for each of the two buys after the pick and payout, because neither ruling named a time.
7. Addresses deleted at close-out, said in public, because the repo's rule against a list has to mean something.
8. "This week" read as the round opening the week starting Monday 12 October.

## Questions for Zaal: one open

**Q4, where the sign-up emails live.** Ruled item 111 (*"Hurricane gets it on his database"*), then reframed
by item 125: he and Hurricane are one team, so it is a team build. **Q5** was auto-proceeded: PR #247, merged.

**Q6, open, for a Monday 12 October cast: where the form stores on day one.**
- A) The team's store, starting on our side: Zaal connects poidhz.com's own Upstash with one key through
  `/secret`, the form goes live Monday, and the rows move to the WaveZStation database when Hurricane adds
  him to the repo. Rule 1 of the bounty text changes from "WaveZStation's own database" to "the WaveZStation
  team", which is true on both days. This lane restores the Upstash adapter behind the same one function
  (it was written and reviewed in PR #247 before item 111). **Recommended: it is the only path that does not
  hang Monday on someone else's Sunday.**
- B) Wait for the WaveZStation side: send the team note, cast when the route is live. The text stays as it
  is. The cast slips if the route does.
- C) Cast Monday with the form dark: the page says "sign-up opens this week" until the route lands. Nothing
  to build, and the first artists to click find a closed door.

Default if unanswered: nothing is cast, nothing is stored, nothing is sent.

**Open, and his:** the team note to Hurricane; the invitation to BennyJ504; the cast.
