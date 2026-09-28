import type { Phase } from '@/lib/types';
const TEXT: Record<Phase, string> = { open: 'Open', 'awaiting-pick': 'Closed, awaiting pick', won: 'Winner picked', canceled: 'Canceled' };
export function PhaseBadge({ phase }: { phase: Phase }) {
  const color = phase === 'open' ? 'var(--accent)' : phase === 'awaiting-pick' ? 'var(--warn)' : 'var(--muted)';
  return <span className="rounded border px-2 py-0.5 text-xs font-semibold" style={{ borderColor: color, color }}>{TEXT[phase]}</span>;
}
