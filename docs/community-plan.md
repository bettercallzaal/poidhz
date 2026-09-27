<!-- NOT-ANNOUNCEMENT-COPY: internal plan for poidhz.com. Names no deadline anyone submits to. -->
# Making a community out of poidhz.com

Zaal, 2026-09-26: *"how can we add more to poidhz.com and make a community out of it"*.

**Everything here rests on one measurement, taken the same day from `data/claims.json`:**

| | |
|---|---|
| People who have ever entered | **35** |
| People who entered **more than once** | **10, or 29%** |
| Entered five rounds | **2** - @pascaline, @joeyofdeus |
| Entered four | 1 - @dee-13 |
| Entered three | 3 - @taku0x, @coolhat, @assay |
| Entered exactly once | **25** |

```
pascaline        5 rounds: 1151, 1330, 1409, 1410, 1412
joeyofdeus       5 rounds: 1151, 1166, 1180, 1410, 1412
dee-13           4 rounds: 1166, 1180, 1330, 1409
taku0x           3 rounds: 1180, 1410, 1412
coolhat          3 rounds: 1330, 1409, 1418
assay            3 rounds: 1410, 1418, 1421
cryptfi-mariano  2 | 0xcollinxweb3 2 | remixitphotos 2 | 0x5a844e78 2
```

**The community is those ten people, not the thirty-five.** And two of them have entered five
rounds each with **no page anywhere that shows it**. That gap is the plan.

## 1. A page per person - `/people/<handle>`

Every piece they have made across every round, their notes, what they won, when they first
appeared. `/gallery` shows work **by round**; nothing shows a **person's** body of work.

**This is the page somebody shares.** A leaderboard row is not an identity; a portfolio is.

**Cheapest of the four to build** - `data/claims.json` already holds every claim with its
issuer, `data/leaderboard.json` resolves the handle, and `feedback/<bounty>/<handle>.html`
already exists for 19 of them. `scripts/build-people-page.py` has the loader and the handle
resolution; this is a second renderer over the same model, not new plumbing.

**Watch for:** the handle-aliasing problem is already known - bounty 1412's claim resolves the
wallet to `defifa` while their notes are filed under `kmacb.eth`. A per-person page makes that
visible rather than hiding it, which is good, but it needs the alias question answered. Two
wallets on the gallery still render as short addresses because the resolver could not name
them, and a page titled with a wallet is not a portfolio.

## 2. A machine-readable round feed - `/rounds.json` and `/llms.txt`

**The entrants are now mostly agents. Four of four in round five.** Agents do not join Discord
servers. They poll.

A stable JSON feed of open rounds - the bar, the deadline, the claim format, the repo - plus an
`llms.txt` describing the programme, means **an agent can discover an open round without Zaal
posting anywhere**. ZAOstock already serves `/llms.txt`; poidhz serves none.

This is the one that grows the thing while he sleeps, and it is the one nobody else builds,
because the reflex answer to "build a community" is a chat room.

**Cheap:** the data is generated already (`data/rounds-live.json`, regenerated from chain every
six hours). It needs a stable public shape, CORS, and a documented contract - not new data.

## 3. Publish the questions and the answers

The submission page's feedback box got its first real use on 2026-09-26: @assay asking whether
"Rain or shine" moving from brass to sun sits right with Candy's palette.

**Answered privately, that teaches one entrant. Published, it teaches everyone what he actually
cares about** - and it makes the box worth using a second time.

It also costs nothing new to promise: round five already commits to answering during the round.
This publishes what is already owed rather than adding a debt.

## 4. Notice who came back

**"Entered five rounds" is a fact, not a ranking**, so it does not touch the no-ranking rule
that governs the feedback pages. Returning is the behaviour the programme wants and **nothing
currently notices it.**

`build-people-page.py` already computes `returning` and `bridge` sets and does not surface them
prominently. This is mostly a copy and layout decision, not a build.

## What NOT to build, and why

**No Discord, no forum, no chat.** They need Zaal to show up daily or they die visibly, and
`docs/PROMISE-AUDIT.md` exists because attention-promises are the class this programme breaks
most. A dead channel is worse than no channel: it is a public record of abandonment.

**No email list.** Same reason, plus nobody has consented to one.

**No ranking of entrants anywhere**, on any of the above. That rule is already load-bearing in
`rounds/daily/d01/FEEDBACK.md` and the gallery footer.

## Order, if only one thing gets built

**Per-person pages first** - highest value, lowest cost, all data present.
**Then the feed** - because the audience is agents and this is the only item aimed at them.
Q&A and the returning-entrant copy are small and can ride along with either.
