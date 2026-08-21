# ZABAL Gamez bug fixes bounty (DRAFT, never cast)

Not live. No bounty ID. This held the "R7" slot before the R5-R7 renumbering freed it up
for other rounds (see root `README.md`'s round index) - "R7" below is a leftover label from
that draft, not a claim that a round by that number ran. Would have been the first CODE
bounty in the series: every round that has actually launched (R1-R5) has been a
clip/content bounty; this one crowdsources real bug fixes for the ZABAL Gamez platform,
with pull requests as submissions instead of clips.

## At a glance

- **Source:** [zabalgamez.com](https://zabalgamez.com) - the build-a-thon platform (workshops, portal, submissions, season quest, wins page)
- **Format:** bug fix - a public PR (or a clear patch + writeup if the fixer cannot PR) that fixes a real bug
- **Deadline:** cast-date + 14 days, 11:59pm PT (code takes longer than clips, so a 2-week window vs the usual 7)
- **Judge:** single judge (Zaal)
- **Issuer:** BCZ Treasury EOA / whichever wallet Zaal connects in [docs/create-bounty.html](../../docs/create-bounty.html)
- **Reward:** seeded by Zaal at create time. NOT winner-take-all - multiple strong fixes can each be paid, because the point is making ZABAL Gamez better.

## Why this one would be different

R1-R5 all judged clips. This one would judge code instead: impact (does it fix a real
user-blocking bug) plus craft (clean, minimal diff that does not break anything else).
Best fixes get merged. It's also designed as the trust-ladder first step for ZOL toward
money actions - a controlled, human-funded bounty ZOL could help scope + judge without
ever holding funds - though that's untested since the bounty never ran.

## Files in this folder

- `description.md` - the POIDH Description field, paste-ready (between the sentinel lines)
- `promo-cast.md` - launch Farcaster cast + X cross-post

## Workflow checklist

- [ ] Confirm reward seed with Zaal
- [ ] POIDH UI (or docs/create-bounty.html) -> Create OPEN bounty on Base with this description
- [ ] Cast `promo-cast.md` with the bounty URL as embed; pin in the ZABAL Gamez channel
- [ ] Firefly cross-post to X
- [ ] Day 7: reply-cast with submission count + days-left
- [ ] Close + review PRs; merge the strong ones; pay each qualifying fix
- [ ] Update the main `README.md` round index
