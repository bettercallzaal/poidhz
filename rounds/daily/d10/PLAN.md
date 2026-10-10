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
| 2 | Build the sign-up form on poidhz.com (Q5) and switch on the store behind it (Q4, a key through `/secret`). | this lane builds; Zaal switches on | the form page is public once deployed |
| 3 | Paste the form URL into `description.md` and block 2 of `ANNOUNCE.md`; cast the OPEN bounty with $500 in the reward field. | Zaal | yes |
| 4 | Post block 1 from Firefly (Farcaster /zao and X). Block 2 on Friday 16 October. | Zaal | yes |
| 5 | Sign-up closes Sunday 18 October 11:59pm Eastern. This lane stamps each entrant's song from `/api/songs` that night: supporters, pool total, cumulative sales. | this lane | the stamp is published in this folder |
| 6 | Rollout month. Entrants post; nothing for us to do except answer questions. | entrants | yes |
| 7 | Close Friday 13 November 5:00pm Eastern. This lane re-stamps every entrant's song and writes the deltas beside the claims. | this lane | yes, in this folder |
| 8 | Zaal picks with the entries and the deltas in front of him; posts the pick the following week; two-day contributor vote; payout. | Zaal | yes |
| 9 | Within a week of the pick: 500 USDC into the winning song from the issuer wallet. Hash into block 3, post it. | Zaal | yes, the instant it lands |
| 10 | The winner's $500 buy, within a week of payout. Share their hash when they post it; if they do not, say so once. | the winner; Zaal posts | yes |

## The sign-up form, and where the emails go

Zaal ruled (item 108): *"Sign up form on website after they put in email"*. He did not say which website. This
lane reads it as poidhz.com, because that is the site this repo deploys and the round's own surface. Two findings
shape the build:

1. **poidhz.com has one store and it is off.** The site is the Next app in `web/`, which already carries an
   Upstash Redis store (`web/lib/votestore.ts`, from PR #223) for community votes. The live endpoint
   `https://poidhz.com/api/vote?bounty=1421` returned `"storeReady": false` at 20:46Z 10 Oct, so no
   `KV_REST_API_*` or `UPSTASH_*` token is set on the Vercel project. A form that posts to the site today has
   nowhere to write.
2. **The repo says no email list.** `docs/community-plan.md`: "No email list. Same reason, plus nobody has
   consented to one." A round sign-up is not a list, and the form and the bounty text both say the address is
   used to reach entrants about this round only. That is the line this lane holds: no newsletter, no export into
   a mailing tool, no reuse for round eleven without asking again.

**Proposed build (Q5):** a page at `poidhz.com/round/10/signup`, in the Next app. Step one asks for an email
and nothing else. Step two, shown after a valid email, asks for artist name, the song's WaveZStation link (checked
against `/api/songs/<id>` on submit, so only a listed song gets through), the X or Farcaster handle, and where the
rollout will be posted. One row per song. The page shows the count of sign-ups, never the names or addresses.

**Where the emails are stored, and who can read them (Q4, the default):** in the site's own Upstash Redis
database under the key `signup:d10`, the same store the vote endpoint uses, once Zaal connects it. Who can read
that store: whoever holds the Vercel project's environment variables, which is Zaal and anyone he has added to
the Vercel project (UNVERIFIED who that is from this lane; the repo does not record it), and the Upstash account
that owns the database. Nothing in the public repo, nothing in a deploy preview, nothing in git. This lane reads
the rows only through a route protected by a token he sets, to stamp each entrant's song. The addresses are
deleted from the store after the round closes out, and the plan says so in public so entrants can hold us to it.

The alternative is a Tally or Google form embedded on the page, which puts the addresses on that vendor's
servers under Zaal's account and needs no key here. It is faster and it is not "on the website" in the way he
said it. Q4 asks which.

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
- **The store never gets switched on.** Then there is no form on the website and the fallback is a vendor form
  (Q4 B). Nothing casts until a sign-up URL exists.
- **The email rule.** Someone reads `community-plan.md` and the form as a contradiction. The answer is in the
  text and above: round contact only, deleted at close-out, no list.
- **ETH moves between cast and payout.** The pot is in ETH; "five hundred dollars of the prize" is written in
  dollars. The text does not pin a conversion; the plan reads it as five hundred dollars at the time of the buy.

## Auto-proceeded choices in this PR (one line each)

1. Read "website" as poidhz.com, and the form as a page in the Next app, because that is the site this repo
   deploys and the one with a store already wired.
2. Default storage: the site's own Upstash store, switched on by Zaal, not a vendor form (Q4 asks).
3. The form checks the song against `/api/songs/<id>` so only listed songs get through.
4. Five dated posts as the minimum record, because "rollout" has to mean more than one post and five is checkable.
5. Half the judging weight on measured deltas, half on craft, because item 99 said "best marketing rollout" and
   the site gives us the number for free.
6. One week for each of the two buys after the pick and payout, because neither ruling named a time.
7. Addresses deleted at close-out, said in public, because the repo's rule against a list has to mean something.
8. "This week" read as the round opening the week starting Monday 12 October.

## Questions for Zaal (the Grill carries them; none blocks the copy)

**Q4. Where the sign-up emails live.**
- A) The site's own Upstash store, which you switch on with the Vercel integration or a token through `/secret`.
  Readable by you and whoever is on the Vercel project; deleted at close-out. **Recommended: it is on the
  website, as you said, and under your account.**
- B) A Tally or Google form embedded on the page. On the vendor's servers under your account. No key needed here.
- C) Something else; type it.

**Q5. Build the form now?**
- A) Yes, this lane opens a separate PR with the page and the API route, held unlinked until you cast.
  **Recommended.**
- B) Not yet; cast only after the form exists and it is built later.
- C) No form on the site; use B above.

Default if unanswered: nothing opens, nothing is bought, nothing is posted, nothing is built.
