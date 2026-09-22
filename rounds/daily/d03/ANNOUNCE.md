# Bounty three - announcement copy

**Nothing sent.** Every block carries the live bounty URL once it is cast. Zaal posts these.

**The close is 5:00pm Eastern, Wednesday 23 September**, and the pick is named live on Twitch
around 5pm, right as it closes. Every block below says so.
`scripts/check-round-copy-agrees.py rounds/daily/d03` enforces that against the immutable
description, because day one's copy said 6pm after the bounty had moved to 4pm and six blocks
had to be rewritten by hand.

**The new thing to lead with is the ban, not the prize.** "Anything but a poster" is a better
hook than another round announcement, and it is the only reason someone who scrolled past the
first two rounds would stop.

**The draft checkpoint has to be in every block.** It is the part that changes what people do
today, and it is worthless if only the bounty page mentions it.

## Farcaster and X, under 280

```
Bounty three: anything but a poster.

Eleven entries in, nearly all posters. So today it is off the table. Video, audio, a meme, something on a real wall. Make the thing only you would make.

Tag a draft by noon ET, I send notes back.

Closes 5pm ET. <BOUNTY-URL>
```

**273 characters** with a 22-character URL, counted in python, not estimated. Recount if the
live URL is longer than 22.

This block took three goes. The first draft was 329 characters and this file claimed "279"
underneath it, a number nobody had measured; the second was 292. Firefly counts against X's
280 across all three targets, so an over-length block is silently truncated at the end, which
is where the deadline and the URL are. Count it, never estimate it.

## The rooms, no limit

```
Bounty three is up and it has one new rule: no posters.

Eleven entries have come in over two rounds and almost all of them were a still image with type on it. They were good. But the kit makes a poster easy, which is exactly why everybody made one, and a feed full of the same rectangle stops working.

So today: anything else. Fifteen seconds that moves with sound. A jingle or a thirty-second spot in your own voice. A meme that is actually funny and still carries the date. A photo of something physical you put up in a real place. A comic, a loop, a sticker sheet. Something nobody on this list thought of.

Make the thing only you would make. Not the best version of the obvious idea.

NEW: tag a draft by 12pm Eastern and I will send you one specific note back before 2pm. Rough is fine, it is not a claim yet. Final claim by 5pm. If two entries land in the same place, the one that took a note wins.

One more thing, and it is the biggest fix available to most of you: upload the FILE, not a screenshot of your post. Four of five claims yesterday were a photo of a phone screen with the battery icon in it.

Closes 5pm Eastern Wednesday. I name the pick live on Twitch right as it closes, so come and argue for your own.

Kit, free to use: https://zaostock.com/brand
Discord: https://discord.thezao.com
The bounty: <BOUNTY-URL>
```

## Reply to everyone who entered round one or two

```
Round three is up and it is the one you have been building toward: no posters, anything else.

You have entered before, so the thing worth knowing is the new checkpoint. Tag a draft by 12pm Eastern and I send you one specific note back before 2pm, then you file the final by 5pm. Nobody has had that before.

Closes 5pm Eastern Wednesday. <BOUNTY-URL>
```

## The Maine-local post

**Still nobody's job, and eleven entries in, not one is a photograph of something physically
placed in a real location.** This block is the one that could change that, and it is the only
block here aimed at people who can actually walk to the festival.

```
ZAOstock is a free music festival on Franklin Street in Ellsworth on Saturday October 3. Noon to six, eight independent acts, all ages, rain or shine.

We are paying people to help get the word out. Today's brief is anything except a poster: a short video, a clip on your phone, or a photo of a flyer you put up somewhere real in Ellsworth or Bangor.

That last one is wide open. Eleven people have entered so far and not one has photographed a flyer in an actual window.

Closes 5pm Eastern Wednesday: <BOUNTY-URL>
Everything about the festival: https://zaostock.com
```

## Two hours before the close

```
Two hours on bounty three. No posters. Anything else.

If you tagged a draft this morning you have my notes, file the final. If you did not, there is still time to make something short.

Closes 5pm Eastern: <BOUNTY-URL>
```

## Before posting any of these

- Replace every `<BOUNTY-URL>` with the live URL. `grep -c "<BOUNTY-URL>" ANNOUNCE.md` should
  return 0 once it is cast.
- **No prize figure in any block.** The pot is OPEN and grows; the number lives on the page.
- The Twitch channel URL is still not supplied, so these say "on Twitch" and nothing more. A
  guessed URL is worse than no URL: twitch.tv returns 200 for a channel that does not exist.
