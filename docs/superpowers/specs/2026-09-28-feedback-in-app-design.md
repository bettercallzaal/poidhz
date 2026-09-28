<!-- NOT-ANNOUNCEMENT-COPY: internal design spec. Names no deadline anyone submits to. -->
# Feedback on submissions, in the app - design (DRAFT, awaiting Zaal)

Zaal, 2026-09-28: *"lets give great feedback through the app on peoples poidh submissions"*.

**Status: draft on a default.** The one open decision, who writes the notes, was filed for the
grill at 14:4x EDT because the picker could not open. This spec assumes the recommended answer.
Nothing here is built until Zaal approves it.

| decision | default taken | alternatives filed |
|---|---|---|
| who writes | **Claude drafts, Zaal edits and publishes** | Zaal writes every note; community writes too; AI plus community |

## What "great feedback" means here, from the repo, not from taste

`docs/feedback-that-recruits.md` (Zaal, 2026-09-22) already set it: the goal is a working
relationship with two or three people, not grading. Every note takes its four-line shape:

1. **The capability the piece proves**, named as a capability, not a property of the image.
2. **One transferable skill**, phrased so it applies to the next twelve pieces.
3. **Where they stand with Zaal**, a relationship statement, never a rank.
4. **A question they can answer.**

Two tiers. **Everyone** gets lines 1 and 2 plus the next close. **The few Zaal picks** get all
four lines plus the offer: price comes from them, and the retainer-versus-pot eligibility trade
is stated up front.

And the notes the programme already ships are **measured, not described**: "25.6 seconds,
1080x1920, every fact on every frame". A draft that has not looked at the work is not a draft.

## Hard rules the app enforces, not just asks for

Each is a check that blocks Publish, with the reason shown:

- **No ranking and no superlatives** ("best", "most complete", "top", "first place", ordinal
  placings). Doc 2536 decision 4; Zaal 2026-09-22.
- **No distribution promises** ("we'll repost", "pin", "share on our channels"). Broken five
  rounds running per `docs/PROMISE-AUDIT.md`.
- **No budget named first** in an offer note.
- **Line 4 must end in a question mark.**
- **Every entrant in the field at the close has a published note** before the round is marked
  done. This is the existing `check-feedback-promises.py` gate, now fed from the app.

## Flow

1. **A claim lands.** The 6-hourly cron already sees it. A drafting job gathers the brief (the
   bounty text), the claim, and **measurements of the work**:
   - video: duration, frame size, audio, and sampled frames through ffmpeg
   - image: dimensions
   - PR: diff stats and CI state through `gh`
   - post: its reach, where readable
   Measuring needs ffmpeg and gh, so the job runs where those exist (GitHub Actions or the
   lane), not in a Vercel function.
2. **Claude drafts** the note in the four-line shape from the brief plus the measurements, and
   stores it as `draft` with the measurements attached. It never invents a measurement: a fact
   it could not read is written as UNKNOWN in the evidence panel.
3. **Zaal reviews in the app.** `/admin/feedback`, signed in with Farcaster, FID 19640 only.
   - One card per claim: the work embedded, the measurements, and the draft in an editor.
   - The rule checks run live.
   - A toggle adds the offer lines for the few.
   - Publish is one tap.
4. **Published** notes appear on `/b/<id>`, `/u/<person>` and `/feedback/<bounty>/<handle>`,
   the page the bounty text already promises.
5. **The entrant hears about it.** When Zaal presses "Tell them", the app casts a reply from
   his account under their claim post in /zao. It uses his Neynar signer, and he fires it, never
   the app on its own. Later, a mini-app notification goes to entrants who added the app.
6. **They can answer.** Line 4 is a question, and replies land in the Farcaster thread shown on
   the bounty page.

## Data

`notes` in Supabase, replacing hand-edited `data/feedback/*.json`. The existing files are
imported once, and the app writes the JSON back so the Python gates keep working unchanged.

| field | |
|---|---|
| claim_id, bounty_id, handle | the claim this is about |
| capability, skill, standing, question | the four lines |
| offer | nullable; the offer lines when toggled |
| measurements | JSON of what was measured, with UNKNOWN where it could not be |
| status | draft, published |
| drafted_by, edited_by, published_at | provenance |
| told_cast_hash | the reply cast, once Zaal fires it |

## Needs from Zaal

- **The answer to the grill question.** Everything above assumes the default.
- Through `/secret`: a Neynar API key and client id, a Supabase project, and an Anthropic API
  key for the drafting job.

## Out of scope

- Community feedback, unless the grill answer says otherwise.
- Changing any live round's promises.
