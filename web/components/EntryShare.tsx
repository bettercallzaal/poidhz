'use client';
import { useState } from 'react';
import { composeEntryPost } from '@/lib/share';

type Hints = { link?: string; about?: string };

export function EntryShare({ title, boardUrl, channel, hints }: { title: string; boardUrl: string; channel: string; hints?: Hints }) {
  const [claim, setClaim] = useState('');
  const [link, setLink] = useState('');
  const [about, setAbout] = useState('');
  const [copied, setCopied] = useState(false);
  const p = composeEntryPost({ title, boardUrl, channel, claim, link, about });
  const field = 'mt-1 w-full rounded border border-[var(--line)] bg-transparent px-3 py-2 text-sm';
  const btn = 'rounded px-3 py-2 text-sm font-semibold no-underline';
  return (
    <section className="mt-8 rounded-lg border border-[var(--line)] p-4">
      <h2 className="text-xl font-semibold">Tell everyone about your entry</h2>
      <p className="mt-1 text-sm text-[var(--muted)]">After you claim on poidh, post the details where people can see and reply. It goes out under your own name, in /{channel} on Farcaster or on X. Nothing is stored here.</p>
      <label className="mt-3 block text-sm">Your poidh claim number (optional)<input className={field} value={claim} onChange={(e) => setClaim(e.target.value)} placeholder="8400" /></label>
      <label className="mt-3 block text-sm">{hints?.link ?? 'Link to your work'}<input className={field} value={link} onChange={(e) => setLink(e.target.value)} placeholder="https://" /></label>
      <label className="mt-3 block text-sm">{hints?.about ?? 'A few lines about it'}<textarea className={field} rows={4} value={about} onChange={(e) => setAbout(e.target.value)} /></label>
      {p.ready && <pre className="mt-3 whitespace-pre-wrap rounded bg-[var(--line)]/40 p-3 text-sm">{p.text}</pre>}
      <div className="mt-3 flex flex-wrap gap-2">
        <a aria-disabled={!p.ready} className={`${btn} bg-[var(--accent)] text-[var(--on-accent)] ${p.ready ? '' : 'pointer-events-none opacity-40'}`} href={p.farcasterUrl} target="_blank" rel="noopener">Post in /{channel}</a>
        <a aria-disabled={!p.ready} className={`${btn} border border-[var(--line)] ${p.ready ? '' : 'pointer-events-none opacity-40'}`} href={p.xUrl} target="_blank" rel="noopener">Post on X</a>
        <button type="button" disabled={!p.ready} className={`${btn} border border-[var(--line)] disabled:opacity-40`} onClick={async () => { await navigator.clipboard.writeText(p.text); setCopied(true); }}>{copied ? 'Copied' : 'Copy text'}</button>
      </div>
    </section>
  );
}
