import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import { extractDraft, isHeading, linkParts } from '@/lib/draft';

// Built once per deploy from rounds/daily/<round>/description.md, the same file that gets cast.
export const dynamic = 'force-static';
export const dynamicParams = false;
const DIR = join(process.cwd(), 'public', 'rounds', 'daily');

async function load(round: string) {
  if (!/^d\d+$/.test(round)) return null;
  try { return extractDraft(await readFile(join(DIR, round, 'description.md'), 'utf8')); } catch { return null; }
}

export async function generateStaticParams() {
  const out: { round: string }[] = [];
  for (const d of await readdir(DIR)) if (await load(d)) out.push({ round: d });
  return out;
}

export async function generateMetadata({ params }: { params: Promise<{ round: string }> }): Promise<Metadata> {
  const d = await load((await params).round);
  if (!d) return {};
  const lead = d.body.split('\n').filter((l) => l.trim())[1] ?? '';
  const description = (d.cast ? '' : 'Draft for review, not live yet. ') + lead.slice(0, 160);
  return { title: `${d.title} - poidhz`, description, robots: { index: false, follow: false }, openGraph: { title: d.title, description } };
}

export default async function DraftPage({ params }: { params: Promise<{ round: string }> }) {
  const d = await load((await params).round);
  if (!d) notFound();
  const blocks = d.body.split(/\n\s*\n/).map((b) => b.trim()).filter(Boolean);
  return (
    <article className="mt-6">
      {!d.cast && <p className="rounded border border-[var(--warn)] px-3 py-2 text-sm text-[var(--warn)]">Draft for review. This bounty is not live on poidh yet, and the text can still change.</p>}
      <h1 className="mt-4 text-3xl font-bold tracking-tight">{d.title}</h1>
      <div className="mt-4 space-y-4 text-[15px] leading-relaxed">
        {blocks.map((b, i) => isHeading(b)
          ? <h2 key={i} className="pt-4 text-lg font-bold">{b}</h2>
          : <p key={i} className="whitespace-pre-wrap">{linkParts(b).map((p, j) => p.href ? <a key={j} href={p.href} target="_blank" rel="noopener" className="break-all">{p.text}</a> : <span key={j}>{p.text}</span>)}</p>)}
      </div>
    </article>
  );
}
