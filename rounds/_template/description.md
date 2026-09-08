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

**Known-bad numbers, measured by the wwtracker lane 2026-09-07. Do not carry these forward.**

**This table is enforced, not advisory.** `scripts/precast-check.py` blocks a cast on any of
these appearing between the paste sentinels in a round's `description.md`. It was verified
against R5's live text, which it blocks on two counts - a bounty description is immutable
once cast, so the check has to happen before, not after.

**Adding a row here without a matching pattern now fails the selftest.** The two cannot
drift apart: `precast-check --selftest` parses this table and asserts every row is caught by
a `KNOWN_BAD` pattern. Asking the next person to keep them in step was honor-system, and
honor-system rules run at 3-40% here against ~100% for enforced ones - so it is checked
rather than requested. If you add a row, add the pattern, and the selftest will tell you if
you forgot.

| Do not use | Why |
|---|---|
| "13.9 SOL to artists as of Aug 20" | right number, wrong date - see above |
| "458 SOL volume as of 2026-05-25" | **superseded May figure. Its own source says so.** Use `wavewarz/974-wavewarz-financials-snapshot-2026-07`: **878.316 SOL volume, 13.3918 SOL artist payouts, validated 2026-07-23.** |
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

**How that error actually travelled, because the mechanism is the lesson.** The source
document had it right twice - a table row said "artist share of the trade fee, at 1.005%",
and the sentence below the headline carried the full 1.500% and the 67/33 split. The wrong
compression was the part in **bold**. The bold line is the part that gets read, quoted and
relayed, so a correct body under a compressed headline still propagates the headline. When
you write a figure into a bounty, the shortest form of it is the one that will travel: make
that form the true one, or do not put a short form in at all.

It was caught by opening the generator to cite its path and reading `FEE = 0.015` and
`ARTIST_SHARE = 0.67` on the way past - not by re-reading anyone's prose. That is the
argument for regenerating rather than copying, in one line.

## Resolve the doc number. Cite the slug. Open the document.

Three steps, and skipping the third is the worst of the failures on this page.

**"458 SOL is about 11% high" was itself wrong** - not the instruction, the reason. The
figure is not a bad number caught by measurement. It is a **superseded May figure whose own
source already says not to use it.** `wavewarz/743-wavewarz-whitepaper-v2-deep-dive` carries
this at the top, added 2026-08-09, three weeks before anyone here touched it:

> "This doc contains TWO different sets of headline figures... the 458 figure is the May
> number, and the 878.30 figure is July... **Use doc 974 for any current figure. Do not copy
> Key Decision 1's numbers.** A public brand page copied them on 2026-08-09 and had to be
> corrected."

The warning was stronger than ours, named the replacement, and recorded that a public page
had already made this exact mistake once. **Nobody had opened the document.** The conclusion
was reconstructed from a chain scan and relayed twice before someone read the source.

**A bare doc number is what let that happen.** It looks like a citation and identifies
nothing: 218 numbers in the research library resolve to more than one document, and `743`
names a WaveWarZ whitepaper *and* a cold-outreach workflow. Resolve with
`zao-research-health --resolve <n>`, cite `topic/NNNN-slug`, and then actually open it.

**One more thing that document settles.** The volume spread is not one bad number - it is
four figures for the same period from four methodologies (410.97 chain-measured, 403.90 from
the volume series, 458 from the Intelligence dashboard, 472.71 from another library doc),
which 743 already attributes to test-battle exclusion and counting method. It is a
definitional disagreement about what counts as a battle, and describing it as an error
misrepresents it.

And the "1.53% artist payout rate" on the do-not-carry list above traces to here: `974`
computes 1.52% as cumulative payouts divided by cumulative volume. That is a ratio between
two lifetime totals, not a rate applied to a trade, and it moves whenever either total moves.

**Generate the artist line, do not copy it.** The correct string above is right today; the
generator is right always. Run
`python3 tools/artist-earnings.py --census census.json --trades trades.json` in
`wavewarz-protocol`. It reports by leg - artist share of the trade fee, plus the 5% winner
and 2% loser settlement bonuses - and labels which legs are measured versus inherited.

**Re-measure before every cast, and put a re-check date next to anything time-bound.**
These figures move. A number that was right in August is not right in October, and a bounty
runs for weeks after you paste it.

**Re-check the figures on this page by 2026-10-08.** The 974 snapshot is validated
2026-07-23 and was already six weeks old when it was cited here; the chain-derived artist
line was measured 2026-09-07. Neither is wrong today and neither stays right. A claim about
an external service, a programme or a cycle with no re-check date is the defect this whole
page is about, so this page carries one. The wwtracker lane hit
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
