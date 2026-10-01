# ZAOstock audio for poidh rounds

Transcripts and notes for audio that a poidh round links. The audio itself lives in the
ZAOstock brand kit at `https://zaostock.com/brand` (owned by the zaostock lane), which is
durable and already live; a second 15 MB copy in this repo was dropped from PR #225 once that
was measured.

## The 1 October session: https://zaostock.com/brand/audio/zaostock-radio-update-2026-10-01.mp3

- **Where it is:** ZAODEVZ/ZAOstock #424, merged 2026-10-01 09:42 EDT, listed first in the
  kit's RADIO list as "Zaal on Star 97.7, 1 October 2026". Byte-identical to the Downloads
  file below (sha256 `c77cbeba70e8d53b405d18c743d475ea75aee3da9ea4bc3fb7f11a854ac501f6`).
  Returns 200 `audio/mpeg`, 15,174,008 bytes, with range requests honoured.

- **What:** Zaal live in the Star 97.7 studio with hosts Paul and Mike, the morning of
  Thursday 1 October 2026, two days before ZAOstock. Two segments, the second after a station
  break. The station IDs itself on air at 2:35 ("More next on Star 97.7") and Zaal thanks
  Star 97.7 by name as a partner at 5:43.
- **Source:** Zaal's own recording, saved to `~/Downloads/Zaostock Update 10-1.mp3` at 09:26
  on 2026-10-01. The full stream of the
  slot is the Twitch VOD <https://www.twitch.tv/videos/2888849470> ("Live on Star 97.7",
  bettercallzaal, started 08:00:02 EDT, 32 min 49 s).
- **Measured with ffprobe:** 379.35 s (6 min 19 s), mp3, 320 kbps, 44.1 kHz stereo, 15,174,008
  bytes. Speech ends at about 6:17.
- **Transcript:** `zaostock-radio-session-2026-10-01.srt`, machine transcript (mlx_whisper,
  large-v3-turbo), timestamps good, spellings NOT corrected: it writes "Zal" and "Zoll" for
  Zaal and "Zalstock" for ZAOstock. Use it for cut points and caption timing, then fix the
  names against <https://zaostock.com/artists>.
- **Rights:** Zaal's interview, recorded by him, offered by him for cutting (his words to the
  seat, 1 Oct: "use my radio sesh and make something i can post to instagram"). Credit Star
  97.7 in anything cut from it.

## Cut points worth knowing (mm:ss, from the srt)

| From | To | What is said |
|---|---|---|
| 0:00 | 0:10 | "Special guest in our studio, Zaal is back" / "ZAOstock is coming" |
| 0:59 | 1:06 | eight acts, free, all day, noon to 6 |
| 1:07 | 1:31 | the after party moves inside to Black Moon Public House at 6 |
| 2:29 | 2:38 | host: downtown Ellsworth, this Saturday, 12 noon, "more next on Star 97.7" |
| 2:44 | 2:56 | host: Franklin Street Parklet at noon Saturday, "somebody said better call Zaal, so we did" |
| 3:02 | 4:37 | the whole lineup in running order, all eight acts |
| 4:37 | 4:41 | "And it's all free." "Exactly. All free." |
| 5:22 | 5:35 | "free to attend, no ticket, no gate", support the artists at zaostock.com |
| 5:43 | 6:15 | thanks to Star 97.7 and the other partners, "come join us on Saturday" |
