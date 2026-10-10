<!-- NOT-ANNOUNCEMENT-COPY: a DM draft, unsent. Names no deadline anyone submits to. -->
# Note to Hurricane - DRAFT, NOT SENT, HELD

**Zaal sends it, or does not.** Written 2026-10-10 after he ruled (item 111) that round ten's sign-up emails go
to Hurricane's database. hurric4n3ike builds WaveZStation; the page that collects the sign-ups is on poidhz.com
(PR #247) and forwards each one to an endpoint he provides. Nothing is kept on our side.

## The DM (about 180 words)

```
Hurricane, Zaal. I am running a round for artists on WaveZStation: best marketing rollout for one song over a month, $500 pot on poidh, and I buy $500 of the winner's song. Artists sign up on poidhz.com with their email and their song link. I want the sign-ups in your database, not ours.

What I need from you, whenever you have a minute:

1. A POST endpoint that takes one JSON row: {round, email, artist, song_id, song_link, handle, where, recorded_at}, with a bearer token you give me. One row per song_id; answer 409 if the song is already in. Answer {ok: true, count: N} on success.
2. Optional: GET the same URL with ?round=10 returning {count: N}, so the page can show how many are in. Never names or emails.
3. Your word on two things I have already told entrants: the emails are used to reach them about this round and for nothing else, and they are deleted when the round closes out (mid-November). Also, who on your side can read the table.

The page is built and does nothing until the endpoint is set. Sign-up closes Oct 18, so the sooner the better, but it waits for you.
```

## What it does not say

- No request for data back beyond a count. The emails are his to hold; we read nothing.
- No promise of anything to WaveZStation beyond the round itself.
- No deadline on him. If the endpoint is late, the cast waits (`PLAN.md`, "What could go wrong").
