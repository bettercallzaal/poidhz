# Daily 01 - the first one (paste-ready for POIDH Title + Description)

Strip this header before pasting. Everything between the sentinel lines goes in the
Description field.

**POIDH RENDERS MARKDOWN, NOT PLAIN TEXT.** This header claimed the opposite until
2026-09-20 23:1x, when Zaal pasted the body into the form and read the preview back. Three
blocks were mangled, and every one of them was a single newline the renderer joined:

- **"Tagging @bettercallzaal ... is not required today" was absorbed into THE BAR as a fifth
  numbered item** - so the one line saying a thing is optional rendered as a requirement.
- **REACH, CRAFT and SUBSTANCE vanished into the bullet above them** - the preview read
  "Someone who is not in this bounty shared it Craft".
- **The five asset-kit links collapsed onto one line**, turning the most useful block in the
  description into a wall.

The fix is structural, not cosmetic: labels are ALL-CAPS on their own line with a blank line
under them, every list uses real markdown bullets, and no line that must stand alone shares a
paragraph with another. `scripts/check-render-safe.py` now refuses the shapes that joined.

**Read the preview tab before casting, every time.** The description is immutable; the
preview is the last moment anything can be fixed.

**Title field:** `Make one piece of media for ZAOstock`

**Type: OPEN.** The pot must be able to grow.

**Prize: 0.0094 ETH, about $25** at ETH $2,657.49, measured 2026-09-20. **Re-price before
casting** - the pot is small enough that an hour of movement shows.

**Opens:** today, Sunday 20 September 2026.
**Closes:** Monday 21 September 2026, 4:00pm Eastern - one hour before the 5pm stream.

**Two corrections to what was said out loud, both deliberate.** Zaal said "6pm EST".

1. **"Eastern", never "EST".** In September US Eastern is on daylight time (EDT, UTC-4), so
   "6pm EST" literally means 7pm local. "Eastern" cannot be read an hour wrong.
2. **4:00pm, not 6:00pm.** He also said he picks the winner live on stream at 5pm the same
   day. A bounty that closes after its own decision is decided on an incomplete field. 4pm
   leaves an hour to read the entries.

Every announcement in `DISTRIBUTION.md` says 4pm to match. **They have to**, because this
description is immutable once cast: if the copy and the chain disagree, only the copy can be
fixed, and by then someone has already been told the wrong time.

## The Discord link, and why the vanity URL rather than the invite

Zaal gave `discord.thezao.com` on 2026-09-20. Verified the same minute: it returns 200 and
redirects to `https://discord.com/invite/ACJyYQH3BE`.

**The description carries the vanity URL, not the raw invite, and that is deliberate.** A
poidh description is immutable once cast. A Discord invite can be revoked, rotated or expire,
and if the raw code were baked in, the bounty would permanently point at a dead door with no
way to fix it. The vanity is a redirect we control - if the invite changes, the redirect
changes and the bounty still works.

That is the same reasoning as every re-check date in this repo: put the changeable thing
behind something you can edit.


> **THE BLOCK BELOW WAS REPLACED WITH THE TEXT ACTUALLY ON CHAIN, 2026-09-23.** What sat here
> was a LATER, better-worded draft - it added an "OPTIONAL, AND GENUINELY OPTIONAL" heading and
> extra paragraph breaks that bounty 1409 does not have. The improvements were real and were
> made after casting, which means this file was quietly claiming that entrants read something
> they never saw. A poidh description is immutable; the file is the thing that has to move.
>
> Found by `scripts/verify-cast-text.py --all`, which diffs each round's paste body against
> what poidh serves. The wording that was here has not been thrown away - it is in git history
> at commit `9ea5539^` and the lesson it encodes, that an optional line needs its own labelled
> block or the renderer swallows it, is already in the daily template.

<!-- PASTE BELOW THIS LINE -->

Make one piece of media using the ZAOstock brand kit. That is the whole ask.

A poster, a clip, a story, a meme, a flyer, a 15-second pitch to camera - whatever you want. Post it publicly, drop the link here. Best one wins the pot, and the pot grows as others chip in.

ZAOstock is a free music festival on Saturday October 3, 2026, in Ellsworth, Maine. Franklin Street closes to traffic and eight independent acts play back to back on the parklet stage from noon to six. Free, all ages, rain or shine.

Thirteen days out, and this closes tomorrow afternoon. Low bar on purpose - day one is not where we find the perfect asset, it is where we find out who turns up. Twenty minutes is enough.

WHY THIS ROUND EXISTS

Because a free festival on one street in a small city lives or dies on whether anyone hears about it, and we would rather pay people who are good at that than shout louder ourselves. Everything you need is at https://zaostock.com - go and read it before you make anything.

THE BAR (short, on purpose)

1. Use the ZAOstock brand kit. It is linked below, it is CC-BY, there is nothing to ask permission for.
2. Post it publicly and submit the live URL here. If it is not claimed on this page, it is not entered.
3. Put ZAOstock and Saturday October 3 somewhere a reader can see them.
4. AUDIO: if there is audio, use original or one clear instrumental that does not compete with speech. Library music over dialog is a floor fail.

Tagging @bettercallzaal and cross-posting in /poidh helps and is not required today.

THE RUBRIC (more boxes ticked, more weight)

Reach
+ It went where people who could actually attend will see it - Ellsworth, Bangor, Downeast, Maine groups
+ A physical placement photographed as proof beats a post nobody saw
+ Someone who is not in this bounty shared it

Craft
+ Looks finished, not like a draft
+ Vertical or square for mobile
+ Captions if there is speech
+ Date and place readable in three seconds, without clicking

Substance
+ Specific about the day rather than "come to a festival"
+ Names an act from the lineup
+ Honest about what it is: small, free, outdoors, one street

THE ASSET KIT (use any of this, CC-BY)

Everything in one download: https://zaostock.com/brand/zaostock-brand-kit.zip
The brand page, each file separately: https://zaostock.com/brand
The moose, primary mark: https://zaostock.com/brand/logos/zaostock26_moose.png
Poster reference: https://zaostock.com/brand/posters/moose-cracked-cement-red-1024.png
The lineup, all eight acts: https://zaostock.com/artists

The moose mark is by attabotty. Keep the ZAOstock name visible in your final piece.

THE REWARD

Winner takes the whole pot. This is an OPEN bounty, so the pot is whatever this page says it is right now, and it grows in real time as others contribute. Read the number at the top of this page, not a number in this text.

Every submitter earns $ZABAL automatically through the POIDH Submitters leaderboard on Empire Builder, and the drop scales with how many BCZ rounds you have entered in total.

Track it live: https://www.empirebuilder.world/empire/0xbb48f19b0494ff7c1fe5dc2032aeee14312f0b07

This bounty promises the pot and nothing else. We might run the best entries on ZAOstock's own channels and we would like to, but it is not written here as a commitment - this programme has a record of making publication promises it did not keep, and you can read that record at https://poidhz.com/about

HOW THE WINNER IS PICKED

Live on stream at 5pm Eastern, the same day it closes. Zaal picks it out loud with the entries on screen.

Discord is where it happens and where you can argue for your own entry: https://discord.thezao.com

This is day one of thirteen, one bounty a day until ZAOstock itself. Same shape every day: opens, closes at 4pm Eastern, decided live at 5pm.

DEADLINE

Submissions close 4:00pm Eastern, Monday September 21, 2026.
Winner picked live on stream at 5:00pm Eastern the same day.

ZAOstock is Saturday October 3. Promo that lands after it is worth nothing, which is why these close fast.

The festival: https://zaostock.com

<!-- PASTE ABOVE THIS LINE -->
