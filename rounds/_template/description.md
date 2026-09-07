# Description template (paste-ready for POIDH Description field)

Replace `<placeholders>` and adapt rubric items per the bounty's intent. Strip this header before pasting.

## Rule for any partner statistic you put in a bounty

A bounty description is public, permanent and immutable once cast. A number in it that
nobody can reproduce reads as invented, even when it is correct.

**Never quote a partner figure without naming its legs and its measurement date.** A bare
total is what produced three irreconcilable copies of the same WaveWarZ artist-earnings
number across three documents.

- **Wrong:** "13.9 SOL paid straight to artists, as of Aug 20"
- **Right:** "13.94 SOL to artists, all legs, as of 7 September 2026 - 9.33 from the artist
  share of the trade fee, 4.61 from settlement bonuses"

R5 (bounty 1330) shipped the wrong form. The figure was defensible under the all-legs
reading, but it was dated **two weeks before the total actually reached it** - on 20 August
the artist total was 13.47, and 13.9 is where it gets to around 5 September. Anyone checking
it against an August snapshot fails to reproduce it and concludes we made it up. 1330 is
on-chain and immutable, so that one cannot be fixed. The point is not to inherit it.

**Known-bad numbers, measured by the wwtracker lane 2026-09-07. Do not carry these forward:**

| Do not use | Why |
|---|---|
| "13.9 SOL to artists as of Aug 20" | right number, wrong date - see above |
| "458 SOL volume as of 2026-05-25" (doc 743) | about 11% high, and predates a volume repair |
| "1.00% artist share" | it is **1.005%**, verified at exact lamports |
| "2.28% effective fee rate" | that is platform revenue over volume, so it FALLS as volume rises. Not a fee rate. |
| "1.53% artist payout rate on every trade" | includes settlement bonuses, which are not per-trade |

**The fee numbers, stated correctly**, because a compressed version of this reached us and
was briefly written into this very file as a fourth wrong variant:

- The **trade fee is 1.500%** of volume.
- It splits **67/33, artist to platform**.
- So the **artist share is 1.005% of volume** - not the 1.00% that the PRD and
  `wavewarz-math.ts` both state. Small, and real.

Do not say "the trade fee is 1.005%". That is the artist's share of the fee, not the fee.

**Generate the artist line, do not copy it.** The correct string above is right today; the
generator is right always. Run
`python3 tools/artist-earnings.py --census census.json --trades trades.json` in
`wavewarz-protocol`. It reports by leg - artist share of the trade fee, plus the 5% winner
and 2% loser settlement bonuses - and labels which legs are measured versus inherited.

**Re-measure before every cast.** These figures move. A number that was right in August is
not right in October, and a bounty runs for weeks after you paste it. The wwtracker lane hit
this same date-drift defect on their own case-study page the same day, where it was emitted
as JSON-LD FAQ schema and therefore scraped into answer engines - two lanes, two surfaces,
one day, same signature.

---

Make the best <ARTIFACT> for <CAMPAIGN>. Any format. Best one wins <PRIZE> ETH on Base and we run it.

<CAMPAIGN> is <ONE-PARAGRAPH WHY>. <SOURCE PAGE / EPISODE / EVENT>.

<SECOND PARAGRAPH WITH THE EMOTIONAL HOOK + WHY THIS CAMPAIGN MATTERS>


THE BAR (do these or you are not in the running)

1. Make a <ARTIFACT> for <CAMPAIGN> in any format - image, video, meme, motion graphic, cast, poster, audio drop, whatever sells it. No format gate.
2. Tag @bettercallzaal on X when you post publicly.
3. Cross-post the same piece in the <CHANNEL> channel on Farcaster so the community sees it.
4. Submit the public URL on this POIDH bounty page, and put your handle in the claim text. If it is not claimed here, it is not entered.
5. AUDIO: if your <ARTIFACT> has audio, use the official <CAMPAIGN> promo MP3 from the asset kit, or original source-episode audio, or one clear instrumental that does not compete with spoken dialog. Random library music or melodic pads over dialog = floor fail.


THE RUBRIC (more boxes ticked = stronger judging weight)

Distribution
+ Cross-post on any additional Farcaster feed beyond <CHANNEL>
+ Cross-post on Bluesky, Threads, LinkedIn, Instagram, or TikTok in addition to X
+ Tag @kennyistyping on X / @kenny on Farcaster (POIDH founder, will boost)
+ Tag @poidhxyz on X / @poidh on Farcaster
+ Tag <CAMPAIGN-RELEVANT-ACCOUNT> (e.g. @yerbearserker on Farcaster for ZABAL/Empire Builder)
+ Include <CAMPAIGN-URL> as a visible link in the asset OR the post body

Craft
+ Clarity - you get what it is in 3 seconds
+ On-brand energy - reads like <CAMPAIGN> not generic crypto
+ Vertical or square format for mobile-native scroll
+ Captions if there is audio
+ <CAMPAIGN> wordmark or logo visible somewhere readable
+ A short intro / context line in the post body (not just a drop)
+ Shareability - the kind of asset someone would forward without being asked

Substance
+ One clear takeaway about why <CAMPAIGN> matters (<KEY-BENEFITS>)
+ Names a real beat from the event - <SPECIFIC TIMECODES OR MOMENTS>
+ Speaks to the right viewer - <AUDIENCE-PERSONA> - not a generic "join us" pitch

Bonus angles (rare, big multiplier)
+ <BONUS-1: novel framing>
+ <BONUS-2: rare quote / B-roll / motion>
+ <BONUS-3: cross-format playability>


THE ASSET KIT (use any of this, CC-BY)

Pre-cleared brand kit (full folder):
https://bettercallzaal.com/assets/<campaign-brand>/

Direct download links:
- <LIST 5-8 KEY ASSETS WITH DIRECT URLs>

Live source page:
<CAMPAIGN-URL>

Repo + every document:
<CAMPAIGN-REPO-URL>

Farcaster channel:
https://farcaster.xyz/~/channel/<channel>

Canonical bounty bar:
https://poidhz.com/best-practices

CC-BY 4.0. Remix freely. Just keep "<CAMPAIGN>" or "<CAMPAIGN-URL>" visible somewhere in your final piece.


THE REWARD

Best <ARTIFACT> wins <PRIZE> ETH on Base. Winner clip becomes <CAMPAIGN>'s pinned promo across @bettercallzaal channels.

Every submitter earns $ZABAL automatically via the slot 8 leaderboard on Empire Builder. Drop scales by how many BCZ POIDH bounties you have entered total - submit to all rounds and your score compounds. <PRIOR-ROUNDS-NOTE>.

Track live: https://www.empirebuilder.world/empire/0xbb48f19b0494ff7c1fe5dc2032aeee14312f0b07
Submitter leaderboard hub: https://poidhz.com/hub

This is an OPEN bounty - the pot grows in real time if others stack contributions.


DEADLINE

Submissions close 11:59pm PT, <DAY-OF-WEEK> <DATE>.
Winner cast by end of day <DAY-OF-WEEK + 1> <DATE + 1>.

Site: <CAMPAIGN-URL>
