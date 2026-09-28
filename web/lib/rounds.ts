import type { Phase, Round } from './types';
export function roundPhase(r: Round, now: Date): Phase {
  if (r.status === 'CANCELED') return 'canceled';
  if (r.winner || r.status === 'WINNER SET') return 'won';
  if (r.closes_at && new Date(r.closes_at).getTime() <= now.getTime()) return 'awaiting-pick';
  return 'open';
}
export const publicRounds = (rs: Round[]) => rs.filter((r) => typeof r.bounty_id === 'number');
