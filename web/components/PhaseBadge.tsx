import type { Phase } from '@/lib/types';
const TEXT: Record<Phase, string> = { open: 'Open', 'awaiting-pick': 'Closed, awaiting pick', won: 'Winner picked', canceled: 'Canceled', closed: 'Closed' };
export function PhaseBadge({ phase }: { phase: Phase }) {
  // Open is the one state to act on, so it gets poidh's filled red; the rest stay outlined.
  if (phase === 'open') return <span className="whitespace-nowrap rounded bg-[var(--accent)] px-2 py-0.5 text-xs font-semibold text-[var(--on-accent)]">{TEXT[phase]}</span>;
  const color = phase === 'awaiting-pick' ? 'var(--warn)' : 'var(--muted)';
  return <span className="whitespace-nowrap rounded border px-2 py-0.5 text-xs font-semibold" style={{ borderColor: color, color }}>{TEXT[phase]}</span>;
}
