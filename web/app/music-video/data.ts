// The poidh bounty, once Zaal casts it. The button renders only when this is set.
export const BOUNTY_URL = '';

export const SONG_MP3 = 'https://github.com/bettercallzaal/poidhz/releases/download/bettercallzaal-song-mp3/IMan-Afrikah-BetterCallZaal.mp3';
export const SONG_AUDIUS = 'https://audius.co/thezaodao/bettercallzaal-by-iman-afrikah';

// Sections of the song, read from a machine transcript of the mp3 (whisper, 2026-11-03). Times are approximate.
export const SONG_MAP: [string, string, string][] = [
  ['0:00 to 0:04', 'Intro', '"This is... Zaal"'],
  ['0:04 to 0:16', 'Hook', '"Got a big build on your mind, better call Zaal"'],
  ['0:16 to 0:28', 'Verse', '"Turn the vision to a route, from Maine to Africa"'],
  ['0:28 to 0:41', 'Hook', '"Got a problem, better call Zaal. Need connections"'],
  ['0:41 to 0:51', 'Bridge', '"WaveWarZ, hear the sound... ecosystem gather round"'],
  ['0:51 to 1:05', 'Verse', '"Working through the night, RIT engineer, robotics project"'],
  ['1:05 to 1:14', 'Hook', '"Need a launch, need a team, for anything"'],
  ['1:14 to 1:28', 'Verse', '"Open source repos all day long, builder, connector, putting people on"'],
  ['1:28 to 1:41', 'Hook', '"Community leader with a style, need it done right with a smile"'],
  ['1:41 to 2:00', 'Verse', '"Making things connect... hundred meetings, hundred plans"'],
  ['2:00 to 2:05', 'Hook', '"Better call Zaal, that\'s for real"'],
  ['2:05 to 2:22', 'Outro', '"This is... Zaal"'],
];

export type Source = { href: string; label: string; note: string };

export const IRL: Source[] = [
  { href: 'https://drive.google.com/drive/folders/1SNKFMJBxIEs5lZG4dAcEy4gJb6CLZXbg', label: 'ZAOstock raw footage (Google Drive)', note: 'Drone, time-lapse and stage footage from ZAOstock, 3 October 2026, Ellsworth, Maine.' },
  { href: 'https://www.twitch.tv/zaofestivals', label: 'ZAOstock livestream (Twitch)', note: 'The festival stream and its highlights.' },
  { href: 'https://www.twitch.tv/videos/2888849470', label: 'Live on Star 97.7 (Twitch)', note: 'Zaal in the radio studio, the full stream.' },
  { href: 'https://zaostock.com', label: 'zaostock.com', note: 'The festival site.' },
];

export const ONLINE: Source[] = [
  { href: 'https://www.youtube.com/@bettercallzaal', label: 'YouTube, @bettercallzaal', note: 'BCZ YapZ interviews, ZAO MIXZ streams, BCZ POV and builds. Horizontal.' },
  { href: 'https://www.youtube.com/watch?v=IFG_34K7Vig', label: 'BCZ YapZ Episode 19 with Kenny from POIDH', note: 'A good one for the poidh credit.' },
  { href: 'https://www.twitch.tv/bettercallzaal', label: 'Twitch, bettercallzaal', note: 'Live streams. Past broadcasts only stay up for about a week, so grab what you need early.' },
  { href: 'https://x.com/bettercallzaal', label: 'X, @bettercallzaal', note: 'Posts, clips and photos.' },
  { href: 'https://farcaster.xyz/zaal', label: 'Farcaster, @zaal', note: 'Casts, clips and photos.' },
  { href: 'https://thezao.com', label: 'thezao.com', note: 'The ZAO, the community around Zaal.' },
];

