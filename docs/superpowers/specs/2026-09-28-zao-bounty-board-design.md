<!-- NOT-ANNOUNCEMENT-COPY: internal design spec. Names no deadline anyone submits to. -->
# The ZAO bounty board - design

Agreed with Zaal 2026-09-28 in the `poidhz` session. poidhz.com stops being a static site and
becomes a Farcaster client built on the Neynar API: The ZAO's bounty board, and the place the
people who enter its bounties belong.

## Intent

**Success, in Zaal's words, is "all of these and more":** people come back for a second round,
agents find open rounds without Zaal posting, entrants see each other's work, and funders see
proof. Measured baseline 2026-09-26 (`docs/community-plan.md`): 35 people have ever entered, 10
entered more than once, all four round-five entrants were agents.

**Who posts bounties:** Zaal's issuer wallet only, for now. Later, any ZAO project, and later
still anyone who sees something that moves The ZAO forward, from a $2 floor. Nothing in the
code may assume a single issuer.

## Decisions taken

| question | answer |
|---|---|
| shape | Farcaster client on the Neynar API (option B, over growing the static site) |
| where | **replaces poidhz.com**; every existing URL keeps working |
| sign-in | Farcaster for humans, wallet-signed API key for agents |
| v1 scope | profiles and portfolios, comments and Q&A, proposals, notifications, "and more" |
| channel | **/zao** for now (lead @zaal, FID 19640). Config value; /poidh (lead @kenny) only if Kenny agrees |
| stack | ZAO OS's: Next 16, React 19, Tailwind 4, Supabase, Neynar SDK, Farcaster quick-auth and mini-app SDK, viem |

## Constraints carried from the programme

- **Zaal fires every outbound action.** The app never casts as Zaal on its own. A bounty's
  thread root is a cast Zaal made; he attaches it on the admin page.
- **No ranking of entrants**, anywhere. Portfolios list work; they never order people by quality.
  "Entered five rounds" is a fact and may be shown.
- **A number that could not be measured prints UNKNOWN**, never 0. If poidh or Neynar is down, a
  claim count is unknown, not zero.
- **The Python pipeline stays.** Its checks (send gates, promise audits, deadline parser,
  feedback gates) keep running on the 6-hourly cron and keep writing `data/*.json`. The app
  reads that output. Porting the scripts is out of scope.

## 1. Architecture

```
poidhz.com  (Next app in web/, Vercel)
  Board | Bounty | Person | People | Proposals | Feed | Admin | API | llms.txt
     |          |            |               |
  Supabase   Neynar API   poidh API +     mini-app SDK
  (app state) (casts,      Base (viem)     (notifications)
              users,
              signers)
     ^
  existing crons write data/*.json -> the app reads them at build and request time
```

Three sources of truth, none duplicated:

- **Chain and poidh API** own bounties, claims, winners, payouts.
- **Farcaster** owns conversation and identity: casts, replies, likes, users.
- **Supabase** owns only what exists nowhere else (section 2).

The app lives in `web/` in this repo so the static site stays live on production until the
cutover. It deploys to a Vercel preview first. Production moves only when Zaal has tested it
and says so.

## 2. Identity and data

A person is a FID plus that FID's verified wallets (from Neynar). A portfolio is every claim
made from any of those wallets. This replaces handle-guessing and closes the known alias case
(`defifa` / `kmacb.eth`, bounty 1412). A wallet with no FID is still a person, titled by its
short address, until someone links it.

Agents sign a fixed message with their claim wallet and receive an API key. With a key they
can read everything and create proposals. **Casting needs a FID**; an agent with no Farcaster
account cannot cast through the app.

Supabase tables:

| table | holds |
|---|---|
| `sources` | issuer wallets and poidh albums counted as ZAO; `min_usd` for the later $2 floor |
| `bounty_threads` | bounty id -> root cast hash in the channel, attached by Zaal |
| `notes` | written feedback per claim, imported from `data/feedback/*.json` |
| `proposals` | cast hash, ZAO project, status (open, cast-as-bounty, declined), linked bounty id |
| `agent_keys` | wallet, hashed key, optional fid, created_at, last_used_at |
| `hidden` | item hash hidden on poidhz.com, by whom, why |
| `notif_tokens` | mini-app notification url and token per FID |

Bounties, claims and people are **not** tables of record. They are read from `data/*.json`
and the poidh API and cached. If Supabase is wiped, only notes (also in the repo),
proposals, hidden flags, keys and tokens are lost.

## 3. Pages

| route | what it shows |
|---|---|
| `/` | **the board.** Open ZAO bounties first: pot, time left, the bar, entry count, thread reply count, how to enter. Then closed rounds with winners. A strip from the /zao channel |
| `/b/[id]` | one bounty: full text, every claim with its media, the winner, the notes on each claim, the Farcaster thread under the root cast with a reply box, and an Enter button (poidh link plus `/submit`) |
| `/u/[handle-or-address]` | one person: every piece across rounds, notes received, wins, first round, "entered N rounds", their casts in /zao |
| `/people` | everyone, grouped by rounds entered (fact, not rank) |
| `/proposals` | open proposals with likes and replies; a form that casts a proposal into /zao with a poidhz embed. Zaal marks one cast-as-bounty and links the bounty |
| `/feed` | the /zao channel feed |
| `/admin` | FID 19640 only: attach a root cast to a bounty, mark proposals, hide items, edit sources |
| `/rounds.json`, `/api/v1/*` | the agent feed: open rounds with bar, deadline, pot, claim format; proposals; people |
| `/llms.txt` | **generated** from the same data, so it cannot go stale again (today's file points agents at the old domain and lists R1-R5 only) |

Existing URLs (`/submit`, `/gallery`, `/calendar`, `/dashboard`, `/create-bounty`,
`/feedback/...`, `/data/*.json`, `/leaderboard`, `/round/:n`) keep working, as app pages
or as the existing static files served from `public/`.

## 4. Flows

- **Sign in.** Web: Sign In With Farcaster through Neynar. Mini app: quick-auth. Casting
  from the app needs a Neynar managed signer, approved once by the user in Warpcast.
- **Comment or ask.** A reply to the bounty's root cast. A reply by the bounty's issuer to a
  question marks it answered on the page.
- **Propose.** A cast into /zao whose embed is `poidhz.com/proposals`; the app indexes
  channel casts carrying that embed.
- **Notifications** (mini app, opt-in by adding the app): a bounty from a source gets a root
  cast (a round opened); the issuer replied to your cast in a thread; notes landed on your
  claim. Sent by a job, at most one per event per person.
- **Moderation.** The channel is moderated in Farcaster by its lead. On poidhz.com, the admin
  can hide any item; hidden items are listed on `/admin` with the reason.

## 5. Errors and testing

- Every page renders from cached data if Neynar or poidh fails, with an "as of" time. A
  count that could not be read shows UNKNOWN.
- Writes fail loudly: a cast that Neynar rejects shows the error, never a silent success.
- Unit tests (vitest) for the data layer: source filtering, wallet-to-person resolution,
  round status, the UNKNOWN rule, llms.txt and rounds.json generation.
- A smoke test that renders every route against the committed `data/*.json`.
- The Python checks in CI continue unchanged.

## Build order

1. **Read-only board over the existing data, no secrets needed:** `/`, `/b/[id]`,
   `/u/[x]`, `/people`, `/rounds.json`, generated `/llms.txt`, old URLs carried over.
   Zaal can test this on a preview the day it lands.
2. Neynar reads: threads under root casts, the /zao feed, FIDs on people. Needs `NEYNAR_API_KEY`.
3. Sign-in, signers, reply box, proposals. Needs a Neynar app and a Supabase project.
4. Admin, agent keys, hidden.
5. Mini-app manifest and notifications.

## Needs Zaal

- A Neynar API key and client id, and a Supabase project, entered through `/secret`. Not
  needed for step 1.
- Testing the preview, then the word to move production.
- Later: whether to ask Kenny about /poidh.
