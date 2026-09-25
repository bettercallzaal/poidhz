# Round five - promo copy, unsent

**NOTHING HERE HAS BEEN POSTED.** Zaal posts. Written 2026-09-25 against the cast text in
`description.md`, which passes `validate-bounty-description --kind code`, `check-render-safe`
and `check-copy-counts`.

## This round needs different channels and that is the whole point

Rounds one to four went to people who make media. **This one goes to people who build agents**,
and they are not in the same places. Four blocks below are for audiences the previous rounds
never touched. If round five gets posted in exactly the same three places as round four, it
will get the same three entrants and the split will have been for nothing.

## Replace `<BOUNTY-URL>` before posting

A real poidh bounty URL is 34 characters - `https://poidh.xyz/base/bounty/` is 30 and a
four-digit id makes 34. **No example id is written here on purpose:** an earlier draft of round
four's copy used a plausible-looking one and it turned out to be a real, live bounty belonging
to a stranger.

Lengths below are measured against 34, not against the 12-character placeholder.

## Block 1 - Farcaster, the main one

Tag **@zaal**, not @bettercallzaal - there is no bettercallzaal on Farcaster.

```
New bounty, and this one is for agents.

Open a pull request against the ZAOstock repo that makes the site visibly better, or makes the repo better to work in. Claim it with the PR link.

Public, MIT, TypeScript and Next.js. You need no credentials - clone it, npm ci, and typecheck, lint, test and build all run with no secrets, which is exactly what CI does on your PR.

An OPEN pull request is a complete entry. It does not have to be merged to win, because whether you can win should not depend on how fast I review. Merged wins ties.

Closes 5pm Eastern Monday October 5. Everyone who enters gets written notes.

https://github.com/ZAODEVZ/ZAOstock

<BOUNTY-URL>
```

## Block 2 - X

**343 characters with a URL, so this needs a premium account.** Use block 3 otherwise.
(I wrote 310 here first from an estimate; measured it was 342; moving the close to Monday made
it 343. Three hand-counted lengths have been wrong in this repo. Measure, then write the
number, and measure again after any edit.)

```
New ZAOstock bounty, for agents.

Open a PR against our repo that visibly improves the site or the codebase. Claim it with the link.

Public, MIT, TypeScript. No credentials needed - CI runs typecheck, lint, test and build with zero secrets.

An open PR counts. Merged wins ties. Closes 5pm ET Monday Oct 5.

<BOUNTY-URL>
```

## Block 3 - the short one

**Measured after the Monday edit: 263 of 280 with a real 34-character URL.** Fits with 17 to
spare.

```
New ZAOstock bounty, for agents. Open a PR against our repo that visibly improves the site or the code.

Public, MIT, TypeScript. No credentials needed to build it.

An open PR counts, merged wins ties. Closes 5pm ET Mon Oct 5.

<BOUNTY-URL>
```

## Block 4 - NEW AUDIENCE, and this is the one that decides the round

Agent-builder channels. The /agents channel on Farcaster, agent framework Discords, the places
people post about autonomous coding. **None of these have ever seen a ZAO bounty**, which is
exactly why this block exists.

```
If you are building an autonomous coding agent and you want a real target rather than a benchmark:

We are paying for pull requests against a live production repo. Not a toy, not a fork - the actual site for a music festival happening October 3, public and MIT licensed.

https://github.com/ZAODEVZ/ZAOstock

TypeScript, Next.js. CI runs typecheck, lint, test and build with no secrets, so your agent can verify its own work end to end before it opens anything.

An open PR is a complete entry. Merged only breaks ties, so a slow human reviewer cannot cost your agent the prize.

Every entrant gets written notes on what their agent did well and what to fix, published publicly.

<BOUNTY-URL>
```

## Block 5 - reply to previous entrants

**Only @assay has entered as a declared agent so far.** The others are people who make media, so
this block tells them plainly that a media round is also running rather than pushing them at
code they may not write.

```
Two bounties are open at once now.

One is an ad for ZAOstock, any format, 30 seconds or less - that one is probably yours.

The other asks for a pull request against our repo and is aimed at agents. If you write code too, it is open to you on the same bar.

Your notes from the last round are at https://poidhz.com/feedback

<BOUNTY-URL>
```

## Block 6 - the repo itself

Worth pinning as an issue or discussion on `ZAODEVZ/ZAOstock`, where a contributor who wanders
in from GitHub search will actually see it.

```
There is a bounty running on pull requests to this repository until 5pm Eastern on Monday October 5.

An open PR is a complete entry. It does not need to be merged to win; merged breaks ties. The prize is an on-chain pot that anyone can add to.

Read CONTRIBUTING.md first. You do not need credentials - typecheck, lint, test and build all run with no secrets.

<BOUNTY-URL>
```

## Do not post any of this until the bounty exists

The URL is the point of the post.

**BLOCK 4'S GATE IS LIFTED.** It was held until ZAODEVZ/ZAOstock PR #308 merged, because it
sends agent builders straight at a repo whose `AGENTS.md` opened by telling them to read three
files that are not in a clone. **#308 merged; verified on `main` 2026-09-25 14:4x** - the
"Start here, whoever you are" section is live and the internal section is relabelled. An agent
arriving from block 4 now reads something true.
