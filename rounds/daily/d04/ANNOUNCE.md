<!-- NOT-ANNOUNCEMENT-COPY-EXEMPT: this file IS announcement copy. The marker below is the real one. -->
# Round four - promo copy, unsent

**NOTHING HERE HAS BEEN POSTED.** Zaal posts. Written 2026-09-24 against the cast text in
`description.md`, which passes validate-bounty-description, check-render-safe and
check-copy-counts.

## Replace `<BOUNTY-URL>` before posting, and re-count the short block after you do

A real poidh bounty URL is **34 characters** (`https://poidh.xyz/base/bounty/1413`). The
placeholder below is 12. **Every length in this file was measured against the real 34, not
against the placeholder** - the 280-character block was got wrong four separate times in this
programme by counting against a placeholder and shipping something over the limit.

The short block below has **245 characters of room** once a 34-character URL and one space
are taken out of 280.

## Block 1 - Farcaster

Post in /poidh and on the main feed. Tag **@zaal** on Farcaster, not @bettercallzaal - there
is no bettercallzaal on Farcaster, the fname registry returns nothing for it.

```
Make an ad for ZAOstock. Thirty seconds or less, any format you like.

Free music festival, Saturday October 3, one street in Ellsworth Maine, eight acts, noon to six. The brand kit is free to use and there is a radio interview in it almost nobody has opened.

Winner takes the pot, and the pot can grow while the round runs.

Closes 5pm Eastern Sunday. Everyone who enters gets written notes on their own piece, win or lose, and they go up publicly.

<BOUNTY-URL>
```

## Block 2 - X

**This one is 309 characters with a real URL, so it needs a premium account.**
If the account is not premium, post block 3 instead - that one is measured at 260.

```
Make an ad for ZAOstock. 30 seconds or less, any format.

Free festival, Saturday October 3, Ellsworth Maine. One street, one stage, eight acts, noon to six.

Kit is free to use. Winner takes the whole pot. Closes 5pm ET Sunday.

Everyone who enters gets written notes back.

<BOUNTY-URL>
```

## Block 3 - the short one, 245 characters of text

**Measured: 225 characters of text, 260 of 280 with a real URL.** It fits with 20 to spare.
Re-count if you change a word - I wrote 238 here first from an estimate and the script said 225,
which is the whole reason this file insists on measuring.

```
Make an ad for ZAOstock. 30 seconds or less, any format.

Free music festival, Sat Oct 3, Ellsworth Maine. Eight acts, noon to six, one street.

Winner takes the pot. Closes 5pm ET Sunday. Everyone who enters gets notes back.

<BOUNTY-URL>
```

## Block 4 - Maine-local, and this is the one that has never been done

Front Street forums, Downeast Maine groups, Ellsworth and Bangor community pages, the local
music Facebook groups. **Three rounds have run and nobody has posted a single one of these**,
which is why every entry so far has come from crypto-native accounts rather than from anyone
who could actually walk to the festival.

```
ZAOstock is a free music festival in downtown Ellsworth on Saturday October 3. Franklin Street closes to traffic, one stage goes up in the parklet, and eight local and regional acts play from noon to six. Free, all ages, rain or shine.

We are paying people to make an advert for it. Thirty seconds or less, any format - film it on your phone if you like. There is a prize pot and the winner takes all of it.

If you live around here, you will make a better one than anybody online has. You know what the street looks like.

<BOUNTY-URL>
```

## Block 5 - reply to everyone who entered before

> **DO NOT SEND THIS UNTIL PR #172 IS MERGED.** It points people at
> https://poidhz.com/feedback for their own notes. Round one's pages are live; **rounds two
> and three return 404** because they sit on an unmerged branch. Measured 2026-09-24:
> `/feedback/1409` 200, `/feedback/1410` 404, `/feedback/1412` 404. Sending someone to read
> their notes and handing them a 404 is worse than not mentioning it.

Send as a reply under each entrant's last entry, so it lands in their notifications. Handles
verified from their own claims: @pascaline (X `pascaline7933`), @joeyofdeus (X `joey_of_deus`,
Farcaster `joeyofdeus`), @taku0x (X `0xcryt29`, Farcaster `taku0x`), @barsam (Farcaster),
@assay (Farcaster), @mfa - **@mfa has no public post on any claim, so there is nowhere to
reply to him.**

```
New one is up and it runs three days instead of one, so there is time to make something properly.

Make an ad for ZAOstock, 30 seconds or less, any format. Closes 5pm Eastern Sunday.

Your notes from the last round are at https://poidhz.com/feedback - one thing your piece did, one thing to do next.

<BOUNTY-URL>
```

## Block 6 - the one for people who have not entered because they think it is a crypto thing

```
You do not need a wallet to make the thing. You need one to get paid.

Make an ad for a free music festival in Ellsworth Maine on October 3. Thirty seconds or less. Phone footage is fine - the entries that stand out are the ones shot on the actual street, not the ones made on a computer.

The brand kit is free: https://zaostock.com/brand

<BOUNTY-URL>
```

## Do not post any of this until the bounty exists

The URL is the point of the post. Casting first, posting second - and
`scripts/check-copy-counts.py rounds/daily/d04` should be re-run after the round is cast,
because the claim counts quoted anywhere in this folder move the moment entries arrive.
