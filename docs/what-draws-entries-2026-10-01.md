<!-- NOT-ANNOUNCEMENT-COPY: internal research memo. Names no deadline anyone submits to. -->
# What has drawn entries, and what has not - the record to 1 October 2026

Zaal, 2026-10-01, in the poidhz pane: *"research and talk with poidhz terminal about what has
been done in past and what has worked well for getting submissions"*. This is that answer,
built only from what this repo already measured. Every number names the file it came from.
Nothing here was re-measured on chain today except the issuer wallet (0.000107 ETH, two Base
RPCs, 09:33 EDT), so the claim counts are as `data/claims.json` stood at the last cron refresh.

## Our own eleven rounds, by claims

From `data/claims.json`, one row per claim, wallets deduplicated per bounty:

| Bounty | Round | Ask shape | Window | Claims | Wallets |
|---|---|---|---|---|---|
| 1151 | R1 | 60 s clip from an episode | ~1 week | 10 | 10 |
| 1166 | R2 | 60 s poidh ad from an episode | ~1 week | 8 | 8 |
| 1180 | R3 | ZABAL Gamez ad, any format | ~2 weeks | 8 | 8 |
| 1249 | R4 | July open build pot | month | 0 (canceled at closeout) | 0 |
| 1330 | R5 | 60 s clip from a Twitch stream | ~2 weeks | 7 | 7 |
| 1409 | Daily 01 | one piece of media, posters mostly | 1 day | 6 | 6 |
| 1410 | Daily 02 | one piece of media, video asked for | 1 day | 6 | 6 |
| 1412 | Daily 03 | anything but a poster | 1 day | 4 | 4 |
| 1418 | Daily 04 | 30 s ad | 1 day | 6 | 6 |
| 1421 | Daily 05 | ship code, not a poster | ~2 weeks | 7 | 7 |
| 1453 | Daily 07 | run your own bounty | 5 days | 2 | 2 |

Reading it plainly:

- **Clip rounds built on OUR OWN source audio or video are the most reliable shape we have
  run.** R1, R2 and R5 all handed entrants a recording and asked for a cut; they drew 10, 8
  and 7 wallets at one to two week windows. Daily 02 did the same with the September radio
  interview in a one-day window and drew 6, and its winner (@assay, claim 8111) was a cut of
  that interview: 31 s, 1080x1920, nine captioned passages, every act named in running order
  (`rounds/daily/ANALYSIS.md`). Round eight is this shape again on fresh audio.
- **The hardest asks drew the least.** Daily 07 asked people to create and run their own
  bounty and has 2 claims after two days. R4 asked for builds and ended with none paid. Daily
  05 asked for code and drew 7, but across two weeks and mostly from agents (four of four in
  the first wave, `docs/community-plan.md`).
- **One-day windows cost about a third of the field against week-long ones** (6, 6, 4, 6
  against 10, 8, 8, 7), but they are the only cadence that lands before a fixed date, and
  every daily pot grew in public while it ran. For a festival two days out, the window is not
  a choice.

## The levers, measured on the wider market

From `rounds/RATING.md` (99 open bounties, 2026-09-20, ZAOOS research doc 2522) and
`docs/how-bounties-got-shared-2026-09-21.md` (600 completed Base bounties, 179 issuers):

| Lever | Effect | Confidence |
|---|---|---|
| **A stated deadline** | entries roughly double: 74% with-submissions against 48% | survives controls for format and prize band |
| **Format** | photo 68%, clip 64%, build 52%, code 43%, social 33% | pattern, uncontrolled for age |
| **Prize size** | none. Under $5 runs 69%, $50 plus runs 43%. $6 to $15 is the dead band at 33% | pattern, n=21 for the dead band |
| **Someone other than the issuer boosted the pot** | median 5.5 entries against 1.5, and 35% reach ten entries against 17% | n=552, direction unknown |
| **Naming ONE room to post the entry in** | median 11.5 entries against 3 | n=10, suggestive |
| **Asking for a link back to your post** | nothing: 24% against 26% reach ten | useful null, n=600 |
| **Inverting the ask ("worst ad")** | 66 entries for Hivemind's worst-ad bounty | n=1, an idea |

## What our own rounds showed about rules and people

From `rounds/daily/ANALYSIS.md` and `docs/community-plan.md`:

- **A mandatory tag-both-platforms rule excluded five of eight entries in round two.** It
  moved behaviour from 0 of 6 to 3 of 8 and still disqualified most of the field. Tagging is
  worth asking for and worth making optional.
- **poidh's uploader takes images only (every upload goes to IPFS).** Three rounds of
  "they filed a screenshot" turned out to be the platform, not the entrants. The rule that
  works: upload one frame, link the piece. Kenny confirmed it 2026-09-23.
- **A near-universal miss was ours three times:** the upload rule above, a hedged end time
  we marked people down for repeating, and a sync bug that left nine R5 claimants scoring
  zero. Check the instrument before the entrants.
- **The community is ten people, not thirty-five.** 10 of 39 wallets have entered more than
  once. Six have entered three or more rounds: @joeyofdeus (6), @pascaline (5), @dee-13 (5),
  @taku0x (4), @assay (4), @coolhat (3). Three of them have cut video from our own audio
  before. These six are the people a new clip round should reach directly, by name.
- **Both channels produce.** Round one's entries split 3 X and 3 Farcaster. Every late entry
  came from Farcaster; every X entry was on time. Two cases, a thing to watch.
- **Improvement happened without feedback, retention did not.** The two most improved
  entrants improved on their own inside a round; exactly one round-one entrant returned for
  round two before any notes went out. Notes are for keeping people, not for the first entry.
- **Pots grow when people can see them.** Bounty one went from 0.004 to 0.0061 ETH during
  its own vote, unasked. Kenny has boosted every BCZ round he was told about.

## What this means for round eight, applied

1. **Shape: a cut of our own audio, clip format, one-day window, stated close.** The best
   three levers we have, all free. Done in `rounds/daily/d08/description.md`.
2. **Reward in the $2 to $6 band**, not $10. Suggested 0.0019 ETH. Done.
3. **Name one room.** The description now says: post the cut in /zao on Farcaster, or tag
   @bettercallzaal on X, and that the room is where entries will be seen. Optional, so it
   never disqualifies anyone. Done.
4. **Get it boosted within the hour.** Kenny first; the DM is in
   `rounds/_template/cast-templates/catalytic-dm.md`. Zaal sends. Listed in `ANNOUNCE.md`.
5. **DM the six returners by name with the bounty link.** Three have already cut video from
   the kit's radio interview. Zaal sends; the list and a two-line DM are in `ANNOUNCE.md`.
6. **Do not require two tags, do not require a video upload, do not write a number in the
   text.** All three have cost entries before. Done.
7. **Send every entrant a note the same evening**, and point the note at the next round.
   Written into the description as "everyone who enters gets a note back".

## What this memo does not know

- Promotion data. How other issuers pushed their bounties on X and Farcaster was never read;
  the API keys were refused on 2026-09-21. Everything about boosting and rooms is about set-up.
- Whether the one-room effect holds for an Instagram deliverable, where the room and the
  destination are different platforms. n=10 was all on Farcaster.
- The current claim counts for 1421 and 1453 on chain; the table reads the committed JSON.
