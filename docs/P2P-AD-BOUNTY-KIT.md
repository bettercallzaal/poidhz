# The P2P Ad Bounty Kit

A reusable, org-agnostic template for running a peer-to-peer advertising campaign as a
POIDH bounty instead of paying for ads. Real people make real ads for your brand,
compete on a public rubric, and the best one becomes your official promo - all for the
price of one bounty (typically $20-40 in ETH on Base).

This is not theory. It is the exact structure that produced BCZ's two highest-quality
rounds (R2, R3 - `rounds/r2/`, `rounds/r3/`), extracted here so any org can run the same
playbook without re-deriving it. If you are BCZ/ZABAL Gamez, use
`docs/how-to-draft-next-bounty.md` instead - that doc has your org's specific wallet,
channels, and voice baked in. This doc is the pattern underneath it, stripped of BCZ
specifics, for anyone forking `zpoidh` or just borrowing the idea.

## Why this works (the mechanism, not just the vibe)

A bounty is not a job posting - it is a standing public prize with no cap on entrants.
That changes the economics of "getting an ad made":

- **You pay once for the best submission, not per attempt.** A traditional freelance ad
  costs money whether it's good or not. A bounty only pays out on the winner; everyone
  else's effort was free R&D you get to look at.
- **Distribution is baked into the entry requirement, not bolted on after.** THE BAR (below)
  makes "post it publicly and tag us" a condition of a valid submission, not an optional
  ask. Every entrant is already promoting you the moment they submit - whether or not
  they win.
- **A public rubric turns judgment into content.** Publishing scorecards (see
  `rounds/r2/judging.html`) is itself shareable, builds trust that judging isn't rigged,
  and gives losers a reason to try again next round instead of walking away.
- **Open bounties let anyone add to the pot.** POIDH's OPEN bounty type lets other
  people/orgs co-fund your bounty in public. A credible early submission or a name-brand
  co-funder can catalyze a wave of entries (see `docs/how-to-draft-next-bounty.md` step 7,
  the "catalytic contributor DM" pattern - this mirrors Jesse Pollak's own real-world use
  of POIDH bounty 906).
- **A secondary reward rail keeps low-effort entrants engaged too.** BCZ layered a
  same-org token leaderboard (Empire Builder / $ZABAL) on top of the ETH prize so every
  submitter earns *something*, not just the winner. This is optional - swap in whatever
  your org's own reward rail is (a role, a token, a raffle entry, nothing at all) - but it
  measurably increased repeat submitters across R1->R2->R3 (BCZ's own submitters compounded
  a score across rounds; see `rounds/r3/description.md` line 86).

## The five-part structure (fill in the blanks)

Every winning BCZ round description used the same five sections, in this order. Do not
reorder them - THE BAR has to come before THE RUBRIC or entrants skip the floor checks.

### 1. THE BAR (floor requirements - binary pass/fail, no partial credit)

3-5 numbered rules. Anything that fails THE BAR is disqualified regardless of how good the
submission is creatively - this is what makes judging fast and defensible.

Always include:
- The deliverable itself (format, if you're gating one - or "any format" if you're not)
- A public-post + tag requirement (this is the distribution mechanism - do not skip it)
- A submission-location requirement (post the public URL on the bounty page itself)
- An audio/asset-quality rule if applicable to your medium (BCZ's rule: no random library
  music or melodic pads over spoken dialog - a specific, checkable rule beats "make it
  sound good")

Template:
```
THE BAR (do these or you are not in the running)

1. Make a[n] <deliverable> for <your org/campaign> in <format or "any format">.
2. Tag <@your-org-handle> on <primary platform> when you post it publicly.
3. Cross-post the same <deliverable> in <your community's home channel> so <your community> sees it.
4. Submit the public URL on this bounty page.
5. <medium-specific quality rule, phrased as a checkable binary, not a vibe>
```

### 2. THE RUBRIC (weighted extras - more boxes ticked = stronger judging weight)

Grouped into 3-4 categories. BCZ used Distribution / Craft / Substance / Bonus - keep this
grouping unless your medium genuinely needs a different split. Each line is a `+` a judge
can literally check off while scoring - specific and observable, never "good vibes."

- **Distribution**: extra platforms, extra tags (especially tagging *other* accounts whose
  audience you want - a co-founder, a partner project, an investor with reach), a visible
  link to your site/page
- **Craft**: clarity in N seconds, on-brand tone, format fit for the platform, captions,
  logo/wordmark visibility, shareability
- **Substance**: one clear takeaway about why your thing matters, names a real specific
  beat/fact (not generic hype), speaks to a named audience segment rather than "everyone"
- **Bonus** (rare, big multiplier): the angle that makes a submission genuinely
  exceptional - a testimonial pull-quote, real footage of the actual product/event, an
  unusual format that still lands the message

### 3. THE ASSET KIT (make it a one-click job, not a scavenger hunt)

- One folder URL with everything (logo, palette doc, an official audio track if relevant,
  a phrases/voice doc, a glossary of correct handles/spellings)
- 5-8 **direct download links**, not just the folder - entrants copy-paste, they don't dig
- A link to your live source page/site for editors who want to lift real copy/footage
- License clarity: CC-BY (remix freely) with one condition (e.g. "keep our name/URL visible
  somewhere in the final piece") is the BCZ default - pick whatever your org is comfortable
  giving away
- **Ship the kit BEFORE you cast the bounty.** A folder URL with nothing in it (or without
  an `index.html` if your host doesn't auto-list directories - see the Vercel gotcha in
  `docs/how-to-draft-next-bounty.md`) kills the bounty on arrival.

### 4. THE REWARD

- State the prize plainly (amount + chain) and what happens to the winning piece (do you
  actually run it as your promo? say so - "we run it" is a real incentive, not just cash)
- If you're running a secondary reward rail (see "Why this works" above), state the
  mechanism plainly and make clear it applies to *every* submitter, not just the winner
- State the bounty type: OPEN (lets others co-fund publicly, contributor-vote decides the
  winner, slower but grows in real time) vs SOLO (you fund + accept directly, faster,
  no vote)

### 5. DEADLINE

- Exact date + time + timezone. Double-check the day-of-week matches the date before you
  post - a real bug BCZ hit in R3 (a Saturday/Sunday mismatch a community member caught
  before cast). Verify with:
  ```bash
  python3 -c "import datetime; print(datetime.date(YYYY,MM,DD).strftime('%A'))"
  ```
- State when you'll announce the winner, not just when submissions close - a stated
  judging SLA (BCZ default: within 48h of close) keeps the bounty from going quiet after
  the deadline, which is exactly the kind of thing that erodes trust for your *next* round.

## Judging without drama

Publish a scorecard, don't just announce a winner. `rounds/r2/judging.html` +
`rounds/r2/judging.json` is the reference implementation: per-submission BAR pass/fail,
RUBRIC score breakdown, pros/cons, and the final verdict, all public. This is cheap to
build (a static JSON + one HTML template) and expensive to fake - which is the point. A
public rubric is what lets you floor-fail an entry without an argument: the rule was
public, the check is binary, the submission didn't clear it.

## What NOT to skip (lessons paid for in real rounds)

- Don't gate format unless you have a specific reason to (BCZ's R2 video-only gate
  produced fewer, more homogeneous entries than R3's any-format gate)
- Don't publish the brand kit folder without an index page if your host needs one
- Don't let the judging window drift past your stated SLA - it's the single fastest way
  to make future rounds feel low-stakes
- Don't reuse a handle/spelling without checking it against your own brand glossary first
  (BCZ's R2 round shipped with a wrong handle in the description; entrants caught it and
  tagged the correct one anyway, but it was a visible unforced error)
- Don't skip the audio/quality rule in THE BAR if your medium has an obvious failure mode -
  make the rule specific enough that a judge doesn't have to argue about it

## Adapting this for a partner org

This kit assumes you already have: a wallet that can sign a POIDH bounty (EOA, not a smart
wallet - POIDH reverts smart-wallet bounty creation), a home community channel to post in,
and *something* worth defending as a brand asset. If a partner org wants to run this and
doesn't have POIDH tooling of their own yet, `zpoidh`'s `org.config.json` (see
`docs/PARTNER-GUIDE.md`) is built exactly for that - fork the repo, edit one config file,
and the calendar/dashboard/leaderboard tooling in this repo works for their bounties
instead of BCZ's.

## Reference implementations in this repo

| Round | What it proved | Files |
|---|---|---|
| R2 | Format-gated (45-60s video), first public scorecard | `rounds/r2/` |
| R3 | Any-format, full 5-part structure above, public brand kit | `rounds/r3/` |

## Also see

- `docs/how-to-draft-next-bounty.md` - BCZ's own step-by-step playbook (this doc's
  concrete, org-specific sibling)
- `docs/bounty-best-practices.html` - the canonical bar as a public page entrants can be
  linked to directly
- `docs/PARTNER-GUIDE.md` - forking this repo's tooling for your own org
