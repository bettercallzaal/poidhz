# Platform audit - 2026-09-06

Short version of research **doc 2466** in the ZAO research library
(`ZAO OS V1/research/business/2466-poidhz-platform-honest-audit/`). That doc has the full
method, every source, and the reasoning. This file exists so anyone reading the repo finds
the findings without needing access to the other repo.

Everything below is measured, not remembered. Reproduce the bounty numbers with
`python3 scripts/query-bounty.py --bounty <id>`.

## What poidh actually is

- **Small.** Highest live bounty id across all chains was **1366** on 2026-09-06; Base's
  on-chain counter was at **380**. R5 was id 1330 / Base 344 on 2026-08-19, so the platform
  added roughly **36 bounties in 17 days** - about **2 per day, every chain combined**.
- **Of the 89 open bounties** in `data/bounty-dashboard.json`: median prize **$13.27**,
  **46% have zero submissions**, **87% have no parseable deadline**, 41 distinct issuers,
  70 on Base.

## What that says about our rounds

| Round | Prize (USD) | Claims | State |
|---|---|---|---|
| R1 (1151) | $26.29 | 11 | paid |
| R2 (1166) | $26.29 | 8 | paid |
| R3 (1180) | $62.60 | 8 | paid |
| R4 (1249) | $34.55 | - | canceled at closeout |
| R5 (1330) | $59.59 | 9 | paid 2026-09-05 |

**36 claims across the four rounds that ran. Never zero, in a field where 46% get zero.**
Every prize cleared the platform median by 2x to 5x.

## The claim we should not make

**We are not the highest-cadence issuer on poidh and it is not close.** Bounty 1366 is
`Log a Dog x poidh: September 6th Daily Winner` - a **daily** series at ~$52/day, wired
into logadog.xyz, new page every day. That issuer holds 9 of the 89 open bounties. We have
cast five rounds since April.

"ZAO brings the energy" does not survive a check if energy means volume. Completion,
prize size and tooling do survive it. Use those.

## What is broken right now

1. **`/calendar` returns 404** while `/` serves the same file at 200. `vercel.json`
   rewrites `/calendar` to `/index.html`; the rewrite does not work. The README calls the
   calendar the front page.
2. **The leaderboard cron fails intermittently** - 2 of the last 8 runs, both
   `HTTP Error 504: Gateway Timeout` from poidh at
   `scripts/refresh-poidh-leaderboard.py:111`. This is the PR #107 guard working correctly,
   refusing to publish degraded data. The gap is that there is no retry, so a transient
   upstream blip reds the build.
3. **The name is split three ways.** Repo is `poidhz`, the live deployment is
   **`zpoidh.vercel.app`**, and `poidhz.xyz` / `poidhz.com` do not resolve. The README
   correctly links the working URL; the risk is any post that says "poidhz" and links
   something poidhz-branded.
4. **Every `bettercallzaal.com/poidh-*` URL redirects to this GitHub repo** - including
   `poidh-bounty-best-practices.html`, which `rounds/_template/description.md` tells every
   future round to cite in its bounty text. The page is alive at
   `zpoidh.vercel.app/best-practices`. We host it and point entrants at a repo.
5. **`rounds/_template/cast-templates/winner-announce.md` carries two false claims** for
   any round without a $ZABAL trail: it promises every submitter an Empire Builder airdrop,
   and links a per-round judging page that was never built. R5 has no $ZABAL trail.
6. **R5's winner is paid and unannounced.** Copy drafted at `rounds/r5/winner-announce.md`.

## The one-line conclusion

The tooling layer is built, deployed, CORS-open and effectively unadvertised. R5 drew nine
claims while reaching none of its own audience; the data layer has reached nobody at all,
including Kenny, who gave us the undocumented `/data` endpoint and is on record wanting
exactly this kind of thing built on poidh.

**The asset is built. The telling has not happened.** That is the cheaper problem to have.
