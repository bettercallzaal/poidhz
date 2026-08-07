# Fork this for your org

`zpoidh` was built as BCZ/The ZAO's own POIDH bounty ops repo, but the tooling underneath
it (calendar, dashboard, leaderboard refresh, deadline scanner) is not actually
BCZ-specific - it just had BCZ's own values hardcoded. This guide is the real "point this
at a different org" onboarding doc: fork the repo, edit one file, deploy.

If you want the *bounty-writing pattern* (not the tooling) - the BAR/RUBRIC/ASSET
KIT/REWARD structure that produced BCZ's best rounds - see
[P2P-AD-BOUNTY-KIT.md](P2P-AD-BOUNTY-KIT.md) instead. This doc is about running the repo;
that doc is about writing the bounty description.

## What you're forking

- A live bounty deadline calendar (`docs/bounty-calendar.html` + `scripts/build-bounty-calendar.py`)
- A platform-wide POID deadline scanner (`docs/bounty-dashboard.html` + `scripts/scan-poidh-deadlines.py`, `scripts/build-bounty-dashboard.py`)
- An Empire Builder $-token leaderboard refresh script (`scripts/refresh-poidh-leaderboard.py`)
- A round-by-round bounty playbook + P2P Ad Bounty Kit pattern (`docs/how-to-draft-next-bounty.md`, `docs/P2P-AD-BOUNTY-KIT.md`)
- A standalone (non-Farcaster-required) bounty-creation page (`docs/create-bounty.html`)

## Step 1 - Fork the repo

```bash
gh repo fork bettercallzaal/zpoidh --clone
cd zpoidh
```

## Step 2 - Edit `org.config.json`

This is the entire "make it yours" step for the scripts that are already wired up. Every
field has a comment in the file explaining what it drives:

```jsonc
{
  "org_name": "Your Org / Your DAO",
  "org_short": "YOUR",
  "treasury_wallet": "0xYOUR_EOA_HERE",          // must be an EOA - POIDH reverts smart-wallet bounty creation
  "empire_token_address": "0x...",                 // only if you're using Empire Builder for a secondary reward rail - optional
  "empire_token_symbol": "$YOUR",                   // shown in generated winner-announcement drafts, e.g. "You've earned a slot in $YOUR leaderboard"
  "empire_leaderboard_name": "Your Leaderboard Name",
  "empire_leaderboard_url": "https://www.empirebuilder.world/empire/...",
  "empire_leaderboard_uuid": "...",
  "farcaster_album": "your-warpcast-media-album",
  "farcaster_handle": "@your-handle",
  "default_bounty_ids": [1234, 5678],              // your own known POIDH bounty ids, if any exist yet
  "default_chain_id": 8453,                         // 8453 = Base, 42161 = Arbitrum, 666666666 = Degen, 1 = Ethereum mainnet
  "site_url": "https://your-deploy.vercel.app",
  "brand": { "bg": "#000000", "cyan": "#00e5ff", "gold": "#f5c842" },
  "rounds": [
    {"round": 1, "bounty_id": 1234, "title": "Your R1 title"}
  ],
  "planned_rounds": [
    {"round": 2, "title": "Your R2 title, not cast yet"}
  ]
}
```

Every script that reads this file falls back to BCZ's own hardcoded values if a key is
missing or the file doesn't exist - so a partial edit never breaks anything, it just means
that one field is still BCZ's. Fill in what you have; leave the rest for later.

If you don't have an Empire Builder leaderboard (or any secondary token reward), leave
those fields as-is - the leaderboard refresh script will just fail gracefully on that one
integration and the rest of the tooling (calendar, dashboard, deadline scanner) doesn't
depend on it at all.

## Step 3 - Verify each script picks up your config

```bash
python3 scripts/build-bounty-calendar.py --selftest   # deadline-parser sanity check, org-independent
python3 scripts/build-bounty-calendar.py               # pulls your rounds, writes data/bounty-calendar.json
python3 scripts/scan-poidh-deadlines.py --selftest
python3 scripts/scan-poidh-deadlines.py --chain 8453    # or omit --chain to use your configured default
python3 scripts/refresh-poidh-leaderboard.py --selftest
```

Check `data/bounty-calendar.json` and `data/poidh-deadlines-global.json` after running -
if your `rounds`/`default_bounty_ids` are in there instead of BCZ's, the config wired
correctly.

## Step 4 - Deploy

`vercel.json` already routes `/dashboard`, `/calendar`, `/hub`, `/best-practices` to the
right static pages. Deploy with `vercel --prod` or connect the repo in the Vercel
dashboard. Update `org.config.json`'s `site_url` to match your real deploy URL once you
have it.

## Step 5 - Automate the refresh (optional but recommended)

Two GitHub Actions workflows already exist (`.github/workflows/refresh-bounty-dashboard.yml`,
`.github/workflows/refresh-leaderboard.yml`) that re-run the scripts on a cron and commit
the refreshed data. They need **Settings -> Actions -> General -> Workflow permissions ->
Read and write permissions** flipped on for your fork (this is a real gotcha BCZ hit -
both crons silently fail with a 0-second startup failure until this is flipped).

## Current wiring status (honest, as of this doc)

| Script | Reads org.config.json? |
|---|---|
| `scripts/refresh-poidh-leaderboard.py` | Yes |
| `scripts/build-bounty-calendar.py` | Yes |
| `scripts/scan-poidh-deadlines.py` | Yes (chain default only - it was already org-agnostic otherwise) |
| `scripts/build-bounty-dashboard.py` | Yes (chain default only - it was already org-agnostic otherwise) |
| `scripts/deadlines-to-ics.py` | N/A - already fully org-agnostic, no wiring needed. It only reads whatever JSON `scan-poidh-deadlines.py` / `build-bounty-calendar.py` already produced (both already wired above) and has no chain default, bounty ids, or BCZ-specific strings of its own. |
| `scripts/prepare-winner-announcement.py` | Yes (`empire_token_symbol` - turned out to have far less BCZ coupling than expected once actually read: no hardcoded wallet or handles, just one reward-rail mention in a cast template) |
| `docs/create-bounty.html` | Not yet - has BCZ Treasury wallet + brand colors hardcoded in the page itself |

If you fork before `docs/create-bounty.html` is finished, you'll hit hardcoded BCZ values
in that one file - open an issue or a PR, the pattern for wiring a new script is identical
across every script already done (see any of the "Yes" rows for the `load_org_config()`
pattern to copy).

## What stays yours regardless of config

- The actual bounty descriptions you write (see `docs/P2P-AD-BOUNTY-KIT.md` for the
  pattern, but your brand voice/rules are yours)
- Your brand kit assets (`assets/brand-kits/<your-campaign>/` - nothing here ships one for
  you, BCZ's own kit stays under `assets/brand-kits/zabal-games/` as a reference example
  of the *shape* a kit should take, not something to reuse)
- Judging - the rubric structure is a template, the actual scoring is a human call every
  time

## Also see

- [P2P-AD-BOUNTY-KIT.md](P2P-AD-BOUNTY-KIT.md) - the bounty-writing pattern itself
- [how-to-draft-next-bounty.md](how-to-draft-next-bounty.md) - BCZ's own concrete
  step-by-step (useful as a worked example even if you're not BCZ)
- `org.config.json` - the file this whole doc is about
