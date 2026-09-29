// Turns an entrant's details into a post they send themselves. No backend: the post lives on
// Farcaster or X under their own name, which is where the conversation belongs anyway.
export type EntryInput = { title: string; boardUrl: string; channel: string; claim: string; link: string; about: string };

const httpOnly = (s: string) => (/^https?:\/\/\S+$/i.test(s.trim()) ? s.trim() : '');

export function composeEntryPost(i: EntryInput) {
  const claim = i.claim.trim().replace(/^#/, '');
  const link = httpOnly(i.link);
  const about = i.about.trim();
  const lines = [`My entry for ${i.title}${claim ? ` (claim ${claim})` : ''}`, link, about].filter(Boolean);
  const text = lines.join('\n\n');
  const fc = new URL('https://farcaster.xyz/~/compose');
  fc.searchParams.set('text', text);
  fc.searchParams.set('channelKey', i.channel);
  fc.searchParams.append('embeds[]', i.boardUrl);
  const x = new URL('https://x.com/intent/post');
  x.searchParams.set('text', text);
  x.searchParams.set('url', i.boardUrl);
  return { text, farcasterUrl: fc.toString(), xUrl: x.toString(), ready: Boolean(link || about) };
}
