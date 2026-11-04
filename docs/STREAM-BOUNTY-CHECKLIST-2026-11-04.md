# Stream and bounty readiness checklist, Wed 4 Nov 2026

Local working checklist from known facts only. Every cast, post, send, fund, stream start and merge is the owner's tap. This lane drafts and wires; it never fires.

Sources: vault decisions/grill-2026-11-02-misc-morning.md items 150, 181, 192; vault handoffs/poidhz.md (2026-11-03 handoff).

## Order (owner rulings 181, 192)

1. After work today: finalize the POIDH and Singapore bounties live on a stream, with the related outbound items.
2. Then the X Space.
3. Then the Paragraph work (Day 308), after the Space. The 4:30 pm Paragraph start is superseded; do not re-ask it.

Who starts the stream and posts publicly: owner only. Stream confirmed by ruling 192. Whether a stream also runs alongside the Space is not ruled beyond that.

## Ready now

- [x] /music-video is live (PR #259 merged, page returns 200). The music video bounty text links to it, so the bounty can be cast.
- [x] Singapore page is live with the Stripe-on-request line and zaal.eth (PR #258).
- [x] Music video bounty text v6 exists in the vault (inbox/clips, v6). Fields: Base, OPEN, $10 seed, closes 5:00 pm Eastern, Sunday 29 November 2026. Entry format: 1920x1080, 30 fps, MP4 (H.264), any length. Song map stays on the website only.
- [x] Singapore Congress bounty fields exist in the vault (inbox/clips). Fields: Base, OPEN, $100 seed.

## Code wiring, runs the moment each URL is provided

| Step | File | Constant | State |
|------|------|----------|-------|
| Set music video bounty URL | web/app/music-video/data.ts | BOUNTY_URL | UNRESOLVED, empty until provided |
| Set Singapore bounty URL | web/app/singapore/links.ts | POIDH_BOUNTY_URL | UNRESOLVED, empty until provided |

After each: run vitest (web/lib/music-video.test.ts, singapore.test.ts), open a held PR with zao-pr-open --label hold, report head and readiness to messenger. No link is guessed or invented.

## Open, still needs the owner

- [ ] The two bounty URLs (above).
- [ ] May a creator claim his own poidh bounty (Singapore)? Asked in misc, not confirmed.
- [ ] Iman's X handle for rule 8 of the music video bounty (Farcaster tag only until then).
- [ ] Shared Drive folder of Iman's horizontal footage for /music-video.
- [ ] The five Zoroastrianism answers for the personal section of /singapore (nothing drafted before he answers).
- [ ] zao-learns-zoroastrianism site URL, to replace the interim email link behind the question button.

## Coordination with the paragraph lane

- Wed's Singapore edition keeps a bounty link slot to fill from the Singapore bounty URL once provided (ruling 150). No placeholder text in the Paragraph draft.
- Paragraph work itself runs after the Space. This lane asks no Paragraph questions; it only hands over the Singapore bounty URL when it exists.

## Not this lane

No casts, funding, payment links, merges, pushes to main, or deletes.
