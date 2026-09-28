import type { Note } from './types';
export function notesFrom(files: { round: { bounty_id: number }; entrants: any[] }[]): Map<number, Note> {
  const m = new Map<number, Note>();
  for (const f of files) for (const e of f.entrants ?? []) {
    const claim = Number(e.claim);
    if (!Number.isFinite(claim)) continue;
    m.set(claim, { claim, handle: e.handle, headline: e.headline ?? '', did_well: e.did_well ?? '', items: e.items ?? [], bounty_id: Number(f.round.bounty_id) });
  }
  return m;
}
