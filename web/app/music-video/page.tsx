import type { Metadata } from 'next';
import { BOUNTY_URL, IRL, ONLINE, SONG_AUDIUS, SONG_MAP, SONG_MP3, type Source } from './data';

export const metadata: Metadata = {
  title: 'BetterCallZaal music video - poidhz',
  description: 'Footage guide and song map for the BetterCallZaal music video bounty. Cut real footage and photos of Zaal and The ZAO to IMan Afrikah\'s song.',
};

function SourceList({ items }: { items: Source[] }) {
  return (
    <ul className="mt-2 max-w-2xl list-disc space-y-2 pl-5">
      {items.map((s) => (
        <li key={s.href}><a href={s.href} target="_blank" rel="noopener">{s.label}</a>. {s.note}</li>
      ))}
    </ul>
  );
}

export default function MusicVideo() {
  return (
    <>
      <h1 className="mt-6 text-3xl font-bold tracking-tight">Make a part of the BetterCallZaal music video</h1>
      <p className="mt-3 max-w-2xl">IMan Afrikah made a song called BetterCallZaal, and we are making the music video together. Pick a part of the song, cut real footage and photos of Zaal and The ZAO to it, and enter it on the poidh bounty. The best parts get stitched into the final video.</p>
      <p className="mt-3 max-w-2xl">This page is the footage guide. I&apos;ll try and update this page as much as I can with more info on more places to find footage.</p>
      {BOUNTY_URL && <p className="mt-3"><a href={BOUNTY_URL} target="_blank" rel="noopener" className="inline-block rounded-lg bg-[var(--accent)] px-4 py-2 font-semibold text-[var(--on-accent)] no-underline">Enter on the poidh bounty</a></p>}

      <h2 className="mt-8 text-xl font-semibold">The song</h2>
      <p className="mt-2 max-w-2xl"><a href={SONG_MP3}>Download the mp3</a> (2:22) or <a href={SONG_AUDIUS} target="_blank" rel="noopener">listen on Audius</a>. Use it as it is: no remix, no speed change, no other music on top.</p>

      <h2 className="mt-8 text-xl font-semibold">Song map</h2>
      <p className="mt-2 max-w-2xl">Pick a section and match the footage to the line. Parts of the song nobody else has covered stand out. Times are approximate, so check them against the song.</p>
      <div className="mt-3 max-w-2xl overflow-x-auto">
        <table className="w-full text-sm">
          <thead><tr className="text-left text-[var(--muted)]"><th className="py-1 pr-3">Time</th><th className="py-1 pr-3">Part</th><th className="py-1">Line</th></tr></thead>
          <tbody>
            {SONG_MAP.map(([time, part, line]) => (
              <tr key={time} className="border-t border-[var(--line)]"><td className="whitespace-nowrap py-1 pr-3">{time}</td><td className="py-1 pr-3">{part}</td><td className="py-1">{line}</td></tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2 className="mt-8 text-xl font-semibold">Where to find footage: IRL</h2>
      <p className="mt-2 max-w-2xl">The best material is IRL: Zaal and the people around him out doing things, at events, on stage, building, hanging out. Photos count too.</p>
      <SourceList items={IRL} />

      <h2 className="mt-8 text-xl font-semibold">Where to find footage: online</h2>
      <SourceList items={ONLINE} />

      <h2 className="mt-8 text-xl font-semibold">Format</h2>
      <ul className="mt-2 max-w-2xl list-disc space-y-1 pl-5">
        <li>Horizontal, 1920x1080 (16:9), 30 fps, MP4 (H.264). Vertical footage is fine, reframed to fill the horizontal frame.</li>
        <li>Any length, up to the whole song. The song is the only audio.</li>
        <li>Real footage and photos only. No AI-generated footage, no face swaps, no voice clones.</li>
      </ul>

      <p className="mt-8 max-w-2xl">Need a shot that does not exist yet, or know a place with footage that is not on this list? Say so in the <a href="https://discord.thezao.com" target="_blank" rel="noopener">Discord</a>.</p>
    </>
  );
}
