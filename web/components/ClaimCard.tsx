import Link from 'next/link';
import type { Claim, Note } from '@/lib/types';
import { shortAddr } from '@/lib/format';

const firstUrl = (s: string) => s.match(/https?:\/\/[^\s)]+/)?.[0] ?? null;

export function ClaimCard({ c, note, won, personKey }: { c: Claim; note?: Note; won: boolean; personKey: string }) {
  const link = firstUrl(c.description);
  return (
    <article className="rounded-lg border border-[var(--line)] p-4">
      {c.image_url && <img src={c.image_url} alt="" className="mb-3 max-h-64 w-full rounded object-cover" loading="lazy" />}
      <div className="flex flex-wrap items-baseline gap-2 text-sm">
        <Link href={`/u/${encodeURIComponent(personKey)}`} className="font-semibold">{c.handle ? `@${c.handle}` : personKey.startsWith('0x') ? shortAddr(personKey) : `@${personKey}`}</Link>
        <span className="text-[var(--muted)]">claim {c.claim_id}</span>
        {won && <span className="font-semibold text-[var(--accent)]">Winner</span>}
      </div>
      <h3 className="mt-1 font-medium">{c.title}</h3>
      {link && <a href={link} className="mt-1 block break-all text-sm">{link}</a>}
      {note && (
        <details className="mt-3 text-sm">
          <summary className="cursor-pointer font-medium">Notes: {note.headline}</summary>
          <p className="mt-2">{note.did_well}</p>
          {note.items.map((i) => <p key={i.title} className="mt-2"><strong>{i.title}.</strong> {i.body}</p>)}
        </details>
      )}
    </article>
  );
}
