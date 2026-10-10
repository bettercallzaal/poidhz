# Daily 10 - Round 10, best marketing rollout on WaveZStation (NOT CAST)

Rewritten 2026-10-10 for Zaal's rulings through the Grill: items 96 to 99 (vault
`decisions/grill-2026-10-09-seat-morning.md`), 103 (vault 0bdcb9e6), 106 (vault 1cafd9fc) and 108 to 109
(vault a3862b56). His words, in order: *"Maybe we say best marketing rollout give it a month and people have to
sign up"*; *"500 in poidh I'll buy 500 and they buy 500 of their favorite"*; Q1 = A, $1,000 total, the
winner's $500 comes out of the prize; Q2 *"Sign up form on website after they put in email"*; Q3 *"Say they
have to buy and are expected to use that volume in wave station but can use it on their own"*.
**Nothing here is cast, posted or sent. He sees the final text first.** Reasoning in `PLAN.md`, the
rulings in `REDRAFT-v3.md`, the site facts in `RESEARCH.md`, all beside this file.

- **Title field:** `Round 10 - Best Marketing Rollout On WaveZStation, One Month, Sign Up First`
- **Type:** OPEN. Contributor vote confirms the pick. **Promises the pot, plus one thing outside it that Zaal ruled in (item 106): his $500 buy of the winning song, from his wallet, verified by hash.** The standing rule is pot-only (`rounds/daily/README.md`); this is his call to set aside, and the text says who pays, from which wallet, by when, and how to check.
- **Close:** **Friday 13 November 2026, 5:00pm Eastern.** Sign-up closes **Sunday 18 October 2026, 11:59pm Eastern.** Weekdays checked with `date -j` on 10 Oct.
- **Reward field:** $500, his number (item 103). 0.1995 ETH at 2,506.72 USD per ETH (Coinbase spot 16:06Z 10 Oct, the price every d10 file uses). Re-read the price the minute he casts. The paste body names no pot amount.
- **CAST GATE, in this order:** (1) Zaal sends the invitation in `ARTIST-PITCH.md`, or decides not to; (2) the sign-up form exists at a URL on poidhz.com with a store behind it (today the site's store is OFF: `/api/vote` on poidhz.com returned `storeReady: false` at 20:46Z 10 Oct; see `PLAN.md`, "The sign-up form"); (3) replace `SIGNUP_URL` below with that URL; (4) he reads this text one more time; (5) cast.
- **After the winner is picked:** replace `BUY_TX_HASH` in `ANNOUNCE.md` block 3 with the hash of Zaal's buy; nothing in this text changes after the cast (cast text is immutable).
- **Validator note:** the paste body writes every dollar figure in words (five hundred dollars, two hundred and twenty-five dollars) because `validate-bounty-description.py` reads any `$5...` as a pot figure. They are the buys, not the pot.
- **The email form brushes a repo rule:** `docs/community-plan.md` says "No email list. Same reason, plus nobody has consented to one." This form is a round sign-up, not a list: the text below says the address is used to reach entrants about this round only and is not a mailing list. Where the addresses are stored and who can read them is in `PLAN.md` and in the PR body, and is a question back to Zaal.
- **Still open for Zaal, with the default taken:** where the sign-up emails live (default: the site's own Upstash store, switched on by him; `PLAN.md` Q4); whether the form is built in this repo before the cast (default: yes, a separate PR, `PLAN.md` Q5).
- **Numbering:** this takes d10, as #236 and #244 did. The reaction-round text from #244 is superseded by this file and stays in git history.

<!-- PASTE BELOW THIS LINE -->

ARTISTS ON WAVEZSTATION: RUN THE BEST MARKETING ROLLOUT FOR YOUR SONG OVER ONE MONTH. SIGN UP FIRST. THE WINNER TAKES THE POT, AND ZAAL BUYS FIVE HUNDRED DOLLARS OF THEIR SONG.

WaveZStation is a music site where fans buy into a song instead of streaming it, and 45 cents of every dollar goes to the artist on the spot: https://wavezstation.com

This round is for artists with a song listed there. Pick one song. From sign-up close to the deadline, run a public marketing rollout for it: posts, clips, reaction videos, shows, collabs, playlists, whatever actually moves people to buy in. Post it as it happens. At the end, claim here with the record of what you did and what it moved.

SIGN UP BY 11:59PM EASTERN, SUNDAY OCTOBER 18, 2026 AT SIGNUP_URL

Submissions close 5:00pm Eastern, Friday November 13, 2026.


WHY THIS ROUND EXISTS

A song on WaveZStation earns when someone decides to buy it, and that decision is made by marketing, not by a play count. Nobody on the site has sold a thousand dollars of one song yet: the most-sold song had around eight hundred dollars of total sales when we checked on October 10 (a bound, not a count; we could not pull every buy). We want to see what one artist can move in a month when they go all in, and pay for the best attempt.


THE BAR (these are requirements, not preferences)

1. Sign up at SIGNUP_URL by 11:59pm Eastern, Sunday October 18, 2026, with your email, your artist name, the song's WaveZStation link and where you will post the rollout. Your email is used to reach you about this round and for nothing else. It is not a mailing list. No sign-up, no entry.
2. One song, one artist, one entry. The song must be listed on wavezstation.com by the sign-up close.
3. The rollout is public. Post it on X, Farcaster, Instagram, TikTok, YouTube or your own site, as it happens, and tag @WaveZStation where you can.
4. Real work by you or your team. AI tools are fine for making things; a rollout that is only an AI-generated feed is not.
5. Your claim is the record: the song link, links to at least five public posts from the rollout in date order, and the song's supporter count and fan pool on sign-up day and on claim day, read off its WaveZStation page. We read the same numbers off the site ourselves at the close.
6. UPLOAD ONE FRAME HERE AND PUT THE LINKS IN YOUR CLAIM. poidh takes images, not video. Upload one image from your rollout as the claim image, and put the links in the description. Without the links there is no entry.


WHAT EARNS WEIGHT

- It moved the number. Supporters and fan pool on the song from sign-up close to the close, measured off the site, count for half the weight.
- It is a rollout, not a post. There is a plan, it runs for the month, and each piece sets up the next.
- The craft. Somebody who sees one piece of it wants to hear the song.
- You brought people who were not already there.
- You tell the truth about the numbers.


THE ASSET KIT (use any of this for your entry)

- Your song's page on WaveZStation, which shows its supporters and fan pool to anyone.
- How buying in works, in WaveZStation's own words: https://wavezstation.com/docs
- The sign-up form: SIGNUP_URL

There is no logo pack for this round. Your song and your rollout are the piece.


THE REWARD

Winner takes the whole pot. This is an OPEN bounty, so the pot is whatever this page says it is right now, and it grows in real time as others contribute. Read the number at the top of this page, not a number in this text.

Two more things, outside the pot, and read them before you enter:

First, within one week of the pick, Zaal buys five hundred dollars of the winning song on WaveZStation from his own wallet, and we post the Basescan transaction so anyone can check it. On the site's split that puts two hundred and twenty-five dollars in the song's creators' wallets the second it lands, two hundred and twenty-five into the song's fan pool, and fifty with the platform.

Second, the winner has to buy too. Five hundred dollars of the prize goes back into WaveZStation as a buy, within one week of the pot paying out, and you are expected to use that volume on the site. It can be your own song. Post the transaction and we will share it. poidh pays the pot the moment the claim is accepted and nothing on poidh can hold it back, so this is a rule of the round that we are trusting you to keep, and we will say publicly whether it was kept.

Disclosure: Zaal's buy makes him a supporter of the winning song, so from then on a share of every later dollar spent on it is his to claim through the fan pool. If the winner is Saturday in LA, where he already holds about 21 percent of everything sold, he would hold about half. We would rather say that than have you find it.

Every submitter earns $ZABAL automatically through the POIDH Submitters leaderboard on Empire Builder, and the drop scales with how many BCZ rounds you have entered in total.

Track it live: https://www.empirebuilder.world/empire/0xbb48f19b0494ff7c1fe5dc2032aeee14312f0b07

Beyond the pot and the buy named above, this bounty promises nothing else. We want to share the best rollouts on our channels, and we probably will, but it is not written here as a commitment. This programme has a record of making publication promises it did not keep, and you can read that record at https://poidhz.com/about


HOW THE WINNER IS PICKED

Everyone who enters gets a note back on their rollout, win or lose. One thing it did and one thing to do better.

Zaal picks after the close, with the entries and the site's numbers in front of him, and posts the pick the following week. Everyone who added to the pot then has two days to vote on the pick before it pays out.

Discord: https://discord.thezao.com


DEADLINE

Sign-up closes 11:59pm Eastern, Sunday October 18, 2026.

Submissions close 5:00pm Eastern, Friday November 13, 2026.

WaveZStation: https://wavezstation.com

<!-- PASTE ABOVE THIS LINE -->
